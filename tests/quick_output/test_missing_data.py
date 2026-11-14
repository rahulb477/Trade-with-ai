"""Missing-data guards: unavailable live data, stale news, blurry screenshot."""
import unittest
from trading_intel.quick_signal import build_quick_signal, render_quick_text


class TestUnavailableLiveData(unittest.TestCase):
    """Prompt §16.7 unavailable live market data -> no fabricated prices."""

    def test_no_price_data_yields_sentinel(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short",
            last_price=None, entry_price=None, entry_low=None, entry_high=None,
            swing_level=None, structural_stop=None, levels_for_targets=None,
            atr=None, candle_state="unknown", quality_score=8,
        )
        self.assertIsNone(out.stop_loss.price)
        self.assertIsNone(out.targets.tp1)
        text = render_quick_text(out)
        self.assertIn("NOT AVAILABLE", text)
        # Must not invent a price like 67,300 when none was supplied
        self.assertNotIn("67,300", text)
        self.assertEqual(out.verdict, "WAIT")

    def test_no_levels_no_targets(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_price=67350, structural_stop=67800,
            levels_for_targets=None, atr=None,
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=8,
        )
        self.assertEqual(out.targets.tp_display(1), "NOT AVAILABLE")
        self.assertEqual(out.verdict, "WAIT")  # not READY without targets


class TestStaleNews(unittest.TestCase):
    """Prompt §16.12 stale news / event risk -> NO TRADE or WAIT."""

    def test_stale_data_downgrades_ready(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short",
            entry_price=67350, structural_stop=67800,
            levels_for_targets=[66900, 66500, 66200], atr=60,
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=8, data_fresh=False,  # stale
        )
        self.assertEqual(out.verdict, "WAIT")
        self.assertEqual(out.data_freshness, "UNKNOWN")  # unless timestamp provided

    def test_event_risk_produces_no_trade(self):
        out = build_quick_signal(
            instrument="NIFTY", exchange="NSE", timeframe="1D",
            direction="long", entry_price=26000, structural_stop=25800,
            levels_for_targets=[26200, 26400, 26600], atr=50,
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=8, event_risk="RBI MPC 2026-11-19",
        )
        self.assertEqual(out.verdict, "NO TRADE")
        self.assertIn("2026-11-19", out.wait.condition)

    def test_stale_with_explicit_timestamp(self):
        # When data_timestamp is old, freshness classifier should reflect it
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_price=67350, structural_stop=67800,
            levels_for_targets=[66900, 66500, 66200], atr=60,
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=8, data_timestamp="2026-11-01T10:00:00+00:00",
            data_fresh=True,  # explicitly fresh despite old timestamp — tests logic decoupling
        )
        # Freshness class should be STALE/HISTORICAL because timestamp is old vs now
        self.assertIn(out.data_freshness, ("STALE", "HISTORICAL", "DELAYED", "UNKNOWN"))


class TestScreenshotQualityFailures(unittest.TestCase):
    """Prompt §16.13 screenshot quality failures -> WAIT cap."""

    def test_low_quality_caps_verdict(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_price=67350, structural_stop=67800,
            levels_for_targets=[66600, 66200, 65800], atr=None,
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=3,  # poor screenshot
        )
        self.assertEqual(out.verdict, "WAIT")
        self.assertIn("quality", out.wait.condition.lower())

    def test_blurry_chart_does_not_produce_levels(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short",
            last_price=None, entry_price=None, swing_level=None, structural_stop=None,
            levels_for_targets=None, atr=None,
            candle_state="unknown", quality_score=1,
        )
        text = render_quick_text(out)
        self.assertIn("NOT AVAILABLE — INSUFFICIENT DATA", text)
        self.assertIn("STOP LOSS:", text)


if __name__ == "__main__":
    unittest.main()
