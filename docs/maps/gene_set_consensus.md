# Milestone Map: gene_set_consensus (GSC)

## Purpose
Provide a system to aggregate, normalize, and score gene-level evidence from multiple sources, producing:
    - curated gene-level evidence
    - consensus-scored gene-level evidence
    - provenance-aware gene-level annotations
These outputs serve as overlay evidence for:
    - VAP (annotation context) 
    - RSP (functional interpretation) 
    - RDGP (prioritization weighting) 

GSC converts heterogeneous gene sets into structured, comparable, and auditable gene-level evidence.

---

## Layer Ecosystem
1. provider layer (VDB)
2. contract layer (vdb_rdgp_interface)
3. overlay layer (GSC)
4. reasoning layer (RDGP)

---

## Terminology:
- "gene-level evidence" refers to a gene annotated with one or more supporting sources and associated metadata.
- "gene sets" refer to collections of genes derived from a single source prior to aggregation.

- GSC gene-level evidence is global (not sample-specific) and is applied uniformly across samples unless versioned otherwise

---

## Strategic Value (Moderate → High when integrated)
Signals:
  - data integration (multi-source) 
  - gene-level reasoning 
  - provenance tracking 
  - handling conflicting evidence 
  - preparation for clinical interpretation workflows 

Provenance is preserved in GSC outputs but downstream systems may consume summarized representations (e.g., consensus_score, source_list).

---

## Core Data Model (v1)

At minimum, GSC operates on a gene-centric representation:

Fields:
- gene_symbol
- gene_id (if available)
- source_list
- source_count
- consensus_score
- provenance (source names, timestamps)

### Example Record (v1)

A single gene-level evidence record should resemble:

- gene_symbol: TP53
- gene_id: ENSG00000141510
- source_list: ["OMIM", "ClinVar", "Literature_Study_X"]
- source_count: 3
- consensus_score: 3
- provenance:
    - source: OMIM
      version: 2024-01
    - source: ClinVar
      version: 2024-02
    - source: Literature_Study_X
      year: 2022

---

## Standard Output Format (v1)

All downstream integrations (VDB, RSP, RDGP) should consume:

- gene_symbol
- consensus_score
- source_list
- source_count

## Milestones

### M1 — Basic Gene Set Aggregation (Utility Layer)

Implement:
- ingest simple gene lists (e.g., text/CSV) 
- normalize: 
    - gene symbols 
    - casing 
    - duplicates 
- produce: 
    - unified gene set 

Goal:
A clean, deduplicated gene set from multiple inputs

---


### M2 — Multi-Source Aggregation + Metadata

Extend to:
- support multiple input sources: 
    - curated lists 
    - literature-derived lists 
- attach metadata: 
    - source name 
    - source type 
    - confidence label (if available) 

Output:
- gene-level evidence records with attached source lists

Goal:
gene-level evidence preserves full source provenance rather than collapsing to simple membership

---


### M3 — GTR Integration (Structured External Source)

Add:
- ingestion from GTR-derived data (your prior work) 
- mapping: `condition → gene → test evidence`
- integrate with existing sets 

Output:
- gene-level evidence enriched with clinical test context 

Goal:
GSC moves from generic aggregation → clinically contextualized gene-level evidence

---


### M4 — Consensus Scoring Layer

Implement initial deterministic scoring:

- base score = number of supporting sources
- optional weighting:
    curated sources > literature-derived > automated
- preserve raw counts alongside score

Important:
- scoring must be explainable
- no black-box weighting in v1
  
Handle:
- conflicting sources 
- sparse support 

Goal:

Genes have quantified and explainable support across heterogeneous sources.

---


### M5 — Provenance + Versioning

Track:
- which sources contributed to each gene 
- when gene-level evidence records were generated
- version identifier for gene-level evidence 

Output:
- versioned gene-level evidence artifact

Example:
- gene_evidence_v1
- gene_evidence_v2

Goal:
gene-level evidence are reproducible and auditable

---


### M6 — Integration with VDB (Critical Upgrade)

GSC outputs must be compatible with VDB gene identifiers (gene_symbol or gene_id)

This enables GSC outputs to be directly joined with variant-level evidence in VDB for downstream prioritization workflows.

Enable:
- linking gene-level evidence to VDB gene table 
- ability to: 
    - query genes in VDB that belong to specific sets 
    - attach consensus scores to gene records 

Goal:
GSC becomes data-aware, not standalone

---


### M7 — Integration with RSP (Functional Context)

GSC outputs must be compatible with RSP gene identifiers (gene_symbol or gene_id)

Add:
- ability to incorporate: 
    - expression-derived gene signals 
    - network convergence outputs 
- update consensus scores with: 
    - functional evidence 

Goal:
gene-level evidence reflect multi-modal evidence

---


### M8 — Validation + Edge Case Handling

Define and document:
- assumptions: 
    - gene symbol normalization correctness 
- limitations: 
    - incomplete coverage of gene space 
- edge cases: 
    - conflicting gene assignments 
    - outdated gene symbols 
    - sparse data sources 
- validation: 
    - compare against known curated gene-level evidence 

Validation should include:

- known disease gene recovery:
    curated disease genes should appear in high-ranking positions

- cross-source consistency:
    genes present in multiple sources should have higher scores

- stability check:
    re-running aggregation produces identical outputs

- spot-check:
    manually verify 3–5 genes across sources

- identifier consistency:
    gene_symbol and gene_id mappings remain stable across sources


Goal:
System is defensible and transparent

---


## Release Gate (Public v1.0)

GSC is portfolio-ready when:
- supports multi-source aggregation 
- includes GTR integration 
- produces consensus gene-level evidence 
- tracks provenance per gene 
- generates versioned outputs 
- integrates (at least minimally) with VDB 
- documentation includes: 
    - assumptions 
    - limitations 
    - edge cases 
    - validation strategy 
    - implementation details 

At this point:
GSC v1.0 (public)

---


## Future Upgrades (Post v1.0)
- advanced weighting models 
- disease-specific gene set stratification 
- automated literature ingestion 
- ontology integration (e.g., pathways, GO terms) 
- tighter RDGP coupling 

---


## Critical Teaching Point
This repo is NOT:
“a list of genes”

The gene_set_consensus (GSC) repo is 
`a system for managing uncertainty in gene-level evidence across heterogeneous sources.`

---


## How GSC Fits in the Overall System:

```text
GSC → provides:
    gene-level evidence
    consensus scores
    provenance

Used by:
    VAP (annotation context)
    RSP (functional interpretation)
    RDGP (prioritization weighting)

Integrated via:
    VDB (central hub)
```

---


## One Sentence Summary
GSC answers: “Which genes have supporting evidence, and how strong is that support?”

---


