from flask_sqlalchemy import SQLAlchemy
#taken from 'https://www.askpython.com/python-modules/flask/flask-crud-application'
userdb = SQLAlchemy()

class UserModel(userdb.Model):
    __tablename__ = "usertable"

    user_id =  userdb.Column(userdb.Integer, primary_key= True, unique = True, autoincrement=True)
    username = userdb.Column(userdb.String, unique = True)
    password = userdb.Column(userdb.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.username}:{self.username}"
