import unittest

from trading_intel import indicators as ind


class TestPivots(unittest.TestCase):
    def test_classic_values(self):
        p = ind.pivot_points(high=120, low=110, close=117)
        self.assertAlmostEqual(p["P"], (120 + 110 + 117) / 3)
        self.assertAlmostEqual(p["R1"], 2 * p["P"] - 110)
        self.assertAlmostEqual(p["S1"], 2 * p["P"] - 120)
        self.assertAlmostEqual(p["R2"], p["P"] + 10)

    def test_level_ordering(self):
        p = ind.pivot_points(120, 110, 117)
        self.assertGreater(p["R3"], p["R2"])
        self.assertGreater(p["R2"], p["R1"])
        self.assertGreater(p["R1"], p["P"])
        self.assertGreater(p["P"], p["S1"])

    def test_fibonacci_ratios(self):
        p = ind.pivot_points(200, 100, 150, method="fibonacci")
        self.assertAlmostEqual(p["R1"], p["P"] + 38.2, places=6)

    def test_camarilla_and_woodie_exist(self):
        self.assertIn("R4", ind.pivot_points(120, 110, 117, "camarilla"))
        self.assertIn("P", ind.pivot_points(120, 110, 117, "woodie"))

    def test_unknown_method(self):
        with self.assertRaises(ValueError):
            ind.pivot_points(1, 2, 3, "magic")


if __name__ == "__main__":
    unittest.main()
