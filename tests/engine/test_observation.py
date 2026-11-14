import unittest

from trading_intel import observation as obs


class TestChartObservation(unittest.TestCase):
    def base(self, **kwargs):
        defaults = dict(instrument="RELIANCE", exchange="NSE", timeframe="1D",
                        last_price=2900.0, quality_score=9, volume_present=True,
                        indicators_visible=["RSI(14)"])
        defaults.update(kwargs)
        return obs.ChartObservation(**defaults)

    def test_permits_verdict_when_data_present(self):
        self.assertTrue(self.base().permits_verdict())

    def test_low_quality_blocks_verdict(self):
        self.assertFalse(self.base(quality_score=4).permits_verdict())

    def test_unknown_instrument_blocks_verdict(self):
        self.assertFalse(self.base(instrument=None).permits_verdict())

    def test_precise_levels_need_price(self):
        self.assertFalse(self.base(last_price=None).permits_precise_levels())

    def test_missing_lists_gaps(self):
        missing = self.base(volume_present=False).missing()
        self.assertIn("volume", missing)

    def test_gate_report_caps_at_insufficient_without_instrument(self):
        gate = self.base(instrument=None).gate_report()
        self.assertFalse(gate["passed"])
        self.assertEqual(gate["permitted_verdict_cap"], "INSUFFICIENT DATA — NO VALID SETUP")

    def test_gate_report_caps_at_wait_with_low_quality(self):
        gate = self.base(quality_score=3).gate_report()
        self.assertEqual(gate["permitted_verdict_cap"], "WAIT — NO CONFIRMED SETUP")

    def test_non_candlestick_chart_fails_gate(self):
        gate = self.base(chart_type="heikin-ashi").gate_report()
        self.assertFalse(gate["passed"])
        self.assertTrue(any("chart type" in f for f in gate["failures"]))

    def test_to_dict_round_trip(self):
        payload = self.base().to_dict()
        self.assertEqual(payload["instrument"], "RELIANCE")
        self.assertIn("missing", payload)


class TestTranscription(unittest.TestCase):
    def test_build_from_dict(self):
        data = {
            "instrument": "TCS", "exchange": "NSE", "timeframe": "15m",
            "last_price": "3900.5", "volume_present": True,
            "trend": "up", "quality_observed": {"instrument_identifiable": True,
                                                "timeframe_visible": True,
                                                "price_axis_readable": True},
        }
        parsed = obs.from_transcription(data)
        self.assertEqual(parsed.instrument, "TCS")
        self.assertEqual(parsed.last_price, 3900.5)
        self.assertEqual(parsed.quality_score, 5)
        self.assertEqual(parsed.source, "user-transcription")

    def test_unmapped_fields_are_kept(self):
        parsed = obs.from_transcription({"instrument": "X", "custom_note": "hello"})
        self.assertTrue(any("custom_note" in n for n in parsed.notes))

    def test_bad_price_becomes_none(self):
        parsed = obs.from_transcription({"instrument": "X", "last_price": "n/a"})
        self.assertIsNone(parsed.last_price)


class TestLevels(unittest.TestCase):
    def test_tradable_needs_two_touches(self):
        self.assertFalse(obs.Level(100, "support", 1).tradable)
        self.assertTrue(obs.Level(100, "support", 2).tradable)

    def test_sort_resistance_first(self):
        levels = [obs.Level(95, "support", 2), obs.Level(110, "resistance", 3)]
        self.assertEqual(obs.sort_levels(levels)[0].price, 110)

    def test_distance_to_next_resistance(self):
        levels = [obs.Level(110, "resistance", 2), obs.Level(95, "support", 2)]
        self.assertAlmostEqual(obs.distance_to_next_resistance(100, levels), 10)

    def test_distance_in_atr_and_room_class(self):
        levels = [obs.Level(110, "resistance", 2)]
        self.assertAlmostEqual(obs.distance_in_atr(100, levels, 4.0), 2.5)
        self.assertEqual(obs.room_class(2.5), "workable")
        self.assertEqual(obs.room_class(1.5), "marginal")
        self.assertEqual(obs.room_class(0.5), "untradeable")
        self.assertEqual(obs.room_class(None), "unknown")

    def test_no_resistance_above(self):
        self.assertIsNone(obs.distance_to_next_resistance(200, [obs.Level(110, "resistance", 2)]))

    def test_nearest_level(self):
        levels = [obs.Level(90, "support", 2), obs.Level(120, "resistance", 2)]
        self.assertEqual(obs.nearest_level(115, levels).price, 120)


if __name__ == "__main__":
    unittest.main()
