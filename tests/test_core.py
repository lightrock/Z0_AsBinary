import unittest

from characteristic_impedance import characteristic_impedance_vacuum


class CharacteristicImpedanceTests(unittest.TestCase):
    def test_vacuum_impedance_is_near_expected_value(self):
        self.assertAlmostEqual(characteristic_impedance_vacuum(), 376.7303137, places=4)

    def test_rejects_nonpositive_inputs(self):
        with self.assertRaises(ValueError):
            characteristic_impedance_vacuum(mu_0=0)
        with self.assertRaises(ValueError):
            characteristic_impedance_vacuum(epsilon_0=0)


if __name__ == "__main__":
    unittest.main()
