# GSC Evidence Tiering Framework

## Purpose

GSC integrates heterogeneous evidence sources into phenotype-scoped gene consensus sets.

Not all evidence sources carry equivalent biological or clinical meaning.

This document defines the conceptual interpretation framework for evidence tiering within GSC.

See also:

`docs/conventions/evidence_semantics_and_tiers.md`

for the formal distinction between:

- evidence semantics
- evidence confidence tiers
- semantic orthogonality

---

## Core Principle

Different evidence sources answer different scientific questions.

Examples:

| Source Type | Primary Question |
|---|---|
| Epi25 | statistically associated with disease? |
| MitoCarta | functionally localized to mitochondria? |
| GTR | utilized in real-world clinical testing? |
| ClinVar (future) | clinically interpreted variants reported? |
| Literature overlays | discussed in peer-reviewed publications? |

Therefore:

```text
evidence aggregation must preserve evidence semantics
```

rather than collapsing all evidence into a single undifferentiated score.

---

## Proposed Evidence Tiers

### Platinum

Highest-confidence evidence with exceptional rigor, direct disease relevance, and strong governance.

Platinum evidence generally reflects direct large-scale human disease-association evidence or exceptionally mature expert consensus frameworks.

Characteristics:

- massive cohort scale where applicable
- stringent statistical conservatism
- highly reproducible
- direct disease-association evidence
- exceptional governance quality

Examples:

- Epi25 high-confidence loci

Platinum tier should remain rare.

### Gold

Strong biological evidence with high-quality validation and governance.

Characteristics:

- strong biological evidence
- multi-modal integration
- extensive validation
- high governance quality

Examples:

- MitoCarta

Gold evidence is highly valuable but may not directly represent disease association.

### Silver

Clinical utilization or translational evidence.

Characteristics:

- reflects real-world diagnostic practice
- influenced by panel design and clinical workflows
- useful translational signal
- not equivalent to mechanistic proof

Examples:

- GTR-derived testing utilization evidence
- future diagnostic panel aggregation datasets

Important:

```text
clinical testing utilization does not equal disease causality
```

A gene may appear frequently in testing panels because:

- it is clinically important
- it is exploratory
- it is historically included
- it is part of broad sequencing assays

Silver-tier evidence should therefore be interpreted conservatively.

### Bronze

Exploratory or lower-confidence evidence.

Characteristics:

- hypothesis-generating
- incomplete validation
- potentially noisy
- may still contain biologically valuable signal

Examples:

- broad literature mining
- exploratory computational overlays
- weakly replicated associations
- Genes4Epilepsy

---

## Evidence Dimensions

GSC evidence sources may contribute different quantitative dimensions.

Examples include:

| Dimension                      | Interpretation                   |
| ------------------------------ | -------------------------------- |
| cohort_count                   | independent study replication    |
| test_count                     | clinical utilization frequency   |
| independent_lab_count          | cross-laboratory adoption        |
| trait_count                    | phenotype breadth                |
| ontology_collapsed_trait_count | normalized phenotype specificity |
| publication_count              | literature prevalence            |

Not all evidence dimensions apply equally to all evidence sources.

Dimensions should be interpreted within the semantic context of the originating source.

---

## Evidence Semantics Matter

GSC intentionally separates:

```text
association
```

from:

```text
utilization
```

and from:

```text
functional localization
```

Examples:

- MitoCarta suggests mitochondrial localization.
- Epi25 suggests epilepsy association.
- GTR suggests diagnostic utilization.
- Future ClinVar overlays may suggest clinical interpretation activity.

These evidence types should not be treated as interchangeable.

---

## Raw Evidence vs Summarized Evidence

GSC distinguishes:

### Raw Evidence

Preserves:

- parser outputs
- ontology relationships
- detailed provenance
- row-level observations

Raw evidence prioritizes:

- reproducibility
- auditability
- downstream reinterpretation

---

## Summarized Evidence

Derived phenotype-scoped summaries intended for downstream aggregation and consensus scoring.

Summaries may apply:

- ontology normalization
- filtering
- weighting
- duplicate collapse
- broad test suppression
- tier-aware interpretation policies

## Cross-Tier Aggregation Caution

Evidence originating from different semantic tiers should not be naively merged into a single undifferentiated score.

For example:

- statistical association
- clinical utilization
- functional localization

represent distinct biological and translational concepts.

Future aggregation frameworks should preserve interpretability and provenance-aware weighting.

## Planned Future Expansion

Planned future evidence adapters may include:

- ClinVar XML
- OMIM-derived structured overlays
- PanelApp
- metabolomics assay registries
- transcriptomic convergence overlays
- pathway/network evidence systems

All future adapters should preserve:

- provenance
- evidence semantics
- parser versioning
- extraction-rule versioning
- release-scoped determinism

Planned future adapters remain conceptual until:
- parser implementation exists
- provenance policy is defined
- release integration is validated

---