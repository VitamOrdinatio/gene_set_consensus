# DEE Semantic Walkthrough

## Purpose

This walkthrough demonstrates how GSC constructs a subtype-aware semantic consensus for developmental and epileptic encephalopathy (DEE).

The example illustrates:

- subtype-specific semantic anchors
- semantic evidence layering
- provenance-aware consensus scoring
- preservation of biologically meaningful subtype structure

---

# Biological Background

Developmental and epileptic encephalopathy (DEE) represents a severe epilepsy subtype characterized by:

- early-onset seizures
- developmental impairment
- heterogeneous genetic etiologies
- strong enrichment for neurodevelopmental genes

The 2024 Epi25 study identified five high-confidence DEE-associated loci:

| Gene |
|---|
| NEXMIF |
| SCN1A |
| STX1B |
| SYNGAP1 |
| WDR45 |

These loci form the direct-disease semantic anchor layer for the DEE semantic release.

---

# Semantic Release

The DEE semantic release is executed using:

```bash
python run_pipeline.py \
  --release config/releases/dee_semantic_gtr_experimental_v0.1.yaml
```

The release integrates:

| Source | Semantic Role |
|---|---|
| Epi25 DEE high-confidence genes | direct disease anchors |
| Genes4Epilepsy | utilization evidence |
| GTR epilepsy evidence | clinical testing utilization |
| broader epilepsy semantic evidence universe| contextual semantic expansion |

---

# Semantic Candidate Universe

The DEE release does not restrict analysis exclusively to the five DEE anchor genes.

Instead, GSC constructs a shared epilepsy-family semantic candidate universe derived from integrated semantic evidence sources.

The DEE subtype anchors influence:

- semantic weighting
- direct disease scoring
- subtype prioritization
- semantic interpretation

while preserving broader contextual evidence relationships.

---

# Example Semantic Layering

## SCN1A

Example semantic interpretation for `SCN1A`:

| Semantic Component | Example Contribution |
|---|---|
| direct_disease_score | DEE subtype anchor |
| utilization_score | strong epilepsy utilization evidence |
| exploratory_score | broader epilepsy semantic support |

Representative output behavior:

```text
gene_symbol=SCN1A
source_count=3
weighted_source_sum=6.0
direct_disease_score=4
utilization_score=1
exploratory_score=0.75
```

This illustrates how subtype-specific anchors combine with broader semantic evidence layers.

---

# Preservation of Subtype Structure

The DEE semantic release preserves the expected high-confidence subtype anchors:

```text
NEXMIF
SCN1A
STX1B
SYNGAP1
WDR45
```

Cross-system validation demonstrated preservation of these subtype anchors across:

- Sys76 Pop!_OS workstation
- MARK Linux HPC environment

See:

- `../validation/comparisons/sys76_vs_mark_release_comparison.md`

---

# Why Semantic Layering Matters

Traditional aggregate scoring approaches may collapse clinically distinct evidence types into a single undifferentiated score.

GSC instead separates evidence into semantic channels including:

- direct disease
- utilization
- contextual biology
- exploratory evidence

This permits biologically interpretable semantic consensus behavior.

Different semantic evidence classes therefore remain independently inspectable during downstream interpretation.

---

# Clinical Interpretation Perspective

A DEE-focused semantic overlay may help contextualize variants identified through:

- whole exome sequencing (WES)
- whole genome sequencing (WGS)
- epilepsy-focused diagnostic panels

The semantic framework is especially useful when multiple moderate-effect loci collectively reinforce subtype-specific biological interpretation.

---

# Key Architectural Concepts Demonstrated

This walkthrough demonstrates:

- subtype-aware semantic overlays
- semantic candidate universes
- provenance-aware evidence integration
- semantic scoring channels
- release-driven execution
- cross-system semantic reproducibility

---

# Related Documents

| Document | Purpose |
|---|---|
| `../design/gsc_architecture.md` | architecture overview |
| `../validation/README.md` | validation documentation |
| `../validation/comparisons/README.md` | reproducibility comparison artifacts |
| `../design/runtime_portability_refactor.md` | runtime portability rationale |

Future extensions may incorporate coding and noncoding variant interpretation overlays generated from downstream variant annotation frameworks such as VAP.