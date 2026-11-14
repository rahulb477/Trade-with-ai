import unittest

from trading_intel import stats


class TestBasics(unittest.TestCase):
    def test_mean_median(self):
        self.assertAlmostEqual(stats.mean([1, 2, 3, 4]), 2.5)
        self.assertAlmostEqual(stats.median([1, 2, 3, 4]), 2.5)
        self.assertAlmostEqual(stats.median([1, 2, 3]), 2.0)

    def test_empty_returns_none(self):
        self.assertIsNone(stats.mean([]))
        self.assertIsNone(stats.median([]))
        self.assertIsNone(stats.stdev([1]))

    def test_sample_stdev(self):
        values = [2, 4, 4, 4, 5, 5, 7, 9]
        self.assertAlmostEqual(stats.stdev(values, sample=True), 2.13809, places=4)

    def test_percentile_endpoints(self):
        values = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(stats.percentile(values, 0), 1.0)
        self.assertAlmostEqual(stats.percentile(values, 100), 5.0)
        self.assertAlmostEqual(stats.percentile(values, 50), 3.0)

    def test_percentile_bounds(self):
        with self.assertRaises(ValueError):
            stats.percentile([1, 2, 3], 101)

    def test_describe_always_includes_n(self):
        block = stats.describe([1.0, 2.0, 3.0])
        self.assertEqual(block["n"], 3)
        self.assertIn("p05", block)


class TestCorrelation(unittest.TestCase):
    def test_perfect_positive(self):
        self.assertAlmostEqual(stats.correlation([1, 2, 3, 4], [2, 4, 6, 8]), 1.0)

    def test_perfect_negative(self):
        self.assertAlmostEqual(stats.correlation([1, 2, 3, 4], [8, 6, 4, 2]), -1.0)

    def test_zero_variance_is_none(self):
        self.assertIsNone(stats.correlation([1, 2, 3], [5, 5, 5]))

    def test_small_sample_is_none(self):
        self.assertIsNone(stats.correlation([1, 2], [2, 3]))

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            stats.correlation([1, 2, 3], [1, 2])


class TestReturnsAndRatios(unittest.TestCase):
    def test_simple_returns(self):
        r = stats.returns([100, 110, 99])
        self.assertAlmostEqual(r[0], 0.1)
        self.assertAlmostEqual(r[1], -0.1)

    def test_log_returns(self):
        import math
        r = stats.returns([100, 110], log=True)
        self.assertAlmostEqual(r[0], math.log(1.1))

    def test_sharpe_requires_30_observations(self):
        self.assertIsNone(stats.sharpe([0.01] * 20))
        self.assertIsNotNone(stats.sharpe([0.01, -0.005] * 30))

    def test_zero_volatility_is_none(self):
        self.assertIsNone(stats.sharpe([0.01] * 100))

    def test_max_drawdown(self):
        self.assertAlmostEqual(stats.max_drawdown([100, 120, 90]), 0.25)


class TestWilson(unittest.TestCase):
    def test_known_value(self):
        low, high = stats.wilson_interval(5, 10)
        self.assertAlmostEqual(low, 0.2366, places=3)
        self.assertAlmostEqual(high, 0.7634, places=3)

    def test_small_sample_is_wide(self):
        low, high = stats.wilson_interval(2, 3)
        self.assertGreater(high - low, 0.4)

    def test_bounds_never_exceed_unit_interval(self):
        for k, n in [(0, 10), (10, 10), (1, 1), (0, 1)]:
            low, high = stats.wilson_interval(k, n)
            self.assertGreaterEqual(low, 0.0)
            self.assertLessEqual(high, 1.0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            stats.wilson_interval(5, 0)
        with self.assertRaises(ValueError):
            stats.wilson_interval(11, 10)


class TestMultipleTesting(unittest.TestCase):
    def test_known_value(self):
        self.assertAlmostEqual(stats.multiple_testing_probability(20, 0.05), 0.6415, places=3)

    def test_zero_tests(self):
        self.assertEqual(stats.multiple_testing_probability(0), 0.0)

    def test_monotonic(self):
        self.assertLess(
            stats.multiple_testing_probability(5),
            stats.multiple_testing_probability(50),
        )


if __name__ == "__main__":
    unittest.main()
