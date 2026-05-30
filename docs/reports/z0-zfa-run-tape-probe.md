# Z0 QLF / Quantum OS Run-Tape Probe

This generated report runs the fixed pre-2019 Z0 bit seed as the
minimal circular-XOR process described in the legacy BigCalc2 notes:

```text
S_next = S XOR RotL1(S)
emit   = S_next[0]
```

It is a first scientific artifact, not a proof. The report separates the
runnable machine, the named token scans, and same-density shuffled
controls.

## Machine

- Seed bits: `101011110110110111000000110001011110101`
- Seed length: `39`
- Period: `4095`
- Tap index: `0`
- Tap-tape length: `4095`
- Tap-tape prefix: `100010010101001011011101010110101010000011100000100110000111100001101101110011001001010111011101`

## Known Forward Segmentation

| Segment | Bits | Length |
|---|---|---:|
| left edge | `10` | 2 |
| DOWN closure word | `10111101` | 8 |
| UP closure word | `101101` | 6 |
| STRANGE closure word | `1100000011` | 10 |
| central gluon gap | `000` | 3 |
| DOWN closure word | `10111101` | 8 |
| right edge | `01` | 2 |

## Circular Seed Hits

Positions are zero-based circular offsets inside each canonical Z0 orientation.

| Orientation | Token | Positions |
|---|---|---|
| forward | DOWN closure word | `2, 29` |
| forward | STRANGE closure word | `16` |
| forward | Q_CHARM | `-none-` |
| forward | Q_BOTTOM | `-none-` |
| forward | Q_TOP | `-none-` |
| forward | UP closure word | `7, 10, 36` |
| reverse | DOWN closure word | `2, 29` |
| reverse | STRANGE closure word | `13` |
| reverse | Q_CHARM | `-none-` |
| reverse | Q_BOTTOM | `-none-` |
| reverse | Q_TOP | `-none-` |
| reverse | UP closure word | `23, 26, 36` |
| inverse | DOWN closure word | `-none-` |
| inverse | STRANGE closure word | `-none-` |
| inverse | Q_CHARM | `-none-` |
| inverse | Q_BOTTOM | `-none-` |
| inverse | Q_TOP | `-none-` |
| inverse | UP closure word | `-none-` |
| inverse_reverse | DOWN closure word | `-none-` |
| inverse_reverse | STRANGE closure word | `-none-` |
| inverse_reverse | Q_CHARM | `-none-` |
| inverse_reverse | Q_BOTTOM | `-none-` |
| inverse_reverse | Q_TOP | `-none-` |
| inverse_reverse | UP closure word | `-none-` |

## Tap-Tape Token Hits

| Token | Bits | Length | Count | First positions |
|---|---|---:|---:|---|
| DOWN closure word | `10111101` | 8 | 18 | `154, 184, 489, 715, 1063, 1511, 1747, 1936, 2063, 2211, 2306, 2320, ...` |
| STRANGE closure word | `1100000011` | 10 | 4 | `426, 750, 1916, 2244` |
| Q_CHARM | `10011111011` | 11 | 1 | `3549` |
| Q_BOTTOM | `110100010` | 9 | 12 | `228, 438, 975, 1038, 1891, 2201, 2389, 2509, 3087, 3235, 3310, 3663` |
| Q_TOP | `11011000011` | 11 | 1 | `3105` |
| UP closure word high-noise short token | `101101` | 6 | 56 | `14, 25, 66, 113, 122, 151, 293, 311, 436, 502, 505, 514, ...` |

## Same-Density Shuffled Controls

Each control shuffles the 39 Z0 seed bits with the same one/zero density,
runs the same circular-XOR tap process for the same 4095 steps, and scans
the same token set. The empirical p column is `P(control >= observed)`
with a one-count smoothing term.

| Token | Observed | Control mean | Control min | Control max | Controls >= observed | Empirical p |
|---|---:|---:|---:|---:|---:|---:|
| DOWN closure word | 18 | 16.35 | 7 | 30 | 93/256 | 0.366 |
| STRANGE closure word | 4 | 3.83 | 0 | 10 | 129/256 | 0.506 |
| Q_CHARM | 1 | 2.04 | 0 | 6 | 225/256 | 0.879 |
| Q_BOTTOM | 12 | 8.13 | 1 | 15 | 29/256 | 0.117 |
| Q_TOP | 1 | 1.95 | 0 | 6 | 221/256 | 0.864 |
| UP closure word | 56 | 63.50 | 42 | 87 | 212/256 | 0.829 |

## Result

The Z0 run tape emits every priority word in this first token set at least
once during one closed 4095-step cycle. That is a real runnable-object
result worth preserving.

The same-density controls are the brake pedal: common closure words are not
surprising by count alone in a 4095-bit emitted tape. The stronger next
question is not raw occurrence. It is whether Z0-generated run fragments
compress official CODATA constants or legacy physics tokens better than
shuffled seeds, alternate constants, and fake same-length token catalogs.

## Declared Limits

- Catalog used: Z0 closure words plus selected legacy quark tokens only.
- Official CODATA constants are not decomposed in this report.
- Orientation transforms are used only for circular seed-hit accounting.
- Tap-tape scans are linear, overlapping substring scans.
- Controls preserve seed length and bit density but not every possible
  linear-feedback/cellular-automaton invariant.
