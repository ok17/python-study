import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

USER = "JS-TESTER"
PASS = "ipCU12ySxI"

session = requests.session()

login_info = {
    "username_mmlbbs6": USER,
    "password_mmlbbs6": PASS,
    "back": "index.php",
    "mml_id": "0"
}

url_login = "http://uta.pw/sakusibbs/users.php?action=login&m=try"
res = session.post(url_login, data=login_info)
# エラー発生時
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")
a = soup.select_one(".islogin > a")

if a is None:
    print("No MyPage")
    exit()

url_mypage = urljoin(url_login, a.attrs["href"])
print("mypage", url_mypage)

res = session.get(url_mypage)
res.raise_for_status()


soup = BeautifulSoup(res.text, "html.parser")
links = soup.select("#favlist li > a")
for a in links:
    href = a.attrs["href"]
    title = a.get_text()
    print("-", title, ">", href)
