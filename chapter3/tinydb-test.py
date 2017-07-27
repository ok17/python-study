from tinydb import TinyDB, Query

filepath = "test-tyny.json"

db = TinyDB(filepath)

print(db)


db.purge_table('hoge')
table = db.table('hoge')

table.insert({'name': 'Banana', 'price': 600})
table.insert({'name': 'Orange', 'price': 400})



print(table.all())


Item = Query()

table.update({'price': 1000}, Item.name == 'Banana')
res = table.search(Item.name == 'Orange')

print("res=:", res)
print("Orange is ", res[0]['price'])

print("500円以上")

res = table.search(Item.price >= 500)

for i in res:
    print("これだ:", i['name'], i['price'])

