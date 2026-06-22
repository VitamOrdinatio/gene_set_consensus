# GSC Gene Namespace Attribution Plan

## Purpose

Define the implementation plan for producer-side gene namespace attribution in Gene Set Consensus.

This plan implements:

docs/contracts/gsc_gene_namespace_attribution_contract.md

The objective is to ensure that gene identifier namespaces are introduced at ingestion, preserved through canonical GSC stages, and transported into GSC-TEPs without downstream inference.

---

# Current State

Current adapters emit:

* gene_symbol
* gene_id
* evidence_label
* notes

Current normalization emits:

* normalized_gene_symbol
* gene_id
* mapping_status

Current TEP construction can expose:

* gene_namespace
* source_gene_namespace

but these fields are not yet derived from authoritative producer-side namespace attribution.

As a result, some transported identifiers remain:

unknown_namespace

This is safe but incomplete.

---

# Design Principle

Namespace attribution SHALL originate as close as possible to the source adapter.

Downstream stages SHALL preserve namespace attribution.

TEP construction SHALL transport namespace attribution.

VDB SHALL perform namespace brokerage and cross-namespace reconciliation.

GSC SHALL NOT infer namespace identity from string shape when source authority is available.

---

# Phase 1 — Adapter Namespace Inventory

## Goal

Determine what namespace authority each adapter can legitimately provide.

## Inspect

* GenericGeneListAdapter
* GTRPanelAdapter
* MitoCartaAdapter
* future adapters

## Questions

For each adapter:

* What identifier fields are present?
* What namespace does each identifier field represent?
* Is the namespace declared by source documentation, source schema, or source configuration?
* Is namespace attribution deterministic?
* Should unresolved or ambiguous cases be marked unknown_namespace?

## Expected Findings

MitoCarta likely supports at least:

* HumanGeneID
* EnsemblGeneID_mapping_version_20200130

GTR likely supports NCBI Gene identifiers, but this SHALL be verified from the actual GTR source artifact/schema before implementation.

Generic gene lists may require source-config-level namespace declaration.

---

# Phase 2 — Source Configuration Namespace Declaration

## Goal

Allow source-specific namespace authority to be declared without hardcoding assumptions into generic adapters.

## Add Optional Source Fields

Each source configuration MAY declare:

* source_gene_namespace
* adapter_gene_id_namespace
* canonical_gene_namespace

## Example

```yaml
source_gene_namespace: hgnc_symbol
adapter_gene_id_namespace: ncbi_gene
canonical_gene_namespace: ensembl_gene
```

## Rule

If an adapter-specific source file provides a known gene_id field, the source configuration or adapter SHALL declare its namespace.

If no authority exists, namespace SHALL be:

unknown_namespace

---

# Phase 3 — Adapter Output Expansion

## Goal

Extend adapter outputs to include namespace fields.

## Required Adapter Output Fields

Adapters SHALL emit:

* source_gene_symbol
* source_gene_id
* source_gene_namespace

Adapters MAY emit:

* adapter_gene_id
* adapter_gene_id_namespace
* preferred_gene_id
* preferred_gene_namespace

depending on source structure.

## Transitional Compatibility

Adapters MAY continue emitting:

* gene_symbol
* gene_id

during transition, but these fields SHALL eventually be replaced or clearly mapped to namespace-aware fields.

---

# Phase 4 — Normalization Preservation

## Goal

Carry source and canonical namespace fields into normalized_source_records.tsv.

## Required Normalized Fields

normalized_source_records.tsv SHALL preserve:

* source_gene_symbol
* source_gene_id
* source_gene_namespace
* gene_symbol
* gene_id
* gene_namespace
* mapping_status

## Mapping Boundary

Normalization SHALL make explicit:

source identifier
→ mapping status
→ canonical GSC identifier

GSC SHALL preserve both sides of the mapping.

---

# Phase 5 — Finalized Artifact Retention

## Goal

Preserve namespace attribution in authoritative finalized-run artifacts.

Update:

* source_contributions.tsv
* gene_provenance.tsv
* consensus_gene_set.tsv

to preserve:

* source_gene_namespace
* gene_namespace

where identifier fields are present.

## Requirement

No finalized-run artifact containing gene identifiers SHALL omit namespace attribution unless the namespace is explicitly unknown_namespace.

---

# Phase 6 — TEP Payload and Manifest Preservation

## Goal

Ensure GSC-TEPs preserve namespace attribution without inference.

TEP payload identity SHALL use namespace values from authoritative finalized-run artifacts.

TEP construction SHALL NOT infer namespace from gene_id string format except as a defensive fallback explicitly marked as such.

## Expected TEP Identity Fields

* source_gene_symbol
* source_gene_id
* source_gene_namespace
* gene_symbol
* gene_id
* gene_namespace
* mapping_status

---

# Phase 7 — Semantic Prior Identifier Hardening

## Goal

Eliminate semantic_prior_id collisions.

## Current Problem

Current semantic_prior_id uses:

phenotype::gene_symbol

This is not unique when multiple identifiers or namespaces share the same gene symbol.

## Target Identifier

semantic_prior_id SHALL include deterministic transport identity fields.

Recommended form:

gsc_release_id::phenotype::gene_namespace::gene_id

or equivalent deterministic identity including:

* release identity
* phenotype
* gene namespace
* gene identifier

## Human-Readable Display

Human-readable display labels MAY remain gene-symbol based.

Example:

mitochondrial_disease::AARS2

But transport identity SHALL be namespace-aware and collision-resistant.

---

# Phase 8 — Validation

## Required Checks

Validation SHALL confirm:

* no missing namespace fields in identifier-bearing records
* unknown namespaces are explicit
* no semantic_prior_id duplicates exist
* source_contributions.tsv preserves source and canonical namespace fields
* TEP payload identity preserves namespace fields
* mitochondrial TEP semantic_prior_id values are unique

## Example Validation Commands

Count duplicate semantic prior IDs:

```bash
jq -r '.payload.semantic_priors[].semantic_prior_id' gsc_tep.json \
  | sort \
  | uniq -d \
  | wc -l
```

Inspect namespace-bearing identity:

```bash
jq '.payload.semantic_priors[0].identity' gsc_tep.json
```

---

# Completion Criteria

This plan is complete when:

* namespace attribution originates at adapters or source configuration
* namespace attribution survives normalization
* namespace attribution survives finalized-run artifacts
* namespace attribution survives TEP construction
* semantic_prior_id is unique for all transported semantic priors
* VDB can perform brokerage without inferring identifier namespace from string shape

The final state should support:

GSC preserves namespace attribution.
GSC-TEP transports namespace attribution.
VDB performs namespace brokerage.
