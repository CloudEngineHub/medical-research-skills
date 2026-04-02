# Audit Reference

## Scope

- Serial dilution planning
- Stepwise concentration workflow framing
- Pipetting-scheme and layout preparation

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/smoke_test.py`

## Fallback Boundary

If dilution inputs are incomplete, the skill should still return:

- the missing concentration or volume inputs
- the steps that can still be calculated safely
- assumptions affecting dilution-factor planning
- the next checks before accepting a final dilution scheme
