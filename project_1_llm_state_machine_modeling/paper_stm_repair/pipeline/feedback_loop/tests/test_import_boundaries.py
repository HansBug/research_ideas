from __future__ import annotations

import subprocess
import sys
import ast
from pathlib import Path


FORBIDDEN_RUNTIME_IMPORT_PREFIXES = (
    "paper_stm_repair_loop",
    "method.loop",
    "method.run_record",
)


def test_common_imports_do_not_load_legacy_repair_loop() -> None:
    src = Path(__file__).resolve().parents[1] / "src"
    code = """
import sys
import paper_stm_feedback_loop
import paper_stm_feedback_loop.common.inputs
import paper_stm_feedback_loop.common.records
import paper_stm_feedback_loop.common.telemetry
assert 'paper_stm_repair_loop' not in sys.modules
assert not any(name.startswith('paper_stm_repair_loop.') for name in sys.modules)
"""
    subprocess.run([sys.executable, "-c", code], check=True, env={"PYTHONPATH": str(src)})


def test_all_feedback_loop_sources_have_no_legacy_import() -> None:
    src = Path(__file__).resolve().parents[1] / "src"
    for path in src.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(
                    not alias.name.startswith(FORBIDDEN_RUNTIME_IMPORT_PREFIXES)
                    for alias in node.names
                ), path
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith(
                    FORBIDDEN_RUNTIME_IMPORT_PREFIXES
                ), path


def test_feedback_loop_makefile_does_not_inject_legacy_pipeline_source() -> None:
    makefile = Path(__file__).resolve().parents[1] / "Makefile"
    text = makefile.read_text(encoding="utf-8")
    assert "pipeline/agent_loop/src" not in text
    assert "paper_stm_repair_loop" not in text


def test_runtime_sentinel_with_legacy_package_available() -> None:
    feedback_src = Path(__file__).resolve().parents[1] / "src"
    repo = Path(__file__).resolve().parents[5]
    legacy_src = (
        repo
        / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/src"
    )
    code = r'''
import builtins
import importlib
FORBIDDEN_RUNTIME_IMPORT_PREFIXES = (
    "paper_stm_repair_loop",
    "method.loop",
    "method.run_record",
)
real_import = builtins.__import__
real_import_module = importlib.import_module
def checked_import(name, *args, **kwargs):
    if name.startswith(FORBIDDEN_RUNTIME_IMPORT_PREFIXES):
        raise AssertionError("legacy runtime import attempted: " + name)
    return real_import(name, *args, **kwargs)
def checked_import_module(name, *args, **kwargs):
    if name.startswith(FORBIDDEN_RUNTIME_IMPORT_PREFIXES):
        raise AssertionError("legacy runtime import_module attempted: " + name)
    return real_import_module(name, *args, **kwargs)
builtins.__import__ = checked_import
importlib.import_module = checked_import_module
import paper_stm_feedback_loop.assertions
import paper_stm_feedback_loop.discover.cli
import paper_stm_feedback_loop.discover.graph
import paper_stm_feedback_loop.discover.report
'''
    env = {
        "PYTHONPATH": f"{feedback_src}:{repo}:{legacy_src}",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    subprocess.run([sys.executable, "-c", code], check=True, env=env)
