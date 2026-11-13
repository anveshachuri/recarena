"""Stochastic slate policies whose probabilities can be computed exactly."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .simulator import Catalog


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
