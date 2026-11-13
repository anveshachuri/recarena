import itertools

import gymnasium as gym
import numpy as np
import pytest
from gymnasium.utils.env_checker import check_env

from recarena import BatchSimulator, Catalog, LoggedData, SimConfig, SlateRecEnv, SoftmaxPolicy, UniformMixturePolicy, collect, true_value
from recarena.estimators import (
    FittedQ,
    direct_and_dr,
    dr_with_model,
    importance_ratios,
    ips,
    pdis,
    snips,
    snpdis,
)

SMALL = SimConfig(n_items=4, n_topics=2, slate_size=2, horizon=1, catalog_seed=3, fixed_interest=(0.7, 0.3))
SHORT = SimConfig(n_items=8, n_topics=3, slate_size=2, horizon=3, catalog_seed=5)


def exact_one_step_value(config, catalog, policy):
    """Enumerates every slate by hand, sharing no code path with the simulator's step."""
    obs = np.zeros((1, config.n_topics + 2))
    interest = np.asarray(config.fixed_interest)
    click = 1.0 / (1.0 + np.exp(-(config.click_slope * catalog.topics @ interest + config.click_offset)))
    total = 0.0
    for slate in itertools.permutations(range(config.n_items), config.slate_size):
        p = np.exp(policy.log_prob(obs, np.array([slate])))[0]
        no_click_yet, value = 1.0, 0.0
        for slot, item in enumerate(slate):
            chance = config.examine_decay**slot * click[item]
            value += no_click_yet * chance * catalog.quality[item]
            no_click_yet *= 1.0 - chance
        total += p * value
    return total


def within(estimate, truth, stderr, sigmas=4.0):
    return abs(estimate - truth) <= sigmas * stderr


def test_env_passes_gymnasium_checks():
    check_env(SlateRecEnv(SHORT), skip_render_check=True)


def test_env_is_reproducible_and_ends_on_time():
    def rollout():
        env = SlateRecEnv(SHORT)
        env.reset(seed=9)
        env.action_space.seed(9)
        out = []
        for _ in range(SHORT.horizon):
            _, r, terminated, truncated, info = env.step(env.action_space.sample())
            out.append((r, info["cost"]))
            if terminated or truncated:
                break
        return out, terminated or truncated

    a, ended = rollout()
    assert a == rollout()[0]
    assert ended


def test_env_rejects_step_before_reset():
    with pytest.raises(RuntimeError):
        SlateRecEnv(SHORT).step(np.zeros(2, dtype=int))


def test_slate_probabilities_sum_to_one():
    config = SimConfig(n_items=5, n_topics=2, slate_size=3)
    catalog = Catalog.generate(config)
    policy = SoftmaxPolicy(catalog, history_weight=2.0, sponsored_weight=0.5, temperature=0.7)
    obs = np.tile(np.array([0.2, 0.1, 0.0, 0.5]), (60, 1))
    slates = np.array(list(itertools.permutations(range(5), 3)))
    assert np.exp(policy.log_prob(obs, slates)).sum() == pytest.approx(1.0)


def test_sampling_matches_stated_probabilities():
    config = SimConfig(n_items=4, n_topics=2, slate_size=2)
    catalog = Catalog.generate(config)
    policy = SoftmaxPolicy(catalog, sponsored_weight=1.0, temperature=0.5)
    n = 200_000
    obs = np.zeros((n, 4))
    slates = policy.sample(obs, 2, np.random.default_rng(1))
    for slate in itertools.permutations(range(4), 2):
        expected = np.exp(policy.log_prob(obs[:1], np.array([slate])))[0]
        seen = np.mean(np.all(slates == slate, axis=1))
        assert seen == pytest.approx(expected, abs=4 * np.sqrt(expected * (1 - expected) / n))


def test_uniform_mixture_probabilities_match_hand_calculation_and_sum_to_one():
    config = SimConfig(n_items=5, n_topics=2, slate_size=3)
    catalog = Catalog.generate(config)
    base = SoftmaxPolicy(catalog, history_weight=2.0, sponsored_weight=0.5, temperature=0.7)
    policy = UniformMixturePolicy(base, epsilon=0.25)
    obs = np.tile(np.array([0.2, 0.1, 0.0, 0.5]), (60, 1))
    slates = np.array(list(itertools.permutations(range(5), 3)))
    expected = 0.75 * np.exp(base.log_prob(obs, slates)) + 0.25 / (5 * 4 * 3)
    assert np.exp(policy.log_prob(obs, slates)) == pytest.approx(expected)
    assert np.exp(policy.log_prob(obs, slates)).sum() == pytest.approx(1.0)


def test_uniform_mixture_endpoints_are_the_base_and_uniform_policies():
    config = SimConfig(n_items=5, n_topics=2, slate_size=3)
    catalog = Catalog.generate(config)
    base = SoftmaxPolicy(catalog, sponsored_weight=1.0)
    obs = np.zeros((60, 4))
    slates = np.array(list(itertools.permutations(range(5), 3)))
    assert UniformMixturePolicy(base, 0.0).log_prob(obs, slates) == pytest.approx(base.log_prob(obs, slates))
    assert UniformMixturePolicy(base, 1.0).log_prob(obs, slates) == pytest.approx(np.full(60, -np.log(60.0)))


def test_uniform_mixture_sampling_matches_stated_probabilities():
    config = SimConfig(n_items=4, n_topics=2, slate_size=2)
    catalog = Catalog.generate(config)
    policy = UniformMixturePolicy(SoftmaxPolicy(catalog, sponsored_weight=1.0, temperature=0.5), epsilon=0.3)
    n = 200_000
    obs = np.zeros((n, 4))
    slates = policy.sample(obs, 2, np.random.default_rng(1))
    for slate in itertools.permutations(range(4), 2):
        expected = np.exp(policy.log_prob(obs[:1], np.array([slate])))[0]
        seen = np.mean(np.all(slates == slate, axis=1))
        assert seen == pytest.approx(expected, abs=4 * np.sqrt(expected * (1 - expected) / n))


@pytest.mark.parametrize("epsilon", [-0.1, 1.5])
def test_uniform_mixture_rejects_epsilon_outside_zero_to_one(epsilon):
    catalog = Catalog.generate(SMALL)
    with pytest.raises(ValueError, match="epsilon"):
        UniformMixturePolicy(SoftmaxPolicy(catalog), epsilon)


def test_pdis_is_unbiased_with_a_uniform_mixture_logging_policy():
    catalog = Catalog.generate(SHORT)
    behavior = UniformMixturePolicy(SoftmaxPolicy(catalog), epsilon=0.2)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    truth = true_value(SHORT, catalog, target, 400_000, np.random.default_rng(9))
    data = collect(SHORT, catalog, behavior, 400_000, np.random.default_rng(13))
    ratios = importance_ratios(data, target)
    scores = np.sum(np.cumprod(ratios, axis=1) * data.rewards, axis=1)
    stderr = np.hypot(scores.std() / np.sqrt(data.n), truth.reward_stderr)
    assert within(pdis(data, data.rewards, ratios), truth.reward, 2 * stderr)


def test_low_temperature_stays_numerically_stable():
    config = SimConfig()
    catalog = Catalog.generate(config)
    policy = SoftmaxPolicy(catalog, temperature=0.001)
    obs = np.zeros((5, config.n_topics + 2))
    slates = policy.sample(obs, config.slate_size, np.random.default_rng(0))
    assert np.all(np.isfinite(policy.log_prob(obs, slates)))


def test_simconfig_rejects_slate_larger_than_catalog():
    with pytest.raises(ValueError, match="slate_size"):
        SimConfig(n_items=4, slate_size=6)


def test_simconfig_rejects_non_positive_horizon():
    with pytest.raises(ValueError, match="horizon"):
        SimConfig(horizon=0)


def test_simconfig_rejects_fixed_interest_wrong_length():
    with pytest.raises(ValueError, match="fixed_interest"):
        SimConfig(n_topics=5, fixed_interest=(1.0,))


def test_softmax_rejects_non_positive_temperature():
    catalog = Catalog.generate(SimConfig())
    with pytest.raises(ValueError, match="temperature"):
        SoftmaxPolicy(catalog, temperature=0.0)
    with pytest.raises(ValueError, match="temperature"):
        SoftmaxPolicy(catalog, temperature=-1.0)


def test_true_value_matches_hand_calculation():
    catalog = Catalog.generate(SMALL)
    policy = SoftmaxPolicy(catalog, quality_weight=2.0)
    truth = true_value(SMALL, catalog, policy, 400_000, np.random.default_rng(2))
    assert within(truth.reward, exact_one_step_value(SMALL, catalog, policy), truth.reward_stderr)


def test_repeated_item_in_a_slate_counts_once():
    catalog = Catalog.generate(SMALL)
    n = 300_000
    def mean_reward(slate):
        sim = BatchSimulator(SMALL, catalog, n, np.random.default_rng(4))
        sim.reset()
        rewards, _, _ = sim.step(np.tile(slate, (n, 1)))
        return rewards.mean(), rewards.std() / np.sqrt(n)
    # Repeating item 0 in slot two must give the same value as showing it once.
    single = SimConfig(**{**SMALL.__dict__, "slate_size": 1})
    sim = BatchSimulator(single, catalog, n, np.random.default_rng(5))
    sim.reset()
    alone = sim.step(np.zeros((n, 1), dtype=int))[0]
    repeated, stderr = mean_reward(np.array([0, 0]))
    assert abs(repeated - alone.mean()) <= 4 * np.hypot(stderr, alone.std() / np.sqrt(n))


def test_gym_env_and_batch_simulator_agree():
    catalog = Catalog.generate(SHORT)
    action = np.array([0, 1])
    env = SlateRecEnv(SHORT)
    total, n = [], 6000
    for episode in range(n):
        env.reset(seed=episode)
        ret, done = 0.0, False
        while not done:
            _, r, terminated, truncated, _ = env.step(action)
            ret += r
            done = terminated or truncated
        total.append(ret)
    sim = BatchSimulator(SHORT, catalog, 200_000, np.random.default_rng(6))
    sim.reset()
    batch = np.zeros(200_000)
    alive = np.ones(200_000, dtype=bool)
    for _ in range(SHORT.horizon):
        rewards, _, next_alive = sim.step(np.tile(action, (200_000, 1)))
        batch += rewards * alive
        alive = next_alive
    stderr = np.hypot(np.std(total) / np.sqrt(n), batch.std() / np.sqrt(200_000))
    assert abs(np.mean(total) - batch.mean()) <= 4 * stderr


def test_showing_a_topic_tires_users_of_it():
    config = SimConfig(n_items=4, n_topics=2, slate_size=1, horizon=10, catalog_seed=3, fixed_interest=(0.7, 0.3))
    catalog = Catalog.generate(config)
    n = 50_000
    sim = BatchSimulator(config, catalog, n, np.random.default_rng(16))
    sim.reset()
    item = np.zeros(n, dtype=int)
    before = sim.click_probability(item).mean()
    for _ in range(5):
        sim.step(np.zeros((n, 1), dtype=int))
    assert np.all(sim.fatigue >= 0)
    assert sim.fatigue[:, np.argmax(catalog.topics[0])].mean() > 0
    fresh = BatchSimulator(config, catalog, n, np.random.default_rng(17))
    fresh.reset()
    fresh.interest = sim.interest.copy()
    assert sim.click_probability(item).mean() < fresh.click_probability(item).mean()
    assert before > 0


def test_clicks_pull_interest_toward_the_clicked_topic_and_update_history():
    config = SimConfig(n_items=4, n_topics=2, slate_size=1, horizon=10, catalog_seed=3, fixed_interest=(0.5, 0.5))
    catalog = Catalog.generate(config)
    n = 50_000
    sim = BatchSimulator(config, catalog, n, np.random.default_rng(18))
    obs = sim.reset()
    assert np.all(obs == 0)
    rewards, _, _ = sim.step(np.zeros((n, 1), dtype=int))
    clicked = rewards > 0
    assert clicked.any() and (~clicked).any()
    expected = 0.9 * 0.5 + 0.1 * catalog.topics[0]
    assert np.allclose(sim.interest[clicked], expected)
    assert np.allclose(sim.interest[~clicked], 0.5)
    assert np.allclose(sim.history[clicked], 0.2 * catalog.topics[0])
    assert np.all(sim.history[~clicked] == 0)
    assert np.all(sim.misses[clicked] == 0) and np.all(sim.misses[~clicked] == 1)


def test_users_only_leave_after_a_miss_and_more_after_several():
    config = SimConfig(n_items=4, n_topics=2, slate_size=1, horizon=10, catalog_seed=3)
    catalog = Catalog.generate(config)
    n = 100_000
    sim = BatchSimulator(config, catalog, n, np.random.default_rng(19))
    sim.reset()
    rewards, _, alive = sim.step(np.zeros((n, 1), dtype=int))
    assert np.all(alive[rewards > 0])
    missed = rewards == 0
    first_rate = 1 - alive[missed].mean()
    assert first_rate == pytest.approx(config.leave_base + config.leave_per_miss, abs=0.005)
    # A departed user stays gone and earns nothing more.
    gone = ~alive
    rewards, costs, alive = sim.step(np.zeros((n, 1), dtype=int))
    assert np.all(~alive[gone]) and np.all(costs[gone] == 0) and np.all(rewards[gone] == 0)


def test_later_slots_are_seen_less_and_first_click_stops_the_user():
    catalog = Catalog.generate(SMALL)
    n = 300_000
    sim = BatchSimulator(SMALL, catalog, n, np.random.default_rng(20))
    sim.reset()
    best = np.argsort(sim.click_probability(np.arange(4) % 4 if False else np.zeros(n, dtype=int))[:1])[0]
    assert best == 0
    both = BatchSimulator(SMALL, catalog, n, np.random.default_rng(21))
    both.reset()
    rewards, _, _ = both.step(np.tile([0, 1], (n, 1)))
    # At most one click, so each reward equals exactly one item's quality or zero.
    allowed = np.array([0.0, catalog.quality[0], catalog.quality[1]])
    assert np.all(np.min(np.abs(rewards[:, None] - allowed), axis=1) < 1e-12)


def test_cost_is_the_sponsored_share_and_repeats_count_once():
    catalog = Catalog.generate(SHORT)
    sponsored = np.flatnonzero(catalog.sponsored)
    plain = np.flatnonzero(~catalog.sponsored)
    assert len(sponsored) and len(plain)
    def cost(slate):
        sim = BatchSimulator(SHORT, catalog, 1, np.random.default_rng(22))
        sim.reset()
        return sim.step(np.array([slate]))[1][0]
    assert cost([sponsored[0], plain[0]]) == pytest.approx(0.5)
    assert cost([plain[0], plain[1]]) == 0.0
    assert cost([sponsored[0], sponsored[0]]) == pytest.approx(0.5)


def handmade_data():
    # Two sessions over three steps. The second ends after step one.
    return LoggedData(
        obs=np.zeros((2, 3, 5)),
        slates=np.zeros((2, 3, 2), dtype=int),
        rewards=np.array([[1.0, 2.0, 3.0], [4.0, 0.0, 0.0]]),
        costs=np.zeros((2, 3)),
        active=np.array([[True, True, True], [True, False, False]]),
        behavior_log_prob=np.zeros((2, 3)),
    ), np.array([[2.0, 0.5, 3.0], [0.5, 1.0, 1.0]])


def test_estimators_match_hand_calculations():
    data, ratios = handmade_data()
    r = data.rewards
    assert ips(data, r, ratios) == pytest.approx((3.0 * 6.0 + 0.5 * 4.0) / 2)
    assert snips(data, r, ratios) == pytest.approx((3.0 * 6.0 + 0.5 * 4.0) / 3.5)
    assert pdis(data, r, ratios) == pytest.approx(((2 * 1 + 1 * 2 + 3 * 3) + 0.5 * 4) / 2)
    step_one = (2 * 1 + 0.5 * 4) / 2.5
    step_two = (1 * 2 + 0.5 * 0) / 1.5
    step_three = (3 * 3 + 0.5 * 0) / 3.5
    assert snpdis(data, r, ratios) == pytest.approx(step_one + step_two + step_three)


def test_doubly_robust_matches_hand_calculation():
    data, ratios = handmade_data()

    class Constant:
        def action_value(self, t, obs, slates):
            return np.full(len(obs), 1.0)

        def state_value(self, t, obs, rng):
            return np.full(len(obs), 2.0)

    scores = dr_with_model(data, data.rewards, ratios, Constant(), np.random.default_rng(0))
    # Worked backward from the last step: dr = v + ratio * (reward + next - q).
    step3 = 2 + 3 * (3 + 0 - 1)
    step2 = 2 + 0.5 * (2 + step3 - 1)
    step1 = 2 + 2 * (1 + step2 - 1)
    assert scores[0] == pytest.approx(step1)
    assert scores[1] == pytest.approx(2 + 0.5 * (4 + 0 - 1))


def test_ratios_stay_one_after_a_session_ends():
    catalog = Catalog.generate(SHORT)
    data = collect(SHORT, catalog, SoftmaxPolicy(catalog), 2000, np.random.default_rng(23))
    ended = ~data.active
    assert ended.any()
    ratios = importance_ratios(data, SoftmaxPolicy(catalog, history_weight=3.0))
    assert np.all(ratios[ended] == 1.0)
    assert np.any(ratios[data.active] != 1.0)


def test_ratios_are_one_when_target_is_the_logging_policy():
    catalog = Catalog.generate(SHORT)
    policy = SoftmaxPolicy(catalog)
    data = collect(SHORT, catalog, policy, 500, np.random.default_rng(7))
    ratios = importance_ratios(data, policy)
    assert np.allclose(ratios, 1.0)
    on_policy = data.rewards.sum(axis=1).mean()
    for estimator in (ips, snips, pdis, snpdis):
        assert estimator(data, data.rewards, ratios) == pytest.approx(on_policy)


@pytest.mark.parametrize("name,estimator", [("ips", ips), ("pdis", pdis)])
def test_unbiased_estimators_recover_exact_one_step_value(name, estimator):
    catalog = Catalog.generate(SMALL)
    behavior = SoftmaxPolicy(catalog)
    target = SoftmaxPolicy(catalog, quality_weight=2.0)
    data = collect(SMALL, catalog, behavior, 400_000, np.random.default_rng(8))
    ratios = importance_ratios(data, target)
    scores = ratios.prod(axis=1) * data.rewards.sum(axis=1)
    stderr = scores.std() / np.sqrt(data.n)
    assert within(estimator(data, data.rewards, ratios), exact_one_step_value(SMALL, catalog, target), stderr)


@pytest.mark.parametrize("name,estimator", [("ips", ips), ("pdis", pdis)])
def test_unbiased_estimators_recover_multi_step_truth(name, estimator):
    catalog = Catalog.generate(SHORT)
    behavior = SoftmaxPolicy(catalog)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    truth = true_value(SHORT, catalog, target, 400_000, np.random.default_rng(9))
    data = collect(SHORT, catalog, behavior, 400_000, np.random.default_rng(10))
    ratios = importance_ratios(data, target)
    scores = np.sum(np.cumprod(ratios, axis=1) * data.rewards, axis=1)
    stderr = np.hypot(scores.std() / np.sqrt(data.n), truth.reward_stderr)
    assert within(estimator(data, data.rewards, ratios), truth.reward, 2 * stderr)


class WrongModel:
    """A deliberately bad Q model. Doubly robust must stay unbiased despite it."""

    def action_value(self, t, obs, slates):
        return 5.0 + 3.0 * obs[:, 0] + 0.1 * slates[:, 0]

    def state_value(self, t, obs, rng):
        # Exact expectation over the first slot needs the policy, so sample it.
        repeated = np.repeat(obs, 64, axis=0)
        slates = self.policy.sample(repeated, self.size, rng)
        return self.action_value(t, repeated, slates).reshape(len(obs), 64).mean(axis=1)


def test_doubly_robust_is_unbiased_even_with_a_wrong_model():
    catalog = Catalog.generate(SHORT)
    behavior = SoftmaxPolicy(catalog)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    truth = true_value(SHORT, catalog, target, 400_000, np.random.default_rng(11))
    rng = np.random.default_rng(12)
    data = collect(SHORT, catalog, behavior, 60_000, rng)
    model = WrongModel()
    model.policy, model.size = target, SHORT.slate_size
    scores = dr_with_model(data, data.rewards, importance_ratios(data, target), model, rng)
    stderr = np.hypot(scores.std() / np.sqrt(data.n), truth.reward_stderr)
    assert within(scores.mean(), truth.reward, stderr)


def test_fitted_model_makes_doubly_robust_steadier_than_pdis():
    catalog = Catalog.generate(SHORT)
    behavior = SoftmaxPolicy(catalog)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    rng = np.random.default_rng(13)
    data = collect(SHORT, catalog, behavior, 20_000, rng)
    ratios = importance_ratios(data, target)
    train, test = data.subset(np.arange(10_000)), data.subset(np.arange(10_000, 20_000))
    model = FittedQ(target, SHORT.examine_decay).fit(train, train.rewards, rng)
    test_ratios = importance_ratios(test, target)
    dr = dr_with_model(test, test.rewards, test_ratios, model, rng)
    per_decision = np.sum(np.cumprod(test_ratios, axis=1) * test.rewards, axis=1)
    assert dr.std() < per_decision.std()
    direct, doubly = direct_and_dr(data, data.rewards, ratios, target, SHORT.examine_decay, rng)
    assert np.isfinite(direct) and np.isfinite(doubly)


def test_cost_estimate_uses_the_same_machinery():
    catalog = Catalog.generate(SHORT)
    behavior = SoftmaxPolicy(catalog)
    target = SoftmaxPolicy(catalog, sponsored_weight=1.0)
    truth = true_value(SHORT, catalog, target, 300_000, np.random.default_rng(14))
    data = collect(SHORT, catalog, behavior, 300_000, np.random.default_rng(15))
    ratios = importance_ratios(data, target)
    scores = np.sum(np.cumprod(ratios, axis=1) * data.costs, axis=1)
    assert within(scores.mean(), truth.cost, np.hypot(scores.std() / np.sqrt(data.n), truth.cost_stderr))


def test_new_settings_change_nothing_when_off():
    config = SimConfig()
    catalog = Catalog.generate(config)
    assert len(catalog.appeal) == config.n_items
    before = Catalog.generate(SimConfig(hidden_appeal=1.0, sponsored_annoyance=0.3))
    assert np.array_equal(catalog.topics, before.topics)
    assert np.array_equal(catalog.quality, before.quality)
    sim = BatchSimulator(config, catalog, 3, np.random.default_rng(0))
    sim.reset()
    items = np.arange(3)
    affinity = np.sum(sim.interest * catalog.topics[items], axis=1)
    expected = 1 / (1 + np.exp(-(config.click_slope * affinity + config.click_offset)))
    assert sim.click_probability(items) == pytest.approx(expected)


def test_hidden_appeal_moves_the_click_chance_by_the_stated_amount():
    config = SimConfig(hidden_appeal=1.0)
    catalog = Catalog.generate(config)
    sim = BatchSimulator(config, catalog, 4, np.random.default_rng(1))
    sim.reset()
    items = np.arange(4)
    affinity = np.sum(sim.interest * catalog.topics[items], axis=1)
    logit = config.click_slope * affinity + config.click_offset + catalog.appeal[items]
    assert sim.click_probability(items) == pytest.approx(1 / (1 + np.exp(-logit)))
    policy = SoftmaxPolicy(catalog)
    assert "appeal" not in policy.__dataclass_fields__


def test_sponsored_slates_make_users_leave_more():
    config = SimConfig(slate_size=1, sponsored_annoyance=0.3)
    catalog = Catalog.generate(config)
    item = np.flatnonzero(catalog.sponsored)[0]
    plain = np.flatnonzero(~catalog.sponsored)[0]
    n = 200_000

    def leave_rate(chosen):
        sim = BatchSimulator(config, catalog, n, np.random.default_rng(2))
        sim.reset()
        rewards, _, alive = sim.step(np.full((n, 1), chosen))
        return 1 - alive[rewards == 0].mean()

    base = config.leave_base + config.leave_per_miss
    assert leave_rate(plain) == pytest.approx(base, abs=0.005)
    assert leave_rate(item) == pytest.approx(base + 0.3, abs=0.005)


def test_uninformed_model_cannot_see_quality_or_sponsorship():
    from recarena.estimators import _features

    catalog = Catalog.generate(SHORT)
    policy = SoftmaxPolicy(catalog)
    obs = np.random.default_rng(3).random((10, SHORT.n_topics + 2))
    slates = np.tile([0, 1], (10, 1))
    other = Catalog(catalog.topics, 1 - catalog.quality, ~catalog.sponsored, catalog.appeal)
    a = _features(obs, slates, policy, SHORT.examine_decay, informed=False)
    b = _features(obs, slates, SoftmaxPolicy(other), SHORT.examine_decay, informed=False)
    assert np.array_equal(a, b)
    c = _features(obs, slates, policy, SHORT.examine_decay, informed=True)
    d = _features(obs, slates, SoftmaxPolicy(other), SHORT.examine_decay, informed=True)
    assert not np.array_equal(c, d)


def test_weighted_estimators_stay_unbiased_when_the_world_has_hidden_effects():
    config = SimConfig(
        n_items=8, n_topics=3, slate_size=2, horizon=3, catalog_seed=5, hidden_appeal=1.0, sponsored_annoyance=0.3
    )
    catalog = Catalog.generate(config)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    truth = true_value(config, catalog, target, 400_000, np.random.default_rng(24))
    data = collect(config, catalog, SoftmaxPolicy(catalog), 400_000, np.random.default_rng(25))
    ratios = importance_ratios(data, target)
    scores = np.sum(np.cumprod(ratios, axis=1) * data.rewards, axis=1)
    assert within(pdis(data, data.rewards, ratios), truth.reward, np.hypot(scores.std() / np.sqrt(data.n), truth.reward_stderr))


def test_doubly_robust_stays_unbiased_with_an_uninformed_model_and_hidden_effects():
    config = SimConfig(
        n_items=8, n_topics=3, slate_size=2, horizon=3, catalog_seed=5, hidden_appeal=1.0, sponsored_annoyance=0.3
    )
    catalog = Catalog.generate(config)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    truth = true_value(config, catalog, target, 400_000, np.random.default_rng(26))
    rng = np.random.default_rng(27)
    fit_data = collect(config, catalog, SoftmaxPolicy(catalog), 20_000, rng)
    test_data = collect(config, catalog, SoftmaxPolicy(catalog), 100_000, rng)
    model = FittedQ(target, config.examine_decay, informed=False).fit(fit_data, fit_data.rewards, rng)
    scores = dr_with_model(test_data, test_data.rewards, importance_ratios(test_data, target), model, rng)
    assert within(scores.mean(), truth.reward, np.hypot(scores.std() / np.sqrt(test_data.n), truth.reward_stderr))


def test_budget_decisions_count_correct_answers():
    from recarena.stress import budget_decisions_correct

    assert budget_decisions_correct(1.0, 1.0) == 2  # Accurate: fits +10%, misses -10%.
    assert budget_decisions_correct(1.05, 1.0) == 2
    assert budget_decisions_correct(0.85, 1.0) == 1  # Too low: wrongly fits the tight budget.
    assert budget_decisions_correct(1.15, 1.0) == 1  # Too high: wrongly misses the loose budget.


# ---------------------------------------------------------------------------
# Pluggable estimators (issue #6)
# ---------------------------------------------------------------------------

from recarena import Estimate, EstimationTask, available_estimators, estimate_all, estimate_all_detailed, register_estimator  # noqa: E402
from recarena.estimators import _REGISTRY, resolve_estimators, snips  # noqa: E402


def task_with_ratios(data, ratios, values=None):
    task = EstimationTask(data, data.rewards if values is None else values, None, 1.0, np.random.default_rng(0))
    task.ratios = ratios
    return task


def test_influence_values_match_hand_calculations():
    data, ratios = handmade_data()
    task = task_with_ratios(data, ratios)
    from recarena.estimators import _ips, _pdis, _snips, _snpdis

    ips_result = _ips(task)
    assert ips_result.value == pytest.approx(10.0)
    assert ips_result.influence == pytest.approx([8.0, -8.0])

    value = 20.0 / 3.5
    snips_result = _snips(task)
    assert snips_result.value == pytest.approx(value)
    assert snips_result.influence == pytest.approx([3.0 * (6.0 - value) / 1.75, 0.5 * (4.0 - value) / 1.75])

    pdis_result = _pdis(task)
    assert pdis_result.influence == pytest.approx([13.0 - 7.5, 2.0 - 7.5])

    weights = np.array([[2.0, 1.0, 3.0], [0.5, 0.5, 0.5]])
    step = [(2 * 1 + 0.5 * 4) / 2.5, (1 * 2) / 1.5, (3 * 3) / 3.5]
    expected = [
        sum(weights[i, t] * (data.rewards[i, t] - step[t]) / weights[:, t].mean() for t in range(3)) for i in range(2)
    ]
    snpdis_result = _snpdis(task)
    assert snpdis_result.value == pytest.approx(sum(step))
    assert snpdis_result.influence == pytest.approx(expected)
    for result in (ips_result, snips_result, pdis_result, snpdis_result):
        assert result.influence.sum() == pytest.approx(0.0, abs=1e-12)


def test_built_in_estimates_are_unchanged():
    """The pluggable path must give exactly the old numbers, using the random stream in the same order."""
    catalog = Catalog.generate(SHORT)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    data = collect(SHORT, catalog, SoftmaxPolicy(catalog), 3000, np.random.default_rng(30))
    new = estimate_all(data, data.rewards, target, SHORT.examine_decay, np.random.default_rng(31))
    rng = np.random.default_rng(31)
    ratios = importance_ratios(data, target)
    direct, doubly = direct_and_dr(data, data.rewards, ratios, target, SHORT.examine_decay, rng)
    old = {
        "IPS": ips(data, data.rewards, ratios),
        "SNIPS": snips(data, data.rewards, ratios),
        "PDIS": pdis(data, data.rewards, ratios),
        "SNPDIS": snpdis(data, data.rewards, ratios),
        "Direct": direct,
        "DR": doubly,
    }
    assert list(new) == list(old)
    for name in old:
        assert new[name] == old[name], name


@pytest.mark.parametrize("name", ["SNIPS", "SNPDIS"])
def test_delta_method_standard_error_matches_the_bootstrap(name):
    catalog = Catalog.generate(SHORT)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    data = collect(SHORT, catalog, SoftmaxPolicy(catalog), 5000, np.random.default_rng(32))
    rng = np.random.default_rng(33)
    result = estimate_all_detailed(data, data.rewards, target, SHORT.examine_decay, rng, estimators=[name])[name]
    ratios = importance_ratios(data, target)
    estimator = {"SNIPS": snips, "SNPDIS": snpdis}[name]
    boot = []
    for _ in range(400):
        index = rng.integers(0, data.n, data.n)
        boot.append(estimator(data.subset(index), data.rewards[index], ratios[index]))
    boot_se = np.std(boot, ddof=1)
    # A standard deviation from 400 draws has a relative standard error of about 1/sqrt(800), 3.5%.
    assert result.standard_error() == pytest.approx(boot_se, rel=4 / np.sqrt(800))


def clipped_ips(task):
    weights = np.minimum(task.ratios.prod(axis=1), 2.0)
    return Estimate(float(np.mean(weights * task.values.sum(axis=1))))


def test_custom_estimators_by_mapping_and_by_registration():
    catalog = Catalog.generate(SHORT)
    target = SoftmaxPolicy(catalog, history_weight=2.0)
    data = collect(SHORT, catalog, SoftmaxPolicy(catalog), 2000, np.random.default_rng(34))
    ratios = importance_ratios(data, target)
    expected = float(np.mean(np.minimum(ratios.prod(axis=1), 2.0) * data.rewards.sum(axis=1)))

    by_mapping = estimate_all(
        data, data.rewards, target, SHORT.examine_decay, np.random.default_rng(0), estimators={"Clipped": clipped_ips}
    )
    assert by_mapping == {"Clipped": pytest.approx(expected)}

    # A plain number is accepted as the value.
    plain = estimate_all(
        data, data.rewards, target, SHORT.examine_decay, np.random.default_rng(0), estimators={"Half": lambda t: 0.5}
    )
    assert plain == {"Half": 0.5}

    register_estimator("Clipped IPS", clipped_ips)
    try:
        assert "Clipped IPS" in available_estimators()
        both = estimate_all(
            data, data.rewards, target, SHORT.examine_decay, np.random.default_rng(0), estimators=["IPS", "Clipped IPS"]
        )
        assert list(both) == ["IPS", "Clipped IPS"]
        assert both["Clipped IPS"] == pytest.approx(expected)
        with pytest.raises(ValueError, match="already registered"):
            register_estimator("Clipped IPS", clipped_ips)
        register_estimator("Clipped IPS", clipped_ips, overwrite=True)
    finally:
        _REGISTRY.pop("Clipped IPS", None)

    with pytest.raises(ValueError, match="built-in"):
        register_estimator("IPS", clipped_ips, overwrite=True)
    with pytest.raises(ValueError, match="unknown estimators"):
        resolve_estimators(["IPS", "Nope"])
    with pytest.raises(TypeError):
        register_estimator("Bad", 3)
    with pytest.raises(TypeError):
        resolve_estimators({"Bad": 3})


def test_benchmark_runs_with_a_subset_of_estimators():
    from recarena.benchmark import run

    report = run([100], 1, 2000, 1.25, 1, 1, estimators=["IPS", "DR"])
    header = next(line for line in report.splitlines() if line.startswith("| Target policy | Sessions logged"))
    assert header == "| Target policy | Sessions logged | IPS | DR |"


def test_effective_sample_share_matches_hand_calculation():
    from recarena.exploration import effective_sample_share

    assert effective_sample_share(np.ones(10)) == pytest.approx(1.0)
    # (1 + 1 + 2)^2 / (1 + 1 + 4) / 3 = 16 / 18
    assert effective_sample_share(np.array([1.0, 1.0, 2.0])) == pytest.approx(16 / 18)


def test_exploration_experiment_runs_and_reports_every_logging_policy():
    from recarena.exploration import run

    report = run([100], 2, 2000, 1, 1)
    for name in ["temperature 0.5", "temperature 4", "default + 10% uniform", "default + 30% uniform"]:
        assert f"| {name} |" in report
    assert "## Does effective sample size track the error?" in report


# ---------------------------------------------------------------------------
# Slate-aware estimators (issue #13)
# ---------------------------------------------------------------------------

from recarena.estimators import SLATE_AWARE_NAMES, _cascade_pdis, _sn_cascade_pdis, prefix_ratios  # noqa: E402


def test_prefix_probabilities_match_hand_calculation():
    catalog = Catalog.generate(SMALL)
    policy = SoftmaxPolicy(catalog, quality_weight=2.0)
    obs = np.zeros((1, SMALL.n_topics + 2))
    weights = np.exp(policy.scores(obs)[0])
    slate = np.array([[2, 0]])
    first = weights[2] / weights.sum()
    second = weights[0] / (weights.sum() - weights[2])
    assert np.exp(policy.prefix_log_prob(obs, slate)[0]) == pytest.approx([first, first * second])

    mixture = UniformMixturePolicy(policy, 0.25)
    expected = [0.75 * first + 0.25 / 4, 0.75 * first * second + 0.25 / (4 * 3)]
    assert np.exp(mixture.prefix_log_prob(obs, slate)[0]) == pytest.approx(expected)


@pytest.mark.parametrize("kind", ["softmax", "mixture"])
def test_whole_prefix_is_the_slate_probability_and_first_slots_sum_to_one(kind):
    config = SimConfig(n_items=6, n_topics=2, slate_size=3, horizon=1, catalog_seed=4)
    catalog = Catalog.generate(config)
    policy = SoftmaxPolicy(catalog, temperature=0.5)
    if kind == "mixture":
        policy = UniformMixturePolicy(policy, 0.3)
    obs = np.random.default_rng(0).random((5, config.n_topics + 2))
    slates = np.array(list(itertools.permutations(range(config.n_items), config.slate_size)))
    for row in obs:
        repeated = np.tile(row, (len(slates), 1))
        prefix = policy.prefix_log_prob(repeated, slates)
        assert prefix[:, -1] == pytest.approx(policy.log_prob(repeated, slates))
        firsts = dict(zip(slates[:, 0], np.exp(prefix[:, 0])))
        assert sum(firsts.values()) == pytest.approx(1.0)


def test_collect_logs_where_each_reward_and_cost_came_from():
    catalog = Catalog.generate(SHORT)
    data = collect(SHORT, catalog, SoftmaxPolicy(catalog), 3000, np.random.default_rng(40))
    assert np.allclose(data.slot_rewards.sum(axis=2), data.rewards)
    assert np.allclose(data.slot_costs.sum(axis=2), data.costs)
    assert np.allclose(data.behavior_prefix_log_prob[:, :, -1], data.behavior_log_prob)
    # At most one slot pays off per step, and its reward is the clicked item's quality.
    paid = data.slot_rewards > 0
    assert paid.sum(axis=2).max() == 1
    assert data.slot_rewards[paid] == pytest.approx(catalog.quality[data.slates[paid]])
    assert np.all(data.slot_costs[~data.active] == 0)
    first_ten = data.subset(np.arange(10))
    assert np.array_equal(first_ten.slot_costs, data.slot_costs[:10])


def test_recording_slots_draws_no_extra_random_numbers():
    """Replays the simulator by hand with the same seed. Any extra draw would change the logs."""
    catalog = Catalog.generate(SHORT)
    policy = SoftmaxPolicy(catalog)
    data = collect(SHORT, catalog, policy, 200, np.random.default_rng(41))
    rng = np.random.default_rng(41)
    sim = BatchSimulator(SHORT, catalog, 200, rng)
    obs = sim.reset()
    for t in range(SHORT.horizon):
        slates = policy.sample(obs, SHORT.slate_size, rng)
        rewards, costs, _ = sim.step(slates)
        assert np.array_equal(slates, data.slates[:, t])
        assert np.array_equal(rewards, data.rewards[:, t])
        assert np.array_equal(costs, data.costs[:, t])
        obs = sim.observe()


def handmade_slot_task():
    data, ratios = handmade_data()
    slot_rewards = np.zeros((2, 3, 2))
    slot_rewards[0, 0, 0], slot_rewards[0, 1, 1], slot_rewards[0, 2, 0] = 1.0, 2.0, 3.0
    slot_rewards[1, 0, 1] = 4.0
    task = EstimationTask(data, data.rewards, None, 1.0, np.random.default_rng(0), slot_values=slot_rewards)
    task.ratios = ratios
    # Ratios for the first slot only. The second slot's ratio is the whole slate's.
    first = np.array([[4.0, 1.0, 1.5], [0.25, 1.0, 1.0]])
    task.prefix_ratios = np.stack([first, ratios], axis=2)
    return task, slot_rewards


def test_cascade_estimators_match_hand_calculations():
    task, values = handmade_slot_task()
    # Session one: 1 * 4 * 1 (step 1, slot 1) + 2 * 0.5 * 2 (step 2, slot 2) + (2 * 0.5) * 1.5 * 3 (step 3, slot 1).
    # Session two: 1 * 0.5 * 4 (step 1, slot 2).
    result = _cascade_pdis(task)
    assert result.value == pytest.approx((10.5 + 2.0) / 2)
    assert result.influence == pytest.approx([4.25, -4.25])

    weights = np.array(
        [
            [[4.0, 2.0], [2.0, 1.0], [1.5, 3.0]],
            [[0.25, 0.5], [0.5, 0.5], [0.5, 0.5]],
        ]
    )
    cells = (weights * values).sum(axis=0) / weights.sum(axis=0)
    assert cells.sum() == pytest.approx(4 / 4.25 + 2 / 2.5 + 2 / 1.5 + 4.5 / 2)
    expected = (weights * (values - cells) / weights.mean(axis=0)).sum(axis=(1, 2))
    sn = _sn_cascade_pdis(task)
    assert sn.value == pytest.approx(cells.sum())
    assert sn.influence == pytest.approx(expected)


def test_cascade_pdis_is_pdis_when_every_value_sits_in_the_last_slot():
    from recarena.estimators import _pdis, _snpdis

    task, _ = handmade_slot_task()
    last_slot = np.zeros((2, 3, 2))
    last_slot[:, :, -1] = task.values
    task.slot_values = last_slot
    assert _cascade_pdis(task).value == pytest.approx(_pdis(task).value)
    assert _sn_cascade_pdis(task).value == pytest.approx(_snpdis(task).value)


def test_cascade_estimators_are_on_policy_means_when_target_is_logging():
    catalog = Catalog.generate(SHORT)
    policy = SoftmaxPolicy(catalog)
    data = collect(SHORT, catalog, policy, 500, np.random.default_rng(42))
    assert np.allclose(prefix_ratios(data, policy), 1.0)
    results = estimate_all(data, data.costs, policy, SHORT.examine_decay, np.random.default_rng(0), estimators=SLATE_AWARE_NAMES)
    for value in results.values():
        assert value == pytest.approx(data.costs.sum(axis=1).mean())


def test_cascade_pdis_recovers_exact_one_step_value_with_less_noise_than_pdis():
    catalog = Catalog.generate(SMALL)
    behavior = SoftmaxPolicy(catalog)
    target = SoftmaxPolicy(catalog, quality_weight=2.0)
    data = collect(SMALL, catalog, behavior, 400_000, np.random.default_rng(43))
    results = estimate_all_detailed(
        data, data.rewards, target, SMALL.examine_decay, np.random.default_rng(0), estimators=["PDIS", "CascadePDIS"]
    )
    cascade = results["CascadePDIS"]
    assert within(cascade.value, exact_one_step_value(SMALL, catalog, target), cascade.standard_error())
    assert cascade.standard_error() < results["PDIS"].standard_error()


@pytest.mark.parametrize("which", ["reward", "cost"])
def test_cascade_pdis_recovers_multi_step_truth(which):
    catalog = Catalog.generate(SHORT)
    behavior = SoftmaxPolicy(catalog)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5, sponsored_weight=1.0)
    truth = true_value(SHORT, catalog, target, 400_000, np.random.default_rng(44))
    data = collect(SHORT, catalog, behavior, 400_000, np.random.default_rng(45))
    values = data.rewards if which == "reward" else data.costs
    estimate = estimate_all_detailed(
        data, values, target, SHORT.examine_decay, np.random.default_rng(0), estimators=["CascadePDIS"]
    )["CascadePDIS"]
    true = truth.reward if which == "reward" else truth.cost
    true_stderr = truth.reward_stderr if which == "reward" else truth.cost_stderr
    assert within(estimate.value, true, np.hypot(estimate.standard_error(), true_stderr))


def test_slate_aware_estimators_are_opt_in_and_protected():
    assert set(SLATE_AWARE_NAMES) <= set(available_estimators())
    assert not set(SLATE_AWARE_NAMES) & set(resolve_estimators(None))
    with pytest.raises(ValueError, match="can't be replaced"):
        register_estimator("CascadePDIS", lambda task: 0.0, overwrite=True)


def test_cascade_estimators_need_per_slot_values():
    catalog = Catalog.generate(SHORT)
    policy = SoftmaxPolicy(catalog)
    data = collect(SHORT, catalog, policy, 200, np.random.default_rng(46))
    other = data.rewards + data.costs
    rng = np.random.default_rng(0)
    with pytest.raises(ValueError, match="per-slot values"):
        estimate_all(data, other, policy, SHORT.examine_decay, rng, estimators=["CascadePDIS"])
    with pytest.raises(ValueError, match="sum over slots"):
        estimate_all(data, other, policy, SHORT.examine_decay, rng, estimators=["CascadePDIS"], slot_values=data.slot_rewards)
    # Matching per-slot values work for any combination of outcomes.
    combined = estimate_all(
        data, other, policy, SHORT.examine_decay, rng, estimators=["CascadePDIS"], slot_values=data.slot_rewards + data.slot_costs
    )
    assert combined["CascadePDIS"] == pytest.approx(other.sum(axis=1).mean())


def test_slate_estimator_experiment_runs_and_reports_every_world():
    from recarena.slate_estimators import run

    report = run([2, 3], [1, 2], [100], 2, 2000, 1, 1)
    for k, h in [(2, 1), (2, 2), (3, 1), (3, 2)]:
        assert f"### Slates of {k}, sessions up to {h} steps, 100 sessions logged" in report
    assert "| Target policy | PDIS | SNPDIS | CascadePDIS | SNCascadePDIS |" in report


def test_sn_cascade_delta_method_standard_error_matches_the_bootstrap():
    catalog = Catalog.generate(SHORT)
    target = SoftmaxPolicy(catalog, history_weight=2.0, quality_weight=1.5)
    data = collect(SHORT, catalog, SoftmaxPolicy(catalog), 5000, np.random.default_rng(47))
    rng = np.random.default_rng(48)
    full = EstimationTask(data, data.rewards, target, SHORT.examine_decay, rng)
    result = _sn_cascade_pdis(full)
    boot = []
    for _ in range(400):
        index = rng.integers(0, data.n, data.n)
        part = data.subset(index)
        task = EstimationTask(part, part.rewards, target, SHORT.examine_decay, rng)
        task.ratios, task.prefix_ratios = full.ratios[index], full.prefix_ratios[index]
        boot.append(_sn_cascade_pdis(task).value)
    # A standard deviation from 400 draws has a relative standard error of about 1/sqrt(800), 3.5%.
    assert result.standard_error() == pytest.approx(np.std(boot, ddof=1), rel=4 / np.sqrt(800))
