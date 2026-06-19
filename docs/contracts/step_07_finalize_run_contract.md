# Step 07 Finalize Run Contract

## Purpose

Define the contract for GSC run finalization.

Step 07 establishes the authoritative preservation state for a completed GSC execution.

---

## Inputs

Step 07 requires:

```text
results/runs/run_<run_id>/reports/<package_id>/run_manifest.yaml
```

and

```text
results/runs/run_<run_id>/reports/<package_id>/output_contract_validation.tsv
```

Both artifacts must exist.

---

## Validation Requirements

Step 07 shall verify:

### Execution Manifest Exists

```text
run_manifest.yaml
```

must exist.

### Validation Artifact Exists

```text
output_contract_validation.tsv
```

must exist.

### Validation Status

Validation status must equal:

```text
PASS
```

### Manifest Integrity

All files referenced by:

```text
run_manifest.yaml
```

must exist.

---

## Outputs

Step 07 shall generate:

```text
results/runs/run_<run_id>/reports/<package_id>/final_run_manifest.yaml
```

---

## Finalized Manifest Requirements

The finalized manifest shall include:

### Execution Identity

* run_id
* phenotype
* package_id

### Validation Identity

* validation_status
* validation_artifact

### Preservation Identity

* authoritative_run_directory
* run_status

### Temporal Metadata

* execution_timestamp
* finalization_timestamp

### Artifact Provenance

* authoritative output artifacts
* authoritative output artifact hashes

---

## Success Conditions

Step 07 succeeds when:

* validation passed
* manifest integrity checks passed
* finalized manifest was written

and

```text
run_status = COMPLETE
```

is recorded.

---

## Failure Conditions

Step 07 shall fail if:

* execution manifest is missing
* validation artifact is missing
* validation status is not PASS
* manifest-referenced artifacts are missing
* finalized manifest cannot be written

No finalized manifest shall be generated for failed runs.

---

## Acceptance Criteria

GSC is compliant when:

* completed runs produce `final_run_manifest.yaml`
* failed runs do not produce `final_run_manifest.yaml`
* finalized manifests reference authoritative run-scoped artifacts
* downstream systems can determine run completeness from finalized manifests alone
