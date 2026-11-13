"""Logging a policy's sessions, and measuring a policy's true value by running it."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .policies import SoftmaxPolicy
from .simulator import BatchSimulator, Catalog, SimConfig


@dataclass
class LoggedData:
    obs: np.ndarray  # (n, horizon, obs_size)
    slates: np.ndarray  # (n, horizon, slate_size)
    rewards: np.ndarray  # (n, horizon)
    costs: np.ndarray  # (n, horizon)
    active: np.ndarray  # (n, horizon), True while the user is still in the session.
    behavior_log_prob: np.ndarray  # (n, horizon)
    # Optional, for slate-aware estimators. ``collect`` fills them in.
    slot_rewards: np.ndarray | None = None  # (n, horizon, slate_size), the reward each slot produced.
    slot_costs: np.ndarray | None = None  # (n, horizon, slate_size), the cost each slot added.
    behavior_prefix_log_prob: np.ndarray | None = None  # (n, horizon, slate_size)

    @property
    def n(self) -> int:
        return self.obs.shape[0]

    @property
    def horizon(self) -> int:
        return self.obs.shape[1]

    def subset(self, index: np.ndarray) -> "LoggedData":
        def pick(array):
            return None if array is None else array[index]

        return LoggedData(
            self.obs[index],
            self.slates[index],
            self.rewards[index],
            self.costs[index],
            self.active[index],
            self.behavior_log_prob[index],
            pick(self.slot_rewards),
            pick(self.slot_costs),
            pick(self.behavior_prefix_log_prob),
        )


def collect(
    config: SimConfig, catalog: Catalog, policy: SoftmaxPolicy, n: int, rng: np.random.Generator
) -> LoggedData:
    sim = BatchSimulator(config, catalog, n, rng)
    obs = sim.reset()
    h, k = config.horizon, config.slate_size
    data = LoggedData(
        obs=np.zeros((n, h, obs.shape[1])),
        slates=np.zeros((n, h, k), dtype=np.int64),
        rewards=np.zeros((n, h)),
        costs=np.zeros((n, h)),
        active=np.zeros((n, h), dtype=bool),
        behavior_log_prob=np.zeros((n, h)),
        slot_rewards=np.zeros((n, h, k)),
        slot_costs=np.zeros((n, h, k)),
        behavior_prefix_log_prob=np.zeros((n, h, k)),
    )
    alive = np.ones(n, dtype=bool)
    for t in range(h):
        slates = policy.sample(obs, k, rng)
        data.obs[:, t] = obs
        data.slates[:, t] = slates
        data.active[:, t] = alive
        data.behavior_log_prob[:, t] = policy.log_prob(obs, slates)
        data.behavior_prefix_log_prob[:, t] = policy.prefix_log_prob(obs, slates)
        rewards, costs, next_alive = sim.step(slates)
        data.rewards[:, t] = rewards
        data.costs[:, t] = costs
        data.slot_rewards[:, t] = sim.last_slot_rewards
        data.slot_costs[:, t] = sim.last_slot_costs
        alive = next_alive
        obs = sim.observe()
    return data


@dataclass(frozen=True)
class TrueValue:
    reward: float
    reward_stderr: float
    cost: float
    cost_stderr: float


def true_value(
    config: SimConfig,
    catalog: Catalog,
    policy: SoftmaxPolicy,
    n: int,
    rng: np.random.Generator,
    chunk: int = 50_000,
) -> TrueValue:
    """The answer every estimator is scored against: run the policy itself many times."""
    reward_returns, cost_returns = [], []
    remaining = n
    while remaining > 0:
        size = min(chunk, remaining)
        sim = BatchSimulator(config, catalog, size, rng)
        obs = sim.reset()
        reward_sum, cost_sum = np.zeros(size), np.zeros(size)
        for _ in range(config.horizon):
            rewards, costs, _ = sim.step(policy.sample(obs, config.slate_size, rng))
            reward_sum += rewards
            cost_sum += costs
            obs = sim.observe()
        reward_returns.append(reward_sum)
        cost_returns.append(cost_sum)
        remaining -= size
    r, c = np.concatenate(reward_returns), np.concatenate(cost_returns)
    return TrueValue(r.mean(), r.std() / np.sqrt(n), c.mean(), c.std() / np.sqrt(n))
