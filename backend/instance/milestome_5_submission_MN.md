# User API Tests
**Description:** These APIs have functionality related to features such as registration, login, and retrieval of user data. They are for normal and other functionalities.

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/api/users/{user_id}```
- **Method:** DELETE

##### Test Cases:
1. ```test_delete_user_user_not_found()```
Tests deletion of a user which does not exist in the database
    - Passed Inputs:
        - ```user_id: 99999```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
        - ```"message": "user not found"```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_delete_user_user_not_found():
            user_id = 999999
            response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
            assert response.status_code == 404
        ```

2. ```test_delete_user_successful()```
Tests the successful deletion of a user
    - Passed Inputs:
        - ```"user_id" : 1```
    - Expected Output:
        - ```HTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_delete_user_successful():
            response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
            assert response.status_code == 200
        ```
### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/api/users```
- **Method:** GET

1. ```test_get_users_successful()```
Tests the retrieval of all the users
    - Passed Inputs:
        - ``` ```
    - Expected Output:
        - A List of all the users present in the database
        - ```HTTP-Status Code: 200```
        - ```JSON List of all users present```
    - Actual Output:
        - ```HTTP-Status Code:200```
        - List of all the users in the database
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_get_users_successful():
            response = requests.get(f"{BASE_URL}/api/users")
            assert response.status_code == 200

            response_data = response.json()
            assert isinstance(response_data, list) 
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/signup```
- **Method:** POST

1. ```def test_signup_empty_inputs()```
Tests whether the application correctly rejects invalid empty inputs during user registration
    - Passed Inputs:
        - ```
          {"username": "", "email": "", "password": ""}
          ```
    - Expected Output:
        - ```HTTP-Status Code: 400```
    - Actual Output:
        - ```HTTP-Status Code: 201```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_signup_empty_inputs():
            response = requests.post(f"{BASE_URL}/signup", json=data)
            assert response.status_code == 400
        ```
    - Screenshot of Issue:
          ![Screenshot of Empty Inputs Issue](https://drive.google.com/uc?id=1fTMU26X0RFB0dMXU1kgzgLX_ZH-m3WUl)
    
2. ```def test_signup_invalid_input()``` 
Tests whether the app correctly rejects invalid inputs such as invalid email or username during user registration
    - Passed Inputs:
        - ```{"username": 123.4, "email": "someemail@email.com", "password": "somepassword"}```
    - Expected Output:
        - ```HTTTP-Status Code: 400```
    - Actual Output:
        - ```HTTP-Status Code: 201```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_signup_invalid_input():
            response = requests.post(f"{BASE_URL}/signup", json=data)
            assert response.status_code == 400, "Invalid username got accepted"
        ```
    - Screenshot of Issue:
          ![Screenshot of Empty Inputs Issue](https://drive.google.com/uc?id=1rsGj4Qohb-22HsB9AcmbkhtHCENk8UYy)

3. ```def test_signup_duplicate_email()```
Tests whether the app correctly handles rejecting duplicate email during user registration
    - Passed Inputs:
        - ```{"username": "newusername", "email": "existing@gmail.com", "password": "somepassword"}```
    - Expected Output:
        - ```HTTTP-Status Code: 400 ``` or ```409```
    - Actual Output:
        - ```HTTP-Status Code: 500```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_signup_duplicate_email():
            response = requests.post(f"{BASE_URL}/signup", json=data)
            assert response.status_code in [400, 409]
        ```
    - Screenshot of the Issue:
    ![Screenshot of Duplicate email](https://drive.google.com/uc?id=1G_8nDXawyLcqkHHn8lVNWhPxuNVqX5kj)

4. ```def test_signup_successful()```
Tests whether the user can successfully signup after passing valid inputs
    - Passed Inputs:
        - ```{"username": "newusername", "email": "newuser@email.com", "password": "newpassword"}```
    - Expected Output:
        - ```HTTTP-Status Code: 201```
    - Actual Output:
        - ```HTTP-Status Code: 201```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_signup_successful():
            response = requests.post(f"{BASE_URL}/signup", json=data)
            assert response.status_code == 201
        ```

### Endpoint: 
- **URL:** ```http://127.0.0.1:5000/login```
- **Method:** POST

1. ```def test_login_empty_inputs()```
Tests whether the app correctly refutes empty inputs when the user tries to login
    - Passed Inputs:
        - ```{"email": "", "password": ""}```
    - Expected Output:
        - ```HTTTP-Status Code: 400```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_login_empty_inputs():
            response = requests.post(f"{BASE_URL}/login", json=data)
            assert response.status_code == 400
        ```

2. ```def test_login_invalid_credentials()```
Tests whether the app correctly rejects invalid username-password combination when the user tries to login
    - Passed Inputs:
        - ```{"email": "newuser@email.com", "password": "wrongpassword"}```
    - Expected Output:
        - ```HTTTP-Status Code: 401```
    - Actual Output:
        - ```HTTP-Status Code: 401```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_login_invalid_credentials():
            response = requests.post(f"{BASE_URL}/login", json=data)
            assert response.status_code == 401
            assert str(response.json()['message']).upper() == "INVALID CREDENTIALS"
        ```      

3. ```def test_login_successful():```
Tests whether the app lets the user log in if he gives correct credentials
    - Passed Inputs:
        - ```{"email": "newuser@email.com", "password": "newpassword"}```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_login_successful():
            response = requests.post(f"{BASE_URL}/login", json=data)
            assert response.status_code == 200
            assert str(response.json()['message']).upper() == "LOGIN SUCCESSFUL"
        ```


# Lectures API Tests
**Description:** These APIs are for the functionalities related to lecture video content such as submitting feedback and generating transcript. API's for chatbot using GenAI and generating sentiment analysis using GenAI. 

### Endpoint:
- **URL:** ```http://127.0.0.1:5000/api/submit_rating```
- **Method:** POST

1. ```def test_submit_ratings_invalid_id()```
Tests whether the app correctly rejects the submission of lecture video content ratings by a user who is not in the database
    - Passed Inputs:
        - ```
          {
          "user_id": 99999,
          "lesson_id" : 1,
          "audio": 4,
          "video": 4,
          "content": 4,
          "feedback": "Excellent tutorial!",
          }
          ```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_submit_ratings_invalid_id():
            response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
            assert response.status_code == 400, "Invalid user_id got accepted"
        ```
    - Screenshot of the Issue:
    ![Image of invalid user_id getting accepted](https://drive.google.com/uc?id=19xcFy5PhDbSRRm3ziwlp5lwdiGJeolN2)

2. ```def test_submit_ratings_invalid_inputs()```
Tests whether the app correctly rejects the incompatible inputs for the user rating 
    - Passed Inputs:
        - ```
          {
          "user_id": 1,
          "lesson_id" : 1,
          "audio": 4.5,
          "video": 4,
          "content": 4,
          "feedback": "Excellent tutorial!",
          }
          ```
    - Expected Output:
        - ```HTTTP-Status Code: 400```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_submit_ratings_invalid_input():
            response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
            assert response.status_code == 400, "Float rating did not get rejected"
        ```
    - Screenshot of the Issue:
    ![Image of invalid user_id getting accepted](https://drive.google.com/uc?id=19xcFy5PhDbSRRm3ziwlp5lwdiGJeolN2)

     
3. ```def test_submit_ratings_successful()```
Tests whether the app correctly accepts the lecture video content ratings when passed valid inputs
    - Passed Inputs:
        - ```
          {
          "user_id": 1,
          "lesson_id" : 1,
          "audio": 4,
          "video": 4,
          "content": 4,
          "feedback": "Excellent tutorial!",
          }
          ```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_submit_ratings_successful():
            response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
            assert response.status_code == 201
            assert str(response.json()["message"]).upper() == "RATING SUBMITTED SUCCESSFULLY"
        ```

### Endpoint:
- **URL:** ```http://127.0.0.1:5000/api/transcript_notes{lesson_id}```
- **Method:** POST

1. ```def test_lesson_transcript_invalid_inputs()```
Tests whether the app correctly rejects invalid lesson_id, such as an empty lesson_id when generating video lecture transcripts for the lesson.
    - Passed Inputs:
        - 
        ``` 
        {"lesson_id": ""}
        ```
    - Expected Output:
        - ```HTTTP-Status Code: 400``` or ```404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_lesson_transcript_invalid_inputs():
            response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")
            assert response.status_code == 404
        ```

2. ```def test_lesson_transcript_not_found()```
Tests whether the app correctly returns 'not found' error when the lesson_id is not found in the database when generating video lecture transcripts for the lesson.
    - Passed Inputs:
        - 
        ```
        {"lesson_id" : 99999}
        ```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
            def test_lesson_transcript_not_found():
                response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")
                assert response.status_code == 404
        ```

3. ```def test_lesson_transcript_successful()```
    - Passed Inputs:
        - 
        ```
        {"lesson_id":1}
        ```
    - Expected Output:
        - 
        ```
        HTTTP-Status Code: 200
        JSON Parameter "transcript_text"
        JSON Parameter "notes"
        ```
    - Actual Output:
        - 
        ```
        HTTTP-Status Code: 200
        JSON Parameter "transcript_text"
        JSON Parameter "notes"
        ```
    - Result: 
        -
        ```Passed```
    - Pytest Code:
        ```
        def test_lesson_transcript_successful():
            response = requests.get(f"{BASE_URL}/api/transcript_notes/{lecture_id}")
            assert response.status_code == 200
            assert response.json()['transcript_text']
            assert response.json()['notes']
        ```

### Endpoint:
- **URL:** ```http://127.0.0.1:5000/api/chat```
- **Method:** POST

1. ```def test_chat_api_empty_chat_message()```
Tests whether the app correctly rejects no inputs in message from the user during chat with chatbot using GenAI.
    - Passed Inputs:
        - ```{ "session_id": 1 , "message": ""} # message not there```
    - Expected Output:
        - ```HTTTP-Status Code: 400  # Bad Request```
    - Actual Output:
        - ```HTTP-Status Code: 500```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_chat_api_empty_chat_message():
            response = requests.post(f"{BASE_URL}/api/chat", json=data)
            assert response.status_code in [ 400, 415, 500 ]
        ```

2. ```def test_chat_api_empty_session_id()```
Tests whether the app correctly creates a session_id internally when a session_id is not provided as input to the chat API.
    - Passed Inputs:
        - ```{"message": "Explain what hashing is to me.", "session_id": None} # session_id is not there```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_chat_api_empty_session_id():
            data = {"message": "Explain what hashing is to me.", "session_id": None} # session_id is not there
            response = requests.post(f"{BASE_URL}/api/chat", json=data)
            assert response.status_code == 200
            assert str(response.json()["response"])
        ```

3. ```def test_chat_api_successful()```
Tests whether the app correctly returns a response from the GenAI model when a valid message (not blank) from the student is passed in the chat.
    - Passed Inputs:
        - ```{"message": "Explain what hashing is to me.", "session_id": 1}```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_chat_api_successful():
            data = {"message": "Explain what hashing is to me.", "session_id": 1} 
            response = requests.post(f"{BASE_URL}/api/chat", json=data)
            assert response.status_code == 200
            assert str(response.json()["response"])
        ```

### Endpoint:
- **URL:** ```http://127.0.0.1:5000/api/sentiment_analysis```
- **Method:** POST

1. ```def test_sentiment_analysis_successful()```
Tests whether the app correctly returns the sentiment analysis from the GenAI model for the feedbacks submitted by the students about the quality of lecture videos. 
    - Passed Inputs:
        - ``` ```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_sentiment_analysis_successful():
            response = requests.post(f"{BASE_URL}/api/sentiment_analysis")
            assert response.status_code == 200
            assert isinstance(response.json()["lecture_feedback_summaries"], list)
        ```

# Activity and Extra Questions API
**Description:** These APIs have functionality related to generation of Activity Questions from the database for student's testing to fetch explanation from GenAI for incorrect answers. The API also contains functionality to generate Extra Practice questions using GenAI Model.

### Endpoint
- **URL:** ```http://127.0.0.1:5000/api/activity/quiz/<int:lesson_id>```
- **Method:** GET

1. ```def test_get_activity_questions_invalid_inputs()```
Tests getting activity questions with invalid inputs
    - Passed Inputs:
        - ``` ```
    - Expected Output:
        - ```HTTTP-Status Code: 404``` or ```400```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_get_activity_questions_invalid_inputs():
            lesson_id = -1 # lesson doesn't exist
            response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
            assert response.status_code in [ 400, 404], "lesson_id not found failed"
        ```

2. ```def test_get_activity_questions_empty_inputs()```
Tests getting activity questions with invalid inputs
    - Passed Inputs:
        - ``` ```
    - Expected Output:
        - ```HTTTP-Status Code: 404``` or ```400```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_get_activity_questions_empty_inputs():
            lesson_id = ""
            response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
            assert response.status_code == 404, "Empty lesson_id failed"
        ```

3. ```def test_get_activity_questions_successful()```
Tests getting activity questions successfully
    - Passed Inputs:
        - ``` ```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_get_activity_questions_successful():
            lesson_id = 1
            response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
            assert response.status_code == 200
        ```

### Endpoint
- **URL:** ```http://127.0.0.1:5000/api/activity/quiz/<int:lesson_id>```
- **Method:** POST

1. ```def test_post_activity_questions_successful()```
Tests whether the activity questions solved by the student can be submitted successfully.
    - Passed Inputs:
          ```
          { "user_id":1, "answers" : { str(0): "answer", str(1) : "wronganswer" }}
          ```
    - Expected Output:
        - 
        ```
        HTTTP-Status Code: 200
        JSON Parameter "results"
        ```
    - Actual Output:
        - 
        ```
        HTTTP-Status Code: 200
        JSON Parameter "results"
        ```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_post_activity_questions_successful():
            lesson_id = 1
            response = requests.post(f"{BASE_URL}/api/activity/quiz/{lesson_id}", json=data)
            assert response.status_code == 200
            assert response.json()["results"]
            
            response_json = response.json()

            incorrect_answers = [ response_json['results'][i] for i in range(len(response_json['results'])) if not response_json['results'][i]['is_correct']] 
            if len(incorrect_answers) > 0:
                assert incorrect_answers[0]['explanation']
        ```

2. ```def test_post_activity_questions_invalid_user_id()```
Tests whether the app returns not found error or bad request error when the user_id is incorrectly given.
    - Passed Inputs:
          ```
          { "user_id":99999, "answers" : { str(0): "answer", str(1) : "wronganswer" }}
          ```
    - Expected Output:
        - ```HTTTP-Status Code: 400``` or ```404```
    - Actual Output:
        -```HTTTP-Status Code: 200```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_post_activity_questions_invalid_user_id():
            lesson_id = 1
            response = requests.post(f"{BASE_URL}/api/activity/quiz/{lesson_id}", json=data)
            assert response.status_code == 404
        ```

3. ```def test_post_activity_questions_invalid_lesson_id()```
Tests whether the app returns not found error or bad request error when the lesson_id is incorrectly given.
    - Passed Inputs:
          ```
          { "user_id":1, "answers" : { str(0): "answer", str(1) : "wronganswer" }}
          ```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        -```HTTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_post_activity_questions_invalid_lesson_id():
            lesson_id = 99999
            response = requests.post(f"{BASE_URL}/api/activity/quiz/{lesson_id}", json=data)
            assert response.status_code == 404
        ```

### Endpoint
- **URL:** ```http://127.0.0.1:5000/api/activity/extra_questions/<int:lesson_id>```
- **Method**: GET

1. ```def test_get_extra_questions_successful()```
Tests whether the app correctly fetches extra questions from GenAI model when prompted by the student/client.
    - Passed Inputs:
        - ``` ```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_get_activity_questions_successful():
            lesson_id = 1
            response = requests.get(f"{BASE_URL}/api/activity/extra_questions/{lesson_id}")
            assert response.status_code == 200
        ```
2. ```def test_get_extra_questions_not_found()```
Tests whether the app correctly returns not found error during generating extra questions when given incorrect lesson_id.
    - Passed Inputs:
        - ``` ```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_get_activity_questions_successful():
            lesson_id = 99999
            response = requests.get(f"{BASE_URL}/api/activity/extra_questions/{lesson_id}")
            assert response.status_code == 404
        ```

# Graded Questions API
**Description:** These APIs have functionality related to generation of Graded Questions from the database for student's testing. There is also a component to fetch explanation from GenAI for incorrect answers.

### Endpoint
- **URL:** ```http://127.0.0.1:5000/api/graded/quiz/{week_id}```
- **Method**: GET

1. ```test_get_graded_questions_successful()```
Tests whether the graded questions for a given week are correctly returned
    - Passed Inputs:
        - ```{"week_id" : 1}```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_get_graded_questions_successful():
            week_id = 1
            response = requests.get(f'{BASE_URL}/api/graded/quiz/{week_id}')
            assert response.status_code == 200
            assert response.json()['quiz_data']
        ```

2. ```test_graded_questions_week_not_found()```
Tests whether the application correctly returns a 404 error if a given week_id is not present when finding graded assignment questions.

    - Passed Inputs:
        - ```{"week_id" : 99999}```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 400```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_get_graded_questions_week_not_found():
            week_id = 99999
            response = requests.get(f'{BASE_URL}/api/graded/quiz/{week_id}')
            assert response.status_code == 404
        ```
    - Screenshot of the Issue:
    ![Image of incorrect status codes issue](https://drive.google.com/uc?id=1F39rO6SpIk6e0TcE0KD_aJ7SO53DbtsB)
    
### Endpoint
- **URL:** ```http://127.0.0.1:5000/api/graded/quiz/{week_id}```
- **Method**: POST

1. ```test_graded_questions_submissions_successful()```
Tests whether the app correctly accepts a graded submission and returns solutions along with explanations for incorrect answers.
    - Passed Inputs:
        - ```{"week_id" : 1, "answers": { "0": "answer", "1" : "wronganswer", "user_id" : 1 }}```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_graded_questions_submissions_successful():
            response = requests.post(f"{BASE_URL}/api/graded/quiz/{week_id}", json=data)
            assert response.status_code == 200
            assert response.json()["results"]
            response_json = response.json()
            incorrect_answers = [ response_json['results'][i] for i in range(len(response_json['results'])) if not response_json['results'][i]['is_correct']] 
            if len(incorrect_answers) > 0:
                assert incorrect_answers[0]['explanation']
        ```
    

2. ```test_graded_questions_submission_invalid_input()```
Tests whether the app correctly returns not found error when passed invalid inputs.
    - Passed Inputs:
        - ```{"week_id" : 1, "answers": { "0": "answer", "1" : "wronganswer", "user_id" : 99999 }}```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 400```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_graded_questions_submission_invalid_inputs():
            user_id = 99999
            data = { "user_id":user_id, "answers" :answers}
            response = requests.post(f"{BASE_URL}/api/graded/quiz/{week_id}", json=data)
            assert response.status_code in [400, 404]
        ```
   - Screenshot of the Issue:
    ![Image of incorrect status codes issue](https://drive.google.com/uc?id=1F39rO6SpIk6e0TcE0KD_aJ7SO53DbtsB)

# Programming Questions API 
**Description:** These APIs have functionality related to generation of Programming Questions from the database for student's testing. Complilation of the code upon submission, testing private test cases and scoring. There is also a component to get hint/code explanation and efficient code from GenAI model.

### Endpoint
- **URL:** ```http://127.0.0.1:5000/api/compile```
- **Method:** POST

1. ```def test_compile_code_successful()```
Tests whether the app correctly compiles a valid python code submitted by the student/client.
    - Passed Inputs:
        - 
        ``` 
            {
                "code": "def add(a, b): return a+b", 
                "language": "python",
                "public_test_cases": [
                    {
                    "input": [
                        1,
                        2
                    ],
                    "expected_output": 3 
                    }
                ],
                "user_id": 1,
                "question_id": 1
            }
        ```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_compile_code_successful():
            response = requests.post(f"{BASE_URL}/api/compile", json=data)
            assert response.status_code == 200
        ```

2. ```def test_compile_code_erroneous_code()```
Tests whether the app correctly identifies errors in code such as syntax error passed by the client. This error is identified and should be returned to the client.
    
    - Passed Inputs:
        - 
        ``` 
            {
                "code": "def add(a, b): return a+c", # NameError
                "language": "python",
                "public_test_cases": [
                    {
                    "input": [
                        1,
                        2
                    ],
                    "expected_output": 3 
                    }
                ],
                "user_id": 1,
                "question_id": 1
            }
        ```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_compile_code_syntax_error():
            response = requests.post(f"{BASE_URL}/api/compile", json=data)
            assert response.status_code == 200
        ```


### Endpoint
- **URL:** ```http://127.0.0.1:5000/api/submit```
- **Method:** POST

1. ```def test_submit_code_erroneous_code()```
Tests whether the app correctly identifies errors such as name error in the code passed by the student/client when submitting the code, and verifies that the private test cases are not passed.

    - Passed Inputs:
        - 
        ``` 
        {
            "code": "def add(a, b): return a+c", # NameError
            "language": "python",
            "private_test_cases": [
                {
                "input": [
                    1,
                    2
                ],
                "expected_output": 3 
                }
            ],
            "user_id": 1,
            "question_id": 1
        }
        ```
    - Expected Output:
        - 
        ```
            HTTTP-Status Code: 200
            "score" : 0
        ```
    - Actual Output:
        - 
        ```
            HTTTP-Status Code: 200
            "score" : 0
        ```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_submit_code_syntax_error():
            response = requests.post(f"{BASE_URL}/api/submit", json=data)
            assert response.status_code == 200
            assert response.json()['score'] == 0
        ```

2. ```def test_private_test_cases_successful()```
Tests whether the app correctly accepts a correct programming code submitted by the student/client and correctly returns the score of the passed private test cases.

    - Passed Inputs:
        - 
        ``` 
        {
            "code": "def add(a, b): return a+b",
            "language": "python",
            "private_test_cases": [
                {
                "input": [
                    1,
                    2
                ],
                "expected_output": 3
                }
            ],
            "user_id": 1,
            "question_id": 1
        }
        ```
    - Expected Output:
        -
        ```
        HTTTP-Status Code: 200
        "score": 1
        ```
    - Actual Output:
        - 
        ```
        HTTP-Status Code: 200
        "score" : 1
        ```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_private_test_cases_successful():
            response = requests.post(f"{BASE_URL}/api/submit", json=data)
            assert response.status_code == 200
            assert response.json()['score'] == 1 
        ```
    
### Endpoint:
- **URL:** ```http://127.0.0.1:5000/api/explainCode```
- **Method:** Post

1. ```def test_generate_hint_successful()```
Tests whether the app correctly responds with a hint from GenAI model to a programming problem when requested by the student/client. This is the Code Explainer feature of the user story.
    - Passed Inputs:
        - 
        ```
        { 
            "code": "def add(a, b): return a", 
            "language": "python",
            "question": "Write a python function to return sum of two numbers"
        }        
        ```
    - Expected Output:
        - 
        ```
        HTTTP-Status Code: 200
        A JSON Parameter: "hint"
        ```
    - Actual Output:
        -     
        ```
        HTTP-Status Code: 200
        Json Parameter: "hint"
        ```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_generate_hint_successful():
            response = requests.post(f"{BASE_URL}/api/explainCode", json=data)
            assert response.status_code == 200
            assert response.json()['hint']
        ```

    
### Endpoint:
- **URL:** ```http://127.0.0.1:5000/api/getEfficientCode```
- **Method:** Post

1. ```def test_efficient_solution_invalid_inputs()```
Tests whether the app correctly rejects invalid inputs when requesting efficient programming code solution from GenAI model by the student/client.
    - Passed Inputs:
        - ```{ "question_id": 99999 }```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_efficient_solution_invalid_inputs():
            response = requests.post(f"{BASE_URL}/api/getEfficientCode", json=data)
            assert response.status_code == 404, "Question not found failed"
        ``` 

    
2. ```def test_efficient_solution_successful()```
Tests whether the app correctly returns an efficient programming code solution from GenAI model when requested by the student/client.
    - Passed Inputs:
        - ```{ "question_id": 1 }```
    - Expected Output:
        - ```HTTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_efficient_solution_invalid_inputs():
            data = { "question_id" : 1 }
            response = requests.post(f"{BASE_URL}/api/getEfficientCode", json=data)
            assert response.status_code == 200
        ``` 
    


# Weekly Performance API
**Description:** These APIs have functionality related to generation of Student Weekly Performance report from GenAI model.

### Endpoint:
- **URL:** ```http://127.0.0.1:5000/api/weekly_performance_analysis```
- **Method:** POST

1. ```def test_weekly_performance_empty_inputs()```
Tests whether the app correctly rejects empty/missing inputs for weekly performance report.
    
    - Passed Inputs:
        - ``` {"user_id" : 1} # missing week_no ```
    - Expected Output:
        - ```HTTTP-Status Code: 400```
    - Actual Output:
        - ```HTTP-Status Code: 500```
    - Result: 
        - ```Failed```
    - Pytest Code:
        ```
        def test_weekly_performance_empty_inputs():
            response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
            assert response.status_code in [ 400 ], "Missing week_no failed"
        ```
    - Screenshot of the Issue:
    ![Screenshot of the missing input in performance issue](https://drive.google.com/uc?id=1kYju8nAZBwId0aSpFGJwU5N3lEmUH7aj)

2. ```def test_weekly_performance_invalid_inputs()```
Tests whether the app correctly rejects invalid inputs such as user_id and week_no for weekly performance report.
    - Passed Inputs:
        - ```{"user_id" : -1, "week_no":1}```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_weekly_performance_invalid_inputs():
            response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
            assert response.status_code in [ 404, 400], "Invalid user_id failed"
        ```

3. ```def test_weekly_performance_successful_generation()```
Tests whether the app returns the user weekly performance report successfully, and returns the SWOT analysis using GenAI model.
    - Passed Inputs:
        - ```{"user_id" : 1, "week_no":1}```
    - Expected Output:
        - 
        ```
        HTTTP-Status Code: 200
        JSON Parameter: "performance"
        JSON Parameter: "swot_analysis"
        ```
    - Actual Output:
        -
        ```
        HTTTP-Status Code: 200
        JSON Parameter: "performance"
        JSON Parameter: "swot_analysis"
        ```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_weekly_performance_successful_generation():
            response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
            assert response.status_code == 200
            assert response.json()["performance"]
            assert response.json()["swot_analysis"]
        ```

4. ```def test_weekly_performance_successful_user_not_found()```
Tests whether the app correctly returns 'not found' for a user not in the database for weekly performance report.
    - Passed Inputs:
        - ```{"user_id" : 99999, "week_no":1}```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ```Passed```
    - Pytest Code:
        ```
        def test_weekly_performance_successful_user_not_found():
            response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
            assert response.status_code == 404, "User not found failed"
        ```
