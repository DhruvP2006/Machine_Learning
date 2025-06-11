import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler

cols = ["fLength", "fWidth", "fSize", "fConc", "fConc1", "fAsym", "fM3Long", "fM3Trans", "fAlpha", "fDist", "class"]
df = pd.read_csv("magic04.data", names = cols)
df.head()
# print(df)

df["class"] = (df["class"] =="g").astype(int) #convert labels (g and h) into 1`s and 0`s
# print(df["class"].unique())
# print(df.head())

for label in cols[:-1]:
  plt.hist(df[df["class"]==1][label], color="blue", label="gamma", alpha=0.7, density=True)
  plt.hist(df[df["class"]==0][label], color="red", label="hadron ", alpha=0.7, density=True)
  plt.title(label)
  plt.ylabel("Probability")
  plt.xlabel(label)
  plt.legend()
  # plt.savefig(f"Probability_vs_{label}_Graph.png")
  # plt.show()

# Train, validation and test dataset

train, valid, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])

def scale_database(dataframe, oversample=False):
  X = dataframe[dataframe.columns[:-1]].values
  Y = dataframe[dataframe.columns[-1]].values

  scaler = StandardScaler()
  X = scaler.fit_transform(X)

  if(oversample):
    ros = RandomOverSampler()
    X, Y = ros.fit_resample(X, Y)

  data = np.hstack((X, np.reshape(Y, (len(Y), 1))))
 
  return data, X, Y
  
# print(train)

# print(len(train[train["class"]==1])) #gamma 
# print(len(train[train["class"]==0])) #alpha 

train, x_train, y_train = scale_database(train, oversample=True)
valid, x_valid, y_valid = scale_database(valid, oversample=False)
test, x_test, y_test = scale_database(test, oversample=False)

# print(len(y_train)) #14896
# print(sum(y_train==1)) #7429
# print(sum(y_train==0)) #7416

# K-Nearest Neighbours
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(x_train, y_train)

y_pred = knn_model.predict(x_test)

print(classification_report(y_test, y_pred))

# Naive Bayes
from sklearn.naive_bayes import GaussianNB

nb_model = GaussianNB()
nb_model = nb_model.fit(x_train, y_train)

y_pred = nb_model.predict(x_test)
# print(classification_report(y_test, y_pred))