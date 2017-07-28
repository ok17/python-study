import pandas as pd
from sklearn import svm, metrics, cross_validation

csv = pd.read_csv("IRIS.csv")

print(csv)
