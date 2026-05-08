# Implementation Plan: `gene_set_consensus`

## Document Control

| Field | Value |
|---|---|
| Repository | `gene_set_consensus` |
| Abbreviation | GSC |
| Artifact type | `implementation_plan` |
| Owning agent | DEX — SWE Agent |
| Intended location | `gene_set_consensus/docs/plans/implementation_plan.md` |
| Companion artifact | `gene_set_consensus/docs/contracts/system_contract.md` |
| Current target | v1.0 portfolio-ready repository with staged semantic-channel scoring |
| Implementation status | Active staged implementation plan |

---

## 1. Objective

Build a reproducible Python/Bash pipeline that constructs phenotype-scoped, provenance-aware, semantically decomposed consensus gene evidence from heterogeneous sources.

The pipeline must:

1. ingest multiple governed gene-level evidence sources
2. validate input schemas, source manifests, release manifests, and scoring profiles
3. normalize gene identifiers
4. collapse within-source duplicates
5. preserve source provenance
6. construct gene-source evidence tables
7. preserve legacy weighted scoring during transition
8. emit semantic-channel score columns
9. prevent scoring inflation
10. support future ClinVar, OMIM, PanelApp, transcriptomics, and metabolomics adapters without schema drift

---

## 2. Current Strategic Decision

GSC will use a **staged semantic rollout**.

Do not immediately replace `consensus_score`.

Transition behavior:

```text
legacy weighted score remains backward-compatible
semantic-channel scores are added experimentally
semantic_consensus_score is emitted
consensus_score becomes semantic_consensus_score only in a future declared release
```

This avoids breaking existing outputs while enabling semantic scoring validation.

---

## 3. Development Phases

### Phase A — Preserve Current Stable Pipeline

Status: partially complete.

Current stable capabilities:

- phenotype-scoped execution
- source validation
- source manifest validation
- release manifest validation
- GTR raw evidence parser
- GTR gene summary builder
- experimental GTR releases
- semantic metadata propagation
- legacy output compatibility

Do not destabilize production releases while implementing semantic scoring.

---

### Phase B — Add Scoring Profile Config Layer

Goal: make semantic scoring behavior explicit and deterministic.

Create:

```text
config/scoring_profiles/
  epilepsy_semantic_v0.1.yaml
  mitochondrial_semantic_v0.1.yaml

config/scoring_rules/
  epi25_semantic_rules.yaml
  gtr_utilization_rules.yaml
  mitocarta_contextual_rules.yaml
  genes4epilepsy_exploratory_rules.yaml
```

Each scoring profile must define:

```yaml
profile:
  profile_id:
  phenotype_family:
  version:
  active_score:
  emit_legacy_scores:
  emit_semantic_scores:

tier_weights:
  platinum: 4.0
  gold: 3.0
  silver: 1.5
  bronze: 0.75
  annotation_only: 0.0

channel_caps:
  direct_disease_score: 4.0
  clinical_interpretation_score: 3.0
  contextual_biology_score: 2.0
  utilization_score: 1.0
  exploratory_score: 0.75
  convergence_score: 1.5

modifier_defaults:
  source_quality_modifier: 1.0
  phenotype_match_modifier: 1.0
  independence_modifier: 1.0
```

Commit target:

```text
Add semantic scoring profile configs
```

Validation required:

```bash
python scripts/validation/validate_scoring_profile.py --profile config/scoring_profiles/epilepsy_semantic_v0.1.yaml
python scripts/validation/validate_scoring_profile.py --profile config/scoring_profiles/mitochondrial_semantic_v0.1.yaml
```

---

### Phase C — Extend Source Metadata Contract

Goal: make source metadata first-class scoring input.

Update phenotype configs/source manifests to include or inherit:

```yaml
evidence_semantics:
evidence_tier:
semantic_channel:
scoring_rule_id:
```

Current canonical mappings:

| Source | semantic_channel | evidence_tier |
|---|---|---|
| Epi25 exome-wide significant | direct_disease | platinum |
| Epi25 strong subthreshold | direct_disease | gold |
| Epi25 candidate | direct_disease | silver |
| MitoCarta | contextual_biology | gold |
| GTR | clinical_utilization | silver |
| Genes4Epilepsy | exploratory_literature | bronze |

Commit target:

```text
Add semantic scoring metadata to source configs
```

Tests:

- config rejects unknown semantic channel
- config rejects unknown evidence tier
- source without semantic metadata becomes `annotation_only` only when allowed by profile

---

### Phase D — Update Normalization and Aggregation Schema

Goal: propagate semantic metadata through all intermediate tables.

Update `normalized_source_records.tsv` to include:

```text
evidence_semantics
evidence_tier
semantic_channel
scoring_rule_id
```

Update `gene_frequency_table.tsv` to include:

```text
evidence_semantics_summary
evidence_tier_summary
semantic_channel_summary
```

Commit target:

```text
Propagate semantic scoring metadata through aggregation
```

Tests:

- semantic summaries match source rows
- no `unspecified` values appear in experimental configs
- legacy outputs remain valid

---

### Phase E — Implement Semantic Scoring Engine

Goal: compute semantic-channel score columns without replacing legacy score.

Update or create:

```text
src/gene_set_consensus/semantic_scoring.py
src/gene_set_consensus/scoring_profiles.py
scripts/step_04_score_consensus.py
tests/unit/test_semantic_scoring.py
```

Required output columns:

```text
semantic_consensus_score
direct_disease_score
clinical_interpretation_score
contextual_biology_score
utilization_score
exploratory_score
convergence_score
conflict_penalty
scoring_profile
active_score
score_explanation
```

Formula:

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

Each channel must be capped.

Commit target:

```text
Implement semantic-channel scoring outputs
```

Tests:

- channel cap enforcement
- semantic_consensus_score arithmetic
- consensus_score remains legacy when `active_score: weighted_source_sum`
- consensus_score equals semantic score when `active_score: semantic_consensus_score`

---

### Phase F — Implement Source-Specific Rules

Goal: avoid generic scoring drift.

#### F1 — Epi25 Rules

Implement deterministic scoring for Epi25 evidence classes:

```text
exomewide_significant = 4.0
strong_subthreshold = 3.0
candidate_signal = 1.5
annotation_only_or_non_enriched = 0.0
```

Required Epi25 ingestion outputs:

```text
phenotype_stratum
variant_class
evidence_class
p_value_raw
p_value_numeric
p_value_zero_flag
odds_ratio
case_count
control_count
ensembl_gene_id
hgnc_symbol
```

Do not collapse Epi25 into a single undifferentiated epilepsy gene list.

Commit target:

```text
Add Epi25 semantic scoring rules
```

#### F2 — GTR Rules

Implement utilization scoring with saturation:

```text
weighted_panel_support =
    targeted_gene_count × 1.0
  + small_panel_count × 0.75
  + medium_panel_count × 0.5
  + large_panel_count × 0.25
  + exome_or_genome_count × 0.0

utilization_score =
    min(1.0, log(1 + weighted_panel_support) / log(21))
```

Required GTR summary fields:

```text
gtr_test_count
independent_lab_count
test_scope_summary
targeted_gene_count
small_panel_count
medium_panel_count
large_panel_count
exome_or_genome_count
```

Commit target:

```text
Add saturated GTR utilization scoring
```

#### F3 — MitoCarta Rules

Implement contextual biology score:

```text
mitochondrial disease profile: 2.0
broad epilepsy profile: 1.0 unless mitochondrial epilepsy profile selected
```

Commit target:

```text
Add MitoCarta contextual scoring rule
```

#### F4 — Genes4Epilepsy Rules

Implement exploratory score:

```text
Genes4Epilepsy membership = 0.75
```

Commit target:

```text
Add exploratory literature scoring rule
```

---

### Phase G — Output Contract Update

Goal: emit final transitional semantic output.

Update:

```text
src/gene_set_consensus/output_validation.py
scripts/step_05_write_outputs.py
tests/validation/test_output_contract.py
```

Final consensus output must include:

```text
phenotype
gene_id
gene_symbol
source_count
weighted_source_sum
consensus_score
semantic_consensus_score
direct_disease_score
clinical_interpretation_score
contextual_biology_score
utilization_score
exploratory_score
convergence_score
conflict_penalty
source_list
weight_tier_summary
evidence_semantics_summary
evidence_tier_summary
semantic_channel_summary
mapping_status_summary
provenance_id
run_id
gsc_version
generated_at
scoring_profile
active_score
score_explanation
```

Commit target:

```text
Extend output contract for semantic scoring
```

---

### Phase H — Validation and Inflation Testing

Goal: prove semantic scoring prevents known failure modes.

Create:

```text
tests/unit/test_semantic_scoring.py
tests/validation/test_semantic_output_contract.py
tests/validation/test_score_inflation_guards.py
scripts/validation/validate_scoring_profile.py
scripts/validation/validate_semantic_scores.py
```

Required checks:

```text
GTR + Genes4Epilepsy < Epi25 exome-wide
MitoCarta alone < MitoCarta + ClinVar/OMIM
Broad GTR WES/WGS does not increase utilization_score
ClinVar variant counts do not linearly inflate clinical_interpretation_score
Duplicate genes within one source do not inflate channel scores
Unknown semantic channel fails validation
Unknown tier fails validation
```

Commit target:

```text
Add semantic scoring validation and inflation guards
```

---

### Phase I — Experimental Release Evaluation

Goal: evaluate semantic scoring without touching production.

Use experimental releases only:

```text
epilepsy_gold_bronze_gtr_experimental_v0.1
mitocarta_gtr_experimental_v0.1
```

Run:

```bash
python run_pipeline.py --phenotype epilepsy_gold_bronze_gtr_experimental
python run_pipeline.py --phenotype mitocarta_gtr_experimental
```

Inspect known genes:

Epilepsy:

```text
SCN1A
DEPDC5
NPRL3
ALDH7A1
POLG
NEXMIF
SYNGAP1
WDR45
```

Mitochondrial:

```text
POLG
TWNK
TK2
SURF1
NDUFS-family genes
MT-ATP6
```

Commit target:

```text
Evaluate experimental semantic scoring releases
```

---

### Phase J — Release Promotion Decision

Semantic scoring may become primary only after:

- test suite passes
- inflation tests pass
- known-gene behavior reviewed
- score explanations are interpretable
- README documents scoring interpretation
- production release configs explicitly opt in

Promotion commit target:

```text
Promote semantic scoring profile for GSC v1
```

Until then:

```text
consensus_score = weighted_source_sum
```

remains production-safe.

---

## 4. Backward Compatibility Plan

During transition preserve:

```text
weighted_source_sum
weight_tier_summary
consensus_score
```

Add:

```text
semantic_consensus_score
semantic channel score columns
evidence_semantics_summary
evidence_tier_summary
semantic_channel_summary
```

Do not remove legacy fields until downstream compatibility is verified.

---

## 5. Reproducibility Plan

Semantic scoring must be deterministic.

Required:

- all weights in config
- all caps in config
- all modifiers in config
- source-specific rule IDs recorded
- scoring profile recorded in final outputs
- no free-text inference
- deterministic sort order
- checksum-based reproducibility validation

---

## 6. Suggested Commit Sequence

```text
Add semantic scoring profile configs
Add semantic scoring metadata to source configs
Propagate semantic scoring metadata through aggregation
Implement semantic-channel scoring outputs
Add Epi25 semantic scoring rules
Add saturated GTR utilization scoring
Add MitoCarta contextual scoring rule
Add exploratory literature scoring rule
Extend output contract for semantic scoring
Add semantic scoring validation and inflation guards
Evaluate experimental semantic scoring releases
Document semantic scoring usage and interpretation
Promote semantic scoring profile for GSC v1
```

---

## 7. Risk Register

| Risk | Mitigation |
|---|---|
| Legacy and semantic scores confuse users | Keep `active_score` explicit and document transition |
| New semantic channels drift uncontrolled | Require profile version bump and validation |
| GTR panel counts inflate scores | Use saturation and broad-test exclusion |
| ClinVar variant counts inflate clinical interpretation | Use max qualifying assertion class, not variant count |
| Epi25 loses subtype/variant-class meaning | Preserve phenotype stratum and variant class |
| MitoCarta interpreted as disease causality | Confine to contextual biology |
| Genes4Epilepsy over-ranks candidates | Cap exploratory score at 0.75 |
| Hidden modifier inference | Fail or annotation_only when rules absent |
| Output schema breaks downstream consumers | Preserve legacy columns during transition |

---

## 8. Final Implementation Principle

GSC should implement semantic scoring as a deterministic, explainable, provenance-preserving extension of the existing pipeline.

The winning architecture is:

```text
legacy compatibility
+
semantic decomposition
+
explicit scoring profiles
+
source-specific deterministic rules
+
inflation guards
+
auditable outputs
```
