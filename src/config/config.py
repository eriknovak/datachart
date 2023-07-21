import copy
import json
from typing import Any, Dict

from .themes import DEFAULT_THEME


class Config:
    def __init__(self):
        self.config = copy.deepcopy(DEFAULT_THEME)

    def reset_config(self) -> None:
        """Resets the global configuration"""
        self.config = copy.deepcopy(DEFAULT_THEME)

    def update_config(self, config: Dict[str, Any]) -> None:
        """Updates the global configuration"""
        self.config.update(config)

    def __call__(self):
        return self.config


config = Config()
