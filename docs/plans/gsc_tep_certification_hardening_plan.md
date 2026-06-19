# GSC TEP Certification Hardening Plan

## Purpose

This plan defines the implementation roadmap required to achieve compliance with the GSC TEP Certification Contract.

The certification contract defines what a certified GSC-TEP must preserve.

This plan defines how GSC will evolve from scientifically valid candidate TEPs to certified preservation-aware transport artifacts suitable for long-term VDB ingestion.

The plan is organized by certification requirement rather than implementation component.

---

# Current Certification Status

Current GSC-TEPs satisfy the following certification areas:

```text
✓ Finalized-run anchoring
✓ Phenotype preservation
✓ Semantic score preservation
✓ Semantic channel preservation
✓ Source attribution preservation
✓ Provenance preservation
✓ Run-scoped producer artifact references
```

Current GSC-TEPs remain candidate artifacts because several certification requirements have not yet been fully implemented.

---

# Phase 1 — Retention Compliance

## Contract Sections

```text
Section 7
Retention Requirements
```

## Objective

Align TEP retention behavior with finalized-run preservation doctrine.

## Current State

Current authoritative output:

results/teps/gsc/<package_id>/gsc_tep.json

This permits later executions to overwrite historical TEPs.

## Target State

Authoritative location:

results/teps/gsc/<package_id>/<run_id>/gsc_tep.json

Convenience projection:

results/teps/gsc/<package_id>/gsc_tep.json

## Deliverables

* Run-scoped TEP output directory.
* Package-level convenience mirror.
* Historical TEP preservation across executions.

## Certification Outcome

Complies with:

```text
Contract Section 7.1
Contract Section 7.2
Contract Section 7.3
```

---

# Phase 2 — Manifest Integrity Compliance

## Contract Sections

```text
Section 5
Manifest Integrity Requirements
```

## Objective

Expose artifact verification authority.

## Current State

Artifact references exist.

Verification authority is only indirectly available through final_run_manifest.yaml.

## Target State

One of the following becomes explicit:

Option A

artifact_hash
hash_algorithm

per artifact.

Option B

checksum_authority:
final_run_manifest.yaml

at the manifest level.

## Deliverables

* Explicit checksum authority.
* Reconstruction documentation.
* Verification path visibility.

## Certification Outcome

Complies with:

```text
Contract Section 5.1
Contract Section 5.2
Contract Section 5.3
```

---

# Phase 3 — Namespace Identity Compliance

## Contract Sections

```text
Section 2
Identity Preservation Requirements
```

## Objective

Prevent namespace collapse during transport.

## Current State

TEPs preserve identifiers but do not always preserve explicit namespace information.

## Target State

Every transported identifier preserves namespace context.

Required additions:

gene_namespace
source_gene_namespace

and any supporting namespace metadata required by VDB brokerage.

## Deliverables

* Explicit namespace preservation.
* Namespace-aware identity records.
* Brokerage-compatible identifier transport.

## Certification Outcome

Complies with:

```text
Contract Section 2.2
Contract Section 2.3
```

---

# Phase 4 — Mapping Uncertainty Compliance

## Contract Sections

```text
Section 3
Mapping Uncertainty Preservation Requirements
```

## Objective

Preserve ambiguity rather than collapse ambiguity.

## Current State

Some compound identifier mappings may appear fully resolved.

## Target State

Ambiguous mappings become explicit uncertainty states.

Examples:

mapping_status: multi_mapped
mapping_uncertainty: one_to_many

and associated uncertainty annotations.

## Deliverables

* Multi-ID detection logic.
* Explicit uncertainty states.
* Preserved ambiguity visibility.

## Certification Outcome

Complies with:

```text
Contract Section 3.1
Contract Section 3.2
Contract Section 3.3
```

---

# Phase 5 — Source Contribution Compliance

## Contract Sections

```text
Section 4
Source Contribution Preservation Requirements
```

## Objective

Preserve source contribution topology.

## Current State

Current source attribution provides summary-level provenance.

Full source → semantics → channel → contribution relationships are not yet transported.

## Target State

Each semantic prior preserves source-level contribution records.

Example structure:

source_contributions:

* source_id
* source_gene_id
* source_gene_symbol
* evidence_semantics
* evidence_tier
* weight_tier
* semantic_channel
* scoring_active
* channel_score_contribution
* provenance_id

## Deliverables

* Source contribution transport model.
* Source contribution payload construction.
* Provenance-complete contribution lineage.

## Certification Outcome

Complies with:

```text
Contract Section 4.1
Contract Section 4.2
Contract Section 4.3
```

---

# Deferred Certification-Neutral Enhancements

The following items remain intentionally outside certification scope:

```text
payload.channel_summary population
portable TEP bundles
artifact embedding
cross-repository artifact replication
```

These may improve usability but are not required for certification.

---

# Certification Gate

A GSC-TEP may be considered certified only when all phases in this plan have been completed and validated against the certification contract.

Certification indicates compliance with:

```text
Identity Preservation
Mapping Uncertainty Preservation
Source Contribution Preservation
Manifest Integrity Preservation
Run Preservation
Retention Preservation
Scientific Non-Collapse Requirements
```

The objective is not merely successful transport.

The objective is preservation-aware transport that protects biological meaning across repository boundaries and through time.
