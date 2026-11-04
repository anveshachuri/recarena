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
