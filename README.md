# Characteristic Impedance Python

Python-first successor project for characteristic impedance and related physics/numeric exploration.

This repository starts as a clean stub. The legacy C# / WinForms reference project is:

```text
E:\physics\bigcalc2
```

## Design posture

- Treat BigCalc2 as legacy reference material, not as a line-by-line port target.
- Prefer small, testable numerical modules over GUI-first implementation.
- Preserve units, assumptions, constants, and provenance for imported physics data.
- Keep notebooks, generated data, and UI experiments separate from core library code.

## Initial layout

- `src/characteristic_impedance/` - Python package.
- `tests/` - unit tests.
- `docs/` may be added when the first model boundary is clear.
