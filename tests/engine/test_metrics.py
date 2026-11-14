import unittest

from trading_intel import metrics


def trades(rs):
    return [metrics.Trade(r=r) for r in rs]


class TestSummarize(unittest.TestCase):
    def test_empty(self):
        out = metrics.summarize([])
        self.assertEqual(out["n"], 0)
        self.assertIn("no trades", out["notes"][0])

    def test_known_series(self):
        out = metrics.summarize(trades([2.0, -1.0, 2.0, -1.0, 2.0, -1.0]))
        self.assertEqual(out["n"], 6)
        self.assertEqual(out["wins"], 3)
        self.assertAlmostEqual(out["hit_rate"], 0.5)
        self.assertAlmostEqual(out["avg_win_r"], 2.0)
        self.assertAlmostEqual(out["avg_loss_r"], -1.0)
        self.assertAlmostEqual(out["expectancy_r"], 0.5)
        self.assertAlmostEqual(out["profit_factor"], 2.0)

    def test_scratch_counted_separately(self):
        out = metrics.summarize(trades([1.0, 0.0, -1.0]))
        self.assertEqual(out["scratches"], 1)
        self.assertEqual(out["wins"], 1)

    def test_small_sample_note(self):
        out = metrics.summarize(trades([1.0, -1.0, 2.0]))
        self.assertTrue(any("below 30" in n for n in out["notes"]))

    def test_confidence_interval_reported(self):
        out = metrics.summarize(trades([1.0] * 60 + [-1.0] * 40))
        low, high = out["hit_rate_ci95"]
        self.assertLess(low, 0.6)
        self.assertGreater(high, 0.6)

    def test_longest_losing_streak(self):
        out = metrics.summarize(trades([1, -1, -1, -1, 1, -1]))
        self.assertEqual(out["longest_losing_streak"], 3)

    def test_no_losses_has_no_profit_factor(self):
        out = metrics.summarize(trades([1.0, 2.0]))
        self.assertIsNone(out["profit_factor"])


class TestCurves(unittest.TestCase):
    def test_equity_curve(self):
        self.assertEqual(metrics.equity_curve(trades([1.0, -2.0])), [0.0, 1.0, -1.0])

    def test_max_drawdown_r(self):
        self.assertAlmostEqual(metrics.max_drawdown_r([0, 5, 2, 6, 1]), 5.0)

    def test_expectancy_with_costs(self):
        value = metrics.expectancy_with_costs(trades([2.0, -1.0]), 0.1)
        self.assertAlmostEqual(value, 0.4)


class TestTagging(unittest.TestCase):
    def test_by_tag(self):
        group = [
            metrics.Trade(r=1.0, tags=["breakout"]),
            metrics.Trade(r=-1.0, tags=["breakout"]),
            metrics.Trade(r=2.0, tags=["pullback"]),
        ]
        out = metrics.by_tag(group)
        self.assertEqual(out["breakout"]["n"], 2)
        self.assertEqual(out["pullback"]["n"], 1)

    def test_untagged_group(self):
        out = metrics.by_tag([metrics.Trade(r=1.0)])
        self.assertIn("untagged", out)

    def test_from_dicts(self):
        parsed = metrics.from_dicts([{"r": "1.5", "instrument": "X"}])
        self.assertEqual(parsed[0].r, 1.5)
        self.assertEqual(parsed[0].instrument, "X")

    def test_mae_mfe(self):
        group = [metrics.Trade(r=1.0, mae_r=-0.5, mfe_r=1.2)]
        out = metrics.mae_mfe_table(group)
        self.assertAlmostEqual(out["avg_mae_r"], -0.5)
        self.assertEqual(out["n_with_mfe"], 1)


if __name__ == "__main__":
    unittest.main()
