from flask import Flask, request, jsonify
import json
from api.models import Questions, Answer, User, questions, answers, users

app = Flask(__name__)


@app.route('/api/v1/questions', methods=['POST'])
def post_question():
    return Questions.post_question()

@app.route('/api/v1/questions', methods=['GET'])
def get_all_questions():
    return Questions.get_all_questions()

@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
def answer(questionId):
    return Answer.post_answer(questionId)

@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def one_qn(questionId):
    return Questions.get_one_question(questionId)

@app.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
def delete_question(questionId):
    return Questions.delete_question(questionId)

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    return User.login()

@app.route('/api/v1/auth/sigup', methods=['POST'])
def signup():
    return User.register()