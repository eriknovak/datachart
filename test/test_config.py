import unittest

from datachart.config import config
from datachart.themes import DEFAULT_THEME


class TestConfig(unittest.TestCase):
    def test_initial_config(self):
        for key, val in DEFAULT_THEME.items():
            self.assertEqual(config[key], val)

    def test_update_config(self):
        updated_config = {"font.general.color": "#FFFFFF"}
        config.update_config(config=updated_config)
        for key, val in updated_config.items():
            self.assertEqual(config[key], val)

    def test_reset_config(self):
        config.reset_config()
        for key, val in DEFAULT_THEME.items():
            self.assertEqual(config[key], val)


if __name__ == "__main__":
    unittest.main()
