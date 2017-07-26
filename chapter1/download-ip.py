import urllib.request

url = "http://api.aoikujira.com/ip/ini"
url__read = urllib.request.urlopen(url).read()

text = url__read.decode('utf-8')
print(text)
