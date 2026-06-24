from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .report import sha256_file


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


def _reuse_committed_scxml_export(*, example_id: str, repo_root: Path, reports_dir: Path) -> tuple[Path | None, str | None]:
    committed = repo_root / "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/toolchain_exports" / example_id / "stm0.scxml"
    if not committed.exists() or committed.stat().st_size == 0:
        return None, None
    out_dir = reports_dir / "toolchain_exports" / example_id
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / committed.name
    if committed.resolve() != target.resolve():
        target.write_bytes(committed.read_bytes())
    return target, sha256_file(target)


def _plantuml_jar_candidates(repo_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for env_name in ("PLANTUML_JAR", "PLANTUML_PATH"):
        val = os.environ.get(env_name)
        if val:
            candidates.append(Path(val))
    if shutil.which("plantuml"):
        # command mode, represented by a sentinel string in evidence only; jar candidates remain paths.
        pass
    candidates.extend([
        Path.home() / "pyplantuml-poc/src/pyplantuml/plantuml.jar",
        Path.home() / "oo-projects/fcstm-ui/docs/plantuml.jar",
        repo_root / "tools/plantuml.jar",
    ])
    seen: set[str] = set()
    out = []
    for c in candidates:
        key = str(c)
        if key not in seen and c.exists():
            seen.add(key)
            out.append(c)
    return out


def preflight_plantuml(stm_path: Path, *, example_id: str, repo_root: Path, reports_dir: Path) -> ToolPreflight:
    source_url = "https://plantuml.com/command-line"
    java_info = _java_version()
    jar_candidates = _plantuml_jar_candidates(repo_root)
    evidence: dict[str, Any] = {
        "official_capability": "headless syntax check/render; state diagram SCXML; XMI is for class diagrams; no documented AST export",
        "java_version": java_info,
        "jar_candidates": sorted({candidate for candidate in (_rel(p, repo_root) for p in jar_candidates) if candidate}),
    }
    if not jar_candidates and not shutil.which("plantuml"):
        reused, reused_sha = _reuse_committed_scxml_export(example_id=example_id, repo_root=repo_root, reports_dir=reports_dir)
        if reused is not None:
            return ToolPreflight(
                tool_name="PlantUML CLI",
                tool_version=None,
                tool_source_url=source_url,
                invocation_status="tool_missing_reused_committed_official_scxml",
                syntax_status="not_run_tool_missing_reused_official_export",
                structured_export_status="scxml_export_reused_tool_missing",
                structured_export_format="scxml",
                structured_export_sha256=reused_sha,
                structured_export_path=_rel_or_abs(reused, repo_root),
                fallback_reason="No plantuml executable or plantuml.jar candidate was available in this environment; R3 reused a committed PlantUML official SCXML export fixture for canonical structured extraction instead of regex/text parsing.",
                evidence={**evidence, "reused_committed_official_export": _rel(reused, repo_root)},
            )
        return ToolPreflight(
            tool_name="PlantUML CLI",
            tool_version=None,
            tool_source_url=source_url,
            invocation_status="not_available_no_canonical_conversion",
            syntax_status="not_run_tool_missing",
            structured_export_status="not_run_tool_missing",
            fallback_reason="No plantuml executable or plantuml.jar candidate was available; R3 cannot produce PlantUML canonical conversion without official SCXML. Text inspection is debug/audit only.",
            evidence=evidence,
        )

    if jar_candidates:
        jar = jar_candidates[0]
        base_cmd = ["java", "-jar", str(jar)]
        tool_ref = _rel(jar, repo_root)
    else:
        base_cmd = [shutil.which("plantuml") or "plantuml"]
        tool_ref = base_cmd[0]

    try:
        version_cp = _run(base_cmd + ["-version"], timeout=20)
        version_text = _tail((version_cp.stdout or "") + "\n" + (version_cp.stderr or ""), 800)
    except Exception as exc:
        return ToolPreflight(
            tool_name="PlantUML CLI",
            tool_version=None,
            tool_source_url=source_url,
            invocation_status="failed_before_syntax_fallback_parser_used",
            syntax_status="not_run_tool_error",
            structured_export_status="not_run_tool_error",
            fallback_reason=f"PlantUML command could not be invoked: {exc}",
            evidence={**evidence, "selected_tool": tool_ref},
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
        fallback = "Official syntax check passed but SCXML export did not produce a usable file; R3 does not use text regex as canonical conversion source and marks the example blocked/partial with tooling loss."
    else:
        invocation_status = "official_cli_syntax_failed_no_canonical_conversion"
        structured_status = "scxml_not_trusted_after_syntax_failure"
        fallback = "Official PlantUML syntax check failed; R3 does not use text regex as canonical conversion source. Any text inspection is limited to debug/audit probe and the example cannot be marked converted."

    replacements = {str(local): _display_source(example_id, stm_path), str(tmp): "<tmp>"}

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
        stdout_tail=_sanitize_output((check_cp.stdout or "") + "\n" + (scxml_cp.stdout or ""), replacements),
        stderr_tail=_sanitize_output((check_cp.stderr or "") + "\n" + (scxml_cp.stderr or ""), replacements),
        fallback_reason=fallback,
        evidence={**evidence, "selected_tool": tool_ref, "scxml_command": ([*base_cmd[:2], tool_ref, "-tscxml", _display_source(example_id, stm_path)] if base_cmd[:2] == ["java", "-jar"] else [base_cmd[0], "-tscxml", _display_source(example_id, stm_path)]), "scxml_returncode": scxml_cp.returncode},
    )


def _umple_jar_candidates(repo_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for env_name in ("UMPLE_JAR", "UMPLE_PATH"):
        val = os.environ.get(env_name)
        if val:
            candidates.append(Path(val))
    candidates.extend([
        repo_root / "tools/umple.jar",
        Path.home() / "umple.jar",
        Path.home() / "下载/llm_state_machine_modeling/backend/resources/umple.jar",
    ])
    seen: set[str] = set()
    out = []
    for c in candidates:
        key = str(c)
        if key not in seen and c.exists():
            seen.add(key)
            out.append(c)
    return out


def preflight_umple(stm_path: Path, *, example_id: str, repo_root: Path, reports_dir: Path) -> ToolPreflight:
    source_url = "https://cruise.umple.org/umple/UmpleTools.html"
    java_info = _java_version()
    candidates = _umple_jar_candidates(repo_root)
    evidence: dict[str, Any] = {
        "official_capability": "headless compiler; documented generators include Json, Scxml, Ecore, Xmi, StateTables; no separate AST export found",
        "java_version": java_info,
        "jar_candidates": sorted({candidate for candidate in (_rel(p, repo_root) for p in candidates) if candidate}),
        "download_hint": "https://cruise.umple.org/umpleonline/scripts/umple.jar",
    }
    if not candidates:
        reused, reused_sha = _reuse_committed_scxml_export(example_id=example_id, repo_root=repo_root, reports_dir=reports_dir)
        if reused is not None:
            return ToolPreflight(
                tool_name="Umple compiler CLI",
                tool_version=None,
                tool_source_url=source_url,
                invocation_status="tool_missing_reused_committed_official_scxml",
                syntax_status="not_run_tool_missing_reused_official_export",
                structured_export_status="scxml_export_reused_tool_missing",
                structured_export_format="scxml",
                structured_export_sha256=reused_sha,
                structured_export_path=_rel_or_abs(reused, repo_root),
                fallback_reason="No local umple.jar was available in this environment; R3 reused a committed Umple official SCXML export fixture for canonical structured extraction. Raw .ump text remains targeted timing/loss audit only.",
                evidence={**evidence, "reused_committed_official_export": _rel(reused, repo_root)},
            )
        return ToolPreflight(
            tool_name="Umple compiler CLI",
            tool_version=None,
            tool_source_url=source_url,
            invocation_status="not_available_no_canonical_conversion",
            syntax_status="not_run_tool_missing",
            structured_export_status="not_run_tool_missing",
            fallback_reason="No local umple.jar was available. R3 cannot produce Umple canonical conversion without official structured export; rerun with UMPLE_JAR or tools/umple.jar for official SCXML extraction.",
            evidence=evidence,
        )

    jar = candidates[0]
    base_cmd = ["java", "-jar", str(jar)]
    try:
        version_cp = _run(base_cmd + ["--version"], timeout=20)
        version_text = _tail((version_cp.stdout or "") + "\n" + (version_cp.stderr or ""), 800)
    except Exception as exc:
        return ToolPreflight(
            tool_name="Umple compiler CLI",
            tool_version=None,
            tool_source_url=source_url,
            invocation_status="failed_before_syntax_fallback_parser_used",
            syntax_status="not_run_tool_error",
            structured_export_status="not_run_tool_error",
            fallback_reason=f"Umple command could not be invoked: {exc}",
            evidence={**evidence, "selected_tool": _rel(jar, repo_root)},
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
        fallback = "Canonical structure is extracted from official Umple SCXML. Raw .ump text is used only for targeted timing/loss audit because official SCXML rewrites after(60) into timeoutTimeoutToReady."
    elif syntax_ok:
        invocation_status = "official_compiler_syntax_ok_scxml_failed_no_canonical_conversion"
        structured_status = "scxml_export_failed"
        fallback = "Official Umple syntax check passed but SCXML export did not produce a usable file; R3 does not use regex parser as canonical conversion source."
    else:
        invocation_status = "official_compiler_syntax_failed_no_canonical_conversion"
        structured_status = "scxml_not_trusted_after_syntax_failure"
        fallback = "Official Umple compiler rejected the file; R3 does not use regex parser as canonical conversion source."

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
