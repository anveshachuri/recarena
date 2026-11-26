Default world and catalog. 50 logged datasets per logging policy and size, each checked once per kind of error (see `results/propensity_error.md` for the kinds). A single probe flags a dataset when its z is beyond 1.96. Score probes raise one weight of the claimed logged policy by 0.05. The score test is a chi-square test on the three score probes together; the Bonferroni test flags when any of the 8 probes is beyond 2.73. With exact probabilities every test should flag about 5% of datasets; the exact rows show that rate ± its Monte Carlo standard error. Shifts are SNPDIS with the wrong probabilities minus SNPDIS with exact ones on the same data, in percent of the true value (truth from 100,000 sessions per target).

## Logging: default, 1,000 sessions

### Share of datasets flagged

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier | history +0.05 | quality +0.05 | sponsored +0.05 | score test | all probes, Bonferroni |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| exact | 0% ± 0.0 | 10% ± 4.2 | 6% ± 3.4 | 2% ± 2.0 | 8% ± 3.8 | 6% ± 3.4 | 10% ± 4.2 | 2% ± 2.0 | 8% ± 3.8 | 4% ± 2.8 |
| temperature 0.8 | 100% | 100% | 100% | 6% | 100% | 10% | 100% | 6% | 100% | 100% |
| temperature 0.9 | 100% | 98% | 42% | 0% | 92% | 4% | 98% | 4% | 94% | 94% |
| temperature 1.1 | 94% | 94% | 40% | 4% | 66% | 10% | 92% | 4% | 90% | 86% |
| temperature 1.2 | 100% | 100% | 100% | 4% | 100% | 14% | 100% | 6% | 100% | 100% |
| history weight 0.8 | 14% | 8% | 12% | 2% | 6% | 14% | 10% | 2% | 10% | 4% |
| history weight 1.2 | 6% | 10% | 6% | 2% | 8% | 6% | 10% | 2% | 8% | 2% |
| fitted, all features | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| fitted, quality only | 88% | 24% | 88% | 2% | 2% | 92% | 0% | 2% | 70% | 64% |

### Mean absolute SNPDIS shift (% of the true value)

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | 1.6 | 2.4 | 1.7 | 2.5 | 5.6 |
| temperature 0.9 | 1.0 | 1.4 | 1.0 | 1.1 | 2.6 |
| temperature 1.1 | 1.1 | 1.4 | 1.2 | 1.0 | 2.2 |
| temperature 1.2 | 2.3 | 2.9 | 2.4 | 1.9 | 4.0 |
| history weight 0.8 | 0.1 | 0.1 | 0.2 | 0.2 | 0.1 |
| history weight 1.2 | 0.1 | 0.1 | 0.2 | 0.2 | 0.1 |
| fitted, all features | 0.3 | 0.3 | 0.3 | 0.6 | 0.7 |
| fitted, quality only | 0.5 | 0.6 | 1.1 | 1.1 | 0.9 |

### Does a flag line up with a large shift?

All datasets with wrong probabilities, split by whether the largest absolute SNPDIS shift over the 4 near targets is above 2% of the true value.

| Largest near shift | Datasets | Flagged by score test | Flagged by Bonferroni |
|---|---:|---:|---:|
| above 2% | 151 | 97% | 95% |
| 2% or less | 249 | 36% | 33% |

## Logging: default, 5,000 sessions

### Share of datasets flagged

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier | history +0.05 | quality +0.05 | sponsored +0.05 | score test | all probes, Bonferroni |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| exact | 0% ± 0.0 | 2% ± 2.0 | 0% ± 0.0 | 0% ± 0.0 | 4% ± 2.8 | 0% ± 0.0 | 4% ± 2.8 | 8% ± 3.8 | 4% ± 2.8 | 2% ± 2.0 |
| temperature 0.8 | 100% | 100% | 100% | 72% | 100% | 54% | 100% | 20% | 100% | 100% |
| temperature 0.9 | 100% | 100% | 98% | 8% | 100% | 16% | 100% | 10% | 100% | 100% |
| temperature 1.1 | 100% | 100% | 96% | 4% | 100% | 12% | 100% | 10% | 100% | 100% |
| temperature 1.2 | 100% | 100% | 100% | 0% | 100% | 24% | 100% | 10% | 100% | 100% |
| history weight 0.8 | 24% | 6% | 22% | 2% | 4% | 24% | 4% | 8% | 16% | 10% |
| history weight 1.2 | 32% | 2% | 34% | 0% | 4% | 32% | 2% | 8% | 16% | 10% |
| fitted, all features | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| fitted, quality only | 100% | 100% | 100% | 4% | 2% | 100% | 0% | 8% | 100% | 100% |

### Mean absolute SNPDIS shift (% of the true value)

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | 1.7 | 2.6 | 1.9 | 2.9 | 8.4 |
| temperature 0.9 | 1.1 | 1.4 | 1.1 | 1.3 | 3.8 |
| temperature 1.1 | 1.2 | 1.5 | 1.3 | 1.1 | 3.2 |
| temperature 1.2 | 2.5 | 3.1 | 2.6 | 2.1 | 6.0 |
| history weight 0.8 | 0.1 | 0.1 | 0.2 | 0.2 | 0.2 |
| history weight 1.2 | 0.0 | 0.1 | 0.2 | 0.2 | 0.1 |
| fitted, all features | 0.1 | 0.1 | 0.1 | 0.3 | 0.3 |
| fitted, quality only | 0.4 | 0.5 | 1.1 | 1.0 | 0.9 |

### Does a flag line up with a large shift?

All datasets with wrong probabilities, split by whether the largest absolute SNPDIS shift over the 4 near targets is above 2% of the true value.

| Largest near shift | Datasets | Flagged by score test | Flagged by Bonferroni |
|---|---:|---:|---:|
| above 2% | 183 | 99% | 99% |
| 2% or less | 217 | 39% | 36% |

## Logging: default + 10% uniform, 1,000 sessions

### Share of datasets flagged

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier | history +0.05 | quality +0.05 | sponsored +0.05 | score test | all probes, Bonferroni |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| exact | 8% ± 3.8 | 8% ± 3.8 | 10% ± 4.2 | 4% ± 2.8 | 10% ± 4.2 | 8% ± 3.8 | 8% ± 3.8 | 0% ± 0.0 | 2% ± 2.0 | 8% ± 3.8 |
| temperature 0.8 | 100% | 100% | 90% | 6% | 100% | 20% | 100% | 4% | 100% | 100% |
| temperature 0.9 | 4% | 96% | 10% | 4% | 86% | 10% | 96% | 0% | 94% | 90% |
| temperature 1.1 | 84% | 80% | 40% | 4% | 42% | 6% | 84% | 0% | 60% | 64% |
| temperature 1.2 | 100% | 100% | 100% | 4% | 96% | 10% | 100% | 0% | 100% | 100% |
| history weight 0.8 | 8% | 8% | 4% | 4% | 10% | 10% | 8% | 0% | 6% | 6% |
| history weight 1.2 | 10% | 8% | 14% | 4% | 10% | 16% | 8% | 0% | 6% | 10% |
| fitted, all features | 0% | 0% | 0% | 2% | 2% | 0% | 0% | 0% | 0% | 0% |
| fitted, quality only | 26% | 0% | 58% | 4% | 2% | 64% | 0% | 0% | 42% | 46% |

### Mean absolute SNPDIS shift (% of the true value)

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | 2.0 | 2.7 | 2.1 | 4.3 | 6.4 |
| temperature 0.9 | 1.1 | 1.4 | 1.1 | 2.0 | 2.9 |
| temperature 1.1 | 1.2 | 1.5 | 1.2 | 1.8 | 2.4 |
| temperature 1.2 | 2.4 | 2.9 | 2.5 | 3.4 | 4.4 |
| history weight 0.8 | 0.1 | 0.1 | 0.2 | 0.2 | 0.2 |
| history weight 1.2 | 0.0 | 0.1 | 0.1 | 0.2 | 0.2 |
| fitted, all features | 0.4 | 0.5 | 0.4 | 1.0 | 1.1 |
| fitted, quality only | 0.5 | 0.7 | 1.2 | 1.4 | 1.8 |

### Does a flag line up with a large shift?

All datasets with wrong probabilities, split by whether the largest absolute SNPDIS shift over the 4 near targets is above 2% of the true value.

| Largest near shift | Datasets | Flagged by score test | Flagged by Bonferroni |
|---|---:|---:|---:|
| above 2% | 180 | 84% | 84% |
| 2% or less | 220 | 24% | 25% |

## Logging: default + 10% uniform, 5,000 sessions

### Share of datasets flagged

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier | history +0.05 | quality +0.05 | sponsored +0.05 | score test | all probes, Bonferroni |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| exact | 6% ± 3.4 | 6% ± 3.4 | 4% ± 2.8 | 6% ± 3.4 | 6% ± 3.4 | 8% ± 3.8 | 8% ± 3.8 | 4% ± 2.8 | 8% ± 3.8 | 2% ± 2.0 |
| temperature 0.8 | 100% | 100% | 100% | 18% | 100% | 52% | 100% | 16% | 100% | 100% |
| temperature 0.9 | 4% | 100% | 12% | 4% | 100% | 8% | 100% | 6% | 100% | 100% |
| temperature 1.1 | 100% | 100% | 100% | 6% | 100% | 10% | 100% | 12% | 100% | 100% |
| temperature 1.2 | 100% | 100% | 100% | 4% | 100% | 18% | 100% | 12% | 100% | 100% |
| history weight 0.8 | 6% | 8% | 22% | 6% | 4% | 20% | 8% | 4% | 16% | 10% |
| history weight 1.2 | 6% | 6% | 32% | 6% | 6% | 28% | 8% | 4% | 18% | 8% |
| fitted, all features | 0% | 0% | 0% | 0% | 12% | 0% | 0% | 0% | 0% | 2% |
| fitted, quality only | 100% | 90% | 100% | 4% | 38% | 100% | 0% | 4% | 100% | 100% |

### Mean absolute SNPDIS shift (% of the true value)

| Kind of error | same as logging | slightly different | more personalized | pushes sponsored | much greedier |
|---|---:|---:|---:|---:|---:|
| temperature 0.8 | 2.0 | 2.7 | 2.1 | 2.9 | 7.1 |
| temperature 0.9 | 1.1 | 1.5 | 1.2 | 1.4 | 3.2 |
| temperature 1.1 | 1.2 | 1.5 | 1.3 | 1.2 | 2.7 |
| temperature 1.2 | 2.4 | 3.0 | 2.5 | 2.3 | 5.0 |
| history weight 0.8 | 0.1 | 0.1 | 0.2 | 0.1 | 0.1 |
| history weight 1.2 | 0.0 | 0.1 | 0.1 | 0.1 | 0.1 |
| fitted, all features | 0.1 | 0.2 | 0.2 | 0.4 | 0.6 |
| fitted, quality only | 0.4 | 0.6 | 1.0 | 0.7 | 1.2 |

### Does a flag line up with a large shift?

All datasets with wrong probabilities, split by whether the largest absolute SNPDIS shift over the 4 near targets is above 2% of the true value.

| Largest near shift | Datasets | Flagged by score test | Flagged by Bonferroni |
|---|---:|---:|---:|
| above 2% | 165 | 98% | 98% |
| 2% or less | 235 | 45% | 42% |

Finished in 1736 s with seed 4004.
