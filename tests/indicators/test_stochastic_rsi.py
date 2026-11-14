import unittest

from trading_intel import indicators as ind

from tests.support import synthetic


class TestStochasticRSI(unittest.TestCase):
    def test_bounds(self):
        data = synthetic(200, seed=4)
        k, d = ind.stochastic_rsi(data["close"])
        for value in k:
            if value is not None:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 100.0)
        for value in d:
            if value is not None:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 100.0)

    def test_flat_rsi_window_is_undefined(self):
        # a strictly rising series keeps RSI at 100, so hi == lo and the value is None
        closes = [100 + i for i in range(80)]
        k, _ = ind.stochastic_rsi(closes)
        self.assertIsNone(k[-1])

    def test_lengths(self):
        closes = [100 + (i % 5) for i in range(90)]
        k, d = ind.stochastic_rsi(closes)
        self.assertEqual(len(k), len(closes))
        self.assertEqual(len(d), len(closes))


if __name__ == "__main__":
    unittest.main()
