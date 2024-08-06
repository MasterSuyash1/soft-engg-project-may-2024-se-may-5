import requests

# TODO / Need help With:

# 1. Currently, any user can access sentiment reports, SWOT reports. They should be accessible only to the authorized users
#    Right now, it will return 200 for all - for which I am testing. Need help with how to test for 401- user auth needs to be passed
# 2. Replicating 500 Internal Server Error
# 3. Compile and submit Code API endpoints. Need help with what happens when invalid syntax, etc are there
# 4. For users / login / signup test cases: need the user_id, username, password that are already there in the database to run cases

BASE_URL = "http://127.0.0.1:5000"

# region Test Cases for Users API
def test_delete_user_user_not_found():
    """
    Tests whether the code correctly rejects deleting a user which does not exist
    """
    user_id = -1
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 400

    user_id = 999999
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 404

def test_delete_user_successful():
    """
    Tests whether the code correctly deletes a user based on the ID
    """
    user_id = 1
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200

def test_get_users_successful():
    """
    Tests whether the app correctly returns the list of users
    """
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list) 

# endregion

# region Test Cases for Signup / Login API
def test_signup_empty_inputs():
    """
    Tests whether the app correctly rejects empty inputs
    """
    data = {"username": "", "email": "", "password": ""} # All empty inputs
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 400

    data = {"username": "someusername", "email": "someemail@email.com", "password": ""} # password empty
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 400    
    
    data = {"username": "", "email": "someemail@email.com", "password": "somepassword"} # Username empty
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 400

    data = {"username": "someusername", "email": "", "password": "somepassword"} # Email empty
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 400

def test_signup_invalid_input():
    """
    Tests whether the app correctly rejects invalid / incompatible inputs for the user registration
    """
    data = {"username": 123.4, "email": "someemail@email.com", "password": ""} # Invalid Username
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 400, "Invalid username got accepted"

    data = {"username": "username", "email": "someemail.com", "password": ""} # Invalid Username
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 400, "Invalid email got accepted"

def test_signup_duplicate_email():
    """
    Tests whether the app correctly rejects duplicate email during registration
    """
    data = {"username": "username", "email": "existing@email.com", "password": "somepassword"} # duplicate email
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 400

def test_signup_duplicate_username():
    """
    Tests whether the app correctly rejects duplicate username during registration
    """
    data = {"username": "existingusername", "email": "newemail@email.com", "password": "somepassword"} # duplicate username
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 400

def test_signup_successful():
    """
    Tests whether the app correctly accepts and registers a new user
    """
    data = {"username": "newusername", "email": "new@email.com", "password": "newpassword"}
    response = requests.post(f"{BASE_URL}/signup", data=data)
    assert response.status_code == 201

def test_login_empty_inputs():
    """
    Tests if the app correctly rejects empty inputs
    """
    data = {"email": "", "password": ""} # All empty
    response = requests.post(f"{BASE_URL}/login", data=data)
    assert response.status_code == 401
    
    data = {"email": "", "password": "somepassword"} # Email empty
    response = requests.post(f"{BASE_URL}/login", data=data)
    assert response.status_code == 401
    
    data = {"email": "someemail@email.com", "password": ""} # Password empty
    response = requests.post(f"{BASE_URL}/login", data=data)
    assert response.status_code == 401

def test_login_invalid_inputs():
    """
    Tests whether the app correctly accepts and logs in a new user
    """
    data = {"email": "usernameemail.com", "password": "somepassword"}
    response = requests.post(f"{BASE_URL}/users", data=data)
    assert response.status_code == 201

def test_login_invalid_credentials():
    """
    Tests whether the app correctly accepts and logs in a new user
    """
    data = {"email": "correctemail@email.com", "password": "wrongpassword"}
    response = requests.post(f"{BASE_URL}/users", data=data)
    assert response.status_code == 401
    assert str(response.json()['message']).upper() == "INVALID CREDENTIALS"
    assert str(response.json()['message']).upper() == "INVALID CREDENTIALS"

    data = {"email": "wrongemail@email.com", "password": "correctpassword"}
    response = requests.post(f"{BASE_URL}/users", data=data)
    assert response.status_code == 401

def test_login_successful():
    """
    Tests whether the app correctly accepts and logs in a new user
    """
    data = {"email": "username@email.com", "password": "somepassword"}
    response = requests.post(f"{BASE_URL}/users", data=data)
    assert response.status_code == 200
    assert str(response.json()['message']).upper() == "LOGIN SUCCESSFUL"

# endregion

# region Test cases for Ratings API

def test_submit_ratings_invalid_id():
    """
    Tests whether the code correctly rejects an invalid user_id such as -1
    """
    data = {
        "user_id": 1,
        "lesson_id" : 1,
        "audio": 4,
        "video": 4,
        "content": 4,
        "feedback": "Excellent tutorial!",
    }

    data["user_id"] = -1 # Invalid user_id
    response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
    assert response.status_code == 400, "Invalid user_id got accepted"
    
    data['user_id'] = 1 # reset

    data['lesson_id'] = -1 # invalid lesson_id
    response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
    assert response.status_code == 400, "Invalid lesson_id got accepted"

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

def test_lesson_transcript_invalid_input():
    """
    Tests whether the app correctly returns not found message when the lesson is not found
    """
    lesson_id = "abc" # Impossible lesson_id
    response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")
    assert response.status_code == 400

    lesson_id = 1.5 # Impossible lesson_id
    response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")
    assert response.status_code == 400
    
    lesson_id = "" # Empty Lesson id
    response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")
    assert response.status_code == 400

def test_lesson_transcript_invalid_input():
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
    data = { } # empty data

    response = requests.post(f"{BASE_URL}/api/chat", data=data)
    assert response.status_code == 400

def test_chat_api_successful_response():
    """
    Tests whether the app correctly returns a response from the GenAI model when message is passed
    """
    data = {"message": "Explain what hashing is to me."}
    response = requests.post(f"{BASE_URL}/api/chat", data=data)
    assert response.status_code == 200
    assert str(response.json()["response"])

def test_sentiment_analysis_successful():
    """
    Tests whether the app correctly returns the sentiment analysis from the GenAI model 
    """
    response = requests.get(f"{BASE_URL}/api/sentiment_analysis")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# endregion

# region Activity and Extra Questions Test Cases
def test_get_activity_invalid_inputs():
    """
    Tests getting activity questions with invalid inputs
    """
    lesson_id = -1 # lesson doesn't exist
    response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
    assert response.status_code == 404, "lesson_id not found failed"
    assert response.json()["error"]

    lesson_id = "abc" # Lesson id type is wrong
    response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
    assert response.status_code == 400, "Invalid lesson_id failed"

def test_get_activity_empty_inputs():
    """
    Tests getting activity questions with empty inputs
    """
    lesson_id = ""
    response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
    assert response.status_code == 400, "Empty lesson_id failed"

def test_get_activity_successful():
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

def test_post_graded_questions_successful():
    """
    Tests whether the app correctly accepts a graded submission and returns solutions
    """
    week_id = 1
    answers = { str(0): "answer" }
    data = { "user_id":1, "answers" :answers}
    response = requests.post(f"{BASE_URL}/api/graded/quiz/{week_id}", data=data)
    assert response.status_code == 200
    assert response.json()["results"]
    
    response_json = response.json()

    # TODO: Verify this code once. Supposed to check whether explanation is given for an incorrect answer
    incorrect_answers = [ i for i in response_json['results'] if not response_json['results'][i]['is_correct']] 
    if len(incorrect_answers) > 0:
        assert incorrect_answers[0]['explanation']

def test_post_graded_questions_more_answers_than_questions():
    """
    Tests whether the application correctly refutes the case where num of answers > num of questions.
    Basically, it will check whether the app correctly handles the case where an answer is submitted for a question that doesn't exist
    """
    week_id = 1
    answers = { str(i): f"answer_i" for i in range(100)}
    data = { "user_id":1, "answers" :answers}
    response = requests.post(f"{BASE_URL}/api/graded/quiz/{week_id}", data=data)
    assert response.status_code == 400

# TODO: Add test cases for invalid user_id, user_not_found, week_not_found, etc.

# endregion

# region Programming Questions Test Cases

def test_compile_code_successful():
    pass

def test_compile_code_syntax_error():
    pass

def test_submit_code_successful():
    """
    Tests whether the app correctly accepts a submitted code
    """

def test_submit_code_syntax_error():
    pass

def test_private_test_cases():
    # TODO: Private test cases are returned from the client. Client can cook up test cases and his submission will get accepted
    pass

def test_generate_hint_successful():
    """
    Tests whether the app correctly responds with a hint to a programming problem
    """
    data = { 
        "code": "def add(a, b): return a", 
        "language": "python",
        "question": "Write a python function to return sum of two numbers"
    }

    response = requests.post(f"{BASE_URL}/api/explainCode", data=data)
    assert response.status_code == 200
    assert response.json()['hint']

def test_efficient_solution_invalid_inputs():
    """
    Tests whether the app correctly rejects invalid inputs
    """
    data = { "question_id" : 99999 }

    response = requests.post(f"{BASE_URL}/api/getEfficientCode", data=data)
    assert response.status_code == 404, "Question not found failed"

    data['question_id'] = None
    response = requests.post(f"{BASE_URL}/api/getEfficientCode", data=data)
    assert response.status_code == 400, "Bad request failed"

    data['question_id'] = -1
    response = requests.post(f"{BASE_URL}/api/getEfficientCode", data=data)
    assert response.status_code == 400, "Bad request failed"

def test_efficient_solution_successful():
    """
    Tests whether the app correctly returns an efficient solution to the problem
    """
    data = { "question_id" : 1 }
    response = requests.post(f"{BASE_URL}/api/getEfficientCode", data=data)
    assert response.status_code == 200

# endregion

# region Weekly Performance Report API Test Cases

def test_weekly_performance_empty_inputs():
    """
    Tests whether the app correctly rejects empty inputs
    """
    data = {"user_id" : 1} # missing lesson_id
    response = requests.post(f"{BASE_URL}/api/weekly_performance", data=data)
    assert response.status_code == 400, "Missing lesson_id failed"

    data = {"lesson_id" : 1} # missing user_id
    response = requests.post(f"{BASE_URL}/api/weekly_performance", data=data)
    assert response.status_code == 400, "Missing user_id failed"

def test_weekly_performance_invalid_inputs():
    """
    Tests whether the app correctly rejects invalid inputs such as user_id and lesson_id
    """
    data = {"user_id" : -1, "lesson_id":1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance", data=data)
    assert response.status_code == 400, "Invalid user_id failed"

    data = {"user_id" : 1, "lesson_id":-1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance", data=data)
    assert response.status_code == 400, "Invalid lesson_id failed"

    data = {"user_id" : "abc", "lesson_id":-1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance", data=data)
    assert response.status_code == 400, "Invalid user_id failed"

def test_weekly_performance_successful_generation():
    """
    Tests whether the app returns the user weekly performance report successfully
    """
    data = {"user_id" : 1, "lesson_id":1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance", data=data)
    assert response.status_code == 200
    assert response.json()["performance"]
    assert response.json()["swot_analysis"]

def test_weekly_performance_successful_user_not_found():
    """
    Tests whether the app correctly returns not found for a user
    """
    data = {"user_id" : 99999, "lesson_id":1}
    response = requests.post(f"{BASE_URL}/api/weekly_performance", data=data)
    assert response.status_code == 404, "User not found failed"

def test_weekly_performance_successful_not_found():
    """
    Tests whether the app correctly returns not found for a user
    """
    data = {"user_id" : 1, "lesson_id":99999}
    response = requests.post(f"{BASE_URL}/api/weekly_performance", data=data)
    assert response.status_code == 404, "Lesson not found failed"

# endregion
