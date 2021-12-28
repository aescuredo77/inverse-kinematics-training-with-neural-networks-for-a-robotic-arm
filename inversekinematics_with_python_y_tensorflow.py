# -*- coding: utf-8 -*-
"""InverseKinematics with Python y Tensorflow

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rt-JDRdV_fdw6Sqiqw4KmKnpCsjVcesX
"""

import tensorflow as tf
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

my_data = genfromtxt('arm_data205.csv',delimiter = ';')
my_data= np.delete(my_data,0,0)
#print(my_data)
shuffled_index = np.random.permutation(len(my_data))
my_data = my_data[shuffled_index]

train_split = int(0.6 * len(my_data))
test_split = int(0.2 * len(my_data) + train_split)
data_train, data_validate, data_test= np.split(my_data,[train_split,test_split])
angle_train,cord_train = np.hsplit(data_train,2)
angle_validate, cord_validate = np.hsplit(data_validate, 2)
angle_test, cord_test = np.hsplit(data_test, 2)

print(angle_train.size)
print(cord_validate[2])

plt.plot(cord_train,'b.',label="Train")
plt.plot(cord_validate,'y.', label="Validate")
plt.plot(cord_test,'r.',label="Test")

plt.legend()
plt.show()

model_1 = tf.keras.Sequential()
model_1.add(tf.keras.layers.Dense(50,activation='relu', input_shape=(2,)))
model_1.add(tf.keras.layers.Dense(50,activation='relu'))
#model_1.add(tf.keras.layers.Dense(6,activation='relu'))
#model_1.add(tf.keras.layers.Dense(6,activation='relu'))
#model_1.add(tf.keras.layers.Dense(6,activation='relu'))
model_1.add(tf.keras.layers.Dense(2, activation='linear' ))
model_1.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
model_1.summary()

history_1= model_1.fit(cord_train,angle_train, epochs=600, batch_size=8, validation_data=(cord_validate,angle_validate))

loss = history_1.history['loss']
val_loss = history_1.history['val_loss']
epochs = range(1,len(loss)+1)
plt.plot(epochs, loss,'g.', label="Training loss")
plt.plot(epochs, val_loss, 'b.', label="Validation loss")
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

skip = 100
plt.plot(epochs[skip:], loss[skip:],'g.', label="Training loss")
plt.plot(epochs[skip:], val_loss[skip:], 'b.', label="Validation loss")
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

mae = history_1.history['mae']
val_mae = history_1.history['val_mae']
plt.plot(epochs[skip:], loss[skip:],'g.', label="Training loss")
plt.plot(epochs[skip:], val_mae[skip:], 'b.', label="Validation MAE")
plt.title('Training and validation mean absolute error')
plt.xlabel('Epochs')
plt.ylabel('MAE')
plt.legend()
plt.show()

predictions = model_1.predict(cord_train)
test = model_1.predict(cord_test)

plt.clf()
plt.title('Training data predicted vs actual values')
#plt.plot(test,'b.', label='Actual')
plt.plot(cord_train,predictions,'r.',label='Predicted')
plt.plot(cord_test,test,'b.', label='Actual')
#plt.plot(predictions,'r.',label='Predicted')

plt.legend()
plt.show()

model_1.save('arm_new205.h5')

model2= tf.keras.models.load_model('arm_model.h5')
resultado = model2.predict([(235,10)])
print(resultado)
print(type(resultado))

from math import pi

conv = 7400/2*pi
resultado= model_1.predict([(250.0 ,10.0)])
print(resultado)