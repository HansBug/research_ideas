from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

from .plantuml_working_contract import validate_working_contract


MANIFEST_SCHEMA_VERSION = "r4_5.llms_emp_java_batch.v5"


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
            "attribution_rules": {
                "compiler_only_diagnostic": "rejected_conversion_artifact",
                "macro_member_diagnostic": "candidate_only_until_source_evidence",
                "confirmed_conversion_artifact_limit": 0,
                "repair_conversion_artifact_limit": 0,
                "confirm_conversion_artifact_limit": 0,
                "main_result_conversion_artifact_limit": 0,
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
            evidence_refs = tuple(
                item["reference"] for item in issue["behavior_evidence"]
            )
            if not self._has_eligible_typed_evidence(issue):
                raise WorkingBundleError(
                    f"confirmed issue lacks capability-eligible typed evidence: {issue['issue_id']}"
                )
            field_refs = tuple(
                sorted(
                    field_ref
                    for field_ref in eligible_fields
                    if field_ref.split("#field:", 1)[0] in source_ids
                )
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
                    behavior_evidence_refs=evidence_refs,
                )
            )
        return tuple(bindings)

    def _has_eligible_typed_evidence(self, issue: dict[str, Any]) -> bool:
        capabilities = self._working_contract["capability_eligibility"]
        status_by_evidence = {
            "source_internal_consistency_check": capabilities[
                "source_static_discovery"
            ]["status"],
            "inspect_diagnostic": capabilities["inspect_diagnostics"]["status"],
            "simulation_trace": capabilities["simulation"]["status"],
            "probe_result": capabilities["simulation"]["status"],
            "verification_counterexample": "not_run",
        }
        return any(
            status_by_evidence.get(item["evidence_type"])
            in {"eligible", "eligible_with_exclusions"}
            for item in issue["behavior_evidence"]
        )

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

    pairs_path = _safe_repo_path(repo, manifest["pairs_path"])
    if _sha256_bytes(pairs_path.read_bytes()) != manifest.get("pairs_sha256"):
        raise WorkingBundleError("manifest pair-pool hash drift")
    source_rows = _read_jsonl(pairs_path)
    source_case_ids = [str(row.get("pair_id", ""))[-4:] for row in source_rows]
    if len(source_case_ids) != len(set(source_case_ids)):
        raise WorkingBundleError("pair pool contains duplicate case identities")
    row_by_case = dict(zip(source_case_ids, source_rows))
    if case_id not in row_by_case:
        raise WorkingBundleError(f"case is not present in pair pool: {case_id}")
    source_row = row_by_case[case_id]
    pair_id = source_row["pair_id"]

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


def _find_repo_root(path: Path) -> Path:
    for parent in (path.resolve(), *path.resolve().parents):
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise WorkingBundleError("repository root not found for working bundle")
