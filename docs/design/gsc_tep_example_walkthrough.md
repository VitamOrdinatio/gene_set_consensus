# GSC-TEP Example Walkthrough

## Purpose

This document provides an illustrative example of GSC semantic-prior preservation during transport into VDB through a GSC-TEP.

This document is not:

* a schema
* a payload specification
* an implementation contract
* a database design

Instead, it demonstrates:

```text
What scientific meaning exists
inside a GSC semantic prior?

What must survive transport?

What information can evolve?

What information must never be discarded?
```

The goal is to provide an intuitive preservation target for DEX-GSC implementation planning.

---

# Example Semantic Prior

Assume GSC produces the following semantic prior.

## Phenotype

```text
epilepsy
```

## Gene

```text
SCN1A
```

## Contributing Sources

```text
EPI25
GTR
MitoCarta
```

## Semantic Channels

```text
Disease Association
Clinical Utilization
Functional Localization
```

## Consensus Score

```text
0.84
```

## Release

```text
epilepsy_gold_bronze_v0.1
```

---

# What Does This Mean?

Importantly:

The semantic prior is not:

```text
SCN1A is important.
```

The semantic prior is:

```text
Within the phenotype context of epilepsy,

SCN1A received semantic support from
multiple evidence sources,

aggregated through a defined scoring framework,

within a specific GSC release.
```

The semantic meaning is therefore much richer than:

```text
gene = SCN1A

score = 0.84
```

---

# What Must Survive Transport?

## Phenotype Context

Must survive:

```text
epilepsy
```

Why:

Without phenotype scope:

```text
SCN1A
```

becomes a phenotype-neutral statement.

The transported evidence would no longer answer:

```text
Relevant to what?
```

---

## Gene Identity

Must survive:

```text
SCN1A

source identifier

source namespace
```

Why:

Future namespace brokerage may assign:

```text
canonical_gene_id
```

but the original GSC-submitted identity must remain recoverable.

---

## Source Multiplicity

Must survive:

```text
EPI25
GTR
MitoCarta
```

Why:

A future investigator may wish to know:

```text
Why did SCN1A score highly?
```

Removing source attribution destroys that explanation.

---

## Semantic Channels

Must survive:

```text
Disease Association

Clinical Utilization

Functional Localization
```

Why:

These channels describe:

```text
what kind of support exists
```

not merely:

```text
how much support exists
```

This distinction is scientifically important.

---

## Consensus Score

Must survive:

```text
0.84
```

Why:

The score represents the aggregated output of the GSC framework.

However:

the score alone is insufficient.

It must remain attached to:

* phenotype context
* source attribution
* semantic channels
* scoring profile

---

## Release Identity

Must survive:

```text
epilepsy_gold_bronze_v0.1
```

Why:

Future releases may generate different outputs.

Without release identity:

historical reproducibility is impossible.

---

## Provenance

Must survive:

```text
source provenance

release provenance

scoring provenance

aggregation provenance
```

Why:

Future users must be able to answer:

```text
Where did this prior come from?
```

---

## Uncertainty

Must survive.

Example:

```text
unknown

unresolved

missing

ambiguous
```

must remain distinguishable.

Why:

Uncertainty is scientific information.

Its absence can lead to false certainty.

---

# What Can Change?

Some things may evolve after transport.

Examples:

## Canonical Identity Assignment

VDB may later determine:

```text
SCN1A
    →
canonical_gene_id
```

This is acceptable because:

```text
normalization is additive
```

The original identity remains preserved.

---

## New Query Surfaces

VDB may later expose:

```text
epilepsy overlays

gene-centric overlays

RDGP support surfaces
```

This does not alter the semantic prior.

It merely changes how it is discovered.

---

## Additional Relationships

Future repositories may attach:

```text
variant evidence

expression evidence

reasoning evidence
```

to the preserved GSC prior.

This extends the evidence ecosystem without altering GSC meaning.

---

# What Must Never Be Discarded?

The following represent irreversible scientific loss.

## Phenotype Scope

Never discard.

---

## Source Attribution

Never discard.

---

## Semantic Channels

Never discard.

---

## Release Identity

Never discard.

---

## Provenance

Never discard.

---

## Scoring Context

Never discard.

---

## Uncertainty

Never discard.

---

## Aggregation Topology

Never discard.

The existence of:

```text
SCN1A
```

is not the evidence.

The relationships that produced the SCN1A semantic prior are part of the evidence.

---

# Scientific Preservation Test

A future investigator examining this transported semantic prior should be able to answer:

1. Which phenotype was this prior associated with?
2. Which gene was evaluated?
3. Which GSC release produced it?
4. Which sources contributed?
5. Which semantic channels contributed?
6. What score was assigned?
7. What scoring profile was used?
8. What uncertainty existed?
9. What provenance supported the prior?
10. Why did the prior receive its support?

If any of these questions cannot be answered after transport, then scientifically meaningful information has been lost.

---

# Summary

The purpose of GSC-TEP is not merely to transport a score.

The purpose of GSC-TEP is to transport a phenotype-scoped semantic prior together with the context required to preserve its meaning, provenance, topology, uncertainty, and future interpretability.

Transport succeeds when future systems can still understand not only:

```text
what GSC concluded
```

but also:

```text
why GSC concluded it.
```
