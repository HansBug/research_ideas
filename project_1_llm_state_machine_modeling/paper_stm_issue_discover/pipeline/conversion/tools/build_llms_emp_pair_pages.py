#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import uuid
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise RuntimeError("repository root not found")


REPO_ROOT = _repo_root()
PAPER_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
CONVERSION_SRC = PAPER_ROOT / "pipeline/conversion/src"
REPRESENTATION_SRC = PAPER_ROOT / "pipeline/representation/src"
sys.path.insert(0, str(CONVERSION_SRC))
sys.path.insert(0, str(REPRESENTATION_SRC))

from paper_stm_conversion.evidence_integrity import (  # noqa: E402
    relevant_implementation_sha256,
)
from paper_stm_conversion.adapters.plantuml_source import (  # noqa: E402
    java_frontend_build_identity,
    java_frontend_source_identity,
)
from paper_stm_representation.manual_pair_review import (  # noqa: E402
    manual_review_observation_digest,
    validate_manual_pair_review,
)

DEFAULT_PAIRS_PATH = (
    PAPER_ROOT
    / "corpora/seed_library/llms-emp-stm-subset/assets/extracted"
    / "feedback_final_pairs.jsonl"
)
DEFAULT_EVIDENCE_DIR = (
    PAPER_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"
)
MANUAL_REVIEW_SCHEMA = (
    PAPER_ROOT / "pipeline/representation/schemas/manual_pair_review.schema.json"
)
EXPECTED_CASES = [f"{index:04d}" for index in range(60)]


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_json(value: Any) -> str:
    return _sha256_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise RuntimeError(f"expected JSON object at {path}:{line_number}")
        rows.append(value)
    return rows


def _fence(language: str, text: str) -> str:
    suffix = "" if text.endswith("\n") else "\n"
    return f"```{language}\n{text}{suffix}```"


def _table_text(value: object) -> str:
    return str(value or "-").replace("|", "\\|").replace("\n", "<br>")


def _display_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines())


def _stage_lineage_lines(source_row: dict) -> list[str]:
    lines = [
        "| stage | output cell | present | output SHA-256 | feedback | resolved |",
        "|---|---|---|---|---|---|",
    ]
    for item in source_row["stage_lineage"]:
        output = item["output"]
        feedback = item["feedback"]
        resolved = item["resolved"]
        lines.append(
            "| `{stage}` | `{cell}` | `{present}` | `{sha}` | {feedback} | {resolved} |".format(
                stage=item["stage_id"],
                cell=output.get("cell") or "-",
                present=str(output["present"]).lower(),
                sha=output.get("sha256") or "-",
                feedback=_table_text(feedback.get("value")),
                resolved=_table_text(resolved.get("value")),
            )
        )
    return lines


def _normalization_lines(comparison: dict) -> list[str]:
    mappings = comparison["source_normalization_mappings"]
    if not mappings:
        return ["本组没有 source-input normalization。"]
    lines = [
        "| raw ref | rule | before | after |",
        "|---|---|---|---|",
    ]
    for item in mappings:
        lines.append(
            f"| `{item['raw_ref']}` | `{item['rule_id']}` | "
            f"`{_table_text(item['before'])}` | `{_table_text(item['after'])}` |"
        )
    return lines


def _official_identity_lines(reconciliation: dict) -> list[str]:
    lines = [
        f"- status：`{reconciliation['status']}`",
        f"- canonical / official states：`{reconciliation['canonical_state_count_after']}` / `{reconciliation['official_state_count']}`",
        f"- aligned transition endpoints：`{reconciliation['transition_identity_alignment_count']}`",
    ]
    state_remaps = reconciliation["state_identity_remaps"]
    transition_remaps = reconciliation["transition_endpoint_remaps"]
    if state_remaps:
        lines.extend(
            [
                "",
                "| source-parser identity | pinned PlantUML identity | raw ref | reason |",
                "|---|---|---|---|",
                *[
                    f"| `{item['before']}` | `{item['after']}` | `{item['raw_ref']}` | `{item['reason']}` |"
                    for item in state_remaps
                ],
            ]
        )
    else:
        lines.extend(["", "本组 state identity 无需重映射。"])
    if transition_remaps:
        lines.extend(
            [
                "",
                "| transition | source before -> after | target before -> after | raw ref |",
                "|---|---|---|---|",
                *[
                    "| `{transition}` | `{source_before}` -> `{source_after}` | "
                    "`{target_before}` -> `{target_after}` | `{raw_ref}` |".format(
                        transition=item["transition_id"],
                        source_before=item["source_before"],
                        source_after=item["source_after"],
                        target_before=item["target_before"],
                        target_after=item["target_after"],
                        raw_ref=item["raw_ref"],
                    )
                    for item in transition_remaps
                ],
            ]
        )
    else:
        lines.extend(["", "本组 transition endpoint 无需重映射。"])
    return lines


def _concurrent_region_lines(comparison: dict) -> list[str]:
    mappings = comparison["concurrent_region_mappings"]
    if not mappings:
        return ["本组没有 PlantUML orthogonal/concurrent region separator。"]
    lines = [
        "| owner | region | direct states | direct transitions | separator before | separator after |",
        "|---|---:|---|---|---|---|",
    ]
    for item in mappings:
        lines.append(
            "| `{owner}` | {region} | {states} | {transitions} | {before} | {after} |".format(
                owner=item.get("owner_scope") or "__root__",
                region=item["region_index"],
                states=_table_text(", ".join(item["state_ids"]) or "-"),
                transitions=_table_text(", ".join(item["transition_ids"]) or "-"),
                before=_table_text(", ".join(item["separator_before_raw_refs"]) or "-"),
                after=_table_text(", ".join(item["separator_after_raw_refs"]) or "-"),
            )
        )
    return lines


def _debt_lines(comparison: dict) -> list[str]:
    reasons = Counter(item["reason_code"] for item in comparison["operational_debts"])
    return [
        "| reason code | count |",
        "|---|---:|",
        *[f"| `{reason}` | {count} |" for reason, count in sorted(reasons.items())],
    ]


def _semantic_correspondence_lines(review: dict[str, Any]) -> list[str]:
    lines = [
        "| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for item in review["semantic_correspondences"]:
        lines.append(
            f"| `{item['projection_kind']}` | `{item['assessment']}` | "
            f"{_table_text(item['nl_anchor'])} | {_table_text(item['plantuml_anchor'])} | "
            f"{_table_text(item['fcstm_anchor'])} | "
            f"{_table_text(', '.join(item['source_element_ids']))} | "
            f"{_table_text(', '.join(item['compiler_element_ids']) or '-')} | "
            f"{_table_text(item['rationale'])} |"
        )
    return lines


def _risk_assessment_lines(review: dict[str, Any]) -> list[str]:
    assessments = review["second_pass"]["risk_assessments"]
    if not assessments:
        return ["本组不要求 risk-tag 第二遍复核。"]
    lines = [
        "| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in assessments:
        lines.append(
            f"| `{item['obligation_id']}` | `{item['risk_tag']}` | "
            f"`{item['assessment']}` | "
            f"{_table_text(', '.join(item['plantuml_anchors']))} | "
            f"{_table_text(', '.join(item['fcstm_anchors']))} | "
            f"{_table_text(', '.join(item['element_ids']))} | "
            f"{_table_text(item['rationale'])} |"
        )
    return lines


def _display(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def _current_implementation_sha256() -> str:
    return relevant_implementation_sha256(
        repo_root=REPO_ROOT,
        paper_root=PAPER_ROOT,
    )


def _current_java_frontend_build() -> dict[str, Any]:
    # Rebuild before comparing with the frozen manifest so ignored bytecode and
    # its cache fingerprint cannot jointly impersonate the reviewed executable.
    return java_frontend_build_identity(force=True)


def _current_java_frontend_source_identity() -> dict[str, Any]:
    return java_frontend_source_identity(_current_java_frontend_build())


def _current_pyfcstm_commit() -> str:
    completed = subprocess.run(
        ["git", "-C", str(REPO_ROOT / "pyfcstm"), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "pyfcstm commit identity is unavailable: " + completed.stderr.strip()
        )
    return completed.stdout.strip()


def _safe_artifact_path(evidence_dir: Path, relative: str) -> Path:
    if relative.startswith("/") or ".." in Path(relative).parts:
        raise RuntimeError(f"unsafe artifact path: {relative}")
    unresolved = evidence_dir / relative
    if unresolved.is_symlink():
        raise RuntimeError(f"artifact is a symlink: {relative}")
    path = unresolved.resolve()
    root = evidence_dir.resolve()
    if path != root and root not in path.parents:
        raise RuntimeError(f"artifact escapes evidence directory: {relative}")
    if not path.is_file():
        raise RuntimeError(f"artifact is not a regular file: {relative}")
    return path


def _validate_manifest(evidence_dir: Path, *, allow_ineligible: bool) -> dict[str, Any]:
    manifest_path = evidence_dir / "manifest.json"
    manifest = _read_json(manifest_path)
    if manifest.get("schema_version") != "r4_5.llms_emp_java_batch.v6":
        raise RuntimeError("pair pages require the v6 attribution-scoped manifest")
    if not manifest.get("evidence_eligible") and not allow_ineligible:
        raise RuntimeError(
            "pair pages require clean evidence; development replay is ineligible"
        )
    if manifest.get("output_dir") != _display(evidence_dir):
        raise RuntimeError(
            "manifest output directory does not match the selected evidence directory"
        )
    if manifest.get("implementation_tree_sha256") != _current_implementation_sha256():
        raise RuntimeError(
            "manifest implementation-tree hash is stale; rerun the 60-case machine "
            "evidence with the current implementation before publishing pair pages"
        )
    try:
        frozen_java_source_identity = java_frontend_source_identity(
            manifest.get("java_frontend_build")
        )
    except RuntimeError as exc:
        raise RuntimeError("manifest Java frontend producer build is invalid") from exc
    if manifest.get("java_frontend_source_identity") != frozen_java_source_identity:
        raise RuntimeError("manifest Java frontend source identity is inconsistent")
    if frozen_java_source_identity != _current_java_frontend_source_identity():
        raise RuntimeError(
            "manifest Java frontend source identity is stale; rerun the 60-case "
            "machine evidence with the current source tree and pinned jar"
        )
    if manifest.get("pyfcstm_commit") != _current_pyfcstm_commit():
        raise RuntimeError(
            "manifest pyfcstm commit is stale; rerun the 60-case machine evidence"
        )
    inventory = manifest.get("artifact_inventory", [])
    if manifest.get("artifact_set_sha256") != _sha256_json(inventory):
        raise RuntimeError("manifest artifact-set hash drift")
    seen: set[str] = set()
    for item in inventory:
        relative = item.get("path")
        if not isinstance(relative, str) or relative in seen:
            raise RuntimeError("manifest artifact paths are missing or duplicated")
        seen.add(relative)
        path = _safe_artifact_path(evidence_dir, relative)
        if _sha256_bytes(path.read_bytes()) != item.get("sha256"):
            raise RuntimeError(f"manifest artifact hash drift: {relative}")
    included_dirs = {
        "canonical",
        "fcstm",
        "case_reports",
        "parse_inspect",
        "working_contracts",
        "source_traces",
    }
    actual_inventory = []
    for path in sorted(evidence_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(evidence_dir)
        if relative.parts[0] not in included_dirs and relative.name not in {
            "comparison.jsonl",
            "official_models.jsonl",
        }:
            continue
        if path.is_symlink():
            raise RuntimeError(f"machine artifact is a symlink: {relative.as_posix()}")
        actual_inventory.append(
            {
                "path": relative.as_posix(),
                "sha256": _sha256_bytes(path.read_bytes()),
            }
        )
    if actual_inventory != inventory:
        raise RuntimeError(
            "manifest artifact inventory does not match the evidence directory"
        )
    contract_inventory = [
        item for item in inventory if item["path"].startswith("working_contracts/")
    ]
    if len(contract_inventory) != 60:
        raise RuntimeError("manifest does not contain exactly 60 working contracts")
    if manifest.get("working_contract_set_sha256") != _sha256_json(contract_inventory):
        raise RuntimeError("manifest working-contract set hash drift")
    supporting_inventory = manifest.get("supporting_artifact_inventory")
    if not isinstance(supporting_inventory, list) or manifest.get(
        "supporting_artifact_set_sha256"
    ) != _sha256_json(supporting_inventory):
        raise RuntimeError("manifest supporting-artifact set hash drift")
    expected_supporting_paths = [
        ".gitattributes",
        "MANUAL_REVIEW_TEMPLATE.jsonl",
        "MANUAL_REVIEW_TEMPLATE.md",
        "SUMMARY.md",
    ]
    if [item.get("path") for item in supporting_inventory] != expected_supporting_paths:
        raise RuntimeError("manifest supporting-artifact inventory drift")
    for item in supporting_inventory:
        path = _safe_artifact_path(evidence_dir, item["path"])
        if _sha256_bytes(path.read_bytes()) != item.get("sha256"):
            raise RuntimeError(
                f"manifest supporting-artifact hash drift: {item['path']}"
            )
    return manifest


def _validate_pairs_input(manifest: dict[str, Any], pairs_path: Path) -> None:
    if manifest.get("pairs_path") != _display(pairs_path):
        raise RuntimeError("manifest pair-pool path does not match the selected input")
    if manifest.get("pairs_sha256") != _sha256_bytes(pairs_path.read_bytes()):
        raise RuntimeError("manifest pair-pool hash drift")


def _ordered_rows(path: Path, identity_key: str) -> list[dict[str, Any]]:
    rows = _read_jsonl(path)
    cases = [str(row.get(identity_key, ""))[-4:] for row in rows]
    if cases != EXPECTED_CASES:
        raise RuntimeError(f"{path.name} is not the ordered 0000..0059 batch: {cases}")
    return rows


def _validate_review(
    *,
    review: dict[str, Any],
    case_id: str,
    pair_id: str,
    comparison: dict[str, Any],
    contract: dict[str, Any],
    contract_sha256: str,
    nl_text: str,
    source_text: str,
    fcstm_text: str,
    validator: Draft202012Validator,
) -> None:
    try:
        validate_manual_pair_review(
            review=review,
            case_id=case_id,
            pair_id=pair_id,
            review_subject_sha256=comparison["review_subject_sha256"],
            contract=contract,
            contract_sha256=contract_sha256,
            nl_text=nl_text,
            source_text=source_text,
            fcstm_text=fcstm_text,
            validator=validator,
        )
    except (ValueError, ValidationError) as exc:
        raise RuntimeError(str(exc)) from exc




def _observation_digest(review: dict[str, Any]) -> str:
    return manual_review_observation_digest(review)


def _validate_contract_artifact_bindings(
    *,
    evidence_dir: Path,
    pair_id: str,
    case_id: str,
    comparison: dict[str, Any],
    detailed: dict[str, Any],
    case_report: dict[str, Any],
    case_report_path: Path,
    contract: dict[str, Any],
    source_trace: dict[str, Any],
) -> dict[str, Path]:
    canonical_path = evidence_dir / "canonical" / f"{pair_id}.json"
    fcstm_path = evidence_dir / "fcstm" / f"{pair_id}.fcstm"
    inspect_path = evidence_dir / "parse_inspect" / f"{pair_id}.json"
    source_trace_path = evidence_dir / "source_traces" / f"{pair_id}.json"
    bindings = contract["artifact_bindings"]
    expected_paths = {
        "canonical_path": canonical_path,
        "fcstm_path": fcstm_path,
        "parse_inspect_path": inspect_path,
        "source_trace_path": source_trace_path,
    }
    for field, path in expected_paths.items():
        if bindings[field] != _display(path):
            raise RuntimeError(f"working-contract {field} drift for {case_id}")
    expected_binding_hashes = {
        "canonical_file_sha256": _sha256_bytes(canonical_path.read_bytes()),
        "fcstm_file_sha256": _sha256_bytes(fcstm_path.read_bytes()),
        "parse_inspect_file_sha256": _sha256_bytes(inspect_path.read_bytes()),
        "source_trace_file_sha256": _sha256_bytes(source_trace_path.read_bytes()),
        "comparison_sha256": _sha256_json(detailed),
        "ast_audit_sha256": _sha256_json(case_report["ast_audit"]),
    }
    for field, value in expected_binding_hashes.items():
        if bindings[field] != value:
            raise RuntimeError(f"working-contract {field} drift for {case_id}")
    if contract["source_trace_base"] != source_trace:
        raise RuntimeError(f"source-trace/contract content drift for {case_id}")
    if _sha256_bytes(case_report_path.read_bytes()) != comparison["case_report_sha256"]:
        raise RuntimeError(f"comparison case-report hash drift for {case_id}")
    return expected_paths


def _manual_review_markdown(
    reviews: list[dict[str, Any]], *, evidence_eligible: bool
) -> str:
    lines = [
        "# LLMS-EMP Phase-II final 60 例 attribution-safe 人工/LLM 对读账本",
        "",
        "本账本由 `MANUAL_REVIEW.jsonl` 确定性生成。每一行均绑定当前 review subject 与 working contract 哈希；PASS 表示完整阅读 NL、PlantUML、FCSTM、ownership/macro/capability contract 和 source trace，不表示全局行为等价。",
        "",
        "| case | review subject SHA-256 | working contract SHA-256 | source anchors | FCSTM anchors | correspondences | risk assessments | ownership | macro | capability | second pass | verdict | notes |",
        "|---|---|---|---|---|---:|---:|---|---|---|---|---|---|",
    ]
    if not evidence_eligible:
        lines[2:2] = [
            "> **DEVELOPMENT ONLY**：本账本绑定的是 dirty/ineligible replay，不得作为正式 60 例验收或 READY 证据。",
            "",
        ]
    for review in reviews:
        second_pass = (
            "completed" if review["second_pass"]["required"] else "not_required"
        )
        lines.append(
            f"| `{review['case_id']}` | `{review['review_subject_sha256']}` | "
            f"`{review['working_contract_sha256']}` | {_table_text(', '.join(review['observations']['plantuml_anchors']))} | "
            f"{_table_text(', '.join(review['observations']['fcstm_anchors']))} | "
            f"{len(review['semantic_correspondences'])} | "
            f"{len(review['second_pass']['risk_assessments'])} | `{review['ownership_verdict']}` | "
            f"`{review['macro_verdict']}` | `{review['capability_verdict']}` | "
            f"`{second_pass}` | `{review['verdict']}` | {_table_text(review['notes'])} |"
        )
    lines.append("")
    return "\n".join(lines)


def _atomic_publish(staging_dir: Path, evidence_dir: Path) -> None:
    backup = evidence_dir.with_name(
        f".{evidence_dir.name}.pair-backup-{uuid.uuid4().hex}"
    )
    try:
        evidence_dir.rename(backup)
        staging_dir.rename(evidence_dir)
    except Exception:
        if not evidence_dir.exists() and backup.exists():
            backup.rename(evidence_dir)
        raise
    else:
        shutil.rmtree(backup)


def _derived_inventory(staging_dir: Path) -> list[dict[str, str]]:
    paths = [
        staging_dir / "MANUAL_REVIEW.jsonl",
        staging_dir / "MANUAL_REVIEW.md",
        staging_dir / "PAIR_INDEX.md",
        *sorted((staging_dir / "pairs").rglob("*")),
    ]
    rows = []
    for path in paths:
        if path.is_symlink():
            raise RuntimeError(
                f"derived publication artifact is a symlink: {path.relative_to(staging_dir)}"
            )
        if path.is_file():
            rows.append(
                {
                    "path": path.relative_to(staging_dir).as_posix(),
                    "sha256": _sha256_bytes(path.read_bytes()),
                }
            )
    return rows


def _check_publication(
    *, evidence_dir: Path, staging_dir: Path, derived_inventory: list[dict[str, str]]
) -> None:
    current_inventory = _derived_inventory(evidence_dir)
    if current_inventory != derived_inventory:
        raise RuntimeError("generated pair publication inventory drift")
    expected_seal = staging_dir / "PUBLICATION_SEAL.json"
    current_seal = evidence_dir / "PUBLICATION_SEAL.json"
    if (
        not current_seal.is_file()
        or current_seal.is_symlink()
        or _sha256_bytes(current_seal.read_bytes())
        != _sha256_bytes(expected_seal.read_bytes())
    ):
        raise RuntimeError("generated pair publication drift: PUBLICATION_SEAL.json")


def build_pair_pages(
    *,
    pairs_path: Path = DEFAULT_PAIRS_PATH,
    evidence_dir: Path = DEFAULT_EVIDENCE_DIR,
    manual_review_path: Path | None = None,
    allow_ineligible: bool = False,
    check: bool = False,
) -> dict[str, Any]:
    evidence_dir = evidence_dir.resolve()
    manual_review_path = (
        manual_review_path or evidence_dir / "MANUAL_REVIEW.jsonl"
    ).resolve()
    pairs_path = pairs_path.resolve()
    manifest = _validate_manifest(evidence_dir, allow_ineligible=allow_ineligible)
    _validate_pairs_input(manifest, pairs_path)
    source_rows = _ordered_rows(pairs_path, "pair_id")
    comparison_list = _ordered_rows(evidence_dir / "comparison.jsonl", "case_id")
    review_list = _ordered_rows(manual_review_path, "case_id")
    comparison_rows = {row["case_id"]: row for row in comparison_list}
    reviews = {row["case_id"]: row for row in review_list}
    review_validator = Draft202012Validator(_read_json(MANUAL_REVIEW_SCHEMA))

    staging_dir = evidence_dir.with_name(
        f".{evidence_dir.name}.pair-tmp-{uuid.uuid4().hex}"
    )
    try:
        shutil.copytree(evidence_dir, staging_dir, symlinks=False)
        pages_dir = staging_dir / "pairs"
        if pages_dir.exists():
            shutil.rmtree(pages_dir)
        pages_dir.mkdir()
        for stale in (
            staging_dir / "PAIR_INDEX.md",
            staging_dir / "MANUAL_REVIEW.md",
            staging_dir / "PUBLICATION_SEAL.json",
        ):
            stale.unlink(missing_ok=True)
        (staging_dir / "MANUAL_REVIEW.jsonl").write_bytes(
            manual_review_path.read_bytes()
        )

        index_lines = [
            "# LLMS-EMP Phase-II final 60 组 NL + PlantUML STM0 + FCSTM STM0",
            "",
            "从 `0000` 到 `0059` 点击“3-in-one Markdown”，可在同一页面完整审阅 NL、作者 Phase-II 最终 PlantUML、转换后 FCSTM、ownership/macro/capability 结论。每组同时保留三个原始文件。",
            "",
            "`structure_preserved` 只表示 source identity 与结构 occurrence 全量保存。`discover_input_with_capability_mask` 表示可进入 attribution-scoped Discover；它不表示全局 behavior equivalence，simulation/transition trace 必须继续服从逐元素 capability。",
            "",
            "| case | LLM | 模型/场景 | 3-in-one Markdown | 原始 NL | 原始 PlantUML | 原始 FCSTM | 结构 | source static | simulation | review |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        if not manifest["evidence_eligible"]:
            index_lines[2:2] = [
                "> **DEVELOPMENT ONLY**：当前是 dirty/ineligible replay，只可验证生成器，不得作为正式人工验收或 READY 证据。",
                "",
            ]
        observation_digests: set[str] = set()
        for index, source_row in enumerate(source_rows):
            pair_id = source_row["pair_id"]
            case_id = pair_id[-4:]
            comparison = comparison_rows[case_id]
            case_report_path = evidence_dir / "case_reports" / f"{pair_id}.json"
            contract_path = evidence_dir / "working_contracts" / f"{pair_id}.json"
            source_trace_path = evidence_dir / "source_traces" / f"{pair_id}.json"
            case_report = _read_json(case_report_path)
            contract = _read_json(contract_path)
            source_trace = _read_json(source_trace_path)
            contract_sha256 = _sha256_bytes(contract_path.read_bytes())
            nl_text = source_row["nl_text"]
            source_text = source_row["stm0_text"]
            fcstm_path = evidence_dir / "fcstm" / f"{pair_id}.fcstm"
            fcstm_text = fcstm_path.read_text(encoding="utf-8")
            _validate_review(
                review=reviews[case_id],
                case_id=case_id,
                pair_id=pair_id,
                comparison=comparison,
                contract=contract,
                contract_sha256=contract_sha256,
                nl_text=nl_text,
                source_text=source_text,
                fcstm_text=fcstm_text,
                validator=review_validator,
            )
            observation_digest = _observation_digest(reviews[case_id])
            if observation_digest in observation_digests:
                raise RuntimeError(
                    f"manual review reused generic observations for {case_id}"
                )
            observation_digests.add(observation_digest)
            if case_report["schema_version"] != "r4_5.llms_emp_java_case_report.v5":
                raise RuntimeError(f"case-report schema drift for {case_id}")
            if case_report["case_id"] != case_id or case_report["pair_id"] != pair_id:
                raise RuntimeError(f"case-report identity drift for {case_id}")
            if case_report["working_contract_sha256"] != contract_sha256:
                raise RuntimeError(f"case-report contract hash drift for {case_id}")
            if (
                contract["review_subject"]["review_subject_sha256"]
                != comparison["review_subject_sha256"]
            ):
                raise RuntimeError(
                    f"working-contract review subject drift for {case_id}"
                )
            if contract["usage_gate"] != "discover_input_with_capability_mask":
                raise RuntimeError(
                    f"working bundle is not attribution-scoped Discover input: {case_id}"
                )
            if (
                contract["attribution_policy"]["main_result_conversion_artifact_limit"]
                != 0
            ):
                raise RuntimeError(
                    f"conversion-artifact main-result gate drift for {case_id}"
                )

            detailed = case_report["comparison"]
            _validate_contract_artifact_bindings(
                evidence_dir=evidence_dir,
                pair_id=pair_id,
                case_id=case_id,
                comparison=comparison,
                detailed=detailed,
                case_report=case_report,
                case_report_path=case_report_path,
                contract=contract,
                source_trace=source_trace,
            )
            bindings = contract["artifact_bindings"]
            nl_sha256 = _sha256_text(nl_text)
            source_sha256 = _sha256_text(source_text)
            fcstm_sha256 = _sha256_text(fcstm_text)
            hashes = bindings
            expected = {
                "nl": (nl_sha256, source_row["nl_sha256"]),
                "source": (source_sha256, source_row["stm0_sha256"]),
                "comparison_source": (source_sha256, comparison["source_sha256"]),
                "comparison_fcstm": (fcstm_sha256, comparison["fcstm_sha256"]),
                "contract_fcstm": (fcstm_sha256, hashes["fcstm_file_sha256"]),
                "contract_source_trace": (
                    _sha256_bytes(source_trace_path.read_bytes()),
                    hashes["source_trace_file_sha256"],
                ),
            }
            for label, (actual, recorded) in expected.items():
                if actual != recorded:
                    raise RuntimeError(f"{label} hash drift for {case_id}")

            official_identity = case_report["official_identity_reconciliation"]
            review = reviews[case_id]
            case_dir = pages_dir / case_id
            case_dir.mkdir()
            (case_dir / "nl.txt").write_text(nl_text, encoding="utf-8")
            (case_dir / "plantuml.puml").write_text(source_text, encoding="utf-8")
            (case_dir / "fcstm.fcstm").write_text(fcstm_text, encoding="utf-8")

            navigation = []
            if index > 0:
                navigation.append(
                    f"[上一组 `{index - 1:04d}`](../{index - 1:04d}/README.md)"
                )
            navigation.append("[返回 60 组索引](../../PAIR_INDEX.md)")
            if index + 1 < len(source_rows):
                navigation.append(
                    f"[下一组 `{index + 1:04d}`](../{index + 1:04d}/README.md)"
                )
            capabilities = contract["capability_eligibility"]
            origins = contract["summary"]["origin_counts"]
            page_lines = [
                f"# Pair `{case_id}`：NL + PlantUML STM0 + FCSTM STM0",
                "",
                " | ".join(navigation),
                "",
                f"- LLM：`{source_row.get('llm') or '-'}`",
                f"- 模型/场景：{_table_text(source_row.get('model_name'))}",
                f"- 作者输出阶段：`{source_row['selected_stage_column']}`",
                f"- 作者输出单元格：`{source_row['selected_stage_cell']}`；Excel row：`{source_row['source_excel_row']}`",
                f"- Phase-I fallback：`{str(source_row['is_phase_i_fallback']).lower()}`",
                f"- 相对 Phase-I 是否变化：`{str(source_row['phase_i_changed']).lower()}`",
                f"- Phase-I PlantUML SHA-256：`{source_row['phase_i_stm0_sha256']}`",
                f"- NL SHA-256：`{nl_sha256}`",
                f"- PlantUML SHA-256：`{source_sha256}`",
                f"- FCSTM SHA-256：`{fcstm_sha256}`",
                f"- review subject SHA-256：`{review['review_subject_sha256']}`",
                f"- working contract SHA-256：`{contract_sha256}`",
                f"- 结构裁决：`{comparison['verdict']}`",
                f"- source states / transitions：`{comparison['source_state_count']}` / `{comparison['source_transition_count']}`",
                f"- mapped / blocked / silent drop：`{comparison['mapped_transition_count']}` / `{comparison['blocked_transition_count']}` / `{comparison['silently_dropped_transition_count']}`",
                f"- final / lifecycle / body coverage：`{comparison['final_transition_coverage']}` / `{comparison['lifecycle_action_coverage']}` / `{comparison['body_line_coverage']}`",
                f"- concurrent region / separator coverage：`{comparison['concurrent_region_coverage']}` / `{comparison['concurrent_region_separator_coverage']}`",
                f"- source normalization coverage：`{comparison['source_normalization_coverage']}`",
                f"- official raw / validation：`{comparison['official_raw_status']}` / `{comparison['official_validation_status']}`",
                f"- official identity states / transitions：`{comparison['official_identity_state_count']}` / `{comparison['official_identity_transition_count']}`",
                f"- official identity remaps：state `{comparison['official_identity_state_remap_count']}` / transition endpoint `{comparison['official_identity_transition_remap_count']}`",
                f"- AST audit：`{comparison['ast_audit_status']}`",
                f"- legacy whole-model FCSTM execution / Discover：`{str(comparison['fcstm_execution_eligible']).lower()}` / `{str(comparison['discover_eligible']).lower()}`",
                f"- working bundle usage gate：`{contract['usage_gate']}`",
                f"- ownership source / compiler / agent：`{origins.get('source_owned', 0)}` / `{origins.get('compiler_owned', 0)}` / `{origins.get('agent_created', 0)}`",
                f"- source macro / positive identity trace / conversion boundary trace：`{contract['summary']['macro_count']}` / `{contract['summary']['positive_trace_count']}` / `{contract['summary']['boundary_trace_count']}`",
                f"- capability source-static / simulation / transition-trace：`{capabilities['source_static_discovery']['status']}` / `{capabilities['simulation']['status']}` / `{capabilities['transition_trace']['status']}`",
                f"- compiler-only diagnostic policy：`{contract['attribution_policy']['compiler_only_diagnostic']}`；main-result conversion artifact limit：`0`",
                f"- 主 session 对读：`{review['verdict']}`；ownership/macro/capability 均为 `pass`；{_table_text(review['notes'])}",
                f"- source anchors：`{_table_text(', '.join(review['observations']['plantuml_anchors']))}`；FCSTM anchors：`{_table_text(', '.join(review['observations']['fcstm_anchors']))}`",
                "- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)",
                "- 审计入口："
                f"[canonical](../../canonical/{pair_id}.json) | "
                f"[冻结 FCSTM](../../fcstm/{pair_id}.fcstm) | "
                f"[case report](../../case_reports/{pair_id}.json) | "
                f"[working contract](../../working_contracts/{pair_id}.json) | "
                f"[source trace](../../source_traces/{pair_id}.json) | "
                "[人工总账](../../MANUAL_REVIEW.md)",
                "",
                "## 主 session 三方语义对应",
                "",
                *_semantic_correspondence_lines(review),
                "",
                "## Risk occurrence 第二遍复核",
                "",
                *_risk_assessment_lines(review),
                "",
                "## 作者阶段 lineage",
                "",
                *_stage_lineage_lines(source_row),
                "",
                "## Official identity ledger",
                "",
                *_official_identity_lines(official_identity),
                "",
                "## Source normalization ledger",
                "",
                *_normalization_lines(detailed),
                "",
                "## Concurrent region ledger",
                "",
                *_concurrent_region_lines(detailed),
                "",
                "## Operational debt",
                "",
                *_debt_lines(detailed),
                "",
                "## NL",
                "",
                _fence("text", _display_text(nl_text)),
                "",
                "## 作者 Phase-II 最终 PlantUML STM0",
                "",
                _fence("plantuml", source_text),
                "",
                "## 转换后 FCSTM STM0",
                "",
                _fence("fcstm", fcstm_text),
                "",
                " | ".join(navigation),
                "",
            ]
            if not manifest["evidence_eligible"]:
                page_lines[2:2] = [
                    "> **DEVELOPMENT ONLY**：本页来自 ineligible replay，不得作为正式人工验收或 READY 证据。",
                    "",
                ]
            (case_dir / "README.md").write_text("\n".join(page_lines), encoding="utf-8")
            index_lines.append(
                "| `{case}` | `{llm}` | {model} | [查看三元组](./pairs/{case}/README.md) | "
                "[nl.txt](./pairs/{case}/nl.txt) | [plantuml.puml](./pairs/{case}/plantuml.puml) | "
                "[fcstm.fcstm](./pairs/{case}/fcstm.fcstm) | `{verdict}` | `{source_static}` | "
                "`{simulation}` | `{review}` |".format(
                    case=case_id,
                    llm=_table_text(source_row.get("llm")),
                    model=_table_text(source_row.get("model_name")),
                    verdict=comparison["verdict"],
                    source_static=capabilities["source_static_discovery"]["status"],
                    simulation=capabilities["simulation"]["status"],
                    review=review["verdict"],
                )
            )

        (staging_dir / "PAIR_INDEX.md").write_text(
            "\n".join(index_lines) + "\n", encoding="utf-8"
        )
        (staging_dir / "MANUAL_REVIEW.md").write_text(
            _manual_review_markdown(
                review_list, evidence_eligible=manifest["evidence_eligible"]
            ),
            encoding="utf-8",
        )
        derived_inventory = _derived_inventory(staging_dir)
        seal = {
            "schema_version": "paper1.llms_emp_pair_publication.v1",
            "case_count": 60,
            "evidence_eligible": manifest["evidence_eligible"],
            "status": (
                "main_session_reviewed_ready_for_discover"
                if manifest["evidence_eligible"]
                else "development_only"
            ),
            "manifest_sha256": _sha256_bytes(
                (evidence_dir / "manifest.json").read_bytes()
            ),
            "artifact_set_sha256": manifest["artifact_set_sha256"],
            "working_contract_set_sha256": manifest["working_contract_set_sha256"],
            "manual_review_file_sha256": _sha256_bytes(manual_review_path.read_bytes()),
            "manual_review_set_sha256": _sha256_json(review_list),
            "derived_artifact_inventory": derived_inventory,
            "derived_artifact_set_sha256": _sha256_json(derived_inventory),
            "pair_index_sha256": _sha256_bytes(
                (staging_dir / "PAIR_INDEX.md").read_bytes()
            ),
        }
        (staging_dir / "PUBLICATION_SEAL.json").write_text(
            json.dumps(seal, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if check:
            _check_publication(
                evidence_dir=evidence_dir,
                staging_dir=staging_dir,
                derived_inventory=derived_inventory,
            )
            shutil.rmtree(staging_dir)
        else:
            _atomic_publish(staging_dir, evidence_dir)
        return seal
    except Exception:
        if staging_dir.exists():
            shutil.rmtree(staging_dir)
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pairs", type=Path, default=DEFAULT_PAIRS_PATH)
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE_DIR)
    parser.add_argument("--manual-review-jsonl", type=Path)
    parser.add_argument("--allow-ineligible", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    seal = build_pair_pages(
        pairs_path=args.pairs,
        evidence_dir=args.evidence_dir,
        manual_review_path=args.manual_review_jsonl,
        allow_ineligible=args.allow_ineligible,
        check=args.check,
    )
    print(json.dumps(seal, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
