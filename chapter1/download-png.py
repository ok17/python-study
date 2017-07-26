import urllib.request

url = "http://uta.pw/shodou/img/28/214.png"
savename = "test_download_1.png"

# save
# urllib.request.urlretrieve(url, savename)
# print("保存しました")

# download
openfile = urllib.request.urlopen(url).read()

# with open(savename, mode="wb") as file:
#     file.write(openfile)
#     print("ダウンロード保存しました")


file = open(savename, mode="wb")
file.write(openfile)
file.close()

