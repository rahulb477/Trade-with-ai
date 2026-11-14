import unittest

from trading_intel import indicators as ind


class TestMFI(unittest.TestCase):
    def test_bounds(self):
        n = 60
        closes = [100 + (i % 9) for i in range(n)]
        highs = [c + 1 for c in closes]
        lows = [c - 1 for c in closes]
        volumes = [1000 + i for i in range(n)]
        for value in ind.mfi(highs, lows, closes, volumes, 14):
            if value is not None:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 100.0)

    def test_all_up_flow_is_100(self):
        closes = [100 + i for i in range(30)]
        out = ind.mfi([c + 1 for c in closes], [c - 1 for c in closes], closes, [1000] * 30, 14)
        self.assertAlmostEqual(out[-1], 100.0)

    def test_all_down_flow_is_zero(self):
        closes = [200 - i for i in range(30)]
        out = ind.mfi([c + 1 for c in closes], [c - 1 for c in closes], closes, [1000] * 30, 14)
        self.assertAlmostEqual(out[-1], 0.0)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            ind.mfi([1, 2], [1, 2], [1, 2], [1])

    def test_warmup_none(self):
        out = ind.mfi([1, 2, 3], [0.5, 1.5, 2.5], [1, 2, 3], [1, 1, 1], 14)
        self.assertTrue(all(v is None for v in out))


if __name__ == "__main__":
    unittest.main()
