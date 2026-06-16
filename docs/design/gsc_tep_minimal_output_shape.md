# GSC-TEP Minimal Output Shape

## Draft Status

Draft v0.1 for first real-world GSC-TEP implementation.

---

# Purpose

This document defines the minimal concrete output shape for the first real-world GSC-TEP.

The goal is to provide a deterministic implementation target for:

```text
scripts/build_gsc_tep.py
```

This document does not define:

```text
final JSON schema
VDB persistence schema
long-term TEP specification
all future GSC-TEP versions
```

It defines the smallest acceptable inspectable GSC-TEP shape for the first producer-side implementation.

---

# Initial Target

The first GSC-TEP target is:

```text
epilepsy_semantic_gtr_experimental
```

Source locations:

```text
results/tables/epilepsy_semantic_gtr_experimental/
results/reports/epilepsy_semantic_gtr_experimental/
```

Output location:

```text
results/teps/gsc/epilepsy_semantic_gtr_experimental/gsc_tep.json
```

---

# Output Format Decision

The first GSC-TEP SHALL be emitted as:

```text
single JSON file
```

with exactly three top-level sections:

```json
{
  "envelope": {},
  "manifest": {},
  "payload": {}
}
```

This shape is intentionally simple to support:

```text
manual inspection
validation development
DEX-VDB handoff
future schema refinement
```

---

# Top-Level Section 1: Envelope

## Purpose

The envelope provides transport identity and transport governance metadata.

The envelope answers:

```text
What transport object is this?
Who produced it?
Which producer package generated it?
Which TEP rules apply?
```

---

## Minimal Envelope Fields

The first GSC-TEP envelope SHOULD include:

```json
{
  "tep_id": "gsc_tep_epilepsy_semantic_gtr_experimental_v0_1",
  "tep_type": "gsc_tep",
  "tep_schema_version": "0.1",
  "tep_sleeve_version": "gsc_tep_sleeve_v0.1",
  "source_repository": "gene_set_consensus",
  "source_package_id": "epilepsy_semantic_gtr_experimental",
  "source_identity_scope": "gsc_release_id + phenotype + gene identity",
  "creation_timestamp": "<ISO-8601 UTC timestamp>",
  "validation_state": "candidate",
  "provenance": {
    "producer": "gene_set_consensus",
    "construction_mode": "producer_side_projection",
    "source_artifacts_authoritative": true
  }
}
```

---

## Envelope Requirements

The envelope must preserve the distinction between:

```text
TEP transport identity
GSC release identity
GSC biological identity
source artifact identity
```

The `tep_id` must not be treated as a biological identity.

The `source_package_id` for GSC should correspond to the GSC release/package identifier used to locate producer outputs.

---

# Top-Level Section 2: Manifest

## Purpose

The manifest preserves source artifact lineage.

The manifest answers:

```text
Which producer artifacts were used?
Where did they come from?
What role did each artifact play?
```

---

## Minimal Manifest Shape

The first GSC-TEP manifest SHOULD include:

```json
{
  "source_package_id": "epilepsy_semantic_gtr_experimental",
  "tables_dir": "results/tables/epilepsy_semantic_gtr_experimental",
  "reports_dir": "results/reports/epilepsy_semantic_gtr_experimental",
  "artifacts": [
    {
      "artifact_id": "consensus_gene_set",
      "artifact_type": "tsv",
      "artifact_path": "results/tables/epilepsy_semantic_gtr_experimental/consensus_gene_set.tsv",
      "semantic_role": "primary_semantic_prior_table",
      "producer_ownership": "gene_set_consensus"
    },
    {
      "artifact_id": "gene_frequency_table",
      "artifact_type": "tsv",
      "artifact_path": "results/tables/epilepsy_semantic_gtr_experimental/gene_frequency_table.tsv",
      "semantic_role": "aggregation_support_table",
      "producer_ownership": "gene_set_consensus"
    },
    {
      "artifact_id": "gene_provenance",
      "artifact_type": "tsv",
      "artifact_path": "results/tables/epilepsy_semantic_gtr_experimental/gene_provenance.tsv",
      "semantic_role": "source_provenance_table",
      "producer_ownership": "gene_set_consensus"
    },
    {
      "artifact_id": "gene_source_matrix",
      "artifact_type": "tsv",
      "artifact_path": "results/tables/epilepsy_semantic_gtr_experimental/gene_source_matrix.tsv",
      "semantic_role": "source_gene_relationship_table",
      "producer_ownership": "gene_set_consensus"
    },
    {
      "artifact_id": "run_manifest",
      "artifact_type": "yaml",
      "artifact_path": "results/reports/epilepsy_semantic_gtr_experimental/run_manifest.yaml",
      "semantic_role": "run_and_release_context",
      "producer_ownership": "gene_set_consensus"
    },
    {
      "artifact_id": "output_contract_validation",
      "artifact_type": "tsv",
      "artifact_path": "results/reports/epilepsy_semantic_gtr_experimental/output_contract_validation.tsv",
      "semantic_role": "output_contract_validation",
      "producer_ownership": "gene_set_consensus"
    },
    {
      "artifact_id": "validation_report",
      "artifact_type": "md",
      "artifact_path": "results/reports/epilepsy_semantic_gtr_experimental/validation_report.md",
      "semantic_role": "human_readable_validation_report",
      "producer_ownership": "gene_set_consensus"
    }
  ]
}
```

---

## Manifest Requirements

The manifest must preserve all producer-owned source artifact references used to construct the TEP.

The manifest should support future addition of:

```text
checksums
file sizes
row counts
field lineage
artifact generation timestamps
```

The absence of checksums in the first implementation is acceptable only if the TEP remains clearly marked as a candidate or provisional artifact.

---

# Top-Level Section 3: Payload

## Purpose

The payload preserves semantic prior evidence.

The payload answers:

```text
What semantic priors were transported?
What phenotype were they scoped to?
Which genes were involved?
Which sources contributed?
Which scores and semantic channels were preserved?
What uncertainty or provenance context survived?
```

---

## Minimal Payload Shape

The first GSC-TEP payload SHOULD include:

```json
{
  "gsc_release_id": "epilepsy_semantic_gtr_experimental",
  "phenotype": "epilepsy",
  "semantic_prior_count": 0,
  "semantic_priors": [],
  "source_summary": {},
  "channel_summary": {},
  "uncertainty_summary": {},
  "construction_notes": []
}
```

---

# Semantic Prior Entity Shape

Each item in `semantic_priors` SHOULD represent one release-scoped phenotype-gene semantic prior.

Minimal shape:

```json
{
  "semantic_prior_id": "epilepsy_semantic_gtr_experimental::epilepsy::SCN1A",
  "identity": {
    "gsc_release_id": "epilepsy_semantic_gtr_experimental",
    "phenotype": "epilepsy",
    "source_gene_symbol": "SCN1A",
    "source_gene_id": null,
    "gene_symbol": "SCN1A",
    "gene_id": null,
    "mapping_status": null
  },
  "scores": {
    "consensus_score": null,
    "semantic_consensus_score": null,
    "weighted_source_sum": null,
    "active_score": null,
    "scoring_profile": null
  },
  "semantic_channels": {
    "semantic_channel_summary": null,
    "direct_disease_score": null,
    "clinical_interpretation_score": null,
    "contextual_biology_score": null,
    "utilization_score": null,
    "exploratory_score": null,
    "convergence_score": null,
    "conflict_penalty": null
  },
  "source_attribution": {
    "source_count": null,
    "source_list": null,
    "evidence_semantics_summary": null,
    "evidence_tier_summary": null,
    "weight_tier_summary": null
  },
  "provenance": {
    "provenance_id": null,
    "run_id": null,
    "gsc_version": null,
    "generated_at": null
  },
  "uncertainty": {
    "mapping_status_summary": null,
    "nullability_notes": []
  }
}
```

---

# Required Payload Guarantees

For every semantic prior, the payload must preserve or explicitly mark:

```text
phenotype context
gene identity
release identity
source attribution
semantic channel composition
score context
provenance
uncertainty
```

A missing value is acceptable only if it is represented explicitly as missing or unavailable.

Silent omission is not acceptable.

---

# Minimal Summary Fields

The first GSC-TEP SHOULD include summary fields to support manual inspection.

Examples:

```json
{
  "semantic_prior_count": 12,
  "source_summary": {
    "sources_observed": ["EPI25", "GTR", "MitoCarta"],
    "source_count_total": 3
  },
  "channel_summary": {
    "channels_observed": ["direct_disease", "clinical_utilization"],
    "channel_count_total": 2
  },
  "uncertainty_summary": {
    "mapping_statuses_observed": ["mapped", "unresolved"]
  }
}
```

These summaries do not replace the per-prior payload.

They exist to support inspection.

---

# Minimal Construction Rules

The first builder implementation should:

1. Read `consensus_gene_set.tsv`.
2. Use each consensus row as one semantic prior.
3. Preserve all available fields from the final consensus output.
4. Attach source/provenance context when recoverable from companion tables.
5. Construct a source artifact manifest.
6. Emit one JSON file with `envelope`, `manifest`, and `payload`.
7. Mark the TEP as `candidate` until validation passes.

---

# Output Inspection Expectations

A human reviewer should be able to open:

```text
results/teps/gsc/epilepsy_semantic_gtr_experimental/gsc_tep.json
```

and answer:

```text
Which GSC package generated this TEP?

Which phenotype is represented?

Which semantic priors were transported?

Which genes are represented?

Which scores were preserved?

Which semantic channels were preserved?

Which sources contributed?

Which provenance identifiers survived?

Which values remain uncertain or missing?
```

---

# Acceptance Boundary

This minimal shape is acceptable for first implementation if it satisfies:

```text
GSC-TEP contract requirements
GSC-TEP identity model requirements
GSC-TEP validation strategy
GSC-TEP acceptance criteria
```

It is not required to satisfy future VDB persistence optimization.

It is required to preserve enough semantic meaning for VDB discovery and intake design.

---

# Future Extensions

Future GSC-TEP versions may add:

```text
checksums
field lineage
explicit relationship arrays
normalized source contribution entities
channel contribution arrays
ontology context entities
multi-release bundles
compressed payload support
schema validation
machine-readable acceptance reports
```

These extensions should preserve compatibility with the core three-section organization:

```text
envelope
manifest
payload
```

---

# Summary

The first GSC-TEP should be a single JSON file containing:

```text
envelope
manifest
payload
```

derived from:

```text
epilepsy_semantic_gtr_experimental
```

and written to:

```text
results/teps/gsc/epilepsy_semantic_gtr_experimental/gsc_tep.json
```

The purpose of the first GSC-TEP is not final schema perfection.

The purpose is to create a real, inspectable, producer-owned semantic transport object that can be validated, scrutinized, and later handed to DEX-VDB for intake architecture development.
