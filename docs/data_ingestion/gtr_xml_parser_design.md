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

Not all `Measure` records represent genes; modality interpretation must therefore occur before downstream aggregation.

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

## GTR Test Scope Classification Policy

GTR test scope must be assigned using an empirical two-pass strategy whenever possible.

The parser should first extract all gene-test observations, then calculate:

```text
genes_per_test = number of unique gene symbols observed for each GTR accession
```

Then assign `test_scope` using deterministic thresholds:

```text
genes_per_test <= 5      targeted_gene
genes_per_test <= 25     small_panel
genes_per_test <= 100    medium_panel
genes_per_test > 100     large_panel
```

This replaces purely text/category-derived panel classification when enough gene-level observations are available.

Rationale:

- GTR test names and categories are heterogeneous.
- Many panel tests lack reliable structured panel-size metadata.
- Empirical `genes_per_test` provides a reproducible approximation of test breadth.
- Test breadth matters for utilization scoring because broad panels should contribute less than targeted tests.
- WES/WGS tests remain excluded or scored as zero contribution where explicitly identified.

Caveats:

`genes_per_test` is calculated from parsed GTR gene observations, not necessarily the complete laboratory wet-lab target design.
- A test may appear smaller than its true assay size if GTR records are incomplete.
- Explicit exome/genome classifications should override empirical gene-count thresholds.
- The thresholds are heuristic and must remain documented/versioned.

Implementation rule:

The parser may initially assign a provisional `test_scope` using test name/category text. After all rows are extracted, a deterministic second-pass classifier should revise non-exome/genome scopes using `genes_per_test`.

The final output should preserve both:

`test_scope`
`genes_per_test`

and optionally:

`test_scope_assignment_method`

Recommended assignment methods:

```text
explicit_exome_genome
empirical_gene_count
text_category_heuristic
unknown
```

## Analyte and Metabolomics Future

Analyte-based clinical tests are scientifically valuable and should be preserved for future work.

Observed example:

```text
Measure Type="Analyte"
```

These records may support future metabolomics- or biochemical-genetics-oriented projects, especially if collaborators move toward:

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

Current v1 implementation prioritizes conservative extraction fidelity over aggressive ontology inference.

The initial production parser should:

- operate only on pinned local GTR XML snapshots
- stream XML rather than load the full file into memory
- extract only test-level Measure Type="Gene" records for GSC gene sets
- preserve matched trait metadata
- preserve test metadata
- preserve lab metadata
- preserve parser version
- preserve extraction rule version
- avoid uncontrolled ontology expansion
- avoid implicit or hidden phenotype collapsing
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
| `independent_lab_count` | Laboratory count |

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

## Ontology Governance

Phenotype matching may introduce ontology expansion effects.

For example:
- broad neurological syndromes
- developmental disorders
- mitochondrial umbrella conditions

may recursively connect to many downstream trait aliases.

Therefore:

```text
raw matched trait counts should not automatically be interpreted as phenotype specificity
```

Future summarization layers may apply:

- ontology collapse
- trait deduplication
- generic term suppression
- primary-keyword prioritization
- ontology depth constraints

to reduce trait explosion and preserve phenotype interpretability.

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

## Broad Sequencing Test Interpretation Policy

GTR contains heterogeneous clinical testing modalities, including:

- targeted single-gene assays
- focused disease panels
- broad multigene panels
- whole exome sequencing (WES)
- whole genome sequencing (WGS)

Broad sequencing assays introduce an important interpretation challenge for GSC.

For example:

```text
a WGS clinical test may technically assay ~20,000 genes
```

but this does not imply:

```text
all assayed genes are phenotype-relevant
```

for the associated clinical indication.

Therefore, GSC must distinguish:

```text
genes explicitly linked to phenotype-associated clinical interpretation
```

from:

```text
genes incidentally captured by broad sequencing modality
```

## Conservative v1 Policy for Broad Tests

Current v1 GTR summarization behavior:

- preserve all raw parsed evidence rows
- exclude `test_scope = exome` from summary counts
- exclude `test_scope = genome` from summary counts
- preserve excluded records in raw evidence outputs
- aggregate evidence at the gene level for GSC-ready summaries

This allows:
- reproducible raw evidence preservation
- conservative phenotype-scoped summarization
- future reinterpretation under revised policies

For GSC v1:

- raw parsed evidence tables should preserve all extracted records
- phenotype-matched WES/WGS records may remain in raw evidence outputs
- GSC-ready summarized gene sets should conservatively exclude broad sequencing tests unless explicit phenotype-linked gene evidence is present

Broad assays should not automatically inflate phenotype-specific gene consensus.

## Proposed Test Scope Classification

Future GTR summarization may classify tests into categories such as:

| test_scope      | interpretation                      |
| --------------- | ----------------------------------- |
| `targeted_gene` | single-gene or highly focused assay |
| `small_panel`   | limited disease-focused panel       |
| `medium_panel`  | moderate panel size                 |
| `large_panel`   | very broad multigene panel          |
| `exome`         | whole exome sequencing              |
| `genome`        | whole genome sequencing             |
| `unknown`       | unable to confidently classify      |

These classifications may eventually support:

- filtering
- weighting
- sensitivity analyses
- provenance-aware interpretation
- reproducible downstream GSC aggregation

## Raw Evidence vs GSC-Ready Summaries

GSC-ready summaries are derived artifacts generated from raw parsed evidence rather than independent primary-source datasets.

GTR-derived outputs should be separated conceptually into:

### Raw Parsed Evidence

Detailed row-level evidence preserving:

- traits
- measures
- tests
- labs
- accessions
- parser provenance

These outputs prioritize completeness and reproducibility.

### GSC-Ready Gene Summaries

Collapsed phenotype-scoped summaries intended for consensus scoring.

These summaries may apply conservative interpretation policies such as:

- exclusion of broad WES/WGS tests
- panel-size heuristics
- duplicate assertion collapse
- analyte exclusion
- lab redundancy reduction

This distinction is critical because:

```text
clinical testing utilization evidence is not equivalent to mechanistic disease certainty
```

Notes:
`independent_lab_count` should be interpreted as a clinical utilization diversity metric rather than mechanistic evidence.

Higher values suggest broader cross-laboratory diagnostic adoption.

## Strategic Summary

For GSC v1:

```text
Trait-matched GTRLabTest + Measure Type="Gene"
```

is the preferred conservative route for phenotype-scoped GTR gene-set extraction.

Analyte-based records should be preserved as a future evidence channel, not discarded or incorrectly collapsed into gene-level evidence.

---