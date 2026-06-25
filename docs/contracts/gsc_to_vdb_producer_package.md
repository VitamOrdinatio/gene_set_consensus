# GSC to VDB Producer Package

## Purpose

This document defines the canonical producer package that Gene Set Consensus (GSC) presents to the Variant Database (VDB) for ingestion.

The purpose of this document is to establish the producer-side preservation boundary between GSC and VDB.

This document does **not** define:

* database schemas
* ingestion algorithms
* persistence models
* namespace brokerage implementation

Instead, it defines the authoritative evidence package that VDB is expected to preserve.

---

# Producer–Consumer Boundary

The VDB ingestion interface begins at the producer's certified release boundary.

Internal derivation artifacts (for example, `data/processed/`) are implementation details of GSC and are **not** required for first-generation VDB interoperability.

The authoritative producer package consists of:

```text
Certified GSC-TEP
+
Authoritative producer release artifacts
```

These together define the complete evidence product.

---

# Certified Producer Packages

## Package 1

Release

```text
epilepsy_semantic_gtr_experimental_v0.1
```

Certified run

```text
run_2026_06_22_184534
```

Transport artifact

```text
results/teps/gsc/
└── epilepsy_semantic_gtr_experimental/
    └── run_2026_06_22_184534/
        └── gsc_tep.json
```

Authoritative producer release

```text
results/runs/run_2026_06_22_184534/
```

Required companion artifacts

```text
tables/
    consensus_gene_set.tsv
    gene_provenance.tsv
    source_contributions.tsv

reports/
    final_run_manifest.yaml
    validation_report.md
```

Certification status

```text
CERTIFIED
```

---

## Package 2

Release

```text
mitochondrial_semantic_gtr_experimental_v0.1
```

Certified run

```text
run_2026_06_23_015533
```

Transport artifact

```text
results/teps/gsc/
└── mitochondrial_semantic_gtr_experimental/
    └── run_2026_06_23_015533/
        └── gsc_tep.json
```

Authoritative producer release

```text
results/runs/run_2026_06_23_015533/
```

Required companion artifacts

```text
tables/
    consensus_gene_set.tsv
    gene_provenance.tsv
    source_contributions.tsv

reports/
    final_run_manifest.yaml
    validation_report.md
```

Certification status

```text
CERTIFIED
```

---

# Required Producer Package Components

| Component                  | Required | Purpose                                                                          |
| -------------------------- | :------: | -------------------------------------------------------------------------------- |
| `gsc_tep.json`             |     ✓    | Transport artifact containing semantic priors, identity, and artifact references |
| `consensus_gene_set.tsv`   |     ✓    | Canonical released semantic consensus                                            |
| `gene_provenance.tsv`      |     ✓    | Per-gene provenance summary                                                      |
| `source_contributions.tsv` |     ✓    | Source contribution topology and preservation metadata                           |
| `final_run_manifest.yaml`  |     ✓    | Authoritative producer execution manifest                                        |
| `validation_report.md`     |     ✓    | Producer validation evidence                                                     |

---

# Internal Producer Artifacts

The following artifacts document how GSC produced the released evidence:

```text
data/processed/<run_id>/

    gene_source_matrix.tsv
    gene_frequency_table.tsv
    scored_gene_evidence.tsv
```

These artifacts are valuable for:

* debugging
* algorithm validation
* scientific inspection
* producer development

However, they are **not** part of the producer package presented to VDB and are not required for first-generation interoperability.

---

# Preservation Expectations

VDB should preserve the producer package without collapsing:

* semantic prior identity
* gene namespace
* source gene namespace
* provenance
* source contribution topology
* referenced release artifacts

The producer package should be treated as an immutable certified evidence product.

---

# Guiding Principle

GSC is responsible for producing certified semantic evidence.

VDB is responsible for faithfully preserving that certified evidence.

The producer package defined in this document establishes the boundary between those responsibilities.
