# Use Cases

The how-to guides answer "how do I draw this chart?". The use cases answer the question a reader usually arrives with: "which figures does my report need, and how do I build them?" Each page takes one field, walks one dataset from the first figure to the last, and ends with the figures composed into a single panel. Every figure links to the chart guide behind it, so the page stays a tour and the guide stays the reference.

The section grows one field at a time: AI, machine learning and NLP, statistics, then medical and biomedical experiments.

- [AI, Machine Learning and NLP](https://eriknovak.github.io/datachart/dev/use-cases/ai-ml-nlp/index.md)

  The figures of a model report, in the order the work happens: training curves, a hyperparameter sweep, a confusion matrix, ROC and precision-recall curves, calibration, per-class scores, feature importance, a leaderboard across benchmarks, and the token statistics of the corpus behind it.

- [Statistics](https://eriknovak.github.io/datachart/dev/use-cases/statistics/index.md)

  The figures of a statistics report, in the order the analysis happens: group distributions with their test results, effect sizes with confidence intervals, a bootstrap distribution, a correlation matrix, a scatter matrix, one pair read two ways, a fitted line with its residuals, a Q-Q plot, and the empirical distributions behind it all.

- [Medical and Biomedical Experiments](https://eriknovak.github.io/datachart/dev/use-cases/biomedical/index.md)

  The figures of a trial report, in the order the questions come: the endpoint per arm with its pairwise tests, the dose-response with intervals, the share at target, the course of the arms over the visits, every subject's own course, who stayed enrolled, the wider marker panel, the safety labs, and the individuals behind a safety signal.

## What each page answers

| Page                                                                                                          | Act                       | Questions it answers                                                              | Charts it reaches for                                            |
| ------------------------------------------------------------------------------------------------------------- | ------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [AI, Machine Learning and NLP](https://eriknovak.github.io/datachart/dev/use-cases/ai-ml-nlp/index.md)        | Training                  | Did the run converge? Which settings mattered?                                    | `LineChart` in a `Panel`, `ParallelCoords`                       |
|                                                                                                               | Evaluation                | What does the model confuse? Can its confidence be trusted?                       | `Heatmap`, `LineChart`, `Histogram`, `BarChart`                  |
|                                                                                                               | Comparison                | Where does it sit among published models, and is the gap real?                    | `BumpChart`, `DumbbellChart`, `ScatterChart`                     |
|                                                                                                               | The data                  | How long are the documents, and what did filtering remove?                        | `RidgelinePlot`, `LineChart`, `SankeyChart`                      |
| [Statistics](https://eriknovak.github.io/datachart/dev/use-cases/statistics/index.md)                         | Comparing the groups      | Do the groups differ, and by how much?                                            | `RaincloudPlot`, `ScatterChart`, `Histogram`                     |
|                                                                                                               | Relating the measurements | Which measurements move together, and how much is the pooling hiding?             | `Heatmap`, `ScatterMatrix`, `ScatterChart`                       |
|                                                                                                               | Checking the model        | Does the fitted line hold up, and are its residuals well behaved?                 | `ScatterChart` in a `Grid`, `LineChart`                          |
| [Medical and Biomedical Experiments](https://eriknovak.github.io/datachart/dev/use-cases/biomedical/index.md) | The primary endpoint      | Do the arms differ, by how much, and how many reached the target?                 | `BoxPlot` and `SwarmPlot` in a `Panel`, `BarChart`, `ViolinPlot` |
|                                                                                                               | Over the twelve weeks     | When did the arms separate, did every subject follow, and who stayed?             | `LineChart`                                                      |
|                                                                                                               | The wider panel           | What else moved with the dose, and is the safety signal an arm or a few subjects? | `Heatmap`, `DumbbellChart`, `SwarmPlot`                          |
