"""Stochastic slate policies whose probabilities can be computed exactly."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.polynomial.laguerre import laggauss

from .simulator import Catalog

# Gauss-Laguerre nodes for the slot probabilities below.
_LAGUERRE_NODES, _LAGUERRE_WEIGHTS = laggauss(20)


def plackett_luce_slot_log_prob(
    scores: np.ndarray, slates: np.ndarray, where: np.ndarray | None = None, chunk: int = 4096
) -> np.ndarray:
    """Log chance that item ``slates[r, j]`` lands in slot ``j``, whatever fills the other slots.

    ``scores`` (rows, n_items) are Plackett-Luce log weights and ``slates`` (rows, slate_size)
    the items. This is the marginal probability that independent (item-position) IPS uses,
    not the probability of the slate's first ``j + 1`` slots.

    It uses the Gumbel form of Plackett-Luce. With ``p`` the softmax of the scores, item
    ``i`` lands in slot ``j`` (from 0) with probability

        p_i * integral over s > 0 of exp(-s) * e_j(exp(p_m s) - 1 for every m != i) ds,

    where ``e_j`` is the elementary symmetric polynomial of degree ``j``. Slot 0 is just
    ``p_i``. The integral is done with Gauss-Laguerre quadrature after rescaling ``s`` by
    one minus the largest mass that ``slate_size - 1`` items can hold, so the integrand
    stays smooth. That is accurate to about 1e-12 when that mass is under one half, and
    the function refuses policies where it is over 0.6 (checked against brute force in
    the tests). The policies in this repo stay under 0.35.

    ``where`` (rows, slate_size), if given, picks the entries to compute. The others are NaN.
    """
    scores = np.asarray(scores, dtype=float)
    slates = np.asarray(slates)
    n_rows, k = slates.shape
    where = np.ones((n_rows, k), dtype=bool) if where is None else np.asarray(where, dtype=bool)
    if n_rows > chunk:
        return np.concatenate(
            [
                _slot_log_prob(scores[i : i + chunk], slates[i : i + chunk], where[i : i + chunk])
                for i in range(0, n_rows, chunk)
            ]
        )
    return _slot_log_prob(scores, slates, where)


def _slot_log_prob(scores: np.ndarray, slates: np.ndarray, where: np.ndarray) -> np.ndarray:
    n_rows, k = slates.shape
    out = np.full((n_rows, k), np.nan)
    logp = scores - scores.max(axis=1, keepdims=True)
    logp = logp - np.log(np.exp(logp).sum(axis=1, keepdims=True))
    first = where[:, 0]
    out[first, 0] = logp[first, slates[first, 0]]
    rows = np.flatnonzero(where[:, 1:].any(axis=1)) if k > 1 else np.array([], dtype=int)
    if len(rows) == 0:
        return out
    p = np.exp(logp[rows])
    top = -np.sort(-p, axis=1)[:, : k - 1]
    largest = top[:, 0]
    mass = top.sum(axis=1)
    if np.any(mass > 0.6):
        raise ValueError(
            "this policy is too peaked for the slot probability quadrature "
            f"({k - 1} items hold up to {mass.max():.0%} of the probability; the limit is 60%)"
        )
    rate = 1.0 - mass
    s = _LAGUERRE_NODES[None, :] / rate[:, None]  # (rows, nodes)
    # x_m = (exp(p_m s) - 1) * exp(-largest * s), between 0 and 1 since p_m <= largest.
    # e_j is homogeneous of degree j, so the scale comes back as exp(j * largest * s).
    # Items go first in x, so the loop over them reads contiguous memory.
    shrink = np.exp(-largest[:, None] * s)
    x = np.expm1(p.T[:, :, None] * s[None, :, :]) * shrink[None, :, :]  # (n_items, rows, nodes)
    e = np.zeros((k,) + s.shape)
    e[0] = 1.0
    for xm in x:
        for count in range(k - 1, 0, -1):
            e[count] += xm * e[count - 1]
    log_weights = np.log(_LAGUERRE_WEIGHTS)[None, :]
    for j in range(1, k):
        pick = np.flatnonzero(where[rows, j])
        if len(pick) == 0:
            continue
        r = rows[pick]
        items = slates[r, j]
        xi = x[items, pick]
        # Take item i back out: e_c(without i) = e_c - x_i * e_{c-1}(without i).
        without = np.ones_like(xi)
        for count in range(1, j + 1):
            without = e[count][pick] - xi * without
        without = np.maximum(without, 0.0)
        # The integrand is exp(-s) e_j(...) = exp(-rate s) * e_j(x) * exp((j largest - mass) s),
        # and Gauss-Laguerre in rate * s takes care of exp(-rate s).
        with np.errstate(divide="ignore"):
            log_terms = np.log(without) + (j * largest[pick] - mass[pick])[:, None] * s[pick] + log_weights
        peak = log_terms.max(axis=1, keepdims=True)
        log_integral = peak[:, 0] + np.log(np.exp(log_terms - peak).sum(axis=1)) - np.log(rate[pick])
        out[r, j] = logp[r, items] + log_integral
    return out


@dataclass(frozen=True)
class SoftmaxPolicy:
    """Scores items, then fills slots one at a time without replacement (Plackett-Luce).

    Off-policy evaluation needs the exact probability of each logged slate, which this
    form gives in closed form.
    """

    catalog: Catalog
    name: str = "policy"
    history_weight: float = 1.0
    quality_weight: float = 1.0
    sponsored_weight: float = 0.0
    temperature: float = 1.0

    def __post_init__(self) -> None:
        if self.temperature <= 0:
            raise ValueError(f"temperature must be positive, got {self.temperature}")

    def scores(self, obs: np.ndarray) -> np.ndarray:
        n_topics = self.catalog.topics.shape[1]
        raw = (
            self.history_weight * obs[:, :n_topics] @ self.catalog.topics.T
            + self.quality_weight * self.catalog.quality
            + self.sponsored_weight * self.catalog.sponsored
        )
        return raw / self.temperature

    def sample(self, obs: np.ndarray, slate_size: int, rng: np.random.Generator) -> np.ndarray:
        # Adding Gumbel noise and taking the top items samples Plackett-Luce exactly.
        scores = self.scores(obs)
        noisy = scores + rng.gumbel(size=scores.shape)
        return np.argsort(-noisy, axis=1)[:, :slate_size]

    def log_prob(self, obs: np.ndarray, slates: np.ndarray) -> np.ndarray:
        scores = self.scores(obs).copy()
        rows = np.arange(len(obs))
        total = np.zeros(len(obs))
        for slot in range(slates.shape[1]):
            items = slates[:, slot]
            top = scores.max(axis=1, keepdims=True)
            with np.errstate(divide="ignore"):
                denominator = top[:, 0] + np.log(np.exp(scores - top).sum(axis=1))
            total += scores[rows, items] - denominator
            scores[rows, items] = -np.inf
        return total

    def prefix_log_prob(self, obs: np.ndarray, slates: np.ndarray) -> np.ndarray:
        """Log probability of each slate's first ``j + 1`` slots, for every ``j``. Shape (n, slate_size).

        The last column is the whole slate's log probability. Slate-aware estimators use
        the earlier columns, since a reward in slot ``j`` depends only on slots up to ``j``.
        """
        scores = self.scores(obs).copy()
        rows = np.arange(len(obs))
        out = np.zeros(slates.shape, dtype=float)
        total = np.zeros(len(obs))
        for slot in range(slates.shape[1]):
            items = slates[:, slot]
            top = scores.max(axis=1, keepdims=True)
            with np.errstate(divide="ignore"):
                denominator = top[:, 0] + np.log(np.exp(scores - top).sum(axis=1))
            total = total + scores[rows, items] - denominator
            out[:, slot] = total
            scores[rows, items] = -np.inf
        return out

    def slot_log_prob(self, obs: np.ndarray, slates: np.ndarray, where: np.ndarray | None = None) -> np.ndarray:
        """Log chance that each slate's item in slot ``j`` lands in slot ``j``. Shape (n, slate_size).

        Marginal over what fills the other slots. See ``plackett_luce_slot_log_prob``.
        """
        return plackett_luce_slot_log_prob(self.scores(obs), slates, where)


@dataclass(frozen=True)
class UniformMixturePolicy:
    """With chance ``epsilon`` shows a uniformly random slate, otherwise follows ``base``.

    A standard way to add exploration to a logging policy. The slate probability is the
    exact mixture ``(1 - epsilon) * base + epsilon * uniform``, so it can be logged and
    used in importance weights like any other policy here.
    """

    base: SoftmaxPolicy
    epsilon: float = 0.1
    name: str = "uniform mixture"

    def __post_init__(self) -> None:
        if not 0.0 <= self.epsilon <= 1.0:
            raise ValueError(f"epsilon must be between 0 and 1, got {self.epsilon}")

    def sample(self, obs: np.ndarray, slate_size: int, rng: np.random.Generator) -> np.ndarray:
        slates = self.base.sample(obs, slate_size, rng)
        explore = rng.random(len(obs)) < self.epsilon
        if explore.any():
            # Random keys sorted give a uniformly random ordered slate without replacement.
            keys = rng.random((int(explore.sum()), self.base.catalog.quality.shape[0]))
            slates[explore] = np.argsort(keys, axis=1)[:, :slate_size]
        return slates

    def log_prob(self, obs: np.ndarray, slates: np.ndarray) -> np.ndarray:
        n_items = self.base.catalog.quality.shape[0]
        uniform = -np.sum(np.log(n_items - np.arange(slates.shape[1])))
        with np.errstate(divide="ignore"):
            return np.logaddexp(
                np.log1p(-self.epsilon) + self.base.log_prob(obs, slates),
                np.log(self.epsilon) + uniform,
            )

    def prefix_log_prob(self, obs: np.ndarray, slates: np.ndarray) -> np.ndarray:
        """Log probability of each slate's first ``j + 1`` slots, for every ``j``. Shape (n, slate_size)."""
        n_items = self.base.catalog.quality.shape[0]
        uniform = -np.cumsum(np.log(n_items - np.arange(slates.shape[1])))
        with np.errstate(divide="ignore"):
            return np.logaddexp(
                np.log1p(-self.epsilon) + self.base.prefix_log_prob(obs, slates),
                np.log(self.epsilon) + uniform,
            )

    def slot_log_prob(self, obs: np.ndarray, slates: np.ndarray, where: np.ndarray | None = None) -> np.ndarray:
        """Log chance that each slate's item in slot ``j`` lands in slot ``j``. Shape (n, slate_size).

        A uniformly random slate puts any item in any slot with chance ``1 / n_items``.
        """
        n_items = self.base.catalog.quality.shape[0]
        with np.errstate(divide="ignore"):
            return np.logaddexp(
                np.log1p(-self.epsilon) + self.base.slot_log_prob(obs, slates, where),
                np.log(self.epsilon) - np.log(n_items),
            )
