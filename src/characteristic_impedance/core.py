"""Core physics helpers for the Python successor project."""

from __future__ import annotations

import math

MU_0_EXACT = 1.25663706212e-6
EPSILON_0_APPROX = 8.8541878128e-12


def characteristic_impedance_vacuum(mu_0: float = MU_0_EXACT, epsilon_0: float = EPSILON_0_APPROX) -> float:
    """Return sqrt(mu_0 / epsilon_0), the vacuum characteristic impedance in ohms."""
    if mu_0 <= 0:
        raise ValueError("mu_0 must be positive")
    if epsilon_0 <= 0:
        raise ValueError("epsilon_0 must be positive")
    return math.sqrt(mu_0 / epsilon_0)
