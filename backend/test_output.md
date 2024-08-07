============================= test session starts ==============================
platform linux -- Python 3.10.13, pytest-8.2.2, pluggy-1.5.0
rootdir: /workspaces/soft-engg-project-may-2024-se-may-5/backend
plugins: anyio-4.4.0
collected 41 items

test_apis.py ..FFFF.FF.FF..F.F....FFF.FFFFFF...F..FF..                   [100%]

=================================== FAILURES ===================================
___________________________ test_signup_empty_inputs ___________________________

    def test_signup_empty_inputs():
        """
        Tests whether the app correctly rejects empty inputs for user registration
        """
        data = {"username": "", "email": "", "password": ""} # All empty inputs
        response = requests.post(f"{BASE_URL}/signup", json=data)
>       assert response.status_code == 400
E       assert 201 == 400
E        +  where 201 = <Response [201]>.status_code

test_apis.py:45: AssertionError
__________________________ test_signup_invalid_input ___________________________

    def test_signup_invalid_input():
        """
        Tests whether the app correctly rejects incompatible inputs for the user registration
        """
        data = {"username": 123.4, "email": "someemail@email.com", "password": "somepassword"} # Invalid Username
        response = requests.post(f"{BASE_URL}/signup", json=data)
>       assert response.status_code == 400, "Invalid username got accepted"
E       AssertionError: Invalid username got accepted
E       assert 201 == 400
E        +  where 201 = <Response [201]>.status_code

test_apis.py:65: AssertionError
_________________________ test_signup_duplicate_email __________________________

    def test_signup_duplicate_email():
        """
        Tests whether the app correctly rejects duplicate email during registration
        """
        data = {"username": "newusername", "email": "user1@gmail.com", "password": "somepassword"} # duplicate email
        response = requests.post(f"{BASE_URL}/signup", json=data)
>       assert response.status_code in [400, 409]
E       assert 500 in [400, 409]
E        +  where 500 = <Response [500]>.status_code

test_apis.py:77: AssertionError
________________________ test_signup_duplicate_username ________________________

    def test_signup_duplicate_username():
        """
        Tests whether the app correctly rejects duplicate username during registration
        """
        data = {"username": "user123", "email": "newemail@email.com", "password": "somepassword"} # duplicate username
        response = requests.post(f"{BASE_URL}/signup", json=data)
>       assert response.status_code in [ 400, 409 ]
E       assert 500 in [400, 409]
E        +  where 500 = <Response [500]>.status_code

test_apis.py:85: AssertionError
___________________________ test_login_empty_inputs ____________________________

    def test_login_empty_inputs():
        """
        Tests if the app correctly rejects empty inputs for the user login
        """
        # data = {"email": "", "password": ""} # All empty
        # response = requests.post(f"{BASE_URL}/login", json=data)
        # assert response.status_code == 400
    
        data = {"email": "", "password": "somepassword"} # Email empty
        response = requests.post(f"{BASE_URL}/login", json=data)
>       assert response.status_code == 400
E       assert 401 == 400
E        +  where 401 = <Response [401]>.status_code

test_apis.py:105: AssertionError
________________________ test_login_invalid_credentials ________________________

    def test_login_invalid_credentials():
        """
        Tests whether the app correctly rejects invalid credentials when logging in
        """
        data = {"email": "newuser@email.com", "password": "wrongpassword"}
        response = requests.post(f"{BASE_URL}/users", json=data)
>       assert response.status_code == 401
E       assert 404 == 401
E        +  where 404 = <Response [404]>.status_code

test_apis.py:117: AssertionError
________________________ test_submit_ratings_invalid_id ________________________

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
>       assert response.status_code == 400, "Invalid user_id got accepted"
E       AssertionError: Invalid user_id got accepted
E       assert 201 == 400
E        +  where 201 = <Response [201]>.status_code

test_apis.py:153: AssertionError
______________________ test_submit_ratings_invalid_input _______________________

    def test_submit_ratings_invalid_input():
        """
        Tests whether the code correctly rejects invalid data types or missing data. Here,
        the audio rating is a float instead of an integer and the field 'feedback' is missing
        """
        data = {"user_id": 1, "lesson_id" : 1, "audio": 4.5, "video": 4, "content": 4}
        response = requests.post(f"{BASE_URL}/api/submit_rating", json=data)
>       assert response.status_code == 400, "Float rating did not get rejected"
E       AssertionError: Float rating did not get rejected
E       assert 201 == 400
E        +  where 201 = <Response [201]>.status_code

test_apis.py:168: AssertionError
____________________ test_lesson_transcript_invalid_inputs _____________________

    def test_lesson_transcript_invalid_inputs():
        """
        Tests whether the app correctly rejects incompatible input of lesson_id when trying to generate transcript for a lesson
        """
        lesson_id = "abc" # Incompatible lesson_id
        response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")
>       assert response.status_code == 400
E       assert 404 == 400
E        +  where 404 = <Response [404]>.status_code

test_apis.py:207: AssertionError
______________________ test_lesson_transcript_successful _______________________

    def test_lesson_transcript_successful():
        """
        Tests whether the app correctly handles transcript generation API
        """
        lecture_id = 1
        response = requests.get(f"{BASE_URL}/api/transcript_notes/{lecture_id}")
>       assert response.status_code == 200
E       assert 400 == 200
E        +  where 400 = <Response [400]>.status_code

test_apis.py:232: AssertionError
__________________ test_get_activity_questions_invalid_inputs __________________

    def test_get_activity_questions_invalid_inputs():
        """
        Tests getting activity questions with invalid inputs
        """
        lesson_id = -1 # lesson doesn't exist
        response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
        assert response.status_code in [ 400, 404], "lesson_id not found failed"
    
        lesson_id = "abc" # Lesson id type is wrong
        response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
>       assert response.status_code == 400, "Invalid lesson_id failed"
E       AssertionError: Invalid lesson_id failed
E       assert 404 == 400
E        +  where 404 = <Response [404]>.status_code

test_apis.py:284: AssertionError
___________________ test_get_activity_questions_empty_inputs ___________________

    def test_get_activity_questions_empty_inputs():
        """
        Tests getting activity questions with empty inputs
        """
        lesson_id = ""
        response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
>       assert response.status_code == 400, "Empty lesson_id failed"
E       AssertionError: Empty lesson_id failed
E       assert 404 == 400
E        +  where 404 = <Response [404]>.status_code

test_apis.py:292: AssertionError
____________________ test_get_activity_questions_successful ____________________

    def test_get_activity_questions_successful():
        """
        Tests getting activity questions successfully
        """
        lesson_id = 1
        response = requests.get(f"{BASE_URL}/api/activity/quiz/{lesson_id}")
>       assert response.status_code == 200
E       assert 404 == 200
E        +  where 404 = <Response [404]>.status_code

test_apis.py:300: AssertionError
___________________ test_get_graded_questions_week_not_found ___________________

    def test_get_graded_questions_week_not_found():
        """
        Tests whether the app correctly returns the week not found
        """
        week_id = 99999
        response = requests.get(f'{BASE_URL}/api/graded/quiz/{week_id}')
>       assert response.status_code == 404
E       assert 400 == 404
E        +  where 400 = <Response [400]>.status_code

test_apis.py:328: AssertionError
_________________ test_graded_questions_submissions_successful _________________

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
    
        # TODO: Verify this code once. Supposed to check whether explanation is given for an incorrect answer
>       incorrect_answers = [ i for i in response_json['results'] if not response_json['results'][i]['is_correct']]

test_apis.py:344: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

.0 = <list_iterator object at 0x7ea9d6d34b80>

>   incorrect_answers = [ i for i in response_json['results'] if not response_json['results'][i]['is_correct']]
E   TypeError: list indices must be integers or slices, not dict

test_apis.py:344: TypeError
_________ test_graded_questions_submission_more_answers_than_questions _________

    def test_graded_questions_submission_more_answers_than_questions():
        """
        Tests whether the application correctly refutes the case where num of answers > num of questions.
        Basically, it will check whether the app correctly handles the case where an answer is submitted for a question that doesn't exist
        """
        week_id = 1
        answers = { str(i): f"answer_i" for i in range(100)}
        data = { "user_id":1, "answers" :answers}
        response = requests.post(f"{BASE_URL}/api/graded/quiz/{week_id}", json=data)
>       assert response.status_code == 400
E       assert 200 == 400
E        +  where 200 = <Response [200]>.status_code

test_apis.py:357: AssertionError
_______________ test_graded_questions_submission_invalid_inputs ________________

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
    
        """
        Tests whether the app correctly compiles a valid python code
        """
        data = {
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
    
        response = requests.post(f"{BASE_URL}/api/compile", json=data)
>       assert response.status_code == 200
E       assert 400 == 200
E        +  where 400 = <Response [400]>.status_code

test_apis.py:397: AssertionError
________________________ test_compile_code_syntax_error ________________________

    def test_compile_code_syntax_error():
        """
        Tests whether the app correctly identifies errors in code such as syntax error passed by the client
        """
        data = {
            "code": "def add(a, b): return a+b;", # syntax error
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
    
        response = requests.post(f"{BASE_URL}/api/compile", json=data)
>       assert response.status_code == 200
E       assert 400 == 200
E        +  where 400 = <Response [400]>.status_code

test_apis.py:420: AssertionError
________________________ test_submit_code_syntax_error _________________________

    def test_submit_code_syntax_error():
        """
        Tests whether the app correctly identifies errors in code such as syntax error passed by the client
        """
        data = {
            "code": "def add(a, b): return a+b;", # syntax error
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
    
        response = requests.post(f"{BASE_URL}/api/submit", json=data)
        assert response.status_code == 200
>       assert response.json()['score'] == 0 # test cases should fail because of syntax error
E       assert 1 == 0

test_apis.py:444: AssertionError
____________________ test_efficient_solution_invalid_inputs ____________________

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
>       assert response.status_code == 400, "Bad request failed"
E       AssertionError: Bad request failed
E       assert 404 == 400
E        +  where 404 = <Response [404]>.status_code

test_apis.py:523: AssertionError
____________________ test_weekly_performance_invalid_inputs ____________________

    def test_weekly_performance_invalid_inputs():
        """
        Tests whether the app correctly rejects invalid inputs such as user_id and lesson_id for weekly performance report
        """
        data = {"user_id" : -1, "week_no":1}
        response = requests.post(f"{BASE_URL}/api/weekly_performance", json=data)
        assert response.status_code in [ 404, 400], "Invalid user_id failed"
    
        data = {"user_id" : 1, "week_no":-1}
        response = requests.post(f"{BASE_URL}/api/weekly_performance", json=data)
        assert response.status_code in [ 400, 404 ], "Invalid lesson_id failed"
    
        data = {"user_id" : "abc", "week_no":-1}
        response = requests.post(f"{BASE_URL}/api/weekly_performance", json=data)
>       assert response.status_code == 400, "Invalid user_id failed"
E       AssertionError: Invalid user_id failed
E       assert 404 == 400
E        +  where 404 = <Response [404]>.status_code

test_apis.py:563: AssertionError
________________ test_weekly_performance_successful_generation _________________

    def test_weekly_performance_successful_generation():
        """
        Tests whether the app returns the user weekly performance report successfully
        """
        data = {"user_id" : 1, "week_no":1}
        response = requests.post(f"{BASE_URL}/api/weekly_performance", json=data, headers = {'Content-Type': 'application/json'})
>       assert response.status_code == 200
E       assert 404 == 200
E        +  where 404 = <Response [404]>.status_code

test_apis.py:571: AssertionError
=========================== short test summary info ============================
FAILED test_apis.py::test_signup_empty_inputs - assert 201 == 400
FAILED test_apis.py::test_signup_invalid_input - AssertionError: Invalid user...
FAILED test_apis.py::test_signup_duplicate_email - assert 500 in [400, 409]
FAILED test_apis.py::test_signup_duplicate_username - assert 500 in [400, 409]
FAILED test_apis.py::test_login_empty_inputs - assert 401 == 400
FAILED test_apis.py::test_login_invalid_credentials - assert 404 == 401
FAILED test_apis.py::test_submit_ratings_invalid_id - AssertionError: Invalid...
FAILED test_apis.py::test_submit_ratings_invalid_input - AssertionError: Floa...
FAILED test_apis.py::test_lesson_transcript_invalid_inputs - assert 404 == 400
FAILED test_apis.py::test_lesson_transcript_successful - assert 400 == 200
FAILED test_apis.py::test_get_activity_questions_invalid_inputs - AssertionEr...
FAILED test_apis.py::test_get_activity_questions_empty_inputs - AssertionErro...
FAILED test_apis.py::test_get_activity_questions_successful - assert 404 == 200
FAILED test_apis.py::test_get_graded_questions_week_not_found - assert 400 ==...
FAILED test_apis.py::test_graded_questions_submissions_successful - TypeError...
FAILED test_apis.py::test_graded_questions_submission_more_answers_than_questions
FAILED test_apis.py::test_graded_questions_submission_invalid_inputs - assert...
FAILED test_apis.py::test_compile_code_syntax_error - assert 400 == 200
FAILED test_apis.py::test_submit_code_syntax_error - assert 1 == 0
FAILED test_apis.py::test_efficient_solution_invalid_inputs - AssertionError:...
FAILED test_apis.py::test_weekly_performance_invalid_inputs - AssertionError:...
FAILED test_apis.py::test_weekly_performance_successful_generation - assert 4...
=================== 22 failed, 19 passed in 73.39s (0:01:13) ===================
