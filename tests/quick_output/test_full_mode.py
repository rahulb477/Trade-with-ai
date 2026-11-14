"""Full-analysis activation: quick mode suppressed only on explicit request."""
import unittest
from trading_intel.quick_signal import build_quick_signal, detect_mode, render_quick_text


class TestFullModeTriggers(unittest.TestCase):
    """Prompt §16.17 full-analysis activation."""

    TRIGGERS = [
        "full analysis",
        "detailed analysis",
        "explain this chart",
        "why this entry?",
        "show indicators",
        "show news",
        "show complete research",
        "/full",
        "Full Analysis please",
        "Can you show indicators?",
    ]

    def test_triggers_activate_full(self):
        for trig in self.TRIGGERS:
            with self.subTest(trigger=trig):
                self.assertEqual(detect_mode(trig), "full", f"failed for: {trig}")

    def test_case_insensitive(self):
        self.assertEqual(detect_mode("FULL ANALYSIS"), "full")
        self.assertEqual(detect_mode("/FULL"), "full")

    def test_non_triggers_stay_quick(self):
        for text in ["", "analyse this chart", "what is happening?", "quick summary", "next steps?"]:
            with self.subTest(text=text):
                self.assertEqual(detect_mode(text), "quick")

    def test_build_marks_full_mode_requested(self):
        out_quick = build_quick_signal(instrument="BTCUSD", exchange="Bitstamp", timeframe="5m", user_text="quick summary")
        self.assertFalse(out_quick.full_mode_requested)

        out_full = build_quick_signal(instrument="BTCUSD", exchange="Bitstamp", timeframe="5m", user_text="please do full analysis")
        self.assertTrue(out_full.full_mode_requested)

    def test_quick_output_still_renderable_in_full_mode(self):
        """Full mode flag does not break the quick renderer — the agent decides which template to emit."""
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=80,
            levels_for_targets=[66900, 66500, 66200],
            candle_state="unconfirmed_breakdown", support_level=67300,
            has_close_confirmation=False, quality_score=8,
            user_text="/full",
        )
        self.assertTrue(out.full_mode_requested)
        text = render_quick_text(out)
        self.assertIn("VERDICT:", text)  # still structurally sound

    def test_quick_suppresses_full_sections(self):
        out = build_quick_signal(
            instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
            direction="short", entry_low=67300, entry_high=67400,
            structural_stop=67800, atr=80,
            levels_for_targets=[66900, 66500, 66200],
            candle_state="unconfirmed_breakdown", support_level=67300,
            has_close_confirmation=False, quality_score=8,
            user_text="analyse this chart",  # quick
        )
        text = render_quick_text(out)
        # Quick mode must NOT include full-mode-only sections
        for banned in ["Full indicator tables", "Complete candlestick encyclopedia", "Long news summaries", "Detailed market structure"]:
            self.assertNotIn(banned, text)


if __name__ == "__main__":
    unittest.main()
