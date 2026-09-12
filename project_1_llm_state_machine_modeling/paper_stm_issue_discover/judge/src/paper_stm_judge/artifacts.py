"""Arm-neutral report adapters and common artifact-closure construction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from utils.stm_artifacts import load_pair
from utils.stm_artifacts.context import (
    hierarchical_reachable_state_refs,
)

from .models import (
    AdapterAudit,
    AdapterIdMap,
    ArtifactAuthority,
    ArtifactConsistencyFinding,
    ArtifactConsistencyPreflight,
    ArtifactConsistencyStatus,
    ArtifactDocument,
    ArtifactRole,
    CandidateEvidence,
    CandidateReport,
    ExpectedAxisHints,
    ExpectedIssue,
    JudgeArtifactClosure,
    UnifiedJudgeInput,
)
from .protocol import (
    ADAPTER_VERSION,
    ARTIFACT_BUILDER_VERSION,
    PROTOCOL_VERSION,
)


def _sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _model_json(value: Any) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return _stable_json(value)


def _inspection_authority_projection(pair: Any) -> str:
    """Add typed carrier and scoped-entry facts without changing source artifacts."""

    inspection = pair.inspection_facts.model_dump(mode="json")
    canonical = pair.canonical_source_ir.model_dump(mode="json")
    canonical_states = canonical.get("model", {}).get("states", ())
    state_carriers = []
    for state in canonical_states:
        attributes = state.get("attributes") or {}
        state_carriers.append(
            {
                "state_id": state.get("id"),
                "body_lines": attributes.get("body_lines") or [],
                "lifecycle_actions": attributes.get("lifecycle_actions") or [],
                "body_lines_are_executable": False,
                "executable_lifecycle_carrier": "attributes.lifecycle_actions",
            }
        )
    transitions = inspection.get("transitions") or []
    initial_entries = [
        {
            "transition_ref": item.get("transition_ref"),
            "owner_scope": item.get("scope"),
            "resolved_target_ref": item.get("resolved_target_ref"),
            "runtime_continuation": False,
            "requires_owner_active": True,
        }
        for item in transitions
        if str(item.get("source") or "").strip() == "[*]"
    ]
    runtime_transitions = [
        {
            "transition_ref": item.get("transition_ref"),
            "resolved_source_ref": item.get("resolved_source_ref"),
            "resolved_target_ref": item.get("resolved_target_ref"),
        }
        for item in transitions
        if str(item.get("source") or "").strip() != "[*]"
    ]
    inspection["judge_typed_semantics"] = {
        "schema_version": "paper1.semantic-judge.typed-artifact-semantics.v1",
        "state_carriers": state_carriers,
        "initial_entries": initial_entries,
        "runtime_transitions": runtime_transitions,
        "containment_implies_runtime_reachability": False,
        "child_initial_requires_owner_entry": True,
        "reason": "Presentation text and owner-scoped entry are separated from executable lifecycle behavior and runtime continuation.",
        "basis": "canonical source IR typed attributes plus inspection-equivalent scoped transition resolution",
    }
    return _stable_json(inspection)


def _stage_projection(
    payload: dict[str, Any],
    *,
    included_fields: tuple[str, ...],
    source_hash: str,
    purpose: str,
) -> str:
    """Project complete Judge-relevant fields with explicit non-truncation provenance."""

    data = {key: payload[key] for key in included_fields if key in payload}
    omitted = tuple(sorted(set(payload) - set(data)))
    return _stable_json(
        {
            "projection": {
                "version": ARTIFACT_BUILDER_VERSION,
                "source_sha256": source_hash,
                "included_fields": included_fields,
                "omitted_fields": omitted,
                "truncation_applied": False,
                "purpose": purpose,
            },
            "data": data,
        }
    )


def _document(
    *,
    role: ArtifactRole,
    authority: ArtifactAuthority,
    content: str,
    schema_version: str,
    reason: str,
    basis: str,
) -> ArtifactDocument:
    artifact_id = f"artifact:{role.value}"
    return ArtifactDocument(
        artifact_id=artifact_id,
        role=role,
        authority=authority,
        sha256=_sha256_bytes(content.encode("utf-8")),
        schema_version=schema_version,
        content=content,
        reason=reason,
        basis=basis,
    )


class ArtifactConsistencyError(RuntimeError):
    """Raised before provider use when deterministic closure facts contradict."""

    def __init__(self, preflight: ArtifactConsistencyPreflight) -> None:
        self.preflight = preflight
        super().__init__(preflight.reason)


def _owned_state_paths(model: Any) -> dict[str, str]:
    """Resolve stable dotted paths from the owned parser's scoped state rows."""

    states = tuple(model.states)
    by_name: dict[str, list[Any]] = {}
    for state in states:
        by_name.setdefault(state.name, []).append(state)
    cache: dict[str, str] = {}

    def path_for(state: Any, visiting: frozenset[str] = frozenset()) -> str:
        if state.ref in cache:
            return cache[state.ref]
        if state.ref in visiting or state.parent is None:
            result = state.name
        else:
            candidates = [
                item
                for item in by_name.get(state.parent, ())
                if item.ref != state.ref and item.line < state.line
            ]
            parent = max(candidates, key=lambda item: item.line) if candidates else None
            result = (
                f"{path_for(parent, visiting | {state.ref})}.{state.name}"
                if parent is not None
                else state.name
            )
        cache[state.ref] = result
        return result

    return {state.ref: path_for(state) for state in states}


def build_pair_artifact_consistency_preflight(
    pair: Any,
) -> ArtifactConsistencyPreflight:
    """Cross-check reachability across graph, owned, verify, and reference facts."""

    findings: list[ArtifactConsistencyFinding] = []
    owned = pair.inspection_facts
    verify = pair.verify_facts
    graph_reachable = hierarchical_reachable_state_refs(pair.model)
    owned_reachable = frozenset(owned.reachable_state_refs)
    finding_no = 0

    def add_finding(
        *,
        fact_kind: str,
        subject_refs: tuple[str, ...],
        values: tuple[str, ...],
        reason: str,
        basis: str,
    ) -> None:
        nonlocal finding_no
        finding_no += 1
        findings.append(
            ArtifactConsistencyFinding(
                finding_id=f"PRE-{finding_no}",
                fact_kind=fact_kind,
                subject_refs=subject_refs,
                values=values,
                reason=reason,
                basis=basis,
            )
        )

    if graph_reachable != owned_reachable:
        add_finding(
            fact_kind="closed_model_reachability_closure",
            subject_refs=tuple(sorted(graph_reachable | owned_reachable))
            or ("closed-model",),
            values=(
                "fcstm_graph=" + ",".join(sorted(graph_reachable)),
                "owned_inspection=" + ",".join(sorted(owned_reachable)),
            ),
            reason="The recomputed scoped FCSTM graph and owned inspection artifact disagree on the complete reachable-state closure.",
            basis="entry-transition-only hierarchical graph v3 versus InspectionEquivalentFacts.reachable_state_refs",
        )

    for state in owned.states:
        expected = state.state_ref in owned_reachable
        if state.reachable_from_initial != expected:
            add_finding(
                fact_kind="owned_state_reachability_flag",
                subject_refs=(state.state_ref,),
                values=(
                    f"state_row={state.reachable_from_initial}",
                    f"owned_closure={expected}",
                ),
                reason="The owned state row contradicts its own complete reachable-state closure.",
                basis="InspectionStateFact.reachable_from_initial versus InspectionEquivalentFacts.reachable_state_refs",
            )

    verify_by_ref = {
        check.subject_refs[0]: check
        for check in verify.checks
        if check.kind == "reachability" and len(check.subject_refs) == 1
    }
    for state in owned.states:
        if state.state_ref == owned.machine_root_ref:
            continue
        check = verify_by_ref.get(state.state_ref)
        expected_status = "proved" if state.state_ref in owned_reachable else "refuted"
        if check is None or check.status != expected_status:
            add_finding(
                fact_kind="verify_reachability",
                subject_refs=(state.state_ref,),
                values=(
                    f"owned={expected_status}",
                    f"verify={check.status if check is not None else 'missing'}",
                ),
                reason="The finite verification summary does not agree with the owned reachability closure.",
                basis="VerificationFacts reachability checks versus InspectionEquivalentFacts.reachable_state_refs",
            )

    paths_by_ref = _owned_state_paths(pair.model)
    refs_by_path: dict[str, list[str]] = {}
    for state_ref, state_path in paths_by_ref.items():
        refs_by_path.setdefault(state_path, []).append(state_ref)
    reference_diagnostics = pair.reference_inspection.payload.get("diagnostics", ())
    for diagnostic in reference_diagnostics:
        if (
            not isinstance(diagnostic, dict)
            or diagnostic.get("code") != "W_UNREACHABLE_STATE"
        ):
            continue
        refs = diagnostic.get("refs")
        reference_path = refs.get("state_path") if isinstance(refs, dict) else None
        if not isinstance(reference_path, str):
            continue
        candidates = refs_by_path.get(reference_path, ())
        if not candidates:
            terminal = reference_path.rsplit(".", 1)[-1]
            terminal_candidates = [
                state.ref for state in pair.model.states if state.name == terminal
            ]
            candidates = terminal_candidates if len(terminal_candidates) == 1 else ()
        contradicting = tuple(
            state_ref for state_ref in candidates if state_ref in owned_reachable
        )
        if contradicting:
            add_finding(
                fact_kind="reference_unreachable_state",
                subject_refs=(reference_path, *contradicting),
                values=("reference=unreachable", "owned_and_fcstm_graph=reachable"),
                reason="The published reference diagnostic marks the state unreachable while the owned closure marks the same state reachable.",
                basis="reference W_UNREACHABLE_STATE versus owned path mapping and entry-transition-only FCSTM graph v3",
            )

    status = (
        ArtifactConsistencyStatus.FAIL if findings else ArtifactConsistencyStatus.PASS
    )
    return ArtifactConsistencyPreflight(
        algorithm_version="paper1.semantic-judge.artifact-preflight.v1",
        pair_id=pair.pair_id,
        status=status,
        checked_fact_families=(
            "fcstm_graph_reachability",
            "owned_inspection_reachability",
            "verify_reachability",
            "reference_unreachable_diagnostics",
        ),
        findings=tuple(findings),
        reason=(
            "The common deterministic artifacts agree on every compared reachability fact."
            if not findings
            else f"The common deterministic artifacts contain {len(findings)} reachability contradiction(s); provider judging is blocked."
        ),
        basis="Exact FCSTM model, entry-transition-only graph v3, owned InspectionEquivalentFacts, VerificationFacts, and published structured reference diagnostics.",
    )


def build_artifact_consistency_preflight(
    report_root: str | Path, pair_id: str
) -> ArtifactConsistencyPreflight:
    """Build a typed consistency receipt without invoking a provider."""

    root = Path(report_root).expanduser().resolve()
    return build_pair_artifact_consistency_preflight(
        load_pair(root / "pairs" / pair_id)
    )


def build_artifact_closure(
    report_root: str | Path,
    pair_id: str,
    *,
    preflight: ArtifactConsistencyPreflight | None = None,
) -> JudgeArtifactClosure:
    """Build the exact same complete pair evidence closure for every source adapter."""

    root = Path(report_root).expanduser().resolve()
    pair = load_pair(root / "pairs" / pair_id)
    preflight = preflight or build_pair_artifact_consistency_preflight(pair)
    if preflight.pair_id != pair_id:
        raise ValueError("artifact preflight identifies a different pair")
    if preflight.status != ArtifactConsistencyStatus.PASS:
        raise ArtifactConsistencyError(preflight)
    assert pair.context_manifest is not None
    assert pair.canonical_source_ir is not None
    assert pair.exact_source_inventory is not None
    assert pair.reference_inspection is not None
    assert pair.inspection_facts is not None
    assert pair.verify_facts is not None
    assert pair.smt_facts is not None
    assert pair.working_contract is not None
    assert pair.source_trace is not None
    assert pair.case_report is not None
    canonical_payload = pair.canonical_source_ir.model_dump(mode="json")
    reference_payload = pair.reference_inspection.payload
    working_payload = pair.working_contract.payload
    case_payload = pair.case_report.payload

    artifacts = (
        _document(
            role=ArtifactRole.NATURAL_LANGUAGE,
            authority=ArtifactAuthority.NORMATIVE_SOURCE,
            content=pair.nl_text,
            schema_version="text/plain.numbered-nl.v1",
            reason="Natural language establishes explicit requirements and compatibility boundaries; artifact-supported implicit testing or domain-essential obligations need not be stated verbatim.",
            basis="published pair nl.txt; exact bytes supplied without truncation",
        ),
        _document(
            role=ArtifactRole.PLANTUML_SOURCE,
            authority=ArtifactAuthority.AUTHOR_SOURCE,
            content=pair.plantuml_text,
            schema_version="text/plantuml.v1",
            reason="Author PlantUML establishes authored carriers, hierarchy, labels, effects, and region separators.",
            basis="published pair plantuml.puml; exact bytes supplied without truncation",
        ),
        _document(
            role=ArtifactRole.FCSTM_MODEL,
            authority=ArtifactAuthority.CLOSED_MODEL,
            content=pair.fcstm_text,
            schema_version="text/fcstm.v1",
            reason="The closed FCSTM establishes lowered model members while remaining distinct from author source.",
            basis=f"published pair fcstm.fcstm; parser={pair.model.algorithm_version}",
        ),
        _document(
            role=ArtifactRole.CANONICAL_SOURCE_IR,
            authority=ArtifactAuthority.AUTHOR_SOURCE,
            content=_stage_projection(
                canonical_payload,
                included_fields=(
                    "schema_version",
                    "adapter",
                    "source_format",
                    "status",
                    "status_reason_code",
                    "diagnostics",
                    "model",
                ),
                source_hash=pair.hashes["canonical"],
                purpose="Retain complete author-source model identities and semantics while excluding duplicated generation metadata.",
            ),
            schema_version=f"{pair.canonical_source_ir.schema_version}.judge-projection.v2",
            reason="Canonical source IR supplies exact author-source identities without promoting lowering members to authored defects.",
            basis=f"published canonical artifact; adapter={pair.canonical_source_ir.adapter}",
        ),
        _document(
            role=ArtifactRole.EXACT_SOURCE_INVENTORY,
            authority=ArtifactAuthority.AUTHOR_SOURCE,
            content=_model_json(pair.exact_source_inventory),
            schema_version=pair.exact_source_inventory.schema_version,
            reason="Exact source inventory exposes positive and negative carrier closure for source attribution.",
            basis=pair.exact_source_inventory.basis,
        ),
        _document(
            role=ArtifactRole.REFERENCE_INSPECTION,
            authority=ArtifactAuthority.DETERMINISTIC_FACT,
            content=_stage_projection(
                reference_payload,
                included_fields=("root_state_path", "metrics", "diagnostics"),
                source_hash=pair.hashes["parse_inspect"],
                purpose="Retain published diagnostic summary; full state/transition facts are supplied once by inspection_equivalent_facts.",
            ),
            schema_version=f"{pair.reference_inspection.ref.schema_version}.judge-projection.v2",
            reason="Published reference inspection provides structured diagnostics and inventory facts, not normative truth.",
            basis=pair.reference_inspection.ref.basis,
        ),
        _document(
            role=ArtifactRole.INSPECTION_EQUIVALENT_FACTS,
            authority=ArtifactAuthority.DETERMINISTIC_FACT,
            content=_inspection_authority_projection(pair),
            schema_version=f"{pair.inspection_facts.schema_version}.judge-typed-authority.v1",
            reason="Owned inspection-equivalent facts expose hierarchy, scoped entry, runtime transition, typed carrier, reachability, and diagnostic closure.",
            basis=f"{pair.inspection_facts.basis}; paper1.semantic-judge.typed-artifact-semantics.v1",
        ),
        _document(
            role=ArtifactRole.VERIFY_FACTS,
            authority=ArtifactAuthority.DETERMINISTIC_FACT,
            content=_model_json(pair.verify_facts),
            schema_version=pair.verify_facts.schema_version,
            reason="Finite verification facts support reachability, dead-end, entry, and consumer truth checks.",
            basis=pair.verify_facts.basis,
        ),
        _document(
            role=ArtifactRole.SMT_FACTS,
            authority=ArtifactAuthority.DETERMINISTIC_FACT,
            content=_model_json(pair.smt_facts),
            schema_version=pair.smt_facts.schema_version,
            reason="Normalized bounded-formula facts expose formal inputs and explicit no-solver boundaries.",
            basis=pair.smt_facts.basis,
        ),
        _document(
            role=ArtifactRole.WORKING_CONTRACT,
            authority=ArtifactAuthority.MAPPING,
            content=_stage_projection(
                working_payload,
                included_fields=(
                    "schema_version",
                    "artifact_role",
                    "artifact_bindings",
                    "attribution_policy",
                    "diagnostic_attribution",
                    "ownership_policy",
                    "inventory_digests",
                    "summary",
                ),
                source_hash=pair.hashes["working_contract"],
                purpose="Retain role, attribution, ownership, and identity policy; method capability prompts and duplicated element inventories are not Judge inputs.",
            ),
            schema_version=f"{pair.working_contract.ref.schema_version}.judge-projection.v2",
            reason="Working mapping contract supplies representation ownership and eligibility boundaries without Judge answers.",
            basis=pair.working_contract.ref.basis,
        ),
        _document(
            role=ArtifactRole.SOURCE_TRACE,
            authority=ArtifactAuthority.PROVENANCE,
            content=_model_json(pair.source_trace.payload),
            schema_version=pair.source_trace.ref.schema_version,
            reason="Source trace distinguishes authored elements, generated members, and lowering provenance.",
            basis=pair.source_trace.ref.basis,
        ),
        _document(
            role=ArtifactRole.CASE_REPORT,
            authority=ArtifactAuthority.PROVENANCE,
            content=_stage_projection(
                case_payload,
                included_fields=(
                    "schema_version",
                    "case_id",
                    "pair_id",
                    "model_name",
                    "selected_stage",
                    "official_raw_status",
                    "official_validation_status",
                    "is_phase_i_fallback",
                    "phase_i_changed",
                    "canonical_sha256",
                    "fcstm_sha256",
                    "parse_inspect_sha256",
                    "source_trace_sha256",
                    "working_contract_sha256",
                    "inspect_metrics",
                    "inspect_diagnostic_severities",
                    "official_identity_reconciliation",
                    "name_mapping",
                    "stage_lineage",
                ),
                source_hash=pair.hashes["case_report"],
                purpose="Retain identity, validation status, name mapping, and stage provenance while excluding duplicated full model comparison payloads.",
            ),
            schema_version=f"{pair.case_report.ref.schema_version}.judge-projection.v2",
            reason="Case report closes artifact identity and representation status without supplying expected answers.",
            basis=pair.case_report.ref.basis,
        ),
        _document(
            role=ArtifactRole.ARTIFACT_CONSISTENCY_PREFLIGHT,
            authority=ArtifactAuthority.DETERMINISTIC_FACT,
            content=_model_json(preflight),
            schema_version=preflight.schema_version,
            reason="The provider receives only a passing typed receipt proving that compared deterministic facts do not contradict.",
            basis=preflight.basis,
        ),
    )
    unhashed = {
        "schema_version": "paper1.semantic-judge.artifact-closure.v4",
        "pair_id": pair_id,
        "artifacts": [item.model_dump(mode="json") for item in artifacts],
        "reason": "Every report source is judged against one identical stage-scoped public pair closure without runtime truncation.",
        "basis": (
            f"{ARTIFACT_BUILDER_VERSION}; PairInput manifest "
            f"{pair.context_manifest.manifest_hash}"
        ),
    }
    return JudgeArtifactClosure(
        **unhashed,
        closure_hash=_sha256_bytes(_stable_json(unhashed).encode("utf-8")),
    )


def load_expected_issues(
    ledger_path: str | Path,
    pair_id: str,
) -> tuple[tuple[ExpectedIssue, ...], tuple[AdapterIdMap, ...]]:
    """Project the frozen D2+D1 denominator while physically removing D and L."""

    path = Path(ledger_path).expanduser().resolve()
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw.get("items")
    if not isinstance(items, dict):
        raise TypeError(f"ledger.items must be an object: {path}")
    selected = sorted(
        (
            item
            for item in items.values()
            if item.get("pair") == pair_id and item.get("D") in {"D1", "D2"}
        ),
        key=lambda item: str(item.get("id")),
    )
    expected: list[ExpectedIssue] = []
    mappings: list[AdapterIdMap] = []
    for index, item in enumerate(selected, start=1):
        anonymous_id = f"E{index:04d}"
        original_id = str(item["id"])
        axes = item.get("axes") or {}
        pair_context = item.get("pair_context") or {}
        nl_id = str(pair_context.get("nl_id") or f"pair:{pair_id}")
        source_text = item.get("_source_text") or {}
        expected.append(
            ExpectedIssue(
                expected_id=anonymous_id,
                summary=str(item.get("summary") or original_id),
                detail=str(item.get("detail") or item.get("summary") or original_id),
                source_statement=(
                    str(source_text["statement"])
                    if source_text.get("statement")
                    else None
                ),
                axes=ExpectedAxisHints(
                    defect_locus=axes.get("defect_locus"),
                    defect_element=axes.get("defect_element"),
                    defect_qualifier=axes.get("defect_qualifier"),
                    defect_logic_kind=axes.get("defect_logic_kind"),
                    defect_reference=axes.get("defect_reference"),
                ),
                source_refs=(
                    f"expected:{anonymous_id}",
                    "artifact:natural_language",
                    nl_id,
                ),
            )
        )
        mappings.append(
            AdapterIdMap(anonymous_id=anonymous_id, original_id=original_id)
        )
    return tuple(expected), tuple(mappings)


def _candidate_field_names() -> tuple[str, ...]:
    return tuple(CandidateReport.model_fields)


EXCLUDED_PROVIDER_FIELDS = (
    "arm",
    "arm_label",
    "baseline_or_method",
    "d_level",
    "witness_level",
    "L",
    "predicate_id",
    "predicate_family",
    "predicate_inputs",
    "compiled_code",
    "execution_receipt",
    "semantic_adjudication",
    "historical_hit",
    "historical_false_positive",
)


def adapt_x1v2_record(
    record_path: str | Path,
    expected_id_map: tuple[AdapterIdMap, ...],
) -> tuple[tuple[CandidateReport, ...], AdapterAudit, int, str]:
    """Adapt existing X1v2 issues without inventing method-only evidence fields."""

    path = Path(record_path).expanduser().resolve()
    raw_bytes = path.read_bytes()
    record = json.loads(raw_bytes)
    if record.get("status") != "ok":
        raise ValueError(f"X1v2 record is not eligible status=ok: {path}")
    pair_value = str(record.get("pair_id") or "")
    pair_id = pair_value.rsplit("_", 1)[-1]
    round_no = int(record.get("round") or 1)
    parsed = record.get("parsed_output") or {}
    raw_issues = parsed.get("issues") or []
    reports: list[CandidateReport] = []
    mappings: list[AdapterIdMap] = []
    for index, issue in enumerate(raw_issues, start=1):
        report_id = f"R{index:04d}"
        original_id = f"{pair_id}:r{round_no}:baseline_issue_{index}"
        reports.append(
            CandidateReport(
                report_id=report_id,
                claim=str(issue.get("issue") or "").strip(),
                where=(str(issue["where"]).strip() if issue.get("where") else None),
                property=None,
                violated_obligation=None,
                expected=None,
                observed=None,
                reason=str(issue.get("reason") or "").strip(),
                basis=None,
                source_refs=(),
                evidence=(),
            )
        )
        mappings.append(AdapterIdMap(anonymous_id=report_id, original_id=original_id))
    audit = AdapterAudit(
        source_format="x1v2_record",
        source_path=str(path),
        source_hash=_sha256_bytes(raw_bytes),
        report_id_map=tuple(mappings),
        expected_id_map=expected_id_map,
        projected_field_names=_candidate_field_names(),
        excluded_field_names=EXCLUDED_PROVIDER_FIELDS,
        reason="X1v2 issue/where/reason were preserved; absent typed fields, basis, and refs remain explicitly null or empty.",
        basis=f"{ADAPTER_VERSION}; x1-baseline-arm/1 record parsed_output.issues",
    )
    return tuple(reports), audit, round_no, pair_id


def adapt_evidence_discovery_release(
    method_path: str | Path,
    expected_id_map: tuple[AdapterIdMap, ...],
) -> tuple[tuple[CandidateReport, ...], AdapterAudit, int, str]:
    """Adapt only final emitted report semantics, excluding method-only W/D/predicate data."""

    path = Path(method_path).expanduser().resolve()
    raw_bytes = path.read_bytes()
    record = json.loads(raw_bytes)
    if record.get("status") not in {"completed", "completed_with_diagnostics"} or not record.get("eligible"):
        raise ValueError(
            f"evidence-discovery method record is not eligible completed: {path}"
        )
    pair_id = str(record["pair_id"])
    round_no = int(record["round"])
    raw_releases = record.get("report_issue_clusters") or []
    reports: list[CandidateReport] = []
    mappings: list[AdapterIdMap] = []
    for index, issue in enumerate(raw_releases, start=1):
        report_id = f"R{index:04d}"
        original_id = str(issue["issue_id"])
        locus_names = tuple(str(value) for value in issue.get("locus_names") or ())
        locus_kind = str(issue.get("locus_kind") or "unspecified")
        where = (
            f"{locus_kind}: " + " -> ".join(locus_names) if locus_names else locus_kind
        )
        evidence: list[CandidateEvidence] = []
        if issue.get("requirement_quote"):
            evidence.append(
                CandidateEvidence(
                    evidence_ref=f"report:{report_id}:requirement_quote",
                    statement=str(issue["requirement_quote"]),
                )
            )
        source_refs = tuple(
            dict.fromkeys(
                str(value)
                for value in (
                    *issue.get("source_refs", ()),
                    *issue.get("element_refs", ()),
                )
                if value
            )
        )
        reports.append(
            CandidateReport(
                report_id=report_id,
                claim=str(
                    issue.get("title") or issue.get("candidate_reason") or original_id
                ),
                where=where,
                property=(str(issue["property"]) if issue.get("property") else None),
                violated_obligation=None,
                expected=(str(issue["expected"]) if issue.get("expected") else None),
                observed=(str(issue["observed"]) if issue.get("observed") else None),
                reason=str(
                    issue.get("candidate_reason")
                    or issue.get("reason")
                    or issue.get("title")
                    or original_id
                ),
                basis=(
                    str(issue["candidate_basis"])
                    if issue.get("candidate_basis")
                    else None
                ),
                source_refs=source_refs,
                evidence=tuple(evidence),
            )
        )
        mappings.append(AdapterIdMap(anonymous_id=report_id, original_id=original_id))
    audit = AdapterAudit(
        source_format="evidence_discovery_release",
        source_path=str(path),
        source_hash=_sha256_bytes(raw_bytes),
        report_id_map=tuple(mappings),
        expected_id_map=expected_id_map,
        projected_field_names=_candidate_field_names(),
        excluded_field_names=EXCLUDED_PROVIDER_FIELDS,
        reason="Only final emitted title/locus/property/expected/observed/reason/basis/refs were projected; W/D/predicate and hidden dossiers were removed.",
        basis=f"{ADAPTER_VERSION}; report_issue_clusters with issue_emitted=true",
    )
    return tuple(reports), audit, round_no, pair_id


def adapt_legacy_report_clusters(
    record_path: str | Path,
    expected_id_map: tuple[AdapterIdMap, ...],
) -> tuple[tuple[CandidateReport, ...], AdapterAudit, int, str]:
    """Adapt D1/D2 raw historical report clusters without method-only fields."""

    path = Path(record_path).expanduser().resolve()
    raw_bytes = path.read_bytes()
    record = json.loads(raw_bytes)
    raw_clusters = record.get("report_issue_clusters")
    if not isinstance(raw_clusters, list):
        raise TypeError(f"legacy record has no report_issue_clusters list: {path}")
    pair_id = str(record.get("pair_id") or path.parent.name[:4])
    round_no = record.get("round")
    if round_no is None:
        round_parent = next(
            (parent.name for parent in path.parents if parent.name.startswith("run")),
            "",
        )
        round_text = round_parent.removeprefix("run")
        if not round_text.isdigit():
            raise ValueError(f"cannot derive historical round from path: {path}")
        round_no = int(round_text)
    selected = [
        cluster
        for cluster in raw_clusters
        if isinstance(cluster, dict) and cluster.get("d_level") in {"D1", "D2"}
    ]
    reports: list[CandidateReport] = []
    mappings: list[AdapterIdMap] = []
    for index, cluster in enumerate(selected, start=1):
        report_id = f"R{index:04d}"
        original_id = str(
            cluster.get("report_issue_id")
            or cluster.get("representative_finding_key")
            or f"{pair_id}:r{round_no}:cluster:{index}"
        )
        claims = tuple(
            str(value).strip()
            for value in cluster.get("claims") or ()
            if str(value).strip()
        )
        obligations = tuple(
            str(value).strip()
            for value in cluster.get("obligations") or ()
            if str(value).strip()
        )
        locations = tuple(
            str(value).strip()
            for value in cluster.get("locations") or ()
            if str(value).strip()
        )
        claim = " ".join(claims).strip() or original_id
        obligation = " ".join(obligations).strip() or None
        reports.append(
            CandidateReport(
                report_id=report_id,
                claim=claim,
                where="; ".join(locations) or None,
                property=None,
                violated_obligation=obligation,
                expected=None,
                observed=None,
                reason=obligation or claim,
                basis=None,
                source_refs=(),
                evidence=(),
            )
        )
        mappings.append(AdapterIdMap(anonymous_id=report_id, original_id=original_id))
    audit = AdapterAudit(
        source_format="legacy_report_clusters",
        source_path=str(path),
        source_hash=_sha256_bytes(raw_bytes),
        report_id_map=tuple(mappings),
        expected_id_map=expected_id_map,
        projected_field_names=_candidate_field_names(),
        excluded_field_names=EXCLUDED_PROVIDER_FIELDS,
        reason="Only D1/D2 raw historical cluster claims, obligations, and locations were projected; D/W/L, predicates, arm identity, and historical outcomes were removed before provider serialization.",
        basis=f"{ADAPTER_VERSION}; read-only report_issue_clusters D1/D2 projection",
    )
    return tuple(reports), audit, int(round_no), pair_id


def build_unified_input(
    *,
    reports: tuple[CandidateReport, ...],
    expected_issues: tuple[ExpectedIssue, ...],
    artifact_closure: JudgeArtifactClosure,
) -> UnifiedJudgeInput:
    """Cross the final adapter boundary into the single provider-visible schema."""

    return UnifiedJudgeInput(
        protocol_version=PROTOCOL_VERSION,
        pair_id=artifact_closure.pair_id,
        reports=reports,
        expected_issues=expected_issues,
        artifact_closure=artifact_closure,
        reason="Anonymous published reports are judged against the frozen pair denominator and one common artifact closure.",
        basis=f"{ADAPTER_VERSION}; {ARTIFACT_BUILDER_VERSION}; {PROTOCOL_VERSION}",
    )


def stable_model_hash(value: Any) -> str:
    """Hash a validated model or JSON-compatible primitive deterministically."""

    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return _sha256_bytes(_stable_json(value).encode("utf-8"))


def candidate_schema_field_set() -> frozenset[str]:
    """Expose the common report field set for fairness regression tests."""

    schema = TypeAdapter(CandidateReport).json_schema()
    return frozenset(schema["properties"])
