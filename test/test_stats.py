import unittest

import numpy as np

from datachart.utils.stats import (
    minimum,
    maximum,
    sum_values,
    variance,
    iqr,
    correlation,
    mean,
    median,
    spearman,
    mode,
    skewness,
    kurtosis,
    linear_fit,
    bootstrap_ci,
    histogram,
    rolling_mean,
    ewma,
    loess,
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

    # Test spearman

    def test_spearman_monotone_is_one(self):
        # a monotone but non-linear relation ranks perfectly
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]
        self.assertAlmostEqual(spearman(x, y), 1.0)
        self.assertAlmostEqual(spearman(x, y[::-1]), -1.0)

    def test_spearman_degenerate_is_nan(self):
        self.assertTrue(np.isnan(spearman([1], [2])))
        self.assertTrue(np.isnan(spearman([], [])))
        self.assertTrue(np.isnan(spearman([1, 2, 3], [4, 4, 4])))

    def test_spearman_invalid_inputs(self):
        with self.assertRaises(ValueError):
            spearman([1, 2, 3], [1, 2])
        with self.assertRaises(TypeError):
            spearman("abc", [1, 2, 3])
        with self.assertRaises(TypeError):
            spearman([1, 2, 3], "abc")

    # Test mode

    def test_mode_smallest_most_frequent(self):
        self.assertEqual(mode([3, 1, 2, 3, 1]), 1.0)
        self.assertEqual(mode([2.5, 2.5, 4]), 2.5)
        self.assertEqual(mode([7]), 7.0)

    def test_mode_empty_is_nan(self):
        self.assertTrue(np.isnan(mode([])))

    def test_mode_type_error(self):
        with self.assertRaises(TypeError):
            mode("abc")

    # Test skewness / kurtosis

    def test_skewness_sign(self):
        self.assertAlmostEqual(skewness([1, 2, 3, 4, 5]), 0.0)
        self.assertGreater(skewness([1, 1, 1, 2, 10]), 0)
        self.assertLess(skewness([-10, -2, -1, -1, -1]), 0)

    def test_kurtosis_is_excess(self):
        # a uniform spread has negative excess kurtosis, a heavy tail positive
        self.assertLess(kurtosis([1, 2, 3, 4, 5]), 0)
        self.assertGreater(kurtosis([0] * 20 + [50]), 0)

    def test_shape_degenerate_is_nan(self):
        for fn in (skewness, kurtosis):
            self.assertTrue(np.isnan(fn([])))
            self.assertTrue(np.isnan(fn([1])))
            self.assertTrue(np.isnan(fn([4, 4, 4])))

    def test_shape_type_error(self):
        with self.assertRaises(TypeError):
            skewness("abc")
        with self.assertRaises(TypeError):
            kurtosis("abc")

    # Test linear_fit

    def test_linear_fit_exact_line(self):
        slope, intercept, r2 = linear_fit([0, 1, 2, 3], [1, 3, 5, 7])
        self.assertAlmostEqual(slope, 2.0)
        self.assertAlmostEqual(intercept, 1.0)
        self.assertAlmostEqual(r2, 1.0)

    def test_linear_fit_r2_between_zero_and_one(self):
        _, _, r2 = linear_fit([1, 2, 3, 4, 5], [2, 1, 4, 3, 5])
        self.assertGreater(r2, 0)
        self.assertLess(r2, 1)

    def test_linear_fit_constant_y(self):
        slope, intercept, r2 = linear_fit([1, 2, 3], [5, 5, 5])
        self.assertEqual((slope, intercept), (0.0, 5.0))
        self.assertTrue(np.isnan(r2))

    def test_linear_fit_degenerate_is_nan(self):
        for x, y in ([], []), ([1], [2]), ([2, 2, 2], [1, 2, 3]):
            self.assertTrue(all(np.isnan(v) for v in linear_fit(x, y)))

    def test_linear_fit_invalid_inputs(self):
        with self.assertRaises(ValueError):
            linear_fit([1, 2, 3], [1, 2])
        with self.assertRaises(TypeError):
            linear_fit("abc", [1, 2, 3])

    # Test bootstrap_ci

    def test_bootstrap_ci_brackets_the_statistic(self):
        values = np.random.RandomState(0).normal(loc=10, size=50).tolist()
        low, high = bootstrap_ci(values, seed=0)
        self.assertLess(low, mean(values))
        self.assertGreater(high, mean(values))
        # a wider level gives a wider interval
        low99, high99 = bootstrap_ci(values, level=0.99, seed=0)
        self.assertLess(low99, low)
        self.assertGreater(high99, high)

    def test_bootstrap_ci_seed_is_deterministic(self):
        values = [1, 5, 2, 8, 3, 9, 4, 7]
        first = bootstrap_ci(values, seed=42)
        self.assertEqual(first, bootstrap_ci(values, seed=42))
        self.assertEqual(first, bootstrap_ci(values, seed=np.random.default_rng(42)))
        self.assertNotEqual(first, bootstrap_ci(values, seed=7))

    def test_bootstrap_ci_other_statistic(self):
        values = [1, 2, 3, 4, 100]
        low, high = bootstrap_ci(values, statistic=median, seed=0)
        self.assertLessEqual(low, median(values))
        self.assertGreaterEqual(high, median(values))
        self.assertLessEqual(high, 100)

    def test_bootstrap_ci_degenerate(self):
        self.assertTrue(all(np.isnan(v) for v in bootstrap_ci([], seed=0)))
        self.assertTrue(all(np.isnan(v) for v in bootstrap_ci([3], seed=0)))
        self.assertEqual(bootstrap_ci([5, 5, 5, 5], seed=0), (5.0, 5.0))

    def test_bootstrap_ci_invalid_inputs(self):
        with self.assertRaises(TypeError):
            bootstrap_ci("abc")
        with self.assertRaises(ValueError):
            bootstrap_ci([1, 2, 3], level=1.0)
        with self.assertRaises(ValueError):
            bootstrap_ci([1, 2, 3], n_resamples=0)

    # Test histogram

    def test_histogram_int_bins(self):
        counts, edges = histogram([1, 2, 2, 3, 3, 3, 4], bins=3)
        self.assertEqual(counts, [1, 2, 4])
        self.assertEqual(edges, [1.0, 2.0, 3.0, 4.0])
        self.assertIsInstance(counts, list)
        self.assertIsInstance(counts[0], int)

    def test_histogram_rules_and_edge_lists(self):
        values = np.random.RandomState(0).normal(size=200).tolist()
        for rule in ("auto", "fd", "rice", "sturges"):
            counts, edges = histogram(values, bins=rule)
            self.assertEqual(len(edges), len(counts) + 1)
            self.assertEqual(sum(counts), 200)
        counts, edges = histogram([1, 2, 3, 4], bins=[0, 2.5, 5])
        self.assertEqual(counts, [2, 2])
        self.assertEqual(edges, [0.0, 2.5, 5.0])

    def test_histogram_degenerate(self):
        self.assertEqual(histogram([]), ([], []))
        counts, edges = histogram([5, 5, 5])
        self.assertEqual(sum(counts), 3)
        self.assertEqual(len(edges), len(counts) + 1)

    def test_histogram_invalid_inputs(self):
        with self.assertRaises(ValueError):
            histogram([1, 2, 3], bins="no-such-rule")
        with self.assertRaises(TypeError):
            histogram("abc")

    # Test rolling_mean / ewma

    def test_rolling_mean_aligned_with_nan_head(self):
        result = rolling_mean([1, 2, 3, 4, 5], 3)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(np.isnan(v) for v in result[:2]))
        self.assertEqual(result[2:], [2.0, 3.0, 4.0])
        self.assertEqual(rolling_mean([1, 2, 3], 1), [1.0, 2.0, 3.0])

    def test_rolling_mean_degenerate(self):
        self.assertEqual(rolling_mean([], 3), [])
        self.assertTrue(all(np.isnan(v) for v in rolling_mean([1, 2], 3)))

    def test_rolling_mean_invalid_inputs(self):
        with self.assertRaises(ValueError):
            rolling_mean([1, 2, 3], 0)
        with self.assertRaises(TypeError):
            rolling_mean([1, 2, 3], 1.5)
        with self.assertRaises(TypeError):
            rolling_mean("abc", 2)

    def test_ewma_recursion(self):
        result = ewma([1, 2, 3], 0.5)
        self.assertEqual(result, [1.0, 1.5, 2.25])
        self.assertEqual(ewma([4, 5, 6], 1.0), [4.0, 5.0, 6.0])
        self.assertEqual(ewma([], 0.3), [])

    def test_ewma_invalid_inputs(self):
        for alpha in (0, 1.5, -0.1):
            with self.assertRaises(ValueError):
                ewma([1, 2, 3], alpha)
        with self.assertRaises(TypeError):
            ewma("abc", 0.5)

    # Test loess

    def test_loess_recovers_a_line_and_sorts_by_x(self):
        x = [5, 1, 3, 2, 4]
        y = [11, 3, 7, 5, 9]
        curve = loess(x, y, frac=0.6)
        self.assertEqual([p["x"] for p in curve], [1.0, 2.0, 3.0, 4.0, 5.0])
        np.testing.assert_allclose([p["y"] for p in curve], [3, 5, 7, 9, 11])

    def test_loess_large_magnitude_x(self):
        # epoch-second sized x must not collapse the local fit to a mean
        x = [1e9 + i for i in range(10)]
        y = [2 * xi + 1 for xi in x]
        curve = loess(x, y, frac=0.5)
        np.testing.assert_allclose([p["y"] for p in curve], y, rtol=1e-9)

    def test_loess_smooths_noise(self):
        rng = np.random.RandomState(0)
        x = np.linspace(0, 10, 60)
        noise = rng.normal(scale=0.3, size=60)
        y = np.sin(x) + noise
        curve = loess(x.tolist(), y.tolist())
        fitted = np.asarray([p["y"] for p in curve])
        self.assertLess(np.abs(fitted - np.sin(x)).mean(), np.abs(noise).mean())

    def test_loess_duplicate_x_and_degenerate(self):
        curve = loess([1, 1, 2, 2], [0, 2, 4, 6], frac=0.5)
        self.assertEqual([p["x"] for p in curve], [1.0, 1.0, 2.0, 2.0])
        self.assertTrue(all(np.isfinite(p["y"]) for p in curve))
        self.assertEqual(loess([], []), [])
        (point,) = loess([1], [2])
        self.assertEqual(point["x"], 1.0)
        self.assertTrue(np.isnan(point["y"]))

    def test_loess_invalid_inputs(self):
        with self.assertRaises(ValueError):
            loess([1, 2, 3], [1, 2])
        for frac in (0, 1.5):
            with self.assertRaises(ValueError):
                loess([1, 2, 3], [1, 2, 3], frac=frac)
        with self.assertRaises(TypeError):
            loess("abc", [1, 2, 3])

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

    def test_kde_limits_override_the_padded_range(self):
        curve = kde1d([1, 2, 3], gridsize=3, xlim=(0, 10))
        self.assertEqual([point["x"] for point in curve], [0.0, 5.0, 10.0])
        surface = kde2d([1, 2, 3], [1, 3, 2], gridsize=2, xlim=(0, 4), ylim=(-1, 5))
        self.assertEqual(surface["x"], [0.0, 4.0])
        self.assertEqual(surface["y"], [-1.0, 5.0])

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
