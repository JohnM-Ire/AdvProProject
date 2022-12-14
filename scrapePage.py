from urllib.request import urlopen
from bs4 import BeautifulSoup
import itertools
#
url = 'https://www.lighthousecinema.ie/films/'
html = urlopen(url).read()
soup = BeautifulSoup(html, features='html.parser')

# #print(soup)
#
titleList = []
movpageList=[]
fulldesc=[]
for title in soup.find_all("h3"):
    title = title.string
    #print(title)
    titleList.append(title)

for t in titleList:

    movpage = t.replace(" ", "-")
    movpage = movpage.lower()
    url = 'https://www.lighthousecinema.ie/film/'+ movpage
    for full in soup.findAll("div", {"class": "synopsis off"}):
        print(full)

#
# #print(titleList)
# linkList= []
# for link in soup.findAll("td", {"class": "nsp-poster"}):
#     linkText = link.find('a')['href']
#     linkList.append(linkText)
#
#
#
# fullDescription= []
# # for movlink in linkList:
# url = 'https://www.lighthousecinema.ie/film/donnie-darko'
# html = urlopen(url).read()
# soup = BeautifulSoup(html, features='html.parser')
#
# for fulldesc in soup.findAll("div", {"class": "synopsis"}):
#     fulldesc = fulldesc.text
#     fullDescription.append(fulldesc)
#
# #print(fullDescription)
#
# # for movTitle, titleDesc in zip(titleList, fullDescription):
# #     print(movTitle, titleDesc)

# descList = []
# for desc in soup.findAll("div", {"class": "nsp-description"}):
#     desc = desc.string
#     descList.append(desc.replace("\n", ""))
# num = 1;
# for d in descList:
#     #print(num, ": ", d)
#     num = num+1
#print(descList)
# print(len(descList))

#Might have to cut the daylist 99 results in this compared to 33 for other, diffreent movies have different amount of times
#would rather release date
# daylist= []
# for day in soup.find_all("div", {"class": "nsp-day"}):
#     day = day.text
#     #print(day)
#     daylist.append(day.replace("\n", "  "))
# print(daylist)
# detailsList=[]
# for details in soup.find_all("div", {"class": "nsp-details"}):
#     details = details.get_text(separator='\n')
#     details = details.replace('\n \n', '\n')
#     detailsList.append(details)
#print(detailsList)
# dlnum = 1
#for dl in detailsList:
    # print(dl)
    # print(dlnum, ": ", dl)
    # dlnum +=1

# # genre = soup.find("strong")
# # print(genre.string)
# desc = soup.findAll("div", {"class": "nsp-description"})
# print(desc.string)

# for (movTitle, movDetails, movDesc) in zip(titleList, detailsList, descList ):
#     print(f"Title: {movTitle}\n{movDetails}\nMovie Description: {movDesc}")
# imageList= []
# for image in soup.findAll("div", {"class": "nsp-poster"}):
#     imageLink = image.find('img')['src']
#     imageLink = imageLink.replace('/themes', 'https://www.lighthousecinema.ie/themes')
#     imageList.append(imageLink)

#print(imageList)

url = 'https://www.lighthousecinema.ie/films/'
html = urlopen(url).read()
soup = BeautifulSoup(html, features='html.parser')
# scrape movie titles
titleList = []
for title in soup.find_all("h3"):
    title = title.string
    titleList.append(title)
# scrape description
# https://stackoverflow.com/questions/31140143/how-to-add-space-around-removed-tags-in-beautifulsoup how to add space around scraped elements
descList = []
for desc in soup.find_all("div", {"class": "nsp-description"}):
    desc = desc.string
    descList.append(desc.replace("\n", ""))