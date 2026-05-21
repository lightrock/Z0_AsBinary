# Legacy Physics Token Catalog

This catalog preserves the non-CODATA rows that were appended to the legacy
BigCalc2 `NIST_CODATA.TXT` file for experimental convenience.

These rows are not official CODATA constants. In the legacy project, they were
deliberately placed beside the NIST constants so the same parsing, binary
conversion, search, run, and genetic-sequence machinery could treat quark and
hadron mass signatures like any other named bit token.

## Why This Exists

The current repository keeps two catalogs separate:

- `docs/codata/` contains the official pre-2019 CODATA 2014 evidence chain.
- `docs/tokens/legacy-physics-token-catalog.*` contains the legacy exploratory
  tokens that BigCalc2 appended after the official CODATA table.

That separation matters. The project should preserve the original evidence
trail without pretending that exploratory rows are official CODATA rows.

## Conversion Rule

The token conversion uses the same rule as the CODATA evidence chain:

```text
value mantissa -> remove sign, decimal point, spaces, exponent, unit -> integer -> binary
```

Examples:

```text
Q_UP      2.2   -> 22   -> 10110
Q_DOWN    4.7   -> 47   -> 101111
Q_STRANGE 96    -> 96   -> 1100000
Q_CHARM   1.275 -> 1275 -> 10011111011
```

## Primary Quark Mass-Signature Tokens

These are the core tokens behind the claim that quark words are already inside
the Z0 impedance structure.

| name | value | significant digits | bits | bit length | unit |
|---|---:|---:|---|---:|---|
| Q_UP | 2.2 | 22 | `10110` | 5 | MeV/c^2 |
| Q_DOWN | 4.7 | 47 | `101111` | 6 | MeV/c^2 |
| Q_STRANGE | 96 | 96 | `1100000` | 7 | MeV/c^2 |
| Q_CHARM | 1.275 | 1275 | `10011111011` | 11 | GeV/c^2 |
| Q_BOTTOM | 4.18 | 418 | `110100010` | 9 | GeV/c^2 |
| Q_TOP | 173.1 | 1731 | `11011000011` | 11 | GeV/c^2 |

## Full Legacy Token Table

The machine-readable CSV companion is:

```text
docs/tokens/legacy-physics-token-catalog.csv
```

| name | value | significant digits | bits | bit length | unit | legacy role |
|---|---:|---:|---|---:|---|---|
| `FIXED_PlanckTime` | 5.3911613 | 53911613 | `11001101101010000000111101` | 26 | s | legacy fixed Planck-time token |
| `Q_CesiumSecond` | 9192631770 | 9192631770 | `1000100011111011000110110111011010` | 34 | CesiumS | legacy time-standard token |
| `J/Psion3.096916` | 3.096916 | 3096916 | `1011110100000101010100` | 22 | GeV/c^2 | legacy hadron token |
| `Q_38MeV` | 38 | 38 | `100110` | 6 | MeV/c^2 | legacy low-energy mass token |
| `bbg10.061` | 10.061 | 10061 | `10011101001101` | 14 | GeV/c^2 | legacy mass token |
| `Q_UP` | 2.2 | 22 | `10110` | 5 | MeV/c^2 | quark mass-signature token |
| `Q_DOWN` | 4.7 | 47 | `101111` | 6 | MeV/c^2 | quark mass-signature token |
| `Q_STRANGE` | 96 | 96 | `1100000` | 7 | MeV/c^2 | quark mass-signature token |
| `Q_CHARM` | 1.275 | 1275 | `10011111011` | 11 | GeV/c^2 | quark mass-signature token |
| `Q_BOTTOM` | 4.18 | 418 | `110100010` | 9 | GeV/c^2 | quark mass-signature token |
| `Q_TOP` | 173.1 | 1731 | `11011000011` | 11 | GeV/c^2 | quark mass-signature token |
| `Q_TETRA` | 5568 | 5568 | `1010111000000` | 13 | MeV/c^2 | legacy tetraquark candidate token |
| `Q_Penta4380` | 4380 | 4380 | `1000100011100` | 13 | MeV/c^2 | legacy pentaquark candidate token |
| `Q_Penta4450` | 4450 | 4450 | `1000101100010` | 13 | MeV/c^2 | legacy pentaquark candidate token |
| `Q_sds` | 1321 | 1321 | `10100101001` | 11 | MeV/c^2 | legacy quark-composition token |
| `Q_dds` | 1197.3 | 11973 | `10111011000101` | 14 | MeV/c^2 | legacy quark-composition token |
| `Q_ddu` | 939.6 | 9396 | `10010010110100` | 14 | MeV/c^2 | legacy quark-composition token |
| `Q_dsu` | 1115.6 | 11156 | `10101110010100` | 14 | MeV/c^2 | legacy quark-composition token |
| `Q_dsu_2` | 1192.5 | 11925 | `10111010010101` | 14 | MeV/c^2 | legacy quark-composition token |
| `Q_ssu` | 1315 | 1315 | `10100100011` | 11 | MeV/c^2 | legacy quark-composition token |
| `Q_usu` | 1189.4 | 11894 | `10111001110110` | 14 | MeV/c^2 | legacy quark-composition token |
| `Q_udu` | 938.3 | 9383 | `10010010100111` | 14 | MeV/c^2 | legacy quark-composition token |
| `Q_u<d>` | 139.6 | 1396 | `10101110100` | 11 | MeV/c^2 | legacy meson/composition token |
| `Q_d<s>` | 497.7 | 4977 | `1001101110001` | 13 | MeV/c^2 | legacy meson/composition token |
| `Q_s<s>` | 547.8 | 5478 | `1010101100110` | 13 | MeV/c^2 | legacy meson/composition token |
| `Q_s<u>` | 493.7 | 4937 | `1001101001001` | 13 | MeV/c^2 | legacy meson/composition token |
| `Q_u<u>` | 135.0 | 1350 | `10101000110` | 11 | MeV/c^2 | legacy meson/composition token |
| `Q_s<s>2` | 957.6 | 9576 | `10010101101000` | 14 | MeV/c^2 | legacy meson/composition token |
| `Q_u<s>` | 493.7 | 4937 | `1001101001001` | 13 | MeV/c^2 | legacy meson/composition token |
| `Q_d<u>` | 193.6 | 1936 | `11110010000` | 11 | MeV/c^2 | legacy meson/composition token |
| `Q_s<d>` | 493.7 | 4937 | `1001101001001` | 13 | MeV/c^2 | legacy meson/composition token |
| `Q_udc` | 2286.46 | 228646 | `110111110100100110` | 18 | MeV/c^2 | legacy baryon/composition token |
| `Q_udb` | 5620.2 | 56202 | `1101101110001010` | 16 | MeV/c^2 | legacy baryon/composition token |
| `Q_89` | 89 | 89 | `1011001` | 7 | Ulla | legacy external-theory token |
| `Q_191` | 191 | 191 | `10111111` | 8 | Ulla | legacy external-theory token |
| `Q_383` | 383 | 383 | `101111111` | 9 | Ulla | legacy external-theory token |
| `Q_938` | 938 | 938 | `1110101010` | 10 | Ulla | legacy external-theory token |
| `Q_1836` | 1836 | 1836 | `11100101100` | 11 | Ulla | legacy external-theory token |
| `Q_1232` | 1232 | 1232 | `10011010000` | 11 | Ulla | legacy external-theory token |

## Chain Of Evidence

1. The original legacy source is `E:\physics\CharacteristicImpedanceLegacy\BigCalc2\NIST_CODATA.TXT`.
2. The official CODATA portion ends at `Wien wavelength displacement law constant`.
3. The rows after that point were appended by the legacy experiment as
   exploratory tokens.
4. This catalog preserves those appended rows separately so later code can join
   them intentionally with CODATA records when running legacy-style searches.
5. Future reports must state whether they used official CODATA only, legacy
   tokens only, or a combined catalog.
