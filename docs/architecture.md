# GSC Architecture

## Purpose

`gene_set_consensus` (GSC) is a phenotype-scoped gene-level evidence construction pipeline.

It transforms heterogeneous phenotype-associated gene lists into deterministic, provenance-aware consensus gene evidence.

---

## Core Identity Model

The core GSC evidence record is:

```text
(phenotype, gene_id)
```
This means one row represents:
`one gene evaluated within one phenotype context`

GSC is not sample-specific.

---

## System Boundary

GSC belongs to the gene-level overlay layer.

```text
GSC = phenotype-scoped gene evidence
RDGP = sample-scoped gene prioritization
VDB = variant-centric storage
RSP = expression / functional evidence
```

GSC does not perform variant interpretation, sample-level scoring, or enrichment analysis.

---

## Pipeline Flow

```text
phenotype config
source manifest
identifier map
source files
   ↓
input validation
   ↓
source adapters
   ↓
identifier normalization
   ↓
gene-source matrix construction
   ↓
frequency table construction
   ↓
weighted consensus scoring
   ↓
provenance table generation
   ↓
output contract validation
   ↓
reproducibility validation
```

---

## Separation of Concerns

| Layer           | Responsibility                   |
| --------------- | -------------------------------- |
| Config          | execution behavior               |
| Source manifest | source provenance metadata       |
| Adapter         | source file parsing              |
| Normalization   | gene identity mapping            |
| Aggregation     | cross-source membership          |
| Scoring         | deterministic consensus evidence |
| Provenance      | evidence traceability            |
| Validation      | contract enforcement             |

---

## Source Adapters

Adapters translate external file structures into a common internal shape.

The internal source shape is:
- `gene_symbol`
- `gene_id`
- `evidence_label`
- `notes`

Adapter choice is based on file structure, not biological meaning.

Examples:
| File shape                                      | Adapter             |
| ----------------------------------------------- | ------------------- |
| simple TSV with `gene_symbol`                   | `generic_gene_list` |
| GTR-style TSV with condition/test/panel columns | `gtr_panel`         |

---

## Scoring Model

The v1 scoring model is intentionally simple and explainable.

```text
source_count = number of contributing sources
weighted_source_sum = sum(source weights for contributing sources)
consensus_score = weighted_source_sum
```

The v1 scoring model is intentionally linear and interpretable.

This is not a probability.

It is a deterministic support score.

---

## Provenance Model

Every consensus gene record receives a `provenance_id`.

The final consensus table can be joined to the provenance table:

```text
consensus_gene_set.tsv.provenance_id
↓
gene_provenance.tsv.provenance_id
```

This makes each gene-level evidence record traceable to contributing source rows.

---

## Downstream Integration
GSC outputs are designed to be consumed by downstream systems.

---

### RDGP

RDGP may join GSC evidence after selecting a phenotype context:

```text
RDGP(sample_id, gene_id)
JOIN
GSC(phenotype, gene_id)
```

The phenotype must be explicit.

---

### VDB

VDB compatibility requires stable gene identifiers:

- `gene_id`
- `gene_symbol`

---

### RSP

RSP may later provide functional evidence. If incorporated into GSC, it must remain phenotype-scoped.

---

## Runtime Model

Each run uses one `run_id`.

Run-scoped artifacts are written to:

```text
logs/{run_id}/
data/interim/{run_id}/
data/processed/{run_id}/
```

Final phenotype outputs are written to:
```text
results/tables/{phenotype}/
results/reports/{phenotype}/
```

---

## Determinism

GSC is designed so that identical inputs and configurations produce identical outputs.

Determinism is enforced through:
- explicit source weighting
- deterministic sorting
- stable provenance identifiers
- duplicate collapsing rules
- reproducibility validation scripts

---

## Design Principle

GSC should remain a stable engine.

Phenotype-specific behavior should be controlled by:

```text
config/phenotypes/*.yaml
manifests/sources/*.yaml
external source files
```

not by rewriting pipeline code.

---