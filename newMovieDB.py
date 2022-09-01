from flask_sqlalchemy import SQLAlchemy
#taken from 'https://www.askpython.com/python-modules/flask/flask-crud-application'
newdb = SQLAlchemy()

class newMovieModel(newdb.Model):
    __tablename__ = "reviewTable"

    id = newdb.Column(newdb.Integer, primary_key= True, unique = True, autoincrement=True)
    movie_name = newdb.Column(newdb.String())
    relyear = newdb.Column(newdb.Integer())
    genre = newdb.Column(newdb.String())
    signature = newdb.Column(newdb.String(100), )
    description = newdb.Column(newdb.String(800))

    def __init__(self,movie_name, relyear, genre, signature, description):
        self.movie_name = movie_name
        self.relyear = relyear
        self.genre = genre
        self.signature = signature
        self.description = description

    def __repr__(self):
        return f"{self.movie_name}:{self.signature}"
