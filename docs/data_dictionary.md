# Data Dictionary: gene_set_consensus

## Source Gene List Input

Each source gene list is a TSV or CSV file containing genes associated with one phenotype-relevant source.

Minimum requirement: at least one configured gene identifier column.

| Column | Required | Description |
|---|---:|---|
| `gene_symbol` | conditional | Input gene symbol used by source |
| `gene_id` | conditional | Stable gene identifier, preferably Ensembl gene ID |
| `evidence_label` | no | Source-specific evidence category |
| `notes` | no | Free-text source notes |

At least one of `gene_symbol` or `gene_id` must be present.

## Phenotype Config Source Fields

| Field | Required | Description |
|---|---:|---|
| `source_id` | yes | Stable snake_case source identifier |
| `source_name` | yes | Human-readable source name |
| `source_type` | yes | Source class, e.g. curated_database, clinical_panel, literature_derived |
| `file_path` | yes | Path to source file; real data should live outside Git under `/mnt/storage` or `/data/storage` |
| `gene_column` | yes | Column containing input gene symbols |
| `weight_tier` | yes | Evidence tier such as gold, silver, bronze |
| `source_weight` | yes | Numeric source weight used in deterministic scoring |

## Normalized Source Records

Intermediate file:

`data/interim/{run_id}/normalized_source_records.tsv`

| Column | Description |
|---|---|
| `phenotype` | Explicit phenotype scope |
| `source_id` | Source identifier |
| `source_name` | Source name |
| `source_type` | Source class |
| `weight_tier` | Authority tier |
| `source_weight` | Numeric source weight |
| `source_row_number` | Original row number within source file |
| `input_gene_symbol` | Original source gene symbol |
| `normalized_gene_symbol` | Normalized gene symbol after mapping |
| `gene_id` | Stable gene identifier when resolved |
| `mapping_status` | Identifier resolution status |
| `evidence_label` | Source-specific evidence label |
| `notes` | Optional notes |
| `source_record_hash` | Stable short hash for source record traceability |

## Consensus Gene Set

Final file:

`results/tables/{phenotype}/consensus_gene_set.tsv`

| Column | Description |
|---|---|
| `phenotype` | Phenotype context |
| `gene_id` | Stable gene identifier when available |
| `gene_symbol` | Normalized gene symbol |
| `consensus_score` | Deterministic v1 consensus score |
| `source_count` | Number of contributing sources |
| `weighted_source_sum` | Sum of contributing source weights |
| `source_list` | Pipe-delimited contributing source IDs |
| `weight_tier_summary` | Pipe-delimited contributing evidence tiers |
| `mapping_status_summary` | Pipe-delimited mapping statuses observed |
| `provenance_id` | Join key to provenance table |
| `run_id` | Pipeline run identifier |
| `gsc_version` | GSC repo/config version |
| `generated_at` | Output generation timestamp |

## Provenance Table

Final file:

`results/tables/{phenotype}/gene_provenance.tsv`

Each row links one gene-level consensus record back to one contributing source record.
