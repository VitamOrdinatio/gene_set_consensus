# GSC Gene Namespace Attribution Contract

## Purpose

This contract establishes producer-side requirements for gene identifier namespace attribution within Gene Set Consensus (GSC).

The objective is to ensure that identifier provenance is preserved from ingestion through TEP construction so that downstream consumers, including VDB, can reason about identifier origin, normalization history, and uncertainty without inference.

This contract governs namespace attribution preservation.

This contract does not govern namespace brokerage, namespace reconciliation, or cross-namespace identity resolution.

---

# Architectural Principle

Namespace attribution is a producer-side preservation responsibility.

Namespace resolution is a consumer-side brokerage responsibility.

GSC SHALL preserve identifier namespace information.

VDB MAY perform namespace brokerage and cross-namespace reasoning.

---

# Preservation Principle

Every gene identifier crossing a GSC operational boundary SHALL carry explicit namespace attribution or explicit unknown state.

Unknown attribution SHALL be represented as:

```text
unknown_namespace
```

Unknown attribution SHALL NOT be replaced by inferred attribution.

---

# Scope

This contract applies to:

* adapters
* normalization
* aggregation
* scoring
* output generation
* finalized-run artifacts
* GSC-TEP construction

This contract applies to both:

* source identifiers
* normalized identifiers

---

# Required Identity Elements

## Source Identity

Source-derived records SHALL preserve:

```text
source_gene_namespace
source_gene_id
source_gene_symbol
```

These values represent the identifier state supplied by the originating source.

---

## Canonical Identity

Normalized records SHALL preserve:

```text
gene_namespace
gene_id
gene_symbol
```

These values represent the identifier state used by GSC after normalization.

---

## Mapping State

Normalization SHALL preserve:

```text
mapping_status
```

Examples:

```text
resolved
unresolved
multi_mapped
partially_resolved
unknown
```

Additional mapping uncertainty MAY be preserved when available.

---

# Namespace Attribution Authority

Namespace attribution SHALL originate at the adapter layer whenever source authority exists.

Examples:

```text
Ensembl export
    → ensembl_gene

NCBI Gene export
    → ncbi_gene

HGNC export
    → hgnc_id

OMIM export
    → omim_gene
```

Adapters SHALL preserve declared namespace information supplied by source authorities.

---

# Prohibited Behaviors

The following are prohibited when source authority exists:

## Namespace Guessing

Examples:

```text
startswith("ENSG")
    → ensembl_gene

isdigit()
    → ncbi_gene
```

Such inference SHALL NOT replace source-declared namespace information.

---

## Silent Namespace Conversion

Adapters SHALL NOT discard source namespace attribution during normalization.

---

## Namespace Collapse

Distinct identifier namespaces SHALL NOT be collapsed into a shared namespace representation without explicit mapping metadata.

---

# Artifact Preservation Requirements

Namespace attribution SHALL be preserved within:

```text
normalized_source_records.tsv
source_contributions.tsv
gene_provenance.tsv
consensus_gene_set.tsv
```

and any future finalized-run artifacts containing identifier information.

---

# TEP Preservation Requirements

GSC-TEP SHALL preserve:

```text
source_gene_namespace
gene_namespace
mapping_status
```

when available from authoritative finalized-run artifacts.

TEP construction SHALL preserve namespace information.

TEP construction SHALL NOT invent namespace information.

---

# VDB Boundary

GSC SHALL provide namespace attribution.

VDB SHALL remain authoritative for:

* namespace brokerage
* cross-namespace reconciliation
* equivalence reasoning
* identifier federation

GSC SHALL NOT attempt to become a namespace brokerage system.

---

# Success Criteria

A future consumer SHALL be able to determine:

```text
what identifier was received
what namespace it belonged to
what normalization occurred
what uncertainty remains
```

without relying on string-pattern inference.

Namespace provenance SHALL remain traceable from ingestion through TEP construction.
