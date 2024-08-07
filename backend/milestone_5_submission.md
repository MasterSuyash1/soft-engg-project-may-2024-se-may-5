    - Passed Inputs:
        - ``` ```
    - Expected Output:
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 404```
    - Result: 
        - ``` ```

# User API Tests
**Description:** These APIs have functionality related to features such as registration, login, and retrieval of user data

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
    - ```
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
      ```

2. ```test_delete_user_successful()```
Tests the successful deletion of a user
    - Passed Inputs:
        - ```1```
    - Expected Output:
        - ```HTTP-Status Code: 200```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Passed```
      
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
        - ```
          [
            {
              "id": 1,
              "username": "johndoe",
              "email": "johndoe@example.com",
              "created_at": "2023-07-29T10:00:00Z"
            }
          ]
          ```
    - Actual Output:
        - ```HTTP-Status Code:200```
        - List of all the users in the database
    - Result: 
        - ```Passed```


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


# Lectures API Tests
**Description:** These APIs are for the functionalities related to lecture content such as submitting feedback, generating transcript, chatbot with GenAI, and sentiment analysis using GenAI. 

### Endpoint:
- **URL:** ```http://127.0.0.1:5000/api/submit_rating```
- **Method:** POST

1. ```def test_submit_ratings_invalid_id()```
Tests whether the app correctly rejects the submission of content ratings by a user who is not in the database
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
        - ```HTTTP-Status Code: 404```
    - Actual Output:
        - ```HTTP-Status Code: 200```
    - Result: 
        - ```Failed```

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
     
3. ```def test_submit_ratings_successful()```
Tests whether the app correctly accepts the content ratings when passed valid inputs
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
     
