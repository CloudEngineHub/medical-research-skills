---
name: in-silico-perturbation-oracle
description: Plan virtual gene perturbation studies with foundation-model workflows, bounded assumptions, and structured validation checkpoints for protocol design tasks.
license: MIT
skill-author: AIPOCH
---
# In Silico Perturbation Oracle

**ID:** 207  
**Category:** Protocol Design  
**Status:** Draft

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

- Use this skill when the task needs a virtual gene knockout or knockdown protocol framed before wet-lab execution.
- Use this skill for protocol design tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a fallback path for missing model inputs, unavailable datasets, or incomplete perturbation parameters.

## Workflow

1. Confirm the study objective, target genes, cell type, perturbation mode, and model family before detailed work.
2. Validate that the request stays within in silico perturbation planning and does not overclaim biological certainty.
3. Use the packaged script path or the reasoning path with only the inputs that are actually available.
4. Return a structured output that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Overview

This skill supports virtual perturbation planning with biological foundation models such as Geneformer or scGPT. It is designed for target-screening and experimental prioritization tasks where the user needs a bounded simulation plan, explicit assumptions, and interpretable next steps before investing in wet-lab validation.

## Supported Scope

- Virtual gene knockout, knockdown, or overexpression planning
- Cell-state response hypothesis generation
- Differential expression and pathway follow-up planning
- Prioritization of candidate targets for validation

## Inputs

Required inputs:

- `cell_type`
- `perturbation_type`
- one of `genes` or `genes_file`

Optional inputs:

- `model`
- `pathways`
- `top_k`
- `output`

## Output Requirements

Every substantial response should make these items explicit:

1. Objective
2. Inputs Received
3. Assumptions
4. Perturbation Plan
5. Validation Plan
6. Risks and Limits
7. Next Checks

## Guardrails

- Do not claim experimental truth from an in silico model alone.
- Do not fabricate differential-expression results, pathway enrichments, or validation outcomes.
- Keep model limitations, data constraints, and wet-lab dependency visible.
- Stop if the request requires unsupported causal claims or clinical recommendations.

## Example Commands

```text
python scripts/main.py --model geneformer --genes TP53,BRCA1 --cell-type lung_adenocarcinoma --output ./results/
python scripts/main.py --model scgpt --genes-file ./target_genes.txt --cell-type hepatocyte --top-k 20 --pathways KEGG,GO_BP --output ./results/
```

## Recommended Deliverable Template

Use this structure when the request is non-trivial:

1. Objective
2. Inputs Received
3. Assumptions
4. Model and Perturbation Setup
5. Expected Readouts
6. Validation and Follow-up
7. Risks and Limits
8. Next Checks

## Error Handling

- If required perturbation inputs are missing, state exactly which fields are missing.
- If the request goes outside the documented scope, stop instead of widening the task silently.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Input Validation

This skill accepts requests that match the documented purpose of `in-silico-perturbation-oracle` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `in-silico-perturbation-oracle` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

## References

- [references/audit-reference.md](references/audit-reference.md) - Supported perturbation scope, audit commands, and fallback boundaries

## Response Template

For non-trivial requests, keep the answer in this fixed order:

1. Objective
2. Inputs Received
3. Assumptions
4. Perturbation Plan
5. Validation Plan
6. Risks and Limits
7. Next Checks
