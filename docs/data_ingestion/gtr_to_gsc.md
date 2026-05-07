# GTR to GSC Data Ingestion Strategy

## Purpose

This document defines the planned strategy for transforming a pinned local snapshot of the NCBI Genetic Testing Registry (GTR) into provenance-aware, phenotype-scoped gene-set products suitable for Gene Set Consensus (GSC).

The goal is not simply to query GTR dynamically, but to:

- preserve reproducibility
- preserve provenance
- support deterministic rebuilding
- support scientific auditability
- support future clinical interpretation workflows

---

# Core Philosophy

## GTR Is a Dynamic Clinical Metadata Resource

Unlike:

- MitoCarta
- Epi25
- literature-derived gene lists

GTR represents:

```text
dynamic clinical testing metadata
```

rather than static scientific consensus.

Therefore, GTR integration requires:
- timestamped acquisition
- pinned source snapshots
- explicit provenance
- careful phenotype-scoping rules

---

# Deterministic Snapshot Philosophy

Derived GTR phenotype products are expected to participate in:
- release manifests
- source manifests
- provenance-aware GSC releases

## Preferred Design

GSC should operate on:

```text
pinned local GTR snapshots
```

rather than:
```text
live online GTR queries
```

This ensures:
- deterministic execution
- reproducibility
- temporal provenance
- stable rebuilds
- auditability

---

# Storage Architecture

## Raw GTR Snapshot

The full GTR FTP snapshot is treated as the immutable source-of-truth artifact.

Example structure:

```text
/mnt/storage/gtr/
├── gtr_ftp.xml.gz
├── gtr_ftp.xml
└── metadata/
    ├── source_metadata.yaml
    └── checksums.tsv
```


---


# Planned vs Active Source Governance

GTR-derived sources may exist in multiple operational states within GSC.

## Active Sources

Active sources are:

- locally staged
- validated
- provenance-aware
- reproducible
- included in deterministic execution

Active sources:
- must pass source manifest validation
- must reference existing local files
- are eligible for release-aware GSC execution

Example:

```text
gtr_epilepsy_panel
status: active
```

---

## Planned Sources

Planned sources represent future intended integrations that are not yet fully staged or validated.

Planned sources may:

- lack finalized local files
- lack completed parsing pipelines
- lack finalized extraction rules
- remain under scientific evaluation

Planned sources:

- remain visible in source manifests
- preserve architectural intent
- support roadmap transparency
- are excluded from strict file existence enforcement

Example:

```text
gtr_mitochondrial_panel
status: planned
```

---

## Governance Philosophy

This distinction allows GSC to:

- preserve deterministic validation
- maintain provenance discipline
- expose future architectural direction
- avoid silently implying operational readiness

The planned vs active distinction is treated as formal governance metadata rather than informal developer notes.

---

# Derived GSC Gene Sets

Phenotype-scoped GTR-derived products are stored separately from the raw snapshot.

Example:

```text
/mnt/storage/gene_sets/
├── gtr_epilepsy/
├── gtr_mitochondria/
```

These are:
- processed
- phenotype-scoped
- provenance-aware
- GSC-ready

The raw XML snapshot remains the canonical source.

---

# Raw vs Derived Boundary

## Canonical Rule

```text
GTR XML snapshot = raw source truth

Parsing logic itself is treated as versioned infrastructure.

GTR-derived phenotype gene sets = processed GSC inputs
```


GSC should never treat phenotype-scoped GTR outputs as raw GTR.

All derived products should preserve provenance links back to:
- source snapshot
- acquisition timestamp
- extraction rules
- matching strategy

---

# Initial GTR v1 Philosophy

## Conservative v1 Design

Initial GTR ingestion should prioritize:

- provenance
- inspectability
- deterministic behavior
- explicit matching

rather than:
- semantic inference
- ontology expansion
- AI-driven disease collapsing

---

# GTR v1 Extraction Rules

Initial extraction should use:

- explicit phenotype keyword matching
- exact panel inclusion extraction
- deterministic filtering
- preservation of matched test metadata

Initial versions should avoid:
- fuzzy ontology inference
- latent disease grouping
- semantic disease expansion
- hidden phenotype collapsing

---

# Example Epilepsy Matching Questions

Important future questions include:

Should epilepsy extraction include:
- epilepsy
- DEE
- infantile spasms
- febrile seizures
- generalized epilepsy
- neurodevelopmental disorders with epilepsy
- mitochondrial epilepsy syndromes

These ontology decisions should remain:
- explicit
- versioned
- documented
- provenance-aware

---

# Initial GTR Evidence Semantics

## GTR Evidence Type

GTR evidence should be interpreted as:

```text
clinical testing utilization evidence
```

not:
- pathogenicity evidence
- mechanistic evidence
- consortium burden significance

This distinction is critically important.


```text
Genes may appear in large exploratory panels,
broad neurodevelopmental panels,
or commercially permissive testing products.
```

Therefore:

```text
raw GTR frequency should not be treated as mechanistic certainty.
```

---

# Potential Future GTR Evidence Channels

Future GTR integration may incorporate:

- panel inclusion frequency
- independent laboratory diversity
- phenotype-specific panel inclusion
- panel size normalization
- panel specificity weighting
- temporal panel evolution
- longitudinal clinical adoption trends

These are considered future expansions beyond initial v1 ingestion.

---

# Planned Provenance Fields

Derived GTR gene products should ideally preserve:

| Field | Description |
|---|---|
| `gene_symbol` | Parsed gene symbol |
| `matched_test_name` | Original matched GTR test name |
| `lab_name` | Reporting laboratory |
| `gtr_accession` | GTR accession ID |
| `matched_keyword` | Keyword responsible for phenotype match |
| `source_snapshot` | GTR snapshot identifier |
| `acquisition_date` | Snapshot acquisition date |
| `panel_size` | Number of genes in originating panel |
| `panel_category` | Clinical test category |
| `extraction_rule_version` | Versioned extraction logic |
| `parser_version` | Versioned parser behavior |

---

# Future Architecture Direction

Future GTR integration may evolve toward:

- ontology-aware phenotype mapping
- disease hierarchy expansion
- weighted panel specificity scoring
- clinical evidence density metrics
- longitudinal release comparison
- transcriptomic integration
- VAP prioritization overlays
- RDGP evidence integration

However, the initial implementation should remain conservative and provenance-first.

---

# Strategic Summary

The guiding philosophy for GTR integration into GSC is:

```text
maximize provenance and inspectability first
```

before pursuing:
- semantic expansion
- ontology inference
- advanced weighting
- AI-assisted interpretation

This preserves:
- scientific rigor
- reproducibility
- clinical auditability
- future extensibility
```

---