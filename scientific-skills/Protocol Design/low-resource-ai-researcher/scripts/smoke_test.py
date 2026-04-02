#!/usr/bin/env python3
"""Lightweight smoke checks for audit commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def build_payload(mode: str) -> dict[str, object]:
    required_paths = [
        ROOT_DIR / "SKILL.md",
        ROOT_DIR / "scripts" / "main.py",
        ROOT_DIR / "references" / "audit-reference.md",
    ]
    missing = [str(path.relative_to(ROOT_DIR)) for path in required_paths if not path.exists()]
    protocol_map = {
        "baseline": {
            "profile": "consumer-24g",
            "method": "QLoRA 4-bit",
            "focus": "deterministic audit smoke path",
        },
        "hardware-plan": {
            "profile": "a100-40g",
            "method": "LoRA 8-bit",
            "focus": "hardware sizing and checkpoint plan",
        },
        "dataset-check": {
            "profile": "consumer-24g",
            "method": "QLoRA 4-bit",
            "focus": "dataset readiness and validation split",
        },
        "fallback": {
            "profile": "unknown",
            "method": "manual review",
            "focus": "missing-input fallback template",
        },
    }
    payload = {
        "skill": "low-resource-ai-researcher",
        "mode": mode,
        "workspace_ready": not missing,
        "missing_files": missing,
        "recommended_protocol": protocol_map[mode],
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic smoke checks for low-resource-ai-researcher.")
    parser.add_argument(
        "--mode",
        choices=["baseline", "hardware-plan", "dataset-check", "fallback"],
        default="baseline",
        help="Select the audit smoke scenario to print.",
    )
    args = parser.parse_args()
    payload = build_payload(args.mode)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["workspace_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
