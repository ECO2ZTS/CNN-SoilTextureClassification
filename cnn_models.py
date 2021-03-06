#!/usr/bin/env python
# coding: utf-8
"""Package including tensorflow.keras models."""

from tensorflow.keras.layers import (Concatenate, Conv1D, Dense, Flatten,
                                     Input, MaxPooling1D, Reshape)
from tensorflow.keras.models import Model


def getKerasModel(model_name):
    """Get keras model by name.

    Parameters
    ----------
    model_name : str
        Name of the respective model.

    Returns
    -------
    Sequential keras model
        Model.

    """
    if model_name == "LucasCNN":
        return LucasCNN()
    if model_name == "HuEtAl":
        return HuEtAl()
    if model_name == "LiuEtAl":
        return LiuEtAl()
    if model_name == "LucasResNet":
        return LucasResNet()
    if model_name == "LucasCoordConv":
        return LucasCoordConv()
    print("Error: Model {0} not implemented.".format(model_name))
    return None


def HuEtAl():
    """Return 1D-CNN by Wei Hu et al 2014."""
    seq_length = 256

    # definition by Hu et al for parameter k1 and k2
    kernel_size = seq_length // 9
    pool_size = int((seq_length - kernel_size + 1) / 35)

    inp = Input(shape=(seq_length, 1))

    # CONV1
    x = Conv1D(filters=20, kernel_size=kernel_size, activation="tanh")(inp)
    x = MaxPooling1D(pool_size)(x)

    # Flatten, FC1, Softmax
    x = Flatten()(x)
    x = Dense(units=100, activation="tanh")(x)
    x = Dense(4, activation="softmax")(x)

    return Model(inputs=inp, outputs=x)


def LiuEtAl():
    """Return 1D-CNN by Lanfa Liu et al 2018."""
    seq_length = 256
    kernel_size = 3

    inp = Input(shape=(seq_length, 1))

    # CONV1
    x = Conv1D(filters=32, kernel_size=kernel_size, activation="relu")(inp)
    x = MaxPooling1D(2)(x)

    # CONV2
    x = Conv1D(filters=32, kernel_size=kernel_size, activation='relu')(x)
    x = MaxPooling1D(2)(x)

    # CONV3
    x = Conv1D(filters=64, kernel_size=kernel_size, activation='relu')(x)
    x = MaxPooling1D(2)(x)

    # CONV4
    x = Conv1D(filters=64, kernel_size=kernel_size, activation='relu')(x)
    x = MaxPooling1D(2)(x)

    # Flatten & Softmax
    x = Flatten()(x)
    x = Dense(4, activation="softmax")(x)

    return Model(inputs=inp, outputs=x)


def LucasCNN():
    """Return LucasCNN implementation.

    Returns
    -------
    Sequential keras model
        Model.

    """
    seq_length = 256
    kernel_size = 3
    activation = "relu"
    padding = "valid"

    inp = Input(shape=(seq_length, 1))

    # CONV1
    x = Conv1D(filters=32,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(inp)
    x = MaxPooling1D(2)(x)

    # CONV2
    x = Conv1D(filters=32,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # CONV3
    x = Conv1D(filters=64,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # CONV4
    x = Conv1D(filters=64,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # Flatten, FC1, FC2, Softmax
    x = Flatten()(x)
    x = Dense(120, activation=activation)(x)
    x = Dense(160, activation=activation)(x)
    x = Dense(4, activation="softmax")(x)

    return Model(inputs=inp, outputs=x)


def LucasResNet():
    """Return LucasResNet implementation.

    Returns
    -------
    Sequential keras model
        Model.

    """
    seq_length = 256
    kernel_size = 3
    activation = "relu"
    padding = "same"

    inp = Input(shape=(seq_length, 1))

    # CONV1
    x = Conv1D(filters=32,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(inp)
    x = MaxPooling1D(2)(x)

    # CONV2
    x = Conv1D(filters=32,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # CONV3
    x = Conv1D(filters=64,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # CONV4
    x = Conv1D(filters=64,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # Residual block
    inp_res = Reshape((16, 16))(inp)
    x = Concatenate(axis=-1)([x, inp_res])

    # Flatten, FC1, FC2, Softmax
    x = Flatten()(x)
    x = Dense(150, activation=activation)(x)
    x = Dense(100, activation=activation)(x)
    x = Dense(4, activation="softmax")(x)

    return Model(inputs=inp, outputs=x)


def LucasCoordConv():
    """Return LucasCoordConv implementation.

    Returns
    -------
    Sequential keras model
        Model.

    """
    from coord import CoordinateChannel1D

    seq_length = 256
    kernel_size = 3
    activation = "relu"
    padding = "valid"

    inp = Input(shape=(seq_length, 1))

    # CoordCONV1
    x = CoordinateChannel1D()(inp)
    x = Conv1D(filters=32,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # CONV2
    x = Conv1D(filters=64,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # CONV3
    x = Conv1D(filters=64,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # CONV4
    x = Conv1D(filters=128,
               kernel_size=kernel_size,
               activation=activation,
               padding=padding)(x)
    x = MaxPooling1D(2)(x)

    # Flatte, FC1, FC2, Softmax
    x = Flatten()(x)
    x = Dense(256, activation=activation)(x)
    x = Dense(128, activation=activation)(x)
    x = Dense(4, activation="softmax")(x)

    return Model(inputs=inp, outputs=x)
