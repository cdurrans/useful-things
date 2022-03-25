#!/usr/bin/env python
# coding: utf-8

import pandas as pd
# import tensorflow as tf
import matplotlib.pyplot as plt
import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

import wandb

from wandb.keras import WandbCallback
wandb.init(project="kagglehousetraining")


# In[5]:


def plot_acc(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history['val_'+string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend([string, 'val_'+string])
    plt.show()


# In[6]:


train_df = pd.read_excel("kaggle-house.xlsx",sheet_name="train")

X = train_df.iloc[:,:-1]
y = train_df.iloc[:,-1:]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.1, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(X_train,y_train, test_size=0.2, random_state=0)


# In[6]:


#X_test


# # Parameters
# 
# #### optimizer = ['Adadelta', 'Adagrad', 'Adam', 'Ftrl', 'Nadam', 'RMSprop', 'SGD']
# 
# #### activation = ['linear', 'sigmoid', 'tanh', 'relu', 'selu', 'elu']

# In[7]:

dropOut = .25

model = keras.models.Sequential([
    keras.layers.Dense(units=128,input_shape=[304]), #Do not change input shape
    keras.layers.Dense(units=64,activation='relu'), #Kernel regularizers are optional
    keras.layers.Dropout(dropOut),#Add dropouts between layers
    keras.layers.Dense(units=32,activation='relu'), #Kernel regularizers are optional
    keras.layers.Dropout(dropOut),#Add dropouts between layers
    keras.layers.Dense(units=16,activation='relu'), #Kernel regularizers are optional
    keras.layers.Dropout(dropOut),#Add dropouts between layers
    keras.layers.Dense(units=1) #Do not change final layer
])

model.compile(optimizer='adam',loss='mean_squared_error')
model.summary()


import os
history = model.fit(X_train, y_train, batch_size=32, epochs=100, validation_data=(X_val,y_val) , callbacks=[WandbCallback()])
model.save(os.path.join(wandb.run.dir, "model.h5"))

# plot_acc(history,'loss')

test_y_hat = model.predict(X_test)
test_rmse = sqrt(mean_squared_error(y_test, test_y_hat))
print("RMSE: %d" % test_rmse)