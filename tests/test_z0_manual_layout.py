"""Regression checks for the order-preserving 39-bit Z0 layout."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


Z0_DIGITS = 376_730_313_461
Z0_BITS = "101011110110110111000000110001011110101"
SEGMENTS = (
    "10",
    "10111101",
    "101101",
    "1100000011",
    "000",
    "10111101",
    "01",
)
VISUAL_LAYOUT = """\
        1 0

101      11      101
101              101
110    0 0 0 0    011
         0 0 0
101      11      101

         0 1
"""


def bits_only(text: str) -> str:
    """Return only binary digits from a formatted layout."""

    return "".join(re.findall(r"[01]", text))


class Z0ManualLayoutTests(unittest.TestCase):
    def test_decimal_value_produces_the_preserved_39_bit_seed(self) -> None:
        self.assertEqual(format(Z0_DIGITS, "b"), Z0_BITS)
        self.assertEqual(len(Z0_BITS), 39)

    def test_whole_word_segments_are_exact_and_order_preserving(self) -> None:
        self.assertEqual("".join(SEGMENTS), Z0_BITS)
        self.assertEqual(sum(map(len, SEGMENTS)), 39)

    def test_visual_layout_is_the_same_39_bit_object(self) -> None:
        self.assertEqual(bits_only(VISUAL_LAYOUT), Z0_BITS)
        self.assertEqual(len(bits_only(VISUAL_LAYOUT)), 39)

    def test_down_rows_use_two_center_bits_not_three(self) -> None:
        self.assertEqual(SEGMENTS[1], "101" + "11" + "101")
        self.assertEqual(SEGMENTS[5], "101" + "11" + "101")
        self.assertNotEqual(SEGMENTS[1], "101" + "111" + "101")

    def test_published_docs_contain_the_corrected_layout(self) -> None:
        root = Path(__file__).resolve().parents[1]
        markdown = (root / "docs" / "z0-binary-structure.md").read_text(encoding="utf-8")
        html = (root / "docs" / "z0-binary-structure.html").read_text(encoding="utf-8")

        corrected_row = "101      11      101"
        incorrect_row = "101     111     101"

        self.assertGreaterEqual(markdown.count(corrected_row), 2)
        self.assertGreaterEqual(html.count(corrected_row), 2)
        self.assertNotIn(incorrect_row, markdown)
        self.assertNotIn(incorrect_row, html)


if __name__ == "__main__":
    unittest.main()
