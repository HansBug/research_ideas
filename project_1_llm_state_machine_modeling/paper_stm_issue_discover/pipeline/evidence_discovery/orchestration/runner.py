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
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator

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
    SemanticAdjudication,
    StageReceipt,
    assemble_method_response,
    bind_candidate,
    build_contract_prompt,
    build_d_adjudication_prompt,
    build_d_correction_prompt,
    build_grounding_prompt,
    canonical_contract_id,
    canonicalize_grounding_response,
    contract_semantic_key,
    fallback_contracts,
    fallback_d_adjudication,
    fallback_grounding,
    materialize_segment_coverage,
    materialize_v27_frontier,
    normalize_contract_state_roles,
    resolve_state_ref,
    resolve_transition_ref,
)
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
    JUDGE_MAX_STRUCTURED_OUTPUT_TOKENS,
    PROVIDER_CALL_DEADLINE_SECONDS,
    PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS,
    STRUCTURED_STAGE_DEADLINE_SECONDS,
    TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS,
    FixtureStructuredRuntime,
    PublicStructuredRuntime,
    StructuredCallOutcome,
)

REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS = ("0004", "0023", "0029", "0035", "0046", "0053")
METHOD_CELL_SCHEMA = "paper1.evidence_discovery.method_cell.v8"
JUDGE_SCHEMA = "paper1.evidence_discovery.independent_judge.v5"
SUMMARY_SCHEMA = "paper1.evidence_discovery.run_summary.v2"
RUN_MANIFEST_SCHEMA = "paper1.evidence_discovery.run_manifest.v2"
CODE_VERSION = "evidence-discovery-v27-flow.v29"
PROMPT_SCHEMA_VERSION = "evidence-discovery-v27-prompts.v25"
JUDGE_EXACT_IDENTITY_CONTRACT_VERSION = "paper1.judge-exact-identity-contract.v1"


JudgeRelation = Literal[
    "exact",
    "semantic_equivalent",
    "candidate_subsumes_ledger",
    "ledger_subsumes_candidate",
    "partial_overlap",
    "same_cause_different_property",
    "unrelated",
]
_HIT_JUDGE_RELATIONS = frozenset(
    {"exact", "semantic_equivalent", "candidate_subsumes_ledger"}
)


class JudgeRelationAssessment(BaseModel):
    """一个 release issue 与一个 frozen ledger item 的显式语义关系。

    independent pair-wide judge 产生该对象，metrics 只把 exact、
    semantic_equivalent 和有完整蕴含依据的 candidate_subsumes_ledger 计为 hit。
    它不改写 method release；负关系可稀疏记录，无需生成 ledger×release 矩阵。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.judge-relation.v1"] = Field(
        default="paper1.judge-relation.v1",
        description="JudgeRelationAssessment 的持久化 schema 版本。",
    )
    ledger_id: str = Field(
        min_length=1,
        description="本关系比较的 exact frozen ledger ID；只能来自当前 pair-wide judge 输入。",
    )
    issue_id: str = Field(
        min_length=1,
        description="本关系比较的 exact D1/D2 release issue ID；不得引用 D0 或未发布 candidate。",
    )
    relation: JudgeRelation = Field(
        description=(
            "同 locus/property/scope 下的闭集关系。D1 ledger 与 D1 release 若表达相同的"
            "主要缺陷读法并保留相容的另一种称职读法，alternative survives 本身不使其降为"
            "partial_overlap；same cause、wrong source、different property 或不相容 scope 仍不得升级为 hit。"
            "当 candidate 只覆盖 ledger 明确枚举的一个 sibling/component 时必须使用"
            "ledger_subsumes_candidate 或 partial_overlap。多个这种非 hit candidate 不能"
            "通过集合并集升级为 hit；每个计入 matched/accounted 的 issue 都必须独立具有"
            "exact、semantic_equivalent 或 candidate_subsumes_ledger 关系。"
        ),
    )
    entailment_basis: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "仅 candidate_subsumes_ledger 必填：说明 candidate 自身主张如何逻辑上建立完整"
            "ledger defect。ledger 明确枚举多个 sibling scope/event/component 时，candidate"
            "必须覆盖或蕴含全部组件；不得从 ledger detail 反向补全 candidate，shared cause"
            "或 narrow manifestation 不是蕴含。"
        ),
    )
    reason: str = Field(
        min_length=1,
        description="解释 locus、property、scope 和方向为何形成该 relation。",
    )
    basis: str = Field(
        min_length=1,
        description="引用 supplied compact ledger/release 语义字段；不得读取 method audit tree 或历史结果。",
    )

    @model_validator(mode="after")
    def validate_subsumption_basis(self) -> JudgeRelationAssessment:
        """Require explicit entailment only for the relation that can broaden a hit."""

        if self.relation == "candidate_subsumes_ledger" and not self.entailment_basis:
            raise ValueError(
                "candidate_subsumes_ledger requires non-empty entailment_basis "
                "showing that the candidate establishes the complete ledger defect"
            )
        return self


class LedgerAssessment(BaseModel):
    """Independent judge assessment for one frozen ledger entry."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    ledger_id: str = Field(min_length=1, description="Frozen ledger entry ID being assessed; copy it exactly from judge input.")
    hit_r1: bool = Field(default=False, description="Whether method round 1 contains a semantically identical release issue.")
    hit_r2: bool = Field(default=False, description="Whether method round 2 contains a semantically identical release issue.")
    hit_r3: bool = Field(default=False, description="Whether method round 3 contains a semantically identical release issue.")
    matched_issue_ids: list[str] = Field(
        default_factory=list,
        description=(
            "支持该 ledger round hit 的 exact supplied method issue IDs。每个 ID 都必须"
            "独立拥有 exact、semantic_equivalent 或 candidate_subsumes_ledger typed relation，"
            "并在对应 ReleaseAssessment.accounted_ledger_ids 中反向出现。不得把多个"
            "ledger_subsumes_candidate/partial_overlap 子集 issue 合并后当作一个 hit；若没有"
            "单条 release 建立完整 ledger defect，此列表为空且对应 hit_rN=false。"
        ),
    )
    reason: str = Field(min_length=1, description="Non-empty explanation of why this ledger item is or is not semantically matched.")
    basis: str = Field(min_length=1, description="Non-empty evidence basis for this ledger assessment, tied to the supplied ledger and method release data.")


class ReleaseAssessment(BaseModel):
    """Independent judge assessment for one released method issue."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    issue_id: str = Field(
        min_length=1,
        description=(
            "被裁定的 exact released method issue ID，必须从 judge input 原样复制。"
            "每个 supplied issue ID 都需要独立一行；即使多个 release 在语义上重复、"
            "共享 cause 或映射到同一 ledger，也不得合并、去重或省略其中任何一行。"
        ),
    )
    accounted_ledger_ids: list[str] = Field(
        default_factory=list,
        description=(
            "以 hit-eligible typed relation 完整解释该 release 的 exact frozen ledger IDs。"
            "每个 pair 必须在 ledger-side matched_issue_ids 中反向出现，且 relation 只能是"
            "exact、semantic_equivalent 或带完整 entailment_basis 的 candidate_subsumes_ledger。"
            "ledger_subsumes_candidate、partial_overlap、same_cause_different_property 和"
            "unrelated 必须保持未计账，即使多个 subset release 的并集看似覆盖 ledger。"
            "空列表精确表示没有 hit-eligible ledger relation。"
        ),
    )
    is_false_positive: bool = Field(description="True exactly when accounted_ledger_ids is empty. A true value means reason and basis must explain why no hit-eligible ledger relation exists; they must not describe the release as matching a frozen defect.")
    reason: str = Field(min_length=1, description="Non-empty explanation consistent with is_false_positive and accounted_ledger_ids: explain the accepted hit relation when accounted, or the locus/property/scope/direction mismatch when false positive.")
    basis: str = Field(min_length=1, description="Non-empty supplied ledger/release evidence consistent with the release decision; it must not claim a semantic match that the accounting and typed relations omit.")


class JudgeResponse(BaseModel):
    """Complete independent judge response with rationale for all decisions."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    ledger_assessments: list[LedgerAssessment] = Field(default_factory=list, description="Exactly one assessment for every frozen ledger item supplied to the judge; never split one ledger ID into multiple rows.")
    release_assessments: list[ReleaseAssessment] = Field(
        default_factory=list,
        description=(
            "supplied release surface 中每个 exact method issue 各一行且仅一行。该列表"
            "按 issue identity 完整覆盖，不按语义相似性 deduplicate；两个 release 即使"
            "具有相同 locus/property/cause，也必须保留各自的 ReleaseAssessment。"
        ),
    )
    relation_assessments: list[JudgeRelationAssessment] = Field(
        default_factory=list,
        description=(
            "Plausible ledger/release pair 的 sparse typed relations。每个 claimed hit/accounting"
            " pair 必须且只能有一行 hit-eligible relation；负关系可稀疏保留。relation 是逐"
            " candidate 判断，禁止把多个 ledger_subsumes_candidate 或 partial_overlap 行的"
            "集合并集升级成 ledger hit，也禁止生成完整 unrelated 矩阵。"
        ),
    )
    reason: str = Field(min_length=1, description="Non-empty explanation of the judge's overall assessment decision.")
    basis: str = Field(min_length=1, description="Non-empty basis identifying the supplied ledger and method release facts used by the judge.")


class ExactJudgeResponse(JudgeResponse):
    """Per-call judge response whose exact input identities are runtime-bound.

    The runner specializes this Pydantic model for one pair-wide judge input.
    Its validator has authority only over structural identity closure, symmetric
    accounting, round booleans, and typed-reference consistency. It never
    chooses or rewrites a semantic relation, hit, or false-positive decision.
    """

    expected_ledger_ids: ClassVar[tuple[str, ...]] = ()
    expected_release_ids: ClassVar[tuple[str, ...]] = ()
    supplied_rounds: ClassVar[int] = 0
    enforce_exact_identity_contract: ClassVar[bool] = False

    @model_validator(mode="after")
    def validate_exact_identity_contract(self) -> ExactJudgeResponse:
        """Reject structurally incomplete pair-wide accounting in the schema path."""

        if not type(self).enforce_exact_identity_contract:
            return self
        errors = _judge_contract_errors(
            self,
            expected_ledger=type(self).expected_ledger_ids,
            expected_release=type(self).expected_release_ids,
            rounds=type(self).supplied_rounds,
        )
        if errors:
            raise ValueError(
                "exact pair-wide judge identity contract failed:\n- "
                + "\n- ".join(errors)
            )
        return self


METHOD_SYSTEM_PROMPT = """The method is staged. The public method-generation surface is the NL contract extraction stage followed by two v27 complementary discovery-grounding lenses that share one response schema and compact cross-view context. Use only the complete context manifest supplied to each stage. Never read ledger answers, baseline results, judge examples, or historical release outputs. Do not emit W, D, or L levels. Every structured object must contain non-empty reason and basis."""

JUDGE_SYSTEM_PROMPT = """You are an independent judge separated from method generation. You may use the supplied frozen ledger entries to assess method D1/D2 release issues. Judge semantic identity of locus, property, scope, and direction, not string similarity. Emit sparse typed relation_assessments: exact, semantic_equivalent, or candidate_subsumes_ledger may count as a hit; candidate_subsumes_ledger requires a complete logical entailment basis from the candidate's own supplied claim. When a ledger explicitly enumerates multiple sibling scopes, events, states, or components, a candidate covering only a subset is ledger_subsumes_candidate or partial_overlap, even if it shares the same ancestor or cause. Never use ledger detail to add a missing sibling/component to the candidate's claim. ledger_subsumes_candidate, partial_overlap, same_cause_different_property, and unrelated never count as hits. Multiple non-hit subset candidates cannot be unioned or counted collectively as one ledger hit: every issue_id in matched_issue_ids must independently have one exact, semantic_equivalent, or candidate_subsumes_ledger relation that establishes the complete ledger defect. If no single release does so, the ledger is a miss even when several releases together mention every enumerated sibling. For a D1 ledger, compare the represented ambiguity rather than requiring the method release to settle it or use the same D level: when the release identifies the same primary defect reading at the same locus/property/scope/direction and preserves a compatible competent alternative, the surviving alternative is part of the same D1 ambiguity and does not by itself make the relation partial_overlap. This rule never repairs a wrong source, different property, incompatible scope, narrow manifestation, or issue that merely shares a cause; those are not semantic equivalence. Do not emit a full ledger-by-release matrix. Release assessment coverage is identity-based: emit one row for every supplied issue_id even when two releases are semantic duplicates or share one cause/ledger mapping; never deduplicate release rows. The ledger matched_issue_ids, release accounted_ledger_ids, hit-eligible typed relations, hit booleans, false-positive boolean, reason, and basis must all describe the same decision. In particular, a release marked false positive must have accounted_ledger_ids=[] and must not have reason or basis claiming that it matches a frozen defect. Do not read baseline results, other pairs, other judge outputs, or historical examples. Every assessment, relation, and top-level response must contain non-empty reason and basis fields that explain the judgment and its supplied-input support. Preserve the model's original wording."""


def _prompt_schema_hash() -> str:
    """Hash every prompt contract and structured response schema used by a run."""

    return _hash_json(
        {
            "version": PROMPT_SCHEMA_VERSION,
            "system_prompts": {
                "method_boundary": METHOD_SYSTEM_PROMPT,
                "contract": CONTRACT_SYSTEM_PROMPT,
                "discovery_grounding": DISCOVERY_GROUNDING_SYSTEM_PROMPT,
                "discovery_lenses": DISCOVERY_GROUNDING_AUDIT_LENSES,
                "d_adjudication": D_SYSTEM_PROMPT,
                "judge": JUDGE_SYSTEM_PROMPT,
            },
            "schemas": {
                "nl_contract": NLContractResponse.model_json_schema(),
                "grounding": GroundingResponse.model_json_schema(),
                "d_adjudication": DAdjudicationResponse.model_json_schema(),
                "judge": JudgeResponse.model_json_schema(),
                "judge_exact_identity_contract": {
                    "version": JUDGE_EXACT_IDENTITY_CONTRACT_VERSION,
                    "base_schema": ExactJudgeResponse.model_json_schema(),
                    "specialization": (
                        "Per pair, ledger/release IDs become closed Literal sets; "
                        "assessment lengths become exact; the inherited validator "
                        "enforces unique identity closure and symmetric accounting."
                    ),
                },
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
        "stream_first_byte_timeout_seconds": PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS,
        "provider_call_total_timeout_seconds": PROVIDER_CALL_DEADLINE_SECONDS,
        "structured_stage_timeout_seconds": STRUCTURED_STAGE_DEADLINE_SECONDS,
        "non_stream_provider_timeout_seconds": PROVIDER_CALL_DEADLINE_SECONDS,
        "dead_structured_call_retries_after_provider_error": 1,
        "structured_stage_timeout_owner": "local_runtime",
        "structured_stage_timeout_outer_retry": False,
        "schema_and_non_provider_retries_billable": True,
        "unavailable_non_provider_usage": "cost_ineligible_not_zero",
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
    resolved: list[str] = []
    unresolved: list[str] = []
    source_owned_unmapped: list[str] = []
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
            if raw.startswith(("source:", "macro:")):
                source_owned_unmapped.append(raw)
            else:
                unresolved.append(raw)

    # Source refs are provenance, not mandatory FCSTM bindings. They may fill
    # an otherwise empty model side through the published mapping contract,
    # but an unmapped source identity must not invalidate exact FCSTM refs that
    # the candidate already supplied.
    if not resolved:
        for raw in candidate.source_refs:
            if not raw.startswith(("source:", "macro:")):
                continue
            matches = [
                item
                for item in records
                if item.get("element_id") == raw
                or raw in (item.get("source_refs") or [])
            ]
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
                        if ref is not None and ref not in resolved:
                            resolved.append(ref)
                else:
                    state_path = metadata.get("fcstm_path") or semantic.get(
                        "fcstm_identifier"
                    )
                    ref = _model_ref_for_state(pair, state_path)
                    if ref is not None and ref not in resolved:
                        resolved.append(ref)

    if not resolved:
        unresolved.extend(source_owned_unmapped)

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
            state.name: [
                transition.ref
                for transition in pair.model.transitions
                if transition.source == state.name
            ]
            for state in bound_states
        }
        exact_local_progress = bool(
            binding.precise
            and normalized.property == "deadlock_freedom"
            and normalized.violation_direction == "dead_end"
            and bound_states
            and all(outgoing_by_state[state.name] for state in bound_states)
        )
        if not exact_local_progress:
            kept.append(normalized)
            continue

        fact = {
            "contract_id": normalized.contract_id,
            "candidate_hash": _hash_json(normalized),
            "bound_state_refs": [state.ref for state in bound_states],
            "outgoing_transition_refs": outgoing_by_state,
        }
        diagnostics.append(
            {
                "stage": "discovery_grounding",
                "lens": response.lens,
                "class": "exact_local_progress_satisfied",
                **fact,
                "reason": "Every exactly bound state in this dead_end claim has at least one parsed outgoing transition, so unreachability cannot be relabeled as a local dead-end violation.",
                "basis": "typed deadlock_freedom/dead_end identity, exact binding refs, and owned ModelIR transition endpoints",
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


def _materialize_exact_s2_inventory_candidates(
    pair: PairInput,
    contracts: NLContractResponse,
    llm_candidates: list[CandidateIssue],
) -> tuple[list[CandidateIssue], list[dict[str, Any]]]:
    """Compile exact missing-edge contracts that v27 scouts cannot let LLMs suppress."""

    materialized: list[CandidateIssue] = []
    receipts: list[dict[str, Any]] = []
    for contract in contracts.contracts:
        if (
            contract.property != "transition_endpoints"
            or contract.expected_direction != "must_exist"
        ):
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
            transition.source == source_state.name
            and transition.target == target_state.name
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


def _prepared_is_finding_candidate(prepared: Mapping[str, Any]) -> bool:
    """Restore v27's execute-batch boundary between passing checks and findings."""

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
                if any(edge.source == state.name for edge in pair.model.transitions)
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
                "reason": "The whole-cell v27 contract call failed; numbered NL is preserved only as an unresolved audit contract.",
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
            projection_version="v27-contract-projection.v1",
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
    # v27 samples the two complementary lenses sequentially inside one method
    # cell. Pair workers provide process-level parallelism without changing the
    # public AgentApp/LangGraph call semantics or deadline handling.
    for lens, prompt in grounding_prompts.items():
        outcome: StructuredCallOutcome[GroundingResponse] = runtime.call(
            kind="discovery_grounding",
            schema=GroundingResponse,
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
                    "reason": "One v27 discovery lens failed; its contracts remain unresolved and no fallback issue was manufactured.",
                    "basis": "public structured runtime outcome and v27 lens-local failure rule",
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
        "reason": "Two complementary v27 discovery lenses completed or retained explicit lens diagnostics; branch-local derived identities were normalized by the runner before merge.",
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
            projection_version="v27-complementary-grounding-projection.v1",
            reason=stage_outputs["discovery_grounding"]["reason"],
            basis=stage_outputs["discovery_grounding"]["basis"],
        )
    )

    response = assemble_method_response(
        grounding_responses,
        reason="The method merged two complementary v27 discovery lenses after NL contract extraction; typed semantic D is adjudicated separately and W remains deterministic downstream output.",
        basis="two GroundingResponse objects over the same compact cross-view context manifest",
    )
    try:
        frontier_batch = materialize_v27_frontier(
            pair,
            contract_response,
            contracts_by_id,
            grounding_responses,
            response.issues,
        )
    except Exception as exc:
        all_errors.append(
            {
                "stage": "execute_batch",
                "class": "deterministic_frontier_error",
                "error_type": type(exc).__name__,
                "message": str(exc),
                "reason": "The deterministic frontier failed locally; existing grounding candidates remain available and the cell continues with an explicit diagnostic.",
                "basis": "v27 local-stage downgrade rule; non-provider failures cannot erase prior semantic artifacts",
            }
        )
        frontier_batch = FrontierBatch(
            reason="The deterministic frontier produced no obligations because a local implementation error was preserved as a cell diagnostic.",
            basis=f"error_type={type(exc).__name__}; message={exc}",
        )
    frontier_candidates = [
        obligation.candidate for obligation in frontier_batch.obligations
    ]
    admitted_llm_candidates = [
        candidate
        for candidate in response.issues
        if candidate.contract_id
        not in frontier_batch.superseded_candidate_contract_ids
    ]
    for obligation in frontier_batch.obligations:
        contracts_by_id.setdefault(
            obligation.contract.contract_id, obligation.contract
        )
    exact_s2_candidates, exact_s2_receipts = (
        _materialize_exact_s2_inventory_candidates(
            pair,
            contract_response,
            [*admitted_llm_candidates, *frontier_candidates],
        )
    )
    candidates = [
        *admitted_llm_candidates,
        *frontier_candidates,
        *exact_s2_candidates,
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
        except Exception as exc:  # preserve a cell-level diagnostic instead of losing a candidate
            errors.append({"candidate_index": index, "error_type": type(exc).__name__, "message": str(exc), "reason": "Candidate processing failed; the cell remains readable.", "basis": "Candidate-level diagnostic preservation."})
    finding_candidates = [
        item for item in prepared_candidates if _prepared_is_finding_candidate(item)
    ]
    satisfied_candidates = [
        item for item in prepared_candidates if not _prepared_is_finding_candidate(item)
    ]
    stage_outputs["execute_batch"] = {
        "candidate_count": len(candidates),
        "llm_candidate_count": len(response.issues),
        "admitted_llm_candidate_count": len(admitted_llm_candidates),
        "superseded_llm_candidate_contract_ids": list(
            frontier_batch.superseded_candidate_contract_ids
        ),
        "frontier_candidate_count": len(frontier_candidates),
        "frontier_batch": frontier_batch.model_dump(mode="json"),
        "exact_s2_scout_candidate_count": len(exact_s2_candidates),
        "exact_s2_scout_receipts": exact_s2_receipts,
        "prepared_count": len(prepared_candidates),
        "finding_count": len(finding_candidates),
        "satisfied_count": len(satisfied_candidates),
        "finding_obligation_ids": [
            item["obligation_id"] for item in finding_candidates
        ],
        "satisfied_obligation_ids": [
            item["obligation_id"] for item in satisfied_candidates
        ],
        "candidates": [_jsonable(item) for item in prepared_candidates],
        "reason": "Exact binding, the v27 typed domain frontier, the exact S2 inventory scout, frozen predicate compilation, and deterministic backend execution were applied inside one execute-batch; completed true receipts remain passing-check audit records while only counterexamples, unresolved W1/W0, or errors become v27 findings.",
        "basis": "LLM-established typed contracts, owned source/ModelIR/inspection facts, frozen predicate registry, compiler plans, backend receipts, and the v27 passing-check exclusion rule",
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

    d_prompt = ""
    d_correction_prompt = ""
    d_outcome: StructuredCallOutcome[DAdjudicationResponse] | None = None
    d_stage_outcome: StructuredCallOutcome[DAdjudicationResponse] | None = None
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
        "reason": "D validation checked exact obligation coverage, uniqueness, closed enums, and decidable typed-fact contradictions.",
        "basis": "obligation IDs, typed SemanticAdjudication fields, and exact closed-model outgoing-transition inventory",
    }
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
            [item["obligation_id"] for item in finding_candidates],
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
        if repair_ids and d_outcome.succeeded:
            validation_output["repair_attempted"] = True
            d_correction_prompt = build_d_correction_prompt(
                pair,
                dossiers,
                missing_ids=missing_ids,
                duplicate_ids=duplicate_ids,
                extra_ids=extra_ids,
                invalid_decisions=invalid_decisions,
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
                correction_rows = correction_outcome.response.decisions
                correction_extra = [
                    decision.obligation_id
                    for decision in correction_rows
                    if decision.obligation_id not in repair_ids
                ]
                repair_groups: dict[str, list[SemanticAdjudication]] = {}
                for decision in correction_rows:
                    if decision.obligation_id in repair_ids:
                        repair_groups.setdefault(decision.obligation_id, []).append(
                            decision
                        )
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
                    if len(rows) == 1
                    and obligation_id not in correction_invalid
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
                unique_supplied = frozen_decisions
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

    stage_outputs["d_adjudication"] = d_response.model_dump(mode="json")
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:d-adjudication",
            stage_name="d_adjudication",
            status=(
                "completed"
                if not finding_candidates
                or (d_stage_outcome is not None and d_stage_outcome.succeeded)
                else "completed_with_diagnostics"
            ),
            artifact_roles=("natural_language", "plantuml_source", "canonical_source_ir", "source_inventory", "fcstm_model", "working_contract", "source_trace", "predicate_registry"),
            output=d_response,
            outcome=d_stage_outcome,
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
            )
            records.append(record)
            if emitted is not None:
                release.append(emitted)
            if record.get("audit_bundle") is not None:
                audit_path = output_root / "audit_bundles" / f"{record['issue_id']}.json"
                write_json(audit_path, record["audit_bundle"])
                record["audit_bundle_path"] = str(audit_path)
        except Exception as exc:  # preserve a cell-level diagnostic instead of losing a candidate
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
            "d_adjudication": d_prompt,
            "d_adjudication_correction": d_correction_prompt,
        }
    )
    llm_call = _aggregate_outcomes(all_outcomes)
    contract_ready = contract_outcome.real_llm and contract_outcome.succeeded
    grounding_ready = [
        outcome.real_llm and outcome.succeeded
        for outcome in grounding_outcomes
    ]
    closed_semantic_records = [
        record
        for record in records
        if record.get("d_level") in {"D0", "D1", "D2"}
    ]
    semantic_result_available = (
        bool(closed_semantic_records)
        if candidates
        else all(grounding_ready)
    )
    eligible = bool(
        contract_ready
        and any(grounding_ready)
        and semantic_result_available
    )
    eligibility_reasons = (
        [
            "real_contract_output",
            "at_least_one_real_v27_grounding_lens",
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
            "L",
            "D_basis",
            "L_basis",
            "summary",
            "detail",
            "axes",
        )
        if key in item
    }


def _judge_issue_projection(issue: dict[str, Any]) -> dict[str, Any]:
    """Project only the final v27-style D1/D2 semantic publication surface."""

    audit = issue.get("audit_bundle") or {}
    semantic = {
        key: issue[key]
        for key in (
            "issue_id",
            "contract_id",
            "locus_kind",
            "locus_names",
            "property",
            "violation_direction",
            "evidence_types",
            "title",
            "requirement_quote",
            "element_refs",
            "source_refs",
            "expected",
            "observed",
            "strongest_rebuttal",
            "d_level",
            "witness_level",
            "reason",
            "basis",
            "facet_count",
            "facet_issue_ids",
            "contract_ids",
        )
        if key in issue
    }
    return semantic | {
        "method_issue_hash": _hash_json(semantic),
        "audit_reference": {
            "pre_finalization_audit_hash": (
                audit.get("pre_finalization_audit_hash")
                or audit.get("audit_hash")
            ),
            "path": issue.get("audit_bundle_path"),
            "reason": "The complete W2 audit bundle remains on disk; the judge receives its identity only.",
            "basis": "v27-judge-release-projection.v1",
        },
        "reason": issue.get("reason") or "The release issue carries a deterministic method rationale.",
        "basis": issue.get("basis") or "method final-publication projection",
    }


def _normalize_judge_shape(
    response: JudgeResponse,
    ledger_items: list[dict[str, Any]],
    release: list[dict[str, Any]],
    rounds: int,
) -> JudgeResponse:
    """Canonicalize exact-ID ordering without rewriting judge decisions."""

    del ledger_items, release, rounds

    normalized_ledger: list[LedgerAssessment] = []
    for assessment in response.ledger_assessments:
        matched_issue_ids = sorted(assessment.matched_issue_ids)
        normalized_ledger.append(
            assessment.model_copy(
                update={"matched_issue_ids": matched_issue_ids}
            )
        )
    normalized_release = [
        assessment.model_copy(
            update={
                "accounted_ledger_ids": sorted(assessment.accounted_ledger_ids),
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


def _judge_prompt(
    pair: PairInput,
    ledger_items: list[dict[str, Any]],
    method_rounds: list[dict[str, Any]],
    *,
    response_schema_hash: str | None = None,
) -> str:
    """Build the independent pair-wide judge prompt from release issues only."""

    compact_rounds: list[dict[str, Any]] = []
    for cell in method_rounds:
        compact_rounds.append(
            {
                "round": cell.get("round"),
                "release_issue_clusters": [
                    _judge_issue_projection(issue)
                    for issue in cell.get("report_issue_clusters", [])
                ],
            }
        )
    required_release_ids = [
        str(issue.get("issue_id"))
        for cell in method_rounds
        for issue in cell.get("report_issue_clusters", [])
    ]
    required_ledger_ids = [str(item["id"]) for item in ledger_items]
    if response_schema_hash is None:
        response_schema = _judge_response_contract(
            ledger_ids=required_ledger_ids,
            release_ids=required_release_ids,
            rounds=len(method_rounds),
        )
        response_schema_hash = _hash_json(response_schema.model_json_schema())
    required_shape = {
        "identity_contract_version": JUDGE_EXACT_IDENTITY_CONTRACT_VERSION,
        "response_schema_hash": response_schema_hash,
        "ledger_assessment_count": len(required_ledger_ids),
        "ledger_ids_exactly_once": required_ledger_ids,
        "release_assessment_count": len(required_release_ids),
        "release_issue_ids_exactly_once": required_release_ids,
    }
    return f"""Assess the supplied method rounds for frozen pair {pair.pair_id} as an independent judge.

Frozen ledger entries (the judge's only ground-truth answer source; method generation did not read them):
{json.dumps([_judge_ledger_projection(item) for item in ledger_items], ensure_ascii=False, sort_keys=True)}

Final D1/D2 report issue clusters for all supplied method rounds (D0, stage receipts, compiler/backend details, and W2 audit bundles are excluded):
{json.dumps(compact_rounds, ensure_ascii=False, sort_keys=True)}

The exact Pydantic response shape for this request is:
{json.dumps(required_shape, ensure_ascii=False, sort_keys=True)}
You must emit each listed release ID exactly once. Do not emit any other
release ID, even if a similarly named issue appears in another round. Emit each
frozen ledger ID exactly once as well. The frozen ledger list is an array of
objects: emit exactly one ledger assessment for each supplied object. Do not
split one object into multiple assessments because its summary, detail, or
D_basis describes multiple defect aspects; those aspects remain one ledger
unit under its supplied ID.

A hit requires the same locus, property, scope, and defect direction. For every
claimed hit/accounting pair emit exactly one sparse relation_assessment. Only
exact, semantic_equivalent, and candidate_subsumes_ledger can count as hits;
candidate_subsumes_ledger must explain how the candidate logically establishes
the complete ledger defect in entailment_basis using the candidate's own supplied
claim. If the ledger explicitly enumerates multiple sibling scopes, events,
states, or components, a candidate that covers only a subset cannot subsume it:
use ledger_subsumes_candidate or partial_overlap even when both share an ancestor
or root cause. Do not use ledger detail to add an absent sibling or component to
the candidate. ledger_subsumes_candidate,
partial_overlap, same_cause_different_property, and unrelated do not count. A
wrong source, narrow manifestation sharing only a cause, broader category,
opposite direction, passing mention, reference-artifact complaint, or unrelated
bundle is not a hit. For a D1 ledger, do not demand that the method release use
the same D level or resolve the ambiguity: if both sides preserve compatible
competent readings and their primary violating reading has the same owner or locus, counted property,
normative scope, required direction, and shortfall, a surviving satisfying
alternative is part of the same D1 defect and is not by itself partial_overlap.
This D1 rule does not relax any locus/property/scope/direction requirement and
must never repair a wrong source, different property, partial manifestation, or
shared-cause issue. You may record plausible negative nearby relations, but do
not emit the full ledger-by-release matrix. Emit one ledger assessment for every
ledger_id with separate r1/r2/r3 decisions. Emit one release assessment for every
release issue; set is_false_positive=true only when no hit-eligible relation
accounts for it. The release reason and basis must agree with that boolean: if
true, explain why no supplied ledger has the same locus/property/scope/direction
and do not call it a match; if false, name the hit-eligible typed relation that
accounts for it. Do not omit units. Every assessment, relation, and top-level
response must have non-empty reason and basis fields. Do not read baseline
results, other pairs, historical judge examples, or files outside this input.
"""


def _read_ledger_for_pair(ledger_path: Path, pair_id: str) -> list[dict[str, Any]]:
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    items = data.get("items")
    if not isinstance(items, dict):
        raise ValueError("ledger.json items must be a mapping")
    return [dict(item) for item in items.values() if item.get("pair") == pair_id]


def _judge_contract_errors(
    response: JudgeResponse,
    *,
    expected_ledger: Sequence[str],
    expected_release: Sequence[str],
    rounds: int,
) -> list[str]:
    """Validate exact judge identity closure without semantic guessing."""

    def issue_round(issue_id: str) -> int | None:
        parts = issue_id.split(":")
        if len(parts) != 4 or parts[2] != "issue" or not parts[1].startswith("r"):
            return None
        try:
            return int(parts[1][1:])
        except ValueError:
            return None

    errors: list[str] = []
    expected_ledger = set(expected_ledger)
    expected_release = set(expected_release)
    ledger_ids = [item.ledger_id for item in response.ledger_assessments]
    release_ids = [item.issue_id for item in response.release_assessments]
    def coverage_error(
        *,
        label: str,
        id_name: str,
        expected: set[str],
        actual: list[str],
    ) -> str | None:
        counts = Counter(actual)
        missing = sorted(expected - set(actual))
        unknown = sorted(set(actual) - expected)
        duplicates = sorted(item_id for item_id, count in counts.items() if count > 1)
        if not missing and not unknown and not duplicates:
            return None
        return (
            f"{label} must contain each supplied {id_name} exactly once; "
            f"missing={json.dumps(missing, ensure_ascii=False)}; "
            f"unknown={json.dumps(unknown, ensure_ascii=False)}; "
            f"duplicates={json.dumps(duplicates, ensure_ascii=False)}"
        )

    ledger_coverage_error = coverage_error(
        label="ledger_assessments",
        id_name="ledger_id",
        expected=expected_ledger,
        actual=ledger_ids,
    )
    if ledger_coverage_error:
        errors.append(ledger_coverage_error)
    release_coverage_error = coverage_error(
        label="release_assessments",
        id_name="issue_id",
        expected=expected_release,
        actual=release_ids,
    )
    if release_coverage_error:
        errors.append(release_coverage_error)
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
    relation_pairs = [
        (assessment.ledger_id, assessment.issue_id)
        for assessment in response.relation_assessments
    ]
    if len(relation_pairs) != len(set(relation_pairs)):
        errors.append(
            "relation_assessments must contain at most one typed relation per ledger_id/issue_id pair"
        )
    for assessment in response.relation_assessments:
        if assessment.ledger_id not in expected_ledger:
            errors.append(
                f"relation assessment references unknown ledger ID {assessment.ledger_id}"
            )
        if assessment.issue_id not in expected_release:
            errors.append(
                f"relation assessment references unknown release ID {assessment.issue_id}"
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
    typed_hit_relations = {
        (assessment.ledger_id, assessment.issue_id)
        for assessment in response.relation_assessments
        if assessment.relation in _HIT_JUDGE_RELATIONS
        and assessment.ledger_id in expected_ledger
        and assessment.issue_id in expected_release
    }
    if matched_relations and not response.relation_assessments:
        errors.append(
            "every claimed hit/accounting pair requires a typed relation_assessment"
        )
    if response.relation_assessments and matched_relations != typed_hit_relations:
        errors.append(
            "typed hit relations must exactly equal ledger/release accounting pairs; "
            f"typed-only={sorted(typed_hit_relations - matched_relations)}; "
            f"accounting-only={sorted(matched_relations - typed_hit_relations)}"
        )
    if matched_relations != accounted_relations:
        ledger_side_only = sorted(matched_relations - accounted_relations)
        release_side_only = sorted(accounted_relations - matched_relations)
        errors.append(
            "ledger matched_issue_ids and release accounted_ledger_ids must encode the same exact relation pairs; "
            f"ledger-side-only={json.dumps(ledger_side_only, ensure_ascii=False)}; "
            f"release-side-only={json.dumps(release_side_only, ensure_ascii=False)}"
        )
    return errors


def _judge_shape_errors(
    response: JudgeResponse,
    ledger_items: list[dict[str, Any]],
    release: list[dict[str, Any]],
    rounds: int,
) -> list[str]:
    """Validate the persisted judge response against its supplied pair surface."""

    return _judge_contract_errors(
        response,
        expected_ledger=tuple(str(item["id"]) for item in ledger_items),
        expected_release=tuple(str(item["issue_id"]) for item in release),
        rounds=rounds,
    )


def _closed_literal(values: tuple[str, ...]) -> Any:
    """Build a closed Literal type for one non-empty runtime identity set."""

    if not values:
        raise ValueError("a closed Literal identity set cannot be empty")
    return Literal.__getitem__(values)


def _judge_response_contract(
    *,
    ledger_ids: Sequence[str],
    release_ids: Sequence[str],
    rounds: int,
) -> type[ExactJudgeResponse]:
    """Specialize the judge schema to one exact pair-wide identity surface.

    Literal item IDs and exact list cardinalities guide structured generation;
    the inherited validator closes uniqueness, references, round booleans, and
    symmetric accounting. The specialization does not encode semantic matches.
    """

    expected_ledger = tuple(str(item_id) for item_id in ledger_ids)
    expected_release = tuple(str(item_id) for item_id in release_ids)
    if len(expected_ledger) != len(set(expected_ledger)):
        raise ValueError("judge ledger input contains duplicate ledger IDs")
    if len(expected_release) != len(set(expected_release)):
        raise ValueError("judge release input contains duplicate issue IDs")
    if rounds not in {1, 3}:
        raise ValueError(f"judge response contract requires 1 or 3 rounds, got {rounds}")

    contract_key = _hash_json(
        {
            "version": JUDGE_EXACT_IDENTITY_CONTRACT_VERSION,
            "ledger_ids": expected_ledger,
            "release_ids": expected_release,
            "rounds": rounds,
        }
    ).removeprefix("sha256:")[:16]
    ledger_model: type[LedgerAssessment] = LedgerAssessment
    if expected_ledger:
        ledger_model = create_model(
            f"ExactLedgerAssessment_{contract_key}",
            __base__=LedgerAssessment,
            ledger_id=(
                _closed_literal(expected_ledger),
                Field(
                    description=(
                        "Exact frozen ledger ID from this pair-wide call's closed "
                        "identity set; every allowed ID must occur once overall."
                    )
                ),
            ),
        )
    release_model: type[ReleaseAssessment] = ReleaseAssessment
    if expected_release:
        release_model = create_model(
            f"ExactReleaseAssessment_{contract_key}",
            __base__=ReleaseAssessment,
            issue_id=(
                _closed_literal(expected_release),
                Field(
                    description=(
                        "Exact released issue ID from this pair-wide call's closed "
                        "identity set; semantic duplicates remain separate rows."
                    )
                ),
            ),
        )
    relation_model: type[JudgeRelationAssessment] = JudgeRelationAssessment
    if expected_ledger and expected_release:
        relation_model = create_model(
            f"ExactJudgeRelationAssessment_{contract_key}",
            __base__=JudgeRelationAssessment,
            ledger_id=(
                _closed_literal(expected_ledger),
                Field(description="Exact ledger ID from this call's closed identity set."),
            ),
            issue_id=(
                _closed_literal(expected_release),
                Field(description="Exact release issue ID from this call's closed identity set."),
            ),
        )

    response_model = create_model(
        f"ExactJudgeResponse_{contract_key}",
        __base__=ExactJudgeResponse,
        ledger_assessments=(
            list[ledger_model],
            Field(
                ...,
                min_length=len(expected_ledger),
                max_length=len(expected_ledger),
                description=(
                    "Exactly one assessment for every ledger ID in this call's closed "
                    "identity set; IDs may not be omitted, duplicated, or invented."
                ),
            ),
        ),
        release_assessments=(
            list[release_model],
            Field(
                ...,
                min_length=len(expected_release),
                max_length=len(expected_release),
                description=(
                    "Exactly one assessment for every release issue ID in this call's "
                    "closed identity set, including semantically duplicate releases."
                ),
            ),
        ),
        relation_assessments=(
            list[relation_model],
            Field(
                ...,
                max_length=len(expected_ledger) * len(expected_release),
                description=(
                    "Sparse typed relations over only this call's closed ledger/release "
                    "identity sets; it is not a request for a full relation matrix."
                ),
            ),
        ),
    )
    response_model.__doc__ = (
        "Runtime-specialized independent pair-wide judge response. The schema "
        "has authority over exact identity closure only, not semantic relations."
    )
    response_model.expected_ledger_ids = expected_ledger
    response_model.expected_release_ids = expected_release
    response_model.supplied_rounds = rounds
    response_model.enforce_exact_identity_contract = True
    response_model.model_rebuild(force=True)
    return response_model


def _judge_correction_prompt(
    pair: PairInput,
    ledger_items: list[dict[str, Any]],
    method_rounds: list[dict[str, Any]],
    previous_response: JudgeResponse,
    errors: list[str],
    *,
    response_schema_hash: str | None = None,
) -> str:
    """Build a billed same-node correction prompt for judge shape failures."""

    previous = json.dumps(
        previous_response.model_dump(mode="json"),
        ensure_ascii=False,
        sort_keys=True,
    )
    required_ledger_ids = [str(item["id"]) for item in ledger_items]
    required_release_ids = [
        str(issue["issue_id"])
        for cell in method_rounds
        for issue in cell.get("report_issue_clusters", [])
    ]
    previous_ledger_ids = [
        assessment.ledger_id for assessment in previous_response.ledger_assessments
    ]
    previous_release_ids = [
        assessment.issue_id for assessment in previous_response.release_assessments
    ]
    previous_ledger_counts = Counter(previous_ledger_ids)
    previous_release_counts = Counter(previous_release_ids)
    typed_relations = {
        (item.ledger_id, item.issue_id): item.relation
        for item in previous_response.relation_assessments
    }
    ledger_accounting_pairs = {
        (item.ledger_id, issue_id)
        for item in previous_response.ledger_assessments
        for issue_id in item.matched_issue_ids
    }
    release_accounting_pairs = {
        (ledger_id, item.issue_id)
        for item in previous_response.release_assessments
        for ledger_id in item.accounted_ledger_ids
    }
    relation_accounting_rows = [
        {
            "ledger_id": ledger_id,
            "issue_id": issue_id,
            "typed_relation": typed_relations.get((ledger_id, issue_id)),
            "typed_hit_eligible": (
                typed_relations.get((ledger_id, issue_id))
                in _HIT_JUDGE_RELATIONS
            ),
            "ledger_side_accounted": (
                (ledger_id, issue_id) in ledger_accounting_pairs
            ),
            "release_side_accounted": (
                (ledger_id, issue_id) in release_accounting_pairs
            ),
        }
        for ledger_id, issue_id in sorted(
            set(typed_relations)
            | ledger_accounting_pairs
            | release_accounting_pairs
        )
    ]
    replacement_checklist = {
        "required_ledger_ids": required_ledger_ids,
        "previous_ledger_ids": previous_ledger_ids,
        "missing_ledger_ids": [
            item_id
            for item_id in required_ledger_ids
            if previous_ledger_counts[item_id] == 0
        ],
        "duplicate_ledger_ids": sorted(
            item_id
            for item_id, count in previous_ledger_counts.items()
            if count > 1
        ),
        "required_release_issue_ids": required_release_ids,
        "previous_release_issue_ids": previous_release_ids,
        "missing_release_issue_ids": [
            item_id
            for item_id in required_release_ids
            if previous_release_counts[item_id] == 0
        ],
        "duplicate_release_issue_ids": sorted(
            item_id
            for item_id, count in previous_release_counts.items()
            if count > 1
        ),
        "relation_accounting_rows": relation_accounting_rows,
    }
    return (
        _judge_prompt(
            pair,
            ledger_items,
            method_rounds,
            response_schema_hash=response_schema_hash,
        )
        + "\nPrevious pair-wide JudgeResponse to repair:\n"
        + previous
        + "\nExact complete-replacement identity checklist:\n"
        + json.dumps(replacement_checklist, ensure_ascii=False, sort_keys=True)
        + "\nThe previous response violated these deterministic shape contracts:\n- "
        + "\n- ".join(errors)
        + "\nReturn one complete replacement response. First carry forward every prior valid ledger and release assessment whose ID is required, preserving its semantic decision unless a listed relation error implicates it; then add every missing required row. Merge duplicate rows for one ledger ID into its single required row, and collapse release rows only when they repeat the same exact issue_id. Never deduplicate release assessment rows because their content, cause, locus, property, or ledger mapping is similar: identity coverage is by exact issue_id, and the final release issue ID set must equal required_release_issue_ids. Every claimed hit/accounting pair must have one typed relation_assessment, and hit-eligible typed relations must appear on both ledger/release accounting sides. Read every relation_accounting_rows item mechanically: typed_hit_eligible=true requires ledger_side_accounted=true and release_side_accounted=true; typed_hit_eligible=false requires both accounting booleans false unless you make and justify a new semantic decision that changes the typed relation itself. Multiple ledger_subsumes_candidate or partial_overlap rows cannot be unioned into one hit, so do not use words such as jointly, together, collectively, or combined to account subset candidates. For each listed ledger-side-only, release-side-only, or typed-relation inconsistency, make one semantic locus/property/scope/direction decision: if one candidate independently establishes the complete ledger defect, use exact, semantic_equivalent, or a fully justified candidate_subsumes_ledger; otherwise remove the accounting pair and optionally preserve its sparse negative relation. Whenever accounting changes, rewrite that assessment's reason and basis to describe the corrected decision; is_false_positive must equal whether accounted_ledger_ids is empty, and a false-positive row must not retain wording that claims a frozen-ledger match. Before returning, mechanically compare both assessment ID sets and every relation_accounting_rows pair with the checklist and verify that no required ID is missing. Do not add a relation merely to fill shape, do not create a full matrix, and do not leave a claimed pair on only one side. This is schema/coverage correction, not a provider retry. Every supplied unit still requires a semantic reason and basis.\n"
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
    """Run the v27 pair-wide judge with at most one shape correction."""

    ledger_items = _read_ledger_for_pair(ledger_path, pair.pair_id)
    judge_method_rounds = [
        {
            **cell,
            "report_issue_clusters": (
                cell.get("report_issue_clusters", [])
                if cell.get("eligible") is True
                else []
            ),
        }
        for cell in method_rounds
    ]
    release = [
        issue
        for cell in judge_method_rounds
        for issue in cell.get("report_issue_clusters", [])
    ]
    response_schema = _judge_response_contract(
        ledger_ids=tuple(str(item["id"]) for item in ledger_items),
        release_ids=tuple(str(item["issue_id"]) for item in release),
        rounds=len(judge_method_rounds),
    )
    response_schema_hash = _hash_json(response_schema.model_json_schema())
    prompt = _judge_prompt(
        pair,
        ledger_items,
        judge_method_rounds,
        response_schema_hash=response_schema_hash,
    )
    outcomes: list[StructuredCallOutcome[Any]] = []
    errors: list[dict[str, Any]] = []
    mode = "pair_wide"
    outcome: StructuredCallOutcome[Any] = runtime.call(
        kind="judge",
        schema=response_schema,
        system_prompt=JUDGE_SYSTEM_PROMPT,
        prompt=prompt,
        artifact_id=f"judge/{pair.pair_id}",
        max_output_tokens=JUDGE_MAX_STRUCTURED_OUTPUT_TOKENS,
    )
    outcomes.append(outcome)
    response = outcome.response if outcome.succeeded else None
    if response is not None:
        response = _normalize_judge_shape(
            response,
            ledger_items,
            release,
            len(judge_method_rounds),
        )
    shape_errors = (
        _judge_shape_errors(
            response,
            ledger_items,
            release,
            len(judge_method_rounds),
        )
        if response is not None
        else ["pair-wide judge output unavailable"]
    )
    if response is not None and shape_errors:
        correction: StructuredCallOutcome[Any] = runtime.call(
            kind="judge_correction",
            schema=response_schema,
            system_prompt=JUDGE_SYSTEM_PROMPT,
            prompt=_judge_correction_prompt(
                pair,
                ledger_items,
                judge_method_rounds,
                response,
                shape_errors,
                response_schema_hash=response_schema_hash,
            ),
            artifact_id=f"judge/{pair.pair_id}/shape-correction",
            max_output_tokens=JUDGE_MAX_STRUCTURED_OUTPUT_TOKENS,
        )
        outcomes.append(correction)
        if correction.succeeded:
            response = _normalize_judge_shape(
                correction.response,
                ledger_items,
                release,
                len(judge_method_rounds),
            )
            shape_errors = _judge_shape_errors(
                response,
                ledger_items,
                release,
                len(judge_method_rounds),
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
        response = None
        mode = "judge_unavailable"
    semantic_outcome = outcomes[-1] if response is not None else None
    eligible = bool(
        response is not None
        and semantic_outcome is not None
        and semantic_outcome.real_llm
        and semantic_outcome.succeeded
        and not _judge_shape_errors(
            response,
            ledger_items,
            release,
            len(judge_method_rounds),
        )
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
        "response_schema_hash": response_schema_hash,
        "llm_calls": [item.to_dict() for item in outcomes],
        "llm_call": _aggregate_outcomes(outcomes, kind="judge"),
        "judgement": response.model_dump(mode="json") if response is not None else None,
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
                "contract_id": issue.get("contract_id"),
                "locus_kind": issue.get("locus_kind"),
                "locus_names": issue.get("locus_names"),
                "property": issue.get("property"),
                "violation_direction": issue.get("violation_direction"),
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
        "response_schema_hash": None,
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
                "pre_finalization_audit_hash": bundle[
                    "pre_finalization_audit_hash"
                ],
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
        for round_index in range(len(rounds_data) + 1, rounds + 1):
            cell = _method_cell(
                pair=pair,
                round_index=round_index,
                runtime=runtime,
                output_root=output_root,
                run_identity=run_identity,
            )
            rounds_data.append(cell)
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
