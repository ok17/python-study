import struct

png_data = open("test.png", "rb").read()

b_png = struct.unpack_from(">I4sIIBB", png_data, 8)
print("b_png:", b_png)


b_pppng = struct.unpack("I4s", open("test.png", "rb").read(8))
print("b_pppng:", b_pppng)