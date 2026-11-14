"""STOP LOSS engine tests: invalidation logic, ATR buffer, sentinel when unjustified."""
import unittest
from trading_intel.quick_signal import calculate_stop_loss, build_quick_signal


class TestStopLossCalculation(unittest.TestCase):
    """Prompt §16.5 missing stop-loss data -> sentinel."""

    def test_structural_plus_atr(self):
        res = calculate_stop_loss(direction="long", structural_price=100, atr=10, atr_multiplier=0.3)
        self.assertAlmostEqual(res.price, 97.0, places=2)
        self.assertIn("ATR", res.basis)

    def test_short_structural_plus_atr(self):
        res = calculate_stop_loss(direction="short", structural_price=100, atr=10, atr_multiplier=0.3)
        self.assertAlmostEqual(res.price, 103.0, places=2)

    def test_swing_plus_atr(self):
        res = calculate_stop_loss(direction="long", swing_level=95, atr=10)
        self.assertAlmostEqual(res.price, 92.0, places=2)

    def test_structural_only(self):
        res = calculate_stop_loss(direction="long", structural_price=100, atr=None)
        self.assertEqual(res.price, 100)
        self.assertIn("structural", res.basis.lower())

    def test_missing_inputs_returns_sentinel(self):
        res = calculate_stop_loss(direction="long", swing_level=None, atr=None, structural_price=None)
        self.assertIsNone(res.price)
        self.assertEqual(res.display(), "NOT AVAILABLE — INSUFFICIENT DATA")

    def test_atr_alone_without_structure_is_insufficient(self):
        res = calculate_stop_loss(direction="long", swing_level=None, atr=10, structural_price=None)
        self.assertIsNone(res.price)
        self.assertIn("insufficient", res.basis.lower())

    def test_invalid_direction(self):
        res = calculate_stop_loss(direction="sideways", swing_level=100, atr=5)
        self.assertIsNone(res.price)

    def test_quick_signal_propagates_stop_sentinel(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="long", entry_price=67300,
            # No swing_level, no structural_stop, no atr -> no justified stop
            swing_level=None, structural_stop=None, atr=None,
            levels_for_targets=[67600, 67800, 68000],
            candle_state="closed", has_close_confirmation=True, volume_confirmed=True,
            htf_aligned=True, retest_status="confirmed", quality_score=8,
        )
        self.assertIsNone(out.stop_loss.price)
        self.assertEqual(out.stop_loss.display(), "NOT AVAILABLE — INSUFFICIENT DATA")
        # Without a justified stop, verdict must be WAIT not READY
        self.assertNotEqual(out.verdict, "PAPER-TRADING SETUP READY")


if __name__ == "__main__":
    unittest.main()
