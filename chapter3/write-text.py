filename = "a.bin"
data = 100

with open(filename, "wb") as f:
    f.write(bytearray([data]))

with open("b.txt", "w") as f:
    f.write("1234")
