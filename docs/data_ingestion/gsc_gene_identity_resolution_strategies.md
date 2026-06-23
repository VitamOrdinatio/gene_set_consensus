# GSC Gene Identity Resolution Strategies

## Purpose

This document records an important architectural observation discovered during namespace propagation hardening and GSC-TEP certification review.

GSC currently supports two distinct but valid gene-identity resolution paradigms during source ingestion:

```text
1. Identifier-Map Resolution

2. Adapter-Resolved Identity
```

Both paradigms are scientifically defensible.

Both currently exist in production GSC workflows.

This document explains the differences, rationale, advantages, limitations, and future governance considerations.

---

# Executive Summary

During namespace propagation hardening, inspection of epilepsy and mitochondrial pipelines revealed that the two releases arrive at canonical gene identities using different ingestion strategies.

Epilepsy primarily relies on:

```text
symbol
  ↓
identifier map
  ↓
canonical identity
```

while mitochondrial sources primarily rely on:

```text
source payload
  ↓
canonical identity
  ↓
namespace
```

Both approaches ultimately generate valid canonical GSC identities.

The distinction occurs during ingestion and normalization.

---

# Strategy 1: Identifier-Map Resolution

## Concept

Identifier-map resolution begins with a source-provided symbol and resolves that symbol into canonical identifiers using a curated identifier map.

Workflow:

```text
source gene symbol
        ↓
identifier map lookup
        ↓
canonical identifier
        ↓
canonical namespace
```

Example:

```text
DEPDC5
    ↓
epilepsy_identifier_map.tsv
    ↓
ENSG00000100150
    ↓
ensembl_gene
```

---

## Current GSC Usage

This strategy is heavily used by epilepsy sources such as:

```text
EPI25
Genes4Epilepsy
```

These sources frequently arrive as:

```text
gene symbol
```

or

```text
symbol-centric evidence tables
```

rather than fully specified canonical identifiers.

The identifier map provides:

```text
symbol
Ensembl ID
Entrez ID
HGNC ID
namespace
```

resolution.

---

## Advantages

### Centralized Resolution

A single mapping layer can normalize multiple heterogeneous sources.

### Cross-Source Harmonization

Different source formats can converge onto the same canonical identifiers.

### Explicit Governance

Identifier mappings are inspectable and versionable artifacts.

---

## Limitations

### Additional Infrastructure

Requires construction and maintenance of identifier maps.

### Potential Drift

Identifier maps must be regenerated when source collections evolve.

### Additional Resolution Layer

Introduces an extra dependency between ingestion and canonical identity assignment.

---

# Strategy 2: Adapter-Resolved Identity

## Concept

Adapter-resolved identity begins with source records that already contain authoritative identifiers.

Workflow:

```text
source payload
        ↓
adapter extraction
        ↓
canonical identifier
        ↓
canonical namespace
```

No identifier-map lookup is required.

---

## Current GSC Usage

This strategy is heavily used by mitochondrial sources.

Examples include:

### MitoCarta

MitoCarta records provide:

```text
HumanGeneID
Ensembl Gene ID
Gene Symbol
```

directly.

The adapter emits:

```text
source_gene_id
source_gene_namespace
```

during ingestion.

### GTR Mitochondrial

The GTR parser extracts:

```text
NCBI Gene ID
Gene Symbol
```

directly from XML-derived evidence.

The adapter therefore emits canonical identifiers without consulting an identifier map.

---

## Advantages

### Fewer Transformation Steps

Canonical identity is established immediately.

### Reduced Resolution Drift

No intermediate symbol-resolution layer exists.

### Strong Provenance

Canonical identifiers remain directly linked to source records.

### Simpler Execution

Normalization becomes primarily a validation step rather than a resolution step.

---

## Limitations

### Source Dependency

Requires authoritative identifiers to be present in source data.

### Adapter Complexity

Adapters become responsible for identity extraction and validation.

### Less Centralized Resolution

Normalization logic is distributed across adapters rather than concentrated in a single identifier map.

---

# Comparison

| Property                              | Identifier Map  | Adapter Resolved |
| ------------------------------------- | --------------- | ---------------- |
| Requires symbol lookup                | Yes             | No               |
| Requires identifier map artifact      | Yes             | No               |
| Canonical ID supplied by source       | Not necessarily | Yes              |
| Adapter complexity                    | Lower           | Higher           |
| Normalization complexity              | Higher          | Lower            |
| Resolution transparency               | Centralized     | Distributed      |
| Suitable for symbol-only datasets     | Excellent       | Poor             |
| Suitable for rich identifier datasets | Acceptable      | Excellent        |

---

# Namespace Propagation Hardening Findings

During GSC namespace propagation hardening, inspection revealed:

```text
Epilepsy:
primarily identifier-map driven

Mitochondrial:
primarily adapter-resolved
```

This explains why rebuilding:

epilepsy_identifier_map.tsv

was required during namespace propagation work, while mitochondrial releases continued to emit correct namespace-aware identities without rebuilding a dedicated mitochondrial identifier map.

The mitochondrial pipeline was already receiving canonical identifiers directly from source adapters.

---

# Governance Implications

The existence of two resolution paradigms is not inherently a defect.

Instead, it reflects the reality that source ecosystems differ substantially.

Examples:

```text
EPI25
  -> Ensembl-centric burden outputs

Genes4Epilepsy
  -> NCBI Gene identifiers

MitoCarta
  -> HumanGeneID + Ensembl identifiers

GTR
  -> NCBI Gene identifiers
```

Some sources naturally arrive with rich identifier metadata.

Others require external normalization infrastructure.

---

# Future Direction

A future architectural question remains open:

Should GSC converge toward:

```text
all sources emit canonical identities from adapters
```

or continue supporting:

```text
identifier-map resolution
adapter-resolved identity
```

as parallel ingestion strategies?

No decision has been made.

Current GSC supports both paradigms successfully.

Future decisions should prioritize:

```text
provenance
inspectability
determinism
reproducibility
scientific auditability
```

over architectural uniformity alone.

---

# Key Principle

Canonical identity preservation is more important than the mechanism used to obtain canonical identity.

Whether identity originates from:

```text
identifier map resolution
```

or:

```text
adapter-resolved extraction
```

the resulting GSC artifacts must preserve:

```text
gene_id
gene_namespace
source_gene_id
source_gene_namespace
mapping_status
```

through all downstream stages, including:

```text
consensus outputs
provenance outputs
source contribution topology
GSC-TEP transport artifacts
```

This preservation requirement is mandatory regardless of ingestion strategy.
