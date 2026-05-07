# GTR XML Parser Design

## Purpose

This document records the emerging parser architecture for transforming the pinned GTR XML snapshot into phenotype-scoped, provenance-aware GSC-ready gene-set products.

This design is based on exploratory inspection of the local GTR XML snapshot staged at:

```text
/mnt/storage/gtr/gtr_ftp.xml
```

## Core XML Model

The GTR XML snapshot is organized around laboratory and test records.

Observed high-level structure:

```text
GTRLabData
  → GTRLab
    → Organization / lab metadata
    → GeneTesting
    → GTRLabTest
      → ClinVarSet
        → ClinVarAssertion
          → TraitSet / Trait
          → MeasureSet / Measure
```

## Phenotype Semantics

Phenotype and disease semantics are carried primarily through:

```text
TraitSet
  → Trait
    → Name
    → Symbol
    → XRef
```

Trait records may include useful external identifiers such as:

- OMIM
- MONDO
- Orphanet
- MedGen
- GeneReviews
- Human Phenotype Ontology

These identifiers should be preserved when possible.

## Gene Evidence Route

For GSC v1, the preferred conservative gene extraction route is:

```text
ClinVarAssertion
  → MeasureSet
    → Measure Type="Gene"
      → Symbol Type="Preferred"
      → XRef DB="Gene"
      → XRef DB="OMIM"
      → Location assembly="GRCh38"
```

This route directly links:

```text
phenotype trait → gene measure → test metadata → lab metadata
```

and is therefore more appropriate for GSC than lab-level gene summaries alone.

Phenotype-scoped extraction in GSC is fundamentally trait-centric:

```text
Trait match → associated Measure extraction
```

## Lab-Level GeneTesting

The XML also contains:

```text
GTRLab
  → GeneTesting
    → GeneSymbol
```

This appears to be lab-level gene testing metadata.

For GSC v1, lab-level `GeneTesting` should not be treated as direct phenotype-specific gene evidence unless a defensible test-level or trait-level linkage is established.

It may be useful later for:

- lab-level clinical testing coverage
- independent laboratory diversity metrics
- quality control against test-level gene extraction

## Test Modality Distinction

A single GTRLabTest may contain multiple ClinVarAssertions and multiple MeasureSets.

Different assertions within the same test may carry different evidence modalities, including:

- Gene
- Analyte
- potentially additional future Measure types

Therefore, modality interpretation should occur at the `Measure` level rather than the test level.

Additionally, GTR includes multiple clinical testing modalities.

Two important Measure types observed or anticipated are:

```text
Measure Type="Gene"
Measure Type="Analyte"
```

For GSC v1 gene-set construction:

```text
Measure Type="Gene"
```

is the primary route.

Analyte-based tests should not be forced into gene-set evidence in v1.

## Analyte and Metabolomics Future

Analyte-based clinical tests are scientifically valuable and should be preserved for future work.

Observed example:

```text
Measure Type="Analyte"
```

These records may support future metabolomics-oriented projects, especially if collaborators move toward:

- clinical metabolomics
- biochemical genetics
- mitochondrial disease biomarker analysis
- analyte-to-gene/pathway mapping
- metabolite evidence overlays

Future analyte-focused extraction may generate separate products such as:

```text
gtr_mitochondria_analyte_evidence.tsv
gtr_epilepsy_analyte_evidence.tsv
```

These should remain distinct from gene-set products unless a validated analyte-to-gene mapping layer is introduced.

## Conservative v1 Parser Policy

The initial production parser should:

- operate only on pinned local GTR XML snapshots
- stream XML rather than load the full file into memory
- extract only test-level Measure Type="Gene" records for GSC gene sets
- preserve matched trait metadata
- preserve test metadata
- preserve lab metadata
- preserve parser version
- preserve extraction rule version
- avoid fuzzy ontology expansion
- avoid hidden phenotype collapsing
- avoid premature XML element clearing during streaming iteration
- preserve parent-child semantic integrity during extraction

## Proposed v1 Output Schema

A GTR-derived GSC-ready gene evidence row should preserve:

| Field                     | Description                                      |
| ------------------------- | ------------------------------------------------ |
| `gene_symbol`             | Preferred gene symbol from `Measure Type="Gene"` |
| `gene_id`                 | NCBI Gene ID when available                      |
| `omim_gene_id`            | OMIM gene identifier when available              |
| `matched_trait_name`      | Trait name that matched extraction rules         |
| `matched_trait_id`        | GTR/ClinVar trait ID                             |
| `matched_trait_xrefs`     | Pipe-delimited external trait identifiers        |
| `matched_keyword`         | Keyword or rule that triggered phenotype match   |
| `measure_id`              | GTR/ClinVar measure ID                           |
| `measure_type`            | Expected to be `Gene` for v1 gene-set products   |
| `gtr_accession`           | GTR accession for the test                       |
| `gtr_test_id`             | GTR internal test ID                             |
| `test_name`               | GTR test name                                    |
| `test_version`            | GTR test version                                 |
| `test_categories`         | Pipe-delimited GTR test categories               |
| `lab_id`                  | GTR lab ID                                       |
| `lab_name`                | Laboratory name                                  |
| `last_update`             | GTR test last update date                        |
| `last_touched`            | GTR test last touched date                       |
| `source_snapshot`         | Pinned GTR snapshot identifier                   |
| `parser_version`          | Versioned XML parser behavior                    |
| `extraction_rule_version` | Versioned phenotype extraction rule behavior     |


## Phenotype Matching

For v1, phenotype matching should be explicit and conservative.

Example epilepsy terms may include:

- epilepsy
- epileptic
- seizure
- seizures
- developmental epileptic encephalopathy
- infantile spasms
- generalized epilepsy
- focal epilepsy

Example mitochondrial terms may include:

- mitochondrial
- mitochondrial disease
- mitochondrial disorder
- mitochondrial depletion
- oxidative phosphorylation
- OXPHOS
- respiratory chain
- Leigh syndrome
- POLG

These term sets should eventually live in versioned extraction-rule configuration files, not hardcoded parser logic.

This allows the same pinned GTR snapshot to be reinterpreted under evolving phenotype definitions without modifying raw source data.

## Parser Version vs Extraction Rule Version

`parser_version` records structural XML parsing behavior:

```text
How did GSC read the GTR XML?
```

`extraction_rule_version` records phenotype interpretation behavior:

```text
Which phenotype-matching rules were applied?
```

These are separate because the same XML parser may support multiple phenotype rule sets, and the same rule set may be rerun after parser improvements.

## Important Interpretation Caution

GTR evidence represents clinical testing utilization evidence.

It does not directly represent:

- pathogenicity probability
- disease causality certainty
- penetrance
- mechanistic evidence
- consortium statistical significance

Genes may appear in broad panels, exploratory panels, or commercially permissive testing products. Raw GTR frequency should therefore not be interpreted as mechanistic certainty.

## Strategic Summary

For GSC v1:

```text
Trait-matched GTRLabTest + Measure Type="Gene"
```

is the preferred conservative route for phenotype-scoped GTR gene-set extraction.

Analyte-based records should be preserved as a future evidence channel, not discarded or incorrectly collapsed into gene-level evidence.

---