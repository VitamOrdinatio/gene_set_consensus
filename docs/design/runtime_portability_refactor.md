# Runtime Portability Refactor

## Purpose

This document records the runtime portability refactor introduced during MARK reproducibility validation for GSC.

The refactor ensures that release-driven execution honors explicit phenotype configuration paths rather than reconstructing phenotype configuration paths from phenotype identifiers.

## Problem Discovered

During MARK validation, GSC release manifests correctly referenced MARK-local phenotype configuration files:

```text
config/local_mark/phenotypes/
```

However, `run_pipeline.py` propagated only the phenotype ID to downstream pipeline steps. The step scripts then reconstructed phenotype config paths using the default committed layout:

```text
config/phenotypes/{phenotype}.yaml
```

This caused MARK-local release execution to fail because MARK source files were staged under:

`/data/storage/gsc/`

while committed Sys76 configs referenced:

`/mnt/storage/`

## Previous Runtime Behavior

Before the refactor:

```text
release manifest
  → phenotype_config path
  → phenotype ID extracted
  → downstream steps receive phenotype ID only
  → downstream steps reconstruct config/phenotypes/{phenotype}.yaml
```

This made release execution partially environment-coupled.

## Corrected Runtime Behavior

After the refactor:

```text
release manifest
  → explicit phenotype_config path
  → run_pipeline.py propagates phenotype_config
  → downstream steps honor phenotype_config directly
  → phenotype identity and phenotype config location remain decoupled
```

## Files Modified

```text
src/gene_set_consensus/pipeline_runtime.py
run_pipeline.py
scripts/step_01_validate_inputs.py
scripts/step_02_normalize_genes.py
scripts/step_04_score_consensus.py
scripts/step_05_write_outputs.py
scripts/step_06_validate_outputs.py
```

## Design Principle

Phenotype identity and phenotype configuration location are distinct concepts.

A phenotype ID defines the biological/release identity:

```text
epilepsy_semantic_gtr_experimental
dee_semantic_gtr_experimental
nafe_semantic_gtr_experimental
mitochondrial_semantic_gtr_experimental
```

A phenotype config path defines where runtime source definitions are loaded from:

```text
config/phenotypes/
config/local_mark/phenotypes/
```

The runtime should preserve both.

## Why This Matters

This refactor enables:

- portable release execution
- local machine overlays
- HPC validation
- external storage remapping
- cleaner reproducibility protocols
- future deployment profiles without hardcoded path assumptions

## MARK Validation Outcome

After the refactor, MARK successfully executed all four semantic releases using these MARK-local overlays:

```text
config/local_mark/releases/
config/local_mark/phenotypes/
config/local_mark/manifests/
```

The following releases completed successfully:

```text
epilepsy_semantic_gtr_experimental_v0.1
dee_semantic_gtr_experimental_v0.1
nafe_semantic_gtr_experimental_v0.1
mitochondrial_semantic_gtr_experimental_v0.1
```

Each release passed output contract validation.

## Commit Provenance

The successful MARK execution used commit:

```text
416645a551b4a7ac9af1aa8229ec6d817869e932
```

## Conclusion

The runtime portability refactor converted GSC release execution from phenotype-ID-centered path reconstruction to explicit phenotype-config propagation.

This makes GSC more suitable for reproducible multi-environment execution.

---