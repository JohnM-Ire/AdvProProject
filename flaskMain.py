from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from Moviedb import db, MovieModel
from userDB import userdb, UserModel
from urllib.request import urlopen
from bs4 import BeautifulSoup
import itertools
import jinja2

app = Flask(__name__)
app.config['SECRET_KEY'] = "JohnKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jMovie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
    userdb.create_all()
    db.create_all()

#@app.route('/')
# #Alt Login method to see if this works better
# @app.route('/login', methods= ['POST'])
# def login():
#     if request.form['password'] == 'password' and request.form['username'] == 'admin':
#         session['logged_in'] = True
#
#     else:
#         flash('incorrect password entered')
#         return login()



@app.route('/', methods= ['POST', 'GET'])
# def landPage():
#     return render_template('landingPage.html')
def Login():
    if request.method == 'GET':
        return render_template('landingPage.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            attempt = UserModel.query.filter_by(username=name, password=passw).first()
            if attempt is not None:
                session['logged_in'] = True
                return redirect('/home')
            # elif attempt is not None and name == "JohnM89" and passw =="ozzyozzy":
            #     session['logged_in'] = True
            #     return redirect('/homeAdmin')
            else:
                return 'Incorrect Login'
        except:
            return "Incorrect Login"

@app.route("/logout")
def logoutUser():
    session['logged_in'] = False
    return redirect('/')

@app.route('/signUp', methods= ['GET', 'POST'])
def signUp():

    if request.method == 'GET':
        return render_template('signUp.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = UserModel(username=username, password=password)
        userdb.session.add(user)
        userdb.session.commit()
        return redirect('/home')

@app.route('/homeAdmin')
def adminHomePage():
    users = UserModel.query.all()
    return render_template('homeAdmin.html', users= users)

@app.route('/home')
def homePage():
    users = UserModel.query.all()
    return render_template('homePage.html', users= users)

@app.route('/search', methods= ['GET', 'POST'])
def searchMovies():
    if request.method == 'GET':
        return render_template('search.html')

    if request.method == 'POST':
        usersearchTerm = request.form['searchTerm']
        searchTerm = usersearchTerm.replace(' ', '+')
        url = 'https://www.imdb.com/find?q=' + searchTerm + '&s=tt&ttype=ft&ref_=fn_ft'
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features='html.parser')

        searchresultsList = []
        for results in soup.find_all("td", {"class": "result_text"}, limit=10):
            results = results.text
            searchresultsList.append(results)
        numresults = len(searchresultsList)

        searchlinkList = []
        for sLink in soup.findAll("td", {"class": "primary_photo"}, limit=10):
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
        return render_template('searchResults.html',usersearchTerm = usersearchTerm, searchTerm = searchTerm,numresults= numresults,  searchresultsList = searchresultsList, searchlinkList = searchlinkList, genreList = genreList, zip = zip)


# url = 'https://www.imdb.com/find?q='+searchTerm+'&ref_=nv_sr_sm'
# html = urlopen(url).read()
# soup = BeautifulSoup(html, features='html.parser')
#
# searchresultsList= []
# for results in soup.find_all("td", {"class": "result_text"}):
#     results = results.text
#     searchresultsList.append(results)

@app.route('/searchresults', methods = ['GET', 'POST'])
def searchResult():
    if request.method == 'GET':
        return render_template('searchResults.html')


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
        # genre = request.form['genre']
        description = request.form['description']
        movie = MovieModel(id=id, movie_id=movie_id, movie_name=movie_name, relyear=relyear, description=description)

        db.session.add(movie)
        db.session.commit()
        return redirect('/reviewlist')

@app.route('/reviewlist')
def RetrieveReviewList():
    movies = MovieModel.query.all()
    return render_template('reviewlist.html' , movies = movies)



@app.route('/data/<int:movie_id>')
def RetrieveSingleReview(movie_id):
    movie = MovieModel.query.filter_by(movie_id=movie_id).first()
    if movie:
        return render_template('data.html', movie = movie)
    return f"No Movie review with id {id} in Reviews"

@app.route('/delete/<int:movie_id>', methods=['GET', 'POST'])
def DeleteSingleReview(movie_id):
    movie = MovieModel.query.filter_by(movie_id=movie_id).first()
    if request.method == 'POST':
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return redirect('/reviewlist')

    return render_template('deleteMovie.html', movie = movie)


#Code to scrape LightHouse.ie and create lists of Movie Title, Movie Description and Movie Details:

url = 'https://www.lighthousecinema.ie/films/'
html = urlopen(url).read()
soup = BeautifulSoup(html, features='html.parser')
#scrape movie titles
titleList = []
for title in soup.find_all("h3"):
    title = title.string
    titleList.append(title)
# scrape description
#https://stackoverflow.com/questions/31140143/how-to-add-space-around-removed-tags-in-beautifulsoup how to add space around scraped elements
descList = []
for desc in soup.findAll("div", {"class": "nsp-description"}):
    desc = desc.string
    descList.append(desc.replace("\n", ""))
# scrape details
# detailsList=[]
# for details in soup.find_all("div", {"class": "nsp-details"}):
#     details = details.text
#     detailsList.append(details)

detailsList=[]
for details in soup.find_all("div", {"class": "nsp-details"}):
    details = details.get_text(separator='\n')
    details = details.replace('\n \n', '\n')
    detailsList.append(details)
#scrape the link to the movies description page on Lighthouse.ie
linkList= []
for link in soup.findAll("div", {"class": "nsp-poster"}):
    linkText = link.find('a')['href']

    linkList.append(linkText)

#scrape to get the poster images
imageList= []
for image in soup.findAll("div", {"class": "nsp-poster"}):
    imageLink = image.find('img')['src']
#using replace() to allow me to scrape images that are in the lighthousecinema assets folder.
    imageLink = imageLink.replace('/themes', 'https://www.lighthousecinema.ie/themes')
    imageList.append(imageLink)

#https://www.geeksforgeeks.org/python-using-for-loop-in-flask/  how to use for loop in python to html
@app.route('/Lighthouse')
def lighthouseScrape():
    return render_template("scrape.html", titleList = titleList, descList = descList, detailsList = detailsList, linkList = linkList, imageList= imageList, zip = zip)

if __name__ =='__main__':
    app.run(debug = True)