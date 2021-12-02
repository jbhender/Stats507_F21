# -*- coding: utf-8 -*-
"""
Keras and Tensorflow Demo using the Isolet Data

Data from:
 https://archive.ics.uci.edu/ml/machine-learning-databases/isolet/

Updated: Nov 29, 2021
Author: James Henderson
"""

# modules: --------------------------------------------------------------------
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers

# data preparation: -----------------------------------------------------------
df_file = "./isolet1+2+3+4.data"
df = pd.read_csv(df_file, header=None)

target = df.pop(617)
target -= 1

# normalize 
#train_min, train_max = df.min(), df.max()
#df = df.transform(lambda x: (x - np.min(x))/(np.max(x) - np.min(x)))

# prepare data for keras: -----------------------------------------------------
dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))

train_dataset = dataset.shuffle(len(df)).batch(1)

# define the model: -----------------------------------------------------------
model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(26, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# fit the model: --------------------------------------------------------------
model.fit(train_dataset, epochs=15)
m0 = './isolet_ex0_m0'
model.save(m0, save_format='tf')

new_model = tf.keras.models.load_model(m0)

# validation set: -------------------------------------------------------------
n0 = 52 * 26

df0, df1 = df.iloc[0:n0, ], df.iloc[n0:len(df), ]
t0, t1 = target[0:n0], target[n0:len(df)]

train = tf.data.Dataset.from_tensor_slices((df1.values, t1.values))
valid = tf.data.Dataset.from_tensor_slices((df0.values, t0.values))

train = train.shuffle(len(df1)).batch(26)
valid = valid.batch(26)

# model 1, 
m1 = tf.keras.models.Sequential()
m1.add(layers.Dense(128, activation='relu', input_shape=(df1.shape[1],)))
m1.add(layers.Dense(26, activation='softmax'))
m1.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

h1 = m1.fit(train, epochs=15, validation_data=valid)
yv = m1.predict(valid)
m1_loss, m1_accuracy = m1.evaluate(valid)
print('Model 1 Loss {}, Model 1 Accuracy {}'.format(m1_loss, m1_accuracy))

# model 2, uses dropout: ------------------------------------------------------
m2 = tf.keras.models.Sequential([
  layers.Dense(128, activation='relu', input_shape=(df1.shape[1], )),
  layers.Dropout(0.2),
  layers.Dense(26, activation='softmax')
])

m2.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
h2 = m2.fit(train, epochs=15, validation_data=valid)

m2_loss, m2_accuracy = m2.evaluate(valid, verbose=1)
print('Model 2 Loss {}, Model 2 Accuracy {}'.format(m2_loss, m2_accuracy))

# model 3, add another layer: -------------------------------------------------
m3 = tf.keras.models.Sequential([
  layers.Dense(128, activation='relu', input_shape=(df1.shape[1], )),
  layers.Dense(128, activation='relu'),
  layers.Dropout(0.2),
  layers.Dense(26, activation='softmax')
])

m3.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
h3 = m3.fit(train, epochs=15, validation_data=valid)

m3_loss, m3_accuracy = m3.evaluate(valid, verbose=1)
print('Model 3 Loss {}, Model 3 Accuracy {}'.format(m3_loss, m3_accuracy))

# model 4, make single layer larger: ------------------------------------------
m4 = tf.keras.models.Sequential([
  layers.Dense(256, activation='relu', input_shape=(df1.shape[1], )),
  layers.Dense(26, activation='softmax')
])

m4.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
h4 = m4.fit(train, epochs=15, validation_data=valid)

m4_loss, m4_accuracy = m4.evaluate(valid, verbose=1)
print('Model 4 Loss {}, Model 4 Accuracy {}'.format(m4_loss, m4_accuracy))

# model 5, make network deeper: ----------------------------------------------
m5 = tf.keras.models.Sequential([
  layers.Dense(128, activation='relu', input_shape=(df1.shape[1], )),
  layers.Dense(56, activation='relu'),
  layers.Dense(128, activation='relu'),
  layers.Dense(26, activation='softmax')
])

m5.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
h5 = m5.fit(train, epochs=15, validation_data=valid)

m5_loss, m5_accuracy = m5.evaluate(valid, verbose=1)
print('Model 5 Loss {}, Model 5 Accuracy {}'.format(m5_loss, m5_accuracy))

# model 6, smaller second layer: ---------------------------------------------
m6 = tf.keras.models.Sequential([
  layers.Dense(128, activation='relu', input_shape=(df1.shape[1], )),
  layers.Dense(56, activation='relu'),
  layers.Dense(26, activation='softmax')
])

m6.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
h6 = m6.fit(train, epochs=15, validation_data=valid)

m6_loss, m6_accuracy = m6.evaluate(valid, verbose=1)
print('Model 6 Loss {}, Model 6 Accuracy {}'.format(m6_loss, m6_accuracy))

# model 7, use regularization: -----------------------------------------------
m7 = tf.keras.models.Sequential([
  layers.Dense(
      128,
      activation='relu',
      input_shape=(df1.shape[1], ), 
      kernel_regularizer=tf.keras.regularizers.l2(0.001)
  ),
  layers.Dense(26, activation='softmax')
])

m7.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
h7 = m7.fit(train, epochs=15, validation_data=valid)

m7_loss, m7_accuracy = m7.evaluate(valid, verbose=1)
print('Model 7 Loss {}, Model 7 Accuracy {}'.format(m7_loss, m7_accuracy))

# validation comparison: ------------------------------------------------------
acc = ([
    m1_accuracy,
    m2_accuracy,
    m3_accuracy,
    m4_accuracy,                                                 
    m5_accuracy,
    m6_accuracy,
    m7_accuracy
])

models = {'m1': m1, 'm2': m2, 'm3': m3, 'm4': m4, 'm5': m5, 'm6': m6, 'm7': m7}

results = pd.DataFrame({'model': models.keys(), 'accuracy': acc})
results = results.sort_values('accuracy')

m_best = models[results.iloc[len(results) - 1, 0]]

# early stopping: -------------------------------------------------------------
best_acc = []
for h in (h1, h2, h3, h4, h5, h6, h7):
    best_acc.append(np.max(h.history['val_accuracy']))

early_stop = tf.keras.callbacks.EarlyStopping(patience=2)
m4b = tf.keras.models.clone_model(m4)
m4b.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
h4b = m4b.fit(train, epochs=15, validation_data=valid, callbacks=[early_stop])

# testing data: ---------------------------------------------------------------
test_file = "./isolet5.data"
df_test = pd.read_csv(test_file, header=None)

test_target = df_test.pop(617)
test_target -= 1

test = tf.data.Dataset.from_tensor_slices(
    (df_test.values, test_target.values)
)
test = test.batch(26)

m_best.evaluate(test)
