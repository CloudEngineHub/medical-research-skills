# Audit Reference

## Scope

- Primer validation planning
- Basic in silico primer quality review
- Tm, GC, and structure-check workflow framing

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If primer or template inputs are incomplete, the skill should still return:

- the missing sequence inputs
- the checks that can still be performed safely
- assumptions affecting primer assessment
- the next checks before accepting a final primer set
