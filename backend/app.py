from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for all routes

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
