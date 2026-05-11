# CHANGELOG

All notable changes to `gene_set_consensus` (GSC) will be documented in this file.

This project follows a deterministic, provenance-aware development philosophy emphasizing:

- semantic transparency
- reproducibility
- ontology governance
- backward-compatible architectural migration
- explicit validation behavior

---

# [Unreleased]

## Planned

### Semantic Expansion

- ClinVar semantic integration
- OMIM integration
- GenCC integration
- PanelApp integration
- transcriptomic convergence overlays
- probabilistic semantic scoring exploration
- cross-phenotype semantic calibration
- semantic conflict-resolution framework

### Infrastructure

- GitHub Actions CI
- SVG architecture diagrams
- release artifact packaging
- formal semantic release tagging

---

# [v0.3.0-semantic-ontology]

## Added

### Semantic Ontology Architecture

Introduced explicit semantic ontology separation including:

- `evidence_semantics`
- `evidence_tier`
- `semantic_channel`

Supported semantic categories now include:

- `statistical_association`
- `functional_localization`
- `clinical_utilization`
- `exploratory_literature`

Supported semantic channels now include:

- `direct_disease`
- `contextual_biology`
- `clinical_utilization`
- `exploratory_literature`

---

### Release-Driven Runtime

Introduced release manifest execution model:

```bash
python run_pipeline.py \
  --release config/releases/<release>.yaml
```

Release manifests now define:

- phenotype configuration
- source manifests
- scoring profiles
- release metadata
- semantic expectations
- provenance behavior

---

### Semantic Scoring Profiles

Added phenotype-scoped semantic scoring profiles:

- `epilepsy_semantic_v0.1.yaml`
- `mitochondrial_semantic_v0.1.yaml`

Scoring profiles now support:

- semantic weighting
- inflation-aware behavior
- ontology-aware aggregation
- utilization interpretation

---

### Inflation Controls

Introduced semantic inflation mitigation logic including:

- GTR panel-size classification
- utilization saturation behavior
- deterministic aggregation safeguards
- semantic separation of utilization vs disease evidence

---

### GTR Scope Classification

Introduced empirical GTR panel classification categories:

- `targeted_gene`
- `small_panel`
- `medium_panel`
- `large_panel`

Implemented direct GTR classification validation tests.

---

### Validation Infrastructure

Expanded validation framework including:

- ontology validation
- semantic namespace locking
- release manifest validation
- scoring profile validation
- semantic output contract validation
- semantic inflation tests
- provenance integrity validation
- deterministic runtime validation

Current validation suite:

```text
43 automated tests
```

---

### Documentation

Major README rewrite introducing:

- semantic ontology framework
- architecture diagrams
- release runtime documentation
- inflation control rationale
- semantic evidence philosophy
- downstream ecosystem integration

Added semantic ontology infographic.

---

### Runtime Infrastructure

Modernized `Makefile` for semantic release execution including:

- semantic release targets
- scoring profile validation
- release validation
- unified validation execution

---

## Changed

### Architectural Identity

GSC evolved from:

```text
weighted consensus aggregation
```

to:

```text
semantic ontology-driven evidence integration
```

---

### Release Naming

Renamed active releases from legacy weighted-tier naming:

```text
epilepsy_gold_bronze_gtr_experimental
```

to:

```text
epilepsy_semantic_gtr_experimental
```

and:

```text
mitocarta_gtr_experimental
```

to:

```text
mitochondrial_semantic_gtr_experimental
```

---

### Release Validation Logic

Release validators now prioritize:

```text
evidence_tier
```

over legacy:

```text
weight_tier
```

during semantic validation.

---

### Runtime Semantics

Semantic scoring behavior transitioned toward ontology-governed execution while preserving deterministic backward compatibility.

---

## Deprecated

### Legacy Weighted-Tier Terminology

Legacy terminology remains supported for migration compatibility:

- `weight_tier`
- `gold_bronze`
- source-count-oriented ranking semantics

These remain transitional compatibility layers and are no longer considered the primary architectural abstraction.

---

## Fixed

### Aggregation Bugs

Resolved incorrect aggregation behavior producing inflated counts for certain GTR-integrated outputs.

---

### Runtime Metadata Propagation

Resolved incomplete scoring profile propagation during release execution.

---

### Output Validation Gaps

Resolved missing semantic validation coverage including:

- forbidden columns
- invalid semantic channels
- invalid evidence tiers
- score mismatch detection

---

### GTR Metadata Handling

Resolved missing or stale GTR utilization metadata propagation into consensus outputs.

---

# [v0.2.0-weighted-tier]

## Added

### Weighted Evidence Aggregation

Introduced weighted evidence tiers:

- gold
- silver
- bronze

to improve prioritization behavior beyond naive source counting.

---

### Phenotype Configurations

Introduced phenotype-scoped YAML configuration system.

---

### Source Manifests

Introduced source provenance manifests for:

- epilepsy
- mitochondrial disease

---

### Initial GTR Integration

Introduced early experimental GTR utilization ingestion.

---

## Limitations

This architecture still lacked:

- semantic evidence separation
- ontology-aware channels
- inflation controls
- semantic scoring profiles

---

# [v0.1.0-source-count]

## Added

### Initial Deterministic Consensus Framework

Initial release implementing:

- deterministic source overlap aggregation
- identifier normalization
- provenance-aware outputs
- phenotype-scoped execution
- reproducible runtime behavior

---

### Early Source Adapters

Initial support for:

- Epi25
- MitoCarta
- literature-derived gene lists

---

## Limitations

Initial architecture used naive overlap counting and lacked semantic evidence modeling.