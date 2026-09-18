"""`Datachart` is a data visualization package.

The `datachart` package provides utilities for easier data visualization: chart
functions that return a matplotlib figure, the composition of finished figures,
a global style configuration with predefined themes, and the statistics behind
the charts. Each module has its own reference page.

"""

__version__ = "0.10.1"

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
