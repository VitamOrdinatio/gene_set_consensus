# GSC Methodology

## Objective

Build deterministic, phenotype-scoped consensus gene evidence from multiple heterogeneous sources.


---

## Input Model

Each source contributes a list of genes associated with a phenotype.

Sources may represent:

- curated databases
- clinical panels
- literature-derived lists
- user-curated lists

Each source receives an explicit weight.


---

## Identifier Normalization

GSC preserves the original source gene label, then attempts to map it to a normalized gene symbol and stable gene identifier.

Mapping statuses include:

- `resolved`
- `deprecated_symbol_resolved`
- `ambiguous`
- `unresolved`
- `symbol_only`

Unresolved and ambiguous mappings are preserved and reported.

They are not silently discarded.

This prevents one source from artificially inflating support through repeated rows.


---

## Duplicate Handling

Duplicates within one source are collapsed.

This prevents one source from inflating a gene score by listing the same gene multiple times.

Duplicates across different sources are preserved as independent support.


---

## Aggregation

GSC builds a gene-source matrix.

Each source contributes either:

- 1 = source supports gene
- 0 = source does not list gene

Absence from a source is not interpreted as negative evidence.


---

## Scoring

The v1 consensus score is:

```text
consensus_score = weighted_source_sum
```

where:

```text
weighted_source_sum = sum(source_weight for each source supporting the gene)
```

The raw `source_count` is preserved separately.


Future scoring models may incorporate:
- ontology-aware weighting
- publication confidence
- functional evidence
- transcriptomic support
- probabilistic calibration


---

## Provenance

Every final consensus record can be traced back to source-level evidence rows.

This is required for:

- auditability
- debugging
- reproducibility
- downstream interpretation


---

## Validation

GSC validates:

- input source paths
- source columns
- source weights
- output schemas
- forbidden sample-specific fields
- score consistency
- provenance joinability
- reproducibility across repeated runs



---

## Assumptions

- Input sources are phenotype-associated by construction.
- Source weights are meaningful and configured explicitly.
- Gene symbol mapping is imperfect and must be auditable.
- Multiple independent sources increase support.
- Absence from a source is not evidence against a gene.


---

## Limitations

- v1 scoring is heuristic.
- v1 does not estimate calibrated probabilities.
- v1 does not harmonize phenotype ontologies.
- v1 does not automate external source downloads.
- v1 does not perform enrichment analysis.
- v1 does not perform sample-level prioritization.

---

