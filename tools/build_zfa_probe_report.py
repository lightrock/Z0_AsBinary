"""Build the generated Z0/ZFA run-tape probe report."""

from __future__ import annotations

from pathlib import Path

from characteristic_impedance import (
    render_zfa_probe_html,
    render_zfa_probe_markdown,
    run_z0_zfa_probe,
)


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "docs" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    result = run_z0_zfa_probe(control_trials=256)
    (REPORT_DIR / "z0-zfa-run-tape-probe.md").write_text(
        render_zfa_probe_markdown(result),
        encoding="utf-8",
    )
    (REPORT_DIR / "z0-zfa-run-tape-probe.html").write_text(
        render_zfa_probe_html(result),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
