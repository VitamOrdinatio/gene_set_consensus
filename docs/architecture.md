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

## Scientific Revision Architecture

GSC outputs are treated as versioned scientific interpretations rather than immutable biological truth.

Scientific knowledge evolves over time due to:
- larger cohorts
- revised phenotype definitions
- updated consortium analyses
- improved statistical frameworks
- new publications
- revised curation standards

Therefore, GSC preserves:
- source releases
- acquisition timestamps
- publication anchors
- evidence channels
- identifier mapping provenance
- processing versions
- rule configurations

rather than treating any gene set as permanently authoritative.

---

## Evidence Channels

GSC preserves distinct evidence channels independently.

Example:
- browser-derived SNV/indel burden evidence
- publication-derived joint CNV + SNV evidence

These channels are intentionally not flattened into a single opaque evidence source.

This allows future users to distinguish:
- direct statistical evidence
vs
- publication-level interpretive assertions

---

## Release-Aware Design

Future GSC releases may preserve:
- source_release
- source_download_date
- source_checksum
- identifier_map_version
- rule_set_version
- release manifests

This allows deterministic regeneration of historical outputs.

Planned future release-layer directories include:

```text
config/releases/
docs/releases/
```

---

## Identifier Governance

Identifier harmonization is treated as a governed process.

GSC therefore:

- preserves original source identifiers
- uses pinned identifier maps
- separates live API resolution from deterministic execution
- avoids unsafe implicit merges

External APIs such as:

- `MyGene.info`
may be used to construct pinned local resources, but production GSC runs should consume versioned local identifier maps.

---

## Consensus Score Interpretation

The GSC consensus score reflects:

- aggregated cross-source support

not:

- pathogenicity probability
- penetrance
- causal certainty

Higher scores indicate stronger multi-source evidence support within the configured phenotype context.

---