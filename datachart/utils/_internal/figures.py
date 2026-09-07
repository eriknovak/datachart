"""Unmanaged figure construction and display.

Figures are created directly — never through pyplot — so they are owned by the
caller and garbage-collected like any object instead of accumulating in
pyplot's global figure manager. Displaying is explicit via
`DatachartFigure.show`, which with `interactive=True` also attaches the hover
annotations over the layers' registered hover targets (ADR 0031).
"""

import importlib
import io
import itertools
import numbers
import warnings

import numpy as np
import matplotlib._constrained_layout as _constrained_layout
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.figure import Figure
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, PathPatch


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


def _import_interactive(name: str):
    """Import an `interactive` extra's package, naming the extra when it is missing."""

    try:
        return importlib.import_module(name)
    except ImportError as error:
        raise ImportError(
            f"`show(interactive=True)` needs the `{name.split('.')[0]}` package; "
            'install it with `pip install "datachart[interactive]"`.'
        ) from error


# numbers the widget canvases like pyplot numbers its figures
_widget_numbers = itertools.count(1)


def _axis_name(ax, which: str) -> str:
    """The visible label of an axis: its own, a shared sibling's, the figure's, or `x`/`y`.

    A twin axes labels only the axis it adds, so the shared one is read off
    the siblings in its slot — never a grid cell sharing the axis from another
    slot; a chart figure labels its single plot at the figure level.
    """

    shared = ax.get_shared_x_axes() if which == "x" else ax.get_shared_y_axes()
    slot = ax.get_position().bounds
    twins = [s for s in shared.get_siblings(ax) if s.get_position().bounds == slot]
    for candidate in [ax, *twins]:
        label = getattr(candidate, f"get_{which}label")().strip()
        if label:
            return label
    sup_label = getattr(ax.figure, f"_sup{which}label", None)
    if sup_label is not None and sup_label.get_text().strip():
        return sup_label.get_text().strip()
    return which


def _hover_value(ax, which: str, value) -> str:
    """Format a datum value like the axis formats its coordinates; text as is."""

    if isinstance(value, str):
        return value
    return getattr(ax, f"format_{which}data")(value).strip()


def _plain_value(value) -> str:
    """A field value as plain text: whole numbers without a fraction, reals positional."""

    if isinstance(value, numbers.Real) and not isinstance(value, numbers.Integral):
        if not np.isfinite(value):
            return str(value)
        return np.format_float_positional(value, precision=6, trim="-")
    return str(value)


def _hover_text(artist, datum: dict) -> str:
    """The annotation for a datum: legend label, then one `name: value` line per field.

    `x` and `y` are axis coordinates, named and formatted by the axes they
    are drawn on; every other field is shown under its own key, in the
    datum's order (ADR 0031).
    """

    ax = artist.axes if hasattr(artist, "axes") else artist[0].axes
    label = datum.get("label")
    lines = [] if label is None or str(label).startswith("_") else [str(label)]
    for key, value in datum.items():
        if key == "label":
            continue
        if key in ("x", "y"):
            lines.append(f"{_axis_name(ax, key)}: {_hover_value(ax, key, value)}")
        else:
            lines.append(f"{key}: {_plain_value(value)}")
    return "\n".join(lines)


def _selection_index(index):
    """The element index of an mplcursors selection, snapped to the nearest datum.

    Line segments pick a fractional index, step lines an `Index` carrying the
    source point as `.int`; collections, images, and contour sets pick a
    tuple, whose components snap the same way.
    """

    if isinstance(index, tuple):
        return tuple(_selection_index(component) for component in index)
    if hasattr(index, "int"):
        return int(index.int)
    return int(round(float(index)))


def _extend_pickers() -> None:
    """Teach mplcursors the two artist kinds it has no pick for.

    Registered through mplcursors' own single-dispatch seam, only where it
    has no implementation, so an upstream one wins once it exists. A filled
    polygon collection (a stacked band, a violin body, a hexagon) is picked
    by matplotlib's containment test, reporting the polygon and its vertex
    nearest the pointer; an arrow patch (a network edge) is picked like any
    other patch, by the distance to its outline.
    """

    from mplcursors._pick_info import Selection, compute_pick, get_ann_text

    fallback = compute_pick.dispatch(object)
    if compute_pick.dispatch(FancyArrowPatch) is fallback:
        compute_pick.register(FancyArrowPatch, compute_pick.dispatch(PathPatch))
    if compute_pick.dispatch(PolyCollection) is not fallback:
        return
    # the default text is replaced by the datum's; a collection's will do
    get_ann_text.register(PolyCollection, get_ann_text.dispatch(PathCollection))

    @compute_pick.register(PolyCollection)
    def _(artist, event):
        contains, info = artist.contains(event)
        if not contains:
            return None
        polygon = int(info["ind"][-1])
        paths, offsets = artist.get_paths(), artist.get_offsets()
        screen = artist.get_transform().transform_path(paths[polygon % len(paths)])
        vertices = screen.vertices
        if len(offsets):
            offset = offsets[polygon % len(offsets)]
            vertices = vertices + artist.get_offset_transform().transform(offset)
        vertex = int(np.nanargmin(np.hypot(*(vertices - [event.x, event.y]).T)))
        return Selection(
            artist, (event.xdata, event.ydata), (polygon, vertex), 0, None, None
        )


class DatachartFigure(Figure):
    """A figure owned by the caller, never registered with pyplot.

    Creating a chart never displays it and never accumulates global state;
    call `show()` to display the figure — inline in notebooks, in a GUI
    window in scripts.
    """

    def show(self, warn=True, interactive=False):
        """Display the figure.

        Showing is the only way a figure appears: in notebooks the figure is
        displayed inline as a PNG payload; elsewhere it is adopted into
        pyplot's figure manager and shown via `plt.show()`, so a GUI window
        opens where a backend supports one.

        With `interactive=True` the figure becomes zoomable and pannable and
        hovering a mark shows its data: in notebooks the figure is displayed
        on an `ipympl` widget canvas with the matplotlib toolbar, in scripts
        the GUI window's toolbar already provides zoom and pan. Hovering a
        line point, scatter point, or bar annotates it with the series'
        legend label and one `name: value` line per axis, named after the
        axis labels when set; the annotation wears the theme's text
        annotation style. Other chart types zoom and pan but show no hover
        annotation. The optional dependencies come with the
        `interactive` extra: `pip install "datachart[interactive]"`.

        !!! info "Added in Unreleased"

            The `interactive` parameter.

        Args:
            warn: If True, warn when the backend cannot open a window.
            interactive: If True, display the figure with zoom, pan, and
                hover-to-inspect annotations.

        Raises:
            ImportError: If `interactive` is True and `ipympl` or
                `mplcursors` is not installed.
        """
        if _in_notebook_kernel():
            if interactive:
                self._show_widget()
                return

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

        if interactive:
            # fail before any pyplot state changes
            _import_interactive("mplcursors")

        import matplotlib.pyplot as plt

        if self.canvas is None or self.canvas.manager is None:
            # adopt into pyplot: steal a fresh manager and point it at us
            dummy = plt.figure(figsize=self.get_size_inches())
            manager = dummy.canvas.manager
            manager.canvas.figure = self
            self.set_canvas(manager.canvas)
        if interactive:
            self._attach_hover()
        with warnings.catch_warnings():
            if not warn:
                warnings.simplefilter("ignore")
            plt.show()

    def _show_widget(self) -> None:
        """Display the figure on an ipympl widget canvas, with hover attached.

        The canvas and manager are built directly rather than through the
        backend's factory, so the figure stays unmanaged (ADR 0008): nothing
        lands in pyplot's registry or in ipympl's post-cell display queue.
        """

        nbagg = _import_interactive("ipympl.backend_nbagg")
        _import_interactive("mplcursors")
        if not isinstance(self.canvas, nbagg.Canvas):
            with warnings.catch_warnings():
                # ipympl's toolbar trips a traitlets deprecation on init, on
                # `%matplotlib widget` too (matplotlib/ipympl#488)
                warnings.filterwarnings(
                    "ignore", category=DeprecationWarning, module="traitlets"
                )
                manager = nbagg.FigureManager(nbagg.Canvas(self), next(_widget_numbers))
        else:
            manager = self.canvas.manager
        self._attach_hover()
        manager.show()

    def _attach_hover(self) -> None:
        """Attach one hover cursor to the current canvas over the registered targets."""

        import mplcursors

        if getattr(self, "_hover_canvas", None) is self.canvas:
            return
        _extend_pickers()
        previous = getattr(self, "_hover_cursor", None)
        if previous is not None:
            # bound to the canvas a previous show() swapped out
            previous.remove()
        targets = getattr(self, "_hover_targets", [])
        resolvers = {id(artist): resolver for artist, resolver in targets}

        def annotate(selection):
            resolver = resolvers.get(id(selection.artist))
            if resolver is None:
                return
            index = _selection_index(selection.index)
            selection.annotation.set_text(
                _hover_text(selection.artist, resolver(index))
            )
            # a pick between two line points snaps to the one it reports
            if isinstance(selection.artist, Line2D):
                selection.annotation.xy = selection.artist.get_xydata()[index]

        cursor = mplcursors.cursor(
            [artist for artist, _ in targets],
            hover=True,
            annotation_kwargs=getattr(self, "_hover_style", None),
        )
        cursor.connect("add", annotate)
        self._hover_cursor = cursor
        self._hover_canvas = self.canvas


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
