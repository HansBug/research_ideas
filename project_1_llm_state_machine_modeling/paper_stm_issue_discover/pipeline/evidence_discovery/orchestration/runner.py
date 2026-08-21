from __future__ import annotations

import hashlib
import json
import multiprocessing
import re
import subprocess
import uuid
from collections import Counter, defaultdict
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ..backends import run_backend
from ..compiler import compile_plan
from ..compiler.plans import validate_plan
from ..evidence import build_evidence_record, validate_and_hash_w2_audit_bundle
from ..evidence.receipts import RawReceipt
from ..evidence.source_attribution import build_source_attribution
from ..inputs import FROZEN_PAIR_IDS, load_pair
from ..inputs.models import PairInput
from ..registry import load_registry
from ..reporting.export import write_json, write_markdown_summary
from ..semantics import (
    CandidateIssue,
    CONTRACT_SYSTEM_PROMPT,
    ContextBudgetReceipt,
    DAdjudicationResponse,
    D_SYSTEM_PROMPT,
    GroundingResponse,
    MODEL_GROUNDING_SYSTEM_PROMPT,
    NLContractResponse,
    SemanticAdjudication,
    SOURCE_GROUNDING_SYSTEM_PROMPT,
    StageReceipt,
    MethodResponse,
    assemble_method_response,
    bind_candidate,
    build_contract_prompt,
    build_d_adjudication_prompt,
    build_d_correction_prompt,
    build_grounding_prompt,
    fallback_contracts,
    fallback_d_adjudication,
    fallback_grounding,
    resolve_transition_ref,
)
from ..semantics.obligations import fallback_candidates
from .contracts import (
    IndependentJudgeReceipt,
    MethodCellReceipt,
    PairRunStatus,
    RunManifest,
    RunSummaryReceipt,
    SourceProvenance,
)
from .runtime import (
    DEFAULT_TRANSPORT_RETRIES,
    FixtureStructuredRuntime,
    PublicStructuredRuntime,
    StructuredCallOutcome,
    TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS,
)


REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS = ("0004", "0023", "0029", "0035", "0046", "0053")
METHOD_CELL_SCHEMA = "paper1.evidence_discovery.method_cell.v2"
JUDGE_SCHEMA = "paper1.evidence_discovery.independent_judge.v2"
SUMMARY_SCHEMA = "paper1.evidence_discovery.run_summary.v2"
RUN_MANIFEST_SCHEMA = "paper1.evidence_discovery.run_manifest.v2"
CODE_VERSION = "evidence-discovery-orchestration.v5"
PROMPT_SCHEMA_VERSION = "evidence-discovery-staged-prompts.v4"
JUDGE_PROMPT_TOKEN_BUDGET = 180_000
# Keep the normal judge surface small enough that the model can close every
# exact-ID row in one response.  A larger release surface is partitioned
# before provider execution; this avoids a failed pair-wide response falling
# through to an unbounded ledger x release relation matrix.
JUDGE_PAIRWISE_MAX_RELEASES = 5
JUDGE_PARTITION_RELEASE_SIZE = 8
# Atomic fallback is a bounded recovery path for genuinely small relation
# sets.  A failed large partition must remain judge-unavailable; expanding it
# to ledger x release would recreate the quadratic call surface we are trying
# to avoid.
JUDGE_ATOMIC_RELATION_BUDGET = 12


class LedgerAssessment(BaseModel):
    """Independent judge assessment for one frozen ledger entry."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    ledger_id: str = Field(min_length=1, description="Frozen ledger entry ID being assessed; copy it exactly from judge input.")
    hit_r1: bool = Field(default=False, description="Whether method round 1 contains a semantically identical release issue.")
    hit_r2: bool = Field(default=False, description="Whether method round 2 contains a semantically identical release issue.")
    hit_r3: bool = Field(default=False, description="Whether method round 3 contains a semantically identical release issue.")
    matched_issue_ids: list[str] = Field(default_factory=list, description="Method issue IDs that support the claimed round hits.")
    reason: str = Field(min_length=1, description="Non-empty explanation of why this ledger item is or is not semantically matched.")
    basis: str = Field(min_length=1, description="Non-empty evidence basis for this ledger assessment, tied to the supplied ledger and method release data.")


class ReleaseAssessment(BaseModel):
    """Independent judge assessment for one released method issue."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    issue_id: str = Field(min_length=1, description="Released method issue ID being assessed; copy it exactly from method input.")
    accounted_ledger_ids: list[str] = Field(default_factory=list, description="Frozen ledger IDs that semantically account for this release issue.")
    is_false_positive: bool = Field(description="True only when no supplied frozen ledger entry can semantically carry this issue.")
    reason: str = Field(min_length=1, description="Non-empty explanation of why this release issue is or is not a false positive.")
    basis: str = Field(min_length=1, description="Non-empty evidence basis for the release decision, tied to supplied ledger and method release data.")


class JudgeResponse(BaseModel):
    """Complete independent judge response with rationale for all decisions."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    ledger_assessments: list[LedgerAssessment] = Field(default_factory=list, description="One assessment for every frozen ledger item supplied to the judge.")
    release_assessments: list[ReleaseAssessment] = Field(default_factory=list, description="One assessment for every method issue in the supplied release surface.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the judge's overall assessment decision.")
    basis: str = Field(min_length=1, description="Non-empty basis identifying the supplied ledger and method release facts used by the judge.")


class AtomicMatchDecision(BaseModel):
    """One independent semantic relation used when pair-wide judge shape cannot close."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    matches: bool = Field(description="True only when the supplied ledger entry and release issue have the same locus and property.")
    confidence: Literal["high", "medium", "low"] = Field(description="Independent judge confidence in this one semantic relation.")
    reason: str = Field(min_length=1, description="Non-empty semantic explanation of why this exact ledger/issue relation matches or does not match.")
    basis: str = Field(min_length=1, description="Non-empty basis naming only the supplied ledger entry and release issue facts.")


METHOD_SYSTEM_PROMPT = """The method is staged. The public method-generation surface is the NL contract extraction stage followed by two complementary grounding branches. Use only the complete context manifest supplied to each stage. Never read ledger answers, baseline results, judge examples, or historical release outputs. Do not emit W, D, or L levels. Every structured object must contain non-empty reason and basis."""

JUDGE_SYSTEM_PROMPT = """You are an independent judge separated from method generation. You may use the supplied frozen ledger entries to assess method D1/D2 release issues. Judge semantic identity of locus and property, not string similarity. Do not read baseline results, other pairs, other judge outputs, or historical examples. Every assessment and the top-level response must contain non-empty reason and basis fields that explain the judgment and its supplied-input support. Preserve the model's original wording."""


def _prompt_schema_hash() -> str:
    """Hash every prompt contract and structured response schema used by a run."""

    return _hash_json(
        {
            "version": PROMPT_SCHEMA_VERSION,
            "system_prompts": {
                "method_boundary": METHOD_SYSTEM_PROMPT,
                "contract": CONTRACT_SYSTEM_PROMPT,
                "source_grounding": SOURCE_GROUNDING_SYSTEM_PROMPT,
                "model_grounding": MODEL_GROUNDING_SYSTEM_PROMPT,
                "d_adjudication": D_SYSTEM_PROMPT,
                "judge": JUDGE_SYSTEM_PROMPT,
                "atomic_judge": ATOMIC_JUDGE_SYSTEM_PROMPT,
            },
            "schemas": {
                "nl_contract": NLContractResponse.model_json_schema(),
                "grounding": GroundingResponse.model_json_schema(),
                "d_adjudication": DAdjudicationResponse.model_json_schema(),
                "judge": JudgeResponse.model_json_schema(),
                "atomic_judge": AtomicMatchDecision.model_json_schema(),
            },
        }
    )


def _collect_pair_input_hashes(
    report_root: Path,
    selected_pair_ids: Sequence[str],
) -> dict[str, str]:
    """Resolve the complete context-manifest hash for every selected pair."""

    hashes: dict[str, str] = {}
    for pair_id in selected_pair_ids:
        pair = load_pair(report_root / "pairs" / pair_id)
        if pair.context_manifest is None:
            raise ValueError(f"pair {pair_id} has no complete context manifest")
        hashes[pair_id] = pair.context_manifest.manifest_hash
    return hashes


def _resolve_run_root(
    output_dir: Path,
    *,
    resume: bool,
    requested_run_id: str | None,
) -> tuple[Path, str]:
    """Select a run-id-bearing artifact root without guessing across runs."""

    base = output_dir.expanduser().resolve()
    if resume:
        candidates: list[Path] = []
        if (base / "run_manifest.json").is_file():
            candidates.append(base)
        if requested_run_id is not None and (base / requested_run_id / "run_manifest.json").is_file():
            candidates.append(base / requested_run_id)
        if requested_run_id is None and base.is_dir():
            candidates.extend(
                child
                for child in base.iterdir()
                if child.is_dir() and (child / "run_manifest.json").is_file()
            )
        unique = {candidate.resolve() for candidate in candidates}
        if len(unique) != 1:
            raise RuntimeError(
                "resume requires one exact run root or --run-id; no cross-run artifact selection is allowed"
            )
        run_root = unique.pop()
        existing = RunManifest.model_validate_json(
            (run_root / "run_manifest.json").read_text(encoding="utf-8")
        )
        if requested_run_id is not None and existing.run_id != requested_run_id:
            raise RuntimeError("requested run_id does not match run_manifest.json")
        if run_root.name != existing.run_id:
            raise RuntimeError("run artifact root must be named by its run_id")
        return run_root, existing.run_id

    run_id = requested_run_id or uuid.uuid4().hex
    if not re.fullmatch(r"[0-9a-f]{32}", run_id):
        raise ValueError("run_id must be 32 lowercase hexadecimal characters")
    run_root = base if base.name == run_id else base / run_id
    if (run_root / "run_manifest.json").exists():
        raise RuntimeError("run_id already exists; use resume=True or choose a fresh run_id")
    return run_root, run_id


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump(mode="json"))
    return str(value)


def _hash_json(value: Any) -> str:
    """Hash a canonical JSON value for stage and prompt receipts."""

    text = json.dumps(
        _jsonable(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _hash_file(path: Path) -> str:
    """Hash one exact input file without parsing or exposing its contents."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _retry_policy(transport_retries: int) -> dict[str, Any]:
    """Return the run-scoped retry and row-local billing contract."""

    if transport_retries < 0:
        raise ValueError("transport_retries must be non-negative")
    tail = TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS[-1]
    delays = [
        TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS[index]
        if index < len(TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS)
        else tail
        for index in range(transport_retries)
    ]
    return {
        "transport_retries": transport_retries,
        "transport_retry_delays_seconds": delays,
        "dead_structured_call_retries_after_provider_error": 1,
        "schema_and_non_provider_retries_billable": True,
        "provider_retry_exemption": "Only a failed provider attempt followed by an actual same-request retry is exempt; the successful attempt remains billable.",
        "reason": "The run uses v27-equivalent in-place provider recovery without cold cell reruns.",
        "basis": "utils.agent transport middleware plus row-local usage/retry identity",
    }


def _source_provenance() -> dict[str, Any]:
    """Capture the repository revision that produced a run receipt."""

    repo_root = Path(__file__).resolve().parents[5]
    try:
        commit = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        branch = subprocess.run(
            ["git", "-C", str(repo_root), "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo_root),
                    "status",
                    "--porcelain",
                    "--untracked-files=no",
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()
        )
        if not commit or not branch:
            raise RuntimeError("git returned an empty commit or branch")
        return SourceProvenance(
            source_commit=commit,
            source_branch=branch,
            source_dirty=dirty,
            reason=(
                "The run records the exact clean tracked repository revision used to construct method and judge artifacts."
                if not dirty
                else "The repository has tracked changes; fixture checks may proceed, but live execution must fail closed."
            ),
            basis="git rev-parse HEAD, git branch --show-current, and tracked git status",
        ).model_dump(mode="json")
    except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
        return SourceProvenance(
            source_commit="unknown",
            source_branch="unknown",
            source_dirty=True,
            reason="Repository provenance could not be resolved; a live formal run must fail closed.",
            basis=f"git provenance error: {type(exc).__name__}",
        ).model_dump(mode="json")


def _run_contract_hash(payload: dict[str, Any]) -> str:
    """Hash immutable run identity fields used by every resume check."""

    return _hash_json(payload)


def _manifest_contract_payload(
    *,
    profile: str,
    source_provenance: dict[str, Any],
    registry_version: str,
    registry_hash: str,
    prompt_schema_hash: str,
    input_data_hash: str,
    pair_input_hashes: dict[str, str],
    ledger_hash: str,
    rounds: int,
    selected_pair_ids: Sequence[str],
    scope: str,
    workers: int,
    transport_retries: int,
    streaming: bool,
) -> dict[str, Any]:
    """Return the immutable identity projection shared by run artifacts."""

    return {
        "profile": profile,
        "source_commit": source_provenance["source_commit"],
        "source_branch": source_provenance["source_branch"],
        "registry_version": registry_version,
        "registry_hash": registry_hash,
        "code_version": CODE_VERSION,
        "prompt_schema_version": PROMPT_SCHEMA_VERSION,
        "prompt_schema_hash": prompt_schema_hash,
        "input_data_hash": input_data_hash,
        "pair_input_hashes": dict(pair_input_hashes),
        "ledger_hash": ledger_hash,
        "rounds": rounds,
        "selected_pair_ids": list(selected_pair_ids),
        "scope": scope,
        "workers": workers,
        "transport_retries": transport_retries,
        "streaming": streaming,
        "retry_policy": _retry_policy(transport_retries),
    }


def _prepare_run_manifest(
    *,
    output_root: Path,
    profile: str,
    run_id: str,
    source_provenance: dict[str, Any],
    registry_version: str,
    registry_hash: str,
    prompt_schema_hash: str,
    input_data_hash: str,
    pair_input_hashes: dict[str, str],
    ledger_hash: str,
    rounds: int,
    selected_pair_ids: Sequence[str],
    workers: int,
    transport_retries: int,
    streaming: bool,
    resume: bool,
    predecessor_snapshot: str | None,
) -> RunManifest:
    """Create or validate the run manifest before any model call starts."""

    scope = (
        "full_protocol"
        if len(selected_pair_ids) == len(FROZEN_PAIR_IDS)
        else "diagnostic_subset"
    )
    contract = _manifest_contract_payload(
        profile=profile,
        source_provenance=source_provenance,
        registry_version=registry_version,
        registry_hash=registry_hash,
        prompt_schema_hash=prompt_schema_hash,
        input_data_hash=input_data_hash,
        pair_input_hashes=pair_input_hashes,
        ledger_hash=ledger_hash,
        rounds=rounds,
        selected_pair_ids=selected_pair_ids,
        scope=scope,
        workers=workers,
        transport_retries=transport_retries,
        streaming=streaming,
    )
    contract_hash = _run_contract_hash(contract)
    manifest_path = output_root / "run_manifest.json"
    now = datetime.now(timezone.utc)
    if manifest_path.is_file():
        if not resume:
            raise RuntimeError(
                "output directory already has a run manifest; use --resume or a new directory"
            )
        existing = RunManifest.model_validate_json(
            manifest_path.read_text(encoding="utf-8")
        )
        if existing.run_contract_hash != contract_hash:
            raise RuntimeError(
                "resume contract mismatch: profile, commit, registry, rounds, pairs, transport, or streaming changed"
            )
        if existing.run_id != run_id:
            raise RuntimeError("resume run_id does not match the selected run directory")
        resumed = existing.model_copy(update={"status": "running", "updated_at": now})
        write_json(manifest_path, resumed.model_dump(mode="json"))
        return resumed

    existing_cells = any((output_root / "method").glob("*/round-*.json")) or any(
        (output_root / "judge").glob("*.json")
    )
    if existing_cells:
        raise RuntimeError(
            "output directory contains pre-manifest cells; preserve it as a snapshot and use a new contract-compatible run directory"
        )
    if resume:
        raise RuntimeError(
            "cannot resume without run_manifest.json; preserve this directory as a pre-contract snapshot"
        )
    manifest = RunManifest(
        schema=RUN_MANIFEST_SCHEMA,
        run_id=run_id,
        run_contract_hash=contract_hash,
        status="running",
        profile=profile,
        source_provenance=SourceProvenance.model_validate(source_provenance),
        registry_version=registry_version,
        registry_hash=registry_hash,
        code_version=CODE_VERSION,
        prompt_schema_version=PROMPT_SCHEMA_VERSION,
        prompt_schema_hash=prompt_schema_hash,
        input_data_hash=input_data_hash,
        pair_input_hashes=pair_input_hashes,
        ledger_hash=ledger_hash,
        rounds=rounds,  # type: ignore[arg-type]
        selected_pair_ids=tuple(selected_pair_ids),
        scope=scope,  # type: ignore[arg-type]
        workers=workers,
        transport_retries=transport_retries,
        streaming=streaming,
        retry_policy=_retry_policy(transport_retries),
        started_at=now,
        updated_at=now,
        predecessor_snapshot=predecessor_snapshot,
        reason="This manifest freezes the current method/judge code, registry, pair grid, transport policy, and resume identity before provider execution.",
        basis="four-family-19-core.v1 plus the explicit live/full review gate and current clean Git commit",
    )
    write_json(manifest_path, manifest.model_dump(mode="json"))
    return manifest


def _stage_receipt(
    *,
    pair: PairInput,
    stage_id: str,
    stage_name: str,
    status: str,
    artifact_roles: tuple[str, ...],
    output: Any,
    reason: str,
    basis: str,
    outcome: StructuredCallOutcome[Any] | None = None,
    diagnostics: tuple[dict[str, Any], ...] = (),
) -> dict[str, Any]:
    """Build one validated stage receipt with the input manifest hash."""

    if pair.context_manifest is None:
        raise ValueError("stage receipt requires a complete context manifest")
    context_budget = (
        ContextBudgetReceipt.model_validate(
            outcome.context_budget.model_dump(mode="json")
        )
        if outcome is not None
        else ContextBudgetReceipt(
            mode="deterministic",
            projection_version="deterministic-no-prompt.v1",
            prompt_characters=None,
            estimated_prompt_tokens=None,
            provider_input_tokens=None,
            context_window_tokens=None,
            max_output_tokens=None,
            truncation_applied=False,
            projection_decision="This deterministic stage consumed typed artifacts directly and did not serialize an LLM prompt.",
            reason="No LLM context budget applies to this deterministic stage.",
            basis="typed stage inputs and deterministic method execution",
        )
    )
    return StageReceipt(
        stage_id=stage_id,
        stage_name=stage_name,  # type: ignore[arg-type]
        status=status,  # type: ignore[arg-type]
        input_manifest_hash=pair.context_manifest.manifest_hash,
        input_artifact_roles=artifact_roles,
        output_hash=_hash_json(output),
        llm_call_id=(
            str(outcome.result.get("call_id"))
            if outcome is not None and outcome.result.get("call_id")
            else None
        ),
        context_budget=context_budget,
        diagnostics=diagnostics,
        reason=reason,
        basis=basis,
    ).model_dump(mode="json")


def _aggregate_outcomes(
    outcomes: list[StructuredCallOutcome[Any]], *, kind: str = "method"
) -> dict[str, Any]:
    """Retain every public runtime call while keeping the legacy llm_call key."""

    usage = [row for outcome in outcomes for row in outcome.usage]
    attempts = [
        {"stage": outcome.kind, **attempt}
        for outcome in outcomes
        for attempt in outcome.attempts
    ]
    costs = [outcome.cost for outcome in outcomes]
    eligible = all(bool(cost.get("eligible")) for cost in costs) if costs else True
    total = sum(
        float(cost.get("total_usd") or 0.0)
        for cost in costs
        if isinstance(cost.get("total_usd"), (int, float))
    )
    return {
        "kind": kind,
        "status": "success" if outcomes and all(item.succeeded for item in outcomes) else "completed_with_diagnostics",
        "real_llm": bool(outcomes) and all(item.real_llm for item in outcomes),
        "response": None,
        "result": {"stage_count": len(outcomes), "stage_kinds": [item.kind for item in outcomes]},
        "attempts": attempts,
        "usage": usage,
        "cost": {"eligible": eligible, "total_usd": total if eligible else None, "attempts": [cost for cost in costs]},
        "reason": "All staged structured-call receipts were aggregated without discarding retries or diagnostics.",
        "basis": "public runtime outcomes, usage rows, and row-local billing dispositions",
    }


def _enrich_candidate(candidate: CandidateIssue, binding: Any, pair: PairInput) -> CandidateIssue:
    inputs = dict(candidate.predicate_inputs)
    inputs.setdefault("element_refs", list(binding.element_refs))
    bound_transitions = [item for item in pair.model.transitions if item.ref in binding.element_refs]
    transition_hint = inputs.get("transition") or inputs.get("transition_ref")
    transition_ref = resolve_transition_ref(
        transition_hint if isinstance(transition_hint, str) else None,
        pair.model,
        source=inputs.get("source") if isinstance(inputs.get("source"), str) else None,
        target=inputs.get("target") if isinstance(inputs.get("target"), str) else None,
    )
    if transition_ref is None and not transition_hint and len(bound_transitions) == 1:
        transition_ref = bound_transitions[0].ref
    # A predicate requiring one transition must receive one unambiguous
    # transition binding. Composite candidates remain W0 until the method names
    # the exact edge instead of silently selecting the first one.
    if transition_ref is not None:
        transition = pair.model.transition(transition_ref)
        if transition is not None:
            # Predicate inputs are executable fields, not provenance slots.
            # Once the binding identifies one closed-model edge, overwrite any
            # source/target/ref spellings emitted by the model (for example
            # ``state:Searching:line:13``).  Keeping those spellings would
            # make the backend compare a typed source reference with the
            # canonical FCSTM endpoint and report a false missing edge.
            inputs["transition"] = transition.ref
            inputs["transition_ref"] = transition.ref
            inputs["source"] = transition.source
            inputs["target"] = transition.target
    if candidate.predicate_id == "S1" and "element" not in inputs and binding.element_refs:
        ref = binding.element_refs[0]
        state = next((item for item in pair.model.states if item.ref == ref), None)
        event = next((item for item in pair.model.events if item.ref == ref), None)
        inputs["element"] = state.name if state else event.name if event else ref
        inputs.setdefault("kind", "state" if state else "event")
    return candidate.model_copy(update={"predicate_inputs": inputs})


def _endpoint_stem(value: Any) -> str:
    """Normalize a mapped source path to the owned parser's declaration stem."""

    text = str(value or "").strip()
    if text.startswith("@initial:"):
        text = "[*]"
    text = text.lstrip("!")
    if text.startswith("state:"):
        text = text[len("state:") :]
    return text.rsplit(".", 1)[-1]


def _model_ref_for_state(pair: PairInput, value: Any) -> str | None:
    stem = _endpoint_stem(value)
    matches = [
        state.ref
        for state in pair.model.states
        if state.name == stem or state.display_name == stem
    ]
    return matches[0] if len(matches) == 1 else None


def _mapped_model_refs(pair: PairInput, candidate: CandidateIssue) -> list[str]:
    """Translate source-owned grounding refs through the published mapping contract.

    Grounding sees both author-source and closed-model context.  The LLM may
    therefore return a source identity in ``element_refs`` even when its
    predicate inputs identify the corresponding FCSTM element.  The working
    contract is the explicit mapping authority; this helper only resolves
    structured IDs and endpoint fields and never performs textual similarity.
    """

    artifact = pair.working_contract
    elements = artifact.payload.get("elements", []) if artifact else []
    records = [item for item in elements if isinstance(item, dict)]
    raw_refs = list(candidate.element_refs)
    raw_refs.extend(
        ref for ref in candidate.source_refs if ref.startswith("source:")
    )
    resolved: list[str] = []
    unresolved: list[str] = []
    for raw in raw_refs:
        if raw in pair.model.all_refs:
            if raw not in resolved:
                resolved.append(raw)
            continue
        matches = [
            item
            for item in records
            if item.get("element_id") == raw
            or raw in (item.get("source_refs") or [])
        ]
        mapped: list[str] = []
        for item in matches:
            metadata = item.get("metadata") or {}
            semantic = item.get("semantic_fields") or {}
            kind = str(item.get("kind") or "")
            if "transition" in kind:
                source = metadata.get("source") or semantic.get("source_endpoint")
                target = metadata.get("target") or semantic.get("target_endpoint")
                if source is not None and target is not None:
                    ref = resolve_transition_ref(
                        None,
                        pair.model,
                        source=str(source),
                        target=str(target),
                    )
                    if ref is not None:
                        mapped.append(ref)
            else:
                state_path = (
                    metadata.get("fcstm_path")
                    or semantic.get("fcstm_identifier")
                )
                ref = _model_ref_for_state(pair, state_path)
                if ref is not None:
                    mapped.append(ref)
                for model_ref in item.get("model_refs") or []:
                    ref = _model_ref_for_state(pair, model_ref)
                    if ref is not None:
                        mapped.append(ref)
        if mapped:
            for ref in mapped:
                if ref not in resolved:
                    resolved.append(ref)
        elif raw not in pair.model.all_refs:
            unresolved.append(raw)

    # Predicate inputs are authoritative for the typed check.  Binding itself
    # will validate their endpoint/element identity, so this list only fills
    # the missing model-ref side of a dual-source candidate.
    if not resolved:
        for key in ("element", "state", "event"):
            value = candidate.predicate_inputs.get(key)
            ref = _model_ref_for_state(pair, value)
            if ref is not None:
                resolved.append(ref)
    return [*resolved, *unresolved]


def _normalize_candidate_model_refs(pair: PairInput, candidate: CandidateIssue) -> CandidateIssue:
    refs = _mapped_model_refs(pair, candidate)
    return candidate.model_copy(update={"element_refs": refs})


def _prepare_candidate(
    pair: PairInput,
    candidate: CandidateIssue,
    round_index: int,
    index: int,
 ) -> dict[str, Any]:
    """Bind, compile, and execute once before the separate semantic D call."""

    obligation_id = f"{pair.pair_id}:r{round_index}:i{index}"
    candidate = _normalize_candidate_model_refs(pair, candidate)
    binding = bind_candidate(candidate, pair.model)
    candidate = _enrich_candidate(candidate, binding, pair)
    plan = compile_plan(
        candidate,
        binding,
        load_registry(),
        obligation_id=obligation_id,
        round_index=round_index,
        model=pair.model,
        model_hash=pair.hashes["fcstm"],
    )
    validate_plan(plan)
    try:
        receipt = run_backend(plan, pair.model, f"{obligation_id}:receipt")
    except Exception as exc:
        # Backend failures are execution uncertainty, not violations. Preserve
        # a structured receipt so the candidate remains auditable and W cannot
        # be promoted by an exception path.
        receipt = RawReceipt(
            receipt_id=f"{obligation_id}:receipt",
            backend=f"error:{plan.predicate_id or 'none'}",
            terminal_state="error",
            verdict="unknown",
            reason=f"The backend raised {type(exc).__name__}; the exception was downgraded to execution uncertainty, not a violation.",
            basis="backend exception downgraded to explicit execution uncertainty",
            run_metadata={"error_type": type(exc).__name__, "error_message": str(exc)},
        )
    attribution = build_source_attribution(
        pair_id=pair.pair_id,
        obligation_id=obligation_id,
        nl_path=pair.pair_dir / "nl.txt",
        model_path=pair.pair_dir / "fcstm.fcstm",
        model_hash=pair.hashes["fcstm"],
        plan_id=plan.plan_id,
        receipt_id=receipt.receipt_id,
    )
    attribution["input_context"] = {
        "manifest_hash": pair.context_manifest.manifest_hash if pair.context_manifest else None,
        "artifact_hashes": dict(pair.hashes),
        "versions": {
            "model_parser": pair.model.algorithm_version,
            "inspection_equivalent": pair.inspection_facts.algorithm_version if pair.inspection_facts else None,
            "verify": pair.verify_facts.algorithm_version if pair.verify_facts else None,
            "smt": pair.smt_facts.algorithm_version if pair.smt_facts else None,
        },
        "reason": "The candidate receipt carries the same input closure identity used by method and grounding.",
        "basis": "pair context manifest and deterministic fact model versions",
    }
    return {
        "obligation_id": obligation_id,
        "candidate": candidate,
        "binding": binding,
        "plan": plan,
        "receipt": receipt,
        "source_attribution": attribution,
    }


def _deterministic_candidate(
    pair: PairInput,
    candidate: CandidateIssue,
    round_index: int,
    index: int,
    retry_records: list[dict[str, Any]],
    *,
    semantic_adjudication: SemanticAdjudication | None = None,
    prepared: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    prepared = prepared or _prepare_candidate(pair, candidate, round_index, index)
    candidate = prepared["candidate"]
    binding = prepared["binding"]
    plan = prepared["plan"]
    receipt = prepared["receipt"]
    attribution = prepared["source_attribution"]
    obligation_id = prepared["obligation_id"]
    record = build_evidence_record(
        pair=pair,
        obligation_id=obligation_id,
        candidate=candidate,
        binding=binding,
        plan=plan,
        receipt=receipt,
        source_attribution=attribution,
        retry_records=retry_records,
        semantic_adjudication=semantic_adjudication,
    )
    record.update(
        {
            "issue_id": f"{pair.pair_id}:r{round_index}:issue:{index}",
            "title": candidate.title,
            "requirement_quote": candidate.requirement_quote,
            "predicate_inputs": candidate.predicate_inputs,
            "element_refs": list(candidate.element_refs),
            "source_refs": list(candidate.source_refs),
            "expected": candidate.expected,
            "observed": candidate.observed,
            "strongest_rebuttal": candidate.strongest_rebuttal,
            "candidate_reason": candidate.reason,
            "candidate_basis": candidate.basis,
        }
    )
    # A completed positive predicate result is evidence against the candidate's
    # alleged defect. W1 has no executable result, so a precise D1/D2 candidate
    # remains a legal semantic issue.
    record["issue_emitted"] = bool(
        record["d_level"] in {"D1", "D2"}
        and (
            record["witness_level"] == "W1"
            or (record["witness_level"] == "W2" and receipt.verdict == "false")
        )
    )
    if record["witness_level"] == "W2":
        record["audit_bundle"]["issue_emitted"] = record["issue_emitted"]
        record["audit_bundle"] = validate_and_hash_w2_audit_bundle(
            record["audit_bundle"]
        )
    return record, record if record["issue_emitted"] else None


def _fallback_method(pair: PairInput, round_index: int, reason: str) -> MethodResponse:
    fallback = fallback_candidates(pair, round_index)
    return fallback.model_copy(
        update={
            "reason": "The provider or schema response was unavailable; deterministic input facts were preserved.",
            "basis": "The provider/runtime diagnostic is stored in llm_call and cell errors; no ledger or judge data was read.",
        }
    )


def _method_cell(
    *,
    pair: PairInput,
    round_index: int,
    runtime: PublicStructuredRuntime,
    previous: list[dict[str, Any]],
    output_root: Path,
    run_identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if pair.context_manifest is None or pair.exact_source_inventory is None:
        raise ValueError("method cell requires the complete v27-equivalent input closure")
    run_identity = run_identity or {
        "run_id": "0" * 32,
        "run_contract_hash": "sha256:" + "0" * 64,
        "source_provenance": _source_provenance(),
    }
    expected_input_hash = run_identity.get("pair_input_hashes", {}).get(pair.pair_id)
    if expected_input_hash is not None and expected_input_hash != pair.context_manifest.manifest_hash:
        raise RuntimeError(
            f"pair {pair.pair_id} input manifest changed after run identity was frozen"
        )
    stage_receipts: list[dict[str, Any]] = []
    stage_outputs: dict[str, Any] = {}
    all_outcomes: list[StructuredCallOutcome[Any]] = []
    all_errors: list[dict[str, Any]] = []
    prepare_output = {
        "pair_id": pair.pair_id,
        "manifest": pair.context_manifest.model_dump(mode="json"),
        "artifact_hashes": dict(pair.hashes),
        "source_roles": {
            "plantuml": "author_source_localization",
            "canonical_source_ir": "author_source_localization",
            "fcstm": "closed_model_execution",
            "inspection_facts": "deterministic_inventory_and_validation_facts",
            "working_contract": "mapping_and_eligibility_contract",
            "source_trace": "source_attribution",
            "verify_facts": "deterministic_finite_verification_context",
            "smt_facts": "normalized_formal_input_context_not_solver_result",
        },
        "reason": "The complete method input closure was prepared before contract extraction.",
        "basis": "context manifest, artifact hashes, and explicit source-role separation",
    }
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:prepare",
            stage_name="prepare",
            status="completed",
            artifact_roles=tuple(item.role for item in pair.context_manifest.artifacts),
            output=prepare_output,
            reason=prepare_output["reason"],
            basis=prepare_output["basis"],
        )
    )

    contract_prompt = build_contract_prompt(pair, round_index, previous)
    contract_outcome: StructuredCallOutcome[NLContractResponse] = runtime.call(
        kind="nl_contract_extraction",
        schema=NLContractResponse,
        system_prompt=CONTRACT_SYSTEM_PROMPT,
        prompt=contract_prompt,
        artifact_id=f"method/{pair.pair_id}/round-{round_index}/contract",
    )
    all_outcomes.append(contract_outcome)
    contract_response = contract_outcome.response if contract_outcome.succeeded else fallback_contracts(
        pair,
        str(contract_outcome.result.get("error", "structured contract output unavailable")),
    )
    stage_outputs["nl_contract_extraction"] = contract_response.model_dump(mode="json")
    if not contract_outcome.succeeded:
        all_errors.append(
            {
                "stage": "nl_contract_extraction",
                "error": contract_outcome.result.get("error", "structured contract output unavailable"),
                "reason": "Contract provider/schema failure was downgraded to a deterministic receipt.",
                "basis": "public structured runtime outcome and numbered NL fallback",
            }
        )
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:nl-contract",
            stage_name="nl_contract_extraction",
            status="completed" if contract_outcome.succeeded else "completed_with_diagnostics",
            artifact_roles=("natural_language", "working_contract", "source_trace"),
            output=contract_response,
            outcome=contract_outcome,
            reason=contract_response.reason,
            basis=contract_response.basis,
        )
    )

    source_prompt = build_grounding_prompt(
        pair,
        branch="source",
        round_index=round_index,
        contracts=contract_response,
        previous=previous,
    )
    model_prompt = build_grounding_prompt(
        pair,
        branch="model",
        round_index=round_index,
        contracts=contract_response,
        previous=previous,
    )

    def call_grounding(
        branch: Literal["source", "model"],
        prompt: str,
    ) -> StructuredCallOutcome[GroundingResponse]:
        return runtime.call(
            kind=f"{branch}_grounding",
            schema=GroundingResponse,
            system_prompt=(
                SOURCE_GROUNDING_SYSTEM_PROMPT
                if branch == "source"
                else MODEL_GROUNDING_SYSTEM_PROMPT
            ),
            prompt=prompt,
            artifact_id=f"method/{pair.pair_id}/round-{round_index}/{branch}-grounding",
        )

    # The six pair workers already provide process-level parallelism. Keep the
    # two calls sequential inside one PublicStructuredRuntime so the shared
    # AgentApp/LangGraph adapter retains its main-thread 30s first-byte and
    # 120s total deadline semantics; thread fanout previously caused
    # ``Event loop is closed`` non-provider failures.
    source_outcome = call_grounding("source", source_prompt)
    model_outcome = call_grounding("model", model_prompt)
    all_outcomes.extend([source_outcome, model_outcome])
    source_response = source_outcome.response if source_outcome.succeeded else fallback_grounding(
        pair,
        branch="source",
        contracts=contract_response,
        reason=str(source_outcome.result.get("error", "source grounding output unavailable")),
    )
    stage_outputs["source_grounding"] = source_response.model_dump(mode="json")
    if not source_outcome.succeeded:
        all_errors.append(
            {
                "stage": "source_grounding",
                "error": source_outcome.result.get("error", "source grounding output unavailable"),
                "reason": "Source grounding provider/schema failure was downgraded to a deterministic candidate receipt.",
                "basis": "public structured runtime outcome and source-role fallback",
            }
        )
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:source-grounding",
            stage_name="source_grounding",
            status="completed" if source_outcome.succeeded else "completed_with_diagnostics",
            artifact_roles=("natural_language", "plantuml_source", "canonical_source_ir", "source_inventory", "working_contract", "source_trace"),
            output=source_response,
            outcome=source_outcome,
            reason=source_response.reason,
            basis=source_response.basis,
        )
    )

    model_response = model_outcome.response if model_outcome.succeeded else fallback_grounding(
        pair,
        branch="model",
        contracts=contract_response,
        reason=str(model_outcome.result.get("error", "model grounding output unavailable")),
    )
    stage_outputs["model_grounding"] = model_response.model_dump(mode="json")
    if not model_outcome.succeeded:
        all_errors.append(
            {
                "stage": "model_grounding",
                "error": model_outcome.result.get("error", "model grounding output unavailable"),
                "reason": "Model grounding provider/schema failure was downgraded to a deterministic candidate receipt.",
                "basis": "public structured runtime outcome and closed-model fallback",
            }
        )
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:model-grounding",
            stage_name="model_grounding",
            status="completed" if model_outcome.succeeded else "completed_with_diagnostics",
            artifact_roles=("natural_language", "fcstm_model", "reference_inspection_facts", "inspection_equivalent_facts", "verify_facts", "smt_facts", "working_contract"),
            output=model_response,
            outcome=model_outcome,
            reason=model_response.reason,
            basis=model_response.basis,
        )
    )

    response = assemble_method_response(
        source_response,
        model_response,
        reason="The method merged two complementary grounding branches after NL contract extraction; typed semantic D is adjudicated separately and W remains deterministic downstream output.",
        basis="source-grounding and closed-model-grounding responses over the same context manifest",
    )
    candidates = response.issues
    records: list[dict[str, Any]] = []
    release: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = list(all_errors)
    prepared_candidates: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        try:
            prepared = _prepare_candidate(pair, candidate, round_index, index)
            prepared_candidates.append(prepared)
            stage_receipts.extend(
                [
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:i{index}:binding",
                        stage_name="exact_binding",
                        status="completed",
                        artifact_roles=("natural_language", "fcstm_model", "source_inventory", "working_contract"),
                        output=prepared["binding"],
                        reason=prepared["binding"].reason,
                        basis=prepared["binding"].basis,
                    ),
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:i{index}:compile",
                        stage_name="predicate_compilation",
                        status="completed",
                        artifact_roles=("fcstm_model", "inspection_equivalent_facts", "verify_facts", "smt_facts", "predicate_registry"),
                        output=prepared["plan"],
                        reason=prepared["plan"].reason,
                        basis=prepared["plan"].basis,
                    ),
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:i{index}:execute",
                        stage_name="backend_execution",
                        status="completed" if prepared["receipt"].terminal_state in {"completed", "unsupported", "unknown"} else "completed_with_diagnostics",
                        artifact_roles=("fcstm_model", "verify_facts", "smt_facts"),
                        output=prepared["receipt"],
                        reason=prepared["receipt"].reason,
                        basis=prepared["receipt"].basis,
                    )
                ]
            )
        except Exception as exc:  # preserve a cell-level diagnostic instead of losing a candidate
            errors.append({"candidate_index": index, "error_type": type(exc).__name__, "message": str(exc), "reason": "Candidate processing failed; the cell remains readable.", "basis": "Candidate-level diagnostic preservation."})
    if not prepared_candidates:
        # A valid method cell always has a deterministic auditable output, even
        # when the provider returns an empty list or the candidate schema fails.
        candidate = fallback_candidates(pair, round_index).issues[0]
        try:
            prepared = _prepare_candidate(pair, candidate, round_index, 0)
            prepared_candidates.append(prepared)
            stage_receipts.extend(
                [
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:fallback:binding",
                        stage_name="exact_binding",
                        status="completed",
                        artifact_roles=("natural_language", "fcstm_model", "source_inventory", "working_contract"),
                        output=prepared["binding"],
                        reason=prepared["binding"].reason,
                        basis=prepared["binding"].basis,
                    ),
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:fallback:compile",
                        stage_name="predicate_compilation",
                        status="completed",
                        artifact_roles=("fcstm_model", "inspection_equivalent_facts", "verify_facts", "smt_facts", "predicate_registry"),
                        output=prepared["plan"],
                        reason=prepared["plan"].reason,
                        basis=prepared["plan"].basis,
                    ),
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:fallback:execute",
                        stage_name="backend_execution",
                        status="completed" if prepared["receipt"].terminal_state in {"completed", "unsupported", "unknown"} else "completed_with_diagnostics",
                        artifact_roles=("fcstm_model", "verify_facts", "smt_facts"),
                        output=prepared["receipt"],
                        reason=prepared["receipt"].reason,
                        basis=prepared["receipt"].basis,
                    ),
                ]
            )
        except Exception as exc:
            errors.append({"candidate_index": 0, "error_type": type(exc).__name__, "message": str(exc), "reason": "Deterministic fallback processing failed.", "basis": "Fallback diagnostic preservation."})

    d_prompt = ""
    d_correction_prompt = ""
    d_outcome: StructuredCallOutcome[DAdjudicationResponse] | None = None
    d_stage_outcome: StructuredCallOutcome[DAdjudicationResponse] | None = None
    d_response = fallback_d_adjudication(
        [item["obligation_id"] for item in prepared_candidates],
        "no prepared candidate dossier",
    )
    decisions: dict[str, SemanticAdjudication] = {}
    if prepared_candidates:
        dossiers = [
            {
                "obligation_id": item["obligation_id"],
                "candidate": item["candidate"].model_dump(mode="json"),
                "binding": item["binding"].model_dump(mode="json"),
                "plan": item["plan"].to_dict(),
                "receipt": item["receipt"].to_dict(),
                "source_attribution": item["source_attribution"],
                "reason": "The dossier contains exact method outputs and formal execution facts for semantic adjudication.",
                "basis": "prepared candidate, exact binding, frozen predicate plan, and backend receipt",
            }
            for item in prepared_candidates
        ]
        d_prompt = build_d_adjudication_prompt(pair, dossiers)
        d_outcome = runtime.call(
            kind="d_adjudication",
            schema=DAdjudicationResponse,
            system_prompt=D_SYSTEM_PROMPT,
            prompt=d_prompt,
            artifact_id=f"method/{pair.pair_id}/round-{round_index}/d-adjudication",
        )
        all_outcomes.append(d_outcome)
        d_stage_outcome = d_outcome
        d_response = d_outcome.response if d_outcome.succeeded else fallback_d_adjudication(
            [item["obligation_id"] for item in prepared_candidates],
            str(d_outcome.result.get("error", "D adjudication output unavailable")),
        )
        if not d_outcome.succeeded:
            errors.append(
                {
                    "stage": "d_adjudication",
                    "error": d_outcome.result.get("error", "D adjudication output unavailable"),
                    "reason": "Typed semantic D failure was downgraded to explicit unresolved decisions.",
                    "basis": "public structured runtime outcome and no-silent-drop D fallback",
                }
            )
        expected_ids = [item["obligation_id"] for item in prepared_candidates]
        expected_id_set = set(expected_ids)
        def coverage(
            response: DAdjudicationResponse,
        ) -> tuple[list[SemanticAdjudication], list[str], list[str], list[str]]:
            supplied_decisions = [
                decision
                for decision in response.decisions
                if decision.obligation_id in expected_id_set
            ]
            unique: list[SemanticAdjudication] = []
            duplicate: list[str] = []
            for decision in supplied_decisions:
                if any(item.obligation_id == decision.obligation_id for item in unique):
                    duplicate.append(decision.obligation_id)
                    continue
                unique.append(decision)
            supplied_by_id = {decision.obligation_id: decision for decision in unique}
            missing = [
                obligation_id
                for obligation_id in expected_ids
                if obligation_id not in supplied_by_id
            ]
            extra = [
                decision.obligation_id
                for decision in response.decisions
                if decision.obligation_id not in expected_id_set
            ]
            return unique, missing, extra, duplicate

        unique_supplied, missing_ids, extra_ids, duplicate_ids = coverage(d_response)
        if missing_ids and d_outcome.succeeded:
            d_correction_prompt = build_d_correction_prompt(
                pair,
                dossiers,
                missing_ids=missing_ids,
                duplicate_ids=duplicate_ids,
                extra_ids=extra_ids,
            )
            correction_outcome: StructuredCallOutcome[DAdjudicationResponse] = runtime.call(
                kind="d_adjudication_correction",
                schema=DAdjudicationResponse,
                system_prompt=D_SYSTEM_PROMPT,
                prompt=d_correction_prompt,
                artifact_id=f"method/{pair.pair_id}/round-{round_index}/d-adjudication-correction",
            )
            all_outcomes.append(correction_outcome)
            d_stage_outcome = correction_outcome
            if correction_outcome.succeeded:
                d_response = d_response.model_copy(
                    update={
                        "decisions": [
                            *unique_supplied,
                            *correction_outcome.response.decisions,
                        ]
                    }
                )
                unique_supplied, missing_ids, extra_ids, duplicate_ids = coverage(d_response)
            else:
                errors.append(
                    {
                        "stage": "d_adjudication_correction",
                        "error": correction_outcome.result.get(
                            "error",
                            "D correction output unavailable",
                        ),
                        "reason": "The D coverage correction failed; missing obligations remain unresolved.",
                        "basis": "in-node structured contract correction and public runtime outcome",
                    }
                )
        if missing_ids or extra_ids or duplicate_ids:
            diagnostics: list[str] = []
            if missing_ids:
                diagnostics.append(f"missing={missing_ids}")
            if extra_ids:
                diagnostics.append(f"extra={extra_ids}")
            if duplicate_ids:
                diagnostics.append(f"duplicate={duplicate_ids}")
            errors.append(
                {
                    "stage": "d_adjudication",
                    "error": "; ".join(diagnostics),
                    "reason": "D structured output did not cover the exact obligation set; missing units were retained as unresolved.",
                    "basis": "deterministic obligation-ID coverage and uniqueness check",
                }
            )
            missing_response = fallback_d_adjudication(
                missing_ids,
                "D structured output coverage check",
            )
            d_response = d_response.model_copy(
                update={"decisions": unique_supplied + missing_response.decisions}
            )
            unique_supplied, _, _, _ = coverage(d_response)
        decisions = {decision.obligation_id: decision for decision in unique_supplied}
        stage_outputs["d_adjudication"] = d_response.model_dump(mode="json")
        stage_receipts.append(
            _stage_receipt(
                pair=pair,
                stage_id=f"{pair.pair_id}:r{round_index}:d-adjudication",
                stage_name="d_adjudication",
                status="completed" if d_stage_outcome is not None and d_stage_outcome.succeeded and not any(
                    item.get("stage") in {"d_adjudication", "d_adjudication_correction"}
                    for item in errors
                ) else "completed_with_diagnostics",
                artifact_roles=("natural_language", "plantuml_source", "canonical_source_ir", "source_inventory", "fcstm_model", "working_contract", "source_trace", "predicate_registry"),
                output=d_response,
                outcome=d_stage_outcome,
                reason=d_response.reason,
                basis=d_response.basis,
            )
        )
    retry_records = [
        {"stage": outcome.kind, **attempt}
        for outcome in all_outcomes
        for attempt in outcome.attempts
    ]
    for index, prepared in enumerate(prepared_candidates):
        try:
            record, emitted = _deterministic_candidate(
                pair,
                prepared["candidate"],
                round_index,
                index,
                retry_records,
                semantic_adjudication=decisions.get(prepared["obligation_id"]),
                prepared=prepared,
            )
            records.append(record)
            if emitted is not None:
                release.append(emitted)
            stage_receipts.extend(
                [
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:i{index}:w",
                        stage_name="w_publication",
                        status="completed",
                        artifact_roles=("fcstm_model", "predicate_registry", "verify_facts"),
                        output={"witness_level": record["witness_level"], "issue_emitted": record["issue_emitted"]},
                        reason="W level and issue publication were computed by the deterministic evidence state machine.",
                        basis="binding, plan support, backend terminal state, receipt verdict, and D adjudication",
                    ),
                ]
            )
            if record.get("audit_bundle") is not None:
                audit_path = output_root / "audit_bundles" / f"{record['issue_id']}.json"
                write_json(audit_path, record["audit_bundle"])
                record["audit_bundle_path"] = str(audit_path)
        except Exception as exc:  # preserve a cell-level diagnostic instead of losing a candidate
            errors.append({"candidate_index": index, "error_type": type(exc).__name__, "message": str(exc), "reason": "Candidate publication failed; the cell remains readable.", "basis": "Candidate-level diagnostic preservation."})
    prompt_hash = _hash_json(
        {
            "contract": contract_prompt,
            "source_grounding": source_prompt,
            "model_grounding": model_prompt,
            "d_adjudication": d_prompt,
            "d_adjudication_correction": d_correction_prompt,
        }
    )
    llm_call = _aggregate_outcomes(all_outcomes)
    real_llm = bool(all_outcomes) and all(outcome.real_llm for outcome in all_outcomes)
    provider_or_schema_failure = any(not outcome.succeeded for outcome in all_outcomes)
    eligible = bool(records and real_llm and not provider_or_schema_failure)
    eligibility_reasons = (
        ["real_structured_stage_outputs", "method_receipt_complete"]
        if eligible
        else [
            *([] if records else ["no_evidence_record"]),
            *([] if real_llm else ["fixture_or_non_provider_output"]),
            *([] if not provider_or_schema_failure else ["provider_or_schema_stage_failure"]),
        ]
    )
    cell = {
        "schema": METHOD_CELL_SCHEMA,
        "run_id": run_identity["run_id"],
        "run_contract_hash": run_identity["run_contract_hash"],
        "source_provenance": run_identity["source_provenance"],
        "pair_id": pair.pair_id,
        "pair_input_hash": pair.context_manifest.manifest_hash,
        "round": round_index,
        "status": (
            "completed"
            if records and all_outcomes and all(item.succeeded for item in all_outcomes) and not errors
            else "completed_with_diagnostics"
            if records
            else "failed_with_receipt"
        ),
        "prompt_hash": prompt_hash,
        "context_manifest": pair.context_manifest.model_dump(mode="json"),
        "input_hashes": dict(pair.hashes),
        "stage_outputs": stage_outputs,
        "stage_receipts": stage_receipts,
        "model_output": response.model_dump(mode="json"),
        "llm_calls": [outcome.to_dict() for outcome in all_outcomes],
        "llm_call": llm_call,
        "eligible": eligible,
        "eligibility_reasons": eligibility_reasons,
        "evidence_records": records,
        "report_issue_clusters": release,
        "errors": errors,
        "reason": response.reason,
        "basis": response.basis,
    }
    validated = MethodCellReceipt.model_validate(cell).model_dump(mode="json")
    write_json(
        output_root / "method" / pair.pair_id / f"round-{round_index}.json",
        validated,
    )
    return validated


def _judge_ledger_projection(item: dict[str, Any]) -> dict[str, Any]:
    """Project one frozen ledger row to the independent judge surface."""

    return {
        key: item[key]
        for key in (
            "id",
            "pair",
            "D",
            "D_basis",
            "summary",
            "detail",
            "axes",
        )
        if key in item
    }


def _judge_issue_projection(issue: dict[str, Any]) -> dict[str, Any]:
    """Project one release issue without copying its complete audit bundle."""

    plan = issue.get("plan") or {}
    receipt = issue.get("receipt") or {}
    binding = issue.get("binding") or {}
    attribution = issue.get("source_attribution") or {}
    audit = issue.get("audit_bundle") or {}
    return {
        key: issue[key]
        for key in (
            "issue_id",
            "title",
            "requirement_quote",
            "predicate_id",
            "predicate_inputs",
            "element_refs",
            "source_refs",
            "expected",
            "observed",
            "strongest_rebuttal",
            "d_level",
            "witness_level",
            "coverage_class",
            "reason",
            "basis",
            "candidate_reason",
            "candidate_basis",
        )
        if key in issue
    } | {
        "binding": {
            key: binding[key]
            for key in ("precise", "element_refs", "source_refs", "reason", "basis")
            if key in binding
        },
        "predicate_plan": {
            key: plan[key]
            for key in (
                "plan_id",
                "predicate_id",
                "predicate_name",
                "family",
                "semantics",
                "inputs",
                "soundness_fragment",
                "supported",
                "binding_complete",
                "missing_inputs",
                "source_audit_status",
                "source_gate_passed",
                "reason",
                "basis",
            )
            if key in plan
        },
        "backend_receipt": {
            key: receipt[key]
            for key in (
                "receipt_id",
                "backend",
                "terminal_state",
                "verdict",
                "counterexample",
                "trace",
                "reason",
                "basis",
            )
            if key in receipt
        },
        "source_attribution": {
            key: attribution[key]
            for key in ("requirement", "source", "model", "plan", "backend", "input_context")
            if key in attribution
        },
        "audit_reference": {
            "audit_hash": audit.get("audit_hash"),
            "path": issue.get("audit_bundle_path"),
            "reason": "The complete W2 audit bundle remains on disk; the judge receives its identity only.",
            "basis": "judge-release-projection.v3",
        },
        "reason": issue.get("reason") or issue.get("candidate_reason") or "The release issue carries a deterministic method rationale.",
        "basis": issue.get("basis") or issue.get("candidate_basis") or "method release receipt projection",
    }


def _judge_stage_projection(cell: dict[str, Any]) -> list[dict[str, Any]]:
    """Keep stage identity and budget facts while excluding repeated payloads."""

    return [
        {
            "stage_name": item.get("stage_name"),
            "stage_id": item.get("stage_id"),
            "status": item.get("status"),
            "input_manifest_hash": item.get("input_manifest_hash"),
            "output_hash": item.get("output_hash"),
            "context_budget": item.get("context_budget"),
            "reason": item.get("reason"),
            "basis": item.get("basis"),
        }
        for item in cell.get("stage_receipts", [])
    ]


def _normalize_judge_shape(
    response: JudgeResponse,
    ledger_items: list[dict[str, Any]],
    release: list[dict[str, Any]],
    rounds: int,
) -> JudgeResponse:
    """Normalize exact-ID consistency fields without making semantic decisions."""

    expected_release = {str(item["issue_id"]) for item in release}

    def issue_round(issue_id: str) -> int | None:
        parts = issue_id.split(":")
        if len(parts) != 4 or parts[2] != "issue" or not parts[1].startswith("r"):
            return None
        try:
            return int(parts[1][1:])
        except ValueError:
            return None

    normalized_ledger = [
        assessment.model_copy(
            update={
                f"hit_r{round_index}": bool(
                    any(
                        issue_id in expected_release and issue_round(issue_id) == round_index
                        for issue_id in assessment.matched_issue_ids
                    )
                )
                if round_index <= rounds
                else False
                for round_index in range(1, 4)
            }
        )
        for assessment in response.ledger_assessments
    ]
    normalized_release = [
        assessment.model_copy(
            update={
                "is_false_positive": not bool(assessment.accounted_ledger_ids),
            }
        )
        for assessment in response.release_assessments
    ]
    return response.model_copy(
        update={
            "ledger_assessments": normalized_ledger,
            "release_assessments": normalized_release,
        }
    )


def _partitioned_judge(
    *,
    pair: PairInput,
    ledger_items: list[dict[str, Any]],
    release: list[dict[str, Any]],
    method_rounds: list[dict[str, Any]],
    runtime: PublicStructuredRuntime,
) -> tuple[JudgeResponse | None, list[StructuredCallOutcome[Any]], list[dict[str, Any]]]:
    """Judge release chunks independently when the compact pair prompt is too large.

    Each call still sees the complete frozen ledger, but only a bounded release
    subset. Exact IDs are unioned mechanically after all chunks; no missing
    relation is converted to a miss or false positive.
    """

    outcomes: list[StructuredCallOutcome[Any]] = []
    errors: list[dict[str, Any]] = []
    chunks = [
        release[index:index + JUDGE_PARTITION_RELEASE_SIZE]
        for index in range(0, len(release), JUDGE_PARTITION_RELEASE_SIZE)
    ]
    chunk_responses: list[tuple[list[dict[str, Any]], JudgeResponse]] = []
    for chunk_index, chunk in enumerate(chunks):
        chunk_ids = {str(item.get("issue_id")) for item in chunk}
        chunk_rounds = [
            {
                **cell,
                "report_issue_clusters": [
                    issue
                    for issue in cell.get("report_issue_clusters", [])
                    if str(issue.get("issue_id")) in chunk_ids
                ],
            }
            for cell in method_rounds
        ]
        prompt = _judge_prompt(pair, ledger_items, chunk_rounds)
        if (len(prompt) + 3) // 4 > JUDGE_PROMPT_TOKEN_BUDGET:
            errors.append(
                {
                    "chunk": chunk_index,
                    "error": "judge_partition_context_budget_exceeded",
                    "reason": "A compact judge partition still exceeds the configured prompt budget; no provider call was attempted.",
                    "basis": f"estimated_tokens={(len(prompt) + 3) // 4}; budget={JUDGE_PROMPT_TOKEN_BUDGET}",
                }
            )
            continue
        outcome = runtime.call(
            kind="judge_partition",
            schema=JudgeResponse,
            system_prompt=JUDGE_SYSTEM_PROMPT,
            prompt=prompt,
            artifact_id=f"judge/{pair.pair_id}/partition-{chunk_index}",
        )
        outcomes.append(outcome)
        response = outcome.response if outcome.succeeded else None
        if response is not None:
            response = _normalize_judge_shape(response, ledger_items, chunk, len(method_rounds))
            shape_errors = _judge_shape_errors(response, ledger_items, chunk, len(method_rounds))
        else:
            shape_errors = ["judge partition output unavailable"]
        if response is None or shape_errors:
            # A partition may be semantically useful while violating only the
            # exact-ID response shape (duplicate ledger rows or a copied issue
            # ID from another round). Give the same judge one targeted repair
            # with the exact allowed IDs before falling back to atomic
            # relations. This bounds judge calls at two per partition and
            # avoids the old ledger x release explosion.
            correction = runtime.call(
                kind="judge_partition_correction",
                schema=JudgeResponse,
                system_prompt=JUDGE_SYSTEM_PROMPT,
                prompt=_judge_partition_correction_prompt(
                    pair=pair,
                    ledger_items=ledger_items,
                    chunk=chunk,
                    method_rounds=chunk_rounds,
                    errors=shape_errors,
                ),
                artifact_id=f"judge/{pair.pair_id}/partition-{chunk_index}/shape-correction",
            )
            outcomes.append(correction)
            if correction.succeeded:
                response = _normalize_judge_shape(
                    correction.response,
                    ledger_items,
                    chunk,
                    len(method_rounds),
                )
                shape_errors = _judge_shape_errors(
                    response,
                    ledger_items,
                    chunk,
                    len(method_rounds),
                )
            else:
                shape_errors.append("partition shape correction output unavailable")
        if response is None or shape_errors:
            errors.append(
                {
                    "chunk": chunk_index,
                    "error": "; ".join(shape_errors),
                    "reason": "A partition and its targeted exact-ID correction did not close; relations remain unresolved before any bounded fallback.",
                    "basis": "partitioned judge exact-ID coverage contract and targeted correction receipt",
                }
            )
            continue
        chunk_responses.append((chunk, response))

    if errors or len(chunk_responses) != len(chunks):
        return None, outcomes, errors

    ledger_by_id: dict[str, list[LedgerAssessment]] = defaultdict(list)
    release_by_id: dict[str, ReleaseAssessment] = {}
    for _, response in chunk_responses:
        for assessment in response.ledger_assessments:
            ledger_by_id[assessment.ledger_id].append(assessment)
        for assessment in response.release_assessments:
            release_by_id[assessment.issue_id] = assessment
    ledger_assessments = []
    for item in ledger_items:
        rows = ledger_by_id.get(str(item["id"]), [])
        matched_ids = list(dict.fromkeys(
            issue_id for row in rows for issue_id in row.matched_issue_ids
        ))
        ledger_assessments.append(
            LedgerAssessment(
                ledger_id=str(item["id"]),
                hit_r1=any(issue_id.split(":")[1:2] == ["r1"] for issue_id in matched_ids),
                hit_r2=any(issue_id.split(":")[1:2] == ["r2"] for issue_id in matched_ids),
                hit_r3=any(issue_id.split(":")[1:2] == ["r3"] for issue_id in matched_ids),
                matched_issue_ids=matched_ids,
                reason="; ".join(row.reason for row in rows) or "No supplied partition reported a matching release issue.",
                basis="partitioned pair-wide judge responses unioned by exact ledger and issue IDs",
            )
        )
    return (
        JudgeResponse(
            ledger_assessments=ledger_assessments,
            release_assessments=[release_by_id[str(item["issue_id"])] for item in release],
            reason="The compact pair-wide judge was partitioned by release issue count before provider execution.",
            basis="bounded release partitions, complete frozen ledger per partition, and exact-ID aggregation",
        ),
        outcomes,
        [],
    )


def _judge_prompt(
    pair: PairInput,
    ledger_items: list[dict[str, Any]],
    method_rounds: list[dict[str, Any]],
    required_release_ids: Sequence[str] | None = None,
) -> str:
    """Build the independent pair-wide judge prompt from release issues only."""

    compact_rounds: list[dict[str, Any]] = []
    for cell in method_rounds:
        compact_rounds.append(
            {
                "receipt_identity": {
                    "schema": cell.get("schema"),
                    "run_id": cell.get("run_id"),
                    "run_contract_hash": cell.get("run_contract_hash"),
                    "pair_id": cell.get("pair_id"),
                    "round": cell.get("round"),
                    "status": cell.get("status"),
                    "eligible": cell.get("eligible", False),
                    "eligibility_reasons": cell.get("eligibility_reasons", []),
                    "prompt_hash": cell.get("prompt_hash"),
                    "context_manifest_hash": (
                        cell.get("context_manifest", {}).get("manifest_hash")
                        if isinstance(cell.get("context_manifest"), dict)
                        else None
                    ),
                    "input_hashes": cell.get("input_hashes", {}),
                    "stage_receipts": _judge_stage_projection(cell),
                    "method_receipt_hash": _hash_json(cell),
                    "reason": cell.get("reason"),
                    "basis": cell.get("basis"),
                },
                "release_issue_clusters": [
                    _judge_issue_projection(issue)
                    for issue in cell.get("report_issue_clusters", [])
                ],
            }
        )
    required_release_ids = tuple(
        required_release_ids
        if required_release_ids is not None
        else [
            str(issue.get("issue_id"))
            for cell in method_rounds
            for issue in cell.get("report_issue_clusters", [])
        ]
    )
    return f"""Assess the supplied method rounds for frozen pair {pair.pair_id} as an independent judge.

Frozen ledger entries (the judge's only ground-truth answer source; method generation did not read them):
{json.dumps([_judge_ledger_projection(item) for item in ledger_items], ensure_ascii=False, sort_keys=True)}

Complete method receipt identities/stage receipts plus full D1/D2 release receipts for all supplied rounds (D0 is excluded):
{json.dumps(compact_rounds, ensure_ascii=False, sort_keys=True)}

The exact release issue ID set for this request is:
{json.dumps(list(required_release_ids), ensure_ascii=False)}
You must emit each of these release IDs exactly once. Do not emit any other
release ID, even if a similarly named issue appears in another round. Emit each
frozen ledger ID exactly once as well. The frozen ledger list is an array of
objects: emit exactly one ledger assessment for each supplied object. Do not
split one object into multiple assessments because its summary, detail, or
D_basis describes multiple defect aspects; those aspects remain one ledger
unit under its supplied ID.

A hit requires the same locus and the same property. Wording and evidence depth may differ. A broad
category, an opposite-direction claim, a passing mention, a complaint about a reference artifact, or
a bundle of unrelated issues is not a hit for the ledger item. Emit one ledger assessment for every
ledger_id with separate r1/r2/r3 decisions. Emit one release assessment for every release issue; set
is_false_positive=true only when no frozen ledger item can semantically account for it. Do not omit
units. Every assessment and the top-level response must have non-empty reason and basis fields. Do
not read baseline results, other pairs, historical judge examples, or files outside this input.
"""


def _judge_partition_correction_prompt(
    *,
    pair: PairInput,
    ledger_items: list[dict[str, Any]],
    chunk: list[dict[str, Any]],
    method_rounds: list[dict[str, Any]],
    errors: list[str],
) -> str:
    """Build a bounded exact-ID repair prompt for one judge partition."""

    required_release_ids = [str(item["issue_id"]) for item in chunk]
    return (
        _judge_prompt(
            pair,
            ledger_items,
            method_rounds,
            required_release_ids=required_release_ids,
        )
        + "\nThe previous partition response violated these deterministic shape checks:\n- "
        + "\n- ".join(errors)
        + "\nReturn a complete replacement. Copy IDs only from the exact lists above; do not repeat an ID. This is a shape repair, not permission to change the semantic matching rule. Every assessment still needs non-empty reason and basis.\n"
    )


ATOMIC_JUDGE_SYSTEM_PROMPT = """You are the independent semantic fallback judge for paper1 evidence_discovery. Decide only whether one supplied frozen ledger entry and one supplied D1/D2 release issue identify the same locus and the same property. Do not use keyword, substring, regex, edit-distance, embedding, identifier-shape, or other lexical proxies. Do not create issues or inspect other pairs. Return one Pydantic AtomicMatchDecision with non-empty reason and basis."""


def _read_ledger_for_pair(ledger_path: Path, pair_id: str) -> list[dict[str, Any]]:
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    items = data.get("items")
    if not isinstance(items, dict):
        raise ValueError("ledger.json items must be a mapping")
    return [dict(item) for item in items.values() if item.get("pair") == pair_id]


def _judge_shape_errors(
    response: JudgeResponse,
    ledger_items: list[dict[str, Any]],
    release: list[dict[str, Any]],
    rounds: int,
) -> list[str]:
    """Validate exact judge coverage and references without semantic guessing."""

    def issue_round(issue_id: str) -> int | None:
        parts = issue_id.split(":")
        if len(parts) != 4 or parts[2] != "issue" or not parts[1].startswith("r"):
            return None
        try:
            return int(parts[1][1:])
        except ValueError:
            return None

    errors: list[str] = []
    expected_ledger = {str(item["id"]) for item in ledger_items}
    expected_release = {str(item["issue_id"]) for item in release}
    ledger_ids = [item.ledger_id for item in response.ledger_assessments]
    release_ids = [item.issue_id for item in response.release_assessments]
    if set(ledger_ids) != expected_ledger or len(ledger_ids) != len(set(ledger_ids)):
        errors.append("ledger_assessments must contain each supplied ledger_id exactly once")
    if set(release_ids) != expected_release or len(release_ids) != len(set(release_ids)):
        errors.append("release_assessments must contain each supplied issue_id exactly once")
    for assessment in response.ledger_assessments:
        matched = set(assessment.matched_issue_ids)
        unknown = matched - expected_release
        if unknown:
            errors.append(f"{assessment.ledger_id} references unknown release IDs {sorted(unknown)}")
        for round_index in range(1, 4):
            round_ids = {
                issue_id
                for issue_id in matched
                if issue_round(issue_id) == round_index
            }
            hit = bool(getattr(assessment, f"hit_r{round_index}"))
            if round_index <= rounds and hit != bool(round_ids):
                errors.append(
                    f"{assessment.ledger_id}.hit_r{round_index} must agree with matched_issue_ids from that round"
                )
            if round_index > rounds and hit:
                errors.append(f"{assessment.ledger_id}.hit_r{round_index} is outside the supplied round count")
    for assessment in response.release_assessments:
        accounted = set(assessment.accounted_ledger_ids)
        unknown = accounted - expected_ledger
        if unknown:
            errors.append(f"{assessment.issue_id} references unknown ledger IDs {sorted(unknown)}")
        if assessment.is_false_positive != (not bool(accounted)):
            errors.append(
                f"{assessment.issue_id}.is_false_positive must equal whether accounted_ledger_ids is empty"
            )
    matched_relations = {
        (assessment.ledger_id, issue_id)
        for assessment in response.ledger_assessments
        for issue_id in assessment.matched_issue_ids
        if assessment.ledger_id in expected_ledger and issue_id in expected_release
    }
    accounted_relations = {
        (ledger_id, assessment.issue_id)
        for assessment in response.release_assessments
        for ledger_id in assessment.accounted_ledger_ids
        if ledger_id in expected_ledger and assessment.issue_id in expected_release
    }
    if matched_relations != accounted_relations:
        errors.append(
            "ledger matched_issue_ids and release accounted_ledger_ids must encode the same exact relation pairs"
        )
    return errors


def _judge_correction_prompt(
    pair: PairInput,
    ledger_items: list[dict[str, Any]],
    method_rounds: list[dict[str, Any]],
    errors: list[str],
) -> str:
    """Build a billed same-node correction prompt for judge shape failures."""

    return (
        _judge_prompt(pair, ledger_items, method_rounds)
        + "\nThe previous response violated these deterministic shape contracts:\n- "
        + "\n- ".join(errors)
        + "\nReturn a complete replacement response. This is schema/coverage correction, not a provider retry. Every supplied unit still requires a semantic reason and basis.\n"
    )


def _atomic_judge_prompt(
    *,
    pair_id: str,
    ledger_item: dict[str, Any],
    release_issue: dict[str, Any],
) -> str:
    """Build one blind ledger-to-release semantic relation prompt."""

    return f"""Frozen pair: {pair_id}

Frozen ledger entry (judge-only ground truth input):
{json.dumps(_judge_ledger_projection(ledger_item), ensure_ascii=False, sort_keys=True)}

One method D1/D2 release issue:
{json.dumps(_judge_issue_projection(release_issue), ensure_ascii=False, sort_keys=True)}

Set matches=true only for the same locus and same property. Explain the semantic relation in reason and identify the supplied facts in basis. Do not use baseline data, other pairs, or lexical matching.
"""


def _atomic_judge(
    *,
    pair: PairInput,
    ledger_items: list[dict[str, Any]],
    release: list[dict[str, Any]],
    runtime: PublicStructuredRuntime,
) -> tuple[JudgeResponse | None, list[StructuredCallOutcome[Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Recover a complete judge surface through independent atomic LLM relations."""

    outcomes: list[StructuredCallOutcome[Any]] = []
    relations: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    jobs = [
        (ledger_index, ledger_item, issue_index, issue)
        for ledger_index, ledger_item in enumerate(ledger_items)
        for issue_index, issue in enumerate(release)
    ]

    def call_relation(
        job: tuple[int, dict[str, Any], int, dict[str, Any]],
    ) -> StructuredCallOutcome[AtomicMatchDecision]:
        ledger_index, ledger_item, issue_index, issue = job
        return runtime.call(
            kind="judge_atomic_relation",
            schema=AtomicMatchDecision,
            system_prompt=ATOMIC_JUDGE_SYSTEM_PROMPT,
            prompt=_atomic_judge_prompt(
                pair_id=pair.pair_id,
                ledger_item=ledger_item,
                release_issue=issue,
            ),
            artifact_id=f"judge_atomic/{pair.pair_id}/ledger-{ledger_index}/issue-{issue_index}",
        )

    if jobs:
        with ThreadPoolExecutor(max_workers=min(4, len(jobs)), thread_name_prefix="judge-atomic") as executor:
            outcomes = list(executor.map(call_relation, jobs))
    for job, outcome in zip(jobs, outcomes):
        _, ledger_item, _, issue = job
        if not outcome.succeeded:
            errors.append(
                {
                    "ledger_id": ledger_item["id"],
                    "issue_id": issue["issue_id"],
                    "error": outcome.result.get("error", "atomic judge unavailable"),
                    "reason": "An atomic semantic relation failed after public provider retries; it remains unadjudicated rather than becoming a miss or FP.",
                    "basis": "public structured runtime terminal outcome",
                }
            )
            continue
        decision = outcome.response
        relations.append(
            {
                "ledger_id": ledger_item["id"],
                "issue_id": issue["issue_id"],
                **decision.model_dump(mode="json"),
            }
        )
    if errors:
        return None, outcomes, relations, errors

    matched_by_ledger: dict[str, list[dict[str, Any]]] = defaultdict(list)
    matched_by_issue: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in relations:
        if relation["matches"]:
            matched_by_ledger[relation["ledger_id"]].append(relation)
            matched_by_issue[relation["issue_id"]].append(relation)
    ledger_assessments: list[LedgerAssessment] = []
    for item in ledger_items:
        matched = matched_by_ledger[item["id"]]
        issue_ids = [relation["issue_id"] for relation in matched]
        ledger_assessments.append(
            LedgerAssessment(
                ledger_id=item["id"],
                hit_r1=any(":r1:" in issue_id for issue_id in issue_ids),
                hit_r2=any(":r2:" in issue_id for issue_id in issue_ids),
                hit_r3=any(":r3:" in issue_id for issue_id in issue_ids),
                matched_issue_ids=issue_ids,
                reason=(
                    "Atomic semantic relations found matching release issues: "
                    + "; ".join(relation["reason"] for relation in matched)
                    if matched
                    else "No supplied release issue had the same locus and property under the atomic semantic assessments."
                ),
                basis=(
                    "independent atomic LLM relation receipts"
                    if release
                    else "the supplied release set is exactly empty"
                ),
            )
        )
    release_assessments: list[ReleaseAssessment] = []
    for issue in release:
        matched = matched_by_issue[issue["issue_id"]]
        ledger_ids = [relation["ledger_id"] for relation in matched]
        release_assessments.append(
            ReleaseAssessment(
                issue_id=issue["issue_id"],
                accounted_ledger_ids=ledger_ids,
                is_false_positive=not ledger_ids,
                reason=(
                    "Atomic semantic relations matched ledger entries: "
                    + "; ".join(relation["reason"] for relation in matched)
                    if matched
                    else "No frozen ledger entry had the same locus and property under the atomic semantic assessments."
                ),
                basis="independent atomic LLM relation receipts",
            )
        )
    response = JudgeResponse(
        ledger_assessments=ledger_assessments,
        release_assessments=release_assessments,
        reason="Pair-wide judge shape did not close, so every required ledger-to-release relation was independently adjudicated and mechanically aggregated.",
        basis="complete atomic LLM semantic relation matrix plus exact ID aggregation",
    )
    return response, outcomes, relations, []


def _exact_empty_release_judgement(
    ledger_items: list[dict[str, Any]],
) -> JudgeResponse:
    """Close an empty release surface without inventing a semantic relation."""

    return JudgeResponse(
        ledger_assessments=[
            LedgerAssessment(
                ledger_id=item["id"],
                hit_r1=False,
                hit_r2=False,
                hit_r3=False,
                matched_issue_ids=[],
                reason="The complete supplied D1/D2 release surface is exactly empty, so no method issue can match this ledger entry.",
                basis="exact empty release issue ID set; no textual or semantic proxy was used",
            )
            for item in ledger_items
        ],
        release_assessments=[],
        reason="The independent judge boundary mechanically closed an exactly empty release surface without creating a missing assessment or false positive.",
        basis="complete method receipt identities and the exact empty D1/D2 release issue set",
    )


def _judge_pair(
    *,
    pair: PairInput,
    method_rounds: list[dict[str, Any]],
    ledger_path: Path,
    runtime: PublicStructuredRuntime,
    output_root: Path,
    run_identity: dict[str, Any],
) -> dict[str, Any]:
    """Run pair-wide judge, one shape correction, then atomic semantic fallback."""

    ledger_items = _read_ledger_for_pair(ledger_path, pair.pair_id)
    release = [issue for cell in method_rounds for issue in cell.get("report_issue_clusters", [])]
    prompt = _judge_prompt(pair, ledger_items, method_rounds)
    outcomes: list[StructuredCallOutcome[Any]] = []
    errors: list[dict[str, Any]] = []
    atomic_relations: list[dict[str, Any]] = []
    mode = "pair_wide"
    if not release:
        response = _exact_empty_release_judgement(ledger_items)
        payload = IndependentJudgeReceipt(
            schema=JUDGE_SCHEMA,
            run_id=run_identity["run_id"],
            run_contract_hash=run_identity["run_contract_hash"],
            source_provenance=run_identity["source_provenance"],
            pair_id=pair.pair_id,
            pair_input_hash=run_identity["pair_input_hashes"][pair.pair_id],
            status="completed",
            eligible=True,
            eligibility_reasons=["exact_release_set_is_empty", "no_semantic_relation_is_missing"],
            adjudication_mode="exact_empty_release",
            ledger_count=len(ledger_items),
            release_count=0,
            ledger_source=str(ledger_path),
            prompt_hash="sha256:" + hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            llm_calls=[],
            llm_call={
                "kind": "judge",
                "status": "not_required_exact_empty_release",
                "real_llm": False,
                "response": response.model_dump(mode="json"),
                "result": {"relation_count": 0},
                "attempts": [],
                "usage": [],
                "cost": {"eligible": True, "total_usd": 0.0, "attempts": []},
                "reason": "No LLM semantic relation exists to judge because the exact release issue set is empty.",
                "basis": "exact issue ID set and complete method receipt projection",
            },
            judgement=response.model_dump(mode="json"),
            atomic_relations=[],
            errors=[],
            reason=response.reason,
            basis=response.basis,
        ).model_dump(mode="json")
        write_json(output_root / "judge" / f"{pair.pair_id}.json", payload)
        return payload

    estimated_prompt_tokens = (len(prompt) + 3) // 4
    should_partition = (
        estimated_prompt_tokens > JUDGE_PROMPT_TOKEN_BUDGET
        or len(release) > JUDGE_PAIRWISE_MAX_RELEASES
    )
    if should_partition:
        mode = "partitioned_pair_wide"
        response, partition_outcomes, partition_errors = _partitioned_judge(
            pair=pair,
            ledger_items=ledger_items,
            release=release,
            method_rounds=method_rounds,
            runtime=runtime,
        )
        outcomes.extend(partition_outcomes)
        errors.extend(partition_errors)
        shape_errors = (
            _judge_shape_errors(response, ledger_items, release, len(method_rounds))
            if response is not None
            else ["partitioned judge output unavailable"]
        )
    else:
        outcome: StructuredCallOutcome[JudgeResponse] = runtime.call(
            kind="judge",
            schema=JudgeResponse,
            system_prompt=JUDGE_SYSTEM_PROMPT,
            prompt=prompt,
            artifact_id=f"judge/{pair.pair_id}",
        )
        outcomes.append(outcome)
        response = outcome.response if outcome.succeeded else None
        if response is not None:
            response = _normalize_judge_shape(response, ledger_items, release, len(method_rounds))
        shape_errors = (
            _judge_shape_errors(response, ledger_items, release, len(method_rounds))
            if response is not None
            else ["pair-wide judge output unavailable"]
        )
    if mode == "pair_wide" and response is not None and shape_errors:
        correction: StructuredCallOutcome[JudgeResponse] = runtime.call(
            kind="judge_correction",
            schema=JudgeResponse,
            system_prompt=JUDGE_SYSTEM_PROMPT,
            prompt=_judge_correction_prompt(pair, ledger_items, method_rounds, shape_errors),
            artifact_id=f"judge/{pair.pair_id}/shape-correction",
        )
        outcomes.append(correction)
        if correction.succeeded:
            response = _normalize_judge_shape(
                correction.response,
                ledger_items,
                release,
                len(method_rounds),
            )
            shape_errors = _judge_shape_errors(
                response, ledger_items, release, len(method_rounds)
            )
            if not shape_errors:
                mode = "pair_wide_corrected"
        else:
            shape_errors.append("judge shape correction output unavailable")
    if response is None or shape_errors:
        errors.append(
            {
                "stage": "pair_wide_judge",
                "error": "; ".join(shape_errors),
                "reason": "Pair-wide judge output did not close its exact shape contract and was not converted to deterministic misses or false positives.",
                "basis": "exact ledger/release ID coverage and reference validation",
            }
        )
        relation_count = len(ledger_items) * len(release)
        if relation_count <= JUDGE_ATOMIC_RELATION_BUDGET:
            mode = "atomic_llm_fallback"
            response, atomic_outcomes, atomic_relations, atomic_errors = _atomic_judge(
                pair=pair,
                ledger_items=ledger_items,
                release=release,
                runtime=runtime,
            )
            outcomes.extend(atomic_outcomes)
            errors.extend(atomic_errors)
        else:
            mode = "judge_unavailable"
            errors.append(
                {
                    "stage": "atomic_judge_fallback",
                    "error": "atomic_relation_budget_exceeded",
                    "relation_count": relation_count,
                    "relation_budget": JUDGE_ATOMIC_RELATION_BUDGET,
                    "reason": "The failed partition surface was too large for an auditable atomic fallback; relations remain unresolved rather than becoming misses or false positives.",
                    "basis": "bounded judge recovery policy and exact ledger/release cardinalities",
                }
            )
    if mode == "atomic_llm_fallback":
        semantic_outcomes = [
            item for item in outcomes if item.kind == "judge_atomic_relation"
        ]
    elif mode == "partitioned_pair_wide":
        semantic_outcomes = [
            item for item in outcomes if item.kind == "judge_partition"
        ]
    elif mode == "judge_unavailable":
        semantic_outcomes = []
    else:
        semantic_outcomes = [outcomes[-1]]
    eligible = bool(
        response is not None
        and semantic_outcomes
        and all(item.real_llm and item.succeeded for item in semantic_outcomes)
        and not _judge_shape_errors(response, ledger_items, release, len(method_rounds))
    )
    payload = IndependentJudgeReceipt.model_validate({
        "schema": JUDGE_SCHEMA,
        "run_id": run_identity["run_id"],
        "run_contract_hash": run_identity["run_contract_hash"],
        "source_provenance": run_identity["source_provenance"],
        "pair_id": pair.pair_id,
        "pair_input_hash": run_identity["pair_input_hashes"][pair.pair_id],
        "status": "completed" if eligible else "failed_with_receipt",
        "eligible": eligible,
        "eligibility_reasons": (
            ["real_semantic_judgement", "exact_judge_shape_complete"]
            if eligible
            else ["fixture_or_incomplete_semantic_judgement"]
        ),
        "adjudication_mode": mode,
        "ledger_count": len(ledger_items),
        "release_count": len(release),
        "ledger_source": str(ledger_path),
        "prompt_hash": "sha256:" + hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "llm_calls": [item.to_dict() for item in outcomes],
        "llm_call": _aggregate_outcomes(outcomes, kind="judge"),
        "judgement": response.model_dump(mode="json") if response is not None else None,
        "atomic_relations": atomic_relations,
        "errors": errors,
        "reason": (
            response.reason
            if response is not None
            else "Independent semantic judging did not close; no missing unit was converted to a miss or false positive."
        ),
        "basis": (
            response.basis
            if response is not None
            else "public runtime failure receipts and exact judge shape diagnostics"
        ),
    }).model_dump(mode="json")
    write_json(output_root / "judge" / f"{pair.pair_id}.json", payload)
    return payload


def _metrics(
    *,
    ledger_path: Path,
    pair_method: dict[str, list[dict[str, Any]]],
    pair_judge: dict[str, dict[str, Any]],
    selected_pair_ids: Sequence[str],
    rounds: int,
    ineligible_pair_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Compute paired-eligible readings and fixed-grid conservative bounds."""

    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    selected_pair_set = set(selected_pair_ids)
    all_items = [
        item
        for item in data["items"].values()
        if item.get("pair") in selected_pair_set
    ]
    dimensions = {
        "overall": lambda item: True,
        "L2": lambda item: item.get("L") == "L2",
        "D2xL2": lambda item: item.get("D") == "D2" and item.get("L") == "L2",
    }
    metrics: dict[str, Any] = {}
    assessment_map: dict[str, dict[str, LedgerAssessment]] = {}
    for pair_id, payload in pair_judge.items():
        judgement = payload.get("judgement")
        if not payload.get("eligible") or not isinstance(judgement, dict):
            continue
        assessment_map[pair_id] = {
            item["ledger_id"]: LedgerAssessment.model_validate(item)
            for item in judgement["ledger_assessments"]
        }
    forced_ineligible = set(ineligible_pair_ids)
    cell_eligible = {
        (pair_id, int(cell["round"])): bool(
            cell.get("eligible") and pair_id not in forced_ineligible
        )
        for pair_id, cells in pair_method.items()
        for cell in cells
    }
    judge_eligible = {
        pair_id: bool(payload.get("eligible") and pair_id not in forced_ineligible)
        for pair_id, payload in pair_judge.items()
    }
    for name, selector in dimensions.items():
        selected_items = [item for item in all_items if selector(item)]
        full_positions = len(selected_items) * rounds
        eligible_positions = 0
        hit_positions = 0
        hit_any = 0
        hit_all_eligible = 0
        conservative_hit_all = 0
        entries_with_eligible = 0
        eligible_round_counts: Counter[int] = Counter()
        for item in selected_items:
            pair_id = str(item["pair"])
            assessment = assessment_map.get(pair_id, {}).get(item["id"])
            item_eligible: list[bool] = []
            item_hits: list[bool] = []
            for round_index in range(1, rounds + 1):
                eligible = bool(
                    cell_eligible.get((pair_id, round_index), False)
                    and judge_eligible.get(pair_id, False)
                    and assessment is not None
                )
                item_eligible.append(eligible)
                item_hits.append(
                    bool(getattr(assessment, f"hit_r{round_index}"))
                    if eligible and assessment is not None
                    else False
                )
            eligible_count = sum(item_eligible)
            eligible_round_counts[eligible_count] += 1
            eligible_positions += eligible_count
            hit_positions += sum(item_hits)
            if eligible_count:
                entries_with_eligible += 1
                eligible_hits = [
                    hit
                    for hit, eligible in zip(item_hits, item_eligible)
                    if eligible
                ]
                hit_any += int(any(eligible_hits))
                hit_all_eligible += int(all(eligible_hits))
            conservative_hit_all += int(all(item_hits))
        metrics[name] = {
            "entries": len(selected_items),
            "paired_eligible": {
                "positions": eligible_positions,
                "full_grid_positions": full_positions,
                "eligible_rate": eligible_positions / full_positions if full_positions else 0.0,
                "entries_with_eligible_round": entries_with_eligible,
                "eligible_round_count_distribution": {
                    str(key): value for key, value in sorted(eligible_round_counts.items())
                },
                "hit_at_1": hit_positions,
                "hit_at_1_rate": hit_positions / eligible_positions if eligible_positions else 0.0,
                "hit_at_3": hit_any,
                "hit_at_3_rate": hit_any / entries_with_eligible if entries_with_eligible else 0.0,
                "hit_at_all": hit_all_eligible,
                "hit_at_all_rate": hit_all_eligible / entries_with_eligible if entries_with_eligible else 0.0,
            },
            "full_grid_lower_bound": {
                "positions": full_positions,
                "hit_at_1": hit_positions,
                "hit_at_1_rate": hit_positions / full_positions if full_positions else 0.0,
                "hit_at_3": hit_any,
                "hit_at_3_rate": hit_any / len(selected_items) if selected_items else 0.0,
                "hit_at_all": conservative_hit_all,
                "hit_at_all_rate": conservative_hit_all / len(selected_items) if selected_items else 0.0,
            },
        }
    emissions = [
        issue
        for cells in pair_method.values()
        for cell in cells
        for issue in cell.get("report_issue_clusters", [])
    ]
    release_by_pair = {
        pair_id: {
            item["issue_id"]: item
            for item in payload["judgement"]["release_assessments"]
        }
        for pair_id, payload in pair_judge.items()
        if payload.get("eligible") and isinstance(payload.get("judgement"), dict)
    }
    eligible_emissions: list[dict[str, Any]] = []
    unjudged_emissions: list[dict[str, Any]] = []
    false_positive_ids: set[str] = set()
    for issue in emissions:
        pair_id = issue["issue_id"].split(":", 1)[0]
        round_index = int(issue["issue_id"].split(":r", 1)[1].split(":", 1)[0])
        assessment = release_by_pair.get(pair_id, {}).get(issue["issue_id"])
        if cell_eligible.get((pair_id, round_index), False) and assessment is not None:
            eligible_emissions.append(issue)
            if assessment.get("is_false_positive"):
                false_positive_ids.add(issue["issue_id"])
        else:
            unjudged_emissions.append(issue)
    exact_fp_cause_keys = {
        _hash_json(
            {
                "pair_id": issue["issue_id"].split(":", 1)[0],
                "predicate_id": issue.get("predicate_id"),
                "predicate_inputs": issue.get("predicate_inputs"),
                "binding": issue.get("binding"),
                "element_refs": issue.get("element_refs"),
            }
        )
        for issue in eligible_emissions
        if issue["issue_id"] in false_positive_ids
    }
    eligible_release_count = len(eligible_emissions)
    fp = len(false_positive_ids)
    all_release_count = len(emissions)
    method_cell_count = sum(len(cells) for cells in pair_method.values())
    eligible_method_cells = sum(int(value) for value in cell_eligible.values())
    eligible_judges = sum(int(value) for value in judge_eligible.values())
    per_pair_metrics: dict[str, dict[str, Any]] = {}
    for pair_id in selected_pair_ids:
        pair_items = [item for item in all_items if item.get("pair") == pair_id]
        pair_assessments = assessment_map.get(pair_id, {})
        pair_cells = pair_method.get(pair_id, [])
        pair_release = [
            issue
            for cell in pair_cells
            for issue in cell.get("report_issue_clusters", [])
        ]

        def pair_dimension(selector: Any) -> dict[str, Any]:
            dimension_items = [item for item in pair_items if selector(item)]
            positions = 0
            hits = 0
            hit_any = 0
            for item in dimension_items:
                assessment = pair_assessments.get(item["id"])
                round_hits: list[bool] = []
                for round_index in range(1, rounds + 1):
                    eligible = bool(
                        cell_eligible.get((pair_id, round_index), False)
                        and judge_eligible.get(pair_id, False)
                        and assessment is not None
                    )
                    if eligible:
                        positions += 1
                        round_hits.append(bool(getattr(assessment, f"hit_r{round_index}")))
                hits += sum(round_hits)
                hit_any += int(any(round_hits))
            return {
                "entries": len(dimension_items),
                "eligible_positions": positions,
                "hit_at_1": hits,
                "hit_at_1_rate": hits / positions if positions else 0.0,
                "hit_at_3": hit_any,
                "hit_at_3_rate": hit_any / len(dimension_items) if dimension_items else 0.0,
            }

        pair_release_assessments = release_by_pair.get(pair_id, {})
        pair_eligible_release = [
            issue
            for issue in pair_release
            if cell_eligible.get(
                (
                    pair_id,
                    int(issue["issue_id"].split(":r", 1)[1].split(":", 1)[0]),
                ),
                False,
            )
            and issue["issue_id"] in pair_release_assessments
        ]
        pair_fp = sum(
            int(pair_release_assessments[issue["issue_id"]].get("is_false_positive", False))
            for issue in pair_eligible_release
        )
        records = [
            record
            for cell in pair_cells
            for record in cell.get("evidence_records", [])
        ]
        per_pair_metrics[pair_id] = {
            "overall": pair_dimension(lambda item: True),
            "L2": pair_dimension(lambda item: item.get("L") == "L2"),
            "D2xL2": pair_dimension(
                lambda item: item.get("D") == "D2" and item.get("L") == "L2"
            ),
            "method_cells": len(pair_cells),
            "eligible_method_cells": sum(
                int(cell_eligible.get((pair_id, int(cell["round"])), False))
                for cell in pair_cells
            ),
            "judge_eligible": judge_eligible.get(pair_id, False),
            "release_issue_count": len(pair_release),
            "eligible_release_issue_count": len(pair_eligible_release),
            "false_positive": pair_fp,
            "precision": (
                (len(pair_eligible_release) - pair_fp) / len(pair_eligible_release)
                if pair_eligible_release
                else 0.0
            ),
            "witness_levels": dict(Counter(record.get("witness_level") for record in records)),
            "d_levels": dict(Counter(record.get("d_level") for record in records)),
            "unresolved_or_error_records": sum(
                int(
                    record.get("d_level") == "D_UNRESOLVED"
                    or record.get("witness_level") == "UNKNOWN"
                )
                for record in records
            ),
            "method_diagnostics": sum(len(cell.get("errors", [])) for cell in pair_cells),
            "judge_diagnostics": len(pair_judge.get(pair_id, {}).get("errors", [])),
        }
    return {
        "overall": metrics,
        "eligibility": {
            "method_cells": method_cell_count,
            "eligible_method_cells": eligible_method_cells,
            "method_cell_eligible_rate": eligible_method_cells / method_cell_count if method_cell_count else 0.0,
            "judge_pairs": len(pair_judge),
            "eligible_judge_pairs": eligible_judges,
            "judge_pair_eligible_rate": eligible_judges / len(pair_judge) if pair_judge else 0.0,
        },
        "emissions": {
            "all_release_issue_count": all_release_count,
            "eligible_release_issue_count": eligible_release_count,
            "unjudged_or_ineligible_release_issue_count": len(unjudged_emissions),
            "false_positive": fp,
            "ledger_accounted": eligible_release_count - fp,
            "precision": (eligible_release_count - fp) / eligible_release_count if eligible_release_count else 0.0,
            "full_grid_precision_lower_bound": (
                (eligible_release_count - fp) / all_release_count
                if all_release_count
                else 0.0
            ),
            "unique_exact_cause_false_positive": len(exact_fp_cause_keys),
        },
        "method_quality": {
            "witness_levels": dict(Counter(record.get("witness_level") for cells in pair_method.values() for cell in cells for record in cell.get("evidence_records", []))),
            "d_levels": dict(Counter(record.get("d_level") for cells in pair_method.values() for cell in cells for record in cell.get("evidence_records", []))),
        },
        "per_pair": per_pair_metrics,
    }


def _failure_method_cell(
    *,
    pair_id: str,
    round_index: int,
    output_root: Path,
    error: BaseException,
    run_identity: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "schema": METHOD_CELL_SCHEMA,
        "run_id": run_identity["run_id"],
        "run_contract_hash": run_identity["run_contract_hash"],
        "source_provenance": run_identity["source_provenance"],
        "pair_id": pair_id,
        "pair_input_hash": run_identity.get("pair_input_hashes", {}).get(
            pair_id, "sha256:" + "0" * 64
        ),
        "round": round_index,
        "status": "failed_with_receipt",
        "model_output": {
            "issues": [],
            "reason": "Pair setup failed before a model candidate could be produced.",
            "basis": "structured pair-level failure receipt",
        },
        "llm_call": {
            "kind": "method",
            "status": "not_started",
            "real_llm": False,
            "response": None,
            "result": {},
            "attempts": [],
            "usage": [],
            "cost": {"eligible": True, "total_usd": 0.0, "attempts": []},
            "reason": "The method provider path did not start because pair setup failed.",
            "basis": "pair-level orchestration failure",
        },
        "llm_calls": [],
        "eligible": False,
        "eligibility_reasons": ["pair_setup_or_orchestration_failure"],
        "evidence_records": [],
        "report_issue_clusters": [],
        "errors": [{
            "error_type": type(error).__name__,
            "message": str(error),
            "reason": "The pair-level failure was converted to an explicit method-cell receipt.",
            "basis": "no-silent-drop frozen cell contract",
        }],
        "reason": "Pair setup or orchestration failed; no method evidence was silently discarded.",
        "basis": "deterministic pair-level failure receipt",
    }
    validated = MethodCellReceipt.model_validate(payload).model_dump(mode="json")
    write_json(
        output_root / "method" / pair_id / f"round-{round_index}.json",
        validated,
    )
    return validated


def _failure_judge_payload(
    *,
    pair_id: str,
    ledger_path: Path,
    release: list[dict[str, Any]],
    output_root: Path,
    error: BaseException,
    run_identity: dict[str, Any],
) -> dict[str, Any]:
    try:
        ledger_items = _read_ledger_for_pair(ledger_path, pair_id)
        ledger_error = None
    except Exception as ledger_exc:
        ledger_items = []
        ledger_error = {
            "error_type": type(ledger_exc).__name__,
            "message": str(ledger_exc),
            "reason": "The frozen ledger could not be loaded; no semantic position was fabricated.",
            "basis": "ledger read failure receipt",
        }
    payload = {
        "schema": JUDGE_SCHEMA,
        "run_id": run_identity["run_id"],
        "run_contract_hash": run_identity["run_contract_hash"],
        "source_provenance": run_identity["source_provenance"],
        "pair_id": pair_id,
        "pair_input_hash": run_identity.get("pair_input_hashes", {}).get(
            pair_id, "sha256:" + "0" * 64
        ),
        "status": "failed_with_receipt",
        "eligible": False,
        "eligibility_reasons": ["judge_setup_failure_unadjudicated"],
        "adjudication_mode": "not_started",
        "ledger_count": len(ledger_items),
        "release_count": len(release),
        "ledger_source": str(ledger_path),
        "prompt_hash": None,
        "llm_call": {
            "kind": "judge",
            "status": "not_started",
            "real_llm": False,
            "response": None,
            "result": {},
            "attempts": [],
            "usage": [],
            "cost": {"eligible": True, "total_usd": 0.0, "attempts": []},
            "reason": "The independent judge provider path did not start.",
            "basis": "pair-level judge setup failure receipt",
        },
        "llm_calls": [],
        "judgement": None,
        "atomic_relations": [],
        "reason": "The independent judge did not start; every required relation remains explicitly unadjudicated rather than becoming a miss or false positive.",
        "basis": "deterministic no-silent-drop and no-fabricated-judgement failure contract",
        "errors": [
            {
                "error_type": type(error).__name__,
                "message": str(error),
                "reason": "judge setup failure receipt",
                "basis": "pair-level orchestration diagnostic",
            },
            *([ledger_error] if ledger_error else []),
        ],
    }
    validated = IndependentJudgeReceipt.model_validate(payload).model_dump(mode="json")
    write_json(output_root / "judge" / f"{pair_id}.json", validated)
    return validated


def _write_pair_status(
    output_root: Path,
    pair_id: str,
    status: dict[str, Any],
) -> dict[str, Any]:
    payload = PairRunStatus.model_validate(
        {
            "schema": "paper1.evidence_discovery.pair_status.v2",
            "pair_id": pair_id,
            **status,
            "reason": status.get("reason", "Pair status was computed from terminal method and judge receipts."),
            "basis": status.get("basis", "frozen protocol cells, judge receipt, usage, and run contract"),
        }
    )
    write_json(
        output_root / "pairs" / pair_id / "status.json",
        payload.model_dump(mode="json"),
    )
    return payload.model_dump(mode="json")


def _quarantine_incompatible(
    path: Path,
    *,
    output_root: Path,
    reason: str,
) -> None:
    """Preserve an incompatible artifact outside the active resume surface."""

    if not path.exists():
        return
    relative = path.relative_to(output_root)
    target = output_root / "stale" / uuid.uuid4().hex / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    path.replace(target)
    write_json(
        target.with_suffix(target.suffix + ".stale.json"),
        {
            "schema": "paper1.evidence_discovery.stale_artifact.v1",
            "original_path": str(path),
            "preserved_path": str(target),
            "status": "stale_incompatible",
            "reason": reason,
            "basis": "strict run-id, contract, schema, source, and input-manifest resume validation",
        },
    )


def _read_compatible_method_cell(
    path: Path,
    *,
    output_root: Path,
    pair_id: str,
    round_index: int,
    run_identity: dict[str, Any],
) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        receipt = MethodCellReceipt.model_validate_json(path.read_text(encoding="utf-8"))
        if receipt.run_id != run_identity["run_id"]:
            raise ValueError("run_id mismatch")
        if receipt.run_contract_hash != run_identity["run_contract_hash"]:
            raise ValueError("run contract hash mismatch")
        if receipt.pair_id != pair_id or receipt.round != round_index:
            raise ValueError("pair or round mismatch")
        if receipt.pair_input_hash != run_identity["pair_input_hashes"][pair_id]:
            raise ValueError("pair input hash mismatch")
        if receipt.source_provenance.model_dump(mode="json") != run_identity["source_provenance"]:
            raise ValueError("source provenance mismatch")
        expected_input_hash = run_identity["pair_input_hashes"][pair_id]
        if receipt.status != "failed_with_receipt":
            actual_input_hash = (
                receipt.context_manifest.get("manifest_hash")
                if isinstance(receipt.context_manifest, dict)
                else None
            )
            if actual_input_hash != expected_input_hash:
                raise ValueError("pair input manifest hash mismatch")
        return receipt.model_dump(mode="json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        _quarantine_incompatible(
            path,
            output_root=output_root,
            reason=f"Method receipt is incompatible: {type(exc).__name__}: {exc}",
        )
        return None


def _read_compatible_judge(
    path: Path,
    *,
    output_root: Path,
    pair_id: str,
    run_identity: dict[str, Any],
) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        receipt = IndependentJudgeReceipt.model_validate_json(
            path.read_text(encoding="utf-8")
        )
        if receipt.run_id != run_identity["run_id"]:
            raise ValueError("run_id mismatch")
        if receipt.run_contract_hash != run_identity["run_contract_hash"]:
            raise ValueError("run contract hash mismatch")
        if receipt.pair_id != pair_id:
            raise ValueError("pair mismatch")
        if receipt.pair_input_hash != run_identity["pair_input_hashes"][pair_id]:
            raise ValueError("pair input hash mismatch")
        if receipt.source_provenance.model_dump(mode="json") != run_identity["source_provenance"]:
            raise ValueError("source provenance mismatch")
        return receipt.model_dump(mode="json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        _quarantine_incompatible(
            path,
            output_root=output_root,
            reason=f"Judge receipt is incompatible: {type(exc).__name__}: {exc}",
        )
        return None


def _load_pair_receipts(
    *,
    output_root: Path,
    pair_id: str,
    rounds: int,
    run_identity: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Load only a contiguous compatible method prefix and its terminal judge."""

    rounds_data: list[dict[str, Any]] = []
    missing_predecessor = False
    for round_index in range(1, rounds + 1):
        path = output_root / "method" / pair_id / f"round-{round_index}.json"
        if missing_predecessor:
            if path.exists():
                _quarantine_incompatible(
                    path,
                    output_root=output_root,
                    reason="A later method round cannot resume without every earlier compatible round.",
                )
            continue
        cell = _read_compatible_method_cell(
            path,
            output_root=output_root,
            pair_id=pair_id,
            round_index=round_index,
            run_identity=run_identity,
        )
        if cell is None:
            missing_predecessor = True
        else:
            rounds_data.append(cell)

    judge_path = output_root / "judge" / f"{pair_id}.json"
    if len(rounds_data) != rounds:
        if judge_path.exists():
            _quarantine_incompatible(
                judge_path,
                output_root=output_root,
                reason="Judge receipt cannot resume before all compatible method rounds are terminal.",
            )
        return rounds_data, None
    return rounds_data, _read_compatible_judge(
        judge_path,
        output_root=output_root,
        pair_id=pair_id,
        run_identity=run_identity,
    )


def _cost_total(receipt: dict[str, Any]) -> float:
    value = receipt.get("llm_call", {}).get("cost", {}).get("total_usd")
    return float(value) if isinstance(value, (int, float)) else 0.0


def _finalize_w2_audit_links(
    *,
    output_root: Path,
    pair_id: str,
    rounds_data: list[dict[str, Any]],
    judge: dict[str, Any],
) -> None:
    """Link external W2 bundles to immutable method and judge receipts."""

    judge_hash = _hash_json(judge)
    judge_path = output_root / "judge" / f"{pair_id}.json"
    for cell in rounds_data:
        method_path = (
            output_root
            / "method"
            / pair_id
            / f"round-{cell['round']}.json"
        )
        method_hash = _hash_json(cell)
        for record in cell.get("evidence_records", []):
            if record.get("witness_level") != "W2":
                continue
            path_value = record.get("audit_bundle_path")
            if not isinstance(path_value, str) or not path_value:
                raise RuntimeError(
                    f"W2 record {record.get('obligation_id')} has no external audit bundle path"
                )
            audit_path = Path(path_value).resolve()
            try:
                audit_path.relative_to(output_root.resolve())
            except ValueError as exc:
                raise RuntimeError("W2 audit path escapes the active run root") from exc
            bundle = json.loads(audit_path.read_text(encoding="utf-8"))
            finalization = bundle.get("audit_finalization")
            if (
                isinstance(finalization, dict)
                and finalization.get("judge_receipt_hash") == judge_hash
                and bundle.get("method_receipt", {}).get("sha256") == method_hash
            ):
                continue
            bundle.pop("audit_hash", None)
            bundle["method_receipt"] = {
                "schema": cell.get("schema"),
                "path": str(method_path),
                "sha256": method_hash,
                "run_id": cell.get("run_id"),
                "run_contract_hash": cell.get("run_contract_hash"),
                "pair_input_hash": cell.get("pair_input_hash"),
                "status": cell.get("status"),
                "eligible": cell.get("eligible"),
                "reason": "This is the exact terminal method receipt evaluated at the independent judge boundary.",
                "basis": "atomically written v2 method-cell JSON",
            }
            bundle["judge_receipt"] = {
                "schema": judge.get("schema"),
                "path": str(judge_path),
                "sha256": judge_hash,
                "run_id": judge.get("run_id"),
                "run_contract_hash": judge.get("run_contract_hash"),
                "status": judge.get("status"),
                "eligible": judge.get("eligible"),
                "adjudication_mode": judge.get("adjudication_mode"),
                "reason": judge.get("reason"),
                "basis": judge.get("basis"),
            }
            bundle["audit_finalization"] = {
                "finalized_at": datetime.now(timezone.utc).isoformat(),
                "judge_receipt_hash": judge_hash,
                "reason": "The external W2 bundle was finalized only after method and judge receipts became terminal.",
                "basis": "method-before-judge orchestration and atomic receipt writes",
            }
            write_json(audit_path, validate_and_hash_w2_audit_bundle(bundle))


def _pair_status(
    *,
    pair_id: str,
    started_at: str,
    rounds_data: list[dict[str, Any]],
    judge: dict[str, Any],
    run_identity: dict[str, Any],
    audit_errors: int = 0,
    resume_action: str = "reconstructed_terminal_status",
) -> dict[str, Any]:
    method_errors = sum(len(cell.get("errors", [])) for cell in rounds_data)
    judge_errors = len(judge.get("errors", []))
    method_eligible = sum(int(bool(cell.get("eligible"))) for cell in rounds_data)
    judge_eligible = bool(judge.get("eligible"))
    method_cost_eligible = all(
        bool(cell.get("llm_call", {}).get("cost", {}).get("eligible"))
        for cell in rounds_data
    )
    judge_cost_eligible = bool(
        judge.get("llm_call", {}).get("cost", {}).get("eligible")
    )
    failed = bool(
        audit_errors
        or any(cell.get("status") == "failed_with_receipt" for cell in rounds_data)
        or judge.get("status") == "failed_with_receipt"
    )
    clean = bool(
        not failed
        and method_errors == 0
        and judge_errors == 0
        and method_eligible == len(rounds_data)
        and judge_eligible
        and all(cell.get("status") == "completed" for cell in rounds_data)
    )
    status = "failed_with_receipt" if failed else "completed" if clean else "completed_with_diagnostics"
    return {
        "run_id": run_identity["run_id"],
        "run_contract_hash": run_identity["run_contract_hash"],
        "status": status,
        "resume_action": resume_action,
        "started_at": started_at,
        "method_cells": len(rounds_data),
        "eligible_method_cells": method_eligible,
        "judge_status": str(judge.get("status", "failed_with_receipt")),
        "judge_eligible": judge_eligible,
        "errors": method_errors + judge_errors + audit_errors,
        "audit_errors": audit_errors,
        "method_cost_usd": sum(_cost_total(cell) for cell in rounds_data),
        "method_cost_eligible": method_cost_eligible,
        "judge_cost_usd": _cost_total(judge),
        "judge_cost_eligible": judge_cost_eligible,
        "reason": "Pair status was derived only from complete method cells, judge coverage, diagnostics, and audited usage.",
        "basis": "v2 method/judge receipts sharing the exact run contract and pair input identity",
    }


def _finalize_w2_audit_links_with_receipt(
    *,
    output_root: Path,
    pair_id: str,
    rounds_data: list[dict[str, Any]],
    judge: dict[str, Any],
) -> int:
    """Keep an audit-finalization bug local to one pair and preserve its cause."""

    try:
        _finalize_w2_audit_links(
            output_root=output_root,
            pair_id=pair_id,
            rounds_data=rounds_data,
            judge=judge,
        )
        return 0
    except Exception as exc:
        write_json(
            output_root / "pairs" / pair_id / f"audit-finalization-error-{uuid.uuid4().hex}.json",
            {
                "schema": "paper1.evidence_discovery.audit_finalization_error.v1",
                "pair_id": pair_id,
                "error_type": type(exc).__name__,
                "message": str(exc),
                "status": "error",
                "reason": "A W2 bundle could not be linked to terminal method/judge receipts; the pair is failed with a receipt and the batch continues.",
                "basis": "W2 v2 Pydantic validation and active run-root path boundary",
            },
        )
        return 1


def _pair_started_at(
    *,
    output_root: Path,
    pair_id: str,
    run_identity: dict[str, Any],
) -> str:
    """Preserve the original pair start time across compatible resume calls."""

    path = output_root / "pairs" / pair_id / "status.json"
    if path.is_file():
        try:
            status = PairRunStatus.model_validate_json(path.read_text(encoding="utf-8"))
            if (
                status.run_id != run_identity["run_id"]
                or status.run_contract_hash != run_identity["run_contract_hash"]
            ):
                raise ValueError("pair status identity mismatch")
            return status.started_at.isoformat()
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            _quarantine_incompatible(
                path,
                output_root=output_root,
                reason=f"Pair status is incompatible: {type(exc).__name__}: {exc}",
            )
    return datetime.now(timezone.utc).isoformat()


def _terminalize_pair_failure(
    *,
    pair_id: str,
    rounds: int,
    ledger_path: Path,
    output_root: Path,
    run_identity: dict[str, Any],
    started_at: str,
    error: BaseException,
) -> dict[str, Any]:
    rounds_data, judge = _load_pair_receipts(
        output_root=output_root,
        pair_id=pair_id,
        rounds=rounds,
        run_identity=run_identity,
    )
    while len(rounds_data) < rounds:
        rounds_data.append(
            _failure_method_cell(
                pair_id=pair_id,
                round_index=len(rounds_data) + 1,
                output_root=output_root,
                error=error,
                run_identity=run_identity,
            )
        )
    if judge is None:
        release = [
            issue
            for cell in rounds_data
            for issue in cell.get("report_issue_clusters", [])
        ]
        judge = _failure_judge_payload(
            pair_id=pair_id,
            ledger_path=ledger_path,
            release=release,
            output_root=output_root,
            error=error,
            run_identity=run_identity,
        )
    audit_errors = _finalize_w2_audit_links_with_receipt(
        output_root=output_root,
        pair_id=pair_id,
        rounds_data=rounds_data,
        judge=judge,
    )
    status = _pair_status(
        pair_id=pair_id,
        started_at=started_at,
        rounds_data=rounds_data,
        judge=judge,
        run_identity=run_identity,
        audit_errors=audit_errors,
        resume_action="terminalized_after_error",
    )
    return _write_pair_status(output_root, pair_id, status)


def _run_pair_worker(task: dict[str, Any]) -> dict[str, Any]:
    """Run or strictly resume one pair in an isolated process."""

    pair_id = str(task["pair_id"])
    rounds = int(task["rounds"])
    output_root = Path(task["output_root"])
    ledger_path = Path(task["ledger_path"])
    report_root = Path(task["report_root"])
    run_identity = dict(task["run_identity"])
    started_at = _pair_started_at(
        output_root=output_root,
        pair_id=pair_id,
        run_identity=run_identity,
    )
    try:
        rounds_data, judge = _load_pair_receipts(
            output_root=output_root,
            pair_id=pair_id,
            rounds=rounds,
            run_identity=run_identity,
        )
        if len(rounds_data) == rounds and judge is not None:
            audit_errors = _finalize_w2_audit_links_with_receipt(
                output_root=output_root,
                pair_id=pair_id,
                rounds_data=rounds_data,
                judge=judge,
            )
            status = _pair_status(
                pair_id=pair_id,
                started_at=started_at,
                rounds_data=rounds_data,
                judge=judge,
                run_identity=run_identity,
                audit_errors=audit_errors,
                resume_action="skipped_compatible_terminal",
            )
            return _write_pair_status(output_root, pair_id, status)

        pair = load_pair(report_root / "pairs" / pair_id)
        if task["profile"] == "fixture":
            runtime: Any = FixtureStructuredRuntime()
        else:
            runtime = PublicStructuredRuntime(
                str(task["profile"]),
                output_root / "llm",
                transport_retries=int(task["transport_retries"]),
                streaming=bool(task["streaming"]),
            )
        resumed_prefix = bool(rounds_data)
        previous: list[dict[str, Any]] = (
            rounds_data[-1].get("report_issue_clusters", []) if rounds_data else []
        )
        for round_index in range(len(rounds_data) + 1, rounds + 1):
            cell = _method_cell(
                pair=pair,
                round_index=round_index,
                runtime=runtime,
                previous=previous,
                output_root=output_root,
                run_identity=run_identity,
            )
            rounds_data.append(cell)
            previous = cell.get("report_issue_clusters", [])
        if judge is None:
            judge = _judge_pair(
                pair=pair,
                method_rounds=rounds_data,
                ledger_path=ledger_path,
                runtime=runtime,
                output_root=output_root,
                run_identity=run_identity,
            )
        audit_errors = _finalize_w2_audit_links_with_receipt(
            output_root=output_root,
            pair_id=pair_id,
            rounds_data=rounds_data,
            judge=judge,
        )
        status = _pair_status(
            pair_id=pair_id,
            started_at=started_at,
            rounds_data=rounds_data,
            judge=judge,
            run_identity=run_identity,
            audit_errors=audit_errors,
            resume_action=(
                "resumed_compatible_prefix" if resumed_prefix else "executed_fresh"
            ),
        )
        return _write_pair_status(output_root, pair_id, status)
    except Exception as exc:
        return _terminalize_pair_failure(
            pair_id=pair_id,
            rounds=rounds,
            ledger_path=ledger_path,
            output_root=output_root,
            run_identity=run_identity,
            started_at=started_at,
            error=exc,
        )


def run_experiment(
    *,
    report_root: str | Path,
    ledger_path: str | Path,
    output_dir: str | Path,
    profile: str = "gpt-5.6-luna",
    rounds: int = 3,
    resume: bool = False,
    allow_live: bool = False,
    allow_full_live: bool = False,
    pair_ids: Sequence[str] | None = None,
    workers: int = 1,
    transport_retries: int = DEFAULT_TRANSPORT_RETRIES,
    streaming: bool = True,
    run_id: str | None = None,
    predecessor_snapshot: str | None = None,
) -> dict[str, Any]:
    """Execute a contract-compatible diagnostic or frozen full Luna run."""

    if rounds not in {1, 3}:
        raise ValueError("rounds must be 1 for a diagnostic run or 3 for the frozen protocol")
    if workers < 1:
        raise ValueError("workers must be at least 1")
    if transport_retries < 0:
        raise ValueError("transport_retries must be non-negative")
    if profile != "fixture" and not allow_live:
        raise RuntimeError(
            "live Luna execution requires explicit allow_live=True after provider-free review"
        )
    if profile == "gpt-5.6-sol" or profile.endswith("-sol"):
        raise RuntimeError("Sol execution is outside this Luna-only construction and diagnostic run")

    selected_pair_ids = tuple(
        dict.fromkeys(FROZEN_PAIR_IDS if pair_ids is None else pair_ids)
    )
    unknown_pair_ids = sorted(set(selected_pair_ids) - set(FROZEN_PAIR_IDS))
    if not selected_pair_ids:
        raise ValueError("at least one frozen pair ID is required")
    if unknown_pair_ids:
        raise ValueError(f"pair IDs are outside the frozen 54-pair protocol: {unknown_pair_ids}")
    full_protocol = set(selected_pair_ids) == set(FROZEN_PAIR_IDS)
    if profile != "fixture":
        if full_protocol:
            if not allow_full_live:
                raise RuntimeError(
                    "the 54-pair live run requires explicit allow_full_live=True after six-pair review"
                )
            if profile != "gpt-5.6-luna" or rounds != 3:
                raise RuntimeError("full live execution is frozen to gpt-5.6-luna and three rounds")
        else:
            if pair_ids is None:
                raise RuntimeError("live diagnostic execution requires explicit pair_ids")
            if len(selected_pair_ids) > len(REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS):
                raise RuntimeError("live diagnostic runs are capped at six explicit pair IDs")

    report_root_path = Path(report_root).expanduser().resolve()
    ledger = Path(ledger_path).expanduser().resolve()
    source_provenance = _source_provenance()
    if profile != "fixture" and (
        source_provenance["source_dirty"]
        or source_provenance["source_commit"] == "unknown"
    ):
        raise RuntimeError(
            "live execution requires a clean tracked worktree and exact Git commit; commit and push before testing"
        )
    output_root, selected_run_id = _resolve_run_root(
        Path(output_dir),
        resume=resume,
        requested_run_id=run_id,
    )
    registry = load_registry()
    pair_input_hashes = _collect_pair_input_hashes(
        report_root_path,
        selected_pair_ids,
    )
    ledger_hash = _hash_file(ledger)
    input_data_hash = _hash_json(
        {
            "pair_input_hashes": pair_input_hashes,
            "judge_only_ledger_hash": ledger_hash,
        }
    )
    prompt_schema_hash = _prompt_schema_hash()
    manifest = _prepare_run_manifest(
        output_root=output_root,
        profile=profile,
        run_id=selected_run_id,
        source_provenance=source_provenance,
        registry_version=registry.version,
        registry_hash=registry.registry_hash,
        prompt_schema_hash=prompt_schema_hash,
        input_data_hash=input_data_hash,
        pair_input_hashes=pair_input_hashes,
        ledger_hash=ledger_hash,
        rounds=rounds,
        selected_pair_ids=selected_pair_ids,
        workers=workers,
        transport_retries=transport_retries,
        streaming=streaming,
        resume=resume,
        predecessor_snapshot=predecessor_snapshot,
    )
    run_identity = {
        "run_id": manifest.run_id,
        "run_contract_hash": manifest.run_contract_hash,
        "source_provenance": manifest.source_provenance.model_dump(mode="json"),
        "pair_input_hashes": dict(manifest.pair_input_hashes),
    }
    tasks = [
        {
            "pair_id": pair_id,
            "rounds": rounds,
            "output_root": str(output_root),
            "ledger_path": str(ledger),
            "report_root": str(report_root_path),
            "run_identity": run_identity,
            "profile": profile,
            "transport_retries": transport_retries,
            "streaming": streaming,
        }
        for pair_id in selected_pair_ids
    ]
    if workers == 1:
        for task in tasks:
            _run_pair_worker(task)
    else:
        context = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(max_workers=workers, mp_context=context) as pool:
            futures = {
                pool.submit(_run_pair_worker, task): str(task["pair_id"])
                for task in tasks
            }
            for future in as_completed(futures):
                pair_id = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    _terminalize_pair_failure(
                        pair_id=pair_id,
                        rounds=rounds,
                        ledger_path=ledger,
                        output_root=output_root,
                        run_identity=run_identity,
                        started_at=datetime.now(timezone.utc).isoformat(),
                        error=exc,
                    )

    pair_method: dict[str, list[dict[str, Any]]] = {}
    pair_judge: dict[str, dict[str, Any]] = {}
    per_pair: dict[str, dict[str, Any]] = {}
    for pair_id in selected_pair_ids:
        rounds_data, judge = _load_pair_receipts(
            output_root=output_root,
            pair_id=pair_id,
            rounds=rounds,
            run_identity=run_identity,
        )
        if len(rounds_data) != rounds or judge is None:
            _terminalize_pair_failure(
                pair_id=pair_id,
                rounds=rounds,
                ledger_path=ledger,
                output_root=output_root,
                run_identity=run_identity,
                started_at=datetime.now(timezone.utc).isoformat(),
                error=RuntimeError("pair worker returned without a complete terminal receipt set"),
            )
            rounds_data, judge = _load_pair_receipts(
                output_root=output_root,
                pair_id=pair_id,
                rounds=rounds,
                run_identity=run_identity,
            )
        if len(rounds_data) != rounds or judge is None:
            raise RuntimeError(f"pair {pair_id} could not be terminalized")
        pair_method[pair_id] = rounds_data
        pair_judge[pair_id] = judge
        status_path = output_root / "pairs" / pair_id / "status.json"
        try:
            status = PairRunStatus.model_validate_json(
                status_path.read_text(encoding="utf-8")
            )
            if (
                status.run_id != manifest.run_id
                or status.run_contract_hash != manifest.run_contract_hash
            ):
                raise ValueError("pair status run identity mismatch")
            per_pair[pair_id] = status.model_dump(mode="json")
        except (OSError, ValueError, json.JSONDecodeError):
            per_pair[pair_id] = _write_pair_status(
                output_root,
                pair_id,
                _pair_status(
                    pair_id=pair_id,
                    started_at=datetime.now(timezone.utc).isoformat(),
                    rounds_data=rounds_data,
                    judge=judge,
                    run_identity=run_identity,
                ),
            )

    metrics = _metrics(
        ledger_path=ledger,
        pair_method=pair_method,
        pair_judge=pair_judge,
        selected_pair_ids=selected_pair_ids,
        rounds=rounds,
        ineligible_pair_ids=[
            pair_id
            for pair_id, row in per_pair.items()
            if row.get("audit_errors", 0)
        ],
    )
    method_cost = sum(
        _cost_total(cell)
        for cells in pair_method.values()
        for cell in cells
    )
    judge_cost = sum(_cost_total(payload) for payload in pair_judge.values())
    all_cost_eligible = all(
        row["method_cost_eligible"] and row["judge_cost_eligible"]
        for row in per_pair.values()
    )
    metrics["cost"] = {
        "eligible": all_cost_eligible,
        "method_usd": method_cost,
        "judge_usd": judge_cost,
        "total_usd": method_cost + judge_cost,
        "reason": "Method and independent judge costs remain separate and use row-local provider retry exemptions.",
        "basis": "public utils.llm pricing and per-call normalized usage receipts",
    }
    final_status = (
        "completed"
        if all(row["status"] == "completed" for row in per_pair.values())
        else "completed_with_diagnostics"
    )
    completed_at = datetime.now(timezone.utc)
    summary = RunSummaryReceipt(
        schema=SUMMARY_SCHEMA,
        run_id=manifest.run_id,
        run_contract_hash=manifest.run_contract_hash,
        artifact_root=str(output_root),
        status=final_status,
        run_started_at=manifest.started_at,
        run_completed_at=completed_at,
        profile=profile,
        source_commit=source_provenance["source_commit"],
        source_branch=source_provenance["source_branch"],
        source_provenance=source_provenance,
        resume=resume,
        rounds=rounds,
        workers=workers,
        transport_retries=transport_retries,
        streaming=streaming,
        registry_version=registry.version,
        registry_hash=registry.registry_hash,
        pair_count=len(selected_pair_ids),
        protocol_pair_count=len(FROZEN_PAIR_IDS),
        selected_pair_ids=list(selected_pair_ids),
        scope="full_protocol" if full_protocol else "diagnostic_subset",
        selection={
            "pair_ids": list(selected_pair_ids),
            "reason": "The selected pair grid was frozen in the run manifest before provider execution.",
            "basis": (
                "v27-predecessor representative set: 0004, 0023, 0029, 0035, 0046, 0053"
                if set(selected_pair_ids) == set(REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS)
                else "frozen 54-pair protocol" if full_protocol else "explicit diagnostic pair_ids"
            ),
        },
        method_cell_count=sum(len(value) for value in pair_method.values()),
        judge_pair_count=len(pair_judge),
        method_cost_usd=method_cost,
        judge_cost_usd=judge_cost,
        metrics=metrics,
        per_pair=per_pair,
        failed_pairs=[
            pair_id
            for pair_id, row in per_pair.items()
            if row["status"] == "failed_with_receipt"
        ],
        method_cells_with_diagnostics=[
            f"{pair_id}:r{cell['round']}"
            for pair_id, cells in pair_method.items()
            for cell in cells
            if cell.get("status") != "completed"
            or cell.get("errors")
            or not cell.get("eligible")
        ],
        predecessor_snapshot=predecessor_snapshot,
        reason="Every selected pair has terminal method and independent-judge receipts under one strict run identity.",
        basis="four-family-19-core.v1, v2 run manifest, exact input closure hashes, and no-fabricated-judge metrics",
    ).model_dump(mode="json")
    write_json(output_root / "summary.json", summary)
    write_markdown_summary(output_root / "SUMMARY.md", summary)
    write_json(
        output_root / "audit_index.json",
        {
            "schema": "paper1.evidence_discovery.audit_index.v2",
            "run_id": manifest.run_id,
            "run_contract_hash": manifest.run_contract_hash,
            "pairs": per_pair,
            "method_cell_count": summary["method_cell_count"],
            "judge_pair_count": summary["judge_pair_count"],
            "reason": "The index points only to artifacts validated under the active run identity.",
            "basis": "v2 method, judge, pair-status, and run-summary receipts",
        },
    )
    final_manifest = manifest.model_copy(
        update={"status": final_status, "updated_at": completed_at}
    )
    write_json(output_root / "run_manifest.json", final_manifest.model_dump(mode="json"))
    return summary
