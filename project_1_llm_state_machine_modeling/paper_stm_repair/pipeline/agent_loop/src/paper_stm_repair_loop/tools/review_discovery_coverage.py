from __future__ import annotations

import contextvars
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable, Mapping

from utils.agent import AgentApp, AgentSpec
from utils.llm import LLMRegistry

from ..schemas.coverage_review import CoverageReviewVerdict
from ..schemas.tools import NonBlankString, SimpleStructuredTool, StrictToolModel
from .coverage_registry import CoverageRegistry


ReviewRunner = Callable[[str, Mapping[str, Any], int], CoverageReviewVerdict]


class CoverageReviewerError(RuntimeError):
    """Base error for one isolated coverage reviewer invocation."""


class RetryableCoverageReviewerError(CoverageReviewerError):
    """Transient provider/transport failure that permits same-fingerprint retry."""


class CoverageReviewerContractError(CoverageReviewerError):
    """Non-transient reviewer/schema failure that terminates this Discover attempt."""


class ReviewDiscoveryCoverageInput(StrictToolModel):
    reason: NonBlankString


def _stable_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _review_system_prompt(review_kind: str, language: str) -> str:
    chinese = language == "zh-CN"
    role = (
        "语义覆盖审计员" if review_kind == "semantic_coverage" else "对抗性漏报审计员"
    )
    if not chinese:
        role = (
            "semantic coverage auditor"
            if review_kind == "semantic_coverage"
            else "adversarial false-negative auditor"
        )
    language_rule = (
        "所有解释、问题、风险、建议和通过判据必须使用简体中文；ID、枚举值、工具名和代码保持英文。"
        if chinese
        else "Write explanations in English; keep IDs, enum values, tool names, and code in English."
    )
    focus = (
        "逐条核对 NL 的主要行为子句和有效 cue 义务是否被同强度的正向命题覆盖，并检查未被选作证据的模型行为是否会实质影响主要结论。"
        if review_kind == "semantic_coverage"
        else "主动构造能让现有断言错误通过的反例，寻找漏掉的路径、条件、guard、effect、层次、初始化、时序、完成语义以及错误 issue 投影。"
    )
    return f"""你是独立的{role}。你不参与 Discover 主 Agent 的推理，也不得信任其自称完整。

{language_rule}

审查目标：{focus}

结构化输出中的 `review_kind` 必须精确等于 `{review_kind}`。

硬规则：
1. 必须从输入中读取完整 NL、FCSTM、raw source、source trace、InputSegments、CoverageRequirements、全部行为相关 SourceFacts、CoverageUnits、Roots、每条最新断言及其真实执行记录。
2. 必须在 reviewed_segment_ids、reviewed_requirement_ids、reviewed_source_fact_ids、reviewed_root_ids 中逐项列出 review_contract 要求的全部 ID。SourceFact 只要求枚举计划明确选作断言证据的事实；完整 inventory 仍用于判断是否存在会影响主要 NL 行为结论的明显漏项。
3. 不得使用预设缺陷分类表，不得要求 D01-D12 或其他固定 taxonomy。问题类别只能从本例证据中开放式发现。
4. CoverageRequirement 被 assertion basis 引用并不等于语义覆盖。必须判断断言是否保持了原文的对象、触发条件、源状态、目标状态、数量、方向、顺序、持续性、完成范围和时间界限；弱命题必须失败。
5. SourceFact 被 Unit 引用并不等于已探索。对明确选作断言证据的事实，必须检查其是否被实际执行的断言直接支撑；对其余 inventory，只有遗漏会实质改变主要 NL 行为或 issue 结论时才作为阻塞 finding，不做模型全事实穷举验收。
6. matches 只说明一条断言为 True，不说明断言写对了；contradicts 只说明一条正向命题为 False，不自动说明 issue 归因正确。必须审查命题方向和 issue projection。
7. 仿真只证明给定轨迹，局部关系只证明局部事实，有界形式化只证明其边界和性质。证据强度不足时必须失败。
8. passed=true 仅允许在不存在会影响主要行为结论的语义漏项、弱/错向断言、潜在漏报、潜在误报、关键证据缺口或错误 issue projection 时返回。非关键 hardening 建议写入 coverage_analysis，不得为了面面俱到阻塞研究运行。
9. passed=false 时每个 finding 必须在 related_segment_ids / related_requirement_ids / related_source_fact_ids / related_root_ids / related_assertion_chain_ids 中至少给出一个 review_contract 当前台账 ID，且不得引用 review_contract 之外的 ID。
10. 每个 finding 必须同时说明新增 coverage_dimensions、recommended_tools、recommended_steps、recommended_action 和 pass_criteria：recommended_action 必须逐字点名至少一个 recommended_tools 中的工具、至少一个 related_*_ids 中的当前台账 ID，并说明具体检查对象/路径/条件；recommended_steps 必须逐工具给出关联 ID、目标、符合真实工具输入 schema 的 suggested_arguments 和预期观察，且工具集合与 recommended_tools 完全一致；pass_criteria 必须写可观察的台账或模型结果，不能只说“复审通过”。不得让主 Agent 直接改 Controller projection / runtime_issue_assessment / confirmed 状态；不得把 FBMCQ 或 read_fbmcq_guide 当作解释 NL / 自然语言语义的工具。
11. NL 明确 in-scope 的行为若在当前模型中没有表达，应按模型行为缺口或断言缺口处理；不得凭空降级为“抽象层差异”。但也不得把 NL 强化成原文没有的 only / every-state / future-model 义务。
12. 必须检查会直接制造错误主要结论的哨兵变量、硬编码候选名、过滤后凑基数和弱映射等 anti-gaming 模式；仅属理论极端而不影响本例结论的风险写入 coverage_analysis 作为改进建议。
13. 不得访问 reference/gold、不得修改模型、不得替主 Agent 修复问题。你只审查当前台账的主要行为覆盖是否足以支持本次 Discover 结论，并在 coverage_analysis 中说明覆盖边界和可选增强方向；不得宣称绝对 100% 覆盖。
14. 正向条件义务不自动产生排他性负义务。“在状态 S 收到 E 时到达 T”要求检查该条件成立时的行为；除非同一关联 NL 明确出现 only、must not、不得、禁止等排他措辞，不得进一步要求其他状态收到 E 时不能到达 T，也不得建议包含 is False 或 not(...) 的负半句来制造 issue。
15. 按 FCSTM 层次语义解释无事件迁移：复合状态的 event=None 出边可能是子机到达 final 后的 completion transition，不等于每个普通 cycle 都立即无条件触发。I_TRANSITION_NEVER_EVENT_TRIGGERED 只说明该边不由事件触发。若要声称它导致提前退出，必须引用已执行 simulation/formal 证据；结构存在本身不足以支持该结论。
16. 当前 review 发生在完整计划已经注册之后。现有工具只能 revise 已注册 assertion chain，不能新增 CoverageUnit、Root 或 assertion chain，也不能重新注册完整计划。每个 revise_assertion step 的 assertion_chain_id 必须来自 review_contract.required_assertion_chain_ids；若当前工具无法实现某建议，不得把它作为 finding 返回。
17. 建议的断言仍必须遵循正向布尔原则：True 表示现有 Root 得到满足。若 NL 明确禁止某行为，表达式应在该行为不存在时为 True；不得把“不希望存在的边确实存在”写成 True 后仍声称它会投影为 issue。

recommended_steps.suggested_arguments 必须遵守以下真实工具输入合同；示例值应替换成当前台账中的真实 ID、表达式和模型元素：
- query_model: {{"query_kind":"transitions","name_contains":null,"offset":0,"limit":50,"root_node_ids":["ROOT-..."],"reason":"..."}}；query_kind 只允许 states/events/transitions/variables/diagnostics。
- observe_trace: {{"question":"...","root_node_ids":["ROOT-..."],"cycles":[[],["Root.Event"]],"reason":"..."}}
- lookup_source_trace: {{"element_refs":["state:Root.Target"],"direction":"fcstm_to_source","reason":"..."}}；direction 只允许 fcstm_to_source/source_to_fcstm。
- read_fbmcq_guide: {{"reason":"..."}}
- register_coverage_plan: {{"plan":{{"segment_dispositions":[],"fact_dispositions":[],"coverage_units":[],"proposition_roots":[],"logical_assertions":[],"rationale":"..."}},"reason":"..."}}；实际建议必须在 plan 中给出保留全部既有义务并完成所述修订的完整 CoveragePlan，不能只写 delta/plan_change。
- revise_assertion: {{"assertion_chain_id":"ASSERT-...","assert":"一个完整正向 Python bool 表达式","reason":"..."}}
- eval_assert: {{"assert":"与 latest assertion 完全一致的表达式","reason":"..."}}
"""


class LLMCoverageReviewRunner:
    """Run isolated structured reviewers through the repository Agent framework."""

    def __init__(
        self,
        *,
        llm_registry: LLMRegistry,
        profile: str,
        audit_root: Path,
        content_language: str,
        limits: Mapping[str, int | float] | None = None,
    ) -> None:
        self.llm_registry = llm_registry
        self.profile = profile
        self.audit_root = audit_root
        self.content_language = content_language
        self.limits = dict(limits or {})

    def __call__(
        self, review_kind: str, payload: Mapping[str, Any], attempt_no: int
    ) -> CoverageReviewVerdict:
        review_dir = self.audit_root / f"review-{attempt_no:03d}-{review_kind}"
        review_dir.mkdir(parents=True, exist_ok=False)
        spec = AgentSpec(
            name=f"paper1-discover-{review_kind}-reviewer",
            system_prompt=_review_system_prompt(review_kind, self.content_language),
            tools=(),
            output_schema=CoverageReviewVerdict,
            limits=self.limits or None,
            require_tool_call=False,
            retry_missing_structured_output=True,
        )
        app = AgentApp.from_registry(
            spec,
            self.llm_registry,
            profile=self.profile,
            model_options={"streaming": True, "stream_usage": False, "max_retries": 0},
        )
        try:
            result = contextvars.Context().run(
                app.run,
                json.dumps(payload, ensure_ascii=False, sort_keys=True),
                renderer="quiet",
                log_level="INFO",
                audit_out=review_dir / "audit.jsonl",
                result_out=review_dir / "result.json",
                compact_trigger_ratio=0.85,
            )
        except Exception as exc:  # noqa: BLE001 - normalize provider/runtime drift
            _raise_classified_reviewer_error(review_kind, exc)
        if result.status != "success" or not result.real_llm:
            _raise_classified_reviewer_error(
                review_kind,
                result.error or result.status,
            )
        try:
            verdict = result.require_output()
            if not isinstance(verdict, CoverageReviewVerdict):
                verdict = CoverageReviewVerdict.model_validate(verdict)
        except Exception as exc:  # noqa: BLE001 - schema failure is non-transient
            raise CoverageReviewerContractError(
                f"coverage_reviewer_contract_failed:{review_kind}:{exc}"
            ) from exc
        if verdict.review_kind != review_kind:
            raise CoverageReviewerContractError(
                f"coverage_reviewer_kind_mismatch:{review_kind}:{verdict.review_kind}"
            )
        return verdict


def _raise_classified_reviewer_error(review_kind: str, error: Any) -> None:
    rendered = json.dumps(error, ensure_ascii=False, sort_keys=True, default=str)
    structured_tokens = _structured_error_tokens(error)
    contract_markers = (
        "schema",
        "validation",
        "structured_output",
        "response_format",
        "review_kind",
        "contract",
        "invalid_json",
    )
    transient_markers = (
        "provider_error",
        "remoteprotocolerror",
        "timeout",
        "rate_limit",
        "connection_error",
        "transport_error",
        "http_429",
        "http_500",
        "http_502",
        "http_503",
        "http_504",
    )
    if any(marker in token for token in structured_tokens for marker in contract_markers):
        error_type: type[CoverageReviewerError] = CoverageReviewerContractError
    elif any(
        marker in token for token in structured_tokens for marker in transient_markers
    ):
        error_type = RetryableCoverageReviewerError
    else:
        exception_type_name = type(error).__name__.lower()
        transient_exception_types = {
            "connectionerror",
            "connecterror",
            "connecttimeout",
            "readtimeout",
            "writetimeout",
            "pooltimeout",
            "remoteprotocolerror",
            "networkerror",
            "transporterror",
        }
        fallback = f"{type(error).__name__}:{error}".lower()
        precise_transient_patterns = (
            r"remoteprotocolerror",
            r"(?:read|connect|pool)timeout",
            r"connection (?:reset|refused|aborted)",
            r"rate limit",
            r"status code (?:429|50[0234])",
            r"incomplete chunked read",
            r"temporarily unavailable",
            r"service unavailable",
        )
        is_retryable_exception = exception_type_name in transient_exception_types
        is_retryable_message = any(
            re.search(pattern, fallback) for pattern in precise_transient_patterns
        )
        error_type = (
            RetryableCoverageReviewerError
            if is_retryable_exception or is_retryable_message
            else CoverageReviewerContractError
        )
    raise error_type(f"coverage_reviewer_failed:{review_kind}:{rendered}")


def _structured_error_tokens(value: Any) -> tuple[str, ...]:
    tokens: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() in {"code", "type", "status", "source", "category"}:
                tokens.append(str(item).lower())
            tokens.extend(_structured_error_tokens(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            tokens.extend(_structured_error_tokens(item))
    return tuple(tokens)


class CoverageReviewGate:
    """Append-only dual-review gate bound to one mutable assertion registry."""

    def __init__(
        self,
        *,
        registry: CoverageRegistry,
        task_snapshot: Mapping[str, Any],
        runner: ReviewRunner,
    ) -> None:
        self.registry = registry
        self.task_snapshot = json.loads(json.dumps(task_snapshot, ensure_ascii=False))
        self.runner = runner
        self.attempt_count = 0
        self.latest_result: dict[str, Any] | None = None
        self.terminal_failure = False

    def state_fingerprint(self) -> str:
        latest_evaluations: dict[str, Any] = {}
        for version in self.registry.latest_versions():
            attempts = self.registry.evaluations.get(version.assertion_version_id, [])
            latest_evaluations[version.assertion_version_id] = (
                attempts[-1] if attempts else None
            )
        return _stable_sha256(
            {
                "coverage_units": self.registry.coverage_units,
                "roots": self.registry.roots,
                "latest_assertions": [
                    item.to_record() for item in self.registry.latest_versions()
                ],
                "latest_evaluations": latest_evaluations,
                "requirement_assertion_chains": {
                    key: sorted(value)
                    for key, value in sorted(
                        self.registry.requirement_assertion_chains.items()
                    )
                },
                "source_fact_assertion_chains": {
                    key: sorted(value)
                    for key, value in sorted(
                        self.registry.source_fact_assertion_chains.items()
                    )
                },
            }
        )

    def current_passed(self) -> bool:
        return bool(
            self.latest_result
            and self.latest_result.get("passed") is True
            and self.latest_result.get("reviewed_state_fingerprint")
            == self.state_fingerprint()
        )

    def has_terminal_failure(self) -> bool:
        return self.terminal_failure

    def review(self, *, reason: str) -> dict[str, Any]:
        if self.terminal_failure and self.latest_result is not None:
            return json.loads(json.dumps(self.latest_result, ensure_ascii=False))
        if not self.registry.plan_registered:
            return self._reject(reason, ["coverage_plan_not_registered"])
        missing = self.registry.missing_latest_required_assertions()
        incomplete = self.registry.incomplete_latest_required_assertions()
        if missing or incomplete:
            errors = []
            if missing:
                errors.append("latest_required_assertions_not_executed")
            if incomplete:
                errors.append("latest_required_assertions_inconclusive")
            return self._reject(reason, errors)

        fingerprint = self.state_fingerprint()
        projection = self.registry.project_roots()
        payload = {
            "schema_version": "paper1.discovery_coverage_review_input.v1",
            "reviewed_state_fingerprint": fingerprint,
            "task_snapshot": self.task_snapshot,
            "registered_plan": {
                "coverage_units": self.registry.coverage_units,
                "proposition_roots": self.registry.roots,
                "latest_assertions": [
                    item.to_record() for item in self.registry.latest_versions()
                ],
            },
            "latest_evaluations": {
                version.assertion_version_id: self.registry.evaluations[
                    version.assertion_version_id
                ][-1]
                for version in self.registry.latest_versions()
            },
            "controller_projection_before_review": projection,
            "review_contract": {
                "required_segment_ids": sorted(self.registry.input_segment_ids),
                "required_requirement_ids": sorted(self.registry.coverage_requirements),
                "required_source_fact_ids": sorted(
                    self.registry.selected_source_fact_ids()
                ),
                "required_root_ids": sorted(self.registry.roots),
                "required_assertion_chain_ids": sorted(self.registry.chains),
                "pass_requires": [
                    "both_independent_reviews_pass",
                    "every_required_id_is_explicitly_reviewed",
                    "no_actionable_findings",
                    "review_fingerprint_matches_current_latest_ledger",
                ],
            },
        }
        reusable_verdicts: dict[str, CoverageReviewVerdict] = {}
        previous = self.latest_result or {}
        if (
            previous.get("execution_status") == "retryable_reviewer_failure"
            and previous.get("reviewed_state_fingerprint") == fingerprint
        ):
            reusable_verdicts = {
                verdict.review_kind: verdict
                for verdict in (
                    CoverageReviewVerdict.model_validate(item)
                    for item in previous.get("completed_review_verdicts", [])
                )
            }
        verdicts: list[CoverageReviewVerdict] = []
        for review_kind in (
            "semantic_coverage",
            "adversarial_falsification",
        ):
            if review_kind in reusable_verdicts:
                verdicts.append(reusable_verdicts[review_kind])
                continue
            self.attempt_count += 1
            try:
                verdicts.append(self.runner(review_kind, payload, self.attempt_count))
            except RetryableCoverageReviewerError as exc:
                return self._reviewer_retry_required(
                    reason=reason,
                    fingerprint=fingerprint,
                    review_kind=review_kind,
                    error=exc,
                    completed_verdicts=verdicts,
                )
            except Exception as exc:  # noqa: BLE001 - fail closed on bad review contracts
                return self._reviewer_contract_failed(
                    reason=reason,
                    fingerprint=fingerprint,
                    review_kind=review_kind,
                    error=exc,
                    completed_verdicts=verdicts,
                )

        expected = {
            "segment": self.registry.input_segment_ids,
            "requirement": set(self.registry.coverage_requirements),
            "source_fact": self.registry.selected_source_fact_ids(),
            "root": set(self.registry.roots),
        }
        programmatic_errors: list[str] = []
        invalid_finding_ids: set[str] = set()
        for verdict in verdicts:
            actual = {
                "segment": set(verdict.reviewed_segment_ids),
                "requirement": set(verdict.reviewed_requirement_ids),
                "source_fact": set(verdict.reviewed_source_fact_ids),
                "root": set(verdict.reviewed_root_ids),
            }
            for label, required_ids in expected.items():
                if actual[label] != required_ids:
                    missing_ids = sorted(required_ids - actual[label])
                    unknown_ids = sorted(actual[label] - required_ids)
                    programmatic_errors.append(
                        f"{verdict.review_kind}_{label}_review_set_mismatch:"
                        f"missing={','.join(missing_ids)}:unknown={','.join(unknown_ids)}"
                    )
            known_ids = {
                "segment": expected["segment"],
                "requirement": expected["requirement"],
                "source_fact": expected["source_fact"],
                "root": expected["root"],
                "assertion_chain": set(self.registry.chains),
            }
            for finding in verdict.findings:
                finding_ids = {
                    "segment": set(finding.related_segment_ids),
                    "requirement": set(finding.related_requirement_ids),
                    "source_fact": set(finding.related_source_fact_ids),
                    "root": set(finding.related_root_ids),
                    "assertion_chain": set(finding.related_assertion_chain_ids),
                }
                for label, ids in finding_ids.items():
                    unknown = sorted(ids - known_ids[label])
                    if unknown:
                        invalid_finding_ids.add(finding.finding_id)
                        programmatic_errors.append(
                            f"{verdict.review_kind}_finding_unknown_{label}_ids:"
                            f"finding={finding.finding_id}:unknown={','.join(unknown)}"
                        )
                if _finding_strengthens_frozen_nl(
                    finding,
                    _finding_nl_scopes(finding, self.task_snapshot),
                ):
                    invalid_finding_ids.add(finding.finding_id)
                    programmatic_errors.append(
                        f"{verdict.review_kind}_finding_nl_strengthening:"
                        f"finding={finding.finding_id}"
                    )
                for error in _finding_step_contract_errors(
                    finding,
                    known_assertion_chain_ids=set(self.registry.chains),
                ):
                    invalid_finding_ids.add(finding.finding_id)
                    programmatic_errors.append(
                        f"{verdict.review_kind}_{error}:"
                        f"finding={finding.finding_id}"
                    )

        passed = not programmatic_errors and all(item.passed for item in verdicts)
        finding_actions = [
            finding.model_dump(mode="json")
            for verdict in verdicts
            for finding in verdict.findings
            if finding.finding_id not in invalid_finding_ids
        ]
        previous = self.latest_result or {}
        if (
            programmatic_errors
            and previous.get("execution_status") == "completed"
            and previous.get("reviewed_state_fingerprint") == fingerprint
            and previous.get("programmatic_errors") == programmatic_errors
        ):
            return self._reviewer_contract_failed(
                reason=reason,
                fingerprint=fingerprint,
                review_kind="programmatic_contract",
                error=CoverageReviewerContractError(
                    "repeated_programmatic_review_mismatch:"
                    + "|".join(programmatic_errors)
                ),
                completed_verdicts=verdicts,
            )
        result = {
            "execution_status": "completed",
            "passed": passed,
            "reviewed_state_fingerprint": fingerprint,
            "review_verdicts": [item.model_dump(mode="json") for item in verdicts],
            "programmatic_errors": programmatic_errors,
            "required_actions": [
                *finding_actions,
                *_programmatic_review_actions(programmatic_errors),
            ],
            "reason": reason,
            "limitations": [] if passed else ["semantic_coverage_review_failed"],
        }
        record = self.registry.append_record(
            "discovery_coverage_review_completed", result
        )
        result["record_id"] = record["record_id"]
        self.latest_result = json.loads(json.dumps(result, ensure_ascii=False))
        self.registry.latest_projection = None
        return result

    def _reviewer_retry_required(
        self,
        *,
        reason: str,
        fingerprint: str,
        review_kind: str,
        error: Exception,
        completed_verdicts: list[CoverageReviewVerdict],
    ) -> dict[str, Any]:
        """Return a structured retry action instead of crashing the top-level Agent.

        Provider streaming failures and transient reviewer runtime errors are
        infrastructure failures, not evidence that the current ledger passed or
        failed semantically.  The gate therefore appends a failed review record,
        preserves the assertion/plan ledger, and asks the Agent to retry the same
        `review_discovery_coverage` call against the unchanged fingerprint.
        """

        previous = self.latest_result or {}
        if (
            previous.get("execution_status") == "retryable_reviewer_failure"
            and previous.get("reviewed_state_fingerprint") == fingerprint
        ):
            return self._reviewer_contract_failed(
                reason=reason,
                fingerprint=fingerprint,
                review_kind=review_kind,
                error=CoverageReviewerContractError(
                    "repeated_reviewer_infrastructure_failure:"
                    f"previous={previous.get('failed_review_kind')}:current={review_kind}"
                ),
                completed_verdicts=completed_verdicts,
            )

        error_type = type(error).__name__
        error_message = str(error)
        result = {
            "execution_status": "retryable_reviewer_failure",
            "passed": False,
            "reviewed_state_fingerprint": fingerprint,
            "failed_review_kind": review_kind,
            "completed_review_verdicts": [
                item.model_dump(mode="json") for item in completed_verdicts
            ],
            "errors": [f"coverage_reviewer_retryable_failure:{review_kind}:{error_type}"],
            "required_actions": [
                {
                    "action_id": "REVIEW-INFRA-RETRY-001",
                    "action_kind": "reviewer_infrastructure_retry",
                    "reviewed_state_fingerprint": fingerprint,
                    "failed_review_kind": review_kind,
                    "coverage_dimensions": ["reviewer_infrastructure"],
                    "problem": (
                        "Independent coverage reviewer failed before returning a "
                        "structured verdict; the semantic ledger has not been "
                        "accepted as covered."
                    ),
                    "missed_behavior_risk": (
                        "Treating a provider or streaming interruption as a tool "
                        "exception aborts the top-level Agent and loses the chance "
                        "to retry without changing the evidence ledger."
                    ),
                    "recommended_tools": ["review_discovery_coverage"],
                    "recommended_action": (
                        "Keep the coverage plan, latest assertions, and evaluations "
                        "unchanged, then call review_discovery_coverage again for "
                        "the same reviewed_state_fingerprint. Do not revise "
                        "assertions unless a later successful reviewer returns "
                        "semantic findings."
                    ),
                    "pass_criteria": (
                        "A later review_discovery_coverage call on the same current "
                        "fingerprint returns execution_status=completed with both "
                        "reviewers producing structured verdicts and no retryable "
                        "reviewer failure."
                    ),
                    "record_language": "en-US",
                    "error_type": error_type,
                    "error_message": error_message,
                }
            ],
            "reason": reason,
            "limitations": [
                "semantic_coverage_review_failed",
                "reviewer_infrastructure_retry_required",
            ],
        }
        record = self.registry.append_record(
            "discovery_coverage_review_retry_required", result
        )
        result["record_id"] = record["record_id"]
        self.latest_result = json.loads(json.dumps(result, ensure_ascii=False))
        return result

    def _reviewer_contract_failed(
        self,
        *,
        reason: str,
        fingerprint: str,
        review_kind: str,
        error: Exception,
        completed_verdicts: list[CoverageReviewVerdict],
    ) -> dict[str, Any]:
        result = {
            "execution_status": "reviewer_contract_failure",
            "passed": False,
            "reviewed_state_fingerprint": fingerprint,
            "failed_review_kind": review_kind,
            "completed_review_verdicts": [
                item.model_dump(mode="json") for item in completed_verdicts
            ],
            "errors": [
                f"coverage_reviewer_contract_failure:{review_kind}:"
                f"{type(error).__name__}"
            ],
            "required_actions": [
                {
                    "action_id": "REVIEW-INFRA-STOP-001",
                    "action_kind": "reviewer_contract_failure",
                    "reviewed_state_fingerprint": fingerprint,
                    "failed_review_kind": review_kind,
                    "recommended_tools": [],
                    "recommended_action": (
                        "Stop the current Discover attempt and preserve its audit "
                        "artifacts. This deterministic reviewer/schema failure cannot "
                        "be repaired by changing the semantic ledger or repeatedly "
                        "calling review_discovery_coverage."
                    ),
                    "pass_criteria": (
                        "A later clean run uses a corrected reviewer contract and both "
                        "reviewers return valid structured verdicts."
                    ),
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                }
            ],
            "reason": reason,
            "limitations": [
                "semantic_coverage_review_failed",
                "reviewer_contract_failure",
            ],
        }
        record = self.registry.append_record(
            "discovery_coverage_review_contract_failed", result
        )
        result["record_id"] = record["record_id"]
        self.latest_result = json.loads(json.dumps(result, ensure_ascii=False))
        self.terminal_failure = True
        return result

    def _reject(self, reason: str, errors: list[str]) -> dict[str, Any]:
        result = {
            "execution_status": "prerequisite_required",
            "passed": False,
            "errors": errors,
            "required_actions": _review_prerequisite_actions(errors),
            "reason": reason,
            "limitations": ["review_requires_terminal_registered_assertions"],
        }
        self.registry.append_record("discovery_coverage_review_rejected", result)
        return result


def _finding_strengthens_frozen_nl(
    finding: Any,
    frozen_nl_scopes: tuple[str, ...],
) -> bool:
    suggested_arguments = [
        step.suggested_arguments for step in finding.recommended_steps
    ]
    action = "\n".join(
        [
            finding.recommended_action,
            finding.pass_criteria,
            json.dumps(suggested_arguments, ensure_ascii=False, sort_keys=True),
        ]
    ).lower()
    quantifier_groups = (
        (
            (r"\bonly\b", r"只能", r"仅允许"),
            (r"\bonly\b", r"只能", r"仅允许"),
        ),
        (
            (
                r"\b(?:all|every|each)[- ]states?\b",
                r"(?:所有|全部|每个|任意)状态",
            ),
            (
                r"\b(?:all|every|each)[- ]states?\b",
                r"(?:所有|全部|每个|任意)状态",
            ),
        ),
        (
            (r"future[- ]model", r"未来模型"),
            (r"future[- ]model", r"未来模型"),
        ),
    )
    for action_patterns, nl_patterns in quantifier_groups:
        action_uses_quantifier = any(
            re.search(pattern, action, re.I) for pattern in action_patterns
        )
        every_scope_authorizes = bool(frozen_nl_scopes) and all(
            any(re.search(pattern, scope, re.I) for pattern in nl_patterns)
            for scope in frozen_nl_scopes
        )
        if action_uses_quantifier and not every_scope_authorizes:
            return True
    negative_action_patterns = (
        r"\bis\s+false\b",
        r"\bmust\s+not\b",
        r"\bshall\s+not\b",
        r"\bnever\b",
        r"\bnot\s+(?:transition_exists|simulate|fbmcq|effects|guards_overlap)\b",
        r"不应",
        r"不得",
        r"禁止",
        r"不允许",
    )
    negative_nl_patterns = (
        r"\bonly\b",
        r"\bmust\s+not\b",
        r"\bshall\s+not\b",
        r"\bnever\b",
        r"\bnot\b",
        r"只能",
        r"仅允许",
        r"不应",
        r"不得",
        r"禁止",
        r"不允许",
    )
    action_adds_negative_obligation = any(
        re.search(pattern, action, re.I) for pattern in negative_action_patterns
    )
    every_scope_authorizes_negative = bool(frozen_nl_scopes) and all(
        any(re.search(pattern, scope, re.I) for pattern in negative_nl_patterns)
        for scope in frozen_nl_scopes
    )
    return action_adds_negative_obligation and not every_scope_authorizes_negative


def _finding_step_contract_errors(
    finding: Any,
    *,
    known_assertion_chain_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    if "register_coverage_plan" in set(finding.recommended_tools):
        errors.append("finding_cannot_reregister_plan_after_review")
    for step in finding.recommended_steps:
        if step.tool == "register_coverage_plan":
            errors.append("finding_cannot_reregister_plan_after_review")
            continue
        if step.tool != "revise_assertion":
            continue
        assertion_chain_id = step.suggested_arguments.get("assertion_chain_id")
        if assertion_chain_id not in known_assertion_chain_ids:
            errors.append(
                "finding_unknown_revise_assertion_chain:"
                f"unknown={assertion_chain_id}"
            )
    return sorted(set(errors))


def _finding_nl_scopes(
    finding: Any, task_snapshot: Mapping[str, Any]
) -> tuple[str, ...]:
    current_records = task_snapshot.get("current_records", {})
    if not isinstance(current_records, Mapping):
        return ()
    selected: list[str] = []
    requirement_ids = set(finding.related_requirement_ids)
    for requirement in current_records.get("coverage_requirements", []):
        if not isinstance(requirement, Mapping):
            continue
        if str(requirement.get("requirement_id", "")) in requirement_ids:
            selected.append(str(requirement.get("clause_text", "")))
    if not selected:
        segment_ids = set(finding.related_segment_ids)
        for segment in current_records.get("input_segments", []):
            if not isinstance(segment, Mapping):
                continue
            if str(segment.get("segment_id", "")) in segment_ids:
                selected.append(str(segment.get("text", "")))
    return tuple(item for item in selected if item)


def _programmatic_review_actions(errors: list[str]) -> list[dict[str, Any]]:
    """Give the main Agent a concrete recovery path for reviewer ID omissions."""

    return [
        {
            "action_id": f"REVIEW-CONTRACT-{ordinal:03d}",
            "action_kind": "reviewer_contract_retry",
            "coverage_dimensions": ["reviewer_infrastructure"],
            "problem": error,
            "missed_behavior_risk": (
                "The independent reviewer did not explicitly close the complete "
                "Controller-required ID set, so a full-coverage claim is unsupported."
            ),
            "recommended_action": (
                "Keep the ledger unchanged and call review_discovery_coverage again. "
                "The replacement review must explicitly enumerate every required ID; "
                "if the mismatch repeats, end the run as reviewer-infrastructure failure."
            ),
            "recommended_tools": ["review_discovery_coverage"],
            "pass_criteria": (
                "Both reviewers enumerate exactly every required Segment, Requirement, "
                "SourceFact, and Root ID with no missing or unknown ID."
            ),
            "record_language": "en-US",
        }
        for ordinal, error in enumerate(errors, start=1)
    ]


def _review_prerequisite_actions(errors: list[str]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for ordinal, error in enumerate(errors, start=1):
        if error == "coverage_plan_not_registered":
            tools = ["register_coverage_plan"]
            action = (
                "Do not call review_discovery_coverage again. Read the latest "
                "register_coverage_plan required_actions, correct the complete plan "
                "while preserving every frozen NL obligation, and call "
                "register_coverage_plan. Use only the SourceFacts relevant to the "
                "major NL behavior being checked."
            )
            criteria = "register_coverage_plan returns accepted=true."
        elif error == "latest_required_assertions_not_executed":
            tools = ["eval_assert"]
            action = (
                "Execute every missing latest required assertion exactly as registered."
            )
            criteria = "No latest required assertion remains without an evaluation."
        else:
            tools = ["revise_assertion", "eval_assert"]
            action = (
                "Revise each inconclusive latest assertion without weakening its "
                "obligation, then execute every new latest version."
            )
            criteria = (
                "Every latest required assertion has a terminal evidence-backed bool."
            )
        actions.append(
            {
                "action_id": f"REVIEW-PREREQ-{ordinal:03d}",
                "error": error,
                "problem": (
                    "The independent reviewers cannot run because a required "
                    "Discover prerequisite is not yet closed."
                ),
                "recommended_tools": tools,
                "recommended_action": action,
                "coverage_improvement": (
                    "Following this action closes the actual prerequisite instead "
                    "of repeating a review call that cannot inspect the ledger."
                ),
                "pass_criteria": criteria,
            }
        )
    return actions


def build_tool(gate: CoverageReviewGate) -> SimpleStructuredTool:
    """Build the mandatory semantic-completeness review tool for Discover."""

    def review_discovery_coverage(reason: str) -> dict[str, Any]:
        """Purpose
        -------
        独立审查当前 Discover 台账的主要行为覆盖是否足以支持本次结论。

        When to use
        -----------
        与 ``eval_assert`` 同级的业务工具。所有最新 required assertion
        已执行并得到 terminal bool 后必须调用；只有返回 ``passed=true``，且返回的
        ``reviewed_state_fingerprint`` 仍对应当前最新台账，才允许最终提交。

        When not to use
        ----------------
        不得在 coverage plan 注册前、仍有未执行/inconclusive 断言时调用，也不得
        用旧 pass 覆盖后续 revision/eval 产生的新台账。

        Parameters
        ----------
        ``reason`` 是本次发起复审的自然语言理由，将原样写入 append-only
        record。无路径、模型、ID 列表或 verdict 输入，避免主 Agent 篡改审查范围。

        Returns
        -------
        ``passed``、台账指纹、两个完整结构化 verdict、程序化 ID 闭包错误、
        ``required_actions`` 和 record ID。每个语义 finding 都包含关联台账 ID、当前
        缺口、漏报风险、建议调用的现有工具、具体补查动作和明确通过判据，可直接
        指导主 Agent 增强覆盖后再次调用本工具。reviewer 基础设施 action 改为绑定
        fingerprint 和 review kind，不伪造语义台账 ID。

        Execution
        ---------
        工具把完整 NL、FCSTM、raw source、source trace、全部
        InputSegments/CoverageRequirements/SourceFacts、CoverageUnits/Roots、最新断言、
        真实执行 trace 和 Controller projection 交给两个隔离上下文、无其他工具的
        LLM reviewer。第一个逐条审计语义覆盖，第二个主动构造漏报/误报反例。
        Controller 不向 reviewer 提供固定缺陷 taxonomy，也不预设问题。

        Failure semantics
        -----------------
        未注册计划、仍有未执行或 inconclusive 断言时 fail closed；任一
        reviewer 报告缺口、漏掉任何必须审查的 Segment/Requirement/SourceFact/Root
        ID，或审查后台账发生 revision/eval 变化，均不能沿用旧 pass。provider/stream
        临时失败先由 Agent runtime 对同一 profile 和同一请求透明重发最多两次；重发耗尽后
        不会把 provider 故障冒充语义 verdict。工具会保留同轮已完成 verdict，并 append 一个
        passed=false、execution_status=retryable_reviewer_failure 的结构化记录，要求在不修改
        当前 coverage plan / assertion / evaluation 台账的情况下重试 review。不得把失败
        review 当作终态结果；必须按 required_actions 补查或重试并重新 review。
        schema-invalid verdict、错误 review kind 等确定性合同失败返回
        reviewer_contract_failure，终止当前 Discover attempt，不得冒充临时 provider
        故障反复重试。

        Method-boundary calibration
        ---------------------------
        reviewer 的建议必须可由现有工具执行，逐字点名建议工具和至少一个关联台账 ID，
        并在 recommended_steps 中逐工具说明目标、参数/模型范围和预期观察，再给出新增覆盖
        维度、总体动作和可观察通过条件。不得建议用 FBMCQ 解释 NL，不得要求主 Agent 直接修改 Controller
        projection 状态，不得引用 review_contract 之外 ID。NL 明确 in-scope 的行为若
        模型无表达，应视作模型行为/断言缺口；不得凭空降级为抽象层差异，也不得
        把 NL 强化成 only/every-state/future-model 或未授权负义务。复合状态的
        event=None 出边按 completion transition 校准，不能仅凭结构存在声称它会在
        普通 cycle 立即触发。review 后只能修订现有 assertion chain，不能建议新增
        Unit、Root、chain 或重新注册计划；程序化无效 finding 不会转发给主 Agent。
        reviewer 必须攻击哨兵变量、硬编码候选名和过滤后凑基数等 anti-gaming 覆盖。

        Evidence limitations
        --------------------
        reviewer pass 只对应输入中完整、当前的冻结任务与证据台账；任何后续台账
        变化都会使其过期。它不访问隐藏 gold，也不替代下游实验评价。

        Permissions
        -----------
        只读取当前运行冻结输入和 append-only Discover 台账；内部 reviewer
        不具备工具、文件、网络、reference/gold、Repair、Confirm 或模型修改权限。

        Examples
        --------
        ``{"reason":"全部最新断言已稳定执行，请独立攻击漏项和弱证据并给出补查建议。"}``
        """

        return gate.review(reason=reason)

    return SimpleStructuredTool(
        func=review_discovery_coverage,
        name="review_discovery_coverage",
        description=review_discovery_coverage.__doc__ or "review_discovery_coverage",
        args_schema=ReviewDiscoveryCoverageInput,
    )
