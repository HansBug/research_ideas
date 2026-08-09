from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal, TypedDict

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

from .predicates import (
    PREDICATE_BY_NAME,
    PREDICATE_NAMES,
    PREDICATE_ORDER,
    verification_kind_of,
)

#: Literal of every predicate name, so the closed vocabulary is enforced by the
#: schema the provider sees rather than only by prose in the prompt.
PredicateName = Literal[tuple(PREDICATE_ORDER)]  # type: ignore[valid-type]

SCHEMA_VERSION = "v2"


class StrictBaseModel(BaseModel):
    # JSON arrays are the wire representation of immutable tuple fields. Keep
    # extra-field rejection/frozen outputs while using StrictBool explicitly at
    # the truth-bearing method boundaries.
    model_config = ConfigDict(extra="forbid", frozen=True)


VerificationKind = Literal["structure", "behavior", "property"]
EvidenceFamily = Literal[
    "structure",
    "relation",
    "effect",
    "simulation",
    "fbmcq",
    "topology",
    "provenance",
]
#: `precondition` (issue #170 §11.4) checks a prerequisite of the primary rather
#: than discharging the requirement's predicate.  It is exempt from Gate D, its
#: `False` may still become an issue -- a missing element is a real defect -- and
#: it is the source of the dependency graph.
AssertionRole = Literal["primary", "supporting", "precondition"]


class CoverageObligation(StrictBaseModel):
    domain: str = Field(default="requirement", min_length=1)
    partition_by: str | None = Field(
        default=None,
        description=(
            "The dimension the obligation ranges over when it is not a single element, e.g. a "
            "composite whose children are each checked. Null for a single-element claim."
        ),
    )
    #: `custom` 与 `custom_policy_id` 已于 2026-08-09 退役：v37 全量 28,435 次 `aggregation`
    #: 里 **0 次** 用到它们，而它们占着一个进 tool schema 的枚举值、一个可选字段和一条
    #: validator。一个从未被选过的枚举值只会扩大 producer 的选择面。
    #:
    #: ⚠️ 同批候选里 `effect_declared` 与 `variable_delta_after` **没有**退役：它们看起来
    #: 「324 格 0 次执行」，但那 52 条 primary 是被为假的前置条件 `blocked` 掉的，不是没人写。
    #: 「从未执行」与「从未被规则驱动」是两件事，按错误的那件退役会删掉真正在用的能力。
    aggregation: Literal["all", "any", "exactly_one"] = Field(
        default="all",
        description=(
            "How the per-element results combine: `all` (every element must hold), `any` (at "
            "least one), or `exactly_one`."
        ),
    )
    limitations: tuple[str, ...] = Field(default_factory=tuple)


class NodeName(str, Enum):
    PREPARE = "prepare"
    SPLIT_REQUIREMENTS = "split_requirements"
    REVIEW_REQUIREMENTS = "review_requirements"
    CONVERT_ASSERTIONS = "convert_assertions"
    PRECHECK_AND_SEAL = "precheck_and_seal"
    REVIEW_ASSERTIONS = "review_assertions"
    RELEASE_RESULTS = "release_results"
    BIND_ATTRIBUTION = "bind_attribution"
    ADJUDICATE_RESULTS = "adjudicate_results"
    PUBLISH = "publish"


class RevisionFeedback(StrictBaseModel):
    target: Literal["requirements", "assertions"]
    reason: str = Field(min_length=1)
    findings: tuple[str, ...] = Field(default_factory=tuple)
    target_item_ids: tuple[str, ...] = Field(default_factory=tuple)
    recovery_seed: dict[str, Any] | None = None
    origin: Literal[
        "requirement_review",
        "assertion_contract",
        "assertion_precheck",
        "assertion_review",
    ] = "assertion_review"


class RevisionLedgerEvent(StrictBaseModel):
    """Append-only public history for one producer/reviewer revision loop."""

    sequence: int = Field(ge=1)
    loop: Literal["requirements", "assertions"]
    event: Literal[
        "artifact_created",
        "artifact_rejected",
        "artifact_quarantined",
        "check_completed",
        "review_completed",
    ]
    revision: int = Field(ge=1)
    artifact_hash: str | None = None
    status: str = Field(min_length=1)
    artifact_delta: dict[str, Any] = Field(default_factory=dict)
    rationale: str | None = None
    findings: tuple[str, ...] = Field(default_factory=tuple)
    item_ids: tuple[str, ...] = Field(default_factory=tuple)
    budget_counters: dict[str, int] = Field(default_factory=dict)


class DiscoverInput(StrictBaseModel):
    schema_name: Literal["DiscoverInput"] = "DiscoverInput"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str = Field(min_length=1)
    natural_language: str = Field(min_length=1)
    stm_text: str = Field(min_length=1)
    manifest: dict[str, Any] = Field(default_factory=dict)
    source_trace: dict[str, Any] = Field(default_factory=dict)
    profile: str = Field(default="fake", min_length=1)
    language: Literal["zh-CN", "en-US"] = "zh-CN"


class DiscoverRunIdentity(StrictBaseModel):
    run_id: str = Field(min_length=1)
    profile: str = Field(min_length=1)
    language: Literal["zh-CN", "en-US"]
    created_at: datetime


class FrozenDiscoverInputs(StrictBaseModel):
    schema_name: Literal["FrozenDiscoverInputs"] = "FrozenDiscoverInputs"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str = Field(min_length=1)
    natural_language: str = Field(min_length=1)
    stm_text: str = Field(min_length=1)
    nl_segments: dict[str, str] = Field(default_factory=dict)
    #: Whether the segments above were annotated by hand or split on newlines. Travels into
    #: the run record so a reader can tell which without re-deriving it; see
    #: `common/nl_segmentation.py` for why one specification needs annotation.
    nl_segmentation_source: Literal["manual_override", "line_split"] = "line_split"
    inspect_digest: dict[str, Any] = Field(default_factory=dict)
    source_trace: dict[str, Any] = Field(default_factory=dict)
    working_contract: dict[str, Any] = Field(default_factory=dict)
    input_hashes: dict[str, str]
    tool_env_hash: str = Field(min_length=1)
    profile: str = Field(min_length=1)
    language: Literal["zh-CN", "en-US"]
    # Deterministic pair-level verdict on whether bounded formal checking can
    # run at all on this model (see assertions.fbmcq.probe_fbmcq_feasibility).
    # Empty means "not probed"; the controller then keeps the strict contract.
    fbmcq_canary: dict[str, Any] = Field(default_factory=dict)
    resource_options: dict[str, Any] = Field(default_factory=dict)
    # Every state and event path the frozen model declares, so a relation query
    # over a non-existent element can be rejected instead of silently passing.
    known_model_paths: tuple[str, ...] = Field(default_factory=tuple)
    #: Declared paths grouped by kind, handed to the producers so they can bind a
    #: predicate to exact model terms instead of guessing them from the raw DSL.
    #: A guessed event name makes an assertion vacuously true, which is how pair
    #: 0029 lost a real defect to a one-character typo.
    model_vocabulary: dict[str, tuple[str, ...]] = Field(default_factory=dict)
    #: What the model expresses through `[*]` rather than through a name.
    #:
    #: Entry and termination have no declared element, so a producer reading only
    #: `model_vocabulary` sees nothing that could carry "when power off it reaches
    #: the final state" and concludes the model lacks it -- then proposes a
    #: `FinalState` that no correct model would declare.  Pair 0050 did exactly
    #: that, twice, on a model whose `HumanDrivingMode -> [*] : /Power_Off` is the
    #: right way to write termination.  Naming the facts here is what lets the
    #: four-step procedure decide step 1 from evidence instead of by guessing.
    #:
    #: `terminating_transitions`: `{source, trigger}` per edge that ends a run.
    #: `initial_entries`: `{composite, target, unconditional}` per declared entry.
    pseudo_state_facts: dict[str, tuple[dict[str, Any], ...]] = Field(
        default_factory=dict
    )


class RequirementSourceContext(StrictBaseModel):
    """`Requirement.source_context` 的结构，取代原先的 `dict[str, Any]`。

    ⚠️ `dict[str, Any]` 在 JSON Schema 里退化成 `{"additionalProperties": true}` —— `Any` 把类型
    信息全擦掉，生产者看到的就是「随便填」。实测后果：产出里稳定出现 `nl_parent`（80 次）这个**两边都没要求的键**，而消费侧只读
    `behavior_phase`。

    ⚠️ `basis` 曾被我误判为生产者发明 —— 它其实是 `prompts.py` 明确要求的（「always emit it, with
    `basis` and `behavior_phase`」）。那份契约一直存在，只是**存在于 prompt 而不在 schema** ——
    这正是本次迁移要消除的分裂。

    改成模型后，键名与取值范围由类型自己承载，随 `model_json_schema()` 一起到达生产者，
    也不再需要靠 `json_schema_extra` 手工贴一份说明（那份会与实际校验脱同步）。

    ⚠️ `extra="forbid"` 由 `StrictBaseModel` 继承而来，所以发明的键会被**明确拒绝**并进入
    契约修复循环，而不是静默留在产物里。
    """

    behavior_phase: (
        Literal["structure", "initialization", "operation", "termination"] | None
    ) = Field(
        default=None,
        description=(
            "Which phase the claim is anchored in: `structure` for a claim about what the model "
            "contains, `initialization` for power-on or first entry, `operation` while the "
            "machine already runs, `termination` for the run ending. Gates read this -- `\"[*]\"` "
            "as a `source` or `scope` is accepted only under `initialization`, because anchoring "
            "any other phase before the machine has entered anything asks a different question, "
            "and a model that happens to be wrong in that configuration then answers true for a "
            "reason the sentence never raised. Omitting it is treated as not-initialization."
        ),
    )
    basis: str = Field(
        default="",
        description=(
            "Where in the input this claim is anchored -- the segment or clause it rests on, in "
            "the requested content language. Always emit it."
        ),
    )
    nl_parent: str | None = Field(
        default=None,
        description=(
            "For a containment claim, the parent the NL itself places the child under. A gate "
            "reads it: without it a containment binding cannot be checked against the sentence "
            "and the claim is refused."
        ),
    )
    trace_entry_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Ids that exist verbatim in the supplied source trace. An id not present there is "
            "rejected deterministically."
        ),
    )


class RequirementDerivation(StrictBaseModel):
    """一条 Requirement 是**从另一条 Requirement 机械派生**的，而不是从某句 NL 长出来的。

    ## 为什么需要这个字段

    Splitter 与 Requirement Reviewer 此前有一处**直接冲突**，实测让派生义务在多数格里被删掉：

    - splitter 侧写着「Whenever you form a `cardinality` Requirement on a composite, form exactly
      one entry Requirement on that same composite too. **This trigger is mechanical: it does not
      depend on recognising a phrasing.**」
    - reviewer 侧的常设指令是「Do not add a semantic distinction merely because the current FCSTM
      exposes a convenient state, event, transition, or variable」，并且它**看不到**上面那条触发器
      （实测：该触发器文本只存在于 splitter prompt，reviewer / converter / adjudicator 全为 0 命中）。

    于是 reviewer 按自己的规则判「无 NL 出处 → 语义添加 → 删」，而它是对的 —— 它无从分辨
    「凭 FCSTM 方便就加的义务」和「从一条 NL-grounded 义务蕴含出来的义务」。

    **两者的差别无法从产物推断，只能由 splitter 申报。** 这个模型就是那份申报：带上它，
    reviewer 就有了可判定的判据（见 `kind`）；不带它，reviewer 的原规则不变。

    ⚠️ 这不是给派生义务的免检通道。reviewer 仍可删，只是必须点明是四条判据里的哪一条不满足。
    """

    kind: Literal["entry_follows_cardinality", "activation_residency"] = Field(
        description=(
            "Which licensed entailment this is. The list is closed: an entailment not on it is not "
            "a licensed derivation, and the reviewer deletes the requirement on that ground alone. "
            "`entry_follows_cardinality` -- the parent says how many children a composite declares, "
            "so entering that composite has to land on one of them; a model can declare exactly the "
            "right children and still have no declared way into any of them. "
            "`activation_residency` -- the parent conditions a composite's activation on a trigger, "
            "so the run has to be inside that composite once the trigger arrives; consuming the "
            "event and then leaving are independently violable."
        ),
    )
    parent_requirement_id: str = Field(
        pattern=r"^REQ-[A-Za-z0-9_.-]+$",
        min_length=5,
        description=(
            "The `requirement_id` this one is entailed by. It must be a requirement in this same "
            "set, and it must itself be anchored in the NL -- a derivation whose parent is also "
            "derived has no NL floor and is refused. The reviewer checks the parent's bindings "
            "against this one's: the entailment is only about the parent's own scope."
        ),
    )


class Requirement(StrictBaseModel):
    requirement_id: str = Field(
        pattern=r"^REQ-[A-Za-z0-9_.-]+$",
        min_length=5,
        description=(
            "Stable identifier, `REQ-` followed by digits or dot-separated parts (e.g. REQ-004, "
            "REQ-006B). Reuse the same id across revisions for the same claim; a renamed id reads "
            "as a removed requirement plus a new one."
        ),
    )
    statement: str = Field(
        min_length=1,
        description=(
            "The obligation in one sentence, in the requested content language. State what the "
            "artifact must satisfy -- not whether it does."
        ),
    )
    rationale: str = Field(
        default="",
        description=(
            "Why this obligation follows from the cited NL segments. Name the segment and quote the "
            "words you relied on."
        ),
    )
    source_segment_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "The `nl_segments` ids this obligation comes from, verbatim. Every id you list must "
            "exist in the input, and every segment you mark `covered` in `segment_disposition` must "
            "be listed by at least one requirement here."
        ),
    )
    # Lightweight, input-derived scope ledger.  It may record explicit or
    # carefully qualified inferred source context, but never evaluator gold.
    source_context: RequirementSourceContext = Field(
        default_factory=RequirementSourceContext,
        description=(
            "Input-derived scope ledger. Never put evaluator expectations or model-derived "
            "answers here -- it records where in the *input* the claim is anchored."
        ),
    )
    derivation: RequirementDerivation | None = Field(
        default=None,
        description=(
            "Set this only when the requirement is mechanically entailed by another requirement in "
            "this set rather than stated by an NL segment -- then `source_segment_ids` may be empty "
            "and the reviewer judges it by the four conditions on `RequirementDerivation` instead of "
            "looking for an NL source. Leave it null for every requirement an NL segment states: a "
            "false derivation claim moves the requirement out of NL review and is treated as a "
            "contract violation, not as a shortcut."
        ),
    )
    predicate: PredicateName | None = Field(
        default=None,
        description=(
            "The claim shape, from the closed vocabulary. It *derives* `verification_kind` and the "
            "mandatory evidence family, so pick the predicate whose procedure actually decides the "
            "sentence rather than a cheaper neighbour: a declaration query cannot settle a runtime "
            "claim, and a runtime query cannot settle what the artifact declares."
        ),
    )
    #: Concrete arguments for the predicate, e.g. {"source": ..., "trigger": ...}.
    #: They give the converter the terms to bind and let a later gate check that
    #: the assertion tests this claim rather than an easier neighbouring one.
    predicate_bindings: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "The predicate's arguments, keyed by that predicate's own parameter names (e.g. "
            "`source`, `trigger`, `target` for edge_declared; `composite`, `child` for "
            "initial_target; `scope`, `count` for cardinality). Every value that names a model "
            "element must be a complete dotted path copied verbatim from "
            "`declared_model_vocabulary`, not a bare name and not retyped from the FCSTM text. "
            "`\"[*]\"` is the pseudo-initial and is only legal where the predicate documents it. A "
            "value naming an element the model does not declare is allowed only when `limitations` "
            "records that."
        ),
    )

    @field_validator("predicate_bindings", mode="before")
    @classmethod
    def _stringify_binding_values(cls, value: Any) -> Any:
        """Accept `count=3` as well as `count="3"`.

        The literal bindings are naturally numeric and the prompt renders
        `count: int`, so a producer writing an int was following instructions;
        rejecting it cost a repair round for nothing.
        """

        if not isinstance(value, dict):
            return value
        return {
            str(k): (v if isinstance(v, str) else ("" if v is None else str(v)))
            for k, v in value.items()
        }
    verification_kind: VerificationKind = Field(
        description=(
            "Derived from `predicate` by table lookup -- emit the family that predicate's "
            "vocabulary entry states. Do not judge it per sentence: that judgement is what two "
            "models used to answer differently for the same requirement."
        ),
    )
    quantifier: str = Field(
        default="unspecified",
        min_length=1,
        description=(
            "Scope of the claim over configurations or elements, e.g. `unspecified`, `all`, "
            "`exists`. Leave `unspecified` unless the sentence really quantifies."
        ),
    )
    trigger: str | None = Field(
        default=None,
        description=(
            "The event the claim is conditioned on, as a complete declared path, when the sentence "
            "names one. Null when the claim is unconditional."
        ),
    )
    expected_outcome: str | None = Field(
        default=None,
        description=(
            "What holds if the artifact satisfies this obligation, in the requested content "
            "language."
        ),
    )
    timing: str | None = None
    coverage_obligation: CoverageObligation = Field(default_factory=CoverageObligation)
    limitations: tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "One entry per way this obligation had to be weakened or re-scoped, and why. Two forms "
            "are load-bearing: an entry beginning exactly `scope-local instance required` keeps a "
            "proposed per-scope path that the shared-element comparison would otherwise refuse; and "
            "an entry recording that the model declares no counterpart is what makes a binding to "
            "an undeclared name admissible."
        ),
    )
    # Read-only compatibility for v1 fixtures and historical artifacts. New
    # producer prompts must emit verification_kind and leave this field absent.
    checkability: (
        Literal[
            "structure",
            "relation",
            "effect",
            "simulation",
            "fbmcq",
            "topology",
            "provenance",
        ]
        | None
    ) = Field(
        default=None,
        exclude=True,
        description=(
            "Legacy v1 field. Do not emit it -- emit `verification_kind` and `coverage_obligation`."
        ),
    )

    @model_validator(mode="before")
    @classmethod
    def _derive_kind_from_predicate(cls, value: Any) -> Any:
        """Let the named predicate settle the family, and reject unknown names.

        The predicate is authoritative on purpose.  If a producer names
        ``occupancy_after`` but labels the requirement ``structure``, honouring
        the label would let a declaration check close a runtime claim -- the
        false-positive shape this vocabulary exists to prevent.  So the label is
        overwritten, not merely validated.
        """

        if not isinstance(value, dict):
            return value
        predicate = value.get("predicate")
        if predicate is None:
            return value
        if not isinstance(predicate, str) or predicate not in PREDICATE_NAMES:
            raise ValueError(
                f"unknown predicate {predicate!r}; use one of the closed "
                f"vocabulary: {', '.join(sorted(PREDICATE_NAMES))}"
            )
        entry = PREDICATE_BY_NAME[predicate]
        bound = value.get("predicate_bindings") or {}
        required, forbidden = entry.bindings, ()
        # `entry_follows_cardinality` binds the composite and **must not** bind a child.
        #
        # `initial_target(composite, child)` answers "is *this* child the unconditional entry", so
        # it is False for every child except the one that is. The derived obligation is the weaker
        # and correct claim "entry lands on *some* declared child", which is a disjunction over the
        # children -- and a disjunction cannot live in `dict[str, str]`. Naming one child here is
        # not an approximation of it, it is a different claim that fails a model entered properly
        # through another child.
        #
        # So the shape is not relaxed, it is *replaced*: the child slot moves from required to
        # forbidden, the assertion stage expands the disjunction from the composite, and the wrong
        # shape becomes unrepresentable rather than merely discouraged. Measured on v35 before this
        # change: 2 disjunctions against 23 single bindings, while the splitter prompt already said
        # in as many words that a single binding "reports a defect on a correct model".
        derivation = value.get("derivation")
        kind = derivation.get("kind") if isinstance(derivation, dict) else getattr(derivation, "kind", None)
        if kind == "entry_follows_cardinality" and predicate == "initial_target":
            required = tuple(name for name in entry.bindings if name != "child")
            forbidden = ("child",)
        missing = [
            name
            for name in required
            if not str(bound.get(name) or "").strip()
        ]
        if missing:
            raise ValueError(
                f"predicate {predicate!r} requires bindings {list(required)}; "
                f"missing or empty: {missing}"
            )
        present = [name for name in forbidden if str(bound.get(name) or "").strip()]
        if present:
            raise ValueError(
                f"a `{kind}` derivation must not bind {present}: the obligation is that entry lands "
                f"on *some* declared child, and naming one makes the check False for a model that "
                f"entered correctly through another. Bind only "
                f"{list(required)} -- the assertion stage forms the disjunction over the children."
            )
        return {**value, "verification_kind": verification_kind_of(predicate)}

    @model_validator(mode="before")
    @classmethod
    def _upgrade_v1_checkability(cls, value: Any) -> Any:
        if not isinstance(value, dict) or value.get("verification_kind"):
            return value
        legacy = value.get("checkability")
        mapping = {
            "structure": "structure",
            "relation": "structure",
            "topology": "structure",
            "provenance": "structure",
            "effect": "behavior",
            "simulation": "behavior",
            "fbmcq": "property",
        }
        if legacy in mapping:
            return {**value, "verification_kind": mapping[legacy]}
        return value


class NamedElement(StrictBaseModel):
    """One element the NL names, and whether the model declares it.

    ## 为什么这是字段而不是散文

    v37 的最大单项损失是需求层没形成义务：135 个未命中位（占全部未命中的 39%）的台账谓词
    从未被写进需求集，其中事件类 37 位。v40 把「差集扫描」写成散文后，`event_declared` 的
    形成格数从 4/36 涨到 23/35，**但调用真值是 110 True / 17 False** —— 模型开始写它了，
    却仍绑在制品已声明的名字上，那种检查按构造只能为真。`event_consumed` 更彻底：跨两代
    102 次调用，False 恒为 0。

    本仓库对同一现象有可复算的度量：落在 typed 槽位的规则遵守率 96–100%（`strategies`
    11,826/11,842；`nl_parent` 1,489/1,489），落在 free-text 里当协议用的 25–38%
    （`incumbent considered:` 305/803）。散文说不动的事，槽位能。

    所以枚举**方向**在这里被做成结构：`name_in_sentence` 必填，`declared_match` 是比对结果
    而不是选择。填这张表就是在做「句子点名了什么 → 模型有没有」，而不是反过来。

    provenance: IEEE 29148-2018 §5.2 —— 规范点名的每个要素构成一条独立于其行为的义务；
    形式语义中的预设（presupposition）。
    """

    schema_name: Literal["NamedElement"] = "NamedElement"
    kind: Literal["state", "event", "variable"]
    #: 句子里的原措辞，逐字。不是路径，不做规范化 —— 它是「谁点的名」的证据。
    name_in_sentence: str = Field(min_length=1)
    #: 该措辞规范化后应有的路径/名字：state 与 event 用 `<root>.<name>`，variable 用裸名。
    proposed_path: str = Field(min_length=1)
    #: `declared_model_vocabulary` 里**末段精确相等**的那一条；没有则 null。
    #: null 就是发现：句子点了名而模型没有它。
    declared_match: str | None = None


class RequirementSet(StrictBaseModel):
    schema_name: Literal["RequirementSet"] = "RequirementSet"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    revision: int = Field(
        ge=1,
        description=(
            "Artifact version counter. On create emit 1. On revise emit the value given as "
            "`revision_to_emit` in the input (always current+1): a revision that does not exceed "
            "the current one is rejected deterministically, and repeating the previous value "
            "consumes the repair budget without changing anything."
        ),
    )
    #: 句子点名的每一个 state / event / variable，以及它在 declared vocabulary 里的比对结果。
    #: `declared_match is None` 的每一项都欠一条对应的 `*_declared` Requirement —— 由
    #: `capability.unmatched_named_element_findings` 机械检查，不靠自觉。
    named_elements: tuple[NamedElement, ...] = Field(default_factory=tuple)
    requirements: tuple[Requirement, ...] = Field(
        min_length=1,
        description=(
            "One entry per independently violable claim. At least one is required -- an empty set "
            "cannot be constructed."
        ),
    )
    segment_disposition: dict[
        str, Literal["covered", "context", "ambiguous", "out_of_scope"]
    ] = Field(
        default_factory=dict,
        description=(
            "One key per NL segment id, exactly the ids supplied in `nl_segments`. `covered` "
            "asserts that some Requirement here carries that segment's obligation; marking a "
            "segment covered with nothing assertable behind it is the most common review rejection. "
            "Use `context` for background, `ambiguous` when it cannot be operationalised, "
            "`out_of_scope` when it asks for something the modelling object excludes."
        ),
    )

    @field_validator("requirements")
    @classmethod
    def _unique_requirement_ids(
        cls, reqs: tuple[Requirement, ...]
    ) -> tuple[Requirement, ...]:
        ids = [req.requirement_id for req in reqs]
        if len(ids) != len(set(ids)):
            raise ValueError("requirement_id values must be unique")
        return reqs


class RequirementCoverageProjection(StrictBaseModel):
    covered_requirement_ids: tuple[str, ...]
    missing_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    accepted_requirement_ids: tuple[str, ...] = Field(default_factory=tuple)
    quarantined_requirement_ids: tuple[str, ...] = Field(default_factory=tuple)
    orphaned_covered_segment_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Segments still marked `covered` whose only carrier was quarantined by a gate in this "
            "same step. They are **not** producer error -- the emitted set was consistent, and the "
            "quarantine made it inconsistent. Nothing re-marks them automatically: a segment "
            "silently changed to `context` would erase the record that it was ever claimed "
            "covered, and choosing the right verdict is a semantic judgement the pipeline must not "
            "make for the producer. So the fact is recorded here for the reviewer to act on -- "
            "either a requirement is added back that carries the obligation, or the segment is "
            "re-marked to what it really is."
        ),
    )


class CoverageGap(StrictBaseModel):
    gap_id: str = Field(pattern=r"^GAP-[A-Za-z0-9_.-]+$", min_length=5)
    stage: Literal["requirement_split", "assertion_conversion", "assertion_review"]
    requirement_id: str | None = None
    assertion_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    reason_code: Literal[
        "no_progress",
        "revision_budget_exhausted",
        "contract_invalid",
        "review_unresolved",
    ]
    reason: str = Field(min_length=1)
    last_revision: int = Field(ge=0)
    last_feedback: str | None = None
    history_refs: tuple[str, ...] = Field(default_factory=tuple)
    coverage_impact: str = Field(min_length=1)
    blocks_full_coverage: StrictBool


class ExcludedObservation(StrictBaseModel):
    assertion_id: str
    requirement_id: str
    role: AssertionRole
    disposition: Literal[
        "supporting_false",
        "quarantined",
        "representation_debt",
        "unattributed",
    ]
    rationale: str = Field(min_length=1)


class RequirementReviewFinding(StrictBaseModel):
    requirement_id: str | None = None
    severity: Literal["critical", "important", "minor"]
    message: str = Field(min_length=1)
    required_change: str = Field(min_length=1)


class RequirementReview(StrictBaseModel):
    schema_name: Literal["RequirementReview"] = "RequirementReview"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    decision: Literal["accept", "revise"]
    reviewed_revision: int = Field(
        ge=1,
        description=(
            "The `revision` of the exact RequirementSet you reviewed, copied from the input. A "
            "mismatch means the review is about a different artifact and is rejected."
        ),
    )
    findings: tuple[RequirementReviewFinding, ...] = Field(
        default_factory=tuple,
        description=(
            "One entry per problem, each naming the offending requirement_id and what to change. A "
            "finding the producer cannot act on is re-emitted unchanged and wastes a repair round."
        ),
    )
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def _decision_findings_consistent(self) -> "RequirementReview":
        if self.decision == "accept" and self.findings:
            raise ValueError("accept reviews must not contain findings")
        if self.decision == "revise" and not self.findings:
            raise ValueError("revise reviews require at least one finding")
        return self


class AssertionSpec(StrictBaseModel):
    assertion_id: str = Field(pattern=r"^AST-[A-Za-z0-9_.-]+$", min_length=5)
    requirement_id: str = Field(pattern=r"^REQ-[A-Za-z0-9_.-]+$", min_length=5)
    description: str = Field(min_length=1)
    #: 这条断言在证据层面**说不到**的东西。converter prompt 与 assertion reviewer 此前都要求
    #: 「record in `limitations`」，而这个字段并不存在于本模型上（`limitations` 是 Requirement
    #: 的字段，且需求在断言阶段已冻结、converter 无权改）。v37 实测：637 条 assertion-review
    #: finding 里 70 条（11%）在追这个不存在的字段，reviewer 已自行改投 description/rationale
    #: 绕道 —— 每一轮都在为一条 prompt 指错了归属地的字段消耗修订预算。
    #:
    #: provenance: 「一条策略只能有一个归属地」（本仓库 CLAUDE.md 工程纪律）；字段名与执行点
    #: 必须落在同一个模型上，否则规则既无法被满足也无法被检查。
    limitations: tuple[str, ...] = Field(default_factory=tuple)
    expression: str = Field(min_length=1)
    failure_message: str = Field(min_length=1)
    evidence_family: EvidenceFamily
    # Required in the schema, not merely in the prompt.  These used to be
    # optional with a validator that back-filled a missing value as
    # `legacy:<id>` / `legacy-group:<id>`; the object then validated, and a
    # downstream gate rejected it *for being legacy*.  One omitted field
    # therefore isolated every assertion in the script and killed the cell with
    # "soft isolation cannot publish an empty AssertionScript" -- three of eight
    # matrix cells died exactly this way.  Requiring them puts the failure where
    # it belongs: in the provider's own structured-output validation, one repair
    # round instead of a dead run.
    role: AssertionRole
    coverage_key: str = Field(min_length=1)
    aggregation_group: str = Field(min_length=1)
    #: Assertion ids that must have evaluated **True** before this one runs.  A
    #: plain list, not a mapping: dependencies keyed on a required truth value
    #: were considered and dropped, because a "run only if the prerequisite is
    #: false" branch is expressible as two unconditional assertions and would
    #: make both the graph semantics and the repair stage's reading of it harder.
    depends_on: tuple[str, ...] = Field(default_factory=tuple)
    #: Why this assertion is written this way: which NL clause grounds it, why
    #: this predicate, and -- for a precondition standing in for a term the model
    #: lacks -- why this proposed name.  Distinct from `description`, which says
    #: *what* is checked; this says *why*.  Kept separate because the reviewer
    #: needs an NL citation it can verify, and a producer given one field writes
    #: only the restatement.
    rationale: str = Field(min_length=1)

    @field_validator("expression")
    @classmethod
    def _expression_is_an_expression(cls, value: str) -> str:
        """Reject a whole `assert` statement written into the expression field.

        The controller wraps this value as `assert (<value>), <failure_message>`.
        A producer that writes the statement form ends up with
        `assert (assert ... , "..."), "..."`, which is a syntax error on every
        assertion in the script; both Claude cells of matrix v7 died that way --
        five identical `AssertionScriptSyntaxError`s, every item quarantined, then
        `soft isolation cannot publish an empty AssertionScript`.  Caught here it
        is the provider's own structured-output validation error, naming the field
        and the fix, in one round.
        """

        text = value.strip()
        if text.startswith("assert ") or text.startswith("assert("):
            raise ValueError(
                "expression must be a bare boolean expression, not an `assert` "
                "statement: the controller adds `assert (...)` and your "
                "failure_message itself. Write "
                "`state_declared(state=\"X\", kind=\"leaf\") is True`, and put the "
                "[REQ-xxx][AST-xxx] label in `failure_message`."
            )
        return value


class AssertionScript(StrictBaseModel):
    schema_name: Literal["AssertionScript"] = "AssertionScript"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    revision: int = Field(
        ge=1,
        description=(
            "Artifact version counter. On create emit 1. On revise emit `revision_to_emit` from the "
            "input (always current+1); repeating the previous value only consumes the repair "
            "budget."
        ),
    )
    prefix: str = ""
    assertions: tuple[AssertionSpec, ...] = Field(
        min_length=1,
        description=(
            "One entry per check. Every accepted Requirement needs at least one `primary` calling "
            "the procedure its `predicate` names, bound to its `predicate_bindings`."
        ),
    )
    requirement_mapping: dict[str, tuple[str, ...]] = Field(
        default_factory=dict,
        description=(
            "requirement_id -> the assertion_ids carrying it. Every accepted requirement must "
            "appear."
        ),
    )
    #: `{requirement_id: how this group of assertions jointly covers it}`.  The
    #: reviewer previously had to infer the decomposition intent from a bare list
    #: of assertions; with preconditions and dependencies in play that inference
    #: is no longer tractable.
    strategies: dict[str, str] = Field(default_factory=dict)

    @field_validator("assertions")
    @classmethod
    def _unique_assertion_ids(
        cls, assertions: tuple[AssertionSpec, ...]
    ) -> tuple[AssertionSpec, ...]:
        ids = [item.assertion_id for item in assertions]
        if len(ids) != len(set(ids)):
            raise ValueError("assertion_id values must be unique")
        return assertions


class AssertionExecutionPublic(StrictBaseModel):
    assertion_id: str
    requirement_id: str
    role: AssertionRole = "primary"
    coverage_key: str | None = None
    #: `blocked` means a prerequisite did not hold, so this assertion was never
    #: run.  It is not an execution failure and must not send the script back for
    #: repair -- the prerequisite's own `False` is the finding.  Downstream it
    #: counts as *not satisfied* (issue #170 §11.5); the distinction exists for
    #: the record and the report, not for the verdict.
    status: Literal["executable", "invalid", "blocked"]
    error: str | None = None


class AssertionCheckPublic(StrictBaseModel):
    schema_name: Literal["AssertionCheckPublic"] = "AssertionCheckPublic"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    script_hash: str = Field(min_length=1)
    tool_env_hash: str = Field(min_length=1)
    status: Literal["executable", "invalid"]
    executions: tuple[AssertionExecutionPublic, ...]

    @model_validator(mode="after")
    def _status_matches_executions(self) -> "AssertionCheckPublic":
        # `blocked` is deliberately allowed inside an `executable` check: the
        # script ran fine, one item simply had an unmet prerequisite.  Treating it
        # as invalid would send the whole script back for a repair nobody can
        # make, which is the deadlock class issue #170 §10.9 records.
        if self.status == "executable" and any(
            e.status == "invalid" for e in self.executions
        ):
            raise ValueError("executable check cannot contain invalid executions")
        if self.status == "invalid" and not any(
            e.status == "invalid" for e in self.executions
        ):
            raise ValueError("invalid check requires an invalid execution")
        return self


class AssertionResult(StrictBaseModel):
    assertion_id: str
    requirement_id: str
    role: AssertionRole = "primary"
    coverage_key: str | None = None
    aggregation_group: str | None = None
    truth_value: StrictBool
    script_hash: str
    tool_env_hash: str
    evidence_family: str = Field(min_length=1)
    failure_message: str | None = None
    evidence_scope: dict[str, Any] = Field(default_factory=dict)
    evidence_record_ids: tuple[str, ...] = Field(default_factory=tuple)
    check_detail: dict[str, Any] = Field(default_factory=dict)


class SealedAssertionReceipt(StrictBaseModel):
    schema_name: Literal["SealedAssertionReceipt"] = "SealedAssertionReceipt"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    script_hash: str = Field(min_length=1)
    tool_env_hash: str = Field(min_length=1)
    sealed_hash: str = Field(min_length=1)
    result_count: int = Field(ge=0)
    sealed_payload_ref: str = Field(min_length=1)


class AssertionReviewFinding(StrictBaseModel):
    assertion_id: str | None = None
    requirement_id: str | None = None
    severity: Literal["critical", "important", "minor"]
    message: str = Field(min_length=1)
    required_change: str = Field(min_length=1)


class AssertionReview(StrictBaseModel):
    schema_name: Literal["AssertionReview"] = "AssertionReview"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    decision: Literal["accept", "revise"] = Field(
        description=(
            "`accept` only with no findings; otherwise `revise` with concrete, actionable findings. "
            "Never accept with findings and never revise without any."
        ),
    )
    reviewed_script_hash: str = Field(
        min_length=1,
        description=(
            "Hash of the exact AssertionScript you reviewed, copied from the input. A mismatch "
            "means the review is about a different artifact and is rejected."
        ),
    )
    findings: tuple[AssertionReviewFinding, ...] = Field(
        default_factory=tuple,
        description=(
            "One entry per problem, each naming the offending assertion_id and what to change. A "
            "finding the producer cannot act on is re-emitted unchanged and wastes a repair round."
        ),
    )
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def _decision_findings_consistent(self) -> "AssertionReview":
        if self.decision == "accept" and self.findings:
            raise ValueError("accept reviews must not contain findings")
        if self.decision == "revise" and not self.findings:
            raise ValueError("revise reviews require at least one finding")
        return self


class ReleasedAssertionResults(StrictBaseModel):
    schema_name: Literal["ReleasedAssertionResults"] = "ReleasedAssertionResults"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    script_hash: str
    tool_env_hash: str
    sealed_hash: str
    results: tuple[AssertionResult, ...]


class AttributionBinding(StrictBaseModel):
    assertion_id: str
    requirement_id: str
    status: Literal["safe", "representation_debt", "unattributed"]
    source_refs: tuple[str, ...] = Field(default_factory=tuple)
    trace_entry_ids: tuple[str, ...] = Field(default_factory=tuple)
    exclusion_refs: tuple[str, ...] = Field(default_factory=tuple)
    source_level_claim_allowed: StrictBool = False
    rationale: str = Field(min_length=1)


class AttributionProjection(StrictBaseModel):
    schema_name: Literal["AttributionProjection"] = "AttributionProjection"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    bindings: tuple[AttributionBinding, ...]


class AdjudicatedIssue(StrictBaseModel):
    """One defect, which may be the reason several Requirements failed.

    Requirements are split for checkability rather than by root cause -- `occupancy_after`
    needs a concrete `source`, so a sentence that leaves the source open becomes one
    Requirement per running mode. When the underlying model defect is a single misplaced
    edge, every one of those Requirements fails for that one reason, and reporting them
    separately inflates the defect count.

    `shared_root_cause` and `shared_elements` are what stop that allowance from becoming a
    way to shrink the count instead: a group spanning Requirements must say where the shared
    cause is and name the elements it rests on. `adjudicate_results` enforces their presence,
    and separately enforces that `requirement_ids` equals the Requirements owning the
    referenced assertions -- so a group can neither drop one nor claim one it never touched.
    """

    issue_id: str = Field(pattern=r"^ISSUE-[A-Za-z0-9_.-]+$", min_length=7)
    requirement_ids: tuple[str, ...] = Field(
        min_length=1,
        description=(
            "Every requirement whose False primary this one issue reports. More than one is correct "
            "when a single model edit resolves all of them; then `shared_root_cause` is required."
        ),
    )
    assertion_ids: tuple[str, ...] = Field(
        min_length=1,
        description=(
            "Only the primary and precondition assertion ids carrying the defect. Supporting "
            "evidence is routed by the deterministic layer and must not appear here."
        ),
    )
    title: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    attribution_status: Literal["safe", "representation_debt", "unattributed"] = Field(
        description=(
            "Copied from the frozen attribution for this evidence. Only `safe` may be "
            "published."
        ),
    )
    #: Required once `requirement_ids` holds more than one entry. Absent on single-Requirement
    #: issues, and absent on every excluded finding -- exclusions are never merged.
    shared_root_cause: str | None = None
    shared_elements: tuple[str, ...] = Field(default_factory=tuple)

    @model_validator(mode="before")
    @classmethod
    def _accept_legacy_singular(cls, data: Any) -> Any:
        """Read run records written before this field was pluralised.

        `StrictBaseModel` forbids unknown keys, so without this every
        `discover-completed.json` from v11-v18 would fail to load -- and those are the
        baseline the merge change is measured against. Only the read path is lenient; the
        tool schema handed to the adjudicator advertises `requirement_ids` alone, so nothing
        new is written in the old shape. Carrying both keys is an error rather than a
        precedence rule: two disagreeing answers to "which Requirement" is not a record
        worth guessing about.
        """
        if not isinstance(data, dict) or "requirement_id" not in data:
            return data
        if "requirement_ids" in data:
            raise ValueError(
                "AdjudicatedIssue carries both requirement_id and requirement_ids"
            )
        migrated = dict(data)
        migrated["requirement_ids"] = (migrated.pop("requirement_id"),)
        return migrated


class DiscoverAdjudication(StrictBaseModel):
    schema_name: Literal["DiscoverAdjudication"] = "DiscoverAdjudication"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    has_confirmed_issues: StrictBool
    issues: tuple[AdjudicatedIssue, ...] = Field(
        default_factory=tuple,
        description=(
            "Confirmed model defects. Create one only from a False primary or precondition "
            "assertion whose binding status is safe -- a True assertion is a satisfied obligation, "
            "never a finding."
        ),
    )
    satisfied_requirement_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "A requirement belongs here if and only if every released assertion for it is True. If "
            "any is False -- including one routed to excluded_findings -- it does not belong here."
        ),
    )
    excluded_findings: tuple[AdjudicatedIssue, ...] = Field(
        default_factory=tuple,
        description=(
            "False assertions that cannot be attributed to the author's model (compiler-owned or "
            "lowering- excluded evidence). Recorded, not published as defects."
        ),
    )
    excluded_observations: tuple[ExcludedObservation, ...] = Field(
        default_factory=tuple
    )
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def _issue_flag_consistent(self) -> "DiscoverAdjudication":
        # Neither `has_confirmed_issues` nor attribution status is checked here, though both
        # once were.
        # Structured-output validation is recorded `retryable: False` in the responder, so a
        # rejection at this layer is as fatal as one further down -- it kills the node, which
        # has no contract-feedback round. Meanwhile which basket a primary False belongs in
        # follows from its attribution status alone, so a misfiled one is a clerical error
        # the deterministic layer can simply correct. `adjudicate_results` sorts both
        # collections by status and records every move; it re-establishes the invariant this
        # check used to assert, at a point where getting it wrong costs a correction instead
        # of a whole run. The flag is likewise re-derived there from the sorted collections,
        # so asserting it at parse time protects nothing and can only kill the cell -- and a
        # model that files a safe finding as an exclusion is exactly the model that will then
        # report `has_confirmed_issues=false` to match.
        #
        # Supporting False observations can arrive in excluded_findings from the structured
        # LLM response. The same node removes them before enforcing primary-only closure.
        return self


class DiscoverCompleted(StrictBaseModel):
    schema_name: Literal["DiscoverCompleted"] = "DiscoverCompleted"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str
    status: Literal["completed"] = "completed"
    input_hashes: dict[str, str]
    requirement_set_hash: str
    assertion_script_hash: str
    released_results_hash: str
    adjudication: DiscoverAdjudication
    issues: tuple[AdjudicatedIssue, ...]
    coverage_status: Literal["full", "partial"] = "full"
    coverage_gaps: tuple[CoverageGap, ...] = Field(default_factory=tuple)
    #: Stages that hit an internal budget, gave up on an obligation, and let the run continue
    #: (CLAUDE.md §10).  Published rather than kept in graph state because that is the whole
    #: point: a degraded cell lands a normal-looking artifact, and without this field a reader
    #: of `discover-completed.json` cannot tell "found nothing" from "stopped looking".
    #:
    #: `coverage_gaps` is not a substitute.  Gaps say *what* was not covered and are also
    #: written by ordinary item-local isolation, which is routine; this says *where the
    #: pipeline abandoned its budget*, which is not.  A non-empty value means the cell is
    #: still eligible for recall-side statistics -- it produced an artifact -- but its
    #: zero-issue result must not be read as "no defects found".
    degraded_stages: tuple[str, ...] = Field(default_factory=tuple)
    satisfied_requirement_ids: tuple[str, ...] = Field(default_factory=tuple)
    # Primary False assertions the adjudicator kept out of `issues` because
    # their attribution is representation_debt or unattributed.  These were
    # recorded in the adjudication but never surfaced in the published
    # artifact, so a reader of discover-completed.json could not tell "no
    # evidence was produced" from "False evidence could not be attributed" --
    # on pair 0006 that hid the entire EXP-0006-EA-001 observation.
    excluded_findings: tuple[AdjudicatedIssue, ...] = Field(default_factory=tuple)
    excluded_observations: tuple[ExcludedObservation, ...] = Field(
        default_factory=tuple
    )
    adjudication_reconciliation: dict[str, Any] = Field(default_factory=dict)
    regression_guards: tuple[str, ...] = Field(default_factory=tuple)
    telemetry_summary: dict[str, Any] = Field(default_factory=dict)
    content_language: Literal["zh-CN", "en-US"] = "zh-CN"


class RunFailure(StrictBaseModel):
    schema_name: Literal["RunFailure"] = "RunFailure"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str
    node_name: str
    message: str = Field(min_length=1)
    failed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NodeExecutionRecord(StrictBaseModel):
    schema_name: Literal["NodeExecutionRecord"] = "NodeExecutionRecord"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str
    node_call_id: str
    node_name: str
    revision: int = Field(ge=0)
    kind: Literal["deterministic", "llm"]
    status: Literal["completed", "failed"]
    input_hash: str
    output_hash: str | None = None
    started_at: datetime
    finished_at: datetime
    elapsed_ms: float = Field(ge=0)
    failure: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class LLMCallRecord(StrictBaseModel):
    schema_name: Literal["LLMCallRecord"] = "LLMCallRecord"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str
    llm_call_id: str
    node_call_id: str
    role: str
    revision: int = Field(ge=0)
    profile: str
    adapter: str | None = None
    provider: str | None = None
    configured_model: str | None = None
    observed_model: str | None = None
    started_at: datetime
    finished_at: datetime
    elapsed_ms: float = Field(ge=0)
    status: Literal["completed", "failed"]
    model_id: str | None = None
    input_hash: str
    output_hash: str | None = None
    system_prompt: str
    user_prompt: str
    system_prompt_sha256: str | None = None
    user_prompt_sha256: str | None = None
    parsed_output: dict[str, Any] | None = None
    raw_response: dict[str, Any] | None = None
    parsed_output_sha256: str | None = None
    raw_response_sha256: str | None = None
    system_prompt_chars: int = Field(ge=0)
    user_prompt_chars: int = Field(ge=0)
    output_chars: int | None = Field(default=None, ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    cache_read_input_tokens: int | None = Field(default=None, ge=0)
    cache_creation_input_tokens: int | None = Field(default=None, ge=0)
    ephemeral_5m_input_tokens: int | None = Field(default=None, ge=0)
    ephemeral_1h_input_tokens: int | None = Field(default=None, ge=0)
    reasoning_tokens: int | None = Field(default=None, ge=0)
    usage_status: Literal["complete", "partial", "unavailable"] = "unavailable"
    usage_sources: tuple[str, ...] = Field(default_factory=tuple)
    transport_attempts: tuple[dict[str, Any], ...] = Field(default_factory=tuple)
    failure: str | None = None


class DiscoverGraphState(TypedDict, total=False):
    run_identity: DiscoverRunIdentity
    frozen_inputs: FrozenDiscoverInputs
    requirement_set: RequirementSet
    requirement_coverage: RequirementCoverageProjection
    requirement_review: RequirementReview
    assertion_script: AssertionScript
    assertion_check_public: AssertionCheckPublic
    sealed_assertion_results: SealedAssertionReceipt
    assertion_review: AssertionReview
    released_assertion_results: ReleasedAssertionResults
    attribution_projection: AttributionProjection
    adjudication: DiscoverAdjudication
    coverage_gaps: tuple[CoverageGap, ...]
    #: One entry per stage that gave up on an obligation and continued anyway (CLAUDE.md §10).
    #: Distinct from `coverage_gaps`, which say *what* was not covered: this says *where the
    #: pipeline stopped trying*, so a reader of a landed artifact can tell a clean run from one
    #: that only looks clean because a stage abandoned its budget.  A cell with entries here is
    #: eligible for the measured set -- it produced an artifact -- but its zero-issue result
    #: cannot be read as "no defects found".
    _degraded_stages: tuple[str, ...]
    _adjudication_reconciliation: dict[str, Any]
    final_output: DiscoverCompleted
    failure: RunFailure
    node_execution_records: list[NodeExecutionRecord]
    llm_call_records: list[LLMCallRecord]
    requirement_fingerprints: tuple[str, ...]
    assertion_fingerprints: tuple[str, ...]
    _assertion_contract_failure_signatures: tuple[str, ...]
    _assertion_invalid_signatures: tuple[str, ...]
    _input: DiscoverInput
    _requirement_feedback: RevisionFeedback
    _requirement_revision_ledger: tuple[RevisionLedgerEvent, ...]
    _requirement_review_repair_count: int
    _requirement_contract_repair_count: int
    _requirement_split_contract_feedback: RevisionFeedback | None
    #: Newest RequirementSet that cleared the deterministic contract. Distinct from
    #: `requirement_set`, which on a contract violation holds the *rejected* artifact so
    #: the producer can revise it in place.
    _last_accepted_requirement_set: RequirementSet
    _assertion_feedback: RevisionFeedback | None
    _assertion_feedback_history: tuple[RevisionFeedback, ...]
    _assertion_revision_ledger: tuple[RevisionLedgerEvent, ...]
    _assertion_review_repair_count: int
    _assertion_conversion_contract_feedback: RevisionFeedback | None
    _assertion_contract_repair_count: int
    _assertion_no_progress_recovery_count: int
    # Item-local budgets (Issue #167 §8.3).  Keyed by assertion id and by
    # semantic failure identity respectively, so isolation can act per item
    # instead of per whole script.
    _assertion_item_repair_counts: dict[str, int]
    _assertion_invalid_semantic_counts: dict[str, int]
    _precheck_round_count: int
    _last_executable_assertion_script: AssertionScript
    _quarantined_assertion_ids: tuple[str, ...]
