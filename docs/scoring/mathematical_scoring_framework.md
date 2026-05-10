# Mathematical Scoring Framework for GSC (gene_set_consensus) repository

This mathematical scoring framework for the gene set consensus (GSC) repo is SAGE-owned, and acts a recommended guideline for DEX-mediated implementation.  This document provides guidance for implementation.

## Document Authority

This is a SAGE-owned scientific design document.

It is authoritative for:
- evidence interpretation
- semantic channel definitions
- scientific rationale
- source-tier recommendations
- scoring-governance constraints

It is not the final executable implementation contract.

DEX must translate this document into deterministic implementation behavior in:
- `docs/contracts/system_contract.md`
- scoring configuration files
- tests and validation fixtures

Where this document conflicts with the DEX system contract, the conflict must be resolved explicitly before implementation.

## 1. Purpose

This document defines the mathematical scoring model for GSC hybrid semantic-channel scoring.

The framework is designed to be:

- deterministic
- explainable
- provenance-aware
- resistant to evidence inflation
- extensible to future evidence sources
- usable for epilepsy and mitochondrial disease v1 workflows

GSC scores are evidence-support scores, not probabilities of causality, pathogenicity, penetrance, or clinical actionability.

---

## 2. Core Scoring Equation

For each gene within a phenotype:

```text
semantic_consensus_score =
    direct_disease_score
  + clinical_interpretation_score
  + contextual_biology_score
  + utilization_score
  + exploratory_score
  + convergence_score
  - conflict_penalty
```

Each component score is independently calculated and capped.

`consensus_score` is the implementation-facing final score column used by DEX.

During transition, DEX may preserve:
- `weighted_source_sum`
- `consensus_score`
- `semantic_consensus_score`

Once semantic scoring is adopted as the active scoring profile, `consensus_score` may be defined as `semantic_consensus_score` in the system contract.

---

## 3. Channel Caps

```text
direct_disease_score             cap = 4.0
clinical_interpretation_score    cap = 3.0
contextual_biology_score         cap = 2.0
utilization_score                cap = 1.0
exploratory_score                cap = 0.75
convergence_score                cap = 1.5
```

These caps prevent indirect evidence from overpowering direct human disease evidence.

---

## 4. Tier Weights

```text
platinum        = 4.0
gold            = 3.0
silver          = 1.5
bronze          = 0.75
annotation_only = 0.0
```

Tier weights are applied within semantic channels, then bounded by channel caps.

---

## 5. General Channel Formula


For a semantic channel `c`:

```text
channel_score_c = min(channel_cap_c, normalized_evidence_sum_c)
```

where:

```text
normalized_evidence_sum_c =
    sum(source_weight_i × source_quality_modifier_i × phenotype_match_modifier_i × independence_modifier_i)
```

Thus each evidence contribution is adjusted **before** being added.

### 5.1 Formula Precedence

Source-specific scoring rules override the generic channel formula.

Precedence order:

1. source-specific scoring rule
2. phenotype-specific scoring profile
3. semantic channel default rule
4. global default tier weight

If no deterministic rule exists, the source must be treated as `annotation_only` until the scoring profile is updated.

---

## 6. Required Modifiers

### 6.1 source_weight

Derived from tier:

```text
platinum = 4.0
gold = 3.0
silver = 1.5
bronze = 0.75
annotation_only = 0.0
```

### 6.2 source_quality_modifier

Adjusts for evidence strength within a source.

All modifiers must be explicitly configured or resolved by deterministic source-specific rules.

If no source-specific modifier is provided, the default modifier is `1.0`.

DEX must not infer modifier values from free text.

```text
high_quality = 1.0
moderate_quality = 0.75
low_quality = 0.5
uncertain_quality = 0.25
```

### 6.3 phenotype_match_modifier

Controls whether evidence matches the selected phenotype.

```text
exact_phenotype_match = 1.0
close_subphenotype_match = 0.75
broad_parent_phenotype_match = 0.5
weak_or_ambiguous_match = 0.25
no_match = 0.0
```

Example:

```text
DEE evidence used in DEE profile = 1.0
DEE evidence used in broad epilepsy profile = 0.75
broad neurodevelopmental panel used in epilepsy profile = 0.25–0.5
```

### 6.4 independence_modifier

Controls correlated-source inflation.

```text
independent_primary_source = 1.0
partially_correlated_source = 0.75
strongly_correlated_source = 0.5
derived_or_redundant_source = 0.25
```

Example:

```text
GTR + OMIM + PanelApp may not be fully independent because clinical panels often inherit prior curated disease-gene assumptions.
```

---

## 7. Saturation Rule

Evidence accumulation within a channel should use caps and optional diminishing returns.

For sources with repeated observations, such as GTR panel counts, use log-scaled saturation rather than linear accumulation.

Recommended formula:

```text
saturated_score = channel_cap × log(1 + observed_support) / log(1 + saturation_point)
```

bounded by:

```text
saturated_score <= channel_cap
```

Example for GTR:

```text
utilization_score = min(1.0, 1.0 × log(1 + weighted_panel_support) / log(1 + 20))
```

Interpretation:

- first few phenotype-specific panels matter
- hundreds of panels do not linearly inflate confidence
- broad testing reuse saturates quickly

---

## 8. Current Source Rules

### 8.1 Epi25

Epi25 contributes to:

```text
direct_disease_score
```

Recommended scoring:

```text
exomewide_significant = 4.0
strong_subthreshold = 3.0
candidate_signal = 1.5
annotation_only_or_non-enriched = 0.0
```

Modifiers:

```text
phenotype_match_modifier applies
variant_class_quality_modifier applies
```

Example:

```text
SCN1A, exome-wide significant DEE PTV burden:
4.0 × 1.0 × 1.0 = 4.0
```

Example:

```text
candidate damaging missense signal in broad epilepsy:
1.5 × 0.75 = 1.125
```

### 8.2 MitoCarta

MitoCarta contributes to:

```text
contextual_biology_score
```

Recommended scoring:

```text
MitoCarta membership = 2.0 in mitochondrial disease profile
MitoCarta membership = 1.0 in epilepsy profile unless mitochondrial epilepsy profile is selected
```

Rationale:

MitoCarta supports mitochondrial localization/function, not disease causality.

### 8.3 GTR

GTR contributes to:

`utilization_score`

Recommended maximum:

```text
max utilization_score = 1.0
```

GTR evidence reflects diagnostic testing utilization, not disease causality. Therefore, GTR scoring must suppress broad or ambiguous testing contexts and must saturate rapidly.

Suggested weighted panel support:

```text
weighted_panel_support =
    targeted_gene_count × 1.00
  + small_panel_count × 0.75
  + medium_panel_count × 0.50
  + large_panel_count × 0.25
  + panel_unsized_count × 0.10
  + unknown_scope_count × 0.05
  + exome_or_genome_count × 0.00
```

Then:

```text
utilization_score =
    min(1.0, log2(1 + weighted_panel_support))
```

Implementation note:
`log2(1 + weighted_panel_support)` must be capped at 1.0. 

This means GTR utilization can provide positive support, but cannot exceed the utilization channel cap.

Interpretation:

- targeted gene tests contribute most strongly
- small and medium panels contribute moderately
- large panels contribute weakly
- unsized panels contribute very weakly
- unknown-scope tests contribute minimally
- exome/genome tests contribute zero utilization score
- hundreds of panel observations cannot linearly inflate confidence

This makes GTR positive but weak, preserves clinical-utilization value, and prevents broad or ambiguous testing reuse from dominating consensus scoring.

### 8.4 Genes4Epilepsy

Genes4Epilepsy contributes to:

```text
exploratory_score
```

Recommended:

```text
Genes4Epilepsy membership = 0.75
```

No repeated-count inflation unless future metadata supports internal evidence stratification.

---

## 9. ClinVar Future Rules

ClinVar contributes to:

```text
clinical_interpretation_score
```

Recommended scoring:

```text
Pathogenic + practice guideline = 3.0
Pathogenic + expert panel = 2.75
Pathogenic + multiple submitters/no conflict = 2.25
Likely pathogenic + expert panel/multiple submitters = 2.0
Pathogenic + single submitter = 1.25
Likely pathogenic + single submitter = 1.0
VUS = 0.0
Conflicting interpretations = conflict flag and possible penalty
Benign/Likely benign only = 0.0 or negative evidence flag
```

ClinVar scoring must be phenotype-aware. A pathogenic variant assertion should not score strongly unless the ClinVar disease/trait matches the selected GSC phenotype.

ClinVar gene-level scoring must not sum all pathogenic variants linearly.

For v1 semantic scoring, ClinVar should contribute the maximum qualifying phenotype-matched assertion class per gene, not the number of submitted variants.

Variant count may be preserved as metadata, but it must not inflate `clinical_interpretation_score` unless a future ClinVar burden model is explicitly defined.

---

## 10. OMIM Future Rules

OMIM contributes to:

```text
clinical_interpretation_score
```

or a future:

```text
expert_curation_score
```

Recommended initial treatment:

```text
confirmed phenotype-matched disease-gene relationship = 3.0
phenotype-adjacent relationship = 1.5–2.0
ambiguous relationship = annotation_only
```

OMIM should not be blindly treated as binary membership. Disease-gene relationship strength and phenotype match must be preserved.

---

## 11. PanelApp Future Rules

PanelApp contributes to:

```text
clinical_interpretation_score
```

Recommended:

```text
Green = 2.5–3.0
Amber = 1.0–1.5
Red = 0.0 or annotation_only
```

PanelApp should also receive an independence modifier if overlapping strongly with OMIM, ClinVar, or GTR.

---

## 12. Transcriptomics / Network Future Rules

Transcriptomics and network convergence contribute to:

```text
convergence_score
```

Recommended:

```text
replicated phenotype-relevant convergence = 1.5
single-dataset convergence = 0.75
weak or indirect convergence = 0.25–0.5
non-matching tissue/context = annotation_only
```

This evidence supports functional relevance, not primary disease causality.

---

## 13. Metabolomics / Analyte Future Rules

Metabolomics or analyte evidence contributes to:

```text
convergence_score
```

or future:

```text
biochemical_phenotype_score
```

Recommended:

```text
direct phenotype-relevant analyte-gene/pathway link = 1.5
pathway-level biochemical support = 1.0
weak analyte association = 0.5
unmapped analyte-only evidence = annotation_only
```

Analyte evidence should not be forced into gene scoring without a validated analyte-to-gene or analyte-to-pathway mapping.

---

## 14. Conflict Penalty

Conflict penalties reduce final confidence but should never erase raw evidence.

Recommended:

```text
minor_conflict = 0.25
moderate_conflict = 0.5
major_conflict = 1.0
severe_dispute_or_refutation = 2.0
```

Examples:

```text
ClinVar conflicting interpretations = 0.5–1.0 penalty
PanelApp Red conflicting with other sources = 0.25–0.5 penalty
published failed replication of candidate association = 1.0–2.0 penalty
```

Conflict penalties should be transparent and source-attributed.

---

## 15. Final Score Interpretation

Recommended interpretation bands:

```text
0.00–0.74    minimal support
0.75–1.49    exploratory support
1.50–2.99    moderate support
3.00–4.99    strong support
5.00+        multi-channel high support
```

Important:

These bands are descriptive, not clinical classifications.

---

## 16. Defensive Scoring Examples

### 16.1 Epi25-only strong epilepsy gene

```text
direct_disease_score = 4.0
clinical_interpretation_score = 0.0
contextual_biology_score = 0.0
utilization_score = 0.0
exploratory_score = 0.0
convergence_score = 0.0
conflict_penalty = 0.0

semantic_consensus_score = 4.0
```

Interpretation:

Strong direct human epilepsy association.

### 16.2 GTR + Genes4Epilepsy only

```text
direct_disease_score = 0.0
clinical_interpretation_score = 0.0
contextual_biology_score = 0.0
utilization_score = 1.0
exploratory_score = 0.75
convergence_score = 0.0
conflict_penalty = 0.0

semantic_consensus_score = 1.75
```

Interpretation:

Clinically used and literature-mentioned, but not equivalent to direct disease association.

### 16.3 MitoCarta-only gene in mitochondrial disease profile

```text
contextual_biology_score = 2.0
semantic_consensus_score = 2.0
```

Interpretation:

Strong mitochondrial context, but not sufficient alone for disease-gene status.

### 16.4 MitoCarta + ClinVar pathogenic support

```text
contextual_biology_score = 2.0
clinical_interpretation_score = 2.25
semantic_consensus_score = 4.25
```

Interpretation:

Strong mitochondrial context plus clinical variant interpretation support.

### 16.5 Broad GTR WES-only gene

```text
utilization_score = 0.0
semantic_consensus_score = 0.0 or annotation_only
```

Interpretation:

Technically assayed, but not phenotype-specific gene evidence.

---

## 17. Required Output Columns

Required scoring outputs during semantic-scoring transition:

- `phenotype`
- `gene_symbol`
- `gene_id`
- `source_count`
- `weighted_source_sum`
- `consensus_score`
- `semantic_consensus_score`
- `direct_disease_score`
- `clinical_interpretation_score`
- `contextual_biology_score`
- `utilization_score`
- `exploratory_score`
- `convergence_score`
- `conflict_penalty`
- `source_list`
- `evidence_semantics_summary`
- `tier_summary`
- `scoring_profile`
- `score_explanation`

---

## 18. Assumptions

- Evidence sources are heterogeneous and not directly interchangeable.
- Direct human disease evidence should dominate indirect contextual evidence.
- Clinical utilization is informative but confounded.
- Biological localization supports plausibility but not causality.
- Scores are heuristic evidence-support values, not probabilities.

---

## 19. Limitations

- Weights are governance-defined and not statistically calibrated.
- Channel caps are defensible but heuristic.
- Source-independence modifiers require judgment.
- Future empirical benchmarking may require recalibration.
- Cross-phenotype score comparison is not valid unless scoring profiles are explicitly harmonized.

---

## 20. Edge Cases

- A gene with strong localization but no disease evidence.
- A gene appearing in many broad panels.
- A gene with conflicting clinical interpretations.
- A rare-disease gene lacking large cohort evidence.
- A transcriptomic convergence signal reflecting downstream pathology rather than causality.
- A gene with strong evidence in one epilepsy subtype but weak evidence in another.

---

## 21. Validation Strategy

Before freezing scoring v1.0, validate with:

### Known-gene recovery

##### Epilepsy:

- SCN1A
- DEPDC5
- NEXMIF
- SYNGAP1
- STX1B
- WDR45

#### Mitochondrial disease:

- POLG
- TWNK
- TK2
- SURF1
- NDUFS-family genes
- MT-ATP6

### Inflation testing

Confirm:

```text
GTR + Genes4Epilepsy < Epi25 exome-wide
MitoCarta alone < MitoCarta + ClinVar/OMIM
Broad GTR WES/WGS does not inflate scores
```

### Ablation testing


Run scoring with:

- GTR removed
- exploratory evidence removed
- contextual biology removed
- clinical interpretation removed

Inspect whether rankings behave as expected.

### Explainability testing

For top-ranked genes, verify that the score explanation clearly identifies which evidence channels drive ranking.

---

## 22. Implementation Implications for DEX

DEX should implement:

- independent channel score columns
- deterministic tier weights
- configurable channel caps
- configurable phenotype-specific scoring profiles
- source-specific scoring rules
- raw evidence preservation
- conflict flags and penalties
- score explanations

DEX should not implement:

- irreversible flattened scores only
- linear uncapped additive evidence
- hard-coded phenotype assumptions
- hidden evidence modifiers
- broad panel inflation

---