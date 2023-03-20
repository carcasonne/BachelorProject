import unittest

from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern


class Test_TabuShiftPattern(unittest.TestCase):

    def test_init_returns_correct_merged(self):
        p1 = [1, 1, 1, 0, 0, 0, 1]
        p2 = [0, 0, 0, 0, 0, 0, 0]
        expectedp1p2 = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        expectedp2p1 = [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        tspp1p2 = TabuShiftPattern(p1, p2)
        tspp2p1 = TabuShiftPattern(p2, p1)
        self.assertEqual(expectedp1p2, tspp1p2.merged)
        self.assertEqual(expectedp2p1, tspp2p1.merged)

    def test_day_shift_eq_day_shift_returns_true(self):
        tsp1 = TabuShiftPattern([1, 1, 1, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        tsp2 = TabuShiftPattern([1, 1, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(True, tsp1 == tsp2)

    def test_night_shift_eq_night_shift_returns_true(self):
        tsp1 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 1])
        tsp2 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 1, 0, 1])
        self.assertEqual(True, tsp1 == tsp2)

    def test_day_shift_eq_night_shift_returns_true(self):
        tsp1 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 1])
        tsp2 = TabuShiftPattern([1, 1, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(False, tsp1 == tsp2)


if __name__ == '__main__':
    unittest.main()
