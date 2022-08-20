from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'https://www.lighthousecinema.ie/films/'
html = urlopen(url).read()
soup = BeautifulSoup(html, features='html.parser')

#print(soup)

titleList = []
for title in soup.find_all("h3"):
    title = title.string
    #print(title)
    titleList.append(title)
tnum = 1
for t in titleList:
    print(tnum, ": ", t)
    tnum = tnum+1

#print(titleList)


descList = []
for desc in soup.findAll("div", {"class": "nsp-description"}):
    desc = desc.string
    descList.append(desc.replace("\n", ""))
num = 1;
for d in descList:
    print(num, ": ", d)
    num = num+1
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

for details in soup.find_all("div", {"class": "nsp-details"}):
    print(" ", details.text)
# # genre = soup.find("strong")
# # print(genre.string)
# desc = soup.findAll("div", {"class": "nsp-description"})
# print(desc.string)

#li_newBall_luckyStar = soup.findAll('h3', ['nsp-description','new lucky-star'])
#
# numbers = []
# for i in li_newBall_luckyStar:
#     numbers.append(i.text)
#
# print(numbers)