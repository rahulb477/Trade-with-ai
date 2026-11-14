import unittest

from trading_intel import indicators as ind

from tests.support import FLAT, RISING


class TestBollinger(unittest.TestCase):
    def test_flat_series_zero_width(self):
        upper, middle, lower = ind.bollinger_bands(FLAT, 20, 2.0)
        self.assertAlmostEqual(upper[-1], 100.0)
        self.assertAlmostEqual(middle[-1], 100.0)
        self.assertAlmostEqual(lower[-1], 100.0)

    def test_bands_ordered(self):
        upper, middle, lower = ind.bollinger_bands(RISING, 20, 2.0)
        self.assertGreater(upper[-1], middle[-1])
        self.assertGreater(middle[-1], lower[-1])

    def test_two_sigma_multiplier(self):
        closes = [10, 12, 11, 13, 12, 14, 13, 15, 14, 16]
        upper, middle, lower = ind.bollinger_bands(closes, 5, 2.0)
        window = closes[-5:]
        mean = sum(window) / 5
        sd = (sum((x - mean) ** 2 for x in window) / 5) ** 0.5
        self.assertAlmostEqual(upper[-1], mean + 2 * sd)
        self.assertAlmostEqual(lower[-1], mean - 2 * sd)

    def test_bandwidth_positive(self):
        bw = ind.bollinger_bandwidth(RISING, 20, 2.0)
        self.assertGreater(bw[-1], 0)

    def test_bandwidth_none_during_warmup(self):
        bw = ind.bollinger_bandwidth(RISING, 20)
        self.assertIsNone(bw[0])


if __name__ == "__main__":
    unittest.main()
