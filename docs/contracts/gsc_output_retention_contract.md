# GSC Output Retention Contract

## Purpose

Define the authoritative retention requirements for GSC outputs.

This contract establishes which artifacts are authoritative, which artifacts are convenience exports, and which artifacts must be preserved to support historical reproducibility, provenance reconstruction, and GSC-TEP generation.

---

## Preservation Philosophy

GSC is a scientific evidence producer.

A completed GSC execution represents a historical scientific interpretation produced from:

* specific source releases
* specific identifier maps
* specific phenotype definitions
* specific scoring policies
* specific pipeline versions

Historical executions must remain reconstructable.

GSC therefore distinguishes between:

```text
authoritative run artifacts
```

and

```text
convenience export artifacts
```

---

## Authoritative Artifacts

The following locations constitute the authoritative producer record.

### Run-Scoped Intermediate Artifacts

```text
data/interim/run_<run_id>/
```

Examples:

* normalized_source_records.tsv
* mapping_summary.tsv
* input_validation_summary.tsv

### Run-Scoped Processed Artifacts

```text
data/processed/run_<run_id>/
```

Examples:

* gene_source_matrix.tsv
* gene_frequency_table.tsv
* scored_gene_evidence.tsv

### Run-Scoped Final Export Artifacts

```text
results/runs/run_<run_id>/
```

Examples:

```text
results/runs/run_<run_id>/tables/<package_id>/
results/runs/run_<run_id>/reports/<package_id>/
```

These artifacts represent the authoritative producer outputs used for release reconstruction and TEP generation.

---

## Convenience Artifacts

The following locations are convenience views only.

```text
results/tables/<package_id>/
results/reports/<package_id>/
```

These locations may be overwritten by subsequent executions.

These locations exist to simplify:

* human inspection
* downstream development
* latest-release access

These locations are not authoritative.

---

## Manifest Lifecycle Requirements

GSC distinguishes between:

```text
run_manifest.yaml
```

and

```
final_run_manifest.yaml
```

### Execution Manifest

Each run shall generate an execution manifest:

`run_manifest.yaml`

The execution manifest records the state of the pipeline immediately following output generation.

The execution manifest shall preserve:

- run_id
- phenotype identity
- package identity
- source manifest reference
- source manifest hash
- input artifact hashes
- output artifact hashes
- software versions
- execution timestamp

The execution manifest represents the state of the run prior to final validation and finalization.

---

### Finalized Manifest

Each successfully completed run shall generate:

`final_run_manifest.yaml`

The finalized manifest serves as the authoritative preservation artifact for the run.

The finalized manifest shall incorporate:

- execution manifest information
- validation status
- validation artifact references
- finalization timestamp
- authoritative run directory reference
- completed run status

The finalized manifest represents the complete scientific execution record for the run.

---

## Run Finalization Requirements

GSC shall perform a finalization step after output contract validation.

The finalization step shall:

* verify validation completion
* verify authoritative output presence
* verify manifest-referenced artifacts exist
* generate a finalized manifest

The finalized manifest shall be written to:

```text
results/runs/run_<run_id>/reports/<package_id>/final_run_manifest.yaml
```

This artifact becomes the authoritative preservation anchor for the completed run.

Downstream systems should prefer the finalized manifest when available.

---

## TEP Requirements

GSC-TEPs must reference authoritative producer artifacts.

TEP manifests shall reference:

```text
results/runs/run_<run_id>/
```

and not mutable convenience export locations.

---

## Authoritative Hierarchy

```text
data/interim/run_<run_id>
        ↓
data/processed/run_<run_id>
        ↓
results/runs/run_<run_id>
        ↓
final_run_manifest.yaml
        ↓
GSC-TEP
```

The finalized manifest defines the authoritative preservation boundary between GSC execution artifacts and downstream consumers.

---

## Acceptance Criteria

GSC is compliant when:

* multiple executions create independent run-scoped records
* historical run artifacts remain preserved
* final export artifacts remain preserved
* TEP construction can reference immutable producer outputs
* historical scientific state remains reconstructable

```
