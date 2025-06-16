import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
import copy
import seaborn as sns
import tensorflow as tf
from sklearn.linear_model import LinearRegression

dataset_cols = ["bike_count", "hour", "temp", "humidity", "wind", "visibility", "dew_pt_temp", "radiation", "rain", "snow", "functional"]

df = pd.read_csv(r"C:\Users\dhruv\OneDrive\Documents\GitHub\Machine Learning\BIKE\SeoulBikeData.csv").drop(["Date", "Holiday", "Seasons"], axis=1)

df.columns = dataset_cols
df["functional"] = (df["functional"]=="Yes").astype(int)

df = df[df['hour']==12]
df = df.drop(["hour"], axis=1)


for label in df.columns[1:]:
  plt.scatter(df[label], df["bike_count"])
  plt.title(label)
  plt.ylabel("Bike count at noon")
  plt.xlabel(label)
  filename = f"{label}_vs_Bike_Count_Noon.png"
  # plt.savefig(filename)
  plt.close()

df = df.drop(["wind", "visibility", "functional"], axis=1)

# print(df.head())

trian, val, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])

def get_xy(dataframe, y_label, x_labels=None):
  dataframe = copy.deepcopy(dataframe)
  if x_labels is None:
    X = dataframe[[c for c in dataframe.columns if c!= y_label]].values
  else:
    if len(x_labels)==1:
      x = dataframe[x_labels].values.reshape(-1, 1)
    else:
      x = dataframe[x_labels].values
  y = dataframe[y_label].values.reshape(-1,1)
  data = np.hstack((x, y))
  return data, x, y
_, x_train_temp, y_train_temp = get_xy(trian, "bike_count", x_labels=["temp"])
_, x_val_temp, y_val_temp = get_xy(val, "bike_count", x_labels=["temp"])
_, x_test_temp, y_test_temp = get_xy(test, "bike_count", x_labels=["temp"])

temp_reg = LinearRegression()
temp_reg.fit(x_train_temp, y_train_temp)

# print(temp_reg.coef_, temp_reg.intercept_) #[[19.04271216]] [392.92854588]
# print(temp_reg.score(x_test_temp, y_test_temp)) #0.37379010334466445

plt.scatter(x_train_temp, y_train_temp, label="Data", color="blue")
x = tf.linspace(-20, 40, 100)
plt.plot(x, temp_reg.predict(np.array(x).reshape(-1, 1)), label="Fit", color="red", linewidth=3)
plt.legend()
plt.title("Bikes vs Temp")
plt.ylabel("Number of Bikes")
plt.xlabel("Temp")
# plt.savefig("Bikes_vs_Temp.png")
plt.close()

# Multiple Linear Regrssion
_, x_train_all, y_train_all = get_xy(trian, "bike_count", x_labels=df.columns[1:])
_, x_val_all, y_val_all = get_xy(val, "bike_count", x_labels=df.columns[1:])
_, x_test_all, y_test_all = get_xy(test, "bike_count", x_labels=df.columns[1:]) 

all_reg = LinearRegression()
all_reg.fit(x_train_all, y_train_all)

print(all_reg.score(x_test_all, y_test_all)) #0.45731765372923894