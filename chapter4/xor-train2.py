import pandas as pd
from sklearn import svm, metrics

xor_input = [
    #P, Q, result
    [0, 0, 0],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
]

xor_df = pd.DataFrame(xor_input)
print("df:", xor_df)

# データ
xor_data = xor_df.ix[:, 0:1]
print("data", xor_data)
# ラベル
xor_label = xor_df.ix[:, 2]
print("label", xor_label)


clf = svm.SVC()
clf.fit(xor_data, xor_label)
pre = clf.predict(xor_data)

ac_score = metrics.accuracy_score(xor_label, pre)
print("正解率:", ac_score)
