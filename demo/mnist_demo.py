
# 79: -------------------------------------------------------------------------

# imports: --------------------------------------------------------------------
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

# mnist hand-written digit data: ----------------------------------------------
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
#x_train.shape, y_train.shape
#x_train.dtype

# normalize and flatten data: -------------------------------------------------
x_train = x_train.astype('float32') / 255
x_train_flat = x_train.reshape(x_train.shape[0], np.prod(x_train.shape[1:]))

x_test = x_test.astype('float32') / 255
x_test_flat = x_test.reshape(x_test.shape[0], np.prod(x_test.shape[1:]))

assert x_train_flat.shape[1:] == x_test_flat.shape[1:]

# set aside validation data: --------------------------------------------------
nv = 10000
x_val, x_val_flat, y_val = x_train[:nv], x_train_flat[:nv], y_train[:nv]
x_train, x_train_flat, y_train = x_train[nv:], x_train_flat[nv:], y_train[nv:]

# simple sequential model with dropout: ---------------------------------------

# 128r -> .2d
m0 = Sequential([
    layers.Dense(128, activation='relu', input_shape=(x_train.shape[1],)),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

m0.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

h0 = m0.fit(
    x_train_flat, y_train,
    epochs=5, batch_size=128,
    validation_data=(x_val_flat, y_val)
)

m0.summary()

# note the reason we use 'sparse_categorical_crossentropy' above
y_train_c = tf.keras.utils.to_categorical(y_train)
#y_train_c.shape # use with loss = 'categorical_crossentropy'

# build the same model with the functional API: -------------------------------
input_tensor = layers.Input(shape=(np.prod(x_train.shape[1:]),))
x1 = layers.Dense(128, activation='relu')(input_tensor)
x2 = layers.Dropout(0.2)(x1)
output_tensor = layers.Dense(10, activation='softmax')(x2)

m1 = tf.keras.models.Model(inputs=input_tensor, outputs=output_tensor)

m1.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

h1 = m1.fit(
    x_train_flat, y_train,
    epochs=5, batch_size=128,
    validation_data=(x_val, y_val)
)

m1.summary()

# convolutional layers: -------------------------------------------------------
#help(layers.Conv2D)
#help(layers.MaxPooling2D)
m2 = Sequential([
    layers.Conv2D(
        32,
        kernel_size=(3, 3),
        activation='relu',
        input_shape=(28, 28, 1, )
    ),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

m2.summary()

m2.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

nt = x_train.shape[0]
h2 = m2.fit(
    x_train.reshape(nt, 28, 28, 1), y_train,
    epochs=5, batch_size=64,
    validation_data=(x_val.reshape(nv, 28, 28, 1), y_val)
)

[np.max(h.history['val_accuracy']) for h in [h0, h1, h2]]

# use the functional API to use both in parallel: -----------------------------

## dense network first
input_tensor = layers.Input(shape=(28, 28, 1, ))  
x0 = layers.Flatten()(input_tensor)
x1 = layers.Dense(128, activation='relu')(x0)
x2 = layers.Dropout(0.2)(x1)
x3 = layers.Dense(10, activation='softmax')(x2)

## convolutional network next
c1 = layers.Conv2D(32, (3, 3), activation='relu')(input_tensor)
c2 = layers.MaxPooling2D((2, 2))(c1)
c3 = layers.Conv2D(64, (3, 3), activation='relu')(c2)
c4 = layers.MaxPooling2D((2, 2))(c3)
c5 = layers.Conv2D(64, (3, 3), activation='relu')(c4)
c6 = layers.Flatten()(c5)
c7 = layers.Dense(64, activation='relu')(c6)
c8 = layers.Dense(10, activation='softmax')(c7)

join = layers.concatenate([x3, c8], axis=-1)

## output
output_tensor = layers.Dense(10, activation='softmax')(join)

m3 = tf.keras.models.Model(inputs=input_tensor, outputs=output_tensor)

m3.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

early_stop = tf.keras.callbacks.EarlyStopping(patience=3)
h3 = m3.fit(
    x_train.reshape(nt, 28, 28, 1), y_train,
    epochs=15, batch_size=64,
    validation_data=(x_val.reshape(nv, 28, 28, 1), y_val),
    callbacks=[early_stop]
)

[np.round(np.max(h.history['val_accuracy']), 4) for h in [h0, h1, h2, h3]]

# multi-output model: ---------------------------------------------------------

input_tensor = layers.Input(shape=(28, 28, 1, ))
z0 = layers.Flatten()(input_tensor)
z1 = layers.Dense(128, activation='relu')(z0)
z2 = layers.Dropout(0.2)(z1)
zero_nine = layers.Dense(10, activation='softmax')(z2)
odd_even = layers.Dense(2, activation='softmax')(z2)

m4 = tf.keras.models.Model(input_tensor, [zero_nine, odd_even])
m4.compile(
    optimizer='adam',
    loss=['sparse_categorical_crossentropy', 'sparse_categorical_crossentropy'],
    metrics=['accuracy']
)
h4 = m4.fit(
    x_train.reshape(nt, 28, 28, 1), [y_train, np.mod(y_train, 2)],
    epochs=5, batch_size=64,
    validation_data=(x_val.reshape(nv, 28, 28, 1), (y_val, np.mod(y_val, 2)))
)

#y_test[:3]
#[np.round(x, 3) for x in m4.predict(x_test[:3])]

# a simpler way to combine pre-trained versions of m1 and m2: ----------------- 

m1_flat = Sequential([layers.Flatten(input_shape=(28, 28, 1, )), m1])
m1_out = m1_flat(input_tensor)
m2_out = m2(input_tensor)
join = layers.concatenate([m1_out, m2_out], axis=-1)
m5_out = layers.Dense(10, activation='softmax')(join)
m5 = tf.keras.models.Model(input_tensor, m5_out)

m5.summary()

# "freeze" m1 and m2
m1.trainable = False
m2.trainable = False

m5.summary()

m5.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

h5 = m5.fit(
    x_train.reshape(nt, 28, 28, 1), y_train,
    epochs=15, batch_size=128,
    validation_data=(x_val.reshape(nv, 28, 28, 1), y_val),
    callbacks=[early_stop]
)

[np.round(np.max(h.history['val_accuracy']), 4) for h in [h0, h1, h2, h3, h5]]

[x.shape for x in m5.weights]
len(m5.weights)
np.round(m5.weights[14], 1)[[0, 10], :]
# 79: -------------------------------------------------------------------------
