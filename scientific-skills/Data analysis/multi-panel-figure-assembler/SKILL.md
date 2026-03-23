---
name: multi-panel-figure-assembler
description: Analyze data with `multi-panel-figure-assembler` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation.
license: MIT
skill-author: AIPOCH
---
# Multi-panel Figure Assembler

A Python-based tool for assembling multi-panel scientific figures. Automatically arranges 6 sub-figures (A-F) into a composite image with consistent styling, labels, and high-resolution output.

## When to Use

- Use this skill when the task needs Automatically assemble 6 sub-figures (A-F) into a high-resolution composite.
- Use this skill for data analysis tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Key Features

See `## Features` above for related details.

- Scope-focused workflow aligned to: Analyze data with `multi-panel-figure-assembler` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation.
- Packaged executable path(s): `scripts/__init__.py` plus 2 additional script(s).
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

See `## Prerequisites` above for related details.

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `numpy`: `unspecified`. Declared in `requirements.txt`.
- `pil`: `unspecified`. Declared in `requirements.txt`.
- `pillow`: `unspecified`. Declared in `requirements.txt`.

## Example Usage

See `## Usage` above for related details.

```bash
cd "20260318/scientific-skills/Data Analytics/multi-panel-figure-assembler"
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
- Primary implementation surface: `scripts/__init__.py` with additional helper scripts under `scripts/`.
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
python scripts/main.py --input "Audit validation sample with explicit symptoms, history, assessment, and next-step plan."
```

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Features

- **Automatic Layout**: Supports 2×3 or 3×2 grid arrangements
- **Edge Alignment**: Intelligently crops/pads images to match dimensions
- **Unified Typography**: Consistent font sizing across all panels
- **Auto Labeling**: Adds panel labels (A-F) with customizable position
- **High Resolution**: Output at 300+ DPI for publication quality

## Installation

Requires Python 3.8+ and the following packages:

```text
pip install Pillow numpy
```

Optional for advanced features:
```text
pip install opencv-python-headless
```

## Usage

```text
python scripts/main.py --input A.png B.png C.png D.png E.png F.png --output figure.png [OPTIONS]
```

### Command Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` / `-i` | Yes | - | 6 input image paths (A-F) |
| `--output` / `-o` | Yes | - | Output file path |
| `--layout` / `-l` | No | `2x3` | Layout: `2x3` or `3x2` |
| `--dpi` / `-d` | No | `300` | Output DPI (dots per inch) |
| `--label-font` | No | `Arial` | Font family for labels |
| `--label-size` | No | `24` | Font size for panel labels |
| `--label-position` | No | `topleft` | Label position: `topleft`, `topright`, `bottomleft`, `bottomright` |
| `--padding` / `-p` | No | `10` | Padding between panels (pixels) |
| `--border` / `-b` | No | `2` | Border width around each panel (pixels) |
| `--bg-color` | No | `white` | Background color (white/black/hex) |
| `--label-color` | No | `black` | Label text color (black/white/hex) |

#

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--input` | str | Required |  |
| `--output` | str | Required | Output file path |
| `--layout` | str | "2x3" |  |
| `--dpi` | int | 300 |  |
| `--label-font` | str | "Arial" |  |
| `--label-size` | int | 24 |  |
| `--label-position` | str | "topleft" |  |
| `--padding` | int | 10 |  |
| `--border` | int | 2 |  |
| `--bg-color` | str | "white" |  |
| `--label-color` | str | "black" |  |

## Examples

**Basic usage:**
```text
python scripts/main.py -i A.png B.png C.png D.png E.png F.png -o figure.png
```

**3×2 layout with custom DPI:**
```text
python scripts/main.py -i A.png B.png C.png D.png E.png F.png -o figure.png --layout 3x2 --dpi 600
```

**Custom styling:**
```text
python scripts/main.py -i A.png B.png C.png D.png E.png F.png -o figure.png \
  --label-size 32 --label-position topright --padding 20 --border 4
```

**Programmatic usage:**
```python
from scripts.main import FigureAssembler

assembler = FigureAssembler(
    layout="2x3",
    dpi=300,
    label_size=24,
    padding=10
)

assembler.assemble(
    inputs=["A.png", "B.png", "C.png", "D.png", "E.png", "F.png"],
    output="figure.png",
    labels=["A", "B", "C", "D", "E", "F"]
)
```

## Output

The script generates a high-resolution composite figure with:
- All panels resized to uniform dimensions
- Panel labels (A-F) in specified positions
- Consistent padding and borders
- DPI metadata embedded in output file

## Supported Formats

**Input:** PNG, JPG, JPEG, BMP, TIFF, GIF
**Output:** PNG (recommended), JPG, TIFF

## Notes

- Input images are automatically resized to match the largest dimension while maintaining aspect ratio
- For best results, use input images with similar aspect ratios
- Label fonts require the font to be available on your system
- PNG output preserves transparency if any input images have alpha channels

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

This skill accepts requests that match the documented purpose of `multi-panel-figure-assembler` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `multi-panel-figure-assembler` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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
