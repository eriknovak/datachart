import unittest

import numpy as np

from datachart.constants import CONTOUR_LEVELS
from datachart.utils.stats import (
    minimum,
    maximum,
    sum_values,
    variance,
    iqr,
    correlation,
    contour_levels,
    kde1d,
    kde2d,
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

    # =====================================
    # Test contour_levels
    # =====================================

    @staticmethod
    def _surface(n=120):
        x = np.linspace(-5, 5, n)
        X, Y = np.meshgrid(x, x)
        return (X**2 + Y - 11) ** 2 + (X + Y**2 - 7) ** 2

    def test_contour_levels_auto_is_none(self):
        self.assertIsNone(contour_levels(self._surface(), CONTOUR_LEVELS.AUTO))
        self.assertIsNone(contour_levels(self._surface(), None))

    def test_contour_levels_rice_counts_per_axis(self):
        # rice on sqrt(cells): k = ceil(2 * 120 ** (1/3)) = 10 target bins
        levels = contour_levels(self._surface(), CONTOUR_LEVELS.RICE)
        z = self._surface()
        self.assertTrue(4 <= len(levels) - 1 <= 20)
        self.assertLessEqual(levels[0], z.min())
        self.assertGreaterEqual(levels[-1], z.max())
        self.assertEqual(levels, sorted(levels))

    def test_contour_levels_fd_denser_than_rice(self):
        z = self._surface()
        rice = contour_levels(z, CONTOUR_LEVELS.RICE)
        fd = contour_levels(z, CONTOUR_LEVELS.FD)
        self.assertGreater(len(fd), len(rice))

    def test_contour_levels_clamped(self):
        # a 2x2 grid: rice gives k = ceil(2 * 2 ** (1/3)) = 3 -> clamped to 4
        z = [[0.0, 1.0], [2.0, 3.0]]
        levels = contour_levels(z, CONTOUR_LEVELS.RICE)
        self.assertGreaterEqual(len(levels) - 1, 3)
        # a huge grid saturates at the 20-level cap
        levels = contour_levels(self._surface(2000), CONTOUR_LEVELS.FD)
        self.assertLessEqual(len(levels) - 1, 21)

    def test_contour_levels_fd_zero_iqr_falls_back(self):
        # a flat surface with one spike: IQR is 0, so fd falls back to 8 bins
        z = np.zeros((10, 10))
        z[0, 0] = 10.0
        levels = contour_levels(z, CONTOUR_LEVELS.FD)
        self.assertTrue(6 <= len(levels) - 1 <= 10)

    def test_contour_levels_passthrough(self):
        self.assertEqual(contour_levels(self._surface(), [1, 2, 3]), [1, 2, 3])
        self.assertEqual(contour_levels(self._surface(), 6), 6)

    def test_contour_levels_invalid_rule(self):
        with self.assertRaises(ValueError):
            contour_levels(self._surface(), "sturges")

    # Test kde1d / kde2d

    def test_kde1d_curve_integrates_to_one(self):
        values = np.random.RandomState(0).normal(size=300).tolist()
        curve = kde1d(values)
        self.assertEqual(len(curve), 100)
        x = [point["x"] for point in curve]
        y = [point["y"] for point in curve]
        self.assertAlmostEqual(float(np.trapezoid(y, x)), 1.0, places=2)
        # the grid extends past the values by `cut` bandwidths
        self.assertLess(x[0], min(values))
        self.assertGreater(x[-1], max(values))

    def test_kde1d_cut_zero_spans_the_values(self):
        curve = kde1d([1, 2, 3, 4], gridsize=4, cut=0)
        self.assertEqual([point["x"] for point in curve], [1.0, 2.0, 3.0, 4.0])

    def test_kde2d_shape_and_symmetry(self):
        surface = kde2d([1, 2, 3, 4], [1, 3, 2, 4], gridsize=(3, 2), cut=0)
        self.assertEqual(surface["x"], [1.0, 2.5, 4.0])
        self.assertEqual(surface["y"], [1.0, 4.0])
        z = np.asarray(surface["z"])
        self.assertEqual(z.shape, (2, 3))
        np.testing.assert_allclose(z[0], z[1][::-1])

    def test_kde2d_bandwidth_smooths(self):
        x = [1, 2, 3, 4, 5]
        y = [5, 3, 1, 3, 5]
        narrow = np.asarray(kde2d(x, y, bandwidth=0.2, gridsize=20)["z"])
        wide = np.asarray(kde2d(x, y, bandwidth=2.0, gridsize=20)["z"])
        self.assertGreater(narrow.max(), wide.max())

    def test_kde_invalid_inputs(self):
        with self.assertRaises(ValueError):
            kde1d([1, 2, 3], bandwidth="gaussian")
        with self.assertRaises(ValueError):
            kde1d([1])
        with self.assertRaises(ValueError):
            kde1d([1, float("nan"), 3])
        with self.assertRaises(ValueError):
            kde2d([1, 2, 3], [1, 2])
        with self.assertRaises(ValueError):
            kde2d([1, 2, 3], [1, 2, 3], cut=-1)


if __name__ == "__main__":
    unittest.main()
