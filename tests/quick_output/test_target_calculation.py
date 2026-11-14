"""TAKE PROFIT engine tests: TP1/2/3, directional consistency, cost awareness."""
import unittest
from trading_intel.quick_signal import calculate_targets, build_quick_signal, format_price


class TestTargetBasics(unittest.TestCase):
    """Prompt §16.15 TP calculations."""

    def test_three_structural_levels_map_to_three_targets(self):
        res = calculate_targets(direction="long", entry=100, levels=[107, 112, 120], atr=5)
        self.assertEqual(res.tp1, 107)
        self.assertEqual(res.tp2, 112)
        self.assertEqual(res.tp3, 120)

    def test_short_directional_consistency(self):
        res = calculate_targets(direction="short", entry=67350, levels=[66900, 66500, 66200])
        self.assertLess(res.tp1, 67350)
        self.assertLess(res.tp2, 67350)
        self.assertLess(res.tp3, 67350)

    def test_long_targets_above_entry(self):
        res = calculate_targets(direction="long", entry=100, levels=[105, 110, 115])
        self.assertGreater(res.tp1, 100)
        self.assertGreater(res.tp2, 100)

    def test_wrong_side_levels_filtered(self):
        # For a long, levels below entry must be ignored
        res = calculate_targets(direction="long", entry=100, levels=[90, 95, 107, 112], atr=5)
        self.assertEqual(res.tp1, 107)  # first valid above entry
        self.assertEqual(res.tp2, 112)

    def test_atr_targets_when_no_structure(self):
        res = calculate_targets(direction="long", entry=100, levels=None, atr=10)
        self.assertIsNotNone(res.tp1)
        self.assertIsNotNone(res.tp2)
        # TP1 via 1.5 ATR
        self.assertAlmostEqual(res.tp1, 115.0, places=1)

    def test_no_entry_returns_no_targets(self):
        res = calculate_targets(direction="long", entry=None, levels=[107, 112], atr=5)
        self.assertIsNone(res.tp1)
        self.assertEqual(res.tp_display(1), "NOT AVAILABLE")

    def test_missing_targets_marked_not_available(self):
        """Prompt §16.6 missing target data -> NOT AVAILABLE sentinel, not fabricated."""
        res = calculate_targets(direction="long", entry=100, levels=None, atr=None)
        self.assertIsNone(res.tp1)
        self.assertIsNone(res.tp2)
        self.assertIsNone(res.tp3)
        self.assertEqual(res.tp_display(1), "NOT AVAILABLE")
        self.assertEqual(res.tp_display(2), "NOT AVAILABLE")
        self.assertEqual(res.tp_display(3), "NOT AVAILABLE")

    def test_tp3_not_manufactured(self):
        """TP3 should stay None when insufficient structure, not forced to a round number."""
        res = calculate_targets(direction="long", entry=100, levels=[105], atr=None)
        # Only one structural level, no ATR -> no TP3
        self.assertIsNone(res.tp3)
        self.assertEqual(res.tp_display(3), "NOT AVAILABLE")

    def test_quick_signal_tp_sentinels(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short",
            entry_price=67350, structural_stop=67800,
            levels_for_targets=None, atr=None,  # no structure, no ATR
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=8,
        )
        # No ATR no structure -> no targets -> verdict WAIT (not READY)
        self.assertEqual(out.targets.tp_display(1), "NOT AVAILABLE")
        self.assertEqual(out.verdict, "WAIT")

    def test_avoid_arbitrary_round_numbers(self):
        """A target that is exactly 70000 with no structural basis should not be the default.
        The engine uses structure/ATR, not round-number snapping."""
        res = calculate_targets(direction="long", entry=67300, levels=[67400, 67600, 67800], atr=80)
        self.assertNotEqual(res.tp1, 70000)
        self.assertEqual(res.tp1, 67400)


class TestCostAwareTargets(unittest.TestCase):
    def test_build_targets_with_cost_does_not_change_targets(self):
        # Costs affect R:R, not target placement
        res_no_cost = calculate_targets(direction="long", entry=100, levels=[107, 112, 120], atr=5)
        res_cost = calculate_targets(direction="long", entry=100, levels=[107, 112, 120], atr=5, cost_bps=20)
        self.assertEqual(res_no_cost.tp1, res_cost.tp1)


if __name__ == "__main__":
    unittest.main()
