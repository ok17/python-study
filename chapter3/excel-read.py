import openpyxl

filename = "test.xlsx"
book = openpyxl.load_workbook(filename)

# シートを指定する
sheet = book.worksheets[0]

data = []

for row in sheet.rows:
    data.append([
        row[1].value,
        row[2].value,
        row[3].value,
        row[4].value,
    ])

del data[0]


print(data)

sort_data = sorted(data, key=lambda y:y[1])


for i, a in enumerate(data):
    if i >= 5:
        break
    print(i+1, a[0], int(a[1]), int(a[2]), int(a[3]))
