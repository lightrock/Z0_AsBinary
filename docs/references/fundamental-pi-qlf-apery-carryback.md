# Fundamental Pi: QLF Apéry Carryback

Status: cross-project receipt / Jim Whitescarver carryback from QLF Issue #98.

This note records Jim's response to the new `fundamentalPi.md` direction and keeps
the cross-project claim visible from the Z0_AsBinary side.

## What Jim preserved on the QLF side

Jim recorded `Z0_AsBinary` as another machine of this kind in QLF's
`Physical_Pi.md` §2, inside the list of machines as closure processes, and linked
back to the `fundamentalPi.md` discussion.

That matters because the Fundamental Pi thesis should not live only on the
Z0_AsBinary side. QLF is now carrying the same machine-facing question from its
own formal substrate side:

```text
stop worshiping the notation
find the machine / machines that generate the period receipts
```

## New QLF evidence: the same census hits ζ(3)

Jim's stronger update is that the same closure census

```text
C(2n,n)
```

that renders `π` also renders a second period, Apéry's constant:

```text
ζ(3) = (5/2) · ∑_{n≥1} (-1)^(n-1) / (n^3 · C(2n,n))
```

QLF now has this machine-verified in:

```text
lean/QLF_AperyPeriod.lean
```

The claim is that the finite rational partial sum is `Real.pi`-free, and each
term's central binomial is proven to be the substrate's own closure count via
`apery_summand_census`, reusing `closure_census`.

## Why this matters for Fundamental Pi

The important upgrade is not merely:

```text
π has a pretty series.
ζ(3) has a pretty series.
```

The important upgrade is:

```text
one closure census appears to generate multiple period receipts
```

Jim's framing:

```text
π
ζ(3)
Born statistics
P-vs-NP verify-filter
```

all land on one substrate machine: the ZFA closure census.

That supports the Fundamental Pi rule:

```text
A period carries no information its census does not already contain.
```

In Z0_AsBinary language:

```text
Do not ask the decimal to explain the machine.
Ask the closure census / recurrence / impedance-facing receipt what machine made
the decimal show up.
```

## Fixed-point / recurrence framing

The non-coincidence claim is the scale-step recurrence.

If the census obeys an exact recurrence, then the limit is not borrowed from
Stirling, Apéry, or later analytic naming. Those name the amplitude / public
limit. The recurrence supplies foundation-up convergence.

Project wording:

```text
closure census
-> exact scale-step recurrence
-> forced fixed point / limit behavior
-> period receipt
```

So the period is not treated as primitive. It is treated as the rendered receipt
of the census machine.

## Z0_AsBinary reading

Jim's reading of Z0_AsBinary is:

```text
Z0_AsBinary is the impedance-machine face of the same scale-free generator.
```

This should be held carefully. It is not yet proof that the `Z0` bit machine and
QLF's ZFA closure census are the same substrate machine. The defensible working
claim is:

```text
Z0_AsBinary may be exposing the impedance-facing receipt of a scale-free closure
generator whose QLF face is the ZFA closure census.
```

## Knock-on instruction for fundamentalPi.md

The next Fundamental Pi pass should carry this line back into the main note:

```text
The target is no longer only "derive π without importing Real.pi."
The target is to identify the closure census / scale-step recurrence that forces
period receipts such as π and ζ(3), then ask whether Z0_AsBinary is the
impedance-machine face of that same generator.
```

## Compact version

```text
Jim carried Z0_AsBinary into QLF's Physical_Pi.md as another closure-process
machine. QLF then strengthened the thesis: the same central-binomial closure
census C(2n,n) that renders π also renders ζ(3), through a Real.pi-free rational
partial-sum machine in QLF_AperyPeriod.lean. If the recurrence forces the limit,
then the period is not primitive information; it is the public receipt of the
closure census. Z0_AsBinary may be the impedance-machine face of that same
scale-free generator.
```
