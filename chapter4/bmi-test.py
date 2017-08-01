from sklearn import cross_validation, svm, metrics
import matplotlib.pyplot as plt
import pandas as pd

tbl = pd.read_csv("bmi.csv", encoding="utf-8")

label = tbl["label"]

# 各行を0から1の間になるように正規化している
# 配列の全ての値について実行される
w = tbl["weight"] / 100
h = tbl["height"] / 200

wh = pd.concat([w, h], axis=1)


# データ分ける
data_train, data_test, label_train, label_test = \
    cross_validation.train_test_split(wh, label)


print("data_train", data_train)
print("data_test", data_test)
print("label_train", label_train)
print("label_test", label_test)


# データ学習
clf = svm.SVC()
clf.fit(data_train, label_train)


# データ予測
predict = clf.predict(data_test)

# 確認
ac_score = metrics.accuracy_score(label_test, predict)
cl_report = metrics.classification_report(label_test, predict)

print("せいかい", ac_score)
print("れぽーと", cl_report)







