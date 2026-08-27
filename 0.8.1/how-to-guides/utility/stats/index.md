# Statistics

This section showcases the utility functions found in the [datachart.utils.stats](https://eriknovak.github.io/datachart/0.8.1/references/utils/stats) module.

Let us start by importing the supporting libraries:

```
import random
```

## Statistics Submodule

The [dataset.utils.stats](https://eriknovak.github.io/datachart/0.8.1/references/utils/stats) submodule contains functions for calculating statistics. To showcase its use, let us create a list of random numbers:

```
random_values = random.sample(range(1, 100), 10)
random_values
```

Let us now showcase the functions in the `stats` module.

### Count

The `count` function returns the number of elements in the list.

```
from datachart.utils.stats import count
```

```
count(random_values)
```

### Sum

The `sum_values` function returns the sum of all values in the list.

```
from datachart.utils.stats import sum_values
```

```
sum_values(random_values)
```

### Mean

The `mean` function returns the mean of the values.

```
from datachart.utils.stats import mean
```

```
mean(random_values)
```

### Median

The `median` function returns the median of the values.

```
from datachart.utils.stats import median
```

```
median(random_values)
```

### Standard Deviation

The `stdev` function returns the standard deviation of the values.

```
from datachart.utils.stats import stdev
```

```
stdev(random_values)
```

### Variance

The `variance` function returns the variance of the values. Variance is the square of the standard deviation.

```
from datachart.utils.stats import variance
```

```
variance(random_values)
```

### Quantile

The `quantile` function returns the quantile of the values.

```
from datachart.utils.stats import quantile
```

Show the 25th quantile:

```
quantile(random_values, 25)
```

Show the 75th quantile:

```
quantile(random_values, 75)
```

### Interquartile Range (IQR)

The `iqr` function returns the interquartile range, which is the difference between the 75th percentile (Q3) and 25th percentile (Q1). It is useful for identifying outliers and understanding the spread of the middle 50% of the data.

```
from datachart.utils.stats import iqr
```

```
iqr(random_values)
```

### Minimum

The `minimum` function returns the minimum of the values.

```
from datachart.utils.stats import minimum
```

```
minimum(random_values)
```

### Maximum

The `maximum` function returns the maximum of the values.

```
from datachart.utils.stats import maximum
```

```
maximum(random_values)
```

### Correlation

The `correlation` function calculates the Pearson correlation coefficient between two lists of values. It measures the linear relationship between the datasets, ranging from -1 (perfect negative correlation) to 1 (perfect positive correlation).

```
from datachart.utils.stats import correlation
```

Create a second list of random values to compare:

```
random_values_2 = random.sample(range(1, 100), 10)
random_values_2
```

```
correlation(random_values, random_values_2)
```

Under development

This theme is still under development. If you are interested in improving it, please let us know.
