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

The second part of an `Estimate` is each session's influence on the estimate. Confidence intervals are built from it, and every built-in estimator provides it. The benchmark and stress test take `--estimators` to choose which to run. To use your own estimator there, pass the function itself to `run(..., estimators={"Clipped IPS": clipped_ips})` from a module it can be imported from.

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

**Limits of these results:** this is one simulator with settings chosen by its author, and the hidden effects used here may be too mild. The hidden appeal, for example, isn't related to anything the policies favor. The large errors are also noisy with this few runs. These results need more scenarios and independent checking.

Full tables are in [`results/stress_test.md`](results/stress_test.md), and an earlier single-catalog run is in [`results/first_benchmark.md`](results/first_benchmark.md). Reproduce the stress test with:

```bash
python -m recarena.stress --sizes 1000 5000 --catalogs 5 --repeats 10 --truth 500000
```

If it runs slowly, set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` first, because it already runs one job per CPU core.

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
