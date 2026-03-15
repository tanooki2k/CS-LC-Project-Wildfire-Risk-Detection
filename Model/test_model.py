from unittest import TestCase, main
from Model.wildfire_risk import calculate_wildfire_risk


class TestModel(TestCase):
    def test_edge_case_low_risk(self):
        temp, moist = 0, True
        expected = "low"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)

    def test_low_risk_1(self):
        temp, moist = 22.5, True
        expected = "low"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)

    def test_low_risk_2(self):
        temp, moist = 17.5, True
        expected = "low"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)

    def test_edge_case_very_high_risk(self):
        temp, moist = 45, False
        expected = "very high"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)

    def test_edge_case_high_risk(self):
        temp, moist = 45, True
        expected = "high"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)

    def test_high_risk_1(self):
        temp, moist = 30, False
        expected = "high"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)

    def test_high_risk_2(self):
        temp, moist = 32.5, False
        expected = "high"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)

    def test_moderate_risk_1(self):
        temp, moist = 25, False
        expected = "moderate"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)

    def test_moderate_risk_2(self):
        temp, moist = 35, True
        expected = "moderate"
        result, _ = calculate_wildfire_risk(temp, moist)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    main()
