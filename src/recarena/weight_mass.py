"""Is the mean session weight a warning sign for far targets? (issue #24)

Under the logging policy, the mean session weight (and the mean of the cumulative weights at
each step) has expectation exactly 1, so it can be checked from the logs alone. This logs
datasets in each stress test world, computes ``weight_diagnostics`` for every target, and
measures how the weighted estimators' errors relate to it, and how well "mean weight below a
threshold" flags a large error. Only the weighted estimators are run: the diagnostic is about
importance weights, and they need no fitted model, so worlds that differ only in the model
give the same numbers and are run once.

python -m recarena.weight_mass --catalogs 5 --size 5000 --repeats 40 --truth 200000
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
from .estimators import importance_ratios, ips, pdis, snips, snpdis, weight_diagnostics
from .policies import SoftmaxPolicy
from .simulator import Catalog, SimConfig
from .stress import FAR_TARGETS, SCENARIOS

NAMES = ("IPS", "SNIPS", "PDIS", "SNPDIS")
_FUNCTIONS = (ips, snips, pdis, snpdis)
LARGE_ERROR = 0.10  # An error above 10% of the true value counts as large.
THRESHOLDS = (0.5, 0.7, 0.9)
BINS = ((0.0, 0.5), (0.5, 0.9), (0.9, 1.1), (1.1, np.inf))


def worlds() -> list[tuple[float, float]]:
    """(hidden appeal, sponsored annoyance) of each stress test scenario, without repeats."""
    out = []
    for s in SCENARIOS:
        if (s.hidden_appeal, s.sponsored_annoyance) not in out:
            out.append((s.hidden_appeal, s.sponsored_annoyance))
    return out


def world_name(world: tuple[float, float]) -> str:
    return f"appeal {world[0]:g}, annoyance {world[1]:g}"


def build_config(world: tuple[float, float], catalog_seed: int) -> SimConfig:
    return replace(SimConfig(), catalog_seed=catalog_seed, hidden_appeal=world[0], sponsored_annoyance=world[1])


def truth_job(job):
    world, catalog_seed, policy_name, runs, seed = job
    config = build_config(world, catalog_seed)
    catalog = Catalog.generate(config)
    policy = next(p for p in target_policies(catalog) if p.name == policy_name)
    return (world, catalog_seed, policy_name), true_value(config, catalog, policy, runs, np.random.default_rng(seed))


def estimate_job(job):
    """One logged dataset: diagnostics and reward and cost estimates for every target. Seeded per job."""
    world, catalog_seed, n, seed = job
    config = build_config(world, catalog_seed)
    catalog = Catalog.generate(config)
    data = collect(config, catalog, SoftmaxPolicy(catalog, "logging"), n, np.random.default_rng(seed))
    out = {}
    for p in target_policies(catalog):
        ratios = importance_ratios(data, p)
        d = weight_diagnostics(ratios)
        reward = {e: f(data, data.rewards, ratios) for e, f in zip(NAMES, _FUNCTIONS)}
        cost = {e: f(data, data.costs, ratios) for e, f in zip(NAMES, _FUNCTIONS)}
        out[p.name] = (d.mean_session_weight, d.lowest_step_mean_weight, reward, cost)
    return (world, catalog_seed), out


def _share(x) -> str:
    return f"{100 * np.mean(x):.0f}%" if len(x) else "n/a"


def run(catalogs: int, size: int, repeats: int, truth_runs: int, seed: int, workers: int) -> str:
    all_worlds = worlds()
    targets = [p.name for p in target_policies(Catalog.generate(SimConfig()))]
    near = [p for p in targets if p not in FAR_TARGETS]

    truth_keys = [(w, c, p) for w in all_worlds for c in range(catalogs) for p in targets]
    truth_seeds = np.random.SeedSequence([seed, 0]).spawn(len(truth_keys))
    cells = [(w, c) for w in all_worlds for c in range(catalogs)]
    job_seeds = np.random.SeedSequence([seed, 1]).spawn(len(cells) * repeats)
    jobs = [cell + (size, job_seeds[i * repeats + r]) for i, cell in enumerate(cells) for r in range(repeats)]

    # One row per (dataset, target): world, target, mean weight, lowest step mean, errors as shares of the truth.
    rows = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(pool.map(truth_job, [k + (truth_runs, s) for k, s in zip(truth_keys, truth_seeds)]))
        for (world, catalog_seed), out in pool.map(estimate_job, jobs):
            for p in targets:
                m, lowest, reward, cost = out[p]
                truth = truths[(world, catalog_seed, p)]
                rows.append(
                    {
                        "world": world,
                        "target": p,
                        "m": m,
                        "lowest": lowest,
                        "reward": {e: (reward[e] - truth.reward) / truth.reward for e in NAMES},
                        "cost": {e: (cost[e] - truth.cost) / truth.cost for e in NAMES},
                    }
                )
    truth_se = max(max(v.reward_stderr / v.reward, v.cost_stderr / v.cost) for v in truths.values())

    lines = [
        f"Stress test worlds (hidden appeal and sponsored annoyance; the model doesn't matter here), {catalogs} "
        f"catalogs each, {repeats} logged datasets of {size:,} sessions per catalog and world from the default "
        f"logging policy. Truth from {truth_runs:,} sessions per policy, catalog and world (its standard error "
        f"is at most {100 * truth_se:.2f}% of the true value).",
        "",
        "The mean session weight is the mean over sessions of the product of the slate probability ratios. Its "
        "expectation is exactly 1 under the logging policy. The lowest step mean is the smallest, over steps, "
        "of the mean cumulative weight up to that step, which also has expectation 1 at every step.",
        "",
        "## Mean session weight by world and target",
        "",
        "| World | Target | Median | Mean | Below 1 | 10th percentile | Largest | Median lowest step mean |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for w in all_worlds:
        for p in targets:
            sel = [r for r in rows if r["world"] == w and r["target"] == p]
            m = np.array([r["m"] for r in sel])
            lowest = np.array([r["lowest"] for r in sel])
            lines.append(
                f"| {world_name(w)} | {p} | {np.median(m):.3f} | {m.mean():.3f} | {_share(m < 1)} | "
                f"{np.quantile(m, 0.1):.3f} | {m.max():.2f} | {np.median(lowest):.3f} |"
            )
    lines.append("")

    lines += [
        "## Signed reward error by mean session weight (all worlds pooled)",
        "",
        "Average signed error as a share of the true value, ± its standard error, and the number of datasets.",
        "",
        "| Target | Mean session weight | Datasets | " + " | ".join(NAMES) + " |",
        "|---|---|---:|" + "---:|" * len(NAMES),
    ]
    for p in targets:
        for lo, hi in BINS:
            sel = [r for r in rows if r["target"] == p and lo <= r["m"] < hi]
            if not sel:
                continue
            label = f"below {hi:g}" if lo == 0 else (f"{lo:g} or more" if hi == np.inf else f"{lo:g} to {hi:g}")
            cells_ = []
            for e in NAMES:
                err = np.array([r["reward"][e] for r in sel])
                se = err.std(ddof=1) / np.sqrt(len(err)) if len(err) > 1 else float("nan")
                cells_.append(f"{100 * err.mean():+.1f}% ± {100 * se:.1f}")
            lines.append(f"| {p} | {label} | {len(sel)} | " + " | ".join(cells_) + " |")
    lines.append("")

    far_rows = [r for r in rows if r["target"] in FAR_TARGETS]
    near_rows = [r for r in rows if r["target"] in near]
    flags = [(f"mean session weight below {t:g}", "m", t) for t in THRESHOLDS] + [
        (f"lowest step mean below {t:g}", "lowest", t) for t in THRESHOLDS
    ]
    lines += [
        f"## How well a low weight flags a large error (far targets, all worlds pooled, {len(far_rows)} estimates)",
        "",
        f"A large error is one above {100 * LARGE_ERROR:.0f}% of the true value. Flagged: share of datasets the "
        "flag fires on. Large if flagged / if not: share of large errors among flagged and unflagged datasets. "
        "Caught: share of large errors the flag fires on. False alarms: share of datasets without a large "
        "error that the flag fires on.",
        "",
    ]
    for kind in ("reward", "cost"):
        for e in NAMES:
            large = np.array([abs(r[kind][e]) > LARGE_ERROR for r in far_rows])
            lines += [
                f"### {e}, {kind} (large error in {_share(large)} of datasets)",
                "",
                "| Flag | Flagged | Large if flagged | Large if not | Caught | False alarms |",
                "|---|---:|---:|---:|---:|---:|",
            ]
            for label, key, t in flags:
                fired = np.array([r[key] < t for r in far_rows])
                lines.append(
                    f"| {label} | {_share(fired)} | {_share(large[fired])} | {_share(large[~fired])} | "
                    f"{_share(fired[large])} | {_share(fired[~large])} |"
                )
            lines.append("")

    lines += [
        f"## How often each flag fires on near targets ({', '.join(near)}; {len(near_rows)} datasets)",
        "",
        "| Flag | Fires |",
        "|---|---:|",
    ]
    for label, key, t in flags:
        lines.append(f"| {label} | {_share(np.array([r[key] < t for r in near_rows]))} |")
    near_large = np.array([abs(r["reward"]["PDIS"]) > LARGE_ERROR for r in near_rows])
    lines += ["", f"PDIS's reward error was large in {_share(near_large)} of these datasets.", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogs", type=int, default=5)
    parser.add_argument("--size", type=int, default=5000)
    parser.add_argument("--repeats", type=int, default=40)
    parser.add_argument("--truth", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    start = time.time()
    report = run(args.catalogs, args.size, args.repeats, args.truth, args.seed, args.workers)
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
