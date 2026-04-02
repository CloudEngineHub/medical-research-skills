---
name: flow-cytometry-gating-strategist
description: Recommend optimal flow cytometry gating strategies for specific cell.
license: MIT
skill-author: AIPOCH
---
# Skill: Flow Cytometry Gating Strategist

Recommend optimal flow cytometry gating strategies for given cell types and fluorophores.

## Quick Check

Use this command to verify that the packaged script entry point can be parsed before deeper execution.

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

Use these concrete commands for validation. They are intentionally self-contained and avoid placeholder paths.

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Use this skill when the task needs Recommend optimal flow cytometry gating strategies for specific cell.
- Use this skill for protocol design tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Basic Information

- **ID**: 103
- **Name**: Flow Cytometry Gating Strategist
- **Purpose**: Flow cytometry data analysis and gating strategy recommendations

## Usage

### Command Line

```text
# Recommended format: comma-separated cell types and fluorophores
python scripts/main.py "CD4+ T cells,CD8+ T cells" "FITC,PE,APC"

# Or specify parameters separately
python scripts/main.py --cell-types "CD4+ T cells,CD8+ T cells" --fluorophores "FITC,PE,APC"

# Support more options
python scripts/main.py \
  --cell-types "B cells" \
  --fluorophores "FITC,PE,PerCP-Cy5.5,APC" \
  --instrument "BD FACSCanto II" \
  --purpose "cell sorting"
```

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--cell-types` | string | - | Yes | Comma-separated list of cell types (e.g., "CD4+ T cells,CD8+ T cells") |
| `--fluorophores` | string | - | Yes | Comma-separated list of fluorophores (e.g., "FITC,PE,APC") |
| `--instrument` | string | - | No | Flow cytometer model (e.g., "BD FACSCanto II") |
| `--purpose` | string | analysis | No | Purpose (analysis, cell sorting, screening) |
| `--output`, `-o` | string | stdout | No | Output file path for JSON results |

### Output Format

```json
{
  "recommended_strategy": {
    "name": "Sequential Gating Strategy",
    "description": "Gating based on FSC-A/SSC-A, followed by fluorescence intensity analysis",
    "steps": [
      {
        "step": 1,
        "gate": "FSC-A vs SSC-A",
        "purpose": "Identify target cell population, exclude debris and dead cells",
        "recommendation": "Set oval gate in lymphocyte region"
      }
    ]
  },
  "fluorophore_recommendations": [
    {
      "fluorophore": "FITC",
      "channel": "BL1",
      "detector": "530/30",
      "considerations": ["May spillover with GFP"]
    }
  ],
  "panel_optimization": {
    "suggestions": ["Recommend pairing weakly expressed antigens with bright fluorophores"],
    "avoid_combinations": ["FITC and GFP used simultaneously"]
  },
  "compensation_notes": ["FITC and PE require careful compensation"],
  "quality_control": ["Recommend setting FMO controls", "Use viability dyes to exclude dead cells"]
}
```

## Supported Cell Types

- **T cells**: CD4+ T cells, CD8+ T cells, Treg cells, Th1, Th2, Th17, γδ T cells
- **B cells**: B cells, Plasma cells, Memory B cells, Naive B cells
- **Myeloid cells**: Monocytes, Macrophages, Dendritic cells, Neutrophils, Eosinophils
- **Stem cells**: HSC, MSC, iPSC
- **Tumor cells**: Tumor cells, Cancer stem cells
- **Others**: NK cells, NKT cells, Platelets, Erythrocytes

## Supported Fluorophores

| Fluorophore | Excitation Wavelength | Emission Wavelength | Detection Channel |
|------|---------|---------|---------|
| FITC | 488nm | 525nm | BL1 |
| PE | 488nm | 575nm | YL1/BL2 |
| PerCP | 488nm | 675nm | RL1 |
| PerCP-Cy5.5 | 488nm | 695nm | RL1 |
| PE-Cy7 | 488nm | 785nm | RL2 |
| APC | 640nm | 660nm | RL1 |
| APC-Cy7 | 640nm | 785nm | RL2 |
| BV421 | 405nm | 421nm | VL1 |
| BV510 | 405nm | 510nm | VL2 |
| BV605 | 405nm | 605nm | VL3 |
| BV650 | 405nm | 650nm | VL4 |
| BV785 | 405nm | 785nm | VL6 |
| DAPI | 355nm | 461nm | UV |
| PI | 488nm | 617nm | YL2 |

## Gating Strategy Types

### 1. Sequential Gating
Applicable scenario: Simple immunophenotyping analysis
- FSC-A/SSC-A → Exclude debris/dead cells → Fluorescence intensity analysis

### 2. Boolean Gating
Applicable scenario: Complex cell subset analysis
- Use logical operators (AND, OR, NOT) to define cell populations

### 3. Dimensionality Reduction Gating
Applicable scenario: High-dimensional data (>15 colors)
- t-SNE/UMAP visualization-assisted gating

### 4. Unsupervised Clustering
Applicable scenario: Discovery of unknown cell populations
- FlowSOM, PhenoGraph and other algorithms

## Notes

1. **Spectral Overlap Compensation**: Multi-color panels must undergo compensation calculation
2. **Control Setup**: Must use FMO (fluorescence minus one) and isotype controls
3. **Dead Cell Exclusion**: Strongly recommend using viability dyes
4. **Instrument Calibration**: Perform QC and standard bead detection before experiments

## Dependencies

- Python 3.8+
- No external dependencies (pure Python standard library)

## Version

v1.0.0 - Initial version, supports basic gating strategy recommendations

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python scripts with tools | High |
| Network Access | External API calls | High |
| File System Access | Read/write data | Medium |
| Instruction Tampering | Standard prompt guidelines | Low |
| Data Exposure | Data handled securely | Medium |

## Security Checklist

- [ ] No hardcoded credentials or API keys
- [ ] No unauthorized file system access (../)
- [ ] Output does not expose sensitive information
- [ ] Prompt injection protections in place
- [ ] API requests use HTTPS only
- [ ] Input validated against allowed patterns
- [ ] API timeout and retry mechanisms implemented
- [ ] Output directory restricted to workspace
- [ ] Script execution in sandboxed environment
- [ ] Error messages sanitized (no internal paths exposed)
- [ ] Dependencies audited
- [ ] No exposure of internal service architecture

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

This skill accepts requests that match the documented purpose of `flow-cytometry-gating-strategist` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `flow-cytometry-gating-strategist` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.


## References

- [references/audit-reference.md](references/audit-reference.md) - Supported scope, audit commands, and fallback boundaries

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
