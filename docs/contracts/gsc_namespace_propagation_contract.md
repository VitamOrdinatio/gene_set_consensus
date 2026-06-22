# GSC Namespace Propagation Contract

## Purpose

This contract defines requirements for preservation of canonical gene namespace information throughout Gene Set Consensus (GSC) aggregation, scoring, consensus generation, and TEP construction.

This contract is distinct from the Source Namespace Attribution Contract.

Source Namespace Attribution governs preservation of source-origin identifiers and namespaces.

Namespace Propagation governs preservation of canonical identifiers and namespaces after normalization and aggregation.

---

# Motivation

GSC currently preserves canonical identifiers:

```text
gene_id
```

through aggregation and scoring.

However, namespace information associated with canonical identifiers is not consistently propagated beyond normalization.

As a result, downstream artifacts may preserve:

```text
ENSG00000100150
```

without preserving:

```text
ensembl_gene
```

This creates ambiguity for future interoperability with:

* VDB namespace brokerage
* RDGP consumption
* Future ontology integrations
* Additional identifier systems

including but not limited to:

* Ensembl Gene
* NCBI Gene
* HGNC
* OMIM
* Future identifier authorities

---

# Preservation Principle

Canonical namespace information SHALL be treated as part of canonical identity.

The following fields SHALL be considered inseparable:

```text
gene_id
gene_namespace
```

Preserving one without the other SHALL be considered incomplete preservation.

---

# Required Propagation Boundary

Canonical namespace information SHALL survive:

```text
Identifier Map
    ↓
Normalization
    ↓
Source Matrix Construction
    ↓
Frequency Aggregation
    ↓
Consensus Scoring
    ↓
Consensus Gene Set
    ↓
TEP Construction
```

without loss.

---

# Required Artifacts

The following artifacts SHALL preserve:

```text
gene_id
gene_namespace
```

## Required

### gene_source_matrix.tsv

### gene_frequency_table.tsv

### scored_gene_evidence.tsv

### consensus_gene_set.tsv

### GSC-TEP semantic priors

---

# Aggregation Rules

Aggregation SHALL NOT remove namespace information.

When records are grouped by canonical identifier:

```text
gene_id
```

the associated:

```text
gene_namespace
```

must remain attached.

Namespace preservation SHALL be deterministic.

---

# TEP Requirements

Every semantic prior SHALL preserve:

```yaml
identity:
  gene_id:
  gene_namespace:
```

Canonical namespace information SHALL be transported to VDB.

---

# Semantic Prior Identity

Semantic prior transport identities SHALL be namespace-aware.

Identifiers derived from:

```text
phenotype::gene_symbol
```

are insufficient.

Transport identity SHALL include canonical identifier information.

An acceptable example is:

```text
<release>::<phenotype>::<gene_namespace>::<gene_id>
```

or an equivalent deterministic construction.

Human-readable displays may continue to use:

```text
phenotype::gene_symbol
```

provided transport identity remains unique.

---

# Validation Requirements

Validation SHALL verify:

1. Namespace columns exist where required.
2. Namespace values are non-null when identifiers are present.
3. Semantic prior identifiers remain unique.
4. TEP construction preserves namespace information.

Failure of any requirement SHALL constitute contract failure.

---

# Success Criteria

Namespace information survives from normalization through TEP construction without collapse.

GSC canonical identity becomes:

```text
gene_id
+
gene_namespace
```

rather than:

```text
gene_id
```

alone.
