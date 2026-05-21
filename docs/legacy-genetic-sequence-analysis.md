# Legacy Genetic Sequence Analysis

> Note: the companion HTML version, `legacy-genetic-sequence-analysis.html`, is much nicer looking when opened locally or through a static site. This Markdown version exists so GitHub users can read the document directly in the repository without landing in raw HTML source.

What the BigCalc2 “gene” machinery was trying to do: treat constants as circular tapes, ask whether one tape can spell another with very simple bit transforms, then ask whether the XOR-running Z0 tape emits useful words from the larger constants catalog.

Source files: `BigCalc2/GeneSequence.cs`, `GeneSequence2.cs`, `GeneSequence3.cs`, `GeneSequence4.cs`, `GeneSequence6.cs`, `GeneSequence7.cs`, plus generated CSV outputs in the legacy project.

## Core Interpretation

The old code was not merely searching for cute substrings. It was building a compression grammar over binary constants. Each published constant becomes a circular bit tape. Other constants become named tokens. The decomposer asks: how many literal bits remain if this source tape is spelled with known tokens under only simple transforms?

```text
constant bits -> circular tape
catalog constants -> token words
allowed transforms -> forward, reverse, inverse, inverse-reverse, rotation
score -> literal bits left + token penalty
```

In this language, “genetic sequence” means a recipe for expressing one constant as a small sequence of named bit-words from other constants.

## Algorithm Layers

| Layer | Legacy file | What it does |
|---|---|---|
| General decomposer | `GeneSequence.cs` | Builds token variants from the whole catalog, including F/R/I/IR and all rotations; uses Aho-Corasick plus dynamic programming to minimize literal bits. |
| Z0-restricted named tokens | `GeneSequence2.cs` | Allows only named catalog-token variants that also appear contiguously on the Z0 ring in some orientation. |
| Z0 facets | `GeneSequence3.cs` | Adds raw Z0 substrings as tokens, so Z0 itself becomes a substrate or alphabet of facets. |
| Number collider | `GeneSequence4.cs` | Tries small edits around a number: tail trims, zero pads, and tail-bit flips, then asks whether nearby values compress better against Z0 facets. |
| Ablation bench | `GeneSequence6.cs` | Compares observed decompositions against shuffled baselines and removes token classes to see what is carrying the signal. |
| Z0 run tape | `GeneSequence7.cs` | Runs `S = S XOR RotL1(S)`, emits one tapped bit per step, and scans the emitted tape for catalog patterns. |

## Direct Tape Compression

The first mode asks whether one constant can be expressed by other constant tokens on a circular tape. The output field `GeneString` is the proposed recipe.

```text
Source: characteristic impedance of vacuum
BitsLen: 39
BestOrientation: Reverse
LiteralsCost_Bits: 0
TokensUsed: 4
GeneString:
  {Q_DOWN|F|rot=0}
  {AME20 35Mg(p,n)35Al Q_cKeV|R|rot=3}
  {Q_DOWN|F|rot=0}
  {Q_38MeV|R|rot=4}
```

This says Z0 itself was found as a zero-literal recipe in named words under simple transforms. That is interesting, but by itself it is not the strongest evidence because a rich catalog can overfit.

## Z0 As Substrate

The Z0-facet mode is more radical. It lets raw contiguous substrings of the Z0 ring become available as tokens. Then it asks whether other constants can be spelled from pieces of Z0.

| Z0 facet output | Interpretation |
|---|---|
| `880` rows inspected. `877` had zero literal bits. `342` had zero literal bits using two tokens or fewer. | This is best read as “Z0 is an extremely permissive substring substrate” unless controlled carefully. It is powerful, but power alone is not proof. |

Example from the legacy output:

```text
weak mixing angle -> {Characteristic impedance of vacuum|F|rot=25}
                     {Characteristic impedance of vacuum|F|rot=1}

Q_UP              -> {Characteristic impedance of vacuum|F|rot=7}
Q_DOWN            -> {Characteristic impedance of vacuum|F|rot=2}
Q_STRANGE         -> {Characteristic impedance of vacuum|F|rot=16}
Q_CHARM           -> {Characteristic impedance of vacuum|I|rot=19}
```

## Ablation Result

The ablation output is the most honest legacy warning. For the AME proton-neutron threshold cohort:

| Pass | Count | Zero-literal | Mean literal bits |
|---|---:|---:|---:|
| Observed (Z0 + named) | 2222 | 71 | 6.78308 |
| Shuffle baseline (256x) | 568832 | 16192 | 6.86395 |
| Ablate Q_UP/Q_DOWN/Q_38MeV | 2222 | 71 | 6.78308 |
| Ablate Z0 facets (named only) | 2222 | 0 | 11.3474 |
| Z0 facets only | 2222 | 71 | 6.78308 |

> The ablation says the signal in that run is carried almost entirely by Z0 facets, not by the named quark tokens. That does not kill the idea. It tells the Python port to measure Z0-substrate power separately from quark-name interpretation.

## Z0 As Running Program

The run-tape mode is closest to the “simplest possible Turing tape” idea. Start with the Z0 seed. Each step replaces the state with its XOR against a one-bit rotation. Tap one emitted bit per step. The result is a generated tape.

```text
S_next = S XOR RotL1(S)
emit   = S_next[0]
```

This is a very small machine: one state string, one rotation, one XOR, one tap. The research question becomes:

```text
Does this running Z0 tape emit substrings that reconstruct other physical constants better than chance?
```

In the filtered legacy run output (`min token length > 20`):

| Measure | Value | Meaning |
|---|---:|---|
| rows | 115 | Filtered constants inspected. |
| anchored in run | 65 | Had at least one long token found at a concrete run position. |
| zero literal | 7 | Fully represented by run tokens under the current settings. |
| mean literal bits | 10.77 | Average leftover literal cost in the filtered output. |

This is the cleaner direction: not merely “Z0 contains substrings,” but “Z0, when run as a minimal machine, emits tape fragments that anchor other constants.”

## What Should Be Ported First

| Python module | Purpose |
|---|---|
| `tokens.py` | Named bit tokens, orientations, rotations, and labels. |
| `decompose.py` | Dynamic-programming decomposition with literal cost and token penalty. |
| `z0_substrate.py` | Z0 facet generation and strict substrate scoring. |
| `run_tape.py` | Minimal XOR running tape: seed, evolve, emit, scan. |
| `baselines.py` | Shuffles, random seeds, alternate constants, and unit/precision variants. |
| `reports.py` | Reproducible HTML summaries generated from Python outputs. |

## Porting Discipline

The old C# was an exploratory bench. The Python version should separate four questions that were blurred together:

| Question | Why separate it? |
|---|---|
| Does Z0 contain a target directly? | Substring containment is the weakest claim and needs strong baselines. |
| Can Z0 facets compress a target? | This measures substrate expressiveness, but can become too permissive. |
| Can named physical tokens compress a target? | This tests whether the recipe has semantic physics labels, not just bits. |
| Does a running Z0 tape emit target pieces? | This is the strongest “minimal program” hypothesis and should become the primary experiment. |

> Summary: the legacy “genetic sequence” machinery was a compression and generative-tape experiment. The next Python step should not be a GUI port. It should be a clean implementation of token decomposition plus Z0 run-tape scoring against adversarial controls.
