# Config Directory

GSC uses two configuration layers.

## Phenotype configs

Location:

```text
config/phenotypes/
```

Phenotype configs are execution recipes. They define:

- phenotype ID
- source files
- adapters
- source weights
- scoring configuration

These are used directly by run_pipeline.py.

## Release configs

Location:
`config/releases/`

Release configs are reproducibility records. They define:

- named release ID
- phenotype config used
- source manifest used
- identifier map used
- source release metadata
- acquisition dates
- expected behavior for that release

Release configs do not replace phenotype configs. They wrap them with provenance and revision context.

## Rule configs

Location:
`config/rules/`

Rule configs define deterministic source-specific filtering or rollup behavior, such as Epi25 browser burden thresholds and phenotype rollups.

## Design Principle

Phenotype configs answer:

```text
How should GSC execute?
```

Release configs answer:

```text
What scientific snapshot did this execution represent?
```


## Registry-Hydrated Phenotype Configs

Newer phenotype configs may reference canonical source IDs instead of repeating full source metadata.

Example:

```yaml
sources:
  - source_id: epi25_2024_epi_high_confidence
    source_weight: 3.0

  - source_id: genes4epilepsy
    source_weight: 1.0
```

In this model:

- source identity, adapter, file path, provenance, and tier are hydrated from `manifests/sources/*.yaml`
- phenotype configs define source inclusion and weighting policy
- release configs define the versioned scientific snapshot

This reduces source metadata drift while preserving explicit weighting decisions.

## Configuration Hierarchy

`manifests/sources/*.yaml`
  canonical source registry

`config/phenotypes/*.yaml`
  phenotype composition and weighting

`config/releases/*.yaml`
  versioned scientific release record
  
