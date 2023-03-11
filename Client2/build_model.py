import os
import pandas as pd
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow.python.keras.callbacks import (EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, History)
from tensorflow.python.keras.layers import (Conv1D, MaxPooling1D, ThresholdedReLU, Embedding,)
from tensorflow.python.keras.layers import Input, Flatten, Dense, Dropout
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.metrics import AUC
from sklearn.model_selection import train_test_split, StratifiedKFold

from typing import List, Tuple

def build_model() -> Model:
    # build model
    max_length = 127
    main_input = Input(shape=(max_length,), dtype="int32", name="main_input")
    embedding = Embedding(input_dim=128, output_dim=128, input_length=max_length)(main_input)
    conv1 = Conv1D(filters=128, kernel_size=3, padding="same", strides=1)(embedding)
    thresh1 = ThresholdedReLU(1e-6)(conv1)
    max_pool1 = MaxPooling1D(pool_size=2, padding="same")(thresh1)
    conv2 = Conv1D(filters=128, kernel_size=2, padding="same", strides=1)(max_pool1)
    thresh2 = ThresholdedReLU(1e-6)(conv2)
    max_pool2 = MaxPooling1D(pool_size=2, padding="same")(thresh2)
    flatten = Flatten()(max_pool2)
    fc = Dense(64)(flatten)
    thresh_fc = ThresholdedReLU(1e-6)(fc)
    drop = Dropout(0.5)(thresh_fc)
    output = Dense(1, activation="sigmoid")(drop)
    model = Model(inputs=main_input, outputs=output)
    '''precision = as_keras_metric(tf.metrics.precision)
    recall = as_keras_metric(tf.metrics.recall)'''
    model.compile(
        loss="binary_crossentropy",
        optimizer="adam",
        metrics=["mae", "mean_squared_error", "acc", AUC()],
    )
    #current_model.fit(X_train, y_train, batch_size=16, epochs=5)
    model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
    return model

if __name__ == "__main__":
    build_model()