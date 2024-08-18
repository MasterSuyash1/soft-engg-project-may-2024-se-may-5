============================= test session starts ==============================
platform linux -- Python 3.10.13, pytest-8.2.2, pluggy-1.5.0
rootdir: /workspaces/soft-engg-project-may-2024-se-may-5/backend
plugins: anyio-4.4.0
collected 40 items

test_apis.py ..FFFF.F..FF..F.......F..F.........F....                    [100%]

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

        lesson_id = 1.5 # Impossible lesson_id
        response = requests.get(f"{BASE_URL}/api/transcript_notes/{lesson_id}")
>       assert response.status_code == 400
E       assert 404 == 400
E        +  where 404 = <Response [404]>.status_code

test_apis.py:208: AssertionError
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

test_apis.py:285: AssertionError
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

test_apis.py:321: AssertionError
_____________________ test_weekly_performance_empty_inputs _____________________

    def test_weekly_performance_empty_inputs():
        """
        Tests whether the app correctly rejects empty inputs for weekly performance report
        """
        data = {"user_id" : 1} # missing week_no
        response = requests.post(f"{BASE_URL}/api/weekly_performance_analysis", json=data)
>       assert response.status_code in [ 400, 404], "Missing lesson_id failed"
E       AssertionError: Missing lesson_id failed
E       assert 500 in [400, 404]
E        +  where 500 = <Response [500]>.status_code

test_apis.py:499: AssertionError
=========================== short test summary info ============================
FAILED test_apis.py::test_signup_empty_inputs - assert 201 == 400
FAILED test_apis.py::test_signup_invalid_input - AssertionError: Invalid user...
FAILED test_apis.py::test_signup_duplicate_email - assert 500 in [400, 409]
FAILED test_apis.py::test_signup_duplicate_username - assert 500 in [400, 409]
FAILED test_apis.py::test_login_empty_inputs - assert 401 == 400
FAILED test_apis.py::test_submit_ratings_invalid_id - AssertionError: Invalid...
FAILED test_apis.py::test_submit_ratings_invalid_input - AssertionError: Floa...
FAILED test_apis.py::test_lesson_transcript_invalid_inputs - assert 404 == 400
FAILED test_apis.py::test_get_activity_questions_empty_inputs - AssertionErro...
FAILED test_apis.py::test_get_graded_questions_week_not_found - assert 400 ==...
FAILED test_apis.py::test_weekly_performance_empty_inputs - AssertionError: M...
=================== 11 failed, 29 passed in 61.91s (0:01:01) ===================
