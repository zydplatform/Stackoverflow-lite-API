import unittest
from api.views import app
import json

class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_add_question(self):
        question = dict(
            details = 'details'
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type = 'application/json',
            data = json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Question added')
    
    def test_add_question_empty_string(self):
        question = dict(
            details = ''
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type = 'application/json',
            data = json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Enter a question')

    def test_add_question_user_enters_a_space(self):
        question = dict(
            details = '  '
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type = 'application/json',
            data = json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Enter a question')

    def test_get_one_question(self):
        question = dict(
            details = 'This is my question'
        )
        self.tester.post(
            'api/v1/questions',
            content_type = 'application/json',
            data = json.dumps(question)
        )
        response = self.tester.get(
            'api/v1/questions/1',
            content_type = 'application/json',
            data = json.dumps(question)
        )
        
        self.assertEqual(response.status_code, 200)

    def test_to_get_all_questions(self):
        question = dict(
            details = 'This is my question?'
        )
        response = self.tester.get(
            'api/v1/questions',
            content_type = 'application/json',
            data = json.dumps(question)
        )

        self.assertEqual(response.status_code, 200)

class TestAnswers(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
    
    def test_post_answer(self):
        question = dict(
            details = 'What am I doing?'
        )
        answer = dict(
            details = 'Answer to the question.'
        )
        self.tester.post(
            'api/v1/questions',
            content_type = 'application/json',
            data = json.dumps(question)
        )
        response = self.tester.post(
            'api/v1/questions/1/answers',
            content_type = 'application/json',
            data = json.dumps(answer)
        )

        self.assertEqual(response.status_code, 201)
        

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        
    def test_login(self):
        user = dict(
            username = 'kengowada',
            password = 'ljdfngs'
        )
        response = self.tester.post(
            'api/v1/auth/login',
            content_type = 'application/json',
            data = json.dumps(user)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'kengowada has logged in.')

    def test_login_empty_string(self):
        user = dict(
            username = '',
            password = 'skjdbfaj'
        )
        response = self.tester.post(
            'api/v1/auth/login',
            content_type = 'application/json',
            data = json.dumps(user)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Enter a valid username.')

    def test_register_user(self):
        user = dict(
            username = 'kengo',
            email = 'kengo@gmail.com',
            password = 'kengowada'
        )
        response = self.tester.post(
            'api/v1/auth/signup',
            content_type = 'application/json',
            data = json.dumps(user)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'kengo has been registered succesfully.')

    def test_register_user_empty_username(self):
        user = dict(
            username = '',
            email = 'kengo@gmail.com',
            password = 'kengowada'
        )
        response = self.tester.post(
            'api/v1/auth/signup',
            content_type = 'application/json',
            data = json.dumps(user)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Username field can not be empty.')

    def test_register_user_empty_email(self):
        user = dict(
            username = 'kengo',
            email = '',
            password = 'kengowada'
        )
        response = self.tester.post(
            'api/v1/auth/signup',
            content_type = 'application/json',
            data = json.dumps(user)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Email field can not be empty.')

    def test_register_user_email_syntax(self):
        user = dict(
            username = 'kengo',
            email = 'kengo"asf.HDJ',
            password = 'kengowada'
        )
        response = self.tester.post(
            'api/v1/auth/signup',
            content_type = 'application/json',
            data = json.dumps(user)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Enter a valid email address.')

    def test_register_user_empty_password(self):
        user = dict(
            username = 'kengo',
            email = 'kengo@gamil.com',
            password = ''
        )
        response = self.tester.post(
            'api/v1/auth/signup',
            content_type = 'application/json',
            data = json.dumps(user)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Password field can not be left empty.')

    def test_register_user_password_syntax(self):
        user = dict(
            username = 'kengo',
            email = 'kengo@gmail.com',
            password = 'kengo'
        )
        response = self.tester.post(
            'api/v1/auth/signup',
            content_type = 'application/json',
            data = json.dumps(user)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Password must be at least 8 characters.')