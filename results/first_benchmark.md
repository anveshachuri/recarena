Catalog of 50 items, slates of 3, sessions up to 20 steps. 30 repeats per cell, truth from 2,000,000 simulated sessions.

## True values

| Target policy | Reward | Sponsored exposure | Within budget? |
|---|---:|---:|---|
| same as logging | 0.797 ± 0.001 | 1.465 ± 0.001 | yes |
| slightly different | 0.815 ± 0.001 | 1.460 ± 0.001 | yes |
| more personalized | 0.803 ± 0.001 | 1.471 ± 0.001 | yes |
| pushes sponsored | 0.781 ± 0.001 | 3.983 ± 0.002 | no |
| much greedier | 1.017 ± 0.001 | 1.388 ± 0.001 | yes |

Budget: sponsored exposure of at most 1.832.

## Reward error (RMSE as a share of the true value, lower is better)

| Target policy | Sessions logged | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| same as logging | 200 | 7.2% | 7.2% | 7.2% | 7.2% | 9.4% | 7.3% |
| same as logging | 1,000 | 3.9% | 3.9% | 3.9% | 3.9% | 4.0% | 3.8% |
| same as logging | 5,000 | 1.8% | 1.8% | 1.8% | 1.8% | 1.7% | 1.8% |
| slightly different | 200 | 7.8% | 7.3% | 7.2% | 7.1% | 9.2% | 7.6% |
| slightly different | 1,000 | 4.5% | 4.0% | 4.1% | 3.9% | 4.1% | 3.8% |
| slightly different | 5,000 | 2.1% | 1.9% | 1.9% | 1.8% | 1.8% | 1.8% |
| more personalized | 200 | 9.6% | 8.2% | 7.8% | 7.5% | 9.7% | 7.7% |
| more personalized | 1,000 | 5.6% | 4.8% | 4.3% | 4.1% | 4.3% | 3.9% |
| more personalized | 5,000 | 2.0% | 2.0% | 1.7% | 1.8% | 1.9% | 1.7% |
| pushes sponsored | 200 | 321.2% | 57.0% | 114.8% | 31.3% | 9.9% | 64.6% |
| pushes sponsored | 1,000 | 87.2% | 50.2% | 42.2% | 25.6% | 6.8% | 55.6% |
| pushes sponsored | 5,000 | 127.8% | 35.9% | 44.6% | 27.6% | 3.1% | 59.0% |
| much greedier | 200 | 82.5% | 62.8% | 56.3% | 31.6% | 8.6% | 43.5% |
| much greedier | 1,000 | 63.1% | 46.5% | 41.2% | 21.7% | 4.4% | 43.5% |
| much greedier | 5,000 | 79.3% | 40.5% | 37.5% | 18.7% | 2.6% | 35.6% |

## Reward bias (average signed error)

| Target policy | Sessions logged | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| same as logging | 200 | -1.5% | -1.5% | -1.5% | -1.5% | -6.3% | -1.3% |
| same as logging | 1,000 | -0.4% | -0.4% | -0.4% | -0.4% | -1.5% | -0.5% |
| same as logging | 5,000 | +0.0% | +0.0% | +0.0% | +0.0% | -0.1% | +0.1% |
| slightly different | 200 | -1.5% | -1.4% | -1.6% | -1.4% | -6.3% | -1.2% |
| slightly different | 1,000 | +0.0% | -0.3% | -0.2% | -0.3% | -1.6% | -0.5% |
| slightly different | 5,000 | -0.2% | -0.0% | -0.1% | +0.0% | -0.1% | +0.1% |
| more personalized | 200 | -1.5% | -1.9% | -1.1% | -1.3% | -6.9% | -1.1% |
| more personalized | 1,000 | -0.5% | -0.6% | -0.3% | -0.4% | -2.3% | -0.5% |
| more personalized | 5,000 | -0.1% | -0.1% | -0.0% | -0.0% | -0.7% | +0.1% |
| pushes sponsored | 200 | -1.3% | -37.8% | +3.0% | -10.7% | -1.2% | +10.7% |
| pushes sponsored | 1,000 | -44.7% | -38.0% | -7.6% | -11.4% | +0.2% | -6.9% |
| pushes sponsored | 5,000 | -14.0% | -26.4% | +1.7% | -3.8% | -0.0% | -4.1% |
| much greedier | 200 | -59.3% | -53.8% | -16.6% | -19.8% | -4.7% | -15.5% |
| much greedier | 1,000 | -57.6% | -40.9% | -1.4% | -7.6% | -0.8% | +2.7% |
| much greedier | 5,000 | -23.5% | -25.2% | -6.0% | -8.5% | +1.5% | -2.0% |

## Budget decisions (share of runs that correctly said whether the policy fits the budget)

| Target policy | Sessions logged | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| same as logging | 200 | 100% | 100% | 100% | 100% | 100% | 100% |
| same as logging | 1,000 | 100% | 100% | 100% | 100% | 100% | 100% |
| same as logging | 5,000 | 100% | 100% | 100% | 100% | 100% | 100% |
| slightly different | 200 | 100% | 100% | 100% | 100% | 100% | 100% |
| slightly different | 1,000 | 100% | 100% | 100% | 100% | 100% | 100% |
| slightly different | 5,000 | 100% | 100% | 100% | 100% | 100% | 100% |
| more personalized | 200 | 100% | 100% | 100% | 100% | 100% | 100% |
| more personalized | 1,000 | 100% | 100% | 100% | 100% | 100% | 100% |
| more personalized | 5,000 | 100% | 100% | 100% | 100% | 100% | 100% |
| pushes sponsored | 200 | 17% | 50% | 73% | 97% | 100% | 97% |
| pushes sponsored | 1,000 | 37% | 93% | 97% | 100% | 100% | 97% |
| pushes sponsored | 5,000 | 50% | 100% | 100% | 100% | 100% | 93% |
| much greedier | 200 | 90% | 100% | 93% | 97% | 100% | 93% |
| much greedier | 1,000 | 97% | 100% | 90% | 100% | 100% | 93% |
| much greedier | 5,000 | 87% | 93% | 93% | 100% | 100% | 100% |

Finished in 835 s with seed 4004.
