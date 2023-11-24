# ================================================
# Constants
# ================================================


class FIG_SIZE:
    """Figsize constants"""

    DEFAULT = (6.4, 4.8)
    A4 = (8.2, 11.6)
    A4_NARROW = (8.2, 2.4)
    A4_REGULAR = (8.2, 4.8)
    A4_WIDE = (8.2, 7.2)

    SQUARE = (6.4, 6.4)
    SQUARE_SMALL = (4.8, 4.8)
    SQUARE_LARGE = (8.2, 8.2)


class FIG_FORMAT:
    """FigFormat constants"""

    DEFAULT = "png"
    SVG = "svg"
    PDF = "pdf"
    PNG = "png"
    WEBP = "webp"


class FONT_STYLE:
    """Font Style constants"""

    DEFAULT = "normal"
    NORMAL = "normal"
    ITALIC = "italic"
    OBLIQUE = "oblique"


class FONT_WEIGHT:
    """Font Weight constants"""

    DEFAULT = "normal"
    ULTRA_LIGHT = "ultralight"
    LIGHT = "light"
    NORMAL = "normal"
    BOLD = "bold"
    HEAVY = "heavy"
    ULTRA_HEAVY = "ultrabold"


class LINE_MARKER:
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


class LINE_STYLE:
    """Line Style constants"""

    SOLID = "-"
    DASHED = "--"
    DASHDOT = "-."
    DOTTED = ":"


class LINE_DRAW_STYLE:
    """Line Draw Style constants"""

    DEFAULT = "default"
    STEPS = "steps-pre"
    STEPS_PRE = "steps-pre"
    STEPS_MID = "steps-mid"
    STEPS_POST = "steps-post"


class HATCH_STYLE:
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


class LEGEND_ALIGN:
    DEFAULT = "left"
    CENTER = "center"
    RIGHT = "right"
    LEFT = "left"


class HISTOGRAM_TYPE:
    """Hist Type constants"""

    BAR = "bar"
    STEP = "step"
    STEPFILLED = "stepfilled"


class COLORS:
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
    RdGy = "rdgy"
    RdYlGn = "rdylgn"
    Spectral = "spectral"
    MixedLight = "mixed_light"
    MixedDark = "mixed_dark"


class NORMALIZE:
    LINEAR = "linear"
    LOG = "log"
    SYMLOG = "symlog"
    ASINH = "asinh"
    LOGIT = "logit"


class ORIENTATION:
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class VALFMT:
    DEFAULT = "{x}"
    INTEGER = "{x:d}"
    DECIMAL = "{x:.1f}"
    PERCENT = "{x:.1%}"


class THEME:
    DEFAULT = "default"
    GREYSCALE = "greyscale"
