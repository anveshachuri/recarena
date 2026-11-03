"""Stress test: does an estimator's result survive a model and world it wasn't built for?

python -m recarena.stress --sizes 1000 5000 --catalogs 5 --repeats 6 --truth 500000
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace

import numpy as np

from .benchmark import target_policies
from .data import TrueValue, collect, true_value
from .estimators import ESTIMATOR_NAMES, estimate_all
from .policies import SoftmaxPolicy
from .simulator import Catalog, SimConfig

BUDGET_MARGIN = 0.10
FAR_TARGETS = ("pushes sponsored", "much greedier")


@dataclass(frozen=True)
class Scenario:
    name: str
    hidden_appeal: float = 0.0
    sponsored_annoyance: float = 0.0
    informed_model: bool = True


SCENARIOS = (
    Scenario("Baseline: informed model"),
    Scenario("Uninformed model", informed_model=False),
    Scenario("Hidden item appeal", hidden_appeal=1.0),
    Scenario("Sponsored items drive users away", sponsored_annoyance=0.3),
    Scenario("All of the above", hidden_appeal=1.0, sponsored_annoyance=0.3, informed_model=False),
)


def budget_decisions_correct(estimated_cost: float, true_cost: float, margin: float = BUDGET_MARGIN) -> int:
    """Tests two budgets just either side of the true cost. Returns how many of the two were right."""
    fits_loose_budget = estimated_cost <= true_cost * (1 + margin)
    fits_tight_budget = estimated_cost <= true_cost * (1 - margin)
    return int(fits_loose_budget) + int(not fits_tight_budget)


def build_config(scenario: Scenario, catalog_seed: int) -> SimConfig:
    return replace(
        SimConfig(),
        catalog_seed=catalog_seed,
        hidden_appeal=scenario.hidden_appeal,
        sponsored_annoyance=scenario.sponsored_annoyance,
    )


def truth_job(job) -> tuple[tuple, TrueValue]:
    world, catalog_seed, policy_name, runs, seed = job
    config = replace(SimConfig(), catalog_seed=catalog_seed, hidden_appeal=world[0], sponsored_annoyance=world[1])
    catalog = Catalog.generate(config)
    policy = next(p for p in target_policies(catalog) if p.name == policy_name)
    value = true_value(config, catalog, policy, runs, np.random.default_rng(seed))
    return (world, catalog_seed, policy_name), value


def estimate_job(job) -> tuple[tuple, dict]:
    scenario, catalog_seed, n, seed = job
    config = build_config(scenario, catalog_seed)
    catalog = Catalog.generate(config)
    rng = np.random.default_rng(seed)
    data = collect(config, catalog, SoftmaxPolicy(catalog, "logging"), n, rng)
    results = {}
    for p in target_policies(catalog):
        rewards = estimate_all(data, data.rewards, p, config.examine_decay, rng, scenario.informed_model)
        costs = estimate_all(data, data.costs, p, config.examine_decay, rng, scenario.informed_model)
        results[p.name] = (rewards, costs)
    return (scenario.name, catalog_seed, n), results


def run(sizes: list[int], catalogs: int, repeats: int, truth_runs: int, seed: int, workers: int) -> str:
    worlds = sorted({(s.hidden_appeal, s.sponsored_annoyance) for s in SCENARIOS})
    policy_names = [p.name for p in target_policies(Catalog.generate(SimConfig()))]
    root = np.random.SeedSequence(seed)
    truth_keys = [(w, c, p) for w in worlds for c in range(catalogs) for p in policy_names]
    estimate_keys = [(s, c, n) for s in SCENARIOS for c in range(catalogs) for n in sizes for _ in range(repeats)]
    truth_seeds, estimate_seeds = root.spawn(2)

    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(
            pool.map(
                truth_job,
                [(*key, truth_runs, s) for key, s in zip(truth_keys, truth_seeds.spawn(len(truth_keys)))],
            )
        )
        rows = []
        jobs = [(*key, s) for key, s in zip(estimate_keys, estimate_seeds.spawn(len(estimate_keys)))]
        for (name, catalog_seed, n), results in pool.map(estimate_job, jobs):
            scenario = next(s for s in SCENARIOS if s.name == name)
            world = (scenario.hidden_appeal, scenario.sponsored_annoyance)
            for policy_name, (rewards, costs) in results.items():
                truth = truths[(world, catalog_seed, policy_name)]
                for e in ESTIMATOR_NAMES:
                    rows.append(
                        (
                            name,
                            catalog_seed,
                            n,
                            policy_name,
                            e,
                            100 * (rewards[e] - truth.reward) / truth.reward,
                            budget_decisions_correct(costs[e], truth.cost),
                        )
                    )

    def select(**where) -> list[tuple]:
        fields = ("scenario", "catalog", "n", "policy", "estimator")
        return [r for r in rows if all(r[fields.index(k)] == v for k, v in where.items())]

    def rmse(subset) -> float:
        return float(np.sqrt(np.mean(np.square([r[5] for r in subset]))))

    def median_error(subset) -> float:
        return float(np.median(np.abs([r[5] for r in subset])))

    largest = max(sizes)
    lines = [
        f"{catalogs} catalogs, {repeats} logged datasets per catalog and size, truth from {truth_runs:,} sessions per "
        f"policy and catalog. Errors are percent of the true value. Cells show median error / RMSE.",
        "",
    ]
    for s in SCENARIOS:
        lines += [f"## {s.name} ({largest:,} sessions)", ""]
        lines.append("| New policy | " + " | ".join(ESTIMATOR_NAMES) + " |")
        lines.append("|---|" + "---:|" * len(ESTIMATOR_NAMES))
        for p in policy_names:
            cells = [
                (lambda sub: f"{median_error(sub):.1f} / {rmse(sub):.1f}")(
                    select(scenario=s.name, n=largest, policy=p, estimator=e)
                )
                for e in ESTIMATOR_NAMES
            ]
            lines.append(f"| {p} | " + " | ".join(cells) + " |")
        lines.append("")

    lines += ["## Far-from-logging policies at each size (RMSE, pooled across catalogs)", ""]
    lines.append("| Scenario | Sessions | " + " | ".join(ESTIMATOR_NAMES) + " |")
    lines.append("|---|---:|" + "---:|" * len(ESTIMATOR_NAMES))
    for s in SCENARIOS:
        for n in sizes:
            cells = []
            for e in ESTIMATOR_NAMES:
                subset = [r for r in select(scenario=s.name, n=n, estimator=e) if r[3] in FAR_TARGETS]
                cells.append(f"{rmse(subset):.1f}")
            lines.append(f"| {s.name} | {n:,} | " + " | ".join(cells) + " |")
    lines.append("")

    lines += [f"## Far-from-logging RMSE for each catalog ({largest:,} sessions)", ""]
    lines.append("| Scenario | Estimator | " + " | ".join(f"Catalog {c}" for c in range(catalogs)) + " |")
    lines.append("|---|---|" + "---:|" * catalogs)
    for s in SCENARIOS:
        for e in ("SNPDIS", "Direct", "DR"):
            cells = []
            for c in range(catalogs):
                subset = [r for r in select(scenario=s.name, catalog=c, n=largest, estimator=e) if r[3] in FAR_TARGETS]
                cells.append(f"{rmse(subset):.1f}")
            lines.append(f"| {s.name} | {e} | " + " | ".join(cells) + " |")
    lines.append("")

    lines += [
        f"## Tight budget decisions ({largest:,} sessions)",
        "",
        f"Each estimate is tested against budgets {BUDGET_MARGIN:.0%} above and below the true cost. "
        "The table shows the share of decisions that were right. 50% is what a method gets if it always answers the same way.",
        "",
    ]
    lines.append("| Scenario | New policies | " + " | ".join(ESTIMATOR_NAMES) + " |")
    lines.append("|---|---|" + "---:|" * len(ESTIMATOR_NAMES))
    for s in SCENARIOS:
        for label, keep in (("Near", lambda p: p not in FAR_TARGETS), ("Far", lambda p: p in FAR_TARGETS)):
            cells = []
            for e in ESTIMATOR_NAMES:
                subset = [r for r in select(scenario=s.name, n=largest, estimator=e) if keep(r[3])]
                cells.append(f"{100 * np.mean([r[6] for r in subset]) / 2:.0f}%")
            lines.append(f"| {s.name} | {label} | " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 5000])
    parser.add_argument("--catalogs", type=int, default=5)
    parser.add_argument("--repeats", type=int, default=6)
    parser.add_argument("--truth", type=int, default=500_000)
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    start = time.time()
    report = run(args.sizes, args.catalogs, args.repeats, args.truth, args.seed, args.workers)
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
