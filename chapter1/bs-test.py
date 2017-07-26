from bs4 import BeautifulSoup
import urllib.request as request

url = ""


res = request.urlopen(url)

print(res)

soup = BeautifulSoup(res, "html.parser")

prettify = soup.prettify()


# print("prettify=", prettify)
# print("prettify=", soup.find("p").string)


select = soup.select("div.news_article > dl > dd")

# print("select", select)


for li in select:
    print("dl=", li.string)
