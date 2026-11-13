Default world: catalog of 50 items, slates of 3, sessions up to 20 steps. 50 logged datasets per cell, truth from 500,000 simulated sessions per policy.

## What each logging policy gives up to explore

| Logging policy | Its own reward | Change from the default |
|---|---:|---:|
| temperature 0.5 | 0.8815 ± 0.0013 | +10.5% |
| temperature 1 (default) | 0.7978 ± 0.0012 | +0.0% |
| temperature 2 | 0.7490 ± 0.0011 | -6.1% |
| temperature 4 | 0.7295 ± 0.0011 | -8.6% |
| default + 10% uniform | 0.7888 ± 0.0011 | -1.1% |
| default + 30% uniform | 0.7714 ± 0.0011 | -3.3% |

## True values of the target policies

| Target policy | Reward |
|---|---:|
| same as logging | 0.7969 ± 0.0012 |
| slightly different | 0.8171 ± 0.0012 |
| more personalized | 0.8030 ± 0.0012 |
| pushes sponsored | 0.7813 ± 0.0011 |
| much greedier | 1.0166 ± 0.0014 |

## Reward error with 1,000 sessions logged

RMSE as a share of the true value, ± its Monte Carlo standard error. ESS is the mean effective sample size of the session weights, as a share of sessions logged.

### Target: same as logging

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 22.2% | 13.9% ± 1.2 | 8.9% ± 1.0 | 5.9% ± 0.5 | 5.3% ± 0.5 | 3.2% ± 0.3 | 5.7% ± 0.7 |
| temperature 1 (default) | 100.0% | 3.2% ± 0.4 | 3.2% ± 0.4 | 3.2% ± 0.4 | 3.2% ± 0.4 | 3.3% ± 0.3 | 3.1% ± 0.4 |
| temperature 2 | 66.9% | 6.2% ± 0.7 | 5.0% ± 0.5 | 4.3% ± 0.4 | 3.9% ± 0.4 | 3.8% ± 0.3 | 3.9% ± 0.4 |
| temperature 4 | 40.3% | 8.4% ± 0.9 | 6.4% ± 0.7 | 4.5% ± 0.4 | 4.2% ± 0.4 | 3.6% ± 0.4 | 4.3% ± 0.4 |
| default + 10% uniform | 98.4% | 3.2% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.0% ± 0.3 | 3.1% ± 0.2 |
| default + 30% uniform | 87.0% | 4.9% ± 0.4 | 4.2% ± 0.3 | 3.9% ± 0.3 | 3.8% ± 0.3 | 3.8% ± 0.3 | 3.7% ± 0.3 |

### Target: slightly different

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 35.9% | 8.7% ± 0.8 | 6.4% ± 0.7 | 4.6% ± 0.4 | 4.3% ± 0.4 | 3.3% ± 0.3 | 4.3% ± 0.4 |
| temperature 1 (default) | 93.9% | 3.9% ± 0.4 | 3.5% ± 0.4 | 3.5% ± 0.4 | 3.4% ± 0.4 | 3.4% ± 0.4 | 3.3% ± 0.4 |
| temperature 2 | 45.2% | 9.9% ± 1.2 | 7.4% ± 1.1 | 5.1% ± 0.5 | 4.6% ± 0.4 | 4.1% ± 0.3 | 4.6% ± 0.4 |
| temperature 4 | 24.8% | 15.6% ± 3.5 | 10.5% ± 2.2 | 5.6% ± 0.5 | 5.1% ± 0.5 | 3.8% ± 0.4 | 5.0% ± 0.5 |
| default + 10% uniform | 86.8% | 4.1% ± 0.4 | 3.6% ± 0.3 | 3.5% ± 0.4 | 3.3% ± 0.3 | 3.1% ± 0.3 | 3.3% ± 0.3 |
| default + 30% uniform | 68.0% | 6.0% ± 0.5 | 4.7% ± 0.4 | 4.1% ± 0.4 | 3.9% ± 0.3 | 3.8% ± 0.4 | 3.8% ± 0.3 |

### Target: more personalized

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 20.2% | 13.7% ± 1.5 | 9.0% ± 0.9 | 5.7% ± 0.5 | 5.4% ± 0.6 | 3.5% ± 0.3 | 5.0% ± 0.5 |
| temperature 1 (default) | 89.9% | 4.2% ± 0.4 | 3.8% ± 0.4 | 3.3% ± 0.4 | 3.3% ± 0.4 | 3.6% ± 0.3 | 3.3% ± 0.4 |
| temperature 2 | 58.2% | 7.3% ± 0.8 | 5.8% ± 0.7 | 4.5% ± 0.4 | 4.1% ± 0.4 | 4.2% ± 0.4 | 4.1% ± 0.4 |
| temperature 4 | 34.9% | 17.7% ± 5.8 | 11.3% ± 3.1 | 5.4% ± 0.5 | 5.0% ± 0.5 | 3.8% ± 0.4 | 4.9% ± 0.5 |
| default + 10% uniform | 88.4% | 4.2% ± 0.4 | 3.5% ± 0.3 | 3.2% ± 0.3 | 3.1% ± 0.3 | 3.2% ± 0.3 | 3.0% ± 0.2 |
| default + 30% uniform | 76.3% | 5.9% ± 0.5 | 4.9% ± 0.4 | 4.1% ± 0.3 | 4.0% ± 0.3 | 3.8% ± 0.4 | 4.0% ± 0.3 |

### Target: pushes sponsored

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 1.4% | 76.4% ± 3.8 | 51.2% ± 2.5 | 90.6% ± 39.3 | 32.6% ± 5.6 | 5.1% ± 0.6 | 82.7% ± 37.8 |
| temperature 1 (default) | 1.9% | 229.2% ± 98.0 | 58.6% ± 4.5 | 40.8% ± 5.3 | 22.3% ± 1.7 | 5.7% ± 0.5 | 59.0% ± 15.5 |
| temperature 2 | 1.7% | 77.6% ± 8.3 | 45.5% ± 2.3 | 154.8% ± 70.9 | 27.8% ± 3.1 | 5.0% ± 0.5 | 76.8% ± 16.4 |
| temperature 4 | 2.0% | 398.5% ± 193.1 | 48.1% ± 2.1 | 109.9% ± 49.3 | 26.4% ± 4.8 | 5.6% ± 0.5 | 258.1% ± 127.3 |
| default + 10% uniform | 1.8% | 156.5% ± 42.1 | 46.8% ± 2.2 | 36.9% ± 5.6 | 26.0% ± 2.1 | 5.0% ± 0.4 | 53.0% ± 11.6 |
| default + 30% uniform | 1.7% | 81.4% ± 16.1 | 43.2% ± 2.5 | 139.7% ± 34.5 | 38.1% ± 5.7 | 5.6% ± 0.5 | 141.7% ± 35.5 |

### Target: much greedier

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 4.8% | 52.3% ± 10.2 | 28.4% ± 4.0 | 50.5% ± 23.5 | 21.3% ± 6.9 | 4.2% ± 0.5 | 42.1% ± 18.5 |
| temperature 1 (default) | 2.4% | 79.4% ± 9.9 | 44.3% ± 2.1 | 26.9% ± 2.2 | 17.7% ± 1.4 | 4.1% ± 0.5 | 56.1% ± 23.5 |
| temperature 2 | 1.3% | 146.7% ± 37.0 | 57.0% ± 2.5 | 35.5% ± 3.1 | 29.9% ± 2.1 | 4.7% ± 0.5 | 61.2% ± 21.9 |
| temperature 4 | 1.3% | 99.1% ± 16.3 | 63.1% ± 2.5 | 38.5% ± 2.9 | 31.2% ± 2.0 | 4.9% ± 0.5 | 37.3% ± 4.7 |
| default + 10% uniform | 1.4% | 75.8% ± 7.0 | 47.7% ± 3.5 | 39.5% ± 7.8 | 23.5% ± 1.9 | 4.5% ± 0.4 | 37.3% ± 5.3 |
| default + 30% uniform | 1.4% | 73.7% ± 4.4 | 49.8% ± 2.8 | 39.5% ± 7.8 | 22.2% ± 1.6 | 4.5% ± 0.4 | 28.0% ± 3.8 |

## Reward error with 5,000 sessions logged

RMSE as a share of the true value, ± its Monte Carlo standard error. ESS is the mean effective sample size of the session weights, as a share of sessions logged.

### Target: same as logging

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 17.5% | 6.4% ± 0.7 | 4.1% ± 0.4 | 3.0% ± 0.2 | 2.6% ± 0.2 | 1.7% ± 0.2 | 2.6% ± 0.2 |
| temperature 1 (default) | 100.0% | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.3% ± 0.2 | 1.2% ± 0.2 |
| temperature 2 | 67.3% | 2.5% ± 0.2 | 1.9% ± 0.2 | 1.9% ± 0.2 | 1.7% ± 0.2 | 1.6% ± 0.2 | 1.7% ± 0.2 |
| temperature 4 | 38.5% | 5.2% ± 0.7 | 3.9% ± 0.5 | 3.0% ± 0.5 | 2.8% ± 0.5 | 1.6% ± 0.1 | 2.6% ± 0.5 |
| default + 10% uniform | 98.4% | 1.6% ± 0.2 | 1.5% ± 0.2 | 1.5% ± 0.2 | 1.5% ± 0.2 | 1.4% ± 0.1 | 1.4% ± 0.1 |
| default + 30% uniform | 87.0% | 1.7% ± 0.2 | 1.4% ± 0.1 | 1.6% ± 0.1 | 1.4% ± 0.1 | 1.2% ± 0.1 | 1.4% ± 0.1 |

### Target: slightly different

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 32.8% | 3.8% ± 0.3 | 2.5% ± 0.2 | 2.2% ± 0.2 | 2.0% ± 0.1 | 1.8% ± 0.2 | 2.0% ± 0.1 |
| temperature 1 (default) | 93.9% | 1.4% ± 0.1 | 1.3% ± 0.2 | 1.4% ± 0.2 | 1.3% ± 0.2 | 1.4% ± 0.2 | 1.3% ± 0.2 |
| temperature 2 | 45.1% | 3.9% ± 0.3 | 2.7% ± 0.3 | 2.2% ± 0.2 | 1.9% ± 0.2 | 1.6% ± 0.2 | 2.0% ± 0.2 |
| temperature 4 | 21.9% | 9.0% ± 1.7 | 6.5% ± 1.2 | 5.2% ± 1.7 | 4.7% ± 1.5 | 1.6% ± 0.1 | 4.6% ± 1.5 |
| default + 10% uniform | 86.9% | 2.0% ± 0.2 | 1.7% ± 0.1 | 1.8% ± 0.2 | 1.6% ± 0.2 | 1.5% ± 0.1 | 1.6% ± 0.1 |
| default + 30% uniform | 67.6% | 2.4% ± 0.2 | 1.8% ± 0.2 | 1.8% ± 0.1 | 1.6% ± 0.1 | 1.3% ± 0.1 | 1.5% ± 0.1 |

### Target: more personalized

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 16.6% | 6.7% ± 0.9 | 4.0% ± 0.4 | 2.5% ± 0.2 | 2.2% ± 0.2 | 2.0% ± 0.2 | 2.3% ± 0.2 |
| temperature 1 (default) | 90.2% | 1.7% ± 0.2 | 1.5% ± 0.2 | 1.4% ± 0.2 | 1.3% ± 0.2 | 1.6% ± 0.2 | 1.3% ± 0.2 |
| temperature 2 | 56.5% | 3.6% ± 0.7 | 2.7% ± 0.5 | 2.1% ± 0.2 | 1.9% ± 0.2 | 1.7% ± 0.2 | 1.9% ± 0.2 |
| temperature 4 | 32.0% | 6.2% ± 0.7 | 4.6% ± 0.5 | 3.1% ± 0.4 | 2.8% ± 0.4 | 1.5% ± 0.1 | 2.6% ± 0.4 |
| default + 10% uniform | 88.2% | 1.8% ± 0.2 | 1.5% ± 0.2 | 1.5% ± 0.2 | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.4% ± 0.1 |
| default + 30% uniform | 76.1% | 2.4% ± 0.3 | 1.9% ± 0.2 | 1.6% ± 0.1 | 1.5% ± 0.1 | 1.3% ± 0.1 | 1.4% ± 0.1 |

### Target: pushes sponsored

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 0.7% | 68.5% ± 3.7 | 41.8% ± 2.2 | 22.9% ± 1.4 | 20.1% ± 2.2 | 2.7% ± 0.2 | 21.9% ± 2.7 |
| temperature 1 (default) | 0.6% | 115.5% ± 43.2 | 41.6% ± 2.6 | 117.7% ± 53.5 | 24.5% ± 4.0 | 2.4% ± 0.2 | 56.8% ± 18.9 |
| temperature 2 | 0.7% | 59.2% ± 2.2 | 42.5% ± 2.2 | 23.3% ± 2.2 | 18.5% ± 2.1 | 2.7% ± 0.3 | 24.1% ± 3.1 |
| temperature 4 | 0.7% | 580.4% ± 286.7 | 57.6% ± 12.2 | 25.2% ± 1.4 | 19.7% ± 1.3 | 2.3% ± 0.2 | 32.3% ± 12.0 |
| default + 10% uniform | 0.8% | 64.4% ± 5.2 | 41.9% ± 4.2 | 43.2% ± 13.9 | 21.0% ± 4.4 | 2.3% ± 0.2 | 35.3% ± 11.8 |
| default + 30% uniform | 0.8% | 56.4% ± 2.2 | 39.3% ± 1.8 | 18.4% ± 1.3 | 14.9% ± 1.2 | 2.4% ± 0.2 | 14.3% ± 1.5 |

### Target: much greedier

| Logging policy | ESS | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperature 0.5 | 2.6% | 49.2% ± 11.2 | 22.7% ± 4.9 | 28.3% ± 12.2 | 14.4% ± 5.1 | 1.9% ± 0.2 | 27.4% ± 11.7 |
| temperature 1 (default) | 0.8% | 64.4% ± 8.4 | 37.4% ± 1.8 | 22.7% ± 2.6 | 15.7% ± 1.0 | 1.8% ± 0.2 | 19.3% ± 3.1 |
| temperature 2 | 0.5% | 73.8% ± 4.2 | 50.2% ± 2.2 | 31.4% ± 2.3 | 22.6% ± 1.3 | 2.9% ± 0.3 | 28.9% ± 6.5 |
| temperature 4 | 0.5% | 74.7% ± 2.0 | 52.5% ± 1.9 | 73.4% ± 31.4 | 39.1% ± 13.2 | 3.2% ± 0.3 | 84.5% ± 34.0 |
| default + 10% uniform | 0.7% | 58.3% ± 2.7 | 37.2% ± 1.7 | 874.4% ± 436.6 | 19.9% ± 2.0 | 2.8% ± 0.3 | 936.7% ± 467.6 |
| default + 30% uniform | 0.6% | 90.0% ± 12.7 | 47.1% ± 2.3 | 108.7% ± 32.0 | 28.3% ± 5.5 | 3.1% ± 0.3 | 100.5% ± 29.0 |

## Does effective sample size track the error?

Spearman rank correlation, across every (logging policy, target policy) cell, between mean ESS share and RMSE share. Negative means more effective samples go with less error. Each size has 30 cells.

| Sessions logged | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | -0.92 | -0.97 | -0.92 | -0.96 | -0.78 | -0.91 |
| 5,000 | -0.98 | -0.98 | -0.95 | -0.97 | -0.91 | -0.95 |

Finished in 1108 s with seed 4004.
