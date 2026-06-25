from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .report import sha256_file


class ToolchainSetupError(RuntimeError):
    """Raised when a required external conversion tool/runtime is unavailable or misconfigured."""


_PLANTUML_BASE_CACHE: dict[str, tuple[list[str], str, str]] = {}

NO_TEXT_FALLBACK_POLICY_ZH = (
    "R3 不允许在官方工具链缺失、不可执行、syntax check 失败或结构化导出失败时，"
    "静默退回 regex/string/source-text parser，也不允许复用已提交 SCXML fixture 冒充本次转换证据。"
)


@dataclass
class ToolPreflight:
    tool_name: str
    tool_version: str | None
    tool_source_url: str
    invocation_status: str
    syntax_status: str
    structured_export_status: str
    structured_export_format: str | None = None
    structured_export_sha256: str | None = None
    structured_export_path: str | None = None
    command: list[str] | None = None
    returncode: int | None = None
    stdout_tail: str | None = None
    stderr_tail: str | None = None
    fallback_reason: str | None = None
    evidence: dict[str, Any] | None = None

    def to_metadata(self) -> dict[str, Any]:
        return {
            "tool_name": self.tool_name,
            "tool_version": self.tool_version,
            "tool_source_url": self.tool_source_url,
            "tool_invocation_status": self.invocation_status,
            "syntax_status": self.syntax_status,
            "structured_export_status": self.structured_export_status,
            "structured_export_format": self.structured_export_format,
            "structured_export_sha256": self.structured_export_sha256,
            "structured_export_path": self.structured_export_path,
            "command": self.command,
            "returncode": self.returncode,
            "stdout_tail": self.stdout_tail,
            "stderr_tail": self.stderr_tail,
            "fallback_reason": self.fallback_reason,
            "evidence": self.evidence or {},
        }


def _tail(text: str, limit: int = 1200) -> str:
    text = text.strip()
    return text[-limit:] if len(text) > limit else text


def _sanitize_output(text: str, replacements: dict[str, str]) -> str:
    out = _tail(text)
    for old, new in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        if old:
            out = out.replace(old, new)
    return out


def _run(cmd: list[str], *, cwd: Path | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False)


def _java_version() -> str | None:
    try:
        cp = _run(["java", "-version"], timeout=10)
    except Exception:
        return None
    return _tail((cp.stderr or "") + "\n" + (cp.stdout or ""), 400)


def _rel(path: Path | None, repo_root: Path) -> str | None:
    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return f"external-local-tool/{path.name}"


def _rel_or_abs(path: Path | None, repo_root: Path) -> str | None:
    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def _display_source(example_id: str, stm_path: Path) -> str:
    return f"selected_seed_examples/{example_id}/{stm_path.name}"


def _display_candidate(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return f"external-run-artifact/{path.name}"


def _configured_path(env_name: str) -> Path | None:
    val = os.environ.get(env_name)
    return Path(val).expanduser() if val else None


def _configured_missing(env_names: tuple[str, ...]) -> list[tuple[str, Path]]:
    missing = []
    for env_name in env_names:
        path = _configured_path(env_name)
        if path is not None and not path.exists():
            missing.append((env_name, path))
    return missing


def _format_missing_env_paths(missing: list[tuple[str, Path]]) -> str:
    return "; ".join(f"{name}={path} 不存在" for name, path in missing)


def _require_java_runtime(*, tool_name: str, setup_hint: str) -> str:
    if shutil.which("java") is None:
        raise ToolchainSetupError(
            f"{tool_name} 需要 Java runtime，但当前 PATH 中找不到 `java`。\n"
            f"请先安装 JRE/JDK 并确认 `java -version` 可运行；然后按以下方式配置工具：\n{setup_hint}"
        )
    try:
        cp = _run(["java", "-version"], timeout=10)
    except Exception as exc:
        raise ToolchainSetupError(
            f"{tool_name} 需要 Java runtime，但执行 `java -version` 失败：{exc}\n"
            f"请修复 Java 安装后重试；工具配置方式：\n{setup_hint}"
        ) from exc
    version_text = _tail((cp.stderr or "") + "\n" + (cp.stdout or ""), 400)
    if cp.returncode != 0:
        raise ToolchainSetupError(
            f"{tool_name} 需要 Java runtime，但 `java -version` 返回 {cp.returncode}。输出：\n{version_text}\n"
            f"请修复 Java 安装后重试；工具配置方式：\n{setup_hint}"
        )
    return version_text


def _plantuml_setup_hint(repo_root: Path) -> str:
    return (
        "PlantUML 配置建议：\n"
        "1. 下载官方 plantuml.jar： https://github.com/plantuml/plantuml/releases 或 https://plantuml.com/download\n"
        "2. 设置环境变量： `export PLANTUML_JAR=/abs/path/to/plantuml.jar`；或放到仓库 `tools/plantuml.jar`。\n"
        "3. 也可安装 PATH 中可执行的 `plantuml` 命令。\n"
        "4. 复验命令： `java -jar $PLANTUML_JAR -version`、`java -jar $PLANTUML_JAR -checkonly selected_seed_examples/<id>/stm0.puml`、`java -jar $PLANTUML_JAR -tscxml selected_seed_examples/<id>/stm0.puml`。\n"
        "当前仓库候选显式路径：tools/plantuml.jar"
    )


def _umple_setup_hint(repo_root: Path) -> str:
    return (
        "Umple 配置建议：\n"
        "1. 下载官方 umple.jar： https://cruise.umple.org/umpleonline/scripts/umple.jar （入口说明见 https://cruise.umple.org/umple/UmpleTools.html）\n"
        "2. 设置环境变量： `export UMPLE_JAR=/abs/path/to/umple.jar`；或放到仓库 `tools/umple.jar`。\n"
        "3. 复验命令： `java -jar $UMPLE_JAR --version`、`java -jar $UMPLE_JAR -g Nothing selected_seed_examples/<id>/stm0.ump`、`java -jar $UMPLE_JAR -g Scxml selected_seed_examples/<id>/stm0.ump`。\n"
        "当前仓库候选显式路径：tools/umple.jar"
    )


def _plantuml_jar_candidates(repo_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for env_name in ("PLANTUML_JAR", "PLANTUML_PATH"):
        path = _configured_path(env_name)
        if path is not None and path.exists():
            candidates.append(path)
    candidates.append(repo_root / "tools/plantuml.jar")
    seen: set[str] = set()
    out = []
    for c in candidates:
        key = str(c.resolve()) if c.exists() else str(c)
        if key not in seen and c.exists():
            seen.add(key)
            out.append(c)
    return out


def preflight_plantuml(stm_path: Path, *, example_id: str, repo_root: Path, reports_dir: Path) -> ToolPreflight:
    source_url = "https://plantuml.com/command-line"
    setup_hint = _plantuml_setup_hint(repo_root)
    missing = _configured_missing(("PLANTUML_JAR", "PLANTUML_PATH"))
    if missing:
        raise ToolchainSetupError(
            "PlantUML 已通过环境变量配置，但路径无效："
            f"{_format_missing_env_paths(missing)}\n{setup_hint}"
        )
    java_info = _java_version()
    jar_candidates = _plantuml_jar_candidates(repo_root)
    plantuml_cmd = shutil.which("plantuml")
    evidence: dict[str, Any] = {
        "official_capability": "headless syntax check/render; state diagram SCXML; XMI is for class diagrams; no documented AST export",
        "java_version": java_info,
        "jar_candidates": sorted({candidate for candidate in (_rel(p, repo_root) for p in jar_candidates) if candidate}),
        "download_hint": "https://github.com/plantuml/plantuml/releases ; https://plantuml.com/download",
        "setup_hint": setup_hint,
        "no_text_fallback_policy": NO_TEXT_FALLBACK_POLICY_ZH,
        "committed_export_reuse_allowed": False,
    }
    if not jar_candidates and not plantuml_cmd:
        raise ToolchainSetupError(
            "R3 PlantUML 转换需要真实运行 PlantUML 官方工具链，但当前既没有 `plantuml` 命令，也没有可用 plantuml.jar。\n"
            f"{NO_TEXT_FALLBACK_POLICY_ZH}\n请按下面步骤配置后重试。\n"
            f"{setup_hint}"
        )

    if jar_candidates:
        jar = jar_candidates[0]
        _require_java_runtime(tool_name="PlantUML CLI", setup_hint=setup_hint)
        base_cmd = ["java", "-jar", str(jar)]
        tool_ref = _rel(jar, repo_root)
    else:
        base_cmd = [plantuml_cmd or "plantuml"]
        tool_ref = base_cmd[0]

    try:
        version_cp = _run(base_cmd + ["-version"], timeout=20)
        version_text = _tail((version_cp.stdout or "") + "\n" + (version_cp.stderr or ""), 800)
    except Exception as exc:
        raise ToolchainSetupError(
            f"PlantUML 命令无法启动：{exc}\n"
            f"请确认 PlantUML/Java 安装可用。{NO_TEXT_FALLBACK_POLICY_ZH}\n"
            f"{setup_hint}"
        ) from exc
    if version_cp.returncode != 0:
        raise ToolchainSetupError(
            f"PlantUML `-version` 返回 {version_cp.returncode}，工具链不可用。输出：\n{version_text}\n"
            f"请按下列方式修复。{NO_TEXT_FALLBACK_POLICY_ZH}\n"
            f"{setup_hint}"
        )

    with tempfile.TemporaryDirectory(prefix=f"r3_plantuml_{example_id}_") as td:
        tmp = Path(td)
        local = tmp / stm_path.name
        local.write_bytes(stm_path.read_bytes())
        check_cmd = base_cmd + ["-checkonly", str(local)]
        check_cp = _run(check_cmd, timeout=30)
        scxml_cmd = base_cmd + ["-tscxml", str(local)]
        scxml_cp = _run(scxml_cmd, timeout=30)
        scxml_path = local.with_suffix(".scxml")
        persisted_scxml: Path | None = None
        scxml_sha: str | None = None
        if scxml_path.exists() and scxml_path.stat().st_size > 0:
            out_dir = reports_dir / "toolchain_exports" / example_id
            out_dir.mkdir(parents=True, exist_ok=True)
            persisted_scxml = out_dir / scxml_path.name
            persisted_scxml.write_bytes(scxml_path.read_bytes())
            scxml_sha = sha256_file(persisted_scxml)

    syntax_ok = check_cp.returncode == 0
    export_ok = persisted_scxml is not None
    if syntax_ok and export_ok:
        invocation_status = "official_cli_syntax_and_scxml_ok_canonical_source"
        structured_status = "scxml_export_ok"
        fallback = None
    elif syntax_ok:
        invocation_status = "official_cli_syntax_ok_scxml_failed_no_canonical_conversion"
        structured_status = "scxml_export_failed"
        fallback = (
            "Official syntax check passed but SCXML export did not produce a usable file; "
            "R3 does not use any source-text parser as canonical conversion source and marks the example blocked/partial with tooling loss. "
            + NO_TEXT_FALLBACK_POLICY_ZH
        )
    else:
        invocation_status = "official_cli_syntax_failed_no_canonical_conversion"
        structured_status = "scxml_not_trusted_after_syntax_failure"
        fallback = (
            "Official PlantUML syntax check failed; R3 does not use any source-text parser as canonical conversion source. "
            "The example cannot be marked converted. "
            + NO_TEXT_FALLBACK_POLICY_ZH
        )

    replacements = {str(local): _display_source(example_id, stm_path), str(tmp): "<tmp>"}
    stdout_tail = _sanitize_output((check_cp.stdout or "") + "\n" + (scxml_cp.stdout or ""), replacements)
    stderr_tail = _sanitize_output((check_cp.stderr or "") + "\n" + (scxml_cp.stderr or ""), replacements)
    failure_observation: dict[str, Any] | None = None
    if not syntax_ok or not export_ok:
        failure_observation = {
            "check_command": ([*base_cmd[:2], tool_ref, "-checkonly", _display_source(example_id, stm_path)] if base_cmd[:2] == ["java", "-jar"] else [base_cmd[0], "-checkonly", _display_source(example_id, stm_path)]),
            "check_returncode": check_cp.returncode,
            "scxml_command": ([*base_cmd[:2], tool_ref, "-tscxml", _display_source(example_id, stm_path)] if base_cmd[:2] == ["java", "-jar"] else [base_cmd[0], "-tscxml", _display_source(example_id, stm_path)]),
            "scxml_returncode": scxml_cp.returncode,
            "stdout_tail": stdout_tail,
            "stderr_tail": stderr_tail,
            "canonical_decision": "no canonical JSON is emitted unless official PlantUML SCXML exists and is trusted",
            "replacement_probe_path": (
                "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/unified_uml_plantuml_candidate_probe.json"
                if example_id == "unified-uml-synthetic-0000"
                else None
            ),
        }

    return ToolPreflight(
        tool_name="PlantUML CLI",
        tool_version=version_text,
        tool_source_url=source_url,
        invocation_status=invocation_status,
        syntax_status="ok" if syntax_ok else "failed",
        structured_export_status=structured_status,
        structured_export_format="scxml" if export_ok else None,
        structured_export_sha256=scxml_sha,
        structured_export_path=_rel_or_abs(persisted_scxml, repo_root),
        command=[*base_cmd[:2], tool_ref, "-checkonly", _display_source(example_id, stm_path)] if base_cmd[:2] == ["java", "-jar"] else [base_cmd[0], "-checkonly", _display_source(example_id, stm_path)],
        returncode=check_cp.returncode,
        stdout_tail=stdout_tail,
        stderr_tail=stderr_tail,
        fallback_reason=fallback,
        evidence={
            **evidence,
            "selected_tool": tool_ref,
            "scxml_command": ([*base_cmd[:2], tool_ref, "-tscxml", _display_source(example_id, stm_path)] if base_cmd[:2] == ["java", "-jar"] else [base_cmd[0], "-tscxml", _display_source(example_id, stm_path)]),
            "scxml_returncode": scxml_cp.returncode,
            "failure_observation": failure_observation,
        },
    )


def _umple_jar_candidates(repo_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for env_name in ("UMPLE_JAR", "UMPLE_PATH"):
        path = _configured_path(env_name)
        if path is not None and path.exists():
            candidates.append(path)
    candidates.append(repo_root / "tools/umple.jar")
    seen: set[str] = set()
    out = []
    for c in candidates:
        key = str(c.resolve()) if c.exists() else str(c)
        if key not in seen and c.exists():
            seen.add(key)
            out.append(c)
    return out


def preflight_umple(stm_path: Path, *, example_id: str, repo_root: Path, reports_dir: Path) -> ToolPreflight:
    source_url = "https://cruise.umple.org/umple/UmpleTools.html"
    setup_hint = _umple_setup_hint(repo_root)
    missing = _configured_missing(("UMPLE_JAR", "UMPLE_PATH"))
    if missing:
        raise ToolchainSetupError(
            "Umple 已通过环境变量配置，但路径无效："
            f"{_format_missing_env_paths(missing)}\n{setup_hint}"
        )
    java_info = _java_version()
    candidates = _umple_jar_candidates(repo_root)
    evidence: dict[str, Any] = {
        "official_capability": "headless compiler; documented generators include Json, Scxml, Ecore, Xmi, StateTables; no separate AST export found",
        "java_version": java_info,
        "jar_candidates": sorted({candidate for candidate in (_rel(p, repo_root) for p in candidates) if candidate}),
        "download_hint": "https://cruise.umple.org/umpleonline/scripts/umple.jar",
        "setup_hint": setup_hint,
        "no_text_fallback_policy": NO_TEXT_FALLBACK_POLICY_ZH,
        "committed_export_reuse_allowed": False,
    }
    if not candidates:
        raise ToolchainSetupError(
            "R3 Umple 转换需要真实运行 Umple 官方 compiler，但当前没有可用 umple.jar。\n"
            f"{NO_TEXT_FALLBACK_POLICY_ZH}\n请按下面步骤配置后重试。\n"
            f"{setup_hint}"
        )

    jar = candidates[0]
    _require_java_runtime(tool_name="Umple compiler CLI", setup_hint=setup_hint)
    base_cmd = ["java", "-jar", str(jar)]
    try:
        version_cp = _run(base_cmd + ["--version"], timeout=20)
        version_text = _tail((version_cp.stdout or "") + "\n" + (version_cp.stderr or ""), 800)
    except Exception as exc:
        raise ToolchainSetupError(
            f"Umple 命令无法启动：{exc}\n"
            f"请确认 Umple/Java 安装可用。{NO_TEXT_FALLBACK_POLICY_ZH}\n"
            f"{setup_hint}"
        ) from exc
    if version_cp.returncode != 0:
        raise ToolchainSetupError(
            f"Umple `--version` 返回 {version_cp.returncode}，工具链不可用。输出：\n{version_text}\n"
            f"请按下列方式修复。{NO_TEXT_FALLBACK_POLICY_ZH}\n"
            f"{setup_hint}"
        )

    with tempfile.TemporaryDirectory(prefix=f"r3_umple_{example_id}_") as td:
        tmp = Path(td)
        local = tmp / stm_path.name
        local.write_bytes(stm_path.read_bytes())
        syntax_cmd = base_cmd + ["-g", "Nothing", str(local)]
        syntax_cp = _run(syntax_cmd, cwd=tmp, timeout=45)
        scxml_cmd = base_cmd + ["-g", "Scxml", str(local)]
        scxml_cp = _run(scxml_cmd, cwd=tmp, timeout=45)
        scxml_path = local.with_suffix(".scxml")
        persisted_scxml: Path | None = None
        scxml_sha: str | None = None
        if scxml_path.exists() and scxml_path.stat().st_size > 0:
            out_dir = reports_dir / "toolchain_exports" / example_id
            out_dir.mkdir(parents=True, exist_ok=True)
            persisted_scxml = out_dir / scxml_path.name
            persisted_scxml.write_bytes(scxml_path.read_bytes())
            scxml_sha = sha256_file(persisted_scxml)

    syntax_ok = syntax_cp.returncode == 0
    export_ok = persisted_scxml is not None
    if syntax_ok and export_ok:
        invocation_status = "official_compiler_syntax_and_scxml_ok_canonical_source"
        structured_status = "scxml_export_ok"
        fallback = None
    elif syntax_ok:
        invocation_status = "official_compiler_syntax_ok_scxml_failed_no_canonical_conversion"
        structured_status = "scxml_export_failed"
        fallback = (
            "Official Umple syntax check passed but SCXML export did not produce a usable file; "
            "R3 does not use any source-text parser as canonical conversion source. "
            + NO_TEXT_FALLBACK_POLICY_ZH
        )
    else:
        invocation_status = "official_compiler_syntax_failed_no_canonical_conversion"
        structured_status = "scxml_not_trusted_after_syntax_failure"
        fallback = (
            "Official Umple compiler rejected the file; R3 does not use any source-text parser as canonical conversion source. "
            + NO_TEXT_FALLBACK_POLICY_ZH
        )

    replacements = {str(local): _display_source(example_id, stm_path), str(tmp): "<tmp>"}

    return ToolPreflight(
        tool_name="Umple compiler CLI",
        tool_version=version_text,
        tool_source_url=source_url,
        invocation_status=invocation_status,
        syntax_status="ok" if syntax_ok else "failed",
        structured_export_status=structured_status,
        structured_export_format="scxml" if export_ok else None,
        structured_export_sha256=scxml_sha,
        structured_export_path=_rel_or_abs(persisted_scxml, repo_root),
        command=["java", "-jar", _rel(jar, repo_root) or "umple.jar", "-g", "Nothing", _display_source(example_id, stm_path)],
        returncode=syntax_cp.returncode,
        stdout_tail=_sanitize_output((syntax_cp.stdout or "") + "\n" + (scxml_cp.stdout or ""), replacements),
        stderr_tail=_sanitize_output((syntax_cp.stderr or "") + "\n" + (scxml_cp.stderr or ""), replacements),
        fallback_reason=fallback,
        evidence={**evidence, "selected_tool": _rel(jar, repo_root), "scxml_command": ["java", "-jar", _rel(jar, repo_root) or "umple.jar", "-g", "Scxml", _display_source(example_id, stm_path)], "scxml_returncode": scxml_cp.returncode},
    )


def preflight_ttool_xml(stm_path: Path, *, example_id: str, repo_root: Path, reports_dir: Path) -> ToolPreflight:
    # R3 does not invoke a TTool headless converter because official pages document XML artifacts and ttool-cli/MCP,
    # but no stable AVATAR XML -> SCXML/JSON/AST batch export was found for the state-machine slice.
    return ToolPreflight(
        tool_name="TTool / AVATAR XML artifact",
        tool_version=None,
        tool_source_url="https://ttool.telecom-paris.fr/avatar.html",
        invocation_status="official_xml_artifact_inventory_no_documented_headless_structured_export",
        syntax_status="xml_wellformed_checked_by_python_etree",
        structured_export_status="official_xml_available_no_scxml_json_ast_export_documented",
        structured_export_format="xml",
        structured_export_sha256=sha256_file(stm_path),
        structured_export_path=_rel(stm_path, repo_root),
        fallback_reason="Official TTool/AVATAR pages document XML model artifacts and ttool-cli/MCP entry points, but no stable headless AVATAR SMD export to SCXML/JSON/AST was evidenced in R3; therefore R3 performs XML inventory only and marks the example partial.",
        evidence={
            "official_pages": [
                "https://ttool.telecom-paris.fr/avatar.html",
                "https://ttool.telecom-paris.fr/installation_configuration.html",
                "https://ttool.telecom-paris.fr/ttoolai.html",
                "https://gitlab.telecom-paris.fr/mbe-tools/TTool",
            ],
            "documented_cli_entries": ["ttool-cli.jar -mcp", "ttool-cli.jar -mcpcodex", "ttool.exe -config", "ttool.exe -launcher/-nolauncher"],
            "documented_structured_model_asset": "TTool/AVATAR XML file",
            "not_evidenced_in_r3": "documented batch export from AVATAR XML/SMD to SCXML/JSON/AST",
        },
    )


def plantuml_command_base(repo_root: Path) -> tuple[list[str], str, str]:
    """Return a validated PlantUML command base, display ref, and version text.

    This helper is shared by R3 selected-example conversion and R3.1 recovery.
    It validates the same environment variables and emits the same loud setup
    errors; callers still decide which input file to pass to -checkonly/-tscxml.
    """
    cache_key = str(repo_root.resolve()) + "|" + (os.environ.get("PLANTUML_JAR") or "") + "|" + (os.environ.get("PLANTUML_PATH") or "")
    if cache_key in _PLANTUML_BASE_CACHE:
        return _PLANTUML_BASE_CACHE[cache_key]
    setup_hint = _plantuml_setup_hint(repo_root)
    missing = _configured_missing(("PLANTUML_JAR", "PLANTUML_PATH"))
    if missing:
        raise ToolchainSetupError(
            "PlantUML 已通过环境变量配置，但路径无效："
            f"{_format_missing_env_paths(missing)}\n{setup_hint}"
        )
    jar_candidates = _plantuml_jar_candidates(repo_root)
    plantuml_cmd = shutil.which("plantuml")
    if not jar_candidates and not plantuml_cmd:
        raise ToolchainSetupError(
            "R3 PlantUML 转换需要真实运行 PlantUML 官方工具链，但当前既没有 `plantuml` 命令，也没有可用 plantuml.jar。\n"
            f"{NO_TEXT_FALLBACK_POLICY_ZH}\n请按下面步骤配置后重试。\n"
            f"{setup_hint}"
        )
    if jar_candidates:
        jar = jar_candidates[0]
        _require_java_runtime(tool_name="PlantUML CLI", setup_hint=setup_hint)
        base_cmd = ["java", "-jar", str(jar)]
        tool_ref = _rel(jar, repo_root) or str(jar)
    else:
        base_cmd = [plantuml_cmd or "plantuml"]
        tool_ref = base_cmd[0]
    try:
        version_cp = _run(base_cmd + ["-version"], timeout=20)
        version_text = _tail((version_cp.stdout or "") + "\n" + (version_cp.stderr or ""), 800)
    except Exception as exc:
        raise ToolchainSetupError(
            f"PlantUML 命令无法启动：{exc}\n"
            f"请确认 PlantUML/Java 安装可用。{NO_TEXT_FALLBACK_POLICY_ZH}\n"
            f"{setup_hint}"
        ) from exc
    if version_cp.returncode != 0:
        raise ToolchainSetupError(
            f"PlantUML `-version` 返回 {version_cp.returncode}，工具链不可用。输出：\n{version_text}\n"
            f"请按下列方式修复。{NO_TEXT_FALLBACK_POLICY_ZH}\n"
            f"{setup_hint}"
        )
    _PLANTUML_BASE_CACHE[cache_key] = (base_cmd, tool_ref, version_text)
    return base_cmd, tool_ref, version_text


def run_plantuml_on_candidate(
    candidate_path: Path,
    *,
    example_id: str,
    repo_root: Path,
    reports_dir: Path,
    export_subdir: str = "toolchain_exports",
    output_stem: str | None = None,
    timeout: int = 30,
) -> ToolPreflight:
    """Run official PlantUML -checkonly/-tscxml on a concrete candidate file.

    The candidate can be raw or normalized PlantUML.  A successful caller still
    must parse the persisted SCXML; this function does not inspect source text to
    produce canonical STM.
    """
    source_url = "https://plantuml.com/command-line"
    setup_hint = _plantuml_setup_hint(repo_root)
    base_cmd, tool_ref, version_text = plantuml_command_base(repo_root)
    with tempfile.TemporaryDirectory(prefix=f"r3_plantuml_{example_id}_") as td:
        tmp = Path(td)
        local = tmp / candidate_path.name
        local.write_bytes(candidate_path.read_bytes())
        check_cmd = base_cmd + ["-checkonly", str(local)]
        check_cp = _run(check_cmd, timeout=timeout)
        scxml_cmd = base_cmd + ["-tscxml", str(local)]
        scxml_cp = _run(scxml_cmd, timeout=timeout)
        scxml_path = local.with_suffix(".scxml")
        persisted_scxml: Path | None = None
        scxml_sha: str | None = None
        if scxml_path.exists() and scxml_path.stat().st_size > 0:
            out_dir = reports_dir / export_subdir / example_id
            out_dir.mkdir(parents=True, exist_ok=True)
            persisted_scxml = out_dir / f"{output_stem or candidate_path.stem}.scxml"
            persisted_scxml.write_bytes(scxml_path.read_bytes())
            scxml_sha = sha256_file(persisted_scxml)
    syntax_ok = check_cp.returncode == 0
    export_ok = persisted_scxml is not None
    if syntax_ok and export_ok:
        invocation_status = "official_cli_syntax_and_scxml_ok_canonical_source"
        structured_status = "scxml_export_ok"
        fallback = None
    elif syntax_ok:
        invocation_status = "official_cli_syntax_ok_scxml_failed_no_canonical_conversion"
        structured_status = "scxml_export_failed"
        fallback = (
            "Official syntax check passed but SCXML export did not produce a usable file; "
            "R3 does not use any source-text parser as canonical conversion source and marks the example blocked/partial with tooling loss. "
            + NO_TEXT_FALLBACK_POLICY_ZH
        )
    else:
        invocation_status = "official_cli_syntax_failed_no_canonical_conversion"
        structured_status = "scxml_not_trusted_after_syntax_failure"
        fallback = (
            "Official PlantUML syntax check failed; R3 does not use any source-text parser as canonical conversion source. "
            "The example cannot be marked converted. "
            + NO_TEXT_FALLBACK_POLICY_ZH
        )
    replacements = {str(local): _display_source(example_id, candidate_path), str(tmp): "<tmp>"}
    stdout_tail = _sanitize_output((check_cp.stdout or "") + "\n" + (scxml_cp.stdout or ""), replacements)
    stderr_tail = _sanitize_output((check_cp.stderr or "") + "\n" + (scxml_cp.stderr or ""), replacements)
    display = _display_candidate(candidate_path, repo_root)
    evidence: dict[str, Any] = {
        "official_capability": "headless syntax check/render; state diagram SCXML; XMI is for class diagrams; no documented AST export",
        "java_version": _java_version(),
        "download_hint": "https://github.com/plantuml/plantuml/releases ; https://plantuml.com/download",
        "setup_hint": setup_hint,
        "no_text_fallback_policy": NO_TEXT_FALLBACK_POLICY_ZH,
        "committed_export_reuse_allowed": False,
        "selected_tool": tool_ref,
        "scxml_command": ([*base_cmd[:2], tool_ref, "-tscxml", display] if base_cmd[:2] == ["java", "-jar"] else [base_cmd[0], "-tscxml", display]),
        "scxml_returncode": scxml_cp.returncode,
    }
    if not syntax_ok or not export_ok:
        evidence["failure_observation"] = {
            "check_command": ([*base_cmd[:2], tool_ref, "-checkonly", display] if base_cmd[:2] == ["java", "-jar"] else [base_cmd[0], "-checkonly", display]),
            "check_returncode": check_cp.returncode,
            "scxml_command": evidence["scxml_command"],
            "scxml_returncode": scxml_cp.returncode,
            "stdout_tail": stdout_tail,
            "stderr_tail": stderr_tail,
            "canonical_decision": "no canonical JSON is emitted unless official PlantUML SCXML exists and is trusted",
        }
    return ToolPreflight(
        tool_name="PlantUML CLI",
        tool_version=version_text,
        tool_source_url=source_url,
        invocation_status=invocation_status,
        syntax_status="ok" if syntax_ok else "failed",
        structured_export_status=structured_status,
        structured_export_format="scxml" if export_ok else None,
        structured_export_sha256=scxml_sha,
        structured_export_path=_rel_or_abs(persisted_scxml, repo_root),
        command=[*base_cmd[:2], tool_ref, "-checkonly", display] if base_cmd[:2] == ["java", "-jar"] else [base_cmd[0], "-checkonly", display],
        returncode=check_cp.returncode,
        stdout_tail=stdout_tail,
        stderr_tail=stderr_tail,
        fallback_reason=fallback,
        evidence=evidence,
    )


def preflight_for_format(fmt: str, stm_path: Path, *, example_id: str, repo_root: Path, reports_dir: Path) -> ToolPreflight:
    if fmt == "plantuml":
        return preflight_plantuml(stm_path, example_id=example_id, repo_root=repo_root, reports_dir=reports_dir)
    if fmt == "umple":
        return preflight_umple(stm_path, example_id=example_id, repo_root=repo_root, reports_dir=reports_dir)
    if fmt == "ttool_xml":
        return preflight_ttool_xml(stm_path, example_id=example_id, repo_root=repo_root, reports_dir=reports_dir)
    return ToolPreflight(
        tool_name="unknown",
        tool_version=None,
        tool_source_url="",
        invocation_status="unsupported_format",
        syntax_status="not_run_unsupported_format",
        structured_export_status="not_run_unsupported_format",
        fallback_reason=f"Unsupported format: {fmt}",
    )
