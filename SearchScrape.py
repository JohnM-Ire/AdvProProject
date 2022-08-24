from urllib.request import urlopen
from bs4 import BeautifulSoup
import itertools

searchTerm = "300"

#url = 'https://www.allmovie.com/search/movies/300'
url = 'https://www.imdb.com/find?q='+searchTerm+'&ref_=nv_sr_sm'
html = urlopen(url).read()
soup = BeautifulSoup(html, features='html.parser')
print(url)
print(f"Results for {searchTerm}")

searchresultsList= []
for results in soup.find_all("td", {"class": "result_text"}):
    results = results.text
    #print(results)
    searchresultsList.append(results)
#print(searchresultsList)

for l in searchresultsList:
    print(l)