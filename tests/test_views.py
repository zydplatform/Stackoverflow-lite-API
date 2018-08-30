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

        self.assertEqual(message['message'], 'kengowadaty has been registered succesfully.')
    
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

        self.assertEqual(message['message'], 'Username field can not be empty.')

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

        self.assertEqual(message['message'], 'Password field can not be left empty.')

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

        self.assertEqual(message['message'], 'Password must be at least 8 characters.')

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

        self.assertEqual(message['message'], 'This username already has an account.')

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
        pass

db.drop_tables()