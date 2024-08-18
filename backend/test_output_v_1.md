============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.3.2, pluggy-1.5.0
rootdir: /Users/alokdhangare/Asmita_IITM/SEPRO/SE_Project_Testing-anuj 4/backend
collected 46 items

test_apis.py ...............................F...........F..              [100%]

=================================== FAILURES ===================================
______________________ test_private_test_cases_successful ______________________

    def test_private_test_cases_successful():
        """
        Tests whether the app correctly verifies and refutes private test cases being passed by the client
        """
        data = {
            "code": "def add(a, b): return a+b",
            "user_id": 1,
            "question_id": 11
        }
    
        response = requests.post(f"{BASE_URL}/api/submit", json=data)
>       assert response.status_code == 200
E       assert 500 == 200
E        +  where 500 = <Response [500]>.status_code

test_apis.py:400: AssertionError
______________________ test_sentiment_analysis_not_found _______________________

    def test_sentiment_analysis_not_found():
        """
        Tests whether the app correctly returns the sentiment analysis from the GenAI model
        """
        response = requests.post(f"{BASE_URL}/api/sentiment_analysis")
>       assert response.status_code == 404
E       assert 200 == 404
E        +  where 200 = <Response [200]>.status_code

test_apis.py:535: AssertionError
=============================== warnings summary ===============================
../.venv/lib/python3.9/site-packages/urllib3/__init__.py:35
  /Users/alokdhangare/Asmita_IITM/SEPRO/SE_Project_Testing-anuj 4/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED test_apis.py::test_private_test_cases_successful - assert 500 == 200
FAILED test_apis.py::test_sentiment_analysis_not_found - assert 200 == 404
============== 2 failed, 44 passed, 1 warning in 71.01s (0:01:11) ==============
