import copy
import json

# import the schemas
from ..schema.definitions import ConfigAttrs

# import the themes
from .themes import DEFAULT_THEME


class Config:
    config: ConfigAttrs

    def __init__(self):
        self.config = copy.deepcopy(DEFAULT_THEME)

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
