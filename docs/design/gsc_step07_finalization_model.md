# GSC Step 07 Finalization Model

## Purpose

Define the responsibilities of the GSC run finalization stage.

Step 07 exists to establish a single authoritative preservation anchor for a completed GSC execution.

This stage is intentionally separate from output generation and output validation.

---

## Architectural Motivation

Prior to Step 07, GSC generated:

```text
run_manifest.yaml
```

during output generation and:

```text
output_contract_validation.tsv
```

during output validation.

While both artifacts are important, neither independently answers:

```text
Was this run successfully completed?

Was validation successful?

What constitutes the authoritative preserved execution state?
```

Step 07 resolves this ambiguity.

---

## Lifecycle Position

```text
Step 05
Output Generation
        ↓
run_manifest.yaml
        ↓

Step 06
Output Validation
        ↓
output_contract_validation.tsv
        ↓

Step 07
Run Finalization
        ↓
final_run_manifest.yaml
```

---

## Inputs

Step 07 consumes:

```text
results/runs/run_<run_id>/reports/<package_id>/run_manifest.yaml
```

and

```text
results/runs/run_<run_id>/reports/<package_id>/output_contract_validation.tsv
```

These artifacts are considered authoritative inputs.

---

## Validation Responsibilities

Step 07 shall verify:

### Manifest Presence

```text
run_manifest.yaml exists
```

### Validation Presence

```text
output_contract_validation.tsv exists
```

### Validation Success

Output validation status must indicate:

```text
PASS
```

### Referenced Artifact Presence

Every artifact referenced within:

```text
run_manifest.yaml
```

must still exist.

This protects against accidental deletion or partial run corruption.

---

## Finalization Responsibilities

Step 07 shall:

### Establish Completion Status

Determine:

```text
run_status = COMPLETE
```

only if all validation requirements succeed.

---

### Establish Validation Status

Record:

```text
validation_status = PASS
```

or

```text
validation_status = FAIL
```

---

### Establish Preservation Anchor

Record the authoritative run directory:

```text
results/runs/run_<run_id>
```

This becomes the preserved execution root.

---

### Establish Finalization Timestamp

Record:

```text
finalization_timestamp
```

separately from execution timestamp.

This distinguishes:

```text
when outputs were generated
```

from

```text
when the run became authoritative
```

---

## Output

Step 07 generates:

```text
results/runs/run_<run_id>/reports/<package_id>/final_run_manifest.yaml
```

This file becomes the authoritative preservation artifact for the completed execution.

---

## Finalized Manifest Responsibilities

The finalized manifest shall preserve:

### Execution Identity

* run_id
* phenotype
* package_id

### Source Identity

* source manifest
* source manifest hash

### Execution Provenance

* software versions
* execution timestamp

### Validation Provenance

* validation status
* validation artifact reference

### Artifact Provenance

* authoritative output artifact list
* authoritative output artifact hashes

### Finalization Metadata

* run_status
* finalization_timestamp
* authoritative_run_directory

---

## Downstream Usage

Downstream systems should prefer:

```text
final_run_manifest.yaml
```

over:

```text
run_manifest.yaml
```

when available.

The finalized manifest represents the completed and validated execution state.

---

## TEP Integration

Future GSC-TEP construction should reference:

```text
final_run_manifest.yaml
```

rather than:

```text
run_manifest.yaml
```

This ensures that GSC-TEPs originate only from:

* completed runs
* validated runs
* finalized runs

and never from partially completed execution state.

---

## Design Principle

Step 07 does not generate new scientific evidence.

Step 07 generates scientific execution certainty.

Its purpose is not to alter results.

Its purpose is to establish a durable preservation boundary between:

```text
GSC execution
```

and

```text
downstream consumers
```
