# System Contract: `gene_set_consensus`

## Document Control

| Field | Value |
|---|---|
| Repository | `gene_set_consensus` |
| Abbreviation | GSC |
| Artifact type | `system_contract` |
| Owning agent | DEX — SWE Agent |
| Intended location | `gene_set_consensus/docs/contracts/system_contract.md` |
| Companion artifact | `gene_set_consensus/docs/plans/implementation_plan.md` |
| Scientific governance inputs | `hybrid_semantic_scoring_framework.md`; `mathematical_scoring_framework.md`; `epi25_to_gsc.md` |
| Current target | v1.0 portfolio-ready repository with staged semantic scoring rollout |
| Implementation status | Active architecture contract |

---

## 1. Contract Purpose

This system contract defines the architectural, data, interface, validation, scoring, and reproducibility obligations for the `gene_set_consensus` repository.

GSC is a phenotype-scoped, gene-level evidence harmonization system. It transforms heterogeneous gene-level evidence sources into deterministic, provenance-aware, semantically decomposed consensus evidence artifacts.

GSC is not merely a gene-list overlap tool. It is a governed evidence-integration layer that preserves:

- phenotype scope
- source provenance
- evidence semantics
- evidence tiers
- source-level traceability
- legacy weighted score compatibility
- semantic-channel score decomposition

This contract exists to prevent schema drift, hidden weighting, scoring inflation, and irreversible evidence collapse.

---

## 2. Authority and Precedence

SAGE-owned scoring documents are authoritative for scientific rationale and evidence interpretation.

DEX-owned contracts are authoritative for deterministic implementation behavior.

Current scientific governance inputs:

1. `docs/scoring/hybrid_semantic_scoring_framework.md`
2. `docs/scoring/mathematical_scoring_framework.md`
3. `docs/conventions/evidence_semantics_and_tiers.md`
4. `docs/conventions/evidence_tiering.md`
5. `docs/design/semantic_scoring_framework.md`
6. `docs/data_ingestion/epi25_to_gsc.md`
7. `docs/data_ingestion/gtr_to_gsc.md`
8. `docs/data_ingestion/gtr_xml_parser_design.md`

When scientific desirability conflicts with deterministic implementation, the conflict must be documented before code changes.

Implementation precedence:

1. This system contract
2. Release manifest
3. Scoring profile config
4. Phenotype config
5. Source manifest
6. Source-specific scoring rule config
7. Scientific governance documents
8. Historical milestone maps and roadmap documents

---

## 3. System Role

GSC is the gene-level overlay layer in the broader portfolio ecosystem.

```text
VDB  → variant-centric evidence storage
GSC  → phenotype-scoped gene-level evidence overlay
RSP  → functional / transcriptomic evidence overlay
RDGP → sample-scoped gene prioritization and reasoning layer
VAP  → variant annotation and interpretation context consumer
```

GSC answers:

```text
For a selected phenotype, which genes have structured support across governed evidence sources, and what kinds of evidence support them?
```

GSC does not perform:

- variant calling
- variant interpretation
- sample-level prioritization
- RNA-seq differential expression
- enrichment analysis
- clinical diagnosis
- penetrance estimation
- pathogenicity probability estimation

---

### 3.1 Transitional Evidence Product (TEP) Role

GSC source artifacts remain the authoritative producer outputs.

GSC-TEP payloads are transport projections derived from those source artifacts.

GSC-TEP payloads must not be treated as replacement source truth.

GSC participates in the ecosystem as both:

```text
semantic prior producer

and

TEP producer
```

GSC-generated semantic prior evidence may be transported beyond repository boundaries through the GSC-TEP family.

GSC-TEP exists to preserve:

```text
phenotype context
semantic prior meaning
source attribution
semantic channel composition
aggregation topology
scoring context
release identity
provenance
uncertainty
future reinterpretability
```

during transport into persistence systems such as VDB.

GSC remains authoritative for:

```text
semantic prior generation
source aggregation
consensus scoring
semantic channel assignment
release generation
```

GSC-TEP remains authoritative for:

```text
transport identity
transport validation
source artifact manifests
payload preservation
```

GSC-TEP must not redefine GSC semantic meaning.

GSC-TEP requirements are governed by:

```text
docs/contracts/gsc_tep_contract.md
docs/design/gsc_tep_identity_model.md
docs/validation/gsc_tep_validation_strategy.md
docs/validation/gsc_tep_acceptance_criteria.md
```

---

## 4. Non-Negotiable Invariants

### 4.1 Phenotype Scope Invariant

Every GSC run is scoped to exactly one phenotype context.

Invalid behavior:

```text
single unscoped universal consensus score per gene
```

---

### 4.2 Core Evidence Record Invariant

The canonical gene-level evidence record is:

```text
(phenotype, gene_id)
```

If `gene_id` is unavailable, GSC may use `normalized_gene_symbol` as a provisional key, but unresolved identifiers must be flagged.

---

### 4.3 Non-Sample-Specific Invariant

GSC must not contain sample-specific fields such as:

- `sample_id`
- genotype
- zygosity
- patient-specific variant evidence
- RDGP ranking output

---

### 4.4 Variant Independence Invariant

GSC must not aggregate variant-level data into disease-gene claims unless a future governed adapter explicitly defines such behavior. ClinVar-derived future evidence must be transformed into phenotype-scoped gene-level clinical interpretation evidence using explicit rules.

---

### 4.5 Provenance Invariant

Every final gene record must be explainable by contributing sources.

At minimum, final outputs must preserve:

```text
phenotype
gene_id
gene_symbol
source_list
source_count
weighted_source_sum
consensus_score
evidence_semantics_summary
evidence_tier_summary
provenance_id
```

---

### 4.6 Semantic Separability Invariant

Evidence channels must remain separable.

No implementation may collapse all evidence into one irreversible score without preserving channel-specific components.

---

### 4.6.1 Semantic Preservation Invariant

When exported through GSC-TEP, semantic prior evidence must remain scientifically reconstructable.

At minimum, the following concepts must remain recoverable:

```text
phenotype context
gene identity
release identity
source attribution
semantic channel composition
scoring context
aggregation topology
provenance
uncertainty
```

GSC-TEP payloads must not collapse semantic prior evidence into:

```text
gene lists
membership flags
gene + score records
phenotype-neutral annotations
```

Future consumers must be able to determine:

```text
Why did this semantic prior exist?
```

without requiring access to the original GSC execution environment.

---

### 4.7 Determinism Invariant

Same config + same inputs + same code version must produce identical deterministic outputs, excluding intentional timestamps/logs.

Required:

- deterministic sorting
- explicit configs
- explicit source rules
- no hidden weights
- no free-text inference of modifiers
- stable output schemas
- reproducibility checks

---

## 5. Scoring Rollout Decision

GSC will use a **staged semantic rollout**.

### 5.1 Rationale

Immediate replacement of legacy scoring is not appropriate because:

- production outputs already depend on legacy `weighted_source_sum`
- semantic-channel scoring requires additional tests and fixtures
- source-specific rules for Epi25 and GTR require deterministic validation
- future ClinVar/OMIM/PanelApp behavior is not yet implemented
- downstream consumers benefit from backward-compatible columns

### 5.2 Transitional Dual-Scoring Architecture

During transition, GSC must preserve:

```text
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
```

Legacy behavior:

```text
consensus_score = weighted_source_sum
```

Semantic experimental behavior:

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

The active score model must be declared in the scoring profile.

### 5.3 Promotion Rule

Semantic scoring may become primary only in a release where:

```yaml
scoring:
  active_score: semantic_consensus_score
```

Until then, semantic scores are emitted as additional experimental columns.

---

## 6. Evidence Semantics and Tier Contract

### 6.1 Evidence Semantics

`evidence_semantics` answers:

```text
What kind of evidence is this?
```

Canonical v1 semantic channels:

| Semantic channel | Score column | Meaning |
|---|---|---|
| `direct_disease` | `direct_disease_score` | Direct human disease association |
| `clinical_interpretation` | `clinical_interpretation_score` | Curated clinical disease/variant interpretation |
| `contextual_biology` | `contextual_biology_score` | Biological localization/pathway context |
| `clinical_utilization` | `utilization_score` | Diagnostic testing utilization |
| `exploratory_literature` | `exploratory_score` | Candidate/literature aggregation support |
| `convergence` | `convergence_score` | Transcriptomic/network/proteomic/metabolomic convergence |

No new semantic channel may be added silently. A new channel requires:

- documented definition
- scoring column or mapping to existing channel
- cap
- source eligibility rules
- validation tests
- output schema update
- scoring profile version bump

### 6.2 Evidence Tiers

`evidence_tier` answers:

```text
How epistemically strong or reliable is this source or source-derived evidence class?
```

Canonical tiers:

| Tier | Default weight |
|---|---:|
| `platinum` | 4.0 |
| `gold` | 3.0 |
| `silver` | 1.5 |
| `bronze` | 0.75 |
| `annotation_only` | 0.0 |

`weight_tier` is legacy v1 scoring metadata and must not be treated as the canonical evidence-governance field after semantic scoring is activated.

### 6.3 Current Source Assignments

| Source / source-derived class | Semantic channel | Evidence tier |
|---|---|---|
| Epi25 exome-wide significant burden | `direct_disease` | `platinum` |
| Epi25 strong subthreshold | `direct_disease` | `gold` |
| Epi25 candidate support | `direct_disease` | `silver` |
| MitoCarta | `contextual_biology` | `gold` |
| GTR phenotype-scoped gene summary | `clinical_utilization` | `silver` |
| Genes4Epilepsy | `exploratory_literature` | `bronze` |

---

## 7. Scoring Config Architecture

### 7.1 Required Config Layers

Semantic scoring must be controlled by explicit configuration.

Required future files:

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

Release manifests must declare the active scoring profile:

```yaml
scoring:
  scoring_profile: config/scoring_profiles/epilepsy_semantic_v0.1.yaml
  active_score: weighted_source_sum
  emit_semantic_scores: true
```

### 7.2 Scoring Profile Required Fields

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
  platinum:
  gold:
  silver:
  bronze:
  annotation_only:

channel_caps:
  direct_disease_score:
  clinical_interpretation_score:
  contextual_biology_score:
  utilization_score:
  exploratory_score:
  convergence_score:

modifier_defaults:
  source_quality_modifier:
  phenotype_match_modifier:
  independence_modifier:

source_rules:
  - source_id:
    semantic_channel:
    evidence_tier:
    scoring_rule:
```

### 7.3 Modifier Resolution Strategy

For each source contribution, DEX must resolve modifiers in this precedence order:

1. source-specific scoring rule
2. phenotype-specific scoring profile
3. semantic channel default rule
4. global tier default
5. if unresolved: `annotation_only`

No modifier may be inferred from free text.

Required modifiers:

| Modifier | Default | Allowed values |
|---|---:|---|
| `source_quality_modifier` | 1.0 | configured enum or explicit numeric |
| `phenotype_match_modifier` | 1.0 | configured enum or explicit numeric |
| `independence_modifier` | 1.0 | configured enum or explicit numeric |

If a modifier cannot be resolved deterministically, the affected source contribution must be treated as `annotation_only` or fail validation, depending on profile strictness.

---

## 8. Semantic Scoring Calculation Contract

### 8.1 General Channel Formula

For semantic channel `c`:

```text
channel_score_c = min(channel_cap_c, normalized_evidence_sum_c)
```

where:

```text
normalized_evidence_sum_c =
    sum(source_weight_i × source_quality_modifier_i × phenotype_match_modifier_i × independence_modifier_i)
```

### 8.2 Conflict Penalty

Conflict penalties reduce `semantic_consensus_score` but must not erase raw evidence.

```text
semantic_consensus_score = max(
    0,
    sum(channel scores) - conflict_penalty
)
```

Conflict penalties must be source-attributed and explainable.

### 8.3 GTR Saturation Rule

GTR utilization must not accumulate linearly across repeated panel/test observations.

Default v1 GTR utilization formula:

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

Broad WES/WGS records must not inflate utilization scoring.

### 8.4 ClinVar Count Inflation Rule

Future ClinVar scoring must not sum all pathogenic variants linearly.

For v1 semantic scoring, ClinVar must contribute the maximum qualifying phenotype-matched assertion class per gene. Variant counts may be emitted as metadata only unless a future burden-specific ClinVar model is documented.

### 8.5 Epi25 Rule

Epi25 must be stratified by evidence class, phenotype stratum, and variant class.

Default classes:

| Epi25 evidence class | Score |
|---|---:|
| exomewide_significant | 4.0 |
| strong_subthreshold | 3.0 |
| candidate_signal | 1.5 |
| annotation_only_or_non_enriched | 0.0 |

Epi25 raw browser evidence must not be collapsed into one undifferentiated gene list.

---

## 9. Data Contracts

### 9.1 Phenotype Config Source Fields

Each source block must include or inherit:

```yaml
source_id:
source_name:
source_type:
adapter:
file_path:
gene_column:
source_weight:
weight_tier:        # legacy compatibility
evidence_semantics:
evidence_tier:
semantic_channel:
scoring_rule_id:
```

`semantic_channel` may be derived deterministically from `evidence_semantics` if the mapping is defined in the scoring profile.

### 9.2 Normalized Source Records

Required columns:

```text
phenotype
source_id
source_name
source_type
weight_tier
source_weight
evidence_semantics
evidence_tier
semantic_channel
source_row_number
input_gene_symbol
normalized_gene_symbol
gene_id
mapping_status
evidence_label
notes
source_record_hash
```

### 9.3 Gene Frequency Table

Required columns:

```text
phenotype
gene_id
gene_symbol
source_count
weighted_source_sum
source_list
weight_tier_summary
evidence_semantics_summary
evidence_tier_summary
semantic_channel_summary
mapping_status_summary
```

### 9.4 Scored Gene Evidence

Required transitional columns:

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
scoring_profile
active_score
score_explanation
```

### 9.5 Final Consensus Output

`results/tables/{phenotype}/consensus_gene_set.tsv` must include all columns from scored gene evidence plus:

```text
mapping_status_summary
provenance_id
run_id
gsc_version
generated_at
```

During transition, `consensus_score` remains backward-compatible unless the release declares `active_score: semantic_consensus_score`.

### 9.6 Provenance Table

Provenance rows must include:

```text
provenance_id
phenotype
gene_id
gene_symbol
source_id
source_name
source_type
source_weight
weight_tier
evidence_semantics
evidence_tier
semantic_channel
scoring_rule_id
input_gene_symbol
source_record_hash
run_id
```

---

## 10. Validation Contract

### 10.1 Config Validation

Validation must fail if:

- required scoring profile missing
- active score invalid
- source semantic channel invalid
- source evidence tier invalid
- source channel lacks cap
- modifier enum unknown
- scoring rule references unknown source
- new channel lacks output column
- semantic channel not mapped to score column

### 10.2 Output Validation

Validation must require:

- semantic score columns present when `emit_semantic_scores: true`
- `semantic_consensus_score` equals channel sum minus conflict penalty
- each channel score is less than or equal to its cap
- `consensus_score` equals the configured active score
- `evidence_semantics_summary` matches contributing source rows
- `evidence_tier_summary` matches contributing source rows
- provenance rows join back to consensus rows

### 10.3 Inflation Tests

Required test fixtures must verify:

```text
GTR + Genes4Epilepsy < Epi25 exome-wide
MitoCarta alone < MitoCarta + ClinVar/OMIM
Broad GTR WES/WGS does not increase utilization_score
ClinVar variant counts do not linearly inflate clinical_interpretation_score
Duplicate genes within one source do not inflate scores
```

### 10.4 Reproducibility Checks

Repeated runs must produce identical deterministic outputs for:

```text
normalized_source_records.tsv
gene_source_matrix.tsv
gene_frequency_table.tsv
scored_gene_evidence.tsv
consensus_gene_set.tsv
gene_provenance.tsv
```

Timestamped fields are excluded from checksum comparisons.

---

## 11. Compatibility and Migration

### 11.1 Backward Compatibility

The following legacy columns remain during transition:

```text
weighted_source_sum
weight_tier_summary
consensus_score
```

### 11.2 Deprecation Path

`weight_tier` is legacy scoring metadata.

Future releases should prefer:

```text
evidence_tier
semantic_channel
source_weight
```

`source_weight` remains useful as a configurable numeric scoring value, but its source must be explicit.

### 11.3 Production Safety

Production releases must remain untouched until:

- experimental semantic scoring passes validation
- expected-output fixtures are updated
- score behavior is reviewed on known genes
- README and method docs explain the scoring transition

---

## 12. Edge-Case Contract

GSC must explicitly handle:

| Edge case | Required behavior |
|---|---|
| Multiple weak evidence sources | cap by semantic channel; preserve source list |
| Broad GTR WES/WGS | raw evidence retained; score contribution 0 or annotation_only |
| ClinVar VUS-heavy evidence | annotation_only unless explicit rule says otherwise |
| Conflicting ClinVar assertions | visible conflict flag and optional penalty |
| MitoCarta in epilepsy profile | lower contextual score unless mitochondrial epilepsy profile selected |
| Epi25 subtype evidence in broad epilepsy | phenotype_match_modifier applies |
| Missing semantic config | fail or annotation_only, based on strictness |
| Unknown future channel | fail validation unless mapped to existing channel |
| Duplicate genes within source | collapse before scoring |
| Missing gene ID | flag; allow symbol fallback if configured |

---

## 13. Release Gate

Semantic scoring is implementation-ready when:

- scoring profile configs exist
- semantic columns propagate through all stages
- channel scores are emitted
- inflation tests pass
- reproducibility tests pass
- score explanations are generated
- GTR saturation is deterministic
- Epi25 stratified scoring is deterministic
- ClinVar future behavior is constrained by contract even before implementation

---

## 13.1 GSC-TEP Contract Integration

GSC-TEP construction is governed by the following repository-specific TEP artifacts:

```text
docs/contracts/gsc_tep_contract.md

docs/design/gsc_tep_identity_model.md

docs/validation/gsc_tep_validation_strategy.md

docs/validation/gsc_tep_acceptance_criteria.md
```

These documents define:

```text
transport requirements

identity preservation requirements

validation requirements

acceptance requirements
```

for GSC semantic prior transport.

### GSC-TEP Certification Requirement

A GSC-TEP must not be considered release-ready unless:

```text
identity preservation passes

phenotype preservation passes

source attribution preservation passes

semantic channel preservation passes

provenance preservation passes

uncertainty preservation passes

future reinterpretability passes
```

as defined by the GSC-TEP validation and acceptance framework.

### VDB Transport Readiness

A GSC release is considered transport-ready when:

```text
semantic prior evidence can be transported
without loss of scientific meaning
```

and satisfies all GSC-TEP certification requirements.

---

## 14. Contract Summary

GSC must remain:

```text
phenotype-scoped
gene-level
non-sample-specific
provenance-aware
semantically decomposed
tier-governed
deterministic
auditable
backward-compatible during transition
resistant to evidence inflation
```
