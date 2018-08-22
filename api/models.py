from flask import jsonify, request
import json

user = []
questions = []
answers = []

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password

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
        return jsonify({
            'Questions': [question.__dict__ for question in questions],
            'message': 'Questions fetched successfully.'
        }), 200
    
    @staticmethod
    def get_one_question(questionId):
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


class Answer:
    def __init__(self, ans_id, details):
        self.answerId = ans_id
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