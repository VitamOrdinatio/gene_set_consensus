# GSC TEP Finalized Run Implementation Plan

## Purpose

Update GSC-TEP construction so every TEP is built from finalized GSC run state rather than mutable package-scoped convenience outputs.

This plan implements:

```text
docs/contracts/gsc_tep_finalized_run_contract.md
```

---

## Current Problem

Existing GSC-TEP construction was designed before Step 07 finalization.

It may still assume authoritative artifacts live under:

```text
results/tables/<package_id>/
results/reports/<package_id>/
```

These paths are now convenience mirrors only.

---

## Target Behavior

GSC-TEP construction shall use:

```text
results/runs/<run_id>/reports/<package_id>/final_run_manifest.yaml
```

as the authoritative producer anchor.

A TEP shall only be built when:

```text
run_status: COMPLETE
validation_status: PASS
```

---

## Implementation Scope

Update:

```text
src/gene_set_consensus/tep/
scripts/tep/build_gsc_tep.py
```

as needed.

Likely affected modules:

```text
src/gene_set_consensus/tep/envelope.py
src/gene_set_consensus/tep/manifest.py
src/gene_set_consensus/tep/payload.py
src/gene_set_consensus/tep/builder.py
```

---

## Proposed CLI Behavior

Support finalized-run construction:

```bash
python scripts/tep/build_gsc_tep.py \
  --final-run-manifest results/runs/<run_id>/reports/<package_id>/final_run_manifest.yaml
```

Optional convenience form:

```bash
python scripts/tep/build_gsc_tep.py \
  --run-id <run_id> \
  --package-id <package_id>
```

The old form:

```bash
python scripts/tep/build_gsc_tep.py \
  --release-id <package_id>
```

should either be deprecated or treated as latest-only convenience mode.

---

## Output Layout

Authoritative TEP output:

```text
results/teps/gsc/<package_id>/<run_id>/gsc_tep.json
```

Convenience mirror:

```text
results/teps/gsc/<package_id>/gsc_tep.json
```

The run-scoped TEP is authoritative.

The package-scoped TEP is latest convenience.

---

## Envelope Updates

TEP envelope shall include:

```yaml
run_id:
package_id:
package_version:
release_id:
phenotype:
validation_status:
run_status:
finalization_timestamp:
source_final_run_manifest:
```

The envelope should identify the TEP as derived from finalized run state.

---

## Manifest Updates

TEP manifest shall reference authoritative run-scoped artifacts only.

It should use paths and hashes from:

```text
final_run_manifest.yaml
```

TEP manifest should include:

```yaml
source_final_run_manifest:
authoritative_run_directory:
source_artifacts:
  consensus_gene_set.tsv:
  gene_provenance.tsv:
  gene_source_matrix.tsv:
  gene_frequency_table.tsv:
  validation_report.md:
  output_contract_validation.tsv:
```

No source artifact path should point to:

```text
results/tables/<package_id>/
results/reports/<package_id>/
```

---

## Payload Updates

Payload construction shall read:

```text
results/runs/<run_id>/tables/<package_id>/consensus_gene_set.tsv
```

not:

```text
results/tables/<package_id>/consensus_gene_set.tsv
```

Payload identity fields shall preserve:

```yaml
phenotype:
package_id:
release_id:
run_id:
gene_id:
gene_symbol:
```

---

## Validation Rules

TEP construction shall fail if:

* `final_run_manifest.yaml` is missing
* `run_status` is not `COMPLETE`
* `validation_status` is not `PASS`
* referenced consensus table is missing
* referenced provenance/validation artifacts are missing
* any TEP source artifact path points to mutable latest outputs

---

## Smoke Test: Epilepsy

Run GSC:

```bash
python run_pipeline.py \
  --release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml
```

Locate final manifest:

```bash
find results/runs -path "*epilepsy_semantic_gtr_experimental/final_run_manifest.yaml"
```

Build TEP:

```bash
python scripts/tep/build_gsc_tep.py \
  --final-run-manifest results/runs/<run_id>/reports/epilepsy_semantic_gtr_experimental/final_run_manifest.yaml
```

Verify:

```bash
jq '.envelope.run_id' results/teps/gsc/epilepsy_semantic_gtr_experimental/<run_id>/gsc_tep.json

jq '.envelope.validation_status' results/teps/gsc/epilepsy_semantic_gtr_experimental/<run_id>/gsc_tep.json

jq '.manifest.source_final_run_manifest' results/teps/gsc/epilepsy_semantic_gtr_experimental/<run_id>/gsc_tep.json
```

Expected:

```text
run_id matches finalized run
validation_status == PASS
manifest references final_run_manifest.yaml
```

---

## Smoke Test: Mitochondrial

Run GSC:

```bash
python run_pipeline.py \
  --release config/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml
```

Build TEP from finalized run manifest:

```bash
python scripts/tep/build_gsc_tep.py \
  --final-run-manifest results/runs/<run_id>/reports/mitochondrial_semantic_gtr_experimental/final_run_manifest.yaml
```

Verify payload count:

```bash
jq '.payload.semantic_prior_count' results/teps/gsc/mitochondrial_semantic_gtr_experimental/<run_id>/gsc_tep.json
```

---

## Acceptance Criteria

Implementation is complete when:

* TEP builder accepts `--final-run-manifest`
* TEP construction rejects non-finalized runs
* TEP source artifacts are run-scoped
* TEP output is run-scoped
* latest TEP mirror is optional/convenience only
* epilepsy GSC-TEP builds from finalized run state
* mitochondrial GSC-TEP builds from finalized run state
* TEP envelope preserves run, package, release, phenotype, and validation identity
