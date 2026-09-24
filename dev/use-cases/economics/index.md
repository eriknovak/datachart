# Economics and Finance

An economic report asks the same questions in the same order: how the big economies grew and when they shrank, which are the largest and how the order changed, how an economy's structure changes as it grows, where and when inflation bit, what the last shock cost, who caught up on income, and how the economies compare on every front at once. This page walks the world's major economies through those questions and names the figure that answers each, so the chart to reach for arrives with the question rather than the other way round. Every figure links to the chart guide that covers it in full.

Every number is real: the GDP growth of the United States, the euro area, China, Japan and the world since 1980, the nominal GDP of every country in six benchmark years, the sector shares of China, India and South Korea since 1960, and the inflation, growth, unemployment, trade, investment and income of the nineteen G20 countries, all from the World Bank's [World Development Indicators](https://datacatalog.worldbank.org/search/dataset/0037712) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). Swap the countries and the same cells draw it.

```
from datachart.charts import (
    BarChart,
    BumpChart,
    DumbbellChart,
    Heatmap,
    LineChart,
    ParallelCoords,
    StackedAreaChart,
)
from datachart.constants import (
    DUMBBELL_SORT_KEY,
    EMPHASIS,
    FIG_SIZE,
    LEGEND_LOCATION,
    NORMALIZE,
    ORIENTATION,
    SHOW_GRID,
    SORT,
    VALUE_FORMAT,
)
from datachart.utils import Grid
```

The hidden cell below holds the numbers. `GROWTH` is the yearly GDP growth of five economies over the `GROWTH_YEARS`; `GDP_RANK` is the nominal GDP, in trillions of current dollars, of every country that was among the ten largest in any of six benchmark years; `SECTORS` is the share of agriculture, industry and services in the GDP of three economies since 1960; `INFLATION` is the yearly consumer-price inflation of the G20 countries since 2015, `PANDEMIC` their growth in 2020, `INCOME` their GDP per capita in 2000 and 2023, and `G20_2023` six indicators of each in 2023 with its World Bank income group. The sections that follow only reshape those into the records the charts take.

## Growth

### How did the big economies grow, and when did they shrink?

The first figure of an economic report is growth over time, one line per economy, and the years that matter are the ones below zero. A [line chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md) draws the five series over the same years, an `hlines` mark at zero is the line a contraction crosses, and the two global recessions are `vspans`, shaded bands with a `label` that enters the legend, so the reader sees at once which lines dipped into them and which did not. The world line takes the `"highlight"` role through `emphasis`, drawn bold in front of the others, because it is the one the rest are read against.

```
ECONOMIES = list(GROWTH)
RECESSIONS = [
    {"xmin": 2008.5, "xmax": 2009.5, "label": "Financial crisis"},
    {"xmin": 2019.5, "xmax": 2020.5, "label": "Pandemic"},
]
ZERO_LINE = {"plot_hline_color": "#666666", "plot_hline_width": 1}

growth_figure = LineChart(
    [
        [{"x": year, "y": value} for year, value in zip(GROWTH_YEARS, GROWTH[economy])]
        for economy in ECONOMIES
    ],
    title="China never contracted; the others did in both global recessions",
    xlabel="Year",
    ylabel="GDP growth (%)",
    subtitle=ECONOMIES,
    # the world line bold and in front, the rest at normal weight
    emphasis=[None if economy != "World" else EMPHASIS.HIGHLIGHT for economy in ECONOMIES],
    hlines={"y": 0, "style": ZERO_LINE},
    vspans=RECESSIONS,
    show_legend=True,
    legend={"location": LEGEND_LOCATION.OUTSIDE_TOP, "ncols": 4},
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
growth_figure.show()
```

The world line runs between 2 and 5% for four decades and dips below zero only twice, in 2009 at -1.3% and in 2020 at -2.9%, which is what the two bands mark. Inside the bands the lines separate: the euro area and Japan fell furthest both times, the United States less, and China's line never crosses zero at all; its worst year was 2020 at 2.3%. Outside the bands, China's line sits far above the others through the 1990s and 2000s and has drifted down towards them since, which is the growth the next figure turns into rank.

### Which economies are the largest, and how has the order changed?

The size of an economy is a ranking: a report says "the second-largest economy", not its dollar figure. A [bump chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/bumpchart/index.md) draws rankings over time: one line per country, its vertical position each benchmark year is its rank by nominal GDP, and a line that climbs is a country overtaking the others. The chart ranks the raw values itself, so the records carry GDP in trillions and `subtitle` names the lines at their ends. Fourteen lines crossing is a tangle, and `emphasis` cuts it: the two lines the section is about take the `"highlight"` role and the rest the `"background"` role, drawn thin and grey, so the two bold lines carry the story and the others are the context they climb through. A series starts when the country's data does, so Russia's line begins in 1990.

```
COUNTRIES = list(GDP_RANK)

rank_figure = BumpChart(
    [[{"x": year, "y": gdp} for year, gdp in GDP_RANK[country]] for country in COUNTRIES],
    title="China climbed from outside the top ten to second; India entered at fifth",
    xlabel="Year",
    ylabel="Rank by nominal GDP",
    subtitle=COUNTRIES,
    # the two climbers bold, everyone else as grey context
    emphasis=[
        EMPHASIS.HIGHLIGHT if country in ("China", "India") else EMPHASIS.BACKGROUND
        for country in COUNTRIES
    ],
    xticks=[year for year, _ in GDP_RANK["United States"]],
    figsize=(8.0, 5.5),
)
rank_figure.show()
```

The United States holds first place in every year, and Japan holds second for three decades before China passes it in 2010 and Germany in 2023. China's line carries the figure: 12th in 1980, 11th in 1990, 6th in 2000, and second since 2010. India's line enters the top ten in 2010 and reaches fifth in 2023. The other lines drift down a place or two as the two Asian economies pass them.

### How does an economy change as it grows?

Every economy that grows rich goes through the same structural change: agriculture shrinks, industry rises and then yields to services. Three economies at different stages of it show the whole path. The three sector shares add up to nearly the whole of GDP (the remainder is net taxes), so each economy is a [stacked area chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/stackedareachart/index.md) with the bands stacked to the whole. Three charts built with the same `ymax` sit side by side in a [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md), which takes the figures already built and redraws them into its cells, so the reader compares the boundaries across the three at the same scale.

```
SECTOR_NAMES = ["Agriculture", "Industry", "Services"]


def structure(economy):
    years = sorted(SECTORS[economy])
    return StackedAreaChart(
        [
            [{"x": year, "y": SECTORS[economy][year][index]} for year in years]
            for index in range(len(SECTOR_NAMES))
        ],
        title=economy,
        subtitle=SECTOR_NAMES,
        ymax=100,
        # one legend for the row, below the middle chart
        show_legend=economy == "India",
        legend={"location": LEGEND_LOCATION.OUTSIDE_BOTTOM, "ncols": 3},
    )


Grid(
    [structure(economy) for economy in SECTORS],
    title="Agriculture gives way to industry, and industry to services (% of GDP)",
    xlabel="Year",
    ylabel="Share of GDP (%)",
    figsize=(11.0, 3.8),
).show()
```

South Korea is the finished path: agriculture was 36% of GDP in 1960 and is 1% now, industry rose through the 1970s and 1980s and has held near a third since, and services took the rest. China is the same path forty years behind, with industry still near 37% and services passing it only around 2012. India skipped a step: its agriculture band shrank the same way, but industry never rose past a third and services took the share directly.

## Prices, incomes and the shocks

### Where and when did inflation bite?

Nineteen countries over nine years of inflation is a table a reader cannot scan for the hot years; a [heatmap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/heatmap/index.md) colours each cell by its value, so a hot year is a dark column and a chronically inflationary country is a dark row. Two members run inflation in the tens and hundreds of percent, which would leave every other cell the same pale shade on a linear scale, so `norm=NORMALIZE.SYMLOG` gives the colour scale a logarithmic reach that keeps the contrast among the single digits, and `show_values` prints the numbers so the extreme cells are read rather than guessed.

```
MEMBERS = sorted(INFLATION, key=lambda country: -INFLATION[country][INFLATION_YEARS.index(2022)])

inflation_figure = Heatmap(
    {"x": INFLATION_YEARS, "y": MEMBERS, "z": [INFLATION[country] for country in MEMBERS]},
    title="2022 was the hot year everywhere; Argentina and Türkiye are hot every year",
    xlabel="Year",
    ylabel="Country, by 2022 inflation",
    norm=NORMALIZE.SYMLOG,
    show_values=True,
    value_format="{x:.1f}",
    show_colorbars=True,
    colorbar={"label": "Inflation (%)"},
    figsize=(8.0, 6.5),
)
inflation_figure.show()
```

The 2022 column is the darkest for almost every row: the post-pandemic surge took Germany to 7% and Italy to 8%, the United Kingdom to 8% and the United States to 8%, and 2023 is already paler. Two rows are dark in every column, Argentina and Türkiye, where inflation is a condition rather than an episode, and two are pale in every column, China and Japan, which never saw the surge. Saudi Arabia is pale throughout too, with a pegged currency and subsidised prices. The heatmap separates the episode from the condition.

### How much did the pandemic year cost?

One year, nineteen economies, one number each: the growth of 2020 is a [bar chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/barchart/index.md), sorted so the reader sees the order without reading the labels, with a `vlines` mark at zero as the line the bars are measured from. The bars run sideways, with `orientation`, so the country names read as a list and the value axis is horizontal, `show_values` prints each figure at the bar's end, and each record's own `emphasis` gives the economies that grew in the pandemic year the `"highlight"` role and the rest the `"background"` role, because the two that grew are the exception the report has to explain.

```
pandemic_figure = BarChart(
    [
        {
            "label": country,
            "y": growth,
            "emphasis": EMPHASIS.HIGHLIGHT if growth > 0 else EMPHASIS.BACKGROUND,
        }
        for country, growth in PANDEMIC.items()
    ],
    title="Only China and Türkiye grew in 2020",
    xlabel="GDP growth in 2020 (%)",
    orientation=ORIENTATION.HORIZONTAL,
    sort=SORT.ASCENDING,
    show_values=True,
    value_format=VALUE_FORMAT.DECIMAL,
    # the value axis is horizontal, so the zero line is vertical
    vlines={"x": 0, "style": {"plot_vline_color": "#666666", "plot_vline_width": 1}},
    figsize=(6.3, 6.0),
)
pandemic_figure.show()
```

China and Türkiye are the only bars to the right of the line, at 2.3 and 1.8%. Everyone else contracted: the United Kingdom at -10.0% with Argentina, Italy and Mexico close behind, and Australia, South Korea, Indonesia and the United States at the top with falls of 2.1% or less. The figure is one year; the growth chart above shows the world back above zero in 2021.

### Who caught up on income?

Growth rates compound into income levels, and the level is what a household feels. GDP per capita in 2000 and 2023, at purchasing-power parity so the dollars buy the same basket everywhere, is a before-and-after question for a [dumbbell chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/dumbbellchart/index.md): a dot at each year and the connector between them is the gain. `sort_by` the 2023 value puts the richest at the top, and `show_values=True, value_kind="delta"` prints each gain at its connector, so a long connector low on the chart is a country catching up and a short one high on it is a rich country growing slowly.

```
income_figure = DumbbellChart(
    [{"label": country, "start": start, "end": end} for country, (start, end) in INCOME.items()],
    title="China's income per head grew fivefold; Italy's barely moved",
    xlabel="GDP per capita (2021 PPP dollars)",
    start_name="2000",
    end_name="2023",
    sort=SORT.DESCENDING,
    sort_by=DUMBBELL_SORT_KEY.END,
    show_values=True, value_kind="delta",
    value_format=VALUE_FORMAT.THOUSANDS,
    show_legend=True,
    figsize=(7.0, 6.0),
)
income_figure.show()
```

The connectors at the top are long in dollars and short in proportion: the United States added 19,306 dollars, a gain of 35%. Lower down the connectors are the reverse. China multiplied its income per head by 5.6, India by 2.9, and both are still in the lower half of the chart, which says how far they started from. Italy, with a gain of 5%, grew least, and the euro-area members and Japan sit just above it. Convergence is under way, and this figure says how much of the gap is left.

### How do the economies compare on every front at once?

A report ends with the table (growth, inflation, unemployment, the current account, trade and investment for every country), and a table of six columns and seventeen rows is read one column at a time. A [parallel coordinates chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/parallelcoords/index.md) draws every column as its own axis and every country as a line across them, so a country's profile is a shape and the countries that look alike run together. `dimensions` picks the axes, every key of the records but the name and the group, and `hue` colours the lines by the World Bank income group, which is the grouping the profiles are expected to follow. Argentina and Türkiye are left off, because their inflation would squash every other line to the bottom of that axis.

```
DIMENSIONS = [key for key in G20_2023[0] if key not in ("country", "income")]

profile_figure = ParallelCoords(
    G20_2023,
    title="The G20 in 2023: the high-income economies grow slowly and invest less",
    dimensions=DIMENSIONS,
    hue="income",
    show_legend=True,
    legend={"location": LEGEND_LOCATION.OUTSIDE_TOP, "ncols": 3},
    figsize=(9.0, 5.0),
)
profile_figure.show()
```

The lines sort themselves by colour on the first and last axes: the high-income group sits low on growth and low on investment, the middle-income group high on both, which is the catch-up of the previous figure seen from its cause. In between, the groups mix, since unemployment and the current account cut across income, and the outliers stand alone: the two lines at the top of the trade axis are South Korea and Germany, the exporters, and the one at the top of investment is China. The profile chart says which rows of the table to read.

## The report figure

A report has room for one figure, not eight. The four that carry the argument (growth and its recessions, the ranking, the pandemic year, and the inflation surge) go into one panel with [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md), which takes the figures already drawn above and redraws them into its cells. Nested lists are the layout, one inner list per row.

```
Grid(
    [
        [growth_figure, rank_figure],
        [pandemic_figure, inflation_figure],
    ],
    title="The major economies: growth, rank, the pandemic year, and the inflation surge",
    figsize=(13.0, 11.0),
).show()
```

Every figure on this page is one call to a chart function over a list of dicts, and every number in them is a World Bank series reshaped by a line or two of Python written out in the cell above it. To adapt any of them, open the guide it links to and read the parameter that does the job; the [annotations guide](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/annotations/index.md) covers the reference lines, bands and notes the figures share. The charts index lists them all: [Charts](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/index.md).
