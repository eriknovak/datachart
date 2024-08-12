import copy
import json
import warnings
from typing import Any

# import the schemas
from datachart.typings import StyleAttrs
from datachart.constants import THEME

# import the themes
from ..themes import DEFAULT_THEME, GREYSCALE_THEME


class Config:
    """The class representing the configuration options.

    Attributes:
        config (StyleAttrs): The style configuration.

    Methods:
        set_theme(theme):
            Set the global configuration to match the theme.
        reset_config():
            Resets the global configuration.
        update_config(config):
            Updates the global configuration.
        get(attr, default):
            Gets the associated configuration attribute.

    """

    config: StyleAttrs

    def __init__(self):
        """Initializes the global configuration."""

        self.config = copy.deepcopy(DEFAULT_THEME)
        self.theme = THEME.DEFAULT

    def set_theme(self, theme: THEME) -> None:
        """Sets the global configuration to match the theme.

        Examples:
            >>> from datachart.constants import THEME
            >>> from datachart.config import config
            >>> config.set_theme(THEME.DEFAULT)
            >>> config.get("theme")
            'default'

        Args:
            theme: The theme to be set.

        """
        if theme == THEME.DEFAULT:
            self.config = copy.deepcopy(DEFAULT_THEME)
            self.theme = THEME.DEFAULT
        elif theme == THEME.GREYSCALE:
            self.config = copy.deepcopy(GREYSCALE_THEME)
            self.theme = THEME.GREYSCALE
        else:
            warnings.warn(
                f"Warning: {theme} is not a valid theme. Must be one of {[THEME.DEFAULT, THEME.GREYSCALE]}. Reverting to last active theme..."
            )
            self.set_theme(self.theme)

    def reset_config(self) -> None:
        """Resets the global configuration.

        Examples:
            >>> from datachart.config import config
            >>> config.reset_config()
            >>> config.get("theme")
            'default'

        """
        self.config = copy.deepcopy(DEFAULT_THEME)

    def update_config(self, config: StyleAttrs) -> None:
        """Updates the global configuration.

        Examples:
            >>> from datachart.config import config
            >>> config.update_config({"font_general_color": "#FFFFFF"})
            >>> config.get("font_general_color")
            '#FFFFFF'

        Args:
            config: The configuration attributes to be updated.

        """

        for key, val in config.items():
            if key not in self.config:
                print(f"Warning: Attribute '{key}' is not valid. Skipping attribute...")
                continue
            self.config[key] = val

    def __getitem__(self, attr: str) -> Any:
        """Gets the associated configuration attribute.

        Examples:
            >>> from datachart.config import config
            >>> config["font_general_color"]
            '#FFFFFF'

        Args:
            attr: The attribute to retrieve.

        Returns:
            The attribute value if present. Otherwise, `None`.

        """
        return self.config[attr] if attr in self.config else None

    def get(self, attr: str, default: Any = None) -> Any:
        """Gets the associated configuration attribute.

        Examples:
            >>> from datachart.config import config
            >>> config.get("font_general_color")
            '#FFFFFF'

        Args:
            attr: The attribute to retrieve.
            default: The value to return, if the attribute is not present in the config.

        Returns:
            The attribute value if present. Otherwise, returns the `default` value.

        """
        return self.config.get(attr, default)

    def __repr__(self):
        """Represents the configuration as a json string."""
        return json.dumps(self.config, ensure_ascii=False, indent=4)


config: Config = Config()
"""The configuration instance that the users should interact with."""
