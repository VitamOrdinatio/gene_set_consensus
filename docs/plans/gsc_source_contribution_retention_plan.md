# GSC Source Contribution Retention Plan

## Objective

Implement producer-side retention of source contribution topology so that future VDB consumers can access non-collapsed semantic provenance through finalized-run artifacts.

This plan implements the requirements established by:

docs/contracts/gsc_source_contribution_retention_contract.md

---

# Phase 1 — Topology Inventory

## Goal

Determine which source contribution fields already exist within the GSC pipeline and identify where topology is lost.

## Inspect

* normalized_source_records.tsv
* gene_source_matrix.tsv
* gene_provenance.tsv
* consensus_gene_set.tsv

## Deliverable

Field inventory documenting:

* retained fields
* collapsed fields
* missing fields

---

# Phase 2 — Canonical Artifact Design

## Goal

Define a dedicated retention artifact.

## Artifact

source_contributions.tsv

## Design Principle

One row SHALL represent one source contribution.

No aggregation.

No collapse.

## Deliverable

Canonical schema specification.

---

# Phase 3 — Step05 Retention

## Goal

Extend Step05 output generation.

## Modify

scripts/step_05_write_outputs.py

## New Output

results/runs/<run_id>/tables/<package_id>/source_contributions.tsv

## Deliverable

Authoritative source contribution artifact produced during finalized-run construction.

---

# Phase 4 — Manifest Integration

## Goal

Include source contribution retention artifacts within finalized-run integrity tracking.

## Update

* run_manifest.yaml
* final_run_manifest.yaml

## Requirements

Retain:

* artifact path
* checksum
* artifact classification

## Deliverable

Source contribution artifact protected by finalized-run integrity guarantees.

---

# Phase 5 — TEP Manifest Integration

## Goal

Expose preserved topology to VDB through the TEP sleeve.

## Modify

src/gene_set_consensus/tep/manifest.py

## Add Artifact

source_contributions.tsv

to the TEP manifest artifact inventory.

## Non-Goal

Do not introduce payload.source_contributions at this stage.

Reference-based preservation is preferred.

---

# Validation

## Functional Validation

Verify:

* source_contributions.tsv exists
* row counts are preserved
* topology is not collapsed

## Integrity Validation

Verify:

* manifest inclusion
* checksum coverage
* finalized-run retention

## TEP Validation

Verify:

* source_contributions.tsv appears in TEP manifest artifacts
* VDB consumers can discover topology through artifact references

---

# Completion Criteria

The finalized run directory SHALL preserve source contribution topology as an authoritative artifact.

GSC-TEP SHALL reference that artifact without reconstructing or inferring source contribution relationships.

Producer-side preservation SHALL be achieved before any future payload-level topology expansion.
