Default world and catalog, default logging policy (temperature 1, history weight 1, quality weight 1). 100 logged datasets per size, each scored once per kind of error. Truth from 300,000 sessions per target; its standard error is at most 0.19% of the true value. Errors are percent of the true reward. Direct uses no logged probabilities, so it is the same for every kind of error.

| Kind of error | How the logged probabilities are computed |
|---|---|
| exact | the true logging policy |
| temperature 0.8 | the logging policy with temperature 0.8 and history weight 1 |
| temperature 0.9 | the logging policy with temperature 0.9 and history weight 1 |
| temperature 1.1 | the logging policy with temperature 1.1 and history weight 1 |
| temperature 1.2 | the logging policy with temperature 1.2 and history weight 1 |
| history weight 0.8 | the logging policy with temperature 1 and history weight 0.8 |
| history weight 1.2 | the logging policy with temperature 1 and history weight 1.2 |
| fitted, all features | a softmax policy fitted to the logs by maximum likelihood, using history, quality, sponsored |
| fitted, quality only | a softmax policy fitted to the logs by maximum likelihood, using quality |

## Fitted weights (5,000 sessions)

Mean ± standard deviation across datasets. The truth is 1, 1, 0.

| Kind of error | History weight | Quality weight | Sponsored weight |
|---|---:|---:|---:|
| fitted, all features | 1.006 ± 0.139 | 1.000 ± 0.010 | 0.001 ± 0.007 |
| fitted, quality only | 0.000 ± 0.000 | 1.001 ± 0.010 | 0.000 ± 0.000 |

## Bias / RMSE (5,000 sessions)

Mean error / RMSE, in percent of the true value.

### same as logging

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| exact | +0.2 / 1.4 | +0.2 / 1.4 | +0.2 / 1.4 | +0.2 / 1.4 | -0.1 / 1.4 | +0.2 / 1.4 |
| temperature 0.8 | +11.7 / 11.8 | +1.4 / 2.0 | +2.8 / 3.2 | -1.5 / 2.1 | -0.1 / 1.4 | +0.2 / 1.4 |
| temperature 0.9 | +1.6 / 2.2 | -0.3 / 1.4 | -0.0 / 1.4 | -0.9 / 1.6 | -0.1 / 1.4 | +0.2 / 1.4 |
| temperature 1.1 | +3.0 / 3.3 | +1.7 / 2.2 | +1.9 / 2.4 | +1.3 / 1.9 | -0.1 / 1.4 | +0.1 / 1.4 |
| temperature 1.2 | +8.4 / 8.6 | +3.9 / 4.2 | +4.5 / 4.8 | +2.6 / 2.9 | -0.1 / 1.4 | +0.1 / 1.4 |
| history weight 0.8 | +0.3 / 1.4 | +0.2 / 1.4 | +0.2 / 1.4 | +0.2 / 1.4 | -0.1 / 1.4 | +0.2 / 1.4 |
| history weight 1.2 | +0.2 / 1.4 | +0.1 / 1.4 | +0.1 / 1.4 | +0.1 / 1.4 | -0.1 / 1.4 | +0.1 / 1.4 |
| fitted, all features | +0.2 / 1.4 | +0.2 / 1.4 | +0.2 / 1.4 | +0.2 / 1.4 | -0.1 / 1.4 | +0.2 / 1.4 |
| fitted, quality only | +2.3 / 2.7 | +1.3 / 1.9 | +0.9 / 1.7 | +0.6 / 1.5 | -0.1 / 1.4 | +0.4 / 1.4 |

### slightly different

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| exact | +0.0 / 1.4 | +0.0 / 1.4 | +0.0 / 1.4 | +0.1 / 1.4 | -0.2 / 1.4 | +0.1 / 1.4 |
| temperature 0.8 | -0.2 / 1.4 | -2.0 / 2.4 | -1.7 / 2.2 | -2.5 / 2.8 | -0.2 / 1.4 | +0.1 / 1.4 |
| temperature 0.9 | -3.3 / 3.6 | -1.8 / 2.3 | -2.0 / 2.4 | -1.4 / 1.9 | -0.2 / 1.4 | +0.1 / 1.4 |
| temperature 1.1 | +7.0 / 7.3 | +2.8 / 3.2 | +3.4 / 3.7 | +1.6 / 2.1 | -0.2 / 1.4 | +0.1 / 1.5 |
| temperature 1.2 | +16.5 / 16.7 | +6.0 / 6.2 | +7.5 / 7.7 | +3.1 / 3.4 | -0.2 / 1.4 | +0.1 / 1.5 |
| history weight 0.8 | +0.4 / 1.5 | +0.2 / 1.4 | +0.2 / 1.4 | +0.1 / 1.4 | -0.2 / 1.4 | +0.1 / 1.4 |
| history weight 1.2 | -0.2 / 1.5 | -0.1 / 1.4 | -0.0 / 1.4 | -0.0 / 1.4 | -0.2 / 1.4 | +0.0 / 1.4 |
| fitted, all features | +0.0 / 1.4 | +0.1 / 1.4 | +0.1 / 1.4 | +0.1 / 1.4 | -0.2 / 1.4 | +0.1 / 1.4 |
| fitted, quality only | +3.2 / 3.6 | +1.8 / 2.3 | +1.1 / 1.8 | +0.6 / 1.5 | -0.2 / 1.4 | +0.3 / 1.5 |

### more personalized

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| exact | +0.1 / 1.8 | +0.1 / 1.6 | +0.1 / 1.5 | +0.1 / 1.4 | -0.7 / 1.5 | +0.1 / 1.4 |
| temperature 0.8 | +9.8 / 10.0 | +0.4 / 1.8 | +2.4 / 2.8 | -1.7 / 2.2 | -0.7 / 1.5 | +0.2 / 1.5 |
| temperature 0.9 | +0.8 / 2.0 | -0.8 / 1.8 | -0.2 / 1.5 | -1.0 / 1.7 | -0.7 / 1.5 | +0.2 / 1.4 |
| temperature 1.1 | +3.7 / 4.1 | +2.1 / 2.6 | +2.1 / 2.5 | +1.4 / 2.0 | -0.7 / 1.5 | +0.1 / 1.5 |
| temperature 1.2 | +9.8 / 10.0 | +4.6 / 4.9 | +4.8 / 5.1 | +2.7 / 3.1 | -0.7 / 1.5 | +0.2 / 1.5 |
| history weight 0.8 | +1.5 / 2.4 | +0.8 / 1.9 | +0.5 / 1.6 | +0.3 / 1.5 | -0.7 / 1.5 | +0.2 / 1.5 |
| history weight 1.2 | -1.0 / 1.9 | -0.5 / 1.6 | -0.2 / 1.4 | -0.0 / 1.4 | -0.7 / 1.5 | +0.1 / 1.4 |
| fitted, all features | +0.1 / 1.7 | +0.1 / 1.6 | +0.1 / 1.5 | +0.1 / 1.5 | -0.7 / 1.5 | +0.1 / 1.5 |
| fitted, quality only | +9.2 / 9.8 | +4.8 / 5.4 | +2.7 / 3.2 | +1.2 / 2.0 | -0.7 / 1.5 | +0.5 / 1.7 |

### pushes sponsored

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| exact | -45.1 / 80.9 | -34.5 / 41.3 | -12.5 / 22.7 | -9.3 / 18.5 | +0.2 / 2.3 | -7.2 / 33.3 |
| temperature 0.8 | -35.7 / 95.9 | -34.0 / 40.5 | -8.3 / 22.9 | -10.8 / 19.7 | +0.2 / 2.3 | -8.8 / 40.6 |
| temperature 0.9 | -42.6 / 85.3 | -34.7 / 41.2 | -11.6 / 22.7 | -10.1 / 19.1 | +0.2 / 2.3 | -7.6 / 35.5 |
| temperature 1.1 | -45.4 / 78.6 | -33.8 / 41.2 | -12.1 / 22.6 | -8.4 / 18.1 | +0.2 / 2.3 | -7.0 / 32.4 |
| temperature 1.2 | -44.5 / 77.3 | -32.8 / 41.0 | -11.0 / 22.3 | -7.6 / 17.8 | +0.2 / 2.3 | -7.1 / 32.3 |
| history weight 0.8 | -45.0 / 80.9 | -34.5 / 41.3 | -12.4 / 22.7 | -9.2 / 18.4 | +0.2 / 2.3 | -7.2 / 33.4 |
| history weight 1.2 | -45.1 / 80.9 | -34.5 / 41.4 | -12.5 / 22.8 | -9.3 / 18.6 | +0.2 / 2.3 | -7.2 / 33.3 |
| fitted, all features | -45.4 / 80.1 | -34.7 / 41.2 | -12.6 / 23.2 | -9.3 / 18.5 | +0.2 / 2.3 | -7.2 / 33.1 |
| fitted, quality only | -44.3 / 80.4 | -34.0 / 40.7 | -11.9 / 22.4 | -9.0 / 18.1 | +0.2 / 2.3 | -7.1 / 33.6 |

### much greedier

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| exact | -39.1 / 80.5 | -29.3 / 41.4 | +8.4 / 105.5 | -4.2 / 23.3 | +1.8 / 2.5 | +15.5 / 98.1 |
| temperature 0.8 | -74.9 / 76.8 | -43.0 / 47.2 | -33.9 / 42.4 | -11.9 / 21.0 | +1.8 / 2.5 | +4.9 / 23.9 |
| temperature 0.9 | -60.2 / 70.3 | -35.8 / 43.6 | -15.4 / 57.0 | -7.8 / 21.8 | +1.8 / 2.5 | +8.8 / 51.2 |
| temperature 1.1 | -9.9 / 128.2 | -23.7 / 40.2 | +38.4 / 187.2 | -1.2 / 25.0 | +1.8 / 2.5 | +25.8 / 171.3 |
| temperature 1.2 | +29.0 / 220.6 | -18.7 / 39.8 | +75.5 / 305.4 | +1.3 / 26.6 | +1.8 / 2.5 | +40.5 / 277.0 |
| history weight 0.8 | -38.5 / 81.2 | -29.0 / 41.3 | +9.2 / 110.5 | -4.1 / 23.4 | +1.8 / 2.5 | +16.1 / 102.9 |
| history weight 1.2 | -39.6 / 79.9 | -29.6 / 41.5 | +7.6 / 100.9 | -4.3 / 23.2 | +1.8 / 2.5 | +14.9 / 93.8 |
| fitted, all features | -39.4 / 78.9 | -29.4 / 41.2 | +8.2 / 103.4 | -4.2 / 23.2 | +1.8 / 2.5 | +15.2 / 95.5 |
| fitted, quality only | -35.8 / 83.0 | -27.6 / 40.5 | +13.3 / 133.2 | -3.5 / 23.8 | +1.8 / 2.5 | +18.6 / 123.8 |

## Shift caused by the error (5,000 sessions)

Each dataset's estimate with the wrong probabilities minus its estimate with exact ones, in percent of the true value, mean ± Monte Carlo standard error. Pairing on the same data removes most of the run to run noise, so this is much more precise than the difference of the biases above.

### same as logging

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | DR |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | +11.5 ± 0.1 | +1.2 ± 0.1 | +2.7 ± 0.0 | -1.7 ± 0.0 | +0.1 ± 0.0 |
| temperature 0.9 | +1.4 ± 0.0 | -0.5 ± 0.0 | -0.2 ± 0.0 | -1.0 ± 0.0 | +0.0 ± 0.0 |
| temperature 1.1 | +2.9 ± 0.0 | +1.6 ± 0.0 | +1.8 ± 0.0 | +1.2 ± 0.0 | -0.0 ± 0.0 |
| temperature 1.2 | +8.3 ± 0.1 | +3.7 ± 0.0 | +4.4 ± 0.0 | +2.4 ± 0.0 | -0.0 ± 0.0 |
| history weight 0.8 | +0.1 ± 0.0 | +0.1 ± 0.0 | +0.1 ± 0.0 | +0.1 ± 0.0 | +0.0 ± 0.0 |
| history weight 1.2 | +0.0 ± 0.0 | -0.0 ± 0.0 | -0.0 ± 0.0 | -0.0 ± 0.0 | -0.0 ± 0.0 |
| fitted, all features | +0.0 ± 0.0 | +0.0 ± 0.0 | +0.0 ± 0.0 | +0.0 ± 0.0 | +0.0 ± 0.0 |
| fitted, quality only | +2.1 ± 0.0 | +1.2 ± 0.0 | +0.7 ± 0.0 | +0.4 ± 0.0 | +0.2 ± 0.0 |

### slightly different

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | DR |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | -0.2 ± 0.1 | -2.0 ± 0.0 | -1.7 ± 0.0 | -2.5 ± 0.0 | +0.0 ± 0.0 |
| temperature 0.9 | -3.4 ± 0.0 | -1.9 ± 0.0 | -2.1 ± 0.0 | -1.4 ± 0.0 | +0.0 ± 0.0 |
| temperature 1.1 | +7.0 ± 0.0 | +2.8 ± 0.0 | +3.3 ± 0.0 | +1.5 ± 0.0 | -0.0 ± 0.0 |
| temperature 1.2 | +16.5 ± 0.1 | +6.0 ± 0.1 | +7.4 ± 0.0 | +3.0 ± 0.0 | -0.0 ± 0.0 |
| history weight 0.8 | +0.3 ± 0.0 | +0.2 ± 0.0 | +0.1 ± 0.0 | +0.1 ± 0.0 | +0.0 ± 0.0 |
| history weight 1.2 | -0.2 ± 0.0 | -0.1 ± 0.0 | -0.1 ± 0.0 | -0.1 ± 0.0 | -0.0 ± 0.0 |
| fitted, all features | +0.0 ± 0.1 | +0.0 ± 0.0 | +0.0 ± 0.0 | +0.0 ± 0.0 | +0.0 ± 0.0 |
| fitted, quality only | +3.2 ± 0.1 | +1.7 ± 0.0 | +1.0 ± 0.0 | +0.5 ± 0.0 | +0.2 ± 0.0 |

### more personalized

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | DR |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | +9.6 ± 0.1 | +0.3 ± 0.1 | +2.2 ± 0.0 | -1.8 ± 0.0 | +0.1 ± 0.0 |
| temperature 0.9 | +0.7 ± 0.0 | -0.9 ± 0.0 | -0.4 ± 0.0 | -1.1 ± 0.0 | +0.0 ± 0.0 |
| temperature 1.1 | +3.5 ± 0.0 | +1.9 ± 0.0 | +1.9 ± 0.0 | +1.3 ± 0.0 | +0.0 ± 0.0 |
| temperature 1.2 | +9.6 ± 0.1 | +4.5 ± 0.0 | +4.7 ± 0.0 | +2.5 ± 0.0 | +0.0 ± 0.0 |
| history weight 0.8 | +1.3 ± 0.0 | +0.7 ± 0.0 | +0.4 ± 0.0 | +0.2 ± 0.0 | +0.1 ± 0.0 |
| history weight 1.2 | -1.1 ± 0.0 | -0.6 ± 0.0 | -0.3 ± 0.0 | -0.2 ± 0.0 | -0.1 ± 0.0 |
| fitted, all features | -0.0 ± 0.1 | -0.0 ± 0.0 | -0.0 ± 0.0 | +0.0 ± 0.0 | +0.0 ± 0.0 |
| fitted, quality only | +9.1 ± 0.2 | +4.6 ± 0.1 | +2.5 ± 0.1 | +1.1 ± 0.0 | +0.3 ± 0.0 |

### pushes sponsored

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | DR |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | +9.4 ± 2.9 | +0.4 ± 0.6 | +4.1 ± 0.5 | -1.5 ± 0.3 | -1.7 ± 1.1 |
| temperature 0.9 | +2.5 ± 1.0 | -0.2 ± 0.3 | +0.9 ± 0.2 | -0.8 ± 0.1 | -0.5 ± 0.4 |
| temperature 1.1 | -0.3 ± 0.6 | +0.7 ± 0.2 | +0.4 ± 0.1 | +0.9 ± 0.1 | +0.1 ± 0.3 |
| temperature 1.2 | +0.6 ± 1.1 | +1.7 ± 0.4 | +1.5 ± 0.3 | +1.7 ± 0.2 | +0.1 ± 0.5 |
| history weight 0.8 | +0.0 ± 0.1 | +0.0 ± 0.0 | +0.1 ± 0.0 | +0.0 ± 0.0 | +0.0 ± 0.0 |
| history weight 1.2 | +0.0 ± 0.1 | -0.0 ± 0.0 | -0.0 ± 0.0 | -0.0 ± 0.0 | -0.0 ± 0.0 |
| fitted, all features | -0.3 ± 0.5 | -0.2 ± 0.1 | -0.1 ± 0.2 | -0.1 ± 0.1 | -0.1 ± 0.2 |
| fitted, quality only | +0.7 ± 0.3 | +0.5 ± 0.2 | +0.6 ± 0.2 | +0.3 ± 0.1 | +0.0 ± 0.2 |

### much greedier

| Kind of error | IPS | SNIPS | PDIS | SNPDIS | DR |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | -35.8 ± 5.4 | -13.7 ± 1.1 | -42.3 ± 8.0 | -7.7 ± 0.6 | -10.6 ± 7.4 |
| temperature 0.9 | -21.1 ± 3.5 | -6.5 ± 0.5 | -23.8 ± 5.1 | -3.5 ± 0.3 | -6.7 ± 4.7 |
| temperature 1.1 | +29.2 ± 5.9 | +5.7 ± 0.4 | +30.0 ± 7.9 | +3.0 ± 0.2 | +10.3 ± 7.3 |
| temperature 1.2 | +68.1 ± 15.2 | +10.6 ± 0.7 | +67.1 ± 19.2 | +5.5 ± 0.4 | +25.0 ± 17.8 |
| history weight 0.8 | +0.6 ± 0.2 | +0.3 ± 0.0 | +0.9 ± 0.6 | +0.1 ± 0.0 | +0.6 ± 0.5 |
| history weight 1.2 | -0.5 ± 0.1 | -0.3 ± 0.0 | -0.8 ± 0.5 | -0.1 ± 0.0 | -0.5 ± 0.5 |
| fitted, all features | -0.3 ± 0.6 | -0.0 ± 0.1 | -0.2 ± 0.5 | +0.0 ± 0.0 | -0.3 ± 0.4 |
| fitted, quality only | +3.3 ± 0.7 | +1.8 ± 0.2 | +4.9 ± 3.0 | +0.7 ± 0.1 | +3.2 ± 2.8 |

## Warning sign: share of datasets flagged (5,000 sessions)

Percent of datasets whose per-session sum of (step ratio - 1) is more than 1.96 standard errors from 0, for each target's ratios. With exact probabilities about 5% should be flagged by chance.

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---|---:|---:|---:|---:|---:|
| exact | 0% | 1% | 5% | 2% | 3% |
| temperature 0.8 | 100% | 100% | 100% | 60% | 100% |
| temperature 0.9 | 100% | 100% | 95% | 6% | 100% |
| temperature 1.1 | 100% | 100% | 96% | 5% | 100% |
| temperature 1.2 | 100% | 100% | 100% | 5% | 100% |
| history weight 0.8 | 23% | 3% | 23% | 3% | 3% |
| history weight 1.2 | 27% | 1% | 24% | 3% | 4% |
| fitted, all features | 0% | 0% | 0% | 0% | 2% |
| fitted, quality only | 100% | 100% | 100% | 3% | 2% |

Finished in 1935 s with seed 4004.
