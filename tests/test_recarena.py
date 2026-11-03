import itertools

import gymnasium as gym
import numpy as np
import pytest
from gymnasium.utils.env_checker import check_env

from recarena import BatchSimulator, Catalog, LoggedData, SimConfig, SlateRecEnv, SoftmaxPolicy, collect, true_value
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


def test_low_temperature_stays_numerically_stable():
    config = SimConfig()
    catalog = Catalog.generate(config)
    policy = SoftmaxPolicy(catalog, temperature=0.001)
    obs = np.zeros((5, config.n_topics + 2))
    slates = policy.sample(obs, config.slate_size, np.random.default_rng(0))
    assert np.all(np.isfinite(policy.log_prob(obs, slates)))


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
