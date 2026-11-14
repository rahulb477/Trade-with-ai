import unittest

from trading_intel import timeframes as tf
from tests.support import synthetic


class TestRatios(unittest.TestCase):
    def test_known_ratio(self):
        self.assertAlmostEqual(tf.ratio("15m", "1D"), 25.0)
        self.assertAlmostEqual(tf.ratio("1H", "4H"), 4.0)

    def test_quality_bands(self):
        self.assertEqual(tf.ratio_quality("1H", "4H"), "good")
        self.assertEqual(tf.ratio_quality("15m", "1H"), "good")
        self.assertEqual(tf.ratio_quality("15m", "1D"), "too_far")
        self.assertEqual(tf.ratio_quality("1D", "1D"), "invalid")

    def test_unknown_label(self):
        with self.assertRaises(ValueError):
            tf.ratio("7m", "1H")

    def test_suggest_pair(self):
        candidate = tf.suggest_pair("1D", ["5m", "15m", "1H", "1W"])
        self.assertIn(candidate, ["1H", "15m"])


class TestAggregation(unittest.TestCase):
    def test_fixed_count_aggregation(self):
        data = synthetic(bars=40, seed=1)
        out = tf.aggregate(data, "1H", "4H")
        self.assertEqual(len(out["close"]), 10)
        self.assertAlmostEqual(out["high"][0], max(data["high"][:4]))
        self.assertAlmostEqual(out["low"][0], min(data["low"][:4]))
        self.assertAlmostEqual(out["open"][0], data["open"][0])
        self.assertAlmostEqual(out["close"][0], data["close"][3])

    def test_volume_sums(self):
        data = {"open": [1, 2, 3, 4], "high": [2, 3, 4, 5], "low": [0.5, 1.5, 2.5, 3.5],
                "close": [1.5, 2.5, 3.5, 4.5], "volume": [10, 20, 30, 40]}
        out = tf.aggregate(data, "1H", "4H")
        self.assertAlmostEqual(out["volume"][0], 100)

    def test_aggregating_upwards_is_rejected(self):
        # source must be the LOWER timeframe; 4H -> 1H would be disaggregation
        data = {"open": [1], "high": [1], "low": [1], "close": [1], "volume": [0]}
        with self.assertRaises(ValueError):
            tf.aggregate(data, "4H", "1H")

    def test_same_timeframe_rejected(self):
        data = {"open": [1, 2], "high": [2, 3], "low": [0.5, 1.5], "close": [1.5, 2.5],
                "volume": [1, 1]}
        with self.assertRaises(ValueError):
            tf.aggregate(data, "1H", "1H")

    def test_two_to_one_ratio_is_allowed(self):
        data = {"open": [1, 2], "high": [2, 3], "low": [0.5, 1.5], "close": [1.5, 2.5],
                "volume": [1, 1]}
        out = tf.aggregate(data, "1H", "2H")
        self.assertEqual(len(out["close"]), 1)
        self.assertAlmostEqual(out["high"][0], 3)

    def test_daily_grouping_by_date(self):
        timestamps = ["2026-11-13T09:15:00+05:30", "2026-11-13T09:20:00+05:30",
                      "2026-11-14T09:15:00+05:30"]
        ohlc = {"open": [100, 101, 102], "high": [102, 103, 104],
                "low": [99, 100, 101], "close": [101, 102, 103]}
        out = tf.aggregate_intraday_to_daily(timestamps, ohlc, volume=[10, 20, 30])
        self.assertEqual(out["date"], ["2026-11-13", "2026-11-14"])
        self.assertEqual(out["high"], [103, 104])
        self.assertEqual(out["volume"], [30, 30])

    def test_timestamp_length_mismatch(self):
        with self.assertRaises(ValueError):
            tf.aggregate_intraday_to_daily(["2026-11-13"], {"open": [1, 2], "high": [1, 2],
                                                          "low": [1, 2], "close": [1, 2]})


class TestAlignment(unittest.TestCase):
    def test_full_alignment(self):
        out = tf.alignment({"1W": "up", "1D": "up", "1H": "up"})
        self.assertEqual(out["classification"], "fully_aligned")
        self.assertEqual(out["agreement"], 1.0)

    def test_conflict(self):
        out = tf.alignment({"1D": "up", "1H": "down"})
        self.assertEqual(out["classification"], "conflicting")
        self.assertTrue(out["conflicts"])

    def test_mixed(self):
        out = tf.alignment({"1W": "up", "1D": "up", "1H": "down"})
        self.assertEqual(out["classification"], "mixed")

    def test_unknown_is_not_agreement(self):
        out = tf.alignment({"1W": "up", "1D": "unknown", "1H": "flat"})
        self.assertEqual(out["timeframes_counted"], 1)
        self.assertEqual(out["unknown_timeframes"], ["1D", "1H"])

    def test_no_data(self):
        out = tf.alignment({"1D": "unknown"})
        self.assertEqual(out["classification"], "no_data")

    def test_operating_timeframe_good(self):
        out = tf.operating_timeframe("4H", "1H")
        self.assertEqual(out["quality"], "good")

    def test_operating_timeframe_too_far(self):
        out = tf.operating_timeframe("1D", "5m")
        self.assertEqual(out["quality"], "too_far")


if __name__ == "__main__":
    unittest.main()
