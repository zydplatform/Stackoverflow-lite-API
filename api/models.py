from flask import jsonify, request
import json, re, uuid
from db import DatabaseConnection

users = []
questions = []
answers = []

class User:
    def __init__(self, userId, username, password, email):
        self.userId = userId
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def register():
        info = request.get_json()

        username = info.get('username')
        email = info.get('email')
        password = info.get('password')
        userId = uuid.uuid4()

        if not username or username.isspace():
            return jsonify({'message': 'Username filed can not be empty.'}), 400

        if not email or email.isspace():
            return jsonify({'message': 'Email field can not be empty.'}), 400
        elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
            return jsonify({'message': 'Enter a valid email address.'}),400
        else:
            pass
            
        if not password or password.isspace():
            return jsonify({'message': 'Password field can not be left empty.'}), 400
        elif not re.match(r"[A-Z, a-z, 0-9, @#]", password):
            return jsonify({'message': 'Password must contain each one of these characters(A-Za-z0-9@#)'}), 400
        elif len(password) < 8:
            return jsonify({'message': 'Password must be at least 8 characters.'}), 400
        else:
            pass

        user = User(userId, username, email, password)
        users.append(user)

        db = DatabaseConnection()
        db.insert_users(userId, username, email, password)

        return jsonify({
            'User Id': userId,
            'Username': user.username,
            'message': '{} has registered succesfully.'.format(username)
        }), 200

    @staticmethod
    def login():
        info = request.get_json()

        username = info.get('username')
        password = info.get('password')

        if not username or username.isspace():
            return jsonify({
                'message': 'Enter a valid username.'
            }), 400
        if not password or password.isspace():
            return jsonify({
                'message': 'Enter a valid password.'
            }), 400

        db = DatabaseConnection()
        db.login(username, password)
        
        return jsonify({
            'message': '{} has logged in.'.format(username)
        }), 200

class Questions:
    def __init__(self, qn_id, details):
        self.questionId = qn_id
        self.details = details

    @staticmethod
    def post_question():
        info = request.get_json()

        questionId = len(questions)
        questionId += 1

        details = info.get('details')

        if not details or details.isspace():
            return jsonify({"message": "Enter a question"}), 400
        question = Questions(questionId, details)
        questions.append(question)
        return jsonify({
            'id': questionId,
            'question': question.__dict__,
            'message': 'Question added'}), 201

    @staticmethod
    def get_all_questions():
        if len(questions) == 0:
            return jsonify({'message': 'There are no questions yet.'}), 400

        db = DatabaseConnection()
        db.get_all_questions()
        if db.get_all_questions() == None:
            return jsonify({
                'message': 'There are no questions yet.'
            })
        
        return jsonify({
            'Questions': [question.__dict__ for question in questions],
            'message': 'Questions fetched successfully.'
        }), 200
    
    @staticmethod
    def get_one_question(questionId):
        try:
            if questionId > len(questions) or questionId <= 0:
                return jsonify({'message': 'Question doesn\'t exist.'}), 400
            qn = questions[questionId - 1]

            db = DatabaseConnection()
            db.get_one_question(questionId)

            return jsonify({
                'Answer': [answer.__dict__ for answer in answers if answer.questionId == questionId],
                'Question': qn.__dict__,
                'message': 'Questions fetched successfully'
            }), 200
        except TypeError:
            return jsonify({'message': 'Question Id must be a number.'}), 400
    
    @staticmethod
    def delete_question(questionId):
        try:
            if len(questions) == 0:
                return jsonify({'message': 'There are no questions to delete.'}), 400
            for question in questions:
                if questionId == question.questionId:
                    questions.remove(question)
                    return jsonify({'message': 'Question deleted.'}), 200
        except TypeError:
            return jsonify({'message': 'Question does not exist.'}), 400


class Answer:
    def __init__(self, qn_id, details):
        self.questionId = qn_id
        self.details = details

    @staticmethod
    def post_answer(questionId):
        info = request.get_json()

        details = info.get('details')

        try:
            if not details and details.isspace():
                return jsonify({'message': 'Please enter an answer'}), 400
            if len(questions) == 0:
                return jsonify({'messge': 'There are no questions yet.'}), 400
        
            question = questions[questionId - 1]
            answer = Answer(questionId, details)
            answers.append(answer)



            return jsonify({
                'Question': question.__dict__,
                'Answer': answer.__dict__,
                'message': 'Answer added succesfully'
            }), 201
        except IndexError:
            return jsonify({'message': 'The question does not exist.'}), 400

    @staticmethod
    def prefered_answer(questionId, answerId):
        pass