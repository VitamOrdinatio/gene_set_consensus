# GSC TEP Portability Boundary

## Purpose

Define the current portability boundary of GSC Transitional Evidence Products.

This document distinguishes between reference-based TEP transport and fully portable TEP bundles, and records the intentional decision to implement reference-based GSC-TEPs for the current repository maturity stage.

---

## Current Model

GSC currently implements reference-based TEPs.

A GSC-TEP is emitted as:

```text
results/teps/gsc/<package_id>/gsc_tep.json
```

This JSON artifact contains:

* a transport envelope
* a source artifact manifest
* a semantic prior payload

The TEP payload is sufficient for VDB ingestion.

The TEP manifest preserves references to authoritative producer artifacts under:

```text
results/runs/<run_id>/
```

These artifacts remain inside the GSC repository and define the producer-side evidentiary record.

---

## Reference-Based TEP Semantics

A reference-based GSC-TEP means:

```text
gsc_tep.json transports evidence and provenance references.
```

It does not mean:

```text
gsc_tep.json physically contains every producer-side artifact.
```

The TEP is therefore sufficient for routine downstream ingestion but depends on the preserved GSC repository state for complete audit reconstruction.

---

## Authoritative Producer Boundary

The authoritative GSC producer boundary is:

```text
results/runs/<run_id>/
```

This run-scoped directory preserves:

* final_run_manifest.yaml
* run_manifest.yaml
* output_contract_validation.tsv
* validation_report.md
* consensus_gene_set.tsv
* gene_provenance.tsv
* gene_source_matrix.tsv
* gene_frequency_table.tsv

The TEP manifest points to these artifacts.

The producer-side run directory remains the source of audit truth.

---

## What VDB Needs Today

For normal ingestion, VDB requires:

```text
results/teps/gsc/<package_id>/gsc_tep.json
```

The JSON contains the semantic prior payload and enough envelope metadata to identify:

* source repository
* package identity
* release identity
* run identity
* validation status
* finalization state

For audit reconstruction, VDB may follow the manifest references back to:

```text
results/runs/<run_id>/
```

---

## Current Limitation

Reference-based TEPs are not fully machine-independent archival capsules.

If the original GSC repository state is lost, relocated without preservation, or not archived, then the TEP payload may remain ingestible but complete producer-side audit reconstruction may be impaired.

This is an acknowledged portability limitation.

---

## Why Full Portability Is Deferred

Fully portable TEPs would require bundling producer-side artifacts into a self-contained evidence capsule.

For GSC, this is tractable.

For larger producers such as VAP, fully portable TEPs may become very large and operationally expensive because source and intermediate artifacts can be substantial.

The current portfolio objective is to demonstrate:

* deterministic execution
* preservation-aware producer design
* finalized-run provenance
* VDB-ready evidence transport
* clear future extensibility

Full archival portability is therefore intentionally deferred rather than treated as a missing feature.

---

## Future Portable TEP Model

A future portable TEP bundle may take the form:

```text
gsc_tep_bundle.tar.gz
```

containing:

* gsc_tep.json
* final_run_manifest.yaml
* run_manifest.yaml
* output_contract_validation.tsv
* validation_report.md
* consensus_gene_set.tsv
* gene_provenance.tsv
* gene_source_matrix.tsv
* gene_frequency_table.tsv
* bundle_manifest.yaml

Such a bundle would convert the current reference-based TEP into a machine-independent evidence capsule.

---

## Migration Path

The current architecture was designed to preserve a clean migration path.

Because GSC now emits:

```text
results/runs/<run_id>/
```

as a complete finalized producer boundary, future portable TEP construction can package this boundary without changing scientific evidence generation semantics.

This means portability can be added later as a transport-layer enhancement rather than a producer-side redesign.

---

## Design Decision

GSC currently ships reference-based TEPs.

This decision is intentional.

Reference-based TEPs are appropriate for the current repository stage because they demonstrate VDB-ready evidence transport while avoiding premature archival complexity.

Portable TEP bundles remain a planned future extension for environments where long-term machine-independent evidence preservation is required.

---

## Summary

Current state:

```text
GSC finalized run
        ↓
reference-based GSC-TEP
        ↓
VDB ingestion
```

Future state:

```text
GSC finalized run
        ↓
portable GSC-TEP bundle
        ↓
machine-independent VDB ingestion and audit
```

The present architecture supports both models, but implements only the reference-based model today.
