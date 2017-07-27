import pandas

filename = "test.xlsx"


book = pandas.read_excel(filename)

print(book)


book.sort_values(by="項目２", ascending=False)

print(book)
