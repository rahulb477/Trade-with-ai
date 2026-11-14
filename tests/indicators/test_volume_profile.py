import unittest

from trading_intel import indicators as ind


class TestVolumeProfile(unittest.TestCase):
    def test_single_price_level_is_rejected(self):
        # no price range -> no profile; the function refuses rather than inventing one
        with self.assertRaises(ValueError):
            ind.volume_profile([100] * 5, [100] * 5, [100] * 5, [10] * 5, bins=10)

    def test_narrow_range_still_profiles(self):
        out = ind.volume_profile([100.2] * 5, [99.8] * 5, [100] * 5, [10] * 5, bins=10)
        self.assertAlmostEqual(out["total_volume"], 50.0)
        self.assertGreaterEqual(out["poc"], 99.8)
        self.assertLessEqual(out["poc"], 100.2)

    def test_poc_is_highest_volume_price(self):
        highs = [101, 102, 111, 112]
        lows = [100, 101, 110, 111]
        closes = [100.5, 101.5, 110.5, 111.5]
        volumes = [1000, 1000, 50, 50]
        out = ind.volume_profile(highs, lows, closes, volumes, bins=12)
        self.assertLess(out["poc"], 105)

    def test_value_area_contains_poc(self):
        out = ind.volume_profile([101, 111], [99, 109], [100, 110], [500, 500], bins=20)
        self.assertLessEqual(out["val"], out["poc"])
        self.assertGreaterEqual(out["vah"], out["poc"])

    def test_total_volume_is_conserved(self):
        out = ind.volume_profile([101, 105, 110], [99, 100, 105], [100, 102, 108], [10, 20, 30], bins=10)
        self.assertAlmostEqual(out["total_volume"], 60.0)

    def test_degenerate_range_raises(self):
        with self.assertRaises(ValueError):
            ind.volume_profile([100] * 3, [100] * 3, [100] * 3, [1, 2, 3], bins=10)

    def test_invalid_bins(self):
        with self.assertRaises(ValueError):
            ind.volume_profile([101], [99], [100], [1], bins=0)


if __name__ == "__main__":
    unittest.main()
