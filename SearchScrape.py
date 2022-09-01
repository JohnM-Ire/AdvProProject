from urllib.request import urlopen
from bs4 import BeautifulSoup
import itertools
import time

# searchTerm = 'dredd'
# searchTerm = searchTerm.replace(' ', '+')
#
# #url = 'https://www.allmovie.com/search/movies/300'
# #url = 'https://www.imdb.com/find?q='+searchTerm+'&ref_=nv_sr_sm'
# url = 'https://www.imdb.com/find?q='+searchTerm+'&s=tt&ttype=ft&ref_=fn_ft'
# html = urlopen(url).read()
# soup = BeautifulSoup(html, features='html.parser')
#
#
#
# searchresultsList= []
#
# for results in soup.find_all("td", {"class": "result_text"}):
#     results = results.text
#     searchresultsList.append(results)
# # for l in searchresultsList:
# #     print(l)
#
# searchlinkList= []
# for sLink in soup.findAll("td", {"class": "primary_photo"}, limit= 20):
#     sLinkText = sLink.find('a')['href']
#     sLinkText = 'https://www.imdb.com'+ sLinkText
#     searchlinkList.append(sLinkText)
#
# genreList= []
# for a in searchlinkList:
#     url = a
#     html = urlopen(url).read()
#     soup = BeautifulSoup(html, features='html.parser')
#     for genre in soup.find_all("span", {"class": "ipc-chip__text"}):
#         genre =genre.string
#         if genre != "Back to top":
#             genreList.append(genre)
# #print(genreList)
# # for g in genreList:
# #     print(g)
# genreList= list(zip(*[iter(genreList)]*3))


# for movie, g in zip(searchresultsList, genreList):
#     print(movie, g)
searchTerm = 'dredd'
url = 'https://www.imdb.com/find?q=' + searchTerm + '&s=tt&ttype=ft&ref_=fn_ft'
html = urlopen(url).read()
soup = BeautifulSoup(html, features='html.parser')
start = time.time()
searchresultsList = []
for results in soup.find_all("td", {"class": "result_text"}, limit = 20):
    #Taken from 'https://stackoverflow.com/questions/16118598/how-to-display-text-only-using-find-all-in-beautiful-soup'
    results = results.text;
    searchresultsList.append(results);
numresults = len(searchresultsList);

searchlinkList = []
for sLink in soup.findAll("td", {"class": "primary_photo"}, limit = 20):
    sLinkText = sLink.find('a')['href']
    sLinkText = 'https://www.imdb.com' + sLinkText
    searchlinkList.append(sLinkText);

genreList = []
for a in searchlinkList:
    url = a
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features='html.parser')
    for genre in soup.find_all("span", {"class": "ipc-chip__text"}):
        genre = genre.string
        if genre != "Back to top":
            genreList.append(genre);
#taken from 'https://stackoverflow.com/questions/44104729/grouping-every-three-items-together-in-list-python'
# genreList = list(zip(*[iter(genreList)] * 3))

    #return render_template('searchResults.html',usersearchTerm = usersearchTerm, searchTerm = searchTerm,numresults= numresults,  searchresultsList = searchresultsList, searchlinkList = searchlinkList, genreList = genreList, zip = zip)
end= time.time()
for (result, link, genre) in zip(searchresultsList, searchlinkList, genreList):
    print( result, link, genre)
print("Time taken: ", end-start)