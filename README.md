# gene_set_consensus

`gene_set_consensus` (GSC) builds phenotype-scoped consensus gene sets from multiple heterogeneous gene-list sources.

GSC is designed as a reproducible upstream evidence layer for downstream repositories such as:

- `variant_annotation_pipeline` (VAP)
- `variant_database` (VDB)
- `rnaseq_pipeline` (RSP)
- `rare_disease_gene_prioritization` (RDGP)


---

## What GSC Does

GSC converts:

```text
multiple phenotype-associated gene lists
→ normalized gene identifiers
→ source-aware gene matrix
→ weighted consensus gene evidence
→ provenance-aware output tables
```


---

## What GSC Does Not Do

GSC does not:
    - call variants 
    - parse VCF/BAM/FASTQ files 
    - perform enrichment analysis 
    - perform RNA-seq analysis 
    - rank patient-specific genes 
    - store sample-specific evidence 

GSC is phenotype-scoped and gene-level.

The core evidence identity is:
`(phenotype, gene_id)`


---

## Current Status
Current working MVP includes:
  - config-driven execution 
  - phenotype config files 
  - source adapters 
  - identifier normalization 
  - gene-source matrix construction 
  - weighted consensus scoring 
  - provenance table generation 
  - output contract validation 
  - reproducibility validation 
  - source manifest support 
  - Makefile operator commands 
  - pytest test suite 


---

## Quick Start

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the example pipeline:

```bash
make run-example
```

Run reproducibility validation:

```bash
make reproduce
```

Run tests:
```bash
make test
```

Inspect the consensus output:

```bash
make show-consensus
```


---

## Example Outputs

The example run writes:
- `results/tables/example_phenotype/consensus_gene_set.tsv`
- `results/tables/example_phenotype/gene_source_matrix.tsv`
- `results/tables/example_phenotype/gene_frequency_table.tsv`
- `results/tables/example_phenotype/gene_provenance.tsv`
- `results/reports/example_phenotype/run_manifest.yaml`
- `results/reports/example_phenotype/validation_report.md`
- `results/reports/example_phenotype/output_contract_validation.tsv`



---

## Repository Structure

| Folder | Utility
| ------- |  ------- |
| `config/` | pipeline and phenotype configs |
| `data/example/` | tiny toy data for reproducible testing |
| `data/schemas/` | tabular schema descriptions |
| `docs/` | architecture, contracts, plans, notes |
| `manifests/sources/` | source provenance manifests|
| `scripts/` | executable pipeline steps and validators |
| `src/gene_set_consensus/` | reusable Python package code |
| `tests/` | unit, integration, and validation tests |
| `results/` | generated outputs; not committed |
| `logs/` | generated logs; not committed |



---

## Source Adapters

GSC separates biological source type from file parsing strategy.

`source_type` describes biological meaning:
- `curated_database`
- `clinical_panel`
- `literature_derived`
- `user_provided`

`adapter` describes file structure:
- `generic_gene_list`
- `gtr_panel`

This means a clinical panel can use `generic_gene_list` if it is already flattened into a simple TSV, while a full GTR-style export should use `gtr_panel`.



---

## Real Source Storage

Real gene-set files should not be committed to Git.

Use external storage:
  - sys76: `/mnt/storage/gene_sets/`
  - sys76 GTR: `/mnt/storage/gtr/`
  - MARK: `/data/storage/gene_sets/`
  - MARK GTR: `/data/storage/gtr/`

Phenotype configs point to those files using `file_path`.


---

## Assumptions

  - Input gene lists are phenotype-associated by configuration. 
  - Source authority is represented with explicit numeric weights. 
  - Gene identifier normalization depends on the configured identifier map. 
  - Absence from a source is not negative evidence. 


---

## Limitations

  - v1 scoring is heuristic and deterministic, not probabilistic. 
  - v1 does not perform phenotype ontology harmonization. 
  - v1 does not automate external source downloads. 
  - v1 does not perform literature mining. 
  - v1 does not compare consensus scores across phenotypes. 


---

## Validation

GSC validates:
  - input schemas 
  - source configuration 
  - identifier normalization behavior 
  - output contracts 
  - forbidden sample/variant-level fields 
  - provenance joinability 
  - reproducibility across repeated runs 


---

## Current Development Target

Near-term development is focused on:
1. strengthening source adapters 
2. preparing real MitoCarta / GTR / Epi25 ingestion 
3. adding `make run-mito` and `make run-epilepsy`
4. improving documentation and validation reports 
5. preparing future downstream compatibility with VDB/RDGP/RSP

---

## Real Source Ingestion: MitoCarta

For v1, MitoCarta ingestion is operator-staged rather than automatically downloaded.

Manual staging is preferred because:
- source formats may change over time
- downloaded files should remain outside Git
- acquisition date and source version should be recorded explicitly
- source provenance should be auditable

Expected sys76 staging location:


`/mnt/storage/gene_sets/mitocarta/`


Recommended staged files:

`/mnt/storage/gene_sets/mitocarta/Human.MitoCarta3.0.xls`
`/mnt/storage/gene_sets/mitocarta/mitocarta_human.tsv`

The original downloaded Excel file should be preserved.

A cleaned TSV should be derived from it for GSC pipeline input.

The cleaned TSV should minimally contain:

- gene_symbol
- gene_id
- evidence_label
- notes

For MitoCarta, `gene_symbol` should be derived from the MitoCarta `Symbol` column. 

Additional MitoCarta fields such as `Evidence`, `Sub-compartment`, `MitoPathways`, or `Maestro` score may be preserved in `evidence_label` or `notes` during early v1 ingestion.

Do not commit real MitoCarta source files to Git.

---