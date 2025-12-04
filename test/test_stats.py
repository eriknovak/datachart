import unittest

from datachart.utils.stats import (
    minimum,
    maximum,
    sum_values,
    variance,
    iqr,
    correlation,
)


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

    # =====================================
    # Test sum_values
    # =====================================

    def test_sum_values_int(self):
        # check integer values
        int_list = [1, 2, 3, 4, 5]
        result = sum_values(int_list)
        self.assertEqual(result, 15.0)

    def test_sum_values_float(self):
        # check float values
        float_list = [1.5, 2.5, 3.0]
        result = sum_values(float_list)
        self.assertEqual(result, 7.0)

    def test_sum_values_empty(self):
        # check empty list
        empty_list = []
        result = sum_values(empty_list)
        self.assertEqual(result, 0.0)

    # =====================================
    # Test variance
    # =====================================

    def test_variance_int(self):
        # check integer values
        int_list = [1, 2, 3, 4, 5]
        result = variance(int_list)
        self.assertEqual(result, 2.0)

    def test_variance_float(self):
        # check float values
        float_list = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        result = variance(float_list)
        self.assertEqual(result, 4.0)

    def test_variance_single(self):
        # check single value (variance should be 0)
        single_list = [5]
        result = variance(single_list)
        self.assertEqual(result, 0.0)

    # =====================================
    # Test iqr
    # =====================================

    def test_iqr_basic(self):
        # check basic interquartile range
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = iqr(values)
        self.assertEqual(result, 4.5)

    def test_iqr_symmetric(self):
        # check symmetric distribution
        values = [1, 2, 3, 4, 5, 6, 7]
        result = iqr(values)
        self.assertEqual(result, 3.0)

    # =====================================
    # Test correlation
    # =====================================

    def test_correlation_perfect_positive(self):
        # check perfect positive correlation
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        result = correlation(x, y)
        self.assertAlmostEqual(result, 1.0, places=10)

    def test_correlation_perfect_negative(self):
        # check perfect negative correlation
        x = [1, 2, 3, 4, 5]
        y = [5, 4, 3, 2, 1]
        result = correlation(x, y)
        self.assertAlmostEqual(result, -1.0, places=10)

    def test_correlation_no_correlation(self):
        # check no correlation (constant y)
        x = [1, 2, 3, 4, 5]
        y = [3, 3, 3, 3, 3]
        result = correlation(x, y)
        # When one variable is constant, correlation is NaN
        self.assertTrue(result != result)  # NaN check

    def test_correlation_length_mismatch(self):
        # check that mismatched lengths raise ValueError
        x = [1, 2, 3]
        y = [1, 2]
        with self.assertRaises(ValueError):
            correlation(x, y)

    def test_correlation_type_error(self):
        # check that invalid types raise TypeError
        with self.assertRaises(TypeError):
            correlation("not a list", [1, 2, 3])
        with self.assertRaises(TypeError):
            correlation([1, 2, 3], "not a list")


if __name__ == "__main__":
    unittest.main()
