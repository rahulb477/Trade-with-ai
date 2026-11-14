import unittest

from trading_intel import indicators as ind

from tests.support import FLAT, RISING


class TestMACD(unittest.TestCase):
    def test_flat_series_is_zero(self):
        # 26 (slow) + 9 (signal) - 1 bars are needed before the signal exists
        flat = FLAT * 2
        macd_line, signal, hist = ind.macd(flat, 12, 26, 9)
        self.assertAlmostEqual(macd_line[-1], 0.0)
        self.assertAlmostEqual(signal[-1], 0.0)
        self.assertAlmostEqual(hist[-1], 0.0)

    def test_rising_series_positive(self):
        macd_line, _, _ = ind.macd(RISING)
        self.assertGreater(macd_line[-1], 0)

    def test_histogram_is_difference(self):
        macd_line, signal, hist = ind.macd(RISING)
        self.assertIsNotNone(hist[-1])
        self.assertAlmostEqual(hist[-1], macd_line[-1] - signal[-1])

    def test_lengths_match_input(self):
        out = ind.macd(RISING)
        self.assertEqual(len(out[0]), len(RISING))
        self.assertEqual(len(out[1]), len(RISING))
        self.assertEqual(len(out[2]), len(RISING))

    def test_fast_must_be_shorter(self):
        with self.assertRaises(ValueError):
            ind.macd(RISING, fast=26, slow=12)

    def test_insufficient_data(self):
        _, signal, _ = ind.macd([1, 2, 3], 2, 3, 2)
        self.assertTrue(all(v is None for v in signal))

    def test_signal_none_while_warming_up(self):
        macd_line, signal, hist = ind.macd(FLAT, 12, 26, 9)
        self.assertIsNone(signal[-1])
        self.assertIsNone(hist[-1])


if __name__ == "__main__":
    unittest.main()
