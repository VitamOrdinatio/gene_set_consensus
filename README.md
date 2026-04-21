# gene_set_consensus

## Overview

`gene_set_consensus` (GSC) is a bioinformatics system for constructing **phenotype-specific, evidence-weighted gene-level evidence models** by integrating multiple heterogeneous gene lists into a unified, provenance-aware consensus framework.

Unlike enrichment tools that *consume* gene sets, GSC is designed to **construct, evaluate, and version gene sets themselves**.

It produces gene-level evidence models that reflect:
- cross-source agreement
- source authority (e.g., curated vs literature-derived)
- explicit weighting schemes
- full provenance per gene
- phenotype-specific context

---

## Motivation

Downstream interpretation in genomics is only as strong as the gene sets used to 
contextualize results.

```text
Noisy gene sets → weak biological conclusions
```
Most RNA-seq and variant pipelines rely on predefined gene sets (e.g., GO terms, MSigDB collections), but these sets:
    • are static snapshots 
    • do not encode source-level authority 
    • cannot be adapted to specific research contexts 
    • do not preserve provenance at the gene level 

GSC addresses this gap by providing a reproducible system for:

```text
multi-source integration → weighted consensus → phenotype-specific gene evidence
```


---

## Core Concept

```text
Multiple phenotype-associated gene lists
+ explicit source weighting (gold / silver / bronze)
+ provenance tracking
→ consensus gene-level evidence model
```

---

## What GSC Produces

GSC does not produce a simple gene list.

It produces a **gene-level evidence model**, where each gene is associated with:

- multiple independent sources of support
- source-level provenance
- explicit weighting based on source authority
- a consensus score reflecting both support and agreement

Conceptually:

```text
gene → {sources, weights, provenance} → consensus_score
```

This differs from traditional gene sets, where membership is binary:

`gene ∈ set → yes/no`

GSC instead represents:

```text
“How strongly is this gene supported for this phenotype,
and by which sources?”
```

GSC explicitly preserves uncertainty.

```text
Conflicting or sparse evidence is not collapsed into a single decision,
but retained as part of the gene-level evidence model.
```

This allows downstream systems to reason about:
- agreement vs disagreement across sources
- strength vs absence of evidence

---


## Key Distinction: GSC vs DEG → GO → MSigDB Workflows

Traditional workflows vs. GSC:
```text
Traditional gene sets treat membership as binary:
a gene is either in the set or not.

GSC instead models how strongly a gene is supported
for a phenotype, and why.
```


A common transcriptomics workflow is:

```text
DEG list → enrichment (e.g., g:Profiler) → GO / MSigDB terms
```

This answers:

`“What biological processes are enriched in my gene list?”`

GSC answers a fundamentally different question:

```text
“Are the affected genes already associated with a specific phenotype,
and how strong is that evidence across multiple sources?”
```


---

## Side-by-Side Comparison

```text
Feature
GO / MSigDB / g:Profiler
GSC
Primary role
Gene set consumption
Gene set construction
Input
Gene list
Multiple gene lists (sources)
Output
Enriched pathways / terms
Weighted gene-level evidence
Structure
Ontology-driven (GO DAG)
Evidence-driven (source aggregation)
Weighting
None (flat membership)
Explicit (source tiers / weights)
Provenance
Limited
Full per-gene source tracking
Adaptability
Static (versioned releases)
Dynamic (config-driven per phenotype)
Question answered
“What biology is perturbed?”
“Does this perturbation matter for phenotype X?”
```

---

## Why This Matters
GO and pathway analysis identify biological processes.
GSC identifies phenotype relevance.

These are complementary:

```text
GO → what biology is changing
GSC → whether those changes are clinically meaningful
```

---

## Example Use Case

**Phenotype:** Epilepsy

**Sources:**
- ClinGen (gold)
- OMIM (gold)
- Genes4Epilepsy (silver)
- (future) GTR-derived epilepsy gene associations

**Output:**
- Ranked genes by consensus_score
- Weighted evidence contributions
- Source provenance per gene

**Interpretation:**

```text
This gene is not just present in a list—
it is supported by multiple independent, high-confidence sources.
```


---

## Relationship to Transcriptomics (RSP)

In a transcriptomics workflow:

`RNA-seq → DEGs → GO/pathway analysis`

GSC interacts with transcriptomic outputs in two ways:

1) RSP → GSC
   functional signals (e.g., DEG, network evidence) may be incorporated into GSC evidence models

2) GSC → RSP
   phenotype-scoped gene evidence may be used to interpret transcriptomic perturbations

This bidirectional relationship enables integration of:
    functional perturbation ↔ phenotype relevance

This enables questions such as:

```text
Do EBV-induced transcriptional changes disproportionately affect
genes associated with mitochondrial disease or epilepsy?
```

This bridges:

`functional perturbation → clinical relevance`


---

## Input Requirements

### Config File (YAML)

Defines:
    • phenotype 
    • source files 
    • source types 
    • tier assignments (e.g., gold/silver/bronze) 
    • weighting scheme 

### Gene Lists (TSV)

Minimum:
    • gene_symbol 

Optional:
    • gene_id 
    • ensembl_id 
    • source metadata 

### v1 Source Model
    • curated phenotype gene lists 
    • literature-derived gene sets 
    • manually assembled panels 

Future:
    • GTR-derived gene associations 
    • automated ingestion pipelines 


---

## Output

`data/output/<phenotype>_consensus.tsv`

Fields include:
    • phenotype 
    • gene_symbol 
    • weighted_score 
    • consensus_score 
    • supporting_sources 
    • source_types 
Each row represents:

`(phenotype, gene_id) → evidence model`

## Scoring Philosophy

`More independent support + higher-confidence sources → higher consensus`

Key principles:
    • deterministic scoring 
    • interpretable weighting 
    • no hidden heuristics 
    • full transparency of evidence sources 


---

## System Role

GSC operates within a larger system:

```text
variant_annotation_pipeline → What variants are present?
rnaseq_pipeline (RSP)       → What biology is perturbed?
gene_set_consensus (GSC)    → Which genes matter for this phenotype?
rare_disease_gene_prioritization (RDGP) → What matters for this patient?
```

GSC provides phenotype-scoped, gene-level evidence overlays that support downstream interpretation.


---

Why Not Just Use MSigDB?

MSigDB provides curated gene sets, but:


```text
MSigDB provides predefined gene sets with binary membership.

GSC constructs phenotype-specific gene evidence models that:
- integrate multiple sources
- weight sources by authority
- preserve provenance per gene
- produce interpretable consensus scores

This allows downstream systems to reason about evidence strength,
not just gene set membership.
```

GSC enables:
    • combining multiple sources 
    • weighting sources by authority 
    • preserving provenance 
    • adapting gene sets to specific research questions 
    • versioning phenotype-specific evidence models 


---

## Roadmap
### v1
    • multi-source integration 
    • YAML-driven configuration 
    • weighted consensus scoring 
    • provenance tracking 
### v2
    • identifier harmonization 
    • improved curated database integration 
    • GTR ingestion 
### v3
    • integrated literature + clinical evidence modeling 
    • richer weighting schemes 
    • tighter integration with transcriptomic (RSP) outputs 
    • support for convergence analyses 

## Disclaimer

```text
This tool does NOT establish causality.
It provides structured, weighted evidence of gene–phenotype association.
```


---

## Author Philosophy

```text
Reproducibility > convenience
Traceability > automation
Signal > noise
Evidence > assumption
```


---

## License
See LICENSE file.

---