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

# for label in cols[:-1]:
#   plt.hist(df[df["class"]==1][label], color="blue", label="gamma", alpha=0.7, density=True)
#   plt.hist(df[df["class"]==0][label], color="red", label="hadron ", alpha=0.7, density=True)
#   plt.title(label)
#   plt.ylabel("Probability")
#   plt.xlabel(label)
#   plt.legend()
#   plt.savefig(f"Probability_vs_{label}_Graph.png")
#   plt.show()

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

# print(classification_report(y_test, y_pred))

# Naive Bayes
from sklearn.naive_bayes import GaussianNB

nb_model = GaussianNB()
nb_model = nb_model.fit(x_train, y_train)

y_pred = nb_model.predict(x_test)
# print(classification_report(y_test, y_pred))

# Logistic Regression
from sklearn.linear_model import LogisticRegression

lg_model = LogisticRegression()
lg_model = lg_model.fit(x_train, y_train)

y_pred = lg_model.predict(x_test)

# print(classification_report(y_test, y_pred))

# Support Vector Machine
from sklearn.svm import SVC

svm_model = SVC()
svm_model = svm_model.fit(x_train, y_train)

y_pred = svm_model.predict(x_test)

# print(classification_report(y_test, y_pred))

# Neural Networks
import tensorflow as tf

def train_model(x_train, y_train, num_nodes, dropout_prob, lr, batch_size, epochs):
  nn_model = tf.keras.Sequential([
    tf.keras.Input(shape=(10,)),
    tf.keras.layers.Dense(num_nodes, activation='relu'),
    tf.keras.layers.Dropout(dropout_prob),
    tf.keras.layers.Dense(num_nodes, activation='relu'),
    tf.keras.layers.Dropout(dropout_prob),
    tf.keras.layers.Dense(1, activation='sigmoid')
  ])

  nn_model.compile(optimizer = tf.keras.optimizers.Adam(lr), loss='binary_crossentropy', metrics=['accuracy'])

  history = nn_model.fit(
   x_train, y_train,
   epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=0
  )

  return nn_model, history

def plot_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.plot(history.history['loss'], label='loss')
    ax1.plot(history.history['val_loss'], label='val_loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Binary crossentropy')
    ax1.grid(True)

    ax2.plot(history.history['accuracy'], label='accuracy')
    ax2.plot(history.history['val_accuracy'], label='val_accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.grid(True)
    
    filename = f"plots2/plot_nodes{num_nodes}_drop{int(dropout_prob*100)}_lr{lr}_bs{batch_size}.png"
    # plt.savefig(filename)
    plt.close()

least_val_loss = float('inf')
least_loss_model = None

epochs = 100
# for num_nodes in [16, 32, 64]:
#    for dropout_prob in [0, 0.2]:
#       for lr in [0.01, 0.005, 0.001]:
#          for batch_size in [32, 64, 128]:
#             print(f"{num_nodes} nodes, dropout {dropout_prob}, lr {lr}, batch_size {batch_size}")
#             model, history = train_model(x_train, y_train, num_nodes, dropout_prob, lr, batch_size, epochs)
#             plot_history(history)
#             val_loss = model.evaluate(x_valid, y_valid, verbose=0)[0]
#             if val_loss < least_val_loss:
#                least_val_loss = val_loss
#                least_loss_model = model

# y_pred = least_loss_model.predict(x_test)
y_pred = (y_pred>0.5).astype(int).reshape(-1,)

# print(classification_report(y_test, y_pred))