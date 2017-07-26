from bs4 import BeautifulSoup
import urllib.request as request

url = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
res = request.urlopen(url)
print(res)
soup = BeautifulSoup(res, "html.parser")


price = soup.select_one(".stoksPrice").string
print("usd/jpy=", price)
