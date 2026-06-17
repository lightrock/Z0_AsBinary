# Closure-Register Machine

This is the next concrete low-level step after `docs/references/fundamentalPi.md`.
It does not try to derive three-dimensional space. It closes the smaller issue
first: phase and probability math should not begin with primitive pi, radians,
or geometry.

## Doctrine

Start with a finite closure machine:

```text
register state: k mod N
cycle fraction: k / N
full closure:   k == 0 mod N
half closure:   k == N/2 mod N, when N is even
readout:        return/interference receipt
```

The machine has no built-in circle, angle, radian, x/y/z direction, or stored
digits of pi. A full cycle is just a completed closure count. A half cycle is a
distinguished opposite register state when the count admits one.

Only later, for human rendering, may a caller map:

```text
full closure -> 2pi radians
half closure -> pi radians
```

That rendering is not the substrate. It is a report format.

## Probability-Amplitude Replacement

The primitive object is not `exp(i theta)` or `sin(theta)`. The lower-level
object is:

```text
state update
relation-channel selection
cycle accumulation
closure or non-closure
interference/readout
statistics over receipts
```

Probability summarizes repeated closure receipts. It should not be treated as a
free-floating primitive detached from the machine that generated the possible
outcomes.

## Relational Omnidirectionality

Before space, omnidirectional cannot mean no preferred x/y/z direction. There
are no x, y, or z labels yet.

The pre-spatial version is:

```text
no preferred eligible relation-neighbor
no preferred relation channel
no privileged node label
closure/readout statistics invariant under relabeling
```

The runnable test is label erasure:

```text
rename relation channels
run the same update schedule
compare the label-free closure readout
```

If the closure receipt is unchanged by relation-label permutation, the walk is
relationally omnidirectional in this limited sense. Spatial isotropy is a later
projection problem.

## Implementation Anchor

The code anchor is `src/characteristic_impedance/closure.py`.

It defines:

- `ClosureRegister`: `k mod N`, cycle fraction, full closure, half closure.
- `RelationClosureTrace`: a finite walk among relation channels, not positions.
- `run_relation_closure_trace`: a schedule runner whose label-free readout can
  be compared across relation-channel renamings.

The module deliberately does not import `math.pi`. If a future renderer wants
radians, it must be an explicit presentation layer over this lower-level
closure receipt.

## Physical Candidates Come After

After the abstract closure machine is clean, physical candidates can be attached
without smuggling pi into the substrate:

```text
h       action ledger for completed cycles
e       electromagnetic coupling token
h/e     charge-e flux/phase closure unit
h/(2e)  superconducting pair flux closure unit
2e/h    Josephson phase-clock conversion
h/e^2   quantum impedance
Z0      vacuum-side impedance
alpha   dimensionless coupling ratio
c       propagation relation
```

These are candidate carriers of closure, not proof that any decimal digit tape
stores pi.

## Boundary

This step intentionally leaves geometric pi unsolved. It only replaces
primitive pi in phase/amplitude bookkeeping with:

```text
relation swap
cycle state
closure count
return/interference readout
```

The later bridge remains:

```text
relational closure machine
-> boundary/sheet receipts
-> coarse-grained spatial reconstruction
-> circle/sphere geometry
```
