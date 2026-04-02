# Audit Reference

## Scope

- Synthetic biology circuit planning
- Circuit-component and host-system review
- Validation checkpoint definition

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If required inputs are incomplete, the skill should still return:

- the missing required inputs
- the parts of the workflow that can still be completed safely
- assumptions that need confirmation before execution
- the next checks before accepting a final circuit design
