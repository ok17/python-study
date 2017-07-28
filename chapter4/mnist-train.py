from sklearn import cross_validation, svm, metrics

def load_csv(filename):
    labels = []
    images = []

    with open(filename, "r") as fp:
        for line in fp:
            cols = line.split(",")
            if len(cols) < 2:
                continue

            labels.append(int(cols.pop(0)))
            vals = list(map(lambda n: int(n) / 256, cols))

            images.append(vals)
    return {"labels": labels, "images": images}

data = load_csv("./mnist/train.csv")
test = load_csv("./mnist/t10k.csv")

clf = svm.SVC()
clf.fit(data["images"], data["labels"])

predict = clf.predict(test["images"])


ac_score = metrics.accuracy_score(test["labels"], predict)
cl_report = metrics.classification_report(test["labels"], predict)

print("正解率:", ac_score)
print("レポート:")
print(cl_report)
