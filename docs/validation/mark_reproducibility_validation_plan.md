# MARK Reproducibility Validation Plan

## Purpose

This document defines a controlled cross-machine reproducibility validation for `gene_set_consensus` (GSC) on MARK.

The goal is to verify that GSC can be freshly cloned, installed, tested, supplied with staged external source files, and executed from raw or staged source material through final semantic consensus outputs outside the original Sys76 development environment.

---

# Objectives

This validation tests whether GSC can reproducibly execute across independent Linux environments.

Primary objectives:

1. Clone GSC fresh on MARK.
2. Create an isolated Python virtual environment.
3. Install dependencies from `requirements.txt`.
4. Run the complete automated validation suite.
5. Stage required external source files under MARK storage.
6. Parse the GTR XML independently on MARK.
7. Generate GTR gene-measure and gene-summary tables.
8. Execute semantic epilepsy and mitochondrial releases.
9. Compare MARK-generated outputs against Sys76-generated outputs.
10. Capture logs, runtime notes, and reproducibility findings.

---

# Success Criteria

A successful MARK validation requires:

- repository clone succeeds
- virtual environment creation succeeds
- dependency installation succeeds
- `pytest` passes
- release manifest validation passes
- scoring profile validation passes
- GTR XML parsing completes
- epilepsy GTR summary generation completes
- mitochondrial GTR summary generation completes
- semantic epilepsy release completes
- semantic DEE release completes
- semantic NAFE release completes
- semantic mitochondrial release completes
- output contract validation passes
- key consensus outputs are reproducible or explainably equivalent
- all deviations are documented


---

# Scope

## Included

This validation includes:

- fresh MARK clone
- Python environment bootstrap
- CI-equivalent validation
- external source staging
- GTR XML parsing
- MitoCarta source use
- Genes4Epilepsy source use
- Epi25 source use
- semantic scoring release execution
- output inspection
- reproducibility reporting

## Excluded

This validation does not require:

- GitHub Actions reconfiguration
- Dockerization
- probabilistic scoring
- new ontology development
- downstream VAP/VDB/RSP/RDGP integration
- automated external data download workflows

---

# Expected MARK Storage Layout

Recommended storage structure:

```text
/data/storage/
├── gtr/
│   ├── raw/
│   │   └── gtr_ftp.xml.gz
│   └── processed/
├── gene_sets/
│   ├── epi25/
│   │   └── 2024/
│   │       └── processed/
│   │           ├── epi25_2024_epi_high_confidence.tsv
│   │           ├── epi25_2024_dee_high_confidence.tsv
│   │           └── epi25_2024_nafe_high_confidence.tsv
│   ├── genes4epilepsy/
│   │   └── genes4epilepsy.tsv
│   ├── mitocarta/
│   │   ├── raw/
│   │   │   └── Human.MitoCarta3.0.xls
│   │   └── processed/
│   │       └── mitocarta_human.tsv
│   ├── gtr_epilepsy/
│   │   └── processed/
│   └── gtr_mitochondria/
│       └── processed/
```

Raw source files should be preserved where possible.

Processed source tables should be generated deterministically from raw/staged sources.

---

# Phase 0 — MARK Reconnaissance

Before cloning or transferring data, inspect the MARK environment.

Record:

```bash
hostname
date
whoami
pwd
uname -a
python3 --version
git --version
df -h
free -h
ulimit -a
ls -ld /data /data/storage /mnt /mnt/storage 2>/dev/null || true
```

# Phase 1 — MARK Environment Bootstrap

Record:

```bash
hostname
date
pwd
python3 --version
git --version
df -h
free -h
```

Clone repository:

```bash
mkdir -p ~/dev/portfolio_projects
cd ~/dev/portfolio_projects
git clone git@github.com:VitamOrdinatio/gene_set_consensus.git
cd gene_set_consensus
```

If SSH is not configured, use HTTPS:

```bash
git clone https://github.com/VitamOrdinatio/gene_set_consensus.git
```

Create virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# Phase 2 — Repo Portability Validation

Run CI-equivalent checks:

```bash
make validate-all
```

`make validate-all` is CI-safe and already skips external paths.

Expected:

- Python compilation succeeds
- release validation succeeds
- scoring profile validation succeeds
- source manifest validation succeeds
- pytest passes

---

# Phase 3 — External Data Transfer

Transfer required source files from Sys76 to MARK:

Required files:

```text
gtr_ftp.xml.gz
epi25_2024_epi_high_confidence.tsv
epi25_2024_dee_high_confidence.tsv
epi25_2024_nafe_high_confidence.tsv
genes4epilepsy.tsv
mitocarta_human.tsv
Human.MitoCarta3.0.xls
```

Recommended transfer tools:

- scp
- rsync
- SFTP
- browser upload/download if required by environment

Recommended checksum capture:

```bash
sha256sum <file>
```

Capture checksums on both Sys76 and MARK for transferred large files where practical.

---

# Phase 4 — MARK Storage Setup

Create directories:

```bash
mkdir -p /data/storage/gtr/raw
mkdir -p /data/storage/gtr/processed
mkdir -p /data/storage/gene_sets/epi25/2024/processed
mkdir -p /data/storage/gene_sets/genes4epilepsy
mkdir -p /data/storage/gene_sets/mitocarta/raw
mkdir -p /data/storage/gene_sets/mitocarta/processed
mkdir -p /data/storage/gene_sets/gtr_epilepsy/processed
mkdir -p /data/storage/gene_sets/gtr_mitochondria/processed
```

If `/data/storage` is unavailable, use an agreed MARK-accessible alternative and document the path substitution.

---

# Phase 5 — Path Configuration Strategy

GSC release configs currently reference Sys76-style paths such as:

`/mnt/storage/`

For MARK validation, use one of two strategies:

## Preferred Strategy

Create a compatible symlink:

```bash
sudo mkdir -p /mnt
sudo ln -s /data/storage /mnt/storage
```

This preserves release config paths and avoids modifying committed configs.

Important note: On MARK, use the preferred strategy only if `/mnt/storage` does NOT already exist.

## Alternative Strategy

Create MARK-specific release configs or local uncommitted overrides.

Use only if symlink creation is unavailable.

---

# Phase 6 — GTR XML Parsing on MARK

## GTR Parsing and Resource Monitoring

Use the resource-monitoring commands below as the actual parse commands.

During large GTR XML parsing, record approximate runtime, memory, and output sizes.

Epilepsy parse with resource monitoring:

```bash
/usr/bin/time -v python scripts/ingest/parse_gtr_xml_gene_measures.py \
  --xml /mnt/storage/gtr/raw/gtr_ftp.xml.gz \
  --rules config/rules/gtr_epilepsy_terms.yaml \
  --output /mnt/storage/gene_sets/gtr_epilepsy/processed/gtr_epilepsy_gene_measures.tsv
```

Mitochondrial parse with resource monitoring:

```bash
/usr/bin/time -v python scripts/ingest/parse_gtr_xml_gene_measures.py \
  --xml /mnt/storage/gtr/raw/gtr_ftp.xml.gz \
  --rules config/rules/gtr_mitochondrial_terms.yaml \
  --output /mnt/storage/gene_sets/gtr_mitochondria/processed/gtr_mitochondria_gene_measures.tsv
```

If `/usr/bin/time -v` is unavailable, use shell `time`:

```bash
time python scripts/ingest/parse_gtr_xml_gene_measures.py ...
```

After each parse:

```bash
ls -lh /mnt/storage/gene_sets/gtr_epilepsy/processed/
ls -lh /mnt/storage/gene_sets/gtr_mitochondria/processed/
```

Record output file sizes and runtime summaries in the reproducibility report.

---

# Phase 7 — GTR Summary Generation

Generate epilepsy GTR summary:

```bash
python scripts/ingest/summarize_gtr_gene_evidence.py \
  --input /mnt/storage/gene_sets/gtr_epilepsy/processed/gtr_epilepsy_gene_measures.tsv \
  --output /mnt/storage/gene_sets/gtr_epilepsy/processed/gtr_epilepsy_gene_summary.tsv \
  --source-id gtr_epilepsy_gene_summary \
  --source-name GTR_Epilepsy \
  --source-tier silver
```

Generate mitochondrial GTR summary:

```bash
python scripts/ingest/summarize_gtr_gene_evidence.py \
  --input /mnt/storage/gene_sets/gtr_mitochondria/processed/gtr_mitochondria_gene_measures.tsv \
  --output /mnt/storage/gene_sets/gtr_mitochondria/processed/gtr_mitochondria_gene_summary.tsv \
  --source-id gtr_mitochondrial_gene_summary \
  --source-name GTR_Mitochondria \
  --source-tier silver
```

Inspect summaries:

```bash
head -n 1 /mnt/storage/gene_sets/gtr_epilepsy/processed/gtr_epilepsy_gene_summary.tsv | tr '\t' '\n'
head -n 1 /mnt/storage/gene_sets/gtr_mitochondria/processed/gtr_mitochondria_gene_summary.tsv | tr '\t' '\n'
```

---

# Phase 8 — Semantic Release Execution

Run epilepsy semantic release:

```bash
make run-epilepsy-semantic
```

Run DEE (epilepsy subtype) semantic release:

```bash
make run-dee-semantic
```

Run NAFE (epilepsy subtype) semantic release:

```bash
make run-nafe-semantic
```

Run mitochondrial semantic release:

```bash
make run-mito-semantic
```

Validate outputs and external source paths:

```bash
make validate-all-with-paths
```

---

# Phase 9 — Output Inspection

Inspect selected genes:

```bash
awk -F'\t' '$3 ~ /^(SCN1A|DEPDC5|NPRL3|SYNGAP1|POLG)$/ {print}' \
  results/tables/epilepsy_semantic_gtr_experimental/consensus_gene_set.tsv

awk -F'\t' '$3 ~ /^(POLG|TWNK|TFAM|SURF1|CYC1)$/ {print}' \
  results/tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv

awk -F'\t' '$3 ~ /^(NEXMIF|SCN1A|STX1B|SYNGAP1|WDR45)$/ {print}' \
  results/tables/dee_semantic_gtr_experimental/consensus_gene_set.tsv

awk -F'\t' '$3 ~ /^(DEPDC5|NPRL3)$/ {print}' \
  results/tables/nafe_semantic_gtr_experimental/consensus_gene_set.tsv
```

Inspect headers:

```bash
head -n 1 results/tables/epilepsy_semantic_gtr_experimental/consensus_gene_set.tsv | tr '\t' '\n'
head -n 1 results/tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv | tr '\t' '\n'
```

---

# Phase 10 — Sys76 vs MARK Comparison

Recommended comparison targets:

```text
results/tables/epilepsy_semantic_gtr_experimental/consensus_gene_set.tsv
results/tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv
results/tables/dee_semantic_gtr_experimental/consensus_gene_set.tsv
results/tables/nafe_semantic_gtr_experimental/consensus_gene_set.tsv
```

Suggested checks:

```bash
sha256sum results/tables/epilepsy_semantic_gtr_experimental/consensus_gene_set.tsv
sha256sum results/tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv
```

If exact hashes differ, compare:

- row counts
- selected gene rows
- semantic score columns
- provenance IDs
- generated timestamps
- run IDs

Expected possible differences:

- run_id
- generated_at
- provenance hashes if source path metadata differs
- ordering only if nondeterminism is discovered

Unexpected differences should be documented.

---

# Phase 11 — Reproducibility Report

After execution, create:

`docs/validation/mark_reproducibility_validation_report.md`

Recommended report sections:

- MARK environment
- data files staged
- checksums
- commands executed
- validation results
- output comparison
- deviations
- final conclusion

---

# Final Reproducibility Claim

If successful, GSC can claim:

```text
GSC semantic release execution was independently reproduced on MARK from externally staged source material through final semantic consensus outputs.
```

A stronger claim may be used only if raw GTR parsing, summary generation, and final semantic outputs are all completed successfully on MARK.

---