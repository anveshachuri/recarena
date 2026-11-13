"""Off-policy estimators: the value of a new policy, from another policy's logs.

Every estimator takes ``values``, a (n, horizon) array of per-step outcomes. Passing
rewards estimates the policy's reward. Passing costs estimates its budget use.

To add your own estimator, write a function from ``EstimationTask`` to ``Estimate`` and
either pass it to ``estimate_all(..., estimators={"Mine": fn})`` or register it with
``register_estimator("Mine", fn)``.

Two slate-aware estimators, ``CascadePDIS`` and ``SNCascadePDIS``, are available by name
but are not run by default, so existing results don't change.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from functools import cached_property

import numpy as np

from .data import LoggedData
from .policies import SoftmaxPolicy


def importance_ratios(data: LoggedData, target: SoftmaxPolicy) -> np.ndarray:
    """Per-step probability ratio between target and behavior. After a session ends it is 1."""
    n, h = data.n, data.horizon
    flat_obs = data.obs.reshape(n * h, -1)
    flat_slates = data.slates.reshape(n * h, -1)
    target_log_prob = target.log_prob(flat_obs, flat_slates).reshape(n, h)
    return np.where(data.active, np.exp(target_log_prob - data.behavior_log_prob), 1.0)


def prefix_ratios(data: LoggedData, target: SoftmaxPolicy) -> np.ndarray:
    """Ratio of target to behavior probability for each slate's first ``j + 1`` slots.

    Shape (n, horizon, slate_size). The last slot's ratio equals ``importance_ratios``.
    After a session ends every ratio is 1.
    """
    if data.behavior_prefix_log_prob is None:
        raise ValueError("these logs have no behavior_prefix_log_prob; log them with collect()")
    n, h, k = data.slates.shape
    flat_obs = data.obs.reshape(n * h, -1)
    flat_slates = data.slates.reshape(n * h, k)
    target_log_prob = target.prefix_log_prob(flat_obs, flat_slates).reshape(n, h, k)
    return np.where(data.active[:, :, None], np.exp(target_log_prob - data.behavior_prefix_log_prob), 1.0)


def ips(data: LoggedData, values: np.ndarray, ratios: np.ndarray) -> float:
    """Reweight whole sessions. Unbiased, with very high variance."""
    return float(np.mean(ratios.prod(axis=1) * values.sum(axis=1)))


def snips(data: LoggedData, values: np.ndarray, ratios: np.ndarray) -> float:
    """IPS with normalized weights. Slightly biased, and usually much steadier."""
    weights = ratios.prod(axis=1)
    return float(np.sum(weights * values.sum(axis=1)) / np.sum(weights))


def pdis(data: LoggedData, values: np.ndarray, ratios: np.ndarray) -> float:
    """Per-decision IS: each step only pays for the decisions made before it."""
    return float(np.mean(np.sum(np.cumprod(ratios, axis=1) * values, axis=1)))


def snpdis(data: LoggedData, values: np.ndarray, ratios: np.ndarray) -> float:
    """Per-decision IS with normalized weights at each step."""
    weights = np.cumprod(ratios, axis=1)
    return float(np.sum(np.sum(weights * values, axis=0) / np.sum(weights, axis=0)))


def _features(
    obs: np.ndarray, slates: np.ndarray, target: SoftmaxPolicy, examine_decay: float, informed: bool = True
) -> np.ndarray:
    """Hand-built features of (what the system sees, slate shown), weighted by slot."""
    catalog = target.catalog
    n_topics = catalog.topics.shape[1]
    slot_weights = examine_decay ** np.arange(slates.shape[1])
    slot_weights = slot_weights / slot_weights.sum()
    topics = np.sum(catalog.topics[slates] * slot_weights[:, None], axis=1)
    quality = np.sum(catalog.quality[slates] * slot_weights, axis=1)
    sponsored = np.sum(catalog.sponsored[slates] * slot_weights, axis=1)
    history, misses = obs[:, :n_topics], obs[:, n_topics]
    if not informed:
        # What a model looks like when nobody told it what drives reward.
        return np.column_stack([np.ones(len(obs)), history, topics, misses])
    return np.column_stack(
        [np.ones(len(obs)), history, topics, history * topics, quality, sponsored, misses, misses * quality]
    )


class FittedQ:
    """Fitted Q evaluation: a separate ridge regression for each step, fitted backwards."""

    def __init__(
        self,
        target: SoftmaxPolicy,
        examine_decay: float,
        ridge: float = 1.0,
        value_samples: int = 16,
        informed: bool = True,
    ):
        self.target = target
        self.examine_decay = examine_decay
        self.ridge = ridge
        self.value_samples = value_samples
        self.informed = informed

    def fit(self, data: LoggedData, values: np.ndarray, rng: np.random.Generator) -> "FittedQ":
        h = data.horizon
        self.weights: list[np.ndarray | None] = [None] * h
        self.slate_size = data.slates.shape[2]
        for t in range(h - 1, -1, -1):
            here = data.active[:, t]
            if not here.any():
                continue
            target_values = values[here, t].copy()
            if t + 1 < h:
                still_here = data.active[here, t + 1]
                future = np.zeros(int(here.sum()))
                if still_here.any():
                    future[still_here] = self.state_value(t + 1, data.obs[here, t + 1][still_here], rng)
                target_values += future
            x = _features(data.obs[here, t], data.slates[here, t], self.target, self.examine_decay, self.informed)
            gram = x.T @ x + self.ridge * np.eye(x.shape[1])
            self.weights[t] = np.linalg.solve(gram, x.T @ target_values)
        return self

    def action_value(self, t: int, obs: np.ndarray, slates: np.ndarray) -> np.ndarray:
        if self.weights[t] is None:
            return np.zeros(len(obs))
        return _features(obs, slates, self.target, self.examine_decay, self.informed) @ self.weights[t]

    def state_value(self, t: int, obs: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Average action value over slates the target policy would pick."""
        repeated = np.repeat(obs, self.value_samples, axis=0)
        slates = self.target.sample(repeated, self.slate_size, rng)
        return self.action_value(t, repeated, slates).reshape(len(obs), self.value_samples).mean(axis=1)


def dr_with_model(
    data: LoggedData, values: np.ndarray, ratios: np.ndarray, model, rng: np.random.Generator
) -> np.ndarray:
    """Doubly robust score for each session (Jiang and Li, 2016)."""
    n, h = data.n, data.horizon
    score = np.zeros(n)
    for t in range(h - 1, -1, -1):
        here = data.active[:, t]
        if not here.any():
            continue
        q = model.action_value(t, data.obs[here, t], data.slates[here, t])
        v = model.state_value(t, data.obs[here, t], rng)
        score[here] = v + ratios[here, t] * (values[here, t] + score[here] - q)
    return score


def direct_and_dr_scores(
    data: LoggedData,
    values: np.ndarray,
    ratios: np.ndarray,
    target: SoftmaxPolicy,
    examine_decay: float,
    rng: np.random.Generator,
    informed: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Per-session direct method and doubly robust scores, each from a model fitted on the other fold."""
    order = rng.permutation(data.n)
    folds = np.array_split(order, 2)
    direct_scores = np.zeros(data.n)
    dr_scores = np.zeros(data.n)
    for held_out, fit_on in ((folds[0], folds[1]), (folds[1], folds[0])):
        model = FittedQ(target, examine_decay, informed=informed).fit(data.subset(fit_on), values[fit_on], rng)
        part = data.subset(held_out)
        direct_scores[held_out] = model.state_value(0, part.obs[:, 0], rng)
        dr_scores[held_out] = dr_with_model(part, values[held_out], ratios[held_out], model, rng)
    return direct_scores, dr_scores


def direct_and_dr(
    data: LoggedData,
    values: np.ndarray,
    ratios: np.ndarray,
    target: SoftmaxPolicy,
    examine_decay: float,
    rng: np.random.Generator,
    informed: bool = True,
) -> tuple[float, float]:
    """Direct method and doubly robust, each model scored on data it was not fitted on."""
    direct_scores, dr_scores = direct_and_dr_scores(data, values, ratios, target, examine_decay, rng, informed)
    return float(direct_scores.mean()), float(dr_scores.mean())


# ---------------------------------------------------------------------------
# Pluggable estimators
#
# An estimator is any function that takes an ``EstimationTask`` and returns an
# ``Estimate``. Built-in and user estimators are treated the same way.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Estimate:
    """An estimate, and optionally how much each logged session moved it.

    ``influence`` has one entry per session with mean zero, such that the estimate's
    variance is approximately ``influence.var() / n``. It is what confidence intervals
    are built from. Estimators that can't provide it leave it as ``None``.
    """

    value: float
    influence: np.ndarray | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", float(self.value))
        if self.influence is not None:
            object.__setattr__(self, "influence", np.asarray(self.influence, dtype=float))

    def standard_error(self) -> float:
        """Plug-in standard error from the influence values, or NaN if there are none."""
        if self.influence is None or len(self.influence) < 2:
            return float("nan")
        return float(np.std(self.influence, ddof=1) / np.sqrt(len(self.influence)))


@dataclass
class EstimationTask:
    """Everything an estimator may use: the logs, the values to estimate, and the target policy.

    ``values`` is ``data.rewards`` to estimate reward, or ``data.costs`` to estimate cost.
    Shared work (importance ratios, the fitted models for Direct and DR) is computed once
    and reused by every estimator that asks for it.
    """

    data: LoggedData
    values: np.ndarray
    target: SoftmaxPolicy
    examine_decay: float
    rng: np.random.Generator
    informed: bool = True
    # Per-slot values, (n, horizon, slate_size), summing over slots to ``values``. Only the
    # slate-aware estimators use them. If left out, they are taken from the logs when
    # ``values`` is ``data.rewards`` or ``data.costs``.
    slot_values: np.ndarray | None = None
    _model_scores: tuple[np.ndarray, np.ndarray] | None = field(default=None, init=False, repr=False)

    @cached_property
    def ratios(self) -> np.ndarray:
        return importance_ratios(self.data, self.target)

    @cached_property
    def prefix_ratios(self) -> np.ndarray:
        return prefix_ratios(self.data, self.target)

    @cached_property
    def per_slot_values(self) -> np.ndarray:
        """``slot_values`` if given, otherwise the logged per-slot rewards or costs."""
        slot_values = self.slot_values
        if slot_values is None:
            if self.values is self.data.rewards:
                slot_values = self.data.slot_rewards
            elif self.values is self.data.costs:
                slot_values = self.data.slot_costs
        if slot_values is None:
            raise ValueError(
                "slate-aware estimators need per-slot values: pass slot_values, or pass "
                "data.rewards or data.costs from logs made by collect()"
            )
        slot_values = np.asarray(slot_values, dtype=float)
        if slot_values.shape != self.data.slates.shape or not np.allclose(slot_values.sum(axis=2), self.values):
            raise ValueError("slot_values must have shape (n, horizon, slate_size) and sum over slots to values")
        return slot_values

    def model_scores(self) -> tuple[np.ndarray, np.ndarray]:
        """Per-session (Direct, DR) scores. Fitted once, on first use."""
        if self._model_scores is None:
            self._model_scores = direct_and_dr_scores(
                self.data, self.values, self.ratios, self.target, self.examine_decay, self.rng, self.informed
            )
        return self._model_scores


Estimator = Callable[[EstimationTask], Estimate]


def _mean_estimate(scores: np.ndarray) -> Estimate:
    value = float(scores.mean())
    return Estimate(value, scores - value)


def _ips(task: EstimationTask) -> Estimate:
    return _mean_estimate(task.ratios.prod(axis=1) * task.values.sum(axis=1))


def _snips(task: EstimationTask) -> Estimate:
    weights = task.ratios.prod(axis=1)
    returns = task.values.sum(axis=1)
    value = float(np.sum(weights * returns) / np.sum(weights))
    # Delta method for a ratio of means.
    return Estimate(value, weights * (returns - value) / weights.mean())


def _pdis(task: EstimationTask) -> Estimate:
    return _mean_estimate(np.sum(np.cumprod(task.ratios, axis=1) * task.values, axis=1))


def _snpdis(task: EstimationTask) -> Estimate:
    weights = np.cumprod(task.ratios, axis=1)
    step_values = np.sum(weights * task.values, axis=0) / np.sum(weights, axis=0)
    # Delta method, step by step: each step is a ratio of means.
    influence = np.sum(weights * (task.values - step_values) / weights.mean(axis=0), axis=1)
    return Estimate(float(step_values.sum()), influence)


def _direct(task: EstimationTask) -> Estimate:
    # The influence treats the fitted models as fixed, so intervals from it ignore model-fitting noise.
    return _mean_estimate(task.model_scores()[0])


def _dr(task: EstimationTask) -> Estimate:
    return _mean_estimate(task.model_scores()[1])


def _cascade_weights(task: EstimationTask) -> np.ndarray:
    """Weight for the value in slot ``j`` of step ``t``: full slates before ``t``, then slots up to ``j``."""
    before = np.cumprod(task.ratios, axis=1)
    before = np.concatenate([np.ones((task.data.n, 1)), before[:, :-1]], axis=1)
    return before[:, :, None] * task.prefix_ratios


def _cascade_pdis(task: EstimationTask) -> Estimate:
    """Per-decision IS that, within a step, only pays for the slots at or above the one that paid off.

    Follows the cascade idea of Kiyohara et al. (2022) and McInerney et al. (2020), applied
    per step of a session. It is unbiased when a slot's reward and cost depend only on the
    slots above it in the same step, which holds in this simulator: users read top down
    and stop at their first click. What happens in later steps can depend on the whole
    slate, so earlier steps still pay for full slates.
    """
    return _mean_estimate(np.sum(_cascade_weights(task) * task.per_slot_values, axis=(1, 2)))


def _sn_cascade_pdis(task: EstimationTask) -> Estimate:
    """CascadePDIS with normalized weights for each step and slot."""
    weights = _cascade_weights(task)
    values = task.per_slot_values
    cell_values = np.sum(weights * values, axis=0) / np.sum(weights, axis=0)
    # Delta method: each (step, slot) is a ratio of means.
    influence = np.sum(weights * (values - cell_values) / weights.mean(axis=0), axis=(1, 2))
    return Estimate(float(cell_values.sum()), influence)


ESTIMATOR_NAMES = ("IPS", "SNIPS", "PDIS", "SNPDIS", "Direct", "DR")
SLATE_AWARE_NAMES = ("CascadePDIS", "SNCascadePDIS")

_BUILT_IN: dict[str, Estimator] = {
    "IPS": _ips,
    "SNIPS": _snips,
    "PDIS": _pdis,
    "SNPDIS": _snpdis,
    "Direct": _direct,
    "DR": _dr,
}
# Available by name, but not run by default.
_SLATE_AWARE: dict[str, Estimator] = {
    "CascadePDIS": _cascade_pdis,
    "SNCascadePDIS": _sn_cascade_pdis,
}
_REGISTRY: dict[str, Estimator] = {**_BUILT_IN, **_SLATE_AWARE}


def register_estimator(name: str, estimator: Estimator, *, overwrite: bool = False) -> None:
    """Make ``estimator`` available by ``name`` to ``estimate_all`` and the benchmarks.

    Built-in names can't be replaced. Registration only lasts for the current process, so
    to use a new estimator in the benchmark's worker processes, pass the function itself
    (it must be importable, for example defined at the top level of a module).
    """
    if not callable(estimator):
        raise TypeError("estimator must be callable")
    if name in _BUILT_IN or name in _SLATE_AWARE:
        raise ValueError(f"{name!r} is a built-in estimator and can't be replaced")
    if name in _REGISTRY and not overwrite:
        raise ValueError(f"an estimator named {name!r} is already registered; pass overwrite=True to replace it")
    _REGISTRY[name] = estimator


def available_estimators() -> tuple[str, ...]:
    """Names of every estimator that can be requested, built-in ones first."""
    return tuple(_REGISTRY)


def resolve_estimators(
    estimators: Iterable[str] | Mapping[str, Estimator] | None = None,
) -> dict[str, Estimator]:
    """Turn names, a name-to-function mapping, or ``None`` (the built-ins) into a name-to-function dict."""
    if estimators is None:
        return dict(_BUILT_IN)
    if isinstance(estimators, Mapping):
        resolved = dict(estimators)
        for name, fn in resolved.items():
            if not callable(fn):
                raise TypeError(f"estimator {name!r} is not callable")
        return resolved
    names = list(estimators)
    unknown = [n for n in names if n not in _REGISTRY]
    if unknown:
        raise ValueError(f"unknown estimators {unknown}; available: {list(_REGISTRY)}")
    return {n: _REGISTRY[n] for n in names}


def estimate_all_detailed(
    data: LoggedData,
    values: np.ndarray,
    target: SoftmaxPolicy,
    examine_decay: float,
    rng: np.random.Generator,
    informed: bool = True,
    estimators: Iterable[str] | Mapping[str, Estimator] | None = None,
    slot_values: np.ndarray | None = None,
) -> dict[str, Estimate]:
    """Run each estimator on the same task. Defaults to the built-in estimators."""
    task = EstimationTask(data, values, target, examine_decay, rng, informed, slot_values)
    resolved = resolve_estimators(estimators)
    # Fit the models first whenever Direct or DR is requested, so the random number
    # stream is used in the same order as before estimators were pluggable.
    if "Direct" in resolved or "DR" in resolved:
        task.model_scores()
    results = {}
    for name, fn in resolved.items():
        result = fn(task)
        if not isinstance(result, Estimate):
            result = Estimate(float(result))
        results[name] = result
    return results


def estimate_all(
    data: LoggedData,
    values: np.ndarray,
    target: SoftmaxPolicy,
    examine_decay: float,
    rng: np.random.Generator,
    informed: bool = True,
    estimators: Iterable[str] | Mapping[str, Estimator] | None = None,
    slot_values: np.ndarray | None = None,
) -> dict[str, float]:
    """Point estimates from each estimator. Defaults to the built-in estimators."""
    detailed = estimate_all_detailed(data, values, target, examine_decay, rng, informed, estimators, slot_values)
    return {name: result.value for name, result in detailed.items()}
