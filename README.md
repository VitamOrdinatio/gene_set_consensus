# ================================
# root/README.md
# ================================

# gene_set_consensus

## Overview

gene_set_consensus is a bioinformatics utility for constructing evidence-aware consensus gene rankings for a given phenotype.

It aggregates multiple gene lists and produces a unified scoring framework that reflects:

- source quality
- cross-source agreement
- traceable provenance
- future integration of both literature-derived and GTR-derived evidence

---

## Motivation

Variant interpretation depends on the quality of gene sets used to contextualize results.

`Poor gene sets → noisy biological conclusions`

This repository addresses that gap by providing a reproducible method for:

`multi-source integration → consensus scoring → ranked gene output`

---

## Core Concept

```text
Multiple gene lists + evidence tiers (gold / silver / bronze) → weighted consensus gene ranking
```

---

## Why This Repo Matters

A sequencing pipeline can be technically correct and still produce weak biological conclusions if the interpretation scaffold is noisy.

This repository is designed to improve the interpretation layer by answering:

`Which genes have the strongest cross-source support for association with a phenotype?`

---

## Example Use Case

```text
Phenotype: Epilepsy

Sources:
- ClinGen (gold)
- OMIM (gold)
- Genes4Epilepsy (silver)

Future source class:
- GTR-derived epilepsy panel genes (clinical utilization evidence)

Output:
- Ranked genes with consensus scores
- Supporting source provenance per gene
```

---

## Installation

```bash
git clone <repo_url>
cd gene_set_consensus
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

```bash
python scripts/build_consensus.py --config data/input/config.yaml
```

---

## Input Requirements

### Config File (YAML)

Defines:

- phenotype
- source files
- source types
- tier assignments
- weights

### Gene Lists (TSV)

Minimum:
- gene_symbol

Optional:
- gene_id
- ensembl_id
- notes

### v1 Source Model

v1 uses:

- user-supplied, provenance-preserving curated phenotype gene lists

Typical examples include:

- literature-derived gene lists
- manually curated phenotype panels
- exported tables from vetted resources such as ClinGen, OMIM, MitoCarta, or Genes4Epilepsy

Future versions will add:
- GTR-derived phenotype-associated gene lists

---

## Output

`data/output/<phenotype>_consensus.tsv`

Expected fields include:

- gene_symbol
- weighted_score
- consensus_score
- supporting_sources
- source_types

---

## Scoring Philosophy

`More independent support + higher evidence tiers → higher confidence`

v1 intentionally uses a simple, interpretable weighting system.

---

## Repository Structure

```text
data/
docs/
scripts/
src/
tests/
```

---

## Relationship to Other Projects

This repository complements:

```text
variant_annotation_pipeline
```

by improving the interpretation layer of genomic analyses.

Together, the two repositories answer:

```text
variant_annotation_pipeline → What variants are present?
gene_set_consensus          → Which genes have the strongest evidence for phenotype relevance?
```

---

## Roadmap

### v1
- literature-driven consensus scoring
- YAML-driven inputs
- TSV outputs
- provenance-preserving source integration

### v2
- identifier harmonization
- ClinGen / OMIM integration improvements
- GTR phenotype mining and ingestion

### v3
- integrated literature + GTR meta-scoring
- citation-aware weighting
- richer evidence modeling

---

## Disclaimer

```text
This tool does NOT establish causality.
It ranks genes based on cross-source support and preserved provenance.
```

---

## Author Philosophy

```text
Reproducibility > convenience
Traceability > automation
Signal > noise
```

---

## License

`See LICENSE file.`

---

# END of README.md











