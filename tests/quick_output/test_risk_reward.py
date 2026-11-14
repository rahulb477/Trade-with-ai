"""Risk/reward calculations: correctness, cost adjustment, break-even."""
import unittest
from trading_intel.quick_signal import calculate_targets, calculate_risk_reward, build_quick_signal
from trading_intel import risk as risk_mod


class TestRiskRewardMath(unittest.TestCase):
    """Prompt §16.14 risk/reward calculations."""

    def test_long_rr_basic(self):
        t = calculate_targets(direction="long", entry=100, levels=[107, 112, 120])
        rr = calculate_risk_reward(direction="long", entry=100, stop=95, targets=t)
        self.assertAlmostEqual(rr.rr_t1, 1.4, places=2)  # (107-100)/5
        self.assertAlmostEqual(rr.rr_t2, 2.4, places=2)
        self.assertAlmostEqual(rr.rr_t3, 4.0, places=2)

    def test_short_rr_basic(self):
        t = calculate_targets(direction="short", entry=100, levels=[93, 88, 80])
        rr = calculate_risk_reward(direction="short", entry=100, stop=105, targets=t)
        self.assertAlmostEqual(rr.rr_t1, 1.4, places=2)
        self.assertAlmostEqual(rr.rr_t2, 2.4, places=2)

    def test_cost_adjusted_rr(self):
        t = calculate_targets(direction="long", entry=100, levels=[107], atr=5)
        rr = calculate_risk_reward(direction="long", entry=100, stop=95, targets=t, cost_bos=10) if False else None
        # Use cost_bps = 100 -> 1% slippage, cost_R = 0.01*100/5=0.20
        rr2 = calculate_risk_reward(direction="long", entry=100, stop=95, targets=t, cost_bps=100)
        # Gross 1.4, cost_R ~0.20 -> net 1.20
        self.assertAlmostEqual(rr2.net_rr_t1, rr2.rr_t1 - rr2.cost_r, places=4)
        self.assertGreater(rr2.cost_r, 0)

    def test_zero_cost_net_equals_gross(self):
        t = calculate_targets(direction="long", entry=100, levels=[107])
        rr = calculate_risk_reward(direction="long", entry=100, stop=95, targets=t, cost_bps=0)
        self.assertEqual(rr.net_rr_t1, rr.rr_t1)

    def test_missing_entry_returns_none(self):
        t = calculate_targets(direction="long", entry=None, levels=[107])
        rr = calculate_risk_reward(direction="long", entry=None, stop=95, targets=t)
        self.assertIsNone(rr.rr_t1)
        msg = rr.display()
        self.assertIn("NOT AVAILABLE", msg)

    def test_display_format(self):
        t = calculate_targets(direction="long", entry=100, levels=[107, 112, 120])
        rr = calculate_risk_reward(direction="long", entry=100, stop=95, targets=t)
        d = rr.display()
        self.assertIn("T1", d)
        self.assertIn("1.40", d)

    def test_break_even_math_matches_risk_module(self):
        rr = 2.0
        be = risk_mod.break_even_win_rate(rr)
        self.assertAlmostEqual(be, 1.0 / (1 + rr), places=4)
        be_cost = risk_mod.break_even_win_rate(rr, cost_r=0.1)
        self.assertGreater(be_cost, be)

    def test_quick_signal_rr_gates(self):
        # Poor R:R should make verdict NO TRADE, not READY
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="long", entry_price=100, structural_stop=95,
            levels_for_targets=[101], atr=5,
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=8,
        )
        self.assertEqual(out.verdict, "NO TRADE")
        self.assertLess(out.risk_reward.rr_t1, 1.5)


if __name__ == "__main__":
    unittest.main()
