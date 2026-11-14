"""What if hidden appeal is related to what policies favor? (issue #9)

In the stress test, hidden item appeal is unrelated to anything a policy scores, so moving
toward quality or sponsored items doesn't change the hidden effect on average. This
experiment links appeal to item quality or to sponsorship and scores every built-in
estimator on the usual five targets, with the informed model.

python -m recarena.linked_appeal --catalogs 5 --sizes 5000 --repeats 20 --truth 200000
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace

import numpy as np

from .benchmark import target_policies
from .data import collect, true_value
from .estimators import available_estimators, estimate_all, resolve_estimators
from .policies import SoftmaxPolicy
from .simulator import Catalog, SimConfig


@dataclass(frozen=True)
class World:
    name: str
    hidden_appeal: float = 0.0
    appeal_quality_link: float = 0.0
    appeal_sponsored_shift: float = 0.0


WORLDS = (
    World("No hidden appeal"),
    World("Unrelated appeal (stress test)", hidden_appeal=1.0),
    World("Appeal follows quality", hidden_appeal=1.0, appeal_quality_link=0.7),
    World("Appeal against quality", hidden_appeal=1.0, appeal_quality_link=-0.7),
    World("Sponsored items more appealing", hidden_appeal=1.0, appeal_sponsored_shift=1.0),
    World("Sponsored items less appealing", hidden_appeal=1.0, appeal_sponsored_shift=-1.0),
)


def build_config(world: World, catalog_seed: int) -> SimConfig:
    return replace(
        SimConfig(),
        catalog_seed=catalog_seed,
        hidden_appeal=world.hidden_appeal,
        appeal_quality_link=world.appeal_quality_link,
        appeal_sponsored_shift=world.appeal_sponsored_shift,
    )


def truth_job(job):
    world, catalog_seed, policy_name, runs, seed = job
    config = build_config(world, catalog_seed)
    catalog = Catalog.generate(config)
    policy = next(p for p in target_policies(catalog) if p.name == policy_name)
    return (world.name, catalog_seed, policy_name), true_value(config, catalog, policy, runs, np.random.default_rng(seed))


def estimate_job(job):
    """One logged dataset, every target. Seeded per job, so worker count doesn't matter."""
    world, catalog_seed, n, seed, estimators = job
    config = build_config(world, catalog_seed)
    catalog = Catalog.generate(config)
    rng = np.random.default_rng(seed)
    data = collect(config, catalog, SoftmaxPolicy(catalog, "logging"), n, rng)
    out = {
        p.name: estimate_all(data, data.rewards, p, config.examine_decay, rng, estimators=estimators)
        for p in target_policies(catalog)
    }
    return (world.name, catalog_seed, n), out


def run(catalogs: int, sizes: list[int], repeats: int, truth_runs: int, seed: int, workers: int, estimators=None) -> str:
    estimators = resolve_estimators(estimators)
    names = list(estimators)
    targets = [p.name for p in target_policies(Catalog.generate(SimConfig()))]

    truth_keys = [(w, c, p) for w in WORLDS for c in range(catalogs) for p in targets]
    truth_seeds = np.random.SeedSequence([seed, 0]).spawn(len(truth_keys))
    cells = [(w, c, n) for w in WORLDS for c in range(catalogs) for n in sizes]
    job_seeds = np.random.SeedSequence([seed, 1]).spawn(len(cells) * repeats)
    jobs = [cell + (job_seeds[i * repeats + r], estimators) for i, cell in enumerate(cells) for r in range(repeats)]

    # Errors in percent of the true value, keyed by (world, n, target, estimator), pooled across catalogs.
    errors: dict[tuple, list[float]] = {}
    truth_se: list[float] = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(pool.map(truth_job, [(w, c, p, truth_runs, s) for (w, c, p), s in zip(truth_keys, truth_seeds)]))
        for (world_name, catalog_seed, n), out in pool.map(estimate_job, jobs):
            for p in targets:
                truth = truths[(world_name, catalog_seed, p)].reward
                for e in names:
                    errors.setdefault((world_name, n, p, e), []).append(100 * (out[p][e] - truth) / truth)
    for value in truths.values():
        truth_se.append(100 * value.reward_stderr / value.reward)

    def cell(key) -> str:
        x = np.asarray(errors[key])
        return f"{x.mean():+.1f} / {np.sqrt(np.mean(x**2)):.1f}"

    lines = [
        f"{catalogs} catalogs, {repeats} logged datasets per catalog and size, truth from {truth_runs:,} sessions per "
        f"policy, catalog and world. Informed model. Errors are percent of the true value, pooled across catalogs "
        f"({catalogs * repeats} datasets per cell). Cells show mean error / RMSE. The truth's own standard error is at "
        f"most {max(truth_se):.2f}% of the true value.",
        "",
        "| World | Hidden appeal | Link to quality | Sponsored shift |",
        "|---|---:|---:|---:|",
    ]
    lines += [
        f"| {w.name} | {w.hidden_appeal:g} | {w.appeal_quality_link:g} | {w.appeal_sponsored_shift:g} |" for w in WORLDS
    ]
    lines.append("")
    for n in sizes:
        for w in WORLDS:
            lines += [f"## {w.name} ({n:,} sessions)", ""]
            lines.append("| New policy | " + " | ".join(names) + " |")
            lines.append("|---|" + "---:|" * len(names))
            for p in targets:
                lines.append(f"| {p} | " + " | ".join(cell((w.name, n, p, e)) for e in names) + " |")
            lines.append("")

    largest = max(sizes)
    model_names = [e for e in ("Direct", "DR", "SNPDIS") if e in names]
    lines += [
        f"## Mean error by world ({largest:,} sessions)",
        "",
        "Mean error ± its Monte Carlo standard error, in percent of the true value. Catalogs differ, so part of "
        "the spread is between catalogs.",
        "",
    ]
    lines.append("| World | Estimator | " + " | ".join(targets) + " |")
    lines.append("|---|---|" + "---:|" * len(targets))
    for w in WORLDS:
        for e in model_names:
            cells_ = []
            for p in targets:
                x = np.asarray(errors[(w.name, largest, p, e)])
                cells_.append(f"{x.mean():+.1f} ± {x.std(ddof=1) / np.sqrt(len(x)):.1f}")
            lines.append(f"| {w.name} | {e} | " + " | ".join(cells_) + " |")
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
