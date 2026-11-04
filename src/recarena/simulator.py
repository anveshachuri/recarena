"""A batched recommender simulator with hidden user state.

Users have interests that drift and a fatigue that builds up. Neither is shown to
the recommender, which only sees what a real system could log: a summary of past
clicks, how long the user has gone without clicking, and the session step.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SimConfig:
    n_items: int = 50
    n_topics: int = 5
    slate_size: int = 3
    horizon: int = 20
    catalog_seed: int = 0
    sponsored_share: float = 0.2
    examine_decay: float = 0.7  # Chance of looking at each next slot.
    click_slope: float = 6.0
    click_offset: float = -3.0
    interest_drift: float = 0.1
    fatigue_rate: float = 0.15
    fatigue_decay: float = 0.9
    history_decay: float = 0.8
    leave_base: float = 0.02
    leave_per_miss: float = 0.04
    # Every user starts with these interests when set. Otherwise they are random.
    fixed_interest: tuple[float, ...] | None = None
    # How much each item's unlogged appeal moves its click chance. Policies never see it.
    hidden_appeal: float = 0.0
    # Extra chance of leaving after a miss, per unit of sponsored share in the slate.
    sponsored_annoyance: float = 0.0

    def __post_init__(self) -> None:
        if self.slate_size > self.n_items:
            raise ValueError(
                f"slate_size ({self.slate_size}) cannot exceed n_items ({self.n_items})"
            )
        if self.horizon <= 0:
            raise ValueError(f"horizon must be positive, got {self.horizon}")
        if self.fixed_interest is not None and len(self.fixed_interest) != self.n_topics:
            raise ValueError(
                f"fixed_interest length ({len(self.fixed_interest)}) must equal "
                f"n_topics ({self.n_topics})"
            )


@dataclass(frozen=True)
class Catalog:
    topics: np.ndarray  # (n_items, n_topics), each row sums to 1.
    quality: np.ndarray  # (n_items,), reward for a click, in (0, 1).
    sponsored: np.ndarray  # (n_items,), boolean.
    appeal: np.ndarray  # (n_items,), standard normal, hidden from policies and models.

    @classmethod
    def generate(cls, config: SimConfig) -> "Catalog":
        rng = np.random.default_rng(config.catalog_seed)
        return cls(
            topics=rng.dirichlet(np.full(config.n_topics, 0.3), config.n_items),
            quality=rng.beta(2.0, 2.0, config.n_items),
            sponsored=rng.random(config.n_items) < config.sponsored_share,
            appeal=rng.standard_normal(config.n_items),
        )


def observation_size(config: SimConfig) -> int:
    return config.n_topics + 2


class BatchSimulator:
    """Runs many independent users at once. The Gymnasium wrapper uses a batch of one."""

    def __init__(self, config: SimConfig, catalog: Catalog, n_users: int, rng: np.random.Generator):
        self.config = config
        self.catalog = catalog
        self.n_users = n_users
        self.rng = rng

    def reset(self) -> np.ndarray:
        c = self.config
        if c.fixed_interest is None:
            self.interest = self.rng.dirichlet(np.ones(c.n_topics), self.n_users)
        else:
            self.interest = np.tile(np.asarray(c.fixed_interest, dtype=float), (self.n_users, 1))
        self.fatigue = np.zeros((self.n_users, c.n_topics))
        self.history = np.zeros((self.n_users, c.n_topics))
        self.misses = np.zeros(self.n_users)
        self.step_index = 0
        self.alive = np.ones(self.n_users, dtype=bool)
        return self.observe()

    def observe(self) -> np.ndarray:
        c = self.config
        return np.column_stack(
            [
                self.history,
                np.minimum(self.misses / 5.0, 1.0),
                np.full(self.n_users, self.step_index / c.horizon),
            ]
        )

    def click_probability(self, items: np.ndarray) -> np.ndarray:
        """Chance each user clicks the given item if they look at it."""
        c = self.config
        topics = self.catalog.topics[items]
        affinity = np.sum((self.interest - self.fatigue) * topics, axis=1)
        logit = c.click_slope * affinity + c.click_offset + c.hidden_appeal * self.catalog.appeal[items]
        return 1.0 / (1.0 + np.exp(-logit))

    def step(self, slates: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Advance every alive user. Returns rewards, costs, and who is still alive."""
        c = self.config
        n, k = slates.shape
        was_alive = self.alive
        rewards = np.zeros(n)
        clicked_item = np.full(n, -1)

        # An item already shown earlier in the slate is not looked at again.
        # Computed once for all slots and reused by the cascade and cost loops.
        repeated = np.zeros((n, k), dtype=bool)
        for slot in range(1, k):
            items = slates[:, slot]
            repeated[:, slot] = np.any(slates[:, :slot] == items[:, None], axis=1)

        # Cascade: look down the slate in order and stop at the first click.
        browsing = was_alive.copy()
        for slot in range(k):
            items = slates[:, slot]
            looks = self.rng.random(n) < c.examine_decay**slot
            clicks = self.rng.random(n) < self.click_probability(items)
            hit = browsing & looks & clicks & ~repeated[:, slot]
            rewards[hit] = self.catalog.quality[items[hit]]
            clicked_item[hit] = items[hit]
            browsing &= ~hit

        shown_sponsored = np.zeros(n)
        for slot in range(k):
            items = slates[:, slot]
            shown_sponsored += self.catalog.sponsored[items] & ~repeated[:, slot]
        costs = np.where(was_alive, shown_sponsored / k, 0.0)

        # Showing a topic tires the user of it, whether or not they click.
        shown_topics = self.catalog.topics[slates].mean(axis=1)
        self.fatigue = c.fatigue_decay * self.fatigue + c.fatigue_rate * shown_topics

        clicked = clicked_item >= 0
        clicked_topics = np.zeros_like(self.history)
        clicked_topics[clicked] = self.catalog.topics[clicked_item[clicked]]
        self.history = c.history_decay * self.history + (1.0 - c.history_decay) * clicked_topics
        self.interest[clicked] = (1.0 - c.interest_drift) * self.interest[clicked] + c.interest_drift * clicked_topics[clicked]
        self.misses = np.where(clicked, 0.0, self.misses + 1.0)

        # Users may give up after a miss, and they give up sooner after several.
        leave_chance = np.clip(
            c.leave_base + c.leave_per_miss * self.misses + c.sponsored_annoyance * shown_sponsored / k, 0.0, 1.0
        )
        leaves = ~clicked & (self.rng.random(n) < leave_chance)
        self.step_index += 1
        self.alive = was_alive & ~leaves
        if self.step_index >= c.horizon:
            self.alive = np.zeros(n, dtype=bool)
        return rewards, costs, self.alive.copy()
