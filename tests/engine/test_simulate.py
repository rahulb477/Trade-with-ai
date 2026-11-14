import unittest

from trading_intel import simulate


class TestMonteCarlo(unittest.TestCase):
    def test_deterministic_with_seed(self):
        a = simulate.monte_carlo_trades([1, -1, 2, -1], trades_per_run=20, runs=50, seed=5)
        b = simulate.monte_carlo_trades([1, -1, 2, -1], trades_per_run=20, runs=50, seed=5)
        self.assertEqual(a["ending_equity_median"], b["ending_equity_median"])

    def test_different_seeds_differ(self):
        a = simulate.monte_carlo_trades([1, -1, 2, -1], trades_per_run=20, runs=50, seed=1)
        b = simulate.monte_carlo_trades([1, -1, 2, -1], trades_per_run=20, runs=50, seed=2)
        self.assertNotEqual(a["ending_equity_mean"], b["ending_equity_mean"])

    def test_percentile_ordering(self):
        out = simulate.monte_carlo_trades([2, -1, -1, 1.5], trades_per_run=40, runs=500, seed=3)
        self.assertLessEqual(out["ending_equity_p05"], out["ending_equity_median"])
        self.assertLessEqual(out["ending_equity_median"], out["ending_equity_p95"])

    def test_caveats_present(self):
        out = simulate.monte_carlo_trades([1, -1], trades_per_run=10, runs=10, seed=1)
        self.assertGreaterEqual(len(out["caveats"]), 3)

    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            simulate.monte_carlo_trades([])

    def test_costs_reduce_outcome(self):
        gross = simulate.monte_carlo_trades([1.5, -1, 1.5, -1], trades_per_run=20,
                                            runs=300, seed=4, cost_r=0.0)
        net = simulate.monte_carlo_trades([1.5, -1, 1.5, -1], trades_per_run=20,
                                          runs=300, seed=4, cost_r=0.2)
        self.assertLess(net["ending_equity_mean"], gross["ending_equity_mean"])


class TestSynthetic(unittest.TestCase):
    def test_deterministic(self):
        a = simulate.synthetic_ohlcv(bars=50, seed=9)
        b = simulate.synthetic_ohlcv(bars=50, seed=9)
        self.assertEqual(a["close"], b["close"])

    def test_ohlc_integrity(self):
        data = simulate.synthetic_ohlcv(bars=200, seed=1)
        for o, h, l, c in zip(data["open"], data["high"], data["low"], data["close"]):
            self.assertGreaterEqual(h, max(o, c))
            self.assertLessEqual(l, min(o, c))
            self.assertGreater(l, 0)

    def test_lengths(self):
        data = simulate.synthetic_ohlcv(bars=77, seed=2)
        self.assertTrue(all(len(v) == 77 for v in data.values()))

    def test_volumes_positive(self):
        data = simulate.synthetic_ohlcv(bars=100, seed=2)
        self.assertTrue(all(v > 0 for v in data["volume"]))


class TestBootstrap(unittest.TestCase):
    def test_ci_brackets_point_estimate(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        out = simulate.bootstrap_ci(values, "mean", runs=300, seed=2)
        self.assertLessEqual(out["ci_low"], out["point"])
        self.assertGreaterEqual(out["ci_high"], out["point"])

    def test_small_sample_none(self):
        self.assertIsNone(simulate.bootstrap_ci([1, 2, 3]))

    def test_reproducible(self):
        values = [float(i % 7) for i in range(40)]
        a = simulate.bootstrap_ci(values, runs=200, seed=1)
        b = simulate.bootstrap_ci(values, runs=200, seed=1)
        self.assertEqual(a["ci_low"], b["ci_low"])


if __name__ == "__main__":
    unittest.main()
