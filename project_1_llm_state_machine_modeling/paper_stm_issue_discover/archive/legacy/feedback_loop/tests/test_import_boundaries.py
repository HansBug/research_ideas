from __future__ import annotations

import subprocess
import sys
import ast
from pathlib import Path


FORBIDDEN_RUNTIME_IMPORT_PREFIXES = (
    "paper_stm_repair_loop",
    "archive.agent_loop_method.loop",
    "archive.agent_loop_method.run_record",
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


LEGACY_SRC = (
    Path(__file__).resolve().parents[5]
    / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
    / "archive/r9_agent_loop_pipeline/agent_loop/src"
)


def test_feedback_loop_makefile_does_not_inject_legacy_pipeline_source() -> None:
    makefile = Path(__file__).resolve().parents[1] / "Makefile"
    text = makefile.read_text(encoding="utf-8")
    # 旧 agent_loop 于 2026-08-11 归档到 archive/r9_agent_loop_pipeline/。⚠️ 归档之后
    # 原先断言的 "pipeline/agent_loop/src" 这个字符串再也不可能出现，该断言随之变成
    # 永真 —— 守卫绿着但已不再守任何东西。这是本会话里同一个文件第二次静默失效
    # （上一次是它检查一个已不可能存在的模块名 method.loop），所以这里同时钉住新路径
    # 与「新路径必须真实存在」，让下一次搬迁直接把测试打红而不是悄悄放行。
    assert LEGACY_SRC.is_dir(), (
        f"归档路径已失效：{LEGACY_SRC}。搬迁后必须同步本文件，否则下面的断言会变成永真。"
    )
    assert "archive/r9_agent_loop_pipeline/agent_loop/src" not in text
    assert "pipeline/agent_loop/src" not in text
    assert "paper_stm_repair_loop" not in text


def test_runtime_sentinel_with_legacy_package_available() -> None:
    feedback_src = Path(__file__).resolve().parents[1] / "src"
    repo = Path(__file__).resolve().parents[5]
    # ⚠️ Python 会静默忽略 PYTHONPATH 里不存在的条目。若这里指向一个已被搬走的路径，
    # 本测试仍然通过，但它声称的前提「legacy 包可导入」根本没成立 —— 空转的绿灯。
    legacy_src = LEGACY_SRC
    assert legacy_src.is_dir(), (
        f"legacy 包源码路径不存在：{legacy_src}；本测试的前提未成立，不能算通过。"
    )
    code = r'''
import builtins
import importlib
FORBIDDEN_RUNTIME_IMPORT_PREFIXES = (
    "paper_stm_repair_loop",
    "archive.agent_loop_method.loop",
    "archive.agent_loop_method.run_record",
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
