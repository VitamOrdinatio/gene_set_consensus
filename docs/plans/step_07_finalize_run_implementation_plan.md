# Step 07 Finalize Run Implementation Plan

## Purpose

Implement Step 07 for GSC run finalization.

Step 07 shall convert a validated run into an authoritative completed run by generating:

```text
final_run_manifest.yaml
```

This plan follows:

```text
docs/contracts/step_07_finalize_run_contract.md
docs/design/gsc_step07_finalization_model.md
docs/contracts/gsc_output_retention_contract.md
```

---

## Implementation Scope

Implement a new pipeline stage:

```text
scripts/step_07_finalize_run.py
```

Integrate it into:

```text
run_pipeline.py
```

No scientific output tables should be modified by Step 07.

Step 07 only verifies and finalizes run state.

---

## Inputs

Step 07 shall consume:

```text
results/runs/<run_id>/reports/<package_id>/run_manifest.yaml
results/runs/<run_id>/reports/<package_id>/output_contract_validation.tsv
```

The `run_id` and `package_id` shall be passed by `run_pipeline.py`.

---

## Outputs

Step 07 shall write:

```text
results/runs/<run_id>/reports/<package_id>/final_run_manifest.yaml
```

Step 07 shall also mirror this file to:

```text
results/reports/<package_id>/final_run_manifest.yaml
```

The run-scoped file is authoritative.

The package-scoped file is a convenience copy.

---

## Finalized Manifest Shape

The finalized manifest should include:

```yaml
run_id: run_...
phenotype: epilepsy
package_id: epilepsy_semantic_gtr_experimental
run_status: COMPLETE
validation_status: PASS
authoritative_run_directory: results/runs/run_...
execution_manifest: results/runs/run_.../reports/<package_id>/run_manifest.yaml
validation_artifact: results/runs/run_.../reports/<package_id>/output_contract_validation.tsv
execution_generated_at: ...
finalization_timestamp: ...
input_files:
  ...
output_files:
  ...
validation_files:
  ...
software_versions:
  ...
```

The `input_files` and `output_files` sections may be inherited from `run_manifest.yaml`.

The `validation_files` section shall include the output contract validation artifact and its hash.

---

## Validation Logic

Step 07 shall fail if:

* `run_manifest.yaml` is missing
* `output_contract_validation.tsv` is missing
* `output_contract_validation.tsv` contains any `error` rows
* any file referenced in `run_manifest.yaml` is missing
* final manifest cannot be written

Step 07 shall pass if:

* all required artifacts exist
* validation artifact contains no errors
* all manifest-referenced files exist
* final manifest is written successfully

---

## Validation Artifact Parsing

`output_contract_validation.tsv` has columns:

```text
level    message
```

Validation status logic:

```text
if any row has level == "error":
    validation_status = FAIL
else:
    validation_status = PASS
```

Warnings do not block finalization.

---

## Hashing Requirements

Step 07 shall compute SHA-256 hashes for:

```text
output_contract_validation.tsv
final_run_manifest.yaml
```

The finalized manifest shall include the hash of:

```text
output_contract_validation.tsv
```

The hash of `final_run_manifest.yaml` itself may be omitted from inside the manifest to avoid self-referential hashing.

---

## Recommended Helper Functions

Implement small internal helpers inside:

```text
scripts/step_07_finalize_run.py
```

Suggested helpers:

```python
load_yaml(path: Path) -> dict
sha256_file(path: Path) -> str
parse_validation_status(path: Path) -> str
assert_manifest_paths_exist(manifest: dict) -> None
build_final_manifest(...) -> dict
write_yaml(path: Path, data: dict) -> None
```

Keep Step 07 script-local for now.

If reused later by TEP builders, helpers can migrate into `src/gene_set_consensus/`.

---

## run_pipeline.py Integration

Add Step 07 after Step 06.

Execution order:

```text
step_01_validate_inputs
step_02_normalize_genes
step_03_build_source_matrix
step_04_score_consensus
step_05_write_outputs
step_06_validate_outputs
step_07_finalize_run
```

`run_pipeline.py` shall pass:

```text
--config
--phenotype
--phenotype-config
--run-id
--package-id
```

to Step 07.

---

## Logging

Step 07 shall log:

* run_id
* phenotype
* package_id
* execution_manifest_path
* validation_artifact_path
* final_manifest_path
* validation_status
* run_status

---

## Smoke Test

After implementation, run:

```bash
python run_pipeline.py \
  --release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml
```

Then confirm:

```bash
tree -L 6 results
```

Expected:

```text
results/runs/<run_id>/reports/<package_id>/
├── run_manifest.yaml
├── output_contract_validation.tsv
├── validation_report.md
└── final_run_manifest.yaml
```

and:

```text
results/reports/<package_id>/
├── run_manifest.yaml
├── output_contract_validation.tsv
├── validation_report.md
└── final_run_manifest.yaml
```

---

## Verification Commands

Check final manifest exists:

```bash
find results/runs -name final_run_manifest.yaml | sort
```

Inspect final manifest:

```bash
cat results/runs/<run_id>/reports/<package_id>/final_run_manifest.yaml
```

Verify no validation errors:

```bash
cut -f1 results/runs/<run_id>/reports/<package_id>/output_contract_validation.tsv | sort | uniq -c
```

Run tests:

```bash
pytest
```

---

## Acceptance Criteria

Implementation is complete when:

* Step 07 executes after Step 06
* successful runs produce `final_run_manifest.yaml`
* failed validation prevents finalization
* finalized manifest records `run_status: COMPLETE`
* finalized manifest records `validation_status: PASS`
* finalized manifest points to run-scoped authoritative artifacts
* latest reports mirror includes `final_run_manifest.yaml`
* existing pipeline behavior remains compatible
