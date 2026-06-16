# GSC Identity Separation Contract

## Purpose

This contract defines the mandatory identity separation requirements for Gene Set Consensus (GSC).

The purpose of this contract is to eliminate identity collapse between:

* phenotype identity
* package identity
* release identity

and establish deterministic producer behavior for all future GSC outputs.

This contract is authoritative for:

```text
GSC producer outputs

GSC release artifacts

GSC-TEP construction

VDB interoperability
```

---

# Background

During initial GSC-TEP implementation, inspection of real producer outputs revealed that package identity had been propagated through the pipeline using the phenotype field.

Example:

```text
phenotype

=
epilepsy_semantic_gtr_experimental
```

This value is not a biological phenotype.

It is a package identifier.

This behavior violates the identity separation principles defined by the GSC identity model.

This contract establishes the corrective requirements.

---

# Identity Classes

The following identities are independent and must remain independent.

## Phenotype Identity

Represents:

```text
Biological scope
```

Examples:

```text
epilepsy

developmental_epileptic_encephalopathy

non_acquired_focal_epilepsy

mitochondrial_disease
```

Phenotype identity answers:

```text
What biology?
```

---

## Package Identity

Represents:

```text
Producer output package
```

Examples:

```text
epilepsy_semantic_gtr_experimental

epilepsy_gold_bronze

mitochondrial_semantic_gtr_experimental
```

Package identity answers:

```text
What package?
```

---

## Release Identity

Represents:

```text
Immutable scientific release
```

Examples:

```text
epilepsy_semantic_gtr_experimental_v0.1

mitocarta_only_v0.1
```

Release identity answers:

```text
What release?
```

---

# Producer Requirements

## Requirement 01

Phenotype identity must represent biological phenotype only.

Producer outputs must not emit:

```text
package identity

release identity

execution mode
```

inside phenotype fields.

---

## Requirement 02

Package identity must be represented independently.

Package identity may contain:

```text
execution mode

scoring mode

implementation descriptors
```

Package identity must not be interpreted as phenotype identity.

---

## Requirement 03

Release identity must be represented independently.

Release identity must support:

```text
historical reproducibility

release provenance

future reinterpretability
```

---

# Output Artifact Requirements

## consensus_gene_set.tsv

Required:

```text
phenotype
```

Value:

```text
biological phenotype identity
```

Example:

```text
epilepsy
```

Forbidden:

```text
epilepsy_semantic_gtr_experimental
```

---

## gene_frequency_table.tsv

Required:

```text
phenotype
```

Value:

```text
biological phenotype identity
```

---

## gene_source_matrix.tsv

Required:

```text
phenotype
```

Value:

```text
biological phenotype identity
```

---

## scored_gene_evidence.tsv

Required:

```text
phenotype
```

Value:

```text
biological phenotype identity
```

---

# Directory Structure Requirements

Directory structures remain package-scoped.

Example:

```text
results/tables/
    epilepsy_semantic_gtr_experimental/

results/reports/
    epilepsy_semantic_gtr_experimental/
```

Directory names are package identity.

Directory names are not phenotype identity.

---

# GSC-TEP Requirements

GSC-TEP generation must inherit corrected identities from producer outputs.

Transport logic must not reconstruct phenotype identity through inference.

Transport logic must not derive package identity from phenotype identity.

Transport logic must preserve all identity classes independently.

---

# VDB Interoperability Requirements

The following identities must remain independently queryable:

```text
phenotype identity

package identity

release identity
```

VDB consumers must not be required to infer one identity from another.

---

# Migration Requirements

Existing historical artifacts may contain collapsed identities.

These artifacts are considered:

```text
legacy experimental outputs
```

and do not define future producer behavior.

Future releases must satisfy this contract.

---

# Validation Requirements

Identity separation is considered valid only if the following questions can be answered independently:

```text
What biology?

What package?

What release?
```

without inference and without ambiguity.

---

# Acceptance Criteria

The contract is satisfied when:

```text
phenotype fields contain biological phenotype identity

package identifiers remain package identifiers

release identifiers remain release identifiers

no producer artifact collapses these concepts
```

and

```text
GSC-TEP construction requires no identity repair logic.
```

The producer must emit correct identities directly.
