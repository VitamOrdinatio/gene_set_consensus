# Epilepsy Semantic Output Example

This example demonstrates how GSC separates distinct semantic evidence types during epilepsy-focused consensus ranking.

Example table:

```text
docs/examples/tables/epilepsy_semantic_selected_genes.tsv
```

---

# Scientific Context

The epilepsy semantic release integrates evidence from multiple semantically distinct sources:

| Source | Semantic Role |
|---|---|
| Epi25 | direct statistical disease association |
| GTR epilepsy panels | clinical utilization |
| Genes4Epilepsy | exploratory literature aggregation |

Rather than treating all sources equivalently, GSC decomposes evidence into semantic channels.

---

# Example Interpretation

## SCN1A

`SCN1A` demonstrates strong semantic convergence across multiple evidence layers:

- direct disease association (`Epi25`)
- clinical utilization (`GTR`)
- exploratory literature evidence (`Genes4Epilepsy`)

This produces:

```text
direct_disease_score = 4.0
utilization_score    = 1.0
exploratory_score    = 0.75
semantic_consensus_score = 5.75
```

The high direct disease score reflects statistically significant epilepsy burden evidence.

The additional utilization and exploratory evidence increase confidence while remaining semantically separated.

---

## DEPDC5 / NPRL3 / SYNGAP1

These genes demonstrate similar semantic convergence patterns:

- direct disease evidence
- clinical testing prevalence
- exploratory support

Importantly, GSC preserves the distinction between:

```text
disease causality
≠
clinical utilization
≠
literature prevalence
```

rather than collapsing all evidence into naive overlap counts.

---

## POLG

`POLG` provides an important semantic contrast example.

POLG appears in:

- exploratory epilepsy literature
- epilepsy-related clinical utilization panels

However, it lacks direct statistical epilepsy burden evidence within the configured Epi25 release.

Therefore:

```text
direct_disease_score = 0.0
utilization_score    = 1.0
exploratory_score    = 0.75
semantic_consensus_score = 1.75
```

This demonstrates one of the primary goals of GSC:

```text
preventing exploratory or utilization evidence
from inflating direct disease association scores
```

---

# Semantic Interpretation

This example illustrates several core GSC principles:

| Principle | Demonstrated |
|---|---|
| semantic evidence separation | yes |
| ontology-aware aggregation | yes |
| inflation-aware scoring | yes |
| provenance preservation | yes |
| deterministic semantic ranking | yes |

---

# Key Observation

Naive overlap-based systems would treat all evidence sources equivalently.

GSC instead models:

- evidence meaning
- evidence context
- evidence semantics
- evidence role within biological interpretation

This allows semantically interpretable consensus ranking rather than simple source accumulation.