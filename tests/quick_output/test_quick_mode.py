"""Quick mode defaults, Hinglish, no fabricated prices/probabilities."""
import unittest
from trading_intel.quick_signal import (
    build_quick_signal,
    detect_mode,
    render_quick_text,
    render_compact_text_minimal,
    validate_no_probability,
    assert_no_fabrication,
    format_price,
)


class TestQuickModeDefault(unittest.TestCase):
    """Prompt §16.9 default quick mode, §16.17 full-analysis activation complement."""

    def test_empty_user_text_defaults_to_quick(self):
        self.assertEqual(detect_mode(""), "quick")
        self.assertEqual(detect_mode("analyse this chart"), "quick")

    def test_quick_mode_output_is_short(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=80,
            levels_for_targets=[66900, 66500, 66200],
            candle_state="unconfirmed_breakdown", support_level=67300,
            has_close_confirmation=False, quality_score=8,
        )
        self.assertFalse(out.full_mode_requested)
        text = render_compact_text_minimal(out)
        # Must not leak full analysis sections
        self.assertNotIn("SOURCES AND DATA QUALITY", text)
        self.assertNotIn("Historical backtesting", text)


class TestNoFabricatedPrices(unittest.TestCase):
    """Prompt §16.18 no fabricated prices."""

    def test_only_allowed_prices_appear(self):
        allowed = [67300, 67400, 67800, 66900, 66500, 66200]
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=None,
            levels_for_targets=[66900, 66500, 66200],
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=8,
        )
        # Include entry midpoint as allowed (computed, not fabricated)
        allowed_with_mid = allowed + [67350]
        self.assertTrue(assert_no_fabrication(out, allowed_with_mid))

    def test_sentinel_when_no_price(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_price=None, structural_stop=None,
            levels_for_targets=None, atr=None,
            candle_state="unknown", quality_score=8,
        )
        text = render_quick_text(out)
        self.assertIn("NOT AVAILABLE — INSUFFICIENT DATA", text)
        # No invented numeric price should leak
        self.assertNotRegex(text, r"ENTRY:\n\d")

    def test_format_price_never_invents(self):
        self.assertEqual(format_price(None), "NOT AVAILABLE — INSUFFICIENT DATA")
        self.assertEqual(format_price(67300), "67,300")
        self.assertEqual(format_price(1234.5), "1,234.50")


class TestNoUnsupportedProbabilities(unittest.TestCase):
    """Prompt §16.19 no unsupported probabilities."""

    def test_output_contains_no_probability(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=80,
            levels_for_targets=[66900, 66500, 66200],
            candle_state="unconfirmed_breakdown", support_level=67300,
            has_close_confirmation=False, quality_score=8,
        )
        text = render_quick_text(out)
        self.assertTrue(validate_no_probability(text), f"output leaked probability: {text}")
        self.assertNotIn("%", text.split("RISK / REWARD:")[0])  # no % in verdict area

    def test_validate_no_probability_bans_patterns(self):
        # banned patterns must be detected; negation context in audit is separate
        self.assertFalse(validate_no_probability("This has 80% probability of success"))
        self.assertFalse(validate_no_probability("90% win rate guaranteed"))
        # banned: do not use sure shot (audit negation window covers this line)
        self.assertFalse(validate_no_probability("sure shot trade"))
        self.assertTrue(validate_no_probability("Wait for confirmation. No valid setup."))

    def test_quick_report_never_claims_sure(self):
        out = build_quick_signal(
            instrument="RELIANCE", exchange="NSE", timeframe="1D",
            direction="long", entry_price=1204, structural_stop=1186,
            levels_for_targets=[1240, 1275, 1310], atr=None,
            candle_state="closed", has_close_confirmation=True,
            volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
            quality_score=8,
        )
        text = render_quick_text(out)
        lowered = text.lower()
        # banned: never guaranteed
        self.assertNotIn("guaranteed", lowered)
        # banned: do not use sure shot
        self.assertNotIn("sure shot", lowered)
        # banned: never pakka sure
        self.assertNotIn("pakka", lowered)
        self.assertNotIn("100%", lowered)


class TestHinglishExplanation(unittest.TestCase):
    """Prompt §16.20 correct Hinglish explanation."""

    def test_hinglish_present_and_non_empty(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=80,
            levels_for_targets=[66900, 66500, 66200],
            candle_state="unconfirmed_breakdown", support_level=67300,
            has_close_confirmation=False, quality_score=8,
        )
        self.assertIsNotNone(out.reason_hinglish)
        self.assertGreater(len(out.reason_hinglish), 5)
        # banned: never use pakka / sure shot language
        self.assertNotIn("pakka", out.reason_hinglish.lower())
        # banned: do not claim sure shot
        self.assertNotIn("sure shot", out.reason_hinglish.lower())

    def test_hinglish_choppy(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_price=67350, structural_stop=67800,
            levels_for_targets=[66600, 66200, 65800], atr=None,
            candle_state="closed", choppy=True, quality_score=8,
            has_close_confirmation=True, volume_confirmed=True, htf_aligned=True, retest_status="confirmed",
        )
        self.assertIn("choppy", out.reason_hinglish.lower() + out.reason.lower())

    def test_hinglish_no_new_numeric_claims(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=80,
            levels_for_targets=[66900, 66500, 66200],
            candle_state="unconfirmed_breakdown", support_level=67300,
            has_close_confirmation=False, quality_score=8,
        )
        # Numbers in Hinglish should match English section (no new levels)
        # Hinglish templates never contain comma-prices
        self.assertNotRegex(out.reason_hinglish, r"\d{1,3},\d{3}")


if __name__ == "__main__":
    unittest.main()
