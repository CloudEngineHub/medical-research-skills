# Audit Reference

## Scope

- Flow-cytometry panel planning
- Marker and fluorophore assignment
- Spillover-aware panel review

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If marker or instrument details are incomplete, the skill should still return:

- the missing panel inputs
- a provisional panel-planning structure
- assumptions affecting fluorophore selection
- the next checks before accepting a final panel design
