import unittest

from trading_intel import sizing


class TestSizePosition(unittest.TestCase):
    def test_hand_computed(self):
        # 500,000 * 0.75% = 3,750 / 5 = 750 units
        result = sizing.size_position(500_000, 100, 95)
        self.assertEqual(result.units, 750)
        self.assertAlmostEqual(result.risk_amount, 3750)
        self.assertAlmostEqual(result.notional, 75_000)

    def test_rounds_down_never_up(self):
        # 100,000 * 1% = 1000 / 3 = 333.33 -> 333
        result = sizing.size_position(100_000, 100, 97, risk_pct=0.01)
        self.assertEqual(result.units, 333)
        self.assertLessEqual(result.risk_amount, 1000)

    def test_lot_size_respected(self):
        # 500,000 * 1% = 5000 / 20 = 250 -> 5 lots of 50
        result = sizing.size_position(500_000, 1000, 980, risk_pct=0.01, lot_size=50)
        self.assertEqual(result.units, 250)
        self.assertEqual(result.units % 50, 0)

    def test_zero_units_warns(self):
        result = sizing.size_position(10_000, 100, 80, risk_pct=0.005, lot_size=75)
        self.assertEqual(result.units, 0)
        self.assertTrue(result.warnings)

    def test_notional_cap(self):
        result = sizing.size_position(100_000, 100, 99.9, risk_pct=0.02,
                                      max_notional_fraction=0.5)
        self.assertLessEqual(result.notional, 50_000)
        self.assertTrue(any("notional cap" in w for w in result.warnings))

    def test_rejects_zero_stop_distance(self):
        with self.assertRaises(ValueError):
            sizing.size_position(100_000, 100, 100)

    def test_rejects_excessive_risk(self):
        with self.assertRaises(ValueError):
            sizing.size_position(100_000, 100, 95, risk_pct=0.05)

    def test_rejects_negative_equity(self):
        with self.assertRaises(ValueError):
            sizing.size_position(-1, 100, 95)

    def test_dict_round_trip(self):
        d = sizing.size_position(200_000, 50, 48).as_dict()
        self.assertIn("units", d)
        self.assertEqual(d["risk_per_unit"], 2.0)


class TestStops(unittest.TestCase):
    def test_long_stop_below_structure(self):
        self.assertAlmostEqual(sizing.stop_from_atr(100, 2.0, "long", 0.3), 99.4)

    def test_short_stop_above_structure(self):
        self.assertAlmostEqual(sizing.stop_from_atr(100, 2.0, "short", 0.3), 100.6)

    def test_bad_direction(self):
        with self.assertRaises(ValueError):
            sizing.stop_from_atr(100, 2.0, "sideways")

    def test_stop_width_warning(self):
        self.assertIsNotNone(sizing.stop_width_check(100, 80, 2.0))
        self.assertIsNone(sizing.stop_width_check(100, 98, 2.0))


class TestScaling(unittest.TestCase):
    def test_scale_out_splits(self):
        self.assertEqual(sizing.scale_out_plan(300, 3), [100, 100, 100])

    def test_scale_out_remainder(self):
        self.assertEqual(sizing.scale_out_plan(100, 3), [33, 33, 34])

    def test_scale_out_too_few_units(self):
        with self.assertRaises(ValueError):
            sizing.scale_out_plan(2, 3)

    def test_blended_r(self):
        # entry 100 stop 90, exits at 110 (1R) and 130 (3R), 50/50 -> 2R
        value = sizing.partial_exit_r(100, 90, [110, 130], [0.5, 0.5])
        self.assertAlmostEqual(value, 2.0)

    def test_fractions_must_sum_to_one(self):
        with self.assertRaises(ValueError):
            sizing.partial_exit_r(100, 90, [110, 130], [0.5, 0.6])


if __name__ == "__main__":
    unittest.main()
