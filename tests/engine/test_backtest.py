import unittest

from trading_intel import backtest, simulate
from tests.support import synthetic


class TestSimulate(unittest.TestCase):
    def setUp(self):
        self.data = synthetic(bars=300, seed=21)

    def test_runs_and_reports_structure(self):
        result = backtest.simulate(self.data, backtest.simple_ema_cross_strategy(10, 30))
        for key in ("trades", "summary", "equity_r", "max_drawdown_r", "final_equity", "caveats"):
            self.assertIn(key, result)
        self.assertGreaterEqual(len(result["caveats"]), 3)

    def test_no_lookahead_fill_is_next_bar_open(self):
        data = self.data
        def always_long(ctx, i):
            return backtest.Signal("long", ctx["low"][i] - 1.0)
        result = backtest.simulate(data, always_long,
                                   backtest.BacktestConfig(max_bars_in_trade=1))
        if result["trades"]:
            first = result["trades"][0]
            self.assertEqual(first.entry_price, data["open"][first.entry_index])

    def test_stop_is_checked_before_target(self):
        # a bar that touches both directions should exit at the stop, not a profit
        data = {
            "open": [100, 100, 100],
            "high": [101, 130, 101],
            "low": [99, 70, 99],
            "close": [100, 100, 100],
            "volume": [1, 1, 1],
        }
        def long_once(ctx, i):
            return backtest.Signal("long", 90.0) if i == 0 else None
        result = backtest.simulate(data, long_once, backtest.BacktestConfig(cost_bps_round_trip=0))
        self.assertEqual(result["trades"][0].reason, "stop")
        self.assertAlmostEqual(result["trades"][0].exit_price, 90.0)

    def test_gap_through_stop_fills_at_open(self):
        data = {
            "open": [100, 100, 85],
            "high": [101, 101, 86],
            "low": [99, 99, 84],
            "close": [100, 100, 85],
            "volume": [1, 1, 1],
        }
        def long_once(ctx, i):
            return backtest.Signal("long", 90.0) if i == 0 else None
        result = backtest.simulate(data, long_once, backtest.BacktestConfig(cost_bps_round_trip=0))
        self.assertEqual(result["trades"][0].reason, "gap_stop")
        self.assertAlmostEqual(result["trades"][0].exit_price, 85.0)
        self.assertLess(result["trades"][0].r, -1.0)

    def test_costs_reduce_r(self):
        data = self.data
        def long_once(ctx, i):
            return backtest.Signal("long", ctx["close"][i] * 0.98) if i == 20 else None
        free = backtest.simulate(data, long_once, backtest.BacktestConfig(cost_bps_round_trip=0))
        costly = backtest.simulate(data, long_once, backtest.BacktestConfig(cost_bps_round_trip=50))
        if free["trades"] and costly["trades"]:
            self.assertLess(costly["trades"][0].r, free["trades"][0].r)

    def test_short_disabled(self):
        data = self.data
        def short_signal(ctx, i):
            return backtest.Signal("short", ctx["close"][i] * 1.02) if i == 20 else None
        result = backtest.simulate(data, short_signal,
                                   backtest.BacktestConfig(allow_short=False))
        self.assertEqual(len(result["trades"]), 0)

    def test_invalid_risk_rejected(self):
        with self.assertRaises(ValueError):
            backtest.simulate(self.data, lambda ctx, i: None, backtest.BacktestConfig(risk_pct=0.6))

    def test_mismatched_series_rejected(self):
        with self.assertRaises(ValueError):
            backtest.simulate({"open": [1, 2], "high": [1], "low": [1, 2], "close": [1, 2]},
                              lambda ctx, i: None)


class TestWalkForward(unittest.TestCase):
    def test_split_count_and_ordering(self):
        splits = backtest.walk_forward_splits(1000, 200, 100)
        self.assertGreater(len(splits), 0)
        for train_start, train_end, test_start, test_end in splits:
            self.assertEqual(train_end, test_start)
            self.assertLess(train_start, test_end)

    def test_no_overlap_in_test_segments(self):
        splits = backtest.walk_forward_splits(1000, 200, 100)
        for a, b in zip(splits, splits[1:]):
            self.assertEqual(a[3], b[2])

    def test_insufficient_bars(self):
        self.assertEqual(backtest.walk_forward_splits(100, 200, 100), [])

    def test_invalid_windows(self):
        with self.assertRaises(ValueError):
            backtest.walk_forward_splits(1000, 0, 100)


if __name__ == "__main__":
    unittest.main()
