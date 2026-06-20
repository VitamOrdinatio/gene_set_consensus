# GSC Source Contribution Retention Contract

## Purpose

This contract defines the producer-side preservation requirements for source contribution topology within Gene Set Consensus (GSC).

The objective is to ensure that future consumers, including VDB, can reconstruct how individual source records contributed to a semantic prior without relying on inference, summary reconstruction, or external configuration files.

This contract exists to prevent semantic collapse between source ingestion and TEP construction.

---

# Preservation Principle

GSC SHALL preserve source contribution topology before TEP construction.

GSC-TEP SHALL transport or reference preserved topology.

GSC-TEP SHALL NOT reconstruct, infer, or invent topology from collapsed summaries.

---

# Source Contribution Definition

A source contribution is defined as a single source-derived evidence record that participates in construction of a semantic prior.

Conceptually:

source contribution
→ semantic interpretation
→ semantic channel
→ scoring contribution
→ semantic prior

---

# Required Preservation Fields

For every source contribution retained by GSC, the following information SHALL be preserved.

## Identity

* gene_id
* gene_symbol
* source_gene_id
* source_gene_symbol

## Source Attribution

* source_id
* source_name
* source_record_hash
* source_row_number

## Semantic Classification

* evidence_semantics
* evidence_tier
* semantic_channel
* weight_tier

## Mapping State

* mapping_status
* namespace information when available

## Provenance

* provenance_id

---

# Retention Artifact

GSC SHALL retain source contribution topology in an authoritative finalized-run artifact.

Preferred artifact:

source_contributions.tsv

Location:

results/runs/<run_id>/tables/<package_id>/

One row SHALL represent one source contribution.

The artifact SHALL NOT contain collapsed gene-level summaries.

---

# Finalized Run Authority

The authoritative source contribution artifact SHALL participate in:

* run_manifest.yaml
* final_run_manifest.yaml

and SHALL receive the same integrity protections applied to other finalized-run artifacts.

---

# TEP Integration Requirements

GSC-TEP SHALL reference the authoritative source contribution artifact through the manifest artifact inventory.

Embedding source contribution topology directly within payload.source_contributions is OPTIONAL.

Reference-based preservation satisfies this contract.

---

# Prohibited Behaviors

The following are explicitly prohibited:

* reconstructing topology from summary fields
* inferring semantic channels from summaries
* inferring evidence tiers from summaries
* inventing source-level score contributions
* replacing preserved topology with aggregate representations

---

# Success Criteria

A future consumer SHALL be able to reconstruct:

gene
→ source contribution
→ evidence semantics
→ semantic channel
→ weight tier
→ provenance

without consulting external configuration files and without semantic inference.

Preservation SHALL occur at the producer level.
