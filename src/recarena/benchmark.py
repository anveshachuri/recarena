"""Score every estimator against true policy values.

python -m recarena.benchmark --sizes 200 1000 5000 --seeds 30 --truth 1000000
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .data import collect, true_value
from .estimators import available_estimators, estimate_all, resolve_estimators
from .policies import SoftmaxPolicy
from .simulator import Catalog, SimConfig


def target_policies(catalog: Catalog) -> list[SoftmaxPolicy]:
    return [
        SoftmaxPolicy(catalog, "same as logging", 1.0, 1.0, 0.0, 1.0),
        SoftmaxPolicy(catalog, "slightly different", 1.5, 1.2, 0.0, 1.0),
        SoftmaxPolicy(catalog, "more personalized", 4.0, 1.0, 0.0, 1.0),
        SoftmaxPolicy(catalog, "pushes sponsored", 1.0, 1.0, 1.5, 1.0),
        SoftmaxPolicy(catalog, "much greedier", 1.0, 1.0, 0.0, 0.25),
    ]


def score_one_dataset(job):
    """One logged dataset scored for every target. Seeded per job, so worker count doesn't matter."""
    config, catalog, behavior, targets, n, seed, estimators = job
    rng = np.random.default_rng(seed)
    data = collect(config, catalog, behavior, n, rng)
    return n, {
        p.name: (
            estimate_all(data, data.rewards, p, config.examine_decay, rng, estimators=estimators),
            estimate_all(data, data.costs, p, config.examine_decay, rng, estimators=estimators),
        )
        for p in targets
    }


def run(
    sizes: list[int],
    seeds: int,
    truth_runs: int,
    budget_ratio: float,
    seed: int,
    workers: int,
    estimators=None,
) -> str:
    """``estimators`` is a list of names, a name-to-function mapping, or None for the built-ins."""
    estimators = resolve_estimators(estimators)
    names = list(estimators)
    config = SimConfig()
    catalog = Catalog.generate(config)
    behavior = SoftmaxPolicy(catalog, "logging", 1.0, 1.0, 0.0, 1.0)
    rng = np.random.default_rng(seed)
    targets = target_policies(catalog)

    truths = {p.name: true_value(config, catalog, p, truth_runs, rng) for p in targets}
    behavior_truth = truths["same as logging"]
    budget = budget_ratio * behavior_truth.cost

    lines = [
        f"Catalog of {config.n_items} items, slates of {config.slate_size}, sessions up to {config.horizon} steps. "
        f"{seeds} repeats per cell, truth from {truth_runs:,} simulated sessions.",
        "",
        "## True values",
        "",
        "| Target policy | Reward | Sponsored exposure | Within budget? |",
        "|---|---:|---:|---|",
    ]
    for p in targets:
        t = truths[p.name]
        lines.append(
            f"| {p.name} | {t.reward:.3f} ± {t.reward_stderr:.3f} | {t.cost:.3f} ± {t.cost_stderr:.3f} | "
            f"{'yes' if t.cost <= budget else 'no'} |"
        )
    lines += ["", f"Budget: sponsored exposure of at most {budget:.3f}.", ""]

    errors = {(p.name, n, e): [] for p in targets for n in sizes for e in names}
    correct = {(p.name, n, e): 0 for p in targets for n in sizes for e in names}
    job_seeds = np.random.SeedSequence(seed).spawn(len(sizes) * seeds)
    jobs = [
        (config, catalog, behavior, targets, n, job_seeds[i * seeds + j], estimators)
        for i, n in enumerate(sizes)
        for j in range(seeds)
    ]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for n, results in pool.map(score_one_dataset, jobs):
            for p in targets:
                t = truths[p.name]
                rewards, costs = results[p.name]
                for e in names:
                    errors[(p.name, n, e)].append(rewards[e] - t.reward)
                    correct[(p.name, n, e)] += (costs[e] <= budget) == (t.cost <= budget)

    def table(title: str, cell) -> list[str]:
        out = [f"## {title}", ""]
        out.append("| Target policy | Sessions logged | " + " | ".join(names) + " |")
        out.append("|---|---:|" + "---:|" * len(names))
        for p in targets:
            for n in sizes:
                out.append(f"| {p.name} | {n:,} | " + " | ".join(cell(p, n, e) for e in names) + " |")
        return out + [""]

    def rmse(p, n, e) -> str:
        err = np.array(errors[(p.name, n, e)])
        return f"{100 * np.sqrt(np.mean(err**2)) / truths[p.name].reward:.1f}%"

    def bias(p, n, e) -> str:
        err = np.array(errors[(p.name, n, e)])
        return f"{100 * err.mean() / truths[p.name].reward:+.1f}%"

    def decision(p, n, e) -> str:
        return f"{100 * correct[(p.name, n, e)] / seeds:.0f}%"

    lines += table("Reward error (RMSE as a share of the true value, lower is better)", rmse)
    lines += table("Reward bias (average signed error)", bias)
    lines += table("Budget decisions (share of runs that correctly said whether the policy fits the budget)", decision)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[200, 1000, 5000])
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--truth", type=int, default=1_000_000)
    parser.add_argument("--budget-ratio", type=float, default=1.25, help="Budget as a multiple of the logging policy's cost")
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--output", default=None)
    parser.add_argument("--estimators", nargs="+", default=None, help=f"Default: all built-in. Available: {', '.join(available_estimators())}")
    args = parser.parse_args()
    start = time.time()
    report = run(args.sizes, args.seeds, args.truth, args.budget_ratio, args.seed, args.workers, args.estimators)
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
