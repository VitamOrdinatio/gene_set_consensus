# Release Notes: mitocarta_only_v0.1

## Purpose

This release defines a development-stage MitoCarta-only GSC output using:

- MitoCarta3.0 human mitochondrial gene inventory
- GSC `mitocarta` adapter
- source-preserving TSV extracted from the original Excel workbook

## Scientific Interpretation

This release is a versioned scientific interpretation, not permanent biological truth.

The output reflects:
- MitoCarta3.0 source file staged as of 2026-05-06
- `human_mitocarta` worksheet exported to TSV without manual column renaming
- native MitoCarta Ensembl identifier field
- GSC v0.1 scoring model

## Evidence Tier

| Source | Tier | Weight |
|---|---:|---:|
| MitoCarta3.0 Human | gold | 3.0 |

## Expected Behavior

Because this is a single-source release, all included genes receive:

```text
source_count = 1
weighted_source_sum = 3.0
consensus_score = 3.0
```

Expected gene count for this staged source snapshot:
`1136 genes`

## Revision Policy

Future MitoCarta releases may differ if:

- MitoCarta releases version 4.0 or later
- mitochondrial localization evidence is revised
- Ensembl mappings change
- source columns change
- GSC adapter behavior changes

Historical releases should remain reproducible through release manifests, source checksums, and Git history.
