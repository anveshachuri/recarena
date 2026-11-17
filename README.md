# recarena

**How well can you judge a new recommender using only old logs?**

Teams often want to know how a new recommender would perform before showing it to anyone. Off-policy evaluation (OPE) estimates that from logs of the old system. On real data, the true answer is unknown, so it is hard to tell which estimator to trust.

recarena is a simulator where the true answer is known. It runs each policy directly to get its true value, then scores every estimator against that value.

> Early prototype. The API will change, and the results below come from one simulated setup.

## What's in it

- **Simulated users** with hidden interests that drift, fatigue that builds up, and a chance of leaving after missed recommendations.
- **Slates:** users look down a list and stop at their first click, and they are less likely to look at lower slots.
- **A Gymnasium environment**, `SlateRecEnv`, for training RL agents.
- **Six estimators:** IPS, SNIPS, PDIS, SNPDIS, a direct method (fitted Q evaluation) and doubly robust.
- **Two slate-aware estimators**, CascadePDIS and SNCascadePDIS, which you can ask for by name.
- **Budgets:** each step reports sponsored exposure as a cost, so you can test whether an estimator can tell if a policy stays within a budget.

## Quickstart

```bash
git clone https://github.com/anveshachuri/recarena.git
cd recarena
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"   # On Linux or macOS: .venv/bin/python
.venv/Scripts/python -m pytest
.venv/Scripts/python -m recarena.benchmark --sizes 200 1000 --seeds 5 --truth 200000
```

Score the estimators yourself:

```python
import numpy as np
from recarena import Catalog, SimConfig, SoftmaxPolicy, collect, estimate_all, true_value

config = SimConfig()
catalog = Catalog.generate(config)
rng = np.random.default_rng(0)

old = SoftmaxPolicy(catalog, "old")
new = SoftmaxPolicy(catalog, "new", history_weight=1.5, quality_weight=1.2)

logs = collect(config, catalog, old, 1000, rng)
estimates = estimate_all(logs, logs.rewards, new, config.examine_decay, rng)
truth = true_value(config, catalog, new, 200_000, rng)

print("true value:", round(truth.reward, 3))
print({name: round(value, 3) for name, value in estimates.items()})
```

Add your own estimator. It gets an `EstimationTask` (the logs, the values to estimate, the target policy and shared importance ratios) and returns an `Estimate`:

```python
from recarena import Estimate, estimate_all_detailed, register_estimator

def clipped_ips(task):
    weights = np.minimum(task.ratios.prod(axis=1), 10.0)
    scores = weights * task.values.sum(axis=1)
    return Estimate(scores.mean(), scores - scores.mean())  # The second part is optional.

register_estimator("Clipped IPS", clipped_ips)
results = estimate_all_detailed(logs, logs.rewards, new, config.examine_decay, rng, estimators=["IPS", "Clipped IPS"])
print({name: (round(r.value, 3), round(r.standard_error(), 3)) for name, r in results.items()})
```

The second part of an `Estimate` is each session's influence on the estimate. Confidence intervals are built from it. Every built-in estimator except Direct provides it. Direct's per-session scores barely vary because sessions start from nearly the same state, so its `standard_error()` is NaN rather than misleadingly small (see #22). The benchmark and stress test take `--estimators` to choose which to run. To use your own estimator there, pass the function itself to `run(..., estimators={"Clipped IPS": clipped_ips})` from a module it can be imported from.

Or train an agent:

```python
from recarena import SlateRecEnv

env = SlateRecEnv()
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
print(reward, info["cost"])
```

## What the stress test found

**No estimator won everywhere.** The results depended on how far the new policy was from the logged one, and on what the model knew.

Results for the two new policies far from the logged one, with 5,000 logged sessions, across 5 catalogs and 10 logged datasets per catalog:

| Scenario | SNPDIS | Direct | DR |
|---|---:|---:|---:|
| Informed model | 18.5% | **2.5%** | 86.1% |
| Uninformed model | 21.6% | **14.4%** | 52.2% |
| Hidden item appeal | 18.3% | **3.5%** | 44.5% |
| Sponsored items drive users away | 17.2% | **2.8%** | 24.0% |
| All of the above | **15.2%** | 22.0% | 35.8% |

*Reward error (RMSE as a share of the true value, lower is better). IPS, SNIPS and PDIS were never the best here, and are in the full results.*

Each estimate was also tested against budgets 10% above and below the policy's true cost:

| Scenario | SNPDIS | Direct | DR |
|---|---:|---:|---:|
| Informed model | 64% | **100%** | 83% |
| Uninformed model | 63% | 55% | **70%** |
| Hidden item appeal | 64% | **100%** | 79% |
| Sponsored items drive users away | 70% | **100%** | 84% |
| All of the above | 62% | 65% | **80%** |

*Share of budget decisions that were correct (higher is better). A method that always gives the same answer scores 50%.*

What this suggests so far:

- **Close to the logged policy, the choice barely matters.** All six estimators were accurate, and all got 100% of budget decisions right.
- **The direct method is only as good as its features.** It stayed accurate with hidden effects when it knew about quality and sponsorship, and it became the wrong choice for budgets when it didn't.
- **Reward accuracy doesn't guarantee budget accuracy.** With the uninformed model, the direct method's median error on the sponsored policy's reward was only 2.2%, but it got just 55% of budget decisions right across the far policies, because it can't see which items are sponsored.
- **Doubly robust is usually fine and occasionally terrible.** Its typical error was far below its RMSE, which a few extreme runs dominate. For example, its median error on one policy was 13.6%, while its RMSE was 118.4%.

**Limits of these results:** this is one simulator with settings chosen by its author, and the hidden effects used here may be too mild. The hidden appeal, for example, isn't related to anything the policies favor (see the linked appeal section below for what happens when it is). The large errors are also noisy with this few runs. These results need more scenarios and independent checking.

Full tables are in [`results/stress_test.md`](results/stress_test.md), and an earlier single-catalog run is in [`results/first_benchmark.md`](results/first_benchmark.md). Reproduce the stress test with:

```bash
python -m recarena.stress --sizes 1000 5000 --catalogs 5 --repeats 10 --truth 500000
```

If it runs slowly, set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` first, because it already runs one job per CPU core.

## Does more exploration in the logs help?

`UniformMixturePolicy` adds exploration to a logging policy: with chance `epsilon` it shows a uniformly random slate, and its slate probabilities stay exact. `python -m recarena.exploration` logs data with six logging policies (temperatures 0.5, 1, 2 and 4, and the default mixed with 10% or 30% uniform slates) and scores every estimator on the usual five targets. Full tables are in [`results/exploration.md`](results/exploration.md).

What it found in the default world, with 50 logged datasets per cell:

- **Exploring costs reward, and less than it might seem.** Mixing in 10% uniform slates cost 1.1% of the logging policy's own reward, 30% cost 3.3%, and raising the temperature to 4 cost 8.6%.
- **None of these logging policies made the far targets much easier.** For "pushes sponsored" and "much greedier", with 5,000 sessions the effective sample size stayed between 0.5% and 2.6% of the sessions logged for every logging policy, and SNPDIS error stayed between 14.4% and 39.1%. A uniform slate here is one of 117,600, so random exploration rarely shows the slates a far target prefers.
- **Effective sample size ranked the cells well.** Its rank correlation with RMSE was between -0.91 and -0.98 for every estimator with 5,000 sessions. Most of that comes from separating near targets from far ones; among the far cells, where it matters most, effective sample size only spanned 0.5% to 2.6% while SNPDIS error spanned 14.4% to 39.1%, so it says "be careful" more than "how wrong".
- **Some far cells are dominated by one or two extreme runs**, for example PDIS at 874.4% ± 436.6. Treat those cells as noisy.

**Limits:** one catalog, the default world, an informed model for Direct and DR, and only uniform exploration. Exploration aimed at the slates a target would show could behave very differently. Reproduce with:

```bash
python -m recarena.exploration --sizes 1000 5000 --repeats 50 --truth 500000
```

## Do slate-aware weights help?

The weighted estimators above treat a whole slate as one action. `CascadePDIS` instead weights a reward in slot j of a step by the ratio of only the first j slots of that step, times the full slate ratios of earlier steps. That is unbiased here because users read top down and stop at their first click, so a slot's reward and cost don't depend on the slots below it. Later steps can depend on the whole slate (fatigue, leaving), so earlier steps still pay for full slates. `SNCascadePDIS` normalizes the weights for each step and slot. Both follow the cascade idea of Kiyohara et al. (2022) and McInerney et al. (2020), applied per step of a session. They are opt in, so default results don't change:

```python
estimate_all(logs, logs.rewards, new, config.examine_decay, rng, estimators=["SNPDIS", "CascadePDIS", "SNCascadePDIS"])
```

`python -m recarena.slate_estimators` compares them with PDIS and SNPDIS across slate sizes and session lengths. Full tables are in [`results/slate_estimators.md`](results/slate_estimators.md). What it found, with 200 logged datasets per cell (RMSE as a share of the true value):

- **In one-step sessions, the gain grows with slate size.** For the two far targets with 5,000 sessions, CascadePDIS cut PDIS error from 5.4% to 4.4% and 4.5% to 4.1% with slates of 2, and from 8.2% to 5.0% and 6.5% to 4.1% with slates of 5.
- **In 20-step sessions, most of that gain disappears.** The full slate ratios of earlier steps dominate the weight. With slates of 3 and 5,000 sessions, SNCascadePDIS improved on SNPDIS only from 19.7% to 17.9% and from 17.1% to 15.2%. Unnormalized CascadePDIS was sometimes worse than PDIS (29.7% ± 5.6 against 27.3% ± 3.0 for "much greedier"), within noise.
- **Near targets don't change.** All four estimators agree to within 0.2 points.
- **Far targets in long sessions show a large average error even for the unbiased estimators** (for example between -12.3% and -16.2% for all four estimators on "much greedier" with slates of 5 and 5,000 sessions). A likely reason, not yet checked, is that the weights are so heavy tailed that 200 datasets rarely include the huge weights that make the average come out right.

**Limits:** one catalog, the default world, the default logging policy, rewards only (costs are supported but weren't scored here), and only the cascade estimator. The pseudoinverse estimator and independent or position-based IPS from #13 aren't implemented. Reproduce with:

```bash
python -m recarena.slate_estimators --slate-sizes 2 3 5 --horizons 1 20 --sizes 1000 5000 --repeats 200 --truth 500000
```

## What if hidden appeal follows what policies favor?

In the stress test, hidden item appeal is unrelated to anything a policy scores. Two settings, both off by default, link it: `appeal_quality_link` sets the correlation between appeal and item quality (from -1 to 1), and `appeal_sponsored_shift` adds to the appeal of sponsored items. Both reuse the same random draws, so with both at 0 every catalog is unchanged. `python -m recarena.linked_appeal` scores every built-in estimator in six worlds with the informed model. Full tables are in [`results/linked_appeal.md`](results/linked_appeal.md). What it found, with 5,000 sessions and 100 logged datasets per cell over 5 catalogs (mean error as a share of the true value, ± Monte Carlo standard error):

- **Linking appeal moved Direct's bias by a few points but didn't break it.** For "much greedier", Direct's mean error was +0.3% ± 0.2 with no hidden appeal and +3.4% ± 0.3 with unrelated appeal. It fell to -0.0% ± 0.3 when appeal followed quality and rose to +5.1% ± 0.3 when appeal ran against quality. For "pushes sponsored", it was +0.7% ± 0.3 with unrelated appeal and +2.3% ± 0.3 when sponsored items were more appealing.
- **Direct stayed the most accurate on far targets in every world** (RMSE under 6% of the true value, against 15% to 25% for SNPDIS and 22% or more for DR). A likely reason, not checked, is that the informed model already has quality and sponsorship as features, so it can absorb part of a link to them.
- **The weighted estimators don't depend on appeal, but their far target errors still moved between worlds** (SNPDIS mean error on "much greedier" from -2.6% ± 1.8 to -10.8% ± 1.5), because the true values and weights change with the world. This fits the heavy tailed weights in #24.

**Limits:** one link strength each (0.7 and a shift of 1), 5,000 sessions only, rewards only, and only the informed model. A link to something the model can't see, such as a hidden item feature that the target policy reads, would be a harder test. Reproduce with:

```bash
python -m recarena.linked_appeal --catalogs 5 --sizes 5000 --repeats 20 --truth 200000
```

## What if the logged probabilities are slightly wrong?

Every weighting estimator divides by the logging policy's probabilities, and `collect` records them exactly. Outside a simulator they are often estimated. `collect(..., logged_policy=other)` and `relog(logs, other)` record another policy's probabilities for the same sessions, and `recarena.propensity_error.fit_softmax_policy` fits a softmax policy to logged slates by maximum likelihood. `python -m recarena.propensity_error` scores every estimator with nine versions of the logged probabilities: exact, temperature 0.8 to 1.2 (the truth is 1), history weight 0.8 or 1.2 (the truth is 1), and policies fitted to the logs with all three features or with quality only. Full tables are in [`results/propensity_error.md`](results/propensity_error.md). What it found in the default world, with 100 datasets of 5,000 sessions (shift = estimate with wrong probabilities minus estimate with exact ones on the same data, in percent of the true value, ± Monte Carlo standard error):

- **A 10% temperature error moves near targets by a few points, and IPS most.** For "slightly different" with temperature 1.1, IPS shifted by +7.0% ± 0.0, PDIS by +3.3% ± 0.0 and SNPDIS by +1.5% ± 0.0. With temperature 1.2 the shifts were +16.5%, +7.4% and +3.0%. That is several times their RMSE with exact probabilities (1.4%), and it doesn't shrink with more data.
- **DR barely moved for near targets** (at most 0.3 points, in every row), as its "either the model or the weights can be right" property suggests. Direct uses no logged probabilities.
- **Far targets amplify a temperature error, for DR too.** For "much greedier", temperature 1.2 shifted SNPDIS by +5.5% ± 0.4, DR by +25.0% ± 17.8 and IPS by +68.1% ± 15.2. SNPDIS moved least among the estimators that use weights.
- **A wrong history weight hardly mattered** (at most 1.3 points), because the history term is small next to quality here. When fitted, the history weight was also the least precise (1.006 ± 0.139 across datasets, against 1.000 ± 0.010 for quality).
- **Fitting with the right features cost nothing measurable** (every shift within 0.3 points of 0). Leaving out history and sponsorship cost up to +9.1% ± 0.2 for IPS on "more personalized", and +0.3% for DR.
- **A free check flags most of these errors.** With exact probabilities each step's ratio averages to 1, so the per-session sum of (ratio - 1) should be near 0. Testing that at the 5% level flagged 95% to 100% of datasets for every temperature error and for the quality only fit, using the ratios of "same as logging", "slightly different" or "more personalized", and at most 5% with exact or correctly fitted probabilities. It flagged a 20% history weight error in only 23% to 27% of datasets, which fits how little that error moved the estimates.

**Limits:** one catalog, the default world and logging policy, 5,000 sessions, rewards only, and only errors in the policy's own form (a wrong temperature or weight, or a fitted softmax). DR here reuses each target's fitted model across the nine versions, so its numbers differ slightly from `estimate_all`'s DR, which refits. Interval coverage under wrong probabilities waits for #14. Reproduce with:

```bash
python -m recarena.propensity_error --sizes 5000 --repeats 100 --truth 300000
```

## How it's tested

The tests compare the simulator with values worked out by hand from every possible slate, check the estimators against hand-calculated answers, and confirm that doubly robust stays unbiased even with a deliberately wrong model.

## Where this is going

The goal is a shared, trustworthy place to answer: **which offline evaluation method can I trust, for which kind of recommender problem, and how would I know?**

| Stage | What it adds |
|---|---|
| Now | One simulator, six estimators, and a stress test |
| Next | Plug-in user models (estimators can already be plugged in), so anyone can benchmark their own world |
| Then | Harder worlds, trained RL agents, warnings for when not to trust an estimate |
| Later | Simulators calibrated to public datasets, and a public leaderboard of methods with reproducible results |
| Open question | Choosing policies under budgets and fairness limits when you can only estimate their effects |

This is a direction, not a promise. If you have a better idea, [open an issue](https://github.com/anveshachuri/recarena/issues). Contributions are welcome, and [CONTRIBUTING.md](CONTRIBUTING.md) explains how to start.

## License

Apache-2.0
