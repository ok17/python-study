import struct


def to_csv(name, maxdata):
    # open label  & image file
    lbl_file = open("./mnist/" + name + "-labels-idx1-ubyte", "rb")
    img_file = open("./mnist/" + name + "-images-idx3-ubyte", "rb")
    csv_file = open("./mnist/" + name + ".csv", "w", encoding='utf-8')

    # header info
    # I ... unsigned int 4バイト
    # 下記は12バイト
    # lbl_count = struct.unpack(">III", lbl_file.read(12))
    # これは、I(4バイト) + I(4バイト) で 8バイト読み出す
    lbl_magic_number, lbl_count = struct.unpack(">II", lbl_file.read(8))
    img_magic_number, img_count = struct.unpack(">II", img_file.read(8))

    print("lbl_magic_number:", lbl_magic_number, "lbl_count:", lbl_count)
    print("img_magic_number:", img_magic_number, "img_count:", img_count)
    print("lbl_file", lbl_file)

    rows, cols = struct.unpack(">II", img_file.read(8))
    pixels = rows * cols

    res = []

    for idx in range(lbl_count):
        if idx > maxdata:
            break

        # lbl_fileポインタの指すさきは、上記で8バイト読み込んでいるから9バイト目をさしている
        # 答えラベルを取得する先頭から9バイト目
        # タプルで帰ってくるからlistの最初の要素を指定
        label = struct.unpack(">B", lbl_file.read(1))[0]

        print("label", label)
        print("lbl_file", lbl_file)

        bdata = img_file.read(pixels)
        sdata = list(map(lambda n: str(n), bdata))
        csv_file.write(str(label) + ",")
        csv_file.write(",".join(sdata) + "\r\n")

        if idx < 5:
            s = "P2 28 28 255\n"
            s += " ".join(sdata)
            iname = "./mnist/{0}-{1}-{2}.pgm".format(name, idx, label)

            with open(iname, "w", encoding="utf-8") as fp:
                fp.write(s)

    csv_file.close()
    lbl_file.close()
    img_file.close()


to_csv("train", 60000)
to_csv("t10k", 500)
