# DEE Semantic Output Example

This example demonstrates subtype-specific semantic ranking for developmental and epileptic encephalopathy (DEE).

Example table:

```text
docs/examples/tables/dee_semantic_selected_genes.tsv
```

The DEE semantic release uses `epi25_2024_dee_high_confidence` as the platinum direct-disease anchor while preserving supporting evidence from Genes4Epilepsy and GTR epilepsy clinical utilization.

Expected high-confidence DEE genes:

```text
NEXMIF, SCN1A, SYNGAP1, STX1B, WDR45
```

These genes demonstrate semantic convergence across:

- direct disease association
- exploratory literature support
- clinical utilization

The release preserves DEE-specific evidence rather than collapsing all epilepsy evidence into a single undifferentiated gene list.

---