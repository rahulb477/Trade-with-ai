import unittest

from trading_intel import indicators as ind

from tests.support import FALLING, FLAT, RISING


class TestRSI(unittest.TestCase):
    def test_strictly_rising_is_100(self):
        self.assertAlmostEqual(ind.rsi(RISING, 14)[-1], 100.0)

    def test_strictly_falling_is_zero(self):
        self.assertAlmostEqual(ind.rsi(FALLING, 14)[-1], 0.0)

    def test_flat_series_flags_50(self):
        # undefined by the formula; the implementation returns 50 and documents it
        self.assertAlmostEqual(ind.rsi(FLAT, 14)[-1], 50.0)

    def test_warmup_is_none(self):
        out = ind.rsi(RISING, 14)
        self.assertTrue(all(v is None for v in out[:14]))
        self.assertIsNotNone(out[14])

    def test_bounds(self):
        closes = [100 + (i % 7) for i in range(120)]
        for value in ind.rsi(closes, 14):
            if value is not None:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 100.0)

    def test_short_input(self):
        self.assertEqual(ind.rsi([1, 2, 3], 14), [None, None, None])


if __name__ == "__main__":
    unittest.main()
