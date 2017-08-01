from sklearn import svm
from sklearn.externals import joblib
import json

with open("./lang/freq.json", "r", encoding="utf-8") as fp:
    d = json.load(fp)
    data = d[0]

    # print(data)


clf = svm.SVC()
clf.fit(data["freqs"], data["labels"])

joblib.dump(clf, "./cgi-bin/freq.pkl")
print("ok")
