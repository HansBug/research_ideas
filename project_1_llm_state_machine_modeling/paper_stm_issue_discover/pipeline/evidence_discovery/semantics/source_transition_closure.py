"""Deterministic closure for author transitions represented by compiler macros."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ..inputs.models import PairInput
from .obligations import CandidateIssue
from .workflow import NLContract

ClosureStatus = Literal["satisfied", "unresolved", "not_applicable"]
CandidateDisposition = Literal[
    "suppress_matching_endpoint_candidates",
    "retain_candidates",
]


class SourceTransitionClosureHashes(BaseModel):
    """Artifact identities used by one source-transition closure decision."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    fcstm_sha256: str | None = Field(
        default=None,
        description="SHA-256 identity of the exact closed FCSTM artifact, when present in the pair closure.",
    )
    plantuml_sha256: str | None = Field(
        default=None,
        description="SHA-256 identity of the exact author PlantUML artifact, when present in the pair closure.",
    )
    canonical_source_sha256: str | None = Field(
        default=None,
        description="SHA-256 identity of the canonical author-source IR artifact, when present in the pair closure.",
    )
    source_inventory_sha256: str | None = Field(
        default=None,
        description="SHA-256 identity of the deterministic exact source inventory artifact, when present.",
    )
    working_contract_sha256: str | None = Field(
        default=None,
        description="SHA-256 identity of the published source-to-compiler working contract, when present.",
    )


class SourceTransitionClosureMemberReceipt(BaseModel):
    """Mechanical line and ownership closure for one protected macro member."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal[
        "evidence-discovery.source-transition-closure-member.v1"
    ] = Field(
        default="evidence-discovery.source-transition-closure-member.v1",
        description="Persistence schema version for one protected macro-member closure receipt.",
    )
    macro_id: str = Field(
        min_length=1,
        description="Exact compiler macro identity that claims this member.",
    )
    member_element_id: str = Field(
        min_length=1,
        description="Exact working-contract element identity expected in the macro member set.",
    )
    member_kind: str | None = Field(
        default=None,
        description="Published working-contract kind of the member, or null when the member row is absent.",
    )
    generated_role: str | None = Field(
        default=None,
        description="Published generated role of the member, or null when the working contract supplies none.",
    )
    model_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact closed-model references published for this compiler-owned member.",
    )
    declared_line_sha256: str | None = Field(
        default=None,
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the exact FCSTM line declared by the working contract, or null when no line is declared.",
    )
    resolved_fcstm_line: int | None = Field(
        default=None,
        ge=1,
        description="Unique one-based FCSTM line matching the published member line, or null when line closure fails.",
    )
    resolved_fcstm_ref: str | None = Field(
        default=None,
        description="Stable FCSTM line reference materialized from the exact closed artifact, or null when unresolved.",
    )
    protected_compiler_member: bool = Field(
        description="Whether origin, edit policy, and macro membership all identify a protected compiler-owned member.",
    )
    exact_line_match: bool = Field(
        description="Whether the declared member line occurs uniquely and exactly in the closed FCSTM artifact.",
    )
    source_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact author-source references attributed to this macro member by the working contract.",
    )
    closed: bool = Field(
        description="Whether this member passes both protected ownership and exact FCSTM line closure.",
    )
    reason: str = Field(
        min_length=1,
        description="English explanation of the member closure result.",
    )
    basis: str = Field(
        min_length=1,
        description="Exact element, macro, line, and artifact basis used for the member result.",
    )


class SourceTransitionClosureReceipt(BaseModel):
    """Auditable closure for one required endpoint represented by a protected macro."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.source-transition-closure.v1"] = Field(
        default="evidence-discovery.source-transition-closure.v1",
        description="Persistence schema version for deterministic source-transition macro closure.",
    )
    algorithm_version: Literal["source-transition-macro-closure.v1"] = Field(
        default="source-transition-macro-closure.v1",
        description="Version of the deterministic endpoint, macro, digest, ownership, and exact-line join.",
    )
    contract_id: str = Field(
        min_length=1,
        description="Exact typed endpoint contract evaluated by this closure receipt.",
    )
    required_source: str | None = Field(
        default=None,
        description="Exact required source concept from the typed contract, or null when endpoint extraction is unresolved.",
    )
    required_target: str | None = Field(
        default=None,
        description="Exact required target concept from the typed contract, or null when endpoint extraction is unresolved.",
    )
    source_transition_id: str | None = Field(
        default=None,
        description="Unique exact author-source transition identity joined to the contract endpoints, or null when unresolved.",
    )
    source_transition_raw_ref: str | None = Field(
        default=None,
        description="Exact author-source line reference for the joined transition, or null when unresolved.",
    )
    source_line_sha256: str | None = Field(
        default=None,
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the exact author-source line identified by the source inventory, or null when unresolved.",
    )
    macro_id: str | None = Field(
        default=None,
        description="Unique working-contract macro identity joined to the source transition, or null when unresolved.",
    )
    expected_member_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Complete sorted macro member inventory published by the working contract.",
    )
    observed_member_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Sorted member identities actually found as unique working-contract element rows.",
    )
    published_member_digest: str | None = Field(
        default=None,
        pattern=r"^[0-9a-f]{64}$",
        description="Published digest of the complete sorted member inventory, or null when unavailable.",
    )
    recomputed_member_digest: str | None = Field(
        default=None,
        pattern=r"^[0-9a-f]{64}$",
        description="Digest recomputed from the complete sorted member inventory, or null when unavailable.",
    )
    target_entry_member_id: str | None = Field(
        default=None,
        description="Unique protected target-entry member that realizes the required target, or null when unresolved.",
    )
    target_entry_fcstm_ref: str | None = Field(
        default=None,
        description="Exact closed FCSTM line reference for the target-entry segment, or null when unresolved.",
    )
    member_receipts: tuple[SourceTransitionClosureMemberReceipt, ...] = Field(
        default_factory=tuple,
        description="One mechanical closure receipt for every published macro member identity.",
    )
    hashes: SourceTransitionClosureHashes = Field(
        description="Exact artifact hashes bound into the closure decision.",
    )
    diagnostics: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Deterministic English failure details; an empty tuple means every required join closed.",
    )
    status: ClosureStatus = Field(
        description="satisfied only for complete endpoint, macro, digest, ownership, target-entry, line, and hash closure.",
    )
    candidate_disposition: CandidateDisposition = Field(
        description="Whether matching endpoint candidates are suppressed or retained after this deterministic closure.",
    )
    source_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact author and working-contract references supporting the closure decision.",
    )
    reason: str = Field(
        min_length=1,
        description="English explanation of why the endpoint is closed or remains unresolved.",
    )
    basis: str = Field(
        min_length=1,
        description="Exact contract, source-transition, macro, member, line, digest, and hash basis for the decision.",
    )


class SourceTransitionCandidateDispositionReceipt(BaseModel):
    """Audit row for one endpoint candidate suppressed by a satisfied macro closure."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal[
        "evidence-discovery.source-transition-candidate-disposition.v1"
    ] = Field(
        default="evidence-discovery.source-transition-candidate-disposition.v1",
        description="Persistence schema version for one source-transition candidate disposition.",
    )
    candidate_origin: Literal["grounding", "deterministic_frontier"] = Field(
        description="Method component that produced the candidate before deterministic closure.",
    )
    contract_id: str = Field(
        min_length=1,
        description="Exact endpoint contract identity copied from the suppressed candidate.",
    )
    candidate_title: str = Field(
        min_length=1,
        description="English title of the suppressed endpoint candidate for audit traceability.",
    )
    source_transition_id: str = Field(
        min_length=1,
        description="Exact author transition whose complete protected macro satisfies the candidate endpoint.",
    )
    macro_id: str = Field(
        min_length=1,
        description="Exact complete protected macro that caused deterministic suppression.",
    )
    disposition: Literal["suppressed_satisfied_endpoint"] = Field(
        default="suppressed_satisfied_endpoint",
        description="Deterministic candidate disposition after complete source-transition macro closure.",
    )
    reason: str = Field(
        min_length=1,
        description="English explanation of why this candidate is a compiler-expansion false positive.",
    )
    basis: str = Field(
        min_length=1,
        description="Exact closure receipt identities supporting suppression.",
    )


def _sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sha256_json(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _endpoint_matches(required: str, observed: str) -> bool:
    """Match one typed concept to one exact or uniquely qualified source endpoint."""

    return observed == required or observed.rsplit(".", 1)[-1] == required


def _artifact_hashes(pair: PairInput) -> SourceTransitionClosureHashes:
    manifest_hashes = {
        artifact.role: artifact.sha256
        for artifact in (
            pair.context_manifest.artifacts if pair.context_manifest else ()
        )
    }
    return SourceTransitionClosureHashes(
        fcstm_sha256=pair.hashes.get("fcstm") or manifest_hashes.get("fcstm_model"),
        plantuml_sha256=pair.hashes.get("plantuml")
        or manifest_hashes.get("plantuml_source"),
        canonical_source_sha256=pair.hashes.get("canonical")
        or manifest_hashes.get("canonical_source_ir"),
        source_inventory_sha256=pair.hashes.get("source_inventory")
        or manifest_hashes.get("source_inventory"),
        working_contract_sha256=pair.hashes.get("working_contract")
        or manifest_hashes.get("working_contract"),
    )


def _contract_endpoints(contract: NLContract) -> tuple[str, str] | None:
    sources = [hint.value for hint in contract.binding_hints if hint.role == "source"]
    targets = [hint.value for hint in contract.binding_hints if hint.role == "target"]
    if len(sources) != 1 or len(targets) != 1:
        return None
    return sources[0], targets[0]


def _source_line(pair: PairInput, line: int | None) -> tuple[str | None, str | None]:
    if line is None:
        return None, None
    lines = pair.plantuml_text.splitlines()
    if line > len(lines):
        return None, None
    return f"plantuml:line:{line}", _sha256_text(lines[line - 1])


def _member_receipt(
    pair: PairInput,
    *,
    macro_id: str,
    member_id: str,
    element: Mapping[str, Any] | None,
) -> SourceTransitionClosureMemberReceipt:
    if element is None:
        return SourceTransitionClosureMemberReceipt(
            macro_id=macro_id,
            member_element_id=member_id,
            protected_compiler_member=False,
            exact_line_match=False,
            closed=False,
            reason="The published macro member has no unique working-contract element row.",
            basis=f"macro_id={macro_id}; member_element_id={member_id}; matching_element_count=0",
        )

    metadata = element.get("metadata")
    metadata = metadata if isinstance(metadata, Mapping) else {}
    declared_line = metadata.get("line")
    declared_line = (
        declared_line if isinstance(declared_line, str) and declared_line else None
    )
    matching_lines = (
        [
            line_no
            for line_no, line_text in enumerate(pair.fcstm_text.splitlines(), start=1)
            if line_text.strip() == declared_line.strip()
        ]
        if declared_line
        else []
    )
    resolved_line = matching_lines[0] if len(matching_lines) == 1 else None
    member_kind = element.get("kind")
    transition_line_closed = True
    if member_kind == "transition_segment" and resolved_line is not None:
        transition_line_closed = any(
            transition.line == resolved_line for transition in pair.model.transitions
        )
    exact_line_match = resolved_line is not None and transition_line_closed
    protected = (
        element.get("origin") == "compiler_owned"
        and element.get("edit_policy") == "protected"
        and macro_id in element.get("macro_ids", [])
    )
    closed = protected and exact_line_match
    source_refs = tuple(
        value
        for value in element.get("source_refs", [])
        if isinstance(value, str) and value
    )
    if closed:
        reason = "The compiler-owned protected member resolves to one exact closed-FCSTM line."
    elif not protected:
        reason = "The member does not close the required compiler-owned protected ownership boundary."
    else:
        reason = "The protected member does not resolve to one unique exact closed-FCSTM line."
    return SourceTransitionClosureMemberReceipt(
        macro_id=macro_id,
        member_element_id=member_id,
        member_kind=member_kind if isinstance(member_kind, str) else None,
        generated_role=(
            str(metadata["generated_role"])
            if metadata.get("generated_role") is not None
            else None
        ),
        model_refs=tuple(
            value
            for value in element.get("model_refs", [])
            if isinstance(value, str) and value
        ),
        declared_line_sha256=_sha256_text(declared_line) if declared_line else None,
        resolved_fcstm_line=resolved_line,
        resolved_fcstm_ref=(
            f"fcstm:line:{resolved_line}" if resolved_line is not None else None
        ),
        protected_compiler_member=protected,
        exact_line_match=exact_line_match,
        source_refs=source_refs,
        closed=closed,
        reason=reason,
        basis=(
            f"macro_id={macro_id}; member_element_id={member_id}; "
            f"matching_fcstm_lines={matching_lines}; model_refs={list(element.get('model_refs', []))}"
        ),
    )


def evaluate_source_transition_closure(
    pair: PairInput,
    contract: NLContract,
) -> SourceTransitionClosureReceipt:
    """Join one exact endpoint contract to a complete protected compiler macro."""

    hashes = _artifact_hashes(pair)
    endpoints = _contract_endpoints(contract)
    if (
        contract.property != "transition_endpoints"
        or contract.expected_direction != "must_exist"
    ):
        return SourceTransitionClosureReceipt(
            contract_id=contract.contract_id,
            hashes=hashes,
            status="not_applicable",
            candidate_disposition="retain_candidates",
            reason="The contract is not an exact required transition-endpoint obligation.",
            basis="typed contract property and expected_direction",
        )
    if endpoints is None:
        return SourceTransitionClosureReceipt(
            contract_id=contract.contract_id,
            hashes=hashes,
            status="unresolved",
            candidate_disposition="retain_candidates",
            diagnostics=(
                "The contract does not contain exactly one source hint and one target hint.",
            ),
            reason="Source-transition closure requires one exact source and one exact target.",
            basis="typed contract binding-hint cardinality",
        )

    required_source, required_target = endpoints
    inventory = pair.exact_source_inventory
    working = pair.working_contract
    if inventory is None or working is None:
        return SourceTransitionClosureReceipt(
            contract_id=contract.contract_id,
            required_source=required_source,
            required_target=required_target,
            hashes=hashes,
            status="unresolved",
            candidate_disposition="retain_candidates",
            diagnostics=(
                "The exact source inventory or working contract is unavailable.",
            ),
            reason="The public artifact closure is incomplete, so endpoint candidates remain eligible.",
            basis="PairInput exact_source_inventory and working_contract availability",
        )

    source_matches = [
        transition
        for transition in inventory.transitions
        if _endpoint_matches(required_source, transition.source)
        and _endpoint_matches(required_target, transition.target)
    ]
    if len(source_matches) != 1:
        return SourceTransitionClosureReceipt(
            contract_id=contract.contract_id,
            required_source=required_source,
            required_target=required_target,
            hashes=hashes,
            status="unresolved",
            candidate_disposition="retain_candidates",
            diagnostics=(
                "The typed contract endpoints do not join to exactly one author-source transition.",
            ),
            reason="A unique author-transition identity is required before compiler-macro closure can suppress a candidate.",
            basis=f"required_source={required_source}; required_target={required_target}; source_match_count={len(source_matches)}",
        )

    source_transition = source_matches[0]
    source_element_id = f"source:transition:{source_transition.transition_id}"
    payload = working.payload
    raw_elements = [
        item for item in payload.get("elements", []) if isinstance(item, Mapping)
    ]
    element_rows = [
        item for item in raw_elements if item.get("element_id") == source_element_id
    ]
    raw_macros = [
        item for item in payload.get("macros", []) if isinstance(item, Mapping)
    ]
    matching_macros = [
        item
        for item in raw_macros
        if source_element_id in item.get("source_element_ids", [])
    ]
    diagnostics: list[str] = []
    if len(element_rows) != 1:
        diagnostics.append(
            "The author-transition macro root does not have exactly one working-contract element row."
        )
    if len(matching_macros) != 1:
        diagnostics.append(
            "The author-transition identity does not join to exactly one working-contract macro."
        )
    if diagnostics:
        source_ref, source_line_hash = _source_line(pair, source_transition.line)
        return SourceTransitionClosureReceipt(
            contract_id=contract.contract_id,
            required_source=required_source,
            required_target=required_target,
            source_transition_id=source_transition.transition_id,
            source_transition_raw_ref=source_transition.raw_ref,
            source_line_sha256=source_line_hash,
            hashes=hashes,
            diagnostics=tuple(diagnostics),
            status="unresolved",
            candidate_disposition="retain_candidates",
            source_refs=tuple(
                value
                for value in dict.fromkeys((source_transition.raw_ref, source_ref))
                if value
            ),
            reason="The author transition is exact, but its compiler-macro identity is not closed.",
            basis=f"source_element_id={source_element_id}; element_row_count={len(element_rows)}; macro_count={len(matching_macros)}",
        )

    root = element_rows[0]
    macro = matching_macros[0]
    macro_id = macro.get("macro_id")
    if not isinstance(macro_id, str) or not macro_id:
        macro_id = None
        diagnostics.append("The matching macro has no stable macro identity.")
    root_macro_ids = root.get("macro_ids", [])
    root_semantics = root.get("semantic_fields")
    root_semantics = root_semantics if isinstance(root_semantics, Mapping) else {}
    if not (
        root.get("origin") == "source_owned"
        and root.get("kind") == "transition_macro_root"
        and root.get("edit_policy") == "macro_issue_bound"
        and macro_id is not None
        and macro_id in root_macro_ids
        and root_semantics.get("source_endpoint") == source_transition.source
        and root_semantics.get("target_endpoint") == source_transition.target
    ):
        diagnostics.append(
            "The source-owned macro root does not preserve the exact author-transition endpoint identity and macro boundary."
        )

    expected_member_ids = tuple(
        sorted(
            value
            for value in macro.get("member_element_ids", [])
            if isinstance(value, str) and value
        )
    )
    published_digest = macro.get("member_digest")
    published_digest = (
        published_digest
        if isinstance(published_digest, str) and len(published_digest) == 64
        else None
    )
    recomputed_digest = (
        _sha256_json(list(expected_member_ids)) if expected_member_ids else None
    )
    if not expected_member_ids or len(expected_member_ids) != len(
        set(expected_member_ids)
    ):
        diagnostics.append(
            "The macro member inventory is empty or contains duplicate identities."
        )
    if published_digest is None or published_digest != recomputed_digest:
        diagnostics.append(
            "The published macro member digest does not close over the complete sorted member inventory."
        )

    elements_by_id: dict[str, list[Mapping[str, Any]]] = {}
    for element in raw_elements:
        element_id = element.get("element_id")
        if isinstance(element_id, str):
            elements_by_id.setdefault(element_id, []).append(element)
    member_receipts = tuple(
        _member_receipt(
            pair,
            macro_id=macro_id or "unresolved-macro",
            member_id=member_id,
            element=(
                elements_by_id[member_id][0]
                if len(elements_by_id.get(member_id, [])) == 1
                else None
            ),
        )
        for member_id in expected_member_ids
    )
    observed_member_ids = tuple(
        sorted(
            member_id
            for member_id in expected_member_ids
            if len(elements_by_id.get(member_id, [])) == 1
        )
    )
    if any(not receipt.closed for receipt in member_receipts):
        diagnostics.append(
            "At least one published macro member lacks protected ownership or one unique exact FCSTM line."
        )

    target_entries = [
        receipt
        for receipt in member_receipts
        if receipt.generated_role == "composite_source_target_entry_segment"
    ]
    target_entry = target_entries[0] if len(target_entries) == 1 else None
    if target_entry is None or target_entry.resolved_fcstm_line is None:
        diagnostics.append(
            "The complete macro does not expose exactly one closed target-entry segment."
        )
    else:
        transition = next(
            (
                item
                for item in pair.model.transitions
                if item.line == target_entry.resolved_fcstm_line
            ),
            None,
        )
        if (
            transition is None
            or transition.source != "[*]"
            or not _endpoint_matches(required_target, transition.target)
        ):
            diagnostics.append(
                "The protected target-entry segment does not enter the exact required target."
            )

    input_identity = payload.get("input_identity")
    input_identity = input_identity if isinstance(input_identity, Mapping) else {}
    source_trace = payload.get("source_trace_base")
    source_trace = source_trace if isinstance(source_trace, Mapping) else {}
    traceability = source_trace.get("source_traceability")
    traceability = traceability if isinstance(traceability, Mapping) else {}
    expected_fcstm_hash = (hashes.fcstm_sha256 or "").removeprefix("sha256:")
    expected_source_hash = (hashes.plantuml_sha256 or "").removeprefix("sha256:")
    hash_checks = (
        inventory.source_ir_hash == hashes.canonical_source_sha256,
        input_identity.get("fcstm_sha256") == expected_fcstm_hash,
        input_identity.get("source_sha256") == expected_source_hash,
        traceability.get("fcstm_sha256") == expected_fcstm_hash,
        traceability.get("source_stm0_sha256") == expected_source_hash,
        working.ref.sha256 == hashes.working_contract_sha256,
    )
    if not all(hash_checks):
        diagnostics.append(
            "The source inventory, working contract, source trace, and current pair do not share one artifact-hash closure."
        )

    source_ref, source_line_hash = _source_line(pair, source_transition.line)
    if source_ref is None or source_line_hash is None:
        diagnostics.append(
            "The exact author-source line cannot be materialized from the supplied PlantUML artifact."
        )

    status: ClosureStatus = "satisfied" if not diagnostics else "unresolved"
    disposition: CandidateDisposition = (
        "suppress_matching_endpoint_candidates"
        if status == "satisfied"
        else "retain_candidates"
    )
    source_refs = tuple(
        dict.fromkeys(
            value
            for value in (
                source_transition.raw_ref,
                source_ref,
                source_element_id,
                macro_id,
                *(ref for receipt in member_receipts for ref in receipt.source_refs),
            )
            if value
        )
    )
    if status == "satisfied":
        reason = "The exact author transition is represented by one complete protected compiler macro with a closed member digest, exact member lines, and an exact target-entry segment."
    else:
        reason = "The author transition or compiler macro is only partially closed, so endpoint candidates remain eligible for downstream adjudication."
    return SourceTransitionClosureReceipt(
        contract_id=contract.contract_id,
        required_source=required_source,
        required_target=required_target,
        source_transition_id=source_transition.transition_id,
        source_transition_raw_ref=source_transition.raw_ref,
        source_line_sha256=source_line_hash,
        macro_id=macro_id,
        expected_member_ids=expected_member_ids,
        observed_member_ids=observed_member_ids,
        published_member_digest=published_digest,
        recomputed_member_digest=recomputed_digest,
        target_entry_member_id=(
            target_entry.member_element_id if target_entry is not None else None
        ),
        target_entry_fcstm_ref=(
            target_entry.resolved_fcstm_ref if target_entry is not None else None
        ),
        member_receipts=member_receipts,
        hashes=hashes,
        diagnostics=tuple(diagnostics),
        status=status,
        candidate_disposition=disposition,
        source_refs=source_refs,
        reason=reason,
        basis=(
            f"contract_id={contract.contract_id}; source_transition_id={source_transition.transition_id}; "
            f"macro_id={macro_id}; member_count={len(expected_member_ids)}; "
            f"published_member_digest={published_digest}; recomputed_member_digest={recomputed_digest}; "
            f"target_entry_ref={target_entry.resolved_fcstm_ref if target_entry else None}; hashes={hashes.model_dump(mode='json')}"
        ),
    )


def endpoint_candidate_is_satisfied_by_macro(
    candidate: CandidateIssue,
    receipt: SourceTransitionClosureReceipt | None,
) -> bool:
    """Return whether complete macro closure satisfies this exact endpoint candidate."""

    return bool(
        receipt is not None
        and receipt.status == "satisfied"
        and receipt.candidate_disposition == "suppress_matching_endpoint_candidates"
        and candidate.contract_id == receipt.contract_id
        and candidate.property == "transition_endpoints"
    )


def suppress_satisfied_source_transition_candidates(
    candidates: Sequence[CandidateIssue],
    receipts: Mapping[str, SourceTransitionClosureReceipt],
    *,
    candidate_origin: Literal["grounding", "deterministic_frontier"],
) -> tuple[list[CandidateIssue], list[SourceTransitionCandidateDispositionReceipt]]:
    """Remove only endpoint candidates with complete protected source-macro closure."""

    retained: list[CandidateIssue] = []
    dispositions: list[SourceTransitionCandidateDispositionReceipt] = []
    for candidate in candidates:
        receipt = receipts.get(candidate.contract_id)
        if not endpoint_candidate_is_satisfied_by_macro(candidate, receipt):
            retained.append(candidate)
            continue
        assert receipt is not None
        assert receipt.source_transition_id is not None
        assert receipt.macro_id is not None
        dispositions.append(
            SourceTransitionCandidateDispositionReceipt(
                candidate_origin=candidate_origin,
                contract_id=candidate.contract_id,
                candidate_title=candidate.title,
                source_transition_id=receipt.source_transition_id,
                macro_id=receipt.macro_id,
                reason="The candidate treats a protected compiler expansion member as an independent missing endpoint even though the complete macro realizes the exact author transition.",
                basis=(
                    f"contract_id={candidate.contract_id}; source_transition_id={receipt.source_transition_id}; "
                    f"macro_id={receipt.macro_id}; target_entry_ref={receipt.target_entry_fcstm_ref}; "
                    f"member_digest={receipt.recomputed_member_digest}"
                ),
            )
        )
    return retained, dispositions


__all__ = [
    "SourceTransitionCandidateDispositionReceipt",
    "SourceTransitionClosureHashes",
    "SourceTransitionClosureMemberReceipt",
    "SourceTransitionClosureReceipt",
    "endpoint_candidate_is_satisfied_by_macro",
    "evaluate_source_transition_closure",
    "suppress_satisfied_source_transition_candidates",
]
