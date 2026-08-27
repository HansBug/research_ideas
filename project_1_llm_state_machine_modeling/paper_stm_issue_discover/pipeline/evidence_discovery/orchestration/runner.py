from __future__ import annotations

import hashlib
import json
import multiprocessing
import re
import subprocess
import uuid
from collections import Counter
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar

from pydantic import Field, create_model, model_validator

from ..backends import run_backend
from ..compiler import compile_plan
from ..compiler.plans import validate_plan
from ..evidence import (
    build_evidence_record,
    build_predicate_execution_receipt,
    validate_and_hash_w2_audit_bundle,
)
from ..evidence.receipts import RawReceipt
from ..evidence.source_attribution import build_source_attribution
from ..evidence.witness_levels import calculate_witness_level
from ..inputs import FROZEN_PAIR_IDS, load_pair
from ..inputs.fcstm_native_projection import (
    load_native_document,
    native_assignment_pairs,
    native_guard_equality_pairs,
    transition_by_reference,
)
from ..inputs.models import PairInput
from ..registry import load_registry
from ..reporting.export import write_json, write_markdown_summary
from ..semantics import (
    CONTRACT_SYSTEM_PROMPT,
    D_SYSTEM_PROMPT,
    DISCOVERY_GROUNDING_AUDIT_LENSES,
    DISCOVERY_GROUNDING_SYSTEM_PROMPT,
    CandidateIssue,
    CardinalityDomainBinding,
    ContextBudgetReceipt,
    DAdjudicationResponse,
    FrontierBatch,
    GroundingResponse,
    GroupIdentityNormalizationReceipt,
    IdentityNormalizationReceipt,
    NLContract,
    NLContractResponse,
    NLTransitionGroup,
    SemanticAdjudication,
    SemanticBinding,
    SourceTransitionClosureReceipt,
    StageReceipt,
    assemble_method_response,
    bind_candidate,
    build_contract_prompt,
    build_d_adjudication_batches,
    build_d_correction_batches,
    build_grounding_prompt,
    canonical_contract_id,
    canonicalize_grounding_response,
    contract_semantic_key,
    evaluate_source_transition_closure,
    fallback_contracts,
    fallback_d_adjudication,
    fallback_grounding,
    materialize_segment_coverage,
    materialize_typed_frontier,
    normalize_contract_state_roles,
    resolve_state_ref,
    resolve_transition_ref,
    suppress_closed_route_controller_candidates,
    suppress_contradicted_ambiguous_source_candidates,
    suppress_satisfied_source_transition_candidates,
)
from ..semantics.predicate_routing import (
    build_r1_cold_runtime_scenario,
    finalize_route_telemetry,
    route_primary_candidates,
)
from .contracts import (
    MethodCellReceipt,
    PairRunStatus,
    RunManifest,
    RunSummaryReceipt,
    SelectionPreflightReference,
    SourceProvenance,
)
from .runtime import (
    DEFAULT_TRANSPORT_RETRIES,
    MAX_STRUCTURED_OUTPUT_TOKENS,
    PROVIDER_CALL_DEADLINE_SECONDS,
    PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS,
    STRUCTURED_STAGE_FINALIZATION_GRACE_SECONDS,
    STRUCTURED_WRAPPER_FINALIZATION_GRACE_SECONDS,
    TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS,
    FixtureStructuredRuntime,
    PublicStructuredRuntime,
    StructuredCallOutcome,
    _structured_model_call_reservation_limit,
    _structured_stage_deadline_seconds,
)

REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS = (
    "0001",
    "0002",
    "0004",
    "0010",
    "0012",
    "0013",
    "0023",
    "0024",
    "0029",
    "0035",
    "0046",
    "0049",
    "0053",
    "0054",
    "0056",
)
METHOD_CELL_SCHEMA = "evidence-discovery.method_cell.v8"
SUMMARY_SCHEMA = "evidence-discovery.run_summary.v3"
RUN_MANIFEST_SCHEMA = "evidence-discovery.run_manifest.v3"
CODE_VERSION = "evidence-discovery-typed-flow.v54-method-only"
PROMPT_SCHEMA_VERSION = "evidence-discovery-prompts.v45-method-only"
GROUNDING_EXACT_IDENTITY_CONTRACT_VERSION = (
    "evidence-discovery.grounding-exact-identity-contract.v3"
)
D_ADJUDICATION_MAX_PROMPT_TOKENS = 40_000
D_ADJUDICATION_CONTEXT_FRACTION = 0.65
D_ADJUDICATION_SYSTEM_SCHEMA_RESERVE_TOKENS = 4_000
D_ADJUDICATION_PROMPT_CHARACTERS_PER_TOKEN = 4


def _d_prompt_character_budget(runtime: Any) -> int:
    """Derive a conservative per-call D budget before the agent compact trigger."""

    config = getattr(runtime, "config", None)
    context_window_tokens = getattr(config, "context_window_tokens", None)
    if not isinstance(context_window_tokens, int) or context_window_tokens <= 0:
        prompt_tokens = D_ADJUDICATION_MAX_PROMPT_TOKENS
    else:
        available = (
            int(context_window_tokens * D_ADJUDICATION_CONTEXT_FRACTION)
            - MAX_STRUCTURED_OUTPUT_TOKENS
            - D_ADJUDICATION_SYSTEM_SCHEMA_RESERVE_TOKENS
        )
        prompt_tokens = max(
            1,
            min(D_ADJUDICATION_MAX_PROMPT_TOKENS, available),
        )
    return prompt_tokens * D_ADJUDICATION_PROMPT_CHARACTERS_PER_TOKEN


class ExactGroundingResponse(GroundingResponse):
    """Per-call grounding response bound to the supplied contract identity set.

    The runner specializes this Pydantic model for one method cell. Its
    authority is limited to exact contract-reference closure and structurally
    complete accounting for supplied cardinality contracts: grounding rows may
    reference supplied contracts or additional contracts declared in that same
    response, and every cardinality contract must receive one typed domain row.
    It does not select that domain or decide whether an obligation exists,
    whether a candidate is valid, or any W, D, L, publication, or external
    evaluation result.

    The supplied contract set may be empty when the NL-only stage finds no
    independently violable atomic contract. In that case, the only legal
    contract references are typed ``additional_contracts`` declared by the
    same grounding response.
    """

    expected_contract_ids: ClassVar[tuple[str, ...]] = ()
    expected_cardinality_contract_ids: ClassVar[tuple[str, ...]] = ()
    enforce_exact_identity_contract: ClassVar[bool] = False

    @model_validator(mode="after")
    def validate_exact_contract_reference_closure(self) -> ExactGroundingResponse:
        """Reject invented IDs and missing cardinality rows with correction text."""

        if not type(self).enforce_exact_identity_contract:
            return self
        known_ids = set(type(self).expected_contract_ids)
        known_ids.update(
            contract.contract_id for contract in self.additional_contracts
        )
        referenced_rows = [
            *(
                (f"semantic_bindings[{index}].contract_id", item.contract_id)
                for index, item in enumerate(self.semantic_bindings)
            ),
            *(
                (f"cardinality_bindings[{index}].contract_id", item.contract_id)
                for index, item in enumerate(self.cardinality_bindings)
            ),
            *(
                (f"candidates[{index}].contract_id", item.contract_id)
                for index, item in enumerate(self.candidates)
            ),
            *(
                (f"unresolved[{index}].contract_id", item.contract_id)
                for index, item in enumerate(self.unresolved)
            ),
        ]
        errors = [
            f"{path}={contract_id!r} is not a supplied contract or an "
            "additional_contracts row in this response"
            for path, contract_id in referenced_rows
            if contract_id not in known_ids
        ]
        if errors:
            raise ValueError(
                "exact grounding contract-reference closure failed; omit rows "
                "that do not correspond to a real contract, or return a complete "
                "typed additional_contracts row and reference its exact local ID:\n- "
                + "\n- ".join(errors)
                + "\nallowed supplied contract IDs="
                + repr(list(type(self).expected_contract_ids))
            )

        supplied_ids = set(type(self).expected_contract_ids)
        supplied_cardinality_ids = set(
            type(self).expected_cardinality_contract_ids
        )
        additional_property_by_id = {
            contract.contract_id: contract.property
            for contract in self.additional_contracts
        }
        required_cardinality_ids = supplied_cardinality_ids | {
            contract_id
            for contract_id, property_name in additional_property_by_id.items()
            if property_name == "cardinality"
        }
        actual_cardinality_ids = {
            binding.contract_id for binding in self.cardinality_bindings
        }
        missing_cardinality_ids = sorted(
            required_cardinality_ids - actual_cardinality_ids
        )
        non_cardinality_targets = sorted(
            contract_id
            for contract_id in actual_cardinality_ids
            if (
                contract_id in supplied_ids
                and contract_id not in supplied_cardinality_ids
            )
            or additional_property_by_id.get(contract_id) not in {
                None,
                "cardinality",
            }
        )
        if missing_cardinality_ids or non_cardinality_targets:
            errors = []
            if missing_cardinality_ids:
                errors.append(
                    "cardinality_bindings is missing one required exact/ambiguous/"
                    "unbound row for contract IDs="
                    + repr(missing_cardinality_ids)
                )
            if non_cardinality_targets:
                errors.append(
                    "cardinality_bindings targets supplied/additional contracts "
                    "whose property is not cardinality: "
                    + repr(non_cardinality_targets)
                )
            raise ValueError(
                "exact grounding cardinality coverage failed; return a complete "
                "replacement response retaining all valid rows and add exactly "
                "one typed binding row for every required cardinality contract:\n- "
                + "\n- ".join(errors)
            )
        return self


METHOD_SYSTEM_PROMPT = """The method is staged. Its public generation surface is the NL contract-extraction stage followed by two complementary discovery-grounding lenses that share one response schema and compact cross-view context. Use only the complete context manifest supplied to each stage. Never read evaluation ground truth, scores, reviewer examples, or previously generated reports. Do not emit W, D, or L levels. Every structured object must contain non-empty reason and basis. Write every generated title, statement, summary, reason, basis, and audit explanation in English; preserve non-English text only inside exact quotations or identifiers copied from supplied artifacts."""

def _prompt_schema_hash() -> str:
    """Hash every method prompt contract and response schema used by a run."""

    return _hash_json(
        {
            "version": PROMPT_SCHEMA_VERSION,
            "system_prompts": {
                "method_boundary": METHOD_SYSTEM_PROMPT,
                "contract": CONTRACT_SYSTEM_PROMPT,
                "discovery_grounding": DISCOVERY_GROUNDING_SYSTEM_PROMPT,
                "discovery_lenses": DISCOVERY_GROUNDING_AUDIT_LENSES,
                "d_adjudication": D_SYSTEM_PROMPT,
            },
            "schemas": {
                "nl_contract": NLContractResponse.model_json_schema(),
                "grounding": GroundingResponse.model_json_schema(),
                "grounding_exact_identity_contract": {
                    "version": GROUNDING_EXACT_IDENTITY_CONTRACT_VERSION,
                    "base_schema": ExactGroundingResponse.model_json_schema(),
                    "specialization": (
                        "Per method cell, supplied contract identities and the "
                        "cardinality-contract subset are closed; every cardinality "
                        "contract requires exactly one exact, ambiguous, or unbound "
                        "typed domain row in each complementary grounding lens. The "
                        "supplied set may be empty; then only same-response typed "
                        "additional contracts can be referenced."
                    ),
                },
                "d_adjudication": DAdjudicationResponse.model_json_schema(),
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
    reservation_limit = _structured_model_call_reservation_limit(
        transport_retries
    )
    structured_stage_deadline = _structured_stage_deadline_seconds(
        transport_retries
    )
    structured_wrapper_deadline = (
        structured_stage_deadline
        + STRUCTURED_WRAPPER_FINALIZATION_GRACE_SECONDS
    )
    return {
        "transport_retries": transport_retries,
        "transport_retry_delays_seconds": delays,
        "stream_first_byte_timeout_seconds": PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS,
        "provider_call_total_timeout_seconds": PROVIDER_CALL_DEADLINE_SECONDS,
        "structured_model_call_reservation_limit": reservation_limit,
        "structured_stage_retry_delay_budget_seconds": sum(delays),
        "structured_stage_finalization_grace_seconds": (
            STRUCTURED_STAGE_FINALIZATION_GRACE_SECONDS
        ),
        "structured_stage_timeout_seconds": structured_stage_deadline,
        "structured_stage_wrapper_finalization_grace_seconds": (
            STRUCTURED_WRAPPER_FINALIZATION_GRACE_SECONDS
        ),
        "structured_stage_wrapper_timeout_seconds": structured_wrapper_deadline,
        "structured_stage_timeout_formula": (
            "reservation_limit*provider_call_total_timeout_seconds"
            "+sum(transport_retry_delays_seconds)+finalization_grace_seconds"
        ),
        "non_stream_provider_timeout_seconds": PROVIDER_CALL_DEADLINE_SECONDS,
        "dead_structured_call_retries_after_provider_error": 1,
        "structured_stage_timeout_owner": "local_runtime",
        "structured_stage_timeout_outer_retry": False,
        "schema_and_non_provider_retries_billable": True,
        "unavailable_non_provider_usage": "cost_ineligible_not_zero",
        "provider_retry_exemption": "Only a failed provider attempt followed by an actual same-request retry is exempt; the successful attempt remains billable.",
        "reason": "The run uses in-place provider recovery without cold cell reruns.",
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
                "The run records the exact clean tracked repository revision used to construct method artifacts."
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
    rounds: int,
    selected_pair_ids: Sequence[str],
    scope: str,
    workers: int,
    transport_retries: int,
    streaming: bool,
    selection_preflight: dict[str, Any] | None,
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
        "rounds": rounds,
        "selected_pair_ids": list(selected_pair_ids),
        "scope": scope,
        "workers": workers,
        "transport_retries": transport_retries,
        "streaming": streaming,
        "selection_preflight": selection_preflight,
        "retry_policy": _retry_policy(transport_retries),
    }


def _load_selection_preflight(
    path: str | Path | None,
    *,
    selected_pair_ids: Sequence[str],
) -> dict[str, Any] | None:
    """Validate selection metadata without importing it into method execution."""

    if path is None:
        return None
    preflight_path = Path(path).expanduser().resolve()
    payload = json.loads(preflight_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("selection preflight must be a JSON object")
    claimed_hash = payload.get("artifact_hash")
    if not isinstance(claimed_hash, str):
        raise ValueError("selection preflight has no artifact_hash")
    unsigned = dict(payload)
    unsigned.pop("artifact_hash", None)
    computed_hash = _hash_json(unsigned)
    if claimed_hash != computed_hash:
        raise ValueError(
            f"selection preflight hash mismatch: claimed={claimed_hash} computed={computed_hash}"
        )
    preflight_pairs = tuple(payload.get("selected_pair_ids", ()))
    if preflight_pairs != tuple(selected_pair_ids):
        raise ValueError(
            "selection preflight pair order does not match the run's selected_pair_ids"
        )
    candidate_predicates = tuple(payload.get("candidate_predicates_e15", ()))
    if not isinstance(payload.get("schema"), str) or not candidate_predicates:
        raise ValueError("selection preflight is missing schema or E15 predicate set")
    return SelectionPreflightReference(
        artifact_schema=payload["schema"],
        artifact_path=str(preflight_path),
        artifact_hash=claimed_hash,
        selected_pair_ids=preflight_pairs,
        candidate_predicates_e15=candidate_predicates,
        reason="The run records the deterministic pair/predicate preflight used before provider execution; it is not supplied to method prompts.",
        basis="preflight artifact self-hash and exact selected-pair equality",
    ).model_dump(mode="json")


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
    rounds: int,
    selected_pair_ids: Sequence[str],
    workers: int,
    transport_retries: int,
    streaming: bool,
    selection_preflight: dict[str, Any] | None,
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
        rounds=rounds,
        selected_pair_ids=selected_pair_ids,
        scope=scope,
        workers=workers,
        transport_retries=transport_retries,
        streaming=streaming,
        selection_preflight=selection_preflight,
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

    existing_cells = any((output_root / "method").glob("*/round-*.json"))
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
        selection_preflight=selection_preflight,
        reason="This manifest freezes the current method code, registry, pair grid, transport policy, and resume identity before provider execution.",
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
    projection_version: str | None = None,
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
    if projection_version is not None:
        context_budget = context_budget.model_copy(
            update={"projection_version": projection_version}
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


_PREDICATE_PROPERTY_COMPATIBILITY: dict[str, frozenset[str]] = {
    "S1": frozenset({"element_declaration"}),
    "S2": frozenset({"transition_endpoints", "initial_entry"}),
    "S3": frozenset({"trigger_set"}),
    "S4": frozenset({"state_action"}),
    "S5": frozenset({"guard"}),
    "S6": frozenset({"effect"}),
    "G1": frozenset({"reachability"}),
    "G2": frozenset({"universal_reachability", "termination"}),
    "G3": frozenset({"route_avoidance"}),
    "G4": frozenset({"coaccessibility", "termination"}),
    "R1": frozenset({"event_consumption"}),
    "R2": frozenset({"state_after_stimulus"}),
    "R3": frozenset({"behavior_occurrence"}),
    "R4": frozenset({"state_retention"}),
    "V1": frozenset({"guard_disjointness"}),
    "V2": frozenset({"guard_completeness"}),
    "V3": frozenset({"bounded_response"}),
    "V4": frozenset({"deadlock_freedom"}),
    "V5": frozenset({"state_invariant"}),
}


def _apply_typed_predicate_boundary(
    pair: PairInput,
    candidate: CandidateIssue,
) -> CandidateIssue:
    """Downgrade a semantically mismatched executable claim to precise W1.

    This rule compares only typed contract properties, predicate IDs, and
    parsed transition fields. It never interprets candidate prose. The issue
    remains present; only the unsupported executable assertion is removed.
    """

    predicate_id = candidate.predicate_id
    if predicate_id is None:
        return candidate
    allowed_properties = _PREDICATE_PROPERTY_COMPATIBILITY.get(predicate_id)
    reason: str | None = None
    if allowed_properties is not None and candidate.property not in allowed_properties:
        reason = (
            f"Predicate {predicate_id} does not decide typed property "
            f"{candidate.property}; preserve the exact issue as predicate-null W1."
        )
    elif (
        predicate_id in {"S1", "S2"}
        and candidate.violation_direction == "extra"
    ):
        reason = (
            f"Predicate {predicate_id} proves positive existence but the typed "
            "candidate alleges extra behavior; the current compiler has no "
            "audited negated assertion for this claim."
        )
    elif predicate_id == "S2" and candidate.property == "initial_entry":
        inputs = candidate.predicate_inputs
        source = inputs.get("source")
        target = inputs.get("target")
        transition_hint = inputs.get("transition") or inputs.get("transition_ref")
        transition_ref = resolve_transition_ref(
            transition_hint if isinstance(transition_hint, str) else None,
            pair.model,
            source=source if isinstance(source, str) else None,
            target=target if isinstance(target, str) else None,
        )
        transition = pair.model.transition(transition_ref) if transition_ref else None
        if transition is not None and transition.guard is not None:
            reason = (
                "S2 proves that the pseudo-state endpoint edge exists, but it "
                "cannot decide the stronger default/unconditional initial-entry "
                "property of a present guarded edge."
            )
    if reason is None:
        return candidate
    return candidate.model_copy(
        update={
            "predicate_id": None,
            "predicate_inputs": {},
            "reason": candidate.reason + " " + reason,
            "basis": (
                candidate.basis
                + "; typed predicate/property compatibility and exact parsed transition fields"
            ),
        }
    )


def _enrich_candidate(candidate: CandidateIssue, binding: Any, pair: PairInput) -> CandidateIssue:
    if candidate.predicate_id is None:
        return candidate.model_copy(update={"predicate_inputs": {}})
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
    if (
        transition_ref is None
        and not transition_hint
        and candidate.predicate_id in {"S3", "S5", "S6"}
        and len(bound_transitions) == 1
    ):
        transition_ref = bound_transitions[0].ref
    # A predicate requiring one transition must receive one unambiguous
    # transition binding. Composite candidates remain W0 until the method names
    # the exact edge instead of silently selecting the first one.
    if transition_ref is not None:
        transition = pair.model.transition(transition_ref)
        if transition is not None:
            # Predicate inputs are executable fields, not provenance slots.
            # Once the predicate identifies one closed-model edge, overwrite
            # typed source/target/ref spellings with canonical FCSTM values.
            # S2 absence checks without a transition hint deliberately do not
            # infer a subject edge from supporting refs: their source/target
            # pair is the required edge that the backend must test.
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
    text = text.removeprefix("state:")
    return text.rsplit(".", 1)[-1]


def _endpoint_aliases_for_runner(value: Any) -> set[str]:
    """Return structural endpoint aliases for working-contract joins."""

    normalized = " ".join(str(value or "").strip().split())
    aliases = {normalized}
    if normalized.startswith("@initial:"):
        aliases.add("[*]")
        normalized = normalized[len("@initial:") :]
    normalized = normalized.lstrip("!")
    if normalized.startswith("state:"):
        normalized = normalized[len("state:") :]
    aliases.add(normalized)
    if "." in normalized:
        aliases.add(normalized.rsplit(".", 1)[-1])
    return {item for item in aliases if item}


def _model_ref_for_state(pair: PairInput, value: Any) -> str | None:
    stem = _endpoint_stem(value)
    matches = [
        state.ref
        for state in pair.model.states
        if state.name == stem or state.display_name == stem
    ]
    return matches[0] if len(matches) == 1 else None


def _identity_key(value: Any) -> str:
    """Normalize one structured identity for exact case/space comparison."""

    return " ".join(str(value or "").strip().split()).casefold()


def _model_ref_for_event(pair: PairInput, value: Any) -> str | None:
    """Resolve an event only when its structured name/display identity is unique."""

    key = _identity_key(value)
    if not key:
        return None
    matches = [
        event.ref
        for event in pair.model.events
        if _identity_key(event.name) == key
        or _identity_key(event.display_name) == key
    ]
    return matches[0] if len(matches) == 1 else None


def _working_contract_records(pair: PairInput) -> list[dict[str, Any]]:
    """Return mapping rows from the immutable working-contract artifact."""

    artifact = pair.working_contract
    if artifact is None:
        return []
    return [
        item
        for item in artifact.payload.get("elements", [])
        if isinstance(item, dict)
    ]


def _working_record_matches(record: Mapping[str, Any], raw: str) -> bool:
    """Match a raw identity against explicit working-contract identity fields."""

    return (
        record.get("element_id") == raw
        or raw in (record.get("source_refs") or [])
        or raw in (record.get("model_refs") or [])
    )


def _working_transition_ref(
    pair: PairInput,
    record: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
) -> str | None:
    """Resolve one working transition row through explicit endpoint metadata."""

    direct = [
        ref
        for ref in record.get("model_refs") or []
        if ref in pair.model.transition_refs
    ]
    if len(set(direct)) == 1:
        return direct[0]

    metadata = record.get("metadata")
    metadata = metadata if isinstance(metadata, Mapping) else {}
    semantic = record.get("semantic_fields")
    semantic = semantic if isinstance(semantic, Mapping) else {}

    # A protected transition segment carries the source transition ID but not
    # the source/target/event fields. Resolve its macro root first so a
    # segment never becomes an independent guessed carrier.
    source_transition_id = metadata.get("source_transition_id")
    if source_transition_id:
        roots = [
            item
            for item in records
            if item.get("element_id") == f"source:transition:{source_transition_id}"
            or (
                (item.get("metadata") or {}).get("transition_id")
                == source_transition_id
                and "transition_macro_root" in str(item.get("kind") or "")
            )
        ]
        root_refs = [
            ref
            for root in roots
            for ref in [_working_transition_ref(pair, root, records)]
            if ref is not None
        ]
        if len(set(root_refs)) == 1:
            return root_refs[0]
        if len(set(root_refs)) > 1:
            return None

    source = metadata.get("source") or semantic.get("source_endpoint")
    target = metadata.get("target") or semantic.get("target_endpoint")
    if source is None or target is None:
        return None

    candidates = [
        transition
        for transition in pair.model.transitions
        if _endpoint_aliases_for_runner(transition.source)
        & _endpoint_aliases_for_runner(str(source))
        and _endpoint_aliases_for_runner(transition.target)
        & _endpoint_aliases_for_runner(str(target))
    ]
    if len(candidates) == 1:
        return candidates[0].ref

    # Endpoint identity alone is intentionally insufficient when several
    # transitions share endpoints. A working-contract event interpretation is
    # a declared disambiguator, not a free-text similarity fallback.
    event_value = (
        metadata.get("raw_label")
        or metadata.get("event_interpretation")
        or semantic.get("raw_label")
        or semantic.get("event_interpretation")
    )
    event_ref = _model_ref_for_event(pair, event_value)
    event = next(
        (item for item in pair.model.events if item.ref == event_ref),
        None,
    )
    if event is not None:
        candidates = [
            transition
            for transition in candidates
            if event.name in transition.triggers
        ]
    return candidates[0].ref if len(candidates) == 1 else None


def _working_record_model_refs(
    pair: PairInput,
    record: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Project one working-contract row to unique closed ModelIR references."""

    kind = str(record.get("kind") or "")
    if "transition" in kind or str(record.get("element_id") or "").startswith(
        ("source:transition:", "compiler:transition_segment:")
    ):
        ref = _working_transition_ref(pair, record, records)
        return [ref] if ref is not None else []

    refs = [
        ref
        for ref in record.get("model_refs") or []
        if ref in pair.model.all_refs
    ]
    metadata = record.get("metadata")
    metadata = metadata if isinstance(metadata, Mapping) else {}
    semantic = record.get("semantic_fields")
    semantic = semantic if isinstance(semantic, Mapping) else {}

    # Event projections have a compiler-owned FCSTM identifier and may share
    # a name with a state (for example ``Intercepted``). Never interpret an
    # event projection's identifier as a state path.
    if "event" in kind:
        event_value = metadata.get("raw_label") or semantic.get("raw_label")
        event_ref = _model_ref_for_event(pair, event_value)
        if event_ref is not None:
            refs.append(event_ref)
        return list(dict.fromkeys(refs))

    state_path = metadata.get("fcstm_path") or semantic.get("fcstm_identifier")
    if state_path is not None:
        state_ref = _model_ref_for_state(pair, state_path)
        if state_ref is not None:
            refs.append(state_ref)
    return list(dict.fromkeys(refs))


def _resolve_working_contract_refs(
    pair: PairInput,
    *,
    element_ids: Sequence[str] = (),
    source_refs: Sequence[str] = (),
    model_refs: Sequence[str] = (),
) -> tuple[list[str], list[str]]:
    """Join explicit working-contract identities to closed ModelIR refs.

    The join accepts only declared mapping fields and unique ModelIR results.
    It does not compare free text, display labels, embeddings, or historical
    evaluation data.  The second return value contains unresolved model-side
    requests so callers can retain a W0/W1 audit disposition.
    """

    records = _working_contract_records(pair)
    resolved: list[str] = []
    unresolved: list[str] = []
    source_owned_unmapped: list[str] = []
    requests = [
        ("element", value) for value in element_ids
    ] + [
        ("source", value) for value in source_refs
    ] + [
        ("model", value) for value in model_refs
    ]
    seen_requests: set[tuple[str, str]] = set()
    for kind, raw_value in requests:
        raw = str(raw_value or "").strip()
        if not raw or (kind, raw) in seen_requests:
            continue
        seen_requests.add((kind, raw))
        if raw in pair.model.all_refs:
            if raw not in resolved:
                resolved.append(raw)
            continue
        matching_records = [
            record for record in records if _working_record_matches(record, raw)
        ]
        mapped = list(
            dict.fromkeys(
                ref
                for record in matching_records
                for ref in _working_record_model_refs(pair, record, records)
            )
        )
        if mapped:
            for ref in mapped:
                if ref not in resolved:
                    resolved.append(ref)
        elif raw.startswith(("source:", "macro:")):
            source_owned_unmapped.append(raw)
        elif kind != "source":
            unresolved.append(raw)
    if not resolved:
        unresolved.extend(source_owned_unmapped)
    return resolved, list(dict.fromkeys(unresolved))


def _resolved_exact_binding_refs(
    pair: PairInput,
    binding: Any,
) -> list[str]:
    """Project one exact grounding binding to closed ModelIR refs."""

    resolved, _ = _resolve_working_contract_refs(
        pair,
        element_ids=tuple(
            ref
            for ref in (binding.model_element_ref,)
            if ref
        ),
        source_refs=tuple(
            ref
            for ref in (binding.source_element_ref,)
            if ref
        ),
        model_refs=tuple(
            ref
            for ref in (binding.carrier_transition_ref,)
            if ref
        ),
    )
    return [ref for ref in resolved if ref in pair.model.all_refs]


def _mapped_model_refs(pair: PairInput, candidate: CandidateIssue) -> list[str]:
    """Translate source-owned grounding refs through the published mapping contract.

    Grounding sees both author-source and closed-model context.  The LLM may
    therefore return a source identity in ``element_refs`` even when its
    predicate inputs identify the corresponding FCSTM element.  The working
    contract is the explicit mapping authority; this helper only resolves
    structured IDs and endpoint fields and never performs textual similarity.
    """

    resolved, unresolved = _resolve_working_contract_refs(
        pair,
        element_ids=candidate.element_refs,
        source_refs=candidate.source_refs,
    )

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
    migrated_source_refs = [
        ref
        for ref in candidate.element_refs
        if ref.startswith(("source:", "macro:"))
    ]
    source_refs = list(
        dict.fromkeys([*candidate.source_refs, *migrated_source_refs])
    )
    return candidate.model_copy(
        update={"element_refs": refs, "source_refs": source_refs}
    )


def _normalize_grounding_exact_facts(
    pair: PairInput,
    response: GroundingResponse,
) -> tuple[GroundingResponse, list[dict[str, Any]]]:
    """Normalize exact mapped owner refs and remove refuted local dead ends.

    This is the deterministic counterpart of the grounding prompt's property
    boundary. It compares only typed source IDs, published mapping rows, exact
    model refs, candidate fields, and parsed transition endpoints. Raw provider
    output remains in the public LLM audit, while this normalized branch uses
    owned ModelIR refs for deterministic frontier execution.
    """

    normalized_cardinality_bindings: list[CardinalityDomainBinding] = []
    normalized_cardinality_count = 0
    source_inventory = pair.exact_source_inventory
    working_contract = pair.working_contract
    mapping_rows = [
        item
        for item in (
            working_contract.payload.get("elements", [])
            if working_contract is not None
            else []
        )
        if isinstance(item, dict)
    ]
    for cardinality_binding in response.cardinality_bindings:
        source_matches = [
            item
            for item in (source_inventory.states if source_inventory else ())
            if item.source_id == cardinality_binding.owner_source_id
        ]
        expected_element_id = (
            f"source:state:{cardinality_binding.owner_source_id}"
            if cardinality_binding.owner_source_id is not None
            else None
        )
        exact_mapping_rows = [
            item
            for item in mapping_rows
            if expected_element_id is not None
            and item.get("element_id") == expected_element_id
            and cardinality_binding.owner_model_ref
            in (item.get("model_refs") or [])
        ]
        mapped_owned_refs = {
            ref
            for item in exact_mapping_rows
            for mapped_ref in (item.get("model_refs") or [])
            if mapped_ref == cardinality_binding.owner_model_ref
            and (ref := _model_ref_for_state(pair, mapped_ref)) is not None
        }
        if len(source_matches) != 1 or len(mapped_owned_refs) != 1:
            normalized_cardinality_bindings.append(cardinality_binding)
            continue
        owned_ref = next(iter(mapped_owned_refs))
        if owned_ref == cardinality_binding.owner_model_ref:
            normalized_cardinality_bindings.append(cardinality_binding)
            continue
        normalized_cardinality_bindings.append(
            cardinality_binding.model_copy(
                update={
                    "owner_model_ref": owned_ref,
                    "basis": cardinality_binding.basis
                    + "; runner exact join: source inventory owner -> published working-contract model_ref -> unique owned ModelIR state ref",
                }
            )
        )
        normalized_cardinality_count += 1

    kept: list[CandidateIssue] = []
    diagnostics: list[dict[str, Any]] = []
    for candidate in response.candidates:
        normalized = _normalize_candidate_model_refs(pair, candidate)
        binding = bind_candidate(normalized, pair.model)
        bound_states = [
            state
            for state in pair.model.states
            if state.ref in binding.element_refs
        ]
        outgoing_by_state = {
            state.ref: [
                transition.ref
                for transition in pair.model.transitions
                if transition.source_ref == state.ref
            ]
            for state in bound_states
        }
        exact_local_progress = bool(
            binding.precise
            and normalized.property == "deadlock_freedom"
            and normalized.violation_direction == "dead_end"
            and bound_states
            and all(outgoing_by_state[state.ref] for state in bound_states)
        )
        if not exact_local_progress:
            kept.append(normalized)
            continue

        fact = {
            "contract_id": normalized.contract_id,
            "candidate_hash": _hash_json(normalized),
            "bound_state_refs": [state.ref for state in bound_states],
            # Keep the legacy display-keyed field for existing consumers. It is
            # audit presentation only; duplicate local names are never used by
            # the actual exact-progress decision.
            "outgoing_transition_refs": {
                state.name: outgoing_by_state[state.ref]
                for state in bound_states
            },
            "outgoing_transition_refs_by_state_ref": outgoing_by_state,
        }
        diagnostics.append(
            {
                "stage": "discovery_grounding",
                "lens": response.lens,
                "class": "exact_local_progress_satisfied",
                **fact,
                "reason": "Every exactly bound state in this dead_end claim has at least one native-projected outgoing transition, so unreachability cannot be relabeled as a local dead-end violation.",
                "basis": "typed deadlock_freedom/dead_end identity, exact binding refs, and pyfcstm native carrier endpoint projection",
            }
        )

    response_update: dict[str, Any] = {
        "cardinality_bindings": normalized_cardinality_bindings,
        "candidates": kept,
    }
    if normalized_cardinality_count:
        response_update.update(
            {
                "reason": response.reason
                + " Published representation owner refs were exactly joined to owned ModelIR refs before frontier execution.",
                "basis": response.basis
                + "; exact source inventory, working-contract mapping, and unique owned ModelIR ref join",
            }
        )
    if not diagnostics:
        return response.model_copy(update=response_update), []
    return (
        response.model_copy(
            update={
                **response_update,
                "reason": response_update.get("reason", response.reason)
                + " Exact local-progress satisfactions were normalized before execution.",
                "basis": response_update.get("basis", response.basis)
                + "; exact typed binding and owned ModelIR outgoing-transition check",
            }
        ),
        diagnostics,
    )


def _unresolved_exact_refs(
    pair: PairInput,
    grounding_responses: Sequence[GroundingResponse],
    contract_id: str,
) -> tuple[list[str], list[str], list[str]]:
    """Collect only exact typed refs for one unresolved contract.

    Grounding unresolved rows are not permission to guess from names.  A ref is
    admitted only when the grounding schema marks it ``exact`` and the ref is
    present in the closed ModelIR.  Conflicting exact refs for the same role
    are retained as an audit conflict and are excluded from the executable
    binding, which deterministically leaves the candidate at W0.
    """

    model_refs: list[str] = []
    source_refs: list[str] = []
    conflicts: list[str] = []
    model_ref_set = set(pair.model.all_refs)
    refs_by_role: dict[str, set[str]] = {}
    for response in grounding_responses:
        for binding in response.semantic_bindings:
            if binding.contract_id != contract_id or binding.status != "exact":
                continue
            exact_model_refs = [
                ref
                for ref in (binding.model_element_ref, binding.carrier_transition_ref)
                if ref is not None and ref in model_ref_set
            ]
            refs_by_role.setdefault(binding.role, set()).update(exact_model_refs)
            if binding.source_element_ref:
                source_refs.append(binding.source_element_ref)
    for role, refs in sorted(refs_by_role.items()):
        if len(refs) > 1:
            conflicts.append(f"role={role}; refs={sorted(refs)}")
            continue
        model_refs.extend(sorted(refs))
    return (
        list(dict.fromkeys(model_refs)),
        list(dict.fromkeys(source_refs)),
        conflicts,
    )


def _admit_grounding_unresolved(
    pair: PairInput,
    contracts_by_id: Mapping[str, NLContract],
    grounding_responses: Sequence[GroundingResponse],
    existing_candidates: Sequence[CandidateIssue],
) -> tuple[list[CandidateIssue], list[dict[str, Any]]]:
    """Publish every valid unresolved row as a W1/W0-auditable candidate.

    ``GroundingUnresolved`` is a sparse audit row, not a terminal drop.  When
    exact state/carrier refs exist, the candidate is predicate-null and binds
    those refs, so the compiler assigns W1.  When identity remains genuinely
    open, the same typed contract is retained with no guessed model ref and
    deterministic binding assigns W0.  Existing candidates win over a second
    candidate while the unresolved reason remains in this disposition log.
    """

    existing_ids = {candidate.contract_id for candidate in existing_candidates}
    unresolved_by_contract: dict[str, list[tuple[str, Any]]] = {}
    for response in grounding_responses:
        for unresolved in response.unresolved:
            unresolved_by_contract.setdefault(unresolved.contract_id, []).append(
                (response.lens, unresolved)
            )

    admitted: list[CandidateIssue] = []
    dispositions: list[dict[str, Any]] = []
    for contract_id in sorted(unresolved_by_contract):
        rows = unresolved_by_contract[contract_id]
        contract = contracts_by_id.get(contract_id)
        if contract is None:
            dispositions.append(
                {
                    "contract_id": contract_id,
                    "status": "unresolved_unknown_contract",
                    "reason": "The grounding unresolved row has no accepted typed contract and cannot be published as an issue.",
                    "basis": "exact contract-ID membership check",
                }
            )
            continue
        row_reasons = [f"{lens}: {row.reason}" for lens, row in rows]
        row_bases = [f"{lens}: {row.basis}" for lens, row in rows]
        model_refs, binding_source_refs, conflicts = _unresolved_exact_refs(
            pair, grounding_responses, contract_id
        )
        source_refs = list(
            dict.fromkeys([*contract.source_refs, *binding_source_refs])
        )
        cardinality_rows = [
            binding
            for response in grounding_responses
            for binding in response.cardinality_bindings
            if binding.contract_id == contract_id
        ]
        for binding in cardinality_rows:
            if binding.owner_source_id:
                source_refs.append(f"source:state:{binding.owner_source_id}")
            if (
                binding.owner_model_ref
                and binding.owner_model_ref in pair.model.all_refs
                and binding.owner_model_ref not in model_refs
            ):
                model_refs.append(binding.owner_model_ref)
        source_refs = list(dict.fromkeys(source_refs))
        cardinality_context = ""
        if contract.cardinality_requirement is not None:
            requirement = contract.cardinality_requirement
            cardinality_context = (
                f" required_count={requirement.required_count};"
                f" member_domain={requirement.member_domain};"
                f" scope_concept={requirement.scope_concept};"
                f" member_concept={requirement.member_concept};"
                f" alternative_readings={[row.alternative_reading for row in cardinality_rows if row.alternative_reading]}"
            )
        binding_status = "exact_refs" if model_refs and not conflicts else "identity_unresolved"
        if contract_id in existing_ids:
            dispositions.append(
                {
                    "contract_id": contract_id,
                    "status": "existing_candidate_preserved",
                    "binding_status": binding_status,
                    "model_refs": model_refs,
                    "conflicts": conflicts,
                    "reason": "An existing candidate already carries this exact typed contract; unresolved rows were retained as supporting audit facts.",
                    "basis": "; ".join(row_bases),
                }
            )
            continue
        candidate = CandidateIssue(
            contract_id=contract.contract_id,
            locus_kind=contract.locus_kind,
            locus_names=contract.locus_names,
            property=contract.property,
            violation_direction=contract.violation_direction,
            evidence_types=tuple(
                dict.fromkeys([*contract.evidence_types, "semantic_comparison"])
            ),
            title=f"Grounding remains unresolved for {contract.scope}",
            requirement_quote=contract.quote,
            predicate_id=None,
            predicate_inputs={},
            element_refs=model_refs,
            source_refs=source_refs,
            expected=contract.normative_statement,
            observed=(
                "The grounding lens did not close this typed obligation."
                f"{cardinality_context}"
            ),
            strongest_rebuttal=(
                "A complete exact binding or a typed satisfying fact could resolve the obligation;"
                " no model identity was inferred from names or display text."
            ),
            reason=(
                "The grounding response explicitly retained this contract as unresolved;"
                " the method preserves it instead of silently dropping the candidate. "
                + " | ".join(row_reasons)
            ),
            basis=(
                f"contract={contract.contract_id}; binding_status={binding_status}; "
                f"model_refs={model_refs}; conflicts={conflicts}; "
                + "; ".join(row_bases)
            ),
        )
        admitted.append(candidate)
        dispositions.append(
            {
                "contract_id": contract_id,
                "status": "admitted_w1" if binding_status == "exact_refs" else "admitted_w0",
                "binding_status": binding_status,
                "model_refs": model_refs,
                "source_refs": source_refs,
                "conflicts": conflicts,
                "candidate_property": contract.property,
                "reason": candidate.reason,
                "basis": candidate.basis,
            }
        )
    return admitted, dispositions


def _admit_frontier_unresolved(
    pair: PairInput,
    contracts_by_id: Mapping[str, NLContract],
    frontier_batch: FrontierBatch,
    existing_candidates: Sequence[CandidateIssue],
) -> tuple[list[CandidateIssue], list[dict[str, Any]]]:
    """Publish unresolved deterministic checks as W1/W0 audit candidates.

    Frontier checks are complete deterministic receipts, but an unresolved check
    must not disappear merely because it did not form a normal frontier
    obligation. Exact closed-model refs produce a predicate-null W1 candidate;
    partial or absent identity produces a predicate-null W0 candidate with no
    guessed model carrier.
    """

    checks_by_contract: dict[str, list[Any]] = {}
    for check in frontier_batch.checks:
        if check.status != "unresolved":
            continue
        for contract_id in check.source_contract_ids:
            checks_by_contract.setdefault(contract_id, []).append(check)

    admitted: list[CandidateIssue] = []
    dispositions: list[dict[str, Any]] = []
    existing_by_contract = {candidate.contract_id for candidate in existing_candidates}
    for contract_id in sorted(checks_by_contract):
        checks = checks_by_contract[contract_id]
        contract = contracts_by_id.get(contract_id)
        if contract is None:
            dispositions.append(
                {
                    "contract_id": contract_id,
                    "status": "frontier_unresolved_unknown_contract",
                    "check_ids": [check.check_id for check in checks],
                    "reason": "The unresolved frontier check has no accepted typed contract, so no candidate can be published without inventing its semantic identity.",
                    "basis": "exact frontier source_contract_ids membership",
                }
            )
            continue

        raw_model_refs = list(
            dict.fromkeys(ref for check in checks for ref in check.model_refs)
        )
        valid_model_refs = [
            ref for ref in raw_model_refs if ref in pair.model.all_refs
        ]
        exact_model_refs = bool(raw_model_refs) and (
            valid_model_refs == raw_model_refs
        )
        source_refs = list(
            dict.fromkeys(
                [
                    *contract.source_refs,
                    *[ref for check in checks for ref in check.source_refs],
                ]
            )
        )
        check_reasons = [
            f"{check.kind}/{check.check_id}: {check.reason}" for check in checks
        ]
        check_bases = [
            f"{check.kind}/{check.check_id}: {check.basis}" for check in checks
        ]
        binding_status = "exact_refs" if exact_model_refs else "identity_unresolved"
        if contract_id in existing_by_contract:
            dispositions.append(
                {
                    "contract_id": contract_id,
                    "status": "existing_candidate_preserved_with_frontier_audit",
                    "binding_status": binding_status,
                    "model_refs": valid_model_refs,
                    "raw_model_refs": raw_model_refs,
                    "check_ids": [check.check_id for check in checks],
                    "reason": "An existing candidate already carries this exact typed contract; unresolved frontier checks remain supporting audit and do not create a duplicate dossier.",
                    "basis": "; ".join(check_bases),
                }
            )
            continue

        candidate = CandidateIssue(
            contract_id=contract.contract_id,
            locus_kind=contract.locus_kind,
            locus_names=contract.locus_names,
            property=contract.property,
            violation_direction=contract.violation_direction,
            evidence_types=tuple(
                dict.fromkeys(
                    [
                        *contract.evidence_types,
                        "closed_model_inventory",
                        "semantic_comparison",
                    ]
                )
            ),
            title=f"Deterministic {checks[0].kind} frontier remains unresolved for {contract.scope}",
            requirement_quote=contract.quote,
            predicate_id=None,
            predicate_inputs={},
            element_refs=valid_model_refs if exact_model_refs else [],
            source_refs=source_refs,
            expected=contract.normative_statement,
            observed="The deterministic frontier retained an unresolved check instead of selecting a model identity or silently dropping the obligation.",
            strongest_rebuttal="A later exact owner/carrier binding could close this check; no identity was inferred from names, display text, or an incomplete ref set.",
            reason=(
                "The deterministic frontier explicitly retained this typed obligation as unresolved. "
                + " | ".join(check_reasons)
            ),
            basis=(
                f"contract={contract.contract_id}; binding_status={binding_status}; "
                f"model_refs={valid_model_refs}; raw_model_refs={raw_model_refs}; "
                + "; ".join(check_bases)
            ),
        )
        admitted.append(candidate)
        dispositions.append(
            {
                "contract_id": contract_id,
                "status": "admitted_w1" if exact_model_refs else "admitted_w0",
                "binding_status": binding_status,
                "model_refs": valid_model_refs,
                "raw_model_refs": raw_model_refs,
                "check_ids": [check.check_id for check in checks],
                "candidate_property": contract.property,
                "reason": candidate.reason,
                "basis": candidate.basis,
            }
        )
    return admitted, dispositions


def _preflight_existing_endpoint_candidates(
    pair: PairInput,
    candidates: Sequence[CandidateIssue],
    contracts_by_id: Mapping[str, NLContract],
) -> tuple[list[CandidateIssue], list[dict[str, Any]]]:
    """Prevent a missing-edge claim when an exact ordinary carrier exists.

    This is a typed endpoint check only.  It distinguishes ordinary transition
    carriers from owner-local initial edges by requiring the candidate contract
    to provide exact source and target hints and by checking the parsed
    transition inventory directly.  Labels, display text, and route tokens do
    not participate in the decision.
    """

    retained: list[CandidateIssue] = []
    dispositions: list[dict[str, Any]] = []
    for candidate in candidates:
        contract = contracts_by_id.get(candidate.contract_id)
        if not (
            contract is not None
            and contract.property == "transition_endpoints"
            and contract.expected_direction == "must_exist"
            and contract.violation_direction == "missing"
        ):
            retained.append(candidate)
            continue
        source_hints = [hint for hint in contract.binding_hints if hint.role == "source"]
        target_hints = [hint for hint in contract.binding_hints if hint.role == "target"]
        source_ref = resolve_state_ref(source_hints[0].value, pair.model) if len(source_hints) == 1 else None
        target_ref = resolve_state_ref(target_hints[0].value, pair.model) if len(target_hints) == 1 else None
        carriers = [
            transition
            for transition in pair.model.transitions
            if source_ref is not None
            and target_ref is not None
            and transition.source_ref == source_ref
            and transition.target_ref == target_ref
        ]
        if not carriers:
            retained.append(candidate)
            continue
        carrier_refs = [transition.ref for transition in carriers]
        dispositions.append(
            {
                "contract_id": candidate.contract_id,
                "candidate_title": candidate.title,
                "status": "suppressed_existing_endpoint",
                "carrier_refs": carrier_refs,
                "reason": "The exact ordinary source-to-target transition exists in the native FCSTM projection, so a missing-transition claim is not publishable.",
                "basis": f"source_ref={source_ref}; target_ref={target_ref}; carrier_refs={carrier_refs}; native authored-carrier preflight",
            }
        )
    return retained, dispositions


def _normalize_state_retention_carriers(
    pair: PairInput,
    candidates: Sequence[CandidateIssue],
    contracts_by_id: Mapping[str, NLContract],
) -> tuple[list[CandidateIssue], list[dict[str, Any]]]:
    """Attach an exact hierarchical exit carrier to state-retention claims."""

    retained: list[CandidateIssue] = []
    dispositions: list[dict[str, Any]] = []
    inventory = pair.exact_source_inventory
    if inventory is None:
        return list(candidates), dispositions
    try:
        native_document = load_native_document(pair.model.source_text)
    except Exception as exc:  # noqa: BLE001 - retain precise candidates for W1 degradation upstream.
        return list(candidates), [
            {
                "status": "retention_carrier_native_load_failed",
                "reason": "The closed FCSTM artifact could not be loaded through pyfcstm, so no retention carrier was inferred.",
                "basis": f"pyfcstm native load; exception={type(exc).__name__}: {exc}",
            }
        ]

    for candidate in candidates:
        contract = contracts_by_id.get(candidate.contract_id)
        if contract is None or contract.property != "state_retention":
            retained.append(candidate)
            continue
        state_refs = [
            ref
            for ref in candidate.element_refs
            if any(state.ref == ref for state in pair.model.states)
        ]
        if not state_refs:
            for hint in contract.binding_hints:
                if hint.role not in {"state", "owner", "scope"}:
                    continue
                ref = resolve_state_ref(hint.value, pair.model)
                if ref is not None:
                    state_refs.append(ref)
        state_refs = list(dict.fromkeys(state_refs))
        if len(state_refs) != 1:
            retained.append(candidate)
            continue
        state = next(item for item in pair.model.states if item.ref == state_refs[0])
        if state.parent_ref is None:
            retained.append(candidate)
            continue
        source_rows = [
            row
            for row in inventory.transitions
            if resolve_state_ref(_endpoint_stem(row.source), pair.model) == state.ref
            and resolve_state_ref(_endpoint_stem(row.target), pair.model)
            == state.parent_ref
        ]
        if len(source_rows) != 1:
            retained.append(candidate)
            continue
        source_row = source_rows[0]
        def carrier_token(value: str | None) -> str:
            return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())

        source_event = carrier_token(source_row.event)
        exit_rows = [
            row
            for row in pair.model.transitions
            if row.source_ref == state.ref
            and row.target_ref is None
            and source_event
            and (
                (native_carrier := transition_by_reference(native_document, row.ref))
                is not None
            )
            and any(
                carrier_token(event.name) == source_event
                for event in native_carrier.events
            )
        ]
        parent_rows = []
        if len(exit_rows) == 1:
            exit_carrier = transition_by_reference(native_document, exit_rows[0].ref)
            assignment_pairs = (
                native_assignment_pairs(exit_carrier)
                if exit_carrier is not None
                else frozenset()
            )
            parent_rows = [
                row
                for row in pair.model.transitions
                if row.source_ref == state.parent_ref
                and row.target_ref == state.parent_ref
                and (
                    (native_carrier := transition_by_reference(native_document, row.ref))
                    is not None
                )
                and not native_carrier.events
                and bool(
                    assignment_pairs
                    & native_guard_equality_pairs(native_carrier)
                )
            ]
        model_rows = [*exit_rows, *parent_rows]
        if len(source_rows) != 1 or len(model_rows) not in {1, 2}:
            retained.append(candidate)
            dispositions.append(
                {
                    "contract_id": candidate.contract_id,
                    "candidate_title": candidate.title,
                    "status": "retention_carrier_unresolved",
                    "source_transition": f"{source_row.source}->{source_row.target}",
                    "source_transition_id": source_row.transition_id,
                    "model_candidate_refs": [row.ref for row in model_rows],
                    "reason": "The source retention edge did not join to one exact closed-model carrier or one exact route continuation.",
                    "basis": "exact source endpoint, normalized event token, and route-controller guard join",
                }
            )
            continue
        parent = next((item for item in pair.model.states if item.ref == state.parent_ref), None)
        element_refs = list(
            dict.fromkeys(
                [
                    *candidate.element_refs,
                    state.ref,
                    *([parent.ref] if parent is not None else []),
                    *[row.ref for row in model_rows],
                ]
            )
        )
        retained.append(
            candidate.model_copy(
                update={
                    "element_refs": element_refs,
                    "source_refs": list(
                        dict.fromkeys([*candidate.source_refs, source_row.raw_ref])
                    ),
                    "observed": (
                        candidate.observed
                        + f" Exact retention carrier is {source_row.source}->{source_row.target} "
                        f"with closed-model carrier chain {[row.ref for row in model_rows]}."
                    ),
                    "reason": (
                        candidate.reason
                        + " The exact source inventory and closed model both retain the state-to-owner carrier, including its deterministic route continuation."
                    ),
                    "basis": (
                        candidate.basis
                        + f"; source_transition={source_row.transition_id}; model_transitions={[row.ref for row in model_rows]}; "
                        "hierarchical retention-carrier normalization via pyfcstm native event, assignment, and guard-AST join"
                    ),
                }
            )
        )
        dispositions.append(
            {
                "contract_id": candidate.contract_id,
                "candidate_title": candidate.title,
                "status": "normalized_exact_retention_carrier",
                "state_ref": state.ref,
                "source_transition_id": source_row.transition_id,
                "source_transition": f"{source_row.source}->{source_row.target}",
                "model_transition_refs": [row.ref for row in model_rows],
                "reason": "The state-retention candidate now preserves the exact source-to-owner carrier and its native closed-model exit/continuation carrier chain.",
                "basis": "exact source inventory, native parent identity, normalized event identity, and unique pyfcstm effect/guard AST route continuation",
            }
        )
    return retained, dispositions


def _preflight_synthetic_root_wrapper_reachability(
    pair: PairInput,
    candidates: Sequence[CandidateIssue],
) -> tuple[list[CandidateIssue], list[dict[str, Any]]]:
    """Do not transfer a generated root-wrapper diagnostic to a reachable child."""

    facts = pair.inspection_facts
    root_ref = facts.machine_root_ref if facts else None
    reachable_refs = set(facts.reachable_state_refs) if facts else set()
    if root_ref is None or not reachable_refs:
        return list(candidates), []

    retained: list[CandidateIssue] = []
    dispositions: list[dict[str, Any]] = []
    for candidate in candidates:
        source_values = candidate.predicate_inputs.get("source")
        source_values = (
            list(source_values)
            if isinstance(source_values, (list, tuple))
            else [source_values]
        )
        if not (
            candidate.property == "reachability"
            and candidate.violation_direction == "unreachable"
            and candidate.predicate_id == "G1"
            and root_ref in source_values
        ):
            retained.append(candidate)
            continue
        target_values = candidate.predicate_inputs.get("target")
        target_values = (
            list(target_values)
            if isinstance(target_values, (list, tuple))
            else [target_values]
        )
        target_states = []
        for value in target_values:
            if not isinstance(value, str):
                continue
            state = next(
                (item for item in pair.model.states if item.ref == value),
                None,
            )
            if state is None:
                ref = resolve_state_ref(value, pair.model)
                state = next(
                    (item for item in pair.model.states if item.ref == ref),
                    None,
                )
            if state is not None:
                target_states.append(state)
        initial_rows = []
        if pair.exact_source_inventory is not None:
            target_names = {state.name for state in target_states}
            initial_rows = [
                item
                for item in pair.exact_source_inventory.transitions
                if item.source.startswith("@initial:")
                and _endpoint_stem(item.target) in target_names
            ]
        if (
            not target_states
            or any(state.ref not in reachable_refs for state in target_states)
            or not initial_rows
        ):
            retained.append(candidate)
            continue
        dispositions.append(
            {
                "contract_id": candidate.contract_id,
                "candidate_title": candidate.title,
                "status": "suppressed_synthetic_root_wrapper_projection",
                "root_wrapper_ref": root_ref,
                "reachable_target_refs": [state.ref for state in target_states],
                "source_initial_refs": [item.raw_ref for item in initial_rows],
                "reason": "The G1 source is the compiler-owned machine wrapper, while the exact target is reached by a supplied top-level initial transition and is marked reachable by the owned hierarchical projection.",
                "basis": "InspectionEquivalentFacts.machine_root_ref/reachable_state_refs plus exact author-source initial-transition inventory",
            }
        )
    return retained, dispositions


def _merge_grounding_contracts(
    pair: PairInput,
    contracts: NLContractResponse,
    branches: Sequence[GroundingResponse],
) -> tuple[dict[str, NLContract], list[dict[str, Any]]]:
    """Merge runner-canonicalized grounding contracts by complete typed identity."""

    merged = {contract.contract_id: contract for contract in contracts.contracts}
    supplied_segment_ids = {segment.segment_id for segment in pair.nl_segments}
    semantic_keys = {
        contract.contract_id: contract_semantic_key(contract) for contract in contracts.contracts
    }
    diagnostics: list[dict[str, Any]] = []

    for branch in branches:
        for contract in branch.additional_contracts:
            diagnostic_base = {
                "stage": "discovery_grounding",
                "lens": branch.lens,
                "contract_id": contract.contract_id,
                "segment_id": contract.segment_id,
            }
            if contract.segment_id not in supplied_segment_ids:
                diagnostics.append(
                    {
                        **diagnostic_base,
                        "class": "unknown_additional_contract_segment",
                        "reason": "The branch-local contract names a segment ID absent from the supplied numbered NL artifact.",
                        "basis": "exact segment-ID membership check without text interpretation",
                    }
                )
                continue
            expected_id = canonical_contract_id(contract)
            if contract.contract_id != expected_id:
                diagnostics.append(
                    {
                        **diagnostic_base,
                        "class": "noncanonical_additional_contract_id",
                        "expected_contract_id": expected_id,
                        "reason": "The additional contract reached merge without runner-authoritative typed identity normalization.",
                        "basis": "exact canonical ID recomputation from ContractSemanticKey",
                    }
                )
                continue
            key = contract_semantic_key(contract)
            existing = merged.get(contract.contract_id)
            if existing is None:
                merged[contract.contract_id] = contract
                semantic_keys[contract.contract_id] = key
                continue
            if semantic_keys[contract.contract_id] == key:
                # The first normalized row is the execution projection. Both lens
                # versions, including distinct reason/basis, remain in stage audit.
                continue
            diagnostics.append(
                {
                    **diagnostic_base,
                    "class": "canonical_contract_hash_collision",
                    "reason": "Different typed semantic keys produced one canonical ID; the additional row was not admitted.",
                    "basis": "exact canonical ID equality and ContractSemanticKey inequality",
                }
            )

    known_ids = set(merged)
    for branch in branches:
        for binding in branch.semantic_bindings:
            if binding.contract_id not in known_ids:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "lens": branch.lens,
                        "class": "unknown_semantic_binding_contract_id",
                        "contract_id": binding.contract_id,
                        "binding_id": binding.binding_id,
                        "reason": "The semantic binding does not name a supplied or accepted branch-local contract.",
                        "basis": "exact contract-ID membership check without semantic inference",
                    }
                )
        for binding in branch.cardinality_bindings:
            if binding.contract_id not in known_ids:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "lens": branch.lens,
                        "class": "unknown_cardinality_binding_contract_id",
                        "contract_id": binding.contract_id,
                        "binding_id": binding.binding_id,
                        "reason": "The cardinality domain binding does not name a supplied or accepted branch-local cardinality contract.",
                        "basis": "exact contract-ID membership check without semantic inference",
                    }
                )
        for unresolved in branch.unresolved:
            if unresolved.contract_id not in known_ids:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "lens": branch.lens,
                        "class": "unknown_unresolved_contract_id",
                        "contract_id": unresolved.contract_id,
                        "reason": "The sparse unresolved row does not name a supplied or accepted branch-local contract.",
                        "basis": "exact contract-ID membership check without semantic inference",
                    }
                )
        for candidate in branch.candidates:
            if candidate.contract_id not in known_ids:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "lens": branch.lens,
                        "class": "unknown_candidate_contract_id",
                        "contract_id": candidate.contract_id,
                        "candidate_hash": _hash_json(candidate),
                        "reason": "The candidate does not name a supplied or accepted branch-local contract and will remain imprecisely bound.",
                        "basis": "exact contract-ID membership check; downstream W0/D_UNRESOLVED boundary",
                    }
                )
    return merged, diagnostics


def _prepare_candidate(
    pair: PairInput,
    candidate: CandidateIssue,
    round_index: int,
    index: int,
    contracts_by_id: Mapping[str, NLContract] | None = None,
) -> dict[str, Any]:
    """Bind, compile, and execute once before the separate semantic D call."""

    obligation_id = f"{pair.pair_id}:r{round_index}:i{index}"
    candidate = _normalize_candidate_model_refs(pair, candidate)
    candidate = _apply_typed_predicate_boundary(pair, candidate)
    binding = bind_candidate(candidate, pair.model)
    if contracts_by_id is not None:
        contract = contracts_by_id.get(candidate.contract_id)
        mismatch_fields: list[str] = []
        if contract is None:
            mismatch_fields.append("contract_id")
        else:
            if candidate.locus_kind != contract.locus_kind:
                mismatch_fields.append("locus_kind")
            if tuple(candidate.locus_names) != tuple(contract.locus_names):
                mismatch_fields.append("locus_names")
            if candidate.property != contract.property:
                mismatch_fields.append("property")
            if candidate.violation_direction != contract.violation_direction:
                mismatch_fields.append("violation_direction")
        if mismatch_fields:
            binding = binding.model_copy(
                update={
                    "precise": False,
                    "reason": "The candidate does not preserve the exact typed semantic key of one supplied atomic NL contract.",
                    "basis": "exact contract ID and typed locus/property/direction comparison; mismatched fields: "
                    + ", ".join(mismatch_fields)
                    + "; W0 and D_UNRESOLVED are required",
                }
            )
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
    except Exception as exc:  # noqa: BLE001 - backend failures become structured uncertainty
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


def _materialize_exact_s2_inventory_candidates(
    pair: PairInput,
    contracts: NLContractResponse,
    llm_candidates: list[CandidateIssue],
    source_transition_closures: Mapping[
        str, SourceTransitionClosureReceipt
    ] | None = None,
) -> tuple[list[CandidateIssue], list[dict[str, Any]]]:
    """Compile exact missing-edge contracts that LLM output cannot suppress."""

    materialized: list[CandidateIssue] = []
    receipts: list[dict[str, Any]] = []
    for contract in contracts.contracts:
        if (
            contract.property != "transition_endpoints"
            or contract.expected_direction != "must_exist"
        ):
            continue
        closure = (source_transition_closures or {}).get(contract.contract_id)
        if closure is not None and closure.status == "satisfied":
            continue
        source_hints = [
            hint for hint in contract.binding_hints if hint.role == "source"
        ]
        target_hints = [
            hint for hint in contract.binding_hints if hint.role == "target"
        ]
        if len(source_hints) != 1 or len(target_hints) != 1:
            continue
        source_ref = resolve_state_ref(source_hints[0].value, pair.model)
        target_ref = resolve_state_ref(target_hints[0].value, pair.model)
        if source_ref is None or target_ref is None:
            continue
        source_state = next(
            (state for state in pair.model.states if state.ref == source_ref), None
        )
        target_state = next(
            (state for state in pair.model.states if state.ref == target_ref), None
        )
        if source_state is None or target_state is None:
            continue
        if any(
            transition.source_ref == source_ref
            and transition.target_ref == target_ref
            for transition in pair.model.transitions
        ):
            continue
        already_exact = False
        for candidate in llm_candidates:
            if (
                candidate.contract_id != contract.contract_id
                or candidate.predicate_id != "S2"
                or candidate.predicate_inputs.get("source") != source_state.name
                or candidate.predicate_inputs.get("target") != target_state.name
            ):
                continue
            binding = bind_candidate(candidate, pair.model)
            if binding.precise and {source_ref, target_ref} <= set(
                binding.element_refs
            ):
                already_exact = True
                break
        if already_exact:
            continue
        source_refs = list(contract.source_refs)
        for hint in (*source_hints, *target_hints):
            if hint.source_ref and hint.source_ref not in source_refs:
                source_refs.append(hint.source_ref)
        evidence_types = list(contract.evidence_types)
        for evidence_type in ("closed_model_inventory", "transition_fact"):
            if evidence_type not in evidence_types:
                evidence_types.append(evidence_type)
        candidate = CandidateIssue(
            contract_id=contract.contract_id,
            locus_kind=contract.locus_kind,
            locus_names=contract.locus_names,
            property=contract.property,
            violation_direction=contract.violation_direction,
            evidence_types=tuple(evidence_types),
            title=(
                f"Required transition {source_state.name} -> "
                f"{target_state.name} is absent"
            ),
            requirement_quote=contract.quote,
            predicate_id="S2",
            predicate_inputs={
                "source": source_state.name,
                "target": target_state.name,
                "scope": "closed_fcstm",
            },
            element_refs=[source_ref, target_ref],
            source_refs=source_refs,
            expected=contract.normative_statement,
            observed=(
                "The complete closed ModelIR transition inventory contains no "
                f"edge from {source_state.name} to {target_state.name}."
            ),
            strongest_rebuttal=(
                "No edge with different endpoints satisfies this exact typed "
                "source-target obligation."
            ),
            reason=(
                "The LLM-extracted typed contract supplies one source and one "
                "target; both resolve uniquely, and the complete ModelIR has no "
                "transition with that exact ordered endpoint pair."
            ),
            basis=(
                f"contract={contract.contract_id}; source_ref={source_ref}; "
                f"target_ref={target_ref}; model_algorithm={pair.model.algorithm_version}; "
                f"model_hash={pair.hashes['fcstm']}"
            ),
        )
        materialized.append(candidate)
        receipts.append(
            {
                "contract_id": contract.contract_id,
                "predicate_id": "S2",
                "source": source_state.name,
                "target": target_state.name,
                "element_refs": [source_ref, target_ref],
                "model_hash": pair.hashes["fcstm"],
                "reason": candidate.reason,
                "basis": candidate.basis,
            }
        )
    return materialized, receipts


def _exact_grounding_model_refs(
    pair: PairInput,
    grounding_responses: Sequence[GroundingResponse],
    contract_id: str,
) -> list[str]:
    """Collect unique exact closed-model refs for one grounded contract.

    This helper is deliberately limited to ``SemanticBinding.status=exact``.
    It does not resolve names, source IDs, or display labels, so an execution
    probe can never manufacture a carrier from an ambiguous grounding row.
    """

    refs: list[str] = []
    for response in grounding_responses:
        for binding in response.semantic_bindings:
            if binding.contract_id != contract_id or binding.status != "exact":
                continue
            for ref in _resolved_exact_binding_refs(pair, binding):
                if ref not in refs:
                    refs.append(ref)
    return refs


def _s1_probe_descriptor(pair: PairInput, model_ref: str) -> tuple[str, str] | None:
    """Return the frozen S1 kind and declaration identity for one exact ref."""

    state = next((item for item in pair.model.states if item.ref == model_ref), None)
    if state is not None:
        return "state", state.name
    event = next((item for item in pair.model.events if item.ref == model_ref), None)
    if event is not None:
        return "event", event.name
    transition = next(
        (item for item in pair.model.transitions if item.ref == model_ref), None
    )
    if transition is not None:
        return "transition", transition.ref
    return None


def _working_event_transition_context(
    pair: PairInput,
    event_ref: str,
) -> tuple[set[str], set[str], list[str]]:
    """Return transitions linked to an event projection through macro IDs.

    The working contract is the only authority for this join. A transition
    segment is resolved through its protected macro root, and an ambiguous
    endpoint/event mapping contributes no carrier instead of selecting a first
    row.
    """

    records = _working_contract_records(pair)
    event_rows = [
        record
        for record in records
        if "event" in str(record.get("kind") or "")
        and event_ref in _working_record_model_refs(pair, record, records)
    ]
    macro_ids = {
        macro_id
        for record in event_rows
        for macro_id in (record.get("macro_ids") or [])
    }
    transition_refs: set[str] = set()
    source_refs: list[str] = []
    for record in records:
        record_macros = set(record.get("macro_ids") or [])
        if not macro_ids.intersection(record_macros):
            continue
        if "transition" not in str(record.get("kind") or "") and not str(
            record.get("element_id") or ""
        ).startswith(("source:transition:", "compiler:transition_segment:")):
            continue
        ref = _working_transition_ref(pair, record, records)
        if ref is not None:
            transition_refs.add(ref)
        for source_ref in record.get("source_refs") or []:
            if source_ref not in source_refs:
                source_refs.append(source_ref)
    return transition_refs, macro_ids, source_refs


def _materialize_deterministic_execution_probes(
    pair: PairInput,
    contracts_by_id: Mapping[str, NLContract],
    grounding_responses: Sequence[GroundingResponse],
    existing_candidates: Sequence[CandidateIssue],
    transition_groups: Sequence[NLTransitionGroup] = (),
    frontier_batch: FrontierBatch | None = None,
) -> tuple[list[CandidateIssue], dict[str, NLContract], list[dict[str, Any]]]:
    """Create executable probes from exact method-owned bindings only.

    Probes are audit executions, not extra obligations.  S1 checks declaration
    membership for an exact carrier named by an endpoint/trigger contract; the
    primary contract remains unchanged.  G4 checks finite coaccessibility only
    when a termination contract supplies exact owner and marked target states.
    Runtime predicates are intentionally absent here: static source/model facts
    cannot be promoted to a trajectory scenario. An aggregate stable-termination
    frontier check may additionally project one supporting G4 topology execution
    when its typed root and marked refs are complete.
    """

    probes: list[CandidateIssue] = []
    probe_contracts: dict[str, NLContract] = {}
    dispositions: list[dict[str, Any]] = []
    existing_predicates = {
        (candidate.contract_id, candidate.predicate_id)
        for candidate in existing_candidates
    }

    # An element probe is a supporting closed-declaration check.  It is only
    # derived for endpoint/trigger contracts: containment, cardinality, and
    # initial-entry contracts are never relabelled as S1.
    for contract in sorted(contracts_by_id.values(), key=lambda item: item.contract_id):
        if contract.property not in {"transition_endpoints", "trigger_set"}:
            continue
        refs = _exact_grounding_model_refs(pair, grounding_responses, contract.contract_id)
        if not refs:
            continue
        model_ref = refs[0]
        descriptor = _s1_probe_descriptor(pair, model_ref)
        if descriptor is None:
            continue
        kind, element = descriptor
        probe_id = (
            f"{contract.contract_id}-S1-PROBE-"
            f"{_hash_json(model_ref).removeprefix('sha256:')[:12]}"
        )
        probe_contract = contract.model_copy(
            update={
                "contract_id": probe_id,
                "locus_kind": "model" if kind == "transition" else kind,
                "locus_names": (element,),
                "property": "element_declaration",
                "expected_direction": "must_exist",
                "violation_direction": "missing",
                "normative_statement": (
                    f"The exact closed-model {kind} carrier {element} must belong "
                    "to the declaration inventory."
                ),
                "scope": "closed_fcstm_declaration_inventory",
                "reason": (
                    "This supporting probe checks the exact grounded carrier's "
                    "declaration membership without replacing the parent contract."
                ),
                "basis": (
                    f"parent_contract={contract.contract_id}; exact_model_ref={model_ref}; "
                    "grounding SemanticBinding.status=exact"
                ),
                "binding_hints": (),
            }
        )
        candidate = CandidateIssue(
            contract_id=probe_id,
            locus_kind=probe_contract.locus_kind,
            locus_names=probe_contract.locus_names,
            property=probe_contract.property,
            violation_direction=probe_contract.violation_direction,
            evidence_types=("closed_model_inventory", "source_identity"),
            title=f"Declaration probe for exact {kind} carrier {element}",
            requirement_quote=contract.quote,
            predicate_id="S1",
            predicate_inputs={
                "kind": kind,
                "element": element,
                "scope": "closed_fcstm",
            },
            element_refs=[model_ref],
            source_refs=list(contract.source_refs),
            expected=probe_contract.normative_statement,
            observed=f"The exact ModelIR ref {model_ref} is checked against the closed declaration inventory.",
            strongest_rebuttal="The probe is supporting execution evidence only; it does not decide the parent endpoint or trigger obligation.",
            reason="An exact grounded carrier is available for a standalone declaration-membership execution.",
            basis=(
                f"parent_contract={contract.contract_id}; model_ref={model_ref}; "
                "S1 element_exists supporting probe"
            ),
        )
        if (probe_id, "S1") not in existing_predicates:
            probe_contracts[probe_id] = probe_contract
            probes.append(candidate)
            dispositions.append(
                {
                    "probe": "S1",
                    "status": "admitted_exact_carrier",
                    "contract_id": probe_id,
                    "parent_contract_id": contract.contract_id,
                    "model_ref": model_ref,
                    "reason": candidate.reason,
                    "basis": candidate.basis,
                }
            )
            break

    # G4 is a termination/coaccessibility check, not a generic termination
    # alias.  Both owner and marked target must come from exact grounding and
    # the author-source model must be finite and non-concurrent.
    concurrent = bool(
        pair.canonical_source_ir is not None
        and pair.canonical_source_ir.model.concurrent_regions
    )
    if not concurrent:
        for contract in sorted(contracts_by_id.values(), key=lambda item: item.contract_id):
            if contract.property != "termination":
                continue
            exact_by_role: dict[str, set[str]] = {}
            for response in grounding_responses:
                for binding in response.semantic_bindings:
                    if binding.contract_id != contract.contract_id or binding.status != "exact":
                        continue
                    raw_ref = binding.model_element_ref or binding.carrier_transition_ref
                    binding_refs = _resolved_exact_binding_refs(pair, binding)
                    if raw_ref and binding_refs:
                        ref = binding_refs[0]
                        exact_by_role.setdefault(binding.role, set()).add(ref)
            owners = exact_by_role.get("owner", set()) | exact_by_role.get("source", set())
            targets = exact_by_role.get("target", set())
            if len(owners) != 1 or len(targets) != 1:
                continue
            owner_ref = next(iter(owners))
            target_ref = next(iter(targets))
            owner = next((item for item in pair.model.states if item.ref == owner_ref), None)
            target = next((item for item in pair.model.states if item.ref == target_ref), None)
            if owner is None or target is None:
                continue
            if (contract.contract_id, "G4") in existing_predicates:
                continue
            candidate = CandidateIssue(
                contract_id=contract.contract_id,
                locus_kind=contract.locus_kind,
                locus_names=contract.locus_names,
                property=contract.property,
                violation_direction=contract.violation_direction,
                evidence_types=tuple(
                    dict.fromkeys([*contract.evidence_types, "reachability_fact"])
                ),
                title=f"Termination coaccessibility from {owner.name} to {target.name}",
                requirement_quote=contract.quote,
                predicate_id="G4",
                predicate_inputs={
                    "roots": [owner.name],
                    "marked": [target.name],
                },
                element_refs=[owner_ref, target_ref],
                source_refs=list(contract.source_refs),
                expected=contract.normative_statement,
                observed=(
                    f"Finite coaccessibility is checked from exact owner {owner.ref} "
                    f"to marked termination target {target.ref}."
                ),
                strongest_rebuttal="The G4 probe is admitted only for an exact owner/target termination contract and a non-concurrent finite source model.",
                reason="The termination contract supplies explicit roots and marked target states for the registered G4 coaccessibility fragment.",
                basis=(
                    f"contract={contract.contract_id}; owner_ref={owner_ref}; "
                    f"target_ref={target_ref}; finite_model=true; concurrent_regions=false"
                ),
            )
            probes.append(candidate)
            dispositions.append(
                {
                    "probe": "G4",
                    "status": "admitted_exact_termination",
                    "contract_id": contract.contract_id,
                    "owner_ref": owner_ref,
                    "target_ref": target_ref,
                    "reason": candidate.reason,
                    "basis": candidate.basis,
                }
            )
            break

    # A trigger-set contract can be executed when grounding supplies one
    # exact event and its exact transition carrier.  The event name is the
    # normative trigger input; the parsed transition remains the observed
    # carrier, so a mismatch yields a real S3 result instead of a relabelled
    # endpoint or a source-only plan.
    trigger_bindings: dict[tuple[str, str, str], SemanticBinding] = {}
    for response in grounding_responses:
        for binding in response.semantic_bindings:
            if (
                binding.status == "exact"
                and binding.role == "event"
                and binding.model_element_ref in pair.model.all_refs
                and binding.carrier_transition_ref in pair.model.transition_refs
            ):
                trigger_bindings[
                    (
                        binding.contract_id,
                        binding.model_element_ref or "",
                        binding.carrier_transition_ref or "",
                    )
                ] = binding
    for contract in sorted(contracts_by_id.values(), key=lambda item: item.contract_id):
        if contract.property != "trigger_set":
            continue
        rows = [
            binding
            for (contract_id, _event_ref, _transition_ref), binding in trigger_bindings.items()
            if contract_id == contract.contract_id
        ]
        unique_rows = {
            (
                binding.model_element_ref,
                binding.carrier_transition_ref,
            ): binding
            for binding in rows
        }
        if len(unique_rows) != 1:
            continue
        binding = next(iter(unique_rows.values()))
        event = next(
            (
                item
                for item in pair.model.events
                if item.ref == binding.model_element_ref
            ),
            None,
        )
        transition = pair.model.transition(binding.carrier_transition_ref)
        if event is None or transition is None:
            continue
        if (contract.contract_id, "S3") in existing_predicates:
            continue
        source_refs = list(contract.source_refs)
        if binding.source_element_ref and binding.source_element_ref not in source_refs:
            source_refs.append(binding.source_element_ref)
        candidate = CandidateIssue(
            contract_id=contract.contract_id,
            locus_kind=contract.locus_kind,
            locus_names=contract.locus_names,
            property=contract.property,
            violation_direction=contract.violation_direction,
            evidence_types=tuple(
                dict.fromkeys(
                    [*contract.evidence_types, "closed_model_inventory", "transition_fact"]
                )
            ),
            title=(
                f"Trigger set for {transition.source} -> {transition.target} "
                f"uses {event.name}"
            ),
            requirement_quote=contract.quote,
            predicate_id="S3",
            predicate_inputs={
                "transition": transition.ref,
                "triggers": [event.name],
            },
            element_refs=[event.ref, transition.ref],
            source_refs=source_refs,
            expected=contract.normative_statement,
            observed=(
                f"The exact carrier {transition.ref} has parsed trigger set "
                f"{list(transition.triggers)!r}."
            ),
            strongest_rebuttal=(
                "The S3 execution compares the exact grounded required event "
                "with the exact parsed carrier trigger set; another carrier "
                "cannot satisfy this contract."
            ),
            reason=(
                "One exact event binding and one exact carrier transition are "
                "available for a standalone trigger-set equality execution."
            ),
            basis=(
                f"contract={contract.contract_id}; event_ref={event.ref}; "
                f"carrier_transition_ref={transition.ref}; "
                "grounding SemanticBinding.status=exact"
            ),
        )
        probes.append(candidate)
        dispositions.append(
            {
                "probe": "S3",
                "status": "admitted_exact_trigger_carrier",
                "contract_id": contract.contract_id,
                "event_ref": event.ref,
                "carrier_transition_ref": transition.ref,
                "required_trigger": event.name,
                "reason": candidate.reason,
                "basis": candidate.basis,
            }
        )
        break

    # A state-action contract is directly executable only when the requirement
    # itself closes all three S4 arguments.  The native backend, rather than
    # the route, determines whether that exact lifecycle slot contains the
    # action.  This prevents a missing LLM issue candidate from suppressing a
    # valid native satisfaction/violation receipt, while never inventing a
    # lifecycle phase from source text or state names.
    for contract in sorted(contracts_by_id.values(), key=lambda item: item.contract_id):
        if contract.property != "state_action":
            continue
        state_hints = [hint for hint in contract.binding_hints if hint.role == "state"]
        phase_hints = [hint for hint in contract.binding_hints if hint.role == "phase"]
        action_hints = [hint for hint in contract.binding_hints if hint.role == "action"]
        if (
            len(state_hints) != 1
            or len(phase_hints) != 1
            or phase_hints[0].value not in {"entry", "do", "exit"}
            or len(action_hints) != 1
        ):
            continue
        state_ref = resolve_state_ref(state_hints[0].value, pair.model)
        state = next(
            (item for item in pair.model.states if item.ref == state_ref), None
        )
        if state is None or (contract.contract_id, "S4") in existing_predicates:
            continue
        source_refs = list(contract.source_refs)
        for hint in (*state_hints, *phase_hints, *action_hints):
            if hint.source_ref and hint.source_ref not in source_refs:
                source_refs.append(hint.source_ref)
        candidate = CandidateIssue(
            contract_id=contract.contract_id,
            locus_kind=contract.locus_kind,
            locus_names=contract.locus_names,
            property=contract.property,
            violation_direction=contract.violation_direction,
            evidence_types=tuple(
                dict.fromkeys([*contract.evidence_types, "closed_model_inventory", "action_fact"])
            ),
            title=(
                f"Lifecycle action {action_hints[0].value!r} on "
                f"{state.name} {phase_hints[0].value}"
            ),
            requirement_quote=contract.quote,
            predicate_id="S4",
            predicate_inputs={
                "state": state.canonical_path,
                "phase": phase_hints[0].value,
                "action": action_hints[0].value,
            },
            element_refs=[state.ref],
            source_refs=source_refs,
            expected=contract.normative_statement,
            observed=(
                f"The exact native lifecycle slot {phase_hints[0].value} on "
                f"{state.ref} is evaluated by S4."
            ),
            strongest_rebuttal=(
                "Only the exact native State lifecycle collection for this "
                "state and phase is compared; an event, effect, body text, or "
                "another lifecycle slot cannot discharge this contract."
            ),
            reason=(
                "The typed contract supplies one exact state, one legal lifecycle "
                "phase, and one action without inferring any input from model text."
            ),
            basis=(
                f"contract={contract.contract_id}; state_ref={state.ref}; "
                f"phase={phase_hints[0].value}; action={action_hints[0].value!r}; "
                "unique native-derived state identity plus requirement-side typed hints"
            ),
        )
        probes.append(candidate)
        dispositions.append(
            {
                "probe": "S4",
                "status": "admitted_exact_lifecycle_contract",
                "contract_id": contract.contract_id,
                "state_ref": state.ref,
                "phase": phase_hints[0].value,
                "action": action_hints[0].value,
                "reason": candidate.reason,
                "basis": candidate.basis,
            }
        )
        break

    # An effect contract can be executed by S6 only when grounding supplies
    # one exact transition carrier.  The effect hint remains the normative
    # input; event names, variable deltas, state scope, and display labels are
    # not transition-effect evidence and must not be used to guess a carrier.
    effect_bindings: dict[tuple[str, str], SemanticBinding] = {}
    for response in grounding_responses:
        for binding in response.semantic_bindings:
            if binding.status != "exact" or binding.role != "transition":
                continue
            carrier_ref = binding.carrier_transition_ref
            if not carrier_ref or carrier_ref not in pair.model.transition_refs:
                continue
            resolved_refs = _resolved_exact_binding_refs(pair, binding)
            transition_refs = tuple(
                ref for ref in resolved_refs if ref in pair.model.transition_refs
            )
            if len(transition_refs) != 1 or transition_refs[0] != carrier_ref:
                continue
            effect_bindings[(binding.contract_id, carrier_ref)] = binding
    for contract in sorted(contracts_by_id.values(), key=lambda item: item.contract_id):
        if contract.property != "effect":
            continue
        effect_hints = [hint for hint in contract.binding_hints if hint.role == "effect"]
        carrier_rows = [
            (carrier_ref, binding)
            for (contract_id, carrier_ref), binding in effect_bindings.items()
            if contract_id == contract.contract_id
        ]
        if len(effect_hints) != 1 or len(carrier_rows) != 1:
            continue
        effect_hint = effect_hints[0]
        carrier_ref, binding = carrier_rows[0]
        transition = pair.model.transition(carrier_ref)
        if transition is None:
            continue
        if (contract.contract_id, "S6") in existing_predicates:
            continue
        source_refs = list(contract.source_refs)
        for source_ref in (effect_hint.source_ref, binding.source_element_ref):
            if source_ref and source_ref not in source_refs:
                source_refs.append(source_ref)
        candidate = CandidateIssue(
            contract_id=contract.contract_id,
            locus_kind=contract.locus_kind,
            locus_names=contract.locus_names,
            property=contract.property,
            violation_direction=contract.violation_direction,
            evidence_types=tuple(
                dict.fromkeys([*contract.evidence_types, "transition_fact", "effect_fact"])
            ),
            title=(
                f"Effect {effect_hint.value!r} on exact transition "
                f"{transition.source} -> {transition.target}"
            ),
            requirement_quote=contract.quote,
            predicate_id="S6",
            predicate_inputs={
                "transition": transition.ref,
                "effect": [effect_hint.value],
            },
            element_refs=[transition.ref],
            source_refs=source_refs,
            expected=contract.normative_statement,
            observed=(
                f"The exact carrier {transition.ref} has parsed effects "
                f"{list(transition.effects)!r}."
            ),
            strongest_rebuttal=(
                "The S6 execution is limited to the one exact grounded carrier; "
                "a state scope, event name, variable delta, or another transition "
                "cannot satisfy this effect attachment check."
            ),
            reason=(
                "One exact transition binding and one explicit effect hint are "
                "available for a standalone transition-effect membership execution."
            ),
            basis=(
                f"contract={contract.contract_id}; effect_hint={effect_hint.value!r}; "
                f"carrier_transition_ref={transition.ref}; binding_id={binding.binding_id}; "
                "grounding SemanticBinding.status=exact"
            ),
        )
        probes.append(candidate)
        dispositions.append(
            {
                "probe": "S6",
                "status": "admitted_exact_effect_carrier",
                "contract_id": contract.contract_id,
                "carrier_transition_ref": transition.ref,
                "effect": effect_hint.value,
                "binding_id": binding.binding_id,
                "reason": candidate.reason,
                "basis": candidate.basis,
            }
        )
        break

    # An aggregate stable-termination check already contains the exact
    # coaccessibility obligation, but it used to stop at the predicate-null
    # frontier candidate. Project only the frontier's typed root/marked refs:
    # no role is recovered from prose, a contract ID, or the basis string.
    if frontier_batch is not None and not any(
        item.predicate_id == "G4" for item in probes
    ) and not any(
        candidate.predicate_id == "G4" for candidate in existing_candidates
    ):
        concurrent = bool(
            pair.canonical_source_ir is not None
            and pair.canonical_source_ir.model.concurrent_regions
        )
        aggregate_checks = sorted(
            (
                check
                for check in frontier_batch.checks
                if check.kind == "aggregate_stable_termination"
                and check.status == "candidate"
            ),
            key=lambda check: check.check_id,
        )
        for check in aggregate_checks:
            contract = contracts_by_id.get(check.canonical_contract_id or "")
            if contract is None:
                dispositions.append(
                    {
                        "probe": "G4",
                        "status": "frontier_aggregate_missing_contract",
                        "check_id": check.check_id,
                        "canonical_contract_id": check.canonical_contract_id,
                        "reason": "The aggregate termination check has no accepted typed contract, so a G4 probe would require inventing its semantic owner.",
                        "basis": "exact FrontierCheckReceipt.canonical_contract_id lookup",
                    }
                )
                continue
            if concurrent or pair.canonical_source_ir is None:
                dispositions.append(
                    {
                        "probe": "G4",
                        "status": "frontier_aggregate_blocked_non_sequential_model",
                        "check_id": check.check_id,
                        "reason": "G4 coaccessibility projection requires the finite sequential author-source model; concurrent or unavailable source IR remains outside this fragment.",
                        "basis": "canonical_source_ir.model.concurrent_regions and source-IR availability",
                    }
                )
                continue
            root_refs = tuple(dict.fromkeys(check.root_refs))
            marked_refs = tuple(dict.fromkeys(check.marked_refs))
            frontier_refs = set(check.model_refs)
            topology_refs = set(root_refs) | set(marked_refs)
            if (
                not root_refs
                or not marked_refs
                or topology_refs != frontier_refs
                or not topology_refs.issubset(set(pair.model.all_refs))
                or set(root_refs) & set(marked_refs)
            ):
                dispositions.append(
                    {
                        "probe": "G4",
                        "status": "frontier_aggregate_incomplete_typed_refs",
                        "check_id": check.check_id,
                        "model_refs": list(check.model_refs),
                        "root_refs": list(root_refs),
                        "marked_refs": list(marked_refs),
                        "reason": "The aggregate frontier check does not provide a complete disjoint root/marked partition of its exact ModelIR refs.",
                        "basis": "exact typed root_refs, marked_refs, model_refs, and closed ModelIR reference membership",
                    }
                )
                continue
            states_by_ref = {
                state.ref: state for state in pair.model.states
            }
            roots = [states_by_ref.get(ref) for ref in root_refs]
            marked = [states_by_ref.get(ref) for ref in marked_refs]
            if any(state is None for state in (*roots, *marked)):
                dispositions.append(
                    {
                        "probe": "G4",
                        "status": "frontier_aggregate_non_state_refs",
                        "check_id": check.check_id,
                        "root_refs": list(root_refs),
                        "marked_refs": list(marked_refs),
                        "reason": "G4 topology inputs must be exact state refs; event or transition refs cannot be promoted to roots or marked nodes.",
                        "basis": "closed ModelIR state inventory membership",
                    }
                )
                continue
            root_names = [state.name for state in roots if state is not None]
            marked_names = [state.name for state in marked if state is not None]
            source_refs = list(
                dict.fromkeys([*contract.source_refs, *check.source_refs])
            )
            candidate = CandidateIssue(
                contract_id=contract.contract_id,
                locus_kind=contract.locus_kind,
                locus_names=contract.locus_names,
                property=contract.property,
                violation_direction=contract.violation_direction,
                evidence_types=tuple(
                    dict.fromkeys([*contract.evidence_types, "reachability_fact"])
                ),
                title=(
                    f"Aggregate termination coaccessibility from "
                    f"{root_names!r} to {marked_names!r}"
                ),
                requirement_quote=contract.quote,
                predicate_id="G4",
                predicate_inputs={"roots": root_names, "marked": marked_names},
                element_refs=[*root_refs, *marked_refs],
                source_refs=source_refs,
                expected=contract.normative_statement,
                observed=(
                    f"The exact aggregate frontier carrier supplies roots="
                    f"{list(root_refs)!r} and marked={list(marked_refs)!r} "
                    "for finite coaccessibility execution."
                ),
                strongest_rebuttal=(
                    "The G4 probe is supporting execution evidence only; it is "
                    "admitted from the aggregate frontier's exact typed partition "
                    "and does not replace the termination obligation."
                ),
                reason=(
                    "The deterministic aggregate termination frontier supplied a "
                    "complete exact root/marked partition over the closed model, "
                    "so the registered G4 coaccessibility fragment can execute "
                    "without inferring identity from prose."
                ),
                basis=(
                    f"frontier_check={check.check_id}; "
                    f"canonical_contract={contract.contract_id}; "
                    f"root_refs={list(root_refs)}; marked_refs={list(marked_refs)}; "
                    "finite_model=true; concurrent_regions=false"
                ),
            )
            probes.append(candidate)
            dispositions.append(
                {
                    "probe": "G4",
                    "status": "admitted_frontier_aggregate_termination",
                    "check_id": check.check_id,
                    "contract_id": contract.contract_id,
                    "root_refs": list(root_refs),
                    "marked_refs": list(marked_refs),
                    "source_refs": source_refs,
                    "reason": candidate.reason,
                    "basis": candidate.basis,
                }
            )
            break

    # Contract extraction usually keeps an event as a transition-group
    # alternative rather than emitting a duplicate trigger_set contract.
    # Project one such group through the compiler-owned event projection and
    # its macro/segment carrier. This remains a supporting execution probe: it
    # never replaces the group's endpoint obligation or creates a new norm.
    needs_s3_probe = not any(item.predicate_id == "S3" for item in probes) and not any(
        candidate.predicate_id == "S3" for candidate in existing_candidates
    )
    needs_r1_probe = not any(item.predicate_id == "R1" for item in probes) and not any(
        candidate.predicate_id == "R1" for candidate in existing_candidates
    )
    if needs_s3_probe or needs_r1_probe:
        for group in sorted(transition_groups, key=lambda item: item.group_id):
            segment_contract_ids = {
                contract.contract_id
                for contract in contracts_by_id.values()
                if contract.segment_id == group.segment_id
            }
            segment_transition_refs = {
                binding.carrier_transition_ref
                for response in grounding_responses
                for binding in response.semantic_bindings
                if (
                    binding.contract_id in segment_contract_ids
                    and binding.status == "exact"
                    and binding.carrier_transition_ref in pair.model.transition_refs
                )
            }
            for alternative in group.alternatives:
                event_ref = _model_ref_for_event(pair, alternative.event)
                if event_ref is None:
                    continue
                macro_transition_refs, macro_ids, working_source_refs = (
                    _working_event_transition_context(pair, event_ref)
                )
                if not macro_transition_refs:
                    continue
                candidate_transition_refs = set(macro_transition_refs)
                shared_refs = candidate_transition_refs.intersection(
                    segment_transition_refs
                )
                if shared_refs:
                    candidate_transition_refs = shared_refs
                elif len(candidate_transition_refs) > 1 and len(
                    segment_transition_refs
                ) == 1:
                    segment_ref = next(iter(segment_transition_refs))
                    if segment_ref in candidate_transition_refs:
                        candidate_transition_refs = {segment_ref}
                observed_ref = alternative.observed_transition_ref
                if observed_ref:
                    observed_matches = resolve_transition_ref(
                        observed_ref,
                        pair.model,
                    )
                    if observed_matches is not None:
                        candidate_transition_refs.intersection_update(
                            {observed_matches}
                        )
                if len(candidate_transition_refs) != 1:
                    continue
                transition_ref = next(iter(candidate_transition_refs))
                transition = pair.model.transition(transition_ref)
                event = next(
                    (item for item in pair.model.events if item.ref == event_ref),
                    None,
                )
                if transition is None or event is None:
                    continue
                parent_contract = next(
                    (
                        contract
                        for contract in sorted(
                            contracts_by_id.values(),
                            key=lambda item: item.contract_id,
                        )
                        if contract.segment_id == group.segment_id
                        and contract.property in {
                            "transition_endpoints",
                            "trigger_set",
                        }
                    ),
                    None,
                )
                digest = _hash_json(
                    {
                        "group_id": group.group_id,
                        "alternative_id": alternative.alternative_id,
                        "event_ref": event.ref,
                        "transition_ref": transition.ref,
                    }
                ).removeprefix("sha256:")[:16]
                probe_id = (
                    f"NL-CONTRACT-{group.group_id}-S3-PROBE-{digest}"
                )
                source_refs = list(
                    dict.fromkeys(
                        [
                            *(parent_contract.source_refs if parent_contract else ()),
                            *group.source_refs,
                            *alternative.source_refs,
                            *working_source_refs,
                        ]
                    )
                )
                normative = (
                    f"The {group.source_name} transition alternative to "
                    f"{alternative.target_name} must use the exact event "
                    f"{event.name}."
                )
                reason = (
                    "A typed transition-group event resolves to one compiler "
                    "event projection and one working-contract macro/segment "
                    "carrier; the supporting S3 equality check preserves that "
                    "exact relation."
                )
                basis = (
                    f"group={group.group_id}; segment={group.segment_id}; "
                    f"event_ref={event.ref}; macro_ids={sorted(macro_ids)}; "
                    f"carrier_transition_ref={transition.ref}; "
                    f"segment_exact_refs={sorted(segment_transition_refs)}"
                )
                r1_scenario = build_r1_cold_runtime_scenario(
                    pair, transition, event.name
                )
                r1_admitted = False
                if needs_r1_probe and parent_contract is not None and r1_scenario is not None:
                    r1_probe_id = f"NL-CONTRACT-{group.group_id}-R1-PROBE-{digest}"
                    r1_reason = (
                        "One exact transition-group event and a unique cold-start "
                        "FCSTM runtime setup are available for a supporting event-"
                        "consumption execution."
                    )
                    r1_basis = (
                        f"{basis}; runtime_scenario_basis={r1_scenario['basis']}"
                    )
                    r1_contract = parent_contract.model_copy(
                        update={
                            "contract_id": r1_probe_id,
                            "locus_kind": "scenario",
                            "locus_names": (transition.source, event.name),
                            "property": "event_consumption",
                            "expected_direction": "must_occur",
                            "violation_direction": "unconsumed",
                            "evidence_types": (
                                "source_identity",
                                "closed_model_inventory",
                                "transition_fact",
                                "trigger_fact",
                                "trace_fact",
                            ),
                            "binding_hints": (),
                            "cardinality_requirement": None,
                            "normative_statement": (
                                f"The exact queued event {event.name} must be consumed "
                                f"in the closed macrostep from {transition.source}."
                            ),
                            "scope": "closed_fcstm_cold_runtime_macrostep",
                            "source_refs": tuple(source_refs),
                            "reason": r1_reason,
                            "basis": r1_basis,
                        }
                    )
                    r1_candidate = CandidateIssue(
                        contract_id=r1_probe_id,
                        locus_kind="scenario",
                        locus_names=(transition.source, event.name),
                        property="event_consumption",
                        violation_direction="unconsumed",
                        evidence_types=(
                            "source_identity",
                            "closed_model_inventory",
                            "transition_fact",
                            "trigger_fact",
                            "trace_fact",
                        ),
                        title=f"Closed macrostep consumes {event.name} from {transition.source}",
                        requirement_quote=parent_contract.quote,
                        predicate_id="R1",
                        predicate_inputs={
                            "scenario": r1_scenario,
                            "event": event.name,
                            "step": 1,
                        },
                        element_refs=[event.ref, transition.ref],
                        source_refs=source_refs,
                        expected=r1_contract.normative_statement,
                        observed=(
                            f"The frozen FCSTM will be cold-started and execute the "
                            f"exact queued event path {r1_scenario['selected_event_path']}."
                        ),
                        strongest_rebuttal=(
                            "The probe is admitted only when the runtime setup has a "
                            "unique initial source and one unguarded same-source event "
                            "carrier; otherwise no R1 scenario is materialized."
                        ),
                        reason=r1_reason,
                        basis=r1_basis,
                    )
                    probe_contracts[r1_probe_id] = r1_contract
                    probes.append(r1_candidate)
                    r1_admitted = True
                    dispositions.append(
                        {
                            "probe": "R1",
                            "status": "admitted_closed_fcstm_runtime_macrostep",
                            "contract_id": r1_probe_id,
                            "group_id": group.group_id,
                            "event_ref": event.ref,
                            "carrier_transition_ref": transition.ref,
                            "runtime_scenario": r1_scenario,
                            "reason": r1_reason,
                            "basis": r1_basis,
                        }
                    )
                if parent_contract is not None:
                    probe_contract = parent_contract.model_copy(
                        update={
                            "contract_id": probe_id,
                            "locus_kind": "transition",
                            "locus_names": (transition.source, transition.target),
                            "property": "trigger_set",
                            "expected_direction": "must_equal",
                            "violation_direction": "mismatched",
                            "evidence_types": (
                                "source_identity",
                                "closed_model_inventory",
                                "transition_fact",
                                "trigger_fact",
                            ),
                            "binding_hints": (),
                            "cardinality_requirement": None,
                            "normative_statement": normative,
                            "scope": f"transition-group {group.group_id}",
                            "source_refs": tuple(source_refs),
                            "reason": reason,
                            "basis": basis,
                        }
                    )
                else:
                    probe_contract = NLContract(
                        contract_id=probe_id,
                        segment_id=group.segment_id,
                        quote=(
                            f"Typed transition-group {group.group_id} alternative "
                            f"{alternative.alternative_id}."
                        ),
                        normative_statement=normative,
                        locus_kind="transition",
                        locus_names=(transition.source, transition.target),
                        property="trigger_set",
                        expected_direction="must_equal",
                        violation_direction="mismatched",
                        evidence_types=(
                            "source_identity",
                            "closed_model_inventory",
                            "transition_fact",
                            "trigger_fact",
                        ),
                        binding_hints=(),
                        scope=f"transition-group {group.group_id}",
                        source_refs=tuple(source_refs),
                        reason=reason,
                        basis=basis,
                    )
                if not needs_s3_probe:
                    if r1_admitted:
                        return probes, probe_contracts, dispositions
                    continue
                candidate = CandidateIssue(
                    contract_id=probe_id,
                    locus_kind="transition",
                    locus_names=(transition.source, transition.target),
                    property="trigger_set",
                    violation_direction="mismatched",
                    evidence_types=(
                        "source_identity",
                        "closed_model_inventory",
                        "transition_fact",
                        "trigger_fact",
                    ),
                    title=(
                        f"Trigger set for {transition.source} -> "
                        f"{transition.target} uses {event.name}"
                    ),
                    requirement_quote=probe_contract.quote,
                    predicate_id="S3",
                    predicate_inputs={
                        "transition": transition.ref,
                        "triggers": [event.name],
                    },
                    element_refs=[event.ref, transition.ref],
                    source_refs=source_refs,
                    expected=normative,
                    observed=(
                        f"The exact carrier {transition.ref} has parsed trigger "
                        f"set {list(transition.triggers)!r}."
                    ),
                    strongest_rebuttal=(
                        "The event projection or macro membership would have to "
                        "identify a different exact carrier to defeat this probe."
                    ),
                    reason=reason,
                    basis=basis,
                )
                probe_contracts[probe_id] = probe_contract
                probes.append(candidate)
                dispositions.append(
                    {
                        "probe": "S3",
                        "status": "admitted_transition_group_event_carrier",
                        "contract_id": probe_id,
                        "group_id": group.group_id,
                        "segment_id": group.segment_id,
                        "alternative_id": alternative.alternative_id,
                        "event_ref": event.ref,
                        "carrier_transition_ref": transition.ref,
                        "macro_ids": sorted(macro_ids),
                        "segment_exact_refs": sorted(segment_transition_refs),
                        "reason": reason,
                        "basis": basis,
                    }
                )
                return probes, probe_contracts, dispositions

    return probes, probe_contracts, dispositions


def _prepared_is_finding_candidate(prepared: Mapping[str, Any]) -> bool:
    """Apply the execute-batch boundary between passing checks and findings."""

    receipt = prepared.get("receipt")
    return not (
        isinstance(receipt, RawReceipt)
        and receipt.terminal_state == "completed"
        and receipt.verdict == "true"
    )


def _deterministic_candidate(
    pair: PairInput,
    candidate: CandidateIssue,
    round_index: int,
    index: int,
    retry_records: list[dict[str, Any]],
    *,
    semantic_adjudication: SemanticAdjudication | None = None,
    prepared: dict[str, Any] | None = None,
    run_id: str = "00000000000000000000000000000000",
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
        run_id=run_id,
    )
    record.update(
        {
            "issue_id": f"{pair.pair_id}:r{round_index}:issue:{index}",
            "contract_id": candidate.contract_id,
            "locus_kind": candidate.locus_kind,
            "locus_names": list(candidate.locus_names),
            "property": candidate.property,
            "violation_direction": candidate.violation_direction,
            "evidence_types": list(candidate.evidence_types),
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


def _d_decision_consistency_errors(
    decision: SemanticAdjudication,
    *,
    prepared: Mapping[str, Any] | None = None,
    pair: PairInput | None = None,
) -> list[str]:
    """Validate closed D fields and exact typed fact contradictions."""

    errors: list[str] = []
    if decision.defeater_kind == "none":
        if decision.strongest_defeater is not None:
            errors.append("defeater_kind=none requires strongest_defeater=null")
        if decision.defeater_disposition != "defeated":
            errors.append("defeater_kind=none requires defeater_disposition=defeated")
    elif decision.strongest_defeater is None:
        errors.append("a typed defeater requires a non-null strongest_defeater")
    if prepared is not None and pair is not None and decision.grounding == "established":
        candidate = prepared.get("candidate")
        binding = prepared.get("binding")
        if (
            isinstance(candidate, CandidateIssue)
            and candidate.property == "deadlock_freedom"
            and candidate.violation_direction == "dead_end"
            and binding is not None
        ):
            bound_states = [
                state
                for state in pair.model.states
                if state.ref in binding.element_refs
            ]
            states_with_outgoing = [
                state.name
                for state in bound_states
                if any(edge.source_ref == state.ref for edge in pair.model.transitions)
            ]
            if bound_states and len(states_with_outgoing) == len(bound_states):
                errors.append(
                    "grounding=established contradicts the exact closed-model outgoing-transition inventory: "
                    f"every bound dead_end locus has outgoing transitions ({states_with_outgoing}); "
                    "unreachability is not a local dead-end or V4 deadlock violation"
                )
        if (
            isinstance(candidate, CandidateIssue)
            and candidate.property == "event_consumer_coverage"
            and candidate.violation_direction == "unconsumed"
            and binding is not None
            and pair.inspection_facts is not None
            and decision.defeater_kind == "rebutting"
            and decision.defeater_disposition == "survives"
        ):
            bound_refs = set(binding.element_refs)
            matching_facts = [
                fact
                for fact in pair.inspection_facts.event_consumers
                if (
                    fact.declared_ref in bound_refs
                    or bool(bound_refs & set(fact.consumer_transition_refs))
                )
            ]
            if matching_facts and all(
                not fact.reachable_consumer_transition_refs
                for fact in matching_facts
            ):
                errors.append(
                    "a surviving rebutting defeater contradicts the exact event-consumer inventory: "
                    "every bound event is declared or consumed only by unreachable transitions, "
                    "so declaration-only presence cannot rebut reachable-consumer coverage"
                )
    return errors


def _normalize_d_decision_shape(
    decision: SemanticAdjudication,
    *,
    stage: str,
    normalization_log: list[dict[str, Any]],
) -> SemanticAdjudication:
    """Repair the one context-free D shape invariant before semantic mapping.

    ``defeater_kind=none`` has no alternative reading to preserve.  Therefore
    its defeater payload must be null and its disposition must be defeated.
    This is a structural normalization, not a semantic D decision: all
    grounding, violated-obligation, reason, and basis fields remain untouched.
    Other invalid combinations stay unresolved and continue through the
    existing targeted correction path.
    """

    if decision.defeater_kind != "none":
        return decision
    updates: dict[str, Any] = {}
    changes: list[str] = []
    if decision.strongest_defeater is not None:
        updates["strongest_defeater"] = None
        changes.append("strongest_defeater=null")
    if decision.defeater_disposition != "defeated":
        updates["defeater_disposition"] = "defeated"
        changes.append("defeater_disposition=defeated")
    if not updates:
        return decision
    normalized = decision.model_copy(
        update={
            **updates,
            "basis": (
                f"{decision.basis}; deterministic D shape normalization "
                f"({', '.join(changes)})"
            ),
        }
    )
    normalization_log.append(
        {
            "stage": stage,
            "obligation_id": decision.obligation_id,
            "changes": changes,
            "reason": "The typed defeater-none invariant was normalized without interpreting free text or changing semantic grounding.",
            "basis": "defeater_kind=none requires strongest_defeater=null and defeater_disposition=defeated",
        }
    )
    return normalized


def _release_semantic_key(issue: Mapping[str, Any]) -> tuple[Any, ...]:
    """Return the exact typed defect identity used for report-level dedup."""

    return (
        issue.get("locus_kind"),
        tuple(issue.get("locus_names") or ()),
        issue.get("property"),
        issue.get("violation_direction"),
    )


def _deduplicate_release_issues(
    release: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Collapse only exact typed defect identities without reading prose."""

    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for issue in release:
        grouped.setdefault(_release_semantic_key(issue), []).append(issue)
    d_rank = {"D1": 1, "D2": 2}
    w_rank = {"W1": 1, "W2": 2}
    result: list[dict[str, Any]] = []
    for facets in grouped.values():
        representative = max(
            enumerate(facets),
            key=lambda indexed: (
                d_rank.get(str(indexed[1].get("d_level")), 0),
                w_rank.get(str(indexed[1].get("witness_level")), 0),
                -indexed[0],
            ),
        )[1]
        item = dict(representative)
        item["facet_issue_ids"] = [str(facet["issue_id"]) for facet in facets]
        item["facet_count"] = len(facets)
        item["contract_ids"] = list(
            dict.fromkeys(str(facet["contract_id"]) for facet in facets)
        )
        item["deduplication"] = {
            "algorithm_version": "exact-typed-defect-key.v1",
            "semantic_key": {
                "locus_kind": item.get("locus_kind"),
                "locus_names": item.get("locus_names", []),
                "property": item.get("property"),
                "violation_direction": item.get("violation_direction"),
            },
            "reason": "Candidates with the same exact typed locus, property, and violation direction were published as one report issue.",
            "basis": "context-free equality over typed fields; no prose, ledger, similarity, or lexical heuristic",
        }
        result.append(item)
    return result


def _method_cell(
    *,
    pair: PairInput,
    round_index: int,
    runtime: PublicStructuredRuntime,
    output_root: Path,
    run_identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if pair.context_manifest is None or pair.exact_source_inventory is None:
        raise ValueError("method cell requires the complete typed input closure")
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

    contract_prompt = build_contract_prompt(pair, round_index)
    contract_outcome: StructuredCallOutcome[NLContractResponse] = runtime.call(
        kind="contract_extraction",
        schema=NLContractResponse,
        system_prompt=CONTRACT_SYSTEM_PROMPT,
        prompt=contract_prompt,
        artifact_id=f"method/{pair.pair_id}/round-{round_index}/contract-extraction",
    )
    all_outcomes.append(contract_outcome)
    raw_contract_response = (
        contract_outcome.response
        if contract_outcome.succeeded
        else fallback_contracts(
            pair,
            str(contract_outcome.result.get("error", "structured contract output unavailable")),
        )
    )
    contract_response, contract_normalization_diagnostics = (
        normalize_contract_state_roles(raw_contract_response)
    )
    contract_response = materialize_segment_coverage(
        contract_response,
        [segment.segment_id for segment in pair.nl_segments],
    )
    if not contract_outcome.succeeded:
        all_errors.append(
            {
                "stage": "contract_extraction",
                "error": contract_outcome.result.get("error", "structured contract output unavailable"),
                "reason": "The whole-cell contract call failed; numbered NL is preserved only as an unresolved audit contract.",
                "basis": "public structured runtime outcome and exact numbered NL fallback",
            }
        )
    stage_outputs["contract_extraction"] = contract_response.model_dump(mode="json")
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:contract-extraction",
            stage_name="contract_extraction",
            status="completed" if contract_outcome.succeeded else "failed_with_receipt",
            artifact_roles=("natural_language", "working_contract", "source_trace"),
            output=contract_response,
            outcome=contract_outcome,
            diagnostics=tuple(contract_normalization_diagnostics),
            projection_version="typed-contract-projection.v2",
            reason=contract_response.reason,
            basis=contract_response.basis,
        )
    )

    grounding_prompts = {
        lens: build_grounding_prompt(
            pair,
            lens=lens,
            round_index=round_index,
            contracts=contract_response,
        )
        for lens in DISCOVERY_GROUNDING_AUDIT_LENSES
    }
    grounding_outcomes: list[StructuredCallOutcome[GroundingResponse]] = []
    grounding_responses: list[GroundingResponse] = []
    identity_normalization_receipts: list[
        IdentityNormalizationReceipt | GroupIdentityNormalizationReceipt
    ] = []
    grounding_normalization_diagnostics: list[dict[str, Any]] = []
    grounding_schema = _grounding_response_contract(contract_response.contracts)
    # The method samples the two complementary lenses sequentially inside one
    # cell. Pair workers provide process-level parallelism without changing the
    # public AgentApp/LangGraph call semantics or deadline handling.
    for lens, prompt in grounding_prompts.items():
        outcome: StructuredCallOutcome[GroundingResponse] = runtime.call(
            kind="discovery_grounding",
            schema=grounding_schema,
            system_prompt=DISCOVERY_GROUNDING_SYSTEM_PROMPT,
            prompt=prompt,
            artifact_id=(
                f"method/{pair.pair_id}/round-{round_index}/"
                f"discovery-grounding/{lens}"
            ),
        )
        grounding_outcomes.append(outcome)
        response = outcome.response if outcome.succeeded else fallback_grounding(
            pair,
            lens=lens,
            contracts=contract_response,
            reason=str(
                outcome.result.get(
                    "error",
                    f"{lens} discovery grounding output unavailable",
                )
            ),
        )
        response, identity_receipts = canonicalize_grounding_response(response)
        identity_normalization_receipts.extend(identity_receipts)
        response, exact_fact_diagnostics = _normalize_grounding_exact_facts(
            pair, response
        )
        grounding_normalization_diagnostics.extend(exact_fact_diagnostics)
        grounding_responses.append(response)
        if not outcome.succeeded:
            all_errors.append(
                {
                    "stage": "discovery_grounding",
                    "lens": lens,
                    "error": outcome.result.get(
                        "error",
                        f"{lens} discovery grounding output unavailable",
                    ),
                    "reason": "One complementary discovery lens failed; its contracts remain unresolved and no fallback issue was manufactured.",
                    "basis": "public structured runtime outcome and lens-local failure rule",
                }
            )
    all_outcomes.extend(grounding_outcomes)
    contracts_by_id, grounding_contract_diagnostics = _merge_grounding_contracts(
        pair,
        contract_response,
        grounding_responses,
    )
    grounding_normalization_diagnostics.extend(grounding_contract_diagnostics)
    all_errors.extend(grounding_contract_diagnostics)
    stage_outputs["discovery_grounding"] = {
        "branches": [
            response.model_dump(mode="json")
            for response in grounding_responses
        ],
        "accepted_additional_contract_ids": sorted(
            set(contracts_by_id)
            - {contract.contract_id for contract in contract_response.contracts}
        ),
        "identity_normalization_receipts": [
            receipt.model_dump(mode="json")
            for receipt in identity_normalization_receipts
        ],
        "reason": "Two complementary discovery lenses completed or retained explicit lens diagnostics; branch-local derived identities were normalized by the runner before merge.",
        "basis": "one shared GroundingResponse schema, compact cross-view context, and canonical ContractSemanticKey identities over the same contract plan",
    }
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:discovery-grounding",
            stage_name="discovery_grounding",
            status=(
                "completed"
                if all(outcome.succeeded for outcome in grounding_outcomes)
                and not grounding_normalization_diagnostics
                else "completed_with_diagnostics"
            ),
            artifact_roles=("natural_language", "plantuml_source", "canonical_source_ir", "source_inventory", "fcstm_model", "reference_inspection_facts", "inspection_equivalent_facts", "verify_facts", "smt_facts", "working_contract", "source_trace"),
            output=stage_outputs["discovery_grounding"],
            outcome=grounding_outcomes[-1],
            diagnostics=tuple(grounding_normalization_diagnostics),
            projection_version="complementary-grounding-projection.v2",
            reason=stage_outputs["discovery_grounding"]["reason"],
            basis=stage_outputs["discovery_grounding"]["basis"],
        )
    )

    response = assemble_method_response(
        grounding_responses,
        reason="The method merged two complementary discovery lenses after NL contract extraction; typed semantic D is adjudicated separately and W remains deterministic downstream output.",
        basis="two GroundingResponse objects over the same compact cross-view context manifest",
    )
    unresolved_candidates, unresolved_admission = _admit_grounding_unresolved(
        pair,
        contracts_by_id,
        grounding_responses,
        response.issues,
    )
    initial_candidates, retention_carrier_dispositions = (
        _normalize_state_retention_carriers(
            pair,
            [*response.issues, *unresolved_candidates],
            contracts_by_id,
        )
    )
    initial_candidates, endpoint_preflight_dispositions = (
        _preflight_existing_endpoint_candidates(
            pair,
            initial_candidates,
            contracts_by_id,
        )
    )
    initial_candidates, root_wrapper_preflight_dispositions = (
        _preflight_synthetic_root_wrapper_reachability(
            pair,
            initial_candidates,
        )
    )
    initial_candidates, route_controller_preflight_dispositions = (
        suppress_closed_route_controller_candidates(pair, initial_candidates)
    )
    try:
        frontier_batch = materialize_typed_frontier(
            pair,
            contract_response,
            contracts_by_id,
            grounding_responses,
            initial_candidates,
        )
    except Exception as exc:  # noqa: BLE001 - preserve the cell as a diagnostic receipt
        all_errors.append(
            {
                "stage": "execute_batch",
                "class": "deterministic_frontier_error",
                "error_type": type(exc).__name__,
                "message": str(exc),
                "reason": "The deterministic frontier failed locally; existing grounding candidates remain available and the cell continues with an explicit diagnostic.",
                "basis": "local-stage downgrade rule; non-provider failures cannot erase prior semantic artifacts",
            }
        )
        frontier_batch = FrontierBatch(
            reason="The deterministic frontier produced no obligations because a local implementation error was preserved as a cell diagnostic.",
            basis=f"error_type={type(exc).__name__}; message={exc}",
        )
    frontier_candidates = [
        obligation.candidate for obligation in frontier_batch.obligations
    ]
    raw_admitted_llm_candidates = [
        candidate
        for candidate in initial_candidates
        if candidate.contract_id
        not in frontier_batch.superseded_candidate_contract_ids
    ]
    for obligation in frontier_batch.obligations:
        contracts_by_id.setdefault(
            obligation.contract.contract_id, obligation.contract
        )
    frontier_unresolved_candidates, frontier_unresolved_admission = (
        _admit_frontier_unresolved(
            pair,
            contracts_by_id,
            frontier_batch,
            initial_candidates,
        )
    )
    frontier_candidates.extend(frontier_unresolved_candidates)
    source_transition_closures = {
        contract_id: evaluate_source_transition_closure(pair, contract)
        for contract_id, contract in contracts_by_id.items()
        if contract.property == "transition_endpoints"
        and contract.expected_direction == "must_exist"
    }
    raw_admitted_llm_candidates, binding_dispositions = (
        suppress_contradicted_ambiguous_source_candidates(
            pair,
            raw_admitted_llm_candidates,
            grounding_responses,
        )
    )
    admitted_llm_candidates, llm_macro_dispositions = (
        suppress_satisfied_source_transition_candidates(
            raw_admitted_llm_candidates,
            source_transition_closures,
            candidate_origin="grounding",
        )
    )
    frontier_candidates, frontier_macro_dispositions = (
        suppress_satisfied_source_transition_candidates(
            frontier_candidates,
            source_transition_closures,
            candidate_origin="deterministic_frontier",
        )
    )
    primary_route_projection = route_primary_candidates(
        pair,
        contracts_by_id,
        grounding_responses,
        [*admitted_llm_candidates, *frontier_candidates],
    )
    routed_primary_candidates = list(primary_route_projection.candidates)
    exact_s2_candidates, exact_s2_receipts = (
        _materialize_exact_s2_inventory_candidates(
            pair,
            contract_response,
            routed_primary_candidates,
            source_transition_closures,
        )
    )
    execution_probe_candidates, execution_probe_contracts, execution_probe_dispositions = (
        _materialize_deterministic_execution_probes(
            pair,
            contracts_by_id,
            grounding_responses,
            [*routed_primary_candidates, *exact_s2_candidates],
            transition_groups=(
                *contract_response.transition_groups,
                *[
                    group
                    for grounding_response in grounding_responses
                    for group in grounding_response.additional_transition_groups
                ],
            ),
            frontier_batch=frontier_batch,
        )
    )
    contracts_by_id.update(execution_probe_contracts)
    candidates = [
        *routed_primary_candidates,
        *exact_s2_candidates,
        *execution_probe_candidates,
    ]
    records: list[dict[str, Any]] = []
    release: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = list(all_errors)
    prepared_candidates: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        try:
            prepared = _prepare_candidate(
                pair,
                candidate,
                round_index,
                index,
                contracts_by_id,
            )
            prepared_candidates.append(prepared)
        except Exception as exc:  # noqa: BLE001 - preserve candidate diagnostics
            errors.append({"candidate_index": index, "error_type": type(exc).__name__, "message": str(exc), "reason": "Candidate processing failed; the cell remains readable.", "basis": "Candidate-level diagnostic preservation."})
    finding_candidates = [
        item for item in prepared_candidates if _prepared_is_finding_candidate(item)
    ]
    satisfied_candidates = [
        item for item in prepared_candidates if not _prepared_is_finding_candidate(item)
    ]
    execution_receipts = [
        build_predicate_execution_receipt(
            pair_id=pair.pair_id,
            run_id=run_identity["run_id"],
            contract_id=item["candidate"].contract_id,
            obligation_id=item["obligation_id"],
            plan=item["plan"],
            receipt=item["receipt"],
            source_attribution=item["source_attribution"],
            binding_precise=item["binding"].precise,
        )
        for item in prepared_candidates
    ]
    primary_route_witness_levels = {
        str(item["obligation_id"]): calculate_witness_level(
            item["binding"], item["plan"], item["receipt"]
        )
        for item in prepared_candidates
        if item["candidate"].predicate_id is not None
    }
    primary_route_telemetry = finalize_route_telemetry(
        primary_route_projection.telemetry,
        prepared_candidates,
        primary_route_witness_levels,
    )
    stage_outputs["execute_batch"] = {
        "candidate_count": len(candidates),
        "llm_candidate_count": len(response.issues),
        "unresolved_admitted_candidate_count": len(unresolved_candidates),
        "unresolved_admission": unresolved_admission,
        "retention_carrier_dispositions": retention_carrier_dispositions,
        "carrier_preflight_dispositions": endpoint_preflight_dispositions,
        "root_wrapper_preflight_dispositions": root_wrapper_preflight_dispositions,
        "route_controller_preflight_dispositions": route_controller_preflight_dispositions,
        "admitted_llm_candidate_count": len(admitted_llm_candidates),
        "primary_route_telemetry": [
            row.model_dump(mode="json") for row in primary_route_telemetry
        ],
        "source_transition_macro_closure_count": len(source_transition_closures),
        "source_transition_macro_closures": [
            receipt.model_dump(mode="json")
            for receipt in source_transition_closures.values()
        ],
        "source_transition_suppressed_candidate_count": len(binding_dispositions)
        + len(llm_macro_dispositions)
        + len(frontier_macro_dispositions),
        "source_transition_candidate_dispositions": [
            receipt.model_dump(mode="json")
            for receipt in (
                *binding_dispositions,
                *llm_macro_dispositions,
                *frontier_macro_dispositions,
            )
        ],
        "superseded_llm_candidate_contract_ids": list(
            frontier_batch.superseded_candidate_contract_ids
        ),
        "frontier_candidate_count": len(frontier_candidates),
        "frontier_unresolved_admission": frontier_unresolved_admission,
        "frontier_unresolved_admitted_candidate_count": len(
            frontier_unresolved_candidates
        ),
        "frontier_batch": frontier_batch.model_dump(mode="json"),
        "exact_s2_scout_candidate_count": len(exact_s2_candidates),
        "exact_s2_scout_receipts": exact_s2_receipts,
        "execution_probe_count": len(execution_probe_candidates),
        "execution_probe_dispositions": execution_probe_dispositions,
        "prepared_count": len(prepared_candidates),
        "finding_count": len(finding_candidates),
        "satisfied_count": len(satisfied_candidates),
        "finding_obligation_ids": [
            item["obligation_id"] for item in finding_candidates
        ],
        "satisfied_obligation_ids": [
            item["obligation_id"] for item in satisfied_candidates
        ],
        "predicate_execution_receipts": execution_receipts,
        "candidates": [_jsonable(item) for item in prepared_candidates],
        "reason": "Exact binding, protected source-transition macro closure, primary typed-contract predicate routing, the typed domain frontier, the exact S2 inventory scout, frozen predicate compilation, and deterministic backend execution were applied inside one execute batch; completed true receipts remain passing-check audit records while only counterexamples, unresolved W1/W0, or errors become findings.",
        "basis": "LLM-established typed contracts, exact source inventory, published working-contract macro membership, owned source/ModelIR/inspection facts, frozen predicate registry, compiler plans, backend receipts, primary-route telemetry, and the passing-check exclusion rule",
    }
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:execute-batch",
            stage_name="execute_batch",
            status="completed" if len(prepared_candidates) == len(candidates) else "completed_with_diagnostics",
            artifact_roles=("natural_language", "fcstm_model", "source_inventory", "working_contract", "inspection_equivalent_facts", "verify_facts", "smt_facts", "predicate_registry"),
            output=stage_outputs["execute_batch"],
            reason=stage_outputs["execute_batch"]["reason"],
            basis=stage_outputs["execute_batch"]["basis"],
        )
    )

    d_prompts: list[str] = []
    d_correction_prompts: list[str] = []
    d_stage_outcome: StructuredCallOutcome[DAdjudicationResponse] | None = None
    d_stage_succeeded = True
    d_prompt_budget = _d_prompt_character_budget(runtime)
    d_batch_audit: list[dict[str, Any]] = []
    d_correction_batch_audit: list[dict[str, Any]] = []
    expected_ids = [item["obligation_id"] for item in finding_candidates]
    d_response = DAdjudicationResponse(
        decisions=[],
        reason="No executed candidate required semantic D adjudication.",
        basis="the exact execute-batch candidate set is empty",
    )
    decisions: dict[str, SemanticAdjudication] = {}
    validation_output: dict[str, Any] = {
        "expected_obligation_ids": expected_ids,
        "initial_missing_ids": [],
        "initial_extra_ids": [],
        "initial_duplicate_ids": [],
        "initial_invalid_decisions": {},
        "repair_attempted": False,
        "repair_missing_ids": [],
        "repair_extra_ids": [],
        "repair_duplicate_ids": [],
        "repair_invalid_decisions": {},
        "final_unresolved_ids": [],
        "deterministic_shape_normalizations": [],
        "prompt_character_budget": d_prompt_budget,
        "initial_batches": d_batch_audit,
        "repair_batches": d_correction_batch_audit,
        "reason": "D validation checked exact obligation coverage, uniqueness, closed enums, and decidable typed-fact contradictions.",
        "basis": "obligation IDs, typed SemanticAdjudication fields, and exact closed-model outgoing-transition inventory",
    }
    d_shape_normalizations: list[dict[str, Any]] = []
    if finding_candidates:
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
            for item in finding_candidates
        ]
        d_batches = build_d_adjudication_batches(
            pair,
            dossiers,
            character_budget=d_prompt_budget,
        )
        initial_decisions: list[SemanticAdjudication] = []
        for batch in d_batches:
            d_prompts.append(batch.prompt)
            batch_artifact = (
                f"method/{pair.pair_id}/round-{round_index}/d-adjudication"
                if len(d_batches) == 1
                else (
                    f"method/{pair.pair_id}/round-{round_index}/"
                    f"d-adjudication/batch-{batch.batch_index:03d}"
                )
            )
            batch_audit: dict[str, Any] = {
                "batch_index": batch.batch_index,
                "obligation_ids": list(batch.obligation_ids),
                "prompt_characters": batch.prompt_characters,
                "character_budget": batch.character_budget,
                "exceeds_budget": batch.exceeds_budget,
                "artifact_id": batch_artifact,
                "status": "pending",
                "reason": batch.reason,
                "basis": batch.basis,
            }
            if batch.exceeds_budget:
                d_stage_succeeded = False
                batch_audit["status"] = "failed_with_receipt"
                batch_audit["failure_kind"] = "context_budget_exceeded"
                initial_decisions.extend(
                    fallback_d_adjudication(
                        list(batch.obligation_ids),
                        "One complete D dossier exceeds the pre-provider context budget",
                    ).decisions
                )
                errors.append(
                    {
                        "stage": "d_adjudication",
                        "batch_index": batch.batch_index,
                        "obligation_ids": list(batch.obligation_ids),
                        "error": "context_budget_exceeded",
                        "reason": "The indivisible semantic dossier exceeded the bounded D prompt budget and was downgraded without a provider call.",
                        "basis": batch.basis,
                    }
                )
                d_batch_audit.append(batch_audit)
                continue
            d_outcome: StructuredCallOutcome[DAdjudicationResponse] = runtime.call(
                kind="d_adjudication",
                schema=DAdjudicationResponse,
                system_prompt=D_SYSTEM_PROMPT,
                prompt=batch.prompt,
                artifact_id=batch_artifact,
            )
            all_outcomes.append(d_outcome)
            d_stage_outcome = d_outcome
            batch_audit["status"] = (
                "completed" if d_outcome.succeeded else "failed_with_receipt"
            )
            batch_audit["context_budget"] = d_outcome.context_budget.model_dump(
                mode="json"
            )
            batch_audit["call_id"] = d_outcome.result.get("call_id")
            if d_outcome.succeeded:
                initial_decisions.extend(d_outcome.response.decisions)
            else:
                d_stage_succeeded = False
                batch_error = d_outcome.result.get(
                    "error", "D adjudication output unavailable"
                )
                batch_audit["failure_kind"] = batch_error
                initial_decisions.extend(
                    fallback_d_adjudication(
                        list(batch.obligation_ids),
                        str(batch_error),
                    ).decisions
                )
                errors.append(
                    {
                        "stage": "d_adjudication",
                        "batch_index": batch.batch_index,
                        "obligation_ids": list(batch.obligation_ids),
                        "error": batch_error,
                        "reason": "One typed semantic D batch failed and only that batch was downgraded to explicit unresolved decisions.",
                        "basis": "public structured runtime outcome, stable obligation-ID batching, and no-silent-drop D fallback",
                    }
                )
            d_batch_audit.append(batch_audit)
        d_response = DAdjudicationResponse(
            decisions=initial_decisions,
            reason="Stable bounded D batches adjudicated every finding dossier or retained an explicit unresolved fallback.",
            basis="dossier-prompt-projection.v4, exact obligation-ID partitioning, and public structured runtime receipts",
        )
        expected_id_set = set(expected_ids)

        def coverage(
            response: DAdjudicationResponse,
        ) -> tuple[list[SemanticAdjudication], list[str], list[str], list[str]]:
            supplied_decisions = [
                _normalize_d_decision_shape(
                    decision,
                    stage="initial",
                    normalization_log=d_shape_normalizations,
                )
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
        prepared_by_id = {
            item["obligation_id"]: item for item in finding_candidates
        }
        invalid_decisions = {
            decision.obligation_id: decision_errors
            for decision in unique_supplied
            if (
                decision_errors := _d_decision_consistency_errors(
                    decision,
                    prepared=prepared_by_id.get(decision.obligation_id),
                    pair=pair,
                )
            )
        }
        validation_output.update(
            {
                "initial_missing_ids": missing_ids,
                "initial_extra_ids": extra_ids,
                "initial_duplicate_ids": duplicate_ids,
                "initial_invalid_decisions": invalid_decisions,
            }
        )
        repair_ids = set(missing_ids) | set(duplicate_ids) | set(invalid_decisions)
        frozen_decisions = [
            decision
            for decision in unique_supplied
            if decision.obligation_id not in repair_ids
        ]
        if repair_ids:
            validation_output["repair_attempted"] = True
            correction_batches = build_d_correction_batches(
                pair,
                dossiers,
                missing_ids=missing_ids,
                duplicate_ids=duplicate_ids,
                extra_ids=extra_ids,
                invalid_decisions=invalid_decisions,
                character_budget=d_prompt_budget,
            )
            correction_rows: list[SemanticAdjudication] = []
            for batch in correction_batches:
                d_correction_prompts.append(batch.prompt)
                batch_artifact = (
                    f"method/{pair.pair_id}/round-{round_index}/d-adjudication-correction"
                    if len(correction_batches) == 1
                    else (
                        f"method/{pair.pair_id}/round-{round_index}/"
                        f"d-adjudication-correction/batch-{batch.batch_index:03d}"
                    )
                )
                batch_audit = {
                    "batch_index": batch.batch_index,
                    "obligation_ids": list(batch.obligation_ids),
                    "prompt_characters": batch.prompt_characters,
                    "character_budget": batch.character_budget,
                    "exceeds_budget": batch.exceeds_budget,
                    "artifact_id": batch_artifact,
                    "status": "pending",
                    "reason": batch.reason,
                    "basis": batch.basis,
                }
                if batch.exceeds_budget:
                    d_stage_succeeded = False
                    batch_audit["status"] = "failed_with_receipt"
                    batch_audit["failure_kind"] = "context_budget_exceeded"
                    errors.append(
                        {
                            "stage": "d_adjudication_correction",
                            "batch_index": batch.batch_index,
                            "obligation_ids": list(batch.obligation_ids),
                            "error": "context_budget_exceeded",
                            "reason": "The indivisible correction dossier exceeded the bounded prompt budget and remained unresolved without a provider call.",
                            "basis": batch.basis,
                        }
                    )
                    d_correction_batch_audit.append(batch_audit)
                    continue
                correction_outcome: StructuredCallOutcome[DAdjudicationResponse] = runtime.call(
                    kind="d_adjudication_correction",
                    schema=DAdjudicationResponse,
                    system_prompt=D_SYSTEM_PROMPT,
                    prompt=batch.prompt,
                    artifact_id=batch_artifact,
                )
                all_outcomes.append(correction_outcome)
                d_stage_outcome = correction_outcome
                batch_audit["status"] = (
                    "completed"
                    if correction_outcome.succeeded
                    else "failed_with_receipt"
                )
                batch_audit["context_budget"] = (
                    correction_outcome.context_budget.model_dump(mode="json")
                )
                batch_audit["call_id"] = correction_outcome.result.get("call_id")
                if correction_outcome.succeeded:
                    correction_rows.extend(
                        _normalize_d_decision_shape(
                            decision,
                            stage="correction",
                            normalization_log=d_shape_normalizations,
                        )
                        for decision in correction_outcome.response.decisions
                    )
                else:
                    d_stage_succeeded = False
                    batch_error = correction_outcome.result.get(
                        "error", "D correction output unavailable"
                    )
                    batch_audit["failure_kind"] = batch_error
                    errors.append(
                        {
                            "stage": "d_adjudication_correction",
                            "batch_index": batch.batch_index,
                            "obligation_ids": list(batch.obligation_ids),
                            "error": batch_error,
                            "reason": "One D correction batch failed; only its obligation IDs remain unresolved.",
                            "basis": "bounded in-node correction and public runtime outcome",
                        }
                    )
                d_correction_batch_audit.append(batch_audit)
            correction_extra = [
                decision.obligation_id
                for decision in correction_rows
                if decision.obligation_id not in repair_ids
            ]
            repair_groups: dict[str, list[SemanticAdjudication]] = {}
            for decision in correction_rows:
                if decision.obligation_id in repair_ids:
                    repair_groups.setdefault(decision.obligation_id, []).append(decision)
            correction_duplicate = [
                obligation_id
                for obligation_id, rows in repair_groups.items()
                if len(rows) > 1
            ]
            correction_missing = [
                obligation_id
                for obligation_id in expected_ids
                if obligation_id in repair_ids
                and len(repair_groups.get(obligation_id, [])) != 1
            ]
            correction_invalid = {
                obligation_id: decision_errors
                for obligation_id, rows in repair_groups.items()
                if len(rows) == 1
                and (
                    decision_errors := _d_decision_consistency_errors(
                        rows[0],
                        prepared=prepared_by_id.get(obligation_id),
                        pair=pair,
                    )
                )
            }
            repaired = [
                rows[0]
                for obligation_id, rows in repair_groups.items()
                if len(rows) == 1 and obligation_id not in correction_invalid
            ]
            unique_supplied = [*frozen_decisions, *repaired]
            validation_output.update(
                {
                    "repair_missing_ids": correction_missing,
                    "repair_extra_ids": correction_extra,
                    "repair_duplicate_ids": correction_duplicate,
                    "repair_invalid_decisions": correction_invalid,
                }
            )
        else:
            unique_supplied = frozen_decisions

        final_by_id = {
            decision.obligation_id: decision for decision in unique_supplied
        }
        final_unresolved_ids = [
            obligation_id
            for obligation_id in expected_ids
            if obligation_id not in final_by_id
        ]
        validation_output["final_unresolved_ids"] = final_unresolved_ids
        if final_unresolved_ids:
            d_stage_succeeded = False
            diagnostics: list[str] = []
            if missing_ids:
                diagnostics.append(f"missing={missing_ids}")
            if extra_ids:
                diagnostics.append(f"extra={extra_ids}")
            if duplicate_ids:
                diagnostics.append(f"duplicate={duplicate_ids}")
            if invalid_decisions:
                diagnostics.append(f"invalid={invalid_decisions}")
            if validation_output["repair_missing_ids"]:
                diagnostics.append(
                    f"repair_missing={validation_output['repair_missing_ids']}"
                )
            if validation_output["repair_extra_ids"]:
                diagnostics.append(
                    f"repair_extra={validation_output['repair_extra_ids']}"
                )
            if validation_output["repair_duplicate_ids"]:
                diagnostics.append(
                    f"repair_duplicate={validation_output['repair_duplicate_ids']}"
                )
            if validation_output["repair_invalid_decisions"]:
                diagnostics.append(
                    f"repair_invalid={validation_output['repair_invalid_decisions']}"
                )
            errors.append(
                {
                    "stage": "d_adjudication",
                    "error": "; ".join(diagnostics),
                    "reason": "D structured output and its one targeted repair did not close every obligation; remaining units were retained as unresolved.",
                    "basis": "deterministic obligation-ID coverage and uniqueness check",
                }
            )
        if final_unresolved_ids:
            missing_response = fallback_d_adjudication(
                final_unresolved_ids,
                "D structured output validation or targeted repair did not close",
            )
            final_by_id.update(
                (decision.obligation_id, decision)
                for decision in missing_response.decisions
            )
        ordered_decisions = [final_by_id[obligation_id] for obligation_id in expected_ids]
        d_response = d_response.model_copy(update={"decisions": ordered_decisions})
        decisions = {
            decision.obligation_id: decision for decision in ordered_decisions
        }
        validation_output["deterministic_shape_normalizations"] = d_shape_normalizations

    stage_outputs["d_adjudication"] = d_response.model_dump(mode="json")
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:d-adjudication",
            stage_name="d_adjudication",
            status=(
                "completed"
                if not finding_candidates or d_stage_succeeded
                else "completed_with_diagnostics"
            ),
            artifact_roles=("natural_language", "plantuml_source", "canonical_source_ir", "source_inventory", "fcstm_model", "working_contract", "source_trace", "predicate_registry"),
            output=d_response,
            outcome=d_stage_outcome,
            diagnostics=(*d_batch_audit, *d_correction_batch_audit),
            projection_version=(
                "dossier-prompt-projection.v4-batched"
                if finding_candidates
                else None
            ),
            reason=d_response.reason,
            basis=d_response.basis,
        )
    )
    stage_outputs["validate_d"] = validation_output
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:validate-d",
            stage_name="validate_d",
            status=(
                "completed"
                if not validation_output["final_unresolved_ids"]
                else "completed_with_diagnostics"
            ),
            artifact_roles=("natural_language", "fcstm_model", "predicate_registry"),
            output=validation_output,
            reason=validation_output["reason"],
            basis=validation_output["basis"],
        )
    )
    retry_records = [
        {"stage": outcome.kind, **attempt}
        for outcome in all_outcomes
        for attempt in outcome.attempts
    ]
    for index, prepared in enumerate(finding_candidates):
        try:
            record, emitted = _deterministic_candidate(
                pair,
                prepared["candidate"],
                round_index,
                index,
                retry_records,
                semantic_adjudication=decisions.get(prepared["obligation_id"]),
                prepared=prepared,
                run_id=run_identity["run_id"],
            )
            records.append(record)
            if emitted is not None:
                release.append(emitted)
            if record.get("audit_bundle") is not None:
                audit_path = output_root / "audit_bundles" / f"{record['issue_id']}.json"
                write_json(audit_path, record["audit_bundle"])
                record["audit_bundle_path"] = str(audit_path)
        except Exception as exc:  # noqa: BLE001 - preserve publication diagnostics
            errors.append({"candidate_index": index, "error_type": type(exc).__name__, "message": str(exc), "reason": "Candidate publication failed; the cell remains readable.", "basis": "Candidate-level diagnostic preservation."})
    release = _deduplicate_release_issues(release)
    publish_output = {
        "evidence_record_count": len(records),
        "pre_dedup_release_count": sum(
            bool(record.get("issue_emitted")) for record in records
        ),
        "report_issue_count": len(release),
        "report_issue_ids": [item["issue_id"] for item in release],
        "w_distribution": dict(
            Counter(str(record.get("witness_level")) for record in records)
        ),
        "d_distribution": dict(
            Counter(str(record.get("d_level")) for record in records)
        ),
        "reason": "Deterministic W publication retained only D1/D2 violations and collapsed exact typed duplicate defects.",
        "basis": "binding completeness, frozen predicate support, backend terminal verdict, method-owned D, and exact-typed-defect-key.v1",
    }
    stage_outputs["publish"] = publish_output
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:publish",
            stage_name="publish",
            status=(
                "completed"
                if len(records) == len(finding_candidates)
                else "completed_with_diagnostics"
            ),
            artifact_roles=("fcstm_model", "predicate_registry", "verify_facts"),
            output=publish_output,
            reason=publish_output["reason"],
            basis=publish_output["basis"],
        )
    )
    prompt_hash = _hash_json(
        {
            "contract_extraction": contract_prompt,
            "discovery_grounding": grounding_prompts,
            "d_adjudication": d_prompts,
            "d_adjudication_correction": d_correction_prompts,
        }
    )
    llm_call = _aggregate_outcomes(all_outcomes)
    contract_ready = contract_outcome.real_llm and contract_outcome.succeeded
    grounding_ready = [
        outcome.real_llm and outcome.succeeded
        for outcome in grounding_outcomes
    ]
    semantic_result_available = bool(records) or all(grounding_ready)
    eligible = bool(
        contract_ready
        and any(grounding_ready)
        and semantic_result_available
    )
    eligibility_reasons = (
        [
            "real_contract_output",
            "at_least_one_completed_grounding_lens",
            "auditable_semantic_result",
            "method_receipt_complete",
        ]
        if eligible
        else [
            *([] if contract_ready else ["contract_output_unavailable_or_fixture"]),
            *([] if any(grounding_ready) else ["grounding_outputs_unavailable_or_fixture"]),
            *([] if semantic_result_available else ["no_auditable_semantic_result"]),
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
            if eligible and not errors
            else "completed_with_diagnostics"
            if eligible
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
        "predicate_execution_receipts": execution_receipts,
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


def _grounding_response_contract(
    contracts: Sequence[NLContract],
) -> type[ExactGroundingResponse]:
    """Specialize grounding identity and cardinality coverage to one method cell."""

    expected_contract_ids = tuple(contract.contract_id for contract in contracts)
    if len(expected_contract_ids) != len(set(expected_contract_ids)):
        raise ValueError("grounding input contains duplicate contract IDs")
    expected_cardinality_contract_ids = tuple(
        contract.contract_id
        for contract in contracts
        if contract.property == "cardinality"
    )
    contract_key = _hash_json(
        {
            "version": GROUNDING_EXACT_IDENTITY_CONTRACT_VERSION,
            "contract_ids": expected_contract_ids,
            "cardinality_contract_ids": expected_cardinality_contract_ids,
        }
    ).removeprefix("sha256:")[:16]
    cardinality_description = (
        "Typed member-domain accounting for cardinality contracts. Unlike the "
        "other sparse grounding rows, this list is exhaustive for the supplied "
        "property=cardinality contracts in this method cell: return exactly one "
        "exact, ambiguous, or unbound row for each required ID, even when this "
        "lens cannot select a domain or owner. Schema correction must return a "
        "complete replacement response retaining every previously valid row. "
        "Rows never contain observed counts, W, D, L, or ledger data. Required "
        f"supplied cardinality contract IDs={list(expected_cardinality_contract_ids)!r}."
    )
    response_model = create_model(
        f"ExactGroundingResponse_{contract_key}",
        __base__=ExactGroundingResponse,
        cardinality_bindings=(
            list[CardinalityDomainBinding],
            Field(default_factory=list, description=cardinality_description),
        ),
    )
    response_model.__doc__ = (
        "Runtime-specialized grounding response. All contract_id references "
        "must resolve to the supplied contract set or one typed additional "
        "contract declared in this response. The supplied set may be empty; in "
        "that case only same-response additional contracts may be referenced. "
        "Every supplied cardinality contract "
        "must also receive exactly one typed domain row in this lens, including an "
        "explicit ambiguous or unbound row when no exact reading closes. These "
        "structural checks have no authority over semantic discovery, W, D, L, "
        "publication or external evaluation decisions."
    )
    response_model.expected_contract_ids = expected_contract_ids
    response_model.expected_cardinality_contract_ids = (
        expected_cardinality_contract_ids
    )
    response_model.enforce_exact_identity_contract = True
    response_model.model_rebuild(force=True)
    return response_model


def _method_metrics(
    *,
    pair_method: dict[str, list[dict[str, Any]]],
    selected_pair_ids: Sequence[str],
    ineligible_pair_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Aggregate only method-owned eligibility, releases, D/W, and diagnostics."""

    registry = load_registry()
    forced_ineligible = set(ineligible_pair_ids)
    all_cells = [cell for cells in pair_method.values() for cell in cells]
    eligible_cells = [
        cell
        for pair_id, cells in pair_method.items()
        for cell in cells
        if cell.get("eligible") and pair_id not in forced_ineligible
    ]
    records = [
        record
        for cell in all_cells
        for record in cell.get("evidence_records", [])
    ]
    releases = [
        issue
        for cell in all_cells
        for issue in cell.get("report_issue_clusters", [])
    ]
    execution_receipts = [
        receipt
        for cell in all_cells
        for receipt in cell.get("predicate_execution_receipts", [])
    ]
    executed_predicates = sorted(
        {
            receipt.get("predicate_id")
            for receipt in execution_receipts
            if receipt.get("execution_status") == "executed"
            and receipt.get("predicate_id")
        }
    )
    w2_records = [
        record
        for record in records
        if record.get("witness_level") == "W2"
    ]
    eligible_releases = [
        issue
        for pair_id, cells in pair_method.items()
        if pair_id not in forced_ineligible
        for cell in cells
        if cell.get("eligible")
        for issue in cell.get("report_issue_clusters", [])
    ]
    per_pair: dict[str, dict[str, Any]] = {}
    for pair_id in selected_pair_ids:
        pair_cells = pair_method.get(pair_id, [])
        pair_records = [
            record
            for cell in pair_cells
            for record in cell.get("evidence_records", [])
        ]
        pair_releases = [
            issue
            for cell in pair_cells
            for issue in cell.get("report_issue_clusters", [])
        ]
        pair_execution_receipts = [
            receipt
            for cell in pair_cells
            for receipt in cell.get("predicate_execution_receipts", [])
        ]
        pair_eligible_cells = [
            cell
            for cell in pair_cells
            if cell.get("eligible") and pair_id not in forced_ineligible
        ]
        per_pair[pair_id] = {
            "method_cells": len(pair_cells),
            "eligible_method_cells": len(pair_eligible_cells),
            "release_issue_count": len(pair_releases),
            "eligible_release_issue_count": sum(
                len(cell.get("report_issue_clusters", []))
                for cell in pair_eligible_cells
            ),
            "evidence_record_count": len(pair_records),
            "witness_levels": dict(
                Counter(record.get("witness_level") for record in pair_records)
            ),
            "d_levels": dict(
                Counter(record.get("d_level") for record in pair_records)
            ),
            "unresolved_or_error_records": sum(
                int(
                    record.get("d_level") == "D_UNRESOLVED"
                    or record.get("execution_receipt", {}).get("execution_state") == "failed"
                )
                for record in pair_records
            ),
            "method_diagnostics": sum(
                len(cell.get("errors", [])) for cell in pair_cells
            ),
            "predicate_execution_receipts": len(pair_execution_receipts),
            "executed_predicates": sorted(
                {
                    receipt.get("predicate_id")
                    for receipt in pair_execution_receipts
                    if receipt.get("execution_status") == "executed"
                    and receipt.get("predicate_id")
                }
            ),
        }
    return {
        "method": {
            "method_cells": len(all_cells),
            "eligible_method_cells": len(eligible_cells),
            "method_cell_eligible_rate": (
                len(eligible_cells) / len(all_cells) if all_cells else 0.0
            ),
            "release_issue_count": len(releases),
            "eligible_release_issue_count": len(eligible_releases),
            "evidence_record_count": len(records),
            "witness_levels": dict(
                Counter(record.get("witness_level") for record in records)
            ),
            "d_levels": dict(Counter(record.get("d_level") for record in records)),
            "unresolved_or_error_records": sum(
                int(
                    record.get("d_level") == "D_UNRESOLVED"
                    or record.get("execution_receipt", {}).get("execution_state") == "failed"
                )
                for record in records
            ),
            "method_diagnostics": sum(
                len(cell.get("errors", [])) for cell in all_cells
            ),
            "predicate_execution_receipts": len(execution_receipts),
            "executed_predicates": executed_predicates,
            "execution_verdicts": dict(
                Counter(receipt.get("verdict") for receipt in execution_receipts)
            ),
            "coverage_accounting": {
                "predicate_execution_coverage": {
                    "executed_distinct_predicates": len(executed_predicates),
                    "registry_predicate_denominator": len(registry.predicates),
                    "executed_predicates": executed_predicates,
                    "basis": "terminal PredicateExecutionReceipt records only; prompt appearance and plans do not count",
                },
                "w2_finding_coverage": {
                    "w2_evidence_record_count": len(w2_records),
                    "w2_finding_record_count": sum(
                        bool(record.get("issue_emitted")) for record in w2_records
                    ),
                    "basis": "method-owned evidence records and deterministic witness level",
                },
                "full_w2_ledger_coverage": {
                    "status": "pending_external_judge_mapping",
                    "reason": "The method does not read ledger expectations; FULL/W2 ledger coverage is computed only after frozen external Judge expected mapping.",
                    "basis": "method/evaluation physical isolation boundary",
                },
            },
        },
        "per_pair": per_pair,
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


def _write_pair_status(
    output_root: Path,
    pair_id: str,
    status: dict[str, Any],
) -> dict[str, Any]:
    payload = PairRunStatus.model_validate(
        {
            "schema": "evidence-discovery.pair_status.v3",
            "pair_id": pair_id,
            **status,
            "reason": status.get("reason", "Pair status was computed from terminal method receipts and W2 audits."),
            "basis": status.get("basis", "frozen method cells, W2 audit links, usage, and run contract"),
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
            "schema": "evidence-discovery.stale_artifact.v1",
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


def _load_pair_receipts(
    *,
    output_root: Path,
    pair_id: str,
    rounds: int,
    run_identity: dict[str, Any],
) -> list[dict[str, Any]]:
    """Load only a contiguous compatible method-cell prefix."""

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
    return rounds_data


def _cost_total(receipt: dict[str, Any]) -> float:
    value = receipt.get("llm_call", {}).get("cost", {}).get("total_usd")
    return float(value) if isinstance(value, (int, float)) else 0.0


def _finalize_w2_audit_links(
    *,
    output_root: Path,
    pair_id: str,
    rounds_data: list[dict[str, Any]],
) -> None:
    """Link W2 bundles to immutable method receipts and leave Judge pending."""

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
                and finalization.get("method_receipt_hash") == method_hash
                and bundle.get("method_receipt", {}).get("sha256") == method_hash
                and bundle.get("judge_receipt", {}).get("status")
                == "pending_independent_judge"
            ):
                continue
            if bundle.get("pre_finalization_audit_hash") is None:
                bundle["pre_finalization_audit_hash"] = bundle.get("audit_hash")
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
                "reason": "This is the exact terminal method receipt that owns the W2 evidence bundle.",
                "basis": "atomically written method-cell JSON",
            }
            bundle["judge_receipt"] = {
                "status": "pending_independent_judge",
                "protocol": "semantic-judge.two-stage.v3.2",
                "reason": "Formal validity, relation, hit, and FP are produced only by the external frozen evaluation layer.",
                "basis": "method/evaluation physical isolation boundary",
            }
            bundle["audit_finalization"] = {
                "finalized_at": datetime.now(timezone.utc).isoformat(),
                "method_receipt_hash": method_hash,
                "pre_finalization_audit_hash": bundle[
                    "pre_finalization_audit_hash"
                ],
                "reason": "The W2 bundle was finalized when its owning method receipt became terminal; independent evaluation remains pending.",
                "basis": "method-only orchestration and atomic receipt writes",
            }
            write_json(audit_path, validate_and_hash_w2_audit_bundle(bundle))


def _pair_status(
    *,
    pair_id: str,
    started_at: str,
    rounds_data: list[dict[str, Any]],
    run_identity: dict[str, Any],
    audit_errors: int = 0,
    resume_action: str = "reconstructed_terminal_status",
) -> dict[str, Any]:
    method_errors = sum(len(cell.get("errors", [])) for cell in rounds_data)
    method_eligible = sum(int(bool(cell.get("eligible"))) for cell in rounds_data)
    method_cost_eligible = all(
        bool(cell.get("llm_call", {}).get("cost", {}).get("eligible"))
        for cell in rounds_data
    )
    failed = bool(
        audit_errors
        or any(cell.get("status") == "failed_with_receipt" for cell in rounds_data)
    )
    clean = bool(
        not failed
        and method_errors == 0
        and method_eligible == len(rounds_data)
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
        "errors": method_errors + audit_errors,
        "audit_errors": audit_errors,
        "method_cost_usd": sum(_cost_total(cell) for cell in rounds_data),
        "method_cost_eligible": method_cost_eligible,
        "reason": "Pair status was derived only from complete method cells, W2 audit links, diagnostics, and audited usage.",
        "basis": "method receipts sharing the exact run contract and pair input identity",
    }


def _finalize_w2_audit_links_with_receipt(
    *,
    output_root: Path,
    pair_id: str,
    rounds_data: list[dict[str, Any]],
) -> int:
    """Keep an audit-finalization bug local to one pair and preserve its cause."""

    try:
        _finalize_w2_audit_links(
            output_root=output_root,
            pair_id=pair_id,
            rounds_data=rounds_data,
        )
        return 0
    except Exception as exc:  # noqa: BLE001 - audit failures must terminalize as receipts
        write_json(
            output_root / "pairs" / pair_id / f"audit-finalization-error-{uuid.uuid4().hex}.json",
            {
                "schema": "evidence-discovery.audit_finalization_error.v1",
                "pair_id": pair_id,
                "error_type": type(exc).__name__,
                "message": str(exc),
                "status": "error",
                "reason": "A W2 bundle could not be linked to its terminal method receipt; the pair is failed with a receipt and the batch continues.",
                "basis": "W2 Pydantic validation and active run-root path boundary",
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
    output_root: Path,
    run_identity: dict[str, Any],
    started_at: str,
    error: BaseException,
) -> dict[str, Any]:
    rounds_data = _load_pair_receipts(
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
    audit_errors = _finalize_w2_audit_links_with_receipt(
        output_root=output_root,
        pair_id=pair_id,
        rounds_data=rounds_data,
    )
    status = _pair_status(
        pair_id=pair_id,
        started_at=started_at,
        rounds_data=rounds_data,
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
    report_root = Path(task["report_root"])
    run_identity = dict(task["run_identity"])
    started_at = _pair_started_at(
        output_root=output_root,
        pair_id=pair_id,
        run_identity=run_identity,
    )
    runtime: Any | None = None
    try:
        rounds_data = _load_pair_receipts(
            output_root=output_root,
            pair_id=pair_id,
            rounds=rounds,
            run_identity=run_identity,
        )
        if len(rounds_data) == rounds:
            audit_errors = _finalize_w2_audit_links_with_receipt(
                output_root=output_root,
                pair_id=pair_id,
                rounds_data=rounds_data,
            )
            status = _pair_status(
                pair_id=pair_id,
                started_at=started_at,
                rounds_data=rounds_data,
                run_identity=run_identity,
                audit_errors=audit_errors,
                resume_action="skipped_compatible_terminal",
            )
            return _write_pair_status(output_root, pair_id, status)

        pair = load_pair(report_root / "pairs" / pair_id)
        if task["profile"] == "fixture":
            runtime = FixtureStructuredRuntime()
        else:
            runtime = PublicStructuredRuntime(
                str(task["profile"]),
                output_root / "llm",
                transport_retries=int(task["transport_retries"]),
                streaming=bool(task["streaming"]),
            )
        resumed_prefix = bool(rounds_data)
        for round_index in range(len(rounds_data) + 1, rounds + 1):
            cell = _method_cell(
                pair=pair,
                round_index=round_index,
                runtime=runtime,
                output_root=output_root,
                run_identity=run_identity,
            )
            rounds_data.append(cell)
        audit_errors = _finalize_w2_audit_links_with_receipt(
            output_root=output_root,
            pair_id=pair_id,
            rounds_data=rounds_data,
        )
        status = _pair_status(
            pair_id=pair_id,
            started_at=started_at,
            rounds_data=rounds_data,
            run_identity=run_identity,
            audit_errors=audit_errors,
            resume_action=(
                "resumed_compatible_prefix" if resumed_prefix else "executed_fresh"
            ),
        )
        return _write_pair_status(output_root, pair_id, status)
    except Exception as exc:  # noqa: BLE001 - pair failures must terminalize as receipts
        return _terminalize_pair_failure(
            pair_id=pair_id,
            rounds=rounds,
            output_root=output_root,
            run_identity=run_identity,
            started_at=started_at,
            error=exc,
        )
    finally:
        if isinstance(runtime, PublicStructuredRuntime):
            runtime.close()


def run_experiment(
    *,
    report_root: str | Path,
    output_dir: str | Path,
    profile: str = "gpt-5.6-luna",
    rounds: int = 3,
    resume: bool = False,
    allow_live: bool = False,
    allow_full_live: bool = False,
    pair_ids: Sequence[str] | None = None,
    workers: int = 16,
    transport_retries: int = DEFAULT_TRANSPORT_RETRIES,
    streaming: bool = True,
    run_id: str | None = None,
    predecessor_snapshot: str | None = None,
    selection_preflight: str | Path | None = None,
) -> dict[str, Any]:
    """Execute a contract-compatible diagnostic or frozen full provider run."""

    if rounds not in {1, 3}:
        raise ValueError("rounds must be 1 for a diagnostic run or 3 for the frozen protocol")
    if workers < 1:
        raise ValueError("workers must be at least 1")
    if transport_retries < 0:
        raise ValueError("transport_retries must be non-negative")
    if profile != "fixture" and not allow_live:
        raise RuntimeError(
            "live provider execution requires explicit allow_live=True after provider-free review"
        )
    if profile == "gpt-5.6-sol" or profile.endswith("-sol"):
        raise RuntimeError("the selected profile is outside the frozen construction and diagnostic protocol")

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
                    "full-protocol provider execution requires explicit allow_full_live=True after bounded diagnostic review"
                )
            if profile != "gpt-5.6-luna" or rounds != 3:
                raise RuntimeError("full live execution requires the frozen model profile and three rounds")
        else:
            if pair_ids is None:
                raise RuntimeError("live diagnostic execution requires explicit pair_ids")
            if len(selected_pair_ids) > len(REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS):
                raise RuntimeError(
                    f"live diagnostic runs are capped at {len(REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS)} explicit pair IDs"
                )

    report_root_path = Path(report_root).expanduser().resolve()
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
    input_data_hash = _hash_json({"pair_input_hashes": pair_input_hashes})
    prompt_schema_hash = _prompt_schema_hash()
    selection_preflight_reference = _load_selection_preflight(
        selection_preflight,
        selected_pair_ids=selected_pair_ids,
    )
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
        rounds=rounds,
        selected_pair_ids=selected_pair_ids,
        workers=workers,
        transport_retries=transport_retries,
        streaming=streaming,
        selection_preflight=selection_preflight_reference,
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
                except Exception as exc:  # noqa: BLE001 - worker failures must terminalize
                    _terminalize_pair_failure(
                        pair_id=pair_id,
                        rounds=rounds,
                        output_root=output_root,
                        run_identity=run_identity,
                        started_at=datetime.now(timezone.utc).isoformat(),
                        error=exc,
                    )

    pair_method: dict[str, list[dict[str, Any]]] = {}
    per_pair: dict[str, dict[str, Any]] = {}
    for pair_id in selected_pair_ids:
        rounds_data = _load_pair_receipts(
            output_root=output_root,
            pair_id=pair_id,
            rounds=rounds,
            run_identity=run_identity,
        )
        if len(rounds_data) != rounds:
            _terminalize_pair_failure(
                pair_id=pair_id,
                rounds=rounds,
                output_root=output_root,
                run_identity=run_identity,
                started_at=datetime.now(timezone.utc).isoformat(),
                error=RuntimeError("pair worker returned without a complete terminal receipt set"),
            )
            rounds_data = _load_pair_receipts(
                output_root=output_root,
                pair_id=pair_id,
                rounds=rounds,
                run_identity=run_identity,
            )
        if len(rounds_data) != rounds:
            raise RuntimeError(f"pair {pair_id} could not be terminalized")
        pair_method[pair_id] = rounds_data
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
                    run_identity=run_identity,
                ),
            )

    metrics = _method_metrics(
        pair_method=pair_method,
        selected_pair_ids=selected_pair_ids,
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
    all_cost_eligible = all(row["method_cost_eligible"] for row in per_pair.values())
    metrics["cost"] = {
        "eligible": all_cost_eligible,
        "method_usd": method_cost,
        "reason": "The method cost uses row-local provider retry exemptions and excludes all independent evaluation calls.",
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
                "frozen representative diagnostic set"
                if set(selected_pair_ids) == set(REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS)
                else "frozen 54-pair protocol" if full_protocol else "explicit diagnostic pair_ids"
            ),
        },
        method_cell_count=sum(len(value) for value in pair_method.values()),
        method_cost_usd=method_cost,
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
        reason="Every selected pair has terminal method receipts and method-owned W2 audits under one strict run identity.",
        basis="four-family-19-core.v1, v3 method-only run manifest, and exact input closure hashes",
    ).model_dump(mode="json")
    write_json(output_root / "summary.json", summary)
    write_markdown_summary(output_root / "SUMMARY.md", summary)
    write_json(
        output_root / "audit_index.json",
        {
            "schema": "evidence-discovery.audit_index.v3",
            "run_id": manifest.run_id,
            "run_contract_hash": manifest.run_contract_hash,
            "pairs": per_pair,
            "method_cell_count": summary["method_cell_count"],
            "reason": "The index points only to artifacts validated under the active run identity.",
            "basis": "v3 method-only pair-status and run-summary receipts",
        },
    )
    final_manifest = manifest.model_copy(
        update={"status": final_status, "updated_at": completed_at}
    )
    write_json(output_root / "run_manifest.json", final_manifest.model_dump(mode="json"))
    return summary
