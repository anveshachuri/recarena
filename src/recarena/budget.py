"""Safer budget decisions: false approvals, false rejections, and deciding with an upper bound (issue #16).

The stress test approves a policy for a budget when its estimated cost is at most the budget,
and scores right and wrong answers together. The two mistakes cost different things: a false
approval lets a policy break its budget, a false rejection only passes up a good one. This
experiment counts them separately, and also decides with a one-sided upper bound on cost,
estimate + z * standard error, for several confidence levels. The standard error is the
plug-in one from each estimator's per-session influence values (a normal interval). Direct
reports none (issue #22), so it only has the point estimate row.

python -m recarena.budget --catalogs 5 --sizes 5000 --repeats 20 --truth 200000
"""

from __future__ import annotations

import argparse
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor
from statistics import NormalDist

import numpy as np

from .benchmark import target_policies
from .data import collect, true_value
from .estimators import available_estimators, estimate_all_detailed, resolve_estimators
from .policies import SoftmaxPolicy
from .simulator import Catalog, SimConfig
from .stress import BUDGET_MARGIN, FAR_TARGETS, SCENARIOS, Scenario, build_config

# One-sided confidence levels for the upper bound. 0.5 is the point estimate (z = 0).
LEVELS = (0.5, 0.8, 0.9, 0.95, 0.99)


def upper_bound(estimated_cost: float, standard_error: float, level: float) -> float:
    """One-sided normal upper bound. At level 0.5 it is the estimate itself, even without a standard error."""
    if not 0.5 <= level < 1:
        raise ValueError(f"level must be in [0.5, 1), got {level}")
    if level == 0.5:
        return float(estimated_cost)
    return float(estimated_cost + NormalDist().inv_cdf(level) * standard_error)


def budget_errors(bound: float, true_cost: float, margin: float = BUDGET_MARGIN) -> tuple[bool, bool]:
    """Approve a budget when ``bound`` is at most the budget, for budgets ``margin`` below and above the true cost.

    Returns (false approval, false rejection): approving the tight budget the policy breaks, and
    rejecting the loose budget it fits. With the point estimate as ``bound``, the number of right
    answers is the stress test's ``budget_decisions_correct``.
    """
    false_approval = bound <= true_cost * (1 - margin)
    false_rejection = not bound <= true_cost * (1 + margin)
    return bool(false_approval), bool(false_rejection)


def truth_job(job):
    scenario, catalog_seed, policy_name, runs, seed = job
    config = build_config(scenario, catalog_seed)
    catalog = Catalog.generate(config)
    policy = next(p for p in target_policies(catalog) if p.name == policy_name)
    world = (scenario.hidden_appeal, scenario.sponsored_annoyance)
    return (world, catalog_seed, policy_name), true_value(config, catalog, policy, runs, np.random.default_rng(seed))


def estimate_job(job):
    """One logged dataset, cost estimates and standard errors for every target. Seeded per job."""
    scenario, catalog_seed, n, seed, estimators = job
    config = build_config(scenario, catalog_seed)
    catalog = Catalog.generate(config)
    rng = np.random.default_rng(seed)
    data = collect(config, catalog, SoftmaxPolicy(catalog, "logging"), n, rng)
    out = {}
    for p in target_policies(catalog):
        detailed = estimate_all_detailed(
            data, data.costs, p, config.examine_decay, rng, scenario.informed_model, estimators
        )
        out[p.name] = {e: (r.value, r.standard_error()) for e, r in detailed.items()}
    return (scenario.name, catalog_seed, n), out


def run(catalogs: int, sizes: list[int], repeats: int, truth_runs: int, seed: int, workers: int, estimators=None) -> str:
    estimators = resolve_estimators(estimators)
    names = list(estimators)
    targets = [p.name for p in target_policies(Catalog.generate(SimConfig()))]

    # Scenarios that differ only in the model share a world, and so share true values.
    worlds: dict[tuple, Scenario] = {}
    for s in SCENARIOS:
        worlds.setdefault((s.hidden_appeal, s.sponsored_annoyance), s)
    truth_keys = [(s, c, p) for s in worlds.values() for c in range(catalogs) for p in targets]
    truth_seeds = np.random.SeedSequence([seed, 0]).spawn(len(truth_keys))
    cells = [(s, c, n) for s in SCENARIOS for c in range(catalogs) for n in sizes]
    job_seeds = np.random.SeedSequence([seed, 1]).spawn(len(cells) * repeats)
    jobs = [cell + (job_seeds[i * repeats + r], estimators) for i, cell in enumerate(cells) for r in range(repeats)]

    # (scenario, n, target, estimator, level) -> list of (false approval, false rejection, true cost above bound)
    outcomes: dict[tuple, list[tuple[bool, bool, bool]]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(pool.map(truth_job, [(s, c, p, truth_runs, js) for (s, c, p), js in zip(truth_keys, truth_seeds)]))
        for (name, catalog_seed, n), out in pool.map(estimate_job, jobs):
            scenario = next(s for s in SCENARIOS if s.name == name)
            world = (scenario.hidden_appeal, scenario.sponsored_annoyance)
            for p in targets:
                true_cost = truths[(world, catalog_seed, p)].cost
                for e in names:
                    value, se = out[p][e]
                    for level in LEVELS:
                        bound = upper_bound(value, se, level)
                        if math.isnan(bound):
                            continue
                        fa, fr = budget_errors(bound, true_cost)
                        outcomes.setdefault((name, n, p, e, level), []).append((fa, fr, true_cost > bound))
    truth_se = max(100 * v.cost_stderr / v.cost for v in truths.values())

    def pooled(scenario_name, n, keep, e, level):
        rows = []
        for p in targets:
            if keep(p):
                rows += outcomes.get((scenario_name, n, p, e, level), [])
        return np.asarray(rows, dtype=float).reshape(-1, 3)

    def far(p):
        return p in FAR_TARGETS

    def near(p):
        return p not in FAR_TARGETS

    level_names = ["point" if lv == 0.5 else f"{lv:.0%}" for lv in LEVELS]
    datasets = catalogs * repeats
    lines = [
        f"{catalogs} catalogs, {repeats} logged datasets per catalog and size, truth from {truth_runs:,} sessions per "
        f"policy, catalog and world. Budgets are {BUDGET_MARGIN:.0%} below and above each policy's true cost. A policy "
        "is approved for a budget when the upper bound on its estimated cost is at most the budget. The upper bound is "
        "the estimate plus z standard errors (one-sided normal interval at the given level), and \"point\" is the "
        "estimate itself, as in the stress test.",
        "",
        "- **False approval:** approving the budget 10% below the true cost, which the policy breaks.",
        "- **False rejection:** rejecting the budget 10% above the true cost, which the policy fits.",
        "- **Above bound:** the true cost is above the upper bound.",
        "",
        f"Each far cell pools {2 * datasets} decisions per budget ({len(FAR_TARGETS)} far targets, {datasets} datasets), "
        f"so a rate's Monte Carlo standard error is at most {100 * 0.5 / math.sqrt(2 * datasets):.1f} points. The truth's "
        f"own standard error is at most {truth_se:.2f}% of the true cost. Direct reports no standard error, so it only "
        "has the point row.",
        "",
    ]
    for n in sizes:
        lines += [f"## Far targets: false approvals / false rejections ({n:,} sessions)", ""]
        lines.append("| Scenario | Estimator | " + " | ".join(level_names) + " |")
        lines.append("|---|---|" + "---:|" * len(LEVELS))
        for s in SCENARIOS:
            for e in names:
                row = []
                for level in LEVELS:
                    x = pooled(s.name, n, far, e, level)
                    row.append(f"{100 * x[:, 0].mean():.0f}% / {100 * x[:, 1].mean():.0f}%" if len(x) else "n/a")
                lines.append(f"| {s.name} | {e} | " + " | ".join(row) + " |")
        lines.append("")

        lines += [f"## Far targets: true cost above the upper bound ({n:,} sessions)", ""]
        lines.append("A level's bound should be exceeded in about (1 - level) of datasets if the interval is right.")
        lines.append("")
        lines.append("| Scenario | Estimator | " + " | ".join(level_names) + " |")
        lines.append("|---|---|" + "---:|" * len(LEVELS))
        for s in SCENARIOS:
            for e in names:
                row = []
                for level in LEVELS:
                    x = pooled(s.name, n, far, e, level)
                    row.append(f"{100 * x[:, 2].mean():.0f}%" if len(x) else "n/a")
                lines.append(f"| {s.name} | {e} | " + " | ".join(row) + " |")
        lines.append("")

        lines += [f"## Near targets: false approvals / false rejections ({n:,} sessions)", ""]
        lines.append("| Scenario | Estimator | " + " | ".join(level_names) + " |")
        lines.append("|---|---|" + "---:|" * len(LEVELS))
        for s in SCENARIOS:
            for e in names:
                row = []
                for level in LEVELS:
                    x = pooled(s.name, n, near, e, level)
                    row.append(f"{100 * x[:, 0].mean():.0f}% / {100 * x[:, 1].mean():.0f}%" if len(x) else "n/a")
                lines.append(f"| {s.name} | {e} | " + " | ".join(row) + " |")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogs", type=int, default=5)
    parser.add_argument("--sizes", type=int, nargs="+", default=[5000])
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--truth", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--output", default=None)
    parser.add_argument("--estimators", nargs="+", default=None, help=f"Default: all built-in. Available: {', '.join(available_estimators())}")
    args = parser.parse_args()
    start = time.time()
    report = run(args.catalogs, args.sizes, args.repeats, args.truth, args.seed, args.workers, args.estimators)
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
