# GSC Identity Separation Model

## Purpose

This document defines the separation of identity classes within Gene Set Consensus (GSC).

The purpose of this model is to prevent accidental collapse of:

* biological phenotype identity
* package identity
* release identity

into a single field.

Identity collapse was discovered during initial GSC-TEP implementation, where a package identifier was propagated through the pipeline as though it were a biological phenotype.

This document establishes the authoritative identity boundaries that all future GSC producer outputs, release artifacts, and TEP projections must follow.

---

# Identity Classes

## Phenotype Identity

### Definition

Phenotype identity represents the biological condition, disease category, or biological scope under investigation.

Examples:

```text
epilepsy

developmental_epileptic_encephalopathy

non_acquired_focal_epilepsy

mitochondrial_disease
```

### Purpose

Phenotype identity answers:

```text
What biological domain
does this evidence concern?
```

### Authority

Phenotype identity is a scientific concept.

It is governed by:

* phenotype definitions
* disease definitions
* biological scope definitions

Phenotype identity is independent of:

* release version
* scoring profile
* execution mode
* output package structure

### Requirements

Phenotype identity:

```text
MUST be biologically meaningful

MUST NOT contain release version information

MUST NOT contain execution mode information

MUST NOT contain implementation details

MUST survive transport into TEP

MUST survive persistence into VDB
```

---

## Package Identity

### Definition

Package identity represents a producer-owned output package.

Examples:

```text
epilepsy_gold_bronze

epilepsy_semantic_gtr_experimental

mitochondrial_semantic_gtr_experimental
```

### Purpose

Package identity answers:

```text
Which producer package
generated these outputs?
```

### Authority

Package identity is governed by:

* producer implementation
* output organization
* scoring strategy
* source composition

Package identity is not a biological concept.

### Requirements

Package identity:

```text
MAY contain implementation descriptors

MAY contain execution mode descriptors

MAY contain scoring strategy descriptors

MUST NOT be interpreted as phenotype identity
```

---

## Release Identity

### Definition

Release identity represents an immutable scientific release.

Examples:

```text
epilepsy_semantic_gtr_experimental_v0.1

mitocarta_only_v0.1

epilepsy_gold_bronze_v0.1
```

### Purpose

Release identity answers:

```text
Which versioned scientific release
produced this evidence?
```

### Authority

Release identity is governed by:

* release configuration
* release governance
* scientific versioning policy

### Requirements

Release identity:

```text
MUST contain version information

MUST support historical reproducibility

MUST support future reinterpretability

MUST remain stable once released
```

---

# Identity Relationship Model

The three identities represent distinct concepts.

```text
Phenotype Identity
        ↓

Package Identity
        ↓

Release Identity
```

Example:

```text
Phenotype Identity

    epilepsy

Package Identity

    epilepsy_semantic_gtr_experimental

Release Identity

    epilepsy_semantic_gtr_experimental_v0.1
```

These values are related but not interchangeable.

---

# Artifact Placement Rules

## consensus_gene_set.tsv

Required fields:

```text
phenotype
```

Value:

```text
biological phenotype identity
```

Examples:

```text
epilepsy

mitochondrial_disease
```

Package identity must not be stored in the phenotype column.

---

## Output Directory Structure

Package identity governs output organization.

Example:

```text
results/tables/
    epilepsy_semantic_gtr_experimental/

results/reports/
    epilepsy_semantic_gtr_experimental/
```

Package identity may appear in directory paths.

---

## Release Configuration

Release identity governs release records.

Example:

```text
epilepsy_semantic_gtr_experimental_v0.1
```

Release identity may appear in:

```text
release manifests

release notes

release governance artifacts
```

---

# TEP Implications

GSC-TEP construction must preserve identity separation.

Required mappings:

```text
Phenotype Identity
    → payload phenotype context

Package Identity
    → source package identity

Release Identity
    → release provenance context
```

TEP construction must not reconstruct missing identities through inference.

Producer outputs must provide identity separation explicitly.

---

# VDB Implications

VDB persistence must preserve all three identity classes independently.

VDB must not collapse:

```text
phenotype identity

package identity

release identity
```

into a single persistence field.

Future analytical workflows may require independent querying of each identity space.

---

# Migration Strategy

Existing experimental releases that used package identity as phenotype identity should be treated as legacy artifacts.

Future releases should emit:

```text
phenotype identity

package identity

release identity
```

as independent concepts.

GSC-TEP generation should occur only after identity separation has been corrected in producer outputs.

---

# Success Criteria

Identity separation is considered successful when:

```text
Biological phenotype context remains recoverable.

Package organization remains recoverable.

Release provenance remains recoverable.
```

without ambiguity and without inference.

The same evidence record must be capable of answering:

```text
What biology?

What package?

What release?
```

through separate identity fields.
