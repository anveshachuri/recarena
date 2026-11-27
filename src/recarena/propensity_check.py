"""Which probe makes the wrong-probability check reliable? (issue #29)

With exact logged probabilities, each step's ratio between any policy's probability and the
logged one averages to 1, so the per-session sum of (ratio - 1) has mean 0 for every probe
policy. ``propensity_error.flag_statistic`` tests this with one target as the probe. This
compares probes:

- each target policy, as in #20;
- score probes: the logged policy with one weight raised slightly. As the step shrinks,
  (ratio - 1) / step tends to the score of that weight, so these make the check close to a
  score test of the logged policy's own parameters;
- two combined tests: a chi-square test on the three score probes together (using the
  sample covariance of their session sums), and a Bonferroni test across all eight probes.

Each dataset is logged once and checked once per kind of error from ``propensity_error``,
with the default logging policy and with a 10% uniform mixture of it (#17). It also records
how far each kind of error moves SNPDIS, to see whether a flag lines up with a large shift.

python -m recarena.propensity_check --sizes 1000 5000 --repeats 50 --truth 100000 --workers 4
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from statistics import NormalDist

import numpy as np

from .benchmark import target_policies
from .data import LoggedData, collect, relog
from .estimators import importance_ratios, snpdis
from .policies import SoftmaxPolicy, UniformMixturePolicy
from .propensity_error import ERRORS, Error, fit_softmax_policy, truth_job
from .simulator import Catalog, SimConfig

LEVEL = 0.05
SCORE_STEP = 0.05
SCORE_WEIGHTS = ("history", "quality", "sponsored")
# 95% quantiles of the chi-square distribution, by degrees of freedom.
CHI2_95 = {1: 3.841459, 2: 5.991465, 3: 7.814728}
LOGGING = ("default", "default + 10% uniform")
LARGE_SHIFT = 2.0  # A shift above 2% of the true value counts as large.
FAR_TARGET = "pushes sponsored"


def logging_policy(kind: str, catalog: Catalog):
    base = SoftmaxPolicy(catalog, "logging")
    if kind == "default":
        return base
    if kind == "default + 10% uniform":
        return UniformMixturePolicy(base, 0.1, kind)
    raise ValueError(f"unknown logging policy {kind!r}; available: {list(LOGGING)}")


def claimed_policy(error: Error, behavior, catalog: Catalog, data: LoggedData):
    """The policy whose probabilities get logged under ``error``.

    A wrong temperature or history weight is applied to the softmax part of a mixture. A
    fitted policy is always a plain softmax, so with mixture logging it also has the wrong form.
    """
    if error.fit is not None:
        return fit_softmax_policy(catalog, data, error.fit, error.name)
    if isinstance(behavior, UniformMixturePolicy):
        base = replace(behavior.base, temperature=error.temperature, history_weight=error.history_weight)
        return replace(behavior, base=base, name=error.name)
    return replace(behavior, name=error.name, temperature=error.temperature, history_weight=error.history_weight)


def score_probes(claimed, step: float = SCORE_STEP) -> list:
    """The claimed logged policy with each softmax weight raised by ``step``, one at a time."""
    probes = []
    for weight in SCORE_WEIGHTS:
        field = f"{weight}_weight"
        if isinstance(claimed, UniformMixturePolicy):
            base = replace(claimed.base, **{field: getattr(claimed.base, field) + step})
            probes.append(replace(claimed, base=base, name=f"{weight} +{step:g}"))
        else:
            probes.append(replace(claimed, **{field: getattr(claimed, field) + step}, name=f"{weight} +{step:g}"))
    return probes


def session_sums(data: LoggedData, probe) -> np.ndarray:
    """Per-session sum of (step ratio - 1). Its mean is 0 when the logged probabilities are exact."""
    return (importance_ratios(data, probe) - 1.0).sum(axis=1)


def z_statistic(sums: np.ndarray) -> float:
    spread = sums.std(ddof=1)
    if spread == 0:
        # Every ratio is exactly 1, as when the probe is the logged policy itself.
        return 0.0
    return float(sums.mean() / (spread / np.sqrt(len(sums))))


def chi_square_statistic(sums: np.ndarray) -> tuple[float, int]:
    """n * mean' S^-1 mean for an (n, k) matrix of session sums, and its degrees of freedom.

    S is the sample covariance. Columns that are linear combinations of others (or constant)
    are handled with a pseudoinverse, and the degrees of freedom are the rank of S.
    """
    n = len(sums)
    mean = sums.mean(axis=0)
    cov = np.atleast_2d(np.cov(sums, rowvar=False))
    rank = int(np.linalg.matrix_rank(cov))
    if rank == 0:
        return 0.0, 0
    return float(n * mean @ np.linalg.pinv(cov) @ mean), rank


def bonferroni_critical(k: int, level: float = LEVEL) -> float:
    """Two-sided normal critical value for ``k`` tests at total level ``level``."""
    return NormalDist().inv_cdf(1 - level / (2 * k))


def check(data: LoggedData, claimed, targets: list) -> dict:
    """z for each probe, and whether the score test and the Bonferroni test flag the data."""
    out = {}
    for p in targets:
        out[p.name] = z_statistic(session_sums(data, p))
    scores = np.column_stack([session_sums(data, p) for p in score_probes(claimed)])
    for j, weight in enumerate(SCORE_WEIGHTS):
        out[f"{weight} +{SCORE_STEP:g}"] = z_statistic(scores[:, j])
    stat, df = chi_square_statistic(scores)
    out["score test"] = bool(df > 0 and stat > CHI2_95[df])
    zs = [abs(v) for v in out.values() if not isinstance(v, bool)]
    out["all probes, Bonferroni"] = bool(max(zs) > bonferroni_critical(len(zs)))
    return out


def probe_names(targets: list) -> list[str]:
    return [p.name for p in targets] + [f"{w} +{SCORE_STEP:g}" for w in SCORE_WEIGHTS]


def check_job(job):
    """One logged dataset, checked once per kind of error. Seeded per job, so worker count doesn't matter."""
    config, kind, n, seed = job
    catalog = Catalog.generate(config)
    behavior = logging_policy(kind, catalog)
    data = collect(config, catalog, behavior, n, np.random.default_rng(seed))
    targets = target_policies(catalog)
    out = {}
    for error in ERRORS:
        claimed = claimed_policy(error, behavior, catalog, data)
        relogged = relog(data, claimed)
        flags = check(relogged, claimed, targets)
        estimates = {p.name: snpdis(relogged, relogged.rewards, importance_ratios(relogged, p)) for p in targets}
        out[error.name] = (flags, estimates)
    return out


def run(sizes: list[int], repeats: int, truth_runs: int, seed: int, workers: int, logging=LOGGING) -> str:
    config = SimConfig()
    targets = target_policies(Catalog.generate(config))
    names = [p.name for p in targets]
    probes = probe_names(targets)
    tests = probes + ["score test", "all probes, Bonferroni"]
    near = [t for t in names if t != FAR_TARGET]
    truth_seeds = np.random.SeedSequence([seed, 0]).spawn(len(names))
    jobs = [
        (config, kind, n, s)
        for kind in logging
        for n in sizes
        for s in np.random.SeedSequence([seed, 1, LOGGING.index(kind), n]).spawn(repeats)
    ]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(pool.map(truth_job, [(config, p, truth_runs, s) for p, s in zip(names, truth_seeds)]))
        results = list(pool.map(check_job, jobs))

    def flagged(run_, error, test) -> bool:
        v = run_[error][0][test]
        return v if isinstance(v, bool) else abs(v) > NormalDist().inv_cdf(1 - LEVEL / 2)

    def shift(run_, error, target) -> float:
        truth = truths[target].reward
        return 100 * (run_[error][1][target] - run_["exact"][1][target]) / truth

    lines = [
        f"Default world and catalog. {repeats} logged datasets per logging policy and size, each checked once per "
        f"kind of error (see `results/propensity_error.md` for the kinds). A single probe flags a dataset when its z "
        f"is beyond {NormalDist().inv_cdf(1 - LEVEL / 2):.2f}. Score probes raise one weight of the claimed logged "
        f"policy by {SCORE_STEP:g}. The score test is a chi-square test on the three score probes together; the "
        f"Bonferroni test flags when any of the {len(probes)} probes is beyond {bonferroni_critical(len(probes)):.2f}. "
        f"With exact probabilities every test should flag about {100 * LEVEL:.0f}% of datasets; the exact rows show "
        f"that rate ± its Monte Carlo standard error. Shifts are SNPDIS with the wrong probabilities minus SNPDIS "
        f"with exact ones on the same data, in percent of the true value (truth from {truth_runs:,} sessions per target).",
        "",
    ]
    for i, kind in enumerate(logging):
        for j, n in enumerate(sizes):
            start = (i * len(sizes) + j) * repeats
            runs = results[start : start + repeats]
            lines += [
                f"## Logging: {kind}, {n:,} sessions",
                "",
                "### Share of datasets flagged",
                "",
                "| Kind of error | " + " | ".join(tests) + " |",
                "|---|" + "---:|" * len(tests),
            ]
            for e in ERRORS:
                cells = []
                for t in tests:
                    rate = np.mean([flagged(r, e.name, t) for r in runs])
                    if e.name == "exact":
                        cells.append(f"{100 * rate:.0f}% ± {100 * np.sqrt(rate * (1 - rate) / repeats):.1f}")
                    else:
                        cells.append(f"{100 * rate:.0f}%")
                lines.append(f"| {e.name} | " + " | ".join(cells) + " |")
            lines += [
                "",
                "### Mean absolute SNPDIS shift (% of the true value)",
                "",
                "| Kind of error | " + " | ".join(names) + " |",
                "|---|" + "---:|" * len(names),
            ]
            for e in ERRORS[1:]:
                cells = [f"{np.mean([abs(shift(r, e.name, t)) for r in runs]):.1f}" for t in names]
                lines.append(f"| {e.name} | " + " | ".join(cells) + " |")
            lines += [
                "",
                "### Does a flag line up with a large shift?",
                "",
                f"All datasets with wrong probabilities, split by whether the largest absolute SNPDIS shift over the "
                f"{len(near)} near targets is above {LARGE_SHIFT:g}% of the true value.",
                "",
                "| Largest near shift | Datasets | Flagged by score test | Flagged by Bonferroni |",
                "|---|---:|---:|---:|",
            ]
            pairs = [(r, e.name) for r in runs for e in ERRORS[1:]]
            large = np.array([max(abs(shift(r, e, t)) for t in near) > LARGE_SHIFT for r, e in pairs])
            score = np.array([flagged(r, e, "score test") for r, e in pairs])
            bonf = np.array([flagged(r, e, "all probes, Bonferroni") for r, e in pairs])
            for label, mask in ((f"above {LARGE_SHIFT:g}%", large), (f"{LARGE_SHIFT:g}% or less", ~large)):
                if mask.any():
                    lines.append(
                        f"| {label} | {mask.sum()} | {100 * score[mask].mean():.0f}% | {100 * bonf[mask].mean():.0f}% |"
                    )
                else:
                    lines.append(f"| {label} | 0 | - | - |")
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 5000])
    parser.add_argument("--repeats", type=int, default=100)
    parser.add_argument("--truth", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--logging", nargs="+", default=list(LOGGING), choices=list(LOGGING))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    start = time.time()
    report = run(args.sizes, args.repeats, args.truth, args.seed, args.workers, tuple(args.logging))
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
