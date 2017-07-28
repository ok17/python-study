import urllib.request as request
import gzip
import os
import os.path

savepath = "./mnist"
download_url = "http://yann.lecun.com/exdb/mnist"

files = [
    "train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz",
]

if not os.path.exists(savepath):
    os.mkdir(savepath)

for file in files:
    url = download_url + "/" + file
    save = savepath + "/" + file
    print("download:", url)

    if not os.path.exists(save):
        request.urlretrieve(url, save)


# 解凍

for file in files:
    gz_file = savepath + "/" + file
    raw_file = savepath + "/" + file.replace(".gz", "")

    print("gzip:", raw_file)

    with gzip.open(gz_file, "rb") as fp:
        body = fp.read()
        with open(raw_file, "wb") as wp:
            wp.write(body)


print("かんりょう")
