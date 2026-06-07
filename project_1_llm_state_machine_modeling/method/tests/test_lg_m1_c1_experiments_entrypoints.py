"""LG-M1-C1 experiment entrypoint migration characterization tests."""

from __future__ import annotations

import argparse
import ast
import importlib
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
METHOD_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling" / "method"

ENTRYPOINT_PAIRS = [
    ("method.pr_e1_real_runs", "method.experiments.real_run_matrix"),
    ("method.pr_lg_f1_resume_experiment", "method.experiments.checkpoint_resume"),
    ("method.pr_d_representative", "method.experiments.representative_cases"),
]

USED_SYMBOLS = {
    "method.pr_e1_real_runs": [
        "PrE1RunSummary",
        "condition_specs",
        "make_pr_e1_config",
        "pr_e1_cases",
        "render_matrix_summary",
        "render_pr_comment",
        "render_run_report",
        "run_pr_e1_matrix",
        "summarize_pr_e1_run",
        "classify_primary_failure",
        "build_reproducibility_payload",
        "_inject_pr_e1_quality_boundary",
        "main",
    ],
    "method.pr_lg_f1_resume_experiment": [
        "build_lg_f1_mock_adapters",
        "main",
    ],
    "method.pr_d_representative": [
        "FULL_STAGED_REQUIRED_STAGE_IDS",
        "RepresentativeCase",
        "_schema_validation_error",
        "assert_pr_d_provider_env",
        "make_pr_d_config",
        "missing_provider_env",
        "render_issue_comment",
        "representative_cases",
        "run_representative_cases",
        "summarize_run",
        "summaries_to_jsonable",
        "main",
    ],
}


def _python_env() -> dict[str, str]:
    import os

    env = dict(os.environ)
    env["PYTHONPATH"] = "project_1_llm_state_machine_modeling"
    return env


def _repo_root_env_without_pythonpath() -> dict[str, str]:
    import os

    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    return env


def _help(module: str) -> argparse.ArgumentParser:
    imported = importlib.import_module(module)
    parser_holder: dict[str, argparse.ArgumentParser] = {}
    original = argparse.ArgumentParser.parse_args

    def capture(self: argparse.ArgumentParser, args: Any = None, namespace: Any = None):
        parser_holder["parser"] = self
        return original(self, args, namespace)

    try:
        argparse.ArgumentParser.parse_args = capture  # type: ignore[assignment]
        rc = imported.main(["--help"])
        assert rc == 0
    except SystemExit as exc:
        assert exc.code == 0
    finally:
        argparse.ArgumentParser.parse_args = original  # type: ignore[assignment]
    return parser_holder["parser"]


def _option_signature(parser: argparse.ArgumentParser) -> list[tuple[tuple[str, ...], str | None, tuple[str, ...] | None, Any]]:
    signature: list[tuple[tuple[str, ...], str | None, tuple[str, ...] | None, Any]] = []
    for action in parser._actions:  # noqa: SLF001 - argparse has no public stable equivalent for this smoke.
        if not action.option_strings:
            continue
        choices = tuple(str(item) for item in action.choices) if action.choices is not None else None
        default = None if action.default is argparse.SUPPRESS else action.default
        signature.append((tuple(action.option_strings), action.dest, choices, default))
    return signature


def test_lg_m1_c1_old_shims_reexport_used_symbols_and_share_objects() -> None:
    for old_module_name, new_module_name in ENTRYPOINT_PAIRS:
        old_module = importlib.import_module(old_module_name)
        new_module = importlib.import_module(new_module_name)
        for symbol in USED_SYMBOLS[old_module_name]:
            assert hasattr(old_module, symbol), f"{old_module_name} missing {symbol}"
            assert hasattr(new_module, symbol), f"{new_module_name} missing {symbol}"
            assert getattr(old_module, symbol) is getattr(new_module, symbol), f"{old_module_name}.{symbol} is not re-exported from {new_module_name}"


def test_lg_m1_c1_old_and_new_help_surfaces_are_semantically_equivalent() -> None:
    for old_module_name, new_module_name in ENTRYPOINT_PAIRS:
        old_signature = _option_signature(_help(old_module_name))
        new_signature = _option_signature(_help(new_module_name))
        assert new_signature == old_signature


def test_lg_m1_c1_all_old_and_new_module_entrypoints_exit_zero_without_provider() -> None:
    for old_module_name, new_module_name in ENTRYPOINT_PAIRS:
        for module_name in (old_module_name, new_module_name):
            completed = subprocess.run(
                [sys.executable, "-m", module_name, "--help"],
                cwd=REPO_ROOT,
                env=_python_env(),
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            assert completed.returncode == 0, completed.stderr
            assert "usage:" in completed.stdout


def test_lg_m1_c1_repo_root_package_entrypoints_exit_zero_without_pythonpath() -> None:
    for old_module_name, new_module_name in ENTRYPOINT_PAIRS:
        for module_name in (old_module_name, new_module_name):
            package_module = f"project_1_llm_state_machine_modeling.{module_name}"
            completed = subprocess.run(
                [sys.executable, "-m", package_module, "--help"],
                cwd=REPO_ROOT,
                env=_repo_root_env_without_pythonpath(),
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            assert completed.returncode == 0, completed.stderr
            assert "usage:" in completed.stdout


def test_lg_m1_c1_experiment_implementations_do_not_import_legacy_shims() -> None:
    forbidden_modules = {
        "method.pr_e1_real_runs",
        "method.pr_lg_f1_resume_experiment",
        "method.pr_d_representative",
    }
    for path in sorted((METHOD_ROOT / "experiments").glob("*.py")):
        if path.name == "__init__.py":
            continue
        module = ast.parse(path.read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(module):
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
            elif isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
        assert not (imports & forbidden_modules), f"{path} imports old shim(s): {sorted(imports & forbidden_modules)}"
