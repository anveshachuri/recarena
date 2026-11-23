"""Logging a policy's sessions, and measuring a policy's true value by running it."""

from __future__ import annotations

from dataclasses import dataclass, replace

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
    # Optional, for independent IPS: log chance that the logged item in slot j lands in slot j,
    # over everything else in the slate. NaN where it wasn't computed. ``with_slot_log_prob``
    # fills it in. ``collect`` doesn't, because it is slow to compute.
    behavior_slot_log_prob: np.ndarray | None = None  # (n, horizon, slate_size)

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
            pick(self.behavior_slot_log_prob),
        )


def collect(
    config: SimConfig,
    catalog: Catalog,
    policy: SoftmaxPolicy,
    n: int,
    rng: np.random.Generator,
    logged_policy: SoftmaxPolicy | None = None,
) -> LoggedData:
    """Runs ``policy`` for ``n`` sessions and logs what it did.

    The logged probabilities come from ``policy`` unless ``logged_policy`` is given, which
    mimics logs whose probabilities are estimated or slightly wrong (issue #20). It uses no
    random numbers, so the sessions are the same either way.
    """
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
    if logged_policy is not None:
        data = relog(data, logged_policy)
    return data


def relog(data: LoggedData, policy) -> LoggedData:
    """The same sessions, with logged probabilities recomputed as if ``policy`` had acted."""
    n, h, k = data.slates.shape
    flat_obs = data.obs.reshape(n * h, -1)
    flat_slates = data.slates.reshape(n * h, k)
    data = replace(
        data,
        behavior_log_prob=policy.log_prob(flat_obs, flat_slates).reshape(n, h),
        behavior_prefix_log_prob=policy.prefix_log_prob(flat_obs, flat_slates).reshape(n, h, k),
    )
    if data.behavior_slot_log_prob is not None:
        data = with_slot_log_prob(data, policy, np.isfinite(data.behavior_slot_log_prob))
    return data


def with_slot_log_prob(data: LoggedData, policy, where: np.ndarray | None = None) -> LoggedData:
    """The same logs with ``behavior_slot_log_prob`` filled in from ``policy``.

    ``where`` (n, horizon, slate_size) picks the entries to compute, since each one is slow.
    By default it is every slot of every step the user was still there for. Independent IPS
    only needs the slots whose value is not zero, so
    ``where=(data.slot_rewards != 0) | (data.slot_costs != 0)`` is enough for rewards and costs.
    Uses no random numbers.
    """
    n, h, k = data.slates.shape
    if where is None:
        where = np.broadcast_to(data.active[:, :, None], (n, h, k))
    where = np.asarray(where, dtype=bool) & data.active[:, :, None]
    flat = policy.slot_log_prob(data.obs.reshape(n * h, -1), data.slates.reshape(n * h, k), where.reshape(n * h, k))
    return replace(data, behavior_slot_log_prob=flat.reshape(n, h, k))


def check_gamma(gamma: float) -> float:
    """A discount factor must be between 0 and 1. 1 (the default) means no discounting."""
    gamma = float(gamma)
    if not 0.0 <= gamma <= 1.0:
        raise ValueError(f"gamma must be between 0 and 1, got {gamma}")
    return gamma


def discounts(horizon: int, gamma: float) -> np.ndarray:
    """``gamma ** t`` for each step ``t`` from 0 to ``horizon - 1``."""
    return check_gamma(gamma) ** np.arange(horizon)


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
    gamma: float = 1.0,
) -> TrueValue:
    """The answer every estimator is scored against: run the policy itself many times.

    With ``gamma < 1`` the value is the discounted return, which counts what happens at
    step ``t`` (starting from 0) times ``gamma ** t``.
    """
    gamma = check_gamma(gamma)
    reward_returns, cost_returns = [], []
    remaining = n
    while remaining > 0:
        size = min(chunk, remaining)
        sim = BatchSimulator(config, catalog, size, rng)
        obs = sim.reset()
        reward_sum, cost_sum = np.zeros(size), np.zeros(size)
        for t in range(config.horizon):
            rewards, costs, _ = sim.step(policy.sample(obs, config.slate_size, rng))
            if gamma != 1.0:
                rewards, costs = gamma**t * rewards, gamma**t * costs
            reward_sum += rewards
            cost_sum += costs
            obs = sim.observe()
        reward_returns.append(reward_sum)
        cost_returns.append(cost_sum)
        remaining -= size
    r, c = np.concatenate(reward_returns), np.concatenate(cost_returns)
    return TrueValue(r.mean(), r.std() / np.sqrt(n), c.mean(), c.std() / np.sqrt(n))
