# GSC Step08 TEP Construction Plan

## Objective

Integrate automatic GSC-TEP generation into normal pipeline execution without requiring operator discovery of run identifiers.

## Phase 1: Pipeline Integration

Add:

```text
scripts/step_08_build_tep.py
```

Responsibilities:

1. Accept:

   * run_id
   * package_id
   * final_run_manifest path

2. Invoke existing TEP builder.

3. Verify output existence.

4. Emit logging consistent with Steps01-07.

Example:

```text
[GSC] starting step_08_build_tep
[GSC] completed step_08_build_tep
```

## Phase 2: Runtime Integration

Update:

```text
run_pipeline.py
```

Sequence becomes:

```text
Step01 Validate Inputs
Step02 Normalize Genes
Step03 Build Source Matrix
Step04 Score Consensus
Step05 Write Outputs
Step06 Validate Outputs
Step07 Finalize Run
Step08 Build TEP
```

Step08 receives the exact finalized manifest path emitted by Step07.

No filesystem discovery logic is permitted.

## Phase 3: Validation

Execute:

```bash
python run_pipeline.py \
  --release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml
```

Verify:

```text
results/runs/<run_id>/...
results/teps/gsc/<package_id>/gsc_tep.json
```

Verify TEP references:

```text
results/runs/<run_id>/
```

Verify:

```text
source_run_status = COMPLETE
source_validation_status = PASS
```

inside the envelope.

## Acceptance Criteria

Operator workflow becomes:

```bash
python run_pipeline.py --release <release.yaml>
```

and automatically yields:

```text
finalized run
+
VDB-ready GSC-TEP
```

with no manual run discovery or post-processing steps.
