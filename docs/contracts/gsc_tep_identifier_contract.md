# GSC-TEP Identifier Contract

## Purpose

Define the construction rule for `tep_id` in GSC-TEP envelopes.

## Problem

Current `tep_id` construction can duplicate version identity.

Example:

```text
gsc_tep_epilepsy_semantic_gtr_experimental_v0.1_v0_1
```

This is not pristine because the release identifier already contains the release version, while the builder appends an additional TEP/schema-style version suffix.

## Contract

`tep_id` shall identify the transported GSC evidence product without duplicating version concepts.

A GSC-TEP identifier shall be derived from:

```text
gsc_tep + source_release_id
```

where `source_release_id` already contains package and release version identity.

## Required Shape

For:

```text
source_release_id = epilepsy_semantic_gtr_experimental_v0.1
```

the `tep_id` shall be:

```text
gsc_tep_epilepsy_semantic_gtr_experimental_v0_1
```

## Prohibited Shape

The following shape is prohibited:

```text
gsc_tep_<release_id>_v0_1
```

when `<release_id>` already includes a version suffix.

## Rationale

The TEP schema version is already preserved separately as:

```text
tep_schema_version
```

The TEP sleeve version is already preserved separately as:

```text
tep_sleeve_version
```

Therefore, `tep_id` shall not append schema or sleeve version identity.
