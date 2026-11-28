Default world, 3 catalogs, 40 logged datasets per catalog, logging policy and size (so 120 per row), sessions of 20 steps. Truth from 300,000 sessions per target and catalog, kept step by step. Its standard error, bounded by adding the per-step ones, is at most 0.58% of the full true value. All errors are pooled over catalogs as shares of each catalog's own true value.

PDIS's term for step t is the mean over sessions of the cumulative weight up to step t times the step's value, and SNPDIS divides the same sum by the sum of the cumulative weights instead of the number of sessions. Each estimates the true mean value at step t, and the terms add up to the full estimate.

## PDIS, reward: signed error of each block of steps, as a share of the full true value

Mean ± standard error. The block errors add up to the full error. Truth in late half: the share of the full true value that steps 11 to 20 hold.

| Logging | Sessions | Target | Truth in late half | Steps 1 to 5 | Steps 6 to 10 | Steps 11 to 15 | Steps 16 to 20 | Full |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| default | 1,000 | same as logging | 9% | +0.0% ± 0.2 | -0.0% ± 0.1 | -0.0% ± 0.1 | -0.0% ± 0.0 | -0.0% ± 0.3 |
| default | 1,000 | slightly different | 9% | +0.1% ± 0.2 | -0.1% ± 0.1 | +0.0% ± 0.1 | -0.0% ± 0.0 | -0.1% ± 0.3 |
| default | 1,000 | more personalized | 10% | +0.2% ± 0.2 | -0.0% ± 0.2 | -0.1% ± 0.1 | -0.0% ± 0.1 | +0.0% ± 0.3 |
| default | 1,000 | pushes sponsored | 9% | -0.6% ± 1.9 | -10.2% ± 1.1 | -5.0% ± 0.5 | -2.0% ± 0.0 | -17.7% ± 2.5 |
| default | 1,000 | much greedier | 9% | +0.3% ± 1.2 | -3.9% ± 2.2 | -2.5% ± 1.8 | -1.9% ± 0.0 | -8.0% ± 3.2 |
| default | 5,000 | same as logging | 9% | +0.0% ± 0.1 | -0.0% ± 0.1 | -0.1% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.1 |
| default | 5,000 | slightly different | 9% | +0.0% ± 0.1 | -0.1% ± 0.1 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default | 5,000 | more personalized | 10% | +0.2% ± 0.1 | +0.0% ± 0.1 | -0.1% ± 0.0 | -0.0% ± 0.0 | +0.0% ± 0.1 |
| default | 5,000 | pushes sponsored | 9% | +0.1% ± 1.4 | +5.5% ± 8.6 | +0.8% ± 3.2 | -1.6% ± 0.2 | +4.8% ± 9.2 |
| default | 5,000 | much greedier | 9% | +0.3% ± 0.6 | -3.1% ± 1.1 | -3.1% ± 1.0 | +11.9% ± 13.5 | +5.9% ± 13.4 |
| default | 20,000 | same as logging | 9% | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.1 |
| default | 20,000 | slightly different | 9% | +0.0% ± 0.0 | -0.1% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default | 20,000 | more personalized | 10% | +0.2% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default | 20,000 | pushes sponsored | 9% | -0.4% ± 0.5 | -1.4% ± 1.4 | -3.0% ± 0.6 | -1.8% ± 0.1 | -6.6% ± 1.7 |
| default | 20,000 | much greedier | 9% | +0.0% ± 0.4 | -2.3% ± 1.1 | -0.1% ± 1.6 | -1.0% ± 0.5 | -3.4% ± 2.0 |
| default + 10% uniform | 1,000 | same as logging | 9% | +0.0% ± 0.2 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.0 | +0.3% ± 0.3 |
| default + 10% uniform | 1,000 | slightly different | 9% | +0.0% ± 0.2 | +0.1% ± 0.2 | +0.2% ± 0.1 | +0.1% ± 0.1 | +0.4% ± 0.3 |
| default + 10% uniform | 1,000 | more personalized | 10% | +0.2% ± 0.2 | +0.2% ± 0.2 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.5% ± 0.3 |
| default + 10% uniform | 1,000 | pushes sponsored | 9% | +0.6% ± 1.8 | +2.1% ± 6.7 | -5.2% ± 0.6 | -1.7% ± 0.2 | -4.2% ± 7.4 |
| default + 10% uniform | 1,000 | much greedier | 9% | -1.0% ± 1.3 | -1.3% ± 3.4 | -0.1% ± 2.3 | -1.9% ± 0.0 | -4.2% ± 5.7 |
| default + 10% uniform | 5,000 | same as logging | 9% | +0.1% ± 0.1 | +0.1% ± 0.1 | -0.0% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default + 10% uniform | 5,000 | slightly different | 9% | +0.1% ± 0.1 | -0.0% ± 0.1 | +0.0% ± 0.0 | -0.0% ± 0.0 | +0.0% ± 0.1 |
| default + 10% uniform | 5,000 | more personalized | 10% | +0.2% ± 0.1 | +0.0% ± 0.1 | -0.1% ± 0.0 | -0.1% ± 0.0 | +0.1% ± 0.2 |
| default + 10% uniform | 5,000 | pushes sponsored | 9% | -0.2% ± 1.1 | +33.3% ± 37.4 | -0.6% ± 2.0 | -1.7% ± 0.3 | +30.8% ± 38.1 |
| default + 10% uniform | 5,000 | much greedier | 9% | -1.5% ± 0.5 | +1.6% ± 4.8 | -2.8% ± 1.6 | -1.6% ± 0.1 | -4.4% ± 5.2 |
| default + 10% uniform | 20,000 | same as logging | 9% | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default + 10% uniform | 20,000 | slightly different | 9% | -0.0% ± 0.0 | -0.1% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default + 10% uniform | 20,000 | more personalized | 10% | +0.1% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.0 | -0.0% ± 0.0 | +0.0% ± 0.1 |
| default + 10% uniform | 20,000 | pushes sponsored | 9% | +0.8% ± 0.6 | +1.0% ± 2.3 | -3.0% ± 0.8 | +12.8% ± 13.3 | +11.6% ± 13.9 |
| default + 10% uniform | 20,000 | much greedier | 9% | -0.4% ± 0.3 | -3.1% ± 0.8 | -2.3% ± 1.0 | -0.5% ± 0.7 | -6.3% ± 1.7 |

## SNPDIS, reward: signed error of each block of steps, as a share of the full true value

Mean ± standard error. The block errors add up to the full error. Truth in late half: the share of the full true value that steps 11 to 20 hold.

| Logging | Sessions | Target | Truth in late half | Steps 1 to 5 | Steps 6 to 10 | Steps 11 to 15 | Steps 16 to 20 | Full |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| default | 1,000 | same as logging | 9% | +0.0% ± 0.2 | -0.0% ± 0.1 | -0.0% ± 0.1 | -0.0% ± 0.0 | -0.0% ± 0.3 |
| default | 1,000 | slightly different | 9% | +0.1% ± 0.2 | -0.1% ± 0.1 | +0.0% ± 0.1 | -0.0% ± 0.0 | -0.0% ± 0.3 |
| default | 1,000 | more personalized | 10% | +0.2% ± 0.2 | -0.1% ± 0.1 | -0.1% ± 0.1 | -0.0% ± 0.1 | -0.0% ± 0.3 |
| default | 1,000 | pushes sponsored | 9% | -0.5% ± 1.2 | -7.1% ± 1.0 | -4.1% ± 0.6 | -1.9% ± 0.1 | -13.5% ± 1.8 |
| default | 1,000 | much greedier | 9% | -0.1% ± 0.9 | -4.2% ± 1.3 | -3.0% ± 0.9 | -1.9% ± 0.1 | -9.2% ± 1.8 |
| default | 5,000 | same as logging | 9% | +0.0% ± 0.1 | -0.0% ± 0.1 | -0.1% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.1 |
| default | 5,000 | slightly different | 9% | +0.0% ± 0.1 | -0.1% ± 0.1 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default | 5,000 | more personalized | 10% | +0.1% ± 0.1 | +0.0% ± 0.1 | -0.1% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default | 5,000 | pushes sponsored | 9% | -0.4% ± 0.7 | -2.0% ± 1.4 | -1.7% ± 1.4 | -1.5% ± 0.3 | -5.6% ± 2.1 |
| default | 5,000 | much greedier | 9% | -0.1% ± 0.5 | -2.8% ± 0.9 | -3.5% ± 0.5 | -0.4% ± 1.1 | -6.9% ± 1.6 |
| default | 20,000 | same as logging | 9% | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.1 |
| default | 20,000 | slightly different | 9% | +0.0% ± 0.0 | -0.1% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.1 |
| default | 20,000 | more personalized | 10% | +0.2% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default | 20,000 | pushes sponsored | 9% | -0.6% ± 0.3 | -1.1% ± 1.1 | -2.7% ± 0.5 | -1.8% ± 0.1 | -6.2% ± 1.3 |
| default | 20,000 | much greedier | 9% | +0.1% ± 0.3 | -2.6% ± 0.8 | -1.5% ± 0.8 | -1.0% ± 0.4 | -5.1% ± 1.2 |
| default + 10% uniform | 1,000 | same as logging | 9% | +0.0% ± 0.2 | +0.1% ± 0.1 | +0.1% ± 0.1 | +0.1% ± 0.0 | +0.3% ± 0.3 |
| default + 10% uniform | 1,000 | slightly different | 9% | +0.0% ± 0.2 | +0.1% ± 0.1 | +0.2% ± 0.1 | +0.1% ± 0.1 | +0.4% ± 0.3 |
| default + 10% uniform | 1,000 | more personalized | 10% | +0.1% ± 0.2 | +0.2% ± 0.2 | +0.1% ± 0.1 | +0.0% ± 0.1 | +0.5% ± 0.3 |
| default + 10% uniform | 1,000 | pushes sponsored | 9% | +1.2% ± 1.3 | -3.2% ± 2.1 | -4.1% ± 0.8 | -1.5% ± 0.3 | -7.7% ± 3.2 |
| default + 10% uniform | 1,000 | much greedier | 9% | -1.4% ± 1.0 | -3.7% ± 1.2 | -1.5% ± 1.0 | -1.8% ± 0.1 | -8.5% ± 2.2 |
| default + 10% uniform | 5,000 | same as logging | 9% | +0.1% ± 0.1 | +0.1% ± 0.1 | -0.0% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default + 10% uniform | 5,000 | slightly different | 9% | +0.1% ± 0.1 | -0.0% ± 0.1 | +0.0% ± 0.0 | -0.0% ± 0.0 | +0.0% ± 0.1 |
| default + 10% uniform | 5,000 | more personalized | 10% | +0.2% ± 0.1 | +0.0% ± 0.1 | -0.0% ± 0.0 | -0.1% ± 0.0 | +0.1% ± 0.2 |
| default + 10% uniform | 5,000 | pushes sponsored | 9% | -0.2% ± 0.7 | -3.0% ± 1.4 | -1.5% ± 1.0 | -1.7% ± 0.3 | -6.4% ± 2.2 |
| default + 10% uniform | 5,000 | much greedier | 9% | -1.2% ± 0.4 | -3.1% ± 1.0 | -3.8% ± 0.7 | -1.4% ± 0.2 | -9.5% ± 1.4 |
| default + 10% uniform | 20,000 | same as logging | 9% | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default + 10% uniform | 20,000 | slightly different | 9% | -0.0% ± 0.0 | -0.1% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default + 10% uniform | 20,000 | more personalized | 10% | +0.1% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.0 | -0.0% ± 0.0 | +0.0% ± 0.1 |
| default + 10% uniform | 20,000 | pushes sponsored | 9% | +0.7% ± 0.4 | -0.6% ± 1.2 | -2.6% ± 0.6 | +0.0% ± 1.3 | -2.6% ± 2.2 |
| default + 10% uniform | 20,000 | much greedier | 9% | -0.3% ± 0.3 | -2.5% ± 0.7 | -2.2% ± 0.7 | -0.7% ± 0.5 | -5.7% ± 1.3 |

## PDIS, cost: signed error of each block of steps, as a share of the full true value

Mean ± standard error. The block errors add up to the full error. Truth in late half: the share of the full true value that steps 11 to 20 hold.

| Logging | Sessions | Target | Truth in late half | Steps 1 to 5 | Steps 6 to 10 | Steps 11 to 15 | Steps 16 to 20 | Full |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| default | 5,000 | same as logging | 18% | -0.0% ± 0.0 | -0.1% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.2% ± 0.1 |
| default | 5,000 | slightly different | 18% | -0.1% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.2% ± 0.1 |
| default | 5,000 | more personalized | 18% | -0.1% ± 0.0 | -0.1% ± 0.1 | -0.0% ± 0.1 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default | 5,000 | pushes sponsored | 17% | +1.2% ± 1.5 | +2.7% ± 4.6 | +6.9% ± 9.3 | -3.2% ± 0.5 | +7.7% ± 13.0 |
| default | 5,000 | much greedier | 17% | +0.5% ± 0.5 | -1.1% ± 1.6 | +0.2% ± 2.7 | -1.8% ± 1.4 | -2.2% ± 4.1 |
| default + 10% uniform | 5,000 | same as logging | 18% | +0.1% ± 0.0 | +0.1% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default + 10% uniform | 5,000 | slightly different | 18% | +0.0% ± 0.0 | +0.1% ± 0.1 | -0.0% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default + 10% uniform | 5,000 | more personalized | 18% | +0.0% ± 0.0 | +0.0% ± 0.1 | -0.0% ± 0.0 | -0.1% ± 0.0 | -0.0% ± 0.1 |
| default + 10% uniform | 5,000 | pushes sponsored | 17% | -0.6% ± 0.7 | +10.5% ± 9.8 | +10.5% ± 14.3 | -3.5% ± 0.4 | +16.8% ± 18.9 |
| default + 10% uniform | 5,000 | much greedier | 17% | -0.1% ± 0.5 | -2.1% ± 2.0 | +1.8% ± 7.7 | -2.5% ± 1.1 | -2.8% ± 8.6 |

## SNPDIS, cost: signed error of each block of steps, as a share of the full true value

Mean ± standard error. The block errors add up to the full error. Truth in late half: the share of the full true value that steps 11 to 20 hold.

| Logging | Sessions | Target | Truth in late half | Steps 1 to 5 | Steps 6 to 10 | Steps 11 to 15 | Steps 16 to 20 | Full |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| default | 5,000 | same as logging | 18% | -0.0% ± 0.0 | -0.1% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.2% ± 0.1 |
| default | 5,000 | slightly different | 18% | -0.1% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | -0.2% ± 0.1 |
| default | 5,000 | more personalized | 18% | -0.1% ± 0.0 | -0.0% ± 0.0 | +0.0% ± 0.0 | -0.0% ± 0.0 | -0.1% ± 0.1 |
| default | 5,000 | pushes sponsored | 17% | -0.6% ± 0.3 | -4.9% ± 0.8 | -6.3% ± 0.7 | -3.4% ± 0.3 | -15.2% ± 1.3 |
| default | 5,000 | much greedier | 17% | -0.1% ± 0.3 | -1.9% ± 0.8 | -2.9% ± 1.1 | -2.8% ± 0.4 | -7.6% ± 1.6 |
| default + 10% uniform | 5,000 | same as logging | 18% | +0.1% ± 0.0 | +0.1% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default + 10% uniform | 5,000 | slightly different | 18% | +0.0% ± 0.0 | +0.1% ± 0.0 | -0.0% ± 0.0 | -0.0% ± 0.0 | +0.1% ± 0.1 |
| default + 10% uniform | 5,000 | more personalized | 18% | +0.0% ± 0.0 | +0.1% ± 0.1 | -0.0% ± 0.0 | -0.1% ± 0.0 | +0.0% ± 0.1 |
| default + 10% uniform | 5,000 | pushes sponsored | 17% | -1.0% ± 0.2 | -4.9% ± 0.7 | -5.8% ± 0.6 | -3.5% ± 0.2 | -15.3% ± 1.4 |
| default + 10% uniform | 5,000 | much greedier | 17% | +0.2% ± 0.3 | -2.8% ± 0.9 | -5.8% ± 0.8 | -3.2% ± 0.3 | -11.6% ± 1.5 |

## Where the reward error takes off, and where the weight mass drops

Error takes off: the first step whose own term has a relative RMSE above 20% of that step's true value. Weight drop: the first step where the median (over datasets) of the step mean cumulative weight from #24 is below 0.9. Its expectation is 1 at every step.

| Logging | Sessions | Target | PDIS error takes off | SNPDIS error takes off | Weight drop | Median step mean weight at step 20 |
|---|---:|---|---:|---:|---:|---:|
| default | 1,000 | same as logging | 12 | 12 | never | 1.000 |
| default | 1,000 | slightly different | 12 | 12 | never | 1.002 |
| default | 1,000 | more personalized | 11 | 11 | never | 0.999 |
| default | 1,000 | pushes sponsored | 2 | 2 | 4 | 0.576 |
| default | 1,000 | much greedier | 3 | 3 | 5 | 0.656 |
| default | 5,000 | same as logging | 18 | 18 | never | 1.000 |
| default | 5,000 | slightly different | 18 | 18 | never | 1.000 |
| default | 5,000 | more personalized | 17 | 17 | never | 0.999 |
| default | 5,000 | pushes sponsored | 3 | 3 | 6 | 0.681 |
| default | 5,000 | much greedier | 4 | 4 | 8 | 0.724 |
| default | 20,000 | same as logging | never | never | never | 1.000 |
| default | 20,000 | slightly different | never | never | never | 1.000 |
| default | 20,000 | more personalized | 15 | 15 | never | 1.000 |
| default | 20,000 | pushes sponsored | 4 | 5 | 7 | 0.729 |
| default | 20,000 | much greedier | 5 | 5 | 9 | 0.799 |
| default + 10% uniform | 1,000 | same as logging | 12 | 12 | never | 1.000 |
| default + 10% uniform | 1,000 | slightly different | 11 | 11 | never | 1.000 |
| default + 10% uniform | 1,000 | more personalized | 10 | 10 | never | 1.000 |
| default + 10% uniform | 1,000 | pushes sponsored | 2 | 2 | 4 | 0.515 |
| default + 10% uniform | 1,000 | much greedier | 2 | 3 | 5 | 0.545 |
| default + 10% uniform | 5,000 | same as logging | 19 | 19 | never | 1.000 |
| default + 10% uniform | 5,000 | slightly different | 17 | 17 | never | 0.999 |
| default + 10% uniform | 5,000 | more personalized | 17 | 17 | never | 0.998 |
| default + 10% uniform | 5,000 | pushes sponsored | 3 | 3 | 6 | 0.644 |
| default + 10% uniform | 5,000 | much greedier | 4 | 4 | 6 | 0.661 |
| default + 10% uniform | 20,000 | same as logging | never | never | never | 1.000 |
| default + 10% uniform | 20,000 | slightly different | never | never | never | 1.000 |
| default + 10% uniform | 20,000 | more personalized | never | never | never | 1.000 |
| default + 10% uniform | 20,000 | pushes sponsored | 4 | 4 | 8 | 0.685 |
| default + 10% uniform | 20,000 | much greedier | 5 | 5 | 9 | 0.767 |

## Step by step reward error for pushes sponsored (default logging, 5,000 sessions)

Each step's term against that step's true value: mean relative error ± standard error / relative RMSE. Truth: the step's mean true value, averaged over catalogs.

| Step | Truth | PDIS | SNPDIS | Median step mean weight |
|---:|---:|---|---|---:|
| 1 | 0.1541 | +0.2% ± 0.5 / 5.4% | +0.4% ± 0.4 / 4.8% | 0.997 |
| 2 | 0.1300 | +1.0% ± 1.5 / 16.2% | +0.8% ± 1.1 / 12.3% | 0.997 |
| 3 | 0.1070 | +3.6% ± 3.3 / 36.5% | +3.3% ± 2.7 / 29.3% | 0.981 |
| 4 | 0.0879 | -1.5% ± 4.7 / 51.2% | -2.3% ± 3.4 / 37.4% | 0.971 |
| 5 | 0.0712 | -4.1% ± 12.5 / 136.7% | -8.7% ± 5.7 / 63.2% | 0.914 |
| 6 | 0.0575 | -8.6% ± 6.5 / 71.4% | -4.0% ± 6.0 / 65.8% | 0.873 |
| 7 | 0.0458 | -25.7% ± 6.4 / 73.9% | -20.4% ± 5.8 / 66.6% | 0.837 |
| 8 | 0.0362 | -10.7% ± 16.7 / 182.4% | -9.0% ± 11.9 / 129.6% | 0.823 |
| 9 | 0.0290 | -12.0% ± 17.3 / 189.5% | -14.7% ± 12.9 / 141.3% | 0.798 |
| 10 | 0.0228 | +299.6% ± 300.8 / 3295.5% | +12.9% ± 29.9 / 325.9% | 0.786 |
| 11 | 0.0180 | +70.9% ± 105.3 / 1151.0% | -5.9% ± 28.7 / 313.7% | 0.757 |
| 12 | 0.0140 | -48.5% ± 18.9 / 211.9% | -37.4% ± 19.7 / 218.4% | 0.742 |
| 13 | 0.0111 | -35.0% ± 21.5 / 237.5% | -34.7% ± 20.4 / 225.7% | 0.726 |
| 14 | 0.0088 | +128.2% ± 173.3 / 1894.7% | +28.4% ± 77.7 / 848.2% | 0.703 |
| 15 | 0.0069 | -87.1% ± 5.3 / 104.3% | -82.3% ± 6.6 / 109.2% | 0.707 |
| 16 | 0.0053 | -56.1% ± 26.4 / 293.8% | -53.7% ± 28.4 / 314.6% | 0.700 |
| 17 | 0.0041 | -74.7% ± 22.4 / 255.4% | -61.3% ± 35.2 / 389.1% | 0.698 |
| 18 | 0.0033 | -86.9% ± 8.2 / 124.7% | -82.9% ± 11.7 / 151.8% | 0.681 |
| 19 | 0.0026 | -98.6% ± 0.6 / 98.8% | -97.6% ± 1.1 / 98.4% | 0.687 |
| 20 | 0.0019 | -92.2% ± 4.9 / 106.6% | -90.1% ± 6.2 / 112.9% | 0.681 |

## Step by step reward error for much greedier (default logging, 5,000 sessions)

Each step's term against that step's true value: mean relative error ± standard error / relative RMSE. Truth: the step's mean true value, averaged over catalogs.

| Step | Truth | PDIS | SNPDIS | Median step mean weight |
|---:|---:|---|---|---:|
| 1 | 0.2049 | +0.9% ± 0.4 / 4.7% | +0.4% ± 0.4 / 4.1% | 1.003 |
| 2 | 0.1721 | +1.7% ± 0.9 / 10.1% | +1.3% ± 0.8 / 9.0% | 1.004 |
| 3 | 0.1427 | +0.2% ± 1.8 / 19.7% | -1.1% ± 1.5 / 16.6% | 1.001 |
| 4 | 0.1163 | +1.9% ± 3.1 / 34.3% | +0.8% ± 2.4 / 26.5% | 0.996 |
| 5 | 0.0942 | -4.4% ± 3.7 / 40.5% | -4.3% ± 3.7 / 40.5% | 0.971 |
| 6 | 0.0758 | -1.1% ± 6.8 / 74.5% | -2.5% ± 5.5 / 59.8% | 0.958 |
| 7 | 0.0605 | -24.1% ± 4.9 / 58.8% | -20.5% ± 4.6 / 54.1% | 0.902 |
| 8 | 0.0480 | -9.7% ± 10.5 / 114.9% | -5.0% ± 9.1 / 99.8% | 0.886 |
| 9 | 0.0376 | -13.1% ± 17.5 / 190.9% | -14.1% ± 11.7 / 128.9% | 0.859 |
| 10 | 0.0299 | -29.7% ± 12.8 / 142.3% | -28.0% ± 11.4 / 127.5% | 0.834 |
| 11 | 0.0236 | -42.8% ± 10.9 / 126.8% | -41.7% ± 9.0 / 106.2% | 0.828 |
| 12 | 0.0184 | -2.0% ± 56.2 / 613.0% | -36.7% ± 20.0 / 221.6% | 0.796 |
| 13 | 0.0145 | -64.2% ± 11.8 / 143.7% | -62.9% ± 10.6 / 131.3% | 0.766 |
| 14 | 0.0114 | -61.3% ± 9.8 / 123.0% | -56.5% ± 10.7 / 130.1% | 0.771 |
| 15 | 0.0087 | -76.3% ± 7.3 / 110.2% | -71.3% ± 8.0 / 112.5% | 0.752 |
| 16 | 0.0069 | -79.2% ± 5.6 / 99.7% | -75.6% ± 5.7 / 97.9% | 0.745 |
| 17 | 0.0053 | -80.5% ± 10.6 / 141.2% | -71.7% ± 15.7 / 185.5% | 0.741 |
| 18 | 0.0042 | -86.8% ± 5.3 / 104.6% | -80.2% ± 8.1 / 119.6% | 0.743 |
| 19 | 0.0032 | +1032.6% ± 1095.9 / 11999.3% | +92.5% ± 148.8 / 1626.1% | 0.746 |
| 20 | 0.0024 | +4227.5% ± 4320.7 / 47322.2% | +185.4% ± 276.5 / 3021.9% | 0.724 |

## Discounting against truncation (reward, far targets)

Each variant is scored against its own true value: mean relative error ± standard error / relative RMSE. Truncated variants count only the first k steps, and IPS and SNIPS then use the weight of those steps alone. Discounting leaves IPS and SNIPS with the whole session weight.

| Logging | Sessions | Target | Value | IPS | SNIPS | PDIS | SNPDIS |
|---|---:|---|---|---|---|---|---|
| default | 1,000 | pushes sponsored | full | -52.3% ± 5.1 / 76.1% | -36.3% ± 3.1 / 50.0% | -17.7% ± 2.5 / 32.7% | -13.5% ± 1.8 / 24.3% |
| default | 1,000 | pushes sponsored | gamma 0.9 | -46.6% ± 5.4 / 75.3% | -28.0% ± 3.3 / 45.8% | -10.1% ± 2.2 / 26.2% | -7.3% ± 1.5 / 18.2% |
| default | 1,000 | pushes sponsored | gamma 0.7 | -40.7% ± 5.5 / 72.7% | -18.1% ± 3.6 / 43.3% | -2.6% ± 1.6 / 17.5% | -1.4% ± 1.2 / 12.8% |
| default | 1,000 | pushes sponsored | first 10 steps | -34.1% ± 6.0 / 73.5% | -20.1% ± 3.3 / 41.3% | -11.8% ± 2.7 / 31.5% | -8.4% ± 1.8 / 21.6% |
| default | 1,000 | pushes sponsored | first 5 steps | -11.9% ± 5.1 / 56.4% | -6.8% ± 2.7 / 30.4% | -0.8% ± 2.9 / 31.5% | -0.7% ± 1.7 / 18.8% |
| default | 1,000 | much greedier | full | -24.7% ± 14.9 / 164.3% | -31.3% ± 3.0 / 45.3% | -8.0% ± 3.2 / 35.7% | -9.2% ± 1.8 / 22.0% |
| default | 1,000 | much greedier | gamma 0.9 | -14.6% ± 16.7 / 183.2% | -22.5% ± 3.0 / 39.9% | -3.3% ± 2.3 / 25.7% | -4.3% ± 1.3 / 15.2% |
| default | 1,000 | much greedier | gamma 0.7 | -2.9% ± 18.8 / 205.3% | -11.4% ± 3.3 / 37.9% | +0.3% ± 1.3 / 14.6% | -0.3% ± 0.9 / 9.7% |
| default | 1,000 | much greedier | first 10 steps | -13.5% ± 11.6 / 127.6% | -17.5% ± 2.9 / 36.5% | -4.0% ± 2.8 / 31.3% | -4.7% ± 1.6 / 18.4% |
| default | 1,000 | much greedier | first 5 steps | +11.8% ± 12.9 / 141.2% | -1.1% ± 2.1 / 22.8% | +0.4% ± 1.7 / 19.1% | -0.1% ± 1.3 / 14.2% |
| default | 5,000 | pushes sponsored | full | -6.9% ± 18.8 / 204.7% | -23.3% ± 3.6 / 45.5% | +4.8% ± 9.2 / 101.0% | -5.6% ± 2.1 / 23.5% |
| default | 5,000 | pushes sponsored | gamma 0.9 | -0.1% ± 19.9 / 217.5% | -16.6% ± 3.2 / 38.5% | +2.8% ± 5.1 / 55.5% | -2.7% ± 1.3 / 14.3% |
| default | 5,000 | pushes sponsored | gamma 0.7 | +10.8% ± 25.0 / 273.0% | -8.2% ± 3.4 / 38.4% | +0.6% ± 1.4 / 14.8% | -0.3% ± 0.7 / 7.5% |
| default | 5,000 | pushes sponsored | first 10 steps | +25.1% ± 27.2 / 297.4% | -9.3% ± 3.2 / 36.3% | +6.2% ± 9.6 / 105.0% | -2.6% ± 1.7 / 19.1% |
| default | 5,000 | pushes sponsored | first 5 steps | +7.0% ± 7.5 / 82.0% | +0.0% ± 2.2 / 23.7% | +0.2% ± 2.1 / 23.0% | -0.5% ± 1.1 / 11.7% |
| default | 5,000 | much greedier | full | -9.8% ± 25.1 / 274.3% | -27.6% ± 2.5 / 38.5% | +5.9% ± 13.4 / 146.8% | -6.9% ± 1.6 / 18.4% |
| default | 5,000 | much greedier | gamma 0.9 | -19.0% ± 11.5 / 126.4% | -21.1% ± 2.4 / 33.3% | -0.6% ± 2.8 / 30.3% | -3.5% ± 0.9 / 10.2% |
| default | 5,000 | much greedier | gamma 0.7 | -18.8% ± 8.5 / 94.6% | -12.5% ± 2.6 / 31.5% | +0.1% ± 0.7 / 7.2% | -0.5% ± 0.5 / 5.4% |
| default | 5,000 | much greedier | first 10 steps | +4.8% ± 18.2 / 198.8% | -12.4% ± 2.6 / 31.3% | -3.1% ± 1.5 / 16.2% | -3.2% ± 1.2 / 13.2% |
| default | 5,000 | much greedier | first 5 steps | +2.5% ± 2.6 / 28.5% | +0.4% ± 1.6 / 17.1% | +0.4% ± 0.9 / 9.9% | -0.2% ± 0.8 / 8.2% |
| default | 20,000 | pushes sponsored | full | -31.6% ± 4.6 / 59.1% | -23.4% ± 2.5 / 35.6% | -6.6% ± 1.7 / 19.8% | -6.2% ± 1.3 / 15.1% |
| default | 20,000 | pushes sponsored | gamma 0.9 | -26.7% ± 4.7 / 57.7% | -17.4% ± 2.2 / 29.2% | -2.9% ± 1.2 / 13.6% | -2.8% ± 0.8 / 9.6% |
| default | 20,000 | pushes sponsored | gamma 0.7 | -22.1% ± 4.8 / 56.5% | -10.8% ± 2.1 / 25.5% | -0.6% ± 0.6 / 6.4% | -0.7% ± 0.4 / 4.0% |
| default | 20,000 | pushes sponsored | first 10 steps | -10.6% ± 5.2 / 57.3% | -9.6% ± 2.1 / 25.0% | -2.0% ± 1.8 / 20.0% | -1.9% ± 1.3 / 14.3% |
| default | 20,000 | pushes sponsored | first 5 steps | +0.2% ± 3.1 / 33.7% | -1.5% ± 1.2 / 13.5% | -0.6% ± 0.8 / 8.7% | -0.9% ± 0.5 / 5.7% |
| default | 20,000 | much greedier | full | -19.1% ± 7.1 / 79.3% | -21.4% ± 2.5 / 35.0% | -3.4% ± 2.0 / 22.2% | -5.1% ± 1.2 / 14.0% |
| default | 20,000 | much greedier | gamma 0.9 | -16.2% ± 5.9 / 66.0% | -16.2% ± 2.3 / 30.2% | -2.0% ± 1.0 / 11.0% | -2.6% ± 0.7 / 7.8% |
| default | 20,000 | much greedier | gamma 0.7 | -12.3% ± 5.6 / 61.8% | -9.9% ± 2.6 / 30.1% | -0.6% ± 0.4 / 4.1% | -0.6% ± 0.3 / 3.3% |
| default | 20,000 | much greedier | first 10 steps | -4.7% ± 4.6 / 50.1% | -7.4% ± 2.2 / 25.1% | -2.6% ± 1.2 / 13.9% | -2.8% ± 0.9 / 10.5% |
| default | 20,000 | much greedier | first 5 steps | +1.9% ± 2.3 / 25.7% | +1.2% ± 1.2 / 12.8% | +0.0% ± 0.6 / 6.5% | +0.1% ± 0.5 / 5.5% |
| default + 10% uniform | 1,000 | pushes sponsored | full | -31.0% ± 20.7 / 228.4% | -36.7% ± 3.0 / 49.0% | -4.2% ± 7.4 / 80.6% | -7.7% ± 3.2 / 35.6% |
| default + 10% uniform | 1,000 | pushes sponsored | gamma 0.9 | -26.5% ± 19.6 / 215.1% | -29.2% ± 3.1 / 44.5% | -0.7% ± 5.1 / 56.1% | -3.1% ± 2.4 / 26.2% |
| default + 10% uniform | 1,000 | pushes sponsored | gamma 0.7 | -27.5% ± 13.9 / 154.1% | -20.3% ± 3.3 / 40.9% | +0.4% ± 2.2 / 24.0% | -0.1% ± 1.4 / 15.2% |
| default + 10% uniform | 1,000 | pushes sponsored | first 10 steps | -0.5% ± 23.5 / 256.3% | -18.2% ± 3.7 / 44.0% | +3.0% ± 7.9 / 86.5% | -2.3% ± 3.1 / 34.2% |
| default + 10% uniform | 1,000 | pushes sponsored | first 5 steps | +8.9% ± 12.3 / 134.7% | -0.6% ± 3.2 / 34.9% | +0.9% ± 2.7 / 29.7% | +1.8% ± 1.9 / 20.9% |
| default + 10% uniform | 1,000 | much greedier | full | -31.6% ± 12.0 / 134.6% | -37.5% ± 3.6 / 54.0% | -4.2% ± 5.7 / 62.4% | -8.5% ± 2.2 / 25.6% |
| default + 10% uniform | 1,000 | much greedier | gamma 0.9 | -32.9% ± 10.7 / 121.3% | -33.0% ± 3.3 / 48.6% | -2.2% ± 3.6 / 39.0% | -5.0% ± 1.6 / 18.2% |
| default + 10% uniform | 1,000 | much greedier | gamma 0.7 | -36.9% ± 8.3 / 97.3% | -28.0% ± 3.1 / 43.8% | -1.0% ± 1.6 / 18.0% | -2.2% ± 1.0 / 11.6% |
| default + 10% uniform | 1,000 | much greedier | first 10 steps | -8.4% ± 13.7 / 149.2% | -22.3% ± 3.6 / 45.0% | -2.5% ± 4.2 / 45.8% | -5.6% ± 1.8 / 20.6% |
| default + 10% uniform | 1,000 | much greedier | first 5 steps | -11.5% ± 3.8 / 43.4% | -7.4% ± 2.4 / 27.7% | -1.4% ± 1.9 / 21.2% | -2.0% ± 1.4 / 15.6% |
| default + 10% uniform | 5,000 | pushes sponsored | full | -18.0% ± 19.2 / 210.2% | -26.5% ± 3.3 / 44.6% | +30.8% ± 38.1 / 416.6% | -6.4% ± 2.2 / 24.5% |
| default + 10% uniform | 5,000 | pushes sponsored | gamma 0.9 | -15.3% ± 17.0 / 186.5% | -19.7% ± 3.1 / 39.0% | +19.1% ± 23.1 / 253.2% | -3.3% ± 1.3 / 15.0% |
| default + 10% uniform | 5,000 | pushes sponsored | gamma 0.7 | -15.1% ± 13.2 / 144.4% | -11.7% ± 3.1 / 35.8% | +3.8% ± 5.3 / 57.8% | -0.9% ± 0.7 / 7.4% |
| default + 10% uniform | 5,000 | pushes sponsored | first 10 steps | +37.6% ± 34.3 / 376.2% | -7.8% ± 4.0 / 44.3% | +36.5% ± 41.4 / 452.7% | -3.5% ± 1.7 / 19.1% |
| default + 10% uniform | 5,000 | pushes sponsored | first 5 steps | -2.3% ± 4.0 / 44.0% | -0.8% ± 2.0 / 21.6% | -0.3% ± 1.7 / 18.3% | -0.2% ± 1.1 / 11.7% |
| default + 10% uniform | 5,000 | much greedier | full | -36.3% ± 9.3 / 107.5% | -31.4% ± 2.5 / 41.8% | -4.4% ± 5.2 / 57.0% | -9.5% ± 1.4 / 18.2% |
| default + 10% uniform | 5,000 | much greedier | gamma 0.9 | -32.0% ± 8.7 / 100.1% | -24.6% ± 2.4 / 35.8% | -2.2% ± 3.0 / 32.5% | -5.0% ± 0.9 / 11.4% |
| default + 10% uniform | 5,000 | much greedier | gamma 0.7 | -27.3% ± 8.0 / 91.3% | -16.7% ± 2.4 / 31.3% | -1.0% ± 0.8 / 9.3% | -1.4% ± 0.5 / 5.2% |
| default + 10% uniform | 5,000 | much greedier | first 10 steps | +6.8% ± 24.1 / 263.2% | -13.9% ± 2.6 / 31.4% | +0.0% ± 5.4 / 59.2% | -4.7% ± 1.3 / 14.6% |
| default + 10% uniform | 5,000 | much greedier | first 5 steps | -2.8% ± 3.2 / 35.0% | -3.5% ± 1.5 / 16.7% | -2.3% ± 0.8 / 8.8% | -1.7% ± 0.6 / 6.7% |
| default + 10% uniform | 20,000 | pushes sponsored | full | +129.3% ± 116.5 / 1277.5% | -20.9% ± 5.6 / 64.9% | +11.6% ± 13.9 / 152.6% | -2.6% ± 2.2 / 23.8% |
| default + 10% uniform | 20,000 | pushes sponsored | gamma 0.9 | +79.6% ± 79.0 / 865.6% | -16.1% ± 4.2 / 48.2% | +3.6% ± 4.0 / 43.7% | -0.6% ± 1.1 / 12.0% |
| default + 10% uniform | 20,000 | pushes sponsored | gamma 0.7 | +45.4% ± 57.6 / 630.5% | -9.5% ± 3.6 / 40.8% | +0.9% ± 0.7 / 8.1% | +0.5% ± 0.4 / 4.9% |
| default + 10% uniform | 20,000 | pushes sponsored | first 10 steps | -2.9% ± 10.1 / 110.3% | -7.6% ± 2.8 / 31.0% | +2.0% ± 2.8 / 31.0% | +0.1% ± 1.4 / 15.3% |
| default + 10% uniform | 20,000 | pushes sponsored | first 5 steps | +1.2% ± 2.7 / 29.4% | +1.0% ± 1.2 / 13.6% | +1.1% ± 0.9 / 9.6% | +1.0% ± 0.7 / 7.4% |
| default + 10% uniform | 20,000 | much greedier | full | -27.2% ± 6.7 / 78.1% | -23.3% ± 2.5 / 35.9% | -6.3% ± 1.7 / 20.1% | -5.7% ± 1.3 / 15.4% |
| default + 10% uniform | 20,000 | much greedier | gamma 0.9 | -22.1% ± 7.0 / 79.6% | -17.3% ± 2.3 / 30.2% | -3.4% ± 0.9 / 10.9% | -2.9% ± 0.8 / 8.7% |
| default + 10% uniform | 20,000 | much greedier | gamma 0.7 | -16.5% ± 8.2 / 91.3% | -10.7% ± 2.2 / 26.5% | -0.8% ± 0.4 / 4.3% | -0.6% ± 0.3 / 3.6% |
| default + 10% uniform | 20,000 | much greedier | first 10 steps | -14.7% ± 6.3 / 70.6% | -11.5% ± 2.1 / 25.5% | -3.9% ± 1.1 / 12.6% | -3.0% ± 0.9 / 10.4% |
| default + 10% uniform | 20,000 | much greedier | first 5 steps | -1.9% ± 1.3 / 14.3% | -1.4% ± 0.7 / 8.2% | -0.6% ± 0.5 / 5.5% | -0.4% ± 0.4 / 4.7% |

Finished in 1304 s with seed 4004.
