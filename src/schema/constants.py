# ================================================
# Constants
# ================================================


class Figsize:
    """Figsize constants"""

    DEFAULT = (6.4, 4.8)
    A4 = (8.2, 11.6)
    A4_1_ROWS = (8.2, 2.4)
    A4_2_ROWS = (8.2, 4.8)
    A4_3_ROWS = (8.2, 7.2)


class FigFormat:
    """FigFormat constants"""

    DEFAULT = "png"
    SVG = "svg"
    PDF = "pdf"
    PNG = "png"


class FontStyle:
    """Font Style constants"""

    DEFAULT = "normal"
    NORMAL = "normal"
    ITALIC = "italic"
    OBLIQUE = "oblique"


class FontWeight:
    """Font Weight constants"""

    DEFAULT = "normal"
    ULTRA_LIGHT = "ultralight"
    LIGHT = "light"
    NORMAL = "normal"
    BOLD = "bold"
    HEAVY = "heavy"
    ULTRA_HEAVY = "ultrabold"


class LineMarker:
    """Line Marker constants"""

    PIXEL = ","
    POINT = "."
    CIRCLE = "o"
    TRIANGLE = "^"
    SQUARE = "s"
    PENTAGON = "p"
    HEXAGON = "h"
    STAR = "*"
    CROSS = "x"
    PLUS = "+"


class LineStyle:
    """Line Style constants"""

    SOLID = "-"
    DASHED = "--"
    DASHDOT = "-."
    DOTTED = ":"


class LineDrawStyle:
    """Line Draw Style constants"""

    DEFAULT = "default"
    STEPS = "steps-pre"
    STEPS_PRE = "steps-pre"
    STEPS_MID = "steps-mid"
    STEPS_POST = "steps-post"


class Hatch:
    """Hatch constants"""

    DEFAULT = None
    DIAGONAL = "/"
    VERTICAL = "|"
    HORIZONTAL = "-"
    CROSSED = "+"
    CROSSED_DIAGONAL = "x"
    DOTS = "."
    CIRCLES = "o"
    STARS = "*"


class LegendAlignment:
    DEFAULT = "left"
    CENTER = "center"
    RIGHT = "right"
    LEFT = "left"


class HistType:
    """Hist Type constants"""

    BAR = "bar"
    STEP = "step"
    STEPFILLED = "stepfilled"


class Colors:
    Blue = "blue"
    Green = "green"
    Orange = "orange"
    Purple = "purple"
    Grey = "grey"
    YlGnBu = "ylgnbu"
    YlGn = "ylgn"
    BuGn = "bugn"
    GnBu = "gnbu"
    PuBu = "pubu"
    RdBn = "rdbn"
    RdYlBu = "rdylbu"
    BrNg = "brng"
    PrGn = "prgn"
    PuOr = "puor"
    Rdgy = "rdgy"
    RdYlGn = "rdylgn"
    Spectral = "spectral"
    MixedLight = "mixed_light"
    MixedDark = "mixed_dark"
