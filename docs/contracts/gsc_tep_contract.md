# GSC-TEP Contract

## Draft Status

Draft v0.1 for DEX-GSC implementation planning.

## Purpose

This contract defines deterministic implementation requirements for constructing GSC-TEP, the Transitional Evidence Product family responsible for transporting Gene Set Consensus (GSC) semantic prior evidence into downstream ecosystem systems such as VDB.

This document converts the GSC scientific-preservation package into implementation-facing contract language.

GSC-TEP exists to preserve:

```text
phenotype-scoped semantic prior meaning
source attribution
semantic channel composition
aggregation topology
scoring context
release identity
provenance
uncertainty
future reinterpretability
```

GSC-TEP must not reduce GSC outputs to:

```text
gene lists
binary membership flags
phenotype-neutral annotations
opaque score exports
flattened source summaries
```

The goal is not merely transport.

The goal is durable preservation of semantic prior meaning across repository boundaries.

---

## Scope

This contract applies to GSC-TEP construction, validation, and future VDB intake preparation.

This contract defines:

* producer authority boundaries
* transport identity requirements
* payload preservation requirements
* source artifact manifest requirements
* provenance requirements
* uncertainty requirements
* semantic channel requirements
* topology preservation requirements
* validation expectations
* implementation non-goals

This contract does not define:

* final JSON schema
* SQL schema
* VDB table structure
* GSC scoring algorithms
* RDGP prioritization logic
* phenotype ontology implementation
* physical storage layout

Those concerns belong to downstream implementation specifications.

---

## Authority Boundaries

### GSC Authority

GSC remains authoritative for:

```text
semantic prior meaning
phenotype-scoped evidence aggregation
source weighting
consensus scoring
semantic channel assignment
release generation
source attribution
```

GSC-TEP construction must preserve GSC-owned meaning.

GSC-TEP must not transfer semantic authority from GSC to VDB.

---

### TEP Authority

TEP provides transport governance.

TEP owns:

```text
transport identity
envelope semantics
sleeve versioning
source artifact manifest structure
transport validation state
```

TEP does not replace GSC biological identity.

TEP does not replace GSC release identity.

TEP does not replace GSC source artifacts.

---

### VDB Authority

VDB owns:

```text
discovery
validation
namespace brokerage
semantic persistence
query-surface exposure
```

VDB may broker and persist GSC evidence.

VDB must not recompute, reinterpret, or redefine GSC semantic priors.

---

### RDGP Authority

RDGP may consume VDB-preserved GSC priors as phenotype-level support during sample-gene reasoning.

RDGP must not treat GSC priors as sample-specific variant evidence.

---

## Core Contract Principle

A valid GSC-TEP SHALL preserve GSC semantic priors as:

```text
release-scoped
phenotype-scoped
gene-associated
source-attributed
channel-aware
provenance-rich
uncertainty-preserving
future-reinterpretable
semantic evidence states
```

A valid GSC-TEP SHALL NOT preserve GSC evidence merely as:

```text
gene_id + score
gene_symbol + membership
phenotype + gene flag
```

---

## Evidence Class

The primary evidence class transported by GSC-TEP is:

```text
Phenotype-Scoped Semantic Prior Evidence
```

This evidence class is distinct from:

```text
VAP observed variant evidence
RSP transcriptomic evidence
RDGP reasoning evidence
VDB brokered persistence entities
```

GSC-TEP payloads must explicitly preserve this evidence-class identity.

---

## Core Biological Identity

The core GSC biological identity is:

```text
(phenotype, gene)
```

The release-scoped semantic prior identity is:

```text
(gsc_release_id, phenotype, gene)
```

After VDB namespace brokerage, the persisted overlay identity may become:

```text
(gsc_release_id, phenotype, canonical_gene_id)
```

However, canonical identity assignment is additive and must not erase GSC-submitted identity.

---

## Transport Identity Requirements

GSC-TEP must preserve the distinction among the following identity classes.

### TEP Identity

```text
tep_id
```

Identifies the transport object.

It does not replace GSC biological identity.

---

### TEP Type

```text
tep_type = gsc_tep
```

Identifies the TEP family.

---

### TEP Schema Version

```text
tep_schema_version
```

Identifies the governing structural specification.

---

### TEP Sleeve Version

```text
tep_sleeve_version
```

Identifies the GSC-owned semantic projection layer used to construct the payload.

---

### Source Repository

```text
source_repository = gene_set_consensus
```

Identifies GSC as the evidence producer.

---

### Source Package Identity

```text
source_package_id = gsc_release_id
```

For GSC, the producer package is a release-scoped semantic prior package.

`gsc_release_id` must not be replaced by generic `run_id`.

---

### Source Identity Scope

GSC-TEP must declare its producer-owned identity scope as:

```text
gsc_release_id + phenotype + gene identity
```

This identifies the semantic prior identity represented in the payload.

---

## Required Envelope Fields

Every GSC-TEP envelope SHALL preserve:

```text
tep_id
tep_type
tep_schema_version
tep_sleeve_version
source_repository
source_package_id
source_identity_scope
source_artifact_manifest
creation_timestamp
validation_state
provenance
```

Envelope metadata must be sufficient to determine:

```text
what object was transported
who produced it
which producer package generated it
which sleeve created it
which source artifacts contributed
whether validation occurred
```

---

## Required Source Artifact Manifest

Every GSC-TEP SHALL include or reference a source artifact manifest.

The source artifact manifest SHALL preserve:

```text
artifact_id
artifact_type
artifact_path_or_reference
artifact_checksum_if_available
source_repository
source_package_id
contributing_fields
field_lineage
semantic_role
producer_ownership
```

The manifest must support reconstruction of which GSC artifacts contributed to the transported semantic prior evidence.

The source artifact manifest must not be treated as optional metadata.

It is part of the preservation contract.

---

## Required Payload Entities

A GSC-TEP payload SHALL preserve the following conceptual entities.

These are conceptual implementation requirements, not mandatory physical table names.

### 1. Semantic Prior Entity

Represents the core phenotype-scoped evidence-supported gene prior.

Required meaning:

```text
gene has GSC-generated semantic support for phenotype
within a specific release and scoring context
```

Required fields or recoverable concepts:

```text
gsc_release_id
phenotype_id_or_label
source_gene_id
source_gene_symbol
consensus_score
semantic_consensus_score
active_score
scoring_profile
semantic_channel_summary
source_list
uncertainty_state
```

---

### 2. Phenotype Entity

Preserves the phenotype context in which the prior is meaningful.

Required concepts:

```text
phenotype_id
phenotype_label
phenotype_namespace_if_available
phenotype_profile_or_scope
phenotype_version_or_context_if_available
```

Phenotype context must never be dropped.

---

### 3. Gene Identity Entity

Preserves GSC-submitted gene identity.

Required concepts:

```text
source_gene_symbol
source_gene_id
source_namespace
gsc_gene_symbol
gsc_mapping_status
unresolved_or_ambiguous_state
```

Canonical VDB identity may be added later, but source identity must remain recoverable.

---

### 4. Release Entity

Preserves the semantic prior package identity.

Required concepts:

```text
gsc_release_id
gsc_version
release_label
source_package_identity
source_release_identifiers
gsc_run_id_if_available
generation_context
```

Release identity is part of semantic prior identity.

It is not optional metadata.

---

### 5. Score Entity

Preserves quantitative evidence support.

Required concepts:

```text
consensus_score
semantic_consensus_score
weighted_source_sum
active_score
source_count
score_interpretation_context
score_nullability_state
```

Scores must remain attached to scoring profile and source context.

---

### 6. Scoring Profile Entity

Preserves how scores should be interpreted.

Required concepts:

```text
scoring_profile_name
scoring_profile_version
scoring_framework
active_scoring_mode
semantic_channel_model
score_interpretation_assumptions
```

A score without a scoring profile is not sufficient.

---

### 7. Semantic Channel Entity

Preserves the composition of evidence meaning.

Required concepts:

```text
channel_name
channel_type
channel_state
channel_contribution
channel_scoring_activity
channel_uncertainty
```

Allowed or expected channel states include:

```text
scoring_active
annotation_only
absent
unknown
not_applicable
conflict
```

Semantic channels must not be collapsed into a single support score.

---

### 8. Source Contribution Entity

Preserves source-level evidence support.

Required concepts:

```text
source_id
source_name
source_type
source_tier
source_semantics
source_release
source_contributed_to_score
source_contribution_class
source_artifact_reference
source_provenance_context
```

Source multiplicity must remain visible.

---

### 9. Provenance Entity

Preserves origin and transformation context.

Required concepts:

```text
source_artifact_provenance
gsc_release_provenance
aggregation_provenance
scoring_provenance
rule_or_config_provenance
source_ownership
field_lineage_if_available
```

Provenance must permit future audit of why a semantic prior exists.

---

### 10. Aggregation Topology Entity

Preserves relationships that produced the consensus.

Required relationships:

```text
phenotype_to_gene
source_to_gene
source_to_phenotype
source_to_channel
source_to_score
release_to_prior
prior_to_provenance
```

A flattened final table alone is insufficient if these relationships cannot be reconstructed.

---

### 11. Uncertainty Entity

Preserves ambiguity, absence, and conflict.

Required states include:

```text
unknown
missing
unresolved
ambiguous
not_applicable
zero_support
no_match
conflict
annotation_only
```

Uncertainty must never be represented solely through omission.

---

### 12. Ontology Context Entity

Preserves phenotype and gene interpretation context.

Required or optional concepts:

```text
phenotype_namespace
phenotype_mapping_status
gene_namespace
gene_mapping_status
source_ontology_identifiers
ontology_version_or_context
```

Ontology context supports future reinterpretation.

---

## Preservation Guarantees

A valid GSC-TEP SHALL satisfy the following guarantees.

### Phenotype Preservation Guarantee

Every semantic prior must remain explicitly associated with its phenotype context.

A gene-level prior without phenotype context is invalid.

---

### Gene Identity Preservation Guarantee

GSC-submitted gene identity must remain recoverable even after downstream namespace brokerage.

Original source identity must not be overwritten.

---

### Release Preservation Guarantee

Every semantic prior must remain associated with the GSC release that generated it.

Release identity must remain part of prior identity.

---

### Source Attribution Preservation Guarantee

Every transported semantic prior must preserve source attribution sufficient to determine which evidence sources contributed.

---

### Semantic Channel Preservation Guarantee

Semantic evidence channels must remain recoverable after transport.

A transported prior containing only a single score fails this guarantee.

---

### Scoring Context Preservation Guarantee

Scores must remain attached to scoring profile, active scoring mode, and score interpretation context.

---

### Topology Preservation Guarantee

Relationships among phenotype, gene, source, channel, score, release, and provenance must remain reconstructable.

---

### Provenance Preservation Guarantee

A future consumer must be able to reconstruct where the evidence originated and how it was generated.

---

### Uncertainty Preservation Guarantee

Uncertainty states must remain explicit.

Missing, unknown, unresolved, ambiguous, not applicable, no match, zero support, conflict, and annotation-only states must not be collapsed.

---

### Future Reinterpretability Guarantee

A future consumer must be able to reinterpret preserved GSC semantic priors without requiring access to the original GSC execution environment.

---

## Namespace Brokerage Requirements

GSC-TEP SHALL preserve producer-submitted identities exactly as emitted or projected by the GSC sleeve.

VDB MAY add canonical identities during intake.

VDB MUST perform namespace brokerage additively.

GSC-TEP construction SHALL support downstream brokerage by preserving:

```text
source_gene_symbol
source_gene_id
source_namespace
mapping_status
phenotype_identifier_or_label
phenotype_namespace_if_available
```

VDB brokerage may later add:

```text
canonical_gene_id
canonical_phenotype_id
resolution_event_id
mapping_source
mapping_version
resolution_status
```

These brokerage outputs must not replace original GSC payload identities.

---

## Nullability and Uncertainty Contract

GSC-TEP SHALL distinguish:

```text
NULL = unknown or unavailable
0 = measured zero
no_match = attempted but unresolved or absent
not_applicable = biologically inapplicable
annotation_only = evidence present but not scoring-active
conflict = contradictory evidence or mapping ambiguity
```

The following interpretations are forbidden:

```text
missing score = zero support
absent source = negative evidence
unresolved gene identity = non-membership
no overlay = biological irrelevance
```

---

## Release-Scoped Reproducibility Contract

GSC-TEP SHALL preserve enough release context to permit historical reproducibility.

Minimum release context includes:

```text
gsc_release_id
gsc_version
scoring_profile
source_package_identity
source_artifact_manifest
source_versions_if_available
tep_schema_version
tep_sleeve_version
creation_timestamp
```

A future user must be able to determine which GSC evidence state supported a downstream analysis.

---

## Producer Artifact Immutability

GSC-TEP generation SHALL NOT mutate GSC source artifacts.

GSC-TEP generation MAY project, package, summarize, or organize source evidence into transportable payload structures.

Any projection must remain provenance-aware and reconstructable.

---

## Required Validation Classes

A GSC-TEP implementation SHALL include validation covering:

```text
envelope completeness
source artifact manifest completeness
phenotype preservation
release identity preservation
gene identity preservation
source attribution preservation
semantic channel preservation
scoring context preservation
topology preservation
provenance preservation
uncertainty preservation
namespace brokerage readiness
future reinterpretability
```

Validation strategy is specified separately in:

```text
docs/validation/gsc_tep_validation_strategy.md
```

---

## Acceptance Gate

A GSC-TEP SHALL NOT be considered mature if any of the following are true:

```text
phenotype context is absent
gsc_release_id is absent
source gene identity is unrecoverable
source attribution is unrecoverable
semantic channels are unrecoverable
scoring profile is absent
provenance is insufficient
uncertainty is hidden
aggregation topology is unreconstructable
source artifact manifest is absent
```

Formal acceptance criteria are specified separately in:

```text
docs/validation/gsc_tep_acceptance_criteria.md
```

---

## Implementation Non-Goals

GSC-TEP implementation SHALL NOT:

```text
redesign GSC scoring
redesign VDB schema
redesign RDGP prioritization
perform clinical interpretation
collapse semantic priors into membership flags
normalize identities destructively
treat VDB canonical identity as source truth
homogenize GSC payloads to match VAP payloads
discard source topology for convenience
discard uncertainty for convenience
```

---

## Minimal Implementation Target

The first implementation target should produce a deterministic GSC-TEP from an existing GSC release export and associated provenance artifacts.

The minimal valid GSC-TEP should contain:

```text
valid envelope
source artifact manifest
semantic prior payload
phenotype context
source gene identity
gsc_release_id
scores and scoring profile
semantic channels
source contribution context
provenance
uncertainty states
```

This minimal target is sufficient for early VDB discovery and intake evaluation.

---

## Future Extension Targets

Future GSC-TEP versions may support:

```text
multi-release comparison
expanded phenotype ontology context
source-level contribution matrices
semantic channel decompositions
source artifact checksum enforcement
graph-style aggregation topology
cross-phenotype semantic prior bundles
VDB-mediated overlay discovery surfaces
```

These extensions must preserve backward compatibility with historical GSC-TEP versions whenever possible.

---

## Compliance Summary

A valid GSC-TEP preserves not only what GSC concluded, but why GSC concluded it.

The contract is satisfied when a future consumer can recover:

```text
phenotype context
gene identity
release identity
source attribution
semantic channel composition
scoring context
provenance
uncertainty
aggregation topology
future reinterpretability context
```

from the transported evidence state without requiring access to the original GSC execution environment.

---

## Summary

GSC-TEP is the transport family for GSC semantic prior evidence.

Its purpose is not to compress GSC outputs.

Its purpose is to keep GSC semantic prior meaning alive across systems, releases, reinterpretations, and time.

GSC remains the semantic prior authority.

TEP preserves transportable evidence state.

VDB discovers, brokers, persists, and exposes that evidence without redefining it.

RDGP may later consume preserved priors as phenotype-level support during sample-gene reasoning.

This contract is the implementation authority for DEX-GSC GSC-TEP construction.
