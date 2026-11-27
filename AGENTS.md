# Guide for coding agents

Follow [CONTRIBUTING.md](CONTRIBUTING.md). It applies to you, including its AI rules. The person you work for is responsible for your PR.

## Commands

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m recarena.benchmark --sizes 200 --seeds 2 --truth 50000   # Quick check
```

The full stress test takes a long time. Don't run it unless the task needs it.

## Layout

| File | Purpose |
|---|---|
| `src/recarena/simulator.py` | Batched users and catalog, the source of truth for behavior |
| `src/recarena/env.py` | Gymnasium wrapper around a batch of one |
| `src/recarena/policies.py` | Slate policies with exact probabilities |
| `src/recarena/data.py` | Logging sessions and measuring true values |
| `src/recarena/estimators.py` | Off-policy estimators and fitted Q evaluation |
| `src/recarena/benchmark.py`, `stress.py` | Scoring estimators against true values |
| `src/recarena/exploration.py` | How the logging policy's exploration level changes estimator error (#17) |
| `src/recarena/slate_estimators.py` | Slate-aware estimators (cascade, independent IPS) against plain per-decision IS, for rewards and costs (#13, #27) |
| `src/recarena/linked_appeal.py` | Hidden appeal linked to quality or sponsorship (#9) |
| `src/recarena/propensity_error.py` | Estimators when the logged probabilities are slightly wrong or fitted from the logs (#20) |
| `src/recarena/propensity_check.py` | Which probe policies make the wrong-probability check reliable, including a score test (#29) |
| `src/recarena/budget.py` | False approvals and false rejections of budgets, and deciding with an upper bound on cost (#16) |
| `src/recarena/weight_mass.py` | The mean session weight as a warning sign for far targets (#24) |
| `src/recarena/late_steps.py` | Per-decision error split by step, and discounting against truncating the session (#31) |
| `tests/test_recarena.py` | Hand calculations and statistical checks |

## Rules that are easy to break

- Policies and fitted models must not read `Catalog.appeal` or any hidden user state. That is what makes the problem hard.
- `importance_ratios` must stay 1 after a session ends, because the weighted estimators depend on it.
- New simulator settings must default to off and leave existing results unchanged.
- Statistical tests must use a fixed seed, and their tolerance should come from a standard error.
- Run a new test against the old code and confirm that it fails.
- Report only what you ran. If a result comes from a small sample, say so.
- Don't change numbers in `results/` by hand. Regenerate them with the command in the README.
