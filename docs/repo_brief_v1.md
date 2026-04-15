# ================================
# docs/repo_brief_v1.md
# ================================

# Repo Brief — gene_set_consensus (v1)

## Purpose

The **gene_set_consensus** repository is designed to aggregate multiple phenotype-associated gene lists into a **traceable, weighted consensus gene ranking**.

This repository addresses a critical bottleneck in genomics:

```text
Variant calling pipelines can be technically correct,
but downstream biological interpretation depends heavily
on the quality, provenance, and internal consistency
of the gene-set overlays used to contextualize those variants.
```

This tool provides a reproducible method to:
- Integrate multiple phenotype-associated gene lists
- Preserve source provenance
- Assign evidence-aware weights
- Generate consensus scores
- Produce ranked output tables suitable for downstream interpretation

---

## Problem Statement

Gene sets used for phenotype association (for example, epilepsy or mitochondrial disease) often suffer from:

- inconsistent identifiers
- gene_symbol ↔ gene_id drift
- unclear provenance
- mixed evidence quality
- redundancy across sources
- disagreement between literature and real-world clinical usage

This leads to:
```text
false positives / false negatives in downstream enrichment analyses
and noisy biological interpretation even when upstream variant calling is correct
```

---

## Solution Overview

The repository implements a consensus scoring engine:

**Input:**
1. phenotype
2. multiple user-supplied gene lists
3. user-defined source tiers (gold / silver / bronze)
4. source metadata for provenance

**Output:**
1. ranked gene table with weighted consensus scores
2. source-level provenance per gene
3. optional source summary tables

---

## v1 Scope

### Core Features
- config-driven execution (YAML)
- phenotype-specific gene-list aggregation
- user-supplied source tiers (gold / silver / bronze)
- gene-level aggregation across sources
- weighted consensus scoring
- source provenance tracking
- reproducible TSV outputs

### v1 Evidence Model

v1 is intentionally limited to:
`user-supplied, provenance-preserving curated phenotype gene lists`

Typical examples include:

- literature-derived gene lists
- manually curated phenotype panels
- exported tables from vetted resources such as ClinGen, OMIM, MitoCarta, or Genes4Epilepsy

### v1 Explicit Exclusions

- no automated GTR mining yet
- no citation-based weighting
- no ontology integration
- no GUI
- no automatic gene-ID rescue or correction
- no implicit identifier harmonization beyond minimal normalization

---

## Inputs

### Input 1: Phenotype Configuration (YAML)

Example:

```yaml
phenotype: epilepsy

weights:
  gold: 1.0
  silver: 0.6
  bronze: 0.3

consensus_bonus:
  enabled: true
  per_additional_source: 0.1

sources:
  - name: ClinGen
    path: data/input/sources/clingen_epilepsy.tsv
    tier: gold
    source_type: literature
  - name: OMIM
    path: data/input/sources/omim_epilepsy.tsv
    tier: gold
    source_type: literature
  - name: Genes4Epilepsy
    path: data/input/sources/genes4epilepsy.tsv
    tier: silver
    source_type: literature
```

### Input 2: Gene List Files (TSV)

#### Minimum required columns:
1. gene_symbol (required)

#### Optional columns: 
2. ensembl_id
3. gene_id
4. evidence_note
5. source_note

#### Input Requirements
- input files must be clean and explicitly curated
- v1 will not attempt to repair ambiguous identifiers
- duplicate rows within a source may be deduplicated
- source provenance must be preserved

---

## Outputs

### Output 1 — Consensus Table (TSV)

Suggested columns: 
1. gene_symbol
2. ensembl_id
3. gene_id
4. phenotype
5. source_count
6. gold_count
7. silver_count
8. bronze_count
9. weighted_score
10. consensus_score
11. supporting_sources
12. supporting_tiers
13. source_types

### Output 2 — Source Summary Table (optional)

Suggested columns:
- source_name
- source_type
- tier
- file_path
- input_gene_count
- retained_gene_count

---

## Scoring Model (v1)

### Base weights:

gold   = 1.0
silver = 0.6
bronze = 0.3

### Weighted sum:
`weighted_score = sum(source_weight per gene)`

### Optional consensus multiplier:
`consensus_score = weighted_score × (1 + 0.1 × (source_count - 1))`

### Rationale

This scoring model is intentionally simple, interpretable, and easy to audit.

v1 prioritizes:
`clarity and provenance over algorithmic sophistication`

## Non-Goals (v1)

- No automated gene ID correction
- No hidden identifier remapping
- No citation-based weighting
- No GTR scraping or XML mining
- No ClinVar / OMIM API integration
- No ontology expansion
- No web interface

---

## Future Versions

### v2
- add GTR-derived phenotype mining as a second evidence stream
- define a GTR source ingestion path
- preserve distinction between 1) literature evidence and 2) clinical utilization evidence
- identifier validation / harmonization against HGNC / Ensembl

### v3
- integrated meta-scoring across:
    - literature-derived sources
    - GTR-derived sources
- citation-aware or evidence-aware weighting extensions
- cross-phenotype comparisons
- richer provenance and source-confidence modeling

---

## Relationship to repo2 (variant_annotation_pipeline)

This repository complements:
`variant_annotation_pipeline (repo2)`
By improving:
`interpretation layer → gene-set quality → biological conclusions`

Repo2 (variant_annotation_pipeline) answers:
`What variants are present?`

This repo (gene_set_consensus) answers:
`Which genes have the strongest cross-source support
for relevance to a phenotype?`

---

## Summary
`gene_set_consensus transforms multiple phenotype-associated gene lists into a reproducible, evidence-aware consensus ranking, while preserving provenance and preparing for future integration of both literature-derived and GTR-derived evidence.`

# End of Repo Brief (v1)