# GSC Post-GTR Strategic Roadmap

## Overview

Once GTR integration is successfully incorporated into Gene Set Consensus (GSC), the project transitions from foundational infrastructure development into scientific expansion, evidence enrichment, and downstream systems integration.

At that stage, the core architectural framework of GSC will already include:

- deterministic execution
- provenance-aware releases
- canonical source registries
- source hydration
- identifier governance
- evidence tier semantics
- phenotype composition
- release validation
- scientific revision philosophy
- operator-oriented reproducibility

This means future work becomes progressively less about pipeline engineering and increasingly about scientific sophistication and translational utility.

---

# 1. Phenotype Expansion

## Goal

Expand GSC beyond epilepsy and mitochondrial disease into a reusable phenotype evidence engine.

## Future Phenotype Domains

Potential future phenotype universes include:

- leukodystrophy
- ataxia
- cardiomyopathy
- neuromuscular disease
- immunodeficiency
- mitochondrial depletion syndromes
- movement disorders
- rare metabolic disease
- autoinflammatory disease
- neurodevelopmental disorders

## Strategic Importance

This transforms GSC from:

```text
a disease-specific prototype
```

into:

```text
a generalized phenotype evidence infrastructure layer
```

usable across multiple downstream bioinformatics systems.

---

# 2. Smarter Evidence Integration

## Current State
Current consensus scoring is primarily based on:

- source overlap
- weighted aggregation
- deterministic source composition

## Future Direction

Future GSC versions may incorporate:

- ontology-aware weighting
- inheritance-aware scoring
- ClinVar-aware weighting
- OMIM integration
- HPO integration
- panel overlap density
- transcriptomic support
- pathway enrichment support
- network convergence support


## Strategic Importance

This evolves GSC from:

```text
evidence aggregation
```

toward:

```text
evidence reasoning
```

---

# 3. Transcriptomic Integration

## Goal

Integrate RNA-seq and enrichment-derived evidence into phenotype-aware gene prioritization.

## Potential Inputs

Future transcriptomic evidence may include:

- DEG convergence
- pathway enrichment overlap
- EBV-response signatures
- mitochondrial suppression signatures
- network convergence patterns
- GEO-derived enrichment landscapes

## Integration Target

This work would strongly interface with the future RSP (RNA-seq Pipeline) repository.

## Strategic Importance

Genes may eventually accumulate support from:

- consortium genetics
- GTR clinical testing
- literature evidence
- transcriptomic convergence
- pathway/network evidence

This significantly enriches prioritization depth.

---

# 4. VAP Integration

## Goal

Use GSC as a phenotype-aware prioritization overlay for variant interpretation workflows.

## Future Workflow

VAP may produce:

- coding variants
- splice variants
- noncoding variants
- candidate genes

GSC may then supply:

- phenotype-aware evidence overlays
- consensus-based prioritization
- cross-source evidence weighting

## Example

```text
Variant detected in SCN1A
+
SCN1A strongly supported by:
  - Epi25
  - GTR
  - literature
  - transcriptomic evidence
```

## Strategic Importance

This creates clinically meaningful variant prioritization infrastructure.

Especially important once:

- AlphaMissense
- SpliceAI
- AlphaGenome
- noncoding prioritization

are incorporated into VAP.

---

# 5. RDGP Integration

## Goal

Provide the gene-evidence substrate for future rare disease prioritization systems.

## Future RDGP Evidence Model

Potential future RDGP systems may integrate:

- patient phenotype evidence
- variant evidence
- gene consensus evidence
- transcriptomic evidence
- network evidence
- pathway evidence

## GSC Role

GSC becomes:

```text
the governed gene evidence layer
```

underlying higher-order prioritization systems.

## Strategic Importance

This is where provenance-aware scientific governance becomes critically important.

---

# Clinical Auditability and Release Governance

## Goal

Develop GSC into a release-aware scientific infrastructure platform.

## Current Governance Strengths

GSC already supports:

- timestamped acquisition
- release manifests
- deterministic execution
- source manifests
- planned vs active source governance
- scientific revision philosophy
- identifier provenance
- release validation

## Future Governance Directions

Potential future improvements include:

- source checksums
- formal release archives
- signed release manifests
- clinical audit exports
- provenance snapshots
- frozen historical rebuilds
- longitudinal release comparisons

## Strategic Importance

Many bioinformatics pipelines:

- mutate silently
- lack provenance
- are difficult to reproduce longitudinally

GSC is intentionally evolving toward:

```text
versioned scientific infrastructure
```

rather than:

```text
disposable analytical scripts
```

---

# Strategic Summary

Post-GTR GSC development is expected to shift from:

```text
building the infrastructure
```

toward:

```text
expanding scientific breadth
enriching evidence reasoning
integrating downstream systems
maturing governance
```

The current architectural direction strongly supports these future expansions.

---