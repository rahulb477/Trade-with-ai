import unittest

from trading_intel import indicators as ind

from tests.support import synthetic


class TestSupertrend(unittest.TestCase):
    def test_uptrend_is_up(self):
        closes = [100 + 1.5 * i for i in range(60)]
        highs = [c + 0.5 for c in closes]
        lows = [c - 0.5 for c in closes]
        line, direction = ind.supertrend(highs, lows, closes, 10, 3.0)
        self.assertEqual(direction[-1], "up")
        self.assertLess(line[-1], closes[-1])

    def test_downtrend_is_down(self):
        closes = [300 - 1.5 * i for i in range(60)]
        highs = [c + 0.5 for c in closes]
        lows = [c - 0.5 for c in closes]
        line, direction = ind.supertrend(highs, lows, closes, 10, 3.0)
        self.assertEqual(direction[-1], "down")
        self.assertGreater(line[-1], closes[-1])

    def test_direction_values_are_constrained(self):
        data = synthetic(200, seed=2)
        _, direction = ind.supertrend(data["high"], data["low"], data["close"])
        self.assertTrue(set(d for d in direction if d) <= {"up", "down"})

    def test_warmup_none(self):
        _, direction = ind.supertrend([1, 2, 3], [0.5, 1.5, 2.5], [1, 2, 3], 10, 3.0)
        self.assertTrue(all(d is None for d in direction))


if __name__ == "__main__":
    unittest.main()
