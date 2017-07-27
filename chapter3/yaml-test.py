import yaml

yaml_str = """
Date: 2015-01-01
List:
    -
        id: 111
        name: Banana
        color: yellow
        price: 999
    -
        id: 222
        name: Hoge
        color: brown
        price: 10000
"""


data = yaml.load(yaml_str)

for item in data['List']:
    print(item["name"] + ":" + str(item["price"]))
