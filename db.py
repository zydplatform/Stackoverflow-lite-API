import psycopg2
from pprint import pprint

class DatabaseConnection:
    
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname=stackoverflow user=postgres host=localhost password=kengo1234 port=5432"
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            pprint('Database connected.')
        except:
            pprint('Cannot connect to the database.')

    def insert_users(self, userId, username, email, password):
        insert_user = "INSERT INTO users(userId, username, email, password) VALUES('{}', '{}', '{}', '{}')".format(userId, username, email, password)
        pprint(insert_user)
        self.cursor.execute(insert_user)

    def insert_question(self, questionId, details, userId):
        insert_question = "INSERT INTO questions(questionId, details, userId) VALUES('{}', '{}', '{}')".format(questionId, details, userId)
        pprint(insert_question)
        self.cursor.execute(insert_question)

    def login(self, username, password):
        query = "SELECT * FROM users WHERE password='{}' AND username='{}'".format(password, username)
        pprint(query)
        self.cursor.execute(query)

    def insert_answer(self, details, userId, questionId):
        insert_answer = "INSERT INTO answers(details, userId, questionId) VALUES('{}','{}','{}')".format(details, userId, questionId)
        pprint(insert_answer)
        self.cursor.execute(insert_answer)

    def get_all_questions(self):
        query = "SELECT * FROM questions"
        pprint(query)
        self.cursor.execute(query)

    def get_one_question(self,questionId):
        query = "SELECT * FROM questions WHERE questionId='{}'".format(questionId)
        pprint(query)
        self.cursor.execute(query)

    def delete_question(self, questionId, userId):
        query = "DELETE FROM questions WHERE questionId='{}'".format(questionId)
        pprint(query)
        self.cursor.execute(query)


if __name__ == '__main__':
    database_connection = DatabaseConnection()