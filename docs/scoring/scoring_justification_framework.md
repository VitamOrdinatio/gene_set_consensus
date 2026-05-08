# Scoring Justification Framework
## gene_set_consensus (GSC) repository

---

## 1. Purpose

This document explains the scientific rationale behind the scoring weights, semantic-channel hierarchy, modifiers, caps, and defensive mathematical behavior used in the GSC hybrid semantic scoring architecture.

This document exists to:

- justify scoring philosophy
- support explainability
- support scientific review
- support future governance discussions
- support interview and reviewer defense
- explain why specific scoring choices were made

This document is NOT:

- a statistical calibration framework
- a probabilistic disease model
- a clinical interpretation guideline

The scoring system is designed to produce:

```text
deterministic, provenance-aware, explainable evidence-support scores
```

rather than:

- pathogenicity probabilities
- disease risk estimates
- penetrance estimates
- clinical actionability predictions

---

## 2. Core Philosophy

The GSC scoring system is intentionally:

- conservative
- explainable
- monotonic
- deterministic
- provenance-preserving
- resistant to weak-evidence inflation

The scoring framework is built around the following principle:

```text
Different evidence modalities answer different scientific questions.
```

Therefore:

```text
different evidence types are NOT linearly interchangeable.
```

---

## 3. Why Hybrid Semantic Scoring Was Needed

The original weighted-source model risked allowing:

```text
multiple weak indirect signals
=
strong direct disease evidence
```

Example:

```text
Genes4Epilepsy + GTR
≈
Epi25 exome-wide significant association
```

Scientifically, this is inappropriate because:

- exploratory literature aggregation
- clinical utilization
- pathway membership
- localization evidence

do not represent the same epistemic claim as:

```text
direct replicated human disease association
```

Therefore, GSC evolved toward:

```text
hybrid semantic-channel scoring
```

where:

- evidence types remain separated
- evidence classes receive bounded influence
- indirect evidence cannot dominate direct evidence

---

## 4. Tier Weight Justification

### 4.1 Tier Weights

| Tier            | Weight |
| --------------- | -----: |
| platinum        |    4.0 |
| gold            |    3.0 |
| silver          |    1.5 |
| bronze          |   0.75 |
| annotation_only |    0.0 |


### 4.2 Why These Numbers Were Chosen

The weights are intentionally simple and hierarchical.

The framework uses approximate halving relationships:

```text
gold ≈ 2 × silver
silver ≈ 2 × bronze
```

This structure provides:

- interpretability
- deterministic scaling
- intuitive hierarchy
- resistance to uncontrolled accumulation

The numbers were NOT chosen to imply:

- probabilities
- odds ratios
- likelihood ratios
- Bayesian posterior estimates

Instead, they represent:

```text
relative evidence-support strength
```

### 4.3 Why Platinum = 4.0

Platinum represents the strongest direct human disease evidence.

The value `4.0` was intentionally chosen so that:

```text
strong direct evidence
>
multiple weak indirect evidence sources combined
```

Example:

```text
GTR max contribution = 1.0
Genes4Epilepsy max contribution = 0.75

combined = 1.75
```

This ensures:

```text
GTR + exploratory literature
cannot numerically equal
direct exome-wide significant disease association
```

This was one of the primary scientific goals of the redesign.

### 4.4 Why Gold = 3.0

Gold represents:

- strong curated evidence
- strong biological evidence
- strong but indirect support
- clinically important evidence

Gold was intentionally placed below platinum because:

- curated evidence can be circular
- biological evidence may not imply causality
- expert assertions may inherit prior assumptions

Gold remains highly influential, but cannot independently overpower direct statistical disease evidence.

### 4.5 Why Silver = 1.5

Silver represents:

- moderate support
- partially indirect support
- candidate-level support
- moderate confidence

Silver was intentionally set at half of gold to preserve strong evidence separation.

This ensures:

- moderate evidence helps
- moderate evidence does not dominate
- multiple silver sources are required before approaching - high-confidence support

### 4.6 Why Bronze = 0.75

Bronze represents:

- exploratory support
- literature aggregation
- weak candidate support
- hypothesis-generation evidence

Bronze was intentionally chosen as half of silver.

This ensures:

- exploratory evidence contributes
- exploratory evidence cannot dominate
- literature-derived candidate collections remain useful without becoming overpowered

### 4.7 Why Annotation-Only = 0.0

Some evidence is useful for:

- metadata
- provenance
- explainability
- filtering

without representing positive support.

Examples:

- VUS-heavy ClinVar entries
- broad GO categories
- broad WES inclusion
- weak pathway membership

Such evidence should remain visible without inflating scores.

---

## 5. Channel Cap Justification

### 5.1 Channel Caps

| Channel                       |  Cap |
| ----------------------------- | ---: |
| direct_disease_score          |  4.0 |
| clinical_interpretation_score |  3.0 |
| contextual_biology_score      |  2.0 |
| utilization_score             |  1.0 |
| exploratory_score             | 0.75 |
| convergence_score             |  1.5 |


### 5.2 Why Caps Exist

Caps exist to preserve:

```text
epistemic hierarchy
```

The framework intentionally prevents:

- unlimited evidence accumulation
- repeated weak-source inflation
- correlated-source explosion
- pathway inflation
- panel-count inflation

Without caps:

- large panel datasets
- large literature collections
- heavily studied genes

could dominate scoring improperly.

---

## 6. Why Direct Disease Evidence Dominates

The framework intentionally prioritizes:

```text
direct human disease association
```

over:

- localization
- pathways
- panel inclusion
- exploratory literature
- downstream transcriptomic changes

This reflects a core scientific principle:

```text
direct replicated human disease evidence
is stronger than indirect biological plausibility.
```

---

## 7. Why Clinical Interpretation Is Strong but Capped

Clinical interpretation resources such as:

- ClinVar
- OMIM
- PanelApp

contain valuable expert knowledge.

However:

- they may inherit prior literature assumptions
- they may exhibit curation circularity
- they may contain conflicting assertions
- they may reflect variant-level rather than gene-level evidence

Therefore:

```text
clinical interpretation evidence is strong 
but is not unconstrained
```

---

## 8. Why MitoCarta Was Treated as Contextual Biology

MitoCarta is high-quality biological evidence for:

- mitochondrial localization
- mitochondrial pathway relevance
- mitochondrial systems biology

However:

```text
mitochondrial localization
≠
mitochondrial disease causality
```

Therefore:

```text
MitoCarta receives a strong contextual score, 
but also does not enter direct disease scoring
```

This distinction prevents:

```text
mitochondrial guilt by localization
```

---

## 9. Why GTR Was Capped at 1.0

GTR reflects:

- diagnostic usage
- clinical panel inclusion
- translational adoption

However:

```text
clinical testing utilization
≠
causal disease evidence
```

GTR is susceptible to:

- broad panels
- historical inertia
- commercial testing strategy
- inherited panel assumptions
- exploratory inclusion

Therefore:

```text
GTR contributes positively 
but weakly and with rapid saturation
```

---

## 10. Why Logarithmic Saturation Was Chosen

Repeated evidence observations should not scale linearly.

Example:

```text
a gene in 100 panels
is not 100× stronger
than a gene in 1 targeted phenotype-specific panel
```

Therefore:

- repeated observations use diminishing returns
- evidence saturates quickly
- early support matters most

This prevents:

- panel inflation
- literature inflation
- overrepresentation bias

---

## 11. Why Modifiers Use Quarter-Step Scaling

The modifier system uses:

| Modifier | Meaning               |
| -------- | --------------------- |
| 1.0      | full applicability    |
| 0.75     | strong but imperfect  |
| 0.5      | partial applicability |
| 0.25     | weak/ambiguous        |
| 0.0      | not applicable        |

This approach was chosen because it:

- avoids fake precision
- remains interpretable
- remains deterministic
- remains configurable
- is easy to audit

The modifiers are intentionally coarse-grained.

---

## 12. Why ClinVar Uses Maximum Assertion Rather Than Variant Counts

Large genes or heavily studied genes may accumulate many ClinVar submissions.

If variant counts were summed linearly:

- large genes would inflate artificially
- heavily tested genes would dominate
- submission behavior would masquerade as biological truth

Therefore:

```text
ClinVar scoring uses
maximum qualifying phenotype-matched assertion class
```

rather than:

- raw pathogenic variant count
- raw submission count

unless a future calibrated burden model is developed.

---

## 13. Why Transcriptomics and Network Evidence Were Limited

Transcriptomic convergence and network convergence are biologically meaningful.

However:

```text
differential expression
≠
causal disease mechanism
```

Many transcriptomic changes may represent:

- downstream consequences
- stress responses
- secondary adaptations

Therefore:

```text
convergence evidence contributes moderately
but remains below direct disease evidence
```

---

## 14. Why Conflict Penalties Exist

The framework intentionally preserves:

- uncertainty
- disagreement
- contradictory evidence

Examples:

- conflicting ClinVar assertions
- failed replication studies
- disputed disease genes

Without conflict penalties:

- positive evidence accumulation becomes biased
- contradictory evidence disappears silently

```text
The framework therefore prefers 
visible uncertainty rather than 
silent conflict resolution and 
forced binary classification
```

---

## 15. Why the Framework Is Deterministic Rather Than Probabilistic

The framework intentionally prioritizes:

- reproducibility
- interpretability
- explainability
- provenance

over:

- mathematically optimal inference

This was chosen because:

- source evidence is heterogeneous
- source independence is imperfect
- many evidence types are non-calibrated
- causal priors are unknown

Therefore:
- deterministic governance is safer for GSC v1
- probabilistic inference is deferred to future versions

---

## 16. Future Evolution

The framework is intentionally extensible.

Future versions may introduce:

- Bayesian integration
- empirical calibration
- graph propagation
- ontology-aware penalties
- probabilistic uncertainty propagation
- correlation-aware weighting

These are considered:

- v2/v3 concerns
- nonblocking for GSC v1

---

## 17. Interview / Reviewer Explanation

A concise explanation of the framework is:

```text
The scoring framework was designed as a deterministic, provenance-aware evidence-support model rather than a probabilistic disease model.

Direct human disease evidence receives the strongest support.

Curated clinical interpretation and biological context are important but capped because they answer different scientific questions.

Clinical utilization and exploratory literature contribute weakly because they are susceptible to ascertainment bias, circularity, and evidence inflation.

The framework prioritizes explainability, semantic separation, and resistance to weak-evidence accumulation.
```

---

## 18. Assumptions

- Evidence sources differ fundamentally in meaning.
- Direct disease evidence should dominate indirect evidence.
- Many biomedical resources are correlated rather than independent.
- GSC v1 prioritizes deterministic explainability over probabilistic modeling.

---

## 19. Limitations

- Current weights are heuristic.
- Scores are not calibrated probabilities.
- Source-independence modifiers remain approximate.
- Different phenotypes may eventually require calibration adjustment.
- Future empirical testing may justify weight refinement.

---

## 20. Edge Cases

Examples:

- heavily studied genes
- large genes with many ClinVar submissions
- broad panel inflation
- localization without causality
- transcriptomic downstream effects
- ultra-rare disease genes with sparse evidence
- conflicting expert assertions

---

## 21. Validation Strategy

Validation should include:

- known-gene recovery benchmarking
- inflation testing
- ablation testing
- explainability inspection
- phenotype-specific ranking inspection
- conflict-behavior inspection

Particular attention should be paid to ensuring:

```text
weak correlated evidence
does not overpower
strong direct evidence
```

---

## 22. Implementation Relevance

This justification framework exists to support:

- DEX implementation planning
- scoring-contract development
- future governance refinement
- scientific explainability
- reviewer defense
- interview discussion
- future extensibility planning

This document should be read alongside:

`hybrid_semantic_scoring_framework.md`
`mathematical_scoring_framework.md`

---