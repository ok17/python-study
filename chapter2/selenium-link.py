import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import os, os.path, time

html = open("table.html", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")
# links = soup.select("a[href]")

table = soup.select_one("table")
tr_list = table.find_all("tr")

result = []

for list in tr_list:
    result_row = []
    tds = list.find_all("td")
    for td in tds:
        cell = td.get_text()
        result_row.append(cell)

    result.append(result_row)

# for a in links:
#     href = a.attrs["href"]
#     title = a.string
#     result.append((title, href))


print(result)
time.sleep(10)


for row in result:
    print(",".join(row))




