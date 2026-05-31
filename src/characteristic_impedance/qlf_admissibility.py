"""First-pass QLF/ZFA admissibility layer.

This module deliberately separates generated bit observations from interpreted
candidate objects. A tap tape window can be turned into a QLF/ZFA candidate, but
it is admissible only when positive/action and negative/lift twists balance.
"""

from __future__ import annotations

from dataclasses import dataclass

from .core import Z0_PRE_2019_BITS, xor_ring_run
from .zfa import z0_tap_tape


POSITIVE_TWISTS = ("^", ">", "/", "+")
NEGATIVE_TWISTS = ("v", "<", "\\", "-")
BALANCED_BIT_TWIST_PAIRS = {
    "0": "^v",
    "1": "+-",
}


@dataclass(frozen=True)
class QlfCandidate:
    """Candidate interpreted process/capability/proof-like twist object."""

    name: str
    bits: str
    twists: str
    source: str


@dataclass(frozen=True)
class QlfAdmissibility:
    """Admissibility decision for one candidate under twist balance."""

    candidate: QlfCandidate
    positive_count: int
    negative_count: int
    spectral_gap: int
    admissible: bool


@dataclass(frozen=True)
class QlfAdmissibilityReport:
    """First-pass admissibility report over deterministic Z0 tap-tape windows."""

    seed_bits: str
    period_steps: int
    tap_index: int
    candidates: tuple[QlfAdmissibility, ...]


def twist_polarity(twist: str) -> int:
    """Return +1 for action/positive twists, -1 for lift/negative twists."""
    if twist in POSITIVE_TWISTS:
        return 1
    if twist in NEGATIVE_TWISTS:
        return -1
    raise ValueError(f"unknown twist symbol: {twist!r}")


def spectral_gap(twists: str) -> int:
    """Return positive_count - negative_count."""
    return sum(twist_polarity(twist) for twist in twists)


def evaluate_candidate(candidate: QlfCandidate) -> QlfAdmissibility:
    """Evaluate whether a candidate is ZFA-admissible under twist balance."""
    gap = spectral_gap(candidate.twists)
    positive_count = sum(1 for twist in candidate.twists if twist_polarity(twist) == 1)
    negative_count = len(candidate.twists) - positive_count
    return QlfAdmissibility(
        candidate=candidate,
        positive_count=positive_count,
        negative_count=negative_count,
        spectral_gap=gap,
        admissible=gap == 0,
    )


def bits_to_balanced_twists(bits: str) -> str:
    """Map each bit to a balanced twist pair. This is a safe embedding, not a discovery claim."""
    _validate_bits(bits)
    return "".join(BALANCED_BIT_TWIST_PAIRS[bit] for bit in bits)


def bits_to_window_candidate(name: str, bits: str, source: str = "") -> QlfCandidate:
    """Map a bit word into a candidate twist sequence that may be balanced or unbalanced.

    This windowed mapping is intentionally lossy: each bit becomes one twist,
    with `1` selecting from action/positive symbols and `0` selecting from
    lift/negative symbols by position. It creates an inspectable balance test
    without making every candidate automatically admissible.
    """
    _validate_bits(bits)
    twists = "".join(
        POSITIVE_TWISTS[index % len(POSITIVE_TWISTS)]
        if bit == "1"
        else NEGATIVE_TWISTS[index % len(NEGATIVE_TWISTS)]
        for index, bit in enumerate(bits)
    )
    return QlfCandidate(name=name, bits=bits, twists=twists, source=source)


def run_z0_qlf_admissibility_probe(
    tap_index: int = 0,
    window_size: int = 12,
    limit: int = 32,
) -> QlfAdmissibilityReport:
    """Evaluate deterministic Z0 tap-tape windows as QLF/ZFA candidates."""
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if limit <= 0:
        raise ValueError("limit must be positive")

    run = xor_ring_run(Z0_PRE_2019_BITS)
    tape = z0_tap_tape(Z0_PRE_2019_BITS, tap_index=tap_index, steps=run.period_steps)
    candidates: list[QlfAdmissibility] = []

    for candidate_index in range(limit):
        start = candidate_index * window_size
        end = start + window_size
        if end > len(tape):
            break
        bits = tape[start:end]
        candidate = bits_to_window_candidate(
            name=f"z0_tap{tap_index}_window_{candidate_index:04d}",
            bits=bits,
            source=f"Z0 tap tape bits {start}:{end}",
        )
        candidates.append(evaluate_candidate(candidate))

    return QlfAdmissibilityReport(
        seed_bits=Z0_PRE_2019_BITS,
        period_steps=run.period_steps,
        tap_index=tap_index,
        candidates=tuple(candidates),
    )


def render_qlf_admissibility_markdown(report: QlfAdmissibilityReport) -> str:
    """Render a Markdown report for the QLF/ZFA admissibility layer."""
    admissible_count = sum(1 for result in report.candidates if result.admissible)
    lines = [
        "# Z0 QLF / ZFA Admissibility Probe",
        "",
        "This is not a proof. It does not validate a physics claim or establish",
        "Jim Scarver's framework experimentally.",
        "",
        "This layer separates generated bits from candidate QLF/ZFA admissibility:",
        "the XOR orbit is the generated substrate, tap-tape windows are generated",
        "observation streams, named bit tokens are observed words, and QLF/ZFA",
        "candidate objects are interpreted process/capability/proof-like",
        "structures.",
        "",
        "A candidate is admissible only when positive/action and negative/lift",
        "twists balance to spectral gap zero. Unbalanced candidates are not bad",
        "strings; they are non-admissible under this interpretation.",
        "",
        "## Probe Settings",
        "",
        f"- Seed bits: `{report.seed_bits}`",
        f"- Period: `{report.period_steps}`",
        f"- Tap index: `{report.tap_index}`",
        f"- Candidate windows: `{len(report.candidates)}`",
        f"- Admissible windows: `{admissible_count}`",
        "",
        "## Candidate Windows",
        "",
        "| Candidate | Bits | Twists | Positive | Negative | Spectral gap | Admissible |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for result in report.candidates:
        lines.append(
            f"| {result.candidate.name} | `{result.candidate.bits}` | `{result.candidate.twists}` | "
            f"{result.positive_count} | {result.negative_count} | {result.spectral_gap} | "
            f"{'yes' if result.admissible else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Next Scientific Step",
            "",
            "The serious next step is comparing admissible candidate rates and",
            "compression/reconstruction performance against alternate constants,",
            "same-density randomized controls, shuffled seeds, and fake token",
            "catalogs. This report only adds the admissibility scaffold.",
        ]
    )
    return "\n".join(lines) + "\n"


def _validate_bits(bits: str) -> None:
    if not bits:
        raise ValueError("bits must not be empty")
    invalid = set(bits) - {"0", "1"}
    if invalid:
        raise ValueError("bits must contain only 0 and 1")
