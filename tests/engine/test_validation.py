import unittest
from datetime import datetime, timedelta, timezone

from trading_intel import validation as val
from trading_intel.providers import Bar, InMemoryProvider, NotSupported, describe_environment, validate_bars


class TestOHLCValidation(unittest.TestCase):
    def test_clean_series_passes(self):
        report = val.validate_ohlc([100, 101], [102, 103], [99, 100], [101, 102], [10, 20])
        self.assertTrue(report.ok, report.summary())

    def test_high_below_close_fails(self):
        report = val.validate_ohlc([100], [99], [98], [101])
        self.assertFalse(report.ok)
        self.assertTrue(any(r.check == "ohlc_bounds" for r in report.failures()))

    def test_length_mismatch_fails(self):
        report = val.validate_ohlc([100, 101], [102], [99, 100], [101, 102])
        self.assertFalse(report.ok)
        self.assertEqual(report.results[0].check, "series_lengths")

    def test_negative_volume_fails(self):
        report = val.validate_ohlc([100], [101], [99], [100], volume=[-5])
        self.assertFalse(report.ok)

    def test_duplicate_timestamps_fail(self):
        ts = ["2026-11-14T09:15:00+05:30", "2026-11-14T09:15:00+05:30"]
        report = val.validate_ohlc([1, 1], [2, 2], [0.5, 0.5], [1.5, 1.5], timestamps=ts)
        self.assertFalse(report.ok)

    def test_missing_timezone_fails(self):
        ts = ["2026-11-14T09:15:00", "2026-11-14T09:20:00"]
        report = val.validate_ohlc([1, 1], [2, 2], [0.5, 0.5], [1.5, 1.5], timestamps=ts)
        self.assertFalse(report.ok)


class TestJumpAndGapDetection(unittest.TestCase):
    def test_split_like_jump_flagged(self):
        flags = val.detect_jumps([100, 50])
        self.assertEqual(len(flags), 1)

    def test_normal_move_not_flagged(self):
        self.assertEqual(val.detect_jumps([100, 101, 100.5]), [])

    def test_atr_scaled_threshold(self):
        flags = val.detect_jumps([100, 103], atr_units=8.0, atr_value=1.0)
        self.assertEqual(len(flags), 0)

    def test_gap_detection(self):
        ts = ["2026-11-14T09:15:00+05:30", "2026-11-14T09:20:00+05:30",
              "2026-11-14T10:00:00+05:30"]
        gaps = val.detect_gaps(ts, 5)
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["missing_bars_estimate"], 7)

    def test_no_gaps(self):
        ts = ["2026-11-14T09:15:00+05:30", "2026-11-14T09:20:00+05:30"]
        self.assertEqual(val.detect_gaps(ts, 5), [])


class TestFreshness(unittest.TestCase):
    def now(self):
        return datetime(2026, 11, 14, 10, 0, tzinfo=timezone.utc)

    def test_live(self):
        out = val.freshness(self.now(), self.now() - timedelta(seconds=30))
        self.assertEqual(out["class"], "LIVE")

    def test_recent(self):
        out = val.freshness(self.now(), self.now() - timedelta(minutes=10))
        self.assertEqual(out["class"], "RECENT")

    def test_delayed(self):
        out = val.freshness(self.now(), self.now() - timedelta(hours=2))
        self.assertEqual(out["class"], "DELAYED")

    def test_stale(self):
        out = val.freshness(self.now(), self.now() - timedelta(days=3))
        self.assertEqual(out["class"], "STALE")

    def test_historical(self):
        out = val.freshness(self.now(), self.now() - timedelta(days=90))
        self.assertEqual(out["class"], "HISTORICAL")

    def test_future_rejected(self):
        out = val.freshness(self.now(), self.now() + timedelta(minutes=5))
        self.assertEqual(out["class"], "FUTURE")

    def test_naive_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            val.freshness(datetime(2026, 11, 14), datetime(2026, 11, 14))


class TestChartQuality(unittest.TestCase):
    def test_perfect_chart(self):
        observed = {key: True for key, _, _ in val.QUALITY_DIMENSIONS}
        out = val.score_chart_quality(observed)
        self.assertEqual(out["score"], out["max"])
        self.assertIn("full analysis", out["consequence"])

    def test_empty_chart_is_a_stop(self):
        out = val.score_chart_quality({})
        self.assertEqual(out["score"], 0)
        self.assertIn("stop", out["consequence"])

    def test_mid_quality_caps_the_verdict(self):
        observed = {"instrument_identifiable": True, "timeframe_visible": True,
                    "price_axis_readable": True}
        out = val.score_chart_quality(observed)
        self.assertEqual(out["score"], 5)
        self.assertIn("no precise levels", out["consequence"])

    def test_missing_listed(self):
        out = val.score_chart_quality({"instrument_identifiable": True})
        self.assertIn("volume_present", out["missing"])


class TestTimestampNormalisation(unittest.TestCase):
    def test_naive_gets_default_offset(self):
        out = val.normalise_timestamp("2026-11-14T09:15:00", "+05:30")
        self.assertTrue(out.endswith("+05:30"))

    def test_zulu_converted(self):
        out = val.normalise_timestamp("2026-11-14T09:15:00Z")
        self.assertIn("+00:00", out)

    def test_unparseable(self):
        with self.assertRaises(ValueError):
            val.normalise_timestamp("not-a-date")


class TestProviders(unittest.TestCase):
    def test_bar_validation_catches_bad_high(self):
        bar = Bar(timestamp="2026-01-01T00:00:00+00:00", open=100, high=99, low=98,
                  close=100, source="test")
        self.assertTrue(validate_bars([bar]))

    def test_validate_bars_clean(self):
        bars = [
            Bar("2026-01-01T00:00:00+00:00", 100, 101, 99, 100, 10, source="t"),
            Bar("2026-01-02T00:00:00+00:00", 100, 102, 99, 101, 12, source="t"),
        ]
        self.assertEqual(validate_bars(bars), [])

    def test_missing_source_flagged(self):
        bar = Bar("2026-01-01T00:00:00+00:00", 100, 101, 99, 100)
        self.assertTrue(any("source" in p for p in validate_bars([bar])))

    def test_in_memory_provider(self):
        provider = InMemoryProvider({"X": {"open": [1], "high": [2], "low": [0.5],
                                          "close": [1.5], "volume": [10]}})
        bars = provider.fetch_ohlcv("X", "1D")
        self.assertEqual(len(bars), 1)
        self.assertEqual(bars[0].source, "in-memory")
        self.assertEqual(provider.health()["status"], "ok")

    def test_in_memory_option_chain_unsupported(self):
        provider = InMemoryProvider({"X": {"open": [1], "high": [2], "low": [0.5],
                                          "close": [1.5], "volume": [10]}})
        with self.assertRaises(NotSupported):
            provider.fetch_option_chain("X", "2026-11-27")

    def test_environment_reports_presence_not_values(self):
        env = describe_environment({"TI_MARKET_DATA_KEY": "super-secret-value",
                                    "TI_MARKET_DATA_PROVIDER": "demo"})
        self.assertIn("TI_MARKET_DATA_KEY", env["configured"])
        self.assertNotIn("super-secret-value", str(env))

    def test_offline_mode_default(self):
        self.assertIn("OFFLINE", describe_environment({})["mode"])


if __name__ == "__main__":
    unittest.main()
