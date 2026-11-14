import unittest

from trading_intel import indicators as ind

from tests.support import synthetic


class TestATR(unittest.TestCase):
    def test_true_range_first_bar(self):
        tr = ind.true_range([102], [98], [100])
        self.assertAlmostEqual(tr[0], 4.0)

    def test_true_range_includes_gaps(self):
        tr = ind.true_range([10, 15], [9, 14], [9.5, 14.5])
        self.assertAlmostEqual(tr[1], max(1.0, abs(15 - 9.5), abs(14 - 9.5)))

    def test_constant_range_series(self):
        n = 40
        highs = [101.0] * n
        lows = [99.0] * n
        closes = [100.0] * n
        value = ind.atr(highs, lows, closes, 14)[-1]
        self.assertAlmostEqual(value, 2.0)

    def test_warmup_none(self):
        out = ind.atr([1, 2, 3], [0.5, 1, 2], [1, 1.5, 2.5], 14)
        self.assertTrue(all(v is None for v in out))

    def test_positive_on_synthetic(self):
        data = synthetic()
        value = ind.atr(data["high"], data["low"], data["close"])[-1]
        self.assertIsNotNone(value)
        self.assertGreater(value, 0)

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            ind.true_range([1, 2], [1], [1, 2])


if __name__ == "__main__":
    unittest.main()
