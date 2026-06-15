# GSC-TEP Risk Assessment

## Scientific Failure Modes for GSC → VDB Preservation

Intended location: `docs/design/gsc_tep_risk_assessment.md`

---

## 1. Purpose

This document identifies scientific failure modes that could damage GSC evidence during transport into VDB through GSC-TEP.

For each risk, this document describes:

* failure mode
* scientific consequence
* impact on VDB discovery
* impact on future RDGP reasoning
* mitigation strategy

This document does not define implementation details.

---

## 2. Risk 1 — Loss of Phenotype Scope

### Failure Mode

GSC evidence is persisted as gene-level support without phenotype context.

Example:

```text
POLG = high support
```

instead of:

```text
POLG in mitochondrial_disease = high support
POLG in epilepsy = different support
```

### Scientific Consequence

A phenotype-scoped semantic prior becomes a phenotype-neutral gene claim.

This destroys the central GSC identity model.

### VDB Impact

VDB discovery cannot distinguish disease-specific overlays.

Phenotype-based query surfaces become misleading.

### RDGP Impact

RDGP may attach the wrong disease prior to a sample-gene row.

### Mitigation

Require phenotype context as part of preserved semantic prior identity.

---

## 3. Risk 2 — Score Flattening

### Failure Mode

GSC evidence is reduced to one score without preserving source, channel, or scoring profile context.

### Scientific Consequence

A downstream user cannot determine whether support came from:

* direct disease evidence
* clinical interpretation
* localization
* utilization
* exploratory literature

### VDB Impact

Discovery can retrieve a score but cannot characterize its meaning.

### RDGP Impact

RDGP may treat contextual evidence as equivalent to direct disease evidence.

### Mitigation

Preserve semantic channel composition, active scoring profile, weighted source sum, consensus score, and semantic consensus score.

---

## 4. Risk 3 — Loss of Semantic Channels

### Failure Mode

Semantic channels are discarded or collapsed into a single support value.

### Scientific Consequence

Evidence meaning is lost.

A gene with GTR + exploratory support may become indistinguishable from a gene with direct disease association.

### VDB Impact

VDB cannot expose evidence-type-aware query surfaces.

### RDGP Impact

RDGP loses the ability to distinguish high-confidence disease priors from weaker contextual priors.

### Mitigation

Preserve channel-specific evidence contributions and channel summaries.

---

## 5. Risk 4 — Loss of Source Multiplicity

### Failure Mode

Only final gene rows survive, while source contributions disappear.

### Scientific Consequence

Future users cannot distinguish:

* single-source support
* multi-source support
* correlated-source support
* direct versus indirect source support

### VDB Impact

Discovery cannot characterize evidence provenance or source diversity.

### RDGP Impact

RDGP confidence explanations become weaker and less auditable.

### Mitigation

Preserve source list, source count, source tiers, source semantics, and source contribution state.

---

## 6. Risk 5 — Loss of Provenance

### Failure Mode

The transported prior lacks source artifact lineage, release provenance, scoring provenance, or aggregation provenance.

### Scientific Consequence

The prior becomes difficult to trust, audit, reproduce, or reinterpret.

### VDB Impact

VDB cannot reconstruct why evidence was persisted or where it came from.

### RDGP Impact

RDGP explanations may cite GSC support without traceable basis.

### Mitigation

Preserve source artifact manifest, release identity, scoring profile, source attribution, and provenance identifiers.

---

## 7. Risk 6 — Ontology Collapse

### Failure Mode

Phenotype labels, gene identifiers, and source identifiers are normalized destructively.

Example:

```text
source_gene_symbol is replaced by canonical_gene_id
```

### Scientific Consequence

Original GSC-submitted identity is lost.

Ambiguity and historical mapping context disappear.

### VDB Impact

Namespace brokerage becomes mutation rather than additive normalization.

### RDGP Impact

RDGP may consume apparently clean identities that hide unresolved or ambiguous mappings.

### Mitigation

Require additive normalization. Preserve source identities, canonical identities, mapping status, and resolution uncertainty.

---

## 8. Risk 7 — Identity Collapse

### Failure Mode

Distinct identity spaces are merged.

Examples:

* GSC `(phenotype, gene)` identity collapsed into RDGP `(sample, gene)`
* GSC release identity collapsed into generic run ID
* source package identity collapsed into TEP ID

### Scientific Consequence

Repository-owned meanings become indistinguishable.

### VDB Impact

Discovery and brokerage cannot preserve layer boundaries.

### RDGP Impact

RDGP may confuse semantic priors with sample-specific variant evidence.

### Mitigation

Preserve identity-space independence:

* GSC biological identity
* GSC release identity
* TEP transport identity
* VDB canonical identity
* RDGP sample-gene identity

---

## 9. Risk 8 — Release Ambiguity

### Failure Mode

GSC release identity is omitted or treated as optional metadata.

### Scientific Consequence

Historical semantic priors cannot be reproduced.

The same phenotype-gene row may differ across releases.

### VDB Impact

VDB cannot persist multiple historical overlays coherently.

### RDGP Impact

RDGP cannot explain which GSC release supported a prior analysis.

### Mitigation

Treat `gsc_release_id` as required identity context for GSC-TEP.

---

## 10. Risk 9 — Hidden Uncertainty

### Failure Mode

Missing, zero, unresolved, ambiguous, no-match, and not-applicable values are collapsed.

### Scientific Consequence

Uncertainty becomes invisible.

Absence may be misread as negative evidence.

### VDB Impact

Discovery cannot characterize null semantics.

### RDGP Impact

RDGP may reason incorrectly from missing or unresolved evidence.

### Mitigation

Preserve explicit uncertainty states and null semantics.

---

## 11. Risk 10 — Binary Membership Reduction

### Failure Mode

GSC semantic priors are transported as simple membership flags.

Example:

```text
gene in epilepsy_set = true
```

### Scientific Consequence

The semantic richness of GSC is destroyed.

Scores, channels, source multiplicity, provenance, and uncertainty vanish.

### VDB Impact

VDB can only answer primitive membership queries.

### RDGP Impact

RDGP receives thin priors that cannot support explainable reasoning.

### Mitigation

Preserve score, source, semantic channel, provenance, release, and phenotype context.

---

## 12. Risk 11 — VDB Reinterpretation of GSC Meaning

### Failure Mode

VDB recomputes, modifies, or reclassifies GSC semantic priors as if VDB owns their meaning.

### Scientific Consequence

Producer semantic authority is violated.

GSC truth becomes VDB-derived truth.

### VDB Impact

Authority boundaries drift.

### RDGP Impact

RDGP may unknowingly consume altered priors.

### Mitigation

VDB may broker and persist GSC priors, but must not recompute or redefine them.

---

## 13. Risk 12 — Loss of Future Reinterpretability

### Failure Mode

Only currently useful summaries are preserved.

### Scientific Consequence

Future scoring models, ontology changes, or source reevaluations cannot be applied.

### VDB Impact

Semantic persistence becomes archival storage rather than future-proof preservation.

### RDGP Impact

Future RDGP versions cannot take advantage of richer historical evidence.

### Mitigation

Preserve source-level and channel-level context, not only final summaries.

---

## 14. Risk 13 — Payload Homogenization

### Failure Mode

GSC-TEP is forced to resemble VAP-TEP, RSP-TEP, or generic evidence payloads.

### Scientific Consequence

GSC’s semantic-prior nature is lost.

### VDB Impact

VDB cannot learn from structurally distinct producer TEPs.

### RDGP Impact

RDGP may receive evidence stripped of semantic-prior context.

### Mitigation

Respect heterogeneous TEP-family doctrine. GSC-TEP should preserve GSC-specific semantic prior cargo.

---

## 15. Risk 14 — Loss of Aggregation Topology

### Failure Mode

The relationships among phenotype, gene, source, score, channel, and release are discarded.

### Scientific Consequence

Consensus rationale is lost.

### VDB Impact

Discovery cannot reconstruct evidence topology.

### RDGP Impact

RDGP explanations become shallow and less trustworthy.

### Mitigation

Preserve aggregation topology and source contribution relationships.

---

## 16. Risk 15 — Treating GSC as Raw Evidence

### Failure Mode

GSC priors are persisted as raw biological observations.

### Scientific Consequence

The distinction between observed evidence and semantic prior evidence is erased.

### VDB Impact

Persistence domains become conceptually confused.

### RDGP Impact

RDGP may overvalue GSC as direct observation rather than prior knowledge.

### Mitigation

Classify GSC outputs as semantic prior evidence / phenotype-scoped semantic overlays.

---

## 17. Summary Risk Table

| Risk                    | Primary Damage           | Mitigation                    |
| ----------------------- | ------------------------ | ----------------------------- |
| Loss of phenotype scope | Wrong biological context | Preserve phenotype identity   |
| Score flattening        | Evidence meaning loss    | Preserve channels and profile |
| Source loss             | No audit trail           | Preserve source attribution   |
| Provenance loss         | Irreproducibility        | Preserve artifact lineage     |
| Ontology collapse       | Identity corruption      | Additive normalization        |
| Release ambiguity       | Historical loss          | Preserve `gsc_release_id`     |
| Hidden uncertainty      | False certainty          | Preserve null semantics       |
| Binary reduction        | Loss of semantic prior   | Preserve rich payload         |
| VDB reinterpretation    | Authority drift          | Preserve producer authority   |
| Topology loss           | No rationale             | Preserve relationships        |

---

## 18. Scientific Risk Conclusion

A GSC-TEP fails scientifically if it can move data while losing meaning.

Transport success is not enough.

A valid GSC-TEP must preserve:

* semantic prior identity
* phenotype scope
* release context
* source attribution
* scoring context
* semantic channels
* uncertainty
* topology
* future reinterpretability

Only then can VDB preserve GSC evidence as durable ecosystem knowledge rather than as flattened annotation.
