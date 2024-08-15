"""`Datachart` is a data visualization package.

The `datachart` package provides utilities for easier data visualization. It provides
a set of modules and utilities for data visualization, creating different charts
and plots. It also provides methods for defining your own plot styles, and support
for calculating the statistics.

Modules:
    charts: The module containing the methods for creating different charts.
    utils: The module containing the utility classes and methods.
    config: The module containing the utility for customizing the plot styles.
    themes: The module containing the predefined style themes.
    constants: The module containing the predefined constants used for easier plot creation.
    typings: The module containing all of the typings used across the module.

"""

__version__ = "0.6.1"

from . import charts
from . import utils
from . import config
from . import themes
from . import constants
from . import typings


__all__ = [
    "charts",
    "utils",
    "config",
    "themes",
    "constants",
    "typings",
]
