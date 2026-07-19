from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

from .manual_pair_review import (
    manual_review_observation_digest,
    validate_manual_pair_review,
)
from .plantuml_working_contract import validate_working_contract


MANIFEST_SCHEMA_VERSION = "r4_5.llms_emp_java_batch.v5"
PUBLICATION_SCHEMA_VERSION = "paper1.llms_emp_pair_publication.v1"
PUBLICATION_READY_STATUS = "main_session_reviewed_ready_for_discover"
EXPECTED_CASE_IDS = [f"{index:04d}" for index in range(60)]


class WorkingBundleError(ValueError):
    """Raised when a PlantUML working bundle cannot support attributed use."""


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _sha256_json(value: Any) -> str:
    return _sha256_text(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def _read_json(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise WorkingBundleError(f"bundle artifact is not a regular file: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise WorkingBundleError(f"bundle artifact is not a JSON object: {path}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if path.is_symlink() or not path.is_file():
        raise WorkingBundleError(f"bundle artifact is not a regular file: {path}")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise WorkingBundleError(
                f"bundle JSONL row is not an object: {path}:{line_number}"
            )
        rows.append(value)
    return rows


def _safe_repo_path(repo_root: Path, relative: str) -> Path:
    path_value = Path(relative)
    if path_value.is_absolute() or ".." in path_value.parts:
        raise WorkingBundleError(f"unsafe repository artifact path: {relative}")
    unresolved = repo_root / path_value
    if unresolved.is_symlink():
        raise WorkingBundleError(f"repository artifact is a symlink: {relative}")
    path = unresolved.resolve()
    root = repo_root.resolve()
    if path != root and root not in path.parents:
        raise WorkingBundleError(f"repository artifact escapes root: {relative}")
    return path


def _repo_relative(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise WorkingBundleError(f"bundle is outside repository root: {path}") from exc


def _current_implementation_sha256(repo_root: Path) -> str:
    try:
        from paper_stm_repair_conversion.evidence_integrity import (
            relevant_implementation_sha256,
        )
    except ImportError as exc:
        raise WorkingBundleError(
            "conversion evidence-integrity package is unavailable"
        ) from exc
    paper_root = (
        repo_root / "project_1_llm_state_machine_modeling/paper_stm_repair"
    )
    return relevant_implementation_sha256(
        repo_root=repo_root,
        paper_root=paper_root,
    )


@lru_cache(maxsize=1)
def _current_java_frontend_build() -> dict[str, Any]:
    try:
        from paper_stm_repair_conversion.adapters.plantuml_source import (
            java_frontend_build_identity,
        )
    except ImportError as exc:
        raise WorkingBundleError("PlantUML Java frontend package is unavailable") from exc
    return java_frontend_build_identity(force=False)


def _current_pyfcstm_commit(repo_root: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo_root / "pyfcstm"), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise WorkingBundleError(
            "pyfcstm commit identity is unavailable: " + completed.stderr.strip()
        )
    return completed.stdout.strip()


def _artifact_path(evidence_dir: Path, relative: str) -> Path:
    path_value = Path(relative)
    if path_value.is_absolute() or ".." in path_value.parts:
        raise WorkingBundleError(f"unsafe evidence artifact path: {relative}")
    unresolved = evidence_dir / path_value
    if unresolved.is_symlink():
        raise WorkingBundleError(f"evidence artifact is a symlink: {relative}")
    path = unresolved.resolve()
    root = evidence_dir.resolve()
    if path != root and root not in path.parents:
        raise WorkingBundleError(f"evidence artifact escapes directory: {relative}")
    if not path.is_file():
        raise WorkingBundleError(f"evidence artifact is missing: {relative}")
    return path


def _derived_publication_inventory(evidence_dir: Path) -> list[dict[str, str]]:
    paths = [
        evidence_dir / "MANUAL_REVIEW.jsonl",
        evidence_dir / "MANUAL_REVIEW.md",
        evidence_dir / "PAIR_INDEX.md",
        *sorted((evidence_dir / "pairs").rglob("*")),
    ]
    inventory: list[dict[str, str]] = []
    for path in paths:
        if path.is_symlink():
            raise WorkingBundleError(
                f"publication artifact is a symlink: {path.relative_to(evidence_dir)}"
            )
        if path.is_file():
            inventory.append(
                {
                    "path": path.relative_to(evidence_dir).as_posix(),
                    "sha256": _sha256_bytes(path.read_bytes()),
                }
            )
    return inventory


@dataclass(frozen=True)
class ConfirmedIssueBinding:
    issue_id: str
    source_element_ids: tuple[str, ...]
    positive_identity_trace_ids: tuple[str, ...]
    eligible_field_refs: tuple[str, ...]
    behavior_evidence_refs: tuple[str, ...]
    repair_authorized: bool = False


@dataclass(frozen=True)
class AttributionSafeWorkingBundle:
    repo_root: Path
    evidence_dir: Path
    case_id: str
    pair_id: str
    nl_text: str
    source_text: str
    fcstm_text: str
    _canonical: dict[str, Any]
    _inspect_report: dict[str, Any]
    _working_contract: dict[str, Any]
    _source_trace: dict[str, Any]
    _case_report: dict[str, Any]
    _comparison: dict[str, Any]

    @property
    def canonical(self) -> dict[str, Any]:
        return copy.deepcopy(self._canonical)

    @property
    def inspect_report(self) -> dict[str, Any]:
        return copy.deepcopy(self._inspect_report)

    @property
    def working_contract(self) -> dict[str, Any]:
        return copy.deepcopy(self._working_contract)

    @property
    def source_trace(self) -> dict[str, Any]:
        return copy.deepcopy(self._source_trace)

    @property
    def case_report(self) -> dict[str, Any]:
        return copy.deepcopy(self._case_report)

    @property
    def comparison(self) -> dict[str, Any]:
        return copy.deepcopy(self._comparison)

    def discover_view(self) -> dict[str, Any]:
        capability = self._working_contract["capability_eligibility"][
            "source_static_discovery"
        ]
        if capability["status"] not in {"eligible", "eligible_with_exclusions"}:
            raise WorkingBundleError("source-static Discover is not eligible")
        eligible_elements = set(capability["eligible_element_ids"])
        eligible_fields = set(capability["eligible_field_refs"])
        source_facts: list[dict[str, Any]] = []
        for element in self._working_contract["elements"]:
            element_id = element["element_id"]
            if element_id not in eligible_elements:
                continue
            fields = {
                field_name: copy.deepcopy(field_value)
                for field_name, field_value in element["semantic_fields"].items()
                if f"{element_id}#field:{field_name}" in eligible_fields
            }
            source_facts.append(
                {
                    "element_id": element_id,
                    "kind": element["kind"],
                    "source_refs": copy.deepcopy(element["source_refs"]),
                    "semantic_fields": fields,
                    "edit_policy": element["edit_policy"],
                }
            )
        attribution_policy = self._working_contract["attribution_policy"]
        return {
            "schema_version": "paper1.attribution_safe_discover_view.v1",
            "case_id": self.case_id,
            "pair_id": self.pair_id,
            "nl_text": self.nl_text,
            "source_plantuml": self.source_text,
            "fcstm_working_text": self.fcstm_text,
            "source_facts": source_facts,
            "protected_compiler_element_ids": sorted(
                item["element_id"]
                for item in self._working_contract["elements"]
                if item["origin"] == "compiler_owned"
            ),
            "macros": copy.deepcopy(self._working_contract["macros"]),
            "diagnostic_attribution": copy.deepcopy(
                self._working_contract["diagnostic_attribution"]
            ),
            "operational_debts": copy.deepcopy(
                self._case_report["comparison"]["operational_debts"]
            ),
            "capability_eligibility": copy.deepcopy(
                self._working_contract["capability_eligibility"]
            ),
            "evidence_binding": {
                "nl_sha256": _sha256_text(self.nl_text),
                "nl_reference_policy": "literal_substring_of_frozen_nl",
                "source_sha256": _sha256_text(self.source_text),
                "source_reference_inventory": {
                    item["element_id"]: copy.deepcopy(item["source_refs"])
                    for item in source_facts
                },
                "source_static_field_reference_inventory": sorted(eligible_fields),
            },
            "attribution_rules": {
                "compiler_only_diagnostic": attribution_policy[
                    "compiler_only_diagnostic"
                ],
                "macro_member_diagnostic": attribution_policy[
                    "macro_member_diagnostic"
                ],
                "candidate_conversion_artifact_policy": attribution_policy[
                    "candidate_conversion_artifact_policy"
                ],
                "source_internal_consistency_check_policy": attribution_policy[
                    "source_internal_consistency_check_policy"
                ],
                "confirmed_conversion_artifact_limit": attribution_policy[
                    "confirmed_issue_conversion_artifact_limit"
                ],
                "repair_conversion_artifact_limit": attribution_policy[
                    "repair_target_conversion_artifact_limit"
                ],
                "confirm_conversion_artifact_limit": attribution_policy[
                    "confirm_accepted_conversion_artifact_limit"
                ],
                "main_result_conversion_artifact_limit": attribution_policy[
                    "main_result_conversion_artifact_limit"
                ],
            },
        }

    def bind_confirmed_issues(
        self, issue_ledger: dict[str, Any]
    ) -> tuple[ConfirmedIssueBinding, ...]:
        schema_path = (
            self.repo_root
            / "project_1_llm_state_machine_modeling/paper_stm_repair"
            / "pipeline/evaluation/schemas/source_issue_ledger.schema.json"
        )
        try:
            Draft202012Validator(_read_json(schema_path)).validate(issue_ledger)
        except ValidationError as exc:
            raise WorkingBundleError(
                f"source issue ledger violates attribution contract: {exc.message}"
            ) from exc
        if issue_ledger["case_id"] not in {self.case_id, self.pair_id}:
            raise WorkingBundleError("source issue ledger case does not match bundle")
        if issue_ledger["source_model_id"] != self.pair_id:
            raise WorkingBundleError("source issue ledger model does not match bundle")

        elements = {
            item["element_id"]: item for item in self._working_contract["elements"]
        }
        positive_traces = {
            entry["source_elements"][0]: entry["trace_id"]
            for entry in self._source_trace["entries"]
        }
        source_capability = self._working_contract["capability_eligibility"][
            "source_static_discovery"
        ]
        eligible_source_ids = set(source_capability["eligible_element_ids"])
        eligible_fields = set(source_capability["eligible_field_refs"])
        potential_targets = set(
            self._working_contract["repair_gate"]["potential_source_target_ids"]
        )
        bindings: list[ConfirmedIssueBinding] = []
        for issue in issue_ledger["issues"]:
            if issue["confirmation_status"] != "confirmed":
                continue
            if not issue["downstream_repair_allowed"]:
                raise WorkingBundleError(
                    f"confirmed issue is not repair-eligible: {issue['issue_id']}"
                )
            boundary = issue["attribution_boundary"]
            if (
                not boundary["source_level_claim_allowed"]
                or boundary["conversion_or_lowering_related"]
                or boundary["representation_related"]
            ):
                raise WorkingBundleError(
                    f"confirmed issue crosses the conversion boundary: {issue['issue_id']}"
                )
            source_ids = tuple(
                item["element_id"] for item in issue["source_element_refs"]
            )
            if len(source_ids) != len(set(source_ids)):
                raise WorkingBundleError(
                    f"confirmed issue repeats source elements: {issue['issue_id']}"
                )
            if any(
                source_id not in elements
                or elements[source_id]["origin"] != "source_owned"
                or source_id not in positive_traces
                or source_id not in eligible_source_ids
                or source_id not in potential_targets
                for source_id in source_ids
            ):
                raise WorkingBundleError(
                    f"confirmed issue lacks an eligible positive source root: {issue['issue_id']}"
                )
            self._validate_source_evidence_bindings(
                issue=issue,
                source_ids=source_ids,
                elements=elements,
            )
            typed_field_refs = self._eligible_typed_evidence_refs(
                issue,
                source_ids=source_ids,
            )
            if not typed_field_refs:
                raise WorkingBundleError(
                    f"confirmed issue lacks capability-eligible typed evidence: {issue['issue_id']}"
                )
            field_refs = tuple(
                sorted(set(typed_field_refs).intersection(eligible_fields))
            )
            if not field_refs:
                raise WorkingBundleError(
                    f"confirmed issue has no source-owned patch fields: {issue['issue_id']}"
                )
            bindings.append(
                ConfirmedIssueBinding(
                    issue_id=issue["issue_id"],
                    source_element_ids=source_ids,
                    positive_identity_trace_ids=tuple(
                        positive_traces[source_id] for source_id in source_ids
                    ),
                    eligible_field_refs=field_refs,
                    behavior_evidence_refs=typed_field_refs,
                )
            )
        return tuple(bindings)

    def _validate_source_evidence_bindings(
        self,
        *,
        issue: dict[str, Any],
        source_ids: tuple[str, ...],
        elements: dict[str, dict[str, Any]],
    ) -> None:
        source_refs_by_id: dict[str, set[str]] = {}
        for source_id in source_ids:
            element = elements[source_id]
            source_refs_by_id[source_id] = set(element["source_refs"])

        for reference in issue["source_element_refs"]:
            source_id = reference["element_id"]
            if reference["reference"] not in source_refs_by_id[source_id]:
                raise WorkingBundleError(
                    f"confirmed issue source reference is not source-bound: "
                    f"{issue['issue_id']}:{source_id}"
                )

        allowed_source_refs = set().union(*source_refs_by_id.values())
        source_fragment_refs: set[str] = set()
        for item in issue["source_stm_evidence"]:
            if item["evidence_type"] != "source_stm_fragment":
                raise WorkingBundleError(
                    f"confirmed issue has non-source STM evidence: {issue['issue_id']}"
                )
            if item["reference"] not in allowed_source_refs:
                raise WorkingBundleError(
                    f"confirmed issue source STM evidence is not source-bound: "
                    f"{issue['issue_id']}:{item['reference']}"
                )
            source_fragment_refs.add(item["reference"])
        uncovered = [
            source_id
            for source_id, source_refs in source_refs_by_id.items()
            if not source_fragment_refs.intersection(source_refs)
        ]
        if uncovered:
            raise WorkingBundleError(
                f"confirmed issue source STM evidence is not source-bound: "
                f"{issue['issue_id']}:{','.join(uncovered)}"
            )

        if issue["confirmation_evidence_path"] == "nl_grounded_behavioral_issue":
            if any(
                item["evidence_type"] != "nl_requirement"
                or item["reference"] not in self.nl_text
                for item in issue["nl_evidence"]
            ):
                raise WorkingBundleError(
                    f"confirmed issue NL evidence is not source-bound: {issue['issue_id']}"
                )

    def _eligible_typed_evidence_refs(
        self,
        issue: dict[str, Any],
        *,
        source_ids: tuple[str, ...],
    ) -> tuple[str, ...]:
        capabilities = self._working_contract["capability_eligibility"]
        capability_by_evidence = {
            "source_internal_consistency_check": "source_static_discovery",
            "inspect_diagnostic": "inspect_diagnostics",
            "simulation_trace": "simulation",
            "probe_result": "simulation",
            "verification_counterexample": "verification",
        }
        bound_refs: set[str] = set()
        for item in issue["behavior_evidence"]:
            capability_name = capability_by_evidence.get(item["evidence_type"])
            if capability_name is None:
                raise WorkingBundleError(
                    f"confirmed issue has unsupported behavior evidence: "
                    f"{issue['issue_id']}:{item['evidence_type']}"
                )
            capability = capabilities.get(capability_name)
            if capability is None:
                raise WorkingBundleError(
                    f"confirmed issue behavior capability is unavailable: "
                    f"{issue['issue_id']}:{capability_name}"
                )
            if capability["status"] not in {"eligible", "eligible_with_exclusions"}:
                raise WorkingBundleError(
                    f"confirmed issue behavior evidence is capability-ineligible: "
                    f"{issue['issue_id']}:{capability_name}"
                )
            if item["evidence_type"] == "source_internal_consistency_check":
                raise WorkingBundleError(
                    "source consistency evidence lacks a manifest-bound executed checker "
                    f"artifact: {issue['issue_id']}"
                )
            if item["reference"] not in capability["evidence_refs"]:
                raise WorkingBundleError(
                    f"typed evidence is not capability-bound: {issue['issue_id']}"
                )
            bound_refs.add(item["reference"])
        return tuple(sorted(bound_refs))

    def validate_confirm_acceptance(self, disposition: dict[str, Any]) -> None:
        del disposition
        if self._working_contract["capability_eligibility"]["confirm"]["status"] == (
            "not_run"
        ):
            raise WorkingBundleError(
                "baseline working bundle cannot authorize Confirm acceptance"
            )
        raise WorkingBundleError("unsupported Confirm contract version")


def load_attribution_safe_working_bundle(
    evidence_dir: Path,
    case_id: str,
    *,
    repo_root: Path | None = None,
) -> AttributionSafeWorkingBundle:
    repo = (repo_root or _find_repo_root(evidence_dir)).resolve()
    evidence = evidence_dir.resolve()
    manifest = _read_json(evidence / "manifest.json")
    if manifest.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise WorkingBundleError("working bundle requires the v5 manifest")
    if manifest.get("evidence_eligible") is not True:
        raise WorkingBundleError("development-only evidence cannot enter Discover")
    if manifest.get("output_dir") != _repo_relative(repo, evidence):
        raise WorkingBundleError("manifest output directory does not match bundle")
    if manifest.get("implementation_tree_sha256") != _current_implementation_sha256(
        repo
    ):
        raise WorkingBundleError(
            "manifest implementation-tree hash is stale; replay and review are required"
        )
    if manifest.get("java_frontend_build") != _current_java_frontend_build():
        raise WorkingBundleError(
            "manifest Java frontend build is stale; replay and review are required"
        )
    if manifest.get("pyfcstm_commit") != _current_pyfcstm_commit(repo):
        raise WorkingBundleError(
            "manifest pyfcstm commit is stale; replay and review are required"
        )
    inventory = manifest.get("artifact_inventory")
    if not isinstance(inventory, list) or manifest.get(
        "artifact_set_sha256"
    ) != _sha256_json(inventory):
        raise WorkingBundleError("manifest artifact inventory digest drift")
    inventory_by_path: dict[str, str] = {}
    for item in inventory:
        relative = item.get("path")
        sha256 = item.get("sha256")
        if (
            not isinstance(relative, str)
            or not isinstance(sha256, str)
            or relative in inventory_by_path
        ):
            raise WorkingBundleError("manifest artifact inventory is malformed")
        path = _artifact_path(evidence, relative)
        if _sha256_bytes(path.read_bytes()) != sha256:
            raise WorkingBundleError(f"manifest artifact hash drift: {relative}")
        inventory_by_path[relative] = sha256
    contract_inventory = [
        item
        for item in inventory
        if item["path"].startswith("working_contracts/")
    ]
    if len(contract_inventory) != 60 or manifest.get(
        "working_contract_set_sha256"
    ) != _sha256_json(contract_inventory):
        raise WorkingBundleError("manifest does not bind exactly 60 working contracts")

    pairs_path = _safe_repo_path(repo, manifest["pairs_path"])
    if _sha256_bytes(pairs_path.read_bytes()) != manifest.get("pairs_sha256"):
        raise WorkingBundleError("manifest pair-pool hash drift")
    source_rows = _read_jsonl(pairs_path)
    source_case_ids = [str(row.get("pair_id", ""))[-4:] for row in source_rows]
    if source_case_ids != EXPECTED_CASE_IDS:
        raise WorkingBundleError("pair pool is not the ordered 0000..0059 batch")
    row_by_case = dict(zip(source_case_ids, source_rows))
    if case_id not in row_by_case:
        raise WorkingBundleError(f"case is not present in pair pool: {case_id}")
    source_row = row_by_case[case_id]
    pair_id = source_row["pair_id"]

    manual_review_by_case = _validate_publication_seal(
        repo=repo,
        evidence=evidence,
        manifest=manifest,
        source_case_ids=source_case_ids,
        source_rows=source_rows,
    )

    relative_paths = {
        "canonical": f"canonical/{pair_id}.json",
        "fcstm": f"fcstm/{pair_id}.fcstm",
        "inspect": f"parse_inspect/{pair_id}.json",
        "contract": f"working_contracts/{pair_id}.json",
        "trace": f"source_traces/{pair_id}.json",
        "case_report": f"case_reports/{pair_id}.json",
    }
    for relative in relative_paths.values():
        if relative not in inventory_by_path:
            raise WorkingBundleError(
                f"required artifact is absent from manifest: {relative}"
            )
    if "comparison.jsonl" not in inventory_by_path:
        raise WorkingBundleError("comparison ledger is absent from manifest")
    canonical = _read_json(evidence / relative_paths["canonical"])
    fcstm_path = evidence / relative_paths["fcstm"]
    if fcstm_path.is_symlink() or not fcstm_path.is_file():
        raise WorkingBundleError("FCSTM artifact is not a regular file")
    fcstm = fcstm_path.read_text(encoding="utf-8")
    inspect_report = _read_json(evidence / relative_paths["inspect"])
    contract = _read_json(evidence / relative_paths["contract"])
    source_trace = _read_json(evidence / relative_paths["trace"])
    case_report = _read_json(evidence / relative_paths["case_report"])
    comparison_rows = _read_jsonl(evidence / "comparison.jsonl")
    comparison_row = next(
        (item for item in comparison_rows if item.get("case_id") == case_id), None
    )
    if comparison_row is None:
        raise WorkingBundleError("comparison ledger does not contain selected case")
    if comparison_row.get("pair_id") != pair_id:
        raise WorkingBundleError("comparison ledger pair identity drift")
    comparison = case_report.get("comparison")
    if not isinstance(comparison, dict):
        raise WorkingBundleError("case report lacks the lowering comparison")

    if _sha256_text(source_row["nl_text"]) != source_row["nl_sha256"]:
        raise WorkingBundleError("NL pair hash drift")
    if _sha256_text(source_row["stm0_text"]) != source_row["stm0_sha256"]:
        raise WorkingBundleError("PlantUML pair hash drift")
    if canonical.get("metadata", {}).get("source_sha256") != source_row["stm0_sha256"]:
        raise WorkingBundleError("canonical source hash does not match PlantUML pair")
    if case_report.get("schema_version") != "r4_5.llms_emp_java_case_report.v5":
        raise WorkingBundleError("working bundle requires the v5 case report")
    if case_report.get("pair_id") != pair_id or case_report.get("case_id") != case_id:
        raise WorkingBundleError("case-report identity drift")
    artifact_hashes = {
        "canonical_file_sha256": _sha256_bytes(
            (evidence / relative_paths["canonical"]).read_bytes()
        ),
        "fcstm_file_sha256": _sha256_bytes(fcstm_path.read_bytes()),
        "parse_inspect_file_sha256": _sha256_bytes(
            (evidence / relative_paths["inspect"]).read_bytes()
        ),
        "source_trace_file_sha256": _sha256_bytes(
            (evidence / relative_paths["trace"]).read_bytes()
        ),
        "comparison_sha256": _sha256_json(comparison),
        "ast_audit_sha256": _sha256_json(case_report["ast_audit"]),
    }
    review_subject_sha256 = _sha256_json(
        {
            "nl_sha256": source_row["nl_sha256"],
            "source_sha256": source_row["stm0_sha256"],
            **artifact_hashes,
            "element_set_sha256": contract["inventory_digests"]["element_set_sha256"],
            "macro_set_sha256": contract["inventory_digests"]["macro_set_sha256"],
        }
    )
    expected_binding_paths = {
        "canonical_path": _repo_relative(repo, evidence / relative_paths["canonical"]),
        "fcstm_path": _repo_relative(repo, fcstm_path),
        "parse_inspect_path": _repo_relative(
            repo, evidence / relative_paths["inspect"]
        ),
        "source_trace_path": _repo_relative(repo, evidence / relative_paths["trace"]),
    }
    bindings = contract.get("artifact_bindings", {})
    if any(bindings.get(key) != value for key, value in expected_binding_paths.items()):
        raise WorkingBundleError("working-contract artifact path binding drift")
    if any(bindings.get(key) != value for key, value in artifact_hashes.items()):
        raise WorkingBundleError("working-contract artifact hash binding drift")
    if contract.get("source_trace_base") != source_trace:
        raise WorkingBundleError("working-contract/source-trace content drift")
    if comparison_row.get("case_report_sha256") != _sha256_bytes(
        (evidence / relative_paths["case_report"]).read_bytes()
    ):
        raise WorkingBundleError("comparison/case-report hash drift")
    if comparison_row.get("working_contract_sha256") != _sha256_bytes(
        (evidence / relative_paths["contract"]).read_bytes()
    ):
        raise WorkingBundleError("comparison/working-contract hash drift")
    expected_case_report_hashes = {
        "source_sha256": source_row["stm0_sha256"],
        "canonical_sha256": artifact_hashes["canonical_file_sha256"],
        "fcstm_sha256": artifact_hashes["fcstm_file_sha256"],
        "parse_inspect_sha256": artifact_hashes["parse_inspect_file_sha256"],
        "source_trace_sha256": artifact_hashes["source_trace_file_sha256"],
        "working_contract_sha256": comparison_row["working_contract_sha256"],
        "review_subject_sha256": review_subject_sha256,
    }
    if any(
        case_report.get(key) != value
        for key, value in expected_case_report_hashes.items()
    ):
        raise WorkingBundleError("case-report artifact identity drift")
    if (
        comparison_row.get("review_subject_sha256") != review_subject_sha256
        or contract.get("review_subject", {}).get("review_subject_sha256")
        != review_subject_sha256
    ):
        raise WorkingBundleError("review-subject identity drift")
    if case_id not in manual_review_by_case:
        raise WorkingBundleError("publication review is missing for selected case")

    schema_path = (
        repo
        / "project_1_llm_state_machine_modeling/paper_stm_repair"
        / "pipeline/representation/schemas/working_fcstm_contract.schema.json"
    )
    try:
        Draft202012Validator(_read_json(schema_path)).validate(contract)
    except ValidationError as exc:
        raise WorkingBundleError(
            f"working contract schema validation failed: {exc.message}"
        ) from exc
    validate_working_contract(
        canonical=canonical,
        fcstm=fcstm,
        comparison=comparison,
        contract=contract,
        inspect_report=inspect_report,
    )
    if contract.get("usage_gate") != "discover_input_with_capability_mask":
        raise WorkingBundleError("working contract is not an attributed Discover input")
    for capability in ("repair", "confirm", "final_export", "main_result"):
        if contract["capability_eligibility"][capability]["status"] != "not_run":
            raise WorkingBundleError(
                f"baseline bundle prematurely authorizes {capability}"
            )
    return AttributionSafeWorkingBundle(
        repo_root=repo,
        evidence_dir=evidence,
        case_id=case_id,
        pair_id=pair_id,
        nl_text=source_row["nl_text"],
        source_text=source_row["stm0_text"],
        fcstm_text=fcstm,
        _canonical=copy.deepcopy(canonical),
        _inspect_report=copy.deepcopy(inspect_report),
        _working_contract=copy.deepcopy(contract),
        _source_trace=copy.deepcopy(source_trace),
        _case_report=copy.deepcopy(case_report),
        _comparison=copy.deepcopy(comparison_row),
    )


def _validate_publication_seal(
    *,
    repo: Path,
    evidence: Path,
    manifest: dict[str, Any],
    source_case_ids: list[str],
    source_rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    if source_case_ids != EXPECTED_CASE_IDS or len(source_rows) != 60:
        raise WorkingBundleError("publication requires the ordered 0000..0059 source batch")
    seal_path = evidence / "PUBLICATION_SEAL.json"
    if seal_path.is_symlink() or not seal_path.is_file():
        raise WorkingBundleError("working bundle lacks a completed publication seal")
    seal = _read_json(seal_path)
    if (
        seal.get("schema_version") != PUBLICATION_SCHEMA_VERSION
        or seal.get("status") != PUBLICATION_READY_STATUS
        or seal.get("evidence_eligible") is not True
        or seal.get("case_count") != 60
    ):
        raise WorkingBundleError("working bundle lacks a completed publication seal")
    if seal.get("manifest_sha256") != _sha256_bytes(
        (evidence / "manifest.json").read_bytes()
    ):
        raise WorkingBundleError("publication seal manifest binding drift")
    if (
        seal.get("artifact_set_sha256") != manifest.get("artifact_set_sha256")
        or seal.get("working_contract_set_sha256")
        != manifest.get("working_contract_set_sha256")
    ):
        raise WorkingBundleError("publication seal machine-artifact binding drift")

    review_path = _artifact_path(evidence, "MANUAL_REVIEW.jsonl")
    reviews = _read_jsonl(review_path)
    if seal.get("manual_review_file_sha256") != _sha256_bytes(review_path.read_bytes()):
        raise WorkingBundleError("publication seal manual-review file binding drift")
    if seal.get("manual_review_set_sha256") != _sha256_json(reviews):
        raise WorkingBundleError("publication seal manual-review set binding drift")
    review_case_ids = [str(item.get("case_id", "")) for item in reviews]
    review_pair_ids = [str(item.get("pair_id", "")) for item in reviews]
    expected_pair_ids = [str(item["pair_id"]) for item in source_rows]
    if (
        review_case_ids != EXPECTED_CASE_IDS
        or review_pair_ids != expected_pair_ids
        or len(reviews) != 60
    ):
        raise WorkingBundleError("publication seal review identities drift")

    derived_inventory = _derived_publication_inventory(evidence)
    if seal.get("derived_artifact_inventory") != derived_inventory or seal.get(
        "derived_artifact_set_sha256"
    ) != _sha256_json(derived_inventory):
        raise WorkingBundleError("publication seal derived-artifact binding drift")
    required_paths = {"MANUAL_REVIEW.jsonl", "MANUAL_REVIEW.md", "PAIR_INDEX.md"}
    for case_id in EXPECTED_CASE_IDS:
        required_paths.update(
            {
                f"pairs/{case_id}/README.md",
                f"pairs/{case_id}/nl.txt",
                f"pairs/{case_id}/plantuml.puml",
                f"pairs/{case_id}/fcstm.fcstm",
            }
        )
    if {item["path"] for item in derived_inventory} != required_paths:
        raise WorkingBundleError("publication does not contain exactly 60 complete pair pages")
    pair_index = _artifact_path(evidence, "PAIR_INDEX.md")
    if seal.get("pair_index_sha256") != _sha256_bytes(pair_index.read_bytes()):
        raise WorkingBundleError("publication seal pair-index binding drift")

    schema_path = (
        repo
        / "project_1_llm_state_machine_modeling/paper_stm_repair"
        / "pipeline/representation/schemas/manual_pair_review.schema.json"
    )
    validator = Draft202012Validator(_read_json(schema_path))
    review_by_case: dict[str, dict[str, Any]] = {}
    observation_digests: set[str] = set()
    review_contexts: set[tuple[str, str]] = set()
    for case_id, pair_id, source_row, review in zip(
        EXPECTED_CASE_IDS,
        expected_pair_ids,
        source_rows,
        reviews,
    ):
        contract_path = _artifact_path(
            evidence, f"working_contracts/{pair_id}.json"
        )
        fcstm_path = _artifact_path(evidence, f"fcstm/{pair_id}.fcstm")
        contract = _read_json(contract_path)
        fcstm = fcstm_path.read_text(encoding="utf-8")
        try:
            validate_manual_pair_review(
                review=review,
                case_id=case_id,
                pair_id=pair_id,
                review_subject_sha256=contract["review_subject"][
                    "review_subject_sha256"
                ],
                contract=contract,
                contract_sha256=_sha256_bytes(contract_path.read_bytes()),
                nl_text=source_row["nl_text"],
                source_text=source_row["stm0_text"],
                fcstm_text=fcstm,
                validator=validator,
            )
        except (ValidationError, ValueError, KeyError) as exc:
            raise WorkingBundleError(
                f"manual review validation failed for {case_id}: {exc}"
            ) from exc
        digest = manual_review_observation_digest(review)
        if digest in observation_digests:
            raise WorkingBundleError(
                f"manual review reused generic observations for {case_id}"
            )
        observation_digests.add(digest)
        context = review["review_context"]
        review_contexts.add((context["session_id"], context["model_id"]))

        pair_dir = evidence / "pairs" / case_id
        if (
            (pair_dir / "nl.txt").read_text(encoding="utf-8")
            != source_row["nl_text"]
            or (pair_dir / "plantuml.puml").read_text(encoding="utf-8")
            != source_row["stm0_text"]
            or (pair_dir / "fcstm.fcstm").read_text(encoding="utf-8") != fcstm
        ):
            raise WorkingBundleError(f"published pair bytes drift for {case_id}")
        review_by_case[case_id] = review
    if len(review_contexts) != 1:
        raise WorkingBundleError("publication reviews do not share one session/model identity")
    return review_by_case






def _find_repo_root(path: Path) -> Path:
    for parent in (path.resolve(), *path.resolve().parents):
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise WorkingBundleError("repository root not found for working bundle")
