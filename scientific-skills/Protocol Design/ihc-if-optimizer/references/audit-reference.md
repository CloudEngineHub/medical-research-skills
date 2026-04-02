# Audit Reference

## Scope

- IHC and IF protocol optimization
- Stain-condition planning
- Control and troubleshooting guidance

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If required inputs are incomplete, the skill should still return:

- the missing required inputs
- the parts of the workflow that can still be completed safely
- assumptions that need confirmation before execution
- the next checks before accepting a final stain optimization plan
