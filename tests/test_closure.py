import unittest
from fractions import Fraction

from characteristic_impedance import ClosureRegister, run_relation_closure_trace


class ClosureRegisterTests(unittest.TestCase):
    def test_register_reports_cycle_fraction_without_radians(self):
        register = ClosureRegister(modulus=8, state=2)

        self.assertEqual(register.cycle_fraction, Fraction(1, 4))
        self.assertFalse(register.full_closure)
        self.assertFalse(register.half_closure)

    def test_register_reports_half_and_full_closure(self):
        half = ClosureRegister(modulus=8, state=4)
        full = half.advance(4)

        self.assertTrue(half.half_closure)
        self.assertFalse(half.full_closure)
        self.assertTrue(full.full_closure)
        self.assertFalse(full.half_closure)

    def test_relation_readout_is_stable_under_channel_relabeling(self):
        schedule = (0, 2, 1, 2, 0, 1, 2, 0)
        first = run_relation_closure_trace(
            ("red", "green", "blue"),
            schedule,
            modulus=4,
        )
        relabeled = run_relation_closure_trace(
            ("charge", "delay", "flux"),
            schedule,
            modulus=4,
        )

        self.assertEqual(first.label_free_readout, relabeled.label_free_readout)
        self.assertEqual(first.full_closure_count, 2)
        self.assertEqual(first.half_closure_count, 2)

    def test_relation_schedule_rejects_spurious_channel_index(self):
        with self.assertRaises(ValueError):
            run_relation_closure_trace(("a", "b"), (0, 2), modulus=3)


if __name__ == "__main__":
    unittest.main()
