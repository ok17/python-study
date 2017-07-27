from bs4 import BeautifulSoup
import urllib.request as request
import os.path

url = "http://www.city.yokohama.lg.jp/somu/org/kikikanri/data/shelter.xml"
savename = "shelter.xml"

if not os.path.exists(savename):
    request.urlretrieve(url, savename)

xml = open(savename, "r", encoding="utf-8")
soup = BeautifulSoup(xml, "html.parser")

info = {}


for i in soup.find_all("shelter"):
    name = i.find('name').string
    ward = i.find('ward').string
    addr = i.find('address').string
    note = i.find('notes').string

    if not (ward in info):
        info[ward] = []
    info[ward].append(name)


for ward in info.keys():
    print("+", ward)

    for name in info[ward]:
        print("l - ", name)