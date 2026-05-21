"""Core helpers for characteristic impedance information experiments."""

from __future__ import annotations

from dataclasses import dataclass
import math

MU_0_EXACT = 1.25663706212e-6
EPSILON_0_APPROX = 8.8541878128e-12
Z0_PRE_2019_DIGITS = "376730313461"
Z0_PRE_2019_BITS = "101011110110110111000000110001011110101"


def characteristic_impedance_vacuum(mu_0: float = MU_0_EXACT, epsilon_0: float = EPSILON_0_APPROX) -> float:
    """Return sqrt(mu_0 / epsilon_0), the vacuum characteristic impedance in ohms."""
    if mu_0 <= 0:
        raise ValueError("mu_0 must be positive")
    if epsilon_0 <= 0:
        raise ValueError("epsilon_0 must be positive")
    return math.sqrt(mu_0 / epsilon_0)


@dataclass(frozen=True)
class ConstantRecord:
    """Published constant represented as a significant-digit information object."""

    name: str
    digits: str
    units: str = ""
    provenance: str = ""

    @property
    def bits(self) -> str:
        return digits_to_bits(self.digits)


@dataclass(frozen=True)
class XorRunResult:
    """Result of circular XOR evolution for one binary seed."""

    seed: str
    period_steps: int
    halted: bool
    closed_loop: bool
    orbit: str


Z0_PRE_2019 = ConstantRecord(
    name="characteristic impedance of vacuum",
    digits=Z0_PRE_2019_DIGITS,
    units="ohm",
    provenance="pre-2019 CODATA significant digits from legacy BigCalc2 source",
)


def digits_to_bits(digits: str) -> str:
    """Convert published significant digits into a binary string."""
    cleaned = "".join(ch for ch in digits if ch.isdigit())
    if not cleaned:
        raise ValueError("digits must contain at least one decimal digit")
    return bin(int(cleaned))[2:]


def invert_bits(bits: str) -> str:
    """Swap 0 and 1 in a binary string."""
    _validate_bits(bits)
    return "".join("1" if ch == "0" else "0" for ch in bits)


def reverse_bits(bits: str) -> str:
    """Reverse a binary string."""
    _validate_bits(bits)
    return bits[::-1]


def orientations(bits: str) -> dict[str, str]:
    """Return forward, reverse, inverse, and inverse-reverse views."""
    _validate_bits(bits)
    inverse = invert_bits(bits)
    return {
        "forward": bits,
        "reverse": reverse_bits(bits),
        "inverse": inverse,
        "inverse_reverse": reverse_bits(inverse),
    }


def xor_ring_step(bits: str) -> str:
    """Apply one circular XOR evolution step to a binary seed."""
    _validate_bits(bits)
    if len(bits) == 1:
        return "0"
    return "".join("1" if bits[i] != bits[(i + 1) % len(bits)] else "0" for i in range(len(bits)))


def xor_ring_run(seed_bits: str, max_steps: int = 300_000, include_orbit: bool = False) -> XorRunResult:
    """Run circular XOR evolution until halt, closed loop, or max_steps."""
    _validate_bits(seed_bits)
    if max_steps <= 0:
        raise ValueError("max_steps must be positive")

    current = seed_bits
    orbit_parts: list[str] = []

    for step in range(1, max_steps + 1):
        current = xor_ring_step(current)
        if include_orbit:
            orbit_parts.append(current)
        if "1" not in current:
            return XorRunResult(seed_bits, step, True, False, "".join(orbit_parts))
        if current == seed_bits:
            return XorRunResult(seed_bits, step, False, True, "".join(orbit_parts))

    return XorRunResult(seed_bits, max_steps, False, False, "".join(orbit_parts))


def _validate_bits(bits: str) -> None:
    if not bits:
        raise ValueError("bits must not be empty")
    invalid = set(bits) - {"0", "1"}
    if invalid:
        raise ValueError("bits must contain only 0 and 1")
