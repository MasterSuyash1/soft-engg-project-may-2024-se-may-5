# This is the testing comment 
from flask import Flask, request, jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
import os
from datetime import datetime
import re
import markdown
from flask_misaka import Misaka
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
from urllib.parse import parse_qs, urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for all routes
Misaka(app)
# Configure the Google Gemini API
api_key = 'AIzaSyBFo_2jMDaxOEtrMxGh8er1NcWabofMAro'
genai.configure(api_key=api_key)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    audio = db.Column(db.Integer, nullable=False)
    video = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))   
class Lesson(db.Model):
    __tablename__ = 'lessons'

    LESSON_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    COURSE_ID = db.Column(db.Integer, nullable=False)
    WEEK_ID = db.Column(db.Integer, nullable=False)
    LESSON_TOPIC = db.Column(db.Text, nullable=False)
    LECTURE_VIDEO_URL = db.Column(db.Text, nullable=False)
    questions = db.relationship('Question', backref='lesson', lazy=True)
    

class Question(db.Model):
    __tablename__ = 'questions'

    QUESTION_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    LESSON_ID = db.Column(db.Integer, db.ForeignKey('lessons.LESSON_ID'), nullable=False)
    QUESTION_TYPE_AQ_PM_PP_GP_GQ = db.Column(db.Text, nullable=True)
    QUESTION = db.Column(db.Text, nullable=True)
    QUESTION_TYPE_MCQ_MSQ = db.Column(db.Text, nullable=True)
    OPTION_1 = db.Column(db.Text, nullable=True)
    OPTION_2 = db.Column(db.Text, nullable=True)
    OPTION_3 = db.Column(db.Text, nullable=True)
    OPTION_4 = db.Column(db.Text, nullable=True)
    CORRECT_OPTION = db.Column(db.Text, nullable=True)
    MARKS = db.Column(db.Integer, nullable=False)
    

    def __init__(self, LESSON_ID=None, QUESTION_TYPE_AQ_PM_PP_GP_GQ=None, QUESTION=None, 
                 QUESTION_TYPE_MCQ_MSQ=None, OPTION_1=None, OPTION_2=None, OPTION_3=None, 
                 OPTION_4=None, CORRECT_OPTION=None, MARKS=None):
        self.LESSON_ID = LESSON_ID
        self.QUESTION_TYPE_AQ_PM_PP_GP_GQ = QUESTION_TYPE_AQ_PM_PP_GP_GQ
        self.QUESTION = QUESTION
        self.QUESTION_TYPE_MCQ_MSQ = QUESTION_TYPE_MCQ_MSQ
        self.OPTION_1 = OPTION_1
        self.OPTION_2 = OPTION_2
        self.OPTION_3 = OPTION_3
        self.OPTION_4 = OPTION_4
        self.CORRECT_OPTION = CORRECT_OPTION
        self.MARKS = MARKS 

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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_message)
        bot_response = response.text
        formatted_response = ' '.join(bot_response.split())
        return jsonify({'response': formatted_response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.get_json()
    user_id = data.get('user_id')
    audio = data.get('audio')
    video = data.get('video')
    content = data.get('content')
    feedback = data.get('feedback')

    new_rating = Rating(user_id=user_id, audio=audio, video=video, content=content, feedback=feedback)
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
        "created_at": user.ratings[-1].created_at if user.ratings else None
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


@app.route('/api/sentiment_analysis', methods=['GET'])
def sentiment_analysis():
    try:
        ratings = Rating.query.all()
        feedback_list = [rating.feedback for rating in ratings if rating.feedback]
        
        sentiments = []
        for feedback in feedback_list:
            prompt = f"""Tell me whether the following sentence's sentiment is positive or negative or something in between.
            Sentence {feedback}
            Sentiment"""
            response = genai.generate_text(
                model='models/text-bison-001',
                temperature=0.5,
                candidate_count=1,
                top_k=40,
                top_p=0.95,
                max_output_tokens=1024,
                prompt=prompt
            )
            sentiment = response.result.strip().split('\n')[-1].strip()  # Extract sentiment
            sentiments.append({
                'feedback': feedback,
                'sentiment': sentiment
            })

        return jsonify(sentiments), 200
    except Exception as e:
        print(f"Error: {e}")  # Log the error to the console
        return jsonify({'error': str(e)}), 500

# Add your code here Anuj,

# Add your code here Asmita,
#______________________________________________Swetha's Code begins______________________________________________________________
quiz_data = [
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'correct': '4',
        'type': 'mcq',
        'question_type': 'AQ',
        'marks': 3,
        'topic': 'Arithmetic - Addition'
    },
    {
        'question': 'Which of the following are prime numbers?',
        'options': ['2', '3', '4', '5'],
        'correct': ['2', '3', '5'],
        'question_type': 'AQ',
        'type': 'msq',
        'marks': 5,
        'topic': 'Arithmetic - Prime Numbers'
    },
    {
        'question': 'What is 3 * 3?',
        'options': ['6', '7', '8', '9'],
        'question_type': 'AQ',
        'correct': '9',
        'type': 'mcq',
        'marks': 3,
        'topic': 'Arithmetic - Multiplication'
    },
    {
        'question': 'Which of the following statements about Python functions are true?',
        'options': [
            'A function in Python is defined using the `def` keyword.',
            'Functions in Python can return multiple values.',
            'In Python, you cannot define a function inside another function.',
            'A function can take another function as an argument.'
        ],
        'correct': [
            'A function in Python is defined using the `def` keyword.',
            'Functions in Python can return multiple values.',
            'A function can take another function as an argument.'
        ],
        'type': 'msq',
        'question_type': 'AQ',
        'marks': 5,
        'topic': 'Python - Functions'
    },
    {
        'question': 'Which of the following is the correct way to define a function in Python?',
        'options': [
            'function myFunction() { }',
            'def myFunction():',
            'myFunction() = function() { }',
            'define myFunction() { }'
        ],
        'correct': 'def myFunction():',
        'type': 'mcq',
        'marks': 3,
        'question_type': 'AQ',
        'topic': 'Python - Functions'
    },
    {
        'question': 'What is the output of the following Python code?\n\n```python\nx = [1, 2, 3, 4]\nprint(x[1:3])\n```',
        'options': [
            '[1, 2]',
            '[1, 2, 3]',
            '[2, 3]',
            '[3, 4]'
        ],
        'correct': '[2, 3]',
        'type': 'mcq',
        'marks': 3,
        'question_type': 'AQ',
        'topic': 'Python - lists'
    }
]

for item in quiz_data:
        new_question = Question(
    QUESTION=item['question'],
    QUESTION_TYPE_AQ_PM_PP_GP_GQ=item['question_type'],
    QUESTION_TYPE_MCQ_MSQ=item['type'],
    TOPIC=item['topic'],
    OPTION_1=item['options'][0],
    OPTION_2=item['options'][1],
    OPTION_3=item['options'][2],
    OPTION_4=item['options'][3],
    CORRECT_OPTION=item['correct'] if item['type'] == 'mcq' else ','.join(item['correct']),
    MARKS=item['marks']
        )
        db.session.add(new_question)
db.session.commit()


def get_explanation(question, correct_answer):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f'You are a teacher, you have to give step-by-step solution of the {question} whose correct answer is {correct_answer}. Explanation:'
    explanation = model.generate_content(prompt)
    explanation_html = markdown.markdown(explanation.text)
    return explanation_html
#____________________Activity Quiz________________________________
@app.route('/api/activity/quiz/<int:lesson_id>', methods=['GET', 'POST'])
def activity_quiz(lesson_id):
    questions = Question.query.filter_by(LESSON_ID=lesson_id, QUESTION_TYPE_AQ_PM_PP_GP_GQ='AQ').all()
    lesson = Lesson.query.get(lesson_id)
    
    quiz_data = [
        {
            'question': q.QUESTION,
            'options': [q.OPTION_1, q.OPTION_2, q.OPTION_3, q.OPTION_4],
            'correct': q.CORRECT_OPTION.split(', ') if q.QUESTION_TYPE_MCQ_MSQ == 'msq' else q.CORRECT_OPTION,
            'type': q.QUESTION_TYPE_MCQ_MSQ,
            'marks': q.MARKS,
            'topic': lesson.LESSON_TOPIC
        } for q in questions
    ]

    if request.method == 'POST':
        data = request.get_json()
        user_answers = data.get('answers', {})
        results = []
        total_score = 0
        max_score = sum([q['marks'] for q in quiz_data])

        for idx, question in enumerate(quiz_data):
            user_answer = user_answers.get(str(idx))
            if question['type'] == 'msq' and user_answer:
                user_answer = set(user_answer)
            is_correct = user_answer == question['correct']
            score = question['marks'] if is_correct else 0
            total_score += score

            if not is_correct:
                explanation = get_explanation(question['question'], question['correct'])
            else:
                explanation = None

            results.append({
                'question': question['question'],
                'correct_answer': question['correct'],
                'user_answer': user_answer,
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
    question_match = re.search(r"Question:\n(.*?)\nOptions:", response_text, re.DOTALL)
    question = question_match.group(1).strip() if question_match else None

    options_match = re.search(r"Options:\n(.*?)\nCorrect Answer:", response_text, re.DOTALL)
    options = options_match.group(1).strip().split('\n') if options_match else None

    correct_answer_match = re.search(r"Correct Answer:\n(.*)", response_text)
    correct_answer = correct_answer_match.group(1).strip() if correct_answer_match else None

    if not question or not options or not correct_answer:
        print("Error: Missing section in response text")
        return None

    def clean_text(text):
        cleaned_text = re.sub(r'^\s*[-*]?\s*', '', text)
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text

    options = [clean_text(option) for option in options]
    correct_answer = clean_text(correct_answer)

    if correct_answer not in options:
        print(f"Error: Correct answer '{correct_answer}' not found in options.")
        return None

    return {
        'question': question,
        'options': options,
        'correct': correct_answer if question_type == 'mcq' else correct_answer.split(', '),
        'type': question_type,
        'marks': 3 if question_type == "mcq" else 5,
        'topic': topic
    }

def generate_new_question(lesson_id):
    questions = Question.query.filter_by(LESSON_ID=lesson_id).all()
    lesson = Lesson.query.get(lesson_id)

    quiz_data = [
        {
            'question': q.QUESTION,
            'options': [q.OPTION_1, q.OPTION_2, q.OPTION_3, q.OPTION_4],
            'correct': q.CORRECT_OPTION.split(', ') if q.QUESTION_TYPE_MCQ_MSQ == 'msq' else q.CORRECT_OPTION,
            'type': q.QUESTION_TYPE_MCQ_MSQ,
            'marks': q.MARKS,
            'topic': q.lesson.LESSON_TOPIC
        } for q in questions if q.QUESTION_TYPE_AQ_PM_PP_GP_GQ == 'AQ'
    ]

    new_questions = []
    model = genai.GenerativeModel('gemini-pro')

    for question_data in quiz_data:
        topic = question_data['topic']
        question_type = question_data['type']

        prompt_template = f"""Generate a new {question_type.upper()} question for the topic: {topic}. 
Please provide the following details in the exact format specified:
Question:
(Write the question here)
Options:
- Option 1
- Option 2
- Option 3
- Option 4
Correct Answer:
(Correct option here)"""

        response = model.generate_content(prompt_template)
        response_text = response.candidates[0].content.parts[0].text
        print(response_text)
        new_question = parse_generated_question(response_text, question_type, topic)
        if new_question is not None:
            new_questions.append(new_question)

    return new_questions

@app.route('/api/<int:lesson_id>/activity/extra_questions', methods=['GET', 'POST'])
def new_quiz(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404

    if request.method == 'POST':
        data = request.get_json()
        user_answers = data.get('answers', {})
        results = []
        total_score = 0
        max_score = sum([q['marks'] for q in session.get('new_quiz_data', [])])

        for idx, question in enumerate(session.get('new_quiz_data', [])):
            user_answer = user_answers.get(str(idx))
            correct_answer = question['correct']
            is_correct = user_answer == correct_answer if question['type'] == 'mcq' else set(user_answer) == set(correct_answer)

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
            
            if not is_correct:
                explanation = get_explanation(question['question'], correct_answer)
                result['explanation'] = explanation
            
            results.append(result)

        return jsonify({
            'new_quiz_data': list(enumerate(session.get('new_quiz_data', []))),
            'results': results,
            'total_score': total_score,
            'max_score': max_score
        })

    session['new_quiz_data'] = generate_new_question(lesson_id)
    return jsonify({'new_quiz_data': list(enumerate(session['new_quiz_data']))})

#______________________Graded Assignment________________________
@app.route('/api/graded/quiz', methods=['GET', 'POST'])
def quiz():
    questions = Question.query.all()
    quiz_data = [
        {
            'question': q.QUESTION,
            'options': [q.OPTION_1, q.OPTION_2, q.OPTION_3, q.OPTION_4],
            'correct': q.CORRECT_OPTION.split(', ') if q.QUESTION_TYPE_MCQ_MSQ == 'msq' else q.CORRECT_OPTION,
            'type': q.QUESTION_TYPE_MCQ_MSQ,
            'marks': q.MARKS,
            'topic': q.TOPIC
        } for q in questions if q.QUESTION_TYPE_AQ_PM_PP_GP_GQ == 'GQ'
    ]

    if request.method == 'POST':
        data = request.get_json()
        user_answers = data.get('answers', {})
        results = []
        total_score = 0
        max_score = sum([q['marks'] for q in quiz_data])

        for idx, question in enumerate(quiz_data):
            user_answer = user_answers.get(str(idx))
            if question['type'] == 'msq' and user_answer:
                user_answer = set(user_answer)
            correct_answer = question['correct']
            is_correct = (user_answer == correct_answer) if question['type'] == 'mcq' else (set(user_answer) == set(correct_answer))
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
            if not is_correct:
                explanation = get_explanation(question['question'], correct_answer)
                result['explanation'] = explanation
            results.append(result)

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

@app.route('/api/transcript_notes/<int:lesson_id>', methods=['GET'])
def process_video(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found."}), 404
    
    video_url = lesson.Lecture_video_url  # Extract the video URL from the lesson object
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
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt_topics + transcript_text)
    important_topics_md = response.text
    important_topics_html = Misaka().render(important_topics_md)
    
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    video_embed = f'<iframe id="videoPlayer" width="560" height="315" src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    
    return jsonify({
        "video_embed": video_embed,
        "transcript_text": transcript_text,
        "notes": notes_html,
        "important_topics": important_topics_html
    })


#______________________________________________________Swetha's Code end__________________________________________________________


# Add your code here Yadvendra



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
