import requests
import json

apikey = "6e5fda94f02e142a891383882b5602d2"

cities = ["Tokyo,JP", "London,UK", "New York,US"]

api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

# ケルビンから摂氏に変更する
k2c = lambda k: k - 273.15

for name in cities:
    url = api.format(city=name, key=apikey)
    r = requests.get(url)
    data = json.loads(r.text)


    print("都市=", data['name'])
    print("最低気温=", k2c(data["main"]["temp_min"]))
    print("最高気温=", k2c(data["main"]["temp_max"]))
