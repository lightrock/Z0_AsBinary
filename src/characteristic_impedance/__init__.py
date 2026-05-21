"""Python-first characteristic impedance helpers."""

from .core import (
    ConstantRecord,
    XorRunResult,
    Z0_PRE_2019,
    Z0_PRE_2019_BITS,
    Z0_PRE_2019_DIGITS,
    characteristic_impedance_vacuum,
    digits_to_bits,
    invert_bits,
    orientations,
    reverse_bits,
    xor_ring_run,
    xor_ring_step,
)

__all__ = [
    "ConstantRecord",
    "XorRunResult",
    "Z0_PRE_2019",
    "Z0_PRE_2019_BITS",
    "Z0_PRE_2019_DIGITS",
    "characteristic_impedance_vacuum",
    "digits_to_bits",
    "invert_bits",
    "orientations",
    "reverse_bits",
    "xor_ring_run",
    "xor_ring_step",
]
