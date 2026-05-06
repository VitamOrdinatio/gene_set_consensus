# system_contract.md

# System Contract: `gene_set_consensus`

## Document Control

| Field | Value |
|---|---|
| Repository | `gene_set_consensus` |
| Abbreviation | GSC |
| Artifact type | `system_contract` |
| Owning agent | DEX — SWE Agent |
| Intended location | `gene_set_consensus/docs/contracts/system_contract.md` |
| Companion artifact | `gene_set_consensus/docs/plans/implementation_plan.md` |
| Current target | v1.0 portfolio-ready repository |
| Implementation status | Pre-code architecture contract |

---

## 1. Contract Purpose

This system contract defines the architectural, data, interface, validation, and reproducibility obligations for the `gene_set_consensus` repository.

GSC is a phenotype-aware, gene-level evidence aggregation system. It transforms heterogeneous phenotype-associated gene lists into deterministic, provenance-aware, consensus-scored gene-level evidence artifacts.

This contract exists to prevent schema drift and scope creep before implementation begins.

---

## 2. System Role

GSC is the **overlay layer** in the broader computational biology repository ecosystem.

```text
VAP / VDB / RSP / GSC / RDGP ecosystem

VDB  → variant-centric evidence storage
GSC  → phenotype-scoped gene-level evidence overlay
RSP  → future functional/transcriptomic evidence overlay
RDGP → sample-scoped gene prioritization and reasoning layer
```

GSC does **not** perform variant calling, variant annotation, variant-to-gene aggregation, transcriptomics analysis, enrichment analysis, sample-level prioritization, or diagnostic interpretation.

GSC answers:

```text
For a selected phenotype, which genes have the strongest support across multiple gene-list evidence sources?
```

---

## 3. Governing Inputs

This contract is constrained by:

1. `DEX_swe_agent/README.md`
2. `agent_bundle.md`
3. `environment_bundle.md`
4. `governance_bundle.md`
5. `interface_bundle.md`
6. `roadmap.md`
7. `repo_brief.md`
8. `milestone_map.md`

When conflicts occur, the following precedence applies:

1. Interface specifications
2. Research standards and scientific correctness
3. Repo brief
4. Milestone map
5. Artifact conventions
6. Pipeline conventions
7. Project and naming conventions
8. Testing conventions
9. Environment/storage conventions
10. Roadmap/portfolio strategy

---

## 4. Non-Negotiable Invariants

The implementation must preserve these invariants.

### 4.1 Identity Invariant

The primary GSC evidence record is:

```text
(phenotype, gene_id)
```

If `gene_id` is unavailable in early-stage inputs, the implementation may use a normalized `gene_symbol` as a provisional key, but final downstream-compatible outputs must preserve a `gene_id` field and explicitly flag unresolved identifiers.

### 4.2 Phenotype Scope Invariant

Each run is scoped to one phenotype context.

Valid examples:

```text
mitochondrial_disease
epilepsy
polg_related_disorders
```

Invalid behavior:

```text
single unscoped universal consensus score per gene
```

### 4.3 Non-Sample-Specific Invariant

GSC must not contain:

- `sample_id`
- sample-level genotype fields
- variant counts per sample
- zygosity
- patient-specific evidence
- RDGP ranking outputs

Those belong downstream.

### 4.4 Variant Independence Invariant

GSC must not perform variant-level evidence aggregation. It may be joinable to VDB by `gene_id` or `gene_symbol`, but it must not reinterpret variants.

### 4.5 Provenance Invariant

Every consensus record must be explainable by its contributing sources.

At minimum:

```text
phenotype
gene_id
gene_symbol
source_list
source_count
consensus_score
provenance
```

### 4.6 Determinism Invariant

Same config + same inputs + same code version must produce the same outputs.

This requires:

- deterministic sorting
- deterministic score calculation
- explicit config paths
- no hidden defaults
- explicit source weights
- stable output schemas
- reproducibility checks

---

## 5. Pipeline Boundary

### 5.1 In Scope

GSC v1 must support:

- ingestion of heterogeneous gene-list inputs
- source metadata parsing
- phenotype configuration parsing
- gene identifier normalization
- duplicate resolution
- gene-source matrix construction
- source-frequency counting
- authority-aware weighted scoring
- provenance-preserving consensus output
- versioned phenotype-specific artifacts
- basic GTR-derived source integration
- VDB/RDGP/RSP-compatible output fields
- validation reports
- reproducibility checks

### 5.2 Out of Scope

GSC v1 must not implement:

- variant calling
- VCF parsing
- BAM/FASTQ processing
- variant interpretation
- sample-specific prioritization
- RDGP scoring
- RNA-seq differential expression
- enrichment analysis
- GO/MSigDB overrepresentation analysis
- ontology-based phenotype reasoning
- automated literature mining
- black-box machine learning weighting

---

## 6. Canonical Execution Model

GSC is a config-driven Python/Bash pipeline.

Expected execution pattern:

```bash
python run_pipeline.py --config config/config.yaml --phenotype mitochondrial_disease
```

Alternative convenience entry points may include:

```bash
make run
bash scripts/run_pipeline.sh
```

All execution paths must call the same core pipeline logic.

---

## 7. Repository Path Contract

### 7.1 sys76 Development Path

```text
/home/steelsparrow/dev/portfolio_projects/gene_set_consensus
```

### 7.2 MARK Execution Path

```text
/root/dev/portfolio_projects/gene_set_consensus
```

### 7.3 Large Gene-Set Storage

Large or externally downloaded gene-set data must live outside Git.

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

Repo-local `data/` is for small examples, small fixtures, test data, and lightweight reproducibility assets.

---

## 8. Required Repository Structure

```text
gene_set_consensus/
├── README.md
├── Makefile
├── run_pipeline.py
├── requirements.txt
├── .gitignore
├── config/
│   ├── config.yaml
│   ├── config.sys76.yaml
│   ├── config.mark.yaml
│   └── phenotypes/
│       ├── mitochondrial_disease.yaml
│       └── example_phenotype.yaml
├── data/
│   ├── raw/
│   │   └── README.md
│   ├── interim/
│   │   └── README.md
│   ├── processed/
│   │   └── README.md
│   ├── example/
│   │   ├── source_a_genes.tsv
│   │   ├── source_b_genes.tsv
│   │   ├── source_metadata.tsv
│   │   └── identifier_map.tsv
│   └── schemas/
│       ├── source_gene_list_schema.tsv
│       ├── source_metadata_schema.tsv
│       └── consensus_gene_set_schema.tsv
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   ├── data_dictionary.md
│   ├── notes.md
│   ├── maps/
│   │   └── milestone_map.md
│   ├── contracts/
│   │   └── system_contract.md
│   └── plans/
│       └── implementation_plan.md
├── environment/
│   └── requirements.txt
├── logs/
│   └── README.md
├── results/
│   ├── tables/
│   ├── reports/
│   └── README.md
├── scripts/
│   ├── step_01_validate_inputs.py
│   ├── step_02_normalize_genes.py
│   ├── step_03_build_source_matrix.py
│   ├── step_04_score_consensus.py
│   ├── step_05_write_outputs.py
│   ├── step_06_validate_outputs.py
│   ├── validation/
│   │   ├── validate_input_schema.py
│   │   ├── validate_identifier_mapping.py
│   │   ├── validate_consensus_outputs.py
│   │   └── validate_reproducibility.py
│   └── mark_probes/
│       ├── mark_smoketest_gsc.sh
│       └── mark_run_gsc_example.sh
├── src/
│   └── gene_set_consensus/
│       ├── __init__.py
│       ├── config.py
│       ├── io.py
│       ├── logging_utils.py
│       ├── models.py
│       ├── validation.py
│       ├── normalization.py
│       ├── aggregation.py
│       ├── scoring.py
│       ├── provenance.py
│       └── reporting.py
└── tests/
    ├── unit/
    │   ├── test_config.py
    │   ├── test_normalization.py
    │   ├── test_aggregation.py
    │   ├── test_scoring.py
    │   └── test_provenance.py
    ├── integration/
    │   └── test_example_pipeline.py
    ├── validation/
    │   └── test_output_contract.py
    └── test_data/
        ├── source_a_genes.tsv
        ├── source_b_genes.tsv
        ├── source_metadata.tsv
        └── identifier_map.tsv
```

---

## 9. Configuration Contract

### 9.1 Root Config

`config/config.yaml` defines project-level defaults.

Required fields:

```yaml
project:
  name: gene_set_consensus
  version: "0.1.0"

runtime:
  environment: sys76
  run_id_strategy: timestamp
  fail_on_schema_error: true
  fail_on_unmapped_required_gene_id: false

paths:
  input_root: data/example
  interim_dir: data/interim
  processed_dir: data/processed
  results_dir: results
  logs_dir: logs
  external_gene_sets_dir: /mnt/storage/gene_sets
  external_gtr_dir: /mnt/storage/gtr
  external_databases_dir: /mnt/storage/databases

identifier_normalization:
  preferred_gene_id: ensembl_gene_id
  allow_symbol_fallback: true
  unresolved_identifier_policy: flag

outputs:
  write_consensus_gene_set: true
  write_gene_source_matrix: true
  write_gene_frequency_table: true
  write_provenance_table: true
  write_validation_report: true
```

### 9.2 Phenotype Config

Each phenotype config defines exactly one phenotype-scoped consensus run.

Example:

```yaml
phenotype:
  phenotype_id: mitochondrial_disease
  phenotype_label: "Mitochondrial disease"
  version: "v0.1"

sources:
  - source_id: mitocarta
    source_name: MitoCarta
    source_type: curated_database
    file_path: data/example/source_a_genes.tsv
    gene_column: gene_symbol
    weight_tier: gold
    source_weight: 3.0

  - source_id: gtr_panel
    source_name: GTR mitochondrial disease panel
    source_type: clinical_panel
    file_path: data/example/source_b_genes.tsv
    gene_column: gene_symbol
    weight_tier: gold
    source_weight: 3.0

  - source_id: literature_review
    source_name: Literature-derived mitochondrial disease list
    source_type: literature_derived
    file_path: data/example/source_c_genes.tsv
    gene_column: gene_symbol
    weight_tier: silver
    source_weight: 2.0

scoring:
  base_score: source_count
  weighted_score: sum_source_weights
  consensus_score_formula: weighted_score
  minimum_source_count: 1
  include_single_source_genes: true
  deterministic_sort:
    - consensus_score: descending
    - source_count: descending
    - gene_symbol: ascending
```

### 9.3 Config Rules

The pipeline must fail fast if:

- phenotype is missing
- source list is empty
- source ID is duplicated
- configured source file is missing
- gene column is missing
- source weight is missing
- source weight is not numeric
- unsupported scoring mode is requested
- output path cannot be written

---

## 10. Input Data Contract

### 10.1 Source Gene List Schema

Each source file may be TSV or CSV.

Minimum required fields:

| Column | Required | Type | Notes |
|---|---:|---|---|
| `gene_symbol` | conditionally | string | Required if `gene_id` absent |
| `gene_id` | conditionally | string | Preferred stable gene identifier |
| `source_gene_label` | no | string | Original gene label from source |
| `evidence_label` | no | string | Optional source-specific evidence label |
| `disease_label` | no | string | Optional disease/condition field |
| `notes` | no | string | Optional free-text notes |

At least one of `gene_symbol` or `gene_id` must be present.

### 10.2 Source Metadata Schema

A source metadata table may be separate or fully encoded in phenotype config.

Recommended fields:

| Column | Required | Type |
|---|---:|---|
| `source_id` | yes | string |
| `source_name` | yes | string |
| `source_type` | yes | string |
| `source_version` | recommended | string |
| `source_url_or_accession` | recommended | string |
| `download_date` | recommended | date |
| `source_weight` | yes | numeric |
| `weight_tier` | yes | string |
| `license_or_access_note` | no | string |

### 10.3 Identifier Map Schema

Recommended fields:

| Column | Required | Type |
|---|---:|---|
| `input_gene_symbol` | yes | string |
| `normalized_gene_symbol` | yes | string |
| `gene_id` | yes | string |
| `ensembl_gene_id` | recommended | string |
| `hgnc_id` | recommended | string |
| `alias_symbol` | no | string |
| `mapping_status` | yes | enum |
| `mapping_source` | yes | string |
| `mapping_version` | recommended | string |

Allowed `mapping_status` values:

```text
resolved
symbol_only
ambiguous
unresolved
deprecated_symbol_resolved
```

---

## 11. Intermediate Data Contracts

### 11.1 Normalized Source Records

File:

```text
data/interim/{run_id}/normalized_source_records.tsv
```

Required columns:

| Column | Type |
|---|---|
| `run_id` | string |
| `phenotype` | string |
| `source_id` | string |
| `source_name` | string |
| `source_type` | string |
| `weight_tier` | string |
| `source_weight` | numeric |
| `input_gene_symbol` | string/null |
| `normalized_gene_symbol` | string |
| `gene_id` | string/null |
| `mapping_status` | string |
| `evidence_label` | string/null |
| `source_row_number` | integer |
| `source_record_hash` | string |

### 11.2 Gene Source Matrix

File:

```text
data/processed/{run_id}/gene_source_matrix.tsv
```

Required structure:

```text
phenotype
gene_id
gene_symbol
source_id_1
source_id_2
...
source_count
weighted_source_sum
```

Source columns must be binary indicators:

```text
0 = source did not contribute gene
1 = source contributed gene
```

Missing from a source must not be interpreted as negative evidence.

### 11.3 Gene Frequency Table

File:

```text
data/processed/{run_id}/gene_frequency_table.tsv
```

Required columns:

| Column | Type |
|---|---|
| `phenotype` | string |
| `gene_id` | string/null |
| `gene_symbol` | string |
| `source_count` | integer |
| `weighted_source_sum` | numeric |
| `source_list` | string |
| `unresolved_source_count` | integer |
| `mapping_status_summary` | string |

---

## 12. Final Output Contract

### 12.1 Consensus Gene Set

File:

```text
results/tables/{phenotype}/consensus_gene_set.tsv
```

Required columns:

| Column | Type | Notes |
|---|---|---|
| `phenotype` | string | Required explicit phenotype scope |
| `gene_id` | string/null | Preferred stable ID |
| `gene_symbol` | string | Normalized gene symbol |
| `consensus_score` | numeric | Deterministic score |
| `source_count` | integer | Number of contributing sources |
| `weighted_source_sum` | numeric | Raw weighted contribution |
| `source_list` | string | Delimited stable source IDs |
| `weight_tier_summary` | string | Summarized tier evidence |
| `mapping_status` | string | Identifier resolution state |
| `provenance_id` | string | Link to provenance table |
| `run_id` | string | Pipeline run ID |
| `gsc_version` | string | Repo or output version |
| `generated_at` | string | Timestamp |

Sort order:

1. `consensus_score` descending
2. `source_count` descending
3. `gene_symbol` ascending
4. `gene_id` ascending

### 12.2 Provenance Table

File:

```text
results/tables/{phenotype}/gene_provenance.tsv
```

Required columns:

| Column | Type |
|---|---|
| `provenance_id` | string |
| `phenotype` | string |
| `gene_id` | string/null |
| `gene_symbol` | string |
| `source_id` | string |
| `source_name` | string |
| `source_type` | string |
| `source_version` | string/null |
| `source_weight` | numeric |
| `weight_tier` | string |
| `input_gene_symbol` | string/null |
| `source_record_hash` | string |
| `download_date` | string/null |
| `run_id` | string |

### 12.3 Validation Report

File:

```text
results/reports/{phenotype}/validation_report.md
```

Required sections:

- input summary
- source counts
- identifier mapping summary
- duplicate resolution summary
- unresolved identifier list
- consensus score distribution
- known-gene recovery check
- cross-source consistency check
- reproducibility checksum
- assumptions
- limitations
- edge cases
- validation status

### 12.4 Run Manifest

File:

```text
results/reports/{phenotype}/run_manifest.yaml
```

Required fields:

```yaml
run_id:
gsc_version:
phenotype:
config_file:
phenotype_config_file:
input_files:
input_file_hashes:
output_files:
output_file_hashes:
software_versions:
generated_at:
status:
```

---

## 13. Scoring Contract

### 13.1 Required v1 Scores

GSC v1 must preserve both raw and weighted evidence.

Required metrics:

```text
source_count
weighted_source_sum
consensus_score
```

### 13.2 Base Score

```text
base_score = source_count
```

### 13.3 Authority-Aware Weighted Score

```text
weighted_source_sum = sum(source_weight for each contributing source)
```

### 13.4 Consensus Score

For v1:

```text
consensus_score = weighted_source_sum
```

Optional future amplification must be explicitly configured and documented.

### 13.5 Score Constraints

The implementation must:

- never infer absence as negative evidence
- never compare scores across phenotypes unless explicitly modeled
- never use hidden weights
- preserve raw source count alongside weighted score
- make each score explainable from provenance rows

---

## 14. Normalization Contract

### 14.1 Required Normalization Steps

For each source record:

1. strip whitespace
2. preserve original input label
3. uppercase gene symbol where appropriate
4. resolve known aliases if mapping data exists
5. assign `gene_id` where possible
6. mark unresolved or ambiguous mappings
7. preserve source row linkage

### 14.2 Duplicate Handling

Duplicates within a source must be collapsed to one contribution per `(source_id, gene_id)` or provisional `(source_id, normalized_gene_symbol)`.

Duplicates across sources must increase `source_count`.

Duplicates within the same source must not inflate `source_count`.

### 14.3 Ambiguous Identifiers

Ambiguous mappings must be flagged, not silently resolved.

Acceptable handling modes:

```text
fail
flag
exclude
```

Default for v1:

```text
flag
```

---

## 15. Provenance Contract

Every final consensus row must trace back to one or more source records.

The pipeline must preserve:

- source ID
- source name
- source type
- source version where available
- source weight
- source tier
- original gene label
- normalized gene label
- source row number or source record hash
- run ID
- generation timestamp

Provenance may be stored in a normalized long-form table and summarized in `source_list` in the final consensus file.

---

## 16. Logging Contract

Each pipeline run must create:

```text
logs/{run_id}/pipeline.log
logs/{run_id}/step_01_validate_inputs.log
logs/{run_id}/step_02_normalize_genes.log
logs/{run_id}/step_03_build_source_matrix.log
logs/{run_id}/step_04_score_consensus.log
logs/{run_id}/step_05_write_outputs.log
logs/{run_id}/step_06_validate_outputs.log
```

Logs must include:

- timestamp
- run ID
- phenotype
- config path
- source files used
- row counts
- output paths
- validation failures
- warnings
- completion status

On MARK, execution harnesses must also write downloadable probe logs to `~/Desktop/`.

Example:

```text
~/Desktop/gsc_mark_smoketest_{run_id}.log
```

---

## 17. Validation Contract

GSC v1 validation must include:

### 17.1 Input Validation

- files exist
- file extensions supported
- required columns present
- no empty source files
- no duplicate `source_id`
- source weights numeric
- phenotype present
- unsupported config keys flagged

### 17.2 Identifier Validation

- gene symbols normalized consistently
- unresolved mappings reported
- ambiguous mappings reported
- deprecated symbols flagged
- gene IDs stable where available

### 17.3 Aggregation Validation

- no duplicate final `(phenotype, gene_id)` records when `gene_id` is available
- source count matches gene-source matrix
- weighted score matches source weights
- source list matches provenance rows
- single-source genes preserved if configured

### 17.4 Output Validation

- required files created
- required columns present
- deterministic sort order applied
- output hashes recorded
- no silent null coercion
- provenance rows join back to consensus records

### 17.5 Reproducibility Validation

The same example run must be executable twice and produce identical checksums for deterministic output files, excluding fields intentionally timestamped in run manifests/logs.

---

## 18. Edge-Case Contract

The implementation must explicitly handle:

| Edge case | Required behavior |
|---|---|
| Duplicate genes within one source | Collapse to one source contribution |
| Same gene across multiple sources | Increase source count and weighted score |
| Outdated gene symbol | Resolve if mapping exists; otherwise flag |
| Ambiguous gene symbol | Flag; do not silently choose |
| Missing gene ID | Allow symbol fallback only if configured |
| Missing gene symbol | Allow only if stable gene ID is present |
| Missing source weight | Fail fast |
| Empty source file | Fail fast |
| Unsupported source file type | Fail fast |
| Conflicting metadata | Preserve conflict in provenance/report |
| Single-source support | Preserve, mark as sparse support |
| Phenotype mismatch | Fail unless explicitly mapped |
| GTR condition maps to many panels | Preserve source granularity |
| RSP-derived future evidence | Must remain phenotype-scoped if incorporated |
| VDB/RDGP join without phenotype selection | Invalid |

---

## 19. Integration Contract

### 19.1 VDB Compatibility

GSC outputs must be joinable to VDB gene-level records using:

```text
gene_id
gene_symbol
```

`gene_id` is preferred.

GSC must not require VDB to consume GSC-specific internals beyond the final output schema.

### 19.2 RDGP Compatibility

RDGP may consume GSC outputs only after selecting the relevant phenotype context.

Valid integration:

```text
RDGP(sample_id, gene_id)
JOIN
GSC(phenotype, gene_id)
WHERE phenotype = selected_analysis_phenotype
```

Invalid integration:

```text
RDGP(sample_id, gene_id)
JOIN
GSC(gene_id)
```

without explicit phenotype scoping.

### 19.3 RSP Compatibility

RSP may later produce gene-level functional evidence. If incorporated into GSC, the resulting evidence must remain phenotype-scoped and must not turn GSC into a sample-specific system.

### 19.4 VAP Compatibility

VAP may use GSC outputs as annotation context, but GSC must not become dependent on VAP outputs.

---

## 20. Versioning Contract

Versioning applies at three levels:

### 20.1 Repo Version

Recorded in:

```text
pyproject.toml or src/gene_set_consensus/__init__.py
```

### 20.2 Phenotype Output Version

Recorded in phenotype config:

```yaml
phenotype:
  version: "v0.1"
```

### 20.3 Run ID

Generated at execution time:

```text
run_YYYY_MM_DD_HHMMSS
```

All final outputs must include `run_id`.

---

## 21. Failure Mode Contract

The pipeline must fail visibly and log errors for:

- missing config
- malformed config
- missing input source
- missing required source column
- duplicated source ID
- invalid source weight
- unsupported scoring mode
- output directory unwritable
- schema validation failure
- no genes after normalization
- all mappings unresolved when strict mode is enabled

The pipeline may warn but continue for:

- partial unresolved mappings
- sparse single-source genes
- optional metadata missing
- deprecated symbols resolved successfully
- noncritical source metadata gaps

---

## 22. Assumptions

- Input gene lists are phenotype-associated by construction.
- Source authority can be represented by explicit weights in v1.
- Stable gene identifiers may not be available for all early-stage inputs.
- Gene-symbol normalization is imperfect and must be audited.
- GSC v1 prioritizes transparent heuristics over black-box scoring.
- GSC outputs are intended for downstream use by VDB/RDGP/RSP but remain independently reproducible.

---

## 23. Limitations

- v1 identifier normalization may depend on a static mapping file.
- v1 scoring is heuristic and not a calibrated probability.
- v1 does not solve phenotype ontology harmonization.
- v1 does not automate literature extraction.
- v1 does not perform enrichment analysis.
- v1 does not evaluate variant-level pathogenicity.
- v1 does not perform cross-phenotype score comparison.
- v1 GTR integration may initially depend on pre-exported GTR-derived tabular files.

---

## 24. Validation Strategy

The v1 validation strategy includes:

1. example-data end-to-end pipeline run
2. known-gene recovery check for selected phenotype
3. cross-source consistency check
4. authority-weight behavior check
5. identifier-resolution audit
6. provenance joinability check
7. VDB/RDGP schema compatibility check
8. repeated-run deterministic checksum test
9. MARK smoke test using a MARK probe
10. manual spot-check of 3–5 genes

---

## 25. Release Gate

GSC v1.0 is ready only when:

- phenotype-specific multi-source aggregation works
- GTR-derived source integration is supported
- final output includes required downstream fields
- provenance per gene is preserved
- weighted consensus scoring is deterministic and explainable
- validation report is generated
- example data run completes locally
- MARK smoke test completes
- outputs are reproducible across repeated runs
- documentation includes assumptions, limitations, edge cases, validation strategy, and implementation notes

---

## 26. Contract Summary

GSC must remain:

```text
phenotype-scoped
gene-level
provenance-aware
config-driven
deterministic
joinable
auditable
non-sample-specific
```

This contract is the boundary that keeps GSC from drifting into RDGP, VDB, RSP, or enrichment-workflow territory.
