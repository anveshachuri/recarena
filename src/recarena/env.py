"""Gymnasium interface to the simulator, for training RL agents."""

from __future__ import annotations

import gymnasium as gym
import numpy as np

from .simulator import BatchSimulator, Catalog, SimConfig, observation_size


class SlateRecEnv(gym.Env):
    """Recommend a slate of items to one user per episode.

    The action is one item id per slot. A repeated item in a slate only counts once.
    ``info["cost"]`` reports the share of the slate that was sponsored, so constrained
    methods can treat it as a budget.
    """

    metadata = {"render_modes": []}

    def __init__(self, config: SimConfig | None = None):
        self.config = config or SimConfig()
        self.catalog = Catalog.generate(self.config)
        self.observation_space = gym.spaces.Box(
            low=0.0, high=1.0, shape=(observation_size(self.config),), dtype=np.float64
        )
        self.action_space = gym.spaces.MultiDiscrete([self.config.n_items] * self.config.slate_size)
        self._sim: BatchSimulator | None = None

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self._sim = BatchSimulator(self.config, self.catalog, 1, self.np_random)
        return self._sim.reset()[0], {}

    def step(self, action):
        if self._sim is None:
            raise RuntimeError("call reset() before step()")
        slates = np.asarray(action, dtype=np.int64).reshape(1, -1)
        rewards, costs, alive = self._sim.step(slates)
        out_of_time = self._sim.step_index >= self.config.horizon
        terminated = not alive[0] and not out_of_time
        return self._sim.observe()[0], float(rewards[0]), terminated, out_of_time, {"cost": float(costs[0])}
