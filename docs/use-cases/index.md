---
title: Use Cases
---

# Use Cases

The how-to guides answer "how do I draw this chart?". The use cases answer the question a reader usually arrives with: "which figures does my report need, and how do I build them?" Each page takes one field, walks one dataset from the first figure to the last, and ends with the figures composed into a single panel. Every figure links to the chart guide behind it, so the page stays a tour and the guide stays the reference.

The section grows one field at a time: AI, machine learning and NLP, then statistics.

<div class="grid cards card-gallery" markdown>

-   [AI, Machine Learning and NLP](ai-ml-nlp.ipynb)

    The figures of a model report, in the order the work happens: training curves, a hyperparameter sweep, a confusion matrix, ROC and precision-recall curves, calibration, per-class scores, feature importance, a leaderboard across benchmarks, and the token statistics of the corpus behind it.

    <p class="card-icon" markdown="span">:material-robot-outline:</p>

-   [Statistics](statistics.ipynb)

    The figures of a statistics report, in the order the analysis happens: group distributions with their test results, effect sizes with confidence intervals, a bootstrap distribution, a correlation matrix, a scatter matrix, one pair read two ways, a fitted line with its residuals, a Q-Q plot, and the empirical distributions behind it all.

    <p class="card-icon" markdown="span">:material-chart-bell-curve:</p>

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
