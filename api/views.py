from flask import Flask, request, jsonify
import json
# import uuid
from api.models import Questions, Answer, questions, answers

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