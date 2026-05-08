# Hybrid Semantic Scoring Framework for GSC (gene_set_consensus) repository

This document provides the scientific rationale for a hybrid semantic scoring system for GSC.

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

This document defines the scientific scoring philosophy used by GSC for integrating heterogeneous gene-level evidence sources into phenotype-scoped consensus evidence profiles.

The scoring framework exists to:

- preserve provenance
- separate evidence semantics from evidence strength
- prevent inappropriate evidence inflation
- support explainable downstream prioritization
- enable future extensibility across new evidence modalities

This framework is designed for:
- epilepsy
- mitochondrial disease
- future rare disease phenotypes

This framework is NOT intended to:
- provide clinical diagnosis
- assign pathogenicity
- replace expert review
- estimate penetrance
- estimate disease probability

---

## 2. Core Philosophical Principles

### 2.1 Evidence semantics are orthogonal to evidence strength

GSC distinguishes:

- `evidence_semantics`
- `evidence_tier`

#### `evidence_semantics`

Answers:

```text
What type of evidence is this?
```

Examples:

- statistical association
- clinical interpretation
- functional localization
- clinical utilization
- network convergence

#### `evidence_tier`

Answers:

```text
How reliable or authoritative is this evidence source?
```

Examples:

- platinum
- gold
- silver
- bronze

### 2.2 Different evidence types are NOT linearly equivalent

GSC explicitly rejects naïve additive scoring models where:

```text
multiple weak indirect signals
=
strong direct human disease evidence
```

Example:

```text
Genes4Epilepsy + GTR
≠
Epi25 exome-wide significant association
```

Different evidence modalities represent different epistemic claims and therefore cannot be treated as interchangeable additive units.

### 2.3 Evidence channels remain separable

All evidence contributions must remain decomposable into independent semantic channels.

GSC must preserve:

- raw evidence provenance
- channel-specific scoring
- source-level attribution

No irreversible score collapse is permitted.

---

## 3. Semantic Evidence Channels

### 3.1 `direct_disease_score`

Represents direct human disease association evidence.

Examples:

- Epi25 exome-wide significant burden
- replicated cohort-scale association

This is the strongest evidence channel in GSC.

### 3.2 `clinical_interpretation_score`

Represents curated clinical interpretation evidence.

Examples:

- ClinVar
- OMIM
- PanelApp
- HGMD-like resources

This channel reflects:

- expert interpretation
- clinical assertion
- curated disease-gene relationships

This channel does NOT necessarily imply:

- statistical causality
- unbiased evidence

### 3.3 `contextual_biology_score`

Represents biological context evidence.

Examples:

- MitoCarta
- pathway membership
- organelle localization
- protein complex membership

This channel reflects biological plausibility, NOT disease causality.

### 3.4 `utilization_score`

Represents clinical testing utilization evidence.

Examples:

- GTR panel membership
- diagnostic panel reuse

This channel reflects:

- laboratory behavior
- translational adoption
- clinical testing inclusion

This channel does NOT represent proof of disease association.

### 3.5 `exploratory_score`

Represents weak or exploratory literature aggregation evidence.

Examples:

- Genes4Epilepsy
- broad literature-derived candidate collections

This channel supports:

- hypothesis generation
- recall expansion

This channel should never dominate consensus scoring.

### 3.6 `convergence_score`

Represents systems-level functional convergence evidence.

Examples:

- transcriptomics
- network convergence
- metabolomics
- proteomics

This channel reflects functional support rather than direct causality.

---

## 4. Evidence Tier Definitions

| Tier            | Meaning                                             |
| --------------- | --------------------------------------------------- |
| platinum        | highest-confidence direct evidence                  |
| gold            | strong curated or experimentally supported evidence |
| silver          | moderate evidence or partially indirect evidence    |
| bronze          | exploratory or weak-support evidence                |
| annotation_only | retained for context but excluded from scoring      |

---

## 5. Default Tier Weights

| Tier            | Default Weight |
| --------------- | -------------: |
| platinum        |            4.0 |
| gold            |            3.0 |
| silver          |            1.5 |
| bronze          |           0.75 |
| annotation_only |            0.0 |


These weights are governance heuristics and NOT probabilistic estimates.

---

## 6. Channel Caps

To prevent inappropriate evidence inflation, each semantic channel has a maximum contribution cap.

| Channel                       | Maximum Contribution |
| ----------------------------- | -------------------: |
| direct_disease_score          |                  4.0 |
| clinical_interpretation_score |                  3.0 |
| contextual_biology_score      |                  2.0 |
| utilization_score             |                  1.0 |
| exploratory_score             |                 0.75 |
| convergence_score             |                  1.5 |


These caps are intended to preserve epistemic hierarchy between evidence classes.

---

## 7. Current Source Assignments

| Source                       | Semantic Channel         | Tier     |
| ---------------------------- | ------------------------ | -------- |
| Epi25 exome-wide significant | direct_disease_score     | platinum |
| Epi25 strong subthreshold    | direct_disease_score     | gold     |
| Epi25 candidate genes        | direct_disease_score     | silver   |
| MitoCarta                    | contextual_biology_score | gold     |
| GTR                          | utilization_score        | silver   |
| Genes4Epilepsy               | exploratory_score        | bronze   |


---

## 8. Source-Specific Rules

### 8.1 Epi25

Epi25 evidence must be stratified internally.

Not all Epi25-derived rows receive equal weight.

Recommended categories:

- exome-wide significant
- strong subthreshold
- candidate support

Exome-wide significant burden evidence represents the strongest current epilepsy evidence layer in GSC.

### 8.2 MitoCarta

MitoCarta reflects:

- localization
- mitochondrial biology
- pathway context

MitoCarta does NOT independently establish disease causality.

MitoCarta must remain confined to contextual biology scoring.

### 8.3 GTR

GTR reflects:

- diagnostic usage
- panel inclusion
- laboratory adoption

GTR does NOT represent:

- statistical association
- pathogenicity
- mechanistic proof

Broad WES/WGS tests should contribute little or no utilization score.

Utilization evidence must saturate rapidly and never dominate direct disease evidence.

### 8.4 Genes4Epilepsy

Genes4Epilepsy is exploratory literature aggregation evidence.

This source supports:

- candidate expansion
- recall sensitivity

This source should never independently elevate a gene to high-confidence disease relevance.

---

## 9. Source Independence Policy

GSC recognizes that many resources are not statistically independent.

Examples:

- GTR may derive from OMIM and ClinVar
- PanelApp may derive from OMIM and literature
- literature-derived resources may overlap extensively

Therefore:

- correlated evidence sources must not multiply confidence linearly
- weak overlapping evidence must not overpower direct evidence

Future scoring systems may incorporate explicit correlation penalties.

---

## 10. Annotation-Only Evidence

Some evidence sources may be retained for:

- metadata
- filtering
- explainability
- provenance

without contributing numerically to scoring.

Examples may include:

- VUS-heavy ClinVar entries
- broad GO terms
- broad WES panel inclusion

Such evidence should use:

`annotation_only`

---

## 11. Negative Evidence and Conflict Handling

GSC supports explicit uncertainty representation.

Potential negative or uncertainty-generating evidence includes:

- conflicting ClinVar assertions
- disputed disease associations
- failed replication studies
- contradictory convergence evidence

Future versions may apply explicit conflict penalties.

Current recommendation:

- preserve conflicts visibly
- avoid silent conflict resolution

---

## 12. Phenotype-Specific Scoring Profiles

Different phenotypes possess different evidence landscapes.

Examples:

- epilepsy has strong consortium-scale statistical genetics
- mitochondrial disease often relies more heavily on mechanistic and curated evidence

Therefore:

- scoring calibration may differ by phenotype
- scoring profiles should remain configurable

Examples:

- epilepsy_v1_profile
- mitochondrial_v1_profile

---

## 13. Explainability Requirements

All GSC scores must remain explainable.

A downstream consumer must be able to determine:

- which sources contributed
- which channels contributed
- why the gene scored highly
- what evidence classes dominate the score

Example:

```text
SCN1A
  direct_disease_score: 4.0
  clinical_interpretation_score: 2.5
  utilization_score: 0.8
  contextual_biology_score: 0.0
```

---

## 14. Recommended Future Semantic Channels

Future supported channels may include:

- expert_curation_score
- biochemical_phenotype_score
- animal_model_score
- experimental_function_score
- evolutionary_constraint_score
- predictive_model_score

This framework is intentionally extensible.

Future channels must not be added silently.

A future channel must either:

1. map into an existing v1 channel, or
2. require a new scoring profile version.

Adding a new scoring channel requires:
- channel definition
- cap
- source eligibility rules
- output column
- validation tests
- documentation update

---

## 15. Assumptions

- GSC operates at phenotype-scoped gene-level evidence integration.
- Scores represent evidence support, not disease probability.
- Evidence sources differ fundamentally in meaning and reliability.

---

## 16. Limitations

- Current weights are heuristic governance values.
- Scores are not statistically calibrated probabilities.
- Cross-phenotype score comparison may be invalid.
- Some future evidence sources may require additional semantic channels.

---

## 17. Edge Cases

Examples:

- strong localization but weak disease evidence
- high GTR utilization without strong causality
- conflicting clinical assertions
- sparse ultra-rare disease evidence
- convergence evidence without direct genetic support

---

## 18. Validation Strategy

Validation should include:

- known-gene recovery benchmarking
- ablation testing
- inflation testing
- reviewer explainability assessment
- cross-source consistency evaluation

---

## 19. Implementation Implications

DEX implementations should:

- preserve source provenance
- preserve channel separability
- avoid irreversible score collapse
- support phenotype-specific profiles
- support future evidence channels
- preserve raw evidence rows
- preserve conflict visibility

DEX should avoid:

- naïve additive scoring
- uncontrolled evidence accumulation
- hidden weighting logic
- irreversible normalization

---

## 20. Remaining Future Work (NOT blocking)

These can wait until later versions:

- empirical calibration
- Bayesian integration
- graph/network scoring
- probabilistic uncertainty propagation
- correlation-aware weighting
- phenotype transfer learning

Those are GSC v2/v3 concerns.

---

### 20.1 Future Assumptions

- GSC v1 prioritizes explainability and scientific defensibility over mathematically optimal ranking.
- DEX needs stable ontology and governance more urgently than perfect calibration.
- Future overlays (ClinVar, OMIM, transcriptomics) are expected.

### 20.2 Future Limitations

- Weight values remain heuristic.
- Final ranking behavior will require empirical testing.
- Some future evidence sources may require ontology expansion.

### 20.3 Future Validation Strategy

Before v1 stabilization:

- benchmark known epilepsy genes
- benchmark known mitochondrial disease genes
- perform ablation testing
- inspect score inflation behavior
- validate explainability with mock downstream RDGP outputs

### 20.4 Future Implementation Relevance

This draft should now be sufficient for DEX to:

- implement score channels
- implement schema
- preserve provenance
- build phenotype profiles
- stabilize scoring infrastructure

without needing another ontology redesign later.

---