"""Evaluation-only source-static pyfcstm oracles for sound gold proxies."""

from __future__ import annotations

import argparse
import inspect
import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import Field, JsonValue, model_validator

from .predicate_gold import (
    SHA256_PATTERN,
    ExactnessRelation,
    StrictModel,
    TypedInput,
    canonical_sha256,
    sha256_path,
    write_json,
)

REQUEST_SCHEMA_VERSION = "paper1.predicate-gold.static-oracle-request.v1"
RECEIPT_SCHEMA_VERSION = "paper1.predicate-gold.static-oracle-receipt.v1"
REPLAY_SCHEMA_VERSION = "paper1.predicate-gold.static-oracle-replay.v1"


class StaticOracleId(str, Enum):
    """Narrow source-static oracle contracts admitted by this module."""

    RUNNING_EVENT_ROOT_EXIT_CONSUMERS = "RUNNING_EVENT_ROOT_EXIT_CONSUMERS"
    SEPARATED_CONDITION_TAKEOVER_CONSUMERS = "SEPARATED_CONDITION_TAKEOVER_CONSUMERS"


class ArtifactRole(str, Enum):
    """Role of the FCSTM artifact evaluated by a source-static oracle."""

    DEFECTIVE = "DEFECTIVE"
    POSITIVE_CONTROL = "POSITIVE_CONTROL"


class StaticOracleRequest(StrictModel):
    """Pre-result request for one source-static native-object oracle."""

    schema_version: Literal[REQUEST_SCHEMA_VERSION] = Field(default=REQUEST_SCHEMA_VERSION, description="Source-static oracle request schema version.")
    request_id: str = Field(description="Stable request identity.", pattern=r"^[A-Za-z0-9_.:-]+$")
    ledger_id: str = Field(description="Immutable ledger issue owning the proxy.", min_length=1)
    property_id: str = Field(description="Selected pre-execution proxy identity.", min_length=1)
    property_proposal_sha256: str = Field(description="Hash frozen before execution output was visible.", pattern=SHA256_PATTERN)
    exactness_relation: Literal[ExactnessRelation.O_IMPLIES_P] = Field(
        default=ExactnessRelation.O_IMPLIES_P,
        description="These oracles are sound necessary-condition proxies, never exact gold.",
    )
    oracle_id: StaticOracleId = Field(description="Narrow native-object oracle contract.")
    artifact_role: ArtifactRole = Field(description="Defective artifact or independently justified positive control.")
    artifact_path: str = Field(description="Repository-relative FCSTM artifact path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of exact FCSTM bytes.", pattern=SHA256_PATTERN)
    typed_inputs: tuple[TypedInput, ...] = Field(description="All source-provenanced oracle inputs frozen before execution.", min_length=3)
    assumptions: tuple[str, ...] = Field(description="Representation and source-static assumptions bounding this proxy.")
    expected_boolean_for_acceptance: bool = Field(description="False for defective artifacts and true for positive controls.")
    created_at: str = Field(description="UTC request freeze time.", min_length=1)
    request_sha256: str = Field(description="Canonical request hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_request(self) -> StaticOracleRequest:
        """Enforce exact input vocabulary, role polarity, and request digest."""

        values = {item.field_name: item.normalized_value for item in self.typed_inputs}
        expected_names = {
            StaticOracleId.RUNNING_EVENT_ROOT_EXIT_CONSUMERS: {
                "event_path",
                "required_running_leaf_paths",
                "required_exit_target",
            },
            StaticOracleId.SEPARATED_CONDITION_TAKEOVER_CONSUMERS: {
                "required_event_tokens",
                "state_condition",
                "response_state",
            },
        }[self.oracle_id]
        if set(values) != expected_names or len(values) != len(self.typed_inputs):
            raise ValueError(f"{self.oracle_id.value} requires exactly {sorted(expected_names)}")
        if self.oracle_id == StaticOracleId.RUNNING_EVENT_ROOT_EXIT_CONSUMERS:
            if not isinstance(values["event_path"], str) or not values["event_path"]:
                raise TypeError("event_path must be one exact nonempty path")
            leaves = values["required_running_leaf_paths"]
            if not isinstance(leaves, list) or not leaves or not all(isinstance(item, str) and item for item in leaves):
                raise TypeError("required_running_leaf_paths must be a nonempty exact-path array")
            if values["required_exit_target"] != "[*]":
                raise ValueError("the root-exit oracle admits only the native EXIT_STATE marker [*]")
        else:
            tokens = values["required_event_tokens"]
            if not isinstance(tokens, list) or not tokens or not all(isinstance(item, str) and item for item in tokens):
                raise TypeError("required_event_tokens must be a nonempty exact-token array")
            if len(tokens) != len(set(tokens)):
                raise ValueError("required event tokens must be unique")
            if not isinstance(values["state_condition"], str) or not values["state_condition"]:
                raise TypeError("state_condition must be one exact state path")
            if not isinstance(values["response_state"], str) or not values["response_state"]:
                raise TypeError("response_state must be one exact state path")
        if self.artifact_role == ArtifactRole.DEFECTIVE and self.expected_boolean_for_acceptance is not False:
            raise ValueError("defective proxy requests pre-register false")
        if self.artifact_role == ArtifactRole.POSITIVE_CONTROL and self.expected_boolean_for_acceptance is not True:
            raise ValueError("positive-control proxy requests pre-register true")
        if self.request_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"request_sha256"})):
            raise ValueError("request_sha256 does not match the pre-result request")
        return self


class StaticConstituentResult(StrictModel):
    """One completed Boolean source-static constituent."""

    constituent_id: str = Field(description="Stable check identity.", min_length=1)
    verdict: bool = Field(description="Completed Boolean result.")
    expected: JsonValue = Field(description="Pre-registered identity or structural condition.")
    observed: JsonValue = Field(description="Native declaration/carrier observation.")
    reason: str = Field(description="How the observation determines this necessary condition.", min_length=1)


class StaticOracleReceipt(StrictModel):
    """Hash-sealed completed Boolean receipt for one source-static proxy."""

    schema_version: Literal[RECEIPT_SCHEMA_VERSION] = Field(default=RECEIPT_SCHEMA_VERSION, description="Source-static oracle receipt schema version.")
    request_id: str = Field(description="Request identity.", min_length=1)
    request_sha256: str = Field(description="Hash of the pre-result request.", pattern=SHA256_PATTERN)
    ledger_id: str = Field(description="Ledger issue owning the proxy.", min_length=1)
    property_id: str = Field(description="Selected proxy identity.", min_length=1)
    exactness_relation: Literal[ExactnessRelation.O_IMPLIES_P] = Field(description="Sound necessary-condition direction.")
    oracle_id: StaticOracleId = Field(description="Executed source-static oracle contract.")
    artifact_role: ArtifactRole = Field(description="Defective artifact or positive control.")
    artifact_path: str = Field(description="Repository-relative FCSTM path.", min_length=1)
    artifact_sha256: str = Field(description="Hash of exact FCSTM bytes.", pattern=SHA256_PATTERN)
    state: Literal["COMPLETED_BOOLEAN"] = Field(description="Only completed native-object Booleans are persisted.")
    verdict: bool = Field(description="AND of every persisted constituent.")
    acceptance_match: bool = Field(description="Whether verdict equals the pre-registered artifact-role expectation.")
    observations: tuple[dict[str, JsonValue], ...] = Field(description="Native declaration and authored-carrier inventory used by the checks.")
    constituents: tuple[StaticConstituentResult, ...] = Field(description="All checks evaluated without short-circuiting.", min_length=1)
    query_path: str = Field(description="Receipt-root-relative query JSON path.", min_length=1)
    query_sha256: str = Field(description="Hash of query JSON bytes.", pattern=SHA256_PATTERN)
    code_hashes: dict[str, str] = Field(description="Hashes of this oracle, pyfcstm model code, and native projection code.", min_length=3)
    source_commit: str = Field(description="Main repository commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    pyfcstm_commit: str = Field(description="Pinned pyfcstm commit used for execution.", pattern=r"^[0-9a-f]{40}$")
    command: tuple[str, ...] = Field(description="Exact provider-free replay argv.", min_length=1)
    started_at: str = Field(description="UTC execution start time.", min_length=1)
    completed_at: str = Field(description="UTC execution completion time.", min_length=1)
    replay_status: Literal["NOT_REPLAYED"] = Field(description="Replay is sealed in a separate audit receipt.")
    reason: str = Field(description="Result interpretation that does not overstate the proxy as exact.", min_length=1)
    basis: str = Field(description="Native API, input, artifact, and source-static basis.", min_length=1)
    receipt_sha256: str = Field(description="Canonical receipt hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_receipt(self) -> StaticOracleReceipt:
        """Require complete conjunction and receipt digest closure."""

        if self.verdict != all(item.verdict for item in self.constituents):
            raise ValueError("oracle verdict must equal every constituent Boolean")
        if self.receipt_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"})):
            raise ValueError("receipt_sha256 does not match source-static receipt payload")
        return self


class StaticOracleReplayReceipt(StrictModel):
    """Independent deterministic replay comparison for a source-static oracle."""

    schema_version: Literal[REPLAY_SCHEMA_VERSION] = Field(default=REPLAY_SCHEMA_VERSION, description="Source-static replay-audit schema version.")
    request_sha256: str = Field(description="Hash of the replayed request.", pattern=SHA256_PATTERN)
    original_receipt_path: str = Field(description="Repository-relative original receipt path, or invocation-root-relative path for an external test root.", min_length=1)
    original_receipt_sha256: str = Field(description="Hash of original receipt bytes.", pattern=SHA256_PATTERN)
    replay_receipt_path: str = Field(description="Replay-root-relative replay receipt path.", min_length=1)
    replay_receipt_sha256: str = Field(description="Hash of replay receipt bytes.", pattern=SHA256_PATTERN)
    original_projection_sha256: str = Field(description="Hash of original verdict, observations, and constituents.", pattern=SHA256_PATTERN)
    replay_projection_sha256: str = Field(description="Hash of replay verdict, observations, and constituents.", pattern=SHA256_PATTERN)
    overall_match: bool = Field(description="Whether deterministic semantic projections match.")
    replayed_at: str = Field(description="UTC replay completion time.", min_length=1)
    receipt_sha256: str = Field(description="Canonical replay-audit hash excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_replay(self) -> StaticOracleReplayReceipt:
        """Bind overall_match and replay-audit digest to the compared bytes."""

        if self.overall_match != (self.original_projection_sha256 == self.replay_projection_sha256):
            raise ValueError("overall_match does not reflect semantic projection hashes")
        if self.receipt_sha256 != canonical_sha256(self.model_dump(mode="json", exclude={"receipt_sha256"})):
            raise ValueError("receipt_sha256 does not match replay-audit payload")
        return self


def _utc_now() -> str:
    """Return an RFC 3339 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _values(request: StaticOracleRequest) -> dict[str, JsonValue]:
    """Return the validated input map."""

    return {item.field_name: item.normalized_value for item in request.typed_inputs}


def _state_is_within(state: object, ancestor: object) -> bool:
    """Use exact native parent links to test hierarchy ancestry."""

    current = state
    while current is not None:
        if current is ancestor:
            return True
        current = current.parent
    return False


def _carrier_source_state(document: object, carrier: object) -> object | None:
    """Resolve an authored carrier source through its exact native owner path."""

    from utils.stm_artifacts.fcstm_native_projection import resolve_state

    if carrier.source == "[*]":
        return None
    return resolve_state(document, f"{carrier.owner_path}.{carrier.source}")


def _carrier_observation(carrier: object) -> dict[str, JsonValue]:
    """Serialize only public native authored-carrier facts."""

    return {
        "owner_path": carrier.owner_path,
        "source": carrier.source,
        "target": carrier.target,
        "events": [event.path_name for event in carrier.events],
        "has_guard": carrier.guard is not None,
        "source_line": carrier.source_line,
    }


def _running_event_exit(
    request: StaticOracleRequest,
    document: object,
) -> tuple[tuple[dict[str, JsonValue], ...], tuple[StaticConstituentResult, ...]]:
    """Check one root-exit event consumer on every required running ancestry."""

    from utils.stm_artifacts.fcstm_native_projection import (
        all_transition_carriers,
        resolve_event,
        resolve_state,
        state_path,
    )

    values = _values(request)
    event = resolve_event(document, values["event_path"])
    carriers = all_transition_carriers(document)
    observations = tuple(_carrier_observation(carrier) for carrier in carriers)
    constituents: list[StaticConstituentResult] = []
    event_ok = event is not None and event.path_name == values["event_path"]
    constituents.append(
        StaticConstituentResult(
            constituent_id="event_identity",
            verdict=event_ok,
            expected=values["event_path"],
            observed=event.path_name if event is not None else None,
            reason="Resolved one exact declared native event path; no fuzzy token matching was used.",
        )
    )
    root = document.machine.root_state
    for leaf_path in values["required_running_leaf_paths"]:
        leaf = resolve_state(document, leaf_path)
        matched: list[dict[str, JsonValue]] = []
        if leaf is not None and event is not None:
            current = leaf
            while current is not None and current.parent is not None:
                parent = current.parent
                if parent is root:
                    for carrier in carriers:
                        if (
                            carrier.owner_path == state_path(root)
                            and carrier.source == current.name
                            and carrier.target == values["required_exit_target"]
                            and any(item.path_name == event.path_name for item in carrier.events)
                        ):
                            matched.append(_carrier_observation(carrier))
                current = parent
        constituents.append(
            StaticConstituentResult(
                constituent_id=f"root_exit_consumer:{leaf_path}",
                verdict=bool(matched),
                expected={"leaf_path": leaf_path, "event_path": values["event_path"], "root_exit_target": "[*]"},
                observed=matched,
                reason="Checked the leaf's exact root-child ancestry for an authored event carrier to root EXIT_STATE; root-initial carriers were excluded.",
            )
        )
    return observations, tuple(constituents)


def _has_takeover_route(
    *,
    document: object,
    carriers: tuple[object, ...],
    source_scope: object,
    response_state: object,
    event_path: str | None,
    require_eventless_first_edge: bool,
) -> list[dict[str, JsonValue]]:
    """Find source-static direct or owner-exit-plus-continuation takeover carriers."""

    from utils.stm_artifacts.fcstm_native_projection import state_path

    root = document.machine.root_state
    matched: list[dict[str, JsonValue]] = []
    for carrier in carriers:
        source = _carrier_source_state(document, carrier)
        if source is None or not _state_is_within(source, source_scope):
            continue
        event_paths = [item.path_name for item in carrier.events]
        event_matches = not event_paths if require_eventless_first_edge else event_path in event_paths
        if not event_matches:
            continue
        if carrier.owner_path == state_path(root) and carrier.target == response_state.name:
            matched.append({"first": _carrier_observation(carrier), "continuation": None})
            continue
        if carrier.target != "[*]" or source.parent is None:
            continue
        exited_owner = source.parent
        for continuation in carriers:
            if (
                continuation.owner_path == state_path(root)
                and continuation.source == exited_owner.name
                and continuation.target == response_state.name
                and not continuation.events
            ):
                matched.append(
                    {
                        "first": _carrier_observation(carrier),
                        "continuation": _carrier_observation(continuation),
                    }
                )
    return matched


def _separated_conditions(
    request: StaticOracleRequest,
    document: object,
) -> tuple[tuple[dict[str, JsonValue], ...], tuple[StaticConstituentResult, ...]]:
    """Check separate event consumers plus a state-condition takeover route."""

    from utils.stm_artifacts.fcstm_native_projection import (
        all_events,
        all_transition_carriers,
        resolve_state,
    )

    values = _values(request)
    carriers = all_transition_carriers(document)
    events = all_events(document)
    state_condition = resolve_state(document, values["state_condition"])
    response_state = resolve_state(document, values["response_state"])
    observations = tuple(
        [
            {"kind": "event", "path": event.path_name, "name": event.name}
            for event in events
        ]
        + [
            {"kind": "carrier", **_carrier_observation(carrier)}
            for carrier in carriers
        ]
    )
    constituents: list[StaticConstituentResult] = []
    scope = state_condition.parent if state_condition is not None else None
    for token in values["required_event_tokens"]:
        declared = [event for event in events if event.name == token]
        constituents.append(
            StaticConstituentResult(
                constituent_id=f"event_declaration:{token}",
                verdict=len(declared) == 1,
                expected=token,
                observed=[event.path_name for event in declared],
                reason="Compared an exact requirement-side token with native Event.name; absence is false and no fuzzy alias is inferred.",
            )
        )
        routes = (
            _has_takeover_route(
                document=document,
                carriers=carriers,
                source_scope=scope,
                response_state=response_state,
                event_path=declared[0].path_name,
                require_eventless_first_edge=False,
            )
            if len(declared) == 1 and scope is not None and response_state is not None
            else []
        )
        constituents.append(
            StaticConstituentResult(
                constituent_id=f"takeover_consumer:{token}",
                verdict=bool(routes),
                expected={"event_token": token, "response_state": values["response_state"]},
                observed=routes,
                reason="Checked direct or owner-exit-plus-eventless-continuation authored carriers within the exact takeover scope; no RTC claim is made.",
            )
        )
    state_ok = state_condition is not None
    constituents.append(
        StaticConstituentResult(
            constituent_id="state_condition_identity",
            verdict=state_ok,
            expected=values["state_condition"],
            observed=".".join(state_condition.path) if state_condition is not None else None,
            reason="Resolved the exact native state path independently of all event identities.",
        )
    )
    state_routes = (
        _has_takeover_route(
            document=document,
            carriers=carriers,
            source_scope=state_condition,
            response_state=response_state,
            event_path=None,
            require_eventless_first_edge=True,
        )
        if state_condition is not None and response_state is not None
        else []
    )
    constituents.append(
        StaticConstituentResult(
            constituent_id="state_condition_takeover_route",
            verdict=bool(state_routes),
            expected={"active_state": values["state_condition"], "response_state": values["response_state"], "additional_event": None},
            observed=state_routes,
            reason="Checked an eventless authored edge from the exact state condition followed, when needed, by an eventless owner continuation to the response state.",
        )
    )
    return observations, tuple(constituents)


def evaluate_request(
    request: StaticOracleRequest,
    *,
    repo_root: Path,
) -> tuple[tuple[dict[str, JsonValue], ...], tuple[StaticConstituentResult, ...]]:
    """Load exact FCSTM bytes and evaluate every native-object constituent."""

    from utils.stm_artifacts.fcstm_native_projection import load_native_document

    artifact = repo_root / request.artifact_path
    if sha256_path(artifact) != request.artifact_sha256:
        raise ValueError("artifact bytes do not match the pre-hashed source-static request")
    document = load_native_document(artifact.read_text(encoding="utf-8"))
    if request.oracle_id == StaticOracleId.RUNNING_EVENT_ROOT_EXIT_CONSUMERS:
        return _running_event_exit(request, document)
    return _separated_conditions(request, document)


def execute_request(
    request: StaticOracleRequest,
    *,
    repo_root: Path,
    receipt_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> StaticOracleReceipt:
    """Execute, hash, and persist one completed source-static query."""

    from pyfcstm.model import model as pyfcstm_model
    from utils.stm_artifacts import fcstm_native_projection

    started_at = _utc_now()
    observations, constituents = evaluate_request(request, repo_root=repo_root)
    verdict = all(item.verdict for item in constituents)
    receipt_root.mkdir(parents=True, exist_ok=True)
    query_path = receipt_root / "query.json"
    write_json(query_path, request.model_dump(mode="json"))
    module_path = Path(__file__).resolve()
    pyfcstm_path = Path(inspect.getsourcefile(pyfcstm_model) or "").resolve()
    projection_path = Path(inspect.getsourcefile(fcstm_native_projection) or "").resolve()
    unsigned = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "request_id": request.request_id,
        "request_sha256": request.request_sha256,
        "ledger_id": request.ledger_id,
        "property_id": request.property_id,
        "exactness_relation": request.exactness_relation,
        "oracle_id": request.oracle_id,
        "artifact_role": request.artifact_role,
        "artifact_path": request.artifact_path,
        "artifact_sha256": request.artifact_sha256,
        "state": "COMPLETED_BOOLEAN",
        "verdict": verdict,
        "acceptance_match": verdict == request.expected_boolean_for_acceptance,
        "observations": observations,
        "constituents": [item.model_dump(mode="json") for item in constituents],
        "query_path": query_path.relative_to(receipt_root).as_posix(),
        "query_sha256": sha256_path(query_path),
        "code_hashes": {
            module_path.relative_to(repo_root.resolve()).as_posix(): sha256_path(module_path),
            pyfcstm_path.relative_to(repo_root.resolve()).as_posix(): sha256_path(pyfcstm_path),
            projection_path.relative_to(repo_root.resolve()).as_posix(): sha256_path(projection_path),
        },
        "source_commit": source_commit,
        "pyfcstm_commit": pyfcstm_commit,
        "command": command,
        "started_at": started_at,
        "completed_at": _utc_now(),
        "replay_status": "NOT_REPLAYED",
        "reason": "The source-static necessary condition completed with a Boolean. False can falsify O under the declared representation assumptions; true does not prove O.",
        "basis": "pyfcstm State/Event/Transition objects and hierarchy links plus provenance-preserving authored carriers; no PlantUML regex, fuzzy matching, or custom runtime was used.",
    }
    receipt = StaticOracleReceipt(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(receipt_root / "receipt.json", receipt.model_dump(mode="json"))
    return receipt


def _semantic_projection(receipt: StaticOracleReceipt) -> dict[str, JsonValue]:
    """Return deterministic receipt facts used by independent replay."""

    return {
        "request_sha256": receipt.request_sha256,
        "oracle_id": receipt.oracle_id.value,
        "artifact_sha256": receipt.artifact_sha256,
        "state": receipt.state,
        "verdict": receipt.verdict,
        "observations": list(receipt.observations),
        "constituents": [item.model_dump(mode="json") for item in receipt.constituents],
    }


def replay_request(
    request: StaticOracleRequest,
    *,
    original_receipt: StaticOracleReceipt,
    original_receipt_path: Path,
    repo_root: Path,
    replay_root: Path,
    source_commit: str,
    pyfcstm_commit: str,
    command: tuple[str, ...],
) -> StaticOracleReplayReceipt:
    """Re-execute and compare deterministic source-static observations."""

    replay = execute_request(
        request,
        repo_root=repo_root,
        receipt_root=replay_root,
        source_commit=source_commit,
        pyfcstm_commit=pyfcstm_commit,
        command=command,
    )
    original_projection_sha256 = canonical_sha256(_semantic_projection(original_receipt))
    replay_projection_sha256 = canonical_sha256(_semantic_projection(replay))
    replay_receipt_path = replay_root / "receipt.json"
    try:
        original_path = original_receipt_path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        original_path = original_receipt_path.resolve().relative_to(replay_root.resolve().parent).as_posix()
    unsigned = {
        "schema_version": REPLAY_SCHEMA_VERSION,
        "request_sha256": request.request_sha256,
        "original_receipt_path": original_path,
        "original_receipt_sha256": sha256_path(original_receipt_path),
        "replay_receipt_path": replay_receipt_path.relative_to(replay_root).as_posix(),
        "replay_receipt_sha256": sha256_path(replay_receipt_path),
        "original_projection_sha256": original_projection_sha256,
        "replay_projection_sha256": replay_projection_sha256,
        "overall_match": original_projection_sha256 == replay_projection_sha256,
        "replayed_at": _utc_now(),
    }
    audit = StaticOracleReplayReceipt(**unsigned, receipt_sha256=canonical_sha256(unsigned))
    write_json(replay_root / "replay_audit.json", audit.model_dump(mode="json"))
    return audit


def _parser() -> argparse.ArgumentParser:
    """Build the provider-free source-static oracle CLI."""

    parser = argparse.ArgumentParser(description="Execute or replay one pre-hashed source-static predicate-gold oracle.")
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--receipt-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pyfcstm-commit", required=True)
    parser.add_argument("--replay-against", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate and execute an original or replay source-static query."""

    args = _parser().parse_args(argv)
    request = StaticOracleRequest.model_validate_json(args.request.read_text(encoding="utf-8"))
    command = (
        "python",
        "-m",
        "paper_stm_evaluation.predicate_gold_static_oracle",
        "--request",
        str(args.request),
        "--repo-root",
        str(args.repo_root),
        "--receipt-root",
        str(args.receipt_root),
        "--source-commit",
        args.source_commit,
        "--pyfcstm-commit",
        args.pyfcstm_commit,
    )
    if args.replay_against is None:
        receipt = execute_request(
            request,
            repo_root=args.repo_root,
            receipt_root=args.receipt_root,
            source_commit=args.source_commit,
            pyfcstm_commit=args.pyfcstm_commit,
            command=command,
        )
        output = {"receipt": str(args.receipt_root / "receipt.json"), "verdict": receipt.verdict, "acceptance_match": receipt.acceptance_match}
    else:
        original = StaticOracleReceipt.model_validate_json(args.replay_against.read_text(encoding="utf-8"))
        audit = replay_request(
            request,
            original_receipt=original,
            original_receipt_path=args.replay_against,
            repo_root=args.repo_root,
            replay_root=args.receipt_root,
            source_commit=args.source_commit,
            pyfcstm_commit=args.pyfcstm_commit,
            command=command + ("--replay-against", str(args.replay_against)),
        )
        output = {"replay_audit": str(args.receipt_root / "replay_audit.json"), "overall_match": audit.overall_match}
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
