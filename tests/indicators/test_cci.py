import unittest

from trading_intel import indicators as ind

from tests.support import synthetic


class TestCCI(unittest.TestCase):
    def test_flat_series_is_undefined(self):
        n = 30
        out = ind.cci([100] * n, [100] * n, [100] * n, 20)
        self.assertIsNone(out[-1])

    def test_rising_series_positive(self):
        closes = [100 + i for i in range(60)]
        out = ind.cci([c + 1 for c in closes], [c - 1 for c in closes], closes, 20)
        self.assertGreater(out[-1], 0)

    def test_warmup_none(self):
        out = ind.cci([1, 2, 3], [0.5, 1.5, 2.5], [1, 2, 3], 20)
        self.assertTrue(all(v is None for v in out))

    def test_length(self):
        data = synthetic(150, seed=6)
        self.assertEqual(len(ind.cci(data["high"], data["low"], data["close"])), 150)


if __name__ == "__main__":
    unittest.main()
