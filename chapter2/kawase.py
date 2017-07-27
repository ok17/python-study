import urllib.request as request
import datetime
import json

API = "http://api.aoikujira.com/kawase/get.php?code=USD&format=json"

decode_json = request.urlopen(API).read().decode("utf-8")
data = json.loads(decode_json)
print("USD="+data["JPY"] + "JPY")

t = datetime.date.today()
filename = t.strftime("%Y-%m-%d") + ".json"
with open(filename, "w", encoding="utf-8") as f:
    f.write(decode_json)