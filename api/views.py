from flask import Flask, request, jsonify
import json
import uuid
from api.models import *

app = Flask(__name__)


@app.route('/api/v1/questions', methods=['POST'])
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


@app.route('/api/v1/questions', methods=['GET'])
def get_all_questions():
    if len(questions) == 0:
        return jsonify({'message': 'There are no questions yet.'}), 400
    return jsonify({
        'Questions': [question.__dict__ for question in questions],
        'message': 'Questions fetched succesfully.'
    }), 200


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
def answer(questionId):
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


@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def one_qn(questionId):
    try:
        if questionId > len(questions) or questionId <= 0:
            return jsonify({'message': 'Question doesn\'t exist.'}), 400
        qn = questions[questionId]
        return jsonify({
            'Question': qn.__dict__,
            'message': 'Questions fetched successfully'
        }), 200
    except TypeError:
        return jsonify({'message': 'Question Id must be a number.'}), 400