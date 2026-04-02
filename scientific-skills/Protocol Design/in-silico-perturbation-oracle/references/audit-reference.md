# Audit Reference

## Scope

- In silico perturbation planning
- Gene knockout or knockdown workflow framing
- Model-choice and validation-checkpoint review

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`

## Fallback Boundary

If required perturbation inputs are incomplete, the skill should still return:

- the missing gene, model, or cell-type inputs
- the steps that can still be planned safely
- assumptions affecting model interpretation
- the next checks before accepting a final perturbation plan
