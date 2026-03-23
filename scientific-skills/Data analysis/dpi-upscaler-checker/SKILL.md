---
name: dpi-upscaler-checker
description: Check if images meet 300 DPI printing standards, and intelligently restore blurry low-resolution images using AI super-resolution technology.
license: MIT
skill-author: AIPOCH
---
# DPI Upscaler & Checker

Check if images meet 300 DPI printing standards, and intelligently restore blurry low-resolution images using AI super-resolution technology.

## When to Use

- Use this skill when the task needs Check if images meet 300 DPI printing standards, and intelligently restore blurry low-resolution images using AI super-resolution technology.
- Use this skill for data analysis tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Key Features

See `## Features` above for related details.

- Scope-focused workflow aligned to: Check if images meet 300 DPI printing standards, and intelligently restore blurry low-resolution images using AI super-resolution technology.
- Packaged executable path(s): `scripts/main.py`.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

- Python >= 3.8
- Pillow >= 9.0.0
- opencv-python >= 4.5.0
- numpy >= 1.21.0
- realesrgan (optional, for best results)

## Example Usage

See `## Usage` above for related details.

```bash
cd "20260318/scientific-skills/Data Analytics/dpi-upscaler-checker"
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
python scripts/main.py --input "Audit validation sample with explicit symptoms, history, assessment, and next-step plan."
```

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Features

- **DPI Detection**: Read and verify image DPI information
- **Intelligent Analysis**: Calculate actual print size and pixel density
- **Super-Resolution Restoration**: Use Real-ESRGAN algorithm to enhance image clarity
- **Batch Processing**: Support single image and batch folder processing
- **Format Support**: JPG, PNG, TIFF, BMP, WebP

## Use Cases

- Academic paper figure DPI checking
- Print image quality pre-inspection
- Low-resolution material restoration
- Document scan enhancement

## Usage

### Check Single Image DPI
```text
python scripts/main.py check --input image.jpg
```

### Batch Check Folder
```text
python scripts/main.py check --input ./images/ --output report.json
```

### Super-Resolution Restoration
```text
python scripts/main.py upscale --input image.jpg --output upscaled.jpg --scale 4
```

### Batch Fix Low DPI Images
```text
python scripts/main.py upscale --input ./images/ --output ./output/ --min-dpi 300 --scale 2
```

## Parameters

### Check Command
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--input` | string | - | Yes | Input image path or folder |
| `--output` | string | stdout | No | Output report path |
| `--target-dpi` | int | 300 | No | Target DPI threshold |

### Upscale Command
| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--input` | string | - | Yes | Input image path or folder |
| `--output` | string | - | Yes | Output path |
| `--scale` | int | 2 | No | Scale factor (2/3/4) |
| `--min-dpi` | int | - | No | Only process images below this DPI |
| `--denoise` | int | 0 | No | Denoise level (0-3) |
| `--face-enhance` | flag | false | No | Enable face enhancement |

## Output Description

### DPI Check Report
```json
{
  "file": "image.jpg",
  "dpi": [72, 72],
  "width_px": 1920,
  "height_px": 1080,
  "print_width_cm": 67.7,
  "print_height_cm": 38.1,
  "meets_300dpi": false,
  "recommended_scale": 4.17
}
```

### Restored Image
- Automatically saved as `<original_filename>_upscaled.<extension>`
- Preserves original EXIF information
- Sets DPI to 300

## Algorithm Description

### DPI Calculation
```
Actual DPI = Pixel dimensions / Physical dimensions
Print size (cm) = Pixel count / DPI * 2.54
```

### Super-Resolution
- Default use of Real-ESRGAN model
- Support lightweight bicubic interpolation fallback
- Intelligent model selection (general/anime/face)

## Notes

1. Input image DPI information may be inaccurate; actual pixel calculation shall prevail
2. Super-resolution cannot create non-existent information; extremely blurry images have limited improvement
3. Large file processing requires more memory
4. GPU acceleration requires CUDA environment (optional)

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

This skill accepts requests that match the documented purpose of `dpi-upscaler-checker` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `dpi-upscaler-checker` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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
