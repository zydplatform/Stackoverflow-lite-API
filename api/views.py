from flask import Flask, request, jsonify
import json
import uuid
import re
from db import DatabaseConnection
from api.models import User, Answer, Questions
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'KenG0W@Da4!'

db = DatabaseConnection()

@app.route('/api/v1/questions', methods=['POST'])
@jwt_required
def post_question():
    username = get_jwt_identity()
    info = request.get_json()

    question = info.get('question')

    if not question or question.isspace():
        return jsonify({'message': 'Enter a question.'}), 400

    db = DatabaseConnection()
    db.insert_question(question, username[0])

    return jsonify({
        'Question': question
    }), 201


@app.route('/api/v1/questions', methods=['GET'])
@jwt_required
def get_all_questions():
    db = DatabaseConnection()
    question_db = db.get_all_questions()

    if question_db == None:
        return jsonify({
            'message': 'There are no questions yet.'
        }), 400
    else:
        return jsonify({
            'Question': [question for question in question_db]
        }), 201


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
@jwt_required
def post_answer(questionId):
    try:
        info = request.get_json()
        userId = get_jwt_identity()

        details = info.get('details')

        if not details and details.isspace():
            return jsonify({'message': 'Please enter an answer'}), 400
        if not isinstance(details, str):
            return jsonify({'message': 'Only strings allowed for answers.'})

        db = DatabaseConnection()
        db.insert_answer(details, userId[0], questionId)

        return jsonify({
            'message': 'Answer added succesfully.'
        }), 201
    except IndexError:
        return jsonify({'message': 'The question does not exist'}), 400


@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
@jwt_required
def get_one_qn(questionId):
    try:
        db = DatabaseConnection()
        question = db.get_one_question(questionId)
        answers = db.get_answers(questionId)

        print(type(answers))

        if question == None:
            return jsonify({'message': 'Question doesn\'t exist'}), 400

        return jsonify({
            'Question': question,
            'Answer': [answer for answer in answers],
            'message': 'Question fetched succesfully.',
        }), 200
    except TypeError:
        return jsonify({'message': 'Question Id must be a number.'}), 400


@app.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId):
    try:
        username = get_jwt_identity()

        db = DatabaseConnection()
        question = db.get_one_question(questionId)

        if question[2] == username[0]:
            db.delete_question(questionId, username)
            return jsonify({'message': 'Question deleted succesfully.'})
        else:
            return jsonify({'message': 'You don\'t have permission to delete this question.'})
    except TypeError:
        return jsonify({'message': 'Question does not exist.'}), 400


@app.route('/api/v1/auth/login', methods=['POST'])
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
    user = db.login(username)

    if check_password_hash(user[3], password) and user[1] == username:
        access_token = create_access_token(identity=username)
        return jsonify({
            'token': access_token,
            'message': '{} has logged in.'.format(username)
        }), 200
    else:
        return jsonify({'message': 'Wrong login credentials.'}), 400


@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    info = request.get_json()

    username = info.get('username')
    email = info.get('email')
    password = info.get('password')
    userId = uuid.uuid4()
    password_hash = generate_password_hash(password, method='sha256')

    if not username or username.isspace():
        return jsonify({'message': 'Username field can not be empty.'}), 400

    if not email or email.isspace():
        return jsonify({'message': 'Email field can not be empty.'}), 400
    elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
        return jsonify({'message': 'Enter a valid email address.'}), 400

    if not password or password.isspace():
        return jsonify({'message': 'Password field can not be left empty.'}), 400
    elif not re.match(r"[A-Z, a-z, 0-9, @#]", password):
        return jsonify({'message': 'Password must contain each one of these characters (A-Za-z0-9@#)'}), 400
    elif len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters.'}), 400

    db = DatabaseConnection()
    email_db = db.check_email(email)
    username_db = db.check_username(username)

    if username_db != None:
        return jsonify({'message': 'This username already has an account.'}), 400
    if email_db != None:
        return jsonify({'message': 'This email is already taken.'}), 400
    db.insert_users(userId, username, email, password_hash)
    access_token = create_access_token(username)

    return jsonify({
        'access_token': access_token,
        'message': '{} has been registered succesfully.'.format(username)
    })


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['PUT'])
@jwt_required
def preferred_answer(questionId, answerId):
    userId = get_jwt_identity()
    db = DatabaseConnection()
    question_userId = db.asked(questionId)
    answer_userId = db.answered(answerId, questionId)

    if userId[0] == question_userId[0]:
        db.preferred(userId[0])
        return jsonify({'message': 'Welcome!'})
    elif userId[0] == answer_userId[0]:
        info = request.get_json()
        details = info.get('details')

        db.edit_answer(details, userId, questionId)

        return jsonify({'message': 'Wlecome.'})
    else:
        return jsonify({'message': 'You don\'t have permission to be here.'}), 400
