import urllib.request as request
import os.path
import random
import json

url = "http://api.aoikujira.com/hyakunin/get.php?fmt=json"

savename = "hyaku.json"

if not os.path.exists(savename):
    request.urlretrieve(url, savename)

data = json.load(open(savename, 'r', encoding="utf-8"))

for j in data:
    print(j['kami'], j['simo'])

# r = random.choice(data)
#
# print(r['kami'], r['simo'])
