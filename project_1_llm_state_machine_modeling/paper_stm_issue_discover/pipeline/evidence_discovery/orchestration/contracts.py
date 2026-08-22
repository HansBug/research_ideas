"""Pydantic run-envelope contracts for resumable evidence-discovery experiments."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class SourceProvenance(BaseModel):
    """Exact repository identity used to generate one run and its cells."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    source_commit: str = Field(
        pattern=r"^(?:[0-9a-f]{40}|unknown)$",
        description="Exact Git commit used by method and judge execution, or unknown after an audited lookup failure.",
    )
    source_branch: str = Field(
        min_length=1,
        description="Git branch used for the run, or unknown after an audited lookup failure.",
    )
    source_dirty: bool = Field(
        description="Whether tracked files differed from source_commit when provenance was captured; untracked run artifacts are excluded.",
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of why repository provenance is recorded.",
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty command or diagnostic basis used to resolve repository provenance.",
    )


class RunManifest(BaseModel):
    """Immutable experiment identity plus mutable terminal status for one run root."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["paper1.evidence_discovery.run_manifest.v2"] = Field(
        description="Versioned run-manifest schema identifier."
    )
    run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Stable random identity shared by all method, judge, pair-status, and summary receipts in this run root.",
    )
    run_contract_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of immutable run identity fields used to reject incompatible resume inputs.",
    )
    status: Literal["running", "completed", "completed_with_diagnostics"] = Field(
        description="Current run status; running manifests remain resumable without changing identity."
    )
    profile: str = Field(
        min_length=1,
        description="Exact public utils.llm profile used for method and independent judge calls.",
    )
    source_provenance: SourceProvenance = Field(
        description="Repository commit, branch, and tracked-worktree state used by the run."
    )
    registry_version: str = Field(
        min_length=1,
        description="Frozen predicate registry version used by every method cell.",
    )
    registry_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the exact frozen predicate registry payload used by the run.",
    )
    code_version: str = Field(
        min_length=1,
        description="Versioned evidence-discovery orchestration and receipt implementation."
    )
    prompt_schema_version: str = Field(
        min_length=1,
        description="Version shared by staged method and independent-judge prompt/schema contracts."
    )
    prompt_schema_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of system prompts and every structured LLM response schema used by the run."
    )
    input_data_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of ordered pair context-manifest hashes and the judge-only frozen ledger hash."
    )
    pair_input_hashes: dict[str, str] = Field(
        min_length=1,
        description="Pair-keyed complete context-manifest hashes used for strict cell resume."
    )
    ledger_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the frozen judge-only ledger; ledger content is never supplied to method generation."
    )
    rounds: Literal[1, 3] = Field(
        description="One diagnostic round or the frozen three-round protocol."
    )
    selected_pair_ids: tuple[str, ...] = Field(
        min_length=1,
        description="Exact ordered frozen pair IDs included in this run; resume requires equality.",
    )
    scope: Literal["diagnostic_subset", "full_protocol"] = Field(
        description="Whether selected_pair_ids is a diagnostic subset or all 54 frozen pairs."
    )
    workers: int = Field(
        ge=1,
        description="Maximum independent pair processes used by the run."
    )
    transport_retries: int = Field(
        ge=0,
        description="Run-scoped in-place provider transport retry count configured through public utils.agent.",
    )
    streaming: bool = Field(
        description="Whether provider calls use streaming with the frozen first-byte and total deadlines."
    )
    retry_policy: dict[str, Any] = Field(
        description="Audited transport delays, one local dead-cell retry, and row-local billing policy."
    )
    started_at: datetime = Field(
        description="Timezone-aware timestamp at which this run identity was first created."
    )
    updated_at: datetime = Field(
        description="Timezone-aware timestamp of the latest manifest status update."
    )
    predecessor_snapshot: str | None = Field(
        default=None,
        description="Optional preserved diagnostic run root that motivated this fresh contract-compatible run; it is never imported as current cells.",
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of this run's scope and resume policy.",
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty protocol, registry, and explicit gate basis for this run.",
    )


class PairRunStatus(BaseModel):
    """Terminal or resumable status receipt for one frozen pair."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["paper1.evidence_discovery.pair_status.v2"] = Field(
        description="Versioned pair-status schema identifier."
    )
    run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Run identity owning this pair status."
    )
    run_contract_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Run contract hash used to reject mixed-run pair receipts."
    )
    pair_id: str = Field(
        pattern=r"^[0-9]{4}$",
        description="Frozen pair identifier represented by this receipt."
    )
    status: Literal["completed", "completed_with_diagnostics", "failed_with_receipt"] = Field(
        description="Terminal pair status after all requested method rounds and judge handling."
    )
    resume_action: Literal[
        "executed_fresh",
        "resumed_compatible_prefix",
        "skipped_compatible_terminal",
        "terminalized_after_error",
        "reconstructed_terminal_status",
    ] = Field(
        description="Deterministic execution, resume, skip, or failure-terminalization action for this invocation."
    )
    started_at: datetime = Field(
        description="Timezone-aware pair execution start timestamp."
    )
    method_cells: int = Field(
        ge=0,
        description="Number of terminal method-cell receipts present for this pair."
    )
    eligible_method_cells: int = Field(
        ge=0,
        description="Number of method cells with real validated provider output and no provider/schema cell failure."
    )
    judge_status: str = Field(
        min_length=1,
        description="Independent judge terminal status for this pair."
    )
    judge_eligible: bool = Field(
        description="Whether every required judge position has a real semantic decision."
    )
    errors: int = Field(
        ge=0,
        description="Count of structured method and judge diagnostics retained for this pair."
    )
    audit_errors: int = Field(
        ge=0,
        description="Count of W2 external audit finalization errors retained for this pair."
    )
    method_cost_usd: float = Field(
        ge=0,
        description="Billable method cost after row-local provider retry exemptions."
    )
    method_cost_eligible: bool = Field(
        description="Whether every method usage row had a resolvable pricing card and token accounting."
    )
    judge_cost_usd: float = Field(
        ge=0,
        description="Billable independent judge cost after row-local provider retry exemptions."
    )
    judge_cost_eligible: bool = Field(
        description="Whether every judge usage row had a resolvable pricing card and token accounting."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of the pair terminal status."
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty method-cell, judge, usage, and run-contract basis for the pair status."
    )


class MethodCellReceipt(BaseModel):
    """Versioned terminal receipt for one method pair-round cell."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["paper1.evidence_discovery.method_cell.v3"] = Field(
        description="Versioned method-cell schema identifier."
    )
    run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Run identity owning this method cell."
    )
    run_contract_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Immutable run contract hash used to prevent mixed-run resume."
    )
    source_provenance: SourceProvenance = Field(
        description="Exact repository identity that generated this method cell."
    )
    pair_id: str = Field(
        pattern=r"^[0-9]{4}$",
        description="Frozen pair identifier processed by this cell."
    )
    pair_input_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Complete context-manifest hash frozen for this pair in the run contract."
    )
    round: Literal[1, 2, 3] = Field(
        description="Independent method round represented by this receipt."
    )
    status: Literal["completed", "completed_with_diagnostics", "failed_with_receipt"] = Field(
        description="Terminal method-cell status; every requested cell must end in one of these states."
    )
    prompt_hash: str | None = Field(
        default=None,
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of all staged method prompts, or null when setup failed before prompting."
    )
    context_manifest: dict[str, Any] | None = Field(
        default=None,
        description="Complete v27-equivalent context manifest supplied to method stages, or null after pre-load failure."
    )
    input_hashes: dict[str, str] = Field(
        default_factory=dict,
        description="Role-keyed hashes of exact method input artifacts."
    )
    stage_outputs: dict[str, Any] = Field(
        default_factory=dict,
        description="Validated Pydantic output of each completed method stage."
    )
    stage_receipts: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Ordered prepare-to-publication receipts with manifest identity and rationale."
    )
    model_output: dict[str, Any] = Field(
        description="Structured model-generation surface, including top-level reason and basis."
    )
    llm_calls: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Every staged public-runtime call, retry, usage row, and billing disposition."
    )
    llm_call: dict[str, Any] = Field(
        description="Pair-round aggregate of all staged LLM calls retained for reporting compatibility."
    )
    eligible: bool = Field(
        description="Whether this cell has real validated model output and is eligible for paired metrics."
    )
    eligibility_reasons: list[str] = Field(
        min_length=1,
        description="Deterministic reasons supporting or denying method-cell eligibility."
    )
    evidence_records: list[dict[str, Any]] = Field(
        default_factory=list,
        description="All deterministic W/D evidence records, including non-release and coverage-gap records."
    )
    report_issue_clusters: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Only final D1/D2 release issues exposed to the independent judge."
    )
    errors: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Structured provider, schema, stage, compiler, backend, and publication diagnostics."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of this method cell's terminal output."
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty input, model, stage, and deterministic-evidence basis for this cell."
    )


class IndependentJudgeReceipt(BaseModel):
    """Versioned terminal receipt for one independent pair-wide judge surface."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["paper1.evidence_discovery.independent_judge.v2"] = Field(
        description="Versioned independent-judge schema identifier."
    )
    run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Run identity owning this judge receipt."
    )
    run_contract_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Immutable run contract hash used to reject mixed judge artifacts."
    )
    source_provenance: SourceProvenance = Field(
        description="Exact repository identity that generated this judge receipt."
    )
    pair_id: str = Field(
        pattern=r"^[0-9]{4}$",
        description="Frozen pair identifier judged by this receipt."
    )
    pair_input_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Complete method input manifest hash tied to this pair's judged release surface."
    )
    status: Literal["completed", "failed_with_receipt"] = Field(
        description="Terminal judge status; failed receipts remain unadjudicated and ineligible."
    )
    eligible: bool = Field(
        description="Whether every required judge position has a real semantic decision."
    )
    eligibility_reasons: list[str] = Field(
        min_length=1,
        description="Deterministic reasons supporting or denying judge eligibility."
    )
    adjudication_mode: Literal[
        "pair_wide",
        "partitioned_pair_wide",
        "pair_wide_corrected",
        "atomic_llm_fallback",
        "judge_unavailable",
        "exact_empty_release",
        "not_started",
    ] = Field(
        description="Semantic judge path that produced the terminal judgement."
    )
    ledger_count: int = Field(
        ge=0,
        description="Number of frozen ledger entries supplied only to the independent judge."
    )
    release_count: int = Field(
        ge=0,
        description="Number of D1/D2 method release issues supplied to the judge."
    )
    ledger_source: str = Field(
        min_length=1,
        description="Path to the frozen ledger read only at the judge boundary."
    )
    prompt_hash: str | None = Field(
        default=None,
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the pair-wide judge prompt, or null when judge setup did not start."
    )
    llm_calls: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Every pair-wide, correction, or atomic semantic judge call with usage and retries."
    )
    llm_call: dict[str, Any] = Field(
        description="Aggregate judge runtime and billing receipt."
    )
    judgement: dict[str, Any] | None = Field(
        default=None,
        description="Complete validated judge output, or null when semantic adjudication remains incomplete."
    )
    atomic_relations: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Audited ledger-to-release semantic relations used by the atomic fallback."
    )
    errors: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Structured pair-wide shape, provider, schema, and atomic relation diagnostics."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of the independent judge terminal outcome."
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty ledger, release, model-call, and exact-shape basis for the outcome."
    )


class RunSummaryReceipt(BaseModel):
    """Validated final summary for one contract-compatible method and judge run."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["paper1.evidence_discovery.run_summary.v2"] = Field(
        description="Versioned run-summary schema identifier."
    )
    run_id: str = Field(
        pattern=r"^[0-9a-f]{32}$",
        description="Stable identity shared with the run manifest and every cell."
    )
    run_contract_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Immutable contract hash shared with all resumed artifacts."
    )
    artifact_root: str = Field(
        min_length=1,
        description="Absolute run-id-bearing directory containing the manifest and every artifact."
    )
    status: Literal["completed", "completed_with_diagnostics"] = Field(
        description="Final run status derived from terminal pair receipts."
    )
    run_started_at: datetime = Field(
        description="Timezone-aware timestamp copied from the original run manifest."
    )
    run_completed_at: datetime = Field(
        description="Timezone-aware timestamp when final metrics and summary were written."
    )
    profile: str = Field(
        min_length=1,
        description="Exact utils.llm profile used for method and judge calls."
    )
    source_commit: str = Field(
        pattern=r"^(?:[0-9a-f]{40}|unknown)$",
        description="Exact Git commit used by this run."
    )
    source_branch: str = Field(
        min_length=1,
        description="Git branch used by this run."
    )
    source_provenance: SourceProvenance = Field(
        description="Complete repository identity and tracked-worktree state."
    )
    resume: bool = Field(
        description="Whether this invocation resumed the same compatible run identity."
    )
    rounds: Literal[1, 3] = Field(
        description="Diagnostic or frozen protocol round count."
    )
    workers: int = Field(
        ge=1,
        description="Maximum independent pair processes used by this invocation."
    )
    transport_retries: int = Field(
        ge=0,
        description="In-place provider transport retry count configured through utils.agent."
    )
    streaming: bool = Field(
        description="Whether calls used the 30-second first-byte plus 120-second total streaming contract."
    )
    registry_version: str = Field(
        min_length=1,
        description="Frozen four-family registry version used by the run."
    )
    registry_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the exact predicate registry payload."
    )
    pair_count: int = Field(
        ge=1,
        description="Number of selected frozen pairs represented in the run."
    )
    protocol_pair_count: int = Field(
        ge=1,
        description="Fixed full-protocol pair count used as the conservative grid denominator."
    )
    selected_pair_ids: list[str] = Field(
        min_length=1,
        description="Exact ordered frozen pair IDs represented in this summary."
    )
    scope: Literal["diagnostic_subset", "full_protocol"] = Field(
        description="Whether the summary covers a diagnostic subset or all frozen pairs."
    )
    selection: dict[str, Any] = Field(
        description="Audited pair-selection reason and basis."
    )
    method_cell_count: int = Field(
        ge=0,
        description="Number of terminal method-cell receipts included in metrics."
    )
    judge_pair_count: int = Field(
        ge=0,
        description="Number of terminal pair judge receipts included in metrics."
    )
    method_cost_usd: float = Field(
        ge=0,
        description="Billable method cost after row-local provider retry exemptions."
    )
    judge_cost_usd: float = Field(
        ge=0,
        description="Billable independent judge cost after row-local provider retry exemptions."
    )
    metrics: dict[str, Any] = Field(
        description="Paired-eligible readings, full-grid lower bounds, FP, W/D, and per-pair metrics."
    )
    per_pair: dict[str, dict[str, Any]] = Field(
        description="Validated PairRunStatus payload for every selected pair."
    )
    failed_pairs: list[str] = Field(
        default_factory=list,
        description="Selected pair IDs ending in failed_with_receipt."
    )
    method_cells_with_diagnostics: list[str] = Field(
        default_factory=list,
        description="Pair-round identities carrying method diagnostics or ineligibility."
    )
    predecessor_snapshot: str | None = Field(
        default=None,
        description="Preserved pre-contract diagnostic snapshot recorded for provenance only."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of run scope and terminal completeness."
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty registry, run manifest, frozen grid, and independent judge basis."
    )


__all__ = [
    "IndependentJudgeReceipt",
    "MethodCellReceipt",
    "PairRunStatus",
    "RunManifest",
    "RunSummaryReceipt",
    "SourceProvenance",
]
