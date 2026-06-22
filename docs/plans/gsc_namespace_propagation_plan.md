# GSC Namespace Propagation Plan

## Purpose

Implement canonical namespace propagation throughout aggregation, scoring, consensus generation, and TEP construction.

This plan executes the requirements defined in:

```text
docs/contracts/gsc_namespace_propagation_contract.md
```

---

# Current State

Completed:

```text
Source Manifest
Source Registry
Identifier Map
Normalization
normalized_source_records.tsv
source_contributions.tsv
gene_provenance.tsv
```

Source and canonical namespace attribution are now preserved.

Outstanding:

```text
gene_source_matrix.tsv
gene_frequency_table.tsv
scored_gene_evidence.tsv
consensus_gene_set.tsv
GSC-TEP
semantic_prior_id uniqueness
```

---

# Phase 1

## Trace Namespace Loss

Objective:

Determine where canonical namespace information is dropped.

Inspect:

```text
aggregation.py
step_03_build_source_matrix.py
step_04_score_consensus.py
```

Verify presence of:

```text
gene_namespace
```

within:

```text
gene_source_matrix.tsv
gene_frequency_table.tsv
scored_gene_evidence.tsv
```

Deliverable:

Namespace propagation boundary identified.

---

# Phase 2

## Preserve Namespace Through Aggregation

Objective:

Modify aggregation workflows to retain:

```text
gene_namespace
```

during grouping operations.

Required outputs:

```text
gene_source_matrix.tsv
gene_frequency_table.tsv
```

must contain:

```text
gene_id
gene_namespace
```

Deliverable:

Namespace-aware aggregation.

---

# Phase 3

## Preserve Namespace Through Scoring

Objective:

Carry canonical namespace information into:

```text
scored_gene_evidence.tsv
```

Required fields:

```text
gene_id
gene_namespace
```

Deliverable:

Namespace-aware scoring outputs.

---

# Phase 4

## Restore Consensus Namespace Preservation

Objective:

Reintroduce:

```text
gene_namespace
```

into:

```text
consensus_gene_set.tsv
```

without breaking tests.

Update output validation as required.

Deliverable:

Consensus outputs preserve canonical namespace identity.

---

# Phase 5

## TEP Identity Hardening

Objective:

Propagate namespace information into semantic priors.

Required fields:

```yaml
identity:
  gene_id:
  gene_namespace:
```

Update semantic prior identity construction.

Replace:

```text
phenotype::gene_symbol
```

with deterministic namespace-aware identity.

Recommended structure:

```text
<release>::<phenotype>::<gene_namespace>::<gene_id>
```

Deliverable:

Unique semantic_prior_id values.

---

# Phase 6

## Validation

Execute:

```text
example
mitochondrial
epilepsy
```

Validate:

* namespace propagation
* semantic prior uniqueness
* TEP preservation
* interoperability readiness

Deliverable:

Certification-ready namespace propagation.

---

# Exit Criteria

All required artifacts preserve:

```text
gene_id
gene_namespace
```

Semantic prior identifiers are unique.

TEPs transport canonical namespace information without collapse.

Namespace propagation contract passes.
