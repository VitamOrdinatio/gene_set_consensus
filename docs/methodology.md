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


---

## Scientific Revision Policy

GSC is designed to support scientific revision with provenance preservation.

Gene-disease associations may change over time due to:
- new consortium releases
- larger patient cohorts
- revised phenotype ontology
- updated burden analyses
- publication reinterpretation

Therefore:
- GSC outputs are versioned interpretations
- not permanent biological truth

Historical outputs should remain reproducible even after future scientific revisions.

---

## Temporal Provenance

A GSC output reflects:
- the source releases
- source acquisition timestamps
- identifier mappings
- rule configurations
- evidence channels

available at the time of processing.

Future runs using newer source releases may legitimately produce different outputs.

Planned provenance-aware metadata includes:
- source_release
- source_download_date
- publication_anchor
- identifier_map_version
- mapping_source
- rule_set_version

---

## Evidence Tier Philosophy

Evidence tiers reflect:
- curation philosophy
- scale of supporting evidence
- source confidence

not absolute biological truth.

Current tier semantics:

- gold
  - flagship consortium-scale evidence
  - highly curated canonical resources

- silver
  - systematic aggregation
  - clinical data mining

- bronze
  - literature-derived lists
  - smaller curated publications

---

## Phenotype Rollups

Some phenotypes represent umbrella clinical concepts.

Example:
- EPI may incorporate subtype evidence from:
  - DEE
  - NAFE

Rollup behavior should remain:
- explicit
- versioned
- reproducible
- provenance-aware

rather than implicit.
