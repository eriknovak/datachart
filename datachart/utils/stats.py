"""The module containing the `stats` methods.

The `stats` module provides methods for calculating statistics.

Methods:
    count(values):
        Counts the number of elements in the list.
    sum_values(values):
        Calculates the sum of the values.
    mean(values):
        Calculates the mean of the values.
    median(values):
        Calculates the median of the values.
    stdev(values):
        Calculates the standard deviation of the values.
    variance(values):
        Calculates the variance of the values.
    quantile(values, q):
        Calculates the quantile of the values.
    iqr(values):
        Calculates the interquartile range (Q3 - Q1).
    minimum(values):
        Gets the minimum of the values.
    maximum(values):
        Gets the maximum of the values.
    correlation(x, y):
        Calculates the Pearson correlation coefficient between two lists.
    spearman(x, y):
        Calculates the Spearman rank correlation between two lists.
    mode(values):
        Gets the most frequent value.
    skewness(values):
        Calculates the skewness of the values.
    kurtosis(values):
        Calculates the excess kurtosis of the values.
    linear_fit(x, y):
        Fits a straight line to the (x, y) points.
    bootstrap_ci(values, statistic, level, n_resamples, seed):
        Estimates a confidence interval of a statistic by bootstrapping.
    histogram(values, bins):
        Bins the values into histogram counts and edges.
    rolling_mean(values, window):
        Smooths the values with a trailing moving average.
    ewma(values, alpha):
        Smooths the values with an exponentially weighted moving average.
    loess(x, y, frac):
        Smooths the (x, y) points with a locally weighted linear fit.
    kde1d(values, bandwidth, gridsize, cut):
        Estimates the density of the values as a curve.
    kde2d(x, y, bandwidth, gridsize, cut):
        Estimates the density of the (x, y) points as a gridded surface.
"""

from numbers import Real
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
from matplotlib.mlab import GaussianKDE

from ..constants import BANDWIDTH
from ._internal.validate import validate_bandwidth

# ================================================
# Statistical values
# ================================================


def count(values: List[Union[int, float]]) -> int:
    """Counts the number of elements in a list.

    Examples:
        >>> from datachart.utils.stats import count
        >>> count([1, 2, 3, 4, 5])
        5

    Args:
        values: The list of values.

    Returns:
        The number of elements in the list.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    return len(values)


def sum_values(values: List[Union[int, float]]) -> float:
    """Calculates the sum of all values.

    !!! info "Added in v0.7.0"

    Examples:
        >>> from datachart.utils.stats import sum_values
        >>> sum_values([1, 2, 3, 4, 5])
        15.0

    Args:
        values: The list of values.

    Returns:
        The sum of all values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    return float(np.sum(values))


def mean(values: List[Union[int, float]]) -> float:
    """Calculates the mean of the values.

    Examples:
        >>> from datachart.utils.stats import mean
        >>> mean([1, 2, 3, 4, 5])
        3.0

    Args:
        values: The list of values.

    Returns:
        The mean of the values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.mean(values))


def median(values: List[Union[int, float]]) -> float:
    """Calculates the median of the values.

    Examples:
        >>> from datachart.utils.stats import median
        >>> median([1, 2, 3, 4, 5])
        3.0

    Args:
        values: The list of values.

    Returns:
        The median of the values.
    """

    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.median(values))


def stdev(values: List[Union[int, float]]) -> float:
    """Calculates the standard deviation of the values.

    Examples:
        >>> from datachart.utils.stats import stdev
        >>> stdev([1, 2, 3, 4, 5])
        1.4142135623730951

    Args:
        values: The list of values.

    Returns:
        The standard deviation of the values.
    """

    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.std(values))


def variance(values: List[Union[int, float]]) -> float:
    """Calculates the variance of the values.

    !!! info "Added in v0.7.0"

    Examples:
        >>> from datachart.utils.stats import variance
        >>> variance([1, 2, 3, 4, 5])
        2.0

    Args:
        values: The list of values.

    Returns:
        The variance of the values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.var(values))


def quantile(values: List[Union[int, float]], q: float) -> float:
    """Calculates the quantile of the values.

    Examples:
        >>> from datachart.utils.stats import quantile
        >>> quantile([1, 2, 3, 4, 5], 25)
        2.0

    Args:
        values: The list of values.
        q: The quantile to calculate (0-100).

    Returns:
        The quantile of the values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.percentile(values, q))


def iqr(values: List[Union[int, float]]) -> float:
    """Calculates the interquartile range (Q3 - Q1).

    !!! info "Added in v0.7.0"

    The interquartile range is the difference between the 75th percentile
    (Q3) and the 25th percentile (Q1). It is a measure of statistical
    dispersion and is useful for identifying outliers.

    Examples:
        >>> from datachart.utils.stats import iqr
        >>> iqr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        4.5

    Args:
        values: The list of values.

    Returns:
        The interquartile range of the values.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return float(np.percentile(values, 75) - np.percentile(values, 25))


def _as_float(value: Any) -> Any:
    """A float for a numeric scalar; anything else (e.g. a datetime) as is."""

    return float(value) if isinstance(value, (Real, np.number)) else value


def minimum(values: List[Any]) -> Any:
    """Gets the minimum of the values.

    Numeric values return a float; any other ordered values, such as
    datetimes, return their minimum unchanged.

    !!! info "Added in Unreleased"

        Non-numeric values pass through instead of raising.

    Examples:
        >>> from datachart.utils.stats import minimum
        >>> minimum([1, 2, 3, 4, 5])
        1

    Args:
        values: The list of values.

    Returns:
        The minimum of the values: a float for numbers, else the value itself.

    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return _as_float(np.min(values))


def maximum(values: List[Any]) -> Any:
    """Gets the maximum of the values.

    Numeric values return a float; any other ordered values, such as
    datetimes, return their maximum unchanged.

    !!! info "Added in Unreleased"

        Non-numeric values pass through instead of raising.

    Examples:
        >>> from datachart.utils.stats import maximum
        >>> maximum([1, 2, 3, 4, 5])
        5

    Args:
        values: The list of values.

    Returns:
        The maximum of the values: a float for numbers, else the value itself.

    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    return _as_float(np.max(values))


def correlation(x: List[Union[int, float]], y: List[Union[int, float]]) -> float:
    """Calculates the Pearson correlation coefficient between two lists.

    !!! info "Added in v0.7.0"

    The Pearson correlation coefficient measures the linear relationship
    between two datasets. It ranges from -1 (perfect negative correlation)
    to 1 (perfect positive correlation), with 0 indicating no linear
    correlation.

    Examples:
        >>> from datachart.utils.stats import correlation
        >>> correlation([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
        1.0
        >>> correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
        -1.0

    Args:
        x: The first list of values.
        y: The second list of values.

    Returns:
        The Pearson correlation coefficient.

    Raises:
        TypeError: If x or y is not a list or numpy array.
        ValueError: If x and y have different lengths.
    """
    if not isinstance(x, (list, np.ndarray)):
        raise TypeError("The x variable must be a list or numpy array.")
    if not isinstance(y, (list, np.ndarray)):
        raise TypeError("The y variable must be a list or numpy array.")
    if len(x) == 0 or len(y) == 0:
        raise ValueError("x and y must have at least one value.")
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")
    return float(np.corrcoef(x, y)[0, 1])


def _paired(x: Any, y: Any) -> Tuple[np.ndarray, np.ndarray]:
    """The (x, y) inputs as float arrays, checked for type and equal length."""

    if not isinstance(x, (list, np.ndarray)):
        raise TypeError("The x variable must be a list or numpy array.")
    if not isinstance(y, (list, np.ndarray)):
        raise TypeError("The y variable must be a list or numpy array.")
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")
    return np.asarray(x, dtype=float), np.asarray(y, dtype=float)


def spearman(x: List[Union[int, float]], y: List[Union[int, float]]) -> float:
    """Calculates the Spearman rank correlation between two lists.

    The Spearman coefficient is the Pearson correlation of the ranks, so it
    measures any monotone relationship, not only a linear one, and is robust
    to outliers. It ranges from -1 to 1 like `correlation`.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import spearman
        >>> round(spearman([1, 2, 3, 4, 5], [1, 4, 9, 16, 25]), 6)
        1.0
        >>> round(spearman([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), 6)
        -1.0

    Args:
        x: The first list of values.
        y: The second list of values.

    Returns:
        The Spearman rank correlation; `nan` for fewer than two points or a
        constant list.

    Raises:
        TypeError: If x or y is not a list or numpy array.
        ValueError: If x and y have different lengths.
    """
    xs, ys = _paired(x, y)
    if len(xs) < 2 or np.ptp(xs) == 0 or np.ptp(ys) == 0:
        return np.nan
    from scipy import stats as scipy_stats

    return float(scipy_stats.spearmanr(xs, ys).statistic)


def mode(values: List[Union[int, float]]) -> float:
    """Gets the most frequent value.

    Meant for discrete data, where values repeat; on continuous data every
    value tends to be unique and the mode is just the smallest one. Ties are
    broken by taking the smallest of the most frequent values.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import mode
        >>> mode([3, 1, 2, 3, 1])
        1.0

    Args:
        values: The list of values.

    Returns:
        The smallest most frequent value; `nan` for an empty list.

    Raises:
        TypeError: If values is not a list or numpy array.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return np.nan
    from scipy import stats as scipy_stats

    return float(scipy_stats.mode(np.asarray(values), keepdims=False).mode)


def _shape(name: str, values: Any) -> float:
    """The scipy shape statistic `name` of the values; nan when it is undefined."""

    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) < 2 or np.ptp(values) == 0:
        return np.nan
    from scipy import stats as scipy_stats

    return float(getattr(scipy_stats, name)(np.asarray(values, dtype=float)))


def skewness(values: List[Union[int, float]]) -> float:
    """Calculates the skewness of the values.

    Skewness measures the asymmetry of the distribution: positive when the
    tail extends to the right of the bulk, negative when it extends to the
    left, and zero for a symmetric distribution.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import skewness
        >>> skewness([1, 2, 3, 4, 5])
        0.0
        >>> round(skewness([1, 1, 1, 2, 10]), 3)
        1.457

    Args:
        values: The list of values.

    Returns:
        The skewness of the values; `nan` for fewer than two values or a
        constant list.

    Raises:
        TypeError: If values is not a list or numpy array.
    """
    return _shape("skew", values)


def kurtosis(values: List[Union[int, float]]) -> float:
    """Calculates the excess kurtosis of the values.

    Kurtosis measures how heavy the tails of the distribution are compared
    to a normal distribution, which scores zero: positive for heavier tails
    and sharper peaks, negative for lighter tails and flatter shapes.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import kurtosis
        >>> kurtosis([1, 2, 3, 4, 5])
        -1.3

    Args:
        values: The list of values.

    Returns:
        The excess kurtosis of the values; `nan` for fewer than two values or
        a constant list.

    Raises:
        TypeError: If values is not a list or numpy array.
    """
    return _shape("kurtosis", values)


def linear_fit(
    x: List[Union[int, float]], y: List[Union[int, float]]
) -> Tuple[float, float, float]:
    """Fits a straight line to the (x, y) points.

    An ordinary least-squares fit of `y = slope * x + intercept`, with the
    coefficient of determination `r2` saying how much of the variation in
    `y` the line explains (1 is a perfect fit).

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import linear_fit
        >>> slope, intercept, r2 = linear_fit([0, 1, 2, 3], [1, 3, 5, 7])
        >>> round(slope, 6), round(intercept, 6), round(r2, 6)
        (2.0, 1.0, 1.0)

    Args:
        x: The x values of the points.
        y: The y values of the points, one per x value.

    Returns:
        The `(slope, intercept, r2)` of the fitted line; all `nan` for fewer
        than two points or a constant `x`, and `r2` alone `nan` for a
        constant `y`, which leaves no variation to explain.

    Raises:
        TypeError: If x or y is not a list or numpy array.
        ValueError: If x and y have different lengths.
    """
    xs, ys = _paired(x, y)
    if len(xs) < 2 or np.ptp(xs) == 0:
        return (np.nan, np.nan, np.nan)
    from scipy import stats as scipy_stats

    fit = scipy_stats.linregress(xs, ys)
    # constant y: r is 0 or nan depending on the scipy version, so decide here
    r2 = np.nan if np.ptp(ys) == 0 else float(fit.rvalue**2)
    return (float(fit.slope), float(fit.intercept), r2)


def bootstrap_ci(
    values: List[Union[int, float]],
    statistic: Callable[[List[Union[int, float]]], float] = mean,
    level: float = 0.95,
    n_resamples: int = 1000,
    seed: Optional[Union[int, np.random.Generator]] = None,
) -> Tuple[float, float]:
    """Estimates a confidence interval of a statistic by bootstrapping.

    The values are resampled with replacement `n_resamples` times, the
    statistic is computed on each resample, and the interval is the central
    `level` share of those results (the percentile bootstrap). The half-width
    of the interval is a ready-made error bar for a `BarChart`.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import bootstrap_ci, median
        >>> low, high = bootstrap_ci([1, 2, 3, 4, 5, 6, 7, 8], seed=0)
        >>> low < 4.5 < high
        True
        >>> bootstrap_ci([1, 2, 3, 4, 100], statistic=median, seed=0)[1] <= 100
        True

    Args:
        values: The list of values.
        statistic: The function of the values to estimate, `mean` by default.
        level: The confidence level, strictly between 0 and 1.
        n_resamples: The number of resamples to draw.
        seed: An integer or `numpy.random.Generator` that makes the resamples
            reproducible.

    Returns:
        The `(low, high)` bounds of the interval; both `nan` for fewer than
        two values.

    Raises:
        TypeError: If values is not a list or numpy array.
        ValueError: If level is not between 0 and 1 or n_resamples is not
            positive.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if not 0 < level < 1:
        raise ValueError("The `level` must be strictly between 0 and 1.")
    if n_resamples < 1:
        raise ValueError("The `n_resamples` must be a positive integer.")
    if len(values) < 2:
        return (np.nan, np.nan)
    from scipy import stats as scipy_stats

    result = scipy_stats.bootstrap(
        (np.asarray(values, dtype=float),),
        statistic,
        vectorized=False,
        confidence_level=level,
        n_resamples=n_resamples,
        method="percentile",
        rng=np.random.default_rng(seed),
    )
    return (
        float(result.confidence_interval.low),
        float(result.confidence_interval.high),
    )


# ================================================
# Binning
# ================================================


def histogram(
    values: List[Union[int, float]],
    bins: Union[str, int, List[Union[int, float]]] = "auto",
) -> Tuple[List[int], List[float]]:
    """Bins the values into histogram counts and edges.

    The `bins` are passed straight to `numpy.histogram_bin_edges`: a rule
    name such as `"auto"`, `"fd"`, `"rice"`, or `"sturges"` picks the edges
    from the data, an integer sets the number of equal-width bins, and a list
    gives the edges explicitly. These rules are unrelated to the
    `CONTOUR_LEVELS` rules that share their names.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import histogram
        >>> histogram([1, 2, 2, 3, 3, 3, 4], bins=3)
        ([1, 2, 4], [1.0, 2.0, 3.0, 4.0])

    Args:
        values: The list of values.
        bins: A bin rule name, a number of bins, or a list of bin edges.

    Returns:
        The `(counts, edges)` lists, with one more edge than counts; both
        empty for an empty list.

    Raises:
        TypeError: If values is not a list or numpy array.
        ValueError: If the bin rule is unknown.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if len(values) == 0:
        return ([], [])
    edges = np.histogram_bin_edges(values, bins=bins)
    counts, _ = np.histogram(values, bins=edges)
    return (counts.tolist(), edges.tolist())


# ================================================
# Smoothers
# ================================================


def rolling_mean(values: List[Union[int, float]], window: int) -> List[float]:
    """Smooths the values with a trailing moving average.

    Each output is the mean of the `window` values ending at that index, so
    the result lines up with the input and is `nan` until the window fills.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import rolling_mean
        >>> rolling_mean([1, 2, 3, 4, 5], 3)
        [nan, nan, 2.0, 3.0, 4.0]

    Args:
        values: The list of values.
        window: The number of values averaged, at least 1.

    Returns:
        The smoothed values, one per input value.

    Raises:
        TypeError: If values is not a list or numpy array, or the window is
            not an integer.
        ValueError: If the window is not positive.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if not isinstance(window, (int, np.integer)):
        raise TypeError("The `window` must be an integer.")
    if window < 1:
        raise ValueError("The `window` must be a positive integer.")
    series = np.asarray(values, dtype=float)
    result = np.full(len(series), np.nan)
    if len(series) >= window:
        result[window - 1 :] = np.convolve(series, np.ones(window), "valid") / window
    return result.tolist()


def ewma(values: List[Union[int, float]], alpha: float) -> List[float]:
    """Smooths the values with an exponentially weighted moving average.

    Each output blends the current value with the previous output,
    `alpha * value + (1 - alpha) * previous`, starting from the first value.
    A larger `alpha` follows the data more closely; a smaller one smooths
    harder.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import ewma
        >>> ewma([1, 2, 3], 0.5)
        [1.0, 1.5, 2.25]

    Args:
        values: The list of values.
        alpha: The weight of the current value, in `(0, 1]`.

    Returns:
        The smoothed values, one per input value.

    Raises:
        TypeError: If values is not a list or numpy array.
        ValueError: If alpha is not in `(0, 1]`.
    """
    if not isinstance(values, (list, np.ndarray)):
        raise TypeError("The values variable must be a list or numpy array.")
    if not 0 < alpha <= 1:
        raise ValueError("The `alpha` must be in the interval (0, 1].")
    result: List[float] = []
    for value in np.asarray(values, dtype=float):
        previous = result[-1] if result else value
        result.append(float(alpha * value + (1 - alpha) * previous))
    return result


def loess(
    x: List[Union[int, float]], y: List[Union[int, float]], frac: float = 0.3
) -> List[Dict[str, float]]:
    """Smooths the (x, y) points with a locally weighted linear fit.

    At each `x` a straight line is fitted to the nearest `frac` share of the
    points, weighted by a tricube kernel so closer points count more, and the
    smoothed `y` is that line's value there (LOESS/LOWESS). The result is a
    list of `{x, y}` points sorted by `x`, ready for `LineChart`, as `kde1d`
    returns. A smaller `frac` follows the data more closely.

    !!! info "Added in Unreleased"

    Examples:
        >>> from datachart.utils.stats import loess
        >>> curve = loess([5, 1, 3, 2, 4], [11, 3, 7, 5, 9], frac=0.6)
        >>> [(point["x"], round(point["y"], 6)) for point in curve]
        [(1.0, 3.0), (2.0, 5.0), (3.0, 7.0), (4.0, 9.0), (5.0, 11.0)]

    Args:
        x: The x values of the points.
        y: The y values of the points, one per x value.
        frac: The share of the points each local fit uses, in `(0, 1]`.

    Returns:
        The `{x, y}` points of the smoothed curve, sorted by `x`; the `y` is
        `nan` for fewer than two points.

    Raises:
        TypeError: If x or y is not a list or numpy array.
        ValueError: If x and y have different lengths or frac is not in
            `(0, 1]`.
    """
    xs, ys = _paired(x, y)
    if not 0 < frac <= 1:
        raise ValueError("The `frac` must be in the interval (0, 1].")
    order = np.argsort(xs, kind="stable")
    xs, ys = xs[order], ys[order]
    n = len(xs)
    if n < 2:
        return [{"x": float(xi), "y": np.nan} for xi in xs]
    k = max(2, int(np.ceil(frac * n)))
    smoothed = []
    for xi in xs:
        # centre x on the fit point so the normal equations stay well scaled
        dx = xs - xi
        distance = np.abs(dx)
        span = np.sort(distance)[k - 1]
        if span > 0:
            weight = np.clip(1 - (distance / span) ** 3, 0, None) ** 3
        else:
            # duplicate x collapse the span: average the points sitting on it
            weight = (distance == 0).astype(float)
        sw, sx, sy = weight.sum(), (weight * dx).sum(), (weight * ys).sum()
        sxx, sxy = (weight * dx * dx).sum(), (weight * dx * ys).sum()
        denominator = sw * sxx - sx * sx
        # a singular fit (all weighted x equal) falls back to the local mean
        if denominator <= 1e-12 * sw * sxx:
            smoothed.append(sy / sw)
            continue
        slope = (sw * sxy - sx * sy) / denominator
        smoothed.append((sy - slope * sx) / sw)
    return [{"x": float(xi), "y": float(yi)} for xi, yi in zip(xs, smoothed)]


# ================================================
# Kernel density estimates
# ================================================


def _kde(points: np.ndarray, bandwidth, cut: float) -> Tuple[GaussianKDE, np.ndarray]:
    """The kernel over the (n_dims, n_points) array and its per-axis padding."""

    validate_bandwidth(bandwidth)
    if points.shape[1] < 2:
        raise ValueError("A density estimate needs at least two points.")
    if not np.isfinite(points).all():
        raise ValueError("The values must be finite numbers.")
    if cut < 0:
        raise ValueError("The `cut` must be a non-negative number.")
    kde = GaussianKDE(points, bandwidth)
    # pad each axis by `cut` kernel widths (about `factor * std`)
    padding = cut * kde.covariance_factor() * points.std(axis=1, ddof=1)
    return kde, padding


def kde1d(
    values: List[Union[int, float]],
    *,
    bandwidth: Optional[Union[BANDWIDTH, str, float]] = None,
    gridsize: int = 100,
    cut: float = 3,
    xlim: Optional[Tuple[float, float]] = None,
) -> List[Dict[str, float]]:
    """Estimates the density of the values as a curve.

    A Gaussian kernel density estimate evaluated on `gridsize` evenly spaced
    points over the range of the values, extended by `cut` bandwidths on each
    side so the curve tails off instead of being clipped at the extremes, or
    over an explicit `xlim` so several curves share one grid. The
    result is a list of `{x, y}` points ready for `LineChart`; the curve
    integrates to 1, so it overlays a density `Histogram` of the same values.

    !!! info "Added in 0.9.0"

    Examples:
        >>> from datachart.utils.stats import kde1d
        >>> curve = kde1d([1, 2, 2, 3, 3, 3, 4, 4, 5], gridsize=5, cut=0)
        >>> [round(point["x"], 2) for point in curve]
        [1.0, 2.0, 3.0, 4.0, 5.0]
        >>> round(sum(point["y"] for point in curve), 2)
        0.94

    Args:
        values: The values to estimate the density of.
        bandwidth: The kernel bandwidth: None or "scott" (Scott's rule),
            "silverman", or a scalar factor. See `BANDWIDTH`.
        gridsize: The number of points the curve is evaluated on.
        cut: How many bandwidths to extend the grid past the extremes.
        xlim: The `(min, max)` range of the grid; overrides the padded range.

    Returns:
        The `{x, y}` points of the density curve.

    Raises:
        ValueError: If the bandwidth is invalid, there are fewer than two
            values, or a value is not finite.
    """
    points = np.asarray(values, dtype=float).reshape(1, -1)
    kde, (padding,) = _kde(points, bandwidth, cut)
    lo, hi = xlim or (points.min() - padding, points.max() + padding)
    grid = np.linspace(lo, hi, gridsize)
    density = kde.evaluate(grid)
    return [{"x": float(x), "y": float(y)} for x, y in zip(grid, density)]


def kde2d(
    x: List[Union[int, float]],
    y: List[Union[int, float]],
    *,
    bandwidth: Optional[Union[BANDWIDTH, str, float]] = None,
    gridsize: Union[int, Tuple[int, int]] = 100,
    cut: float = 3,
    xlim: Optional[Tuple[float, float]] = None,
    ylim: Optional[Tuple[float, float]] = None,
) -> Dict[str, List]:
    """Estimates the density of the (x, y) points as a gridded surface.

    A Gaussian kernel density estimate evaluated on a `gridsize` × `gridsize`
    grid over the range of the points, extended by `cut` bandwidths on each
    side so the outer contours close instead of being clipped, or over explicit
    `xlim`/`ylim` so several surfaces share one grid. The result is
    an `{x, y, z}` chart dict ready for `ContourChart` — the density chart of
    a scattered dataset is `ContourChart(kde2d(x, y))`.

    !!! info "Added in 0.9.0"

    Examples:
        >>> from datachart.utils.stats import kde2d
        >>> surface = kde2d([1, 2, 3, 4], [1, 3, 2, 4], gridsize=(3, 2), cut=0)
        >>> surface["x"], surface["y"]
        ([1.0, 2.5, 4.0], [1.0, 4.0])
        >>> [[round(z, 3) for z in row] for row in surface["z"]]
        [[0.075, 0.038, 0.001], [0.001, 0.038, 0.075]]

    Args:
        x: The x values of the points.
        y: The y values of the points, one per x value.
        bandwidth: The kernel bandwidth: None or "scott" (Scott's rule),
            "silverman", or a scalar factor. See `BANDWIDTH`.
        gridsize: The number of grid columns and rows, as one number or an
            `(x, y)` pair.
        cut: How many bandwidths to extend the grid past the extremes.
        xlim: The `(min, max)` x range of the grid; overrides the padded range.
        ylim: The `(min, max)` y range of the grid; overrides the padded range.

    Returns:
        The `{x, y, z}` chart dict of the density surface.

    Raises:
        ValueError: If the bandwidth is invalid, x and y differ in length,
            there are fewer than two points, or a value is not finite.
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")
    points = np.asarray([x, y], dtype=float)
    kde, (pad_x, pad_y) = _kde(points, bandwidth, cut)
    n_cols, n_rows = (gridsize, gridsize) if isinstance(gridsize, int) else gridsize
    x_lo, x_hi = xlim or (points[0].min() - pad_x, points[0].max() + pad_x)
    y_lo, y_hi = ylim or (points[1].min() - pad_y, points[1].max() + pad_y)
    grid_x = np.linspace(x_lo, x_hi, n_cols)
    grid_y = np.linspace(y_lo, y_hi, n_rows)
    mesh_x, mesh_y = np.meshgrid(grid_x, grid_y)
    density = kde.evaluate(np.vstack([mesh_x.ravel(), mesh_y.ravel()]))
    return {
        "x": grid_x.tolist(),
        "y": grid_y.tolist(),
        "z": density.reshape(mesh_x.shape).tolist(),
    }
