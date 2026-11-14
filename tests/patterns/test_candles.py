import unittest

from trading_intel import patterns as p

from tests.support import synthetic


def build(rows):
    """rows = [(open, high, low, close), ...]"""
    o = [r[0] for r in rows]
    h = [r[1] for r in rows]
    l = [r[2] for r in rows]
    c = [r[3] for r in rows]
    return o, h, l, c


def context_down(count=25, start=150.0):
    """``count`` falling bars, enough for the 20-bar prior-trend test."""
    return [(start - i, start + 1 - i, start - 1.5 - i, start - 1 - i) for i in range(count)]


def context_up(count=25, start=100.0):
    return [(start + i, start + 1.5 + i, start - 0.5 + i, start + 1 + i) for i in range(count)]


class TestHammer(unittest.TestCase):
    def test_hammer_in_downtrend_confirms(self):
        rows = context_down()
        last_close = rows[-1][3]
        # small body at the top, long lower shadow, tiny upper shadow
        rows.append((last_close, last_close + 0.3, last_close - 5.0, last_close + 0.1))
        o, h, l, c = build(rows)
        det = p.detect_hammer(o, h, l, c)
        self.assertEqual(len(det), 1)
        self.assertEqual(det.last.status, p.STATUS_CONFIRMED)
        self.assertEqual(det.last.direction, "bullish")

    def test_hammer_shape_without_downtrend_is_only_possible(self):
        rows = context_up()
        last_close = rows[-1][3]
        rows.append((last_close, last_close + 0.3, last_close - 5.0, last_close + 0.1))
        o, h, l, c = build(rows)
        det = p.detect_hammer(o, h, l, c)
        self.assertEqual(det.last.status, p.STATUS_POSSIBLE)
        self.assertTrue(any("prior trend" in f for f in det.last.rules_failed))

    def test_large_body_is_not_a_hammer(self):
        rows = context_down()
        last_close = rows[-1][3]
        # body is 5.5 of a 7.5 range -> far too large to be a hammer
        rows.append((last_close - 2.5, last_close + 2.0, last_close - 5.0, last_close + 3.0))
        o, h, l, c = build(rows)
        self.assertEqual(len(p.detect_hammer(o, h, l, c)), 0)


class TestEngulfing(unittest.TestCase):
    def test_bullish_engulfing(self):
        rows = context_down()
        base = rows[-1][3]
        rows.append((base, base + 0.2, base - 1.5, base - 1.2))        # bearish small
        rows.append((base - 1.4, base + 1.8, base - 1.6, base + 1.6))  # bullish, engulfs
        o, h, l, c = build(rows)
        det = p.detect_bullish_engulfing(o, h, l, c)
        self.assertEqual(len(det), 1)
        self.assertEqual(det.last.direction, "bullish")

    def test_bearish_engulfing(self):
        rows = context_up()
        base = rows[-1][3]
        rows.append((base - 1.2, base + 0.3, base - 1.4, base + 0.2))
        rows.append((base + 0.4, base + 0.6, base - 2.0, base - 1.8))
        o, h, l, c = build(rows)
        det = p.detect_bearish_engulfing(o, h, l, c)
        self.assertEqual(len(det), 1)
        self.assertEqual(det.last.direction, "bearish")

    def test_no_engulf_when_body_inside(self):
        rows = context_down()
        base = rows[-1][3]
        rows.append((base, base + 0.2, base - 1.5, base - 1.2))
        rows.append((base - 1.0, base - 0.8, base - 1.6, base - 0.9))  # does not engulf
        o, h, l, c = build(rows)
        self.assertEqual(len(p.detect_bullish_engulfing(o, h, l, c)), 0)


class TestStars(unittest.TestCase):
    def test_morning_star(self):
        rows = [(110, 110.5, 108, 108.2), (108.0, 108.2, 106.0, 106.2)]
        rows.append((104.5, 104.8, 103.8, 104.2))       # small star body, gapped down
        rows.append((105.0, 108.5, 104.9, 108.3))       # closes above bar-1 midpoint (109.1? no)
        o, h, l, c = build(rows)
        # midpoint of bar 1 is (110+108.2)/2 = 109.1, so this close must exceed it
        rows[-1] = (105.0, 109.6, 104.9, 109.4)
        o, h, l, c = build(rows)
        det = p.detect_morning_star(o, h, l, c)
        self.assertEqual(len(det), 1)
        self.assertEqual(det.last.direction, "bullish")

    def test_three_white_soldiers(self):
        rows = [(100, 100.2, 99.8, 100.0)]
        rows += [(100.2, 102.2, 100.1, 102.0), (102.1, 104.1, 102.0, 104.0),
                 (104.1, 106.1, 104.0, 106.0)]
        o, h, l, c = build(rows)
        det = p.detect_three_white_soldiers(o, h, l, c)
        self.assertEqual(len(det), 1)
        self.assertEqual(det.last.direction, "bullish")

    def test_three_black_crows(self):
        rows = [(110, 110.2, 109.8, 110.0)]
        rows += [(109.9, 110.0, 108.0, 108.1), (108.0, 108.1, 106.0, 106.1),
                 (106.0, 106.1, 104.0, 104.1)]
        o, h, l, c = build(rows)
        det = p.detect_three_black_crows(o, h, l, c)
        self.assertEqual(len(det), 1)
        self.assertEqual(det.last.direction, "bearish")


class TestDojiAndMarubozu(unittest.TestCase):
    def test_doji(self):
        o, h, l, c = [100.0], [102.0], [98.0], [100.1]
        det = p.detect_doji(o, h, l, c)
        self.assertEqual(len(det), 1)

    def test_marubozu(self):
        o, h, l, c = [100.0], [105.1], [99.9], [105.0]
        det = p.detect_marubozu(o, h, l, c)
        self.assertEqual(len(det), 1)
        self.assertEqual(det.last.direction, "bullish")

    def test_not_marubozu_with_shadows(self):
        o, h, l, c = [100.0], [108.0], [97.0], [105.0]
        self.assertEqual(len(p.detect_marubozu(o, h, l, c)), 0)


class TestRegistry(unittest.TestCase):
    def test_all_detectors_run(self):
        data = synthetic(200, seed=12)
        results = p.detect_all(data["open"], data["high"], data["low"], data["close"], data["volume"])
        self.assertEqual(len(results), len(p.DETECTORS))
        self.assertGreaterEqual(len(p.DETECTORS), 20)

    def test_detector_names_are_unique(self):
        self.assertEqual(len(set(p.DETECTORS)), len(p.DETECTORS))

    def test_every_hit_has_a_status(self):
        data = synthetic(200, seed=12)
        results = p.detect_all(data["open"], data["high"], data["low"], data["close"], data["volume"])
        valid = {p.STATUS_CONFIRMED, p.STATUS_DEVELOPING, p.STATUS_POSSIBLE, p.STATUS_UNCLEAR}
        for det in results.values():
            for hit in det.hits:
                self.assertIn(hit.status, valid)

    def test_empty_input_is_safe(self):
        results = p.detect_all([], [], [], [])
        self.assertTrue(all(len(d.hits) == 0 for d in results.values()))

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            p.detect_all([1, 2], [1], [1, 2], [1, 2])


class TestTrendClassifier(unittest.TestCase):
    def test_up(self):
        closes = [100 + i for i in range(30)]
        self.assertEqual(p.classify_trend(closes, 29, 20), "up")

    def test_down(self):
        closes = [130 - i for i in range(30)]
        self.assertEqual(p.classify_trend(closes, 29, 20), "down")

    def test_flat(self):
        self.assertEqual(p.classify_trend([100.0] * 30, 29, 20), "flat")

    def test_unknown_when_short(self):
        self.assertEqual(p.classify_trend([100, 101], 1, 20), "unknown")


if __name__ == "__main__":
    unittest.main()
