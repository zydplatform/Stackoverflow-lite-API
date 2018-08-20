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

class Answer:
    def __init__(self, ans_id, details):
        self.answerId = ans_id
        self.details = details