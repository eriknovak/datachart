# ================================================
# Constants
# ================================================


class LineMarker:
    POINT = "."
    PIXEL = ","
    CROSS = "x"
    PLUS = "+"
    CIRCLE = "o"
    TRIANGLE = "v"
    SQUARE = "s"
    PENTAGON = "p"


class LineStyle:
    SOLID = "-"
    DASHED = "--"
    DASHDOT = "-."
    DOTTED = ":"


class LineDrawStyle:
    DEFAULT = "default"
    STEPS = "steps"
    STEPS_PRE = "steps-pre"
    STEPS_MID = "steps-mid"
    STEPS_POST = "steps-post"


class Figsize:
    A4_FULL = (8, 11)
    A4_WIDTH = (8, 1)


class FontStyle:
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    BOLD_ITALIC = "bold italic"


class FontWeight:
    NORMAL = "normal"
    BOLD = "bold"
