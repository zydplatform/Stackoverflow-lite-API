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
            create_user_table = "CREATE TABLE IF NOT EXISTS users (userId TEXT NOT NULL PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);"
            create_answers_table = "CREATE TABLE IF NOT EXISTS answers (answerId SERIAL NOT NULL PRIMARY KEY, details TEXT NOT NULL, questionId INTEGER NOT NULL, userId TEXT NOT NULL);"
            create_questions_table = "CREATE TABLE IF NOT EXISTS questions (questionId INTEGER NOT NULL PRIMARY KEY, details TEXT NOT NULL, userId TEXT NOT NULL);"

            self.cursor.execute(create_user_table)
            self.cursor.execute(create_questions_table)
            self.cursor.execute(create_answers_table)

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

    def login(self, username):
        query = "SELECT * FROM users WHERE username='{}'".format(username)
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def user(self, username):
        query = "SELECT userId FROM users WHERE username='{}'".format(username)
        pprint(query)
        self.cursor.execute(query)
        userId = self.cursor.fetchone()
        return userId

    def check_username(self, username):
        query = "SELECT username FROM users WHERE username='{}'".format(username)
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user
    
    def check_email(self, email):
        query = "SELECT email FROM users WHERE email='{}'".format(email)
        pprint(query)
        self.cursor.execute(query)
        email = self.cursor.fetchone()
        return email

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

    def asked(self, questionId):
        query = "SELECT userId FROM questions WHERE questionId='{}'".format(questionId)
        pprint(query)
        self.cursor.execute(query)

    def answered(self, answerId):
        query = "SELECT userId FROM answers WHERE answerId='{}'".format(answerId)
        pprint(query)
        self.cursor.execute(query)

if __name__ == '__main__':
    database_connection = DatabaseConnection()