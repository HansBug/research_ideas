"""Machine-auditable proof that evidence discovery has one FCSTM semantic source.

The audit reads FCSTM text only through :mod:`pyfcstm`.  It checks that the
compatibility ``ModelIR`` projection preserves the native inventory and records
the intentionally retained text handling that is limited to audit references,
provider framing, or method-owned typed hints rather than FCSTM DSL semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
from typing import Literal
import tokenize

from pydantic import BaseModel, ConfigDict, Field

from .fcstm_native_projection import (
    all_events,
    all_states,
    all_transition_carriers,
    all_transitions,
    load_native_document,
    state_path,
    transition_carrier_reference,
)
from .loaders import FROZEN_PAIR_IDS, load_pair
from .models import ModelIR, parse_fcstm


class NativeTextHandlingAllowance(BaseModel):
    """One explicitly allowed non-semantic text-processing location."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    path: str = Field(min_length=1, description="Repository-relative production Python path containing the allowed text operation.")
    text_construct: Literal["regular_expression", "splitlines"] = Field(description="Text-processing construct retained at the location.")
    purpose: str = Field(min_length=1, description="Non-FCSTM-semantic purpose of the retained construct.")


class NativeTextHandlingHit(BaseModel):
    """One static-scan observation of a retained text-processing construct."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    path: str = Field(min_length=1, description="Repository-relative production Python path containing the observed construct.")
    line: int = Field(ge=1, description="One-based source line of the observed construct.")
    text_construct: Literal["regular_expression", "splitlines"] = Field(description="Observed text-processing construct category.")
    allowance_purpose: str | None = Field(default=None, description="Approved non-semantic purpose, or null when the observation is an unapproved regression.")
    source_line: str = Field(min_length=1, description="Exact source-code line retained for static audit review.")


class NativeProjectionPairAudit(BaseModel):
    """Native load and projection-parity result for one FCSTM artifact."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Four-digit source pair identifier.")
    source_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 hash of the exact FCSTM source text loaded by pyfcstm.")
    native_load_succeeded: bool = Field(description="Whether pyfcstm loaded the exact FCSTM source without a method-owned parser.")
    input_closure_loaded: bool = Field(description="Whether the frozen method input closure also loaded for this protocol pair.")
    projection_parity: bool = Field(description="Whether all native inventory identities required by the compatibility projection agree exactly.")
    state_count: int = Field(ge=0, description="Count of native states, including pseudo-states.")
    pseudo_state_count: int = Field(ge=0, description="Count of native pseudo-states preserved by the projection.")
    event_count: int = Field(ge=0, description="Count of distinct native declared events preserved by the projection.")
    authored_transition_count: int = Field(ge=0, description="Count of native authored transition carriers after forced/combo provenance grouping.")
    native_implementation_transition_count: int = Field(ge=0, description="Count of native implementation transitions before authored-carrier grouping.")
    effect_only_transition_count: int = Field(ge=0, description="Count of authored native carriers with no event and at least one native effect operation.")
    lifecycle_action_count: int = Field(ge=0, description="Count of native entry/do/exit lifecycle actions, including native during aspects.")
    forced_carrier_refs: tuple[str, ...] = Field(default_factory=tuple, description="Canonical refs for native forced-transition authored carriers.")
    combo_origin_ids: tuple[str, ...] = Field(default_factory=tuple, description="Native combo-origin identities represented by authored carriers.")
    legacy_ref_count: int = Field(ge=0, description="Number of historical references that map uniquely to one current native projection ref.")
    ambiguous_legacy_refs: tuple[str, ...] = Field(default_factory=tuple, description="Historical refs intentionally rejected because they do not map uniquely to one native carrier.")
    differences: tuple[str, ...] = Field(default_factory=tuple, description="Complete deterministic parity differences; an empty tuple is required for parity.")
    native_load_error: str | None = Field(default=None, description="Native load or projection exception, or null on successful load.")
    reason: str = Field(min_length=1, description="Human-readable native load/projection conclusion.")
    basis: str = Field(min_length=1, description="Native API and compatibility-projection facts used for this row.")


class NativeProjectionAudit(BaseModel):
    """Immutable aggregate audit for the pyfcstm-only FCSTM semantic boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["evidence-discovery.fcstm-native-projection-audit.v1"] = Field(default="evidence-discovery.fcstm-native-projection-audit.v1", description="Persistence schema version for the native projection audit.")
    algorithm_version: Literal["pyfcstm-native-projection-audit.v1"] = Field(default="pyfcstm-native-projection-audit.v1", description="Versioned parity and static-contract algorithm identifier.")
    report_root: str = Field(min_length=1, description="Resolved representation report root containing pair artifacts.")
    source_pair_count: int = Field(ge=0, description="Number of FCSTM source artifacts inspected, normally all 60 source pairs.")
    frozen_input_closure_pair_count: int = Field(ge=0, description="Number of frozen 54-pair full method input closures successfully loaded.")
    all_native_loads_succeeded: bool = Field(description="Whether every discovered FCSTM source loaded directly through pyfcstm.")
    all_projection_parity_succeeded: bool = Field(description="Whether every native-loaded source has zero projection inventory differences.")
    all_frozen_input_closures_succeeded: bool = Field(description="Whether every official frozen pair loaded its full method input closure.")
    pair_audits: tuple[NativeProjectionPairAudit, ...] = Field(description="One native/projection row per discovered source pair in stable order.")
    allowed_text_handling: tuple[NativeTextHandlingAllowance, ...] = Field(description="Complete allowlist of text processing that is not FCSTM DSL interpretation.")
    observed_text_handling: tuple[NativeTextHandlingHit, ...] = Field(description="All production regular-expression and splitlines observations under evidence discovery.")
    unapproved_text_handling: tuple[NativeTextHandlingHit, ...] = Field(default_factory=tuple, description="Observed text processing without an explicit non-semantic allowance; this must remain empty.")
    reason: str = Field(min_length=1, description="Aggregate conclusion on the single pyfcstm semantic-source rule.")
    basis: str = Field(min_length=1, description="Exact loader, model, provenance, and static-contract boundary used by the audit.")


_TEXT_HANDLING_ALLOWANCES: tuple[NativeTextHandlingAllowance, ...] = (
    NativeTextHandlingAllowance(path="backends/fcstm_native.py", text_construct="splitlines", purpose="Linux /proc worker RSS telemetry only."),
    NativeTextHandlingAllowance(path="backends/source_static.py", text_construct="regular_expression", purpose="Presentation whitespace normalization of typed action values; native AST parsers decide FCSTM semantics."),
    NativeTextHandlingAllowance(path="inputs/context.py", text_construct="regular_expression", purpose="Numbered NL segment and audit-reference formatting, never FCSTM DSL parsing."),
    NativeTextHandlingAllowance(path="inputs/fcstm_native_projection.py", text_construct="splitlines", purpose="Working-contract excerpt attribution to a pyfcstm source span; native carrier refs, never source lines, decide FCSTM semantics."),
    NativeTextHandlingAllowance(path="inputs/native_projection_audit.py", text_construct="regular_expression", purpose="Static-contract scanner self-identification only."),
    NativeTextHandlingAllowance(path="inputs/native_projection_audit.py", text_construct="splitlines", purpose="Static-contract scanner reads Python source lines only."),
    NativeTextHandlingAllowance(path="orchestration/runner.py", text_construct="regular_expression", purpose="Run-id validation and cross-artifact display-token normalization; native refs decide all FCSTM identities."),
    NativeTextHandlingAllowance(path="orchestration/runtime.py", text_construct="splitlines", purpose="Provider transport framing only."),
    NativeTextHandlingAllowance(path="route_replay.py", text_construct="regular_expression", purpose="Immutable historical run-id validation only."),
    NativeTextHandlingAllowance(path="semantics/binding.py", text_construct="regular_expression", purpose="Method candidate and historical-ref format parsing, never FCSTM source parsing."),
    NativeTextHandlingAllowance(path="semantics/predicate_routing.py", text_construct="regular_expression", purpose="Method-owned cold_macrosteps typed hint validation only."),
    NativeTextHandlingAllowance(path="semantics/source_transition_closure.py", text_construct="regular_expression", purpose="Cross-artifact display-token normalization, never FCSTM source parsing."),
    NativeTextHandlingAllowance(path="semantics/source_transition_closure.py", text_construct="splitlines", purpose="PlantUML and declared source-line attribution only; native span/carrier refs decide FCSTM identity."),
)


def allowed_text_handling() -> tuple[NativeTextHandlingAllowance, ...]:
    """Return the complete immutable non-semantic text-processing allowlist."""

    return _TEXT_HANDLING_ALLOWANCES


def _source_hash(source_text: str) -> str:
    """Hash one source text without parsing or normalizing it."""

    return "sha256:" + hashlib.sha256(source_text.encode("utf-8")).hexdigest()


def _model_action_count(model: ModelIR) -> int:
    """Count lifecycle actions already projected from native lifecycle slots."""

    return sum(sum(len(values) for values in state.actions.values()) for state in model.states)


def _native_action_count(document: object) -> int:
    """Count entry/do/exit actions directly from pyfcstm State objects."""

    return sum(
        len(state.on_enters)
        + len(state.on_durings)
        + len(state.on_during_aspects)
        + len(state.on_exits)
        for state in all_states(document)
    )


def _legacy_ref_candidates(model: ModelIR) -> dict[str, tuple[str, ...]]:
    """Collect historical references before the projection intentionally rejects ambiguity."""

    values: dict[str, list[str]] = {}
    for item in (*model.states, *model.events, *model.transitions):
        for reference in item.legacy_refs:
            values.setdefault(reference, []).append(item.ref)
    return {
        reference: tuple(sorted(set(refs)))
        for reference, refs in values.items()
    }


def _projection_differences(document: object, model: ModelIR) -> tuple[str, ...]:
    """Compare every method-facing projection identity with native objects."""

    differences: list[str] = []
    native_states = tuple(all_states(document))
    projected_states = {state.canonical_path: state for state in model.states}
    native_state_paths = {state_path(state) for state in native_states}
    if native_state_paths != set(projected_states):
        differences.append("native/projected state canonical-path sets differ")
    for state in native_states:
        path = state_path(state)
        projected = projected_states.get(path)
        if projected is None:
            continue
        if projected.is_pseudo != bool(state.is_pseudo):
            differences.append(f"state pseudo classification differs: {path}")
        parent_path = state_path(state.parent) if state.parent is not None else None
        projected_parent_path = None
        if projected.parent_ref:
            parent = next((item for item in model.states if item.ref == projected.parent_ref), None)
            projected_parent_path = parent.canonical_path if parent is not None else None
        if parent_path != projected_parent_path:
            differences.append(f"state parent canonical path differs: {path}")
    native_event_paths = {event.path_name for event in all_events(document)}
    projected_event_paths = {event.canonical_path for event in model.events}
    if native_event_paths != projected_event_paths:
        differences.append("native/projected event canonical-path sets differ")
    carriers = tuple(all_transition_carriers(document))
    expected_refs = {
        transition_carrier_reference(carrier, ordinal): carrier
        for ordinal, carrier in enumerate(carriers, start=1)
    }
    projected_carriers = {transition.ref: transition for transition in model.transitions}
    if set(expected_refs) != set(projected_carriers):
        differences.append("native/projected authored-carrier ref sets differ")
    event_refs = {event.canonical_path: event.ref for event in model.events}
    for reference, carrier in expected_refs.items():
        projected = projected_carriers.get(reference)
        if projected is None:
            continue
        if (projected.source, projected.target, projected.owner_path) != (
            carrier.source,
            carrier.target,
            carrier.owner_path,
        ):
            differences.append(f"carrier endpoints or owner differs: {reference}")
        native_trigger_refs = tuple(
            event_refs[event.path_name]
            for event in carrier.events
            if event.path_name in event_refs
        )
        if projected.trigger_refs != native_trigger_refs:
            differences.append(f"carrier trigger identity differs: {reference}")
        if projected.native_transition_count != len(carrier.native_transitions):
            differences.append(f"carrier implementation-edge count differs: {reference}")
        if projected.is_forced != (carrier.forced_origin is not None):
            differences.append(f"carrier forced provenance differs: {reference}")
        if projected.combo_origin_id != carrier.combo_origin_id:
            differences.append(f"carrier combo provenance differs: {reference}")
    if _model_action_count(model) != _native_action_count(document):
        differences.append("native/projected lifecycle-action count differs")
    return tuple(sorted(set(differences)))


def audit_pair_source(pair_id: str, source_path: Path, *, input_closure_loaded: bool) -> NativeProjectionPairAudit:
    """Audit one source directly through pyfcstm and its compatibility projection."""

    source_text = source_path.read_text(encoding="utf-8")
    source_hash = _source_hash(source_text)
    try:
        document = load_native_document(source_text)
        model = parse_fcstm(source_text)
    except Exception as exc:  # noqa: BLE001 - the row itself records native load/projection failure.
        return NativeProjectionPairAudit(
            pair_id=pair_id,
            source_hash=source_hash,
            native_load_succeeded=False,
            input_closure_loaded=input_closure_loaded,
            projection_parity=False,
            state_count=0,
            pseudo_state_count=0,
            event_count=0,
            authored_transition_count=0,
            native_implementation_transition_count=0,
            effect_only_transition_count=0,
            lifecycle_action_count=0,
            native_load_error=f"{type(exc).__name__}: {exc}",
            reason="pyfcstm could not load or project the exact FCSTM artifact, so no method semantic fact is accepted.",
            basis="pyfcstm.model.load_state_machine_from_text and native compatibility projection",
        )
    carriers = tuple(all_transition_carriers(document))
    differences = _projection_differences(document, model)
    legacy_candidates = _legacy_ref_candidates(model)
    ambiguous = tuple(
        sorted(
            reference
            for reference, refs in legacy_candidates.items()
            if len(refs) != 1
        )
    )
    forced = tuple(
        transition_carrier_reference(carrier, ordinal)
        for ordinal, carrier in enumerate(carriers, start=1)
        if carrier.forced_origin is not None
    )
    combo_ids = tuple(
        sorted(
            {
                carrier.combo_origin_id
                for carrier in carriers
                if carrier.combo_origin_id is not None
            }
        )
    )
    return NativeProjectionPairAudit(
        pair_id=pair_id,
        source_hash=source_hash,
        native_load_succeeded=True,
        input_closure_loaded=input_closure_loaded,
        projection_parity=not differences,
        state_count=len(model.states),
        pseudo_state_count=sum(state.is_pseudo for state in model.states),
        event_count=len(model.events),
        authored_transition_count=len(carriers),
        native_implementation_transition_count=len(all_transitions(document)),
        effect_only_transition_count=sum(not carrier.events and bool(carrier.effects) for carrier in carriers),
        lifecycle_action_count=_model_action_count(model),
        forced_carrier_refs=forced,
        combo_origin_ids=combo_ids,
        legacy_ref_count=len(model.legacy_ref_map),
        ambiguous_legacy_refs=ambiguous,
        differences=differences,
        reason=(
            "Every projected identity agrees with the pyfcstm native inventory."
            if not differences
            else "One or more compatibility projection identities differ from the pyfcstm native inventory."
        ),
        basis="pyfcstm StateMachine, State, Event, Transition, authored forced/combo provenance, and compatibility ModelIR projection",
    )


def _text_handling_hits(evidence_root: Path) -> tuple[NativeTextHandlingHit, ...]:
    """Scan production files for text processing that could regress into a DSL parser."""

    purposes = {
        (item.path, item.text_construct): item.purpose
        for item in _TEXT_HANDLING_ALLOWANCES
    }
    hits: list[NativeTextHandlingHit] = []
    for path in sorted(evidence_root.rglob("*.py")):
        relative = path.relative_to(evidence_root).as_posix()
        if relative.startswith("tests/"):
            continue
        source_text = path.read_text(encoding="utf-8")
        source_lines = source_text.splitlines()
        tokens = tuple(tokenize.generate_tokens(io.StringIO(source_text).readline))
        for index, token in enumerate(tokens):
            construct: Literal["regular_expression", "splitlines"] | None = None
            if (
                token.type == tokenize.NAME
                and token.string == "re"
                and index + 1 < len(tokens)
                and tokens[index + 1].type == tokenize.OP
                and tokens[index + 1].string == "."
            ):
                construct = "regular_expression"
            elif (
                token.type == tokenize.NAME
                and token.string == "splitlines"
                and index > 0
                and tokens[index - 1].type == tokenize.OP
                and tokens[index - 1].string == "."
            ):
                construct = "splitlines"
            if construct is None or token.start[0] > len(source_lines):
                continue
            hits.append(
                NativeTextHandlingHit(
                    path=relative,
                    line=token.start[0],
                    text_construct=construct,
                    allowance_purpose=purposes.get((relative, construct)),
                    source_line=source_lines[token.start[0] - 1].strip(),
                )
            )
    return tuple(hits)


def build_native_projection_audit(report_root: str | Path) -> NativeProjectionAudit:
    """Build the all-source and frozen-input-closure pyfcstm projection audit."""

    root = Path(report_root).expanduser().resolve()
    pairs_root = root / "pairs"
    source_paths = sorted(pairs_root.glob("[0-9][0-9][0-9][0-9]/fcstm.fcstm"))
    closure_success: dict[str, bool] = {}
    for pair_id in FROZEN_PAIR_IDS:
        try:
            load_pair(pairs_root / pair_id)
        except Exception:  # noqa: BLE001 - report the failed closure in its source row.
            closure_success[pair_id] = False
        else:
            closure_success[pair_id] = True
    pair_audits = tuple(
        audit_pair_source(
            source_path.parent.name,
            source_path,
            input_closure_loaded=closure_success.get(source_path.parent.name, False),
        )
        for source_path in source_paths
    )
    hits = _text_handling_hits(Path(__file__).resolve().parents[1])
    unapproved = tuple(hit for hit in hits if hit.allowance_purpose is None)
    return NativeProjectionAudit(
        report_root=str(root),
        source_pair_count=len(pair_audits),
        frozen_input_closure_pair_count=sum(closure_success.values()),
        all_native_loads_succeeded=all(item.native_load_succeeded for item in pair_audits),
        all_projection_parity_succeeded=all(item.projection_parity for item in pair_audits),
        all_frozen_input_closures_succeeded=(
            len(closure_success) == len(FROZEN_PAIR_IDS)
            and all(closure_success.values())
        ),
        pair_audits=pair_audits,
        allowed_text_handling=_TEXT_HANDLING_ALLOWANCES,
        observed_text_handling=hits,
        unapproved_text_handling=unapproved,
        reason=(
            "Every FCSTM source and frozen method input closure uses pyfcstm as its only semantic source."
            if all(item.native_load_succeeded and item.projection_parity for item in pair_audits)
            and all(closure_success.values())
            and not unapproved
            else "The native-projection gate found a source load, parity, input-closure, or static text-handling failure."
        ),
        basis="pyfcstm native loader/model/provenance plus an explicit production text-handling allowlist",
    )


def write_native_projection_audit(report_root: str | Path, output_path: str | Path) -> NativeProjectionAudit:
    """Build and atomically persist one immutable native projection audit artifact."""

    audit = build_native_projection_audit(report_root)
    destination = Path(output_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(audit.model_dump_json(indent=2), encoding="utf-8")
    temporary.replace(destination)
    return audit


def main() -> int:
    """Run the native projection audit as a small command-line artifact producer."""

    parser = argparse.ArgumentParser(description="Audit pyfcstm-only FCSTM native projection parity.")
    parser.add_argument("--report-root", required=True, help="Representation report root containing pairs/.")
    parser.add_argument("--output", required=True, help="Destination JSON audit artifact path.")
    args = parser.parse_args()
    audit = write_native_projection_audit(args.report_root, args.output)
    return 0 if (
        audit.all_native_loads_succeeded
        and audit.all_projection_parity_succeeded
        and audit.all_frozen_input_closures_succeeded
        and not audit.unapproved_text_handling
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
