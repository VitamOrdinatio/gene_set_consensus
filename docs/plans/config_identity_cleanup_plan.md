# Config Identity Cleanup Plan

## Purpose

This plan defines a small, controlled cleanup of the GSC `config/` directory following the phenotype/package/release identity separation repair.

The goal is to stabilize GSC as a producer so that future GSC outputs and GSC-TEPs are transparent, reproducible, and free from ambiguous configuration behavior.

This is a cleanup plan, not a redesign of GSC.

---

# Background

GSC previously allowed several configuration concepts to drift together:

```text
phenotype identity
package identity
release identity
example/demo configuration
legacy configuration
```

The producer-side identity bug has now been corrected for the active epilepsy semantic release.

However, the repository still contains historical, example, and legacy configuration files that may be referenced by:

```text
tests
Makefile targets
validation scripts
documentation
archive plans
```

These references must be resolved intentionally before configs are moved, deleted, or treated as inactive.

---

# Cleanup Objectives

This cleanup should ensure that:

```text
active configs remain active

legacy configs are clearly marked legacy

tests reference valid configs

Makefile targets reference valid configs

release workflows remain operational

GSC-TEP source packages are unambiguous
```

No configuration file should be moved to `legacy/` unless all active references have been updated, removed, or explicitly archived.

---

# Identity Rules

GSC configuration must preserve three distinct identity classes.

## Phenotype Identity

Represents biological scope.

Examples:

```text
epilepsy
mitochondrial_disease
developmental_epileptic_encephalopathy
non_acquired_focal_epilepsy
```

Phenotype identity belongs in:

```text
phenotype.phenotype_id
```

---

## Package Identity

Represents producer output namespace.

Examples:

```text
epilepsy_semantic_gtr_experimental
mitochondrial_semantic_gtr_experimental
```

Package identity belongs in:

```text
package.package_id
```

Package identity governs:

```text
results/tables/<package_id>
results/reports/<package_id>
results/teps/gsc/<package_id>
```

---

## Release Identity

Represents a versioned scientific release.

Examples:

```text
epilepsy_semantic_gtr_experimental_v0.1
mitochondrial_semantic_gtr_experimental_v0.1
```

Release identity belongs in:

```text
config/releases/*.yaml
```

---

# Active Configuration Set

The following phenotype configurations are the authoritative
active producer configurations for GSC.

```text
config/phenotypes/
├── dee_semantic_gtr_experimental.yaml
├── epilepsy_semantic_gtr_experimental.yaml
├── mitochondrial_semantic_gtr_experimental.yaml
└── nafe_semantic_gtr_experimental.yaml
```

The following release configurations are the authoritative
active release configurations for GSC.

```text
config/releases/
├── dee_semantic_gtr_experimental_v0.1.yaml
├── epilepsy_semantic_gtr_experimental_v0.1.yaml
├── mitochondrial_semantic_gtr_experimental_v0.1.yaml
└── nafe_semantic_gtr_experimental_v0.1.yaml
```

Any configuration outside the active configuration set
must be explicitly classified as one of:

- active
- legacy
- archive
- example fixture

No configuration should exist in an ambiguous state.

The active configuration set serves as the authoritative
source for GSC-TEP generation.

All producer-side GSC-TEPs must originate from one of the
active release configurations listed above.

---

# Legacy Candidate Inventory

Legacy phenotype configs may include:

```text
config/phenotypes/example_phenotype.yaml
config/phenotypes/epilepsy_template.yaml
config/phenotypes/epilepsy_gold_bronze.yaml
config/phenotypes/epilepsy_gold_bronze_registry.yaml
config/phenotypes/epilepsy_gold_bronze_registry_minimal.yaml
config/phenotypes/mitocarta_only.yaml
```

Legacy release configs may include:

```text
config/releases/epilepsy_gold_bronze_v0.1.yaml
config/releases/mitocarta_only_v0.1.yaml
```

These should not be moved or deleted until all references are audited.

---

# Reference Audit Targets

Before committing any legacy movement, audit references in:

```text
Makefile
README.md
CHANGELOG.md
.github/workflows/
scripts/
tests/
docs/
config/README.md
```

Recommended commands:

```bash
git grep -n "example_phenotype"

git grep -n "epilepsy_gold_bronze"

git grep -n "mitocarta_only"

git grep -n "config/phenotypes/"

git grep -n "config/releases/"
```

---

# Test and Tooling Updates

The cleanup must resolve known active references to legacy configs.

Known candidates include:

```text
Makefile
tests/integration/test_example_pipeline.py
tests/unit/test_release_runtime.py
scripts/validation/validate_reproducibility.py
```

For each reference, decide whether to:

```text
update to an active semantic release

move into archive documentation

retain a minimal canonical example config

remove obsolete coverage
```

---

# Canonical Example Decision

A decision is required:

## Option A

Retain a canonical example config.

Example:

```text
config/phenotypes/example_phenotype.yaml
```

Pros:

```text
small test fixture
fast integration testing
easy developer onboarding
```

Cons:

```text
must be updated to new identity schema
can drift from real producer releases
```

## Option B

Retire example config usage.

Use active release configs for tests.

Pros:

```text
tests exercise real producer behavior
less drift from production GSC
```

Cons:

```text
tests may be heavier
external source dependencies may complicate CI
```

Recommended near-term decision:

```text
Retain a minimal canonical example config only if it can be made fully compliant with the identity separation contract.
```

Otherwise, tests should move to active semantic releases.

---

# Cleanup Sequence

## Step 1

Restore or preserve any config still referenced by active tests or Makefile targets.

Do not commit broken references.

---

## Step 2

Update legacy candidate configs to either:

```text
identity-contract compliant active configs
```

or:

```text
legacy archived configs
```

---

## Step 3

Update tests and tooling.

Priority targets:

```text
tests/integration/test_example_pipeline.py
tests/unit/test_release_runtime.py
scripts/validation/validate_reproducibility.py
Makefile
```

---

## Step 4

Run reference audit again.

Required command set:

```bash
git grep -n "example_phenotype"
git grep -n "epilepsy_gold_bronze"
git grep -n "mitocarta_only"
git grep -n "config/phenotypes/"
git grep -n "config/releases/"
```

Any remaining hit must be intentionally classified as:

```text
active
legacy documentation
archive documentation
```

---

## Step 5

Run validation.

Minimum checks:

```bash
pytest

python scripts/validation/validate_release_manifest.py \
  --release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml \
  --skip-external-paths

python run_pipeline.py \
  --release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml
```

---

## Step 6

Commit config cleanup separately.

Commit subject:

```text
Clean up GSC configuration identity references
```

Commit body should describe:

```text
active configs retained
legacy configs archived
tests updated
Makefile targets updated
identity schema compliance preserved
```

---

# Acceptance Criteria

The cleanup is complete when:

```text
active semantic releases execute successfully

tests pass

Makefile targets point to valid configs

CI release validation remains valid

legacy configs are not referenced by active code paths

all active phenotype configs contain phenotype.phenotype_id and package.package_id

all active release configs point to valid phenotype configs
```

---

# Non-Goals

This cleanup does not solve:

```text
run-scoped output retention

release-scoped output immutability

TEP validation expansion

VDB ingestion behavior
```

Those should be handled after GSC producer configuration is stable.

---

# Summary

This cleanup stabilizes the configuration layer so GSC can serve as a clean producer for GSC-TEP construction.

The immediate goal is not to remove all historical material.

The immediate goal is to ensure that every active configuration reference is intentional, valid, and identity-contract compliant.
