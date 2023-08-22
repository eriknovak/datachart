import unittest

from datachart.utils.stats import get_min_max_values


class TestStats(unittest.TestCase):
    def test_get_min_max_values(self):
        # check integer values
        int_list = [1, 2, 3, 4]
        min_val, max_val = get_min_max_values(int_list)
        self.assertEqual(min_val, 1)
        self.assertEqual(max_val, 4)

        # check float values
        float_list = [1.0, 2.0, 3.0, 4.0]
        min_val, max_val = get_min_max_values(float_list)
        self.assertEqual(min_val, 1.0)
        self.assertEqual(max_val, 4.0)


if __name__ == "__main__":
    unittest.main()
