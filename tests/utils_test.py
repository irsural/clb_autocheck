import utils
import unittest


class AutoCalcPointsTest(unittest.TestCase):
    def test_common(self):
        self.assertEqual(utils.auto_calc_points(0, 6, 2), [6, 4, 2, 0])

    def test_common_negative(self):
        self.assertEqual(utils.auto_calc_points(-2, 2, 2), [2, 0, -2])

    def test_reverse(self):
        self.assertEqual(utils.auto_calc_points(2, -2, 2), [2, 0, -2])

    def test_reverse_negative(self):
        self.assertEqual(utils.auto_calc_points(6, 0, 2), [6, 4, 2, 0])

    def test_low_aliquant_start_low(self):
        self.assertEqual(utils.auto_calc_points(1, 6, 2), [6, 5, 3, 1])

    def test_low_aliquant_start_up(self):
        self.assertEqual(utils.auto_calc_points(6, 1, 2), [6, 4, 2, 1])

    def test_up_aliquant_start_low(self):
        self.assertEqual(utils.auto_calc_points(0, 5, 2), [5, 4, 2, 0])

    def test_up_aliquant_start_up(self):
        self.assertEqual(utils.auto_calc_points(5, 0, 2), [5, 3, 1, 0])

    def test_bad_input(self):
        self.assertEqual(utils.auto_calc_points(0, 0, 2), [])

    def test_bad_input_2(self):
        self.assertEqual(utils.auto_calc_points(0, 0, 0), [])


if __name__ == "__main__":
    unittest.main()
