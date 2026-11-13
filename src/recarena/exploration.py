"""How much exploration does a logging policy need? (issue #17)

Logs data with logging policies that explore more or less, then scores every estimator
on the same target policies. Also reports the reward each logging policy gives up to
explore, and whether effective sample size tracks the error.

python -m recarena.exploration --sizes 1000 5000 --repeats 30 --truth 500000
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .benchmark import target_policies
from .data import collect, true_value
from .estimators import ESTIMATOR_NAMES, EstimationTask, estimate_all
from .policies import SoftmaxPolicy, UniformMixturePolicy
from .simulator import Catalog, SimConfig


def logging_policies(catalog: Catalog) -> list:
    """The default logging policy, softer and sharper versions of it, and uniform mixtures."""
    default = SoftmaxPolicy(catalog, "temperature 1 (default)", 1.0, 1.0, 0.0, 1.0)
    return [
        SoftmaxPolicy(catalog, "temperature 0.5", 1.0, 1.0, 0.0, 0.5),
        default,
        SoftmaxPolicy(catalog, "temperature 2", 1.0, 1.0, 0.0, 2.0),
        SoftmaxPolicy(catalog, "temperature 4", 1.0, 1.0, 0.0, 4.0),
        UniformMixturePolicy(default, 0.1, "default + 10% uniform"),
        UniformMixturePolicy(default, 0.3, "default + 30% uniform"),
    ]


def effective_sample_share(weights: np.ndarray) -> float:
    """Kish effective sample size of the session weights, as a share of the sessions logged."""
    return float(weights.sum() ** 2 / np.sum(weights**2) / len(weights))


def truth_job(job):
    config, catalog, policy, runs, seed = job
    return policy.name, true_value(config, catalog, policy, runs, np.random.default_rng(seed))


def estimate_job(job):
    """One logged dataset, every target. Seeded per job, so worker count doesn't matter."""
    config, catalog, behavior, targets, n, seed = job
    rng = np.random.default_rng(seed)
    data = collect(config, catalog, behavior, n, rng)
    out = {}
    for p in targets:
        weights = EstimationTask(data, data.rewards, p, config.examine_decay, rng).ratios.prod(axis=1)
        out[p.name] = (estimate_all(data, data.rewards, p, config.examine_decay, rng), effective_sample_share(weights))
    return behavior.name, n, out


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])


def run(sizes: list[int], repeats: int, truth_runs: int, seed: int, workers: int) -> str:
    config = SimConfig()
    catalog = Catalog.generate(config)
    loggers = logging_policies(catalog)
    targets = target_policies(catalog)
    names = list(ESTIMATOR_NAMES)

    truth_policies = targets + loggers
    truth_seeds = np.random.SeedSequence([seed, 0]).spawn(len(truth_policies))
    job_seeds = np.random.SeedSequence([seed, 1]).spawn(len(loggers) * len(sizes) * repeats)
    jobs = [
        (config, catalog, b, targets, n, job_seeds[(i * len(sizes) + j) * repeats + r])
        for i, b in enumerate(loggers)
        for j, n in enumerate(sizes)
        for r in range(repeats)
    ]
    errors = {(b.name, n, p.name, e): [] for b in loggers for n in sizes for p in targets for e in names}
    ess = {(b.name, n, p.name): [] for b in loggers for n in sizes for p in targets}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(pool.map(truth_job, [(config, catalog, p, truth_runs, s) for p, s in zip(truth_policies, truth_seeds)]))
        for b_name, n, out in pool.map(estimate_job, jobs):
            for p in targets:
                estimates, share = out[p.name]
                ess[(b_name, n, p.name)].append(share)
                for e in names:
                    errors[(b_name, n, p.name, e)].append(estimates[e] - truths[p.name].reward)

    def rmse_share(key) -> tuple[float, float]:
        """RMSE as a share of the true value, and its Monte Carlo standard error (delta method)."""
        sq = np.square(errors[key])
        rmse = np.sqrt(sq.mean())
        se = sq.std(ddof=1) / np.sqrt(len(sq)) / (2 * rmse) if rmse > 0 else 0.0
        truth = truths[key[2]].reward
        return 100 * rmse / truth, 100 * se / truth

    default = loggers[1].name
    lines = [
        f"Default world: catalog of {config.n_items} items, slates of {config.slate_size}, sessions up to "
        f"{config.horizon} steps. {repeats} logged datasets per cell, truth from {truth_runs:,} simulated sessions per policy.",
        "",
        "## What each logging policy gives up to explore",
        "",
        "| Logging policy | Its own reward | Change from the default |",
        "|---|---:|---:|",
    ]
    for b in loggers:
        t, d = truths[b.name], truths[default]
        lines.append(
            f"| {b.name} | {t.reward:.4f} ± {t.reward_stderr:.4f} | {100 * (t.reward - d.reward) / d.reward:+.1f}% |"
        )
    lines += ["", "## True values of the target policies", "", "| Target policy | Reward |", "|---|---:|"]
    for p in targets:
        lines.append(f"| {p.name} | {truths[p.name].reward:.4f} ± {truths[p.name].reward_stderr:.4f} |")
    lines.append("")

    for n in sizes:
        lines += [
            f"## Reward error with {n:,} sessions logged",
            "",
            "RMSE as a share of the true value, ± its Monte Carlo standard error. "
            "ESS is the mean effective sample size of the session weights, as a share of sessions logged.",
            "",
        ]
        for p in targets:
            lines += [f"### Target: {p.name}", ""]
            lines.append("| Logging policy | ESS | " + " | ".join(names) + " |")
            lines.append("|---|---:|" + "---:|" * len(names))
            for b in loggers:
                cells = [f"{m:.1f}% ± {s:.1f}" for m, s in (rmse_share((b.name, n, p.name, e)) for e in names)]
                lines.append(f"| {b.name} | {100 * np.mean(ess[(b.name, n, p.name)]):.1f}% | " + " | ".join(cells) + " |")
            lines.append("")

    lines += [
        "## Does effective sample size track the error?",
        "",
        "Spearman rank correlation, across every (logging policy, target policy) cell, between mean ESS share "
        "and RMSE share. Negative means more effective samples go with less error. "
        f"Each size has {len(loggers) * len(targets)} cells.",
        "",
        "| Sessions logged | " + " | ".join(names) + " |",
        "|---:|" + "---:|" * len(names),
    ]
    for n in sizes:
        keys = [(b.name, n, p.name) for b in loggers for p in targets]
        share = np.array([np.mean(ess[k]) for k in keys])
        cells = [f"{spearman(share, np.array([rmse_share(k + (e,))[0] for k in keys])):+.2f}" for e in names]
        lines.append(f"| {n:,} | " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 5000])
    parser.add_argument("--repeats", type=int, default=30)
    parser.add_argument("--truth", type=int, default=500_000)
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    start = time.time()
    report = run(args.sizes, args.repeats, args.truth, args.seed, args.workers)
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
