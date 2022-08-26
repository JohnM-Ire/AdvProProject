from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class newMovieModel(db.Model):
    __tablename__ = "reviewTable"

    id = db.Column(db.Integer, primary_key= True, unique = True, autoincrement=True)
    movie_name = db.Column(db.String())
    relyear = db.Column(db.Integer())
    genre = db.Column(db.String())
    signature = db.Column(db.String(100), )
    description = db.Column(db.String(800))

    def __init__(self, movie_name, relyear, genre, signature, description):
        self.movie_name = movie_name
        self.relyear = relyear
        self.genre = genre
        self.signature = signature
        self.description = description

    def __repr__(self):
        return f"{self.movie_name}:{self.signature}"
