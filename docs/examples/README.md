# GSC Example Outputs

This directory contains curated example outputs demonstrating how `gene_set_consensus` (GSC) performs semantic evidence integration and ontology-aware consensus ranking.

These examples are intentionally lightweight, human-readable artifacts designed for:

- documentation
- interpretation
- architecture demonstration
- semantic scoring explanation
- downstream integration examples

Unlike runtime-generated outputs under:

```text
results/
```

the files in this directory are curated examples intended to remain version-controlled and stable across releases.

---

# Directory Structure

| Path | Purpose |
|---|---|
| `epilepsy_semantic_output_example.md` | epilepsy semantic ranking interpretation |
| `mitochondrial_semantic_output_example.md` | mitochondrial semantic ranking interpretation |
| `dee_semantic_output_example.md` | DEE subtype semantic ranking interpretation |
| `nafe_semantic_output_example.md` | NAFE subtype semantic ranking interpretation |
| `tables/epilepsy_semantic_selected_genes.tsv` | curated epilepsy semantic example table |
| `tables/mitochondrial_semantic_selected_genes.tsv` | curated mitochondrial semantic example table |
| `tables/dee_semantic_selected_genes.tsv` | curated DEE subtype semantic example table |
| `tables/nafe_semantic_selected_genes.tsv` | curated NAFE subtype semantic example table |

---

# Example Categories

## Epilepsy Semantic Integration

The epilepsy examples demonstrate integration across semantically distinct evidence sources:

| Source | Semantic Role |
|---|---|
| Epi25 | statistical disease association |
| GTR epilepsy panels | clinical utilization |
| Genes4Epilepsy | exploratory literature aggregation |

These examples illustrate:

- semantic evidence separation
- ontology-aware aggregation
- inflation-aware scoring
- provenance-aware interpretation

Key example genes include:

- `SCN1A`
- `DEPDC5`
- `NPRL3`
- `SYNGAP1`
- `POLG`

---

## Mitochondrial Semantic Integration

The mitochondrial examples demonstrate semantic separation between:

| Source | Semantic Role |
|---|---|
| MitoCarta | functional mitochondrial localization |
| GTR mitochondrial panels | clinical utilization |

These examples illustrate:

- contextual biology modeling
- utilization separation
- semantic decomposition
- ontology-aware scoring

Key example genes include:

- `POLG`
- `TWNK`
- `TFAM`
- `SURF1`
- `CYC1`

---

# Why These Examples Matter

Traditional gene list aggregation systems often collapse heterogeneous evidence into simple overlap counts.

GSC instead models:

- evidence meaning
- evidence semantics
- evidence provenance
- evidence context
- evidence role within biological interpretation

The examples in this directory are intended to demonstrate how semantic decomposition changes downstream interpretability.

---

# Important Note

These examples are illustrative snapshots rather than exhaustive scientific outputs.

Full runtime outputs are generated dynamically under:

```text
results/
```

during release execution.

Example runtime execution:

```bash
python run_pipeline.py \
  --release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml
```

---

# Relationship to Runtime Outputs

| Directory | Purpose |
|---|---|
| `results/` | transient runtime-generated outputs |
| `docs/examples/` | curated documentation artifacts |

This separation preserves:

- reproducibility
- lightweight Git history
- documentation stability
- human-readable interpretability examples

---

# Semantic Architecture Demonstrated

The examples in this directory demonstrate several core GSC architectural concepts:

| Concept | Demonstrated |
|---|---|
| semantic ontology separation | yes |
| inflation-aware scoring | yes |
| provenance preservation | yes |
| contextual biology modeling | yes |
| clinical utilization separation | yes |
| deterministic semantic ranking | yes |

---

# Future Example Expansion

Planned future example categories may include:

- ClinVar semantic integration
- transcriptomic convergence overlays
- semantic variant prioritization
- cross-phenotype semantic comparisons
- network convergence overlays
- probabilistic semantic scoring examples