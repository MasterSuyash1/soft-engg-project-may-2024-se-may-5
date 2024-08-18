import requests

BASE_URL = "http://127.0.0.1:5000"

# region Test Cases for Users API
def test_delete_user_user_not_found():
    """
    Tests whether the code correctly rejects deleting a user which does not exist
    """
    user_id = -1
    response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
    assert response.status_code in [400, 404]

    user_id = 999999
    response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
    assert response.status_code == 404

def test_get_users_successful():
    """
    Tests whether the app correctly returns the list of users
    """
    response = requests.get(f"{BASE_URL}/api/users")
    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list) 

# endregion

# region Test Cases for Signup / Login API
def test_signup_empty_inputs():
    """
    Tests whether the app correctly rejects empty inputs for user registration
    """
    data = {"username": "", "email": "", "password": ""} # All empty inputs
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code == 400

    data = {"username": "someusername", "email": "someemail@email.com", "password": ""} # password empty
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code == 400    
    
    data = {"username": "", "email": "someemail@email.com", "password": "somepassword"} # Username empty
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code == 400

    data = {"username": "someusername", "email": "", "password": "somepassword"} # Email empty
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code == 400

def test_signup_invalid_input():
    """
    Tests whether the app correctly rejects incompatible inputs for the user registration
    """
    data = {"username": 123.4, "email": "someemail@email.com", "password": "somepassword"} # Invalid Username
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code == 400, "Invalid username got accepted"

    data = {"username": "username", "email": "someemail.com", "password": ""} # Invalid email
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code == 400, "Invalid email got accepted"

def test_signup_duplicate_email():
    """
    Tests whether the app correctly rejects duplicate email during registration
    """
    data = {"username": "newusername", "email": "user1@gmail.com", "password": "somepassword"} # duplicate email
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code in [400, 409]

def test_signup_duplicate_username():
    """
    Tests whether the app correctly rejects duplicate username during registration
    """
    data = {"username": "user123", "email": "newemail@email.com", "password": "somepassword"} # duplicate username
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code in [ 400, 409 ]

def test_signup_successful():
    """
    Tests whether the app correctly accepts and registers a new user
    """
    data = {"username": "newusername5", "email": "newuser5@email.com", "password": "newpassword"}
    response = requests.post(f"{BASE_URL}/signup", json=data)
    assert response.status_code == 201

def test_login_empty_inputs():
    """
    Tests if the app correctly rejects empty inputs for the user login
    """
    # data = {"email": "", "password": ""} # All empty
    # response = requests.post(f"{BASE_URL}/login", json=data)
    # assert response.status_code == 400
    
    data = {"email": "", "password": "somepassword"} # Email empty
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 400
    
    data = {"email": "someemail@email.com", "password": ""} # Password empty
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 400

def test_login_invalid_credentials():
    """
    Tests whether the app correctly rejects invalid credentials when logging in
    """
    data = {"email": "user1@gmail.com", "password": "wrongpassword"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 401
    #assert str(response.json()['message']).upper() == "INVALID CREDENTIALS"

    data = {"email": "wrongemail@email.com", "password": "somepassword"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 401

def test_login_successful():
    """
    Tests whether the app correctly accepts and logs in a user
    """
    data = {"email": "newuser@email.com", "password": "newpassword"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 200
    assert str(response.json()['message']).upper() == "LOGIN SUCCESSFUL"

# endregion

# region Test cases for Ratings API

def test_submit_ratings_invalid_id():
    """
    Tests whether the code correctly rejects an invalid user_id such as one which doesn't exist in the database
    when submitting content ratings by the users
    """
    data = {
        "user_id": 1,
        "lesson_id" : 1,
        "audio": 4,
        "video": 4,
        "content": 4,
        "feedback": "Excellent tutorial!",
    }

    data["user_id"] = 999999 # Invalid user_id
    response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
    assert response.status_code == 404
    
    data['user_id'] = 1 # reset

    data['lesson_id'] = 99999 # invalid lesson_id
    response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
    assert response.status_code == 404, "Invalid lesson_id got accepted"

def test_submit_ratings_invalid_input():
    """
    Tests whether the code correctly rejects invalid data types or missing data. Here,
    the audio rating is a float instead of an integer and the field 'feedback' is missing
    """
    data = {"user_id": 1, "lesson_id" : 1, "audio": 4.5, "video": 4, "content": 4}
    response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
    assert response.status_code == 400, "Float rating did not get rejected"

def test_submit_ratings_successful():
    """
    Tests the successful creation of a Ratings review and whether the endpoint correctly returns the
    newly created Ratings review
    """
    data = {
        "user_id": 1,
        "lesson_id" : 1,
        "audio": 4,
        "video": 4,
        "content": 4,
        "feedback": "Excellent tutorial!",
    }
    response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)

    assert response.status_code == 201
    assert str(response.json()["message"]).upper() == "RATING SUBMITTED SUCCESSFULLY"

def test_get_ratings():
    """
    Tests whether the app correctly responds with all the ratings when queried
    """
    response = requests.get(f"{BASE_URL}/api/ratings")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

# endregion

# region Lectures API Test

def test_lesson_transcript_invalid_inputs():
    """
    Tests whether the app correctly rejects incompatible input of lesson_id when trying to generate transcript for a lesson
    """
    lesson_id = "" # Empty Lesson id
    response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")
    assert response.status_code == 404

def test_lesson_transcript_not_found():
    """
    Tests whether the app correctly returns not found message when the lesson is not found
    """
    lesson_id = 99999
    response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")

    assert response.status_code == 404

def test_lesson_transcript_successful():
    """
    Tests whether the app correctly handles transcript generation API
    """
    lecture_id = 1
    response = requests.get(f"{BASE_URL}/api/transcript_notes/{lecture_id}")
    assert response.status_code == 200
    assert response.json()['transcript_text']
    assert response.json()['notes']

def test_chat_api_empty_chat_message():
    """
    Tests whether the app correctly rejects accepting no inputs as message from the user during chat
    """
    data = { "session_id": 1 , "message": ""} # message not there

    response = requests.post(f"{BASE_URL}/api/chat", json=data)
    assert response.status_code in [ 400, 415, 500 ]

def test_chat_api_empty_session_id():
    """
    Tests whether the app correctly creates session_id internally when a session_id is not provided in the chat
    """
    data = {"message": "Explain what hashing is to me.", "session_id": None} # session_id is not there
    response = requests.post(f"{BASE_URL}/api/chat", json=data)
    assert response.status_code == 200
    assert str(response.json()["response"])

def test_chat_api_successful():
    """
    Tests whether the app correctly returns a response from the GenAI model when message is passed in the chat
    """
    data = {"message": "Explain what hashing is to me.", "session_id": 1} 
    response = requests.post(f"{BASE_URL}/api/chat", json=data)
    assert response.status_code == 200
    assert str(response.json()["response"])

def test_sentiment_analysis_successful():
    """
    Tests whether the app correctly returns the sentiment analysis from the GenAI model 
    """
    response = requests.post(f"{BASE_URL}/api/sentiment_analysis")
    assert response.status_code == 200
    assert isinstance(response.json()["lecture_feedback_summaries"], list)

# endregion

# region Activity and Extra Questions Test Cases
def test_get_activity_questions_invalid_inputs():
    """
    Tests getting activity questions with invalid inputs
    """
    lesson_id = -1 # lesson doesn't exist
    response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
    assert response.status_code in [ 400, 404], "lesson_id not found failed"

def test_get_activity_questions_empty_inputs():
    """
    Tests getting activity questions with empty inputs
    """
    lesson_id = ""
    response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
    assert response.status_code == 404, "Empty lesson_id failed"

def test_get_activity_questions_successful():
    """
    Tests getting activity questions successfully
    """
    lesson_id = 1
    response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
    assert response.status_code == 200

# endregion

# region Graded Questions API Test Cases
def test_get_graded_questions_successful():
    """
    Tests whether the app correctly returns the graded quiz questions for a week
    """
    week_id = 1
    response = requests.get(f'{BASE_URL}/api/graded/quiz/{week_id}')
    assert response.status_code == 200
    assert response.json()['quiz_data']

def test_get_graded_questions_week_not_found():
    """
    Tests whether the app correctly returns the week not found
    """
    week_id = 99999
    response = requests.get(f'{BASE_URL}/api/graded/quiz/{week_id}')
    assert response.status_code == 404

def test_get_graded_questions_week_not_found():
    """
    Tests whether the app correctly returns the week not found
    """
    week_id = 99999
    response = requests.get(f'{BASE_URL}/api/graded/quiz/{week_id}')
    assert response.status_code == 404

def test_graded_questions_submissions_successful():
    """
    Tests whether the app correctly accepts a graded submission and returns solutions
    """
    week_id = 1
    answers = { str(0): "answer", str(1) : "wronganswer" }
    data = { "user_id":1, "answers" :answers}
    response = requests.post(f"{BASE_URL}/api/graded/quiz/{week_id}", json=data)
    assert response.status_code == 200
    assert response.json()["results"]
    
    response_json = response.json()

    incorrect_answers = [ response_json['results'][i] for i in range(len(response_json['results'])) if not response_json['results'][i]['is_correct']] 
    if len(incorrect_answers) > 0:
        assert incorrect_answers[0]['explanation']

def test_graded_questions_submission_invalid_inputs():
    week_id = 999999
    user_id = 1
    answers = { str(i): f"answer_i" for i in range(100)}
    data = { "user_id": user_id, "answers" :answers}
    response = requests.post(f"{BASE_URL}/api/graded/quiz/{week_id}", json=data)
    assert response.status_code in [ 400, 404 ]

    user_id = 99999
    data = { "user_id":user_id, "answers" :answers}
    response = requests.post(f"{BASE_URL}/api/graded/quiz/{week_id}", json=data)
    assert response.status_code in [400, 404]

# endregion

# region Programming Questions Test Cases
def test_compile_code_successful():
    """
    Tests whether the app correctly compiles a valid python code
    """
    data = {
        "code": "def add(a, b): return a+b", 
        "question_id": 23
    }

    response = requests.post(f"{BASE_URL}/api/compile", json=data)
    assert response.status_code == 200

def test_compile_code_syntax_error():
    """
    Tests whether the app correctly identifies errors in code such as syntax error passed by the client
    """
    data = {
        "code": "def add(a, b): return a+c",
        "question_id": 12
    }

    response = requests.post(f"{BASE_URL}/api/compile", json=data)
    assert response.status_code == 200

def test_submit_code_syntax_error():
    """
    Tests whether the app correctly identifies errors in code such as syntax error passed by the client
    """
    data = {
        "code": "def add(a, b): return a+c",
        "user_id": 1,
        "question_id": 11
    }

    response = requests.post(f"{BASE_URL}/api/submit", json=data)
    assert response.status_code == 200
    assert response.json()['score'] == 0

def test_private_test_cases_successful():
    """
    Tests whether the app correctly verifies and refutes private test cases being passed by the client
    """
    data = {
        "code": "def add(a, b): return a+b",
        "user_id": 1,
        "question_id": 23
    }

    response = requests.post(f"{BASE_URL}/api/submit", json=data)
    assert response.status_code == 200
    #assert response.json()['score'] == 1 # private test case should fail

def test_generate_hint_successful():
    """
    Tests whether the app correctly responds with a hint to a programming problem
    """
    data = { 
        "code": "def add(a, b): return a", 
        "language": "python",
        "question_id": 23
    }

    response = requests.post(f"{BASE_URL}/api/explainCode", json=data)
    assert response.status_code == 200
    assert response.json()['hint']

def test_efficient_solution_invalid_inputs():
    """
    Tests whether the app correctly rejects invalid inputs when requesting efficient code solution
    """
    data = { "question_id" : 99999 }

    response = requests.post(f"{BASE_URL}/api/getEfficientCode", json=data)
    assert response.status_code == 404, "Question not found failed"

    data['question_id'] = None
    response = requests.post(f"{BASE_URL}/api/getEfficientCode", json=data)
    assert response.status_code == 400, "Bad request failed"

    data['question_id'] = -1
    response = requests.post(f"{BASE_URL}/api/getEfficientCode", json=data)
    assert response.status_code in [400, 404], "Bad request failed"

def test_efficient_solution_successful():
    """
    Tests whether the app correctly returns an efficient solution to the problem
    """
    data = { "question_id" : 1 }
    response = requests.post(f"{BASE_URL}/api/getEfficientCode", json=data)
    assert response.status_code == 200

# endregion

# region Weekly Performance Report API Test Cases

def test_weekly_performance_empty_inputs():
    """
    Tests whether the app correctly rejects empty inputs for weekly performance report
    """
    data = {"user_id" : 1} # missing week_no
    response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
    print(response.json())
    assert response.status_code in [ 400, 404 ], "Missing lesson_id failed"

    data = {"week_no" : 1} # missing user_id
    response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
    assert response.status_code in [400, 404], "Missing user_id failed"

def test_weekly_performance_invalid_inputs():
    """
    Tests whether the app correctly rejects invalid inputs such as user_id and lesson_id for weekly performance report
    """
    data = {"user_id" : -1, "week_no":1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
    assert response.status_code in [ 404, 400], "Invalid user_id failed"

    data = {"user_id" : 1, "week_no":-1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
    assert response.status_code in [ 400, 404 ], "Invalid week_no failed"

def test_weekly_performance_successful_generation():
    """
    Tests whether the app returns the user weekly performance report successfully
    """
    data = {"user_id" : 1, "week_no":1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
    assert response.status_code == 200
    assert response.json()["performance"]
    assert response.json()["swot_analysis"]

def test_weekly_performance_successful_user_not_found():
    """
    Tests whether the app correctly returns not found for a user for weekly performance report
    """
    data = {"user_id" : 99999, "week_no":1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
    assert response.status_code == 404, "User not found failed"

def test_weekly_performance_successful_not_found():
    """
    Tests whether the app correctly returns not found for a user for weekly performance
    """
    data = {"user_id" : 1, "week_no":99999}
    response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
    assert response.status_code == 404, "Lesson not found failed"

# endregion
  # new test cases for apis

def test_about_video_invalid_inputs():
    """
    Tests whether the app correctly rejects incompatible input of lesson_id when trying to generate video info for a lesson
    """
    lesson_id = "" # Empty Lesson id
    response = requests.get(f"{BASE_URL}/api/about-video/{lesson_id}")
    assert response.status_code == 404

def test_about_video_not_found():
    """
    Tests whether the app correctly returns not found message when the lesson is not found
    """
    lesson_id = 99999
    response = requests.get(f"{BASE_URL}/api/about-video/{lesson_id}")

    assert response.status_code == 404

def test_about_video_successful():
    """
    Tests whether the app correctly handles transcript generation API
    """
    lecture_id = 1
    response = requests.get(f"{BASE_URL}/api/about-video/{lecture_id}")
    assert response.status_code == 200
    assert response.json()['message']



#senti analysis video nott found 
    
def test_sentiment_analysis_not_found():
    """
    Tests whether the app correctly returns the sentiment analysis from the GenAI model 
    """
    response = requests.post(f"{BASE_URL}/api/sentiment_analysis")
    assert response.status_code == 404

#extra-questions

# compile code error 400 

def test_explainer_invalid_question_id():
    """
    Tests whether the app correctly rejects accepting no inputs as message from the user during chat
    """
    data = { "session_id": 1 , "question_id": 9999} # message not there

    response = requests.post(f"{BASE_URL}/api/explainer", json=data)
    assert response.status_code == 404


def test_explainer_successful():
    """
    Tests whether the app correctly returns a response from the GenAI model when message is passed in the chat
    """
    data = {"question_id": 1, "session_id": 1} 
    response = requests.post(f"{BASE_URL}/api/explainer", json=data)
    assert response.status_code == 200
    assert str(response.json()["response"])
