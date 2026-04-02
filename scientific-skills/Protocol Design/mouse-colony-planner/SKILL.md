---
name: mouse-colony-planner
description: Calculate breeding timelines and cage requirements for transgenic mouse.
license: MIT
skill-author: AIPOCH
---
# Mouse Colony Planner

Calculate timelines and cage numbers required for transgenic mouse breeding to optimize breeding costs.

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

- Use this skill when the task needs Calculate breeding timelines and cage requirements for transgenic mouse.
- Use this skill for protocol design tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Functions

- **Timeline Calculation**: Calculate time required for each stage based on breeding scheme
- **Cage Planning**: Estimate cage numbers needed for experiments
- **Cost Estimation**: Calculate total breeding costs (cage fees, husbandry fees, genotyping fees, etc.)

## Usage

### Command Line

```text
python scripts/main.py --scheme <breeding_scheme> --females <number_of_females> --males <number_of_males> [options]
```

### Parameters

| Parameter | Description | Default |
|------|------|--------|
| `--scheme` | Breeding scheme: `heterozygote`, `homozygote`, `conditional` | Required |
| `--females` | Starting number of females | Required |
| `--males` | Starting number of males | Required |
| `--gestation` | Gestation period (days) | 21 |
| `--weaning` | Weaning age (days) | 21 |
| `--sexual-maturity` | Sexual maturity age (days) | 42 |
| `--cage-capacity` | Maximum cage capacity | 5 |
| `--cage-cost` | Cage cost per day (CNY) | 3.0 |
| `--genotyping-cost` | Genotyping cost per mouse (CNY) | 15.0 |
| `--target-pups` | Target number of specific genotype mice | 10 |

### Breeding Scheme Descriptions

1. **heterozygote (Heterozygote breeding)**: Heterozygote x Wild type → 50% Heterozygotes
2. **homozygote (Homozygote breeding)**: Heterozygote x Heterozygote → 25% Homozygotes
3. **conditional (Conditional knockout)**: Requires two-step breeding, introducing Cre/loxp system

### Examples

```text
# Heterozygote breeding scheme, starting with 10 females and 5 males, target to obtain 10 heterozygote offspring
python scripts/main.py --scheme heterozygote --females 10 --males 5 --target-pups 10

# Homozygote breeding, custom cycle parameters
python scripts/main.py --scheme homozygote --females 20 --males 10 --target-pups 20 --gestation 21 --weaning 21

# Conditional knockout scheme
python scripts/main.py --scheme conditional --females 15 --males 15 --target-pups 15
```

## Output

- Timeline for each stage
- Cage numbers required at each stage
- Estimated total cost
- Breeding flowchart

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

```text
# Python dependencies
pip install -r requirements.txt
```

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

This skill accepts requests that match the documented purpose of `mouse-colony-planner` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `mouse-colony-planner` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.


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
