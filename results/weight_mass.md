Stress test worlds (hidden appeal and sponsored annoyance; the model doesn't matter here), 5 catalogs each, 40 logged datasets of 5,000 sessions per catalog and world from the default logging policy. Truth from 200,000 sessions per policy, catalog and world (its standard error is at most 0.28% of the true value).

The mean session weight is the mean over sessions of the product of the slate probability ratios. Its expectation is exactly 1 under the logging policy. The lowest step mean is the smallest, over steps, of the mean cumulative weight up to that step, which also has expectation 1 at every step.

## Mean session weight by world and target

| World | Target | Median | Mean | Below 1 | 10th percentile | Largest | Median lowest step mean |
|---|---|---:|---:|---:|---:|---:|---:|
| appeal 0, annoyance 0 | same as logging | 1.000 | 1.000 | 0% | 1.000 | 1.00 | 1.000 |
| appeal 0, annoyance 0 | slightly different | 1.000 | 1.000 | 50% | 0.996 | 1.01 | 0.998 |
| appeal 0, annoyance 0 | more personalized | 0.999 | 0.999 | 58% | 0.992 | 1.02 | 0.996 |
| appeal 0, annoyance 0 | pushes sponsored | 0.623 | 0.784 | 86% | 0.455 | 8.46 | 0.614 |
| appeal 0, annoyance 0 | much greedier | 0.742 | 0.883 | 82% | 0.532 | 4.36 | 0.693 |
| appeal 1, annoyance 0 | same as logging | 1.000 | 1.000 | 0% | 1.000 | 1.00 | 1.000 |
| appeal 1, annoyance 0 | slightly different | 1.000 | 1.000 | 50% | 0.996 | 1.01 | 0.998 |
| appeal 1, annoyance 0 | more personalized | 1.001 | 1.001 | 47% | 0.991 | 1.03 | 0.996 |
| appeal 1, annoyance 0 | pushes sponsored | 0.591 | 0.754 | 89% | 0.432 | 4.70 | 0.573 |
| appeal 1, annoyance 0 | much greedier | 0.741 | 0.926 | 74% | 0.535 | 6.19 | 0.695 |
| appeal 0, annoyance 0.3 | same as logging | 1.000 | 1.000 | 0% | 1.000 | 1.00 | 1.000 |
| appeal 0, annoyance 0.3 | slightly different | 1.000 | 1.000 | 46% | 0.996 | 1.01 | 0.998 |
| appeal 0, annoyance 0.3 | more personalized | 1.000 | 1.000 | 53% | 0.992 | 1.02 | 0.997 |
| appeal 0, annoyance 0.3 | pushes sponsored | 0.862 | 0.957 | 74% | 0.705 | 3.39 | 0.831 |
| appeal 0, annoyance 0.3 | much greedier | 0.777 | 0.911 | 82% | 0.648 | 6.18 | 0.760 |
| appeal 1, annoyance 0.3 | same as logging | 1.000 | 1.000 | 0% | 1.000 | 1.00 | 1.000 |
| appeal 1, annoyance 0.3 | slightly different | 1.000 | 1.000 | 54% | 0.996 | 1.01 | 0.998 |
| appeal 1, annoyance 0.3 | more personalized | 1.000 | 1.001 | 52% | 0.990 | 1.15 | 0.996 |
| appeal 1, annoyance 0.3 | pushes sponsored | 0.836 | 0.968 | 76% | 0.677 | 11.91 | 0.804 |
| appeal 1, annoyance 0.3 | much greedier | 0.781 | 1.214 | 84% | 0.627 | 66.26 | 0.764 |

## Signed reward error by mean session weight (all worlds pooled)

Average signed error as a share of the true value, ± its standard error, and the number of datasets.

| Target | Mean session weight | Datasets | IPS | SNIPS | PDIS | SNPDIS |
|---|---|---:|---:|---:|---:|---:|
| same as logging | 0.9 to 1.1 | 800 | +0.0% ± 0.1 | +0.0% ± 0.1 | +0.0% ± 0.1 | +0.0% ± 0.1 |
| slightly different | 0.9 to 1.1 | 800 | +0.0% ± 0.1 | +0.0% ± 0.1 | -0.0% ± 0.1 | -0.0% ± 0.1 |
| more personalized | 0.9 to 1.1 | 799 | +0.1% ± 0.1 | +0.0% ± 0.1 | -0.0% ± 0.1 | -0.0% ± 0.1 |
| more personalized | 1.1 or more | 1 | +44.0% ± nan | +25.6% ± nan | +5.7% ± nan | +2.5% ± nan |
| pushes sponsored | below 0.5 | 91 | -74.5% ± 0.6 | -42.9% ± 1.1 | -17.8% ± 2.2 | -6.1% ± 2.2 |
| pushes sponsored | 0.5 to 0.9 | 479 | -49.8% ± 0.7 | -29.6% ± 0.7 | -9.6% ± 1.8 | -7.3% ± 0.7 |
| pushes sponsored | 0.9 to 1.1 | 118 | -13.6% ± 3.1 | -12.1% ± 3.0 | +2.6% ± 5.2 | -6.1% ± 1.8 |
| pushes sponsored | 1.1 or more | 112 | +82.4% ± 17.0 | +3.9% ± 4.8 | +1.0% ± 3.5 | -9.1% ± 1.7 |
| much greedier | below 0.5 | 18 | -74.7% ± 0.9 | -45.5% ± 1.6 | -11.4% ± 4.2 | -3.6% ± 3.6 |
| much greedier | 0.5 to 0.9 | 547 | -52.6% ± 0.6 | -33.5% ± 0.6 | -8.7% ± 0.9 | -6.9% ± 0.6 |
| much greedier | 0.9 to 1.1 | 119 | -17.7% ± 2.8 | -16.5% ± 2.7 | -5.0% ± 2.1 | -8.2% ± 1.4 |
| much greedier | 1.1 or more | 116 | +288.4% ± 165.7 | +12.1% ± 4.8 | +27.5% ± 17.8 | -4.9% ± 2.1 |

## How well a low weight flags a large error (far targets, all worlds pooled, 1600 estimates)

A large error is one above 10% of the true value. Flagged: share of datasets the flag fires on. Large if flagged / if not: share of large errors among flagged and unflagged datasets. Caught: share of large errors the flag fires on. False alarms: share of datasets without a large error that the flag fires on.

### IPS, reward (large error in 95% of datasets)

| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |
|---|---:|---:|---:|---:|---:|
| mean session weight below 0.5 | 7% | 100% | 95% | 7% | 0% |
| mean session weight below 0.7 | 38% | 100% | 93% | 40% | 0% |
| mean session weight below 0.9 | 71% | 99% | 86% | 74% | 15% |
| lowest step mean below 0.5 | 8% | 100% | 95% | 8% | 0% |
| lowest step mean below 0.7 | 43% | 99% | 92% | 45% | 7% |
| lowest step mean below 0.9 | 83% | 97% | 88% | 85% | 58% |

### SNIPS, reward (large error in 90% of datasets)

| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |
|---|---:|---:|---:|---:|---:|
| mean session weight below 0.5 | 7% | 99% | 89% | 8% | 1% |
| mean session weight below 0.7 | 38% | 97% | 86% | 41% | 12% |
| mean session weight below 0.9 | 71% | 93% | 83% | 73% | 51% |
| lowest step mean below 0.5 | 8% | 99% | 89% | 9% | 1% |
| lowest step mean below 0.7 | 43% | 94% | 87% | 45% | 24% |
| lowest step mean below 0.9 | 83% | 91% | 86% | 84% | 76% |

### PDIS, reward (large error in 70% of datasets)

| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |
|---|---:|---:|---:|---:|---:|
| mean session weight below 0.5 | 7% | 85% | 69% | 8% | 3% |
| mean session weight below 0.7 | 38% | 76% | 66% | 41% | 31% |
| mean session weight below 0.9 | 71% | 71% | 66% | 73% | 67% |
| lowest step mean below 0.5 | 8% | 87% | 68% | 10% | 4% |
| lowest step mean below 0.7 | 43% | 76% | 65% | 47% | 34% |
| lowest step mean below 0.9 | 83% | 72% | 59% | 86% | 78% |

### SNPDIS, reward (large error in 62% of datasets)

| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |
|---|---:|---:|---:|---:|---:|
| mean session weight below 0.5 | 7% | 61% | 62% | 7% | 7% |
| mean session weight below 0.7 | 38% | 61% | 63% | 37% | 39% |
| mean session weight below 0.9 | 71% | 60% | 67% | 69% | 75% |
| lowest step mean below 0.5 | 8% | 61% | 62% | 8% | 8% |
| lowest step mean below 0.7 | 43% | 61% | 63% | 42% | 44% |
| lowest step mean below 0.9 | 83% | 62% | 65% | 83% | 85% |

### IPS, cost (large error in 93% of datasets)

| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |
|---|---:|---:|---:|---:|---:|
| mean session weight below 0.5 | 7% | 100% | 93% | 7% | 0% |
| mean session weight below 0.7 | 38% | 100% | 89% | 40% | 0% |
| mean session weight below 0.9 | 71% | 99% | 79% | 76% | 7% |
| lowest step mean below 0.5 | 8% | 100% | 93% | 9% | 0% |
| lowest step mean below 0.7 | 43% | 99% | 89% | 46% | 5% |
| lowest step mean below 0.9 | 83% | 96% | 78% | 86% | 46% |

### SNIPS, cost (large error in 88% of datasets)

| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |
|---|---:|---:|---:|---:|---:|
| mean session weight below 0.5 | 7% | 100% | 87% | 8% | 0% |
| mean session weight below 0.7 | 38% | 99% | 81% | 43% | 2% |
| mean session weight below 0.9 | 71% | 95% | 69% | 77% | 26% |
| lowest step mean below 0.5 | 8% | 98% | 87% | 9% | 1% |
| lowest step mean below 0.7 | 43% | 97% | 80% | 48% | 10% |
| lowest step mean below 0.9 | 83% | 91% | 70% | 87% | 60% |

### PDIS, cost (large error in 79% of datasets)

| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |
|---|---:|---:|---:|---:|---:|
| mean session weight below 0.5 | 7% | 96% | 78% | 8% | 1% |
| mean session weight below 0.7 | 38% | 93% | 70% | 44% | 13% |
| mean session weight below 0.9 | 71% | 86% | 62% | 77% | 47% |
| lowest step mean below 0.5 | 8% | 94% | 78% | 9% | 2% |
| lowest step mean below 0.7 | 43% | 91% | 69% | 50% | 18% |
| lowest step mean below 0.9 | 83% | 83% | 59% | 88% | 68% |

### SNPDIS, cost (large error in 70% of datasets)

| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |
|---|---:|---:|---:|---:|---:|
| mean session weight below 0.5 | 7% | 87% | 69% | 8% | 3% |
| mean session weight below 0.7 | 38% | 81% | 63% | 44% | 23% |
| mean session weight below 0.9 | 71% | 76% | 56% | 77% | 57% |
| lowest step mean below 0.5 | 8% | 84% | 69% | 10% | 4% |
| lowest step mean below 0.7 | 43% | 79% | 63% | 49% | 30% |
| lowest step mean below 0.9 | 83% | 73% | 57% | 87% | 76% |

## How often each flag fires on near targets (same as logging, slightly different, more personalized; 2400 datasets)

| Flag | Fires |
|---|---:|
| mean session weight below 0.5 | 0% |
| mean session weight below 0.7 | 0% |
| mean session weight below 0.9 | 0% |
| lowest step mean below 0.5 | 0% |
| lowest step mean below 0.7 | 0% |
| lowest step mean below 0.9 | 0% |

PDIS's reward error was large in 0% of these datasets.

Finished in 382 s with seed 4004.
