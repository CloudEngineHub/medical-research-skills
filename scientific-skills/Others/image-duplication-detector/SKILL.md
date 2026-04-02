---
name: image-duplication-detector
description: Detect image duplication and tampering in manuscript figures using computer.
license: MIT
skill-author: AIPOCH
---
# Image Duplication Detector

ID: 195

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

## When to Use

- Use this skill when the task is to Detect image duplication and tampering in manuscript figures using computer.
- Use this skill for other tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Description

Uses Computer Vision (CV) algorithms to scan all images in paper manuscripts to detect potential duplication or local tampering (PS traces).

## Usage

```text
# Scan single PDF file
python scripts/main.py --input paper.pdf --output report.json

# Scan image folder
python scripts/main.py --input ./images/ --output report.json

# Specify similarity threshold (default 0.85)
python scripts/main.py --input paper.pdf --threshold 0.90 --output report.json

# Enable tampering detection
python scripts/main.py --input paper.pdf --detect-tampering --output report.json

# Generate visualization report
python scripts/main.py --input paper.pdf --visualize --output report.json
```

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--input` | string | - | Yes | Input PDF file or image folder path |
| `--output` | string | report.json | No | Output report path |
| `--threshold` | float | 0.85 | No | Similarity threshold (0-1), higher is stricter |
| `--detect-tampering` | flag | false | No | Enable tampering/PS trace detection |
| `--visualize` | flag | false | No | Generate visualization comparison images |
| `--temp-dir` | string | ./temp | No | Temporary file directory |

## Output Format

```json
{
  "summary": {
    "total_images": 12,
    "duplicates_found": 2,
    "tampering_detected": 1,
    "processing_time": "3.5s"
  },
  "duplicates": [
    {
      "group_id": 1,
      "similarity": 0.98,
      "images": [
        {"page": 2, "index": 1, "path": "..."},
        {"page": 5, "index": 3, "path": "..."}
      ]
    }
  ],
  "tampering": [
    {
      "image": "page_3_img_2.png",
      "suspicious_regions": [
        {"x": 120, "y": 80, "width": 50, "height": 50, "confidence": 0.92}
      ]
    }
  ]
}
```

## Requirements

```
opencv-python>=4.8.0
numpy>=1.24.0
Pillow>=10.0.0
PyPDF2>=3.0.0
pdf2image>=1.16.0
imagehash>=4.3.0
scikit-image>=0.21.0
matplotlib>=3.7.0
```

## Algorithm Details

### Duplication Detection
- **Perceptual Hashing**: Uses pHash, dHash, aHash combination to detect visually similar images
- **Feature Matching**: ORB feature point matching to verify similarity
- **SSIM**: Structural similarity index as auxiliary verification

### Tampering Detection
- **ELA (Error Level Analysis)**: Detects JPEG compression level inconsistencies
- **Noise Analysis**: Noise pattern anomaly detection
- **Copy-Move Detection**: Copy-move forgery detection
- **Lighting Inconsistency**: Lighting consistency analysis

## Example

```python
from scripts.main import ImageDuplicationDetector

detector = ImageDuplicationDetector(
    threshold=0.85,
    detect_tampering=True
)

results = detector.scan("paper.pdf")
detector.save_report(results, "report.json")
```

## Notes

- Supports PDF, PNG, JPG, TIFF formats
- Large files recommended for batch processing
- Tampering detection may produce false positives, manual review recommended

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

This skill accepts requests that match the documented purpose of `image-duplication-detector` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `image-duplication-detector` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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
