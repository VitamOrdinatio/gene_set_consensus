#================================
# docs/design.md
#================================

# Design Document - gene_set_consensus repo

## Overview

This repository implements a modular system to:

`Ingest → Normalize → Aggregate → Score → Output`

phenotype-associated gene lists across multiple evidence sources.

The central design goal is to build a traceable consensus layer for genomic interpretation.

---

## Core Design Philosophy

This repository is built around the following principles:

- provenance must never be lost
- interpretation quality depends on source quality
- literature evidence and clinical utilization evidence are related but distinct
- simplicity and auditability are more important than clever weighting in v1
- the system should scale from curated TSV inputs to future mined sources such as GTR

---

## Evidence Model

The repository is designed around two major evidence classes:

### 1. Literature-Derived Evidence

Examples:
- ClinGen-derived gene lists
- OMIM-derived gene lists
- peer-reviewed phenotype gene lists
- manually curated disease panels
- resources such as MitoCarta or Genes4Epilepsy

### 2. Clinical Utilization Evidence (Future)

Examples:
- GTR-derived phenotype-associated test gene lists
- genes appearing repeatedly in clinically deployed assay panels

### Design Principle

These evidence classes should remain conceptually distinct.

`Literature evidence ≠ clinical utilization evidence`

They may later be integrated into a unified meta-score, but they should not be conflated silently.

---

## Architecture

### High-Level Flow (v1)

```yaml
YAML config
    ↓
Load source metadata
    ↓
Load gene lists
    ↓
Normalize identifiers
    ↓
Aggregate per gene
    ↓
Compute weighted scores
    ↓
Export consensus outputs
```

### High-Level Flow (future v2/v3)
YAML config
    ↓
Load curated literature sources
    ↓
Mine phenotype-associated GTR sources
    ↓
Normalize identifiers
    ↓
Aggregate by source class
    ↓
Compute literature_score
    ↓
Compute clinical_utilization_score
    ↓
Compute integrated_meta_score
    ↓
Export outputs

---

## Directory Structure

```text
gene_set_consensus/
├── data/
│   ├── input/
│   │   ├── config.yaml
│   │   └── sources/
│   └── output/
├── docs/
├── scripts/
├── src/
│   ├── io/
│   ├── processing/
│   ├── scoring/
│   ├── models/
│   └── validation/
└── tests/
```

---

## Data Model

### GeneRecord

Represents one aggregated gene after cross-source integration.

Suggested fields:

- gene_symbol
- ensembl_id
- gene_id
- phenotype
- supporting_sources
- source_types
- tier_counts
- weighted_score
- consensus_score

### SourceMetadata

Represents one source gene list.

Suggested fields:

- source_name
- source_type
- tier
- weight
- file_path
- phenotype
- notes

### Future SourceType enum

Examples:

- literature
- clinical_utilization
- expert_curation
- user_curated

---

## Processing Steps

### Step 1 - Load Config

Parse YAML and construct:

- phenotype
- weights
- source metadata
- output settings

### Step 2 - Load Gene Lists

Each source file is loaded into memory.

Requirements:

- must contain `gene_symbol`
- no implicit identifier rescue
- provenance retained per row/source

### Step 3 - Normalize

Minimal normalization only:

- uppercase gene symbols
- strip whitespace
- remove duplicate rows per source
- preserve original source metadata

### Step 4 - Aggregate

Group by:
`gene_symbol`

Track:

- number of supporting sources
- source names
- source types
- tier counts
- optional IDs carried through when present

### Step 5 - Score

Compute:

- weighted_score
- consensus_score

Future versions may also compute:

- literature_score
- clinical_utilization_score
- meta_score

### Step 6 - Output

Write TSV:
`data/output/<phenotype>_consensus.tsv`

Optional:

- source summary table
- run metadata table

---

## Error Handling

- missing required columns → fail fast
- empty files → warning or fail depending on settings
- duplicate rows → deduplicate within source
- conflicting identifier fields → preserve but flag
- ambiguous identifiers → do not auto-correct in v1

---

## Design Constraints
- no mutation of input source files
- all transformations must be traceable
- all scores must be auditable from input provenance
- no hidden rescue logic for bad identifiers
- reproducibility is prioritized over convenience

---

## Scoring Design

### v1 Scoring

Use explicit tier weights:

- gold = 1.0
- silver = 0.6
- bronze = 0.3

Score per gene:
`weighted_score = sum(source_weight per source containing gene)`

Optional:
`consensus_score = weighted_score × consensus_multiplier`

#### Why this is acceptable for v1

- transparent
- explainable
- easy to debug
- easy to inspect against source provenance

#### Why not more complex in v1

Complex weighting is tempting, but premature.

v1 is about:
`building a clean evidence integration engine`
not about claiming perfect biological truth.

---

## Identifier Policy

This repository is intentionally conservative about identifiers.

### v1 Policy
- gene_symbol is the minimum required field
- ensembl_id is strongly preferred when available
- gene_id may be carried through when present
- ambiguous or conflicting identifiers are preserved and flagged, not silently corrected


### Rationale

This design avoids injecting hidden noise into the consensus engine.

```text
Uncertain identifier rescue can create false confidence. v1 therefore prefers explicit provenance and visible ambiguity over automatic correction.
```

---

## Future Direction

Later versions may add explicit identifier validation or harmonization against resources such as HGNC or Ensembl, but only as transparent, auditable steps.

---

## GTR Integration Plan (Future)

### Motivation

GTR provides a way to represent:
`clinical utilization evidence`
rather than purely literature-derived evidence.

This is valuable because it can reflect:
- genes actually used in diagnostic testing
- phenotype-associated panel design in the clinical world
- frequency of gene reuse across real clinical assays

### Planned Future Capability

A future GTR ingestion module may:

- accept phenotype term(s)
- query or parse GTR-derived assay/gene relationships
- generate phenotype-associated gene lists
- convert GTR output into the same schema used by curated TSV inputs

### Important Caution

GTR is not ground truth.

It should be treated as:
`clinical utilization evidence`
not:
`definitive mechanistic or causal evidence`

---

## Extensibility

Future modules include:
- identifier_validation.py
- citation_weighting.py
- ontology_mapping.py
- gtr_ingest.py
- meta_scoring.py

---

## Performance Considerations
- v1 data size is small (gene lists)
- pandas is sufficient
- no need for distributed computing
- future GTR ingestion may increase data volume modestly, but still remains lightweight relative to sequencing pipelines

---

## Relationship to Other Repositories

### repo2 — variant_annotation_pipeline

repo2 provides:

- variant calling
- annotation
- gene-level contextualization

gene_set_consensus improves the quality of the contextualization layer by supplying stronger, provenance-aware phenotype gene rankings.

### Broader Portfolio Role

This repository demonstrates that:
`the challenge in genomics is not only calling variants,
but interpreting them against high-quality evidence structures`

---

## Summary

```text
Design emphasizes clarity, provenance, traceability, and staged growth:
v1 = literature-driven consensus
v2 = add GTR-derived clinical utilization evidence
v3 = integrated evidence-aware meta-scoring
```

---

# End of Design Document





















































