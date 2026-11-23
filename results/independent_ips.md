Default world except slate size and session length: catalog of 50 items, one catalog (seed 0), logging policy at temperature 1, no fitted models. 50 logged datasets per cell, truth from 200,000 simulated sessions per policy and world.

CascadePDIS weights a reward in slot j of step t by the full slate ratios of earlier steps times the ratio of only the first j slots at step t. It is unbiased here because users read top down and stop at their first click. SNCascadePDIS normalizes the weights for each step and slot.

IndependentIPS (Li et al. 2018) weights a value in slot j of step t by the full slate ratios of earlier steps times the ratio of the chance that the logged item lands in slot j, over everything else in the slate. That assumes a slot's value depends only on its own item. Here that holds for costs within a step (a slot adds cost only if its own item is sponsored), so costs are the control, and fails for rewards, because a slot's reward depends on whether the user clicked above it.

## True values (reward)

| Slate size | Session length | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 0.1248 | 0.1264 | 0.1239 | 0.1217 | 0.1603 |
| 2 | 20 | 0.6113 | 0.6248 | 0.6176 | 0.5972 | 0.7802 |
| 3 | 1 | 0.1524 | 0.1560 | 0.1530 | 0.1504 | 0.1988 |
| 3 | 20 | 0.7979 | 0.8157 | 0.8060 | 0.7796 | 1.0173 |
| 5 | 1 | 0.1830 | 0.1879 | 0.1830 | 0.1797 | 0.2364 |
| 5 | 20 | 1.0171 | 1.0416 | 1.0266 | 0.9968 | 1.3037 |

## True values (cost)

| Slate size | Session length | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 0.1745 | 0.1737 | 0.1747 | 0.4800 | 0.1670 |
| 2 | 20 | 1.3661 | 1.3597 | 1.3726 | 3.7500 | 1.2995 |
| 3 | 1 | 0.1747 | 0.1742 | 0.1750 | 0.4747 | 0.1660 |
| 3 | 20 | 1.4670 | 1.4622 | 1.4739 | 3.9784 | 1.3881 |
| 5 | 1 | 0.1745 | 0.1740 | 0.1752 | 0.4625 | 0.1656 |
| 5 | 20 | 1.5782 | 1.5707 | 1.5844 | 4.1745 | 1.4879 |

## Reward error (RMSE as a share of the true value, ± Monte Carlo standard error)

### Slates of 2, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 6.5% ± 0.8 | 6.5% ± 0.8 | 6.5% ± 0.8 | 6.5% ± 0.8 | 6.5% ± 0.8 |
| slightly different | 6.7% ± 0.8 | 6.7% ± 0.8 | 6.7% ± 0.8 | 6.6% ± 0.8 | 6.7% ± 0.8 |
| more personalized | 6.5% ± 0.8 | 6.5% ± 0.8 | 6.5% ± 0.8 | 6.5% ± 0.8 | 6.5% ± 0.8 |
| pushes sponsored | 10.4% ± 1.0 | 10.4% ± 1.0 | 9.8% ± 1.0 | 9.6% ± 1.0 | 9.6% ± 0.9 |
| much greedier | 10.7% ± 1.1 | 10.0% ± 1.0 | 9.0% ± 1.0 | 8.6% ± 0.8 | 8.6% ± 1.0 |

### Slates of 2, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 |
| slightly different | 3.2% ± 0.3 | 3.2% ± 0.3 | 3.2% ± 0.3 | 3.2% ± 0.3 | 3.2% ± 0.3 |
| more personalized | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 |
| pushes sponsored | 4.6% ± 0.4 | 4.4% ± 0.4 | 3.9% ± 0.4 | 3.8% ± 0.4 | 3.3% ± 0.2 |
| much greedier | 5.4% ± 0.5 | 4.7% ± 0.5 | 4.7% ± 0.3 | 4.3% ± 0.4 | 4.2% ± 0.4 |

### Slates of 2, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 4.0% ± 0.5 | 4.0% ± 0.5 | 4.0% ± 0.5 | 4.0% ± 0.5 | 4.0% ± 0.5 |
| slightly different | 4.3% ± 0.5 | 4.2% ± 0.5 | 4.3% ± 0.5 | 4.2% ± 0.5 | 4.3% ± 0.5 |
| more personalized | 4.0% ± 0.4 | 4.0% ± 0.4 | 4.0% ± 0.4 | 4.0% ± 0.4 | 4.0% ± 0.4 |
| pushes sponsored | 66.9% ± 24.5 | 26.6% ± 5.5 | 70.5% ± 30.7 | 26.0% ± 6.2 | 48.9% ± 16.0 |
| much greedier | 54.9% ± 23.5 | 18.2% ± 2.5 | 32.6% ± 9.3 | 18.7% ± 3.0 | 30.9% ± 8.8 |

### Slates of 2, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 1.8% ± 0.1 | 1.8% ± 0.1 | 1.8% ± 0.1 | 1.8% ± 0.1 | 1.8% ± 0.1 |
| slightly different | 1.9% ± 0.2 | 1.8% ± 0.2 | 1.9% ± 0.2 | 1.8% ± 0.2 | 1.9% ± 0.2 |
| more personalized | 1.8% ± 0.1 | 1.8% ± 0.1 | 1.8% ± 0.1 | 1.8% ± 0.1 | 1.8% ± 0.1 |
| pushes sponsored | 13.8% ± 1.3 | 12.3% ± 0.9 | 12.4% ± 0.9 | 11.3% ± 0.8 | 13.0% ± 1.0 |
| much greedier | 13.6% ± 2.5 | 11.4% ± 2.5 | 45.2% ± 21.4 | 17.0% ± 6.2 | 45.1% ± 21.5 |

### Slates of 3, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 5.6% ± 0.6 | 5.6% ± 0.6 | 5.6% ± 0.6 | 5.6% ± 0.6 | 5.6% ± 0.6 |
| slightly different | 5.6% ± 0.6 | 5.5% ± 0.6 | 5.6% ± 0.6 | 5.6% ± 0.6 | 5.6% ± 0.6 |
| more personalized | 5.5% ± 0.6 | 5.5% ± 0.6 | 5.5% ± 0.6 | 5.5% ± 0.6 | 5.5% ± 0.6 |
| pushes sponsored | 12.6% ± 1.2 | 11.8% ± 1.1 | 9.4% ± 1.0 | 8.6% ± 0.7 | 8.1% ± 0.7 |
| much greedier | 11.0% ± 1.2 | 9.7% ± 0.9 | 9.1% ± 0.8 | 8.2% ± 0.7 | 7.8% ± 0.8 |

### Slates of 3, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 |
| slightly different | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.5% ± 0.2 | 2.5% ± 0.2 | 2.5% ± 0.2 |
| more personalized | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 |
| pushes sponsored | 6.8% ± 0.9 | 6.1% ± 0.7 | 4.8% ± 0.4 | 4.7% ± 0.4 | 3.1% ± 0.3 |
| much greedier | 5.1% ± 0.6 | 4.2% ± 0.5 | 4.3% ± 0.5 | 4.1% ± 0.4 | 3.5% ± 0.3 |

### Slates of 3, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 3.5% ± 0.4 | 3.5% ± 0.4 | 3.5% ± 0.4 | 3.5% ± 0.4 | 3.5% ± 0.4 |
| slightly different | 3.7% ± 0.4 | 3.6% ± 0.4 | 3.7% ± 0.4 | 3.6% ± 0.4 | 3.7% ± 0.4 |
| more personalized | 3.7% ± 0.4 | 3.7% ± 0.4 | 3.7% ± 0.4 | 3.6% ± 0.4 | 3.7% ± 0.4 |
| pushes sponsored | 34.2% ± 3.5 | 25.0% ± 2.8 | 41.8% ± 8.6 | 23.5% ± 2.4 | 54.0% ± 18.2 |
| much greedier | 35.3% ± 4.2 | 20.4% ± 1.2 | 32.3% ± 5.4 | 19.8% ± 1.6 | 45.8% ± 12.9 |

### Slates of 3, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 1.5% ± 0.2 | 1.5% ± 0.2 | 1.5% ± 0.2 | 1.5% ± 0.2 | 1.5% ± 0.2 |
| slightly different | 1.6% ± 0.2 | 1.6% ± 0.2 | 1.6% ± 0.2 | 1.6% ± 0.2 | 1.6% ± 0.2 |
| more personalized | 1.7% ± 0.2 | 1.7% ± 0.2 | 1.7% ± 0.2 | 1.7% ± 0.2 | 1.7% ± 0.2 |
| pushes sponsored | 25.1% ± 2.6 | 18.9% ± 1.9 | 21.9% ± 2.5 | 16.8% ± 2.3 | 20.9% ± 2.1 |
| much greedier | 22.8% ± 3.7 | 18.1% ± 2.0 | 19.7% ± 2.9 | 15.9% ± 1.8 | 20.1% ± 2.5 |

### Slates of 5, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 4.7% ± 0.5 | 4.7% ± 0.5 | 4.7% ± 0.5 | 4.7% ± 0.5 | 4.7% ± 0.5 |
| slightly different | 4.9% ± 0.6 | 4.8% ± 0.5 | 4.8% ± 0.5 | 4.8% ± 0.5 | 4.9% ± 0.5 |
| more personalized | 4.7% ± 0.5 | 4.7% ± 0.5 | 4.7% ± 0.5 | 4.7% ± 0.5 | 4.7% ± 0.5 |
| pushes sponsored | 21.9% ± 3.3 | 18.6% ± 2.2 | 8.8% ± 0.8 | 8.2% ± 0.8 | 5.4% ± 0.5 |
| much greedier | 15.8% ± 2.7 | 13.1% ± 1.4 | 8.3% ± 0.9 | 7.6% ± 0.8 | 6.4% ± 0.8 |

### Slates of 5, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 |
| slightly different | 2.1% ± 0.2 | 2.1% ± 0.2 | 2.1% ± 0.2 | 2.1% ± 0.2 | 2.1% ± 0.2 |
| more personalized | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 |
| pushes sponsored | 7.4% ± 0.8 | 6.2% ± 0.7 | 4.7% ± 0.6 | 4.5% ± 0.6 | 3.0% ± 0.3 |
| much greedier | 5.8% ± 0.5 | 5.1% ± 0.4 | 4.3% ± 0.4 | 4.0% ± 0.4 | 2.9% ± 0.2 |

### Slates of 5, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 3.0% ± 0.3 | 3.0% ± 0.3 | 3.0% ± 0.3 | 3.0% ± 0.3 | 3.0% ± 0.3 |
| slightly different | 3.3% ± 0.3 | 3.3% ± 0.3 | 3.3% ± 0.3 | 3.2% ± 0.3 | 3.3% ± 0.3 |
| more personalized | 3.8% ± 0.4 | 3.5% ± 0.3 | 3.7% ± 0.4 | 3.5% ± 0.3 | 3.7% ± 0.4 |
| pushes sponsored | 58.2% ± 7.7 | 35.7% ± 2.4 | 43.7% ± 3.9 | 31.6% ± 1.9 | 37.0% ± 2.3 |
| much greedier | 83.5% ± 25.1 | 35.0% ± 3.7 | 49.3% ± 7.3 | 32.0% ± 2.3 | 39.6% ± 4.0 |

### Slates of 5, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.2% ± 0.2 |
| slightly different | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.2% ± 0.2 | 1.2% ± 0.2 |
| more personalized | 1.4% ± 0.2 | 1.3% ± 0.2 | 1.3% ± 0.2 | 1.3% ± 0.2 | 1.4% ± 0.2 |
| pushes sponsored | 49.2% ± 7.9 | 26.0% ± 1.8 | 36.0% ± 3.1 | 24.5% ± 1.6 | 43.8% ± 10.5 |
| much greedier | 35.2% ± 4.2 | 25.4% ± 1.7 | 32.2% ± 4.5 | 24.0% ± 2.1 | 24.7% ± 1.6 |

## Reward bias (average signed error as a share of the true value, ± standard error)

### Slates of 2, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.5% ± 0.9 | -0.5% ± 0.9 | -0.5% ± 0.9 | -0.5% ± 0.9 | -0.5% ± 0.9 |
| slightly different | +0.6% ± 1.0 | +0.5% ± 1.0 | +0.5% ± 1.0 | +0.5% ± 0.9 | +0.5% ± 1.0 |
| more personalized | +0.2% ± 0.9 | +0.2% ± 0.9 | +0.2% ± 0.9 | +0.2% ± 0.9 | +0.2% ± 0.9 |
| pushes sponsored | +0.4% ± 1.5 | +0.8% ± 1.5 | +0.7% ± 1.4 | +0.8% ± 1.4 | +0.9% ± 1.4 |
| much greedier | +0.7% ± 1.5 | +0.8% ± 1.4 | -0.5% ± 1.3 | -0.2% ± 1.2 | +0.5% ± 1.2 |

### Slates of 2, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.5% ± 0.4 | -0.5% ± 0.4 | -0.5% ± 0.4 | -0.5% ± 0.4 | -0.5% ± 0.4 |
| slightly different | +0.4% ± 0.5 | +0.5% ± 0.4 | +0.4% ± 0.4 | +0.5% ± 0.4 | +0.4% ± 0.4 |
| more personalized | +0.2% ± 0.4 | +0.2% ± 0.4 | +0.2% ± 0.4 | +0.2% ± 0.4 | +0.2% ± 0.4 |
| pushes sponsored | -1.2% ± 0.6 | -0.7% ± 0.6 | -0.3% ± 0.6 | -0.2% ± 0.5 | +0.2% ± 0.5 |
| much greedier | +0.4% ± 0.8 | +0.4% ± 0.7 | +0.2% ± 0.7 | +0.3% ± 0.6 | -0.0% ± 0.6 |

### Slates of 2, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +1.1% ± 0.6 | +1.1% ± 0.6 | +1.1% ± 0.6 | +1.1% ± 0.6 | +1.1% ± 0.6 |
| slightly different | +1.4% ± 0.6 | +1.3% ± 0.6 | +1.4% ± 0.6 | +1.3% ± 0.6 | +1.4% ± 0.6 |
| more personalized | +0.7% ± 0.6 | +0.7% ± 0.6 | +0.7% ± 0.6 | +0.7% ± 0.6 | +0.7% ± 0.6 |
| pushes sponsored | +3.6% ± 9.5 | -2.9% ± 3.8 | +3.7% ± 10.1 | -2.8% ± 3.7 | +1.4% ± 7.0 |
| much greedier | +2.2% ± 7.8 | -2.8% ± 2.6 | -0.8% ± 4.7 | -2.4% ± 2.6 | +0.4% ± 4.4 |

### Slates of 2, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.3% ± 0.3 | +0.3% ± 0.3 | +0.3% ± 0.3 | +0.3% ± 0.3 | +0.3% ± 0.3 |
| slightly different | +0.3% ± 0.3 | +0.3% ± 0.3 | +0.3% ± 0.3 | +0.3% ± 0.3 | +0.3% ± 0.3 |
| more personalized | -0.2% ± 0.3 | -0.2% ± 0.3 | -0.2% ± 0.3 | -0.2% ± 0.3 | -0.2% ± 0.3 |
| pushes sponsored | -5.3% ± 1.8 | -6.0% ± 1.5 | -5.7% ± 1.6 | -6.0% ± 1.4 | -4.6% ± 1.7 |
| much greedier | -2.2% ± 1.9 | -1.8% ± 1.6 | +2.2% ± 6.4 | -1.2% ± 2.4 | +2.1% ± 6.4 |

### Slates of 3, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.6% ± 0.8 | +0.6% ± 0.8 | +0.6% ± 0.8 | +0.6% ± 0.8 | +0.6% ± 0.8 |
| slightly different | +0.5% ± 0.8 | +0.6% ± 0.8 | +0.6% ± 0.8 | +0.6% ± 0.8 | +0.6% ± 0.8 |
| more personalized | +0.3% ± 0.8 | +0.3% ± 0.8 | +0.3% ± 0.8 | +0.3% ± 0.8 | +0.3% ± 0.8 |
| pushes sponsored | -0.3% ± 1.8 | -0.6% ± 1.7 | -0.2% ± 1.3 | -0.7% ± 1.2 | +1.3% ± 1.1 |
| much greedier | -0.3% ± 1.6 | -0.4% ± 1.4 | +0.0% ± 1.3 | -0.3% ± 1.2 | +0.1% ± 1.1 |

### Slates of 3, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.2% ± 0.3 | -0.2% ± 0.3 | -0.2% ± 0.3 | -0.2% ± 0.3 | -0.2% ± 0.3 |
| slightly different | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 |
| more personalized | -0.5% ± 0.3 | -0.5% ± 0.3 | -0.5% ± 0.3 | -0.5% ± 0.3 | -0.5% ± 0.3 |
| pushes sponsored | -1.0% ± 1.0 | -0.6% ± 0.9 | -0.6% ± 0.7 | -0.6% ± 0.7 | -0.4% ± 0.4 |
| much greedier | -1.1% ± 0.7 | -1.0% ± 0.6 | -1.3% ± 0.6 | -1.1% ± 0.6 | -1.1% ± 0.5 |

### Slates of 3, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.2% ± 0.5 | +0.2% ± 0.5 | +0.2% ± 0.5 | +0.2% ± 0.5 | +0.2% ± 0.5 |
| slightly different | +0.2% ± 0.5 | +0.2% ± 0.5 | +0.2% ± 0.5 | +0.2% ± 0.5 | +0.2% ± 0.5 |
| more personalized | -0.1% ± 0.5 | -0.2% ± 0.5 | -0.1% ± 0.5 | -0.1% ± 0.5 | -0.0% ± 0.5 |
| pushes sponsored | -10.9% ± 4.6 | -10.3% ± 3.3 | -10.8% ± 5.8 | -10.9% ± 3.0 | -5.8% ± 7.7 |
| much greedier | -6.0% ± 5.0 | -10.1% ± 2.5 | -5.6% ± 4.5 | -8.9% ± 2.5 | +0.1% ± 6.5 |

### Slates of 3, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.2% ± 0.2 |
| slightly different | +0.3% ± 0.2 | +0.2% ± 0.2 | +0.3% ± 0.2 | +0.2% ± 0.2 | +0.3% ± 0.2 |
| more personalized | -0.1% ± 0.2 | -0.1% ± 0.2 | -0.1% ± 0.2 | -0.1% ± 0.2 | -0.0% ± 0.2 |
| pushes sponsored | -8.7% ± 3.4 | -6.3% ± 2.5 | -7.4% ± 2.9 | -5.1% ± 2.3 | -6.8% ± 2.8 |
| much greedier | -1.7% ± 3.2 | -4.5% ± 2.5 | -3.0% ± 2.8 | -4.7% ± 2.2 | -1.2% ± 2.9 |

### Slates of 5, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.6% ± 0.7 | -0.6% ± 0.7 | -0.6% ± 0.7 | -0.6% ± 0.7 | -0.6% ± 0.7 |
| slightly different | -1.0% ± 0.7 | -1.0% ± 0.7 | -1.0% ± 0.7 | -1.0% ± 0.7 | -1.1% ± 0.7 |
| more personalized | -0.6% ± 0.7 | -0.6% ± 0.7 | -0.6% ± 0.7 | -0.6% ± 0.7 | -0.6% ± 0.7 |
| pushes sponsored | -0.2% ± 3.1 | -0.4% ± 2.7 | -2.5% ± 1.2 | -2.1% ± 1.1 | +0.2% ± 0.8 |
| much greedier | -1.2% ± 2.2 | -1.8% ± 1.8 | +0.2% ± 1.2 | -0.2% ± 1.1 | -1.5% ± 0.9 |

### Slates of 5, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.9% ± 0.3 | +0.9% ± 0.3 | +0.9% ± 0.3 | +0.9% ± 0.3 | +0.9% ± 0.3 |
| slightly different | +0.5% ± 0.3 | +0.4% ± 0.3 | +0.5% ± 0.3 | +0.4% ± 0.3 | +0.4% ± 0.3 |
| more personalized | +0.8% ± 0.3 | +0.8% ± 0.3 | +0.8% ± 0.3 | +0.8% ± 0.3 | +0.8% ± 0.3 |
| pushes sponsored | +0.1% ± 1.1 | -0.2% ± 0.9 | +0.9% ± 0.7 | +1.0% ± 0.6 | +0.6% ± 0.4 |
| much greedier | +0.7% ± 0.8 | +0.5% ± 0.7 | +0.9% ± 0.6 | +0.8% ± 0.6 | +0.9% ± 0.4 |

### Slates of 5, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.0% ± 0.4 | -0.0% ± 0.4 | -0.0% ± 0.4 | -0.0% ± 0.4 | -0.0% ± 0.4 |
| slightly different | +0.1% ± 0.5 | -0.0% ± 0.5 | +0.1% ± 0.5 | -0.0% ± 0.5 | +0.0% ± 0.5 |
| more personalized | +0.3% ± 0.5 | +0.2% ± 0.5 | +0.2% ± 0.5 | +0.2% ± 0.5 | +0.3% ± 0.5 |
| pushes sponsored | -24.0% ± 7.6 | -19.5% ± 4.3 | -26.9% ± 4.9 | -18.8% ± 3.6 | -23.3% ± 4.1 |
| much greedier | -9.2% ± 11.9 | -18.8% ± 4.2 | -17.8% ± 6.6 | -17.5% ± 3.8 | -19.8% ± 4.9 |

### Slates of 5, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.4% ± 0.2 | +0.4% ± 0.2 | +0.4% ± 0.2 | +0.4% ± 0.2 | +0.4% ± 0.2 |
| slightly different | +0.3% ± 0.2 | +0.3% ± 0.2 | +0.3% ± 0.2 | +0.3% ± 0.2 | +0.3% ± 0.2 |
| more personalized | +0.6% ± 0.2 | +0.5% ± 0.2 | +0.5% ± 0.2 | +0.5% ± 0.2 | +0.6% ± 0.2 |
| pushes sponsored | -15.9% ± 6.7 | -17.9% ± 2.7 | -18.7% ± 4.4 | -17.7% ± 2.4 | -13.7% ± 5.9 |
| much greedier | -17.5% ± 4.4 | -17.8% ± 2.6 | -16.1% ± 4.0 | -15.7% ± 2.6 | -17.8% ± 2.4 |

## Cost error (RMSE as a share of the true value, ± Monte Carlo standard error)

### Slates of 2, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 |
| slightly different | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 |
| more personalized | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 |
| pushes sponsored | 7.3% ± 1.0 | 3.8% ± 0.5 | 5.7% ± 0.7 | 2.9% ± 0.4 | 4.4% ± 0.4 |
| much greedier | 7.6% ± 0.7 | 7.5% ± 0.7 | 7.2% ± 0.7 | 7.1% ± 0.7 | 6.0% ± 0.6 |

### Slates of 2, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 |
| slightly different | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 |
| more personalized | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 | 2.0% ± 0.3 |
| pushes sponsored | 3.9% ± 0.6 | 2.1% ± 0.3 | 2.9% ± 0.4 | 1.6% ± 0.2 | 2.0% ± 0.3 |
| much greedier | 3.9% ± 0.5 | 3.6% ± 0.4 | 3.6% ± 0.4 | 3.4% ± 0.3 | 3.2% ± 0.3 |

### Slates of 2, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 2.5% ± 0.3 | 2.5% ± 0.3 | 2.5% ± 0.3 | 2.5% ± 0.3 | 2.5% ± 0.3 |
| slightly different | 2.5% ± 0.2 | 2.5% ± 0.2 | 2.5% ± 0.2 | 2.5% ± 0.2 | 2.5% ± 0.2 |
| more personalized | 2.5% ± 0.2 | 2.4% ± 0.2 | 2.5% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 |
| pushes sponsored | 51.3% ± 11.6 | 20.5% ± 1.3 | 53.3% ± 12.8 | 19.3% ± 1.1 | 60.9% ± 15.9 |
| much greedier | 78.6% ± 31.0 | 17.4% ± 1.7 | 77.6% ± 30.7 | 16.8% ± 1.5 | 49.3% ± 14.8 |

### Slates of 2, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 1.4% ± 0.2 | 1.4% ± 0.2 | 1.4% ± 0.2 | 1.4% ± 0.2 | 1.4% ± 0.2 |
| slightly different | 1.3% ± 0.2 | 1.3% ± 0.2 | 1.3% ± 0.2 | 1.3% ± 0.2 | 1.3% ± 0.2 |
| more personalized | 1.3% ± 0.1 | 1.3% ± 0.2 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 |
| pushes sponsored | 30.4% ± 9.1 | 14.7% ± 2.5 | 32.6% ± 9.6 | 14.3% ± 2.2 | 35.0% ± 10.9 |
| much greedier | 15.3% ± 1.9 | 11.4% ± 1.5 | 15.0% ± 2.0 | 11.6% ± 1.8 | 15.6% ± 2.3 |

### Slates of 3, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 |
| slightly different | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 | 4.4% ± 0.4 |
| more personalized | 4.4% ± 0.5 | 4.4% ± 0.5 | 4.4% ± 0.5 | 4.4% ± 0.5 | 4.4% ± 0.5 |
| pushes sponsored | 11.4% ± 1.1 | 5.3% ± 0.5 | 7.6% ± 0.8 | 3.4% ± 0.4 | 4.5% ± 0.5 |
| much greedier | 7.6% ± 0.9 | 6.1% ± 0.5 | 7.2% ± 0.6 | 6.5% ± 0.5 | 5.5% ± 0.5 |

### Slates of 3, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 |
| slightly different | 1.4% ± 0.1 | 1.4% ± 0.1 | 1.4% ± 0.2 | 1.4% ± 0.1 | 1.4% ± 0.1 |
| more personalized | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 |
| pushes sponsored | 4.8% ± 0.4 | 2.5% ± 0.2 | 2.7% ± 0.3 | 1.4% ± 0.1 | 1.3% ± 0.1 |
| much greedier | 3.9% ± 0.4 | 3.0% ± 0.3 | 3.0% ± 0.3 | 2.4% ± 0.2 | 2.1% ± 0.2 |

### Slates of 3, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 | 2.4% ± 0.2 |
| slightly different | 2.3% ± 0.2 | 2.3% ± 0.2 | 2.3% ± 0.2 | 2.3% ± 0.2 | 2.3% ± 0.2 |
| more personalized | 2.6% ± 0.3 | 2.5% ± 0.2 | 2.6% ± 0.3 | 2.5% ± 0.2 | 2.6% ± 0.3 |
| pushes sponsored | 552.1% ± 274.6 | 26.0% ± 1.2 | 483.4% ± 240.0 | 24.4% ± 1.2 | 420.0% ± 207.7 |
| much greedier | 31.1% ± 2.6 | 22.0% ± 1.4 | 32.2% ± 5.7 | 21.7% ± 1.4 | 26.6% ± 2.3 |

### Slates of 3, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 1.0% ± 0.1 | 1.0% ± 0.1 | 1.0% ± 0.1 | 1.0% ± 0.1 | 1.0% ± 0.1 |
| slightly different | 1.1% ± 0.1 | 1.1% ± 0.1 | 1.1% ± 0.1 | 1.1% ± 0.1 | 1.1% ± 0.1 |
| more personalized | 1.0% ± 0.1 | 1.0% ± 0.1 | 1.0% ± 0.1 | 1.0% ± 0.1 | 1.0% ± 0.1 |
| pushes sponsored | 39.2% ± 7.4 | 19.2% ± 1.1 | 43.0% ± 10.6 | 18.0% ± 1.1 | 39.8% ± 9.2 |
| much greedier | 29.1% ± 4.7 | 16.5% ± 1.2 | 30.7% ± 5.3 | 15.8% ± 1.3 | 24.9% ± 4.0 |

### Slates of 5, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 |
| slightly different | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 |
| more personalized | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 | 3.1% ± 0.3 |
| pushes sponsored | 17.0% ± 1.8 | 8.2% ± 1.1 | 7.1% ± 0.7 | 3.2% ± 0.3 | 3.1% ± 0.3 |
| much greedier | 8.9% ± 0.9 | 6.4% ± 0.7 | 5.8% ± 0.7 | 4.9% ± 0.6 | 4.0% ± 0.4 |

### Slates of 5, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 |
| slightly different | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 |
| more personalized | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 | 1.3% ± 0.1 |
| pushes sponsored | 8.8% ± 0.8 | 4.0% ± 0.4 | 3.6% ± 0.3 | 1.6% ± 0.1 | 1.3% ± 0.1 |
| much greedier | 4.1% ± 0.4 | 2.7% ± 0.3 | 2.8% ± 0.3 | 2.5% ± 0.2 | 1.8% ± 0.2 |

### Slates of 5, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 | 2.2% ± 0.2 |
| slightly different | 2.4% ± 0.3 | 2.3% ± 0.3 | 2.4% ± 0.3 | 2.3% ± 0.3 | 2.4% ± 0.3 |
| more personalized | 3.1% ± 0.4 | 2.6% ± 0.3 | 3.0% ± 0.4 | 2.6% ± 0.3 | 2.9% ± 0.4 |
| pushes sponsored | 63.8% ± 8.2 | 41.3% ± 1.5 | 66.6% ± 14.0 | 39.1% ± 1.4 | 64.8% ± 15.3 |
| much greedier | 245.6% ± 118.5 | 34.3% ± 1.8 | 156.9% ± 72.2 | 32.1% ± 1.8 | 227.8% ± 110.2 |

### Slates of 5, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | 0.9% ± 0.1 | 0.9% ± 0.1 | 0.9% ± 0.1 | 0.9% ± 0.1 | 0.9% ± 0.1 |
| slightly different | 1.0% ± 0.1 | 0.9% ± 0.1 | 1.0% ± 0.1 | 0.9% ± 0.1 | 1.0% ± 0.1 |
| more personalized | 1.1% ± 0.1 | 1.0% ± 0.1 | 1.1% ± 0.1 | 1.0% ± 0.1 | 1.0% ± 0.1 |
| pushes sponsored | 50.6% ± 4.9 | 34.4% ± 1.4 | 49.2% ± 6.0 | 32.4% ± 1.4 | 60.3% ± 13.9 |
| much greedier | 34.5% ± 1.7 | 28.6% ± 1.5 | 35.5% ± 2.2 | 28.2% ± 1.4 | 40.0% ± 7.5 |

## Cost bias (average signed error as a share of the true value, ± standard error)

### Slates of 2, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.1% ± 0.6 | -0.1% ± 0.6 | -0.1% ± 0.6 | -0.1% ± 0.6 | -0.1% ± 0.6 |
| slightly different | -0.2% ± 0.6 | -0.2% ± 0.6 | -0.2% ± 0.6 | -0.2% ± 0.6 | -0.2% ± 0.6 |
| more personalized | -0.3% ± 0.6 | -0.3% ± 0.6 | -0.3% ± 0.6 | -0.3% ± 0.6 | -0.3% ± 0.6 |
| pushes sponsored | -0.3% ± 1.0 | -0.1% ± 0.5 | -0.1% ± 0.8 | -0.1% ± 0.4 | -0.2% ± 0.6 |
| much greedier | -0.4% ± 1.1 | -0.2% ± 1.1 | -0.4% ± 1.0 | -0.0% ± 1.0 | -0.4% ± 0.9 |

### Slates of 2, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.1% ± 0.3 | -0.1% ± 0.3 | -0.1% ± 0.3 | -0.1% ± 0.3 | -0.1% ± 0.3 |
| slightly different | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 |
| more personalized | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 | -0.3% ± 0.3 |
| pushes sponsored | -0.7% ± 0.6 | -0.3% ± 0.3 | -0.4% ± 0.4 | -0.2% ± 0.2 | -0.1% ± 0.3 |
| much greedier | -1.1% ± 0.5 | -1.0% ± 0.5 | -0.9% ± 0.5 | -0.8% ± 0.5 | -0.6% ± 0.4 |

### Slates of 2, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.1% ± 0.4 | +0.1% ± 0.4 | +0.1% ± 0.4 | +0.1% ± 0.4 | +0.1% ± 0.4 |
| slightly different | +0.2% ± 0.4 | +0.2% ± 0.4 | +0.2% ± 0.4 | +0.2% ± 0.4 | +0.2% ± 0.4 |
| more personalized | -0.1% ± 0.4 | -0.1% ± 0.3 | -0.1% ± 0.4 | -0.1% ± 0.3 | -0.1% ± 0.3 |
| pushes sponsored | -3.5% ± 7.3 | -11.8% ± 2.4 | -1.3% ± 7.6 | -10.6% ± 2.3 | +2.0% ± 8.7 |
| much greedier | +9.2% ± 11.1 | -3.8% ± 2.4 | +9.5% ± 11.0 | -3.3% ± 2.4 | +4.6% ± 7.0 |

### Slates of 2, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.6% ± 0.2 | +0.6% ± 0.2 | +0.6% ± 0.2 | +0.6% ± 0.2 | +0.6% ± 0.2 |
| slightly different | +0.4% ± 0.2 | +0.5% ± 0.2 | +0.4% ± 0.2 | +0.5% ± 0.2 | +0.4% ± 0.2 |
| more personalized | +0.3% ± 0.2 | +0.3% ± 0.2 | +0.3% ± 0.2 | +0.3% ± 0.2 | +0.3% ± 0.2 |
| pushes sponsored | -1.1% ± 4.3 | -6.0% ± 1.9 | -0.2% ± 4.7 | -6.0% ± 1.8 | +1.0% ± 5.0 |
| much greedier | -3.5% ± 2.1 | -3.4% ± 1.6 | -3.0% ± 2.1 | -2.9% ± 1.6 | -2.2% ± 2.2 |

### Slates of 3, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.6% ± 0.6 | +0.6% ± 0.6 | +0.6% ± 0.6 | +0.6% ± 0.6 | +0.6% ± 0.6 |
| slightly different | +0.3% ± 0.6 | +0.3% ± 0.6 | +0.3% ± 0.6 | +0.3% ± 0.6 | +0.4% ± 0.6 |
| more personalized | +0.4% ± 0.6 | +0.4% ± 0.6 | +0.4% ± 0.6 | +0.4% ± 0.6 | +0.4% ± 0.6 |
| pushes sponsored | +0.7% ± 1.6 | +0.0% ± 0.8 | +0.6% ± 1.1 | +0.1% ± 0.5 | +0.5% ± 0.6 |
| much greedier | +1.7% ± 1.1 | +1.6% ± 0.8 | +2.0% ± 1.0 | +1.8% ± 0.9 | +1.7% ± 0.7 |

### Slates of 3, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.0% ± 0.2 | -0.0% ± 0.2 | -0.0% ± 0.2 | -0.0% ± 0.2 | -0.0% ± 0.2 |
| slightly different | -0.3% ± 0.2 | -0.3% ± 0.2 | -0.3% ± 0.2 | -0.3% ± 0.2 | -0.3% ± 0.2 |
| more personalized | -0.2% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.2 |
| pushes sponsored | -0.9% ± 0.7 | -0.4% ± 0.3 | -0.3% ± 0.4 | -0.2% ± 0.2 | -0.1% ± 0.2 |
| much greedier | -0.4% ± 0.6 | -0.3% ± 0.4 | -0.3% ± 0.4 | -0.1% ± 0.3 | -0.2% ± 0.3 |

### Slates of 3, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.4% ± 0.3 | +0.4% ± 0.3 | +0.4% ± 0.3 | +0.4% ± 0.3 | +0.4% ± 0.3 |
| slightly different | +0.1% ± 0.3 | +0.1% ± 0.3 | +0.1% ± 0.3 | +0.1% ± 0.3 | +0.1% ± 0.3 |
| more personalized | +0.2% ± 0.4 | +0.1% ± 0.4 | +0.2% ± 0.4 | +0.1% ± 0.4 | +0.2% ± 0.4 |
| pushes sponsored | +57.5% ± 78.4 | -21.7% ± 2.0 | +49.4% ± 68.7 | -19.9% ± 2.0 | +44.3% ± 59.7 |
| much greedier | -16.0% ± 3.8 | -17.1% ± 2.0 | -14.8% ± 4.1 | -15.9% ± 2.1 | -15.0% ± 3.1 |

### Slates of 3, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.0% ± 0.1 | +0.0% ± 0.1 | +0.0% ± 0.1 | +0.0% ± 0.1 | +0.0% ± 0.1 |
| slightly different | -0.2% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.1 |
| more personalized | -0.1% ± 0.1 | -0.1% ± 0.1 | -0.1% ± 0.1 | -0.1% ± 0.1 | -0.1% ± 0.1 |
| pushes sponsored | -12.6% ± 5.3 | -16.1% ± 1.5 | -9.9% ± 6.0 | -15.2% ± 1.4 | -9.8% ± 5.5 |
| much greedier | -2.1% ± 4.1 | -7.7% ± 2.1 | -0.5% ± 4.4 | -6.8% ± 2.0 | -1.1% ± 3.6 |

### Slates of 5, sessions up to 1 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.4% ± 0.4 | +0.4% ± 0.4 | +0.4% ± 0.4 | +0.4% ± 0.4 | +0.4% ± 0.4 |
| slightly different | +0.1% ± 0.4 | +0.1% ± 0.4 | +0.1% ± 0.4 | +0.1% ± 0.4 | +0.1% ± 0.4 |
| more personalized | -0.0% ± 0.4 | -0.0% ± 0.4 | -0.0% ± 0.4 | -0.0% ± 0.4 | -0.0% ± 0.4 |
| pushes sponsored | +0.9% ± 2.4 | +0.2% ± 1.2 | -0.6% ± 1.0 | -0.2% ± 0.5 | +0.0% ± 0.4 |
| much greedier | +0.2% ± 1.3 | -0.2% ± 0.9 | +0.5% ± 0.8 | -0.0% ± 0.7 | -0.6% ± 0.6 |

### Slates of 5, sessions up to 1 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 | +0.1% ± 0.2 |
| slightly different | -0.1% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.2 | -0.2% ± 0.2 |
| more personalized | -0.3% ± 0.2 | -0.3% ± 0.2 | -0.3% ± 0.2 | -0.3% ± 0.2 | -0.3% ± 0.2 |
| pushes sponsored | +0.9% ± 1.2 | +0.4% ± 0.6 | +0.1% ± 0.5 | +0.0% ± 0.2 | -0.3% ± 0.2 |
| much greedier | -0.4% ± 0.6 | -0.6% ± 0.4 | -0.4% ± 0.4 | -0.5% ± 0.3 | -0.3% ± 0.2 |

### Slates of 5, sessions up to 20 steps, 1,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | -0.1% ± 0.3 | -0.1% ± 0.3 | -0.1% ± 0.3 | -0.1% ± 0.3 | -0.1% ± 0.3 |
| slightly different | -0.0% ± 0.3 | -0.1% ± 0.3 | -0.0% ± 0.3 | -0.1% ± 0.3 | -0.0% ± 0.3 |
| more personalized | +0.0% ± 0.4 | -0.0% ± 0.4 | -0.0% ± 0.4 | -0.1% ± 0.4 | -0.0% ± 0.4 |
| pushes sponsored | -36.8% ± 7.4 | -39.4% ± 1.8 | -31.6% ± 8.4 | -37.3% ± 1.7 | -29.0% ± 8.3 |
| much greedier | +0.6% ± 35.1 | -30.5% ± 2.3 | -7.1% ± 22.4 | -27.4% ± 2.4 | +4.5% ± 32.5 |

### Slates of 5, sessions up to 20 steps, 5,000 sessions logged

| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS | IndependentIPS |
|---|---:|---:|---:|---:|---:|
| same as logging | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 |
| slightly different | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.1 |
| more personalized | +0.2% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 | +0.2% ± 0.1 |
| pushes sponsored | -29.4% ± 5.9 | -32.9% ± 1.5 | -25.6% ± 6.0 | -30.8% ± 1.5 | -19.4% ± 8.2 |
| much greedier | -29.0% ± 2.7 | -25.5% ± 1.9 | -26.4% ± 3.4 | -23.8% ± 2.2 | -22.8% ± 4.7 |

Finished in 558 s with seed 4004.
