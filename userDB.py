from flask_sqlalchemy import SQLAlchemy

userdb = SQLAlchemy()

class UserModel(userdb.Model):
    __tablename__ = "usertable"

    username = userdb.Column(userdb.String, primary_key= True, unique = True)
    password = userdb.Column(userdb.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.username}:{self.username}"
