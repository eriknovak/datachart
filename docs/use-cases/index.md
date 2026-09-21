---
title: Use Cases
---

# Use Cases

The how-to guides answer "how do I draw this chart?". The use cases answer the question a reader usually arrives with: "which figures does my report need, and how do I build them?" Each page takes one field, walks one dataset from the first figure to the last, and ends with the figures composed into a single panel. Every figure links to the chart guide behind it, so the page stays a tour and the guide stays the reference.

The section grows one field at a time; AI, machine learning, and NLP is the first.

<div class="grid cards card-gallery" markdown>

-   [AI, Machine Learning and NLP](ai-ml-nlp.ipynb)

    The figures of a model report, in the order the work happens: training curves, a hyperparameter sweep, a confusion matrix, ROC and precision-recall curves, calibration, per-class scores, feature importance, a leaderboard across benchmarks, and the token statistics of the corpus behind it.

    <p class="card-icon" markdown="span">:material-robot-outline:</p>

</div>

## What each page answers

| Page | Act | Questions it answers | Charts it reaches for |
| --- | --- | --- | --- |
| [AI, Machine Learning and NLP](ai-ml-nlp.ipynb) | Training | Did the run converge? Which settings mattered? | `LineChart` in a `Panel`, `ParallelCoords` |
| | Evaluation | What does the model confuse? Can its confidence be trusted? | `Heatmap`, `LineChart`, `Histogram`, `BarChart` |
| | Comparison | Where does it sit among published models, and is the gap real? | `BumpChart`, `DumbbellChart`, `ScatterChart` |
| | The data | How long are the documents, and what did filtering remove? | `RidgelinePlot`, `LineChart`, `SankeyChart` |
