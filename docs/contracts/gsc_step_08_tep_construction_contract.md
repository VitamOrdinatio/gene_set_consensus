# GSC Step08 TEP Construction Contract

## Purpose

Define the final transport-projection stage of a GSC release execution.

Step08 converts a finalized GSC run into a VDB-ingestable GSC-TEP.

## Scope

Step08 executes only after successful completion of:

```text
Step07 Finalize Run
```

and consumes:

```text
results/runs/<run_id>/reports/<package_id>/final_run_manifest.yaml
```

as its authoritative input.

## Inputs

Required:

```text
final_run_manifest.yaml
```

The finalized run manifest is the sole authoritative execution anchor for Step08.

Step08 shall not derive identity from:

```text
results/tables/
results/reports/
```

because those locations are convenience projections and may be overwritten by future runs.

## Outputs

Step08 produces:

```text
results/teps/gsc/<package_id>/gsc_tep.json
```

The generated TEP shall reference only run-scoped authoritative artifacts under:

```text
results/runs/<run_id>/
```

## Success Criteria

Step08 is successful when:

1. GSC-TEP construction completes without error.
2. TEP envelope references finalized run identity.
3. TEP manifest references run-scoped artifacts.
4. TEP payload is generated successfully.
5. Output file exists at:

```text
results/teps/gsc/<package_id>/gsc_tep.json
```

## Failure Semantics

If Step08 fails:

```text
Step07 remains authoritative.
```

The finalized run remains valid and reproducible.

A failed Step08 does not invalidate:

```text
run_status = COMPLETE
validation_status = PASS
```

inside the finalized run manifest.

## Architectural Boundary

Step07 owns:

```text
producer finalization
```

Step08 owns:

```text
transport projection
```

This separation preserves clear troubleshooting boundaries and future extensibility.
