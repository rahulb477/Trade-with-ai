"""WAIT / NO TRADE / PAPER-TRADING SETUP READY verdict tests."""
import unittest
from trading_intel.quick_signal import (
    build_quick_signal,
    VERDICT_WAIT,
    VERDICT_NO_TRADE,
    VERDICT_READY,
    render_quick_text,
    render_compact_text_minimal,
    format_price,
)


class TestWaitOutput(unittest.TestCase):
    """Prompt §16.1 WAIT output: breakout confirmation pending -> WAIT."""

    def test_wait_on_unconfirmed_breakdown(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short",
            last_price=67350, entry_price=67300, entry_low=67300, entry_high=67400,
            swing_level=67800, atr=150,
            levels_for_targets=[66900, 66500, 66200],
            candle_state="unconfirmed_breakdown",
            support_level=67300,
            has_close_confirmation=False,
            quality_score=8,
        )
        self.assertEqual(out.verdict, VERDICT_WAIT)
        self.assertIn("WAIT", out.verdict)
        text = render_quick_text(out)
        self.assertIn("VERDICT: WAIT", text)
        self.assertIn("WAIT UNTIL:", text)
        # WAIT must name a condition, not be bare
        self.assertGreater(len(out.wait.condition), 10)

    def test_wait_example_matches_spec_structure(self):
        """Spec §2 example structure must be reproducible."""
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short",
            entry_low=67300, entry_high=67400,
            structural_stop=67800,
            last_price=67350, atr=120,
            levels_for_targets=[66950, 66500, 66200],
            candle_state="unconfirmed_breakdown",
            support_level=67300,
            has_close_confirmation=False,
            quality_score=8,
        )
        text = render_quick_text(out)
        self.assertIn("BTCUSD | Bitstamp | 5m", text)
        self.assertIn("ENTRY:", text)
        self.assertIn("STOP LOSS:", text)
        self.assertIn("TAKE PROFIT 1:", text)
        self.assertIn("TAKE PROFIT 2:", text)
        self.assertIn("TAKE PROFIT 3:", text)
        self.assertIn("RISK / REWARD:", text)
        self.assertIn("REASON:", text)


class TestNoTradeOutput(unittest.TestCase):
    """Prompt §16.2 NO TRADE: invalidated / poor R:R / hostile conditions."""

    def test_no_trade_on_poor_rr(self):
        # Entry very close to T1 -> R:R < 1.5
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="long",
            entry_price=100, swing_level=95, structural_stop=95,
            levels_for_targets=[101],  # only 1R away -> R:R 1.0
            atr=5, has_close_confirmation=True, volume_confirmed=True,
            htf_aligned=True, quality_score=8,
            candle_state="closed",
            retest_status="confirmed",
        )
        # With R:R < 1.5 should be NO TRADE
        self.assertEqual(out.verdict, VERDICT_NO_TRADE)
        text = render_quick_text(out)
        self.assertIn("VERDICT: NO TRADE", text)

    def test_no_trade_on_invalidation(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short",
            entry_price=67300, swing_level=67800, structural_stop=67800,
            levels_for_targets=[66900], atr=100,
            candle_state="failed_breakout",
            quality_score=8,
        )
        self.assertEqual(out.verdict, VERDICT_NO_TRADE)

    def test_no_trade_on_event_risk(self):
        out = build_quick_signal(
            instrument="RELIANCE", exchange="NSE", timeframe="1D",
            direction="long",
            entry_price=1204, structural_stop=1186, levels_for_targets=[1240, 1275, 1310],
            atr=12, has_close_confirmation=True, volume_confirmed=True,
            htf_aligned=True, quality_score=8,
            event_risk="Q2 results 2026-11-18",
            candle_state="closed",
            retest_status="confirmed",
        )
        self.assertEqual(out.verdict, VERDICT_NO_TRADE)
        self.assertIn("2026-11-18", out.wait.condition)


class TestValidSetupOutput(unittest.TestCase):
    """Prompt §16.3 valid hypothetical setup -> PAPER-TRADING SETUP READY."""

    def test_ready_when_all_gates_pass(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short",
            entry_low=67300, entry_high=67400,  # zone mid 67350
            structural_stop=67800,
            levels_for_targets=[66600, 66200, 65800],
            atr=None,
            candle_state="closed",
            has_close_confirmation=True,
            volume_confirmed=True,
            htf_aligned=True,
            retest_status="confirmed",
            quality_score=9,
            data_fresh=True,
        )
        self.assertEqual(out.verdict, VERDICT_READY)
        text = render_quick_text(out)
        self.assertIn("VERDICT: PAPER-TRADING SETUP READY", text)
        # Stop must be justified, not sentinel
        self.assertNotIn("NOT AVAILABLE", out.stop_loss.display())
        # TPs must be directionally consistent (short: targets < entry)
        entry_mid = 67350
        self.assertLess(out.targets.tp1, entry_mid)
        self.assertLess(out.targets.tp2, entry_mid)

    def test_ready_requires_min_rr(self):
        """READY only if R:R to T1 >= 1.5."""
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="long",
            entry_price=100, structural_stop=95,
            levels_for_targets=[107, 112, 120],  # T1 1.4 -> below 1.5 would be NO TRADE
            # but use better levels
            atr=None, has_close_confirmation=True, volume_confirmed=True,
            htf_aligned=True, retest_status="confirmed",
            quality_score=8, candle_state="closed",
        )
        # T1 R = (107-100)/5=1.4 <1.5 -> NO TRADE
        self.assertEqual(out.verdict, VERDICT_NO_TRADE)

        out2 = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="long",
            entry_price=100, structural_stop=95,
            levels_for_targets=[108, 112, 120],  # T1 R=1.6
            atr=None, has_close_confirmation=True, volume_confirmed=True,
            htf_aligned=True, retest_status="confirmed",
            quality_score=8, candle_state="closed",
        )
        self.assertEqual(out2.verdict, VERDICT_READY)


if __name__ == "__main__":
    unittest.main()
