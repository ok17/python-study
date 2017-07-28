from sklearn import svm, metrics
import glob
import os.path
import re
import json


def check_freq(filename):
    name = os.path.basename(filename)
    print(name)
    lang = re.match(r'^[a-z]{2,}', name).group()
    print(lang)
    with open(filename, "r", encoding="utf-8") as fp:
        text = fp.read()

    text = text.lower()


    cnt = [0 for n in range(0, 26)]
    code_a = ord('a')
    code_z = ord('z')

    for ch in text:
        n = ord(ch)
        if code_a <= n <= code_z:
            cnt[n - code_a] += 1


    # 正規化

    total = sum(cnt)
    # cntの要素を一つづつ読み込んで、cnt / total の結果をlist化する
    freq = list(map(lambda n: n / total, cnt))

    # print("cnt", cnt)
    # print("total", total)
    # print("freq", freq)
    # exit()

    return freq, lang


def load_files(path):
    freqs = []
    labels = []
    file_list = glob.glob(path)

    for fname in file_list:
        r = check_freq(fname)
        freqs.append(r[0])
        labels.append(r[1])

    return {"freqs": freqs, "labels": labels}


data = load_files("./lang/train/*.txt")
test = load_files("./lang/test/*.txt")

with open("./lang/freq.json", "w", encoding="utf-8") as fp:
    json.dump([data, test], fp)

clf = svm.SVC()
clf.fit(data["freqs"], data["labels"])

predict = clf.predict(test["freqs"])


ac_score = metrics.accuracy_score(test["labels"], predict)
cl_report = metrics.classification_report(test["labels"], predict)

print("正解率:", ac_score)
print("レポート")
print(cl_report)
