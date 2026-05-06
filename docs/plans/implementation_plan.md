# implementation_plan.md

# Implementation Plan: `gene_set_consensus`

## Document Control

| Field | Value |
|---|---|
| Repository | `gene_set_consensus` |
| Abbreviation | GSC |
| Artifact type | `implementation_plan` |
| Owning agent | DEX — SWE Agent |
| Intended location | `gene_set_consensus/docs/plans/implementation_plan.md` |
| Companion artifact | `gene_set_consensus/docs/contracts/system_contract.md` |
| Current target | v1.0 portfolio-ready repository |
| Implementation status | Pre-code action plan |

---

## 1. Objective

Build a reproducible Python/Bash pipeline that constructs phenotype-scoped, provenance-aware consensus gene sets from heterogeneous gene-list sources.

The minimal viable pipeline must:

1. ingest multiple source gene lists
2. validate input schemas
3. normalize identifiers
4. collapse within-source duplicates
5. aggregate genes across sources
6. construct a gene-source matrix
7. compute deterministic source-count and weighted consensus scores
8. preserve provenance
9. emit downstream-compatible TSV artifacts
10. produce logs, validation reports, and reproducibility manifests

---

## 2. Guiding Architecture

The pipeline should follow a simple stage-based flow:

```text
config
  ↓
validate inputs
  ↓
normalize gene identifiers
  ↓
build source-level normalized records
  ↓
build gene-source matrix
  ↓
compute source frequency and weighted consensus scores
  ↓
write consensus outputs and provenance tables
  ↓
validate outputs and reproducibility
```

Core design rule:

```text
scripts/ are thin execution wrappers.
src/gene_set_consensus/ contains reusable logic.
```

---

## 3. Development Phases

### Phase 0 — Repository Scaffold and Planning Artifacts

Goal: create the repo shell before writing pipeline logic.

Create:

```text
gene_set_consensus/
├── README.md
├── Makefile
├── run_pipeline.py
├── requirements.txt
├── .gitignore
├── config/
├── data/
├── docs/
├── environment/
├── logs/
├── results/
├── scripts/
├── src/
└── tests/
```

Then add:

```text
docs/maps/milestone_map.md
docs/contracts/system_contract.md
docs/plans/implementation_plan.md
docs/architecture.md
docs/methodology.md
docs/data_dictionary.md
docs/notes.md
```

Commit target:

```text
Initialize GSC repository scaffold
```

---

### Phase 1 — Example Data and Schemas

Goal: define small, safe, committable test data.

Create:

```text
data/example/source_a_genes.tsv
data/example/source_b_genes.tsv
data/example/source_c_genes.tsv
data/example/source_metadata.tsv
data/example/identifier_map.tsv
data/schemas/source_gene_list_schema.tsv
data/schemas/source_metadata_schema.tsv
data/schemas/consensus_gene_set_schema.tsv
```

Example gene-list files should intentionally include:

- repeated genes within one source
- same gene across multiple sources
- one deprecated/alias symbol
- one unresolved symbol
- one gene with stable ID
- one gene with symbol only

This makes validation meaningful from the beginning.

Commit target:

```text
Add example gene-set inputs and schemas
```

---

### Phase 2 — Configuration System

Goal: make all behavior config-driven.

Create:

```text
config/config.yaml
config/config.sys76.yaml
config/config.mark.yaml
config/phenotypes/example_phenotype.yaml
config/phenotypes/mitochondrial_disease.yaml
```

Implement module skeleton:

```text
src/gene_set_consensus/config.py
src/gene_set_consensus/models.py
```

Configuration must define:

- run environment
- input paths
- output paths
- phenotype ID
- source definitions
- source weights
- source tiers
- gene column mapping
- identifier normalization policy
- scoring model
- output options
- validation strictness

Do not hard-code thresholds or source weights.

Commit target:

```text
Add config-driven phenotype setup
```

---

### Phase 3 — Logging and Run Management

Goal: create robust logs before major transformation logic.

Create:

```text
src/gene_set_consensus/logging_utils.py
src/gene_set_consensus/io.py
```

Required behavior:

- generate `run_id`
- create run-scoped log directory
- create run-scoped interim/processed directories
- write `pipeline.log`
- write step-specific logs
- record config path and phenotype
- record input/output paths
- record warnings and failures

Run directory pattern:

```text
logs/{run_id}/
data/interim/{run_id}/
data/processed/{run_id}/
```

Commit target:

```text
Add run management and logging utilities
```

---

### Phase 4 — Input Validation

Goal: fail fast on invalid inputs.

Create:

```text
src/gene_set_consensus/validation.py
scripts/step_01_validate_inputs.py
scripts/validation/validate_input_schema.py
tests/unit/test_config.py
```

Validation checks:

- config exists
- phenotype config exists
- phenotype ID present
- at least one source present
- source IDs unique
- source weights numeric
- source files exist
- source files are TSV/CSV
- required gene columns present
- at least one gene identifier column present
- no empty source files
- output directories writable

Expected output:

```text
data/interim/{run_id}/input_validation_summary.tsv
logs/{run_id}/step_01_validate_inputs.log
```

Commit target:

```text
Implement input validation stage
```

---

### Phase 5 — Gene Identifier Normalization

Goal: normalize source records without losing original source information.

Create:

```text
src/gene_set_consensus/normalization.py
scripts/step_02_normalize_genes.py
tests/unit/test_normalization.py
scripts/validation/validate_identifier_mapping.py
```

Required behavior:

- preserve original input gene label
- strip whitespace
- normalize casing
- use identifier map when available
- resolve aliases where possible
- mark deprecated/resolved symbols
- flag ambiguous symbols
- flag unresolved symbols
- preserve source row number
- generate stable source record hash

Expected output:

```text
data/interim/{run_id}/normalized_source_records.tsv
```

Required columns:

```text
run_id
phenotype
source_id
source_name
source_type
weight_tier
source_weight
input_gene_symbol
normalized_gene_symbol
gene_id
mapping_status
evidence_label
source_row_number
source_record_hash
```

Commit target:

```text
Implement gene identifier normalization
```

---

### Phase 6 — Source Matrix Construction

Goal: create a deterministic gene × source matrix.

Create:

```text
src/gene_set_consensus/aggregation.py
scripts/step_03_build_source_matrix.py
tests/unit/test_aggregation.py
```

Required behavior:

- collapse duplicates within the same source
- preserve one contribution per gene per source
- aggregate across sources
- compute source membership indicators
- compute `source_count`
- compute `weighted_source_sum`
- produce deterministic column ordering
- preserve sparse single-source genes if configured

Expected outputs:

```text
data/processed/{run_id}/gene_source_matrix.tsv
data/processed/{run_id}/gene_frequency_table.tsv
```

Commit target:

```text
Implement source matrix aggregation
```

---

### Phase 7 — Consensus Scoring

Goal: implement deterministic, explainable v1 scoring.

Create:

```text
src/gene_set_consensus/scoring.py
scripts/step_04_score_consensus.py
tests/unit/test_scoring.py
```

Required v1 scoring:

```text
base_score = source_count
weighted_source_sum = sum(source_weight for contributing sources)
consensus_score = weighted_source_sum
```

Rules:

- preserve raw source count
- preserve weighted contribution
- use only configured weights
- fail if scoring mode unsupported
- do not compare across phenotypes
- do not use hidden amplification
- sort deterministically

Expected output:

```text
data/processed/{run_id}/scored_gene_evidence.tsv
```

Commit target:

```text
Implement deterministic consensus scoring
```

---

### Phase 8 — Provenance and Final Output Writing

Goal: emit downstream-compatible artifacts.

Create:

```text
src/gene_set_consensus/provenance.py
src/gene_set_consensus/reporting.py
scripts/step_05_write_outputs.py
tests/unit/test_provenance.py
```

Required final outputs:

```text
results/tables/{phenotype}/consensus_gene_set.tsv
results/tables/{phenotype}/gene_source_matrix.tsv
results/tables/{phenotype}/gene_frequency_table.tsv
results/tables/{phenotype}/gene_provenance.tsv
results/reports/{phenotype}/run_manifest.yaml
results/reports/{phenotype}/validation_report.md
```

`consensus_gene_set.tsv` must include:

```text
phenotype
gene_id
gene_symbol
consensus_score
source_count
weighted_source_sum
source_list
weight_tier_summary
mapping_status
provenance_id
run_id
gsc_version
generated_at
```

Commit target:

```text
Write consensus outputs and provenance tables
```

---

### Phase 9 — Output Validation

Goal: prove that the outputs satisfy the contract.

Create:

```text
scripts/step_06_validate_outputs.py
scripts/validation/validate_consensus_outputs.py
scripts/validation/validate_reproducibility.py
tests/validation/test_output_contract.py
```

Validation checks:

- all required files created
- all required columns present
- no duplicate final `(phenotype, gene_id)` records when `gene_id` exists
- source counts match source matrix
- weighted scores match source weights
- source list matches provenance rows
- unresolved identifiers reported
- output sort is deterministic
- manifest contains input/output hashes

Commit target:

```text
Add output validation checks
```

---

### Phase 10 — End-to-End Pipeline Entrypoint

Goal: make the repository runnable as a pipeline.

Implement:

```text
run_pipeline.py
Makefile
scripts/run_pipeline.sh
```

Expected commands:

```bash
python run_pipeline.py --config config/config.yaml --phenotype example_phenotype
make test
make run-example
```

`run_pipeline.py` should execute stages in order:

```text
01 validate inputs
02 normalize genes
03 build source matrix
04 score consensus
05 write outputs
06 validate outputs
```

Commit target:

```text
Add end-to-end pipeline runner
```

---

### Phase 11 — Unit, Integration, and Reproducibility Testing

Goal: make this a tested software project rather than a script collection.

Create tests:

```text
tests/unit/test_config.py
tests/unit/test_normalization.py
tests/unit/test_aggregation.py
tests/unit/test_scoring.py
tests/unit/test_provenance.py
tests/integration/test_example_pipeline.py
tests/validation/test_output_contract.py
```

Required test coverage:

- config parsing
- missing config failure
- source duplicate handling
- gene symbol normalization
- alias/deprecated symbol mapping
- ambiguous identifier flagging
- duplicate within-source collapse
- across-source count behavior
- weighted score calculation
- output schema
- provenance joinability
- repeated-run deterministic output

Commit target:

```text
Add tests for GSC pipeline behavior
```

---

### Phase 12 — GTR-Derived Input Support

Goal: satisfy v1 clinical-context integration milestone without overbuilding.

Approach:

- do not write a full GTR scraper in v1 unless already available
- ingest pre-exported GTR-derived TSV files
- treat GTR as one or more configured sources
- preserve condition/test/panel metadata if available

Recommended GTR TSV schema:

```text
condition_label
condition_id
test_name
test_id
panel_name
gene_symbol
gene_id
source_version
download_date
```

Create:

```text
src/gene_set_consensus/gtr.py
scripts/validation/validate_gtr_source.py
tests/unit/test_gtr.py
```

Expected output behavior:

- GTR-derived genes contribute like other sources
- GTR provenance retains condition/test/panel context
- GTR evidence remains phenotype-scoped
- GTR does not become sample-specific

Commit target:

```text
Add GTR-derived source ingestion support
```

---

### Phase 13 — VDB/RDGP Compatibility Checks

Goal: make GSC downstream-compatible without implementing downstream repos.

Add validation checks:

```text
scripts/validation/validate_vdb_rdgp_compatibility.py
```

Check that final outputs contain:

```text
phenotype
gene_id
gene_symbol
consensus_score
source_list
source_count
```

Check invalid conditions:

- missing phenotype
- missing both `gene_id` and `gene_symbol`
- duplicate `(phenotype, gene_id)`
- output lacks provenance trace
- RDGP-style `sample_id` appears in GSC output

Commit target:

```text
Add downstream compatibility validation
```

---

### Phase 14 — MARK Probe Harnesses

Goal: support MARK execution and Guacamole-safe debugging.

Create:

```text
scripts/mark_probes/mark_smoketest_gsc.sh
scripts/mark_probes/mark_run_gsc_example.sh
```

Probe behavior:

- run from MARK `~/Desktop/`
- `cd` into `/root/dev/portfolio_projects/gene_set_consensus`
- activate `.venv`
- run tests or example pipeline
- write repo logs under `logs/{run_id}/`
- write downloadable probe log to `~/Desktop/`

Example probe log:

```text
~/Desktop/gsc_mark_smoketest_{timestamp}.log
```

Commit target:

```text
Add MARK smoke-test probes
```

---

### Phase 15 — Documentation Completion

Goal: make the repository legible to outside reviewers.

Create or finalize:

```text
README.md
docs/architecture.md
docs/methodology.md
docs/data_dictionary.md
docs/notes.md
docs/contracts/system_contract.md
docs/plans/implementation_plan.md
```

README must explain:

- what GSC does
- what GSC does not do
- why phenotype scope matters
- example inputs
- example outputs
- how to run the pipeline
- how to run tests
- how outputs integrate with RDGP/VDB/RSP
- assumptions
- limitations
- edge cases
- validation strategy

Commit target:

```text
Document GSC architecture and usage
```

---

## 4. Minimal Viable Pipeline Definition

The MVP is complete when this command works:

```bash
python run_pipeline.py --config config/config.yaml --phenotype example_phenotype
```

and produces:

```text
results/tables/example_phenotype/consensus_gene_set.tsv
results/tables/example_phenotype/gene_source_matrix.tsv
results/tables/example_phenotype/gene_frequency_table.tsv
results/tables/example_phenotype/gene_provenance.tsv
results/reports/example_phenotype/run_manifest.yaml
results/reports/example_phenotype/validation_report.md
logs/{run_id}/pipeline.log
```

The MVP must include tests for:

- duplicate handling
- source counting
- scoring
- provenance
- output schema

---

## 5. v1.0 Release Definition

GSC v1.0 is complete when the repository supports:

- phenotype-specific multi-source aggregation
- explicit source weighting
- provenance-preserving final outputs
- GTR-derived input ingestion
- VDB/RDGP-compatible output schema
- end-to-end example run
- local sys76 run
- MARK smoke test
- validation report
- reproducibility checksum
- documented assumptions, limitations, edge cases, validation, and implementation notes

---

## 6. Implementation Order Summary

```text
0. scaffold repo and docs
1. add example data and schemas
2. add config system
3. add logging/run management
4. implement input validation
5. implement gene normalization
6. implement aggregation/matrix construction
7. implement consensus scoring
8. write final outputs/provenance
9. validate outputs
10. add end-to-end runner
11. add tests
12. add GTR-derived input support
13. add VDB/RDGP compatibility checks
14. add MARK probes
15. complete documentation
```

---

## 7. Suggested Commit Sequence

```text
Initialize GSC repository scaffold
Add planning artifacts for GSC architecture
Add example gene-set inputs and schemas
Add config-driven phenotype setup
Add run management and logging utilities
Implement input validation stage
Implement gene identifier normalization
Implement source matrix aggregation
Implement deterministic consensus scoring
Write consensus outputs and provenance tables
Add output validation checks
Add end-to-end pipeline runner
Add tests for GSC pipeline behavior
Add GTR-derived source ingestion support
Add downstream compatibility validation
Add MARK smoke-test probes
Document GSC architecture and usage
```

---

## 8. Testing Plan

### Unit Tests

Test individual functions:

- config loading
- source metadata parsing
- identifier normalization
- duplicate collapse
- source matrix construction
- scoring
- provenance ID generation
- output sorting

### Integration Tests

Test full example pipeline:

```bash
pytest tests/integration/
```

Expected assertions:

- pipeline exits successfully
- expected outputs exist
- row counts match fixture expectations
- consensus scores match expected values
- provenance rows join to consensus rows
- no sample-specific fields appear

### Validation Tests

Test output contract:

```bash
python scripts/validation/validate_consensus_outputs.py \
  --consensus results/tables/example_phenotype/consensus_gene_set.tsv \
  --provenance results/tables/example_phenotype/gene_provenance.tsv
```

### Reproducibility Test

Run example twice and compare deterministic output hashes.

Exclude from checksum comparison:

- log files
- generated timestamps
- run manifest timestamp fields

Include in checksum comparison:

- `consensus_gene_set.tsv`
- `gene_source_matrix.tsv`
- `gene_frequency_table.tsv`
- `gene_provenance.tsv`

---

## 9. Logging Plan

Every run must create:

```text
logs/{run_id}/pipeline.log
logs/{run_id}/step_01_validate_inputs.log
logs/{run_id}/step_02_normalize_genes.log
logs/{run_id}/step_03_build_source_matrix.log
logs/{run_id}/step_04_score_consensus.log
logs/{run_id}/step_05_write_outputs.log
logs/{run_id}/step_06_validate_outputs.log
```

Every log should include:

- run ID
- phenotype
- timestamp
- input file paths
- row counts
- warnings
- validation failures
- output file paths
- completion status

MARK probe logs should be downloadable from:

```text
/root/Desktop/
```

or equivalently:

```text
~/Desktop/
```

inside MARK.

---

## 10. Reproducibility Plan

Reproducibility requires:

- config-driven execution
- no hard-coded paths
- input file hashes
- output file hashes
- deterministic sorting
- explicit source weights
- preserved run manifest
- versioned phenotype config
- stable schema
- tests using example data
- local and MARK smoke tests

---

## 11. Data Management Plan

### Git-Tracked

Allowed in repo:

- small example TSV files
- schema files
- small fixture files
- config templates
- tests
- scripts
- source code
- docs

### Not Git-Tracked

Do not commit:

- large GTR exports
- large MitoCarta exports if bulky
- database dumps
- downloaded raw external datasets
- large generated outputs
- local virtual environments
- MARK logs downloaded from Desktop unless curated and small

### Storage Locations

sys76:

```text
/mnt/storage/gene_sets
/mnt/storage/gtr
/mnt/storage/databases
```

MARK:

```text
/data/storage/gene_sets
/data/storage/gtr
/data/storage/databases
```

---

## 12. Environment Plan

Use one repo-local virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` should start minimal:

```text
pandas
pyyaml
pytest
```

Optional later dependencies:

```text
pandera
pydantic
rich
```

Do not require Docker for v1.

---

## 13. Interface Compliance Plan

### GSC ↔ RDGP

GSC final outputs must be phenotype-scoped:

```text
(phenotype, gene_id)
```

RDGP integration must require selected phenotype context.

Forbidden in GSC outputs:

```text
sample_id
variant_id
zygosity
clinical_significance_per_sample
rdgp_score
```

### GSC ↔ VDB

GSC outputs must preserve:

```text
gene_id
gene_symbol
```

to support joins to VDB gene tables.

### GSC ↔ RSP

Future RSP evidence may be accepted only as gene-level functional evidence. It must not convert GSC into a sample-level repository.

### GSC ↔ VAP

VAP may consume GSC outputs as annotation context. GSC must not depend on VAP to run.

---

## 14. Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Gene symbol aliases mis-normalized | False consensus records | Use explicit mapping table and mapping status |
| Duplicate genes inflate source count | Inflated score | Collapse within-source duplicates |
| Missing gene IDs reduce VDB joinability | Weak downstream integration | Preserve symbol fallback and unresolved flags |
| Source weights become hidden assumptions | Unexplainable score | Require weights in phenotype config |
| GTR data format varies | Parser fragility | Ingest normalized GTR-derived TSV first |
| Phenotype definitions differ across sources | Mixed evidence context | Require phenotype-specific configs |
| Scores compared across phenotypes | Invalid interpretation | Document and block cross-phenotype comparison |
| MARK clipboard instability slows debugging | Lost execution context | Use MARK probes and file-based logs |
| Large data accidentally committed | Repo bloat | Use `.gitignore` and storage paths |
| GSC drifts into RDGP | Scope contamination | Block sample-specific fields in validation |

---

## 15. Assumptions

- The first implementation will use small local example data.
- Source gene lists can be represented as TSV/CSV.
- Source authority can be encoded as deterministic numeric weights.
- A static identifier map is acceptable for v1.
- GTR integration can begin from pre-exported/normalized GTR-derived TSV.
- sys76 is used for development and local testing.
- MARK is used for smoke testing and scaled runs if needed.
- Python/Bash are sufficient for v1.

---

## 16. Limitations

- v1 scoring is heuristic, not probabilistic.
- v1 does not solve phenotype ontology harmonization.
- v1 does not automate external database download.
- v1 does not automate literature mining.
- v1 does not include RNA-seq analysis.
- v1 does not perform enrichment analysis.
- v1 does not include a production database unless later justified.
- v1 identifier normalization may be incomplete.

---

## 17. Edge Cases to Test Explicitly

- same gene appears twice in one source
- same gene appears in three sources
- gene appears only in low-weight source
- gene appears only in high-weight source
- deprecated symbol resolves to current symbol
- ambiguous symbol flagged
- missing gene ID allowed under fallback mode
- missing gene ID fails under strict mode
- GTR source has same gene repeated across multiple panels
- source file is empty
- phenotype config has duplicate source ID
- source weight is missing
- output contains accidental `sample_id`

---

## 18. Validation Strategy

Before v1.0 release, perform:

1. local example run on sys76
2. repeated local run with checksum comparison
3. unit test suite
4. integration test suite
5. validation script on final outputs
6. manual spot-check of 3–5 known phenotype genes
7. GTR-derived input run
8. downstream compatibility validation
9. MARK smoke test using probe script
10. README usage review from fresh clone perspective

---

## 19. First Build Slice

The first implementation slice should stop after a working MVP using example data.

Build only:

```text
config parsing
input validation
normalization
aggregation
scoring
output writing
basic tests
```

Do not build GTR integration, MARK probes, or advanced documentation until the MVP works.

This prevents overbuilding before the core contract is proven.

---

## 20. Final Implementation Principle

GSC should be built as a small, serious, inspectable system.

The winning architecture is not clever. It is:

```text
clear inputs
explicit configuration
auditable transformations
deterministic outputs
preserved provenance
validated contracts
```

That is the engineering standard for this repository.
