5 catalogs, 20 logged datasets per catalog and size, truth from 200,000 sessions per policy, catalog and world. Budgets are 10% below and above each policy's true cost. A policy is approved for a budget when the upper bound on its estimated cost is at most the budget. The upper bound is the estimate plus z standard errors (one-sided normal interval at the given level), and "point" is the estimate itself, as in the stress test.

- **False approval:** approving the budget 10% below the true cost, which the policy breaks.
- **False rejection:** rejecting the budget 10% above the true cost, which the policy fits.
- **Above bound:** the true cost is above the upper bound.

Each far cell pools 200 decisions per budget (2 far targets, 100 datasets), so a rate's Monte Carlo standard error is at most 3.5 points. The truth's own standard error is at most 0.17% of the true cost. Direct reports no standard error, so it only has the point row.

## Far targets: false approvals / false rejections (5,000 sessions)

| Scenario | Estimator | point | 80% | 90% | 95% | 99% |
|---|---|---:|---:|---:|---:|---:|
| Baseline: informed model | IPS | 89% / 10% | 79% / 15% | 78% / 18% | 74% / 20% | 66% / 24% |
| Baseline: informed model | SNIPS | 88% / 4% | 78% / 7% | 74% / 12% | 69% / 12% | 62% / 19% |
| Baseline: informed model | PDIS | 72% / 10% | 58% / 22% | 50% / 29% | 46% / 32% | 34% / 41% |
| Baseline: informed model | SNPDIS | 74% / 6% | 57% / 12% | 48% / 15% | 40% / 16% | 26% / 22% |
| Baseline: informed model | Direct | 0% / 0% | n/a | n/a | n/a | n/a |
| Baseline: informed model | DR | 18% / 17% | 4% / 34% | 0% / 49% | 0% / 62% | 0% / 79% |
| Uninformed model | IPS | 86% / 8% | 72% / 19% | 66% / 23% | 63% / 26% | 56% / 35% |
| Uninformed model | SNIPS | 86% / 5% | 76% / 9% | 72% / 13% | 65% / 16% | 57% / 22% |
| Uninformed model | PDIS | 66% / 14% | 48% / 25% | 42% / 34% | 34% / 38% | 22% / 46% |
| Uninformed model | SNPDIS | 68% / 6% | 52% / 14% | 44% / 18% | 38% / 22% | 30% / 29% |
| Uninformed model | Direct | 70% / 20% | n/a | n/a | n/a | n/a |
| Uninformed model | DR | 47% / 18% | 26% / 33% | 22% / 45% | 20% / 50% | 16% / 62% |
| Hidden item appeal | IPS | 86% / 10% | 78% / 18% | 72% / 20% | 69% / 24% | 64% / 28% |
| Hidden item appeal | SNIPS | 88% / 6% | 76% / 10% | 71% / 13% | 66% / 15% | 60% / 19% |
| Hidden item appeal | PDIS | 76% / 12% | 58% / 22% | 47% / 27% | 43% / 32% | 34% / 40% |
| Hidden item appeal | SNPDIS | 76% / 4% | 56% / 10% | 48% / 13% | 41% / 17% | 29% / 26% |
| Hidden item appeal | Direct | 0% / 0% | n/a | n/a | n/a | n/a |
| Hidden item appeal | DR | 21% / 12% | 6% / 30% | 1% / 47% | 0% / 60% | 0% / 80% |
| Sponsored items drive users away | IPS | 80% / 12% | 66% / 22% | 57% / 28% | 51% / 30% | 46% / 42% |
| Sponsored items drive users away | SNIPS | 77% / 8% | 60% / 15% | 53% / 21% | 47% / 24% | 38% / 32% |
| Sponsored items drive users away | PDIS | 58% / 14% | 40% / 24% | 28% / 32% | 24% / 36% | 17% / 48% |
| Sponsored items drive users away | SNPDIS | 55% / 6% | 35% / 15% | 27% / 20% | 23% / 26% | 14% / 36% |
| Sponsored items drive users away | Direct | 0% / 0% | n/a | n/a | n/a | n/a |
| Sponsored items drive users away | DR | 18% / 11% | 5% / 27% | 0% / 38% | 0% / 52% | 0% / 78% |
| All of the above | IPS | 78% / 16% | 60% / 23% | 56% / 33% | 50% / 38% | 44% / 44% |
| All of the above | SNIPS | 76% / 14% | 60% / 18% | 51% / 20% | 44% / 25% | 37% / 32% |
| All of the above | PDIS | 55% / 16% | 40% / 31% | 32% / 40% | 26% / 44% | 16% / 53% |
| All of the above | SNPDIS | 51% / 9% | 35% / 18% | 30% / 22% | 22% / 28% | 12% / 38% |
| All of the above | Direct | 50% / 20% | n/a | n/a | n/a | n/a |
| All of the above | DR | 30% / 15% | 12% / 34% | 8% / 43% | 5% / 52% | 3% / 63% |

## Far targets: true cost above the upper bound (5,000 sessions)

A level's bound should be exceeded in about (1 - level) of datasets if the interval is right.

| Scenario | Estimator | point | 80% | 90% | 95% | 99% |
|---|---|---:|---:|---:|---:|---:|
| Baseline: informed model | IPS | 90% | 84% | 80% | 78% | 72% |
| Baseline: informed model | SNIPS | 93% | 86% | 84% | 79% | 74% |
| Baseline: informed model | PDIS | 83% | 68% | 61% | 58% | 51% |
| Baseline: informed model | SNPDIS | 88% | 81% | 75% | 70% | 60% |
| Baseline: informed model | Direct | 62% | n/a | n/a | n/a | n/a |
| Baseline: informed model | DR | 48% | 23% | 8% | 4% | 1% |
| Uninformed model | IPS | 90% | 79% | 74% | 66% | 62% |
| Uninformed model | SNIPS | 92% | 84% | 80% | 76% | 70% |
| Uninformed model | PDIS | 82% | 63% | 56% | 52% | 41% |
| Uninformed model | SNPDIS | 84% | 74% | 68% | 62% | 54% |
| Uninformed model | Direct | 70% | n/a | n/a | n/a | n/a |
| Uninformed model | DR | 66% | 48% | 36% | 30% | 24% |
| Hidden item appeal | IPS | 88% | 80% | 76% | 74% | 68% |
| Hidden item appeal | SNIPS | 90% | 87% | 82% | 80% | 70% |
| Hidden item appeal | PDIS | 84% | 71% | 64% | 60% | 48% |
| Hidden item appeal | SNPDIS | 92% | 79% | 72% | 67% | 58% |
| Hidden item appeal | Direct | 66% | n/a | n/a | n/a | n/a |
| Hidden item appeal | DR | 54% | 30% | 14% | 6% | 0% |
| Sponsored items drive users away | IPS | 84% | 72% | 67% | 60% | 52% |
| Sponsored items drive users away | SNIPS | 86% | 75% | 72% | 65% | 56% |
| Sponsored items drive users away | PDIS | 78% | 62% | 50% | 46% | 34% |
| Sponsored items drive users away | SNPDIS | 84% | 66% | 58% | 52% | 42% |
| Sponsored items drive users away | Direct | 62% | n/a | n/a | n/a | n/a |
| Sponsored items drive users away | DR | 55% | 25% | 10% | 4% | 0% |
| All of the above | IPS | 82% | 67% | 60% | 57% | 50% |
| All of the above | SNIPS | 84% | 76% | 72% | 65% | 56% |
| All of the above | PDIS | 76% | 56% | 48% | 44% | 34% |
| All of the above | SNPDIS | 81% | 66% | 55% | 50% | 42% |
| All of the above | Direct | 70% | n/a | n/a | n/a | n/a |
| All of the above | DR | 62% | 40% | 32% | 26% | 16% |

## Near targets: false approvals / false rejections (5,000 sessions)

| Scenario | Estimator | point | 80% | 90% | 95% | 99% |
|---|---|---:|---:|---:|---:|---:|
| Baseline: informed model | IPS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 1% | 0% / 1% |
| Baseline: informed model | SNIPS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Baseline: informed model | PDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Baseline: informed model | SNPDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Baseline: informed model | Direct | 0% / 0% | n/a | n/a | n/a | n/a |
| Baseline: informed model | DR | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Uninformed model | IPS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 1% |
| Uninformed model | SNIPS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Uninformed model | PDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Uninformed model | SNPDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Uninformed model | Direct | 0% / 0% | n/a | n/a | n/a | n/a |
| Uninformed model | DR | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Hidden item appeal | IPS | 0% / 0% | 0% / 0% | 0% / 1% | 0% / 1% | 0% / 1% |
| Hidden item appeal | SNIPS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Hidden item appeal | PDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Hidden item appeal | SNPDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Hidden item appeal | Direct | 0% / 0% | n/a | n/a | n/a | n/a |
| Hidden item appeal | DR | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Sponsored items drive users away | IPS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 1% |
| Sponsored items drive users away | SNIPS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Sponsored items drive users away | PDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Sponsored items drive users away | SNPDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| Sponsored items drive users away | Direct | 0% / 0% | n/a | n/a | n/a | n/a |
| Sponsored items drive users away | DR | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| All of the above | IPS | 0% / 1% | 0% / 1% | 0% / 1% | 0% / 1% | 0% / 1% |
| All of the above | SNIPS | 0% / 0% | 0% / 1% | 0% / 1% | 0% / 1% | 0% / 1% |
| All of the above | PDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 1% |
| All of the above | SNPDIS | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| All of the above | Direct | 0% / 0% | n/a | n/a | n/a | n/a |
| All of the above | DR | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |

Finished in 1504 s with seed 4004.
