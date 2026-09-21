#!/usr/bin/env python3
"""Safe Skill-up adapter: static validation by default, model run only explicitly."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from validate_skill_package import main as validate_package


def package_ok(skill_dir: Path) -> bool:
    old_argv = sys.argv
    try:
        sys.argv = ["validate_skill_package.py", str(skill_dir)]
        return validate_package() == 0
    finally:
        sys.argv = old_argv


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate or explicitly run Skill-up for one Skill package.")
    parser.add_argument("action", choices=("validate", "run"))
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--execute", action="store_true", help="Required before model-consuming run.")
    parser.add_argument("--engine", default="codex")
    args = parser.parse_args()
    skill_dir = args.skill_dir.resolve()
    if not package_ok(skill_dir):
        return 1
    eval_file = skill_dir / "evals/eval.yaml"
    cli = shutil.which("skill-up")
    if args.action == "validate":
        if not cli:
            print("SKILL_UP_NOT_INSTALLED: static package validation passed; external eval schema not run")
            return 0
        return subprocess.run([cli, "validate", str(eval_file)], check=False).returncode
    if not args.execute:
        print("REFUSED: Skill-up run requires --execute because it may consume model resources", file=sys.stderr)
        return 2
    if not cli:
        print("SKILL_UP_NOT_INSTALLED: cannot run model evaluation", file=sys.stderr)
        return 2
    output = skill_dir.parent / ".skill-up-workspaces" / skill_dir.name
    output.mkdir(parents=True, exist_ok=True)
    command = [cli, "run", str(eval_file), "--engine", args.engine, "--output-dir", str(output)]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
