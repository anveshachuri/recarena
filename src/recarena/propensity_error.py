"""What happens when the logged probabilities are slightly wrong? (issue #20)

Every estimator here divides by the logging policy's probabilities, which ``collect``
records exactly. This experiment logs data with the default logging policy, then
recomputes the logged probabilities as if they came from a slightly different policy:
a wrong temperature, a wrong history weight, or a policy fitted to the logs themselves
by maximum likelihood. Each dataset is scored once per kind of error, so the change
each error causes is measured on the same data.

It also checks one warning sign computable from logs alone: with exact probabilities,
each step's ratio between a target's and the logged probability averages to 1, so the
per-session sum of (ratio - 1) has mean 0. A dataset whose sum is more than 1.96
standard errors from 0 "flags" the probabilities as wrong.

python -m recarena.propensity_error --repeats 100 --truth 300000
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace

import numpy as np

from .benchmark import target_policies
from .data import LoggedData, collect, relog, true_value
from .estimators import FittedQ, dr_with_model, estimate_all, importance_ratios, resolve_estimators
from .policies import SoftmaxPolicy
from .simulator import Catalog, SimConfig

FEATURES = ("history", "quality", "sponsored")


def _item_features(catalog: Catalog, obs: np.ndarray, features: tuple[str, ...]) -> np.ndarray:
    """(rows, n_items, len(features)), the terms ``SoftmaxPolicy.scores`` multiplies by its weights."""
    n_topics = catalog.topics.shape[1]
    n_items = catalog.quality.shape[0]
    columns = {
        "history": lambda: obs[:, :n_topics] @ catalog.topics.T,
        "quality": lambda: np.broadcast_to(catalog.quality, (len(obs), n_items)),
        "sponsored": lambda: np.broadcast_to(catalog.sponsored.astype(float), (len(obs), n_items)),
    }
    return np.stack([columns[f]() for f in features], axis=2)


def _plackett_luce(x: np.ndarray, slates: np.ndarray, theta: np.ndarray):
    """Log likelihood, gradient and Hessian of Plackett-Luce slates with scores ``x @ theta``."""
    rows = np.arange(len(x))
    scores = x @ theta
    available = np.ones(scores.shape, dtype=bool)
    d = len(theta)
    loglik, grad, hess = 0.0, np.zeros(d), np.zeros((d, d))
    for slot in range(slates.shape[1]):
        items = slates[:, slot]
        masked = np.where(available, scores, -np.inf)
        top = masked.max(axis=1, keepdims=True)
        p = np.exp(masked - top)
        total = p.sum(axis=1, keepdims=True)
        p /= total
        loglik += float(np.sum(scores[rows, items] - top[:, 0] - np.log(total[:, 0])))
        mean = np.einsum("ri,rif->rf", p, x)
        grad += (x[rows, items] - mean).sum(axis=0)
        hess -= np.einsum("ri,rif,rig->fg", p, x, x) - mean.T @ mean
        available[rows, items] = False
    return loglik, grad, hess


def fit_softmax_policy(
    catalog: Catalog,
    data: LoggedData,
    features: tuple[str, ...] = FEATURES,
    name: str = "fitted",
    iterations: int = 50,
) -> SoftmaxPolicy:
    """Fits a ``SoftmaxPolicy`` to the logged slates by maximum likelihood.

    Only the weights named in ``features`` are fitted; the others are 0 and the temperature
    is 1 (it can't be told apart from the weights). The log likelihood is concave in the
    weights, so Newton's method with step halving finds the maximum.
    """
    unknown = set(features) - set(FEATURES)
    if unknown:
        raise ValueError(f"unknown features {sorted(unknown)}; available: {list(FEATURES)}")
    active = data.active.reshape(-1)
    obs = data.obs.reshape(data.n * data.horizon, -1)[active]
    slates = data.slates.reshape(data.n * data.horizon, -1)[active]
    x = _item_features(catalog, obs, tuple(features))
    theta = np.zeros(len(features))
    loglik, grad, hess = _plackett_luce(x, slates, theta)
    for _ in range(iterations):
        step = np.linalg.solve(hess - 1e-9 * np.eye(len(theta)), -grad)
        size = 1.0
        while True:
            new = _plackett_luce(x, slates, theta + size * step)
            if new[0] >= loglik - 1e-9 or size < 1e-6:
                break
            size /= 2
        theta = theta + size * step
        improvement = new[0] - loglik
        loglik, grad, hess = new
        if abs(improvement) < 1e-10 * max(1.0, abs(loglik)):
            break
    weights = dict(zip(features, theta))
    return SoftmaxPolicy(
        catalog,
        name,
        history_weight=float(weights.get("history", 0.0)),
        quality_weight=float(weights.get("quality", 0.0)),
        sponsored_weight=float(weights.get("sponsored", 0.0)),
        temperature=1.0,
    )


@dataclass(frozen=True)
class Error:
    """Where the logged probabilities come from. ``fit`` is a tuple of features to fit from the logs."""

    name: str
    temperature: float = 1.0
    history_weight: float = 1.0
    fit: tuple[str, ...] | None = None


ERRORS = (
    Error("exact"),
    Error("temperature 0.8", temperature=0.8),
    Error("temperature 0.9", temperature=0.9),
    Error("temperature 1.1", temperature=1.1),
    Error("temperature 1.2", temperature=1.2),
    Error("history weight 0.8", history_weight=0.8),
    Error("history weight 1.2", history_weight=1.2),
    Error("fitted, all features", fit=FEATURES),
    Error("fitted, quality only", fit=("quality",)),
)


def logged_policy(error: Error, behavior: SoftmaxPolicy, catalog: Catalog, data: LoggedData) -> SoftmaxPolicy:
    if error.fit is not None:
        return fit_softmax_policy(catalog, data, error.fit, error.name)
    return replace(behavior, name=error.name, temperature=error.temperature, history_weight=error.history_weight)


def flag_statistic(data: LoggedData, target: SoftmaxPolicy) -> float:
    """z statistic of the per-session sum of (step ratio - 1), which has mean 0 with exact probabilities."""
    sums = (importance_ratios(data, target) - 1.0).sum(axis=1)
    spread = sums.std(ddof=1)
    if spread == 0:
        # Every ratio is exactly 1, as when the target is the logged policy itself.
        return 0.0
    return float(sums.mean() / (spread / np.sqrt(len(sums))))


def truth_job(job):
    config, policy, runs, seed = job
    catalog = Catalog.generate(config)
    return policy, true_value(config, catalog, next(p for p in target_policies(catalog) if p.name == policy), runs, np.random.default_rng(seed))


def estimate_job(job):
    """One logged dataset, scored once per kind of error. Seeded per job, so worker count doesn't matter."""
    config, n, seed, estimators = job
    catalog = Catalog.generate(config)
    behavior = SoftmaxPolicy(catalog, "logging")
    log_seed, model_seed = seed.spawn(2)
    data = collect(config, catalog, behavior, n, np.random.default_rng(log_seed))
    weighted = {name: fn for name, fn in estimators.items() if name not in ("Direct", "DR")}
    targets = target_policies(catalog)
    # The fitted Q models don't use the logged probabilities, so each target's models are
    # fitted once (cross-fitted on two folds, as in ``direct_and_dr_scores``) and reused for
    # every kind of error. Only the DR correction, which uses the ratios, changes.
    models = {}
    for p in targets:
        rng = np.random.default_rng(model_seed)
        folds = np.array_split(rng.permutation(data.n), 2)
        pairs = []
        for held_out, fit_on in ((folds[0], folds[1]), (folds[1], folds[0])):
            pairs.append((held_out, FittedQ(p, config.examine_decay).fit(data.subset(fit_on), data.rewards[fit_on], rng)))
        direct = np.zeros(data.n)
        for held_out, model in pairs:
            direct[held_out] = model.state_value(0, data.obs[held_out, 0], rng)
        models[p.name] = (pairs, float(direct.mean()))
    out = {}
    for error in ERRORS:
        policy = logged_policy(error, behavior, catalog, data)
        relogged = relog(data, policy)
        for p in targets:
            values = estimate_all(relogged, relogged.rewards, p, config.examine_decay, np.random.default_rng(model_seed), estimators=weighted)
            pairs, direct = models[p.name]
            if "Direct" in estimators:
                values["Direct"] = direct
            if "DR" in estimators:
                ratios = importance_ratios(relogged, p)
                dr = np.zeros(data.n)
                rng = np.random.default_rng(model_seed)  # The same state value draws for every error.
                for held_out, model in pairs:
                    part = relogged.subset(held_out)
                    dr[held_out] = dr_with_model(part, part.rewards, ratios[held_out], model, rng)
                values["DR"] = float(dr.mean())
            out[(error.name, p.name)] = (values, flag_statistic(relogged, p))
        if error.fit is not None:
            out[(error.name, "weights")] = (policy.history_weight, policy.quality_weight, policy.sponsored_weight)
    return out


def run(sizes: list[int], repeats: int, truth_runs: int, seed: int, workers: int, estimators=None) -> str:
    config = SimConfig()
    estimators = resolve_estimators(estimators)
    names = list(estimators)
    targets = [p.name for p in target_policies(Catalog.generate(config))]
    truth_seeds = np.random.SeedSequence([seed, 0]).spawn(len(targets))
    jobs = [(config, n, s, estimators) for n in sizes for s in np.random.SeedSequence([seed, 1, n]).spawn(repeats)]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(pool.map(truth_job, [(config, p, truth_runs, s) for p, s in zip(targets, truth_seeds)]))
        results = list(pool.map(estimate_job, jobs))
    by_size = {n: results[i * repeats : (i + 1) * repeats] for i, n in enumerate(sizes)}
    truth_se = max(100 * v.reward_stderr / v.reward for v in truths.values())

    def errors(runs, error, target, estimator) -> np.ndarray:
        truth = truths[target].reward
        return np.array([100 * (r[(error, target)][0][estimator] - truth) / truth for r in runs])

    def mean_se(x: np.ndarray) -> str:
        return f"{x.mean():+.1f} ± {x.std(ddof=1) / np.sqrt(len(x)):.1f}"

    lines = [
        f"Default world and catalog, default logging policy (temperature 1, history weight 1, quality weight 1). "
        f"{repeats} logged datasets per size, each scored once per kind of error. Truth from {truth_runs:,} sessions "
        f"per target; its standard error is at most {truth_se:.2f}% of the true value. Errors are percent of the true "
        f"reward. Direct uses no logged probabilities, so it is the same for every kind of error.",
        "",
        "| Kind of error | How the logged probabilities are computed |",
        "|---|---|",
    ]
    for e in ERRORS:
        if e.fit is not None:
            how = f"a softmax policy fitted to the logs by maximum likelihood, using {', '.join(e.fit)}"
        elif e.name == "exact":
            how = "the true logging policy"
        else:
            how = f"the logging policy with temperature {e.temperature:g} and history weight {e.history_weight:g}"
        lines.append(f"| {e.name} | {how} |")
    lines.append("")

    for n in sizes:
        runs = by_size[n]
        fitted = [e for e in ERRORS if e.fit is not None]
        if fitted:
            lines += [f"## Fitted weights ({n:,} sessions)", "", "Mean ± standard deviation across datasets. The truth is 1, 1, 0.", ""]
            lines += ["| Kind of error | History weight | Quality weight | Sponsored weight |", "|---|---:|---:|---:|"]
            for e in fitted:
                w = np.array([r[(e.name, "weights")] for r in runs])
                cells = [f"{w[:, i].mean():.3f} ± {w[:, i].std(ddof=1):.3f}" for i in range(3)]
                lines.append(f"| {e.name} | " + " | ".join(cells) + " |")
            lines.append("")

        lines += [f"## Bias / RMSE ({n:,} sessions)", "", "Mean error / RMSE, in percent of the true value.", ""]
        for p in targets:
            lines += [f"### {p}", "", "| Kind of error | " + " | ".join(names) + " |", "|---|" + "---:|" * len(names)]
            for e in ERRORS:
                cells = []
                for est in names:
                    x = errors(runs, e.name, p, est)
                    cells.append(f"{x.mean():+.1f} / {np.sqrt(np.mean(x**2)):.1f}")
                lines.append(f"| {e.name} | " + " | ".join(cells) + " |")
            lines.append("")

        shift_names = [e for e in names if e != "Direct"]
        lines += [
            f"## Shift caused by the error ({n:,} sessions)",
            "",
            "Each dataset's estimate with the wrong probabilities minus its estimate with exact ones, in percent of the "
            "true value, mean ± Monte Carlo standard error. Pairing on the same data removes most of the run to run "
            "noise, so this is much more precise than the difference of the biases above.",
            "",
        ]
        for p in targets:
            lines += [f"### {p}", "", "| Kind of error | " + " | ".join(shift_names) + " |", "|---|" + "---:|" * len(shift_names)]
            for e in ERRORS[1:]:
                cells = [mean_se(errors(runs, e.name, p, est) - errors(runs, "exact", p, est)) for est in shift_names]
                lines.append(f"| {e.name} | " + " | ".join(cells) + " |")
            lines.append("")

        lines += [
            f"## Warning sign: share of datasets flagged ({n:,} sessions)",
            "",
            "Percent of datasets whose per-session sum of (step ratio - 1) is more than 1.96 standard errors from 0, "
            "for each target's ratios. With exact probabilities about 5% should be flagged by chance.",
            "",
            "| Kind of error | " + " | ".join(targets) + " |",
            "|---|" + "---:|" * len(targets),
        ]
        for e in ERRORS:
            cells = [f"{100 * np.mean([abs(r[(e.name, p)][1]) > 1.96 for r in runs]):.0f}%" for p in targets]
            lines.append(f"| {e.name} | " + " | ".join(cells) + " |")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[5000])
    parser.add_argument("--repeats", type=int, default=100)
    parser.add_argument("--truth", type=int, default=300_000)
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--output", default=None)
    parser.add_argument("--estimators", nargs="+", default=None)
    args = parser.parse_args()
    start = time.time()
    report = run(args.sizes, args.repeats, args.truth, args.seed, args.workers, args.estimators)
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
