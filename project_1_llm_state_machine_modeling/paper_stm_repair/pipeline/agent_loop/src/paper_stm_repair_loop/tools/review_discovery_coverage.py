from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Mapping

from pydantic import Field

from utils.agent import AgentApp, AgentSpec
from utils.llm import LLMRegistry

from ..schemas.coverage_review import CoverageReviewVerdict
from ..schemas.tools import SimpleStructuredTool, StrictToolModel
from .coverage_registry import CoverageRegistry


ReviewRunner = Callable[[str, Mapping[str, Any], int], CoverageReviewVerdict]


class ReviewDiscoveryCoverageInput(StrictToolModel):
    reason: str = Field(min_length=1)


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
        "逐条核对 NL 原子子句和 cue 义务是否被同强度的正向命题覆盖，并逐条核对全部行为相关 SourceFact 是否真正进入探索范围。"
        if review_kind == "semantic_coverage"
        else "主动构造能让现有断言错误通过的反例，寻找漏掉的路径、条件、guard、effect、层次、初始化、时序、完成语义以及错误 issue 投影。"
    )
    return f"""你是独立的{role}。你不参与 Discover 主 Agent 的推理，也不得信任其自称完整。

{language_rule}

审查目标：{focus}

结构化输出中的 `review_kind` 必须精确等于 `{review_kind}`。

硬规则：
1. 必须从输入中读取完整 NL、FCSTM、raw source、source trace、InputSegments、CoverageRequirements、全部行为相关 SourceFacts、CoverageUnits、Roots、每条最新断言及其真实执行记录。
2. 必须在 reviewed_segment_ids、reviewed_requirement_ids、reviewed_source_fact_ids、reviewed_root_ids 中逐项列出本次实际审查的全部 ID。不得只写数量，不得省略看似无关的元素。
3. 不得使用预设缺陷分类表，不得要求 D01-D12 或其他固定 taxonomy。问题类别只能从本例证据中开放式发现。
4. CoverageRequirement 被 assertion basis 引用并不等于语义覆盖。必须判断断言是否保持了原文的对象、触发条件、源状态、目标状态、数量、方向、顺序、持续性、完成范围和时间界限；弱命题必须失败。
5. SourceFact 被 Unit 引用并不等于已探索。必须检查它是否被相关断言、模型查询、仿真、形式化性质或 source-trace 证据实际考虑；遗漏模型行为必须失败。
6. matches 只说明一条断言为 True，不说明断言写对了；contradicts 只说明一条正向命题为 False，不自动说明 issue 归因正确。必须审查命题方向和 issue projection。
7. 仿真只证明给定轨迹，局部关系只证明局部事实，有界形式化只证明其边界和性质。证据强度不足时必须失败。
8. passed=true 仅允许在不存在任何语义漏项、未审计模型行为、弱/错向断言、潜在漏报、潜在误报、证据缺口或错误 issue projection 时返回。
9. passed=false 时每个 finding 必须在 related_segment_ids / related_requirement_ids / related_source_fact_ids / related_root_ids / related_assertion_chain_ids 中至少给出一个当前台账 ID，并给出具体风险、可执行的 recommended_action、现有 recommended_tools 和明确 pass_criteria，以便主 Agent 直接补查后复审。recommended_action 不得只是重复审查意见，必须说明新增检查覆盖哪条行为、路径、条件或证据维度，以及怎样修改当前断言或补充探索。禁止只写泛泛建议或虚构 ID。
10. 不得访问 reference/gold、不得修改模型、不得替主 Agent 修复问题。你只审查当前台账是否足以支持“本次 Discover 已全覆盖”的结论。
"""


class LLMCoverageReviewRunner:
    """Run isolated structured reviewers through the repository Agent framework."""

    def __init__(
        self,
        *,
        llm_registry: LLMRegistry,
        profiles: Mapping[str, str],
        audit_root: Path,
        content_language: str,
        limits: Mapping[str, int | float] | None = None,
    ) -> None:
        self.llm_registry = llm_registry
        self.profiles = dict(profiles)
        self.audit_root = audit_root
        self.content_language = content_language
        self.limits = dict(limits or {})

    def __call__(
        self, review_kind: str, payload: Mapping[str, Any], attempt_no: int
    ) -> CoverageReviewVerdict:
        profile = self.profiles[review_kind]
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
            profile=profile,
            model_options={"streaming": True, "stream_usage": False, "max_retries": 0},
        )
        result = app.run(
            json.dumps(payload, ensure_ascii=False, sort_keys=True),
            renderer="quiet",
            log_level="INFO",
            audit_out=review_dir / "audit.jsonl",
            result_out=review_dir / "result.json",
            compact_trigger_ratio=0.85,
        )
        if result.status != "success" or not result.real_llm:
            raise RuntimeError(
                f"coverage_reviewer_failed:{review_kind}:"
                f"{result.error or result.status}"
            )
        verdict = result.require_output()
        if not isinstance(verdict, CoverageReviewVerdict):
            verdict = CoverageReviewVerdict.model_validate(verdict)
        if verdict.review_kind != review_kind:
            raise ValueError(
                f"coverage_reviewer_kind_mismatch:{review_kind}:{verdict.review_kind}"
            )
        return verdict


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

    def review(self, *, reason: str) -> dict[str, Any]:
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
                "required_source_fact_ids": sorted(self.registry.source_fact_ids),
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
        verdicts: list[CoverageReviewVerdict] = []
        for review_kind in (
            "semantic_coverage",
            "adversarial_falsification",
        ):
            self.attempt_count += 1
            verdicts.append(self.runner(review_kind, payload, self.attempt_count))

        expected = {
            "segment": self.registry.input_segment_ids,
            "requirement": set(self.registry.coverage_requirements),
            "source_fact": self.registry.source_fact_ids,
            "root": set(self.registry.roots),
        }
        programmatic_errors: list[str] = []
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
                        programmatic_errors.append(
                            f"{verdict.review_kind}_finding_unknown_{label}_ids:"
                            f"finding={finding.finding_id}:unknown={','.join(unknown)}"
                        )

        passed = not programmatic_errors and all(item.passed for item in verdicts)
        finding_actions = [
            finding.model_dump(mode="json")
            for verdict in verdicts
            for finding in verdict.findings
        ]
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


def _programmatic_review_actions(errors: list[str]) -> list[dict[str, Any]]:
    """Give the main Agent a concrete recovery path for reviewer ID omissions."""

    return [
        {
            "finding_id": f"REVIEW-CONTRACT-{ordinal:03d}",
            "category": "evidence_gap",
            "related_segment_ids": [],
            "related_requirement_ids": [],
            "related_source_fact_ids": [],
            "related_root_ids": [],
            "related_assertion_chain_ids": [],
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
                "Register the complete coverage plan, preserving every frozen NL "
                "obligation and behavior SourceFact, before requesting review."
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
                "recommended_tools": tools,
                "recommended_action": action,
                "pass_criteria": criteria,
            }
        )
    return actions


def build_tool(gate: CoverageReviewGate) -> SimpleStructuredTool:
    """Build the mandatory semantic-completeness review tool for Discover."""

    def review_discovery_coverage(reason: str) -> dict[str, Any]:
        """Purpose
        -------
        独立审查当前 Discover 台账能否支持“全覆盖”结论。

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
        ``required_actions`` 和 record ID。每个 required action 都包含关联 ID、当前
        缺口、漏报风险、建议调用的现有工具、具体补查动作和明确通过判据，可直接
        指导主 Agent 增强覆盖后再次调用本工具。

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
        ID，或审查后台账发生 revision/eval 变化，均不能沿用旧 pass。不得把失败
        review 当作终态结果；必须按 required_actions 补查并重新 review。

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
