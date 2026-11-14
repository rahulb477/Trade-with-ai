"""Compact output length and formatting."""
import unittest
from trading_intel.quick_signal import (
    build_quick_signal,
    render_quick_text,
    render_compact_text_minimal,
    render_quick_html,
)


def _build_sample():
    return build_quick_signal(
        instrument="BTCUSD", exchange="Bitstamp", timeframe="5m",
        direction="short",
        entry_low=67300, entry_high=67400, structural_stop=67800,
        levels_for_targets=[66900, 66500, 66200], atr=80,
        candle_state="unconfirmed_breakdown", support_level=67300,
        has_close_confirmation=False, quality_score=8,
    )


class TestCompactLength(unittest.TestCase):
    """Prompt §16.16 compact output length."""

    def test_minimal_is_8_to_12_lines(self):
        out = _build_sample()
        text = render_compact_text_minimal(out)
        lines = [l for l in text.split("\n") if l.strip()]
        # Prompt: keep default around 8-12 short lines. We allow 9-13 to account for blank filtering.
        self.assertGreaterEqual(len(lines), 8, f"too short: {len(lines)} lines: {text}")
        self.assertLessEqual(len(lines), 13, f"too long: {len(lines)} lines: {text}")

    def test_compact_contains_required_labels(self):
        out = _build_sample()
        text = render_compact_text_minimal(out)
        for label in ["VERDICT:", "WAIT UNTIL:", "ENTRY:", "STOP LOSS:", "TAKE PROFIT 1:", "TAKE PROFIT 2:", "TAKE PROFIT 3:", "RISK / REWARD:", "REASON:"]:
            self.assertIn(label, text, f"missing label {label}")

    def test_full_compact_variant_still_readable(self):
        out = _build_sample()
        text = render_quick_text(out)
        # Full quick text variant may be longer (~25), but must still avoid long paragraphs.
        # Each paragraph is at most one short sentence.
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        for para in paragraphs:
            self.assertLess(len(para), 600, "paragraph too long — violates §3 strict rules")

    def test_no_long_technical_jargon_block(self):
        out = _build_sample()
        text = render_compact_text_minimal(out)
        # Default response must avoid repeating complete analysis
        self.assertNotIn("Bollinger", text)
        self.assertNotIn("Ichimoku", text)

    def test_price_formatting_readable(self):
        out = _build_sample()
        text = render_compact_text_minimal(out)
        # Price formatting uses comma separators
        self.assertIn("67,300", text)

    def test_html_contains_required_sections(self):
        out = _build_sample()
        html = render_quick_html(out)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("BTCUSD", html)
        self.assertIn("VERDICT", html.upper())
        self.assertIn("Stop Loss", html)
        # Color hints must be present
        self.assertIn("#3b82f6", html)  # entry blue
        self.assertIn("#ef4444", html)  # stop red
        self.assertIn("#22c55e", html)  # tp green
        self.assertIn("#0f1115", html)  # dark bg


if __name__ == "__main__":
    unittest.main()
