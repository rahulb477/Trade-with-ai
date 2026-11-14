import unittest

from trading_intel import indicators as ind

from tests.support import synthetic


class TestADX(unittest.TestCase):
    def test_strong_trend_gives_high_adx(self):
        n = 80
        closes = [100 + 2 * i for i in range(n)]
        highs = [c + 1 for c in closes]
        lows = [c - 1 for c in closes]
        adx_line, plus_di, minus_di = ind.adx(highs, lows, closes, 14)
        self.assertGreater(adx_line[-1], 40)
        self.assertGreater(plus_di[-1], minus_di[-1])

    def test_downtrend_flips_di(self):
        n = 80
        closes = [300 - 2 * i for i in range(n)]
        highs = [c + 1 for c in closes]
        lows = [c - 1 for c in closes]
        _, plus_di, minus_di = ind.adx(highs, lows, closes, 14)
        self.assertGreater(minus_di[-1], plus_di[-1])

    def test_bounds(self):
        data = synthetic(300, seed=9)
        adx_line, plus_di, minus_di = ind.adx(data["high"], data["low"], data["close"])
        for value in adx_line:
            if value is not None:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 100.0)

    def test_warmup_none(self):
        adx_line, _, _ = ind.adx([1, 2, 3], [0.5, 1.5, 2.5], [1, 2, 3], 14)
        self.assertTrue(all(v is None for v in adx_line))


if __name__ == "__main__":
    unittest.main()
