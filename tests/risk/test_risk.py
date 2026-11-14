import unittest

from trading_intel import risk


class TestRMultiples(unittest.TestCase):
    def test_long_success(self):
        self.assertAlmostEqual(risk.r_multiple(100, 95, 110), 2.0)

    def test_long_failure(self):
        self.assertAlmostEqual(risk.r_multiple(100, 95, 95), -1.0)

    def test_short_success(self):
        self.assertAlmostEqual(risk.r_multiple(100, 105, 90, "short"), 2.0)

    def test_zero_risk_rejected(self):
        with self.assertRaises(ValueError):
            risk.risk_per_unit(100, 100)

    def test_bad_direction(self):
        with self.assertRaises(ValueError):
            risk.r_multiple(100, 95, 110, "sideways")

    def test_reward_risk(self):
        self.assertAlmostEqual(risk.reward_risk(100, 95, 112), 2.4)

    def test_target_behind_entry_is_negative(self):
        self.assertLess(risk.reward_risk(100, 95, 97), 0)


class TestBreakEven(unittest.TestCase):
    def test_no_costs_at_1_to_1(self):
        self.assertAlmostEqual(risk.break_even_win_rate(1.0), 0.5)

    def test_no_costs_at_2_to_1(self):
        self.assertAlmostEqual(risk.break_even_win_rate(2.0), 1 / 3)

    def test_costs_raise_the_bar(self):
        self.assertGreater(risk.break_even_win_rate(1.0, 0.3), 0.5)
        self.assertAlmostEqual(risk.break_even_win_rate(1.0, 0.3), 1.3 / 2.0)

    def test_costs_can_make_it_impossible(self):
        self.assertEqual(risk.break_even_win_rate(0.5, 0.5), 1.0)

    def test_zero_rr_rejected(self):
        with self.assertRaises(ValueError):
            risk.break_even_win_rate(0)


class TestExpectancy(unittest.TestCase):
    def test_positive_edge(self):
        self.assertAlmostEqual(risk.expectancy(0.5, 2.0), 0.5)

    def test_negative_edge(self):
        self.assertAlmostEqual(risk.expectancy(0.3, 1.0), -0.4)

    def test_zero_edge(self):
        self.assertAlmostEqual(risk.expectancy(1 / 3, 2.0), 0.0)

    def test_bad_win_rate(self):
        with self.assertRaises(ValueError):
            risk.expectancy(1.5, 2.0)


class TestDrawdown(unittest.TestCase):
    def test_max_drawdown(self):
        equity = [100, 120, 90, 110, 60]
        self.assertAlmostEqual(risk.max_drawdown(equity), 0.5)

    def test_no_drawdown(self):
        self.assertEqual(risk.max_drawdown([100, 110, 120]), 0.0)

    def test_recovery_gain(self):
        self.assertAlmostEqual(risk.recovery_gain_required(0.5), 1.0)
        self.assertAlmostEqual(risk.recovery_gain_required(0.25), 1 / 3)

    def test_recovery_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            risk.recovery_gain_required(1.0)

    def test_ruin_trade_count(self):
        # equity after n losses = 0.98^n ; the first n with 0.98^n <= 0.5 is 35
        self.assertEqual(risk.risk_of_ruin(0.02, 0.5), 35)


class TestTradePlan(unittest.TestCase):
    def test_summary(self):
        plan = risk.TradePlan("long", 100, 95, [107, 112, 120])
        summary = plan.summary()
        self.assertAlmostEqual(summary["R_T1"], 1.4)
        self.assertAlmostEqual(summary["R_T2"], 2.4)
        self.assertEqual(summary["invalidation"], 95)

    def test_warns_below_min_rr(self):
        plan = risk.TradePlan("long", 100, 95, [105])
        self.assertTrue(plan.validation_warnings())

    def test_no_warning_above_min_rr(self):
        plan = risk.TradePlan("long", 100, 95, [110])
        self.assertEqual(plan.validation_warnings(), [])

    def test_target_wrong_side_rejected(self):
        with self.assertRaises(ValueError):
            risk.TradePlan("long", 100, 95, [90])

    def test_short_plan(self):
        plan = risk.TradePlan("short", 100, 105, [90, 85])
        self.assertAlmostEqual(plan.target_r(0), 2.0)

    def test_no_targets_rejected(self):
        with self.assertRaises(ValueError):
            risk.TradePlan("long", 100, 95, [])

    def test_zero_risk_rejected(self):
        with self.assertRaises(ValueError):
            risk.TradePlan("long", 100, 100, [110])


if __name__ == "__main__":
    unittest.main()
