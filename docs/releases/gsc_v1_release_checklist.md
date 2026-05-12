# GSC v1.0 Release Checklist

## Purpose

This document records the final validation and release criteria for the initial GSC v1.0 public release.

The checklist emphasizes:

- reproducibility
- semantic correctness
- release portability
- validation completeness
- documentation completeness
- cross-system execution integrity

---

# Repository Integrity

- [x] repository clean (`git status`)
- [x] no unintended generated runtime artifacts tracked
- [x] validation artifacts committed intentionally
- [x] no stale MARK-local overlay configs committed unintentionally
- [x] documentation links verified
- [x] relative markdown paths verified
- [x] example artifacts verified

---

# Python Validation

## Syntax Validation

```bash
python -m py_compile $(find src scripts tests -name "*.py" | tr '\n' ' ')
```

- [x] passed

---

## Test Suite

```bash
pytest
```

Expected:

```text
46 passed
```

- [x] passed

---

# Manifest Validation

## Release Validation

```bash
python scripts/validation/validate_release_manifest.py \
  --release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml \
  --skip-external-paths

python scripts/validation/validate_release_manifest.py \
  --release config/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml \
  --skip-external-paths
```

- [x] passed

---

## Scoring Profile Validation

```bash
python scripts/validation/validate_scoring_profile.py \
  --profile config/scoring_profiles/epilepsy_semantic_v0.1.yaml

python scripts/validation/validate_scoring_profile.py \
  --profile config/scoring_profiles/mitochondrial_semantic_v0.1.yaml
```

- [x] passed

---

## Source Manifest Validation

```bash
python scripts/validation/validate_source_manifest.py \
  --manifest manifests/sources/epilepsy_manifest.yaml

python scripts/validation/validate_source_manifest.py \
  --manifest manifests/sources/mitochondrial_manifest.yaml
```

Expected:

```text
epilepsy sources=6
mitochondrial sources=4
```

- [x] passed

---

# Cross-System Validation

## MARK Reproducibility Validation

Validated:

- [x] fresh repository reconstruction
- [x] isolated virtual environment bootstrap
- [x] external storage remapping
- [x] MARK-local overlay generation
- [x] Epi25 subtype reconstruction
- [x] GTR XML parsing
- [x] release-driven execution
- [x] output contract validation
- [x] semantic reproducibility verification

---

## Semantic Releases Validated

Validated successfully on both Sys76 and MARK:

- [x] epilepsy semantic release
- [x] DEE semantic release
- [x] NAFE semantic release
- [x] mitochondrial semantic release

---

# Documentation Validation

## Core Documentation

- [x] root README
- [x] architecture overview
- [x] runtime portability refactor
- [x] DEE semantic walkthrough
- [x] validation README
- [x] comparison README

---

## Validation Documentation

- [x] reproducibility protocol
- [x] execution summary
- [x] probe inventory
- [x] comparison artifacts
- [x] semantic reproducibility interpretation

---

# Comparison Validation

## Sys76 vs MARK Comparisons

Validated:

- [x] row-count agreement
- [x] subtype anchor preservation
- [x] semantic score equivalence
- [x] semantic channel preservation
- [x] output contract compatibility

Expected behavior:

- byte-identical output hashes are NOT required
- semantic reproducibility IS required

---

# Release Artifacts

## Curated Artifacts

- [x] comparison artifacts committed
- [x] validation artifacts committed
- [x] example walkthroughs committed
- [x] architecture documentation committed
- [x] Sys76 vs MARK comparison artifacts verified

---

# GitHub Release Preparation

## Release Metadata

- [x] release tag prepared
- [x] release notes drafted
- [x] validation summary included
- [x] reproducibility claims verified

---

# Final Release Actions

## Final Validation

```bash
pytest
make validate-all
```

- [x] final validation passed immediately before tagging

---

## Git Tag

Example:

```bash
git tag -a v1.0.0 -m "GSC v1.0.0"
git push origin v1.0.0
```

- [x] tag pushed

---

# v1.0 Release Definition

GSC v1.0 represents the first stable public release demonstrating:

- release-driven semantic execution
- subtype-aware semantic overlays
- provenance-aware semantic scoring
- reproducible semantic candidate universes
- cross-system semantic reproducibility
- portable runtime execution
- validation-backed semantic interpretation
- independent infrastructure reproducibility validation