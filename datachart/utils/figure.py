"""The module containing the commone `figure` utilites.

The `figure` module provides a set of utilities for manipulating the images.

Methods:
    save_figure(figure, path, dpi, format, transparent):
        Saves the figure into a file using the provided format parameters.

"""

import matplotlib.pyplot as plt

from ..constants import FIG_FORMAT

# =====================================
# Helper functions
# =====================================


def save_figure(
    figure: plt.Figure,
    path: str,
    dpi: int = 300,
    format: FIG_FORMAT = None,
    transparent: bool = False,
) -> None:
    """Save the figure to a file.

    Args:
        figure: The figure to save.
        path: The path where the figure is saved.
        dpi: The DPI of the figure.
        format: The format of the figure. If `None`, the format will be determined from the file extension.
        transparent: Whether to make the background transparent.
    """

    # save the figure to a file
    figure.savefig(path, dpi=dpi, format=format, transparent=transparent)
