Default world except slate size and session length: catalog of 50 items, one catalog (seed 0), logging policy at temperature 1, no fitted models. 200 logged datasets per cell, truth from 500,000 simulated sessions per policy and world.

CascadePDIS weights a reward in slot j of step t by the full slate ratios of earlier steps times the ratio of only the first j slots at step t. It is unbiased here because users read top down and stop at their first click. SNCascadePDIS normalizes the weights for each step and slot.

## True values

| Slate size | Session length | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 0.1240 | 0.1266 | 0.1239 | 0.1219 | 0.1601 |
| 2 | 20 | 0.6117 | 0.6250 | 0.6170 | 0.5984 | 0.7808 |
| 3 | 1 | 0.1524 | 0.1564 | 0.1527 | 0.1501 | 0.1981 |
| 3 | 20 | 0.7992 | 0.8150 | 0.8037 | 0.7780 | 1.0168 |
| 5 | 1 | 0.1830 | 0.1882 | 0.1837 | 0.1795 | 0.2364 |
| 5 | 20 | 1.0186 | 1.0416 | 1.0264 | 0.9972 | 1.3003 |

## Reward error (RMSE as a share of the true value, ± Monte Carlo standard error)

### Slates of 2, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 6.5% ± 0.3 | 6.5% ± 0.3 | 6.5% ± 0.3 | 6.5% ± 0.3 |
| slightly different | 6.7% ± 0.3 | 6.6% ± 0.3 | 6.7% ± 0.3 | 6.6% ± 0.3 |
| more personalized | 6.5% ± 0.3 | 6.5% ± 0.3 | 6.5% ± 0.3 | 6.5% ± 0.3 |
| pushes sponsored | 11.6% ± 0.7 | 10.6% ± 0.6 | 10.1% ± 0.6 | 9.5% ± 0.5 |
| much greedier | 10.2% ± 0.5 | 9.2% ± 0.5 | 9.2% ± 0.5 | 8.7% ± 0.4 |

### Slates of 2, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 2.8% ± 0.1 | 2.8% ± 0.1 | 2.8% ± 0.1 | 2.8% ± 0.1 |
| slightly different | 2.9% ± 0.1 | 2.9% ± 0.1 | 2.9% ± 0.1 | 2.9% ± 0.1 |
| more personalized | 2.8% ± 0.1 | 2.8% ± 0.1 | 2.8% ± 0.1 | 2.8% ± 0.1 |
| pushes sponsored | 5.4% ± 0.3 | 5.0% ± 0.3 | 4.4% ± 0.2 | 4.2% ± 0.2 |
| much greedier | 4.5% ± 0.2 | 4.2% ± 0.2 | 4.1% ± 0.2 | 3.9% ± 0.2 |

### Slates of 2, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 3.5% ± 0.2 | 3.5% ± 0.2 | 3.5% ± 0.2 | 3.5% ± 0.2 |
| slightly different | 3.7% ± 0.2 | 3.6% ± 0.2 | 3.7% ± 0.2 | 3.6% ± 0.2 |
| more personalized | 3.5% ± 0.2 | 3.5% ± 0.2 | 3.5% ± 0.2 | 3.5% ± 0.2 |
| pushes sponsored | 25.5% ± 3.7 | 19.0% ± 1.7 | 21.8% ± 1.7 | 17.6% ± 1.2 |
| much greedier | 25.9% ± 3.0 | 17.5% ± 1.0 | 22.5% ± 2.1 | 17.1% ± 1.0 |

### Slates of 2, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 1.8% ± 0.1 | 1.8% ± 0.1 | 1.8% ± 0.1 | 1.8% ± 0.1 |
| slightly different | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 |
| more personalized | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 |
| pushes sponsored | 21.0% ± 2.5 | 15.6% ± 1.2 | 19.1% ± 2.1 | 14.8% ± 1.2 |
| much greedier | 19.7% ± 4.3 | 14.4% ± 2.0 | 18.8% ± 3.8 | 13.2% ± 1.6 |

### Slates of 3, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 5.6% ± 0.2 | 5.6% ± 0.2 | 5.6% ± 0.2 | 5.6% ± 0.2 |
| slightly different | 5.7% ± 0.2 | 5.6% ± 0.2 | 5.7% ± 0.2 | 5.6% ± 0.2 |
| more personalized | 5.6% ± 0.2 | 5.6% ± 0.2 | 5.6% ± 0.2 | 5.6% ± 0.2 |
| pushes sponsored | 12.6% ± 0.7 | 12.1% ± 0.8 | 9.3% ± 0.5 | 9.0% ± 0.4 |
| much greedier | 10.7% ± 0.5 | 9.7% ± 0.4 | 8.5% ± 0.4 | 8.0% ± 0.4 |

### Slates of 3, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 2.5% ± 0.1 | 2.5% ± 0.1 | 2.5% ± 0.1 | 2.5% ± 0.1 |
| slightly different | 2.6% ± 0.1 | 2.5% ± 0.1 | 2.6% ± 0.1 | 2.6% ± 0.1 |
| more personalized | 2.5% ± 0.1 | 2.5% ± 0.1 | 2.5% ± 0.1 | 2.5% ± 0.1 |
| pushes sponsored | 6.4% ± 0.4 | 5.6% ± 0.3 | 4.5% ± 0.2 | 4.1% ± 0.2 |
| much greedier | 4.8% ± 0.3 | 4.3% ± 0.2 | 4.2% ± 0.2 | 3.9% ± 0.2 |

### Slates of 3, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 3.7% ± 0.2 | 3.7% ± 0.2 | 3.7% ± 0.2 | 3.7% ± 0.2 |
| slightly different | 3.9% ± 0.2 | 3.8% ± 0.2 | 3.9% ± 0.2 | 3.8% ± 0.2 |
| more personalized | 3.7% ± 0.2 | 3.7% ± 0.2 | 3.7% ± 0.2 | 3.7% ± 0.2 |
| pushes sponsored | 46.4% ± 8.4 | 26.2% ± 1.5 | 36.3% ± 3.5 | 24.3% ± 1.4 |
| much greedier | 38.9% ± 4.1 | 23.7% ± 1.0 | 28.7% ± 1.8 | 21.3% ± 0.9 |

### Slates of 3, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.5% ± 0.1 |
| slightly different | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.5% ± 0.1 |
| more personalized | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.5% ± 0.1 |
| pushes sponsored | 32.6% ± 3.9 | 19.7% ± 1.0 | 26.5% ± 3.7 | 17.9% ± 0.9 |
| much greedier | 27.3% ± 3.0 | 17.1% ± 1.3 | 29.7% ± 5.6 | 15.2% ± 0.9 |

### Slates of 5, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 4.7% ± 0.2 | 4.7% ± 0.2 | 4.7% ± 0.2 | 4.7% ± 0.2 |
| slightly different | 4.8% ± 0.2 | 4.8% ± 0.2 | 4.8% ± 0.2 | 4.8% ± 0.2 |
| more personalized | 4.7% ± 0.2 | 4.7% ± 0.2 | 4.7% ± 0.2 | 4.7% ± 0.2 |
| pushes sponsored | 20.1% ± 1.9 | 16.8% ± 1.1 | 10.5% ± 0.6 | 10.0% ± 0.6 |
| much greedier | 15.7% ± 0.9 | 12.5% ± 0.6 | 8.2% ± 0.4 | 7.5% ± 0.4 |

### Slates of 5, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 |
| slightly different | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 |
| more personalized | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 | 1.9% ± 0.1 |
| pushes sponsored | 8.2% ± 0.4 | 6.8% ± 0.4 | 5.0% ± 0.3 | 4.7% ± 0.2 |
| much greedier | 6.5% ± 0.3 | 5.3% ± 0.3 | 4.1% ± 0.2 | 3.7% ± 0.2 |

### Slates of 5, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 2.9% ± 0.1 | 2.9% ± 0.1 | 2.9% ± 0.1 | 2.9% ± 0.1 |
| slightly different | 3.2% ± 0.1 | 3.0% ± 0.1 | 3.2% ± 0.1 | 3.0% ± 0.1 |
| more personalized | 3.3% ± 0.2 | 3.2% ± 0.2 | 3.3% ± 0.2 | 3.1% ± 0.2 |
| pushes sponsored | 3482.2% ± 1700.8 | 32.2% ± 1.5 | 7626.9% ± 3811.2 | 29.2% ± 1.3 |
| much greedier | 54.7% ± 7.1 | 31.0% ± 0.9 | 55.2% ± 8.7 | 28.4% ± 0.9 |

### Slates of 5, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 |
| slightly different | 1.5% ± 0.1 | 1.4% ± 0.1 | 1.5% ± 0.1 | 1.4% ± 0.1 |
| more personalized | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.5% ± 0.1 | 1.4% ± 0.1 |
| pushes sponsored | 483.8% ± 238.6 | 30.4% ± 2.1 | 422.1% ± 209.0 | 27.0% ± 1.4 |
| much greedier | 53.3% ± 10.5 | 27.2% ± 1.0 | 51.8% ± 11.9 | 25.8% ± 1.2 |

## Reward bias (average signed error as a share of the true value, ± standard error)

### Slates of 2, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | +0.1% ± 0.5 | +0.1% ± 0.5 | +0.1% ± 0.5 | +0.1% ± 0.5 |
| slightly different | +0.4% ± 0.5 | +0.4% ± 0.5 | +0.4% ± 0.5 | +0.4% ± 0.5 |
| more personalized | +0.3% ± 0.5 | +0.3% ± 0.5 | +0.3% ± 0.5 | +0.3% ± 0.5 |
| pushes sponsored | +0.4% ± 0.8 | +0.5% ± 0.7 | +0.4% ± 0.7 | +0.4% ± 0.7 |
| much greedier | +0.6% ± 0.7 | +0.7% ± 0.7 | +0.3% ± 0.7 | +0.3% ± 0.6 |

### Slates of 2, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | -0.0% ± 0.2 | -0.0% ± 0.2 | -0.0% ± 0.2 | -0.0% ± 0.2 |
| slightly different | +0.3% ± 0.2 | +0.3% ± 0.2 | +0.3% ± 0.2 | +0.3% ± 0.2 |
| more personalized | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 |
| pushes sponsored | +0.1% ± 0.4 | +0.1% ± 0.4 | -0.0% ± 0.3 | -0.1% ± 0.3 |
| much greedier | +0.6% ± 0.3 | +0.5% ± 0.3 | +0.4% ± 0.3 | +0.4% ± 0.3 |

### Slates of 2, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | +0.4% ± 0.2 | +0.4% ± 0.2 | +0.4% ± 0.2 | +0.4% ± 0.2 |
| slightly different | +0.5% ± 0.3 | +0.5% ± 0.3 | +0.5% ± 0.3 | +0.4% ± 0.3 |
| more personalized | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 |
| pushes sponsored | -7.4% ± 1.7 | -5.7% ± 1.3 | -7.0% ± 1.5 | -5.4% ± 1.2 |
| much greedier | -4.3% ± 1.8 | -4.9% ± 1.2 | -4.3% ± 1.6 | -4.4% ± 1.2 |

### Slates of 2, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 |
| slightly different | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 |
| more personalized | -0.3% ± 0.1 | -0.3% ± 0.1 | -0.3% ± 0.1 | -0.3% ± 0.1 |
| pushes sponsored | -1.4% ± 1.5 | -1.5% ± 1.1 | -1.4% ± 1.3 | -1.3% ± 1.0 |
| much greedier | -3.7% ± 1.4 | -3.7% ± 1.0 | -3.3% ± 1.3 | -3.5% ± 0.9 |

### Slates of 3, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | +0.8% ± 0.4 | +0.8% ± 0.4 | +0.8% ± 0.4 | +0.8% ± 0.4 |
| slightly different | +0.5% ± 0.4 | +0.5% ± 0.4 | +0.5% ± 0.4 | +0.4% ± 0.4 |
| more personalized | +0.6% ± 0.4 | +0.6% ± 0.4 | +0.6% ± 0.4 | +0.6% ± 0.4 |
| pushes sponsored | -0.1% ± 0.9 | +0.5% ± 0.9 | -0.1% ± 0.7 | +0.1% ± 0.6 |
| much greedier | +0.6% ± 0.8 | +0.0% ± 0.7 | -0.1% ± 0.6 | -0.3% ± 0.6 |

### Slates of 3, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 |
| slightly different | -0.1% ± 0.2 | -0.1% ± 0.2 | -0.1% ± 0.2 | -0.1% ± 0.2 |
| more personalized | +0.0% ± 0.2 | +0.0% ± 0.2 | +0.0% ± 0.2 | +0.0% ± 0.2 |
| pushes sponsored | +0.0% ± 0.5 | -0.0% ± 0.4 | +0.1% ± 0.3 | +0.2% ± 0.3 |
| much greedier | -0.5% ± 0.3 | -0.5% ± 0.3 | -0.4% ± 0.3 | -0.4% ± 0.3 |

### Slates of 3, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | -0.4% ± 0.3 | -0.4% ± 0.3 | -0.4% ± 0.3 | -0.4% ± 0.3 |
| slightly different | -0.0% ± 0.3 | -0.0% ± 0.3 | -0.0% ± 0.3 | -0.0% ± 0.3 |
| more personalized | -0.2% ± 0.3 | -0.2% ± 0.3 | -0.2% ± 0.3 | -0.3% ± 0.3 |
| pushes sponsored | -10.6% ± 3.2 | -10.5% ± 1.7 | -9.9% ± 2.5 | -9.1% ± 1.6 |
| much greedier | -8.6% ± 2.7 | -9.3% ± 1.5 | -9.6% ± 1.9 | -8.4% ± 1.4 |

### Slates of 3, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | -0.1% ± 0.1 | -0.1% ± 0.1 | -0.1% ± 0.1 | -0.1% ± 0.1 |
| slightly different | +0.3% ± 0.1 | +0.3% ± 0.1 | +0.3% ± 0.1 | +0.3% ± 0.1 |
| more personalized | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 |
| pushes sponsored | -9.5% ± 2.2 | -8.1% ± 1.3 | -9.7% ± 1.7 | -7.4% ± 1.2 |
| much greedier | -3.9% ± 1.9 | -5.5% ± 1.2 | -3.4% ± 2.1 | -5.4% ± 1.0 |

### Slates of 5, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | -0.0% ± 0.3 | -0.0% ± 0.3 | -0.0% ± 0.3 | -0.0% ± 0.3 |
| slightly different | -0.5% ± 0.3 | -0.5% ± 0.3 | -0.6% ± 0.3 | -0.6% ± 0.3 |
| more personalized | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 |
| pushes sponsored | -0.7% ± 1.4 | -0.4% ± 1.2 | +0.5% ± 0.7 | +0.5% ± 0.7 |
| much greedier | +1.0% ± 1.1 | +0.4% ± 0.9 | -0.9% ± 0.6 | -1.2% ± 0.5 |

### Slates of 5, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | +0.2% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 |
| slightly different | -0.3% ± 0.1 | -0.3% ± 0.1 | -0.3% ± 0.1 | -0.3% ± 0.1 |
| more personalized | -0.1% ± 0.1 | -0.1% ± 0.1 | -0.1% ± 0.1 | -0.1% ± 0.1 |
| pushes sponsored | -0.4% ± 0.6 | -0.3% ± 0.5 | +0.1% ± 0.4 | +0.1% ± 0.3 |
| much greedier | -0.3% ± 0.5 | -0.3% ± 0.4 | -0.1% ± 0.3 | -0.1% ± 0.3 |

### Slates of 5, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 |
| slightly different | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 |
| more personalized | +0.3% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 |
| pushes sponsored | +260.4% ± 246.2 | -16.6% ± 2.0 | +534.4% ± 539.3 | -14.4% ± 1.8 |
| much greedier | -18.7% ± 3.6 | -19.4% ± 1.7 | -17.2% ± 3.7 | -17.4% ± 1.6 |

### Slates of 5, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |
|---|---:|---:|---:|---:|
| same as logging | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 |
| slightly different | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 |
| more personalized | +0.2% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 |
| pushes sponsored | +14.7% ± 34.3 | -14.8% ± 1.9 | +10.8% ± 29.9 | -14.1% ± 1.6 |
| much greedier | -15.4% ± 3.6 | -16.2% ± 1.5 | -12.3% ± 3.6 | -13.8% ± 1.5 |

Finished in 475 s with seed 4004.
