# Audit Reference

## Scope

- Western blot troubleshooting planning
- Failure-mode diagnosis workflow
- Corrective-action checkpoint review

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If required inputs are incomplete, the skill should still return:

- the missing required inputs
- the parts of the workflow that can still be completed safely
- assumptions that need confirmation before execution
- the next checks before accepting a final troubleshooting recommendation
