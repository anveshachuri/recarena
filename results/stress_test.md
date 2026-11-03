5 catalogs, 10 logged datasets per catalog and size, truth from 500,000 sessions per policy and catalog. Errors are percent of the true value. Cells show median error / RMSE.

## Baseline: informed model (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | 1.2 / 1.6 | 1.2 / 1.6 | 1.2 / 1.6 | 1.2 / 1.6 | 1.1 / 1.6 | 1.1 / 1.6 |
| slightly different | 1.4 / 1.8 | 1.2 / 1.7 | 1.3 / 1.7 | 1.2 / 1.7 | 1.1 / 1.7 | 1.1 / 1.7 |
| more personalized | 1.7 / 4.1 | 1.3 / 3.3 | 1.2 / 2.3 | 1.2 / 2.2 | 1.6 / 2.2 | 1.2 / 2.0 |
| pushes sponsored | 55.8 / 140.4 | 35.4 / 38.0 | 19.5 / 31.9 | 17.9 / 19.4 | 1.9 / 2.5 | 13.6 / 118.4 |
| much greedier | 63.2 / 105.5 | 43.0 / 46.4 | 17.0 / 25.4 | 10.9 / 17.6 | 1.3 / 2.5 | 8.4 / 28.3 |

## Uninformed model (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | 1.1 / 1.5 | 1.1 / 1.5 | 1.1 / 1.5 | 1.1 / 1.5 | 1.1 / 1.6 | 1.1 / 1.5 |
| slightly different | 1.2 / 1.7 | 1.1 / 1.6 | 1.1 / 1.6 | 1.0 / 1.6 | 2.9 / 3.0 | 1.0 / 1.6 |
| more personalized | 1.8 / 2.2 | 1.6 / 1.9 | 1.4 / 1.6 | 1.2 / 1.6 | 2.0 / 2.4 | 1.2 / 1.6 |
| pushes sponsored | 61.4 / 162.4 | 39.6 / 57.9 | 19.9 / 72.1 | 17.3 / 24.9 | 2.2 / 3.0 | 11.4 / 69.4 |
| much greedier | 58.5 / 62.9 | 37.5 / 38.4 | 15.5 / 40.7 | 14.7 / 17.6 | 19.5 / 20.2 | 10.2 / 25.4 |

## Hidden item appeal (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | 0.5 / 1.2 | 0.5 / 1.2 | 0.5 / 1.2 | 0.5 / 1.2 | 0.5 / 1.2 | 0.5 / 1.2 |
| slightly different | 0.9 / 1.5 | 0.8 / 1.4 | 0.7 / 1.4 | 0.6 / 1.3 | 0.5 / 1.2 | 0.6 / 1.3 |
| more personalized | 1.8 / 2.3 | 1.4 / 1.9 | 0.6 / 1.5 | 0.6 / 1.4 | 1.1 / 1.6 | 0.7 / 1.4 |
| pushes sponsored | 63.9 / 60.6 | 40.2 / 39.7 | 21.5 / 59.4 | 14.6 / 20.3 | 1.9 / 2.4 | 11.5 / 37.3 |
| much greedier | 56.1 / 1383.3 | 32.4 / 49.6 | 17.5 / 26.9 | 14.5 / 16.0 | 3.2 / 4.4 | 9.9 / 50.6 |

## Sponsored items drive users away (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | 1.3 / 1.6 | 1.3 / 1.6 | 1.3 / 1.6 | 1.3 / 1.6 | 1.3 / 1.6 | 1.2 / 1.6 |
| slightly different | 1.2 / 1.7 | 1.0 / 1.6 | 1.1 / 1.7 | 1.1 / 1.6 | 1.4 / 1.7 | 1.0 / 1.7 |
| more personalized | 1.5 / 4.6 | 1.4 / 3.5 | 1.2 / 1.7 | 1.1 / 1.7 | 1.9 / 2.3 | 1.2 / 1.7 |
| pushes sponsored | 37.5 / 48.7 | 29.6 / 29.1 | 12.7 / 17.4 | 11.5 / 15.1 | 2.6 / 3.2 | 7.5 / 18.9 |
| much greedier | 51.6 / 103.6 | 33.5 / 36.1 | 16.6 / 29.5 | 10.3 / 19.0 | 1.5 / 2.4 | 8.3 / 28.1 |

## All of the above (5,000 sessions)

| New policy | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|
| same as logging | 0.8 / 1.2 | 0.8 / 1.2 | 0.8 / 1.2 | 0.8 / 1.2 | 0.8 / 1.3 | 0.8 / 1.2 |
| slightly different | 1.1 / 1.5 | 0.9 / 1.4 | 0.9 / 1.3 | 0.9 / 1.3 | 2.0 / 2.4 | 0.8 / 1.3 |
| more personalized | 1.8 / 2.5 | 1.3 / 1.9 | 0.9 / 1.5 | 0.8 / 1.4 | 1.6 / 2.1 | 0.8 / 1.5 |
| pushes sponsored | 44.6 / 72.6 | 26.6 / 29.7 | 9.3 / 13.4 | 10.0 / 13.8 | 24.5 / 27.8 | 11.5 / 46.5 |
| much greedier | 47.9 / 46.2 | 33.7 / 33.8 | 16.1 / 21.1 | 13.1 / 16.5 | 12.7 / 14.0 | 9.6 / 20.0 |

## Far-from-logging policies at each size (RMSE, pooled across catalogs)

| Scenario | Sessions | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline: informed model | 1,000 | 70.1 | 48.1 | 53.3 | 22.3 | 5.4 | 33.8 |
| Baseline: informed model | 5,000 | 124.2 | 42.4 | 28.8 | 18.5 | 2.5 | 86.1 |
| Uninformed model | 1,000 | 386.9 | 50.5 | 357.4 | 28.5 | 15.1 | 87.2 |
| Uninformed model | 5,000 | 123.1 | 49.1 | 58.6 | 21.6 | 14.4 | 52.2 |
| Hidden item appeal | 1,000 | 305.6 | 52.2 | 48.7 | 23.8 | 5.3 | 76.2 |
| Hidden item appeal | 5,000 | 979.1 | 44.9 | 46.1 | 18.3 | 3.5 | 44.5 |
| Sponsored items drive users away | 1,000 | 178.2 | 45.6 | 27.7 | 20.0 | 6.2 | 65.0 |
| Sponsored items drive users away | 5,000 | 81.0 | 32.8 | 24.2 | 17.2 | 2.8 | 24.0 |
| All of the above | 1,000 | 58.4 | 41.6 | 43.8 | 21.1 | 22.2 | 34.7 |
| All of the above | 5,000 | 60.9 | 31.8 | 17.7 | 15.2 | 22.0 | 35.8 |

## Far-from-logging RMSE for each catalog (5,000 sessions)

| Scenario | Estimator | Catalog 0 | Catalog 1 | Catalog 2 | Catalog 3 | Catalog 4 |
|---|---|---:|---:|---:|---:|---:|
| Baseline: informed model | SNPDIS | 21.1 | 16.5 | 16.8 | 14.3 | 22.5 |
| Baseline: informed model | Direct | 2.4 | 3.0 | 2.0 | 2.5 | 2.5 |
| Baseline: informed model | DR | 26.9 | 180.8 | 40.9 | 14.8 | 41.7 |
| Uninformed model | SNPDIS | 15.6 | 17.6 | 23.5 | 30.9 | 16.4 |
| Uninformed model | Direct | 14.1 | 13.6 | 13.2 | 13.5 | 17.4 |
| Uninformed model | DR | 22.9 | 17.2 | 39.5 | 103.4 | 24.1 |
| Hidden item appeal | SNPDIS | 12.4 | 25.3 | 20.4 | 13.4 | 16.9 |
| Hidden item appeal | Direct | 3.4 | 4.5 | 4.6 | 2.2 | 2.1 |
| Hidden item appeal | DR | 18.9 | 50.8 | 33.2 | 21.1 | 73.6 |
| Sponsored items drive users away | SNPDIS | 19.1 | 14.5 | 13.7 | 12.2 | 23.7 |
| Sponsored items drive users away | Direct | 2.7 | 2.5 | 2.7 | 3.1 | 2.9 |
| Sponsored items drive users away | DR | 24.9 | 12.7 | 21.5 | 10.9 | 38.9 |
| All of the above | SNPDIS | 16.7 | 17.0 | 14.9 | 11.0 | 15.7 |
| All of the above | Direct | 21.5 | 22.7 | 33.9 | 6.9 | 15.9 |
| All of the above | DR | 70.5 | 26.8 | 16.6 | 11.5 | 17.4 |

## Tight budget decisions (5,000 sessions)

Each estimate is tested against budgets 10% above and below the true cost. The table shows the share of decisions that were right. 50% is what a method gets if it always answers the same way.

| Scenario | New policies | IPS | SNIPS | PDIS | SNPDIS | Direct | DR |
|---|---|---:|---:|---:|---:|---:|---:|
| Baseline: informed model | Near | 100% | 100% | 100% | 100% | 100% | 100% |
| Baseline: informed model | Far | 52% | 52% | 61% | 64% | 100% | 83% |
| Uninformed model | Near | 100% | 100% | 100% | 100% | 100% | 100% |
| Uninformed model | Far | 52% | 53% | 62% | 63% | 55% | 70% |
| Hidden item appeal | Near | 100% | 100% | 100% | 100% | 100% | 100% |
| Hidden item appeal | Far | 51% | 55% | 57% | 64% | 100% | 79% |
| Sponsored items drive users away | Near | 100% | 100% | 100% | 100% | 100% | 100% |
| Sponsored items drive users away | Far | 56% | 58% | 61% | 70% | 100% | 84% |
| All of the above | Near | 100% | 100% | 100% | 100% | 100% | 100% |
| All of the above | Far | 56% | 56% | 60% | 62% | 65% | 80% |

Finished in 1912 s with seed 4004.
