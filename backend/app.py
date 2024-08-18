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
from google.generativeai import GenerationConfig, GenerativeModel
from urllib.parse import parse_qs, urlparse
import json
from sqlalchemy.types import TypeDecorator, TEXT
from sqlalchemy.orm import relationship
from tenacity import retry, stop_after_attempt, wait_fixed
from google.generativeai import GenerationConfig
import subprocess
import logging
import tempfile


app = Flask(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'backend/instance/se2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for all routes
Misaka(app)
# Configure the Google Gemini API

api_key = 'AIzaSyAVAMym5LLS1vhEJxTPlB27G71FXY9gIUE'
genai.configure(api_key=api_key)

app.secret_key = '\xce\xa7\x1d\x9fc69\xd8\xfd\xd9\xe1\xbc'


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
    # is_admin = db.Column(db.Boolean, default=False)
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
    
    # New fields
    public_test_cases = db.Column(JSONEncodedText, nullable=True)
    private_test_cases = db.Column(JSONEncodedText, nullable=True)
    code_template = db.Column(db.Text, nullable=True)
    test_code = db.Column(db.Text, nullable=True)


    lesson = db.relationship("Lesson", back_populates="questions")
    student_questions = db.relationship("StudentQuestion", back_populates="question")

    def __init__(self, lesson_id, question_type_aq_pm_pp_gp_gq=None, question=None,
                 question_type_mcq_msq=None, option_1=None, option_2=None, option_3=None,
                 option_4=None, correct_option=None, efficient_code=None,
                 public_test_cases=None, private_test_cases=None, code_template=None, test_code=None):
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
        
        # Initialize new fields
        self.public_test_cases = public_test_cases
        self.private_test_cases = private_test_cases
        self.code_template = code_template
        self.test_code = test_code

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
    try:
        data = request.get_json()
        username = data.get('username')
        
        # Validate the input data
        if not isinstance(username, str) or '@' not in data.get('email'):
            return jsonify({'error': 'Invalid input data or missing required fields'}), 400
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Invalid input data or missing required fields'}), 400
        
        # Check if the username or email already exists in the database
        if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User with this username or email already exists'}), 409

        # Hash the password using PBKDF2 (Password-Based Key Derivation Function 2) with SHA-256
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        # Create a new User object with the provided data
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        
        # Commit the session to save the new user to the database
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Error occurred while creating the user account - {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Validate input data: Check if 'email' and 'password' fields are provided
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Invalid input data or missing required fields'}), 400

        email = data.get('email')
        password = data.get('password')

        # Check for admin login: If the email and password match the admin credentials
        if email == 'admin@gmail.com' and password == 'admin@pass':
            return jsonify({'message': 'Admin login successful', 'is_admin': True}), 200

        # Query the database for a user with the provided email
        user = User.query.filter_by(email=email).first()
        
        # Validate the user's password: Check if the user exists and the password matches the stored hash
        if user and check_password_hash(user.password, password):
            return jsonify({'message': 'Login successful', 'is_admin': False, 'user_Id': user.id}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': f'Error occurred during login - {str(e)}'}), 500

@app.route('/api/submit_rating', methods=['POST'])
def submit_rating():
    try:
        data = request.get_json()

        # Check for missing fields
        required_fields = ['user_id', 'lesson_id', 'audio', 'video', 'content', 'feedback']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            # print(missing_fields)
            return jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400
        

        # Extract data from request
        user_id = data.get('user_id')
        lesson_id = data.get('lesson_id')
        audio = data.get('audio')
        video = data.get('video')
        content = data.get('content')
        feedback = data.get('feedback')

        # print(user_id, lesson_id, audio, video, content, feedback)
        
        user=User.query.filter_by(id=user_id).first()
        if not user :
            return jsonify({'error': 'User not found'}), 404
        
        lessid=Lesson.query.filter_by(lesson_id=lesson_id['lessonId']).first()
        if not lessid :
            return jsonify({'error': 'Lesson not found'}), 404


        # Ensure that ratings are integers and within the acceptable range
        if not (isinstance(audio, int) and isinstance(video, int) and isinstance(content, int)):
            return jsonify({'error': 'Audio, video, and content ratings must be integers.'}), 400
        
        if not (1 <= audio <= 5) or not (1 <= video <= 5) or not (1 <= content <= 5):
            return jsonify({'error': 'Ratings should be between 1 and 5.'}), 400

        # Creating a new rating instance
        new_rating = Rating(
            user_id=user_id,
            lesson_id=lessid.lesson_id,
            audio=audio,
            video=video,
            content=content,
            feedback=feedback
        )

        # Adding the new rating to the database session
        db.session.add(new_rating)
        db.session.commit()

        return jsonify({'message': 'Rating submitted successfully'}), 201

    except Exception as e:
        return jsonify({'error': f'Error occurred while submitting rating - {str(e)}'}), 500   

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    try:
        # Fetch all ratings from the database
        ratings = Rating.query.all()
        
        # Create a list of dictionaries with rating details
        rating_list = [{
            'id': rating.id,
            'user_id': rating.user_id,
            'lesson_id': rating.lesson_id,
            'audio': rating.audio,
            'video': rating.video,
            'content': rating.content,
            'feedback': rating.feedback,
            'created_at': rating.created_at.isoformat()  # Convert to ISO format for JSON serialization
        } for rating in ratings]
        
        return jsonify(rating_list), 200

    except Exception as e:
        return jsonify({'error': f'Error occurred while fetching ratings - {str(e)}'}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        # Fetch all users from the database
        users = User.query.all()
        
        # Create a list of  user details
        user_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        } for user in users]
        
        return jsonify(user_list), 200

    except Exception as e:
        return jsonify({'error': f'Error occurred while fetching users - {str(e)}'}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


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
    questions = Question.query.filter_by(lesson_id=lesson_id, question_type_aq_pm_pp_gp_gq='AQ').all() #queries from the questions table
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

        for idx, question in enumerate(quiz_data): # verification of correct answers with the user's answer
            user_answer = user_answers.get(str(quiz_data[idx]["question_id"]), "null")
            if question['type'] == 'MSQ' and user_answer:
                user_answer = set(user_answer)
            is_correct = user_answer == question['correct']
            score = question['marks'] if is_correct else 0
            total_score += score

            existing_response = StudentQuestion.query.filter_by(user_id = user_id, question_id=question['question_id']).first()
            if existing_response:
                # Updating the existing response if present in the student question table 
                existing_response.is_correct = is_correct
            else:
                # Creating a new response if not present in the student question table 
                student_response = StudentQuestion(user_id = user_id, question_id=question['question_id'], is_correct=is_correct,programming_code=None)
                db.session.add(student_response)
            db.session.commit()


            try:
                if not is_correct:   # if the user answer is incorrect, explanation is coming from gemini api
                    explanation = get_explanation(question['question'], question['correct'])

                else:
                    explanation = None
            except Exception as e:
                return jsonify({'error': f'Error generating activity question"s explanation: {e}'}),404

            existing_response = StudentQuestion.query.filter_by(user_id=user_id,question_id=question['question_id']).first()
            if existing_response:
                # Updating the existing response in the student question table
                existing_response.is_correct = is_correct
            else:
                # if the response is not found in the student question table then a student response is created
                student_response = StudentQuestion(user_id=user_id,question_id=question['question_id'], is_correct=is_correct,programming_code=None)
                db.session.add(student_response)
                db.session.commit()
                
            results.append({   # result is appended here 
                'question': question['question'],
                'correct_answer': question['correct'],
                'user_answer': list(user_answer) if isinstance(user_answer, set) else user_answer,
                'is_correct': is_correct,
                'score': score,
                'explanation': explanation
            })

        return jsonify({
            'results': results,
            'score': total_score,
            'max_score': max_score,
            'score_percentage': (score / max_score) * 100
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
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Explanation for the correct answer"
                    }
                },
                "required": ["question", "options", "correct", "marks", "topic", "explanation"]
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
                    },
                    "explanation": {
                        "type": "string",
                        "description": " In depth explanation for the correct answers"
                    }
                },
                "required": ["question", "options", "correct", "marks", "topic", "explanation"]
            }
        }
    ]
}


    for question_data in quiz_data:
        topic = question_data['topic']
        question_type = question_data['type']
        # this prompt uses the schema defined above and gives a json formatted output using the topic and the question-type([MCQ or MSQ] which is extracted from  the database)
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


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@app.route('/api/activity/extra_questions/<int:lesson_id>', methods=['GET', 'POST'])
def new_quiz(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    if request.method == 'GET':
        try:
            session['new_quiz_data'] = generate_new_question(lesson_id)
            print("Session Data", session.get("new_quiz_data"))
            return jsonify({'new_quiz_data': list(enumerate(session['new_quiz_data']))})
        except Exception as e:
            return jsonify({'error': f'Error generating extra questions: {e}'}),400
    
    if request.method == 'POST':
        print(session)
        if 'new_quiz_data' not in session:
            return jsonify({'error': 'Quiz data not found. Please start a new quiz.'}), 400

        data = request.get_json()
        user_id = data.get("user_id")
        user_answers = data.get('answers', {})

        print("user_answers: ", user_answers)
        results = []
        score = 0
        max_score = sum([q['marks'] for q in session.get('new_quiz_data')])
        print(max_score)
        for idx, question in enumerate(session.get('new_quiz_data')):
            user_answer = user_answers.get(str(idx),"did not understand")
            correct_answer = question['correct']
            is_correct = user_answer == correct_answer if question['type'] == 'MCQ' else set(user_answer) == set(correct_answer)

            if is_correct:
                score += question['marks']

            result = {
                'user_id': user_id,
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
            'score': score,
            'max_score': max_score
        })
    session.pop('new_quiz_data', None)

#______________________Graded Assignment________________________

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@app.route('/api/graded/quiz/<int:week_id>', methods=['GET', 'POST'])
def quiz(week_id):
    lesson_ids = [lesson.lesson_id for lesson in Lesson.query.with_entities(Lesson.lesson_id).filter_by(week_id=week_id).all()]  # the list contains all the list ids for a particular week
    if not lesson_ids:
        return jsonify({"error": "No lesson  in this week."}), 404
    
    questions = Question.query.filter(Question.lesson_id.in_(lesson_ids)).all()  # questions are extracted based on the lesson ids for a particular week
    if not questions:
        return jsonify({"error": "No questions  for this week."}), 404
    
    print("Questions: ",questions)
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
        
        print("user_answers: ", user_answers)

        for idx, question in enumerate(quiz_data): # verification of correct answers with the user answers 
            user_answer = user_answers.get(str(quiz_data[idx]['question_id']),"null")
            if question['type'] == 'MSQ' and user_answer:
                user_answer = set(user_answer)
            print("User_Answer: ", user_answer)
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
                # Updating the existing response if present in the student question table 
                existing_response.is_correct = is_correct
            else:
                # Creating a new response if not present in the student question table 
                student_response = StudentQuestion(user_id = user_id, question_id=question['question_id'], is_correct=is_correct,programming_code=None)
                db.session.add(student_response)
                db.session.commit()
            try:
                if not is_correct:
                    explanation = get_explanation(question['question'], correct_answer)
                    result['explanation'] = explanation
                results.append(result)
            except Exception as e:
                return jsonify({'error': f'Error generating graded question"s explanation: {e}'}),404
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

def generate_swot_analysis(student_performance: dict, lesson_topics: list, correct_attempts: list, incorrect_attempts: list):
    """
    Generates a SWOT analysis report based on student performance data.

    This function uses an AI model to analyze student performance metrics, lesson topics, and attempts (both correct and incorrect) to produce a comprehensive SWOT analysis. 
    The output follows a specified JSON schema.

    Parameters:
    --------------

    - student_performance (dict): Dictionary containing performance scores and overall AI score.

    - lesson_topics (list): List of topics covered in the lessons.

    - correct_attempts (list): List of correctly attempted questions.

    - incorrect_attempts (list): List of incorrectly attempted questions.

    Returns:
    - str: JSON string with SWOT analysis (strengths, weaknesses, opportunities, threats).
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=genai.GenerationConfig(response_mime_type="application/json")
    )

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
    """
    API Endpoint to analyze and retrieve a student's weekly performance.

    Parameters:
    - user_id (int): The ID of the student/user.
    - week_no (int): The week number for which the performance is to be analyzed
    
    Returns:
    - JSON object containing the SWOT analysis report and performance scores.
    - Error responses for cases such as user not found, week not found, 
      no questions found, or student answers not submitted.

    Responses:
    - 200: Success with the SWOT analysis report.
    - 404: User not found, Week not found, No questions found, or Student didn't submit answers.
    - 500: Internal server error during SWOT analysis generation.
    """

    try:
        # Extract user_id and week_no from the request JSON
        data = request.json
        user_id = data.get('user_id')
        week_no = data.get('week_no')

        # Check if user_id and week_no are provided
        if not user_id or not week_no:
            return jsonify({"error": "user_id and week_no are required fields"}), 400
        

        # Fetch the user by user_id
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # Fetch the week by week_no
        week = Week.query.filter_by(week_no=week_no).first()
        if week is None:
            return jsonify({"error": "Week not found"}), 404

        week_id = week.id

        # Check if the SWOT analysis already exists in the database
        existing_performance = StudentWeeklyPerformance.query.filter_by(
            user_id=user_id, week_id=week_id).first()
        
        if existing_performance:
            # Return the existing SWOT analysis if found
            db.session.delete(existing_performance);
            db.session.commit();

        # Fetch all lessons associated with the week
        lessons = Lesson.query.filter_by(week_id=week_id).all()
        if not lessons:
            return jsonify({"error": "No lessons found for this week"}), 404

        
        course = Course.query.filter_by(id=lessons[0].course.id).first()
        if course is None:
            return jsonify({"error": "Course not found"}), 404
        
        lesson_topics = [lesson.lesson_topic for lesson in lessons]

        # Fetch all questions associated with the lessons
        questions = Question.query.filter(Question.lesson_id.in_([lesson.lesson_id for lesson in lessons])).all()
        if not questions:
            return jsonify({"error": "No questions found for this week"}), 404


        # Fetch student answers for the questions
        student_answers = StudentQuestion.query\
            .filter(StudentQuestion.question_id.in_([q.question_id for q in questions]))\
            .filter_by(user_id=user_id).all()
        if not student_answers:
            return jsonify({"error": "Student did not submit answers for this week"}), 404


        correct_attempted_ques = []
        incorrect_attempted_ques = []

        scores = {
            'aq_score': 0,
            'pm_score': 0,
            'pp_score': 0,
            'gp_score': 0,
            'gq_score': 0,
        }
        total_marks = 0
        
        # Calculate scores based on student answers
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

        # Calculate overall AI score
        obtained_score = (scores['aq_score'] + scores['pm_score'] + scores['pp_score'] +
                        scores['gp_score'] + scores['gq_score'])
        overall_ai_score = obtained_score / total_marks if total_marks != 0 else 0

        # Generate SWOT analysis
        try:
            swot_analysis_json = generate_swot_analysis({
                'aq_score': scores['aq_score'],
                'pm_score': scores['pm_score'],
                'pp_score': scores['pp_score'],
                'gp_score': scores['gp_score'],
                'gq_score': scores['gq_score'],
                'overall_ai_score': overall_ai_score
            }, lesson_topics, correct_attempted_ques, incorrect_attempted_ques)
        except Exception as e:
            return jsonify({"error": f"Failed to generate SWOT analysis - {str(e)}"}), 500
        
        # Parse SWOT analysis JSON
        swot_analysis = json.loads(swot_analysis_json)

        # Save the student's weekly performance in the database
        performance = StudentWeeklyPerformance(
            user_id=user_id,
            week_id=week_id,
            course_id=course.id,
            aq_score=scores['aq_score'],
            pm_score=scores['pm_score'],
            pp_score=scores['pp_score'],
            gp_score=scores['gp_score'],
            gq_score=scores['gq_score'],
            overall_ai_score=overall_ai_score,
            ai_report_pdf_url=json.dumps(swot_analysis['swot_analysis'])
        )

        db.session.add(performance)
        db.session.commit()

        return swot_analysis, 200
    except KeyError as e:
        return jsonify({"error": f"Missing key in request: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"INTERNAL SERVER ERROR: {str(e)}"}), 500


# ============================ Feedback Sentiment Analysis ==========================


def generate_feedback_summary(lessons_feedbacks):
    """
    Generates a summarized feedback report for lectures using the AI model.

    This function processes feedback data for each lecture, analyzes sentiment, summarizes key points, and provides improvement suggestions. It returns a JSON-formatted string following a predefined schema.

    Parameters:
    - lessons_feedbacks (dict): Dictionary of feedback lists keyed by lecture IDs.

    Returns:
    - str: JSON string with feedback summaries, sentiment scores, and suggestions.
    """
    
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

    response = model.generate_content(prompt)
    response_text = response.candidates[0].content.parts[0].text
    return response_text


@app.route("/api/sentiment_analysis", methods=['POST'])
def sentiment_analysis():
    """
    API Endpoint to perform sentiment analysis on feedback provided for lessons.

    This API collects all ratings from the database, extracts feedback for each lesson, 
    and then generates a feedback summary using sentiment analysis. 
    The results are returned as a JSON response.

    Returns:
    - JSON object containing the sentiment analysis results for each lesson.
    - Error responses for cases such as issues with database retrieval or sentiment analysis.

    Responses:
    - 200: Success with the feedback summary.
    - 404: No ratings found in the database.
    - 500: Internal server error during database query or feedback summary generation.
    """

    try:
        # Fetch all ratings from the database
        ratings = Rating.query.all()

        # Check if there are no ratings
        if not ratings:
            return jsonify({"error": "No ratings found in the database"}), 404

        lessons_feedback = {}

        # Organize feedbacks by lesson_id
        for rating in ratings:
            lesson_id = rating.lesson_id
            feedback = rating.feedback

            if lesson_id not in lessons_feedback:
                lessons_feedback[lesson_id] = []

            # Add feedback to the corresponding lesson_id
            if feedback:
                lessons_feedback[lesson_id].append(feedback)

        try:
            # Generate feedback summary using sentiment analysis
            f_summary = generate_feedback_summary(lessons_feedback)
            feedback_summary = json.loads(f_summary)
        except Exception as e:
            return jsonify({"error": f"Failed to generate feedback summary - {str(e)}"}), 500

        return feedback_summary, 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


# =========================== Contextual ChatBot API ==============================

# Conversation History for ChatBot
conversations = {}


@app.route("/api/chat", methods=['POST'])
def chat_ai():
    """
    API Endpoint for Chat with AI ChatBot

    This API allows users to interact with an AI Bot

    The conversation history is maintained using a session ID, allowing for continuous dialogue.

    Request:
    - session_id: (Optional) A unique identifier for the chat session.
    - message: The user's message to the AI.

    Returns:
    - JSON object containing the AI's response.
    - Error responses for cases such as missing data or issues with the AI model interaction.

    Responses:
    - 200: Success with the AI's response.
    - 500: Internal server error during AI model interaction.
    """

    try:
        # Extract session_id and user_message from the request JSON
        session_id = request.json.get("session_id")
        user_message = request.json.get("message")

        if not user_message:
            return jsonify({"error": "Message cannot be empty!"}), 400
        
        # Ensure session_id is present and valid, otherwise create a new one
        if not session_id or session_id not in conversations:
            # Initialize the session with an empty conversation history
            conversations[session_id] = []

        # Initialize the chat model with generation configuration
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

         # Retrieve or initialize conversation history
        conversation_history = conversations[session_id]

        chat_session = chat_model.start_chat(
            history=conversation_history
        )

        try:
            response = chat_session.send_message(user_message)
        except Exception as e:
            # Handle exceptions that might occur during message generation
            return jsonify({"error": f"An error occurred while processing the message."}), 500

        model_response = response.text

        conversation_history.append({"role": "user", "parts": [user_message]})
        conversation_history.append({"role": "model", "parts": [model_response]})
        conversations[session_id] = conversation_history

        return jsonify({"response": model_response}), 200
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500



@app.route('/api/compile', methods=['POST'])
def compile_code():
    """
    API route to compile and execute submitted code against public test cases.

    This endpoint receives a question ID and code from the request, retrieves
    the corresponding question from the database, and compiles and runs the code
    against the public test cases associated with the question.

    Returns:
        JSON response containing the results of the code execution,
        including input, expected output, actual output, and whether the test passed.
    """

    # Get question ID and submitted code from the incoming JSON request
    q_id = request.json.get("question_id")
    code = request.json.get("code")
    print(q_id, code)
    # Validate that question ID and code are provided
    if not q_id:
        return jsonify({'error': 'Question ID is required'}), 400
    if not code:
        return jsonify({'error': 'Code is required'}), 400

    # Retrieve the question from the database using the provided question ID
    question = db.session.get(Question, q_id)

    # Check if the question was found
    if question is None:
        return jsonify({'error': 'Question not found'}), 404

    # Extract public test cases and test code from the question object
    public_test_cases = question.public_test_cases
    test_code = question.test_code

    # Debugging: Print the submitted code, public test cases, and test code to the console
    print(q_id)
    print(code)
    print(public_test_cases)
    print(test_code)

    # Validate that public test cases are available
    if not public_test_cases:
        return jsonify({'error': 'Test cases are required'}), 400

    # Run the submitted code using Python subprocess (this only compiles the code)
    response = subprocess.run(['python3', '-c', code], capture_output=True, text=True)

    # If there are any compilation errors, return them as a response
    if response.stderr:
        return jsonify({'error': response.stderr}), 500

    # Initialize an empty list to hold the results of each test case execution
    results = []

    # Loop through each public test case to run the submitted code against it
    for test_case in public_test_cases:
        input_value = test_case['input']
        expected_output = test_case['expected_output']

        # Create a prompt for code explanation and execution (used by an AI model)
        prompt = f"Compile and check the python code and detect and show all the possible syntax errors present in the code and if not then execute this code {code} against the test case {input_value} and return only the result which will be return by function."

        try:
            # Execute the code against the test case using an external model (e.g., AI model)
            response = model2.generate_content(prompt)
            actual_output = response.candidates[0].content.parts[2].code_execution_result.output

            # Debugging: Print the actual and expected outputs to the console
            print(type(actual_output))
            print(type(expected_output))
            print(expected_output)
            print(actual_output)

            # Compare the actual output with the expected output and store the result
            results.append({
                'input': input_value,
                'expected_output': expected_output,
                'actual_output': actual_output,
                'passed': str(actual_output.strip()) == str(expected_output)
            })
        except Exception as e:
            # If an error occurs during execution, store the error message in the results
            results.append({
                'input': input_value,
                'expected_output': expected_output,
                'actual_output': str(e),
                'passed': False
            })

    # Return the results of the code execution as a JSON response
    return jsonify({'results': results})



@app.route('/api/submit', methods=['POST'])
def submit():
    """
    API route for submitting code against private test cases.

    This endpoint receives a user's code and the corresponding question ID,
    compiles and executes the code against the private test cases associated
    with the question, and evaluates the results. If all test cases pass, 
    the submission is saved to the database.

    Returns:
        JSON response containing the score, a success message, or an error message.
    """

    # Get the submitted code and question ID from the incoming JSON request
    code = request.json.get('code')
    q_id = request.json.get("question_id")
    
    # Retrieve the question from the database based on the question ID
    question = db.session.get(Question, q_id)
    if question.question_type_aq_pm_pp_gp_gq != 'PP':
        return jsonify({"error": "invalid question id"}), 400

    # Extract private test cases from the question object
    private_test_cases = question.private_test_cases
    
    # Language of the code (hardcoded as "python" here)
    language = "python"
    
    # Get the user ID from the incoming JSON request
    user_id = request.json.get('user_id')
    
    # Compile and run the submitted code using Python subprocess
    response = subprocess.run(['python3', '-c', code], capture_output=True, text=True)


    # If there are syntax or runtime errors during the initial code execution, return the error
    if response.stderr:
        return jsonify({'error': response.stderr}), 500

    # Initialize the score (number of successful test cases)
    score = 0

    # Loop through each private test case to run the submitted code against it
    for test in private_test_cases:
        input_value = test['input']
        expected_output = test['expected_output']

        # Create a prompt for code explanation and execution (used by an external AI model)
        prompt = f"Compile and check the python code and detect and show all the possible syntax errors present in the code and if not then execute this code {code} written in the language {language} against the test case {input_value} and return only the result which will be return by function."

        try:
            # Execute the code against the test case using an external model (e.g., AI model)
            response = model2.generate_content(prompt)
            actual_output = response.candidates[0].content.parts[2].code_execution_result.output

            # Debugging: Print the actual and expected outputs to the console
            print(type(actual_output))
            print(type(expected_output))
            print(expected_output)
            print(actual_output)

            # Check if the actual output matches the expected output
            if str(expected_output) == str(actual_output.strip()):
                score += 1  # Increment the score if the test case passes
            else:
                print("test case failed")

        except Exception as e:
            # Log any errors that occur during the execution of the test case
            logging.error(f"Error running test: {str(e)}")
            return jsonify({'error': str(e)}), 500

    # If all private test cases pass, save the submission to the database
    if score == len(private_test_cases):
        try:
            # Create a new entry for the student's submission in the StudentQuestion table
            student_submission = StudentQuestion(
                user_id=user_id,
                question_id=q_id,
                is_correct=1,
                programming_code=code,      
            )
            db.session.add(student_submission)  # Add the submission to the session
            db.session.commit()  # Commit the session to save the submission to the database

            # Return success response with the score and success message
            return jsonify({'score': score, 'message': 'Code submitted successfully!'}), 200
        
        except Exception as e:
            # Log any errors that occur during the database transaction
            logging.error(f"Error saving submission: {str(e)}")
            return jsonify({'error': 'Failed to save submission'}), 500

    # Return a message indicating that some test cases failed
    return jsonify({'score': score, 'message': 'Some test cases failed'}), 200


@app.route('/api/explainCode', methods=['POST'])
def get_hint():
    """
    API route to generate a hint or suggestion for improving or debugging a code snippet.

    This endpoint accepts code, language, and a related question as input.
    It uses an AI model to generate hints or suggestions for improving the code.
    The response is returned in HTML format using Markdown for better readability.

    Returns:
        JSON response containing the generated hint in HTML format, or an error message.
    """

    # Extract the code, language, and question from the incoming JSON request
    code = request.json.get('code')
    language = request.json.get('language')
    question_id = request.json.get('question_id')
    
    question = db.session.get(Question, question_id)

    que = question.question

    # Construct the prompt for the AI model, asking for suggestions or hints
    prompt = f'''I have the following code snippet in {language} for the question \n\n{que}\n. Can you provide a hint or suggestion for improving or debugging it?\n\n{code}\n'''

    try:
        # Generate the result by passing the prompt to the AI model
        result = model2.generate_content(prompt)
        
        # Convert the generated text result to HTML using Markdown for better readability
        hint = result.text
        
        # Return the hint as a JSON response in HTML format
        return jsonify({'hint': hint})

    except Exception as e:
        # Log any errors that occur and return an error message in the JSON response
        logging.error(f"Error generating hint: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/getEfficientCode', methods=['POST'])
def getCode():
    """
    API route to retrieve or generate efficient code for a specific question.

    This endpoint receives a `question_id` and retrieves the efficient code from the database if it exists. 
    If the efficient code is not found, it generates efficient code using an AI model, saves it in the database, and returns it.

    Returns:
        JSON response containing the efficient code or an error message.
    """
    
    # Parse the JSON request body to extract the question_id
    data = request.json
    question_id = data.get('question_id')
    print("question_id: ", question_id)

    # Validate the presence of question_id in the request
    if not question_id:
        return jsonify({"error": "question_id is required"}), 400

    # Retrieve the question from the database using the question_id
    question = db.session.get(Question, question_id)

    # If the question is not found, return a 404 error
    if not question:
        return jsonify({"error": "Question not found"}), 404
    
    # Extract the question statement, code template, and efficient code from the question object
    question_statement = question.question
    question_template = question.code_template
    efficient_code = question.efficient_code

    # If efficient code already exists, return it in the JSON response
    if efficient_code:
        return jsonify({"efficient_code": efficient_code}), 200
    
    else:
        # Construct a prompt asking the AI model to generate efficient Python code based on the question statement and template
        prompt = f"Write the efficient Python code with the best time and space complexity for the question '{question_statement}' completing the template '{question_template}'."
        
        try:
            # Use the AI model to generate the efficient code
            response = model2.generate_content(prompt, tools="code_execution")
            best_code = response.text
            
            # Save the generated code in the database for future use
            question.efficient_code = best_code
            db.session.commit()

            # Return the generated efficient code in the response
            return jsonify({"efficient_code": best_code}), 200
        
        except Exception as e:
            # Log the error and return an error message in case of failure
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

    week1 = Week(week_no=1, week_start_date=datetime(2024, 8, 1), week_end_date=datetime(2024, 10, 7))
    week2 = Week(week_no=2, week_start_date=datetime(2024, 8, 8), week_end_date=datetime(2024, 10, 14))
    week3 = Week(week_no=3, week_start_date=datetime(2024, 8, 15), week_end_date=datetime(2024, 10, 21))
    week4 = Week(week_no=4, week_start_date=datetime(2024, 8, 22), week_end_date=datetime(2024, 10, 28))

    lesson1_week1 = Lesson(course_id=1, week_id=1,
                           lesson_topic="Variables and Data Types",
                           lecture_video_url="https://youtube.com/watch?v=Yg6xzi2ie5s")
    lesson1_week2 = Lesson(course_id=1, week_id=2,
                           lesson_topic="Conditional Statements",
                           lecture_video_url="https://youtube.com/watch?v=-dBqiRCHbNw")
    lesson1_week3 = Lesson(course_id=1, week_id=3,
                           lesson_topic="Iterations and Loops",
                           lecture_video_url="https://youtube.com/watch?v=lvXuQ_x7EsI")
    lesson1_week4 = Lesson(course_id=1, week_id=4,
                           lesson_topic="Functions in Python",
                           lecture_video_url="https://youtube.com/watch?v=TBFTFusLIco")

    return [user1, user2, course, week1, week2, week3, week4,
            lesson1_week1, lesson1_week2, lesson1_week3, lesson1_week4]


def generate_week1_questions():
    # Week 1: Lesson 1 (Variables and Data Types) and Lesson 2 (Conditional Statements)

    # Lesson 1: Variables and Data Types
    lesson1_id = 1  # Assume the lesson ID is 1
    questions_lesson1 = [
        {
            "question_type_aq_pm_pp_gp_gq": "AQ",
            "question": "Define a variable in Python.",
            "question_type_mcq_msq": "MCQ",
            "option_1": "A container for storing data values",
            "option_2": "A function that performs an operation",
            "option_3": "A type of loop",
            "option_4": "A conditional statement",
            "correct_option": ["A container for storing data values"],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "AQ",
            "question": "Explain the difference between mutable and immutable types.",
            "question_type_mcq_msq": "MCQ",
            "option_1": "Mutable types can be changed after their creation",
            "option_2": "Immutable types cannot be changed after their creation",
            "option_3": "Mutable types cannot be changed after their creation",
            "option_4": "Immutable types can be changed after their creation",
            "correct_option": ["Mutable types can be changed after their creation",
                               "Immutable types cannot be changed after their creation"],
            "marks": 5
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Which of the following is a valid variable name in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "123variable",
            "option_2": "variable_name",
            "option_3": "variable-name",
            "option_4": "variable name",
            "correct_option": ["variable_name"],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Select all immutable data types in Python.",
            "question_type_mcq_msq": "MSQ",
            "option_1": "int",
            "option_2": "list",
            "option_3": "tuple",
            "option_4": "str",
            "correct_option": ["int", "tuple", "str"],
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
            "correct_option": ["list"],
            "marks": 3
        }
    ]

    # Lesson 2: Conditional Statements
    lesson2_id = 2  # Assume the lesson ID is 2
    questions_lesson2 = [
        {
            "question_type_aq_pm_pp_gp_gq": "AQ",
            "question": "Explain the purpose of conditional statements in Python.",
            "question_type_mcq_msq": "MCQ",
            "option_1": "To perform actions based on conditions",
            "option_2": "To create loops",
            "option_3": "To define variables",
            "option_4": "To store data",
            "correct_option": ["To perform actions based on conditions"],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "AQ",
            "question": "Describe the syntax of an if statement in Python.",
            "question_type_mcq_msq": "MCQ",
            "option_1": "if (condition) { }",
            "option_2": "if condition:",
            "option_3": "if condition then",
            "option_4": "if condition do",
            "correct_option": ["if condition:"],
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
            "correct_option": ["Yes"],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "GQ",
            "question": "Select all logical operators in Python.",
            "question_type_mcq_msq": "MSQ",
            "option_1": "and",
            "option_2": "or",
            "option_3": "not",
            "option_4": "xor",
            "correct_option": ["and", "or", "not"],
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
            "correct_option": ["if condition:", "elif condition:", "else:"],
            "marks": 5
        }
    ]

    return questions_lesson1, questions_lesson2, lesson1_id, lesson2_id


def generate_week2_questions():
    # Week 2: Lesson 1 (Loops) and Lesson 2 (Functions)

    # Lesson 1: Loops
    lesson3_id = 3  # Assume the lesson ID is 3
    questions_lesson3 = [
        {
            "question_type_aq_pm_pp_gp_gq": "AQ",
            "question": "What is the purpose of a loop in programming?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "To repeat a block of code multiple times",
            "option_2": "To perform a single operation",
            "option_3": "To define a function",
            "option_4": "To create a variable",
            "correct_option": ["To repeat a block of code multiple times"],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "AQ",
            "question": "Which keyword is used to exit a loop prematurely in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "continue",
            "option_2": "break",
            "option_3": "exit",
            "option_4": "stop",
            "correct_option": ["break"],
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
            "correct_option": ["for i in range(5)"],
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
            "correct_option": ["break", "continue", "pass"],
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
            "correct_option": ["do-while loop"],
            "marks": 5
        }
    ]

    # Lesson 2: Functions
    lesson4_id = 4  # Assume the lesson ID is 4
    questions_lesson4 = [
        {
            "question_type_aq_pm_pp_gp_gq": "AQ",
            "question": "What is a function in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "A block of code which only runs when it is called",
            "option_2": "A type of variable",
            "option_3": "A loop control statement",
            "option_4": "A type of conditional statement",
            "correct_option": ["A block of code which only runs when it is called"],
            "marks": 3
        },
        {
            "question_type_aq_pm_pp_gp_gq": "AQ",
            "question": "How do you define a function in Python?",
            "question_type_mcq_msq": "MCQ",
            "option_1": "function myFunction():",
            "option_2": "def myFunction():",
            "option_3": "create myFunction():",
            "option_4": "define myFunction():",
            "correct_option": ["def myFunction():"],
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
            "correct_option": ["myFunction()"],
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
            "correct_option": ["return value", "yield value"],
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
            "correct_option": ["A function can have default arguments",
                               "A function can be defined inside another function",
                               "A function can return multiple values"],
            "marks": 5
        }
    ]

    return questions_lesson3, questions_lesson4, lesson3_id, lesson4_id


def generate_programming_questions_w1():
    questions = [
        {
            "question_type_aq_pm_pp_gp_gq": "PP",  # Programming problem
            "question": "Write a function to check if a number is prime.",
            "marks": 10,
            "public_test_cases": [
                {
                    "input": 2,
                    "expected_output": "True"
                },
                {
                    "input": 4,
                    "expected_output": "False"
                },
                {
                    "input": 13,
                    "expected_output": "True"
                }
            ],
            "private_test_cases": [
                {
                    "input": 1,
                    "expected_output": "False"
                },
                {
                    "input": 17,
                    "expected_output": "True"
                },
                {
                    "input": 20,
                    "expected_output": "False"
                }
            ],
            "code_template": """def is_prime(n):\n    # Your code here\n""",
            "test_code": """{code}\nprint(is_prime({input}))"""
        }
    ]
    return questions


def generate_programming_questions_w2():
    questions = [
        {
            "question_type_aq_pm_pp_gp_gq": "PP",  # Programming problem
            "question": "Write a function to find the maximum number in a list.",
            "marks": 10,
            "public_test_cases": [
                {
                    "input": [1, 2, 3, 4, 5],
                    "expected_output": 5
                },
                {
                    "input": [10, 20, 30, 5, 15],
                    "expected_output": 30
                },
                {
                    "input": [-1, -2, -3, -4, -5],
                    "expected_output": -1
                }
            ],
            "private_test_cases": [
                {
                    "input": [100, 200, 300, 400, 500],
                    "expected_output": 500
                },
                {
                    "input": [7, 7, 7, 7, 7],
                    "expected_output": 7
                },
                {
                    "input": [-100, 0, 100, 200, -200],
                    "expected_output": 200
                }
            ],
            "code_template": """def find_max(lst):\n    # Your code here\n""",
            "test_code": """{code}\nprint(find_max({input}))"""
        }
    ]

    return questions


def generate_programming_questions_w3():
    questions = [
        {
            "question_type_aq_pm_pp_gp_gq": "PP",  # Programming problem
            "question": "Write a function to merge two sorted lists into one sorted list.",
            "marks": 10,
            "public_test_cases": [
                {
                    "input": ([1, 3, 5], [2, 4, 6]),
                    "expected_output": [1, 2, 3, 4, 5, 6]
                },
                {
                    "input": ([1, 2, 3], [4, 5, 6]),
                    "expected_output": [1, 2, 3, 4, 5, 6]
                },
                {
                    "input": ([7, 8], [1, 2, 3]),
                    "expected_output": [1, 2, 3, 7, 8]
                }
            ],
            "private_test_cases": [
                {
                    "input": ([0, 2, 4], [1, 3, 5]),
                    "expected_output": [0, 1, 2, 3, 4, 5]
                },
                {
                    "input": ([10, 20, 30], [5, 15, 25]),
                    "expected_output": [5, 10, 15, 20, 25, 30]
                },
                {
                    "input": ([], [1, 2, 3]),
                    "expected_output": [1, 2, 3]
                }
            ],
            "code_template": """def merge_sorted_lists(list1, list2):\n    # Your code here\n""",
            "test_code": """{code}\nprint(merge_sorted_lists({input[0]}, {input[1]}))"""
        },
    ]

    return questions


def generate_programming_questions_w4():
    questions = [
        {
            "question_type_aq_pm_pp_gp_gq": "PP",  # Programming problem
            "question": "Write a function to count the number of vowels in a given string.",
            "marks": 10,
            "public_test_cases": [
                {
                    "input": "hello",
                    "expected_output": 2
                },
                {
                    "input": "world",
                    "expected_output": 1
                },
                {
                    "input": "programming",
                    "expected_output": 3
                }
            ],
            "private_test_cases": [
                {
                    "input": "AEIOU",
                    "expected_output": 5
                },
                {
                    "input": "python",
                    "expected_output": 1
                },
                {
                    "input": "this is a test",
                    "expected_output": 4
                }
            ],
            "code_template": """def count_vowels(s):\n    # Your code here\n""",
            "test_code": """{code}\nprint(count_vowels("{input}"))"""
        }
    ]

    return questions


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
        pq_w1 = generate_programming_questions_w1()
        pq_w2 = generate_programming_questions_w2()
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

        for q in pq_w1:
            question = Question(
                lesson_id=l1,
                question_type_aq_pm_pp_gp_gq=q["question_type_aq_pm_pp_gp_gq"],
                question=q["question"],
                public_test_cases=q["public_test_cases"],
                private_test_cases=q["private_test_cases"],
                code_template=q["code_template"],
                test_code=q["test_code"]
            )
            db.session.add(question)

        for q in pq_w2:
            question = Question(
                lesson_id=l2,
                question_type_aq_pm_pp_gp_gq=q["question_type_aq_pm_pp_gp_gq"],
                question=q["question"],
                public_test_cases=q["public_test_cases"],
                private_test_cases=q["private_test_cases"],
                code_template=q["code_template"],
                test_code=q["test_code"]
            )
            db.session.add(question)

        db.session.commit()

        ql3, ql4, l3, l4 = generate_week2_questions()
        pq_w3 = generate_programming_questions_w3()
        pq_w4 = generate_programming_questions_w4()
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

        for q in pq_w3:
            question = Question(
                lesson_id=l3,
                question_type_aq_pm_pp_gp_gq=q["question_type_aq_pm_pp_gp_gq"],
                question=q["question"],
                public_test_cases=q["public_test_cases"],
                private_test_cases=q["private_test_cases"],
                code_template=q["code_template"],
                test_code=q["test_code"]
            )
            db.session.add(question)

        for q in pq_w4:
            question = Question(
                lesson_id=l4,
                question_type_aq_pm_pp_gp_gq=q["question_type_aq_pm_pp_gp_gq"],
                question=q["question"],
                public_test_cases=q["public_test_cases"],
                private_test_cases=q["private_test_cases"],
                code_template=q["code_template"],
                test_code=q["test_code"]
            )
            db.session.add(question)

        db.session.commit()

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

@app.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    if question:
        return jsonify({
            'question': question.question,
            'code_template': question.code_template,
            'public_test_cases': question.public_test_cases,
            'private_test_cases': question.private_test_cases,
            'test_code': question.test_code,
            # Add more fields as needed
        })
    else:
        return jsonify({'error': 'Question not found'}), 404


@app.route('/api/weeks', methods=['GET'])
def get_weeks():
    weeks = Week.query.all()
    weeks_data = []
    
    for week in weeks:
        week_data = {
            "id": week.id,
            "week_no": week.week_no,
            "week_start_date": week.week_start_date.strftime('%Y-%m-%d'),
            "week_end_date": week.week_end_date.strftime('%Y-%m-%d'),
            "lectures": [],
            "questions": [],
            "assignments": []
        }
        
        # Add lessons
        for lesson in week.lessons:
            lecture_data = {
                "id": lesson.lesson_id,
                "topic": lesson.lesson_topic,
                "video_url": lesson.lecture_video_url
            }
            week_data["lectures"].append(lecture_data)
            
            # Add questions related to this lesson
            for question in lesson.questions:
                question_data = {
                    "id": question.question_id,
                    "question_text": question.question,
                    "type": question.question_type_mcq_msq,
                    "options": [question.option_1, question.option_2, question.option_3, question.option_4]
                }
                week_data["questions"].append(question_data)
        
        # Assuming assignments are a part of questions or a different table/model
        
        weeks_data.append(week_data)
    
    return jsonify(weeks_data)



@app.route('/api/weeks/<int:week_id>/lessons', methods=['GET'])
def get_week_lessons(week_id):
    lessons = Lesson.query.filter_by(week_id=week_id).all()
    lessons_data = []
    for lesson in lessons:
        questions = Question.query.filter_by(lesson_id=lesson.lesson_id).all()
        questions_data = [{
            "question_id": q.question_id,
            "question_text": q.question,
            "options": [q.option_1, q.option_2, q.option_3, q.option_4],
            "correct_option": q.correct_option
        } for q in questions]
        lessons_data.append({
            "id": lesson.lesson_id,
            "topic": lesson.lesson_topic,
            "video_url": lesson.lecture_video_url,
            "questions": questions_data
        })
    return jsonify({"lessons": lessons_data})

@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([{
        'question_id': q.question_id,
        'lesson_id': q.lesson_id,
        'question_type': q.question_type_aq_pm_pp_gp_gq,
        'question': q.question,
        'question_type_MCQ_MSQ': q.question_type_mcq_msq,
        'code_template': q.code_template,
        'options': [q.option_1, q.option_2, q.option_3, q.option_4],
        'correct_option': q.correct_option,
        'marks': q.marks
    } for q in questions])


@app.route("/api/about-video/<int:lesson_id>", methods=["POST","GET"])
def about_video(lesson_id):
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

    prompt = f"""
    You are a content creator who needs to write a compelling "About Video" description. 
    The goal is to provide a concise yet informative summary that highlights the key points, 
    purpose, and value of the video, making it appealing to potential viewers. 
    Using the transcript provided, generate a description that captures the essence of the video, 
    including the main topics covered, any significant insights or takeaways, and 
    why someone should watch it. Ensure the description is engaging and aligns with the video's tone and intent.

    Transcript:
    # {transcript}
    """
    try:
        model = GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=GenerationConfig(
                temperature=0.4
            )
        )

        response = model.generate_content(prompt)
        return jsonify({"message": response.text}), 200
    except Exception as e:
        return jsonify({"error": f"Error in generating about video - {str(e)}"}), 500



@app.route("/api/explainer", methods=['POST',"GET"])
def explain_ai():
    session_id = request.json.get("session_id")
    question_id = request.json.get("question_id")

    # Retrieve the question details using the get_question API
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    # Prepare the question text for the AI model
    question_text = question.question

    generation_config = GenerationConfig(
        temperature=0.1,
        top_p=0.95,
        top_k=64,
        max_output_tokens=500,
        response_mime_type="text/plain"
    )

    explain_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="""
        You are an expert explainer. When given a question, your task is to provide a detailed and easy-to-understand explanation. 
        Break down the concepts, use real-world analogies, and keep the explanation engaging.
        """
    )

    if session_id not in conversations:
        conversations[session_id] = []

    conversation_history = conversations[session_id]

    explain_session = explain_model.start_chat(
        history=conversation_history
    )

    response = explain_session.send_message(question_text)

    model_response = response.text

    conversation_history.append({"role": "user", "parts": [question_text]})
    conversation_history.append({"role": "model", "parts": [model_response]})
    conversations[session_id] = conversation_history

    return jsonify({"response": model_response}), 200

if __name__ == '__main__':
    with app.app_context():
       db.create_all()
    app.run(debug=True)
