# Audit Reference

## Scope

- Docking-input preparation planning
- Grid-box and active-site configuration review
- AutoDock and Vina configuration workflow framing

## Supported Audit Paths

- `python -m py_compile scripts/main.py`
- `python scripts/smoke_test.py`

## Fallback Boundary

If receptor or ligand inputs are incomplete, the skill should still return:

- the missing structure inputs
- the docking configuration steps that can still be drafted safely
- assumptions affecting box placement or software choice
- the next checks before accepting a final docking configuration
