# Sys76 vs MARK Release Comparison

This document summarizes cross-system semantic reproducibility comparisons between Sys76 and MARK outputs.

Exact byte-identical hashes are not required because outputs contain run-specific fields such as `run_id`, `generated_at`, and provenance metadata. Primary criteria are row-count agreement, semantic score agreement for selected genes, preserved subtype anchors, and output contract compatibility.

## Summary

| Release | Sys76 rows | MARK rows | Row count match | Semantic spot checks match | Sys76 SHA256 | MARK SHA256 |
|---|---:|---:|---|---|---|---|
| `epilepsy_semantic_gtr_experimental` | 3543 | 3543 | True | True | `bdea2840eddf...` | `5f8806591382...` |
| `dee_semantic_gtr_experimental` | 3543 | 3543 | True | True | `839dec2393e2...` | `0514a5a85338...` |
| `nafe_semantic_gtr_experimental` | 3543 | 3543 | True | True | `732d3eb1c617...` | `0b4a408afd6b...` |
| `mitochondrial_semantic_gtr_experimental` | 3881 | 3881 | True | True | `73fc7a45ec59...` | `e08797e269de...` |

DEE and NAFE releases preserve subtype-specific semantic anchors while operating over the shared epilepsy-family candidate universe derived from integrated semantic evidence sources.

## Interpretation

The comparison focuses on semantic reproducibility rather than byte-identical output reproduction.

Semantic equivalence is evaluated on biologically meaningful score behavior rather than run-specific metadata identity.

Expected non-identical fields include:

- `run_id`
- `generated_at`
- provenance hashes when path or run metadata differs

Primary reproducibility criteria:

- matching consensus row counts
- preserved subtype-specific anchor genes
- matching semantic score behavior for selected genes
- successful output contract validation on each system

## Per-release comparison tables

| Release | Comparison artifact |
|---|---|
| `epilepsy_semantic_gtr_experimental` | `epilepsy_semantic_comparison.tsv` |
| `dee_semantic_gtr_experimental` | `dee_semantic_comparison.tsv` |
| `nafe_semantic_gtr_experimental` | `nafe_semantic_comparison.tsv` |
| `mitochondrial_semantic_gtr_experimental` | `mitochondrial_semantic_comparison.tsv` |

## Conclusion

These artifacts support the conclusion that GSC semantic release behavior is reproducible across Sys76 and MARK under the current validation criteria.

The comparison supports reproducible semantic behavior across independent infrastructure despite expected divergence in run-specific metadata and output checksums.