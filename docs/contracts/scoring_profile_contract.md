# Scoring Profile Contract

## Purpose

This document defines the executable configuration contract for GSC semantic-channel scoring profiles.

It bridges SAGE-owned scientific scoring governance and DEX-owned deterministic implementation.

---

## Required Profile Location

Scoring profiles must live under:

```text
config/scoring_profiles/
```

Source-specific rules must live under:

```text
config/scoring_rules/
```

---

## Required Profile Schema

```yaml
profile:
  profile_id: epilepsy_semantic_v0.1
  phenotype_family: epilepsy
  version: v0.1
  active_score: weighted_source_sum
  emit_legacy_scores: true
  emit_semantic_scores: true
  strict_semantic_validation: true

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

semantic_channel_map:
  direct_disease: direct_disease_score
  clinical_interpretation: clinical_interpretation_score
  contextual_biology: contextual_biology_score
  clinical_utilization: utilization_score
  exploratory_literature: exploratory_score
  convergence: convergence_score

modifier_defaults:
  source_quality_modifier: 1.0
  phenotype_match_modifier: 1.0
  independence_modifier: 1.0

unknown_policy:
  unknown_semantic_channel: fail
  unknown_evidence_tier: fail
  missing_scoring_rule: annotation_only

source_rules:
  - source_id: epi25_2024_epi_high_confidence
    semantic_channel: direct_disease
    evidence_tier: platinum
    scoring_rule_id: epi25_exomewide_v0.1
```

---

## Valid `active_score` Values

Allowed:

```text
weighted_source_sum
semantic_consensus_score
```

During staged rollout, experimental profiles should use:

```yaml
active_score: weighted_source_sum
```

while emitting semantic columns.

---

## Required Validation

A scoring profile is valid only if:

- every tier has a numeric weight
- every channel has a cap
- every semantic channel maps to a score column
- every source rule uses known tier and channel names
- unknown policies are explicit
- profile ID and version are present
- `active_score` is valid

---

## Deterministic Modifier Rules

Modifier values must be:

- explicit numeric values, or
- configured enum labels resolved by lookup table

DEX must not infer modifiers from free text.

Default modifier values may be used only if allowed by the scoring profile.

---

## Output Contract

If `emit_semantic_scores: true`, the final consensus output must include:

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

---

## Governance Rule

Any new semantic channel requires:

- updated scoring profile
- updated output schema
- updated validation test
- updated documentation
- profile version bump

No silent channel expansion is allowed.
