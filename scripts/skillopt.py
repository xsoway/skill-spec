#!/usr/bin/env python3
"""Safe SkillOpt adapter: preflight first; training never overwrites stable Skill files."""
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path


REQUIRED_OPT = ("optimization/contract.md", "optimization/seed_skill.md", "optimization/train.jsonl", "optimization/validation.jsonl", "optimization/heldout.jsonl", "optimization/config.yaml", "optimization/promotion-record.md")


def preflight(skill_dir: Path) -> list[str]:
    missing = [item for item in REQUIRED_OPT if not (skill_dir / item).is_file()]
    if missing:
        return ["missing " + item for item in missing]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or explicitly run SkillOpt against an optimization-ready Skill.")
    parser.add_argument("action", choices=("preflight", "run"))
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--execute", action="store_true", help="Required before training.")
    args = parser.parse_args()
    skill_dir = args.skill_dir.resolve()
    issues = preflight(skill_dir)
    if issues:
        print("SKILLOPT_NOT_READY: " + "; ".join(issues))
        return 0 if args.action == "preflight" else 2
    if args.action == "preflight":
        print("SKILLOPT_READY: candidate may be trained only after explicit approval")
        return 0
    if not args.execute:
        print("REFUSED: SkillOpt training requires --execute and must not overwrite stable files", file=sys.stderr)
        return 2
    if importlib.util.find_spec("skillopt") is None:
        print("SKILLOPT_NOT_INSTALLED: cannot train", file=sys.stderr)
        return 2
    workspace = skill_dir.parent / ".skillopt-workspaces" / skill_dir.name
    workspace.mkdir(parents=True, exist_ok=True)
    config = skill_dir / "optimization/config.yaml"
    return subprocess.run([sys.executable, "-m", "skillopt.run", "--config", str(config)], cwd=workspace, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
