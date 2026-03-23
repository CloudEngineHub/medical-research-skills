---
name: symptom-checker-triage
description: Suggest triage levels based on red flag symptoms for emergency vs outpatient.
license: MIT
skill-author: AIPOCH
---
# Symptom Checker Triage (ID: 165)

Suggests triage levels (Emergency vs Outpatient) based on red flags in common symptoms.

## When to Use

- Use this skill when the task needs Suggest triage levels based on red flag symptoms for emergency vs outpatient.
- Use this skill for data analysis tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Key Features

See `## Features` above for related details.

- Scope-focused workflow aligned to: Suggest triage levels based on red flag symptoms for emergency vs outpatient.
- Packaged executable path(s): `scripts/main.py`.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

See `## Prerequisites` above for related details.

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `dataclasses`: `unspecified`. Declared in `requirements.txt`.
- `enum`: `unspecified`. Declared in `requirements.txt`.

## Example Usage

```bash
cd "20260318/scientific-skills/Data Analytics/symptom-checker-triage"
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

- Analyzes symptom descriptions entered by users
- Identifies red flags (life-threatening symptoms)
- Suggests triage level: Emergency or Outpatient
- Provides triage rationale and medical advice

## Input

### Command Line Arguments

```text
python scripts/main.py "symptom description"
```

Or interactive mode:

```text
python scripts/main.py --interactive
```

### Input Format

Symptom description (natural language), for example:
- "Chest pain, difficulty breathing, lasting 30 minutes"
- "Headache, fever 38.5 degrees, vomiting"
- "Abdominal pain, right lower quadrant tenderness, fever"

## Output

JSON format:

```json
{
  "triage_level": "emergency|outpatient|urgent",
  "confidence": 0.85,
  "red_flags": ["Chest pain", "Difficulty breathing"],
  "reason": "Chest pain with difficulty breathing may be a sign of myocardial infarction or pulmonary embolism",
  "recommendation": "Please go to emergency department immediately",
  "department": "Emergency/Cardiology",
  "warning": "This is AI-assisted advice and cannot replace professional medical diagnosis"
}
```

## Triage Levels

| Level | Description | Recommendation |
|------|------|------|
| emergency | Life-threatening | Call 120 immediately or go to emergency |
| urgent | Urgent but not immediately fatal | Seek medical care within 2-4 hours |
| outpatient | Non-urgent | Schedule outpatient appointment |

## Red Flags List

### Cardiovascular System
- Chest pain/chest tightness (especially with difficulty breathing, sweating)
- Severe palpitations with syncope
- Extremely high blood pressure (>180/120)

### Respiratory System
- Severe difficulty breathing/sensation of suffocation
- Hemoptysis
- Blood oxygen saturation <90%

### Nervous System
- Sudden severe headache ("worst headache of my life")
- Altered consciousness/coma
- Slurred speech/hemiplegia (stroke signs)
- Status epilepticus

### Digestive System
- Hematemesis/melena
- Severe abdominal pain with abdominal rigidity
- Intestinal obstruction symptoms (abdominal distension, cessation of flatus and defecation)

### Others
- Severe trauma/bleeding
- High fever (>40°C) with altered consciousness
- Drug overdose/poisoning
- Pregnant women: vaginal bleeding, severe abdominal pain, decreased fetal movement

## Usage Examples

```text

# Direct symptom input
python scripts/main.py "Chest pain, radiating to left arm, sweating"

# Interactive mode
python scripts/main.py --interactive

# Detailed output
python scripts/main.py "Headache, fever" --verbose
```

## Disclaimer

⚠️ **Important Notice**:
- This tool only provides AI-assisted triage advice
- **Cannot replace professional medical diagnosis**
- If in doubt, please seek medical care immediately
- Call 120 in emergency situations

## Technical Implementation

- Rule-based engine + keyword matching
- Supports symptom synonym expansion
- Configurable red flag weights
- Supports confidence calculation

## File Structure

```
skills/symptom-checker-triage/
├── SKILL.md
└── scripts/
    └── main.py
```

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

This skill accepts requests that match the documented purpose of `symptom-checker-triage` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `symptom-checker-triage` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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
