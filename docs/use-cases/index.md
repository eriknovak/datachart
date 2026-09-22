---
title: Use Cases
---

# Use Cases

The how-to guides answer "how do I draw this chart?". The use cases answer the question a reader usually arrives with: "which figures does my report need, and how do I build them?" Each page takes one field, walks one dataset from the first figure to the last, and ends with the figures composed into a single panel. Every figure links to the chart guide behind it, so the page stays a tour and the guide stays the reference.

The section grows one field at a time: AI, machine learning and NLP, statistics, medical and biomedical experiments, demographics and social science, business and product analytics, and economics and finance.

<div class="grid cards card-gallery" markdown>

-   [AI, Machine Learning and NLP](ai-ml-nlp.ipynb)

    The figures of a model report, in the order the work happens: training curves, a hyperparameter sweep, a confusion matrix, ROC and precision-recall curves, calibration, per-class scores, feature importance, a leaderboard across benchmarks, and the token statistics of the corpus behind it.

    <p class="card-icon" markdown="span">:material-robot-outline:</p>

-   [Statistics](statistics.ipynb)

    The figures of a statistics report, in the order the analysis happens: group distributions with their test results, effect sizes with confidence intervals, a bootstrap distribution, a correlation matrix, a scatter matrix, one pair read two ways, a fitted line with its residuals, a Q-Q plot, and the empirical distributions behind it all.

    <p class="card-icon" markdown="span">:material-chart-bell-curve:</p>

-   [Medical and Biomedical Experiments](biomedical.ipynb)

    The figures of a trial report, in the order the questions come: the endpoint per arm with its pairwise tests, the dose-response with intervals, the share at target, the course of the arms over the visits, every subject's own course, who stayed enrolled, the wider marker panel, the safety labs, and the individuals behind a safety signal.

    <p class="card-icon" markdown="span">:material-pill:</p>

-   [Demographics and Social Science](demographics.ipynb)

    The figures of a population report, from one country to the world: the pyramid then and now, how the young and the old traded places, the fertility and longevity behind it, who gained the most years of life, whether the world is converging, and whether income still buys longevity.

    <p class="card-icon" markdown="span">:material-account-group-outline:</p>

-   [Business and Product Analytics](business.ipynb)

    The figures of a product review, in the order the questions come: the revenue mix by plan, the segments that carry it, the channels and their changing ranks, where the funnel leaks, when people sign up, whether the customers who pay stay, and what ships next.

    <p class="card-icon" markdown="span">:material-chart-timeline-variant:</p>

-   [Economics and Finance](economics.ipynb)

    The figures of an economic report on the major economies: growth and its recessions, which economies are largest and how the order changed, how structure shifts with growth, where inflation bit, what the pandemic year cost, who caught up on income, and the G20 compared on every front at once.

    <p class="card-icon" markdown="span">:material-finance:</p>

</div>

## What each page answers

| Page | Act | Questions it answers | Charts it reaches for |
| --- | --- | --- | --- |
| [AI, Machine Learning and NLP](ai-ml-nlp.ipynb) | Training | Did the run converge? Which settings mattered? | `LineChart` in a `Panel`, `ParallelCoords` |
| | Evaluation | What does the model confuse? Can its confidence be trusted? | `Heatmap`, `LineChart`, `Histogram`, `BarChart` |
| | Comparison | Where does it sit among published models, and is the gap real? | `BumpChart`, `DumbbellChart`, `ScatterChart` |
| | The data | How long are the documents, and what did filtering remove? | `RidgelinePlot`, `LineChart`, `SankeyChart` |
| [Statistics](statistics.ipynb) | Comparing the groups | Do the groups differ, and by how much? | `RaincloudPlot`, `ScatterChart`, `Histogram` |
| | Relating the measurements | Which measurements move together, and how much is the pooling hiding? | `Heatmap`, `ScatterMatrix`, `ScatterChart` |
| | Checking the model | Does the fitted line hold up, and are its residuals well behaved? | `ScatterChart` in a `Grid`, `LineChart` |
| [Medical and Biomedical Experiments](biomedical.ipynb) | The primary endpoint | Do the arms differ, by how much, and how many reached the target? | `BoxPlot` and `SwarmPlot` in a `Panel`, `BarChart`, `ViolinPlot` |
| | Over the twelve weeks | When did the arms separate, did every subject follow, and who stayed? | `LineChart` |
| | The wider panel | What else moved with the dose, and is the safety signal an arm or a few subjects? | `Heatmap`, `DumbbellChart`, `SwarmPlot` |
| [Demographics and Social Science](demographics.ipynb) | The age structure | What does the population look like now and then, how did the shares shift, and what drove it? | `PyramidChart` in a `Grid`, `StackedAreaChart`, `LineChart` in a `Panel` |
| | The country among the others | Who gained the most years, is the world converging, and do richer countries live longer? | `DumbbellChart`, `RidgelinePlot`, `ScatterChart` |
| [Business and Product Analytics](business.ipynb) | The revenue | Where does the revenue come from, which segments carry it, and which channels bring the customers? | `StackedAreaChart`, `Treemap`, `BumpChart` |
| | Acquisition and retention | Where does the funnel leak, when do people sign up, and do the customers who pay stay? | `SankeyChart`, `CalendarHeatmap`, `Heatmap` |
| | Planning | What ships when, and what is late? | `GanttChart` |
| [Economics and Finance](economics.ipynb) | Growth | When did the economies shrink, which are the largest, and how does structure change with growth? | `LineChart`, `BumpChart`, `StackedAreaChart` in a `Grid` |
| | Prices, incomes and the shocks | Where did inflation bite, what did the pandemic cost, who caught up, and how do the G20 compare at once? | `Heatmap`, `BarChart`, `DumbbellChart`, `ParallelCoords` |
