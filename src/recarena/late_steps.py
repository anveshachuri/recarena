"""Where does the per-decision error on far targets come from, step by step? (issue #31)

PDIS and SNPDIS are sums over steps, and so is the true value, so each estimate splits into
one term per step that estimates that step's true mean value. This logs datasets in the
default world, splits the PDIS and SNPDIS estimates by step, and scores each step's term
against that step's true value. It also compares two ways of asking for less of the session:
discounting (``gamma < 1``) and truncating after the first ``k`` steps, each against its own
true value. Both come from the same per-step truth, so one truth run per policy serves them all.

python -m recarena.late_steps --catalogs 3 --sizes 1000 5000 20000 --repeats 50 --truth 500000
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace

import numpy as np

from .benchmark import target_policies
from .data import collect
from .estimators import importance_ratios, ips, pdis, snips, snpdis
from .policies import SoftmaxPolicy, UniformMixturePolicy
from .simulator import BatchSimulator, Catalog, SimConfig
from .stress import FAR_TARGETS

STEP_NAMES = ("PDIS", "SNPDIS")
TOTAL_NAMES = ("IPS", "SNIPS", "PDIS", "SNPDIS")
_TOTAL_FUNCTIONS = (ips, snips, pdis, snpdis)
GAMMAS = (0.9, 0.7)
TRUNCATIONS = (10, 5)
BLOCK = 5  # Steps per block in the block tables.
TAKEOFF = 0.20  # A step's error "takes off" once its own relative RMSE is above 20%.
WEIGHT_DROP = 0.9  # The step where the median step mean weight first falls below 0.9.


def step_terms(values: np.ndarray, ratios: np.ndarray, normalized: bool = False) -> np.ndarray:
    """PDIS's (or, with ``normalized``, SNPDIS's) term for each step. Shape (horizon,).

    The terms sum to ``pdis`` (or ``snpdis``) with ``gamma = 1``, and the term for step ``t``
    estimates the mean value at step ``t`` under the target policy.
    """
    weights = np.cumprod(ratios, axis=1)
    if normalized:
        return np.sum(weights * values, axis=0) / np.sum(weights, axis=0)
    return np.mean(weights * values, axis=0)


@dataclass(frozen=True)
class StepTruth:
    """Mean reward and cost at each step under a policy, with their standard errors. Shape (horizon,)."""

    reward: np.ndarray
    reward_stderr: np.ndarray
    cost: np.ndarray
    cost_stderr: np.ndarray

    def weighted(self, weights: np.ndarray, kind: str = "reward") -> tuple[float, float]:
        """The value that counts step ``t`` ``weights[t]`` times, and a bound on its standard error.

        The bound adds the per-step standard errors, which can only overstate the true one.
        """
        mean, stderr = (self.reward, self.reward_stderr) if kind == "reward" else (self.cost, self.cost_stderr)
        return float(weights @ mean), float(np.abs(weights) @ stderr)


def true_step_values(
    config: SimConfig, catalog: Catalog, policy, n: int, rng: np.random.Generator, chunk: int = 50_000
) -> StepTruth:
    """The mean value at each step, from ``n`` sessions of the policy itself.

    It draws random numbers exactly as ``true_value`` does, so with the same seed its steps
    sum to ``true_value``'s answer.
    """
    h = config.horizon
    reward_sum, reward_sq, cost_sum, cost_sq = np.zeros(h), np.zeros(h), np.zeros(h), np.zeros(h)
    remaining = n
    while remaining > 0:
        size = min(chunk, remaining)
        sim = BatchSimulator(config, catalog, size, rng)
        obs = sim.reset()
        for t in range(h):
            rewards, costs, _ = sim.step(policy.sample(obs, config.slate_size, rng))
            reward_sum[t] += rewards.sum()
            reward_sq[t] += np.square(rewards).sum()
            cost_sum[t] += costs.sum()
            cost_sq[t] += np.square(costs).sum()
            obs = sim.observe()
        remaining -= size

    def mean_and_stderr(total, squares):
        mean = total / n
        return mean, np.sqrt(np.maximum(squares / n - mean**2, 0.0) / n)

    r, r_se = mean_and_stderr(reward_sum, reward_sq)
    c, c_se = mean_and_stderr(cost_sum, cost_sq)
    return StepTruth(r, r_se, c, c_se)


def variants(horizon: int) -> list[tuple[str, float, int]]:
    """(label, discount factor, steps kept) for the full value, each discount and each truncation."""
    out = [("full", 1.0, horizon)]
    out += [(f"gamma {g:g}", g, horizon) for g in GAMMAS]
    out += [(f"first {k} steps", 1.0, k) for k in TRUNCATIONS if k < horizon]
    return out


def step_weights(horizon: int, gamma: float, keep: int) -> np.ndarray:
    """How many times each step counts: ``gamma ** t`` for the first ``keep`` steps, 0 after."""
    return gamma ** np.arange(horizon) * (np.arange(horizon) < keep)


def variant_estimates(values: np.ndarray, ratios: np.ndarray, gamma: float, keep: int) -> dict[str, float]:
    """IPS, SNIPS, PDIS and SNPDIS of the value discounted by ``gamma`` over the first ``keep`` steps.

    A truncation runs the estimators on the first ``keep`` steps only, so IPS and SNIPS use
    the weight of those steps alone. A discount keeps the whole session weight for them.
    """
    values, ratios = values[:, :keep], ratios[:, :keep]
    return {e: f(None, values, ratios, gamma) for e, f in zip(TOTAL_NAMES, _TOTAL_FUNCTIONS)}


def logging_policies(catalog: Catalog) -> list:
    default = SoftmaxPolicy(catalog, "default", 1.0, 1.0, 0.0, 1.0)
    return [default, UniformMixturePolicy(default, 0.1, "default + 10% uniform")]


def truth_job(job):
    catalog_seed, policy_name, runs, seed = job
    config = replace(SimConfig(), catalog_seed=catalog_seed)
    catalog = Catalog.generate(config)
    policy = next(p for p in target_policies(catalog) if p.name == policy_name)
    return (catalog_seed, policy_name), true_step_values(config, catalog, policy, runs, np.random.default_rng(seed))


def estimate_job(job):
    """One logged dataset: per-step terms, step mean weights and variant estimates for every target."""
    logging_name, catalog_seed, n, seed = job
    config = replace(SimConfig(), catalog_seed=catalog_seed)
    catalog = Catalog.generate(config)
    behavior = next(p for p in logging_policies(catalog) if p.name == logging_name)
    data = collect(config, catalog, behavior, n, np.random.default_rng(seed))
    out = {}
    for p in target_policies(catalog):
        ratios = importance_ratios(data, p)
        out[p.name] = {
            "weights": np.cumprod(ratios, axis=1).mean(axis=0),
            "reward": {e: step_terms(data.rewards, ratios, e == "SNPDIS") for e in STEP_NAMES},
            "cost": {e: step_terms(data.costs, ratios, e == "SNPDIS") for e in STEP_NAMES},
            "variants": {label: variant_estimates(data.rewards, ratios, g, k) for label, g, k in variants(config.horizon)},
        }
    return (logging_name, catalog_seed, n), out


def _mean_se(x: np.ndarray) -> tuple[float, float]:
    x = np.asarray(x, dtype=float)
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 1 else float("nan")


def _bias(x: np.ndarray) -> str:
    m, se = _mean_se(x)
    return f"{100 * m:+.1f}% ± {100 * se:.1f}"


def _rmse(x: np.ndarray) -> str:
    return f"{100 * np.sqrt(np.mean(np.square(x))):.1f}%"


def _first_step(flags: np.ndarray) -> str:
    hit = np.flatnonzero(flags)
    return str(int(hit[0]) + 1) if len(hit) else "never"


def run(catalogs: int, sizes: list[int], repeats: int, truth_runs: int, seed: int, workers: int) -> str:
    config = SimConfig()
    h = config.horizon
    sample_catalog = Catalog.generate(config)
    targets = [p.name for p in target_policies(sample_catalog)]
    loggings = [p.name for p in logging_policies(sample_catalog)]
    blocks = [(s, min(s + BLOCK, h)) for s in range(0, h, BLOCK)]
    labelled = variants(h)

    truth_keys = [(c, p) for c in range(catalogs) for p in targets]
    truth_seeds = np.random.SeedSequence([seed, 0]).spawn(len(truth_keys))
    cells = [(lg, c, n) for lg in loggings for n in sizes for c in range(catalogs)]
    job_seeds = np.random.SeedSequence([seed, 1]).spawn(len(cells) * repeats)
    jobs = [cell + (job_seeds[i * repeats + r],) for i, cell in enumerate(cells) for r in range(repeats)]

    # rows[(logging, n, target)] is a list of per-dataset records with errors already relative.
    rows: dict[tuple, list] = {(lg, n, p): [] for lg in loggings for n in sizes for p in targets}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        truths = dict(pool.map(truth_job, [k + (truth_runs, s) for k, s in zip(truth_keys, truth_seeds)]))
        for (lg, c, n), out in pool.map(estimate_job, jobs):
            for p in targets:
                t, o = truths[(c, p)], out[p]
                full = {"reward": t.reward.sum(), "cost": t.cost.sum()}
                rec = {"weights": o["weights"]}
                for kind in ("reward", "cost"):
                    step_truth = t.reward if kind == "reward" else t.cost
                    for e in STEP_NAMES:
                        diff = o[kind][e] - step_truth
                        # Error of each step's term as a share of the full truth and, for rewards,
                        # of that step's own truth (NaN if a tiny truth run saw nothing at a step).
                        rec[(kind, e, "of full")] = diff / full[kind]
                        if kind == "reward":
                            with np.errstate(divide="ignore", invalid="ignore"):
                                rec[(kind, e, "step")] = np.where(step_truth != 0, diff / np.where(step_truth != 0, step_truth, 1.0), np.nan)
                for label, g, k in labelled:
                    value, _ = t.weighted(step_weights(h, g, k))
                    for e in TOTAL_NAMES:
                        rec[("variant", label, e)] = (o["variants"][label][e] - value) / value
                rows[(lg, n, p)].append(rec)

    worst_truth_se = max(
        max(t.weighted(np.ones(h), k)[1] / t.weighted(np.ones(h), k)[0] for k in ("reward", "cost"))
        for t in truths.values()
    )
    lines = [
        f"Default world, {catalogs} catalogs, {repeats} logged datasets per catalog, logging policy and size "
        f"(so {catalogs * repeats} per row), sessions of {h} steps. Truth from {truth_runs:,} sessions per "
        f"target and catalog, kept step by step. Its standard error, bounded by adding the per-step ones, is "
        f"at most {100 * worst_truth_se:.2f}% of the full true value. All errors are pooled over catalogs as "
        f"shares of each catalog's own true value.",
        "",
        "PDIS's term for step t is the mean over sessions of the cumulative weight up to step t times the step's "
        "value, and SNPDIS divides the same sum by the sum of the cumulative weights instead of the number of "
        "sessions. Each estimates the true mean value at step t, and the terms add up to the full estimate.",
        "",
    ]

    for kind in ("reward", "cost"):
        sizes_here = sizes if kind == "reward" else [s for s in sizes if s == sorted(sizes)[len(sizes) // 2]]
        for e in STEP_NAMES:
            head = " | ".join(f"Steps {a + 1} to {b}" for a, b in blocks)
            lines += [
                f"## {e}, {kind}: signed error of each block of steps, as a share of the full true value",
                "",
                "Mean ± standard error. The block errors add up to the full error. Truth in late half: the share "
                f"of the full true value that steps {h // 2 + 1} to {h} hold.",
                "",
                f"| Logging | Sessions | Target | Truth in late half | {head} | Full |",
                "|---|---:|---|---:|" + "---:|" * (len(blocks) + 1),
            ]
            for lg in loggings:
                for n in sizes_here:
                    for p in targets:
                        sel = rows[(lg, n, p)]
                        of_full = np.array([r[(kind, e, "of full")] for r in sel])
                        late = []
                        for c in range(catalogs):
                            t = truths[(c, p)].reward if kind == "reward" else truths[(c, p)].cost
                            late.append(t[h // 2 :].sum() / t.sum())
                        block_cells = [_bias(of_full[:, a:b].sum(axis=1)) for a, b in blocks]
                        lines.append(
                            f"| {lg} | {n:,} | {p} | {100 * np.mean(late):.0f}% | "
                            + " | ".join(block_cells)
                            + f" | {_bias(of_full.sum(axis=1))} |"
                        )
            lines.append("")

    lines += [
        "## Where the reward error takes off, and where the weight mass drops",
        "",
        f"Error takes off: the first step whose own term has a relative RMSE above {100 * TAKEOFF:.0f}% of that "
        f"step's true value. Weight drop: the first step where the median (over datasets) of the step mean "
        f"cumulative weight from #24 is below {WEIGHT_DROP:g}. Its expectation is 1 at every step.",
        "",
        "| Logging | Sessions | Target | PDIS error takes off | SNPDIS error takes off | Weight drop | "
        f"Median step mean weight at step {h} |",
        "|---|---:|---|---:|---:|---:|---:|",
    ]
    for lg in loggings:
        for n in sizes:
            for p in targets:
                sel = rows[(lg, n, p)]
                weights = np.median(np.array([r["weights"] for r in sel]), axis=0)
                takeoff = []
                for e in STEP_NAMES:
                    step = np.array([r[("reward", e, "step")] for r in sel])
                    takeoff.append(_first_step(np.sqrt(np.mean(np.square(step), axis=0)) > TAKEOFF))
                lines.append(
                    f"| {lg} | {n:,} | {p} | {takeoff[0]} | {takeoff[1]} | {_first_step(weights < WEIGHT_DROP)} | "
                    f"{weights[-1]:.3f} |"
                )
    lines.append("")

    detail_n = sorted(sizes)[len(sizes) // 2]
    for p in FAR_TARGETS:
        lines += [
            f"## Step by step reward error for {p} ({loggings[0]} logging, {detail_n:,} sessions)",
            "",
            "Each step's term against that step's true value: mean relative error ± standard error / relative "
            "RMSE. Truth: the step's mean true value, averaged over catalogs.",
            "",
            "| Step | Truth | PDIS | SNPDIS | Median step mean weight |",
            "|---:|---:|---|---|---:|",
        ]
        sel = rows[(loggings[0], detail_n, p)]
        weights = np.median(np.array([r["weights"] for r in sel]), axis=0)
        truth_mean = np.mean([truths[(c, p)].reward for c in range(catalogs)], axis=0)
        steps = {e: np.array([r[("reward", e, "step")] for r in sel]) for e in STEP_NAMES}
        for t in range(h):
            cells_ = [f"{_bias(steps[e][:, t])} / {_rmse(steps[e][:, t])}" for e in STEP_NAMES]
            lines.append(f"| {t + 1} | {truth_mean[t]:.4f} | " + " | ".join(cells_) + f" | {weights[t]:.3f} |")
        lines.append("")

    lines += [
        "## Discounting against truncation (reward, far targets)",
        "",
        "Each variant is scored against its own true value: mean relative error ± standard error / relative "
        f"RMSE. Truncated variants count only the first k steps, and IPS and SNIPS then use the weight of "
        "those steps alone. Discounting leaves IPS and SNIPS with the whole session weight.",
        "",
        "| Logging | Sessions | Target | Value | " + " | ".join(TOTAL_NAMES) + " |",
        "|---|---:|---|---|" + "---|" * len(TOTAL_NAMES),
    ]
    for lg in loggings:
        for n in sizes:
            for p in FAR_TARGETS:
                sel = rows[(lg, n, p)]
                for label, _, _ in labelled:
                    cells_ = []
                    for e in TOTAL_NAMES:
                        err = np.array([r[("variant", label, e)] for r in sel])
                        cells_.append(f"{_bias(err)} / {_rmse(err)}")
                    lines.append(f"| {lg} | {n:,} | {p} | {label} | " + " | ".join(cells_) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogs", type=int, default=3)
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 5000, 20000])
    parser.add_argument("--repeats", type=int, default=50)
    parser.add_argument("--truth", type=int, default=500_000)
    parser.add_argument("--seed", type=int, default=4004)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    start = time.time()
    report = run(args.catalogs, args.sizes, args.repeats, args.truth, args.seed, args.workers)
    report += f"\nFinished in {time.time() - start:.0f} s with seed {args.seed}.\n"
    print(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
