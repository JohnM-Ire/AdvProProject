from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MovieModel(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key= True, unique = True)
    movie_id = db.Column(db.Integer(), unique = True)
    movie_name = db.Column(db.String())
    relyear = db.Column(db.Integer())
    #genre = db.Column(db.String())
    description = db.Column(db.String(500))

    def __init__(self, id, movie_id, movie_name, relyear, description):
        self.id = id
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.relyear = relyear
        # self.genre = genre
        self.description = description

    def __repr__(self):
        return f"{self.movie_name}:{self.movie_id}"
