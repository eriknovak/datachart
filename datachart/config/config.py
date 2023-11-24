import copy
import json
import warnings

# import the schemas
from datachart.definitions import ConfigAttrs
from datachart.constants import THEME

# import the themes
from ..themes import DEFAULT_THEME, GREYSCALE_THEME


class Config:
    config: ConfigAttrs

    def __init__(self):
        self.config = copy.deepcopy(DEFAULT_THEME)
        self.theme = THEME.DEFAULT

    def set_theme(self, theme: THEME) -> None:
        """Sets the global theme"""
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
        """Resets the global configuration"""
        self.config = copy.deepcopy(DEFAULT_THEME)

    def update_config(self, config: ConfigAttrs) -> None:
        """Updates the global configuration

        Parameters
        ----------
        config: ConfigAttrs
            The new configuration attributes.
        """

        for key, val in config.items():
            if key not in self.config:
                print(f"Warning: Attribute '{key}' is not valid. Skipping attribute...")
                continue
            self.config[key] = val

    def __getitem__(self, attr):
        """Gets the associated configuration attribute"""
        return self.config[attr]

    def get(self, attr, default=None):
        """Gets the associated configuration attribute"""
        return self.config.get(attr, default)

    def __repr__(self):
        return json.dumps(self.config, ensure_ascii=False, indent=4)


config = Config()
