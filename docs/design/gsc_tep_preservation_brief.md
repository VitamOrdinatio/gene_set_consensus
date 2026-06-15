# GSC-TEP Preservation Brief

## Scientific Preservation Requirements for GSC → VDB Transport

Intended location: `docs/design/gsc_tep_preservation_brief.md`

---

## 1. Purpose

This document defines the scientific preservation requirements for transporting GSC-generated semantic prior evidence into VDB through the Transitional Evidence Product framework.

GSC-TEP exists to preserve phenotype-scoped semantic prior evidence during transport.

It must not reduce GSC outputs to:

* binary gene-set membership
* opaque score exports
* phenotype-agnostic gene annotations
* flattened source summaries
* VDB-owned reinterpretations

The central preservation question is:

```text
What must never be lost when GSC evidence moves to VDB?
```

---

## 2. Preservation Position

GSC remains authoritative for semantic prior meaning.

VDB remains authoritative for:

* durable persistence
* discovery
* namespace brokerage
* additive identity normalization
* query-surface exposure

RDGP remains a downstream consumer that may later use VDB-preserved GSC priors as phenotype-level support during sample-gene reasoning.

GSC-TEP therefore transports knowledge-layer evidence into the persistence layer without transferring semantic authority.

---

## 3. Primary Evidence Class

The primary evidence class requiring preservation is:

```text
phenotype-scoped semantic prior evidence
```

A GSC prior is not merely a gene list.

It is a structured statement that a gene has a particular evidence-supported relationship to a phenotype within a defined GSC release, scoring profile, source set, and provenance context.

The core scientific identity is:

```text
(gsc_release_id, phenotype, gene_id)
```

or, before VDB brokerage:

```text
(gsc_release_id, phenotype, source_gene_id/source_gene_symbol)
```

A change to phenotype, release, or gene identity changes the scientific statement.

---

## 4. What Must Never Be Lost

### 4.1 Phenotype Context

Phenotype scope must never be lost.

The same gene may have different evidence meaning in different phenotypes.

Example:

```text
POLG in mitochondrial_disease
≠
POLG in epilepsy
```

Losing phenotype scope would convert a contextual semantic prior into a misleading universal gene claim.

Required preservation:

* phenotype identifier
* phenotype label
* phenotype version or profile context when available
* phenotype-scoring profile
* phenotype source/config context

---

### 4.2 Gene Identity and Source Identity

GSC-submitted gene identity must remain preserved even if VDB later assigns canonical identities.

Required preservation:

* source gene symbol
* source gene identifier
* source namespace
* mapping status from GSC, if available
* unresolved or ambiguous identifier state
* canonical identity only as additive brokerage downstream

Scientific rationale:

Canonical identity supports interoperability, but source identity preserves historical reconstructability and protects against destructive normalization.

---

### 4.3 Release Identity

GSC release identity must be preserved as part of semantic prior identity.

Required preservation:

* `gsc_release_id`
* GSC version
* source package identity
* source release identifiers
* GSC execution/run identity where available
* TEP sleeve version later defined by DEX

Scientific rationale:

A semantic prior generated in one release may differ from the same phenotype-gene row in a later release. Historical reproducibility requires preserving release identity.

---

### 4.4 Semantic Consensus Scores

Scores must remain preserved with their scoring context.

Required preservation:

* `consensus_score`
* `semantic_consensus_score`, if emitted
* `weighted_source_sum`
* `active_score`
* score interpretation context
* scoring profile
* scoring framework/version

Scientific rationale:

A score without its scoring profile becomes uninterpretable. A score alone cannot explain whether support derives from statistical association, clinical interpretation, localization, utilization, or exploratory evidence.

---

### 4.5 Semantic Channel Multiplicity

GSC semantic channels must survive transport.

Required preservation:

* direct disease evidence contribution
* clinical interpretation contribution
* contextual biology contribution
* utilization contribution
* exploratory contribution
* convergence contribution, if present
* channel summary
* active/inactive channel state
* annotation-only evidence state

Scientific rationale:

Flattening semantic channels into one score destroys the distinction between evidence meaning and evidence strength. This would damage downstream RDGP reasoning because RDGP may need to distinguish direct disease evidence from contextual support.

---

### 4.6 Source Multiplicity

Source multiplicity must remain visible.

Required preservation:

* source list
* source count
* source identifiers
* source tiers
* source semantics
* source releases
* per-source contribution state where available
* whether a source contributed scoring-active or annotation-only evidence

Scientific rationale:

A gene supported by one high-confidence source is not equivalent to a gene supported by many weak or correlated sources. Source multiplicity is necessary for audit, reinterpretation, and future scoring recalibration.

---

### 4.7 Aggregation Topology

The relationships that produced the consensus must survive.

Required preservation:

* phenotype-to-gene relationship
* source-to-gene relationship
* source-to-phenotype relationship
* source-to-score contribution relationship
* source-to-semantic-channel relationship
* release-to-output relationship

Scientific rationale:

Consensus meaning arises from aggregation topology. If only final rows survive, future consumers cannot reconstruct why a gene received its score.

---

### 4.8 Provenance

Provenance must remain reconstructable.

Required preservation:

* source dataset provenance
* GSC release provenance
* scoring provenance
* aggregation provenance
* rule/config provenance
* source artifact provenance
* source artifact manifest references
* source ownership

Scientific rationale:

Semantic priors without provenance cannot be trusted, audited, reproduced, or reinterpreted.

---

### 4.9 Uncertainty and Null Semantics

Uncertainty must remain explicit.

Required preservation:

* missing
* unknown
* unresolved
* ambiguous
* not applicable
* no match
* zero support
* annotation only
* conflict state
* mapping uncertainty

Scientific rationale:

Absence of evidence is not negative evidence. Missing score is not zero support. Unresolved identity is not non-membership.

---

### 4.10 Historical Reproducibility

Historical GSC evidence states must remain reconstructable.

Required preservation:

* release identity
* source package identity
* scoring profile
* source artifact manifest
* source versions
* GSC version
* TEP sleeve version once implemented

Scientific rationale:

Future VDB or RDGP users must be able to determine which historical semantic prior was used during a previous analysis.

---

### 4.11 Future Reinterpretability

The GSC-TEP must preserve enough information for future reinterpretation.

Future reinterpretation may include:

* new scoring models
* new phenotype mappings
* new gene identifiers
* new ontology relationships
* new GSC releases
* revised source tiers
* revised source trust
* RDGP reanalysis

Scientific rationale:

A future system should be able to reinterpret preserved GSC priors without requiring historical GSC execution to be repeated.

---

## 5. What Must Not Happen

GSC-TEP must not:

* collapse phenotype scope
* convert semantic priors into binary membership
* preserve only final consensus score
* erase source identities
* erase GSC release identity
* erase scoring profile context
* collapse semantic channels
* hide uncertainty
* silently treat missing values as zero
* silently canonicalize gene identity
* allow VDB to recompute GSC meaning
* allow RDGP to consume phenotype-neutral priors

---

## 6. Preservation Requirements Summary

A scientifically adequate GSC-TEP must preserve:

```text
Phenotype context
Gene identity
GSC release identity
Semantic consensus score
Weighted score context
Semantic channel composition
Source multiplicity
Source attribution
Aggregation topology
Scoring context
Provenance
Uncertainty
Null semantics
Historical reproducibility
Future reinterpretability
```

---

## 7. Scientific Success Criteria

GSC-TEP succeeds if a future user can answer:

1. What phenotype was this prior scoped to?
2. Which gene identity did GSC emit?
3. Which GSC release produced it?
4. Which sources contributed?
5. Which semantic channels contributed?
6. Which score was active?
7. What scoring profile governed interpretation?
8. What uncertainty existed?
9. What source artifacts supported the prior?
10. Could this evidence be reinterpreted later?

If any of these questions cannot be answered, scientific meaning has been lost.

---

## 8. Implementation Boundary

This document does not define:

* JSON schemas
* SQL schemas
* file formats
* database tables
* implementation code
* TEP envelope structure
* DEX implementation plan

Those belong to DEX-GSC and VDB implementation layers.

This document defines what scientific meaning must survive.
