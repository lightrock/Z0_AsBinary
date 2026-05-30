import unittest

from characteristic_impedance import (
    KNOWN_FORWARD_SEGMENTS,
    Z0_PRE_2019_BITS,
    circular_token_hits,
    render_zfa_probe_markdown,
    run_z0_zfa_probe,
    z0_tap_tape,
)


class ZfaProbeTests(unittest.TestCase):
    def test_known_forward_segments_reconstruct_z0(self):
        self.assertEqual("".join(bits for _name, bits in KNOWN_FORWARD_SEGMENTS), Z0_PRE_2019_BITS)

    def test_tap_tape_reproduces_known_prefix(self):
        tape = z0_tap_tape()
        self.assertEqual(len(tape), 4095)
        self.assertEqual(
            tape[:64],
            "1000100101010010110111010101101010100000111000001001100001111000",
        )

    def test_circular_seed_hits_preserve_forward_closure_positions(self):
        hits = circular_token_hits()
        self.assertEqual(hits["forward"]["DOWN closure word"], (2, 29))
        self.assertEqual(hits["forward"]["STRANGE closure word"], (16,))

    def test_zfa_probe_finds_priority_words_in_one_period(self):
        result = run_z0_zfa_probe(control_trials=8)
        counts = {scan.token.name: scan.count for scan in result.token_scans}
        self.assertGreaterEqual(counts["DOWN closure word"], 1)
        self.assertGreaterEqual(counts["STRANGE closure word"], 1)
        self.assertGreaterEqual(counts["Q_CHARM"], 1)
        self.assertGreaterEqual(counts["Q_BOTTOM"], 1)
        self.assertGreaterEqual(counts["Q_TOP"], 1)

    def test_markdown_report_declares_controls(self):
        result = run_z0_zfa_probe(control_trials=8)
        report = render_zfa_probe_markdown(result)
        self.assertIn("Same-Density Shuffled Controls", report)
        self.assertIn("Declared Limits", report)


if __name__ == "__main__":
    unittest.main()
