"""The module containing the `config`.

The `config` module contains the configuration objects, enabling the users
to globally customize the chart and plot styles.

Attributes:
    config (Config): The configuration instance.

Classes:
    Config: The configuration class.

"""

# import configuration object
from .configuration import config, Config


__all__ = ["config", "Config"]
