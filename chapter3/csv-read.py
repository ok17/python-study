import codecs

filename = "test.csv"
csv = codecs.open(filename, "r", "shift_jis").read()

data = []
rows = csv.split("\r\n")

print("rows=",rows)
for row in rows:
    if row == "":
        continue

    cells = row.split(",")
    data.append(cells)


for c in data:
    print(c[1], c[2])