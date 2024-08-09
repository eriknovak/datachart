import unittest

from datachart.utils.stats import minimum, maximum


# =====================================
# Test Stats
# =====================================

class TestStats(unittest.TestCase):

    def test_minimum_int(self):
        # check integer values
        int_list = [1, 2, 3, 4]
        min_val = minimum(int_list)
        self.assertEqual(min_val, 1)

    def test_minimum_float(self):
        # check float values
        float_list = [1.0, 2.0, 3.0, 4.0]
        min_val = minimum(float_list)
        self.assertEqual(min_val, 1.0)

    def test_maximum_int(self):
        # check integer values
        int_list = [1, 2, 3, 4]
        min_val = maximum(int_list)
        self.assertEqual(min_val, 4)

    def test_maximum_float(self):
        # check float values
        float_list = [1.0, 2.0, 3.0, 4.0]
        min_val = maximum(float_list)
        self.assertEqual(min_val, 4.0)


if __name__ == "__main__":
    unittest.main()
