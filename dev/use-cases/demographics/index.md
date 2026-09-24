# Demographics and Social Science

A population report asks the same questions in the same order: what the population looks like today and what it looked like a generation ago, how the young and the old traded places over the decades, what drove that shift, and how the country sits among the others, from who gained the most years of life to whether the world is converging and whether income still buys longevity. This page walks one country through those questions, then widens to the world, and names the figure that answers each, so the chart to reach for arrives with the question rather than the other way round. Every figure links to the chart guide that covers it in full.

The country is **Slovenia**, and every number is real. The World Bank's [World Development Indicators](https://datacatalog.worldbank.org/search/dataset/0037712) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) supply the long series (the population by five-year age band and sex, the age-group shares, the fertility rate and the life expectancy from 1960 to 2023) and the world figures (the life expectancy of every country in 1990, 2000, 2010 and 2022, and the GDP per capita and population of 198 countries in 2022). [Eurostat](https://ec.europa.eu/eurostat/data/database) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)) supplies the national detail the world indicators stop short of: immigration and emigration by citizenship in 2023, and the median age of the twelve statistical regions since 2014. Swap the country and the same cells draw it.

```
from datachart.charts import (
    DumbbellChart,
    Heatmap,
    LineChart,
    PyramidChart,
    RidgelinePlot,
    SankeyChart,
    ScatterChart,
    StackedAreaChart,
)
from datachart.constants import (
    DUMBBELL_SORT_KEY,
    EMPHASIS,
    FIG_SIZE,
    LEGEND_LOCATION,
    RIDGELINE_SCALE,
    SCALE,
    SHOW_GRID,
    SORT,
    VALUE_FORMAT,
)
from datachart.utils import Grid, Panel
```

The hidden cell below holds the numbers. `PYRAMID` is the population of each five-year `AGE_BAND` by sex in 1960 and 2023, in thousands; `AGE_SHARES` is the share of the population under 15, of working age and 65 or over in every year since 1960; `VITALS` is the fertility rate and the life expectancy at birth per year; `MIGRATION` is the 2023 immigration and emigration by citizenship group; `REGION_AGE` is the median age of each statistical region on 1 January of every year since 2014; `LIFE_SPAN` is the life expectancy of a dozen countries in 1990 and 2022; `WORLD_LIFE` is the life expectancy of every country in four years; and `PRESTON` is the GDP per capita, life expectancy and population of 198 countries in 2022, with the World Bank region of each. The sections that follow only reshape those into the records the charts take.

## The age structure

### What does the population look like, and what did it look like a lifetime ago?

The pyramid is the first figure of a population report: men to the left, women to the right, one bar per age band from the youngest at the bottom to the oldest at the top. Its outline records the demographic history in one shape. A wide base means many births, a narrow top means few survivors, and every notch is a war, a baby boom or a wave of emigration passing through. A [pyramid chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/pyramidchart/index.md) takes the two sides as two lists of records in the same band order, and `subtitle` names them for the legend.

A change of shape needs two years. Two pyramids drawn with the same `xmax` sit side by side in a [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md), which takes the figures already built and redraws them into its cells, so the bars of 1960 and 2023 share one scale and compare bar to bar.

```
MEN, WOMEN = "Men", "Women"


def pyramid(year):
    return PyramidChart(
        # the two sides, youngest band first: [left, right]
        [
            [{"label": band, "y": people} for band, people in zip(AGE_BANDS, PYRAMID[year][MEN])],
            [{"label": band, "y": people} for band, people in zip(AGE_BANDS, PYRAMID[year][WOMEN])],
        ],
        subtitle=[MEN, WOMEN],
        title=str(year),
        xlabel="Population (thousands)",
        # the same span on both, so the bars compare across the years
        xmax=95,
        show_legend=True,
    )


pyramid_1960, pyramid_2023 = pyramid(1960), pyramid(2023)

Grid(
    [pyramid_1960, pyramid_2023],
    title="Slovenia's population, 1960 and 2023: a pyramid turned into an urn",
    figsize=(9.0, 5.0),
).show()
```

The 1960 shape is the classic pyramid, widest at the bottom and tapering steadily, with a notch at 40–44 for the small cohorts born during the First World War. The 2023 shape is an urn: the base has narrowed to about two thirds of its 1960 width, the widest bands are now 40–49 and 55–59, and the 80+ band has grown from 15 thousand to 117 thousand, with women outnumbering men in it by more than two to one, which is the sex gap in longevity made visible. The population as a whole grew by a third, and all of that growth landed in the upper half.

### How did the young and the old trade places?

Two snapshots show the ends of the change; the yearly shares show its pace and whether it came in steps. The population splits into the under-15s, the working ages and the 65-and-overs, and three shares that sum to a hundred are a [stacked area chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/stackedareachart/index.md): each band's thickness is its share, the bands stack to the whole, and the boundaries between them carry the change. The year the oldest share overtook the youngest is the number a report quotes from this figure, so it is a `vlines` mark with a `label`, computed from the data rather than typed in.

```
AGE_GROUPS = ["Under 15", "15 to 64", "65 and over"]
REFERENCE_VLINE = {"plot_vline_color": "#444444", "plot_vline_style": "--", "plot_vline_width": 1}
YEARS = sorted(AGE_SHARES)

# the first year the 65+ share exceeds the under-15 share
CROSSOVER = next(year for year in YEARS if AGE_SHARES[year][2] > AGE_SHARES[year][0])

shares_figure = StackedAreaChart(
    [
        [{"x": year, "y": AGE_SHARES[year][index]} for year in YEARS]
        for index in range(len(AGE_GROUPS))
    ],
    title=f"The old overtook the young in {CROSSOVER}",
    xlabel="Year",
    ylabel="Share of the population (%)",
    subtitle=AGE_GROUPS,
    vlines={"x": CROSSOVER, "label": f"Crossover ({CROSSOVER})", "style": REFERENCE_VLINE},
    ymax=100,
    show_legend=True,
    legend={"location": LEGEND_LOCATION.OUTSIDE_TOP, "ncols": 4},
    figsize=FIG_SIZE.FULL_MEDIUM,
)
shares_figure.show()
```

The under-15 band thins from 27% in 1960 to 15% in 2023, fastest in the 1980s and 1990s; the 65-and-over band grows from 8% to 21%, slowly at first and steeply after 2010 as the large post-war cohorts pass 65. The two cross in 2004. The working-age band in the middle peaked around 2000 at 70% and has shrunk since, which is the number behind every pension debate: fewer workers per pensioner, and the trend has not turned.

### What drove the shift?

An age structure changes for two reasons, and a report has to separate them: fewer births narrow the base, and longer lives widen the top. Both are yearly series in different units, so they share the year axis and not the value axis. Two [line charts](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md) go into a [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md), each assigned to its own value axis with `y_axis`, so neither flattens the other. The fertility rate is read against the replacement level of 2.1 births per woman, drawn as an `hlines` mark with a `label` on the fertility figure, which owns the left axis.

```
REPLACEMENT = 2.1
REFERENCE_HLINE = {"plot_hline_color": "#666666", "plot_hline_style": "--", "plot_hline_width": 1}

fertility = LineChart(
    [{"x": year, "y": VITALS[year][0]} for year in YEARS],
    subtitle="Fertility rate",
    hlines={"y": REPLACEMENT, "label": f"Replacement ({REPLACEMENT})", "style": REFERENCE_HLINE},
)
longevity = LineChart(
    [{"x": year, "y": VITALS[year][1]} for year in YEARS],
    subtitle="Life expectancy",
)

vitals_figure = Panel(
    [
        {"figure": fertility, "y_axis": "left"},
        {"figure": longevity, "y_axis": "right"},
    ],
    title="Fewer births, longer lives",
    xlabel="Year",
    ylabel_left="Births per woman",
    ylabel_right="Life expectancy at birth (years)",
    ymin=0,
    ymin_right=60,
    show_legend=True,
    show_grid=SHOW_GRID.Y,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
vitals_figure.show()
```

The fertility rate held above replacement until 1980, then fell through it and bottomed at 1.20 in 2003; the partial recovery since has not brought it back. Life expectancy rose from 69 to 82 years over the same period, most of it after 1990. The two curves are the two halves of the previous figure: the base narrowed when the fertility line crossed the dashed one, and the top widened as the life-expectancy line climbed. Neither is a Slovenian peculiarity, which is the reason to widen the view.

## Who comes, who goes, and where they live

### Who arrives, and who leaves?

Births and deaths are half of a population's change; the other half crosses the border, and a report has to say who. A year's migration is a set of flows, so many people of each citizenship arriving and so many leaving, and a [Sankey chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/sankeychart/index.md) draws flows as bands whose width is their size: the arrivals fan out into citizenship groups on the left, and each group splits on the right into the people who left the same year and the net gain that stayed. A group that lost more people than it gained has no gain to show, so a net loss feeds it from the left instead. The `links` are the flows as (source, target, value) records, `column_labels` names the three stages, and `show_values` prints the counts on the nodes.

```
GROUPS = [group for group in MIGRATION["immigration"] if group != "Total"]
arrivals, departures = MIGRATION["immigration"], MIGRATION["emigration"]

links = []
for group in GROUPS:
    links.append({"source": "Immigrants", "target": group, "value": arrivals[group]})
    links.append({"source": group, "target": "Emigrants", "value": departures[group]})
    balance = arrivals[group] - departures[group]
    if balance > 0:
        links.append({"source": group, "target": "Net gain", "value": balance})
    else:
        # a group that shrank is fed from the left, so its node balances
        links.append({"source": "Net loss", "target": group, "value": -balance})

migration_figure = SankeyChart(
    {"links": links},
    title="Slovenia gained 11,500 people in 2023, nearly all from outside the EU",
    column_labels=["Arrivals", "Citizenship", "Departures"],
    show_values=True,
    value_format=VALUE_FORMAT.THOUSANDS,
    figsize=(9.0, 5.5),
)
migration_figure.show()
```

33,939 people arrived and 22,411 left, a net gain of 11,528. Citizens of Bosnia and Herzegovina alone are a third of the arrivals and a net gain of 6,020, with Kosovo, Serbia and North Macedonia behind them: the successor states of the country Slovenia left in 1991 are still where most of its newcomers come from. EU citizens added 418. The one band running the other way is Slovenian citizens: 5,627 left against 4,031 who returned, a net loss of 1,596, so the non-EU inflow covers the whole net gain and the emigration of nationals besides.

### Which regions are ageing fastest?

A national median age hides that the regions age at different speeds, since the capital draws the young and the periphery keeps the old, and the check is one number per region per year. Twelve regions by twelve years is a table that a [heatmap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/heatmap/index.md) reads in one look: each cell coloured by the median age, the rows sorted by the latest year so the oldest region sits at the top, and `show_values` printing the ages so the cells are read rather than guessed. A row that darkens faster than its neighbours is a region ageing faster.

```
REGIONS = sorted(REGION_AGE, key=lambda region: -REGION_AGE[region][-1])

region_figure = Heatmap(
    {"x": REGION_YEARS, "y": REGIONS, "z": [REGION_AGE[region] for region in REGIONS]},
    title="Every region is older than a decade ago; the capital region stays youngest",
    xlabel="Year",
    ylabel="Statistical region, by median age in 2025",
    show_values=True,
    value_format="{x:.1f}",
    show_colorbars=True,
    colorbar={"label": "Median age (years)"},
    figsize=(9.0, 5.5),
)
region_figure.show()
```

Every row darkens from left to right, so no region got younger, and the rows keep their order: Pomurska is the oldest region in every year and Osrednjeslovenska, which holds the capital, the youngest, 6.1 years apart in 2025. The pace differs. Pomurska added 4.5 years of median age in eleven years and Osrednjeslovenska only 2.6, so the gap between the periphery and the centre is widening. This is the regional version of the crossover figure above.

## The country among the others

### Who gained the most years since 1990?

Life expectancy in two years for a dozen countries is a before-and-after comparison, and a [dumbbell chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/dumbbellchart/index.md) is its figure: a dot at 1990, a dot at 2022, and the connector between them is the gain. `sort` and `sort_by` order the rows so the longest-lived countries sit at the top, `show_values=True, value_kind="delta"` prints each gain at the connector, and the country of the page takes the `"highlight"` role through its record's own `emphasis`, so it stands out among its neighbours without a second chart.

```
HOME = "Slovenia"

span_figure = DumbbellChart(
    [
        {
            "label": country,
            "start": start,
            "end": end,
            "emphasis": EMPHASIS.HIGHLIGHT if country == HOME else None,
        }
        for country, (start, end) in LIFE_SPAN.items()
    ],
    title="Every country gained years, some ten times more than others",
    xlabel="Life expectancy at birth (years)",
    start_name="1990",
    end_name="2022",
    sort=SORT.DESCENDING,
    sort_by=DUMBBELL_SORT_KEY.END,
    show_values=True, value_kind="delta",
    value_format=VALUE_FORMAT.DECIMAL,
    show_legend=True,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
span_figure.show()
```

No connector points left: every country in the set lives longer than in 1990. The longest connectors belong to countries that started low (Ethiopia added 22 years, Rwanda 20), and starting low did not guarantee catching up: Nigeria gained 8 years from the lowest start of all, and South Africa, through the HIV epidemic, only 2.6. At the top the gains are small because less is left to gain; the United States, with 2.2 years, gained least of all. Slovenia added 8 years, more than Japan and less than South Korea, which caught up with both. The mixed picture is why the next figure asks the same of every country at once.

### Is the world converging?

A dozen countries suggest convergence; the claim needs all of them. The life expectancy of every country in one year is a distribution, and four years give four distributions that a [ridgeline plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/ridgelineplot/index.md) stacks one above the other, each a smoothed density over the countries, so a shift to the right and a narrowing are both visible at a glance. The rows are years, given as each record's `label`, and `ridge_scale=RIDGELINE_SCALE.COMMON` draws every row to the same height, so a narrower, taller ridge means more countries clustered at one value.

```
world_figure = RidgelinePlot(
    [
        {"label": str(year), "value": value}
        for year, values in WORLD_LIFE.items()
        for value in values
    ],
    title="The world's countries move right and bunch together",
    xlabel="Life expectancy at birth (years)",
    ylabel="Year",
    ridge_scale=RIDGELINE_SCALE.COMMON,
    overlap=0.5,
    xmin=30,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
world_figure.show()
```

In 1990 the ridge is wide and has a second hump, a cluster of countries in the mid-40s below the main peak in the low 70s. Each later ridge moves right and the lower hump shrinks into the shoulder of the main one. By 2022 the median country is at 74 years against 69 in 1990, and the middle half of the countries spans 11 years instead of 13. The world is converging from below: the left tail is what moved.

### Do richer countries live longer?

The Preston curve is the classic figure of development: every country as one point, GDP per capita across, life expectancy up. Income spans two orders of magnitude, so on a linear axis the poorer half of the world piles up against the left edge; `scalex=SCALE.LOG` spreads them out and turns the curve into something close to a line. The [scatter chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md) takes a `hue` per record to colour the points by region and a `size` to scale them by population, so a small rich country and a large poor one read differently. The country of the page gets a `texts` note with a `target`, which draws the arrow from the note to its point.

```
HOME_POINT = next(row for row in PRESTON if row[0] == HOME)

preston_figure = ScatterChart(
    [
        {"x": gdp, "y": life, "size": people, "hue": region}
        for country, region, gdp, life, people in PRESTON
    ],
    title="Income buys years, with diminishing returns",
    xlabel="GDP per capita (2021 PPP dollars, log scale)",
    ylabel="Life expectancy at birth (years)",
    scalex=SCALE.LOG,
    xticks=[1000, 10000, 100000],
    xticklabels=["1,000", "10,000", "100,000"],
    # a note on the home country, with an arrow to its point
    texts={
        "text": HOME,
        "x": 0.08,
        "y": 0.9,
        "coords": "axes",
        "target": (HOME_POINT[2], HOME_POINT[3]),
    },
    ymin=45,
    show_legend=True,
    legend={"location": LEGEND_LOCATION.LOWER_RIGHT},
    show_grid=SHOW_GRID.BOTH,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
preston_figure.show()
```

The cloud rises steeply through the poorer countries and flattens past about 30,000 dollars: the same doubling of income buys many years at the bottom and almost none at the top. The correlation between log income and life expectancy is 0.85 across the 198 countries. The colours add the geography, with Sub-Saharan Africa in the lower left and Europe in the upper right, and the sizes add the people: the two largest circles, India and China, sit in the middle of the band, where most of the world's population lives. Slovenia sits on the curve, at 47,059 dollars and 81 years, where its income predicts.

## The report figure

A report has room for one figure, not ten. The four that carry the argument (the shape today, how the shares shifted, who gained years, and where income puts the country) go into one panel with [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md), which takes the figures drawn above and redraws them into its cells. Nested lists are the layout, one inner list per row, and the pyramid is the same figure that was one cell of the first grid.

```
Grid(
    [
        [pyramid_2023, shares_figure],
        [span_figure, preston_figure],
    ],
    title="Slovenia's population: the shape, the shift, the neighbours, and the curve",
    figsize=(11.0, 8.5),
).show()
```

Every figure on this page is one call to a chart function over a list of dicts, and every number in them is a World Bank series reshaped by a line or two of Python written out in the cell above it. To adapt any of them, open the guide it links to and read the parameter that does the job; the [annotations guide](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/annotations/index.md) covers the reference lines and notes the figures share. The charts index lists them all: [Charts](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/index.md).
