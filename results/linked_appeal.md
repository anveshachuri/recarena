5 catalogs, 20 logged datasets per catalog and size, truth from 200,000 sessions per policy, catalog and world. Informed model. Errors are percent of the true value, pooled across catalogs (100 datasets per cell). Cells show mean error / RMSE. The truth's own standard error is at most 0.27% of the true value.

| World | Hidden appeal | Link to quality | Sponsored shift |
|---|---:|---:|---:|
| No hidden appeal | 0 | 0 | 0 |
| Unrelated appeal (stress test) | 1 | 0 | 0 |
| Appeal follows quality | 1 | 0.7 | 0 |
| Appeal against quality | 1 | -0.7 | 0 |
| Sponsored items more appealing | 1 | 0 | 1 |
| Sponsored items less appealing | 1 | 0 | -1 |

## No hidden appeal (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | +0.0 / 1.5 | +0.0 / 1.5 | +0.0 / 1.5 | +0.0 / 1.5 | -0.2 / 1.4 | +0.1 / 1.5 |
| slightly different | -0.1 / 1.7 | -0.1 / 1.6 | -0.1 / 1.6 | -0.1 / 1.5 | -0.4 / 1.6 | -0.0 / 1.5 |
| more personalized | -0.0 / 2.7 | -0.0 / 2.1 | -0.1 / 1.6 | -0.1 / 1.5 | -1.4 / 2.1 | -0.1 / 1.5 |
| pushes sponsored | -29.9 / 147.6 | -31.2 / 43.9 | +6.2 / 116.6 | -5.7 / 24.1 | +0.7 / 2.4 | +11.9 / 114.8 |
| much greedier | -42.2 / 65.1 | -31.1 / 39.4 | -5.7 / 25.5 | -4.5 / 18.3 | +0.3 / 2.4 | +3.4 / 29.5 |

## Unrelated appeal (stress test) (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | +0.1 / 1.4 | +0.1 / 1.4 | +0.1 / 1.4 | +0.1 / 1.4 | -0.1 / 1.4 | +0.1 / 1.4 |
| slightly different | +0.0 / 1.7 | +0.1 / 1.6 | +0.1 / 1.5 | +0.1 / 1.5 | -0.2 / 1.4 | +0.1 / 1.5 |
| more personalized | +0.0 / 2.6 | +0.1 / 2.1 | +0.1 / 1.7 | +0.1 / 1.6 | -1.0 / 1.7 | +0.1 / 1.6 |
| pushes sponsored | -47.5 / 68.3 | -32.6 / 40.8 | -11.4 / 26.9 | -8.2 / 20.4 | +0.7 / 2.7 | -1.2 / 29.2 |
| much greedier | -44.3 / 56.7 | -31.4 / 36.8 | -5.6 / 26.7 | -7.5 / 15.8 | +3.4 / 4.8 | +1.5 / 22.9 |

## Appeal follows quality (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | +0.1 / 1.2 | +0.1 / 1.2 | +0.1 / 1.2 | +0.1 / 1.2 | -0.0 / 1.1 | +0.2 / 1.1 |
| slightly different | +0.0 / 1.4 | +0.0 / 1.2 | +0.0 / 1.2 | +0.0 / 1.1 | -0.2 / 1.2 | +0.1 / 1.1 |
| more personalized | -0.4 / 2.5 | -0.2 / 1.9 | +0.1 / 1.3 | +0.1 / 1.3 | -1.0 / 1.5 | +0.1 / 1.3 |
| pushes sponsored | -37.8 / 126.6 | -33.1 / 45.3 | -10.4 / 36.9 | -11.1 / 20.3 | +0.4 / 2.0 | -4.8 / 47.7 |
| much greedier | -41.9 / 87.9 | -34.3 / 40.8 | -6.7 / 50.8 | -10.8 / 18.5 | -0.0 / 2.8 | -0.4 / 53.3 |

## Appeal against quality (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | +0.3 / 1.4 | +0.3 / 1.4 | +0.3 / 1.4 | +0.3 / 1.4 | -0.0 / 1.4 | +0.3 / 1.4 |
| slightly different | +0.1 / 1.6 | +0.2 / 1.5 | +0.2 / 1.5 | +0.2 / 1.4 | -0.1 / 1.4 | +0.1 / 1.5 |
| more personalized | +0.6 / 3.4 | +0.5 / 2.6 | +0.3 / 1.6 | +0.3 / 1.5 | -0.9 / 1.7 | +0.3 / 1.5 |
| pushes sponsored | -46.9 / 74.5 | -29.7 / 43.2 | -2.6 / 81.2 | -7.0 / 24.7 | +1.2 / 2.9 | +9.2 / 68.4 |
| much greedier | -28.6 / 59.8 | -22.6 / 40.3 | -0.2 / 29.2 | -2.6 / 18.1 | +5.1 / 5.8 | +0.5 / 30.6 |

## Sponsored items more appealing (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | +0.0 / 1.3 | +0.0 / 1.3 | +0.0 / 1.3 | +0.0 / 1.3 | -0.2 / 1.3 | +0.0 / 1.3 |
| slightly different | +0.1 / 1.5 | +0.1 / 1.4 | +0.1 / 1.4 | +0.1 / 1.4 | -0.2 / 1.3 | +0.1 / 1.3 |
| more personalized | -0.2 / 3.0 | -0.1 / 2.3 | +0.1 / 1.9 | +0.1 / 1.7 | -1.0 / 1.6 | +0.1 / 1.6 |
| pushes sponsored | -17.1 / 320.2 | -37.9 / 47.5 | +34.7 / 477.5 | -13.1 / 21.8 | +2.3 / 3.6 | +38.4 / 433.9 |
| much greedier | +29.0 / 306.3 | -20.5 / 43.4 | -6.0 / 34.7 | -6.4 / 18.4 | +2.6 / 4.5 | -6.6 / 47.9 |

## Sponsored items less appealing (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | +0.2 / 1.4 | +0.2 / 1.4 | +0.2 / 1.4 | +0.2 / 1.4 | +0.0 / 1.3 | +0.3 / 1.4 |
| slightly different | +0.2 / 1.6 | +0.2 / 1.5 | +0.2 / 1.5 | +0.2 / 1.4 | -0.0 / 1.4 | +0.3 / 1.4 |
| more personalized | +0.1 / 2.4 | +0.1 / 1.9 | +0.2 / 1.6 | +0.2 / 1.5 | -0.8 / 1.7 | +0.3 / 1.5 |
| pushes sponsored | -46.7 / 62.2 | -30.8 / 40.0 | -5.1 / 51.4 | -7.2 / 24.6 | +1.5 / 2.9 | +3.0 / 55.4 |
| much greedier | -34.9 / 70.4 | -28.0 / 41.7 | -7.3 / 22.1 | -7.0 / 15.7 | +3.7 / 4.8 | -1.5 / 26.4 |

## Mean error by world (5,000 sessions)

Mean error ± its Monte Carlo standard error, in percent of the true value. Catalogs differ, so part of the spread is between catalogs.

| World | Estimator | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---|---|---:|---:|---:|---:|---:|
| No hidden appeal | Direct | -0.2 ± 0.1 | -0.4 ± 0.2 | -1.4 ± 0.2 | +0.7 ± 0.2 | +0.3 ± 0.2 |
| No hidden appeal | DR | +0.1 ± 0.1 | -0.0 ± 0.2 | -0.1 ± 0.2 | +11.9 ± 11.5 | +3.4 ± 2.9 |
| No hidden appeal | SNPDIS | +0.0 ± 0.1 | -0.1 ± 0.2 | -0.1 ± 0.2 | -5.7 ± 2.3 | -4.5 ± 1.8 |
| Unrelated appeal (stress test) | Direct | -0.1 ± 0.1 | -0.2 ± 0.1 | -1.0 ± 0.1 | +0.7 ± 0.3 | +3.4 ± 0.3 |
| Unrelated appeal (stress test) | DR | +0.1 ± 0.1 | +0.1 ± 0.1 | +0.1 ± 0.2 | -1.2 ± 2.9 | +1.5 ± 2.3 |
| Unrelated appeal (stress test) | SNPDIS | +0.1 ± 0.1 | +0.1 ± 0.1 | +0.1 ± 0.2 | -8.2 ± 1.9 | -7.5 ± 1.4 |
| Appeal follows quality | Direct | -0.0 ± 0.1 | -0.2 ± 0.1 | -1.0 ± 0.1 | +0.4 ± 0.2 | -0.0 ± 0.3 |
| Appeal follows quality | DR | +0.2 ± 0.1 | +0.1 ± 0.1 | +0.1 ± 0.1 | -4.8 ± 4.8 | -0.4 ± 5.4 |
| Appeal follows quality | SNPDIS | +0.1 ± 0.1 | +0.0 ± 0.1 | +0.1 ± 0.1 | -11.1 ± 1.7 | -10.8 ± 1.5 |
| Appeal against quality | Direct | -0.0 ± 0.1 | -0.1 ± 0.1 | -0.9 ± 0.1 | +1.2 ± 0.3 | +5.1 ± 0.3 |
| Appeal against quality | DR | +0.3 ± 0.1 | +0.1 ± 0.1 | +0.3 ± 0.1 | +9.2 ± 6.8 | +0.5 ± 3.1 |
| Appeal against quality | SNPDIS | +0.3 ± 0.1 | +0.2 ± 0.1 | +0.3 ± 0.1 | -7.0 ± 2.4 | -2.6 ± 1.8 |
| Sponsored items more appealing | Direct | -0.2 ± 0.1 | -0.2 ± 0.1 | -1.0 ± 0.1 | +2.3 ± 0.3 | +2.6 ± 0.4 |
| Sponsored items more appealing | DR | +0.0 ± 0.1 | +0.1 ± 0.1 | +0.1 ± 0.2 | +38.4 ± 43.4 | -6.6 ± 4.8 |
| Sponsored items more appealing | SNPDIS | +0.0 ± 0.1 | +0.1 ± 0.1 | +0.1 ± 0.2 | -13.1 ± 1.8 | -6.4 ± 1.7 |
| Sponsored items less appealing | Direct | +0.0 ± 0.1 | -0.0 ± 0.1 | -0.8 ± 0.1 | +1.5 ± 0.2 | +3.7 ± 0.3 |
| Sponsored items less appealing | DR | +0.3 ± 0.1 | +0.3 ± 0.1 | +0.3 ± 0.1 | +3.0 ± 5.6 | -1.5 ± 2.7 |
| Sponsored items less appealing | SNPDIS | +0.2 ± 0.1 | +0.2 ± 0.1 | +0.2 ± 0.2 | -7.2 ± 2.4 | -7.0 ± 1.4 |

Finished in 1740 s with seed 4004.
