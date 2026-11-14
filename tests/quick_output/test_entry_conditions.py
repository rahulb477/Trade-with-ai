"""ENTRY engine tests: pending / conditionally valid / invalidated, no fabrication."""
import unittest
from trading_intel.quick_signal import (
    build_quick_signal,
    evaluate_entry,
    ENTRY_PENDING,
    ENTRY_CONDITIONALLY_VALID,
    ENTRY_INVALIDATED,
    VERDICT_WAIT,
    VERDICT_NO_TRADE,
)


class TestEntryPending(unittest.TestCase):
    """Prompt §16.4 missing entry data -> NOT AVAILABLE / PENDING, never invented."""

    def test_missing_entry_price_produces_pending(self):
        res = evaluate_entry(direction="long", entry_price=None, entry_low=None, entry_high=None)
        self.assertEqual(res.status, ENTRY_PENDING)
        self.assertFalse(res.is_available())
        self.assertEqual(res.display(), "NOT AVAILABLE — INSUFFICIENT DATA")

    def test_pattern_alone_is_insufficient(self):
        # Hammer printed but no close -> pending, pattern alone not enough
        res = evaluate_entry(direction="long", entry_price=100, has_close_confirmation=False)
        self.assertEqual(res.status, ENTRY_PENDING)
        self.assertIn("pattern alone", res.confirmation.lower() + res.confirmation.lower())

    def test_candle_alone_insufficient(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="long", entry_price=67300, structural_stop=67000, atr=100,
            levels_for_targets=[67600, 67800, 68000],
            candle_state="unknown", has_close_confirmation=False, quality_score=8,
        )
        self.assertEqual(out.verdict, VERDICT_WAIT)
        self.assertEqual(out.entry.status, ENTRY_PENDING)

    def test_pending_never_described_as_active(self):
        res = evaluate_entry(direction="short", entry_price=67000, has_close_confirmation=False, has_volume=True)
        self.assertEqual(res.status, ENTRY_PENDING)
        self.assertNotIn("active", res.confirmation.lower())
        self.assertNotIn("buy now", res.confirmation.lower())


class TestEntryConditionallyValid(unittest.TestCase):
    def test_cond_valid_needs_close_plus_three(self):
        res = evaluate_entry(
            direction="long", entry_price=100, has_close_confirmation=True,
            has_volume=True, has_retest=True, htf_aligned=True,
        )
        self.assertEqual(res.status, ENTRY_CONDITIONALLY_VALID)

    def test_close_plus_one_still_pending(self):
        res = evaluate_entry(
            direction="long", entry_price=100, has_close_confirmation=True,
            has_volume=True, has_retest=False, htf_aligned=False,
        )
        self.assertEqual(res.status, ENTRY_PENDING)


class TestEntryInvalidated(unittest.TestCase):
    def test_failed_breakout_invalidates(self):
        res = evaluate_entry(direction="long", entry_price=100, candle_state="failed_breakout", has_close_confirmation=True)
        self.assertEqual(res.status, ENTRY_INVALIDATED)

    def test_build_invalidated_maps_to_no_trade(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="long", entry_price=67300, structural_stop=67000, atr=100,
            levels_for_targets=[67600], candle_state="failed_breakout", quality_score=8,
        )
        self.assertEqual(out.verdict, VERDICT_NO_TRADE)
        self.assertEqual(out.entry.status, ENTRY_INVALIDATED)


class TestEntryZoneFormatting(unittest.TestCase):
    def test_zone_vs_single_price(self):
        out_zone = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=80,
            levels_for_targets=[66900], candle_state="closed",
            has_close_confirmation=True, volume_confirmed=True, htf_aligned=True,
            retest_status="confirmed", quality_score=8,
        )
        self.assertIn("–", out_zone.entry.display())  # en-dash range

    def test_entry_has_timeframe(self):
        res = evaluate_entry(direction="long", entry_price=100, timeframe="5m", has_close_confirmation=True, has_volume=True, has_retest=True, htf_aligned=True)
        self.assertEqual(res.timeframe, "5m")


if __name__ == "__main__":
    unittest.main()
