"""A2 provider contracts and semantic evidence without predicate execution."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, ClassVar

from pydantic import BaseModel, create_model

from ..inputs.context import (
    CanonicalSourceIR, ContextManifest, ExactSourceInventory, InspectionEquivalentFacts,
    NumberedNLSegment, StructuredArtifact,
)
from ..inputs.models import PairInput
from .adjudication import DAdjudicationResponse, SemanticAdjudication, adjudicate_disposition
from .binding import BindingResult
from .obligations import CandidateIssue, ContractBindingHint, ObligationProperty
from .workflow import (
    ContractCompletionResponse, GroundingResponse, NLContract, NLContractResponse,
    PREDICATE_ROUTING_GUIDANCE,
)


NO_PREDICATES_VERSION = "no-predicates-semantic.v1"
DISABLED_PREDICATE_STEPS = (
    "predicate_vocabulary_guidance",
    "route_primary_candidates",
    "predicate_parameter_binding",
    "_materialize_deterministic_execution_probes",
    "_materialize_group_post_states",
    "compile_plan",
    "validate_plan",
    "run_backend",
    "build_predicate_execution_receipt",
    "predicate_true_filter",
)


class NoPredicatesInput(PairInput):
    """Retain the full input closure while selecting A2 method behavior."""

    ablation_mode: ClassVar[str] = "no-predicates"


NoPredicatesInput.model_rebuild()


def without_predicates(pair: PairInput) -> NoPredicatesInput:
    return NoPredicatesInput(**{name: getattr(pair, name) for name in PairInput.model_fields})


def project_context(payload: dict[str, Any]) -> dict[str, Any]:
    """Change fixed role instructions while preserving every supplied fact."""

    payload["source_roles"]["fcstm_model"] = "closed_model_semantic_binding"
    for section in payload["context_manifest"]["sections"]:
        if section["section_id"] == "model-grounding":
            section["purpose"] = "Bind exact closed-model elements and assess the supplied semantic obligations."
            section["basis"] = "closed-model semantic binding contract"
    if payload.get("fcstm_model"):
        payload["fcstm_model"]["reason"] = "FCSTM is the closed model under evaluation."
    if payload.get("verify_facts"):
        payload["verify_facts"]["reason"] = "The method receives finite verification facts as structured context; they are not copied into W/D levels."
    return payload


def _field(model: type[BaseModel], name: str, *, description: str | None = None) -> Any:
    field = deepcopy(model.model_fields[name])
    if description is not None:
        field.description = description
    return field


_hint_role = ContractBindingHint.model_fields["role"]
_hint_description = _hint_role.description.replace(
    " or a backend fixture", " or a fixture"
).replace(
    " This is not a frozen predicate input name unless grounding later binds it exactly.", ""
)


class SemanticBindingHint(ContractBindingHint):
    __doc__ = ContractBindingHint.__doc__

    role: _hint_role.annotation = _field(ContractBindingHint, "role", description=_hint_description)


class SemanticContract(NLContract):
    __doc__ = NLContract.__doc__

    property: ObligationProperty = _field(
        NLContract,
        "property",
        description=NLContract.model_fields["property"].description.replace(
            "; this vocabulary includes the frozen predicate meanings and explicit unsupported semantic boundaries", ""
        ),
    )
    binding_hints: tuple[SemanticBindingHint, ...] = _field(NLContract, "binding_hints")


# CandidateIssue has no validators; copy its structural fields without exposing
# execution arguments to the provider. Full contracts retain their own schema.
SemanticCandidate = create_model(
    "SemanticCandidate",
    __doc__=CandidateIssue.__doc__,
    __config__=CandidateIssue.model_config,
    **{
        name: (
            field.annotation,
            _field(
                CandidateIssue,
                name,
                description=(field.description or "").replace(
                    " even when no frozen predicate fully expresses it", ""
                ),
            ),
        )
        for name, field in CandidateIssue.model_fields.items()
        if name not in {"predicate_id", "predicate_inputs"}
    },
)


class SemanticContractResponse(NLContractResponse):
    __doc__ = NLContractResponse.__doc__

    contracts: list[SemanticContract] = _field(NLContractResponse, "contracts")


class SemanticContractCompletionResponse(ContractCompletionResponse):
    __doc__ = ContractCompletionResponse.__doc__

    additional_contracts: list[SemanticContract] = _field(ContractCompletionResponse, "additional_contracts")


class SemanticGroundingResponse(GroundingResponse):
    __doc__ = GroundingResponse.__doc__

    additional_contracts: list[SemanticContract] = _field(GroundingResponse, "additional_contracts")
    candidates: list[SemanticCandidate] = _field(GroundingResponse, "candidates")


class SemanticDecision(SemanticAdjudication):
    __doc__ = SemanticAdjudication.__doc__

    grounding: SemanticAdjudication.model_fields["grounding"].annotation = _field(
        SemanticAdjudication,
        "grounding",
        description=SemanticAdjudication.model_fields["grounding"].description.replace(
            "; predicate/backend unavailability is a W boundary and does not itself establish semantic ambiguity", ""
        ).replace(" without a separate predicate receipt", ""),
    )
    defeater_kind: SemanticAdjudication.model_fields["defeater_kind"].annotation = _field(
        SemanticAdjudication,
        "defeater_kind",
        description=SemanticAdjudication.model_fields["defeater_kind"].description.replace(
            ", never merely because a predicate/backend is unsupported", ""
        ),
    )


class SemanticDecisionResponse(DAdjudicationResponse):
    __doc__ = DAdjudicationResponse.__doc__

    decisions: list[SemanticDecision] = _field(DAdjudicationResponse, "decisions")


@lru_cache(maxsize=None)
def response_schema(model: type[BaseModel]) -> type[BaseModel]:
    schemas = {
        NLContractResponse: SemanticContractResponse,
        ContractCompletionResponse: SemanticContractCompletionResponse,
        GroundingResponse: SemanticGroundingResponse,
        DAdjudicationResponse: SemanticDecisionResponse,
    }
    if model in schemas:
        return schemas[model]
    if issubclass(model, GroundingResponse):
        return create_model(
            f"Semantic{model.__name__}",
            __doc__=model.__doc__,
            __base__=model,
            additional_contracts=(list[SemanticContract], _field(model, "additional_contracts")),
            candidates=(list[SemanticCandidate], _field(model, "candidates")),
        )
    raise ValueError(f"No A2 response contract for {model.__name__}")


def compact_semantic_dossier(dossier: dict[str, Any]) -> dict[str, Any]:
    candidate = dossier["candidate"]
    return {
        "obligation_id": dossier["obligation_id"],
        "defeater_evidence_reference_catalog": dossier.get("defeater_evidence_reference_catalog", []),
        "candidate": {name: candidate[name] for name in SemanticCandidate.model_fields if name in candidate},
        "binding": dossier["binding"],
        "reason": "D receives the exact candidate, ordinary binding, and supplied source/model facts.",
        "basis": NO_PREDICATES_VERSION,
    }


# Apply these exact edits only to fixed method instructions before adding any
# source or provider text. This preserves the non-ablated wording and examples.
INSTRUCTION_EDITS = (
    ("\n\n" + PREDICATE_ROUTING_GUIDANCE, ""),
    ("FCSTM is the closed model evaluated by the deterministic backend", "FCSTM is the closed model under evaluation"),
    (" Predicate IDs are closed to the selected 12 IDs. A precise claim that is not expressible by a frozen predicate must remain a candidate with predicate_id=null, not disappear.", ""),
    ("Do not invent any scenario, queue, schedule, macrostep, interval, guard valuation, finite domain, or verdict: a downstream native binder may only construct those execution inputs after exact current-pair closure, and an unclosed input remains a precise W1 boundary.", "Do not invent any scenario, queue, schedule, macrostep, interval, guard valuation, finite domain, or verdict."),
    ("neither value is a property or frozen predicate ID", "neither value is a property"),
    ("the backend does not synthesize missing containment rows from it", "missing containment rows are not synthesized from it"),
    ("""contract property first, then select the minimal frozen predicate that decides
that same property. Do not substitute a nearby endpoint, declaration, or local
path property merely because it is executable.""", """contract property first. Do not substitute a nearby endpoint, declaration, or local
path property."""),
    ("""semantic gap that must remain W1. When the supplied source/model facts satisfy a
contract, omit it from both `candidates` and `unresolved`. Predicate/backend
unavailability does not turn a satisfied fact into
an issue and is not by itself semantic ambiguity.""", """semantic gap. When the supplied source/model facts satisfy a
contract, omit it from both `candidates` and `unresolved`."""),
    ("""that absence is the candidate evidence, not an unresolved binding. Emit one S2
candidate with the required source/target inputs and bind the exact endpoint
state refs; a nonexistent transition cannot supply its own ref.""", """that absence is the candidate evidence, not an unresolved binding. Emit one
candidate and bind the exact endpoint state refs; a nonexistent transition
cannot supply its own ref."""),
    ("""is empty while an atomic contract requires that field, emit the corresponding
S4/S5 candidate for a lifecycle action/guard, or a predicate-null W1 candidate
for an effect. Preserve W1 whenever the precise claim has no applicable
predicate input. Use `unresolved`""", """is empty while an atomic contract requires that field, emit the corresponding
candidate for a lifecycle action, guard, or effect. Use `unresolved`"""),
    ("""no A-to-B edge, emit S2 with `source=A`, `target=B`, and both endpoint state refs
in `element_refs`; do not ask a missing edge for a transition ref.""", """no A-to-B edge, emit a candidate with both endpoint state refs
in `element_refs`; do not ask a missing edge for a transition ref."""),
    ("""carrier ref and emit the issue; use predicate_id=null for W1 when the frozen
predicate cannot represent the semantic value. Missing required content is the""", """carrier ref and emit the issue. Missing required content is the"""),
    ("""copied from its contract. `predicate_inputs` must always be a JSON object; use
an empty object when predicate_id is null, never a list or free-text value.""", "copied from its contract."),
    (" Predicate support affects W only.", ""),
    ("""  `guard_disjointness` candidate with predicate=null/W1. Individual S3/S5
  successes cannot rebut it.""", """  `guard_disjointness` candidate. Individual trigger/guard
  satisfaction cannot rebut it."""),
    ("""Inspection-equivalent routing: a deterministic `LEAF_WITHOUT_OUTGOING` or finite
deadlock-frontier fact is a reason to consider one V1(initial_scope) candidate,
for the exact `deadlock_freedom` operating-state contract and exact state locus,
with the exact leaf refs kept in element_refs/supporting facts; it is not an S1
existence claim. A failed finite reachability fact routes to G1 with its exact
source/target sets. A refuted initial-entry fact routes to an exact S2 initial
edge claim. A refuted event-consumer coverage fact may support a precise
predicate-null W1 candidate for the exact event/consumer scope; do not replace""", """Inspection-equivalent facts: a deterministic `LEAF_WITHOUT_OUTGOING` or finite
deadlock-frontier fact is a reason to consider one candidate
for the exact `deadlock_freedom` operating-state contract and exact state locus,
with the exact leaf refs kept in element_refs/supporting facts.
A failed finite reachability fact supports the exact reachability obligation.
A refuted initial-entry fact supports the exact initial-entry obligation.
A refuted event-consumer coverage fact may support a precise
candidate for the exact event/consumer scope; do not replace"""),
    ("""precisely bound predicate=null candidate for W1, but must not be disguised as
S1/S2/S3.""", "precisely bound candidate for their exact semantic property."),
    ("""The absence of a dedicated frozen predicate changes W to W1; it does not make
the already bound finite comparison unresolved.""", "The already bound finite comparison is not unresolved."),
    ("Preserve the precise relation as predicate-null W1.", "Preserve the precise relation."),
    (", and predicate support affects only W", ""),
    ("stage or the backend to synthesize omitted sibling-containment obligations", "stage to synthesize omitted sibling-containment obligations"),
    ("""target, emit the scoped candidate (predicate=null when the registry cannot state
the full owner semantics); do not substitute the nearby local edge.""", """target, emit the scoped candidate; do not substitute the nearby local edge."""),
    ("""satisfied conjunct. A missing registered predicate
is a precise W1 candidate when the model locus is exact.""", "satisfied conjunct."),
    ("beyond its registered soundness fragment", "beyond its supplied evidence scope"),
    ("exact bindings, predicate plan, and backend receipt", "exact bindings, and supplied model facts"),
    ("D boundary: a predicate-null route, incomplete typed input, or unavailable execution does not erase a precise issue. ", "D boundary: "),
    ("; deterministic code will keep it at W1", ""),
    (" A completed predicate result that is true for the requirement is not a violation merely because the candidate text sounds concerning.", ""),
    ("Predicate/backend availability is a W question, never a D defeater by itself. If", "If"),
    ("""predicate-null candidate may still be D2 when the supplied semantic facts clearly
violate the obligation; deterministic publication will keep it at W1. Do not use
backend=unsupported or verdict=unknown as evidence either for or against the
semantic violation.""", """candidate may still be D2 when the supplied semantic facts clearly
violate the obligation."""),
    ("""  source/model inventory can establish absence or cardinality. A missing dedicated
  predicate or precomputed cardinality receipt is only a W boundary. If two
  competent scope/member readings remain compatible, use established plus an
  undercutting-survives defeater (D1), not grounding=unresolved merely because the
  frozen registry lacks that predicate.""", """  source/model inventory can establish absence or cardinality. If two
  competent scope/member readings remain compatible, use established plus an
  undercutting-survives defeater (D1)."""),
    ("V1 frontier protocol: when predicate_id=V1, inspect the exact bound state refs,", "Progress/deadlock frontier protocol: for that exact property, inspect the bound state refs,"),
    ("""decided from the supplied dossier. Never turn an unsupported V1 plan into W2,
and never discard a precise W1 frontier issue.""", """decided from the supplied dossier. Never discard a precise frontier issue."""),
    ("A coarse satisfied predicate check cannot erase an", "Satisfaction of a weaker property cannot erase an"),
    ("Frozen predicate input spellings: S1={kind, element, scope} S2={source, target, scope} S3={transition, triggers} S4={state, phase, action} S5={transition, guard} G1={source, target} G2={source, target} G3={roots, marked} R1={scenario, event, step} R2={scenario, stimulus, state, window} R3={scenario, state, interval} V1={initial_scope}.\n", ""),
    ("If a precise candidate cannot be expressed by the registry, set predicate_id to null. Do not silently drop it. ", ""),
    ("""missing guard/effect -> exact carrier transition ref. Predicate support controls
W2 versus W1 later and never licenses silent omission.""", "missing guard/effect -> exact carrier transition ref."),
    ("Obligation dossiers. These contain exact method outputs and backend facts, but no", "Obligation dossiers. These contain exact method outputs and supplied model facts, but no"),
    ("- do not turn execution uncertainty or an absent predicate into a semantic violation;\n", ""),
    ("""- backend or predicate unsupported status alone is not a competent undercutting
  reading; when exact facts satisfy expected behavior, use not_established/D0;""", "- when exact facts satisfy expected behavior, use not_established/D0;"),
)


def project_instruction(instruction: str) -> str:
    """Remove the mechanism only from a fixed, unrendered instruction literal."""

    for source, replacement in INSTRUCTION_EDITS:
        instruction = instruction.replace(source, replacement)
    return instruction


def build_semantic_evidence_record(
    *,
    obligation_id: str,
    candidate: CandidateIssue,
    binding: BindingResult,
    source_attribution: dict[str, Any],
    retry_records: list[dict[str, Any]],
    semantic_adjudication: SemanticAdjudication | None = None,
) -> dict[str, Any]:
    disposition = adjudicate_disposition(candidate, binding, semantic_adjudication, receipt=None)
    witness_level = "W1" if binding.precise else "W0"
    return {
        "schema": "evidence-discovery.semantic_evidence_record.v1",
        "obligation_id": obligation_id,
        "predicate_id": None,
        "binding": binding.model_dump(mode="json"),
        "plan": None,
        "receipt": None,
        "execution_receipt": None,
        "execution_status": "disabled_by_ablation",
        "witness_level": witness_level,
        "d_level": disposition["d_level"],
        "semantic_adjudication": disposition["semantic_adjudication"],
        "issue_emitted": binding.precise and disposition["d_level"] in {"D1", "D2"},
        "coverage_class": "semantic_hit" if binding.precise else "coverage_gap",
        "reason": disposition["reason"],
        "basis": disposition["basis"],
        "retry_records": retry_records,
        "source_attribution": source_attribution,
        "audit_bundle": None,
    }
