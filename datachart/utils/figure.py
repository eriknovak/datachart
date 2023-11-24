import matplotlib.pyplot as plt

from ..constants import FIG_FORMAT


def save_figure(
    figure: plt.Figure,
    path: str,
    dpi: int = 300,
    format: FIG_FORMAT = None,
    transparent=False,
) -> None:
    """Save the figure to a file.

    Parameters
    ----------
    figure : plt.Figure
        The figure to save.
    path : str
        The path to save the figure to.
    dpi : int, optional (default=300)
        The DPI of the figure.
    format : FigFormat, optional (default=None)
        The format of the figure. If None, the format will be determined from the file extension.
    transparent : bool, optional (default=False)
        Whether to make the background transparent.
    """

    # save the figure to a file
    figure.savefig(path, dpi=dpi, format=format, transparent=transparent)
