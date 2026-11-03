"""Off-policy estimators: the value of a new policy, from another policy's logs.

Every estimator takes ``values``, a (n, horizon) array of per-step outcomes. Passing
rewards estimates the policy's reward. Passing costs estimates its budget use.
"""

from __future__ import annotations

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
    order = rng.permutation(data.n)
    folds = np.array_split(order, 2)
    direct_scores = np.zeros(data.n)
    dr_scores = np.zeros(data.n)
    for held_out, fit_on in ((folds[0], folds[1]), (folds[1], folds[0])):
        model = FittedQ(target, examine_decay, informed=informed).fit(data.subset(fit_on), values[fit_on], rng)
        part = data.subset(held_out)
        direct_scores[held_out] = model.state_value(0, part.obs[:, 0], rng)
        dr_scores[held_out] = dr_with_model(part, values[held_out], ratios[held_out], model, rng)
    return float(direct_scores.mean()), float(dr_scores.mean())


ESTIMATOR_NAMES = ("IPS", "SNIPS", "PDIS", "SNPDIS", "Direct", "DR")


def estimate_all(
    data: LoggedData,
    values: np.ndarray,
    target: SoftmaxPolicy,
    examine_decay: float,
    rng: np.random.Generator,
    informed: bool = True,
) -> dict[str, float]:
    ratios = importance_ratios(data, target)
    direct, dr = direct_and_dr(data, values, ratios, target, examine_decay, rng, informed)
    return {
        "IPS": ips(data, values, ratios),
        "SNIPS": snips(data, values, ratios),
        "PDIS": pdis(data, values, ratios),
        "SNPDIS": snpdis(data, values, ratios),
        "Direct": direct,
        "DR": dr,
    }
