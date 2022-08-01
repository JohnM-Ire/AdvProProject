from flask import Flask, render_template, request, redirect
from Moviedb import db, MovieModel
from userDB import userdb, UserModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jMovie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
    userdb.create_all()
    db.create_all()

@app.route('/')
def landPage():
    return render_template('landingPage.html')

@app.route('/home')
def homePage():
    return render_template('homePage.html')



#to take the user input and post the details to our database
@app.route('/data/addData', methods= ['GET', 'POST'])
def addDetails():
    if request.method == 'GET':
        return render_template('addpage.html')

    if request.method == 'POST':
        id = request.form['id']
        movie_id = request.form['movie_id']
        movie_name = request.form['movie_name']
        relyear = request.form['relyear']
        description = request.form['description']
        movie = MovieModel(id=id, movie_id=movie_id, movie_name=movie_name, relyear=relyear, description=description)
        db.session.add(movie)
        db.session.commit()
        return redirect('/datalist')

@app.route('/datalist')
def RetrieveDataList():
    movies = MovieModel.query.all()
    return render_template('datalist.html' , movies = movies)



@app.route('/data/<int:movie_id>')
def RetrieveSingleReview(movie_id):
    movie = MovieModel.query.filter_by(movie_id=movie_id).first()
    if movie:
        return render_template('data.html', movie = movie)
    return f"No Movie review with id {id} in Reviews"

if __name__ =='__main__':
    app.run(debug = True)