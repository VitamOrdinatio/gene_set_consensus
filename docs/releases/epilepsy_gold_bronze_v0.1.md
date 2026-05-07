# Release Notes: epilepsy_gold_bronze_v0.1

## Purpose

This release defines a development-stage epilepsy GSC output combining:

- gold-tier Epi25 2024 high-confidence epilepsy evidence
- bronze-tier Genes4Epilepsy literature-derived evidence

## Scientific Interpretation

This release is a versioned scientific interpretation, not permanent biological truth.

The output reflects:
- source files staged as of 2026-05-06
- Epi25 2024 browser and publication-derived evidence processing
- Genes4Epilepsy v1 source staging
- pinned MyGene-derived identifier map
- GSC v0.1 scoring model

## Evidence Tiers

| Source | Tier | Weight |
|---|---:|---:|
| Epi25 2024 EPI high-confidence genes | gold | 3.0 |
| Genes4Epilepsy | bronze | 1.0 |

## Expected Behavior

Genes present in both Epi25 and Genes4Epilepsy receive:

```text
source_count = 2
weighted_source_sum = 4.0
consensus_score = 4.0
```

This is an expected behavior for this release snapshot only.

## Revision Policy

Future epilepsy releases may differ if:

- Epi25 updates its browser or publications
- Genes4Epilepsy is superseded
- identifier mappings change
- phenotype rollup rules change
- scoring weights change

Historical releases should remain reproducible through release manifests and Git history.