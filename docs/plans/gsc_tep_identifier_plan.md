# GSC-TEP Identifier Cleanup Plan

## Target File

```text
src/gene_set_consensus/tep/envelope.py
```

## Current Behavior

`build_tep_id(release_id)` currently appends an additional suffix:

```text
_v0_1
```

after the normalized release identifier.

This causes duplicate version identity when `release_id` already includes `v0.1`.

## Desired Behavior

`build_tep_id(release_id)` shall return:

```text
gsc_tep_<normalized_release_id>
```

where periods are normalized to underscores.

## Required Code Change

Update `normalize_release_id_for_tep_id()` to normalize periods:

```python
.replace(".", "_")
```

Update `build_tep_id()` to stop appending:

```text
_v0_1
```

## Expected Example

Input:

```text
epilepsy_semantic_gtr_experimental_v0.1
```

Output:

```text
gsc_tep_epilepsy_semantic_gtr_experimental_v0_1
```

## Verification

After rebuilding the epilepsy TEP:

```bash
jq '.envelope.tep_id' \
results/teps/gsc/epilepsy_semantic_gtr_experimental/gsc_tep.json
```

Expected:

```text
"gsc_tep_epilepsy_semantic_gtr_experimental_v0_1"
```

## Acceptance Criteria

Identifier cleanup is complete when:

* `tep_id` no longer duplicates release/schema version identity
* `source_release_id` remains preserved separately
* `tep_schema_version` remains preserved separately
* `tep_sleeve_version` remains preserved separately
* rebuilt epilepsy GSC-TEP has a pristine `tep_id`
