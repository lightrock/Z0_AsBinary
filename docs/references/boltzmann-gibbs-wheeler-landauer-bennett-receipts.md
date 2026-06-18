# Boltzmann / Gibbs / Wheeler / Landauer / Bennett Receipts

## Status

This is a sober entropy-information-computation note for the Maxwell-completion /
closure-machine program.

It groups the missing information-physicality figures:

```text
Boltzmann -> microstate counting / entropy as multiplicity
Gibbs     -> ensemble entropy / probability distribution over states
Wheeler   -> yes/no question receipts / it-from-bit pressure
Landauer  -> information erasure has physical cost
Bennett   -> reversible computation and logical/thermodynamic distinction
```

Boltzmann is especially important here because he is the bridge from physical
state multiplicity to information entropy.

---

## Boltzmann: physical entropy as microstate multiplicity

Boltzmann's core receipt is:

```text
S = k log W
```

Through this lens:

```text
macrostate -> many compatible microstates
entropy -> log measure of compatible hidden arrangements
arrow of time -> typical motion from special states to more numerous states
```

This translates directly toward information entropy because the structure is
already about counting possibilities compatible with a description.

In repo language:

```text
visible receipt -> many possible hidden states
entropy -> how much state multiplicity is hidden behind the same visible surface
```

That is exactly the bridge to Shannon.

---

## Gibbs: ensemble / distribution receipt

Gibbs generalizes the statistical frame:

```text
state of knowledge / ensemble distribution -> entropy over possible states
```

Through this lens:

```text
not only one gas box
but probability distributions over states
```

This matters for controls:

```text
randomized bitstrings
shuffled catalogs
precision cuts
unit changes
null distributions
likelihood comparisons
```

Gibbs is the ancestor of treating a pattern as meaningful only against an
explicit ensemble.

---

## Boltzmann -> Shannon bridge

Shannon entropy is not thermodynamic entropy by default, but the mathematical
kinship is not accidental:

```text
Boltzmann/Gibbs -> count compatible physical state possibilities
Shannon         -> count uncertainty / information possibilities in messages
```

For `Z0_AsBinary`, this is crucial:

```text
a bit hit is not enough;
we need to know the ensemble of possible hits
```

Boltzmann/Gibbs provide the physical-statistical discipline behind Shannon-style
information hygiene.

---

## Wheeler: yes/no question receipt

Wheeler's useful pressure is:

```text
physical meaning may arise from yes/no acts of distinction
```

or in his compressed phrase:

```text
it from bit
```

For this repo, Wheeler is useful but dangerous.

Useful:

```text
binary distinctions may be physically serious
measurement/questions matter
observer-participancy and records cannot be ignored
```

Danger:

```text
information worship
mistaking yes/no payload for substrate
```

So Wheeler should always be paired with Shannon, Landauer, Zurek, and controls.

---

## Landauer: erasure has physical cost

Landauer makes information physical:

```text
erasing information has thermodynamic cost
```

This is a hard guardrail against treating bits as ghostly abstractions.

Machine receipt:

```text
logical operation -> physical process -> thermodynamic consequence
```

For this repo:

```text
if bits are doing work as selectors, triggers, or admissibility marks,
there must be a physical accounting layer
```

---

## Bennett: reversible computation receipt

Bennett clarifies that computation and dissipation are not the same thing.

```text
logical irreversibility -> thermodynamic cost
reversible computation -> computation can in principle avoid erasure cost until reset
```

That matters for closure-machine thinking:

```text
update can be reversible or irreversible
recording and erasure are distinct operations
return/period behavior may matter physically
```

---

## Combined receipt

Together:

```text
Boltzmann -> entropy as hidden physical multiplicity
Gibbs     -> ensemble/probability state discipline
Shannon   -> information uncertainty discipline
Wheeler   -> yes/no question pressure
Landauer  -> information operation has physical cost
Bennett   -> reversibility/erasure distinction
Zurek     -> stable records become objective through copying/witnessing
```

For Maxwell completion:

```text
records are physical,
information is disciplined,
entropy is state multiplicity,
erasure costs,
and bits cannot be worshiped as substrate without a running accounting machine
```

---

## Relation to Z0_AsBinary

The `Z0` bit pattern must be treated with this whole stack:

```text
Boltzmann/Gibbs -> compare against ensembles and multiplicities
Shannon         -> count information carefully
Wheeler         -> yes/no distinctions may matter
Landauer        -> bits as operations must have physical accounting
Bennett         -> update/reversal/erasure are different receipts
Zurek           -> hits and records require custody
```

This is why controls are not optional. A striking pattern is only a receipt after
its ensemble, cost, reversibility, record, and selection context are audited.

---

## One-line version

```text
Boltzmann and Gibbs translate physical entropy into state-multiplicity and ensemble
discipline; Wheeler, Landauer, and Bennett then force information to become a
physical yes/no, cost-bearing, reversible-or-irreversible process rather than
free-floating bit mysticism.
```

---

## References for context

- [Theory BBQ Lineup](theory-bbq-lineup.md)
- [Leibniz, Binary, Yin/Yang, and Process Receipts](leibniz-binary-yinyang-process-receipt.md)
- [Kitada / Dugić Local-Time Receipts](kitada-dugic-local-time-receipts.md)
- [Smolin Real-Time Receipts](smolin-real-time-receipts.md)
- Ludwig Boltzmann, statistical mechanics and entropy formula `S = k log W`.
- J. Willard Gibbs, ensemble methods and statistical mechanics.
- Claude Shannon, information entropy.
- John Archibald Wheeler, "It from bit" / yes-no question framing.
- Rolf Landauer, information erasure and physical cost.
- Charles Bennett, reversible computation.
