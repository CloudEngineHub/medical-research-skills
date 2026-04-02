# Audit Reference

## Scope

- ELN template drafting
- Experiment-record structure planning
- Lab notebook section standardization

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If experiment metadata is incomplete, the skill should still return:

- the missing template fields
- the standard sections that can be generated safely
- assumptions introduced for template drafting
- the next checks before finalizing the ELN template
