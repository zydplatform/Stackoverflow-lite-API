from flask import Flask, request, jsonify
import json, uuid, re
from db import DatabaseConnection
from api.models import User, Answer, Questions, users, answers, questions
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'KenG0W@Da4!'

@app.route('/api/v1/questions', methods=['POST'])
@jwt_required
def post_question():
    info = request.get_json()

    questionId = len(questions) + 1
    details = info.get('details')

    if not details or details.isspace():
        return jsonify({"message": "Enter a question"}), 400

    question = Questions(questionId, details)
    questions.append(question)

    return jsonify({
        'id': questionId,
        'question': question.__dict__,
        'message': 'Question added'
    }), 201

@app.route('/api/v1/questions', methods=['GET'])
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

@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
@jwt_required
def answer(questionId):
    try:
        info = request.get_json()

        details = info.get('details')

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
        return jsonify({'message': 'The question does not exist'}), 400

@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def one_qn(questionId):
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

@app.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
@jwt_required
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
    userId = db.user(username)

    if check_password_hash(user[3], password) and user[1] == username:
        access_token = create_access_token(identity=userId)
        return jsonify({
            'token': access_token,
            'message': '{} has logged in.'.format(username)
        }), 200
    else:
        return jsonify({'message': 'Wrong login credentials.'})
    

@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    info = request.get_json()

    username = info.get('username')
    email = info.get('email')
    password = generate_password_hash(info.get('password'), method='sha256')
    userId = uuid.uuid4()

    if not username or username.isspace():
        return jsonify({'message': 'Username field can not be empty.'}), 400

    if not email or email.isspace():
        return jsonify({'message': 'Email field can not be empty.'}), 400
    elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
        return jsonify({'message': 'Enter a valid email address.'}),400
            
    if not password or password.isspace():
        return jsonify({'message': 'Password field can not be left empty.'}), 400
    elif not re.match(r"[A-Z, a-z, 0-9, @#]", password):
        return jsonify({'message': 'Password must contain each one of these characters(A-Za-z0-9@#)'}), 400
    elif len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters.'}), 400
    
    db = DatabaseConnection()
    user = User(userId, username, password, email)
    # users.append(user)
    email_db = db.check_email(email)
    username_db = db.check_username(username)

    if username_db != None:
        return jsonify({'message': 'This username already has an account.'}), 400
    if email_db != None:
        return jsonify({'message': 'This email is already taken.'}), 400
    db.insert_users(userId, username, email, password)
    access_token = create_access_token(username)

    return jsonify({
        'access_token': access_token,
        'UserId': userId,
        'Username': user.username,
        'message': '{} has been registered succesfully.'.format(username)
    })


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['PUT'])
@jwt_required
def preferred_answer(questionId, answerId):
    pass