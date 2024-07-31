# ----------------------------------------------------------------------- #
# DO NOT TRY TO CHANGE THE CODE OTHERWISE YOU WILL FACE CONSEQUENCES
# ----------------------------------------------------------------------- #
# This is the final version of app.py and api testing is based on this.
from sqlalchemy import Column, Integer, String, ForeignKey
from flask import Flask, request, jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
from datetime import datetime
import os
import re
import markdown
from flask_misaka import Misaka
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
from urllib.parse import parse_qs, urlparse
import json
from sqlalchemy.types import TypeDecorator, TEXT
from sqlalchemy.orm import relationship
from tenacity import retry, stop_after_attempt, wait_fixed
from google.generativeai import GenerationConfig
import subprocess
import logging


app = Flask(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'backend/instance/se1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for all routes
Misaka(app)
# Configure the Google Gemini API

api_key = 'AIzaSyC6www5ebwMC2Mpvb0WnZCzgPwzxMO4j-g'
genai.configure(api_key=api_key)

app.secret_key = 'your_secret_key'


model2 = genai.GenerativeModel(model_name="gemini-1.5-flash", tools = "code_execution")

class JSONEncodedText(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    student_weekly_performances = relationship("StudentWeeklyPerformance", back_populates="user")
    student_questions = relationship("StudentQuestion", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'), nullable=False)
    audio = db.Column(db.Integer, nullable=True)
    video = db.Column(db.Integer, nullable=True)
    content = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='ratings')
    lesson = relationship("Lesson", back_populates="ratings")


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(Integer, primary_key=True)
    course_name = db.Column(String, nullable=False)
    course_desc = db.Column(String)

    lessons = db.relationship("Lesson", back_populates="course")
    student_weekly_performances = db.relationship("StudentWeeklyPerformance", back_populates="course")


class Week(db.Model):
    __tablename__ = 'weeks'
    id = db.Column(db.Integer, primary_key=True)
    week_no = db.Column(db.Integer, nullable=False)
    week_start_date = db.Column(db.DateTime, nullable=False)
    week_end_date = db.Column(db.DateTime, nullable=False)

    lessons = db.relationship("Lesson", back_populates="week")
    student_weekly_performances = db.relationship("StudentWeeklyPerformance", back_populates="week")


class Lesson(db.Model):
    __tablename__ = 'lessons'
    lesson_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
    lesson_topic = db.Column(db.Text, nullable=True)
    lecture_video_url = db.Column(db.Text, nullable=True)

    course = relationship("Course", back_populates="lessons")
    week = relationship("Week", back_populates="lessons")
    questions = relationship("Question", back_populates="lesson", lazy=True)
    ratings = relationship("Rating", back_populates="lesson")

    def __init__(self, course_id=None, week_id=None, lesson_topic=None, lecture_video_url=None):
        self.course_id = course_id
        self.week_id = week_id
        self.lesson_topic = lesson_topic
        self.lecture_video_url = lecture_video_url
    

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id'), nullable=False)
    question_type_aq_pm_pp_gp_gq = db.Column(db.Text, nullable=False)
    question = db.Column(db.Text, nullable=False)
    question_type_mcq_msq = db.Column(db.Text, nullable=True)
    option_1 = db.Column(db.Text, nullable=True)
    option_2 = db.Column(db.Text, nullable=True)
    option_3 = db.Column(db.Text, nullable=True)
    option_4 = db.Column(db.Text, nullable=True)
    correct_option = db.Column(JSONEncodedText, nullable=True)
    efficient_code = db.Column(db.Text, nullable=True)
    marks = db.Column(db.Integer, nullable=True)

    lesson = db.relationship("Lesson", back_populates="questions")
    student_questions = db.relationship("StudentQuestion", back_populates="question")

    def __init__(self, lesson_id, question_type_aq_pm_pp_gp_gq=None, question=None,
                 question_type_mcq_msq=None, option_1=None, option_2=None, option_3=None,
                 option_4=None, correct_option=None, efficient_code=None):
        self.lesson_id = lesson_id
        self.question_type_aq_pm_pp_gp_gq = question_type_aq_pm_pp_gp_gq
        self.question = question
        self.question_type_mcq_msq = question_type_mcq_msq
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.correct_option = correct_option
        self.efficient_code=efficient_code
        self.marks = 3 if self.question_type_mcq_msq == 'MCQ' else 5


class StudentQuestion(db.Model):
    __tablename__ = 'student_questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    programming_code = db.Column(db.String(255), nullable=True)

    question = db.relationship("Question", back_populates="student_questions")
    user = db.relationship("User", back_populates="student_questions")

    def __init__(self, user_id, question_id, is_correct, programming_code):
        self.user_id = user_id
        self.question_id = question_id
        self.is_correct = is_correct
        self.programming_code = programming_code


class StudentWeeklyPerformance(db.Model):
    __tablename__ = 'student_weekly_performances'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    aq_score = db.Column(db.Numeric)
    pm_score = db.Column(db.Numeric)
    pp_score = db.Column(db.Numeric)
    gp_score = db.Column(db.Numeric)
    gq_score = db.Column(db.Numeric)
    overall_ai_score = db.Column(db.Numeric)
    ai_report_pdf_url = db.Column(db.String)

    user = relationship("User", back_populates="student_weekly_performances")
    week = relationship("Week", back_populates="student_weekly_performances")
    course = relationship("Course", back_populates="student_weekly_performances")


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Check for admin credentials
    if email == 'admin@gmail.com' and password == 'admin123':
        return jsonify({'message': 'Admin login successful', 'is_admin': True}), 200
    
    # Regular user login
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Login successful', 'is_admin': False}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.get_json()
#     user_message = data.get('message')
#     try:
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         response = model.generate_content(user_message)
#         bot_response = response.text
#         formatted_response = ' '.join(bot_response.split())
#         return jsonify({'response': formatted_response}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/api/submit_rating', methods=['POST'])
def submit_rating():
    data = request.get_json()
    user_id = data.get('user_id')
    audio = data.get('audio')
    video = data.get('video')
    content = data.get('content')
    feedback = data.get('feedback')
    lesson_id = data.get('lesson_id')

    new_rating = Rating(user_id=user_id,lesson_id = lesson_id, audio=audio, video=video, content=content, feedback=feedback)
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({'message': 'Rating submitted successfully'}), 201    

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    ratings = Rating.query.all()
    rating_list = [{
        'id': rating.id,
        'user_id': rating.user_id,
        'audio': rating.audio,
        'video': rating.video,
        'content': rating.content,
        'feedback': rating.feedback,
        'created_at': rating.created_at
    } for rating in ratings]
    return jsonify(rating_list), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        "created_at": user.created_at
    } for user in users]
    return jsonify(user_list), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


# @app.route('/api/sentiment_analysis', methods=['GET'])
# def sentiment_analysis():
#     try:
#         ratings = Rating.query.all()
#         feedback_list = [rating.feedback for rating in ratings if rating.feedback]
        
#         sentiments = []
#         for feedback in feedback_list:
#             prompt = f"""Tell me whether the following sentence's sentiment is positive or negative or something in between.
#             Sentence {feedback}
#             Sentiment"""
#             response = genai.generate_text(
#                 model='models/text-bison-001',
#                 temperature=0.5,
#                 candidate_count=1,
#                 top_k=40,
#                 top_p=0.95,
#                 max_output_tokens=1024,
#                 prompt=prompt
#             )
#             sentiment = response.result.strip().split('\n')[-1].strip()  # Extract sentiment
#             sentiments.append({
#                 'feedback': feedback,
#                 'sentiment': sentiment
#             })

#         return jsonify(sentiments), 200
#     except Exception as e:
#         print(f"Error: {e}")  # Log the error to the console
#         return jsonify({'error': str(e)}), 500

# Add your code here Anuj,

# Add your code here Asmita,


def get_explanation(question, correct_answer):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f'You are a teacher, you have to give step-by-step solution of the {question} whose correct answer is {correct_answer}. Explanation:'
    explanation = model.generate_content(prompt)
    explanation_html = markdown.markdown(explanation.text)
    return explanation_html
#____________________Activity Quiz________________________________
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@app.route('/api/activity/quiz/<int:lesson_id>', methods=['GET', 'POST'])
def activity_quiz(lesson_id):
    questions = Question.query.filter_by(lesson_id=lesson_id, question_type_aq_pm_pp_gp_gq='AQ').all()
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found."}), 404
    if not questions:
        return jsonify({"error": "No Questions found in this lesson."}), 404

    quiz_data = [
        {
            'question_id': q.question_id,
            'question': q.question,
            'options': [q.option_1, q.option_2, q.option_3, q.option_4],
            'correct': q.correct_option if q.question_type_mcq_msq == 'MSQ' else q.correct_option[0],
            'type': q.question_type_mcq_msq,
            'marks': q.marks,
            'topic': lesson.lesson_topic
        } for q in questions
    ]

    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        user_answers = data.get('answers', {})
        results = []
        total_score = 0
        max_score = sum([q['marks'] for q in quiz_data])

        for idx, question in enumerate(quiz_data):
            user_answer = user_answers.get(str(idx),"null")
            if question['type'] == 'MSQ' and user_answer:
                user_answer = set(user_answer)
            is_correct = user_answer == question['correct']
            score = question['marks'] if is_correct else 0
            total_score += score

            try:
                if not is_correct:
                    explanation = get_explanation(question['question'], question['correct'])

                else:
                    explanation = None
            except Exception as e:
                return jsonify({'error': f'Error generating activity question"s explanation: {e}'}),400

            existing_response = StudentQuestion.query.filter_by(user_id=user_id,question_id=question['question_id']).first()
            if existing_response:
                # Update the existing response
                existing_response.is_correct = is_correct
            else:
                # Create a new response
                student_response = StudentQuestion(user_id=user_id,question_id=question['question_id'], is_correct=is_correct,programming_code=None)
                db.session.add(student_response)
                db.session.commit()
                
            results.append({
                'question': question['question'],
                'correct_answer': question['correct'],
                'user_answer': list(user_answer) if isinstance(user_answer, set) else user_answer,
                'is_correct': is_correct,
                'score': score,
                'explanation': explanation
            })

        return jsonify({
            'results': results,
            'total_score': total_score,
            'max_score': max_score,
            'score_percentage': (total_score / max_score) * 100
        })

    return jsonify(quiz_data)

def parse_generated_question(response_text, question_type, topic):
    # This function should parse the response_text and return a dictionary matching the schema
    try:
        generated_question = json.loads(response_text)
        generated_question['type'] = question_type
        generated_question['topic'] = topic
        return generated_question
    except json.JSONDecodeError:
        print("Error parsing the generated question")
        return None

def generate_new_question(lesson_id):
    questions = Question.query.filter_by(lesson_id=lesson_id).all()

    quiz_data = [
        {
            'question': q.question,
            'options': [q.option_1, q.option_2, q.option_3, q.option_4],
            'correct': q.correct_option if q.question_type_mcq_msq == 'MSQ' else q.correct_option[0],
            'type': q.question_type_mcq_msq,
            'marks': q.marks,
            'topic': q.lesson.lesson_topic
        } for q in questions if q.question_type_aq_pm_pp_gp_gq == 'AQ'
    
    ]
    new_questions = []
    model = genai.GenerativeModel('gemini-pro')

    json_schema = {
        "title": "MCQ or MSQ Question Schema",
        "description": "Schema for representing a question that can be either multiple-choice (MCQ) or multiple-select (MSQ)",
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "description": "Type of question",
                "enum": ["MCQ", "MSQ"]
            }
        },
        "required": ["type"],
        "oneOf": [
            {
                "if": {
                    "properties": { "type": { "const": "mcq" } }
                },
                "then": {
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The text of the question"
                        },
                        "options": {
                            "type": "array",
                            "description": "List of answer options",
                            "items": {
                                "type": "string"
                            }
                        },
                        "correct": {
                            "type": "string",
                            "description": "The correct answer"
                        },
                        "marks": {
                            "type": "integer",
                            "description": "Marks awarded for the correct answer",
                            "const": 3
                        },
                        "topic": {
                            "type": "string",
                            "description": "Topic of the question"
                        }
                    },
                    "required": ["question", "options", "correct", "marks", "topic"]
                }
            },
            {
                "if": {
                    "properties": { "type": { "const": "msq" } }
                },
                "then": {
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The text of the question"
                        },
                        "options": {
                            "type": "array",
                            "description": "List of answer options",
                            "items": {
                                "type": "string"
                            }
                        },
                        "correct": {
                            "type": "array",
                            "description": "List of correct answers",
                            "items": {
                                "type": "string"
                            }
                        },
                        "marks": {
                            "type": "integer",
                            "description": "Marks awarded for the correct answers",
                            "const": 5
                        },
                        "topic": {
                            "type": "string",
                            "description": "Topic of the question"
                        }
                    },
                    "required": ["question", "options", "correct", "marks", "topic"]
                }
            }
        ]
    }

    for question_data in quiz_data:
        topic = question_data['topic']
        question_type = question_data['type']
        prompt = (
            f"Generate a new question based on the following topic and type:\n"
            f"Topic: {topic}\n"
            f"Type: {question_type}\n"
            f"Follow JSON schema.<JSONSchema>{json.dumps(json_schema)}</JSONSchema>"
        )

        response = model.generate_content(prompt)
        response_text = response.candidates[0].content.parts[0].text
        new_question = parse_generated_question(response_text, question_type, topic)
        if new_question is not None:
            new_questions.append(new_question)
    return new_questions
#new_questions = generate_new_question(quiz_data)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@app.route('/api/activity/extra_questions/<int:lesson_id>', methods=['GET', 'POST'])
def new_quiz(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    if request.method == 'GET':
        try:
            session['new_quiz_data'] = generate_new_question(lesson_id)
            return jsonify({'new_quiz_data': list(enumerate(session['new_quiz_data']))})
        except Exception as e:
            return jsonify({'error': f'Error generating extra questions: {e}'}),400
    
    if request.method == 'POST':
        print(session)
        if 'new_quiz_data' not in session:
            return jsonify({'error': 'Quiz data not found. Please start a new quiz.'}), 400

        data = request.get_json()
        user_answers = data.get('answers', {})
        results = []
        total_score = 0
        max_score = sum([q['marks'] for q in session['new_quiz_data']])

        for idx, question in enumerate(session['new_quiz_data']):
            user_answer = user_answers.get(str(idx),"did not understand")
            correct_answer = question['correct']
            is_correct = user_answer == correct_answer if question['type'] == 'MCQ' else set(user_answer) == set(correct_answer)

            if is_correct:
                total_score += question['marks']

            result = {
                'question': question['question'],
                'options': question['options'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': ""
            }
            try:
                if not is_correct:
                    explanation = get_explanation(question['question'], correct_answer)
                    result['explanation'] = explanation
            except Exception as e:
                    return jsonify({'error': f'Error generating extra question"s explanation: {e}'}),400

            results.append(result)

        return jsonify({
            'results': results,
            'total_score': total_score,
            'max_score': max_score
        })
    session.pop('new_quiz_data', None)

#______________________Graded Assignment________________________

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@app.route('/api/graded/quiz/<int:week_id>', methods=['GET', 'POST'])
def quiz(week_id):
    lesson_ids = [lesson.lesson_id for lesson in Lesson.query.with_entities(Lesson.lesson_id).filter_by(week_id=week_id).all()]
    if not lesson_ids:
        return jsonify({"error": "No lesson  in this week."}), 400
    
    questions = Question.query.filter(Question.lesson_id.in_(lesson_ids)).all()
    if not questions:
        return jsonify({"error": "No questions  for this week."}), 400
    quiz_data = [
        {
            'question_id':q.question_id,
            'question': q.question,
            'options': [q.option_1, q.option_2, q.option_3, q.option_4],
            'correct': q.correct_option if q.question_type_mcq_msq == 'MSQ' else q.correct_option[0],
            'type': q.question_type_mcq_msq,
            'marks': q.marks,
            'topic': q.lesson.lesson_topic
        } for q in questions if q.question_type_aq_pm_pp_gp_gq == 'GQ' 
    ]

    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        user_answers = data.get('answers', {})
        results = []
        total_score = 0
        max_score = sum([q['marks'] for q in quiz_data])

        for idx, question in enumerate(quiz_data):
            user_answer = user_answers.get(str(idx),"null")
            if question['type'] == 'MSQ' and user_answer:
                user_answer = set(user_answer)
            correct_answer = question['correct']
            is_correct = (user_answer == correct_answer) if question['type'] == 'MCQ' else (set(user_answer) == set(correct_answer))
            if is_correct:
                total_score += question['marks']
            result = {
                'question': question['question'],
                'options': question['options'],
                'user_answer': list(user_answer) if isinstance(user_answer, set) else user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': ""
            }

            existing_response = StudentQuestion.query.filter_by(user_id = user_id, question_id=question['question_id']).first()
            if existing_response:
                # Update the existing response
                existing_response.is_correct = is_correct
            else:
                # Create a new response
                student_response = StudentQuestion(user_id = user_id, question_id=question['question_id'], is_correct=is_correct,programming_code=None)
                db.session.add(student_response)
                db.session.commit()
            try:
                if not is_correct:
                    explanation = get_explanation(question['question'], correct_answer)
                    result['explanation'] = explanation
                results.append(result)
            except Exception as e:
                return jsonify({'error': f'Error generating graded question"s explanation: {e}'}),400
        db.session.commit()
        return jsonify({
            'results': results,
            'score': total_score,
            'max_score': max_score
        })

    return jsonify({'quiz_data': list(enumerate(quiz_data))})

#_______________________AI Transcriptor-Notes__________
def extract_video_id(video_url):
    query = urlparse(video_url).query
    params = parse_qs(query)
    return params.get('v', [None])[0]

def extract_transcript_details(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            transcript = transcript_list.find_generated_transcript(['de', 'en'])
        except NoTranscriptFound:
            transcript = transcript_list.find_manually_created_transcript(['de', 'en'])
        transcript = transcript.fetch()
        transcript_text = '\n'.join([f"{int(entry['start'] // 60)}:{int(entry['start'] % 60):02d} - {int((entry['start'] + entry['duration']) // 60)}:{int((entry['start'] + entry['duration']) % 60):02d}: {entry['text']}" for entry in transcript])
        return transcript, transcript_text
    except Exception as e:
        return None, f"Error extracting transcript: {e}"

prompt = "You are a YouTube video note taker. You will be taking the transcript text and making notes highlighting the important points in a student-friendly manner. The transcript text is as follows:"

def generate_gemini_content(transcript_text):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        return f"Error generating notes: {e}"
    
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))

@app.route('/api/transcript_notes/<int:lesson_id>', methods=['GET'])
def process_video(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found."}), 404
    
    video_url = lesson.lecture_video_url  # Extract the video URL from the lesson object
    if not video_url:
        return jsonify({"error": "Video URL not found for the given lesson."}), 404
    
    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL."}), 400
    
    transcript, transcript_text = extract_transcript_details(video_id)
    if transcript_text.startswith("Error"):
        return jsonify({"error": transcript_text}), 400
    
    notes_md = generate_gemini_content(transcript_text)
    notes_html = Misaka().render(notes_md)

    prompt_topics = "You are a YouTube video note taker. Extract important topics from the notes. Start the content with the heading '## Topics discussed'. Use markdown format."
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt_topics + transcript_text)
    
        important_topics_md = response.text
        important_topics_html = Misaka().render(important_topics_md)
    except Exception as e:
        return jsonify({'error': f'Error generating notes: {e}'}),400   
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    video_embed = f'<iframe id="videoPlayer" width="560" height="315" src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    
    return jsonify({
        "video_embed": video_embed,
        "transcript_text": transcript_text,
        "notes": notes_html,
        "important_topics": important_topics_html
    })

@app.route('/api/lessons', methods=['POST'])
def create_lesson():
    data = request.get_json()
    new_lesson = Lesson(
        course_id=data['course_id'],
        week_id=data['week_id'],
        lesson_topic=data.get('lesson_topic'),
        lecture_video_url=data.get('lecture_video_url')
    )
    db.session.add(new_lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson created successfully', 'lesson_id': new_lesson.lesson_id}), 200

@app.route('/api/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    correct_option = data.get('correct_option')

    # Convert correct_option to a list if it's not already a list (to handle MSQ)
    if isinstance(correct_option, str):
        correct_option = [correct_option]

    new_question = Question(
        lesson_id=data['lesson_id'],
        question_type_aq_pm_pp_gp_gq=data.get('question_type_aq_pm_pp_gp_gq'),
        question=data.get('question'),
        question_type_mcq_msq=data.get('question_type_mcq_msq'),
        option_1=data.get('option_1'),
        option_2=data.get('option_2'),
        option_3=data.get('option_3'),
        option_4=data.get('option_4'),
        correct_option=correct_option,
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'message': 'Question created successfully', 'question_id': new_question.question_id}), 200


# Add your code here Yadvendra

# =================== Student Weekly Performance Analysis ================================

def generate_swot_analysis(student_performance, lesson_topics, correct_attempts, incorrect_attempts):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=genai.GenerationConfig(response_mime_type="application/json"))
    required_response_schema = {
        "title": "SWOT Analysis Schema",
        "description": "Schema for representing a comprehensive SWOT analysis",
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "The ID of the user"
            },
            "week_no": {
                "type": "integer",
                "description": "The week number for the analysis"
            },
            "performance": {
                "type": "object",
                "description": "Performance metrics of the user",
                "properties": {
                    "aq_score": {
                        "type": "integer",
                        "description": "Score in Assessment Questions"
                    },
                    "pm_score": {
                        "type": "integer",
                        "description": "Score in Performance Questions"
                    },
                    "pp_score": {
                        "type": "integer",
                        "description": "Score in Programming Problems"
                    },
                    "gp_score": {
                        "type": "integer",
                        "description": "Score in” General Programming Problems"
                    },
                    "gq_score": {
                        "type": "integer",
                        "description": "Score in General Questions"
                    },
                    "overall_ai_score": {
                        "type": "number",
                        "description": "Overall AI calculated score"
                    }
                },
                "required": ["aq_score", "pm_score", "pp_score", "gp_score", "gq_score", "overall_ai_score"]
            },
            "swot_analysis": {
                "type": "object",
                "description": "SWOT analysis generated by AI",
                "properties": {
                    "strengths": {
                        "type": "array",
                        "description": "List of strengths identified in the SWOT analysis",
                        "items": {
                            "type": "string"
                        }
                    },
                    "weaknesses": {
                        "type": "array",
                        "description": "List of weaknesses identified in the SWOT analysis",
                        "items": {
                            "type": "string"
                        }
                    },
                    "opportunities": {
                        "type": "array",
                        "description": "List of opportunities identified in the SWOT analysis",
                        "items": {
                            "type": "string"
                        }
                    },
                    "threats": {
                        "type": "array",
                        "description": "List of threats identified in the SWOT analysis",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["strengths", "weaknesses", "opportunities", "threats"]
            }
        },
        "required": ["user_id", "week_no", "performance", "swot_analysis"]
    }

    prompt = f"""
        Analyze the following student performance data and provide a SWOT Analysis.
        For Topics: {", ".join(lesson_topics)}\n

        **Performance Data:**
        AQ Score: {student_performance['aq_score']}
        PM Score: {student_performance['pm_score']}
        PP Score: {student_performance['pp_score']}
        GP Score: {student_performance['gp_score']}
        GQ Score: {student_performance['gq_score']}
        Overall AI Score: {student_performance['overall_ai_score']}

        **Correct Attempted Questions:**
        {';'.join(correct_attempts)}

        **Incorrect Attempted Questions:**
        {"; ".join(incorrect_attempts)}
        
        Follow the JSON schema.<JSONSchema>{json.dumps(required_response_schema)}</JSONSchema>
        
        Don't Give Anything Else other than this.
        """

    response = model.generate_content(prompt)
    response_text = response.candidates[0].content.parts[0].text
    return response_text


@app.route("/api/weekly_performance_analysis", methods=['POST'])
def get_weekly_performance():
    data = request.json
    user_id = data['user_id']
    week_no = data['week_no']
    

    # week = Week.query.filter_by(week_no=week_no).first()
    # if week is None:
    #     return jsonify({"error": "Week not Found!"}), 404

    # week_id = week.id

    lessons = Lesson.query.filter_by(week_id=week_no).all()
    #course = Course.query.filter_by(id=lessons[0].course.id).first()
    lesson_topics = [lesson.lesson_topic for lesson in lessons]

    questions = Question.query.filter(Question.lesson_id.in_([lesson.lesson_id for lesson in lessons])).all()

    if not questions:
        return jsonify({"error": "No Questions found for this week"}), 404

    student_answers = StudentQuestion.query\
        .filter(StudentQuestion.question_id.in_([q.question_id for q in questions]))\
        .filter_by(user_id=user_id).all()

    if not student_answers:
        return jsonify({"error": "Student Didn't Submitted the Answers for this week"}), 404

    correct_attempted_ques = []
    incorrect_attempted_ques = []

    total_questions = len(questions)
    scores = {
        'aq_score': 0,
        'pm_score': 0,
        'pp_score': 0,
        'gp_score': 0,
        'gq_score': 0,
    }
    total_marks = 0

    for answer in student_answers:
        question = Question.query.filter_by(question_id=answer.question_id).first()
        if question:
            if answer.is_correct:
                if question.question_type_aq_pm_pp_gp_gq == "AQ":
                    scores['aq_score'] += question.marks
                elif question.question_type_aq_pm_pp_gp_gq == "PM":
                    scores['pm_score'] += question.marks
                elif question.question_type_aq_pm_pp_gp_gq == "PP":
                    scores['pp_score'] += question.marks
                elif question.question_type_aq_pm_pp_gp_gq == "GP":
                    scores['gp_score'] += question.marks
                elif question.question_type_aq_pm_pp_gp_gq == "GQ":
                    scores['gq_score'] += question.marks

                correct_attempted_ques.append(question.question)
            else:
                incorrect_attempted_ques.append(question.question)
            total_marks += question.marks

    obtained_score = (scores['aq_score'] + scores['pm_score'] + scores['pp_score'] +
                      scores['gp_score'] + scores['gq_score'])
    overall_ai_score = obtained_score / total_marks if total_marks != 0 else 0

    # print(scores)
    # print(overall_ai_score)
    swot_analysis_json = generate_swot_analysis({
        'aq_score': scores['aq_score'],
        'pm_score': scores['pm_score'],
        'pp_score': scores['pp_score'],
        'gp_score': scores['gp_score'],
        'gq_score': scores['gq_score'],
        'overall_ai_score': overall_ai_score
    }, lesson_topics, correct_attempted_ques, incorrect_attempted_ques)
    # print(swot_analysis_json)
    swot_analysis = json.loads(swot_analysis_json)
    performance = StudentWeeklyPerformance(
        user_id=user_id,
        week_id=week_no,
        course_id=1,
        aq_score=scores['aq_score'],
        pm_score=scores['pm_score'],
        pp_score=scores['pp_score'],
        gp_score=scores['gp_score'],
        gq_score=scores['gq_score'],
        overall_ai_score=overall_ai_score,
        ai_report_pdf_url = "Use swot analysis" 
    )

    db.session.add(performance)
    db.session.commit()

    return swot_analysis, 200

# ============================ Feedback Sentiment Analysis ==========================


def generate_feedback_summary(lessons_feedbacks):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=genai.GenerationConfig(response_mime_type="application/json"))
    req_response_schema = {
        "title": "Lecture Feedback Summary Schema",
        "description": "Schema for AI-generated feedback summaries for lectures.",
        "type": "object",
        "properties": {
            "lecture_feedback_summaries": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "lesson_id": {
                            "type": "string",
                            "description": "Unique identifier for the lecture."
                        },
                        "sentiment": {
                            "type": "number",
                            "description": "Sentiment score for the lecture feedback, ranging from 0 to 1."
                        },
                        "feedback_summary": {
                            "type": "string",
                            "description": "Summarized feedback provided by the AI for the lecture."
                        },
                        "suggestions": {
                            "type": "string",
                            "description": "AI-generated suggestions for improvement based on feedback."
                        }
                    },
                    "required": ["lesson_id", "sentiment", "average_sentiment", "feedback_summary"]
                }
            }
        },
        "required": ["lecture_feedback_summaries"],
    }

    prompt = f"""
            You are an AI language model tasked with analyzing student feedback for online lectures. 
            The feedback includes ratings for audio, video, and content quality, along with written comments. 
            Based on this data, you will provide a sentiment analysis, summarize the feedback, and 
            suggest improvements for each lecture.

            Here is the feedback data:"""

    for lesson_id, feedback_list in lessons_feedbacks.items():
        prompt += f"\n1. **Lecture ID**: {lesson_id}\n   - **Feedbacks**:\n"
        for feedback in feedback_list:
            prompt += f"     - \"{feedback}\"\n"

    prompt += f"""**Instructions**: 
    1. For each lecture, analyze the feedback comments and ratings. Provide an  sentiment score between 0 and 1
    2. Summarize the key points from the feedback.
    3. Provide suggestions for improvement based on the feedback.
    
    Here is the output format:
    Follow the JSON schema.<JSONSchema>{json.dumps(req_response_schema)}</JSONSchema>
    """

    # print(prompt)

    response = model.generate_content(prompt)
    response_text = response.candidates[0].content.parts[0].text
    return response_text


@app.route("/api/sentiment_analysis", methods=['POST'])
def sentiment_analysis():
    ratings = Rating.query.all()
    lessons_feedback = {}
    # print(ratings)

    for rating in ratings:
        lesson_id = rating.lesson_id
        feedback = rating.feedback
        # print(lesson_id)

        if lesson_id not in lessons_feedback:
            lessons_feedback[lesson_id] = []

        if feedback:
            lessons_feedback[lesson_id].append(feedback)

    analysis_results = []

    # print(lessons_feedback)

    f_summary = generate_feedback_summary(lessons_feedback)
    feedback_summary = json.loads(f_summary)
    # print(feedback_summary)

    return feedback_summary, 200


# =========================== Contextual ChatBot API ==============================

conversations = {}


@app.route("/init", methods=['POST'])
def init_session():
    session_id = str(len(conversations) + 1)
    conversations[session_id] = []
    print(f"Total sessions: {len(conversations)}")
    return jsonify({
        "message": "Session Initialized",
        "session_id": session_id}), 200


@app.route("/api/chat", methods=['POST'])
def chat_ai():
    session_id = request.json.get("session_id")
    user_message = request.json.get("message")

    generation_config = GenerationConfig(
        temperature=0.1,
        top_p=0.95,
        top_k=64,
        max_output_tokens=500,
        response_mime_type="text/plain"
    )

    chat_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="""
        You should behave like a mentor or tutor or teacher for python programming.
        You are also helpful assistant in solving programming question. 
        Explain terms that are understandable.
        Use real world examples and add humor to make conversation interesting and engaging.
        Ask questions, so that you can better understand the student.
        """
    )

    if session_id not in conversations:
        conversations[session_id] = []

    conversation_history = conversations[session_id]

    chat_session = chat_model.start_chat(
        history=conversation_history
    )

    response = chat_session.send_message(user_message)

    model_response = response.text
    # print(model_response)

    conversation_history.append({"role": "user", "parts": [user_message]})
    conversation_history.append({"role": "model", "parts": [model_response]})
    conversations[session_id] = conversation_history

    return jsonify({"response": model_response}), 200



@app.route('/api/compile', methods=['POST'])
def compile_code():
    code = request.json.get("code")
    public_test_cases = request.json.get("public_test_cases")
    test_code = request.json.get("test_code")
    print(code)
    print(public_test_cases)
    print(test_code)
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    
    if not public_test_cases:
        return jsonify({'error': 'Test cases are required'}), 400
    
    response = subprocess.run(['python', '-c', code], capture_output=True, text=True)

    if response.stderr:
        return jsonify({'error': response.stderr}), 500

    results = []
    for test_case in public_test_cases:
        input_value = test_case['input']
        expected_output = test_case['expected_output']
        prompt = f"Compile and check the python code and detect and show all the possible syntax errors present in the code and if not then execute this code {code} against the test case {input_value} and return the result."
        
        try:
            response = model2.generate_content(prompt)
            actual_output = response.candidates[0].content.parts[2].code_execution_result.output
            print(type(actual_output))
            print(type(expected_output))
            print(expected_output)
            print(actual_output)
            results.append({
                'input': input_value,
                'expected_output': expected_output,
                'actual_output': actual_output,
                'passed': str(actual_output.strip()) == str(expected_output)
            })
        except Exception as e:
            results.append({
                'input': input_value,
                'expected_output': expected_output,
                'actual_output': str(e),
                'passed': False
            })

    return jsonify({'results': results})

@app.route('/api/submit', methods=['POST'])
def submit():
    code = request.json.get('code')
    language = request.json.get('language')
    private_test_cases = request.json.get('private_test_cases')
    #question = request.json.get('question')
    user_id = request.json.get('user_id')
    question_id = request.json.get('question_id')
    score = 0
    for test in private_test_cases:
        input_value = test['input']
        expected_output = test['expected_output']
        prompt = f"Compile and check the python code and detect and show all the possible syntax errors present in the code and if not then execute this code {code} written in the languate{language} against the test case {input_value} and return the result."
        try:
            response = model2.generate_content(prompt)
            actual_output = response.candidates[0].content.parts[2].code_execution_result.output
            print(type(actual_output))
            print(type(expected_output))
            print(expected_output)
            print(actual_output)
             
            if (str(expected_output) == str(actual_output.strip())):
                score = score + 1
            else:
                print("test case failed ")

        except Exception as e:  
            logging.error(f"Error running test: {str(e)}")
            return jsonify({'error': str(e)}), 500

    if score == len(private_test_cases):
        try:
            # Add the student's code to the StudentQuestion table
            student_submission = StudentQuestion(
                user_id = user_id,
                question_id = question_id,
                is_correct = 1,
                programming_code = code,      
            )
            db.session.add(student_submission)
            db.session.commit()
            return jsonify({'score': score, 'message': 'Code submitted successfully!'}), 200
        
        except Exception as e:
            logging.error(f"Error saving submission: {str(e)}")
            return jsonify({'error': 'Failed to save submission'}), 500

    return jsonify({'score': score, 'message': 'Some test cases failed'}), 200

@app.route('/api/explainCode', methods=['POST'])
def get_hint():
    code = request.json.get('code')
    language = request.json.get('language')
    question = request.json.get('question')
    prompt = f'''I have the following code snippet in {language} for the question \n\n{question}\n. Can you provide a hint or suggestion for improving or debugging it?\n\n{code}\n'''
    
    try:
        result = model2.generate_content(prompt)
        htmlContent = markdown.markdown(result.text)
        return jsonify({'hint': htmlContent})
    except Exception as e:
        logging.error(f"Error generating hint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/getEfficientCode', methods=['POST'])
def getCode():
    data = request.json
    question_id = data.get('question_id')

    if not question_id:
        return jsonify({"error": "question_id is required"}), 400

    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404
    
    question_statement = question.question
    #efficient_code = question.Efficient_code
    efficient_code = ""
    print(efficient_code)
    if efficient_code:
        return jsonify({"efficient_code": efficient_code}), 200
    
    else:
        prompt = f"Please write the efficient Python code with the best time and space complexity for the question: {question_statement}."
        
        try:
            # Assuming `model.generate_content` returns the desired content.
            response = model2.generate_content(prompt, tools="code_execution")
            best_code = response.text
            
            # Save the best code to the database
            question.Efficient_code = best_code
            db.session.commit()
            return jsonify({"efficient_code": best_code}), 200
        
        except Exception as e:
            # Log the error (for debugging purposes) and handle the exception
            print(f"Error generating code: {e}")
            return jsonify({"error": "Error generating efficient code"}), 500


# =============================== Sample Data =============================

def generate_sample_data():
    user1 = User(username="user123", email="user1@gmail.com", password="pass123")
    user2 = User(username="user321", email="user2@gmail.com", password="pass321")

    course = Course(course_name="Python Programming",
                    course_desc="""
                            Learn basic programming concepts such as variables, expressions, loops, 
                            conditionals and functions in Python.
                            Creating, manipulating, and using more Python specific 
                            features such as lists, tuples, and dictionaries""")

    week1 = Week(week_no=1, week_start_date=datetime(2023, 7, 1), week_end_date=datetime(2023, 7, 7))
    week2 = Week(week_no=2, week_start_date=datetime(2023, 7, 8), week_end_date=datetime(2023, 7, 14))

    lesson1_week1 = Lesson(course_id=1, week_id=1,
                           lesson_topic="Variables and Data Types",
                           lecture_video_url="http://example.com/variables")
    lesson2_week1 = Lesson(course_id=1, week_id=1,
                           lesson_topic="Conditional Statements",
                           lecture_video_url="http://example.com/conditions")

    lesson1_week2 = Lesson(course_id=1, week_id=2,
                           lesson_topic="Iterations and Ranges and Loops",
                           lecture_video_url="http://example.com/loops")
    lesson2_week2 = Lesson(course_id=1, week_id=2,
                           lesson_topic="Functions in Python", lecture_video_url="http://example.com/functions")

    return [user1, user2, course, week1, week2,
            lesson1_week1, lesson2_week1, lesson1_week2, lesson2_week2]


def generate_week1_questions():
    # Lesson 1: Variables and Data Types
    lesson1_id = 1  # Assume the lesson ID is 1 for "Variables and Data Types"
    questions_lesson1 = [
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "What is a variable in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "A container for storing data values",
            "option_2": "A function that performs an operation",
            "option_3": "A type of loop",
            "option_4": "A conditional statement",
            "correct_option": [0],  # Index of correct option
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which of the following is a valid variable name in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "123variable",
            "option_2": "variable_name",
            "option_3": "variable-name",
            "option_4": "variable name",
            "correct_option": [1],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which of the following data types is mutable?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "int",
            "option_2": "str",
            "option_3": "tuple",
            "option_4": "list",
            "correct_option": [3],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Select all the immutable data types in Python.",
            "question_type_mcq_msq": "MSQ",
            "option_1": "int",
            "option_2": "list",
            "option_3": "tuple",
            "option_4": "str",
            "correct_option": [0, 2, 3],
            "marks": 5
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which of the following are not primitive data types in Python?",
            "question_type_mcq_msq": "MSQ",
            "option_1": "int",
            "option_2": "float",
            "option_3": "list",
            "option_4": "str",
            "correct_option": [2],
            "marks": 5
        }
    ]

    # Lesson 2: Conditional Statements
    lesson2_id = 2  # Assume the lesson ID is 2 for "Conditional Statements"
    questions_lesson2 = [
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "What is the syntax for an if statement in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "if (condition) { }",
            "option_2": "if condition:",
            "option_3": "if condition then",
            "option_4": "if condition do",
            "correct_option": [1],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "What will be the output of the following code: if 5 > 3: print('Yes')?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "Yes",
            "option_2": "No",
            "option_3": "Error",
            "option_4": "None",
            "correct_option": [0],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which keyword is used for the alternative condition in an if-else statement?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "elseif",
            "option_2": "elif",
            "option_3": "else if",
            "option_4": "alternate",
            "correct_option": [1],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Select all the logical operators in Python.",
            "question_type_mcq_msq": "MSQ",
            "option_1": "and",
            "option_2": "or",
            "option_3": "not",
            "option_4": "xor",
            "correct_option": [0, 1, 2],
            "marks": 5
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which of the following are valid conditional statements in Python?",
            "question_type_mcq_msq": "MSQ",
            "option_1": "if condition:",
            "option_2": "elif condition:",
            "option_3": "else:",
            "option_4": "switch condition:",
            "correct_option": [0, 1, 2],
            "marks": 5
        }
    ]

    return questions_lesson1, questions_lesson2, lesson1_id, lesson2_id


def generate_week2_questions():
    # Lesson 1: Loops
    lesson3_id = 3  # Assume the lesson ID is 3 for "Loops"
    questions_lesson3 = [
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "What is the purpose of a loop in programming?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "To repeat a block of code multiple times",
            "option_2": "To perform a single operation",
            "option_3": "To define a function",
            "option_4": "To create a variable",
            "correct_option": [0],  # Index of correct option
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which of the following is a valid for loop syntax in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "for i in range(5)",
            "option_2": "loop i from 0 to 5",
            "option_3": "for (i=0; i<5; i++)",
            "option_4": "while (i < 5)",
            "correct_option": [0],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which keyword is used to exit a loop prematurely in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "continue",
            "option_2": "break",
            "option_3": "exit",
            "option_4": "stop",
            "correct_option": [1],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Select all the loop control statements in Python.",
            "question_type_mcq_msq": "MSQ",
            "option_1": "break",
            "option_2": "continue",
            "option_3": "pass",
            "option_4": "end",
            "correct_option": [0, 1, 2],
            "marks": 5
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which of the following loops will execute at least once?",
            "question_type_mcq_msq": "MSQ",
            "option_1": "for loop",
            "option_2": "while loop",
            "option_3": "do-while loop",
            "option_4": "nested loop",
            "correct_option": [2],
            "marks": 5
        }
    ]

    # Lesson 2: Functions
    lesson4_id = 4  # Assume the lesson ID is 4 for "Functions"
    questions_lesson4 = [
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "What is a function in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "A block of code which only runs when it is called",
            "option_2": "A type of variable",
            "option_3": "A loop control statement",
            "option_4": "A type of conditional statement",
            "correct_option": [0],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "How do you define a function in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "function myFunction():",
            "option_2": "def myFunction():",
            "option_3": "create myFunction():",
            "option_4": "define myFunction():",
            "correct_option": [1],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "What is the correct way to call a function named myFunction?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "call myFunction()",
            "option_2": "myFunction.call()",
            "option_3": "myFunction()",
            "option_4": "call function myFunction()",
            "correct_option": [2],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Select all the ways to return a value from a function in Python.",
            "question_type_mcq_msq": "MSQ",
            "option_1": "return value",
            "option_2": "yield value",
            "option_3": "output value",
            "option_4": "return()",
            "correct_option": [0, 1],
            "marks": 5
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which of the following statements about functions is true?",
            "question_type_mcq_msq": "MSQ",
            "option_1": "A function can have default arguments",
            "option_2": "A function cannot have multiple return statements",
            "option_3": "A function can be defined inside another function",
            "option_4": "A function can return multiple values",
            "correct_option": [0, 2, 4],
            "marks": 5
        }
    ]

    return questions_lesson3, questions_lesson4, lesson3_id, lesson4_id


def generate_sample_ratings():
    sample_ratings = [
        {'user_id': 1, 'lesson_id': 1, 'audio': 4, 'video': 3, 'content': 3,
         'feedback': 'Great lesson, but the content could be more detailed.'},
        {'user_id': 1, 'lesson_id': 1, 'audio': 3, 'video': 4, 'content': 4,
         'feedback': 'Good lecture, but the audio could be improved.'},
        {'user_id': 1, 'lesson_id': 1, 'audio': 3, 'video': 4, 'content': 4,
         'feedback': 'The lecture was good, but the audio quality was poor.'},
        {'user_id': 1, 'lesson_id': 1, 'audio': 4, 'video': 3, 'content': 4,
         'feedback': 'Good lecture, but the content could have been more in-depth.'},
        {'user_id': 1, 'lesson_id': 1, 'audio': 4, 'video': 4, 'content': 4,
         'feedback': 'The lecture was well-organized and the presenter was knowledgeable.'},
        {'user_id': 1, 'lesson_id': 1, 'audio': 4, 'video': 4, 'content': 4,
         'feedback': 'Audio quality was excellent, video visuals were clear, and content was well-structured.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 4, 'video': 3, 'content': 3,
         'feedback': 'Decent lecture, but the pace was a bit too slow.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 3, 'video': 3, 'content': 4,
         'feedback': 'Decent lecture, but the audio was a bit too quiet.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 1, 'video': 2, 'content': 2,
         'feedback': 'The lecture was not very engaging and the content was difficult to understand.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 1, 'video': 2, 'content': 1,
         'feedback': 'Poor audio, poor video, and content was irrelevant and boring.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 2, 'video': 2, 'content': 1,
         'feedback': 'Audio was difficult to understand, video was blurry, and content was confusing.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 1, 'video': 2, 'content': 2,
         'feedback': 'Video was clear, but audio was difficult to understand and content was confusing.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 2, 'video': 2, 'content': 1,
         'feedback': 'Audio was muffled, video was blurry, content was confusing.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 3, 'video': 4, 'content': 2,
         'feedback': 'OK audio, OK video, and content was not well-structured.'},
        {'user_id': 1, 'lesson_id': 2, 'audio': 1, 'video': 1, 'content': 1,
         'feedback': 'Bad audio, bad video, and content was very bad.'},
        {'user_id': 1, 'lesson_id': 1, 'audio': 5, 'video': 5, 'content': 4,
         'feedback': 'Excellent lecture! Video was particularly impressive.'},
        {'user_id': 1, 'lesson_id': 1, 'audio': 5, 'video': 5, 'content': 4,
         'feedback': 'Excellent audio, excellent video, and content was well-structured.'}
    ]

    ratings = []

    for data in sample_ratings:
        rating = Rating(
            user_id=data['user_id'],
            lesson_id=data['lesson_id'],
            audio=data['audio'],
            video=data['video'],
            content=data['content'],
            feedback=data['feedback'],
            created_at=datetime.utcnow()
        )
        ratings.append(rating)

    return ratings


def generate_sample_ques_submits():
    sample_submits = [
        {'user_id': 1, 'question_id': 1, 'is_correct': True, 'programming_code': None},
        {'user_id': 1, 'question_id': 2, 'is_correct': True, 'programming_code': None},
        {'user_id': 1, 'question_id': 3, 'is_correct': False, 'programming_code': None},
        {'user_id': 1, 'question_id': 4, 'is_correct': False, 'programming_code': None},
        {'user_id': 1, 'question_id': 5, 'is_correct': True, 'programming_code': None},
        {'user_id': 1, 'question_id': 6, 'is_correct': True, 'programming_code': None},
        {'user_id': 1, 'question_id': 7, 'is_correct': True, 'programming_code': None},
        {'user_id': 1, 'question_id': 8, 'is_correct': False, 'programming_code': None},
        {'user_id': 1, 'question_id': 9, 'is_correct': True, 'programming_code': None},
        {'user_id': 1, 'question_id': 10, 'is_correct': False, 'programming_code': None}
    ]

    student_questions = []

    for submit in sample_submits:
        student_question = StudentQuestion(
            user_id=submit['user_id'],
            question_id=submit['question_id'],
            is_correct=submit['is_correct'],
            programming_code=submit.get('programming_code')
        )
        student_questions.append(student_question)

    return student_questions


@app.route('/create_data', methods=['POST'])
def create_sample_data_api():
    try:
        # Create sample data
        sample_data = generate_sample_data()
        db.session.add_all(sample_data)
        db.session.commit()

        ql1, ql2, l1, l2 = generate_week1_questions()
        # Add questions to the database
        for q in ql1:
            question = Question(
                lesson_id=l1,
                question_type_aq_pm_pp_gp_gq=q["question_type_aq_pm_pp_gp_gq"],
                question=q["question"],
                question_type_mcq_msq=q["question_type_mcq_msq"],
                option_1=q["option_1"],
                option_2=q["option_2"],
                option_3=q["option_3"],
                option_4=q["option_4"],
                correct_option=q["correct_option"]
            )
            db.session.add(question)

        for q in ql2:
            question = Question(
                lesson_id=l2,
                question_type_aq_pm_pp_gp_gq=q["question_type_aq_pm_pp_gp_gq"],
                question=q["question"],
                question_type_mcq_msq=q["question_type_mcq_msq"],
                option_1=q["option_1"],
                option_2=q["option_2"],
                option_3=q["option_3"],
                option_4=q["option_4"],
                correct_option=q["correct_option"]
            )
            db.session.add(question)

        db.session.commit()

        ql3, ql4, l3, l4 = generate_week2_questions()
        for q in ql3:
            question = Question(
                lesson_id=l3,
                question_type_aq_pm_pp_gp_gq=q["question_type_aq_pm_pp_gp_gq"],
                question=q["question"],
                question_type_mcq_msq=q["question_type_mcq_msq"],
                option_1=q["option_1"],
                option_2=q["option_2"],
                option_3=q["option_3"],
                option_4=q["option_4"],
                correct_option=q["correct_option"],
            )
            db.session.add(question)

        for q in ql4:
            question = Question(
                lesson_id=l4,
                question_type_aq_pm_pp_gp_gq=q["question_type_aq_pm_pp_gp_gq"],
                question=q["question"],
                question_type_mcq_msq=q["question_type_mcq_msq"],
                option_1=q["option_1"],
                option_2=q["option_2"],
                option_3=q["option_3"],
                option_4=q["option_4"],
                correct_option=q["correct_option"],
            )
            db.session.add(question)

        ratings = generate_sample_ratings()

        for rating in ratings:
            db.session.add(rating)

        student_questions = generate_sample_ques_submits()

        for student_question in student_questions:
            db.session.add(student_question)

        db.session.commit()
        return jsonify({"message": "Sample data created successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    with app.app_context():
       db.create_all()
    app.run(debug=True)
