---
name: low-resource-ai-researcher
description: Design, validate, and document a low-resource medical LLM fine-tuning workflow for teams that need a reproducible PEFT training plan on consumer GPUs or a single A100. This skill scopes the task, checks inputs, selects a hardware profile, defines dataset and evaluation boundaries, and returns a risk-aware execution plan with fallback guidance instead of unsupported claims.
license: MIT
skill-author: AIPOCH
---
# Skill: Low-Resource AI Researcher

**ID:** 215  
**Category:** AI/ML Research  
**Language:** Python  
**Framework:** PyTorch, Transformers, PEFT, bitsandbytes

## Quick Check

Use this command to verify that the packaged training entry point can be parsed safely.

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

Use these concrete commands for audit validation. They do not require model weights, external APIs, or optional ML dependencies.

```bash
python scripts/smoke_test.py
python scripts/smoke_test.py --mode hardware-plan
python scripts/smoke_test.py --mode dataset-check
python scripts/smoke_test.py --mode fallback
```

## When to Use

- Use this skill when you need a low-resource fine-tuning protocol for a medical or biomedical language model.
- Use this skill when the task requires explicit GPU limits, quantization choices, dataset assumptions, and evaluation checkpoints.
- Use this skill when you need a reproducible training plan that separates required inputs, optional inputs, risks, and fallback actions.
- Use this skill when the request should stay within PEFT-based planning, training setup, and validation guidance rather than unsupported medical decision-making.

## Workflow

1. Confirm the task objective, target model family, hardware envelope, dataset availability, compliance constraints, and expected deliverable.
2. Validate that the request is about training design, adaptation planning, or execution setup for medical-domain LLM work within the documented scope.
3. Select the training protocol: hardware profile, LoRA or QLoRA path, target modules, batch strategy, logging, checkpoint policy, and stop conditions.
4. Define dataset preparation, validation split, benchmark choice, and output format for assumptions, constraints, metrics, and unresolved items.
5. If required inputs are missing or execution cannot proceed, stop cleanly and return the fallback template with the exact blockers.

## Overview

This skill supports teams that want to train or adapt medical LLMs without assuming large multi-GPU clusters. It focuses on PEFT-first workflows such as LoRA and QLoRA, and turns a vague request into a bounded training protocol with hardware-aware defaults, evaluation checkpoints, and explicit safety boundaries. The packaged Python implementation is available for local extension, while the written workflow keeps the result usable even when direct execution is not possible.

## Key Features

- Low-resource training plans for RTX 3090, RTX 4090, and single A100 environments.
- Clear protocol design for LoRA, QLoRA, dataset preparation, and checkpoint strategy.
- Explicit input validation and fallback handling for missing model, data, or compliance details.
- Structured output requirements so the final answer is reusable by both an agent and a human reviewer.
- Security-oriented guidance: validate paths, avoid fabricated benchmark claims, and keep assumptions visible.

## Inputs

Required inputs for a complete run:

- `objective`: training goal such as medical QA tuning, note generation, or domain adaptation
- `base_model`: model family or checkpoint to adapt
- `hardware_profile`: available GPU memory and count
- `dataset_source`: dataset name, path, or a description of the available corpus
- `output_expectation`: expected artifact such as a training plan, config, or validation checklist

Optional but useful inputs:

- `compliance_constraints`
- `target_metrics`
- `max_context_length`
- `checkpoint_budget`
- `preferred_quantization`

## Output Requirements

Every substantial response should make these items explicit:

1. Objective
2. Inputs Received
3. Assumptions
4. Recommended Protocol
5. Validation Plan
6. Risks and Limits
7. Next Checks

## Guardrails

- Do not claim medical correctness, model accuracy, or benchmark gains that are not supported by the provided evidence.
- Do not fabricate datasets, configuration files, training logs, or successful execution outcomes.
- Validate any file path before using it and keep outputs inside the current workspace.
- Stop when the task moves from training design into medical diagnosis, patient-specific advice, or unsupported legal/compliance interpretation.
- Keep security and reproducibility visible in the final answer.

## Hardware Profiles

| Profile | GPU Memory | Recommended Method | Typical Use |
|---|---:|---|---|
| consumer-24g | 24 GB | QLoRA 4-bit | 7B to 13B planning and constrained fine-tuning |
| a100-40g | 40 GB | LoRA 8-bit or QLoRA | 13B to 34B adaptation |
| a100-80g | 80 GB | LoRA 16-bit | higher-throughput single-node training |
| multi-gpu | 2 x A100 or above | distributed LoRA | larger checkpoints or longer context windows |

## Protocol Defaults

| Setting | Default Recommendation |
|---|---|
| Adapter method | QLoRA on constrained hardware, LoRA on larger cards |
| LoRA rank | 64 |
| LoRA alpha | 128 |
| LoRA dropout | 0.05 |
| Warmup | 3 to 5 percent of total steps |
| Starting LR | `2e-4` for LoRA, `1e-4` for broader adaptation |
| Validation cadence | every fixed step window or every epoch |
| Stop rule | early stop on degraded validation trend |

## Recommended Deliverable Template

Use this structure when the request is non-trivial:

1. Objective
2. Inputs Received
3. Assumptions
4. Hardware and Quantization Plan
5. Dataset and Preprocessing Plan
6. Training Protocol
7. Validation and Monitoring
8. Risks and Limits
9. Fallback Path
10. Next Checks

## Failure and Fallback Handling

If a required input is missing, return the smallest set of missing fields and stop. If the script path cannot be executed, provide:

- the exact failed step
- the likely reason
- the parts that are still safe to complete manually
- the next command or file the user should inspect

Use this fallback sentence when needed:

> `low-resource-ai-researcher` only handles the documented low-resource medical LLM training workflow. Provide the missing required inputs or switch to a more suitable skill.

## Local Script Notes

The packaged script in `scripts/main.py` is intended as a local implementation reference for PEFT training. The audit commands use `scripts/smoke_test.py` because it is deterministic, dependency-light, and suitable for structural validation in constrained environments.

Additional implementation notes are stored in [references/audit-reference.md](references/audit-reference.md).

## Example Scenarios

Scenario A:

- Build a QLoRA plan for adapting a 7B medical QA model on a single RTX 4090.
- Define dataset split, gradient accumulation, checkpoint interval, and validation metrics.

Scenario B:

- Review whether a given dataset and hardware pair is sufficient for a 13B adaptation plan.
- Return constraints, expected tradeoffs, and a safer fallback if memory is insufficient.

Scenario C:

- Convert an incomplete training request into a bounded protocol with assumptions, blockers, and next checks.

## Reference Notes

- Prefer PEFT-first adaptation before considering full fine-tuning on constrained hardware.
- Keep benchmark language conservative unless measured outputs are provided.
- Separate protocol recommendations from execution claims.
- Re-check licensing and data governance before touching clinical corpora.

## Response Template

For non-trivial requests, keep the answer in this fixed order:

1. Objective
2. Inputs Received
3. Assumptions
4. Recommended Protocol
5. Validation Plan
6. Risks and Limits
7. Next Checks
