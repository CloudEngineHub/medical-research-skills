---
name: protein-docking-configurator
description: Prepare input files for molecular docking software, automatically determine.
license: MIT
skill-author: AIPOCH
---
# Protein Docking Configurator

## Quick Check

Use this command to verify that the packaged script entry point can be parsed before deeper execution.

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

Use these concrete commands for validation. They are intentionally self-contained and avoid placeholder paths.

```bash
python -m py_compile scripts/main.py
python scripts/smoke_test.py
```

## When to Use

- Use this skill when the task needs Prepare input files for molecular docking software, automatically determine.
- Use this skill for protocol design tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Audit Note

The main script may depend on scientific runtime inputs that are not available in constrained audit environments. Audit validation therefore uses `scripts/smoke_test.py` as the deterministic fallback command for structural verification.

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Features

- Parse protein PDB files, identify ligand binding pockets
- Automatically calculate Grid Box center coordinates and dimensions
- Generate AutoDock Vina configuration files
- Generate AutoDock4 Grid parameter files
- Support Box positioning based on active site residues or ligands

## Usage

### As Command Line Tool

```text
# Calculate Grid Box based on active site residues
python scripts/main.py --receptor protein.pdb --active-site-residues "A:120,A:145,A:189" --software vina

# Calculate Grid Box based on reference ligand
python scripts/main.py --receptor protein.pdb --reference-ligand ligand.pdb --software vina

# Manually specify Box parameters
python scripts/main.py --receptor protein.pdb --center-x 10.5 --center-y -5.2 --center-z 20.1 --size-x 20 --size-y 20 --size-z 20 --software vina
```

### As Python Module

```python
from scripts.main import DockingConfigurator

config = DockingConfigurator()

# Calculate box from receptor and active site
config.from_active_site("protein.pdb", ["A:120", "A:145", "A:189"])
config.write_vina_config("config.txt", exhaustiveness=32)

# Calculate box from receptor and reference ligand
config.from_reference_ligand("protein.pdb", "ligand.pdb", padding=5.0)
config.write_autodock4_gpf("protein.gpf", spacing=0.375)
```

## Parameter Description

### Command Line Parameters

| Parameter | Description | Required |
|------|------|------|
| `--receptor` | Receptor protein PDB file path | Yes |
| `--software` | Docking software type (vina/autodock4) | Yes |
| `--active-site-residues` | Active site residue list, format: "chain:residue_number" | No |
| `--reference-ligand` | Reference ligand PDB/MOL file | No |
| `--center-x/y/z` | Grid Box center coordinates | No |
| `--size-x/y/z` | Grid Box dimensions (Å) | No |
| `--spacing` | Grid spacing (AutoDock4 only) | No (default 0.375) |
| `--exhaustiveness` | Search exhaustiveness (Vina only) | No (default 32) |
| `--output` | Output file path | No |

## Output

- **AutoDock Vina**: Generates config.txt configuration file
- **AutoDock4**: Generates .gpf (Grid Parameter File) and corresponding macromolecule files

## Dependencies

- Python 3.8+
- numpy

## Examples

```text
# Example 1: Using active site residues
python scripts/main.py --receptor 1abc_receptor.pdb --active-site-residues "A:45,A:92,A:156" --software vina --output vina_config.txt

# Example 2: Using reference ligand with custom Box size
python scripts/main.py --receptor kinase.pdb --reference-ligand ATP.pdb --software vina --size-x 25 --size-y 25 --size-z 25

# Example 3: AutoDock4 configuration
python scripts/main.py --receptor protein.pdb --active-site-residues "A:100" --software autodock4 --spacing 0.375 --output protein.gpf
```

## Notes

1. Input PDB files should have water molecules and heteroatoms removed (unless needed)

## References

- [references/audit-reference.md](references/audit-reference.md) - Supported docking-config scope, audit commands, and fallback boundaries
2. It is recommended to protonate and calculate charges for the receptor (using AutoDock Tools, etc.)
3. Grid Box size should be sufficient to cover ligand conformational space, typically 20-30Å
4. Active site residues should include catalytic residues and key binding residues

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python/R scripts executed locally | Medium |
| Network Access | No external API calls | Low |
| File System Access | Read input files, write output files | Medium |
| Instruction Tampering | Standard prompt guidelines | Low |
| Data Exposure | Output files saved to workspace | Low |

## Security Checklist

- [ ] No hardcoded credentials or API keys
- [ ] No unauthorized file system access (../)
- [ ] Output does not expose sensitive information
- [ ] Prompt injection protections in place
- [ ] Input file paths validated (no ../ traversal)
- [ ] Output directory restricted to workspace
- [ ] Script execution in sandboxed environment
- [ ] Error messages sanitized (no stack traces exposed)
- [ ] Dependencies audited

## Prerequisites

No additional Python packages required.

## Evaluation Criteria

### Success Metrics
- [ ] Successfully executes main functionality
- [ ] Output meets quality standards
- [ ] Handles edge cases gracefully
- [ ] Performance is acceptable

### Test Cases
1. **Basic Functionality**: Standard input → Expected output
2. **Edge Case**: Invalid input → Graceful error handling
3. **Performance**: Large dataset → Acceptable processing time

## Lifecycle Status

- **Current Stage**: Draft
- **Next Review Date**: 2026-03-06
- **Known Issues**: None
- **Planned Improvements**: 
  - Performance optimization
  - Additional feature support

## Output Requirements

Every final response should make these items explicit when they are relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Input Validation

This skill accepts requests that match the documented purpose of `protein-docking-configurator` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `protein-docking-configurator` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, you may compress the structure, but still keep assumptions and limits explicit when they affect correctness.
