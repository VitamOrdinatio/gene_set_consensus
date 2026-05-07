# GSC Architecture

## Purpose

`gene_set_consensus` (GSC) is a phenotype-scoped gene-level evidence harmonization and consensus construction pipeline.

GSC transforms heterogeneous biological, statistical, clinical, and translational evidence sources into deterministic, provenance-aware phenotype-scoped gene evidence.

GSC is designed to preserve evidence semantics rather than flattening all evidence into a single undifferentiated signal.

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

## Evidence Semantics Layer

GSC distinguishes between different categories of evidence semantics.

Examples include:

| Evidence Type | Example Source | Interpretation |
|---|---|---|
| statistical association | Epi25 | disease-associated signal |
| functional localization | MitoCarta | subcellular/pathway localization |
| clinical utilization | GTR | real-world diagnostic testing usage |
| clinical interpretation | future ClinVar overlays | submitted clinical variant interpretation |
| literature-derived overlays | publications | curated or exploratory biological assertions |

These evidence channels are intentionally preserved independently.

GSC avoids treating all evidence as interchangeable.

This distinction is critical because:

```text
utilization does not equal causality
localization does not equal disease association
association does not equal mechanistic certainty
```

Future scoring frameworks may weight evidence differently depending on semantic category.

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

However, evidence interpretation is governed separately from file parsing.

Two sources may share similar file structures while carrying fundamentally different evidence semantics.

For example:

- a statistically validated cohort-derived gene list
- a clinically utilized diagnostic panel-derived gene list

may both appear as TSV files, yet represent distinct evidence classes requiring different downstream interpretation policies.

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

## Raw Evidence vs Summarized Evidence

GSC distinguishes between:

### Raw Evidence

Detailed parser-level outputs preserving:

- ontology relationships
- source rows
- clinical assertions
- test metadata
- parser provenance
- extraction-rule provenance

Raw evidence prioritizes:
- reproducibility
- auditability
- future reinterpretation

---

### Summarized Evidence

Collapsed phenotype-scoped summaries intended for downstream aggregation and consensus scoring.

Summaries may apply:
- ontology normalization
- duplicate collapse
- broad test suppression
- evidence weighting
- source-tier interpretation policies

This distinction is especially important for complex sources such as:
- GTR XML
- future ClinVar XML
- ontology-expanded evidence systems

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

GSC should remain a stable evidence harmonization engine.

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

## XML Adapter Architecture

Certain evidence sources are distributed as large structured XML datasets.

Examples include:
- GTR XML
- future ClinVar XML

These sources require:
- streaming parsers
- ontology-aware extraction
- parser versioning
- extraction-rule versioning
- release-scoped provenance

GSC therefore separates:

```text
parser behavior
```

from:

```text
scientific interpretation policy
```

This allows the same pinned XML snapshot to be reinterpreted under evolving phenotype definitions without modifying raw source data.

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