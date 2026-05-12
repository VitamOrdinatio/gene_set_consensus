# Sys76 vs MARK Comparison Artifacts

This directory contains cross-system semantic reproducibility comparison artifacts generated from independent GSC executions on:

- Sys76 Pop!_OS workstation
- MARK Linux HPC environment

The comparisons evaluate semantic reproducibility behavior rather than strict byte-identical output reproduction.

---

# Comparison Strategy

The comparison framework evaluates:

- consensus row-count agreement
- subtype anchor preservation
- semantic score equivalence for selected genes
- semantic channel preservation
- output contract compatibility

Expected non-identical fields include:

- `run_id`
- `generated_at`
- provenance metadata
- output checksums

These fields are runtime-specific and are not considered semantic reproducibility failures.

---

# Directory Structure

| Path | Purpose |
|---|---|
| `sys76_outputs/` | Curated Sys76 semantic release outputs |
| `mark_outputs/` | Curated MARK semantic release outputs |
| `comparison_summary.tsv` | Machine-readable aggregate comparison results |
| `comparison_summary.md` | Lightweight comparison artifact inventory |
| `sys76_vs_mark_release_comparison.md` | Human-readable scientific interpretation |
| `*_comparison.tsv` | Per-release semantic spot-check comparison tables |

---

# Semantic Releases Compared

The following releases were compared:

- epilepsy semantic
- DEE semantic
- NAFE semantic
- mitochondrial semantic

All releases demonstrated:

- matching row counts
- matching semantic spot-check behavior
- preserved subtype anchors

---

# Key Interpretation

The comparison artifacts support the conclusion that GSC semantic release behavior is reproducible across independent infrastructure under the current validation criteria.

See:

- `sys76_vs_mark_release_comparison.md`

for detailed interpretation.