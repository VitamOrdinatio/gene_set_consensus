# Evidence Semantics and Evidence Tiers

## Purpose

GSC distinguishes between:

```text
evidence semantics
```

and:

```text
evidence tier
```

These are related but fundamentally different concepts.

This distinction emerged during experimental GTR integration and semantic scoring analysis.

---

## Core Principle

### Evidence Semantics

Evidence semantics answer:

```
"What kind of evidence is this?"
```

Examples include:

- statistical association
- clinical utilization
- functional localization
- clinical interpretation
- exploratory literature support

Semantics describe the biological or translational meaning of the evidence.

---

### Evidence Tier

Evidence tiers answer:

```text
"How epistemically strong or reliable is this evidence?"
```

Tiers describe:

- confidence
- rigor
- reproducibility
- governance quality
- validation structure

Tier assignment is conceptually independent from semantic category, although some semantic classes may more commonly achieve certain tiers due to their underlying evidence structure.

---

## Orthogonality of Semantics and Tiers

Evidence semantics and evidence tiers form orthogonal axes.

For example:

| Source         | Evidence Semantics      | Evidence Tier |
| -------------- | ----------------------- | ------------- |
| Epi25          | statistical_association | platinum      |
| MitoCarta      | functional_localization | gold          |
| GTR            | clinical_utilization    | silver        |
| Genes4Epilepsy | exploratory_literature  | bronze        |

This distinction is critical because:

```text
different evidence types may carry different biological meanings
while simultaneously differing in confidence and rigor
```

---

## Evidence Semantics Categories

### statistical_association

Meaning:

- cohort-supported disease association
- burden testing
- case-control enrichment
- statistical genetics evidence

Examples:

- Epi25
- future cohort-scale genomic studies

---

### functional_localization

Meaning:

- subcellular localization
- pathway membership
- organelle association
- systems biology inference

Examples:

- MitoCarta
- future pathway localization resources

---

### clinical_utilization

Meaning:

- real-world diagnostic usage
- testing panel inclusion
- translational adoption

Examples:

- GTR-derived testing summaries

Important:

```text
clinical utilization does not imply disease causality
```

---

### clinical_interpretation

Meaning:

- variant interpretation activity
- clinical assertions
- curated pathogenicity interpretation

Examples:

- future ClinVar-derived overlays

---

### exploratory_literature

Meaning:

- literature-derived exploratory support
- smaller curated resources
- hypothesis-generating evidence

Examples:

- Genes4Epilepsy
- future exploratory overlays

---

## Evidence Tier Definitions

### Platinum

Characteristics:

- massive cohort scale
- stringent statistical conservatism
- highly reproducible
- direct disease-association evidence
- exceptional governance quality

Examples:

- Epi25 high-confidence loci

Platinum tier should remain rare.

---

### Gold

Characteristics:

- strong biological evidence
- multi-modal integration
- extensive validation
- high governance quality

Examples:

- MitoCarta

Gold evidence is highly valuable but may not directly represent disease association.

---

### Silver

Characteristics:

- clinically informative
- translationally meaningful
- moderate-to-high utility
- potentially confounded by workflow practices

Examples:

- GTR-derived testing utilization evidence

Silver evidence should be interpreted conservatively.

---

### Bronze

Characteristics:

- exploratory
- hypothesis-generating
- lower governance structure
- narrower provenance

Examples:

- Genes4Epilepsy

Bronze evidence remains scientifically useful but should not dominate scoring.

---

## Correlation Does Not Eliminate Semantic Distinction

Evidence channels may exhibit biological correlation.

Examples:

- clinically utilized genes may also be disease-associated
- mitochondrial localization may enrich mitochondrial disease association
- exploratory literature resources may overlap cohort-supported genes

However:

```text
correlation between evidence channels does not eliminate semantic distinction
```

GSC therefore preserves:

- evidence semantics
- evidence provenance
- evidence tiers

even when evidence sources overlap biologically.

---

## Scoring Implications

Simple additive scoring may incorrectly compress:

- semantics
- evidence rigor
- confidence structure

into a single scalar.

For example:

```text
bronze + silver = gold
```

may be mathematically valid while remaining biologically misleading.

This motivates future semantic-aware scoring systems.

See:

`docs/design/semantic_scoring_framework.md`

---

## Current Canonical Source Assignments

| Source         | Semantics               | Tier     |
| -------------- | ----------------------- | -------- |
| Epi25          | statistical_association | platinum |
| MitoCarta      | functional_localization | gold     |
| GTR            | clinical_utilization    | silver   |
| Genes4Epilepsy | exploratory_literature  | bronze   |

These assignments may evolve as:

- new evidence sources are added
- validation improves
- governance policies mature

---

## Strategic Summary

GSC treats:

- evidence semantics
- evidence tiers
- provenance
- ontology relationships

as independent but interacting governance dimensions.

This allows GSC to preserve:

- biological interpretability
- translational meaning
- scoring transparency
- deterministic reproducibility

while integrating heterogeneous evidence systems.

