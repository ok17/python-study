import json

j = {
    "date": "2015-01-01",
    "price": {
        "aaa": 44,
        "bbb": 55,
        "ccc": 66,
    }
}

out = json.dumps(j)

print(out)