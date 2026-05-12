# Validation Documentation

This directory contains cross-system validation, reproducibility, and runtime portability documentation for GSC.

For a concise overview of the successful MARK execution outcomes, begin with:

- [MARK Execution Summary](mark_execution_summary.md)

Primary validation was performed on MARK, an independent Linux HPC environment distinct from the original Sys76 development workstation.

The MARK validation tested:

- fresh repository reconstruction
- isolated Python environment bootstrap
- external source staging
- Epi25 subtype reconstruction
- GTR XML parsing and summarization
- semantic release execution
- runtime portability
- output contract validation
- reproducibility of semantic scoring behavior

---

# Validation Documents

| Document | Purpose |
|---|---|
| [mark_reproducibility_plan.md](mark_reproducibility_plan.md) | Pre-execution validation goals, scope, and success criteria |
| [mark_reproducibility_protocol.md](mark_reproducibility_protocol.md) | Exact executed reconstruction and validation procedure on MARK |
| [mark_execution_summary.md](mark_execution_summary.md) | Concise summary of successful MARK validation outcomes |
| [mark_probe_inventory.md](mark_probe_inventory.md) | Inventory of MARK execution/debugging probes used during validation |
| [comparisons/](comparisons/) | Cross-system Sys76 vs MARK semantic reproducibility artifacts |

---

# Key Validation Outcomes

MARK validation successfully demonstrated:

- portable release-driven execution
- deterministic Epi25 subtype reconstruction
- reproducible GTR parsing behavior
- provenance-preserving semantic overlays
- MARK-local runtime overlays via `config/local_mark/`
- cross-system semantic reproducibility comparisons between Sys76 and MARK
- successful execution of:
  - epilepsy semantic release
  - DEE semantic release
  - NAFE semantic release
  - mitochondrial semantic release

The validation also revealed and resolved a runtime portability architecture issue involving phenotype config propagation.

For details, see:

- `../design/runtime_portability_refactor.md`

---

# Runtime Portability Notes

The committed repository configuration targets the Sys76-local:

```text
/mnt/storage/
```

layout.

MARK validation intentionally used:

```text
/data/storage/gsc/
```

through machine-local overlay configs generated under:

```text
config/local_mark/
```

These overlays are intentionally not committed to Git and are generated dynamically during validation.

---

## Reproducibility Scope

The current validation establishes:

- cross-machine semantic release portability
- deterministic subtype rollup behavior
- reproducible semantic scoring behavior
- reproducible source integration behavior

Exact byte-identical outputs are not currently expected because outputs contain:

- generated timestamps
- run IDs
- provenance metadata

Primary reproducibility criteria currently include:

- successful output contract validation
- expected row counts
- preserved subtype anchors
- preserved semantic score structure
- preserved biological spot-check behavior

Detailed Sys76 vs MARK comparison artifacts are available under:

```text
docs/validation/comparisons/
```

---
