from urllib.request import urlopen
from bs4 import BeautifulSoup
import itertools

searchTerm = 'three billboards outside ebbing'
searchTerm = searchTerm.replace(' ', '+')

#url = 'https://www.allmovie.com/search/movies/300'
#url = 'https://www.imdb.com/find?q='+searchTerm+'&ref_=nv_sr_sm'
url = 'https://www.imdb.com/find?q='+searchTerm+'&s=tt&ttype=ft&ref_=fn_ft'
html = urlopen(url).read()
soup = BeautifulSoup(html, features='html.parser')



# searchresultsList= []
#
# for results in soup.find_all("td", {"class": "result_text"}):
#     results = results.text
#     searchresultsList.append(results)
# for l in searchresultsList:
#     print(l)

searchlinkList= []
for sLink in soup.findAll("td", {"class": "primary_photo"}):
    sLinkText = sLink.find('a')['href']
    sLinkText = 'https://www.imdb.com'+ sLinkText
    searchlinkList.append(sLinkText)

genreList= []
for a in searchlinkList:
    url = a
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features='html.parser')
    for genre in soup.find_all("span", {"class": "ipc-chip__text"}):
        genre =genre.string
        if genre != "Back to top":
            genreList.append(genre)
print(genreList)
for g in genreList:
    print(g)


