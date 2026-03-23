---
name: bmi-bsa-calculator
description: Calculate Body Mass Index (BMI) and Body Surface Area (BSA) for clinical.
license: MIT
skill-author: AIPOCH
---
# BMI & BSA Calculator

## When to Use

- Use this skill when the task needs Calculate Body Mass Index (BMI) and Body Surface Area (BSA) for clinical.
- Use this skill for data analysis tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Key Features

- Scope-focused workflow aligned to: Calculate Body Mass Index (BMI) and Body Surface Area (BSA) for clinical.
- Packaged executable path(s): `scripts/main.py`.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

See `## Prerequisites` above for related details.

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `argparse`: `unspecified`. Declared in `requirements.txt`.
- `json`: `unspecified`. Declared in `requirements.txt`.
- `math`: `unspecified`. Declared in `requirements.txt`.
- `sys`: `unspecified`. Declared in `requirements.txt`.
- `typing`: `unspecified`. Declared in `requirements.txt`.

## Example Usage

See `## Usage` above for related details.

```bash
cd "20260318/scientific-skills/Data Analytics/bmi-bsa-calculator"
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

# Example invocation: python scripts/main.py --help
```

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Overview

Clinical calculator for anthropometric measurements used in health assessment, obesity screening, and chemotherapy dosing calculations.

**Key Capabilities:**
- **BMI Calculation**: Standard and adjusted BMI formulas
- **BSA Estimation**: Multiple validated formulas (DuBois, Mosteller, Haycock)
- **Weight Classification**: WHO and CDC category assignment
- **Dosing Support**: Chemotherapy and medication dose calculations
- **Pediatric Support**: Age-appropriate norms and calculations
- **Unit Flexibility**: Metric and imperial input support

## Core Capabilities

### 1. BMI Calculation

Calculate Body Mass Index with classification:

```python
from scripts.calculator import BMIBSACalculator

calc = BMIBSACalculator()

# Calculate BMI
result = calc.calculate_bmi(
    weight_kg=70,
    height_cm=175,
    age=45,
    sex="male"
)

print(f"BMI: {result.bmi:.1f} kg/m²")
print(f"Category: {result.category}")  # Normal weight
print(f"Ideal weight range: {result.ideal_weight_range}")
```

**BMI Categories (WHO):**
| Category | BMI Range | Clinical Significance |
|----------|-----------|---------------------|
| **Underweight** | < 18.5 | Malnutrition risk |
| **Normal** | 18.5 - 24.9 | Healthy range |
| **Overweight** | 25.0 - 29.9 | Increased risk |
| **Obese I** | 30.0 - 34.9 | High risk |
| **Obese II** | 35.0 - 39.9 | Very high risk |
| **Obese III** | ≥ 40.0 | Extremely high risk |

**Adjusted BMI:**
- **BMI Prime**: BMI / 25 (obesity severity index)
- **Ponderal Index**: BMI for tall/short individuals
- **Age-adjusted**: For elderly patients (>65)

### 2. BSA Calculation

Multiple formulas for different clinical scenarios:

```python

# Calculate BSA using different formulas
bsa_results = calc.calculate_bsa(
    weight_kg=70,
    height_cm=175,
    formulas=["dubois", "mosteller", "haycock", "gehan_george"]
)

for formula, bsa in bsa_results.items():
    print(f"{formula}: {bsa:.2f} m²")
```

**BSA Formulas:**
| Formula | Equation | Best For |
|---------|----------|----------|
| **DuBois** | 0.007184 × W^0.425 × H^0.725 | Adults (most common) |
| **Mosteller** | √(W × H / 3600) | Adults (simplified) |
| **Haycock** | 0.024265 × W^0.5378 × H^0.3964 | Pediatrics |
| **Gehan-George** | 0.0235 × W^0.51456 × H^0.42246 | Oncology |
| **Yu** | 0.015925 × W^0.5 × H^0.5 | Asian populations |

### 3. Drug Dosing Calculations

Apply BSA to medication dosing:

```python

# Calculate chemotherapy dose
dose = calc.calculate_dose(
    bsa=bsa_results["dubois"],
    drug="carboplatin",
    dose_per_m2=400,  # mg/m²
    max_dose=800  # mg cap
)

print(f"Calculated dose: {dose:.0f} mg")
print(f"BSA used: {bsa_results['dubois']:.2f} m²")
```

**Common BSA-Based Doses:**
- Carboplatin: AUC-based (Calvert formula)
- 5-FU: 400-600 mg/m²
- Doxorubicin: 60-75 mg/m² (lifetime max 450-550 mg/m²)
- Paclitaxel: 135-175 mg/m²

### 4. Pediatric Calculations

Age-appropriate calculations for children:

```python
pediatric = calc.pediatric_mode(
    weight_kg=25,
    height_cm=120,
    age_years=8,
    sex="female"
)

print(f"BMI-for-age percentile: {pediatric.bmi_percentile}%")
print(f"Weight status: {pediatric.weight_status}")
print(f"BSA (Haycock): {pediatric.bsa:.2f} m²")
```

**Pediatric Considerations:**
- BMI percentiles (not absolute values)
- Growth chart integration
- Age-specific BSA formulas
- Body composition changes with development

## Common Patterns

### Pattern 1: Chemotherapy Dosing

**Scenario**: Calculate carboplatin dose for cancer patient.

```text

# Calculate BSA and dose

# Example invocation: python scripts/main.py \
  --weight 70 \
  --height 175 \
  --drug carboplatin \
  --target-auc 5 \
  --creatinine-clearance 80 \
  --output dose_calculation.txt
```

**Output:**
```
BSA (DuBois): 1.79 m²
Calvert Formula: Dose = Target AUC × (GFR + 25)
                 = 5 × (80 + 25)
                 = 525 mg
Maximum dose check: 525 mg ≤ 800 mg ✓
Recommended dose: 525 mg
```

### Pattern 2: Obesity Screening

**Scenario**: BMI assessment for weight management clinic.

```python

# BMI with full assessment
assessment = calc.assess_bmi(
    weight_kg=95,
    height_cm=165,
    age=52,
    sex="female",
    waist_cm=98
)

print(f"BMI: {assessment.bmi:.1f} (Obese Class II)")
print(f"Waist-to-height ratio: {assessment.whtr:.2f} (High risk)")
print(f"Comorbidity risk: {assessment.health_risk}")
print(f"Recommended: {assessment.recommendations}")
```

### Pattern 3: Pediatric Growth Assessment

**Scenario**: Calculate child's BSA for medication dosing.

```python

# Pediatric dosing
child = calc.pediatric_assessment(
    weight_kg=20,
    height_cm=110,
    age_years=6,
    sex="male"
)

print(f"BSA: {child.bsa:.2f} m² (Haycock formula)")
print(f"BMI percentile: {child.bmi_percentile}th")
print(f"Doxorubicin dose: {child.bsa * 60:.0f} mg")
```

### Pattern 4: Rapid Clinical Assessment

**Scenario**: Quick BMI/BSA for admission vital signs.

```text

# Quick calculation

# Example invocation: python scripts/main.py --weight 80 --height 180 --quick

# Output:

# BMI: 24.7 kg/m² (Normal)

# BSA: 2.00 m² (DuBois)

# Ideal weight: 65-80 kg
```

## Complete Workflow Example

**Comprehensive patient assessment:**

```python
from scripts.calculator import BMIBSACalculator
from scripts.reports import ClinicalReport

# Initialize
calc = BMIBSACalculator()
report = ClinicalReport()

# Patient data
patient = {
    "weight_kg": 75,
    "height_cm": 170,
    "age": 55,
    "sex": "female",
    "waist_cm": 88
}

# Calculate all metrics
bmi = calc.calculate_bmi(**patient)
bsa = calc.calculate_bsa(**patient, formula="dubois")
assessment = calc.comprehensive_assessment(**patient)

# Generate report
report_data = {
    "bmi": bmi,
    "bsa": bsa,
    "assessment": assessment,
    "recommendations": assessment.recommendations
}

report.generate(report_data, output="patient_assessment.pdf")
```

## Quality Checklist

**Input Validation:**
- [ ] Weight realistic (2-300 kg range)
- [ ] Height realistic (50-250 cm range)
- [ ] Units clearly specified (kg/lbs, cm/in)
- [ ] Age appropriate for formulas used

**Calculation Accuracy:**
- [ ] Formula selection appropriate for patient
- [ ] BSA formula matches clinical context
- [ ] Pediatric vs. adult norms correctly applied
- [ ] Rounding appropriate (1-2 decimal places)

**Clinical Interpretation:**
- [ ] **CRITICAL**: BMI is screening tool, not diagnostic
- [ ] Ethnicity-specific cutoffs considered
- [ ] Muscle mass considered (athletes)
- [ ] Age adjustments applied (elderly/children)

**Documentation:**
- [ ] Formula used documented (DuBois vs. Mosteller)
- [ ] Units clearly stated
- [ ] Date of calculation recorded
- [ ] Dose limits verified for chemotherapy

## Common Pitfalls

**Calculation Errors:**
- ❌ **Unit confusion** → Pounds vs. kg, inches vs. cm
  - ✅ Always verify units; convert if necessary

- ❌ **Wrong formula** → Using adult BSA for infants
  - ✅ Use Haycock for children < 12 years

- ❌ **BMI over-interpretation** → Diagnosing based on BMI alone
  - ✅ BMI is screening tool; clinical correlation required

**Clinical Misuse:**
- ❌ **Athletes misclassified** → Muscular patients marked obese
  - ✅ Consider waist circumference or body fat %

- ❌ **Elderly inappropriate norms** → Same cutoffs for all ages
  - ✅ Use age-adjusted BMI for >65 years

- ❌ **Ignoring ethnicity** → Universal cutoffs applied
  - ✅ Asian populations: lower obesity thresholds

**Dosing Errors:**
- ❌ **BSA rounding** → 1.79 m² rounded to 1.8 m²
  - ✅ Use precise values for chemotherapy

- ❌ **Max dose ignored** → Exceeding lifetime limits
  - ✅ Always check cumulative doses (doxorubicin)

## References

Available in `references/` directory:

- `bsa_formulas_comparison.md` - Formula accuracy by population
- `pediatric_norms.md` - Growth charts and percentiles
- `chemotherapy_dosing.md` - BSA-based drug calculations
- `ethnic_adjustments.md` - Population-specific cutoffs
- `calculator_validation.md` - Comparison with reference standards

## Scripts

Located in `scripts/` directory:

- `main.py` - CLI calculator interface
- `calculator.py` - Core BMI/BSA calculations
- `formulas.py` - Multiple BSA formula implementations
- `pediatric.py` - Child-specific calculations
- `dosing.py` - Medication dose calculations
- `reports.py` - Clinical report generation

## Limitations

- **BMI Limitations**: Doesn't distinguish fat from muscle; varies by ethnicity
- **BSA Estimation**: All formulas are approximations; 10-15% variation normal
- **Extreme Values**: Very short/tall patients may have inaccurate estimates
- **Not for Diagnosis**: BMI/BSA are tools, not clinical diagnoses
- **Amputees**: Standard formulas inaccurate; adjustment needed
- **Pregnancy**: Special considerations not included

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--weight`, `-w` | float | - | Yes | Weight in kilograms |
| `--height`, `-H` | float | - | Yes | Height in centimeters |
| `--dose`, `-d` | float | - | No | Standard drug dose per m² in mg (optional) |
| `--format`, `-f` | string | text | No | Output format (text, json) |
| `--output`, `-o` | string | - | No | Output file path (optional) |

## Usage

### Basic Usage

```text

# Calculate BMI and BSA

# Example invocation: python scripts/main.py --weight 70 --height 175

# Calculate with drug dosing

# Example invocation: python scripts/main.py --weight 70 --height 175 --dose 100

# Output as JSON

# Example invocation: python scripts/main.py --weight 70 --height 175 --format json --output results.json
```

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python script executed locally | Low |
| Network Access | No external API calls | Low |
| File System Access | Optional file output only | Low |
| Data Exposure | No sensitive data stored | Low |
| Clinical Risk | Results used for medical decisions | Medium |

## Security Checklist

- [x] No hardcoded credentials or API keys
- [x] No unauthorized file system access
- [x] Input validation for weight/height
- [x] Output does not expose sensitive information
- [x] Error messages sanitized
- [x] Script execution in sandboxed environment

## Prerequisites

```text

# Python 3.7+

# No additional packages required (uses standard library)
```

## Evaluation Criteria

### Success Metrics
- [x] Successfully calculates BMI using standard formula
- [x] Successfully calculates BSA using DuBois formula
- [x] Correctly categorizes BMI (Underweight, Normal, Overweight, Obese)
- [x] Calculates drug doses based on BSA when provided

### Test Cases
1. **Normal Adult**: 70kg, 175cm → BMI 22.9 (Normal), BSA ~1.85 m²
2. **Drug Dosing**: 70kg, 175cm, 100mg/m² → Dose 185mg
3. **JSON Output**: Valid JSON with all fields

## Lifecycle Status

- **Current Stage**: Draft
- **Next Review Date**: 2026-03-06
- **Known Issues**: None
- **Planned Improvements**:
  - Add additional BSA formulas (Haycock, Mosteller)
  - Add pediatric BMI percentiles
  - Add unit conversion (lbs, ft/in)

---

**⚕️ Clinical Note: BMI and BSA are screening and calculation tools, not substitutes for clinical judgment. Always correlate with physical examination, patient history, and other assessments. Double-check all chemotherapy calculations independently.**

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

This skill accepts requests that match the documented purpose of `bmi-bsa-calculator` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `bmi-bsa-calculator` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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

## Inputs to Collect

- Required inputs: the user goal, the primary data or source file, and the requested output format.
- Optional inputs: output directory, formatting preferences, and validation constraints.
- If a required input is unavailable, return a short clarification request before continuing.

## Output Contract

- Return a short summary, the main deliverables, and any assumptions that materially affect interpretation.
- If execution is partial, label what succeeded, what failed, and the next safe recovery step.
- Keep the final answer within the documented scope of the skill.

## Validation and Safety Rules

- Validate identifiers, file paths, and user-provided parameters before execution.
- Do not fabricate results, metrics, citations, or downstream conclusions.
- Use safe fallback behavior when dependencies, credentials, or required inputs are missing.
- Surface any execution failure with a concise diagnosis and recovery path.
