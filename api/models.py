users = []
questions = []
answers = []

class User:
    def __init__(self, userId, username, password, email):
        self.userId = userId
        self.username = username
        self.email = email
        self.password = password


class Questions:
    def __init__(self, details, userId):
        self.details = details
        self.userId = userId


class Answer:
    def __init__(self, qn_id, details):
        self.questionId = qn_id
        self.details = details