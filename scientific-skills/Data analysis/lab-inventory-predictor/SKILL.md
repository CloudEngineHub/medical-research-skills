---
name: lab-inventory-predictor
description: Predict depletion time of critical lab reagents based on experimental.
license: MIT
skill-author: AIPOCH
---
# Lab Inventory Predictor

## When to Use

- Use this skill when the task is to Predict depletion time of critical lab reagents based on experimental.
- Use this skill for data analysis tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Key Features

- Scope-focused workflow aligned to: Predict depletion time of critical lab reagents based on experimental.
- Packaged executable path(s): `scripts/main.py`.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

- Python >= 3.8
- No external dependencies (uses only standard library)

## Example Usage

See `## Usage` above for related details.

```bash
cd "20260318/scientific-skills/Data Analytics/lab-inventory-predictor"
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

## Function Overview

This skill is used for laboratory inventory management, predicting reagent depletion time by analyzing historical usage frequency, and automatically generating reminders when purchases are needed.

## Core Capabilities

1. **Inventory Tracking** - Record current reagent stock levels
2. **Usage Frequency Analysis** - Calculate consumption rate based on experiment records
3. **Depletion Prediction** - Predict reagent depletion date based on consumption rate
4. **Purchase Alerts** - Generate alerts before reagents are about to deplete
5. **Safety Stock Alerts** - Alert when inventory falls below safety threshold

## Usage

### Command Line Call

```text

# View all reagent status
openclaw skill lab-inventory-predictor --action status

# Add or update reagent information
openclaw skill lab-inventory-predictor --action add-reagent \
  --name "PBS Buffer" \
  --current-stock 500 \
  --unit "ml" \
  --safety-days 7

# Record experiment consumption
openclaw skill lab-inventory-predictor --action record-usage \
  --name "PBS Buffer" \
  --amount 50 \
  --experiment "Cell Culture Experiment #2024-001"

# Get purchase alerts
openclaw skill lab-inventory-predictor --action alerts

# Generate prediction report
openclaw skill lab-inventory-predictor --action report
```

### Python API

```python
from skills.lab_inventory_predictor import InventoryPredictor

# Initialize
predictor = InventoryPredictor("/path/to/inventory.json")

# Add reagent
predictor.add_reagent(
    name="PBS Buffer",
    current_stock=500,
    unit="ml",
    safety_days=7,
    lead_time_days=3
)

# Record usage
predictor.record_usage("PBS Buffer", 50, "Experiment #001")

# Get prediction
prediction = predictor.predict_depletion("PBS Buffer")
print(f"Predicted depletion time: {prediction['depletion_date']}")

# Get purchase alerts
alerts = predictor.get_alerts()
```

## Parameters

### Global Parameters
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--action` | string | - | Yes | Action to perform (status, add-reagent, record-usage, alerts, report) |
| `--data-file` | string | ~/.openclaw/workspace/data/lab-inventory.json | No | Path to inventory data file |

### add-reagent Action
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--name` | string | - | Yes | Reagent name |
| `--current-stock` | float | - | Yes | Current stock quantity |
| `--unit` | string | - | Yes | Unit of measurement (ml, mg, etc.) |
| `--safety-days` | int | 7 | No | Safety buffer days |
| `--lead-time-days` | int | 3 | No | Expected delivery time |
| `--safety-stock` | float | - | No | Safety stock threshold |

### record-usage Action
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--name` | string | - | Yes | Reagent name |
| `--amount` | float | - | Yes | Amount consumed |
| `--experiment` | string | - | No | Experiment identifier |

### report Action
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--output`, `-o` | string | stdout | No | Output file path |
| `--format` | string | text | No | Output format (text, json, csv) |

## Data Structure

### Reagent Record

```json
{
  "name": "PBS Buffer",
  "current_stock": 500,
  "unit": "ml",
  "safety_stock": 100,
  "safety_days": 7,
  "lead_time_days": 3,
  "usage_history": [
    {
      "date": "2024-01-15",
      "amount": 50,
      "experiment": "Cell Culture #001"
    }
  ],
  "daily_consumption_rate": 10.5,
  "predicted_depletion_date": "2024-02-01",
  "last_updated": "2024-01-15T10:30:00"
}
```

## Prediction Algorithm

### Consumption Rate Calculation

```
daily_consumption = Σ(usage_amount) / days_span
```

### Depletion Date Prediction

```
days_until_depletion = current_stock / daily_consumption
depletion_date = today + days_until_depletion
```

### Purchase Alert Trigger Conditions

1. **Based on depletion time**: When `days_until_depletion <= safety_days + lead_time_days`
2. **Based on safety stock**: When `current_stock <= safety_stock`

## Configuration File

Default data storage location: `~/.openclaw/workspace/data/lab-inventory.json`

Configuration example:

```json
{
  "settings": {
    "default_safety_days": 7,
    "default_lead_time_days": 3,
    "prediction_lookback_days": 30
  },
  "reagents": []
}
```

## Version History

- v1.0.0 (2024-02) - Initial version, supports basic prediction and alert functions

---

**Author**: OpenClaw Skill Framework  
**License**: MIT

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

This skill accepts requests that match the documented purpose of `lab-inventory-predictor` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `lab-inventory-predictor` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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
