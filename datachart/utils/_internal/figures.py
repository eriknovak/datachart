"""Unmanaged figure construction (ADR 0008).

Figures are created directly — never through pyplot — so they are owned by the
caller and garbage-collected like any object instead of accumulating in
pyplot's global figure manager. Displaying is explicit via
`DatachartFigure.show`.
"""

import io
import warnings

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def _in_notebook_kernel() -> bool:
    # kernel detection beats backend sniffing: the backend may resolve to
    # Agg inside Jupyter (MPLBACKEND, matplotlibrc) and inline display
    # must still win there
    try:
        from IPython.core.getipython import get_ipython
    except ImportError:
        return False
    shell = get_ipython()
    return shell is not None and shell.__class__.__name__ == "ZMQInteractiveShell"


class DatachartFigure(Figure):
    """A figure owned by the caller, never registered with pyplot.

    Creating a chart never displays it and never accumulates global state;
    call `show()` to display the figure — inline in notebooks, in a GUI
    window in scripts.
    """

    def show(self, warn=True):
        """Display the figure.

        Showing is the only way a figure appears: in notebooks the figure is
        displayed inline as a PNG payload; elsewhere it is adopted into
        pyplot's figure manager and shown via `plt.show()`, so a GUI window
        opens where a backend supports one.

        Args:
            warn: If True, warn when the backend cannot open a window.
        """
        if _in_notebook_kernel():
            from IPython.display import display

            # a raw payload needs no repr hook, pyplot, or IPython
            # matplotlib integration — and therefore cannot display twice
            buffer = io.BytesIO()
            self.savefig(buffer, format="png", bbox_inches="tight")
            display(
                {"image/png": buffer.getvalue(), "text/plain": repr(self)},
                raw=True,
            )
            return

        import matplotlib.pyplot as plt

        if self.canvas is None or self.canvas.manager is None:
            # adopt into pyplot: steal a fresh manager and point it at us
            dummy = plt.figure(figsize=self.get_size_inches())
            manager = dummy.canvas.manager
            manager.canvas.figure = self
            self.set_canvas(manager.canvas)
        with warnings.catch_warnings():
            if not warn:
                warnings.simplefilter("ignore")
            plt.show()


def new_figure(figsize=None) -> DatachartFigure:
    """Create an unmanaged, constrained-layout figure.

    An Agg canvas is attached so `figure.canvas.draw()` and pixel-buffer
    access work without pyplot; `show()` swaps in an interactive canvas.

    Args:
        figsize: The figure size in inches; `None` uses the matplotlib default.

    Returns:
        The unmanaged figure.

    """
    figure = DatachartFigure(figsize=figsize, layout="constrained")
    FigureCanvasAgg(figure)
    return figure
