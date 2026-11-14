import unittest

from trading_intel import indicators as ind

from tests.support import FALLING, FLAT, RISING


class TestSMA(unittest.TestCase):
    def test_hand_computed(self):
        self.assertEqual(ind.sma([1, 2, 3, 4, 5], 3), [None, None, 2.0, 3.0, 4.0])

    def test_short_input_returns_all_none(self):
        self.assertEqual(ind.sma([1, 2], 5), [None, None])

    def test_length_preserved(self):
        self.assertEqual(len(ind.sma(RISING, 10)), len(RISING))

    def test_flat_series_equals_value(self):
        self.assertEqual(ind.sma(FLAT, 5)[-1], 100.0)

    def test_rejects_bad_period(self):
        with self.assertRaises(ValueError):
            ind.sma([1, 2, 3], 0)


class TestEMA(unittest.TestCase):
    def test_hand_computed_seed_and_smoothing(self):
        # seed = mean(1,2,3) = 2 ; alpha = 2/(3+1) = 0.5
        out = ind.ema([1, 2, 3, 4, 5], 3)
        self.assertIsNone(out[1])
        self.assertAlmostEqual(out[2], 2.0)
        self.assertAlmostEqual(out[3], 3.0)
        self.assertAlmostEqual(out[4], 4.0)

    def test_flat_series_stays_flat(self):
        self.assertAlmostEqual(ind.ema(FLAT, 10)[-1], 100.0)

    def test_ema_tracks_direction(self):
        self.assertGreater(ind.ema(RISING, 10)[-1], ind.ema(RISING, 10)[-5])
        self.assertLess(ind.ema(FALLING, 10)[-1], ind.ema(FALLING, 10)[-5])

    def test_first_period_minus_one_values_are_none(self):
        out = ind.ema(RISING, 12)
        self.assertTrue(all(v is None for v in out[:11]))
        self.assertIsNotNone(out[11])


if __name__ == "__main__":
    unittest.main()
