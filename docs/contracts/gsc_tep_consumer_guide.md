# GSC TEP Consumer Guide

## Purpose

This document provides guidance for downstream systems consuming Gene Set Consensus (GSC) Transitional Evidence Products (TEPs).

The primary intended audience is:

```text
DEX-VDB
```

but the guidance is applicable to any future consumer of GSC-produced TEPs.

This document summarizes:

* what a GSC-TEP represents
* what information is authoritative
* what information is transport identity
* what information must be preserved
* how namespace multiplicity should be interpreted
* current certification status

---

# What a GSC-TEP Represents

A GSC-TEP is a transport artifact that preserves:

```text
phenotype-scoped semantic consensus
```

for phenotype-gene relationships.

The primary output of GSC is:

```text
a phenotype-scoped semantic prior
for phenotype-gene relationships
```

A GSC-TEP is therefore not:

* a variant interpretation
* a patient interpretation
* a pathogenicity assertion
* a diagnostic conclusion

A GSC-TEP preserves the state of a GSC release so that downstream systems may consume, inspect, broker, or reinterpret the consensus.

---

# Identity Model

## Fundamental Entity

The fundamental entity emitted by GSC is:

```text
(phenotype, gene)
```

not:

```text
(sample, gene)
```

The latter is the responsibility of RDGP and other patient-level systems.

---

## Canonical Identity

Consumers should treat:

```text
identity.gene_id
identity.gene_namespace
```

as the canonical biological identity.

Consumers should not rely on:

```text
gene_symbol
```

for uniqueness.

Gene symbols are display-oriented identifiers and may collide across namespaces or source systems.

---

## semantic_prior_id

The canonical transport identity for a semantic prior is:

```text
release_id::
phenotype::
gene_namespace::
gene_id
```

Example:

```text
epilepsy_semantic_gtr_experimental_v0.1::
epilepsy::
ensembl_gene::
ENSG00000100150
```

Consumers should treat:

```text
semantic_prior_id
```

as the authoritative transport identity.

---

# Namespace Preservation

## Important Principle

GSC preserves namespace multiplicity.

Consumers must not assume:

```text
gene_symbol
```

uniquely determines biological identity.

Example:

```text
ACACA
```

may legitimately appear as:

```text
ensembl_gene::
ENSG00000275176|ENSG00000278540
```

and:

```text
ncbi_gene::
31
```

within the same release.

These identities must remain distinct unless an explicit namespace brokerage process establishes equivalence.

---

# Provenance Model

Every semantic prior preserves:

```text
provenance_id
```

which links the semantic prior back to the originating evidence topology.

Consumers should preserve provenance identifiers whenever possible.

Provenance identifiers enable:

* auditability
* reconstruction
* evidence tracing
* future reinterpretation

---

# Source Contribution Topology

## Important Artifact

Current certified GSC-TEPs preserve a reference to:

```text
source_contributions.tsv
```

This artifact is considered authoritative topology evidence.

The source contribution topology preserves:

```text
source_id
source_name
source_type
source_weight
weight_tier
evidence_semantics
evidence_tier
semantic_channel
scoring_rule_id
source_record_hash
```

among other fields.

---

## Consumer Recommendation

Consumers should use:

```text
source_contributions.tsv
```

when they require:

* channel reconstruction
* evidence topology inspection
* source-level attribution
* provenance auditing

Consumers should not attempt to reconstruct topology from aggregate scores alone.

---

# Semantic Channels

Current GSC semantic channels include:

```text
direct_disease
clinical_utilization
contextual_biology
exploratory_literature
```

Consumers should interpret channels as distinct evidence modalities.

Channels should not be treated as interchangeable.

---

# Consensus Scores

Consensus scores represent:

```text
semantic consensus strength
```

within the scope of a phenotype-specific GSC release.

Consensus scores do not represent:

* pathogenicity probability
* causal certainty
* penetrance
* patient risk

Consumers should preserve score provenance and release context.

---

# Reference-Based Preservation Model

Current certified GSC-TEPs use a reference-preservation model.

GSC-TEPs preserve references to authoritative producer artifacts rather than embedding all topology information directly inside the TEP.

Examples include:

```text
consensus_gene_set.tsv
gene_provenance.tsv
source_contributions.tsv
```

Consumers should treat referenced artifacts as authoritative producer outputs.

---

# Certified Releases

As of certification review by SAGE:

## Epilepsy

Release:

```text
epilepsy_semantic_gtr_experimental_v0.1
```

Certified run:

```text
run_2026_06_22_184534
```

Certification status:

```text
CERTIFIED
```

---

## Mitochondrial Disease

Release:

```text
mitochondrial_semantic_gtr_experimental_v0.1
```

Certified run:

```text
run_2026_06_23_015533
```

Certification status:

```text
CERTIFIED
```

---

# Certification Findings

Certification review validated:

```text
semantic_prior_id uniqueness
namespace preservation
source contribution retention
provenance preservation
identity transport semantics
```

for both certified releases.

---

# DEX-VDB Integration Guidance

DEX-VDB should assume:

```text
GSC identities are namespace-aware
```

and should preserve:

```text
gene_id
gene_namespace
source_gene_id
source_gene_namespace
semantic_prior_id
provenance_id
```

without collapse.

Consumers should avoid reducing identity to:

```text
gene_symbol
```

alone.

---

# Future Expectations

Future GSC releases may introduce:

* additional semantic channels
* additional namespace types
* ontology-aware releases
* expanded provenance structures
* portable TEP bundles

Consumers should therefore prefer:

```text
field-preserving ingestion
```

over release-specific assumptions.

---

# Strategic Summary

The primary responsibility of a GSC-TEP consumer is:

```text
preserve phenotype-scoped semantic consensus
without collapsing identity,
namespace,
provenance,
or source topology.
```

If preservation and namespace integrity are maintained, downstream systems remain free to perform additional brokerage, interpretation, ranking, or reasoning without loss of original GSC evidence semantics.
