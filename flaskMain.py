from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from Moviedb import db, MovieModel
from userDB import userdb, UserModel
from newMovieDB import newdb, newMovieModel
from urllib.request import urlopen
from bs4 import BeautifulSoup
import itertools
import jinja2

app = Flask(__name__)
#taken from (some elements) 'https://www.askpython.com/python-modules/flask/flask-crud-application'
#taken from (some elements) 'https://medium.com/analytics-vidhya/creating-login-page-on-flask-9d20738d9f42'
app.config['SECRET_KEY'] = "JohnKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jMovie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
    userdb.create_all()
    db.create_all()
    newdb.create_all()


@app.route('/', methods= ['POST', 'GET'])

#taken from (some elements) 'https://iq.opengenus.org/login-page-in-flask/'
#taken from (some elements) 'https://medium.com/@shrimantshubham/flask-sqlalchemy-tutorial-login-system-with-python-61a3ab9f4990'
def Login():
    if request.method == 'GET':
        return render_template('landingPage.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            attemptLogIn = UserModel.query.filter_by(username=name, password=passw).first()
            if attemptLogIn is not None and name == "JohnM89" and passw =="ozzyozzy":
                session['logged_in'] = True
                return redirect('/homeAdmin')
            elif attemptLogIn is not None:
                session['logged_in'] = True
                return redirect('/home')
            else:
                return 'Incorrect Login Details, Please Go Back'
        except:
            return "Incorrect Login"

@app.route("/logout")
def logoutUser():
    session['logged_in'] = False
    return redirect('/')

@app.route('/signUp', methods= ['GET', 'POST'])
def signUp():
#Elements taken from: 'https://stackoverflow.com/questions/42154602/how-to-get-form-data-in-flask'
    if request.method == 'GET':
        return render_template('signUp.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "" or password == "":
            return 'Please go back and enter values for both Username and Password '
        else:
            user = UserModel(username=username, password=password)
        #taken from 'https://stackoverflow.com/questions/19388555/sqlalchemy-session-add-return-value'
            userdb.session.add(user)
            userdb.session.commit()
            return redirect('/')

@app.route('/homeAdmin')
def adminHomePage():
#taken from 'https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application#step-3-displaying-all-records'
    users = UserModel.query.all()
    return render_template('homeAdmin.html', users= users)

@app.route('/home')
def homePage():
# taken from 'https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application#step-3-displaying-all-records'

    users = UserModel.query.all()
    return render_template('homePage.html', users= users)

@app.route('/search', methods= ['GET', 'POST'])
def searchMovies():
    if request.method == 'GET':
        return render_template('search.html')
    # Taken from (some elements) 'https://www.youtube.com/watch?v=lOzyQgv71_4'
    if request.method == 'POST':
        usersearchTerm = request.form['searchTerm']
        searchTerm = usersearchTerm.replace(' ', '+')
        url = 'https://www.imdb.com/find?q=' + searchTerm + '&s=tt&ttype=ft&ref_=fn_ft'
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features='html.parser')

        searchresultsList = []
        for results in soup.find_all("td", {"class": "result_text"}, limit=20):
            #Taken from 'https://stackoverflow.com/questions/16118598/how-to-display-text-only-using-find-all-in-beautiful-soup'
            results = results.text
            searchresultsList.append(results)
        numresults = len(searchresultsList)

        searchlinkList = []
        for sLink in soup.findAll("td", {"class": "primary_photo"}, limit=20):
            sLinkText = sLink.find('a')['href']
            sLinkText = 'https://www.imdb.com' + sLinkText
            searchlinkList.append(sLinkText)

        genreList = []
        for a in searchlinkList:
            url = a
            html = urlopen(url).read()
            soup = BeautifulSoup(html, features='html.parser')
            for genre in soup.find_all("span", {"class": "ipc-chip__text"}):
                genre = genre.string
                if genre != "Back to top":
                    genreList.append(genre)
        #taken from 'https://stackoverflow.com/questions/44104729/grouping-every-three-items-together-in-list-python'
        genreList = list(zip(*[iter(genreList)] * 3))

        return render_template('searchResults.html',usersearchTerm = usersearchTerm, searchTerm = searchTerm,numresults= numresults,  searchresultsList = searchresultsList, searchlinkList = searchlinkList, genreList = genreList, zip = zip)


@app.route('/searchresults', methods = ['GET', 'POST'])
def searchResult():
    if request.method == 'GET':
        return render_template('searchResults.html')


#to take the user input and post the details to our database
@app.route('/data/addData', methods= ['GET', 'POST'])
def addDetails():
    if request.method == 'GET':
        return render_template('addpage.html')

#NewMovieDB
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        relyear = request.form['relyear']
        genre = request.form['genre']
        signature = request.form['signature']
        description = request.form['description']
        if movie_name == "" or relyear == "" or genre == "" or signature == "" or description == "":
            return 'Please go back and enter values for all fields to submit a review'
        else:
            newmovie = newMovieModel(movie_name=movie_name, relyear=relyear, genre=genre, signature=signature, description=description)
        #taken from 'https://stackoverflow.com/questions/19388555/sqlalchemy-session-add-return-value'
            newdb.session.add(newmovie)
            newdb.session.commit()
            return redirect('/reviewlist')

@app.route('/reviewlist')
def RetrieveReviewList():
    #Original Movie DB
    # movies = MovieModel.query.all()
    # return render_template('reviewlist.html' , movies = movies)

    #NewMovieDB
    movies = newMovieModel.query.all()
    return render_template('reviewlist.html', movies = movies)

@app.route('/usersPage')
def retrieveUsers():
    users = UserModel.query.all()
    return render_template('usersPage.html' , users = users)

    #NEW DATABASE
@app.route('/data/<int:id>')
def RetrieveSingleReview(id):
    movie = newMovieModel.query.filter_by(id=id).first()
    if movie:
        return render_template('data.html', movie = movie)
    return f"No Movie review with id {id} in Reviews"


#NEW UPDATED DATABASE
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def DeleteSingleReview(id):
    movie = newMovieModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if movie:
            newdb.session.delete(movie)
            newdb.session.commit()
            return redirect('/reviewlist')

    return render_template('deleteMovie.html', movie = movie)

@app.route('/deluser/<int:user_id>', methods=['GET', 'POST'])
def DeleteSingleUser(user_id):
    user = UserModel.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        if user:
            userdb.session.delete(user)
            userdb.session.commit()
            return redirect('/usersPage')

    return render_template('deleteUser.html', user = user)
#Code to scrape LightHouse.ie and create lists of Movie Title, Movie Description and Movie Details:
#https://www.geeksforgeeks.org/python-using-for-loop-in-flask/  how to use for loop in python to html
@app.route('/Lighthouse')
def lighthouseScrape():

    url = 'https://www.lighthousecinema.ie/films/'
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features='html.parser')
    # scrape movie titles
    titleList = []
    # Taken from 'https://stackoverflow.com/questions/16118598/how-to-display-text-only-using-find-all-in-beautiful-soup'
    for title in soup.find_all("h3"):
        title = title.string
        titleList.append(title)
    # scrape description
    # https://stackoverflow.com/questions/31140143/how-to-add-space-around-removed-tags-in-beautifulsoup how to add space around scraped elements
    descList = []
    for desc in soup.findAll("div", {"class": "nsp-description"}):
        desc = desc.string
        descList.append(desc.replace("\n", ""))
        #descList.append(desc)


    detailsList = []
    for details in soup.find_all("div", {"class": "nsp-details"}):
        details = details.get_text(separator='\n')
        details = details.replace('\n \n', '\n')
        detailsList.append(details)
    # scrape the link to the movies description page on Lighthouse.ie
    linkList = []
    for link in soup.findAll("div", {"class": "nsp-poster"}):
        linkText = link.find('a')['href']

        linkList.append(linkText)

    # scrape to get the poster images
    imageList = []
    for image in soup.findAll("div", {"class": "nsp-poster"}):
        imageLink = image.find('img')['src']
        # using replace() to allow me to scrape images that are in the lighthousecinema assets folder.
        imageLink = imageLink.replace('/themes', 'https://www.lighthousecinema.ie/themes')
        imageList.append(imageLink)

    return render_template("scrape.html", titleList = titleList, descList = descList, detailsList = detailsList, linkList = linkList, imageList= imageList, zip = zip)

if __name__ =='__main__':
    app.run(debug = True)