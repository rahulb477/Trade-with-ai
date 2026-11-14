import unittest

from trading_intel import indicators as ind

from tests.support import synthetic


class TestIchimoku(unittest.TestCase):
    def test_tenkan_is_range_midpoint(self):
        highs = [10, 12, 14, 16, 18, 20, 22, 24, 26]
        lows = [9, 11, 13, 15, 17, 19, 21, 23, 25]
        closes = [9.5, 11.5, 13.5, 15.5, 17.5, 19.5, 21.5, 23.5, 25.5]
        out = ind.ichimoku(highs, lows, closes, 9, 3, 5)
        self.assertAlmostEqual(out["tenkan"][-1], (26 + 9) / 2)

    def test_all_components_present_and_aligned(self):
        data = synthetic(120, seed=8)
        out = ind.ichimoku(data["high"], data["low"], data["close"])
        self.assertEqual(set(out), {"tenkan", "kijun", "senkou_a", "senkou_b", "chikou"})
        for series in out.values():
            self.assertEqual(len(series), 120)

    def test_leading_span_is_shifted_forward(self):
        data = synthetic(120, seed=8)
        out = ind.ichimoku(data["high"], data["low"], data["close"])
        # values computed early are plotted 26 bars later, so the head is empty
        # and the tail carries the most recent projection
        self.assertIsNone(out["senkou_a"][0])
        self.assertIsNotNone(out["senkou_a"][-1])

    def test_chikou_is_shifted_back(self):
        data = synthetic(120, seed=8)
        out = ind.ichimoku(data["high"], data["low"], data["close"])
        # close[i] is plotted at i-26, so the tail is empty and the head is filled
        self.assertIsNotNone(out["chikou"][0])
        self.assertTrue(all(v is None for v in out["chikou"][-26:]))


if __name__ == "__main__":
    unittest.main()
