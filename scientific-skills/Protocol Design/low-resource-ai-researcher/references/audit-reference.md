# Audit Reference

This reference file exists to keep the skill package audit-complete and self-describing.

## Scope

- Low-resource medical LLM adaptation planning
- LoRA and QLoRA protocol selection
- Dataset readiness and validation planning
- Risk-aware fallback handling

## Audit Notes

- Audit commands use `scripts/smoke_test.py` for deterministic validation.
- The main training implementation remains in `scripts/main.py`.
- Responses should keep assumptions, limits, and unresolved items explicit.
