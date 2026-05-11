# GSC Semantic Scoring Migration

## Purpose

This document describes the evolution of the Gene Set Consensus (GSC)
scoring architecture from early source-count aggregation toward the
current semantic ontology-driven framework.

The migration strategy intentionally preserves deterministic behavior
and backward compatibility while progressively introducing richer
scientific semantics.

---

# Phase 1 — Source Count Architecture

Early GSC prototypes used direct source overlap counts.

Example:

- gene appears in 3 sources
- consensus score = 3

Characteristics:

- deterministic
- simple
- reproducible

Limitations:

- no evidence quality differentiation
- no ontology
- no disease-specific prioritization
- broad clinical panels inflated scores

Representative configs:

- epilepsy_gold_bronze_registry_minimal.yaml

---

# Phase 2 — Weighted Tier Architecture

Second-generation scoring introduced weighted evidence tiers.

Example:

- gold = 3
- silver = 2
- bronze = 1

Characteristics:

- evidence weighting introduced
- more biologically meaningful ranking
- deterministic weighted aggregation

Limitations:

- tier labels overloaded multiple meanings
- ontology semantics still implicit
- utilization vs direct disease evidence not separated
- broad-panel inflation still partially unresolved

Representative configs:

- epilepsy_gold_bronze_registry.yaml
- epilepsy_gold_bronze.yaml

---

# Phase 3 — Semantic Ontology Architecture

Current-generation GSC introduces semantic evidence channels and
explicit ontology separation.

Core concepts:

- evidence semantics
- evidence tiers
- semantic channels
- utilization saturation
- inflation controls
- release-driven runtime configuration

Example semantic channels:

- direct_disease
- clinical_utilization
- contextual_biology
- exploratory_literature

Key scientific goals:

- suppress broad-panel inflation
- preserve disease-specific evidence priority
- separate contextual biology from direct causality
- preserve provenance and explainability
- maintain deterministic reproducibility

Representative configs:

- epilepsy_semantic_gtr_experimental.yaml
- mitochondrial_semantic_gtr_experimental.yaml

---

# Transitional Dual-Stack State

Current GSC remains in a transitional dual-stack state.

Legacy fields still exist:

- weight_tier
- weight_tier_summary
- weighted_source_sum

These fields remain active to preserve:

- backward compatibility
- historical reproducibility
- legacy release validation

However:

- semantic ontology is now authoritative
- semantic validation is enforced
- release-driven scoring profiles are preferred

---

# Future Direction

Planned future work includes:

- semantic-first phenotype naming
- eventual retirement of legacy weight-tier dependence
- expanded convergence scoring
- phenotype-specific semantic profiles
- noncoding semantic integration
- network convergence semantics
- ontology expansion governance

---

# Governance Principles

All future semantic expansion must preserve:

- deterministic execution
- reproducibility
- explainability
- provenance preservation
- ontology stability
- inflation resistance
- backward compatibility where reasonable
