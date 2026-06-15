# GSC-TEP Identity Model

## Draft Status

Draft v0.1 for DEX-GSC implementation planning.

---

# Purpose

This document defines the identity model governing GSC-TEP construction, transport, validation, and downstream persistence.

The purpose of this document is to ensure that:

```text
identity survives transport
identity survives persistence
identity survives reinterpretation
```

without ambiguity or loss of scientific meaning.

This document serves as the authoritative identity reference for:

* GSC-TEP construction
* GSC-TEP validation
* GSC-TEP acceptance criteria
* VDB intake planning
* RDGP interoperability planning

---

# Core Identity Principle

Identity classes represent distinct concepts.

Identity classes must not be collapsed.

A valid GSC-TEP preserves multiple simultaneous identity spaces.

These identity spaces are complementary.

They are not interchangeable.

---

# Identity Hierarchy

The GSC-TEP identity hierarchy is:

```text
Biological Identity
        ↓

Release Identity
        ↓

Semantic Prior Identity
        ↓

Transport Identity
        ↓

Brokered Identity
        ↓

Persistence Identity
```

Each layer serves a distinct purpose.

---

# Biological Identity

## Definition

Biological identity represents the core scientific statement emitted by GSC.

The primary biological identity is:

```text
(phenotype, gene)
```

Examples:

```text
(epilepsy, SCN1A)

(epilepsy, DEPDC5)

(mitochondrial_disease, POLG)
```

These represent distinct biological assertions.

---

## Preservation Requirement

Biological identity must remain recoverable.

Biological identity must never be replaced by:

```text
transport identifiers
release identifiers
canonical identifiers
database identifiers
```

---

# Release Identity

## Definition

Release identity identifies the GSC release responsible for producing a semantic prior.

Examples:

```text
epilepsy_gold_bronze_v1.0

mitocarta_only_v0.1

future_release_x
```

Release identity provides:

```text
historical reproducibility
scientific context
evidence state reconstruction
```

---

## Canonical Representation

```text
gsc_release_id
```

Examples:

```text
gsc_release_id =
epilepsy_gold_bronze_v1.0
```

---

## Preservation Requirement

Release identity is part of semantic prior identity.

Release identity must never be treated as optional metadata.

---

# Semantic Prior Identity

## Definition

Semantic prior identity represents the complete GSC semantic evidence statement.

Canonical form:

```text
(gsc_release_id,
 phenotype,
 gene)
```

Example:

```text
(epilepsy_gold_bronze_v1.0,
 epilepsy,
 SCN1A)
```

This identity uniquely identifies:

```text
one release-scoped
phenotype-scoped
gene-associated
semantic prior
```

---

## Importance

This is the most important scientific identity preserved by GSC-TEP.

Most validation requirements ultimately evaluate preservation of this identity.

---

# Source Identity

## Definition

Source identity represents the producer-owned identifiers emitted by GSC.

Examples:

```text
source_gene_symbol

source_gene_id

source_namespace
```

Examples:

```text
POLG

ENSG00000140521

HGNC:9175
```

depending upon producer outputs.

---

## Preservation Requirement

Source identity must remain recoverable after:

```text
TEP construction

VDB intake

namespace brokerage

future reinterpretation
```

Source identity must never be destroyed.

---

# Phenotype Identity

## Definition

Phenotype identity represents the biological context in which a semantic prior is meaningful.

Examples:

```text
epilepsy

developmental_epileptic_encephalopathy

mitochondrial_disease
```

---

## Preservation Requirement

Phenotype identity must remain attached to semantic prior identity.

The following collapse is forbidden:

```text
(epilepsy, SCN1A)

↓

SCN1A
```

Loss of phenotype identity constitutes preservation failure.

---

# Transport Identity

## Definition

Transport identity identifies the TEP object.

Canonical form:

```text
tep_id
```

Examples:

```text
TEP-000001

TEP-000002
```

implementation-specific.

---

## Purpose

Transport identity exists to support:

```text
transport governance
validation
traceability
artifact management
```

Transport identity does not represent biological identity.

---

## Preservation Requirement

Transport identity must coexist with biological identity.

Transport identity must not replace biological identity.

---

# Sleeve Identity

## Definition

Sleeve identity identifies the producer-owned semantic projection used to create the TEP payload.

Canonical fields:

```text
tep_sleeve_version

sleeve_family

projection_version
```

---

## Purpose

Sleeve identity allows future consumers to determine:

```text
which producer projection generated the payload
```

---

# Producer Package Identity

## Definition

Producer package identity identifies the producer release package that generated transported evidence.

For GSC:

```text
source_package_id
=
gsc_release_id
```

---

## Preservation Requirement

Producer package identity must remain recoverable after transport.

---

# Provenance Identity

## Definition

Provenance identity identifies lineage relationships.

Examples:

```text
provenance_id

aggregation_event_id

manifest_id

artifact_id
```

---

## Purpose

Supports:

```text
auditability
traceability
lineage reconstruction
```

---

# Manifest Identity

## Definition

Every source artifact referenced by a GSC-TEP should possess a stable identity.

Examples:

```text
artifact_id

artifact_checksum

artifact_reference
```

---

## Purpose

Allows reconstruction of:

```text
which source artifacts
supported which semantic priors
```

---

# Namespace Brokerage Identity

## Definition

Namespace brokerage identities are generated downstream by VDB.

Examples:

```text
canonical_gene_id

canonical_phenotype_id

resolution_event_id
```

---

## Purpose

Supports:

```text
identity reconciliation

cross-repository interoperability

query federation
```

---

## Preservation Requirement

Namespace brokerage identities are additive.

They must not replace source identity.

---

# Identity Coexistence Principle

The following identities may simultaneously exist:

```text
source_gene_symbol

source_gene_id

canonical_gene_id

gsc_release_id

phenotype

tep_id

artifact_id

provenance_id
```

This is expected.

Identity multiplicity is not an error condition.

---

# Identity Preservation Guarantees

A valid GSC-TEP must preserve:

## Biological Identity

```text
(phenotype, gene)
```

---

## Release Identity

```text
gsc_release_id
```

---

## Semantic Prior Identity

```text
(gsc_release_id,
 phenotype,
 gene)
```

---

## Source Identity

```text
source_gene_symbol
source_gene_id
source_namespace
```

---

## Transport Identity

```text
tep_id
```

---

## Provenance Identity

```text
provenance_id
artifact_id
manifest_id
```

---

## Brokered Identity

```text
canonical_gene_id
resolution_event_id
```

when generated.

---

# Identity Failure Modes

The following constitute identity preservation failures.

---

## Failure Mode 1

Biological identity collapse.

Example:

```text
(epilepsy, SCN1A)

↓

SCN1A
```

---

## Failure Mode 2

Release identity loss.

Example:

```text
semantic prior survives

release disappears
```

---

## Failure Mode 3

Source identity destruction.

Example:

```text
source_gene_symbol removed

canonical_gene_id only
```

---

## Failure Mode 4

Transport identity substitution.

Example:

```text
tep_id

used as biological identity
```

---

## Failure Mode 5

Namespace overwrite.

Example:

```text
canonical_gene_id

replaces source identity
```

rather than augmenting it.

---

# Validation Expectations

Identity validation should demonstrate:

```text
biological identity recoverable

release identity recoverable

semantic prior identity recoverable

source identity recoverable

transport identity recoverable

brokered identity additive

phenotype scope preserved
```

Validation requirements are defined separately in:

```text
docs/validation/gsc_tep_validation_strategy.md
```

---

# Relationship to VDB

GSC-TEP transports producer-owned identities.

VDB brokers identities.

VDB does not redefine producer identity.

Identity authority remains distributed:

```text
GSC
→ source semantic prior identity

TEP
→ transport identity

VDB
→ brokered canonical identity
```

---

# Relationship to RDGP

RDGP consumes:

```text
(sample, gene)
```

reasoning entities.

GSC emits:

```text
(phenotype, gene)
```

semantic prior entities.

These identity spaces remain distinct.

RDGP may attach GSC priors.

RDGP must not collapse the identity models.

---

# Summary

The purpose of GSC-TEP identity preservation is to ensure that future consumers can determine:

```text
what biological statement existed

which release generated it

which producer identities supported it

which transport object carried it

which provenance artifacts justified it

which brokered identities were later assigned
```

without requiring access to the original GSC execution environment.

Identity is therefore treated as a first-class preservation target rather than a secondary implementation detail.
