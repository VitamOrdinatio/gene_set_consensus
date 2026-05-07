# Semantic-Aware Scoring Framework

## Purpose

This document records the emerging need for GSC to distinguish evidence magnitude from evidence meaning.

The current v1 scoring model is intentionally simple:

```text
consensus_score = weighted_source_sum
```

This is useful for deterministic early development, but experimental GTR integration revealed a key limitation:


```text
bronze exploratory evidence + silver clinical utilization evidence
```

can numerically equal:

```text
platinum statistical association evidence
```

even though these evidence combinations do not carry the same scientific meaning.

## Problem Observed During GTR Experimental Integration

The experimental epilepsy GTR release showed that:

```text
Genes4Epilepsy bronze weight = 1.0
GTR silver weight = 2.0
combined score = 3.0
```

which equals:

```text
Epi25 platinum-equivalent weight = 3.0 under the legacy v1 tier model
```

This is undesirable because:

```text
clinical utilization + exploratory literature support
```

should not automatically equal:

```text
high-confidence statistical association
```

## Core Principle

Evidence sources may be additive within a source type, but evidence semantics should remain interpretable.

See also:

`docs/conventions/evidence_semantics_and_tiers.md`

for formal governance definitions of:

- evidence semantics
- evidence confidence tiers
- semantic orthogonality

GSC should preserve distinctions among:

- statistical association
- clinical utilization
- functional localization
- clinical interpretation
- exploratory literature evidence

Evidence channels may exhibit biological or translational correlation.

For example:
- clinically utilized genes may also be statistically associated
- mitochondrial localization may enrich for mitochondrial disease association

However:

```text
correlation between evidence channels does not eliminate semantic distinction
```

GSC therefore preserves evidence semantics even when evidence channels partially overlap biologically.

## Evidence Semantics

Example evidence channels:

| Channel                 | Example Source | Interpretation                                    |
| ----------------------- | -------------- | ------------------------------------------------- |
| statistical_association | Epi25          | cohort-supported disease association              |
| clinical_utilization    | GTR            | real-world diagnostic testing usage               |
| functional_localization | MitoCarta      | mitochondrial localization evidence               |
| clinical_interpretation | future ClinVar | submitted variant interpretation evidence         |
| exploratory_literature  | Genes4Epilepsy | literature-derived or curated exploratory support |

## Why Simple Additive Scoring Is Insufficient

Simple additive scoring can cause weaker semantic evidence combinations to equal stronger evidence classes.

This creates interpretive ambiguity.

For example:

```text
bronze + silver = gold
```

is mathematically simple but biologically misleading.

## Candidate Future Scoring Approaches

### 1. Tier Reweighting

Reduce silver and bronze weights so they support but do not equal gold evidence.

Example:

| Tier | Candidate Weight |
|---|---|
| platinum | 4.0 |
| gold | 3.0 |
| silver | 1.0 |
| bronze | 0.5 |

Advantage:

- simple
- compatible with current model

Limitation:

- still compresses different evidence semantics into one scalar

### 2. Tier-Capped Scoring

Allow lower-tier evidence to contribute only up to a maximum cap unless supported by higher-tier evidence.

Example:

```text
bronze + silver may not exceed 2.5 without gold evidence
```

Advantage:

- prevents low/mid-tier inflation

Limitation:

- cap values require careful governance

### 3. Semantic Channel Scores

Maintain separate score columns for each evidence class.

Example:

| Column               | Meaning                            |
| -------------------- | ---------------------------------- |
| association_score    | statistical/cohort support         |
| utilization_score    | clinical testing utilization       |
| localization_score   | mitochondrial/pathway localization |
| interpretation_score | clinical variant interpretation    |
| exploratory_score    | literature/exploratory support     |

A final score may still be computed, but users can inspect the semantic composition.

Advantage:

- most interpretable
- best aligned with GSC architecture

Limitation:

- requires schema and downstream changes

### 4. Hybrid Score + Semantic Decomposition

Compute:

```text
consensus_score
```

while also preserving:

```text
association_score
utilization_score
localization_score
exploratory_score
```

This preserves backward compatibility while making the score interpretable.

This is likely the best future direction.

## Recommended Direction

GSC should eventually move toward:

```text
hybrid score + semantic decomposition
```

The v1 weighted score may remain useful as a deterministic support metric, but future experimental releases should expose semantic channel contributions.

## Interpretation Policy

GSC scores should not be interpreted as:

- pathogenicity probability
- penetrance
- causal certainty
- clinical actionability

Instead, scores represent structured evidence support within a configured phenotype and release context.

## Proposed Future Output Columns

Future consensus outputs may include:

- `consensus_score`
- `source_count`
- `weighted_source_sum`
- `association_score`
- `utilization_score`
- `localization_score`
- `clinical_interpretation_score`
- `exploratory_score`
- `evidence_semantics_summary`
- `weight_tier_summary`
- `source_list`

## Implementation Policy

Do not change production scoring behavior until:

- experimental scoring design is documented
- test fixtures are created
- existing release outputs remain reproducible
- semantic scoring outputs are validated separately

## Strategic Summary

GTR integration revealed that evidence semantics must be preserved during scoring.

The next GSC scoring generation should prevent:

```text
bronze + silver = gold
```

from being interpreted as equivalent scientific evidence.

The preferred long-term design is semantic-channel-aware scoring with backward-compatible consensus outputs.

---