# Audit Reference

## Scope

- Clinical trial dashboard planning
- Enrollment and AE monitoring layout sketches
- Monitoring-metric presentation for protocol or operations review

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If study inputs are incomplete, the skill should still return:

- the missing study parameters
- the dashboard modules that can still be drafted safely
- assumptions introduced for mock layout planning
- the next checks before generating a final dashboard file
