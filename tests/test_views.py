import unittest
from api.views import app
import json
from db import DatabaseConnection

db = DatabaseConnection()


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client(self)

    def test_user_register(self):
        user = {
            'username': 'kengowadaty',
            'email': 'kengoty@email.com',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'],
                         'kengowadaty has been registered succesfully.')

    def test_user_register_empty_username(self):
        user = {
            'username': '',
            'email': 'kengoup@email.com',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'],
                         'Username field can not be empty.')

    def test_user_register_empty_password(self):
        user = {
            'username': 'kengoup',
            'email': 'kengoup@email.com',
            'password': ''
        }
        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'],
                         'Password field can not be left empty.')

    def test_user_register_empty_email(self):
        user = {
            'username': 'kengoup',
            'email': '',
            'password': 'okayokayokay'
        }
        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Email field can not be empty.')

    def test_user_register_email_syntax(self):
        user = {
            'username': 'kengoup',
            'email': '123jnskdfjns.com',
            'password': 'okayokayokay'
        }
        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Enter a valid email address.')

    def test_user_register_password_length(self):
        user = {
            'username': 'kengoup',
            'email': '123jns@kdfjns.com',
            'password': 'oka'
        }
        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'],
                         'Password must be at least 8 characters.')

    def test_user_register_username_exists(self):
        user = {
            'username': 'kengowadaty',
            'email': 'ken@email.com',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'],
                         'This username already has an account.')

    def test_user_register_email_exists(self):
        user = {
            'username': 'kengowa',
            'email': 'kengoty@email.com',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'This email is already taken.')

    def test_user_login(self):
        user_reg = {
            'username': 'kengowada132',
            'email': 'kengo132@email.com',
            'password': 'kengowada'
        }
        self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user_reg)
        )
        user = {
            'username': 'kengowada132',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'kengowada132 has logged in.')

    def test_user_login_empty_username(self):
        user_reg = {
            'username': 'kengo132wada',
            'email': '132kengo@email.com',
            'password': 'kengowada'
        }
        self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user_reg)
        )
        user = {
            'username': '',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Enter a valid username.')

    def test_user_login_empty_password(self):
        user_reg = {
            'username': 'kengoada',
            'email': '1kengo@email.com',
            'password': 'kengowada'
        }
        self.test_client.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user_reg)
        )
        user = {
            'username': 'kengoada',
            'password': ''
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Enter a valid password.')


class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client(self)

    def test_post_question(self):
        user = {
            'username': 'kengowadaty',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        question = {
            'question': 'My question?'
        }
        response1 = self.test_client.post(
            'api/v1/questions',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(question)
        )
        message = json.loads(response1.data.decode())
        self.assertEqual(message['Question'], 'My question?')

    def test_post_question_twice(self):
        user = {
            'username': 'kengowadaty',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        question = {
            'question': 'My question?'
        }
        self.test_client.post(
            'api/v1/questions',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(question)
        )

        response1 = self.test_client.post(
            'api/v1/questions',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(question)
        )
        message = json.loads(response1.data.decode())
        self.assertEqual(
            message['message'], 'Please be creative. You can not ask the same question twice.')

    def test_post_empty_question(self):
        user = {
            'username': 'kengowadaty',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        question = {
            'question': ''
        }
        response1 = self.test_client.post(
            'api/v1/questions',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(question)
        )
        message = json.loads(response1.data.decode())
        self.assertEqual(message['message'], 'Enter a question.')

    def test_get_question_no_question_db(self):
        user = {
            'username': 'kengowadaty',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        response1 = self.test_client.get(
            'api/v1/questions/78',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json'
        )
        message = json.loads(response1.data.decode())
        self.assertEqual(message['message'], 'Question doesn\'t exist')

    def test_get_question(self):
        user = {
            'username': 'kengowadaty',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        question = {
            'question': 'Okay another one.'
        }
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        self.test_client.post(
            'api/v1/questions',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(question)
        )

        response1 = self.test_client.get(
            'api/v1/questions/2',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json'
        )
        message = json.loads(response1.data.decode())
        self.assertEqual(message['message'], 'Question fetched succesfully.')

    def test_get_all_questions(self):
        user = {
            'username': 'kengowadaty',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        response1 = self.test_client.get(
            'api/v1/questions',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 201)

    def test_delete_question(self):
        user = {
            'username': 'kengowadaty',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        question = {
            'question': 'Okay another one.'
        }
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        self.test_client.post(
            'api/v1/questions',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(question)
        )

        delete = self.test_client.delete(
            'api/v1/questions/1',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json'
        )
        self.assertEqual(delete.status_code, 200)


class TestAnswers(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client(self)

    def post_answer(self):
        user = {
            'username': 'kengowadaty',
            'password': 'kengowada'
        }
        response = self.test_client.post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        question = {
            'question': 'Okay another one.'
        }
        access_token = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.test_client.post(
            'api/v1/questions',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(question)
        )

        answer = {
            'answer': 'My answer.'
        }
        post_ans = self.test_client.post(
            'api/v1/questions/1/answers',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(answer)
        )
        message = json.loads(post_ans.data.decode())

        self.assertEqual(message['message'], 'Please enter an answer.')


db.drop_tables()
