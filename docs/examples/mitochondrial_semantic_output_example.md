# Mitochondrial Semantic Output Example

This example demonstrates how GSC separates contextual mitochondrial biology from clinical utilization evidence during mitochondrial-focused semantic integration.

Example table:

```text
docs/examples/tables/mitochondrial_semantic_selected_genes.tsv
```

---

# Scientific Context

The mitochondrial semantic release integrates evidence from:

| Source | Semantic Role |
|---|---|
| MitoCarta | functional mitochondrial localization |
| GTR mitochondrial panels | clinical utilization |

These represent fundamentally different evidence categories.

GSC explicitly preserves this distinction.

---

# Example Interpretation

## POLG

`POLG` demonstrates semantic convergence between:

- functional mitochondrial localization
- clinical utilization

This produces:

```text
contextual_biology_score = 2.0
utilization_score        = 1.0
semantic_consensus_score = 3.0
```

Importantly:

```text
functional localization
≠
disease causality
≠
clinical utilization
```

GSC preserves these distinctions explicitly.

---

## TWNK

`TWNK` demonstrates a similar pattern:

- mitochondrial localization support from MitoCarta
- mitochondrial disease clinical utilization evidence from GTR

This produces combined semantic evidence without conflating biological localization with pathogenic certainty.

---

## TFAM / SURF1 / CYC1

These genes provide important examples of contextual biology evidence.

Within the MitoCarta semantic context:

```text
semantic_channel = contextual_biology
```

These genes receive strong contextual biology support due to mitochondrial localization evidence.

However, when represented solely through GTR utilization evidence, they receive:

```text
semantic_channel = clinical_utilization
```

with lower semantic consensus scores.

This demonstrates an important architectural feature of GSC:

```text
the same gene may appear under multiple semantic evidence contexts
```

depending on evidence origin and biological interpretation.

---

# Semantic Interpretation

This example illustrates several important GSC concepts:

| Principle | Demonstrated |
|---|---|
| contextual biology separation | yes |
| utilization separation | yes |
| ontology-aware scoring | yes |
| semantic decomposition | yes |
| provenance-aware interpretation | yes |

---

# Key Observation

Many gene prioritization systems collapse all mitochondrial evidence into a single undifferentiated score.

GSC instead distinguishes:

- biological localization
- clinical utilization
- disease association
- exploratory evidence

This allows downstream workflows to reason about:

```text
why a gene appears important
```

rather than merely:

```text
how many sources mention the gene
```

which improves interpretability and downstream translational utility.