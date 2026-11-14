"""WAIT engine tests: unconfirmed breakout/breakdown, failed retest, HTF conflict."""
import unittest
from trading_intel.quick_signal import (
    build_quick_signal,
    evaluate_wait,
    VERDICT_WAIT,
    CANDLE_FORMING,
    UNCONFIRMED_BREAKOUT,
    UNCONFIRMED_BREAKDOWN,
    FAILED_BREAKOUT,
    FAILED_BREAKDOWN,
)


class TestUnconfirmedBreakout(unittest.TestCase):
    """Prompt §16.8 unconfirmed breakout -> WAIT."""

    def test_unconfirmed_breakout_waits(self):
        w = evaluate_wait(timeframe="5m", candle_state=UNCONFIRMED_BREAKOUT, level=1000, volume_confirmed=False)
        self.assertIn("confirmed breakout", w.condition.lower())
        self.assertNotIn("will", w.condition.lower())  # never promise

    def test_build_wait_on_unconfirmed_breakout(self):
        out = build_quick_signal(
            instrument="NIFTY", exchange="NSE", timeframe="15m",
            direction="long", entry_price=1005, structural_stop=990, atr=8,
            levels_for_targets=[1020, 1035, 1050],
            candle_state=UNCONFIRMED_BREAKOUT, resistance_level=1000,
            volume_confirmed=False, has_close_confirmation=False, quality_score=8,
        )
        self.assertEqual(out.verdict, VERDICT_WAIT)
        self.assertIn("breakout", out.wait.condition.lower())

    def test_no_countdown_invented(self):
        w = evaluate_wait(timeframe="5m", candle_state=UNCONFIRMED_BREAKOUT, level=500)
        self.assertNotIn("3 candles", w.condition)
        self.assertNotIn("10 minutes", w.condition)
        # Must not contain a future time promise
        self.assertNotRegex(w.condition.lower(), r"in \d+ (minutes|candles|bars)")


class TestUnconfirmedBreakdown(unittest.TestCase):
    """Prompt §16.9 unconfirmed breakdown -> WAIT."""

    def test_unconfirmed_breakdown_waits(self):
        w = evaluate_wait(timeframe="5m", candle_state=UNCONFIRMED_BREAKDOWN, level=67300)
        self.assertIn("support", w.condition.lower())
        self.assertIn("confirmed", w.condition.lower())

    def test_build_wait_on_breakdown(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=80,
            levels_for_targets=[66900, 66500, 66200],
            candle_state=UNCONFIRMED_BREAKDOWN, support_level=67300,
            has_close_confirmation=False, quality_score=8,
        )
        self.assertEqual(out.verdict, VERDICT_WAIT)

    def test_candle_forming_vs_closed_distinction(self):
        forming = evaluate_wait(timeframe="5m", candle_state=CANDLE_FORMING, level=1000)
        closed = evaluate_wait(timeframe="5m", candle_state="closed", level=1000, volume_confirmed=True)
        # forming mentions "close" action still needed
        self.assertIn("close", forming.condition.lower())
        # They must be different strings — distinction is normative
        self.assertNotEqual(forming.condition, closed.condition)


class TestFailedRetest(unittest.TestCase):
    """Prompt §16.10 failed retest -> WAIT/NO TRADE, never an active signal."""

    def test_failed_breakout_invalidates_entry(self):
        out = build_quick_signal(
            instrument="NIFTY", exchange="NSE", timeframe="15m",
            direction="long", entry_price=1005, structural_stop=990,
            levels_for_targets=[1020], atr=10,
            candle_state=FAILED_BREAKOUT, quality_score=8,
        )
        self.assertIn(out.verdict, (VERDICT_WAIT, "NO TRADE"))
        self.assertIn("INVALIDATED", out.entry.status)

    def test_wait_for_successful_retest_string(self):
        w = evaluate_wait(timeframe="15m", candle_state="closed", retest_status="pending", level=1000)
        self.assertIn("retest", w.condition.lower())

    def test_failed_retest_template(self):
        w = evaluate_wait(timeframe="15m", retest_status="failed")
        self.assertIn("failed", w.condition.lower())


class TestConflictingTimeframes(unittest.TestCase):
    """Prompt §16.11 conflicting timeframes -> WAIT."""

    def test_htf_conflict_waits(self):
        out = build_quick_signal(
            instrument="BANKNIFTY", exchange="NSE", timeframe="5m",
            direction="long", entry_price=51500, structural_stop=51400,
            levels_for_targets=[51700, 51800, 51900],
            atr=None, candle_state="closed",
            has_close_confirmation=True, volume_confirmed=True,
            htf_aligned=False, htf_conflict=True, htf="1D", ltf="5m",
            retest_status="confirmed", quality_score=8,
        )
        self.assertEqual(out.verdict, VERDICT_WAIT)
        self.assertIn("alignment", out.wait.condition.lower())

    def test_evaluate_wait_htf(self):
        w = evaluate_wait(htf_conflict=True, htf="1D", ltf="15m")
        self.assertIn("higher-timeframe", w.condition.lower())

    def test_no_conflict_can_be_ready(self):
        out = build_quick_signal(
            instrument="BANKNIFTY", exchange="NSE", timeframe="5m",
            direction="long", entry_price=51500, structural_stop=51400,
            levels_for_targets=[51700, 51800, 51900],
            atr=None, candle_state="closed",
            has_close_confirmation=True, volume_confirmed=True,
            htf_aligned=True, htf_conflict=False,
            retest_status="confirmed", quality_score=8,
        )
        self.assertEqual(out.verdict, "PAPER-TRADING SETUP READY")


if __name__ == "__main__":
    unittest.main()
