import unittest

from trading_intel import indicators as ind


class TestOBV(unittest.TestCase):
    def test_rising_prices_add_volume(self):
        out = ind.obv([1, 2, 3], [100, 100, 100])
        self.assertEqual(out, [0.0, 100.0, 200.0])

    def test_falling_prices_subtract(self):
        out = ind.obv([3, 2, 1], [100, 100, 100])
        self.assertEqual(out, [0.0, -100.0, -200.0])

    def test_unchanged_price_is_flat(self):
        out = ind.obv([5, 5, 5], [100, 200, 300])
        self.assertEqual(out, [0.0, 0.0, 0.0])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            ind.obv([1, 2], [1])

    def test_empty(self):
        self.assertEqual(ind.obv([], []), [])


if __name__ == "__main__":
    unittest.main()
