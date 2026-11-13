"""Do slate-aware estimators help, and where? (issue #13)

Scores the cascade estimators against plain per-decision importance sampling across
slate sizes, session lengths and the usual five target policies. Only the weighted
estimators are run, since the comparison is about importance weights.

python -m recarena.slate_estimators --slate-sizes 2 3 5 --horizons 1 20 --sizes 1000 5000 --repeats 100 --truth 500000
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace

import numpy as np

from .benchmark import target_policies
from .data import collect, true_value
from .estimators import estimate_all
from .policies import SoftmaxPolicy
from .simulator import Catalog, SimConfig

NAMES = ("PDIS", "SNPDIS", "CascadePDIS", "SNCascadePDIS")


def world(slate_size: int, horizon: int) -> SimConfig:
    return replace(SimConfig(), slate_size=slate_size, horizon=horizon)


def truth_job(job):
    slate_size, horizon, policy_name, runs, seed = job
    config = world(slate_size, horizon)
    catalog = Catalog.generate(config)
    policy = next(p for p in target_policies(catalog) if p.name == policy_name)
    return (slate_size, horizon, policy_name), true_value(config, catalog, policy, runs, np.random.default_rng(seed))


def estimate_job(job):
    """One logged dataset, every target. Seeded per job, so worker count doesn't matter."""
    slate_size, horizon, n, seed = job
    config = world(slate_size, horizon)
    catalog = Catalog.generate(config)
    rng = np.random.default_rng(seed)
    data = collect(config, catalog, SoftmaxPolicy(catalog, "logging"), n, rng)
    out = {
        p.name: estimate_all(data, data.rewards, p, config.examine_decay, rng, estimators=NAMES)
        for p in target_policies(catalog)
    }
    return (slate_size, horizon, n), out


def run(slate_sizes: list[int], horizons: list[int], sizes: list[int], repeats: int, truth_runs: int, seed: int, workers: int) -> str:
    worlds = [(k, h) for k in slate_sizes for h in horizons]
    targets = [p.name for p in target_policies(Catalog.generate(SimConfig()))]
    names = list(NAMES)

    truth_keys = [(k, h, p) for k, h in worlds for p in targets]
    truth_seeds = np.random.SeedSequence([seed, 0]).spawn(len(truth_keys))
    cells = [(k, h, n) for k, h in worlds for n in sizes]
    job_seeds = np.random.SeedSequence([seed, 1]).spawn(len(cells) * repeats)
    jobs = [cell + (job_seeds[i * repeats + r],) for i, cell in enumerate(cells) for r in range(repeats)]

    errors = {cell + (p, e): [] for cell in cells for p in targets for e in names}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(pool.map(truth_job, [key + (truth_runs, s) for key, s in zip(truth_keys, truth_seeds)]))
        for cell, out in pool.map(estimate_job, jobs):
            for p in targets:
                for e in names:
                    errors[cell + (p, e)].append(out[p][e] - truths[cell[:2] + (p,)].reward)

    def rmse_share(key) -> str:
        """RMSE as a share of the true value, ± its Monte Carlo standard error (delta method)."""
        sq = np.square(errors[key])
        rmse = np.sqrt(sq.mean())
        se = sq.std(ddof=1) / np.sqrt(len(sq)) / (2 * rmse) if rmse > 0 else 0.0
        truth = truths[key[:2] + (key[3],)].reward
        return f"{100 * rmse / truth:.1f}% ± {100 * se / truth:.1f}"

    def bias_share(key) -> str:
        err = np.asarray(errors[key])
        truth = truths[key[:2] + (key[3],)].reward
        return f"{100 * err.mean() / truth:+.1f}% ± {100 * err.std(ddof=1) / np.sqrt(len(err)) / truth:.1f}"

    base = SimConfig()
    lines = [
        f"Default world except slate size and session length: catalog of {base.n_items} items, one catalog "
        f"(seed {base.catalog_seed}), logging policy at temperature 1, no fitted models. "
        f"{repeats} logged datasets per cell, truth from {truth_runs:,} simulated sessions per policy and world.",
        "",
        "CascadePDIS weights a reward in slot j of step t by the full slate ratios of earlier steps times the ratio "
        "of only the first j slots at step t. It is unbiased here because users read top down and stop at their "
        "first click. SNCascadePDIS normalizes the weights for each step and slot.",
        "",
        "## True values",
        "",
        "| Slate size | Session length | " + " | ".join(targets) + " |",
        "|---:|---:|" + "---:|" * len(targets),
    ]
    for k, h in worlds:
        lines.append(f"| {k} | {h} | " + " | ".join(f"{truths[(k, h, p)].reward:.4f}" for p in targets) + " |")
    lines.append("")

    for title, cell_fn in (
        ("Reward error (RMSE as a share of the true value, ± Monte Carlo standard error)", rmse_share),
        ("Reward bias (average signed error as a share of the true value, ± standard error)", bias_share),
    ):
        lines += [f"## {title}", ""]
        for k, h in worlds:
            for n in sizes:
                lines += [f"### Slates of {k}, sessions up to {h} steps, {n:,} sessions logged", ""]
                lines.append("| Target policy | " + " | ".join(names) + " |")
                lines.append("|---|" + "---:|" * len(names))
                for p in targets:
                    lines.append(f"| {p} | " + " | ".join(cell_fn((k, h, n, p, e)) for e in names) + " |")
                lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slate-sizes", type=int, nargs="+", default=[2, 3, 5])
    parser.add_argument("--horizons", type=int, nargs="+", default=[1, 20])
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 5000])
    parser.add_argument("--repeats", type=int, default=100)
    parser.add_argument("--truth", type=int, default=500_000)
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    start = time.time()
    report = run(args.slate_sizes, args.horizons, args.sizes, args.repeats, args.truth, args.seed, args.workers)
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
