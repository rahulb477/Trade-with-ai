import unittest

from trading_intel import indicators as ind


class TestFibonacci(unittest.TestCase):
    def test_up_retracement_levels(self):
        levels = ind.fib_levels(100, 200, "up")
        self.assertAlmostEqual(levels["retr_0.5"], 150.0)
        self.assertAlmostEqual(levels["retr_0.618"], 200 - 0.618 * 100)

    def test_up_extension_levels(self):
        levels = ind.fib_levels(100, 200, "up")
        self.assertAlmostEqual(levels["ext_1.618"], 100 + 1.618 * 100)

    def test_down_direction_mirrors(self):
        up = ind.fib_levels(100, 200, "up")
        down = ind.fib_levels(100, 200, "down")
        # retracements and extensions both mirror about the swing midpoint (150)
        self.assertAlmostEqual(up["retr_0.382"] - 150.0, 150.0 - down["retr_0.382"])
        self.assertAlmostEqual(up["ext_1.272"] - 150.0, 150.0 - down["ext_1.272"])

    def test_invalid_swing(self):
        with self.assertRaises(ValueError):
            ind.fib_levels(200, 100, "up")

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            ind.fib_levels(100, 200, "sideways")


if __name__ == "__main__":
    unittest.main()
