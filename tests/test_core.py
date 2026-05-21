import unittest

from characteristic_impedance import (
    Z0_PRE_2019,
    Z0_PRE_2019_BITS,
    characteristic_impedance_vacuum,
    digits_to_bits,
    invert_bits,
    orientations,
    reverse_bits,
    xor_ring_run,
    xor_ring_step,
)


class CharacteristicImpedanceTests(unittest.TestCase):
    def test_vacuum_impedance_is_near_expected_value(self):
        self.assertAlmostEqual(characteristic_impedance_vacuum(), 376.7303137, places=4)

    def test_rejects_nonpositive_inputs(self):
        with self.assertRaises(ValueError):
            characteristic_impedance_vacuum(mu_0=0)
        with self.assertRaises(ValueError):
            characteristic_impedance_vacuum(epsilon_0=0)

    def test_z0_pre_2019_digits_encode_to_legacy_bits(self):
        self.assertEqual(Z0_PRE_2019.bits, Z0_PRE_2019_BITS)
        self.assertEqual(digits_to_bits("376.730 313 461"), Z0_PRE_2019_BITS)

    def test_bit_orientations(self):
        self.assertEqual(reverse_bits("10110"), "01101")
        self.assertEqual(invert_bits("10110"), "01001")
        self.assertEqual(
            orientations("10110"),
            {
                "forward": "10110",
                "reverse": "01101",
                "inverse": "01001",
                "inverse_reverse": "10010",
            },
        )

    def test_xor_ring_step(self):
        self.assertEqual(xor_ring_step("10110"), "11011")

    def test_z0_forward_seed_closes_legacy_loop(self):
        result = xor_ring_run(Z0_PRE_2019_BITS)
        self.assertTrue(result.closed_loop)
        self.assertFalse(result.halted)
        self.assertEqual(result.period_steps, 4095)


if __name__ == "__main__":
    unittest.main()
