#!/usr/bin/env python3
"""Deterministic smoke test for audit validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        ROOT_DIR / "SKILL.md",
        ROOT_DIR / "scripts" / "main.py",
    ]
    missing = [str(path.relative_to(ROOT_DIR)) for path in required if not path.exists()]
    payload = {
        "skill": "serial-dilution-calculator",
        "workspace_ready": not missing,
        "missing_files": missing,
        "supported_outputs": ["pipetting scheme", "required volumes", "layout suggestion"],
        "fallback_reason": "Use deterministic smoke validation when runtime dilution parameters are unavailable.",
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
