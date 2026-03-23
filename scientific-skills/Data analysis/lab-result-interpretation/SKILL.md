---
name: lab-result-interpretation
description: A medical assistant tool that transforms complex biochemical laboratory test results into clear, patient-friendly explanations.
license: MIT
skill-author: AIPOCH
---
# Lab Result Interpretation Skill

A medical assistant tool that transforms complex biochemical laboratory test results into clear, patient-friendly explanations.

## When to Use

- Use this skill when the task needs A medical assistant tool that transforms complex biochemical laboratory test results into clear, patient-friendly explanations.
- Use this skill for data analysis tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Key Features

See `## Features` above for related details.

- Scope-focused workflow aligned to: A medical assistant tool that transforms complex biochemical laboratory test results into clear, patient-friendly explanations.
- Packaged executable path(s): `scripts/main.py`.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

See `## Prerequisites` above for related details.

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `dataclasses`: `unspecified`. Declared in `requirements.txt`.

## Example Usage

See `## Usage` above for related details.

```bash
cd "20260318/scientific-skills/Data Analytics/lab-result-interpretation"
python -m py_compile scripts/main.py
python scripts/main.py --help
```

Example run plan:
1. Confirm the user input, output path, and any required config values.
2. Edit the in-file `CONFIG` block or documented parameters if the script uses fixed settings.
3. Run `python scripts/main.py` with the validated inputs.
4. Review the generated output and return the final artifact with any assumptions called out.

## Implementation Details

See `## Workflow` above for related details.

- Execution model: validate the request, choose the packaged workflow, and produce a bounded deliverable.
- Input controls: confirm the source files, scope limits, output format, and acceptance criteria before running any script.
- Primary implementation surface: `scripts/main.py`.
- Reference guidance: `references/` contains supporting rules, prompts, or checklists.
- Parameters to clarify first: input path, output path, scope filters, thresholds, and any domain-specific constraints.
- Output discipline: keep results reproducible, identify assumptions explicitly, and avoid undocumented side effects.

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

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Features

- Parses various lab test formats (numeric values, units, reference ranges)
- Compares values against standard reference ranges
- Generates patient-friendly explanations in Chinese
- Flags abnormal values with severity indicators
- Provides contextual health recommendations

## Supported Test Types

| Category | Tests |
|----------|-------|
| **Blood Routine** | WBC, RBC, Hemoglobin, Platelets, Hematocrit |
| **Lipid Panel** | Total Cholesterol, LDL, HDL, Triglycerides |
| **Liver Function** | ALT, AST, ALP, GGT, Bilirubin, Total Protein, Albumin |
| **Kidney Function** | Creatinine, BUN, eGFR, Uric Acid |
| **Blood Sugar** | Fasting Glucose, HbA1c |
| **Thyroid** | TSH, T3, T4, FT3, FT4 |
| **Electrolytes** | Sodium, Potassium, Chloride, Calcium, Magnesium |
| **Inflammation** | CRP, ESR |

## Usage

### As Module

```python
from scripts.main import LabResultInterpreter

interpreter = LabResultInterpreter()
result = interpreter.interpret("total cholesterol: 5.8 mmol/L (refer to: 3.1-5.7)")
print(result.explanation)
```

### CLI

```text
python scripts/main.py --file lab_report.txt
python scripts/main.py --interactive
```

## Parameters

| Name | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| file | string | "" | No | Path to lab report file to process |
| interactive | boolean | false | No | Enable interactive mode for manual input |
| input | string | "" | No | Direct lab test input string for interpretation |

## Input Format

Accepts flexible formats:
```
Test Name: Value Unit (Reference: Min-Max)
Test Name Value Unit Ref: Min-Max
Test Name: Value (Min-Max)
```

## Output Format

```json
{
  "test_name": "total cholesterol",
  "value": 5.8,
  "unit": "mmol/L",
  "reference_min": 3.1,
  "reference_max": 5.7,
  "status": "high",
  "explanation": "Your total cholesterol is slightly above the normal range...",
  "severity": "mild",
  "recommendation": "Recommended to reduce saturated fat intake..."
}
```

## Technical Details

**Difficulty:** Medium

**Key Components:**
- Lab value parsing with regex patterns
- Reference range comparison logic
- Medical knowledge base (references/lab_reference_ranges.json)
- Patient-friendly explanation templates

**Safety:**
- Includes medical disclaimer in all outputs
- Flags values requiring immediate medical attention
- Does not diagnose - only explains test meanings

## References

- `references/lab_reference_ranges.json` - Standard reference ranges
- `references/explanation_templates.json` - Patient-friendly templates
- `references/test_metadata.json` - Test descriptions and clinical notes

## Medical Disclaimer

This tool provides educational information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for interpretation of lab results.

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

This skill accepts requests that match the documented purpose of `lab-result-interpretation` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `lab-result-interpretation` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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
