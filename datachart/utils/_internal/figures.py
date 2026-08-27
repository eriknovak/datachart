"""Unmanaged figure construction.

Figures are created directly — never through pyplot — so they are owned by the
caller and garbage-collected like any object instead of accumulating in
pyplot's global figure manager. Displaying is explicit via
`DatachartFigure.show`.
"""

import io
import warnings

import matplotlib._constrained_layout as _constrained_layout
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.layout_engine import ConstrainedLayoutEngine


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


def _propagate_nested_margins(layoutgrids) -> None:
    """Lift each nested gridspec's outer margins onto its parent cell.

    Constrained layout equalises the *inner* height of a gridspec's rows, and
    a row whose only content is a nested gridspec has no margins of its own,
    so it shrinks by its siblings' margins — a nested Grid alone in a host
    row collapses. Deepest nesting first, so margins reach the outermost grid.
    """
    nested = [gs for gs in layoutgrids if hasattr(gs, "_subplot_spec")]

    def depth(gs):
        d = 0
        while hasattr(gs, "_subplot_spec"):
            gs = gs._subplot_spec.get_gridspec()
            d += 1
        return d

    for gs in sorted(nested, key=depth, reverse=True):
        lg = layoutgrids[gs]
        vals = lg.margin_vals
        subplot_spec = gs._subplot_spec
        parent = layoutgrids.get(subplot_spec.get_gridspec())
        if parent is None:
            continue
        margin = {
            "left": vals["left"][0],
            "leftcb": vals["leftcb"][0],
            "right": vals["right"][-1],
            "rightcb": vals["rightcb"][-1],
            "top": vals["top"][0],
            "topcb": vals["topcb"][0],
            "bottom": vals["bottom"][-1],
            "bottomcb": vals["bottomcb"][-1],
        }
        parent.edit_outer_margin_mins(margin, subplot_spec)


class NestedGridLayoutEngine(ConstrainedLayoutEngine):
    """Constrained layout whose nested gridspecs size their parent cell."""

    def execute(self, fig):
        original = _constrained_layout.make_layout_margins

        def make_layout_margins(layoutgrids, *args, **kwargs):
            original(layoutgrids, *args, **kwargs)
            _propagate_nested_margins(layoutgrids)

        _constrained_layout.make_layout_margins = make_layout_margins
        try:
            return super().execute(fig)
        finally:
            _constrained_layout.make_layout_margins = original


def new_figure(figsize=None) -> DatachartFigure:
    """Create an unmanaged, constrained-layout figure.

    An Agg canvas is attached so `figure.canvas.draw()` and pixel-buffer
    access work without pyplot; `show()` swaps in an interactive canvas.

    Args:
        figsize: The figure size in inches; `None` uses the matplotlib default.

    Returns:
        The unmanaged figure.

    """
    figure = DatachartFigure(figsize=figsize, layout=NestedGridLayoutEngine())
    FigureCanvasAgg(figure)
    return figure
