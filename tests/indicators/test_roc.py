import unittest

from trading_intel import indicators as ind


class TestROC(unittest.TestCase):
    def test_hand_computed(self):
        out = ind.roc([100, 110], 1)
        self.assertAlmostEqual(out[-1], 10.0)

    def test_negative(self):
        out = ind.roc([100, 90], 1)
        self.assertAlmostEqual(out[-1], -10.0)

    def test_warmup_none(self):
        out = ind.roc([1, 2, 3], 5)
        self.assertTrue(all(v is None for v in out))

    def test_zero_base_is_skipped(self):
        out = ind.roc([0, 5], 1)
        self.assertIsNone(out[-1])

    def test_length(self):
        self.assertEqual(len(ind.roc([1, 2, 3, 4], 2)), 4)


if __name__ == "__main__":
    unittest.main()
