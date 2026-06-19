# GSC TEP Certification Contract

## Purpose

This contract defines the requirements a GSC Transitional Evidence Product (GSC-TEP) must satisfy before it may be considered a certified transport artifact suitable for preservation-aware ingestion by VDB.

The purpose of certification is not merely transport.

The purpose of certification is preservation of biological meaning, provenance, identity, uncertainty, and reconstruction capability during cross-repository movement.

---

# 1. Certification Scope

This contract applies to all GSC-produced Transitional Evidence Products.

Examples include:

```text
epilepsy_semantic_gtr_experimental_v0.1
mitochondrial_semantic_gtr_experimental_v0.1
```

and all future phenotype-scoped GSC releases.

---

# 2. Identity Preservation Requirements

## 2.1 Canonical Identity Preservation

Each semantic prior SHALL preserve:

```text
gene_id
gene_symbol
mapping_status
```

as transported identity attributes.

## 2.2 Namespace Preservation

Each semantic prior SHALL explicitly preserve namespace information.

Required fields:

```text
gene_namespace
source_gene_namespace
```

Namespace identity SHALL remain visible after transport.

Namespace identity SHALL NOT be inferred solely from identifier format.

## 2.3 Source Identity Preservation

Where source-level identifiers exist, the TEP SHALL preserve:

```text
source_gene_id
source_gene_symbol
source_gene_namespace
```

to permit downstream provenance reconstruction.

---

# 3. Mapping Uncertainty Preservation Requirements

## 3.1 Ambiguous Resolution Visibility

Mappings that cannot be represented as deterministic one-to-one resolutions SHALL remain visible as uncertainty states.

Examples include:

```text
one_to_many
many_to_one
many_to_many
```

resolution outcomes.

## 3.2 Multi-Identifier Preservation

Compound identifiers SHALL NOT be represented as fully resolved identities.

Examples:

```text
ENSG00000275176|ENSG00000278540
```

shall preserve explicit uncertainty semantics.

Recommended representations include:

```text
mapping_status
mapping_uncertainty
nullability_notes
```

or equivalent fields.

## 3.3 Uncertainty Retention

The transport process SHALL preserve uncertainty rather than collapse uncertainty.

---

# 4. Source Contribution Preservation Requirements

## 4.1 Contribution Topology

A certified GSC-TEP SHALL preserve sufficient information to reconstruct:

```text
source
    →
evidence semantics
    →
semantic channel
    →
score contribution
```

relationships.

## 4.2 Provenance Traceability

Source contribution records SHALL remain traceable to originating evidence sources.

## 4.3 Aggregation Transparency

The transport artifact SHALL preserve aggregation lineage sufficient for downstream scientific interpretation.

---

# 5. Manifest Integrity Requirements

## 5.1 Artifact Preservation

The TEP manifest SHALL preserve references to authoritative producer artifacts.

Required artifact categories include:

```text
consensus outputs
provenance outputs
supporting aggregation outputs
validation outputs
run manifests
```

## 5.2 Verification Authority

The TEP SHALL expose artifact verification authority.

Verification authority may be represented by:

```text
artifact_hash
hash_algorithm
```

or by explicit delegation to:

```text
final_run_manifest.yaml
```

where checksum authority resides.

## 5.3 Reconstruction Capability

Consumers SHALL be able to determine how artifact authenticity is validated.

---

# 6. Run Preservation Requirements

## 6.1 Finalized Run Anchor

Certified GSC-TEPs SHALL originate from finalized runs.

Required finalized state:

```text
run_status = COMPLETE
validation_status = PASS
```

## 6.2 Finalized Manifest Anchor

Certified GSC-TEPs SHALL reference:

```text
final_run_manifest.yaml
```

as the authoritative producer-side preservation anchor.

## 6.3 Run Identity Preservation

The transport artifact SHALL preserve:

```text
run_id
release_id
package_id
package_version
phenotype
```

for reconstruction and audit purposes.

---

# 7. Retention Requirements

## 7.1 Authoritative TEP Retention

Authoritative TEP outputs SHALL be run-scoped.

Required location pattern:

```text
results/teps/gsc/<package_id>/<run_id>/gsc_tep.json
```

## 7.2 Convenience Projections

Package-level TEP projections MAY exist.

Examples:

```text
results/teps/gsc/<package_id>/gsc_tep.json
```

Such projections SHALL be treated as convenience artifacts rather than authoritative preservation artifacts.

## 7.3 Historical Preservation

Subsequent executions SHALL NOT overwrite authoritative historical TEPs.

---

# 8. Scientific Preservation Requirements

## 8.1 Phenotype Scope Preservation

Phenotype context SHALL remain explicitly visible.

## 8.2 Semantic Preservation

Semantic channels SHALL remain visible after transport.

## 8.3 Provenance Preservation

Source provenance SHALL remain reconstructable.

## 8.4 Non-Collapse Principle

The transport process SHALL NOT collapse:

```text
identity
namespace
uncertainty
semantic attribution
source contribution topology
```

into simplified or opaque representations.

---

# 9. Certification Outcome

A GSC-TEP is considered certified when it satisfies all requirements defined by this contract.

Certification indicates that the transport artifact is suitable for:

```text
preservation-aware transport
cross-repository interoperability
VDB ingestion
long-term reconstruction
scientific auditability
```

without unacceptable loss of biological meaning or provenance.
