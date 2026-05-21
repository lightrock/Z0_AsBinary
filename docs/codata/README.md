# CODATA Evidence Chain

This folder preserves the pre-2019 CODATA working source and the derived binary forms used by the project.

## Files

- `pre-2019-codata-2014-source.md` — named/value/unit source table.
- `pre-2019-codata-2014-binary.md` — same row order, with significant digits and binary form.
- `pre-2019-codata-2014-bits-only.txt` — one line of bits per source row, no names, no units, no comments.

## Conversion rule

The project's binary conversion uses the published value mantissa only.

```text
376.730 313 461...     -> 376730313461 -> binary
6.626 070 040 e-34     -> 6626070040   -> binary
299 792 458            -> 299792458    -> binary
```

Ignored during conversion:

- sign
- decimal point
- digit-grouping spaces
- ellipsis
- uncertainty
- unit
- exponent marker such as `e-34`

That is deliberate. The point is to test the significant-digit information object, not the engineering scale factor.

## Rebuild

From the repo root:

```bash
python tools/codata/build_codata_docs.py
```

Optional official-source fetch step:

```bash
python tools/codata/fetch_nist_2014_ascii.py
```

The fetch step downloads the official NIST 2014 all-values ASCII file into `data/codata/raw/`. Review and normalize that file into the Markdown source table before rebuilding generated binary files.
