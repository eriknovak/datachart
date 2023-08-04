import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# input the configuration
from config import config

# TODO: define the bar chart component


def bar_chart(data, title: str = None, xlabel: str = None, ylabel: str = None):
    # check how many data point are there
    if not isinstance(data, list):
        raise ValueError("Parameter 'data' not a list")

    # format the data into a 2D array
    _data = data if all(isinstance(d, list) for d in data) else [data]
    _data = np.array(_data)

    figure, axes = plt.subplots(
        nrows=1, ncols=1, sharex=False, sharey=False, squeeze=False
    )

    axes[0, 0].hist(_data, bins=2)
    axes[0, 0].set_xlabel(xlabel)
    axes[0, 0].set_ylabel(ylabel)

    if title:
        figure.suptitle(title)

    plt.show()
