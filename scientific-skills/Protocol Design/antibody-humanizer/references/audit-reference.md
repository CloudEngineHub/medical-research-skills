# Audit Reference

## Scope

- Antibody humanization planning
- CDR grafting workflow framing
- Immunogenicity and back-mutation review

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/main.py --help`
- `python scripts/main.py -h`

## Fallback Boundary

If sequence or template inputs are incomplete, the skill should still return:

- the missing heavy-chain or light-chain inputs
- the humanization steps that can still be outlined safely
- assumptions affecting framework selection
- the next checks before accepting a final humanized candidate
