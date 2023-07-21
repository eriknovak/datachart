import unittest

from config.config import DEFAULT_CONFIG, CURRENT_CONFIG, reset_config, update_config


class TestConfig(unittest.TestCase):
    def test_current_config(self):
        self.assertEqual(CURRENT_CONFIG, DEFAULT_CONFIG)


unittest.main()
