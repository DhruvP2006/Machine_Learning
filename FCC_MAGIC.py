import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

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

def scale_database(dataframe):
  X = dataframe[dataframe.cols[:-1]].values
  Y = dataframe[dataframe.cols[-1]].values

  scaler = StandardScaler()
  X = scaler.fit_transform(X)
  data = np.hstack((X, np.reshape(Y, (len(Y), 1))))
 
  return data, X, Y
  
# print(train)

print(len(train[train["class"]==1])) #gamma 
print(len(train[train["class"]==0])) #alpha 