# GSC TEP Finalized Run Contract

## Purpose

Define the authoritative source from which a GSC Transitional Evidence Product (GSC-TEP) must be constructed.

This contract establishes the preservation boundary between GSC release execution and downstream evidence transport.

---

# Core Principle

A GSC-TEP shall be constructed from a finalized GSC run.

A GSC-TEP shall not be constructed from mutable package-scoped convenience outputs.

---

# Authoritative Source

The authoritative source for GSC-TEP construction is:

```text
results/runs/<run_id>/
```

specifically:

```text
results/runs/<run_id>/reports/<package_id>/final_run_manifest.yaml
```

The final run manifest represents the completed and validated scientific release execution.

---

# Required Preconditions

A GSC-TEP may only be constructed when:

```text
run_status = COMPLETE
```

and

```text
validation_status = PASS
```

are present in the final run manifest.

If either condition is not satisfied, TEP construction shall fail.

---

# Prohibited Inputs

The following locations shall not be treated as authoritative inputs for TEP construction:

```text
results/tables/<package_id>/
```

```text
results/reports/<package_id>/
```

These locations are convenience mirrors intended for operator access.

They may be overwritten by future executions.

They do not uniquely identify a scientific release execution.

---

# Required Provenance Capture

Every GSC-TEP shall preserve:

* run_id
* package_id
* package_version
* release_id
* phenotype
* validation_status
* finalization_timestamp

from the finalized run state.

---

# Preservation Boundary

The finalized run directory defines the preservation boundary of the GSC producer.

All scientific payloads transported into VDB must be derivable from:

```text
results/runs/<run_id>/
```

without requiring access to mutable package-level outputs.

---

# Consumer Expectations

Downstream consumers including:

* VDB
* RDGP
* future repository consumers

shall treat the GSC-TEP as a representation of a finalized run rather than a representation of the current package state.

This guarantees reproducibility, provenance preservation, and historical recoverability.

---

# Governance Summary

Authoritative:

```text
results/runs/<run_id>/
```

Convenience:

```text
results/tables/<package_id>/
results/reports/<package_id>/
```

Transport:

```text
results/teps/gsc/
```

A GSC-TEP represents a finalized scientific release execution.
