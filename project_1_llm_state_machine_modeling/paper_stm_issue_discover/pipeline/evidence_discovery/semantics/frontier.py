"""Typed v27-style semantic frontier materialization.

The LLM establishes normative contracts and semantic transition groups.  This
module then expands those typed obligations against exact source, ModelIR, and
inspection-equivalent facts.  It never reads ledger data and never interprets
free text with keyword, regular-expression, or similarity rules.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from typing import Literal, Sequence

from pydantic import BaseModel, ConfigDict, Field

from ..inputs.context import (
    InspectionStateFact,
    SourceInventoryState,
    SourceInventoryTransition,
)
from ..inputs.models import PairInput, StateNode, Transition
from .binding import bind_candidate, resolve_state_ref
from .obligations import (
    CandidateIssue,
    ContractBindingHint,
    EvidenceType,
    ExpectedDirection,
    ObligationLocusKind,
    ObligationProperty,
    ViolationDirection,
)
from .workflow import (
    CardinalityDomainBinding,
    CardinalityRequirement,
    GroundingResponse,
    NLContract,
    NLContractResponse,
    NLTransitionGroup,
    SemanticBinding,
    StateSemanticRole,
)


FrontierKind = Literal[
    "containment",
    "cardinality",
    "owner_initial_entry",
    "root_reachability",
    "event_consumer_coverage",
    "stable_termination",
    "transition_group_collision",
    "wrong_target",
    "wrong_scope_route",
    "reachable_dead_end",
    "cross_wrapper_reachability",
]


class ContractSemanticKey(BaseModel):
    """确定一个规范义务身份的 typed key，由 contract/grounding 产生并由 runner 合并。

    该对象只表达义务身份，不表达模型是否满足义务，也不携带 W、D、L 或 judge
    信息。runner 使用其规范化 JSON 生成 derived contract 的权威 ID。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.contract-semantic-key.v2"] = Field(
        default="paper1.contract-semantic-key.v2",
        description="该 typed identity 的 schema 版本；用于 artifact 与 resume 审计，不参与语义裁定。",
    )
    segment_id: str = Field(
        pattern=r"^NL[0-9]+(?:\.[0-9]+)?$",
        description="义务所依据的编号 NL segment；它提供规范来源，但不等于 ledger 身份。",
    )
    locus_kind: ObligationLocusKind = Field(
        min_length=1,
        description="可被违反的领域 locus 类型；与 property 分离，不能用性质名冒充对象类型。",
    )
    locus_names: tuple[str, ...] = Field(
        min_length=1,
        description="LLM 已建立的精确语义 locus 名称序列；顺序属于 identity，不做文本相似度归并。",
    )
    property: ObligationProperty = Field(
        min_length=1,
        description="该义务唯一审查的原子性质；不同 property 即使共享原因也保持不同身份。",
    )
    state_role: StateSemanticRole | None = Field(
        default=None,
        description="NL 建立的状态角色；null 表示该义务不以一个状态角色为中心，不能由名称推断。",
    )
    expected_direction: ExpectedDirection = Field(
        min_length=1,
        description="规范侧正向要求；用于区分 must-enter、must-reach、must-progress 等邻近义务。",
    )
    violation_direction: ViolationDirection = Field(
        min_length=1,
        description="候选应审查的缺陷方向；missing、wrong-scope、unreachable 等不能互相覆盖。",
    )
    cardinality_requirement: CardinalityRequirement | None = Field(
        default=None,
        description="数量义务的规范 required count 与 typed member domain；非 cardinality identity 为 null，不能用自由文本补值。",
    )


class TransitionAlternativeSemanticKey(BaseModel):
    """一个 transition-group member 的 typed identity，不包含 provider 字符串 ID。"""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.transition-alternative-key.v1"] = Field(default="paper1.transition-alternative-key.v1", description="Alternative semantic key 的 schema 版本。")
    target_name: str = Field(min_length=1, description="LLM 已完成 discourse binding 的规范目标；顺序和精确值参与 identity。")
    condition: str | None = Field(default=None, min_length=1, description="完整规范条件；null 表示 typed unconditional alternative，不与空字符串等价。")
    condition_role: Literal["event", "qualified_guard", "unknown"] | None = Field(default=None, description="条件的 typed semantic role；null 仅用于无条件 alternative。")


class TransitionGroupSemanticKey(BaseModel):
    """runner 合并 base/grounding transition group 所使用的权威 typed identity。"""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.transition-group-key.v1"] = Field(default="paper1.transition-group-key.v1", description="Transition group semantic key 的 schema 版本。")
    segment_id: str = Field(pattern=r"^NL[0-9]+(?:\.[0-9]+)?$", description="建立该 relation 的精确 numbered NL segment。")
    source_name: str = Field(min_length=1, description="LLM discourse-resolved shared source；不得由 enclosing owner 自动替代。")
    alternatives: tuple[TransitionAlternativeSemanticKey, ...] = Field(min_length=1, description="有序完整 alternatives；目标、条件或顺序不同即为不同 relation。")


class IdentityNormalizationReceipt(BaseModel):
    """一条 grounding branch-local identity 的确定性规范化回执。

    runner 在 discovery-grounding 边界产生该对象，用 typed semantic key 替换
    LLM 自由生成的字符串 ID。它只证明引用改写和 provenance，不代表 frontier
    检查、模型满足性、W、D、L 或 judge 结论。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.identity-normalization.v3"] = Field(
        default="paper1.identity-normalization.v3",
        description="identity normalization receipt 的持久化 schema 版本。",
    )
    algorithm_version: Literal["typed-contract-identity.v3"] = Field(
        default="typed-contract-identity.v3",
        description="生成 canonical ID 和改写 branch-local 引用的确定性算法版本。",
    )
    lens: Literal["contract_structure_contrast", "behavior_consequence"] = Field(
        description="产生原始 additional contract 的 grounding lens；仅用于 provenance。",
    )
    raw_contract_id: str = Field(
        min_length=1,
        description="provider 返回的 branch-local ID；只留作审计，不能决定语义身份。",
    )
    canonical_contract_id: str = Field(
        min_length=1,
        description="runner 根据完整 ContractSemanticKey 生成的权威 derived contract ID。",
    )
    semantic_key: ContractSemanticKey = Field(
        description="用于 canonical ID 的完整 typed identity；不含满足、W、D 或 ledger 信息。",
    )
    rewritten_candidate_count: int = Field(
        ge=0,
        description="本 lens 中从 raw ID 精确改写到 canonical ID 的 candidate 引用数。",
    )
    projected_candidate_identity_count: int = Field(
        ge=0,
        description="本 lens 中按 referenced contract 权威 typed key 投影 locus/property/direction 的 candidate 数；raw provider payload 仍保留在调用审计中。",
    )
    rewritten_unresolved_count: int = Field(
        ge=0,
        description="本 lens 中从 raw ID 精确改写到 canonical ID 的 unresolved 引用数。",
    )
    rewritten_binding_count: int = Field(
        ge=0,
        description="本 lens 中从 raw ID 精确改写到 canonical ID 的 SemanticBinding 引用数。",
    )
    rewritten_cardinality_binding_count: int = Field(
        ge=0,
        description="本 lens 中从 raw ID 精确改写到 canonical ID 的 CardinalityDomainBinding 引用数。",
    )
    reason: str = Field(
        min_length=1,
        description="解释为何 runner 必须以 typed identity 取代 branch-local 字符串身份。",
    )
    basis: str = Field(
        min_length=1,
        description="列出 lens、raw/canonical ID 和 ContractSemanticKey 的可复核依据。",
    )


class GroupIdentityNormalizationReceipt(BaseModel):
    """一条 grounding branch-local transition group 的 runner canonicalization 回执。"""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.group-identity-normalization.v1"] = Field(default="paper1.group-identity-normalization.v1", description="Group identity normalization receipt 的 schema 版本。")
    algorithm_version: Literal["typed-transition-group-identity.v1"] = Field(default="typed-transition-group-identity.v1", description="canonical group/alternative IDs 的确定性算法版本。")
    lens: Literal["contract_structure_contrast", "behavior_consequence"] = Field(description="产生原始 additional group 的 grounding lens；仅用于 provenance。")
    raw_group_id: str = Field(min_length=1, description="provider 返回的 branch-local group ID；不再决定下游身份。")
    canonical_group_id: str = Field(min_length=1, description="runner 根据 TransitionGroupSemanticKey 生成的权威 group ID。")
    semantic_key: TransitionGroupSemanticKey = Field(description="生成 canonical group ID 的完整 typed relation identity。")
    alternative_id_map: dict[str, str] = Field(description="branch-local alternative ID 到 canonical ordered-member ID 的精确改写表；空值表示 group 无成员，结构上不允许。")
    reason: str = Field(min_length=1, description="解释为何 branch-local 字符串 identity 被 runner canonical identity 替换。")
    basis: str = Field(min_length=1, description="列出 lens、raw/canonical group IDs 和 typed semantic key。")


class FrontierCheckReceipt(BaseModel):
    """一个 v27 frontier 检查的确定性回执，由 execute-batch 产生并供审计消费。

    回执说明 typed obligation 与 exact facts 的展开结果。它不是 issue release，也不
    决定 D；candidate 状态只表示已形成一个待 D 裁定的精确主张。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.frontier-check.v1"] = Field(
        default="paper1.frontier-check.v1",
        description="frontier check receipt 的 schema 版本。",
    )
    algorithm_version: Literal["v27-typed-frontier.v5"] = Field(
        default="v27-typed-frontier.v5",
        description="产生该检查的确定性算法版本；不表示旧谓词或旧 inspect 后端。",
    )
    check_id: str = Field(
        min_length=1,
        description="由 frontier kind、typed contract identity 与 exact refs 计算的稳定检查 ID。",
    )
    kind: FrontierKind = Field(
        description="被系统化展开的领域前沿类型；它不是冻结谓词 ID。",
    )
    source_contract_ids: tuple[str, ...] = Field(
        min_length=1,
        description="建立该检查规范性的 base/derived contract IDs；不得包含 ledger ID。",
    )
    canonical_contract_id: str | None = Field(
        default=None,
        description="若检查形成 candidate，则为 runner 生成的权威 contract ID；否则为 null。",
    )
    status: Literal["candidate", "satisfied", "unresolved", "not_applicable"] = Field(
        description="确定性展开状态；candidate 仍需 D，satisfied 不发布，unresolved 不伪装成 miss。",
    )
    model_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="检查实际使用的 closed ModelIR refs；author-source refs 不得混入。",
    )
    source_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="检查使用的 NL/PlantUML/canonical source refs；这些只负责规范与来源定位。",
    )
    reason: str = Field(
        min_length=1,
        description="解释为何 typed obligation 与 exact facts 形成当前 frontier 状态。",
    )
    basis: str = Field(
        min_length=1,
        description="列出 contract key、ModelIR/inspection/source inventory 及算法版本等可复核依据。",
    )


class FrontierObligation(BaseModel):
    """由规范义务和 exact facts 共同触发的一个待裁定领域性质。

    runner 在 execute-batch 产生该对象，并把其中 candidate 交给冻结 19 谓词的
    compiler/backend。它不是新谓词，也没有权威 D/W/L 等级。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.frontier-obligation.v1"] = Field(
        default="paper1.frontier-obligation.v1",
        description="frontier obligation 持久化 schema 版本。",
    )
    frontier_id: str = Field(
        min_length=1,
        description="由 frontier kind、canonical contract 和 exact refs 生成的稳定 frontier identity。",
    )
    kind: FrontierKind = Field(
        description="领域候选前沿类型；下游仍只能选择冻结的 19 个 predicate 或 null/W1。",
    )
    source_contract_ids: tuple[str, ...] = Field(
        min_length=1,
        description="为该派生义务提供规范依据的 contract IDs；多个 ID 表示跨 contract 关系。",
    )
    contract: NLContract = Field(
        description="candidate 实际绑定的权威 typed contract；derived ID 由 runner 生成而非 LLM 决定。",
    )
    candidate: CandidateIssue = Field(
        description="一个 locus/property/scope 下的原子可证伪主张；不含 W、D、L。",
    )
    reason: str = Field(
        min_length=1,
        description="解释为何该领域义务需要从既有 contract 与 exact facts 中展开。",
    )
    basis: str = Field(
        min_length=1,
        description="列出 typed contract、source/model/inspection facts 和确定性展开规则。",
    )


class FrontierBatch(BaseModel):
    """一次 execute-batch 的完整 typed frontier 输出，供 runner 和 artifact 审计使用。"""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.frontier-batch.v1"] = Field(
        default="paper1.frontier-batch.v1",
        description="该批 frontier artifact 的 schema 版本。",
    )
    algorithm_version: Literal["v27-typed-frontier.v5"] = Field(
        default="v27-typed-frontier.v5",
        description="本批所有 check/obligation 使用的确定性算法版本。",
    )
    obligations: tuple[FrontierObligation, ...] = Field(
        default_factory=tuple,
        description="真正形成 candidate 的领域义务；每项仍需 compiler/backend、D 和 publish。",
    )
    checks: tuple[FrontierCheckReceipt, ...] = Field(
        default_factory=tuple,
        description="候选、满足和未决检查的完整回执，避免只保存发布结果。",
    )
    superseded_candidate_contract_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="已被 exact typed frontier 对同一 contract/property 完整展开所替代的 provisional LLM candidate contract IDs；raw grounding output 仍保留审计，下游只跳过其重复 D dossier。",
    )
    reason: str = Field(
        min_length=1,
        description="说明本批如何恢复 v27 frontier，同时保持新 19 谓词仅负责 W 证据。",
    )
    basis: str = Field(
        min_length=1,
        description="本批使用的 contract/group、ModelIR、source inventory 和 inspection fact 版本依据。",
    )


def contract_semantic_key(contract: NLContract) -> ContractSemanticKey:
    """Return the exact typed identity of one contract without interpreting prose."""

    return ContractSemanticKey(
        segment_id=contract.segment_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        state_role=contract.state_role,
        expected_direction=contract.expected_direction,
        violation_direction=contract.violation_direction,
        cardinality_requirement=contract.cardinality_requirement,
    )


def canonical_contract_id(contract: NLContract) -> str:
    """Generate the runner-authoritative derived ID from the typed semantic key."""

    payload = contract_semantic_key(contract).model_dump(mode="json")
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:20]
    return f"NL-CONTRACT-{contract.segment_id}-DERIVED-{digest}"


def transition_group_semantic_key(
    group: NLTransitionGroup,
) -> TransitionGroupSemanticKey:
    """Return one exact ordered group identity without interpreting prose."""

    return TransitionGroupSemanticKey(
        segment_id=group.segment_id,
        source_name=group.source_name,
        alternatives=tuple(
            TransitionAlternativeSemanticKey(
                target_name=item.target_name,
                condition=item.condition,
                condition_role=item.condition_role,
            )
            for item in group.alternatives
        ),
    )


def canonical_transition_group_id(group: NLTransitionGroup) -> str:
    """Generate a runner-authoritative ID for one typed transition relation."""

    payload = transition_group_semantic_key(group).model_dump(mode="json")
    digest = _hash_payload(payload)
    return f"NL-GROUP-{group.segment_id}-DERIVED-{digest}"


def _canonicalize_transition_group(
    group: NLTransitionGroup,
) -> tuple[NLTransitionGroup, dict[str, str]]:
    canonical_group_id = canonical_transition_group_id(group)
    alternatives = []
    alternative_id_map: dict[str, str] = {}
    for index, alternative in enumerate(group.alternatives, start=1):
        alternative_payload = TransitionAlternativeSemanticKey(
            target_name=alternative.target_name,
            condition=alternative.condition,
            condition_role=alternative.condition_role,
        ).model_dump(mode="json")
        canonical_alternative_id = (
            f"ALT-{index}-{_hash_payload([canonical_group_id, alternative_payload])}"
        )
        alternative_id_map[alternative.alternative_id] = canonical_alternative_id
        alternatives.append(
            alternative.model_copy(
                update={"alternative_id": canonical_alternative_id}
            )
        )
    return (
        group.model_copy(
            update={
                "group_id": canonical_group_id,
                "alternatives": tuple(alternatives),
            }
        ),
        alternative_id_map,
    )


def canonicalize_grounding_response(
    response: GroundingResponse,
) -> tuple[
    GroundingResponse,
    tuple[IdentityNormalizationReceipt | GroupIdentityNormalizationReceipt, ...],
]:
    """Replace LLM branch-local derived IDs with typed canonical identities.

    Raw provider output remains in the runtime audit.  This normalized response
    is the only branch payload admitted to downstream contract/candidate joins.
    """

    raw_to_canonical: dict[str, str] = {}
    contracts_by_id: dict[str, NLContract] = {}
    receipts: list[
        IdentityNormalizationReceipt | GroupIdentityNormalizationReceipt
    ] = []
    for contract in response.additional_contracts:
        canonical_id = canonical_contract_id(contract)
        raw_to_canonical[contract.contract_id] = canonical_id
        canonical = contract.model_copy(update={"contract_id": canonical_id})
        contracts_by_id.setdefault(canonical_id, canonical)
        receipts.append(
            IdentityNormalizationReceipt(
                lens=response.lens,
                raw_contract_id=contract.contract_id,
                canonical_contract_id=canonical_id,
                semantic_key=contract_semantic_key(contract),
                rewritten_candidate_count=sum(
                    candidate.contract_id == contract.contract_id
                    for candidate in response.candidates
                ),
                projected_candidate_identity_count=sum(
                    candidate.contract_id == contract.contract_id
                    for candidate in response.candidates
                ),
                rewritten_unresolved_count=sum(
                    item.contract_id == contract.contract_id
                    for item in response.unresolved
                ),
                rewritten_binding_count=sum(
                    item.contract_id == contract.contract_id
                    for item in response.semantic_bindings
                ),
                rewritten_cardinality_binding_count=sum(
                    item.contract_id == contract.contract_id
                    for item in response.cardinality_bindings
                ),
                reason="The runner replaced a branch-local derived identifier and projected referenced candidates onto the contract-authoritative typed semantic identity.",
                basis=f"lens={response.lens}; semantic_key={contract_semantic_key(contract).model_dump(mode='json')}",
            )
        )

    candidates = []
    contracts_by_raw_id = {
        raw_id: contracts_by_id[canonical_id]
        for raw_id, canonical_id in raw_to_canonical.items()
    }
    for candidate in response.candidates:
        contract = contracts_by_raw_id.get(candidate.contract_id)
        update: dict[str, object] = {
            "contract_id": raw_to_canonical.get(
                candidate.contract_id, candidate.contract_id
            )
        }
        if contract is not None:
            update.update(
                {
                    "locus_kind": contract.locus_kind,
                    "locus_names": contract.locus_names,
                    "property": contract.property,
                    "violation_direction": contract.violation_direction,
                    "evidence_types": contract.evidence_types,
                }
            )
        candidates.append(candidate.model_copy(update=update))
    unresolved = [
        item.model_copy(
            update={"contract_id": raw_to_canonical.get(item.contract_id, item.contract_id)}
        )
        for item in response.unresolved
    ]
    semantic_bindings = [
        item.model_copy(
            update={"contract_id": raw_to_canonical.get(item.contract_id, item.contract_id)}
        )
        for item in response.semantic_bindings
    ]
    cardinality_bindings = [
        item.model_copy(
            update={"contract_id": raw_to_canonical.get(item.contract_id, item.contract_id)}
        )
        for item in response.cardinality_bindings
    ]
    groups_by_id: dict[str, NLTransitionGroup] = {}
    for group in response.additional_transition_groups:
        canonical_group, alternative_id_map = _canonicalize_transition_group(group)
        groups_by_id.setdefault(canonical_group.group_id, canonical_group)
        receipts.append(
            GroupIdentityNormalizationReceipt(
                lens=response.lens,
                raw_group_id=group.group_id,
                canonical_group_id=canonical_group.group_id,
                semantic_key=transition_group_semantic_key(group),
                alternative_id_map=alternative_id_map,
                reason="The runner replaced branch-local transition-group and alternative IDs with one typed ordered relation identity.",
                basis=f"lens={response.lens}; semantic_key={transition_group_semantic_key(group).model_dump(mode='json')}",
            )
        )
    normalized = response.model_copy(
        update={
            "additional_contracts": list(contracts_by_id.values()),
            "additional_transition_groups": list(groups_by_id.values()),
            "candidates": candidates,
            "unresolved": unresolved,
            "semantic_bindings": semantic_bindings,
            "cardinality_bindings": cardinality_bindings,
        }
    )
    return normalized, tuple(receipts)


def _hash_payload(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:20]


def _hint(contract: NLContract, *roles: str) -> ContractBindingHint | None:
    matches = [item for item in contract.binding_hints if item.role in roles]
    return matches[0] if len(matches) == 1 else None


def _state_by_ref(pair: PairInput, ref: str | None) -> StateNode | None:
    return next((item for item in pair.model.states if item.ref == ref), None)


def _state_for_value(pair: PairInput, value: str | None) -> StateNode | None:
    return _state_by_ref(pair, resolve_state_ref(value, pair.model) if value else None)


def _state_by_name(pair: PairInput, name: str | None) -> StateNode | None:
    if not name:
        return None
    matches = [item for item in pair.model.states if item.name == name]
    return matches[0] if len(matches) == 1 else None


def _source_state_by_name(
    pair: PairInput, name: str | None
) -> SourceInventoryState | None:
    if not name or pair.exact_source_inventory is None:
        return None
    matches = [
        item for item in pair.exact_source_inventory.states if item.name == name
    ]
    return matches[0] if len(matches) == 1 else None


def _source_state_by_id(
    pair: PairInput, source_id: str | None
) -> SourceInventoryState | None:
    if not source_id or pair.exact_source_inventory is None:
        return None
    matches = [
        item
        for item in pair.exact_source_inventory.states
        if item.source_id == source_id
    ]
    return matches[0] if len(matches) == 1 else None


def _source_direct_children(
    pair: PairInput, owner: SourceInventoryState
) -> list[SourceInventoryState]:
    if pair.exact_source_inventory is None:
        return []
    return [
        item
        for item in pair.exact_source_inventory.states
        if item.parent == owner.source_id
    ]


def _source_initial_transitions(
    pair: PairInput, owner: SourceInventoryState
) -> list[SourceInventoryTransition]:
    if pair.exact_source_inventory is None:
        return []
    initial_source = f"@initial:{owner.source_id}"
    return [
        item
        for item in pair.exact_source_inventory.transitions
        if item.source == initial_source
    ]


def _inspection_state(pair: PairInput, ref: str) -> InspectionStateFact | None:
    facts = pair.inspection_facts
    return next((item for item in facts.states if item.state_ref == ref), None) if facts else None


def _machine_root(pair: PairInput) -> StateNode | None:
    if pair.inspection_facts and pair.inspection_facts.machine_root_ref:
        return _state_by_ref(pair, pair.inspection_facts.machine_root_ref)
    roots = [item for item in pair.model.states if item.parent is None]
    return roots[0] if len(roots) == 1 else None


def _ancestor_chain(pair: PairInput, state: StateNode) -> list[StateNode]:
    chain = [state]
    cursor = state
    seen = {state.ref}
    while cursor.parent:
        parent = _state_by_name(pair, cursor.parent)
        if parent is None or parent.ref in seen:
            break
        chain.append(parent)
        seen.add(parent.ref)
        cursor = parent
    return chain


def _is_descendant(pair: PairInput, child: StateNode, owner: StateNode) -> bool:
    return owner.ref in {item.ref for item in _ancestor_chain(pair, child)[1:]}


def _highest_unreachable_scope(pair: PairInput, state: StateNode) -> StateNode | None:
    root = _machine_root(pair)
    candidates = []
    for item in _ancestor_chain(pair, state):
        fact = _inspection_state(pair, item.ref)
        if (
            fact
            and fact.is_composite
            and not fact.reachable_from_initial
            and (root is None or item.ref != root.ref)
        ):
            candidates.append(item)
    return candidates[-1] if candidates else None


def _direct_child_under(pair: PairInput, descendant: StateNode, owner: StateNode) -> StateNode | None:
    chain = _ancestor_chain(pair, descendant)
    for index, item in enumerate(chain):
        if item.ref == owner.ref:
            return chain[index - 1] if index > 0 else None
    return None


def _initial_transitions(pair: PairInput, owner: StateNode | None) -> list[Transition]:
    root = _machine_root(pair)
    if owner is None:
        scopes = {None, root.name if root else None}
    else:
        scopes = {owner.name}
    return [
        item
        for item in pair.model.transitions
        if item.source.replace("[ * ]", "[*]") == "[*]" and item.scope in scopes
    ]


def _transition_target_ref(pair: PairInput, transition: Transition) -> str | None:
    if pair.inspection_facts:
        row = next(
            (
                item
                for item in pair.inspection_facts.transitions
                if item.transition_ref == transition.ref
            ),
            None,
        )
        if row:
            return row.resolved_target_ref
    target = _state_for_value(pair, transition.target)
    return target.ref if target else None


def _source_refs(contracts: Sequence[NLContract]) -> list[str]:
    return list(dict.fromkeys(ref for contract in contracts for ref in contract.source_refs))


def _derived_contract(
    base: NLContract,
    *,
    locus_kind: ObligationLocusKind,
    locus_names: Sequence[str],
    property_name: ObligationProperty,
    state_role: StateSemanticRole | None,
    expected_direction: ExpectedDirection,
    violation_direction: ViolationDirection,
    evidence_types: Sequence[EvidenceType],
    normative_statement: str,
    scope: str,
    source_refs: Sequence[str],
    reason: str,
    basis: str,
    cardinality_requirement: CardinalityRequirement | None = None,
) -> NLContract:
    contract = NLContract(
        contract_id=f"NL-CONTRACT-{base.segment_id}-DERIVED-PENDING",
        segment_id=base.segment_id,
        quote=base.quote,
        normative_statement=normative_statement,
        locus_kind=locus_kind,
        locus_names=tuple(locus_names),
        property=property_name,
        state_role=state_role,
        expected_direction=expected_direction,
        violation_direction=violation_direction,
        evidence_types=tuple(dict.fromkeys(evidence_types)),
        binding_hints=base.binding_hints,
        cardinality_requirement=cardinality_requirement,
        scope=scope,
        source_refs=tuple(dict.fromkeys(source_refs)),
        reason=reason,
        basis=basis,
    )
    return contract.model_copy(update={"contract_id": canonical_contract_id(contract)})


def _candidate(
    contract: NLContract,
    *,
    title: str,
    predicate_id: str | None,
    predicate_inputs: dict[str, object],
    element_refs: Sequence[str],
    source_refs: Sequence[str],
    expected: str,
    observed: str,
    strongest_rebuttal: str,
    reason: str,
    basis: str,
) -> CandidateIssue:
    return CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title=title,
        requirement_quote=contract.quote,
        predicate_id=predicate_id,
        predicate_inputs=predicate_inputs,
        element_refs=list(dict.fromkeys(element_refs)),
        source_refs=list(dict.fromkeys(source_refs)),
        expected=expected,
        observed=observed,
        strongest_rebuttal=strongest_rebuttal,
        reason=reason,
        basis=basis,
    )


class _Builder:
    def __init__(self, pair: PairInput, existing: Sequence[CandidateIssue]) -> None:
        self.pair = pair
        self.obligations: list[FrontierObligation] = []
        self.checks: list[FrontierCheckReceipt] = []
        self.seen = {
            contract_semantic_key_from_candidate(candidate)
            for candidate in existing
        }
        self.obligation_index: dict[tuple[object, ...], int] = {}
        self.superseded_candidate_contract_ids: list[str] = []

    def add(
        self,
        kind: FrontierKind,
        source_contract_ids: Sequence[str],
        contract: NLContract,
        candidate: CandidateIssue,
        *,
        reason: str,
        basis: str,
    ) -> None:
        identity = contract_semantic_key_from_candidate(candidate)
        if identity in self.seen:
            existing_index = self.obligation_index.get(identity)
            if existing_index is not None:
                existing = self.obligations[existing_index]
                merged_candidate = existing.candidate.model_copy(
                    update={
                        "element_refs": list(
                            dict.fromkeys(
                                [*existing.candidate.element_refs, *candidate.element_refs]
                            )
                        ),
                        "source_refs": list(
                            dict.fromkeys(
                                [*existing.candidate.source_refs, *candidate.source_refs]
                            )
                        ),
                        "basis": (
                            f"{existing.candidate.basis}; supporting_contract_ids="
                            f"{list(dict.fromkeys([*existing.source_contract_ids, *source_contract_ids]))}"
                        ),
                    }
                )
                self.obligations[existing_index] = existing.model_copy(
                    update={
                        "source_contract_ids": tuple(
                            dict.fromkeys(
                                [*existing.source_contract_ids, *source_contract_ids]
                            )
                        ),
                        "candidate": merged_candidate,
                        "basis": (
                            f"{existing.basis}; merged duplicate typed frontier "
                            f"from {list(source_contract_ids)}"
                        ),
                    }
                )
            self.checks.append(
                self.receipt(
                    kind,
                    source_contract_ids,
                    status="not_applicable",
                    contract=contract,
                    model_refs=candidate.element_refs,
                    source_refs=candidate.source_refs,
                    reason="An existing candidate or frontier obligation already carries this exact typed semantic identity.",
                    basis="typed locus kind, locus names, property, and violation direction equality; duplicate refs remain supporting evidence",
                )
            )
            return
        self.seen.add(identity)
        frontier_id = f"frontier:{kind}:{_hash_payload([contract.contract_id, candidate.element_refs])}"
        obligation = FrontierObligation(
            frontier_id=frontier_id,
            kind=kind,
            source_contract_ids=tuple(source_contract_ids),
            contract=contract,
            candidate=candidate,
            reason=reason,
            basis=basis,
        )
        self.obligations.append(obligation)
        self.obligation_index[identity] = len(self.obligations) - 1
        self.checks.append(
            self.receipt(
                kind,
                source_contract_ids,
                status="candidate",
                contract=contract,
                model_refs=candidate.element_refs,
                source_refs=candidate.source_refs,
                reason=reason,
                basis=basis,
            )
        )

    def receipt(
        self,
        kind: FrontierKind,
        source_contract_ids: Sequence[str],
        *,
        status: Literal["candidate", "satisfied", "unresolved", "not_applicable"],
        contract: NLContract | None = None,
        model_refs: Sequence[str] = (),
        source_refs: Sequence[str] = (),
        reason: str,
        basis: str,
    ) -> FrontierCheckReceipt:
        return FrontierCheckReceipt(
            check_id=f"frontier-check:{kind}:{_hash_payload([list(source_contract_ids), list(model_refs), status])}",
            kind=kind,
            source_contract_ids=tuple(source_contract_ids),
            canonical_contract_id=contract.contract_id if contract else None,
            status=status,
            model_refs=tuple(dict.fromkeys(model_refs)),
            source_refs=tuple(dict.fromkeys(source_refs)),
            reason=reason,
            basis=basis,
        )


def contract_semantic_key_from_candidate(candidate: CandidateIssue) -> tuple[object, ...]:
    return (
        candidate.locus_kind,
        candidate.locus_names,
        candidate.property,
        candidate.violation_direction,
    )


def _materialize_containment(builder: _Builder, contracts: Sequence[NLContract]) -> None:
    pair = builder.pair
    for contract in contracts:
        if contract.property != "containment":
            continue
        owner = _state_for_value(pair, (_hint(contract, "owner") or _hint(contract, "scope")).value if (_hint(contract, "owner") or _hint(contract, "scope")) else None)
        child_hint = _hint(contract, "target") or _hint(contract, "state")
        child = _state_for_value(pair, child_hint.value if child_hint else None)
        if owner is None or child is None:
            builder.checks.append(
                builder.receipt(
                    "containment",
                    (contract.contract_id,),
                    status="unresolved",
                    source_refs=contract.source_refs,
                    reason="The typed owner or child does not resolve to one exact closed-model state.",
                    basis="contract binding_hints and exact ModelIR state identity",
                )
            )
            continue
        if _is_descendant(pair, child, owner):
            builder.checks.append(
                builder.receipt(
                    "containment",
                    (contract.contract_id,),
                    status="satisfied",
                    contract=contract,
                    model_refs=(owner.ref, child.ref),
                    source_refs=contract.source_refs,
                    reason="The exact child ancestry contains the required owner.",
                    basis="owned ModelIR parent chain",
                )
            )
            continue
        actual_chain = [item.name for item in _ancestor_chain(pair, child)]
        candidate = _candidate(
            contract,
            title=f"{child.name} is outside required owner {owner.name}",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(child.ref, owner.ref),
            source_refs=contract.source_refs,
            expected=contract.normative_statement,
            observed=f"The exact closed-model ancestry of {child.name} is {actual_chain}, which does not include {owner.name}.",
            strongest_rebuttal="A transition between the two states would not establish the required containment relation.",
            reason="The LLM-established containment contract binds both states exactly, and the complete parent chain refutes the required owner relation.",
            basis=f"contract={contract.contract_id}; child_ref={child.ref}; owner_ref={owner.ref}; model={pair.model.algorithm_version}",
        )
        builder.add(
            "containment",
            (contract.contract_id,),
            contract,
            candidate,
            reason="A typed containment obligation is refuted by the exact ModelIR parent chain.",
            basis="contract binding hints plus complete owned hierarchy",
        )


def _materialize_cardinality(
    builder: _Builder,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
    existing: Sequence[CandidateIssue],
) -> None:
    pair = builder.pair
    for contract in contracts:
        if contract.property != "cardinality":
            continue
        requirement = contract.cardinality_requirement
        if requirement is None:
            builder.checks.append(
                builder.receipt(
                    "cardinality",
                    (contract.contract_id,),
                    status="unresolved",
                    source_refs=contract.source_refs,
                    reason="The cardinality contract has no typed required count and member domain, so free text is not parsed to manufacture them.",
                    basis="NLContract.cardinality_requirement is null",
                )
            )
            continue

        binding_rows = [
            binding
            for response in grounding_responses
            for binding in response.cardinality_bindings
            if binding.contract_id == contract.contract_id
        ]
        exact_bindings = [
            binding for binding in binding_rows if binding.status == "exact"
        ]
        exact_binding_keys = {
            (
                binding.member_domain,
                binding.owner_source_id,
                binding.owner_model_ref,
            )
            for binding in exact_bindings
        }
        selected_binding: CardinalityDomainBinding | None = None
        effective_requirement = requirement
        if requirement.member_domain == "unresolved":
            if not exact_bindings:
                builder.checks.append(
                    builder.receipt(
                        "cardinality",
                        (contract.contract_id,),
                        status="unresolved",
                        source_refs=contract.source_refs,
                        reason="No grounding lens selected one exact primary cardinality member domain and owner.",
                        basis=(
                            "member_domain=unresolved; cardinality_binding_statuses="
                            f"{[item.status for item in binding_rows]}; no free-text or name-shape fallback is permitted"
                        ),
                    )
                )
                continue
            if len(exact_binding_keys) != 1:
                builder.checks.append(
                    builder.receipt(
                        "cardinality",
                        (contract.contract_id,),
                        status="unresolved",
                        source_refs=contract.source_refs,
                        reason="The grounding lenses selected conflicting exact cardinality domains or owners, so the frontier cannot choose one by branch order.",
                        basis=f"exact_binding_keys={sorted(exact_binding_keys)}",
                    )
                )
                continue
            selected_binding = exact_bindings[0]
            effective_requirement = requirement.model_copy(
                update={
                    "member_domain": selected_binding.member_domain,
                    "alternative_reading": (
                        selected_binding.alternative_reading
                        or requirement.alternative_reading
                    ),
                    "reason": "Grounding selected one primary typed member domain from supplied NL/source semantics while retaining any competing competent reading for D.",
                    "basis": "numbered NL CardinalityRequirement plus exact CardinalityDomainBinding; observed count was not used to choose the domain",
                }
            )
        else:
            agreeing_bindings = [
                binding
                for binding in exact_bindings
                if binding.member_domain == requirement.member_domain
            ]
            agreeing_keys = {
                (binding.owner_source_id, binding.owner_model_ref)
                for binding in agreeing_bindings
            }
            if agreeing_bindings and len(agreeing_keys) != 1:
                builder.checks.append(
                    builder.receipt(
                        "cardinality",
                        (contract.contract_id,),
                        status="unresolved",
                        source_refs=contract.source_refs,
                        reason="The grounding lenses disagree about the exact owner of the contract-selected cardinality domain.",
                        basis=f"member_domain={requirement.member_domain}; agreeing_owner_keys={sorted(agreeing_keys)}",
                    )
                )
                continue
            if len(agreeing_keys) == 1:
                selected_binding = agreeing_bindings[0]
                if (
                    effective_requirement.alternative_reading is None
                    and selected_binding.alternative_reading is not None
                ):
                    effective_requirement = requirement.model_copy(
                        update={
                            "alternative_reading": selected_binding.alternative_reading
                        }
                    )

        if effective_requirement.member_domain != "direct_child_states":
            builder.checks.append(
                builder.receipt(
                    "cardinality",
                    (contract.contract_id,),
                    status="unresolved",
                    source_refs=contract.source_refs,
                    reason="This frontier currently has no exact inventory projection for the contract's selected member domain.",
                    basis=f"member_domain={effective_requirement.member_domain}; no free-text or name-shape fallback is permitted",
                )
            )
            continue

        if selected_binding is not None:
            bound_owner = _state_by_ref(pair, selected_binding.owner_model_ref)
            source_owner = _source_state_by_id(
                pair, selected_binding.owner_source_id
            )
            owner_rows = (
                [
                    (
                        bound_owner,
                        source_owner,
                        _source_direct_children(pair, source_owner),
                    )
                ]
                if bound_owner is not None and source_owner is not None
                else []
            )
            bound_states = [bound_owner] if bound_owner is not None else []
        else:
            bound_states = _contract_state_refs(pair, contract)
            for candidate in existing:
                if (
                    candidate.contract_id == contract.contract_id
                    and candidate.property == "cardinality"
                ):
                    bound_states.extend(_candidate_state_refs(pair, candidate))
            bound_states = list({item.ref: item for item in bound_states}.values())

            structural_owner_rows: list[
                tuple[StateNode, SourceInventoryState, list[SourceInventoryState]]
            ] = []
            bound_source_ids = {
                source_state.source_id
                for state in bound_states
                if (source_state := _source_state_by_name(pair, state.name))
                is not None
            }
            for state in bound_states:
                source_owner = _source_state_by_name(pair, state.name)
                if source_owner is None:
                    continue
                children = _source_direct_children(pair, source_owner)
                if children:
                    structural_owner_rows.append((state, source_owner, children))
            linked_owner_rows = [
                row
                for row in structural_owner_rows
                if any(child.source_id in bound_source_ids for child in row[2])
            ]
            owner_rows = (
                linked_owner_rows
                if linked_owner_rows
                else structural_owner_rows
                if len(structural_owner_rows) == 1
                else []
            )
        if len(owner_rows) != 1:
            builder.checks.append(
                builder.receipt(
                    "cardinality",
                    (contract.contract_id,),
                    status="unresolved",
                    model_refs=[item.ref for item in bound_states],
                    source_refs=contract.source_refs,
                    reason="The typed binding does not identify one exact source/model owner for the complete direct-child member domain.",
                    basis=(
                        f"owner_candidate_count={len(owner_rows)}; "
                        f"cardinality_binding_id={selected_binding.binding_id if selected_binding else None}; "
                        "exact source parent relations only"
                    ),
                )
            )
            continue

        owner, source_owner, members = owner_rows[0]
        actual_count = len(members)
        source_refs = tuple(
            dict.fromkeys(
                [
                    *contract.source_refs,
                    source_owner.raw_ref,
                    *[member.raw_ref for member in members],
                ]
            )
        )
        model_members = [
            state
            for member in members
            if (state := _state_by_name(pair, member.name)) is not None
        ]
        model_refs = [owner.ref, *[item.ref for item in model_members]]
        if actual_count == effective_requirement.required_count:
            builder.checks.append(
                builder.receipt(
                    "cardinality",
                    (contract.contract_id,),
                    status="satisfied",
                    contract=contract,
                    model_refs=model_refs,
                    source_refs=source_refs,
                    reason="The complete exact author-source direct-child inventory has the required finite cardinality.",
                    basis=f"owner={source_owner.source_id}; required={effective_requirement.required_count}; actual={actual_count}; members={[item.source_id for item in members]}",
                )
            )
            continue

        derived = _derived_contract(
            contract,
            locus_kind="composite",
            locus_names=(owner.name,),
            property_name="cardinality",
            state_role=contract.state_role,
            expected_direction="must_cover",
            violation_direction="missing",
            evidence_types=("source_identity", "closed_model_inventory", "containment_fact", "semantic_comparison"),
            normative_statement=(
                f"{owner.name} must contain {effective_requirement.required_count} "
                f"{effective_requirement.member_concept} as direct child states."
            ),
            scope=f"Direct authored children of {owner.name}",
            source_refs=source_refs,
            reason="The NL contract establishes a finite direct-child member-domain reading whose count can be compared with the complete exact source inventory.",
            basis="typed CardinalityRequirement plus exact source parent/member rows",
            cardinality_requirement=effective_requirement,
        )
        candidate = _candidate(
            derived,
            title=f"{owner.name} has {actual_count}, not {effective_requirement.required_count}, direct state areas",
            predicate_id=None,
            predicate_inputs={},
            element_refs=model_refs,
            source_refs=source_refs,
            expected=derived.normative_statement,
            observed=(
                f"The complete exact author-source inventory contains {actual_count} "
                f"direct children under {source_owner.source_id}: "
                f"{[item.source_id for item in members]}."
            ),
            strongest_rebuttal=(
                effective_requirement.alternative_reading
                or "No competing member-domain reading is recorded in the supplied cardinality contract."
            ),
            reason="The required count and direct-child member domain are typed, and the complete source inventory establishes a different finite count.",
            basis=(
                f"contract={contract.contract_id}; owner={source_owner.source_id}; "
                f"required={effective_requirement.required_count}; actual={actual_count}; "
                f"cardinality_binding_id={selected_binding.binding_id if selected_binding else None}"
            ),
        )
        builder.add(
            "cardinality",
            (contract.contract_id,),
            derived,
            candidate,
            reason="A typed finite cardinality requirement differs from the complete exact source member inventory.",
            basis="CardinalityRequirement and canonical source direct-parent inventory",
        )
        if contract.contract_id not in builder.superseded_candidate_contract_ids:
            builder.superseded_candidate_contract_ids.append(contract.contract_id)


def _materialize_initial_entries(builder: _Builder, contracts: Sequence[NLContract]) -> None:
    pair = builder.pair
    for contract in contracts:
        if contract.property != "initial_entry":
            continue
        target_hint = _hint(contract, "target") or _hint(contract, "state")
        owner_hint = _hint(contract, "owner") or _hint(contract, "scope")
        target = _state_for_value(pair, target_hint.value if target_hint else None)
        owner = _state_for_value(pair, owner_hint.value if owner_hint else None)
        owner_is_root = contract.locus_kind == "model"
        if target is None or (owner is None and not owner_is_root):
            builder.checks.append(
                builder.receipt(
                    "owner_initial_entry",
                    (contract.contract_id,),
                    status="unresolved",
                    source_refs=contract.source_refs,
                    reason="The typed initial-entry target or owner does not resolve exactly.",
                    basis="contract owner/target binding hints and ModelIR identity",
                )
            )
            continue
        initial = _initial_transitions(pair, owner)
        matching = [item for item in initial if _transition_target_ref(pair, item) == target.ref]
        unconditional = [item for item in matching if not item.triggers and not item.guard]
        refs = [target.ref]
        if owner:
            refs.append(owner.ref)
        refs.extend(item.ref for item in initial)
        refs.extend(ref for item in initial if (ref := _transition_target_ref(pair, item)))
        if unconditional:
            builder.checks.append(
                builder.receipt(
                    "owner_initial_entry",
                    (contract.contract_id,),
                    status="satisfied",
                    contract=contract,
                    model_refs=refs,
                    source_refs=contract.source_refs,
                    reason="An unconditional initial pseudostate edge enters the exact required target in the required owner scope.",
                    basis="owned scoped transition inventory",
                )
            )
            continue
        observed_targets = [item.target for item in initial]
        normalized_contract = _derived_contract(
            contract,
            locus_kind="model" if owner_is_root else "composite",
            locus_names=(target.name,) if owner_is_root else (owner.name, target.name),
            property_name="initial_entry",
            state_role=contract.state_role,
            expected_direction="must_enter",
            violation_direction="missing",
            evidence_types=contract.evidence_types,
            normative_statement=contract.normative_statement,
            scope=contract.scope,
            source_refs=contract.source_refs,
            reason="The deterministic frontier normalizes owner-level missing-edge and wrong-current-target observations to one exact required default-entry obligation.",
            basis="typed owner/target binding and complete owner-local initial-transition inventory",
        )
        candidate = _candidate(
            normalized_contract,
            title=f"{owner.name if owner else 'Model'} lacks default entry to {target.name}",
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=contract.source_refs,
            expected=contract.normative_statement,
            observed=(
                f"The exact owner-local initial transitions target {observed_targets}; "
                f"matching edges to {target.name} are conditional={bool(matching)}."
            ),
            strongest_rebuttal="A child-region initial edge or a guarded routing edge does not satisfy this exact owner-local default-entry contract.",
            reason="The typed owner and target resolve exactly, but no unconditional owner-local initial edge enters the required target.",
            basis=f"contract={contract.contract_id}; target_ref={target.ref}; owner_ref={owner.ref if owner else 'root'}; initial_refs={[item.ref for item in initial]}",
        )
        builder.add(
            "owner_initial_entry",
            (contract.contract_id,),
            normalized_contract,
            candidate,
            reason="The exact scoped initial-transition inventory refutes the typed default-entry obligation.",
            basis="typed owner/target binding and owned ModelIR initial edges",
        )


def _candidate_state_refs(pair: PairInput, candidate: CandidateIssue) -> list[StateNode]:
    binding = bind_candidate(candidate, pair.model)
    return [item for item in pair.model.states if item.ref in binding.element_refs]


def _contract_state_refs(pair: PairInput, contract: NLContract) -> list[StateNode]:
    states: list[StateNode] = []
    for hint in contract.binding_hints:
        if hint.role not in {"owner", "scope", "source", "target", "state"}:
            continue
        state = _state_for_value(pair, hint.value)
        if state and state.ref not in {item.ref for item in states}:
            states.append(state)
    return states


def _materialize_root_reachability(
    builder: _Builder,
    contracts: Sequence[NLContract],
    existing: Sequence[CandidateIssue],
) -> dict[str, tuple[StateNode, StateNode, NLContract]]:
    pair = builder.pair
    relevant_by_contract: dict[str, list[StateNode]] = {
        contract.contract_id: _contract_state_refs(pair, contract) for contract in contracts
    }
    for candidate in existing:
        relevant_by_contract.setdefault(candidate.contract_id, []).extend(
            _candidate_state_refs(pair, candidate)
        )
    groups: dict[str, list[tuple[NLContract, StateNode]]] = defaultdict(list)
    contracts_by_id = {item.contract_id: item for item in contracts}
    for contract_id, states in relevant_by_contract.items():
        contract = contracts_by_id.get(contract_id)
        if contract is None or contract.state_role not in {"operating_state", "initial_state"}:
            continue
        for state in states:
            fact = _inspection_state(pair, state.ref)
            if fact is None or fact.reachable_from_initial:
                continue
            scope = _highest_unreachable_scope(pair, state)
            if scope:
                groups[scope.ref].append((contract, state))

    scopes: dict[str, tuple[StateNode, StateNode, NLContract]] = {}
    for scope_ref, rows in groups.items():
        scope = _state_by_ref(pair, scope_ref)
        if scope is None:
            continue
        descendant_rows = [
            row
            for row in rows
            if row[1].ref != scope.ref and _is_descendant(pair, row[1], scope)
        ]
        base, descendant = descendant_rows[0] if descendant_rows else rows[0]
        scopes[scope_ref] = (scope, descendant, base)
        derived = _derived_contract(
            base,
            locus_kind="scope",
            locus_names=(scope.name,),
            property_name="reachability",
            state_role="operating_state",
            expected_direction="must_reach",
            violation_direction="unreachable",
            evidence_types=("source_identity", "closed_model_inventory", "reachability_fact", "verify_fact"),
            normative_statement=f"The required operating scope {scope.name} must be reachable from the model root.",
            scope=f"Root reachability of {scope.name}",
            source_refs=_source_refs([row[0] for row in rows]),
            reason="Typed operating contracts bind behavior inside this exact scope, so root reachability is a causal prerequisite rather than a new textual obligation.",
            basis="contract state roles, exact ancestor chain, and inspection-equivalent reachability facts",
        )
        supporting_refs = [scope.ref]
        supporting_refs.extend(row[1].ref for row in rows)
        candidate = _candidate(
            derived,
            title=f"Required operating scope {scope.name} is unreachable from root",
            predicate_id="G1",
            predicate_inputs={"source": "[*]", "target": scope.name},
            element_refs=supporting_refs,
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=f"The exact inspection-equivalent facts mark {scope.ref} and its bound required behavior as unreachable from the top-level initial entry.",
            strongest_rebuttal="Owner-local declarations or transitions do not establish a path from the model root.",
            reason="At least one LLM-established operating obligation is bound below this exact composite, while finite root reachability excludes the composite.",
            basis=f"scope_ref={scope.ref}; supporting_contracts={[row[0].contract_id for row in rows]}; inspection={pair.inspection_facts.algorithm_version if pair.inspection_facts else 'unavailable'}",
        )
        builder.add(
            "root_reachability",
            tuple(dict.fromkeys(row[0].contract_id for row in rows)),
            derived,
            candidate,
            reason="A required operating scope is excluded from finite root reachability.",
            basis="typed operating contracts plus exact ancestor and reachability facts",
        )
    return scopes


def _materialize_scope_entries(
    builder: _Builder,
    scopes: dict[str, tuple[StateNode, StateNode, NLContract]],
) -> None:
    pair = builder.pair
    for scope, descendant, base in scopes.values():
        target = _direct_child_under(pair, descendant, scope)
        if target is None:
            continue
        source_scope = _source_state_by_name(pair, scope.name)
        source_target = _source_state_by_name(pair, target.name)
        source_children = (
            _source_direct_children(pair, source_scope) if source_scope else []
        )
        source_initial = (
            _source_initial_transitions(pair, source_scope) if source_scope else []
        )
        if (
            source_scope is None
            or source_target is None
            or source_target.parent != source_scope.source_id
            or len(source_children) < 2
        ):
            continue
        if any(item.target == source_target.source_id for item in source_initial):
            continue
        initial = _initial_transitions(pair, scope)
        derived = _derived_contract(
            base,
            locus_kind="composite",
            locus_names=(scope.name, target.name),
            property_name="initial_entry",
            state_role="operating_state",
            expected_direction="must_enter",
            violation_direction="missing",
            evidence_types=("source_identity", "closed_model_inventory", "initial_entry_fact", "containment_fact"),
            normative_statement=f"{scope.name} must have an owner-local default entry into required operating child {target.name}.",
            scope=f"Owner-local default entry of {scope.name}",
            source_refs=base.source_refs,
            reason="The LLM-established behavior is owned below this composite, so the owner's default entry must activate the exact required child scope.",
            basis="typed root-reachability frontier plus exact child ancestry and owner-local initial edges",
        )
        refs = [scope.ref, target.ref, *[item.ref for item in initial]]
        refs.extend(ref for item in initial if (ref := _transition_target_ref(pair, item)))
        source_refs = tuple(
            dict.fromkeys(
                [
                    *derived.source_refs,
                    source_scope.raw_ref,
                    *[item.raw_ref for item in source_children],
                    *[item.raw_ref for item in source_initial],
                ]
            )
        )
        candidate = _candidate(
            derived,
            title=f"{scope.name} lacks default entry into {target.name}",
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=source_refs,
            expected=derived.normative_statement,
            observed=(
                f"The exact author-source composite has direct children "
                f"{[item.source_id for item in source_children]} and owner-local "
                f"initial targets {[item.target for item in source_initial]}; the "
                f"closed model records initial targets {[item.target for item in initial]}."
            ),
            strongest_rebuttal="An initial edge inside the child scope does not provide the missing owner-level entry.",
            reason="Exact owner/child binding and complete owner-local initial inventory establish the missing default entry.",
            basis=f"source_owner={source_scope.source_id}; source_child={source_target.source_id}; source_initial_refs={[item.raw_ref for item in source_initial]}; owner_ref={scope.ref}; child_ref={target.ref}; model_initial_refs={[item.ref for item in initial]}",
        )
        builder.add(
            "owner_initial_entry",
            (base.contract_id,),
            derived,
            candidate,
            reason="The required operating child has no unconditional entry from its exact composite owner.",
            basis="root frontier, exact hierarchy, and scoped initial-transition inventory",
        )


def _materialize_dead_ends(builder: _Builder, contracts: Sequence[NLContract]) -> None:
    pair = builder.pair
    for contract in contracts:
        if contract.state_role != "operating_state" or contract.property not in {"state_action", "deadlock_freedom"}:
            continue
        state_hint = _hint(contract, "state") or _hint(contract, "target") or _hint(contract, "owner")
        state = _state_for_value(pair, state_hint.value if state_hint else None)
        if state is None and len(contract.locus_names) == 1:
            state = _state_for_value(pair, contract.locus_names[0])
        fact = _inspection_state(pair, state.ref) if state else None
        if not state or not fact or not fact.reachable_from_initial or fact.outgoing_transition_refs:
            continue
        target_contract = contract
        if contract.property != "deadlock_freedom":
            target_contract = _derived_contract(
                contract,
                locus_kind="state",
                locus_names=(state.name,),
                property_name="deadlock_freedom",
                state_role="operating_state",
                expected_direction="must_progress",
                violation_direction="dead_end",
                evidence_types=("source_identity", "closed_model_inventory", "deadlock_frontier_fact", "verify_fact"),
                normative_statement=f"Required operating state {state.name} must retain an operational continuation.",
                scope=f"Operational continuation of {state.name}",
                source_refs=contract.source_refs,
                reason="The base contract assigns explicit operating behavior to this state, allowing the exact reachable-leaf frontier to test continuation separately from action content.",
                basis="typed operating state_action contract plus exact reachable leaf/no-outgoing fact",
            )
        candidate = _candidate(
            target_contract,
            title=f"{state.name} has no operational continuation",
            predicate_id="V4",
            predicate_inputs={"initial_scope": state.name},
            element_refs=(state.ref,),
            source_refs=target_contract.source_refs,
            expected=target_contract.normative_statement,
            observed=f"{state.ref} is reachable_from_initial=true and outgoing_transition_refs=[].",
            strongest_rebuttal="No explicit terminal role or final edge is supplied for this typed operating state.",
            reason="An explicit operating-state contract and the deterministic reachable leaf frontier establish a reproducible no-continuation candidate.",
            basis=f"state_ref={state.ref}; inspection={pair.inspection_facts.algorithm_version if pair.inspection_facts else 'unavailable'}",
        )
        builder.add(
            "reachable_dead_end",
            (contract.contract_id,),
            target_contract,
            candidate,
            reason="An explicit operating-state obligation is bound to a reachable leaf with no outgoing transition.",
            basis="typed state role plus inspection-equivalent deadlock frontier",
        )


def _source_state_id(pair: PairInput, state: StateNode) -> str | None:
    inventory = pair.exact_source_inventory
    if inventory is None:
        return None
    matches = [item.source_id for item in inventory.states if item.name == state.name]
    return matches[0] if len(matches) == 1 else None


def _source_path(
    pair: PairInput, target_id: str
) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    source_ir = pair.canonical_source_ir
    if source_ir is None:
        return None
    transitions = source_ir.model.transitions
    graph: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for transition in transitions:
        graph[transition.source].append((transition.target, transition.id))
    roots = tuple(source_ir.model.initial_states)
    queue: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [
        (root, (root,), ()) for root in roots
    ]
    seen: set[str] = set()
    while queue:
        node, states, transition_ids = queue.pop(0)
        if node in seen:
            continue
        seen.add(node)
        if node == target_id:
            return states, transition_ids
        for next_state, transition_id in graph.get(node, ()):
            queue.append(
                (
                    next_state,
                    (*states, next_state),
                    (*transition_ids, transition_id),
                )
            )
    return None


def _materialize_termination(builder: _Builder, contracts: Sequence[NLContract]) -> None:
    pair = builder.pair
    for contract in contracts:
        if contract.property != "termination" or contract.state_role != "termination_state":
            continue
        target_hint = _hint(contract, "target") or _hint(contract, "state")
        owner_hint = _hint(contract, "owner") or _hint(contract, "scope")
        target = _state_for_value(pair, target_hint.value if target_hint else None)
        owner = _state_for_value(pair, owner_hint.value if owner_hint else None)
        if target is None:
            continue
        source_ir = pair.canonical_source_ir
        source_target_id = _source_state_id(pair, target)
        source_states = {
            item.id: item for item in source_ir.model.states
        } if source_ir else {}
        source_ancestors: list[str] = []
        cursor = source_target_id
        while cursor and cursor in source_states:
            source_ancestors.append(cursor)
            cursor = source_states[cursor].parent
        source_path = _source_path(pair, source_target_id) if source_target_id else None
        source_transitions = {
            item.id: item for item in source_ir.model.transitions
        } if source_ir else {}
        path_unguarded = bool(source_path) and all(
            source_transitions[transition_id].guard is None
            for transition_id in source_path[1]
            if transition_id in source_transitions
        )
        continuing = [
            item
            for item in source_transitions.values()
            if item.source in source_ancestors
            and item.attributes.get("transition_kind") not in {"initial", "final"}
            and item.guard is None
        ]
        explicit_final = bool(
            source_ir
            and source_target_id in set(source_ir.model.final_states)
        )
        sound_for_claim = bool(
            source_ir
            and source_target_id
            and source_path
            and path_unguarded
            and not source_ir.model.concurrent_regions
        )
        if sound_for_claim and continuing and not explicit_final:
            candidate = _candidate(
                contract,
                title=f"Termination target {target.name} admits continued behavior",
                predicate_id=None,
                predicate_inputs={},
                element_refs=(target.ref,),
                source_refs=(
                    *contract.source_refs,
                    *[item.raw_ref for item in continuing],
                ),
                expected=contract.normative_statement,
                observed=f"The exact reachable author-source target is not explicit-final and its ancestor chain admits guard-free continuations {[item.id for item in continuing]}.",
                strongest_rebuttal="Endpoint existence alone does not prove that the designated ending target is stable.",
                reason="The NL marks the exact target as a termination state, while the closed author-source soundness fragment establishes reachable non-final continuation.",
                basis=f"contract={contract.contract_id}; source_target_id={source_target_id}; source_path={source_path}; continuation_ids={[item.id for item in continuing]}",
            )
            builder.add(
                "stable_termination",
                (contract.contract_id,),
                contract,
                candidate,
                reason="A typed termination target has exact continuing behavior and is not an explicit stable sink.",
                basis="termination state role plus canonical author-source reachability, final-state, hierarchy, and transition inventory",
            )
        if owner and not _is_descendant(pair, target, owner):
            actual_parent = target.parent or "model root"
            derived = _derived_contract(
                contract,
                locus_kind="path",
                locus_names=(owner.name, target.name, actual_parent),
                property_name="route_avoidance",
                state_role="termination_state",
                expected_direction="must_avoid",
                violation_direction="wrong_scope",
                evidence_types=("source_identity", "closed_model_inventory", "transition_fact", "containment_fact", "reachability_fact"),
                normative_statement=f"Completion of {owner.name} must not route into a termination target owned by another operating scope.",
                scope=f"Completion route from {owner.name}",
                source_refs=contract.source_refs,
                reason="The typed termination owner and target resolve exactly, and the target ancestry belongs to a different scope.",
                basis="termination contract owner/target hints and complete ModelIR parent chain",
            )
            candidate = _candidate(
                derived,
                title=f"{owner.name} completion routes into {actual_parent}",
                predicate_id=None,
                predicate_inputs={},
                element_refs=(owner.ref, target.ref),
                source_refs=derived.source_refs,
                expected=derived.normative_statement,
                observed=f"The exact target {target.ref} is owned by {actual_parent}, not {owner.name}.",
                strongest_rebuttal="A same-named termination state in another scope is not the required owner-local target.",
                reason="Exact target ancestry refutes the owner-scoped completion route.",
                basis=f"owner_ref={owner.ref}; target_ref={target.ref}; target_parent={actual_parent}",
            )
            builder.add(
                "wrong_scope_route",
                (contract.contract_id,),
                derived,
                candidate,
                reason="The exact termination target lies under a different operating owner.",
                basis="typed termination owner and exact target ancestor chain",
            )


def _group_operating_source(
    pair: PairInput,
    group: NLTransitionGroup,
    contracts: Sequence[NLContract],
) -> StateNode | None:
    target_names = {item.target_name for item in group.alternatives}

    def matching_target_count(source: StateNode) -> int:
        return len(
            {
                item.target
                for item in pair.model.transitions
                if item.source == source.name and item.target in target_names
            }
        )

    declared_source = _state_for_value(pair, group.source_name)
    if declared_source is not None and matching_target_count(declared_source) >= 2:
        return declared_source

    entry_targets: list[StateNode] = []
    for contract in contracts:
        if contract.segment_id != group.segment_id or contract.property != "initial_entry":
            continue
        owner_hint = _hint(contract, "owner")
        target_hint = _hint(contract, "target")
        if (
            owner_hint is None
            or target_hint is None
            or owner_hint.value != group.source_name
        ):
            continue
        target = _state_for_value(pair, target_hint.value)
        if target is not None and matching_target_count(target) >= 2:
            entry_targets.append(target)
    unique_targets = {item.ref: item for item in entry_targets}
    return next(iter(unique_targets.values())) if len(unique_targets) == 1 else None


def _group_transitions(
    pair: PairInput,
    group: NLTransitionGroup,
    contracts: Sequence[NLContract],
) -> tuple[StateNode | None, list[tuple[object, Transition]]]:
    source = _group_operating_source(pair, group, contracts)
    if source is None:
        return None, []
    rows: list[tuple[object, Transition]] = []
    for alternative in group.alternatives:
        target = _state_for_value(pair, alternative.target_name)
        if target is None:
            continue
        matches = [
            item
            for item in pair.model.transitions
            if item.source == source.name and item.target == target.name
        ]
        if len(matches) == 1:
            rows.append((alternative, matches[0]))
    return source, rows


def _group_base_contract(
    group: NLTransitionGroup,
    source: StateNode,
    contracts: Sequence[NLContract],
) -> NLContract | None:
    target_names = {item.target_name for item in group.alternatives}
    endpoint_contracts = []
    relation_contracts = []
    for contract in contracts:
        if contract.segment_id != group.segment_id:
            continue
        source_hint = _hint(contract, "source")
        target_hints = [item for item in contract.binding_hints if item.role == "target"]
        if (
            contract.property == "transition_endpoints"
            and source_hint is not None
            and source_hint.value in {group.source_name, source.name}
            and any(item.value in target_names for item in target_hints)
        ):
            endpoint_contracts.append(contract)
        scope_hints = [
            item
            for item in contract.binding_hints
            if item.role in {"source", "scope", "owner"}
        ]
        if (
            len({item.value for item in target_hints if item.value in target_names}) >= 2
            and any(item.value == group.source_name for item in scope_hints)
        ):
            relation_contracts.append(contract)
    candidates = endpoint_contracts or relation_contracts
    return candidates[0] if candidates else None


def _materialize_group_collisions(
    builder: _Builder,
    groups: Sequence[NLTransitionGroup],
    contracts: Sequence[NLContract],
) -> None:
    pair = builder.pair
    for group in groups:
        if len(group.alternatives) < 2:
            continue
        if len({alternative.target_name for alternative in group.alternatives}) < 2:
            continue
        source, rows = _group_transitions(pair, group, contracts)
        if len(rows) < 2:
            continue
        normative_conditions = {
            (item.condition_role, item.condition) for item, _transition in rows
        }
        signatures = {
            (transition.triggers, transition.guard) for _item, transition in rows
        }
        if len(signatures) != 1:
            continue
        base = _group_base_contract(group, source, contracts) if source else None
        if base is None or source is None:
            continue
        targets = [_state_for_value(pair, item.target_name) for item, _ in rows]
        targets = [item for item in targets if item]
        derived = _derived_contract(
            base,
            locus_kind="transition",
            locus_names=(source.name, *[item.target_name for item, _ in rows]),
            property_name="guard_disjointness",
            state_role=base.state_role,
            expected_direction="must_cover",
            violation_direction="wrong_guard",
            evidence_types=("source_identity", "closed_model_inventory", "transition_fact", "guard_fact", "semantic_comparison"),
            normative_statement=f"Distinct alternatives in {group.group_id} must remain operationally distinguishable.",
            scope=f"Transition group {group.group_id}",
            source_refs=group.source_refs,
            reason="The LLM transition group establishes distinct alternatives, and a typed owner-entry relation resolves the operational source when the group is stated at composite scope.",
            basis="typed transition group alternatives and exact ModelIR trigger/guard fields",
        )
        refs = [transition.ref for _, transition in rows]
        refs.extend(item.ref for item in ([source] if source else []) + targets)
        candidate = _candidate(
            derived,
            title=f"Alternatives in {group.group_id} are operationally indistinguishable",
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=f"The exact transitions {[transition.ref for _, transition in rows]} share trigger/guard signature {next(iter(signatures))}.",
            strongest_rebuttal="Individual endpoint existence does not establish that distinct alternatives are distinguishable.",
            reason="Distinct typed conditions map to multiple exact targets whose closed transition signatures are identical.",
            basis=f"group={group.group_id}; normative_conditions={sorted(map(str, normative_conditions))}; transition_refs={[transition.ref for _, transition in rows]}",
        )
        builder.add(
            "transition_group_collision",
            tuple(
                item.contract_id
                for item in contracts
                if item.segment_id == group.segment_id
                and any(
                    hint.role == "target"
                    and hint.value
                    in {alternative.target_name for alternative in group.alternatives}
                    for hint in item.binding_hints
                )
            )
            or (base.contract_id,),
            derived,
            candidate,
            reason="A typed multi-target relation has identical exact trigger/guard signatures for distinct alternatives.",
            basis="transition group semantic identity and exact closed-model signatures",
        )


def _source_endpoint_name(value: str) -> str:
    """Return the exact leaf identifier from a canonical qualified source endpoint."""

    return value.rsplit(".", 1)[-1]


def _source_carrier_for_contract(
    pair: PairInput,
    contract: NLContract,
    source_state: StateNode,
) -> SourceInventoryTransition | None:
    inventory = pair.exact_source_inventory
    condition_hint = _hint(contract, "guard", "event", "trigger")
    if inventory is None or condition_hint is None:
        return None
    rows = [
        item
        for item in inventory.transitions
        if _source_endpoint_name(item.source) == source_state.name
        and condition_hint.value in {item.event, item.guard}
    ]
    return rows[0] if len(rows) == 1 else None


def _model_carrier_for_source_row(
    pair: PairInput,
    source_row: SourceInventoryTransition,
) -> Transition | None:
    source_name = _source_endpoint_name(source_row.source)
    target_name = _source_endpoint_name(source_row.target)
    rows = [
        item
        for item in pair.model.transitions
        if item.source == source_name and item.target == target_name
    ]
    return rows[0] if len(rows) == 1 else None


def _materialize_wrong_targets(
    builder: _Builder,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
) -> None:
    pair = builder.pair
    contracts_by_id = {item.contract_id: item for item in contracts}
    exact_target_bindings = [
        binding
        for response in grounding_responses
        for binding in response.semantic_bindings
        if binding.status == "exact"
        and binding.role == "target"
        and binding.model_element_ref
        and binding.carrier_transition_ref
    ]
    for binding in exact_target_bindings:
        base = contracts_by_id.get(binding.contract_id)
        expected_state = _state_by_ref(pair, binding.model_element_ref)
        carrier = pair.model.transition(binding.carrier_transition_ref)
        if (
            base is None
            or base.property != "transition_endpoints"
            or expected_state is None
            or carrier is None
        ):
            continue
        source_hint = _hint(base, "source")
        source_state = _state_for_value(pair, source_hint.value if source_hint else None)
        actual_source = _state_for_value(pair, carrier.source)
        actual_target_ref = _transition_target_ref(pair, carrier)
        actual_target = _state_by_ref(pair, actual_target_ref)
        if (
            source_state is None
            or actual_source is None
            or actual_target is None
            or actual_source.ref != source_state.ref
            or actual_target.ref == expected_state.ref
        ):
            continue
        target_contract = base
        if base.violation_direction != "wrong_target":
            target_contract = _derived_contract(
                base,
                locus_kind="transition",
                locus_names=(source_state.name, expected_state.name),
                property_name="transition_endpoints",
                state_role=base.state_role,
                expected_direction=base.expected_direction,
                violation_direction="wrong_target",
                evidence_types=(
                    "source_identity",
                    "closed_model_inventory",
                    "transition_fact",
                    "semantic_comparison",
                ),
                normative_statement=base.normative_statement,
                scope=base.scope,
                source_refs=base.source_refs,
                reason="An exact grounding binding identifies the normative target and its conflicting closed transition carrier.",
                basis="SemanticBinding target/model refs and exact ModelIR transition endpoints",
            )
        candidate = _candidate(
            target_contract,
            title=f"{source_state.name} routes to {actual_target.name} instead of {expected_state.name}",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(
                source_state.ref,
                expected_state.ref,
                actual_target.ref,
                carrier.ref,
            ),
            source_refs=(
                *target_contract.source_refs,
                *([binding.source_element_ref] if binding.source_element_ref else []),
            ),
            expected=target_contract.normative_statement,
            observed=f"Exact carrier {carrier.ref} leaves {source_state.ref} but targets {actual_target.ref}, while the normative target binding is {expected_state.ref}.",
            strongest_rebuttal="A transition to a different exact target cannot satisfy this condition-scoped endpoint obligation.",
            reason="The target SemanticBinding is exact and the supplied carrier transition has a different resolved target under the same source contract.",
            basis=f"binding_id={binding.binding_id}; source_ref={source_state.ref}; expected_target_ref={expected_state.ref}; carrier_ref={carrier.ref}; actual_target_ref={actual_target.ref}",
        )
        builder.add(
            "wrong_target",
            (base.contract_id,),
            target_contract,
            candidate,
            reason="One exact target binding is refuted by the resolved endpoint of its supplied closed transition carrier.",
            basis="typed SemanticBinding plus exact ModelIR transition source/target refs",
        )

    target_refs_by_concept: dict[str, set[str]] = defaultdict(set)
    bindings_by_concept: dict[str, list[SemanticBinding]] = defaultdict(list)
    for binding in exact_target_bindings:
        target_refs_by_concept[binding.concept_name].add(binding.model_element_ref)
        bindings_by_concept[binding.concept_name].append(binding)
    for base in contracts:
        if base.property != "transition_endpoints":
            continue
        source_hint = _hint(base, "source")
        target_hint = _hint(base, "target")
        if source_hint is None or target_hint is None:
            continue
        expected_refs = target_refs_by_concept.get(target_hint.value, set())
        if len(expected_refs) != 1:
            continue
        expected_state = _state_by_ref(pair, next(iter(expected_refs)))
        source_state = _state_for_value(pair, source_hint.value)
        source_carrier = (
            _source_carrier_for_contract(pair, base, source_state)
            if source_state is not None
            else None
        )
        model_carrier = (
            _model_carrier_for_source_row(pair, source_carrier)
            if source_carrier is not None
            else None
        )
        actual_target = (
            _state_for_value(pair, _source_endpoint_name(source_carrier.target))
            if source_carrier is not None
            else None
        )
        if (
            expected_state is None
            or source_state is None
            or source_carrier is None
            or model_carrier is None
            or actual_target is None
            or actual_target.ref == expected_state.ref
        ):
            continue
        target_contract = base
        if base.violation_direction != "wrong_target":
            target_contract = _derived_contract(
                base,
                locus_kind="transition",
                locus_names=(source_state.name, expected_state.name),
                property_name="transition_endpoints",
                state_role=base.state_role,
                expected_direction=base.expected_direction,
                violation_direction="wrong_target",
                evidence_types=(
                    "source_identity",
                    "closed_model_inventory",
                    "transition_fact",
                    "semantic_comparison",
                ),
                normative_statement=base.normative_statement,
                scope=base.scope,
                source_refs=base.source_refs,
                reason="A unique exact target-concept binding is reused across contracts carrying the same typed target concept.",
                basis="SemanticBinding concept identity plus exact source transition inventory",
            )
        concept_bindings = bindings_by_concept[target_hint.value]
        candidate = _candidate(
            target_contract,
            title=f"{source_state.name} routes to {actual_target.name} instead of {expected_state.name}",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(
                source_state.ref,
                expected_state.ref,
                actual_target.ref,
                model_carrier.ref,
            ),
            source_refs=(
                *target_contract.source_refs,
                source_carrier.raw_ref,
                *[
                    item.source_element_ref
                    for item in concept_bindings
                    if item.source_element_ref
                ],
            ),
            expected=target_contract.normative_statement,
            observed=(
                f"Exact author-source carrier {source_carrier.transition_id} "
                f"targets {source_carrier.target}; its closed-model carrier "
                f"{model_carrier.ref} targets {actual_target.ref}, while the unique "
                f"normative concept binding is {expected_state.ref}."
            ),
            strongest_rebuttal="A condition-scoped transition to a different exact target cannot satisfy the bound target concept.",
            reason="The same typed target concept has one exact cross-artifact binding, and the exact source+condition carrier resolves to a different target.",
            basis=(
                f"concept={target_hint.value}; source_transition_id={source_carrier.transition_id}; "
                f"source_ref={source_state.ref}; expected_target_ref={expected_state.ref}; "
                f"carrier_ref={model_carrier.ref}; actual_target_ref={actual_target.ref}"
            ),
        )
        builder.add(
            "wrong_target",
            (base.contract_id,),
            target_contract,
            candidate,
            reason="One exact shared target-concept binding is refuted by the exact source+condition carrier endpoint.",
            basis="typed concept identity, exact source transition inventory, and exact ModelIR endpoints",
        )

    contract_carriers: list[
        tuple[
            NLContract,
            ContractBindingHint,
            StateNode,
            SourceInventoryTransition,
            Transition,
            StateNode,
        ]
    ] = []
    direct_target_roles: dict[str, list[tuple[NLContract, ContractBindingHint]]] = (
        defaultdict(list)
    )
    for contract in contracts:
        target_hint = _hint(contract, "target")
        if target_hint is not None:
            direct_target = _state_for_value(pair, target_hint.value)
            if direct_target is not None:
                direct_target_roles[direct_target.ref].append((contract, target_hint))
        if contract.property != "transition_endpoints" or target_hint is None:
            continue
        source_hint = _hint(contract, "source")
        source_state = _state_for_value(pair, source_hint.value if source_hint else None)
        source_carrier = (
            _source_carrier_for_contract(pair, contract, source_state)
            if source_state is not None
            else None
        )
        model_carrier = (
            _model_carrier_for_source_row(pair, source_carrier)
            if source_carrier is not None
            else None
        )
        actual_target = (
            _state_for_value(pair, _source_endpoint_name(source_carrier.target))
            if source_carrier is not None
            else None
        )
        if (
            source_state is not None
            and source_carrier is not None
            and model_carrier is not None
            and actual_target is not None
        ):
            contract_carriers.append(
                (
                    contract,
                    target_hint,
                    source_state,
                    source_carrier,
                    model_carrier,
                    actual_target,
                )
            )

    for (
        base,
        target_hint,
        source_state,
        source_carrier,
        model_carrier,
        actual_target,
    ) in contract_carriers:
        foreign_roles = [
            (contract, hint)
            for contract, hint in direct_target_roles.get(actual_target.ref, [])
            if contract.contract_id != base.contract_id
            and hint.value != target_hint.value
        ]
        if not foreign_roles:
            continue
        sibling_rows = [
            row
            for row in contract_carriers
            if row[0].contract_id != base.contract_id
            and row[1].value == target_hint.value
            and row[5].ref != actual_target.ref
        ]
        sibling_target_refs = {row[5].ref for row in sibling_rows}
        foreign_role_names = {hint.value for _contract, hint in foreign_roles}
        if len(sibling_target_refs) != 1 or len(foreign_role_names) != 1:
            continue
        expected_state = _state_by_ref(pair, next(iter(sibling_target_refs)))
        if expected_state is None:
            continue
        target_contract = base
        if base.violation_direction != "wrong_target":
            target_contract = _derived_contract(
                base,
                locus_kind="transition",
                locus_names=(source_state.name, target_hint.value),
                property_name="transition_endpoints",
                state_role=base.state_role,
                expected_direction=base.expected_direction,
                violation_direction="wrong_target",
                evidence_types=(
                    "source_identity",
                    "closed_model_inventory",
                    "transition_fact",
                    "semantic_comparison",
                ),
                normative_statement=base.normative_statement,
                scope=base.scope,
                source_refs=base.source_refs,
                reason="Cross-contract target roles distinguish the required concept from the carrier's actual target.",
                basis="typed target concepts and exact source+condition carriers",
            )
        supporting_source_refs = [
            row[3].raw_ref for row in sibling_rows if row[5].ref == expected_state.ref
        ]
        supporting_source_refs.extend(
            ref
            for contract, _hint_value in foreign_roles
            for ref in contract.source_refs
        )
        foreign_role = next(iter(foreign_role_names))
        candidate = _candidate(
            target_contract,
            title=(
                f"{source_state.name} routes to {actual_target.name} instead of "
                f"the required {target_hint.value} target"
            ),
            predicate_id=None,
            predicate_inputs={},
            element_refs=(
                source_state.ref,
                expected_state.ref,
                actual_target.ref,
                model_carrier.ref,
            ),
            source_refs=(
                *target_contract.source_refs,
                source_carrier.raw_ref,
                *supporting_source_refs,
            ),
            expected=target_contract.normative_statement,
            observed=(
                f"Exact author-source carrier {source_carrier.transition_id} targets "
                f"{source_carrier.target}; sibling carriers for target concept "
                f"{target_hint.value!r} uniquely target {expected_state.ref}, while "
                f"{actual_target.ref} is independently bound as {foreign_role!r}."
            ),
            strongest_rebuttal=(
                "Treating the actual target as an alias for the required concept would "
                "conflict with its independent typed target role and the unique sibling "
                "carrier target."
            ),
            reason="Exact source carriers map one typed target concept inconsistently, and the divergent target has a distinct independently established role.",
            basis=(
                f"concept={target_hint.value}; source_transition_id={source_carrier.transition_id}; "
                f"expected_target_ref={expected_state.ref}; actual_target_ref={actual_target.ref}; "
                f"foreign_role={foreign_role}; sibling_transition_ids="
                f"{[row[3].transition_id for row in sibling_rows]}"
            ),
        )
        builder.add(
            "wrong_target",
            tuple(
                dict.fromkeys(
                    [
                        base.contract_id,
                        *[row[0].contract_id for row in sibling_rows],
                        *[contract.contract_id for contract, _hint_value in foreign_roles],
                    ]
                )
            ),
            target_contract,
            candidate,
            reason="A condition-scoped carrier diverges from the unique sibling target for the same concept and instead reaches a separately typed target role.",
            basis="typed cross-contract relation plus exact source and ModelIR transition identities",
        )


def _missing_endpoint_rows(
    pair: PairInput, contracts: Sequence[NLContract]
) -> list[tuple[NLContract, StateNode, StateNode]]:
    rows = []
    for contract in contracts:
        if contract.property != "transition_endpoints" or contract.expected_direction != "must_exist":
            continue
        source_hint = _hint(contract, "source")
        target_hint = _hint(contract, "target")
        source = _state_for_value(pair, source_hint.value if source_hint else None)
        target = _state_for_value(pair, target_hint.value if target_hint else None)
        if not source or not target:
            continue
        if any(item.source == source.name and item.target == target.name for item in pair.model.transitions):
            continue
        rows.append((contract, source, target))
    return rows


def _wrapper_under(pair: PairInput, state: StateNode, owner: StateNode) -> StateNode | None:
    return _direct_child_under(pair, state, owner)


def _materialize_cross_wrapper(builder: _Builder, contracts: Sequence[NLContract]) -> None:
    pair = builder.pair
    rows = _missing_endpoint_rows(pair, contracts)
    by_source = {source.ref: (contract, source, target) for contract, source, target in rows}
    chains: list[list[tuple[NLContract, StateNode, StateNode]]] = []
    for row in rows:
        chain = [row]
        seen = {row[1].ref}
        cursor = row[2]
        while cursor.ref in by_source and cursor.ref not in seen:
            seen.add(cursor.ref)
            next_row = by_source[cursor.ref]
            chain.append(next_row)
            cursor = next_row[2]
        if len(chain) >= 2:
            chains.append(chain)
    seen_chains: set[tuple[str, ...]] = set()
    for chain in chains:
        ids = tuple(item[0].contract_id for item in chain)
        if ids in seen_chains:
            continue
        seen_chains.add(ids)
        states = [chain[0][1], *[item[2] for item in chain]]
        ancestor_sets = [
            {item.ref: item for item in _ancestor_chain(pair, state)} for state in states
        ]
        common_refs = set.intersection(*(set(item) for item in ancestor_sets))
        owners = [
            item
            for item in _ancestor_chain(pair, states[0])
            if item.ref in common_refs and item.ref != states[0].ref
        ]
        owner = owners[0] if owners else None
        if owner is None:
            continue
        wrappers = [_wrapper_under(pair, state, owner) for state in states]
        if any(item is None for item in wrappers) or len({item.ref for item in wrappers if item}) < 2:
            continue
        base = chain[0][0]
        derived = _derived_contract(
            base,
            locus_kind="scope",
            locus_names=tuple(state.name for state in states),
            property_name="reachability",
            state_role="operating_state",
            expected_direction="must_reach",
            violation_direction="unreachable",
            evidence_types=("source_identity", "closed_model_inventory", "transition_fact", "reachability_fact", "semantic_comparison"),
            normative_statement=f"The required sequential operating states under {owner.name} must be mutually reachable in the stated order.",
            scope=f"Cross-wrapper operating relation under {owner.name}",
            source_refs=_source_refs([item[0] for item in chain]),
            reason="Multiple typed endpoint contracts form one exact sequential chain across distinct wrappers under a common owner.",
            basis="contract source/target bindings, exact parent chains, and complete missing-edge inventory",
        )
        refs = [owner.ref, *[state.ref for state in states], *[item.ref for item in wrappers if item]]
        candidate = _candidate(
            derived,
            title=f"Required cross-wrapper sequence under {owner.name} is disconnected",
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=f"The complete closed transition inventory contains none of the required chain edges {[f'{item[1].name}->{item[2].name}' for item in chain]} across wrappers {[item.name for item in wrappers if item]}.",
            strongest_rebuttal="Independent region-local initial edges do not establish the required cross-wrapper sequence.",
            reason="The LLM-established endpoint chain is exact, and the complete model contains no links between its distinct wrapper scopes.",
            basis=f"owner_ref={owner.ref}; contracts={list(ids)}; state_refs={[state.ref for state in states]}",
        )
        builder.add(
            "cross_wrapper_reachability",
            ids,
            derived,
            candidate,
            reason="A typed multi-contract sequence spans distinct wrappers with no exact connecting transitions.",
            basis="exact contract chain, hierarchy, and complete transition inventory",
        )


def _materialize_event_consumers(
    builder: _Builder,
    contracts: Sequence[NLContract],
    scopes: dict[str, tuple[StateNode, StateNode, NLContract]],
) -> None:
    pair = builder.pair
    if pair.inspection_facts is None:
        return
    grouped: dict[str, list[tuple[NLContract, str, tuple[str, ...]]]] = defaultdict(list)
    facts_by_event = {
        item.event: item for item in pair.inspection_facts.event_consumers
    }
    for scope, _descendant, base in scopes.values():
        for fact in pair.inspection_facts.event_consumers:
            if (
                not fact.consumer_transition_refs
                or fact.reachable_consumer_transition_refs
            ):
                continue
            refs: list[str] = [scope.ref]
            for transition_ref in fact.consumer_transition_refs:
                transition = pair.model.transition(transition_ref)
                source = _state_for_value(pair, transition.source) if transition else None
                if source is None or not (
                    source.ref == scope.ref or _is_descendant(pair, source, scope)
                ):
                    continue
                refs.extend((transition_ref, source.ref))
            if len(refs) > 1:
                grouped[scope.ref].append(
                    (base, fact.event, tuple(dict.fromkeys(refs)))
                )
    for contract in contracts:
        event_hints = [hint for hint in contract.binding_hints if hint.role == "event"]
        for hint in event_hints:
            fact = facts_by_event.get(hint.value)
            if (
                fact is None
                or not fact.consumer_transition_refs
                or fact.reachable_consumer_transition_refs
            ):
                continue
            refs_by_scope: dict[str, list[str]] = defaultdict(list)
            for transition_ref in fact.consumer_transition_refs:
                transition = pair.model.transition(transition_ref)
                source = _state_for_value(pair, transition.source) if transition else None
                scope = _highest_unreachable_scope(pair, source) if source else None
                if scope is None:
                    continue
                refs_by_scope[scope.ref].extend((transition_ref, source.ref))
            for scope_ref, consumer_refs in refs_by_scope.items():
                refs = tuple(
                    dict.fromkeys((scope_ref, *consumer_refs))
                )
                grouped[scope_ref].append((contract, fact.event, refs))
    for scope_ref, rows in grouped.items():
        scope = _state_by_ref(pair, scope_ref)
        if scope is None:
            continue
        base = rows[0][0]
        events = tuple(dict.fromkeys(item[1] for item in rows))
        refs = tuple(dict.fromkeys(ref for item in rows for ref in item[2]))
        derived = _derived_contract(
            base,
            locus_kind="scope",
            locus_names=(scope.name,),
            property_name="event_consumer_coverage",
            state_role="operating_state",
            expected_direction="must_cover",
            violation_direction="unconsumed",
            evidence_types=("source_identity", "closed_model_inventory", "event_consumer_fact", "reachability_fact", "verify_fact"),
            normative_statement=f"Required events {list(events)} must have reachable consumers in operating scope {scope.name}.",
            scope=f"Reachable event-consumer coverage of {scope.name}",
            source_refs=_source_refs([item[0] for item in rows]),
            reason="Typed event-response contracts bind exact consumer transitions below one unreachable operating scope.",
            basis="contract event roles, exact transition refs, and inspection-equivalent consumer reachability rows",
        )
        candidate = _candidate(
            derived,
            title=f"{scope.name} has declared but unreachable event consumers",
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=f"Events {list(events)} have declared consumer transitions, but their reachable_consumer_transition_refs are empty.",
            strongest_rebuttal="Declaration-only consumer existence does not satisfy operational reachable-consumer coverage.",
            reason="Exact event-consumer rows show consumers exist but none can execute from the model root.",
            basis=f"scope_ref={scope.ref}; events={list(events)}; consumer_refs={list(refs)}",
        )
        builder.add(
            "event_consumer_coverage",
            tuple(dict.fromkeys(item[0].contract_id for item in rows)),
            derived,
            candidate,
            reason="One exact operating scope contains required declared consumers that are all unreachable.",
            basis="typed event contracts and exact inspection-equivalent event-consumer coverage",
        )


def materialize_v27_frontier(
    pair: PairInput,
    contracts: NLContractResponse,
    contracts_by_id: dict[str, NLContract],
    grounding_responses: Sequence[GroundingResponse],
    llm_candidates: Sequence[CandidateIssue],
) -> FrontierBatch:
    """Expand established typed obligations into systematic v27 frontier candidates."""

    all_contracts = list(contracts_by_id.values())
    all_groups: list[NLTransitionGroup] = []
    seen_group_keys: set[str] = set()
    for group in [
        *contracts.transition_groups,
        *[
            item
            for response in grounding_responses
            for item in response.additional_transition_groups
        ],
    ]:
        encoded_key = json.dumps(
            transition_group_semantic_key(group).model_dump(mode="json"),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        if encoded_key in seen_group_keys:
            continue
        seen_group_keys.add(encoded_key)
        all_groups.append(group)
    builder = _Builder(pair, llm_candidates)
    _materialize_containment(builder, all_contracts)
    _materialize_cardinality(
        builder, all_contracts, grounding_responses, llm_candidates
    )
    _materialize_initial_entries(builder, all_contracts)
    scopes = _materialize_root_reachability(builder, all_contracts, llm_candidates)
    _materialize_scope_entries(builder, scopes)
    _materialize_dead_ends(builder, all_contracts)
    _materialize_termination(builder, all_contracts)
    _materialize_group_collisions(builder, all_groups, all_contracts)
    _materialize_wrong_targets(builder, all_contracts, grounding_responses)
    _materialize_cross_wrapper(builder, all_contracts)
    _materialize_event_consumers(builder, all_contracts, scopes)
    return FrontierBatch(
        obligations=tuple(builder.obligations),
        checks=tuple(builder.checks),
        superseded_candidate_contract_ids=tuple(
            builder.superseded_candidate_contract_ids
        ),
        reason="The runner systematically expanded LLM-established typed obligations through the v27 domain frontier before predicate selection.",
        basis=(
            "NLContractResponse and grounding semantic identities; owned ModelIR; "
            f"source_inventory={pair.exact_source_inventory.algorithm_version if pair.exact_source_inventory else 'unavailable'}; "
            f"inspection={pair.inspection_facts.algorithm_version if pair.inspection_facts else 'unavailable'}"
        ),
    )


__all__ = [
    "ContractSemanticKey",
    "FrontierBatch",
    "FrontierCheckReceipt",
    "FrontierObligation",
    "GroupIdentityNormalizationReceipt",
    "IdentityNormalizationReceipt",
    "TransitionAlternativeSemanticKey",
    "TransitionGroupSemanticKey",
    "canonical_contract_id",
    "canonical_transition_group_id",
    "canonicalize_grounding_response",
    "contract_semantic_key",
    "materialize_v27_frontier",
    "transition_group_semantic_key",
]
