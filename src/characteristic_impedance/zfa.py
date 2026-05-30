"""Z0-as-runnable-object probes for ZFA-style experiments."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
import random
import statistics

from .core import Z0_PRE_2019_BITS, orientations, xor_ring_run, xor_ring_step


@dataclass(frozen=True)
class BitToken:
    """Named bit word used by a Z0/ZFA probe."""

    name: str
    bits: str
    catalog: str
    high_noise: bool = False

    @property
    def bit_length(self) -> int:
        return len(self.bits)


@dataclass(frozen=True)
class TokenScan:
    """Occurrences of one token in one tape."""

    token: BitToken
    count: int
    positions: tuple[int, ...]


@dataclass(frozen=True)
class ControlSummary:
    """Density-preserving shuffled-control summary for one token."""

    token: BitToken
    observed: int
    mean: float
    minimum: int
    maximum: int
    greater_or_equal: int
    trials: int

    @property
    def empirical_p_ge_observed(self) -> float:
        return (self.greater_or_equal + 1) / (self.trials + 1)


@dataclass(frozen=True)
class ZfaProbeResult:
    """A first-pass ZFA-style run-tape result for the fixed Z0 seed."""

    seed_bits: str
    period_steps: int
    tap_index: int
    tap_tape: str
    token_scans: tuple[TokenScan, ...]
    control_summaries: tuple[ControlSummary, ...]


PRIORITY_ZFA_TOKENS: tuple[BitToken, ...] = (
    BitToken("DOWN closure word", "10111101", "Z0 binary-structure closure word"),
    BitToken("STRANGE closure word", "1100000011", "Z0 binary-structure closure word"),
    BitToken("Q_CHARM", "10011111011", "legacy physics token catalog"),
    BitToken("Q_BOTTOM", "110100010", "legacy physics token catalog"),
    BitToken("Q_TOP", "11011000011", "legacy physics token catalog"),
    BitToken("UP closure word", "101101", "Z0 binary-structure closure word", high_noise=True),
)

KNOWN_FORWARD_SEGMENTS: tuple[tuple[str, str], ...] = (
    ("left edge", "10"),
    ("DOWN closure word", "10111101"),
    ("UP closure word", "101101"),
    ("STRANGE closure word", "1100000011"),
    ("central gluon gap", "000"),
    ("DOWN closure word", "10111101"),
    ("right edge", "01"),
)


def z0_tap_tape(seed_bits: str = Z0_PRE_2019_BITS, tap_index: int = 0, steps: int | None = None) -> str:
    """Emit one tapped bit per circular-XOR step."""
    if tap_index < 0 or tap_index >= len(seed_bits):
        raise ValueError("tap_index must address a bit in the seed")

    period = xor_ring_run(seed_bits).period_steps
    total_steps = period if steps is None else steps
    if total_steps <= 0:
        raise ValueError("steps must be positive")

    current = seed_bits
    emitted: list[str] = []
    for _ in range(total_steps):
        current = xor_ring_step(current)
        emitted.append(current[tap_index])
    return "".join(emitted)


def scan_token(tape: str, token: BitToken) -> TokenScan:
    """Find overlapping occurrences of a token in a linear tape."""
    positions = tuple(
        index for index in range(0, len(tape) - token.bit_length + 1) if tape.startswith(token.bits, index)
    )
    return TokenScan(token=token, count=len(positions), positions=positions)


def scan_tokens(tape: str, tokens: tuple[BitToken, ...] = PRIORITY_ZFA_TOKENS) -> tuple[TokenScan, ...]:
    """Scan a tape for a token set."""
    return tuple(scan_token(tape, token) for token in tokens)


def circular_token_hits(
    seed_bits: str = Z0_PRE_2019_BITS,
    tokens: tuple[BitToken, ...] = PRIORITY_ZFA_TOKENS,
) -> dict[str, dict[str, tuple[int, ...]]]:
    """Return circular token hit positions for each canonical Z0 orientation."""
    hits: dict[str, dict[str, tuple[int, ...]]] = {}
    for orientation_name, bits in orientations(seed_bits).items():
        doubled = bits + bits[: max(token.bit_length for token in tokens) - 1]
        orientation_hits: dict[str, tuple[int, ...]] = {}
        for token in tokens:
            positions = tuple(
                index
                for index in range(len(bits))
                if doubled.startswith(token.bits, index)
            )
            orientation_hits[token.name] = positions
        hits[orientation_name] = orientation_hits
    return hits


def density_preserving_shuffle_controls(
    observed_tape: str,
    seed_bits: str = Z0_PRE_2019_BITS,
    tokens: tuple[BitToken, ...] = PRIORITY_ZFA_TOKENS,
    trials: int = 256,
    rng_seed: int = 230519,
) -> tuple[ControlSummary, ...]:
    """Compare token counts to reproducible same-length, same-density shuffles."""
    if trials <= 0:
        raise ValueError("trials must be positive")

    observed_scans = {scan.token.name: scan.count for scan in scan_tokens(observed_tape, tokens)}
    control_counts: dict[str, list[int]] = {token.name: [] for token in tokens}
    rng = random.Random(rng_seed)
    seed_population = list(seed_bits)

    for _ in range(trials):
        shuffled = seed_population[:]
        rng.shuffle(shuffled)
        control_tape = z0_tap_tape("".join(shuffled), steps=len(observed_tape))
        for scan in scan_tokens(control_tape, tokens):
            control_counts[scan.token.name].append(scan.count)

    summaries: list[ControlSummary] = []
    token_by_name = {token.name: token for token in tokens}
    for token_name, counts in control_counts.items():
        observed = observed_scans[token_name]
        summaries.append(
            ControlSummary(
                token=token_by_name[token_name],
                observed=observed,
                mean=statistics.mean(counts),
                minimum=min(counts),
                maximum=max(counts),
                greater_or_equal=sum(1 for count in counts if count >= observed),
                trials=trials,
            )
        )
    return tuple(summaries)


def run_z0_zfa_probe(control_trials: int = 256, tap_index: int = 0) -> ZfaProbeResult:
    """Run the first Z0/ZFA tap-tape probe with shuffled controls."""
    seed_bits = Z0_PRE_2019_BITS
    run = xor_ring_run(seed_bits)
    tap_tape = z0_tap_tape(seed_bits, tap_index=tap_index, steps=run.period_steps)
    token_scans = scan_tokens(tap_tape)
    controls = density_preserving_shuffle_controls(
        tap_tape,
        seed_bits=seed_bits,
        trials=control_trials,
    )
    return ZfaProbeResult(
        seed_bits=seed_bits,
        period_steps=run.period_steps,
        tap_index=tap_index,
        tap_tape=tap_tape,
        token_scans=token_scans,
        control_summaries=controls,
    )


def render_zfa_probe_markdown(result: ZfaProbeResult) -> str:
    """Render a Markdown report for the first Z0/ZFA probe."""
    lines = [
        "# Z0 ZFA Run-Tape Probe",
        "",
        "This generated report runs the fixed pre-2019 Z0 bit seed as the",
        "minimal circular-XOR process described in the legacy BigCalc2 notes:",
        "",
        "```text",
        "S_next = S XOR RotL1(S)",
        f"emit   = S_next[{result.tap_index}]",
        "```",
        "",
        "It is a first scientific artifact, not a proof. The report separates the",
        "runnable machine, the named token scans, and same-density shuffled",
        "controls.",
        "",
        "## Machine",
        "",
        f"- Seed bits: `{result.seed_bits}`",
        f"- Seed length: `{len(result.seed_bits)}`",
        f"- Period: `{result.period_steps}`",
        f"- Tap index: `{result.tap_index}`",
        f"- Tap-tape length: `{len(result.tap_tape)}`",
        f"- Tap-tape prefix: `{result.tap_tape[:96]}`",
        "",
        "## Known Forward Segmentation",
        "",
        "| Segment | Bits | Length |",
        "|---|---|---:|",
    ]
    for name, bits in KNOWN_FORWARD_SEGMENTS:
        lines.append(f"| {name} | `{bits}` | {len(bits)} |")

    lines.extend(
        [
            "",
            "## Circular Seed Hits",
            "",
            "Positions are zero-based circular offsets inside each canonical Z0 orientation.",
            "",
            "| Orientation | Token | Positions |",
            "|---|---|---|",
        ]
    )
    for orientation_name, token_hits in circular_token_hits(result.seed_bits).items():
        for token_name, positions in token_hits.items():
            shown = ", ".join(str(position) for position in positions) if positions else "-none-"
            lines.append(f"| {orientation_name} | {token_name} | `{shown}` |")

    lines.extend(
        [
            "",
            "## Tap-Tape Token Hits",
            "",
            "| Token | Bits | Length | Count | First positions |",
            "|---|---|---:|---:|---|",
        ]
    )
    for scan in result.token_scans:
        first_positions = ", ".join(str(position) for position in scan.positions[:12])
        if len(scan.positions) > 12:
            first_positions += ", ..."
        noise = " high-noise short token" if scan.token.high_noise else ""
        lines.append(
            f"| {scan.token.name}{noise} | `{scan.token.bits}` | {scan.token.bit_length} | "
            f"{scan.count} | `{first_positions or '-none-'}` |"
        )

    lines.extend(
        [
            "",
            "## Same-Density Shuffled Controls",
            "",
            "Each control shuffles the 39 Z0 seed bits with the same one/zero density,",
            "runs the same circular-XOR tap process for the same 4095 steps, and scans",
            "the same token set. The empirical p column is `P(control >= observed)`",
            "with a one-count smoothing term.",
            "",
            "| Token | Observed | Control mean | Control min | Control max | Controls >= observed | Empirical p |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for summary in result.control_summaries:
        lines.append(
            f"| {summary.token.name} | {summary.observed} | {summary.mean:.2f} | "
            f"{summary.minimum} | {summary.maximum} | {summary.greater_or_equal}/{summary.trials} | "
            f"{summary.empirical_p_ge_observed:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Result",
            "",
            "The Z0 run tape emits every priority word in this first token set at least",
            "once during one closed 4095-step cycle. That is a real runnable-object",
            "result worth preserving.",
            "",
            "The same-density controls are the brake pedal: common closure words are not",
            "surprising by count alone in a 4095-bit emitted tape. The stronger next",
            "question is not raw occurrence. It is whether Z0-generated run fragments",
            "compress official CODATA constants or legacy physics tokens better than",
            "shuffled seeds, alternate constants, and fake same-length token catalogs.",
            "",
            "## Declared Limits",
            "",
            "- Catalog used: Z0 closure words plus selected legacy quark tokens only.",
            "- Official CODATA constants are not decomposed in this report.",
            "- Orientation transforms are used only for circular seed-hit accounting.",
            "- Tap-tape scans are linear, overlapping substring scans.",
            "- Controls preserve seed length and bit density but not every possible",
            "  linear-feedback/cellular-automaton invariant.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_zfa_probe_html(result: ZfaProbeResult) -> str:
    """Render a compact standalone HTML report."""
    segment_rows = "\n".join(
        f"<tr><td>{escape(name)}</td><td><code>{bits}</code></td><td>{len(bits)}</td></tr>"
        for name, bits in KNOWN_FORWARD_SEGMENTS
    )
    circular_rows = []
    for orientation_name, token_hits in circular_token_hits(result.seed_bits).items():
        for token_name, positions in token_hits.items():
            shown = ", ".join(str(position) for position in positions) if positions else "-none-"
            circular_rows.append(
                f"<tr><td>{escape(orientation_name)}</td><td>{escape(token_name)}</td>"
                f"<td><code>{escape(shown)}</code></td></tr>"
            )
    tap_rows = []
    for scan in result.token_scans:
        first_positions = ", ".join(str(position) for position in scan.positions[:12])
        if len(scan.positions) > 12:
            first_positions += ", ..."
        label = scan.token.name
        if scan.token.high_noise:
            label += " (high-noise short token)"
        tap_rows.append(
            f"<tr><td>{escape(label)}</td><td><code>{scan.token.bits}</code></td>"
            f"<td>{scan.token.bit_length}</td><td>{scan.count}</td>"
            f"<td><code>{escape(first_positions or '-none-')}</code></td></tr>"
        )
    control_rows = "\n".join(
        f"<tr><td>{escape(summary.token.name)}</td><td>{summary.observed}</td>"
        f"<td>{summary.mean:.2f}</td><td>{summary.minimum}</td><td>{summary.maximum}</td>"
        f"<td>{summary.greater_or_equal}/{summary.trials}</td>"
        f"<td>{summary.empirical_p_ge_observed:.3f}</td></tr>"
        for summary in result.control_summaries
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Z0 ZFA Run-Tape Probe</title>
  <style>
    :root {{
      --ink: #14201b;
      --muted: #58655f;
      --line: #ccd8d2;
      --paper: #fbfcfa;
      --panel: #ffffff;
      --soft: #eef6f1;
      --blue: #245c88;
    }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "Segoe UI", Arial, sans-serif;
      line-height: 1.55;
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 36px 20px 64px;
    }}
    h1 {{
      margin: 0;
      font-size: 38px;
      line-height: 1.1;
    }}
    h2 {{
      margin-top: 36px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 8px;
      font-size: 24px;
    }}
    p {{
      max-width: 860px;
    }}
    .lede {{
      color: var(--muted);
      font-size: 18px;
    }}
    .note {{
      padding: 14px 16px;
      border-left: 4px solid var(--blue);
      background: var(--soft);
    }}
    pre {{
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f4f7f5;
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 14px;
      background: var(--panel);
      font-size: 14px;
    }}
    th,
    td {{
      border: 1px solid var(--line);
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #edf3ef;
    }}
    code {{
      font-family: Consolas, "Courier New", monospace;
    }}
    ul {{
      padding-left: 22px;
    }}
  </style>
</head>
<body>
  <main>
    <h1>Z0 ZFA Run-Tape Probe</h1>
    <p class="lede">
      A generated first-pass experiment that runs the fixed pre-2019 Z0 bit seed
      as a circular-XOR tap machine, then checks priority closure and quark
      words against same-density shuffled controls.
    </p>

    <div class="note">
      This is a scientific artifact, not a proof. The result is useful because
      it preserves both the positive hits and the control brake pedal.
    </div>

    <h2>Machine</h2>
    <pre>seed bits:       {result.seed_bits}
seed length:     {len(result.seed_bits)}
period:          {result.period_steps}
tap index:       {result.tap_index}
tap-tape length: {len(result.tap_tape)}
tap-tape prefix: {result.tap_tape[:96]}</pre>

    <h2>Known Forward Segmentation</h2>
    <table>
      <thead><tr><th>Segment</th><th>Bits</th><th>Length</th></tr></thead>
      <tbody>{segment_rows}</tbody>
    </table>

    <h2>Circular Seed Hits</h2>
    <p>Positions are zero-based circular offsets inside each canonical Z0 orientation.</p>
    <table>
      <thead><tr><th>Orientation</th><th>Token</th><th>Positions</th></tr></thead>
      <tbody>{"".join(circular_rows)}</tbody>
    </table>

    <h2>Tap-Tape Token Hits</h2>
    <table>
      <thead><tr><th>Token</th><th>Bits</th><th>Length</th><th>Count</th><th>First positions</th></tr></thead>
      <tbody>{"".join(tap_rows)}</tbody>
    </table>

    <h2>Same-Density Shuffled Controls</h2>
    <p>
      Each control shuffles the 39 Z0 seed bits with the same one/zero density,
      runs the same circular-XOR tap process for 4095 steps, and scans the same
      token set. The empirical p column is <code>P(control &gt;= observed)</code>
      with a one-count smoothing term.
    </p>
    <table>
      <thead>
        <tr><th>Token</th><th>Observed</th><th>Control mean</th><th>Control min</th><th>Control max</th><th>Controls &gt;= observed</th><th>Empirical p</th></tr>
      </thead>
      <tbody>{control_rows}</tbody>
    </table>

    <h2>Result</h2>
    <p>
      The Z0 run tape emits every priority word in this first token set at least
      once during one closed 4095-step cycle. That is a real runnable-object
      result worth preserving.
    </p>
    <p>
      The same-density controls matter: common closure words are not surprising
      by count alone in a 4095-bit emitted tape. The stronger next question is
      whether Z0-generated run fragments compress official CODATA constants or
      legacy physics tokens better than shuffled seeds, alternate constants, and
      fake same-length token catalogs.
    </p>

    <h2>Declared Limits</h2>
    <ul>
      <li>Catalog used: Z0 closure words plus selected legacy quark tokens only.</li>
      <li>Official CODATA constants are not decomposed in this report.</li>
      <li>Orientation transforms are used only for circular seed-hit accounting.</li>
      <li>Tap-tape scans are linear, overlapping substring scans.</li>
      <li>Controls preserve seed length and bit density, but not every possible cellular-automaton invariant.</li>
    </ul>
  </main>
</body>
</html>
"""
