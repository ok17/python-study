from bs4 import BeautifulSoup
import re

fp = open("vegetables.html", encoding="utf-8")
soup = BeautifulSoup(fp, "html.parser")

print(soup.select_one("li:nth-of-type(8)").string)
print(soup.select("#ve-list > li.black")[0].string)


cond = {"data-lo":"us", "class":"black"}
print(soup.find("li", cond).string)


print(soup.find(id="ve-list")
          .find("li", cond).string)


li = soup.find_all(href=re.compile(r"^https://"))
print(li)
for e in li:
    print(e.attrs['href'])
