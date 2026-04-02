---
name: data-management-plan-creator
description: Automatically generate draft Data Management and Sharing Plans (DMSP) compliant with NIH 2023 policy requirements and FAIR principles.
license: MIT
skill-author: AIPOCH
---
# Data Management Plan (DMP) Creator

Automatically generate draft Data Management and Sharing Plans (DMSP) compliant with NIH 2023 policy requirements and FAIR principles.

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

- Use this skill when the task needs Automatically generate draft Data Management and Sharing Plans (DMSP) compliant with NIH 2023 policy requirements and FAIR principles.
- Use this skill for protocol design tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Overview

This Skill generates comprehensive Data Management and Sharing Plans (DMSP) that meet NIH's 2023 Final Policy for Data Management and Sharing. The output follows FAIR principles (Findable, Accessible, Interoperable, Reusable) to ensure research data is properly managed and shared.

## Requirements

- Python 3.8+
- No external dependencies required (uses standard library only)

## Usage

### Command Line

```text
python scripts/main.py \
    --project-title "Your Research Project Title" \
    --pi-name "Principal Investigator Name" \
    --data-types "genomic,imaging,clinical" \
    --repository "GEO,Figshare" \
    --output dmsp_draft.md
```

### Interactive Mode

```text
python scripts/main.py --interactive
```

### As a Module

```python
from scripts.main import DMSPCreator

creator = DMSPCreator(
    project_title="Cancer Genomics Study",
    pi_name="Dr. Jane Smith",
    institution="National Cancer Institute",
    data_types=["genomic sequencing", "clinical metadata"],
    estimated_size_gb=500,
    repositories=["dbGaP", "GEO"],
    sharing_timeline="6 months after study completion"
)

dmsp = creator.generate_plan()
creator.save_to_file("dmsp_output.md")
```

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--project-title` | string | - | Yes | Title of the research project |
| `--pi-name` | string | - | Yes | Name of the Principal Investigator |
| `--institution` | string | - | Yes | Research institution or organization |
| `--data-types` | string | - | Yes | Comma-separated list of data types (e.g., "genomic,imaging,clinical") |
| `--estimated-size` | float | - | No | Estimated data size in GB |
| `--repository` | string | - | Yes | Comma-separated list of target repositories |
| `--sharing-timeline` | string | No later than the end of the award period | No | When data will be shared |
| `--access-restrictions` | string | - | No | Any access restrictions (e.g., "controlled-access for sensitive data") |
| `--format-standards` | string | - | No | Data format standards to be used |
| `--output` | string | dmsp_[timestamp].md | No | Output file path |
| `--interactive` | flag | - | No | Run in interactive mode |

## NIH DMSP Required Elements

The generated plan addresses all six required elements per NIH policy:

1. **Data Type** - Types and estimated amount of scientific data
2. **Related Tools, Software and/or Code** - Tools needed to access/manipulate data
3. **Standards** - Standards for data/metadata to be applied
4. **Data Preservation, Access, and Associated Timelines** - Repository selection and sharing timeline
5. **Access, Distribution, or Reuse Considerations** - Factors affecting subsequent access
6. **Oversight of Data Management and Sharing** - Plans for compliance monitoring

## FAIR Principles Implementation

### Findable
- Persistent identifiers (DOIs)
- Rich metadata with standard vocabularies
- Registration in searchable repositories

### Accessible
- Standardized communication protocols
- Metadata available even if data is no longer available
- Access procedures clearly documented

### Interoperable
- Standard data formats
- Standard terminologies and vocabularies
- Qualified references to other data

### Reusable
- Detailed provenance information
- Clear usage licenses
- Domain-relevant community standards

## Example Output

The generated DMSP includes:
- Executive summary
- NIH-compliant section headers
- Specific language for data type descriptions
- FAIR-aligned metadata standards
- Repository recommendations
- Timeline for data sharing
- Access control procedures
- Roles and responsibilities

## References

- [NIH Data Management and Sharing Policy](https://sharing.nih.gov/data-management-and-sharing-policy)
- [NIH DMSP Template](references/nih_dmp_template.md)
- [FAIR Principles](https://www.go-fair.org/fair-principles/)

## License

MIT License - See project root for details.

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

This skill accepts requests that match the documented purpose of `data-management-plan-creator` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `data-management-plan-creator` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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
