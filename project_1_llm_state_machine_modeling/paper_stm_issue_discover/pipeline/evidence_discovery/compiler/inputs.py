"""Typed input protocol for the frozen four-family predicate registry."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, TypeAdapter

from ..semantics.obligations import PredicateId


class PredicateInputsBase(BaseModel):
    """Base predicate-input record produced by the compiler and consumed by the backend.

    Fields come from the frozen registry and the runner's exact binding
    enrichment. This record has no authority over a predicate verdict, W, D,
    L, or Judge relation. Every concrete variant rejects extra fields.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.predicate-inputs.v1"] = Field(
        default="evidence-discovery.predicate-inputs.v1",
        description="Persistence schema version for typed predicate inputs; this metadata is not a backend domain input.",
    )
    predicate_id: str = Field(
        description="Discriminator that must equal the frozen predicate ID represented by this input variant.",
    )
    element_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Closed ModelIR references bound exactly by the runner to constrain execution; an empty tuple means no additional reference constraint.",
    )
    model_hash: str | None = Field(
        default=None,
        description="Content hash of the closed model used for execution; null is allowed only before the record enters a real backend.",
    )

    def to_backend_dict(self) -> dict[str, Any]:
        """Return registry/backend fields without protocol metadata."""

        return self.model_dump(
            mode="json",
            exclude={"schema_version", "predicate_id"},
            exclude_none=True,
        )

    def __getitem__(self, key: str) -> Any:
        return self.to_backend_dict()[key]

    def get(self, key: str, default: Any = None) -> Any:
        """Provide the read-only mapping API expected by deterministic backends."""

        return self.to_backend_dict().get(key, default)

    def __contains__(self, key: object) -> bool:
        return key in self.to_backend_dict()


class S1Inputs(PredicateInputsBase):
    """S1 element membership inputs produced by compiler and consumed by source-static."""

    predicate_id: Literal["S1"] = Field(description="Frozen S1 discriminator.")
    kind: str | None = Field(default=None, description="Required declared element kind; null means binding is incomplete and cannot be W2.")
    element: str | None = Field(default=None, description="Exact required element name/ref; null means binding is incomplete.")
    scope: JsonValue | None = Field(default=None, description="Closed declaration scope supplied by the contract; null means registry-minimal scope is missing.")


class S2Inputs(PredicateInputsBase):
    """S2 exact transition endpoint inputs consumed by source-static."""

    predicate_id: Literal["S2"] = Field(description="Frozen S2 discriminator.")
    source: JsonValue | None = Field(default=None, description="Exact required source node or typed source set; null is incomplete.")
    target: JsonValue | None = Field(default=None, description="Exact required target node or typed target set; null is incomplete.")
    scope: JsonValue | None = Field(default=None, description="Closed transition inventory scope; null means registry-minimal scope is missing.")
    transition: str | None = Field(default=None, description="Optional exact existing carrier transition ref; null is expected for a genuinely missing edge.")


class S3Inputs(PredicateInputsBase):
    """S3 exact trigger-set comparison inputs consumed by source-static."""

    predicate_id: Literal["S3"] = Field(description="Frozen S3 discriminator.")
    transition: str | None = Field(default=None, description="Exact carrier transition ref; null makes deterministic comparison incomplete.")
    triggers: tuple[JsonValue, ...] = Field(default_factory=tuple, description="Required normalized trigger set; empty is a deliberate empty set, not an omitted transition binding.")


class S4Inputs(PredicateInputsBase):
    """S4 state lifecycle-action attachment inputs consumed by source-static."""

    predicate_id: Literal["S4"] = Field(description="Frozen S4 discriminator.")
    state: str | None = Field(default=None, description="Exact state name/ref owning the required action; null is incomplete.")
    phase: str | None = Field(default=None, description="Exact lifecycle phase such as entry/do/exit; null is incomplete.")
    action: JsonValue | None = Field(default=None, description="Required normalized action expression; null is incomplete, not absence evidence.")


class S5Inputs(PredicateInputsBase):
    """S5 transition guard equality inputs consumed by source-static."""

    predicate_id: Literal["S5"] = Field(description="Frozen S5 discriminator.")
    transition: str | None = Field(default=None, description="Exact carrier transition ref; null makes deterministic comparison incomplete.")
    guard: JsonValue | None = Field(default=None, description="Required normalized guard expression; null means the required value was not bound.")


class S6Inputs(PredicateInputsBase):
    """S6 transition effect membership inputs consumed by source-static."""

    predicate_id: Literal["S6"] = Field(description="Frozen S6 discriminator.")
    transition: str | None = Field(default=None, description="Exact carrier transition ref; null makes deterministic comparison incomplete.")
    effect: tuple[JsonValue, ...] = Field(default_factory=tuple, description="Required normalized effect set; empty means no effect value was supplied.")


class G1Inputs(PredicateInputsBase):
    """G1 existential finite-path inputs consumed by the topology backend."""

    predicate_id: Literal["G1"] = Field(description="Frozen G1 discriminator.")
    source: JsonValue | None = Field(default=None, description="Exact source node or nested source set; null is incomplete.")
    target: JsonValue | None = Field(default=None, description="Exact target node or nested target set; null is incomplete.")


class G2Inputs(PredicateInputsBase):
    """G2 universal finite reachability inputs consumed by the topology backend."""

    predicate_id: Literal["G2"] = Field(description="Frozen G2 discriminator.")
    source: JsonValue | None = Field(default=None, description="Exact source node/set under the declared graph completion; null is incomplete.")
    target: JsonValue | None = Field(default=None, description="Exact target node/set required on all paths; null is incomplete.")


class G3Inputs(PredicateInputsBase):
    """G3 route-avoidance inputs consumed by the topology backend."""

    predicate_id: Literal["G3"] = Field(description="Frozen G3 discriminator.")
    source: str | None = Field(default=None, description="Exact route source node; null is incomplete.")
    target: str | None = Field(default=None, description="Exact route target node; null is incomplete.")
    forbidden: tuple[str, ...] = Field(default_factory=tuple, description="Exact forbidden node/edge refs; empty is a deliberate empty set.")


class G4Inputs(PredicateInputsBase):
    """G4 finite coaccessibility inputs consumed by the topology backend."""

    predicate_id: Literal["G4"] = Field(description="Frozen G4 discriminator.")
    roots: JsonValue | None = Field(default=None, description="Exact root node/set; null is incomplete for registry accounting.")
    marked: JsonValue | None = Field(default=None, description="Exact marked target node/set; null is incomplete.")


class R1Inputs(PredicateInputsBase):
    """R1 event-consumption scenario inputs retained for trajectory backend audit."""

    predicate_id: Literal["R1"] = Field(description="Frozen R1 discriminator.")
    scenario: JsonValue | None = Field(default=None, description="Exact supplied scenario/input/schedule object; null is incomplete.")
    event: str | None = Field(default=None, description="Exact event identity to observe; null is incomplete.")
    step: JsonValue | None = Field(default=None, description="Declared macro-step identity/boundary; null is incomplete.")


class R2Inputs(PredicateInputsBase):
    """R2 state-after-stimulus scenario inputs retained for trajectory backend audit."""

    predicate_id: Literal["R2"] = Field(description="Frozen R2 discriminator.")
    scenario: JsonValue | None = Field(default=None, description="Exact supplied scenario/input/schedule object; null is incomplete.")
    stimulus: JsonValue | None = Field(default=None, description="Exact stimulus applied in the scenario; null is incomplete.")
    state: str | None = Field(default=None, description="Exact target state expected after the stimulus; null is incomplete.")
    window: JsonValue | None = Field(default=None, description="Declared observation window; null is incomplete.")


class R3Inputs(PredicateInputsBase):
    """R3 behavior-occurrence scenario inputs retained for trajectory backend audit."""

    predicate_id: Literal["R3"] = Field(description="Frozen R3 discriminator.")
    scenario: JsonValue | None = Field(default=None, description="Exact supplied scenario/input/schedule object; null is incomplete.")
    behavior: JsonValue | None = Field(default=None, description="Required owner/slot behavior identity; null is incomplete.")
    window: JsonValue | None = Field(default=None, description="Declared observation window; null is incomplete.")


class R4Inputs(PredicateInputsBase):
    """R4 state-retention scenario inputs retained for trajectory backend audit."""

    predicate_id: Literal["R4"] = Field(description="Frozen R4 discriminator.")
    scenario: JsonValue | None = Field(default=None, description="Exact supplied scenario/input/schedule object; null is incomplete.")
    state: str | None = Field(default=None, description="Exact state required to remain active; null is incomplete.")
    interval: JsonValue | None = Field(default=None, description="Closed observation interval; null is incomplete.")


class V1Inputs(PredicateInputsBase):
    """V1 bounded guard-disjointness inputs consumed by bounded verification."""

    predicate_id: Literal["V1"] = Field(description="Frozen V1 discriminator.")
    source: str | None = Field(default=None, description="Exact choice-group source state; null is incomplete.")
    trigger: JsonValue | None = Field(default=None, description="Exact shared trigger/event condition; null is incomplete.")
    domain: JsonValue | None = Field(default=None, description="Declared finite guard variable domain; null is incomplete.")
    guards: tuple[str, ...] = Field(default_factory=tuple, description="Exact group guard expressions compiled for execution; empty prevents a sound verdict.")


class V2Inputs(PredicateInputsBase):
    """V2 bounded guard-completeness inputs retained for backend capability audit."""

    predicate_id: Literal["V2"] = Field(description="Frozen V2 discriminator.")
    source: str | None = Field(default=None, description="Exact choice-group source state; null is incomplete.")
    trigger: JsonValue | None = Field(default=None, description="Exact shared trigger/event condition; null is incomplete.")
    domain: JsonValue | None = Field(default=None, description="Declared finite guard variable domain; null is incomplete.")


class V3Inputs(PredicateInputsBase):
    """V3 bounded response inputs retained for backend capability audit."""

    predicate_id: Literal["V3"] = Field(description="Frozen V3 discriminator.")
    p: JsonValue | None = Field(default=None, description="Exact antecedent event/state proposition; null is incomplete.")
    q: JsonValue | None = Field(default=None, description="Exact required response proposition; null is incomplete.")
    bound: JsonValue | None = Field(default=None, description="Declared finite response bound; null is incomplete.")
    unit: str | None = Field(default=None, description="Exact bound unit such as steps or milliseconds; null is incomplete.")
    scope: JsonValue | None = Field(default=None, description="Exact finite verification scope; null is incomplete.")


class V4Inputs(PredicateInputsBase):
    """V4 finite deadlock-freedom scope inputs consumed by bounded verification."""

    predicate_id: Literal["V4"] = Field(description="Frozen V4 discriminator.")
    initial_scope: JsonValue | None = Field(default=None, description="Exact state/scope whose reachable nonterminal configurations are checked; null is incomplete.")


class V5Inputs(PredicateInputsBase):
    """V5 finite state-invariant inputs retained for backend capability audit."""

    predicate_id: Literal["V5"] = Field(description="Frozen V5 discriminator.")
    state: str | None = Field(default=None, description="Exact state whose occupancy is checked; null is incomplete.")
    expected: JsonValue | None = Field(default=None, description="Required finite occupancy value; null is incomplete.")
    initial_scope: JsonValue | None = Field(default=None, description="Exact finite initial scope; null is incomplete.")


class UnsupportedPredicateInputs(PredicateInputsBase):
    """Auditable W1 input that cannot map to a valid frozen predicate variant.

    The compiler produces this variant when predicate is null or the input
    violates the typed schema. raw_values preserves normalized data only for
    audit; the backend never executes it and cannot claim W2 from it.
    """

    predicate_id: Literal["unsupported"] = Field(default="unsupported", description="Unsupported/null input discriminator; it is not a public predicate ID.")
    claimed_predicate_id: PredicateId | None = Field(default=None, description="Frozen predicate ID originally requested by the candidate; null means the candidate explicitly has no applicable predicate.")
    raw_values: dict[str, JsonValue] = Field(default_factory=dict, description="Normalized inputs that failed every concrete variant; retained for failure/W1 audit and never sent to a backend.")
    validation_errors: tuple[str, ...] = Field(default_factory=tuple, description="Specific, localizable typed validation errors; an empty tuple means the predicate was null rather than malformed.")

    def to_backend_dict(self) -> dict[str, Any]:
        """Return preserved values for audit-only callers; this variant is never executed."""

        return dict(self.raw_values)


PredicateInputs = Annotated[
    S1Inputs
    | S2Inputs
    | S3Inputs
    | S4Inputs
    | S5Inputs
    | S6Inputs
    | G1Inputs
    | G2Inputs
    | G3Inputs
    | G4Inputs
    | R1Inputs
    | R2Inputs
    | R3Inputs
    | R4Inputs
    | V1Inputs
    | V2Inputs
    | V3Inputs
    | V4Inputs
    | V5Inputs
    | UnsupportedPredicateInputs,
    Field(discriminator="predicate_id"),
]

_PREDICATE_INPUT_ADAPTER = TypeAdapter(PredicateInputs)


def validate_predicate_inputs(
    predicate_id: PredicateId | None,
    values: dict[str, JsonValue],
) -> PredicateInputsBase:
    """Validate normalized inputs against the exact frozen predicate variant.

    Invalid model output becomes an explicit unsupported input object so a local
    schema defect cannot crash or erase the method cell.
    """

    if predicate_id is None:
        return UnsupportedPredicateInputs(
            claimed_predicate_id=None,
            raw_values=values,
        )
    try:
        return _PREDICATE_INPUT_ADAPTER.validate_python(
            {"predicate_id": predicate_id, **values}
        )
    except Exception as exc:
        return UnsupportedPredicateInputs(
            claimed_predicate_id=predicate_id,
            raw_values=values,
            validation_errors=(str(exc),),
        )


__all__ = [
    "PredicateInputs",
    "PredicateInputsBase",
    "UnsupportedPredicateInputs",
    "validate_predicate_inputs",
]
