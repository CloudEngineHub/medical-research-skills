# Audit Reference

## Scope

- Patient digital-twin planning
- Dose and toxicity simulation setup
- Virtual regimen comparison in protocol design contexts

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If patient or drug inputs are incomplete, the skill should still return:

- the missing input artifacts
- the simulation outputs that cannot be estimated safely
- assumptions required for a virtual trial setup
- the next checks before running a full digital-twin simulation
