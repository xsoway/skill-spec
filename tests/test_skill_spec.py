from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPTS / name), *args], text=True, capture_output=True, check=False)


class SkillSpecTests(unittest.TestCase):
    def test_package_contract_passes(self) -> None:
        result = run_script("validate_skill_package.py", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS: skill-spec package contract", result.stdout)

    def test_skill_up_validate_is_safe_without_cli(self) -> None:
        result = run_script("skill_up.py", "validate", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue("SKILL_UP_NOT_INSTALLED" in result.stdout or result.stdout)

    def test_skill_up_run_requires_explicit_execute(self) -> None:
        result = run_script("skill_up.py", "run", str(ROOT))
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires --execute", result.stderr)

    def test_skillopt_preflight_reports_not_ready_without_training(self) -> None:
        result = run_script("skillopt.py", "preflight", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SKILLOPT_NOT_READY", result.stdout)

    def test_skillopt_run_refuses_without_explicit_execute(self) -> None:
        result = run_script("skillopt.py", "run", str(ROOT))
        self.assertEqual(result.returncode, 2)
        self.assertIn("SKILLOPT_NOT_READY", result.stdout)


if __name__ == "__main__":
    unittest.main()
