import unittest

from trading_intel import indicators as ind


class TestVWAP(unittest.TestCase):
    def test_single_bar(self):
        out = ind.vwap([102], [98], [100], [500])
        self.assertAlmostEqual(out[0], 100.0)

    def test_constant_price(self):
        n = 10
        out = ind.vwap([101] * n, [99] * n, [100] * n, [1000] * n)
        self.assertAlmostEqual(out[-1], 100.0)

    def test_weights_by_volume(self):
        # bar 1: TP 100 vol 100 ; bar 2: TP 110 vol 300 -> (100*100 + 110*300)/400
        out = ind.vwap([100, 110], [100, 110], [100, 110], [100, 300])
        self.assertAlmostEqual(out[-1], (100 * 100 + 110 * 300) / 400)

    def test_reset_index(self):
        out = ind.vwap([100, 200, 200], [100, 200, 200], [100, 200, 200], [1, 1, 1], reset_index=1)
        self.assertIsNone(out[0])
        self.assertAlmostEqual(out[1], 200.0)

    def test_zero_volume_yields_none(self):
        out = ind.vwap([100], [100], [100], [0])
        self.assertIsNone(out[0])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            ind.vwap([1, 2], [1], [1, 2], [1, 2])


if __name__ == "__main__":
    unittest.main()
