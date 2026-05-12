# MARK Probe Inventory

MARK is the high-performance cluster (HPC) node that executes production code.

Due to Cloudshare/Guacamole limitations, the clipboard is unreliable.

For code execution on MARK, there are two rapid entry points:

- git pulls for main repo (GSC) codebase
- uploads into /root/Desktop for execution harnesses as bash scripts

The latter is termed MARK probe. Such an execution harness can also write to /root/Desktop/ console output as runtime log files for testing, validation, and debugging.

## MARK Probes Used for GSC

| Probe     | Purpose                        | Outcome |
| --------- | ------------------------------ | ------- |
| Probe 00  | storage reconnaissance         | PASS    |
| Probe 01  | storage reconnaissance         | PASS    |
| Probe 02  | environment bootstrap          | PASS    |
| Probe 03  | Epi25 reconstruction           | PASS    |
| Probe 04  | source ingestion + GTR parsing | PASS    |
| Probe 05  | semantic release execution     | FAIL    |
| Probe 05b | local release patch validation | PASS    |
| Probe 05c | runtime portability debugging  | PASS    |
| Probe 05d | semantic release execution after runtime refactor    | PASS    |

**Notes**
- Probe 05 initially failed which revealed a runtime portability refactor requirement.
- After refactoring, Probe 05 passed on MARK indicating end-to-end semantic release execution for GSC.

For more details on the runtime portability refactor, please see:
- [Runtime Portability Refactor](../design/runtime_portability_refactor.md)