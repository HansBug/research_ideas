"""Provider-free scale audit for the exact unified semantic Judge payload."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from utils.llm import load_llm_registry

from .artifacts import (
    adapt_evidence_discovery_release,
    adapt_x1v2_record,
    build_artifact_closure,
    build_unified_input,
    load_expected_issues,
    stable_model_hash,
)
from .models import JudgeScaleAudit, UnifiedJudgeInput
from .protocol import (
    JUDGE_ALGORITHM_VERSION,
    JUDGE_MAX_OUTPUT_TOKENS,
    PROMPT_VERSION,
    PROTOCOL_SHA256,
    PROTOCOL_VERSION,
    SYSTEM_PROMPT,
    prompt_hash,
    verify_snapshot,
)
from .runner import build_primary_prompt
from .schema import build_exact_response_model, response_schema_hash

SourceFormat = Literal["x1v2_record", "evidence_discovery_release"]
MATERIAL_ASSERTION_CHARS_PER_ROW = 64


def _sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _estimated_tokens(value: str) -> int:
    """Return the runtime's conservative four-characters-per-token estimate."""

    return (len(value) + 3) // 4


def _algorithm_source_hash() -> str:
    """Hash modules that define Judge input, semantics, execution, and scale."""

    module_root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    paths = (
        ("semantic_judge/artifacts.py", module_root / "artifacts.py"),
        ("semantic_judge/cli.py", module_root / "cli.py"),
        ("semantic_judge/metrics.py", module_root / "metrics.py"),
        ("semantic_judge/models.py", module_root / "models.py"),
        ("semantic_judge/protocol.py", module_root / "protocol.py"),
        ("semantic_judge/runner.py", module_root / "runner.py"),
        ("semantic_judge/scale_audit.py", module_root / "scale_audit.py"),
        ("semantic_judge/schema.py", module_root / "schema.py"),
        (
            "evidence_discovery/orchestration/runtime.py",
            module_root.parent
            / "evidence_discovery"
            / "orchestration"
            / "runtime.py",
        ),
    )
    for name, path in paths:
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def _causal_field_names(report) -> tuple[str, ...]:
    return tuple(
        field_name
        for field_name in ("reason", "basis", "observed")
        if isinstance(getattr(report, field_name), str)
    )


def _material_assertion_count(field_text: str) -> int:
    """Reserve at least one assertion row per short source-text span."""

    return max(
        1,
        (len(field_text) + MATERIAL_ASSERTION_CHARS_PER_ROW - 1)
        // MATERIAL_ASSERTION_CHARS_PER_ROW,
    )


def _material_assertion_envelope(
    *, report_id: str, field_name: str, field_text: str, artifact_ref: str
) -> list[dict]:
    """Build a conservative validated assertion envelope from real field length."""

    return [
        {
            "assertion_id": f"A{index}",
            "assertion": "One independently testable material premise from the complete report field.",
            "verdict": "SUPPORTED",
            "reason": "The exact premise is compatible with the complete common artifact closure.",
            "basis": "The authored report field and common artifacts directly support this premise.",
            "source_refs": [
                f"report:{report_id}:{field_name}",
                artifact_ref,
            ],
        }
        for index in range(1, _material_assertion_count(field_text) + 1)
    ]


def _structural_response_payload(
    judge_input: UnifiedJudgeInput,
    *,
    all_positive: bool,
) -> dict:
    """Build a validated size envelope without supplying a semantic decision."""

    artifact_ref = judge_input.artifact_closure.artifacts[0].artifact_id
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    report_judgments = []
    for report in judge_input.reports:
        causal_fields = _causal_field_names(report)
        certificate_field = "reason"
        positive_relations = (
            [
                {
                    "expected_id": expected_id,
                    "match": "FULL_MATCH",
                    "report_field_refs": ["claim", certificate_field],
                    "reason": "The complete valid report states the same actionable defect relation for this expected issue.",
                    "basis": "The report-owned causal certificate, expected obligation, and common artifacts establish direct repair overlap.",
                    "source_refs": [
                        f"report:{report.report_id}:{certificate_field}",
                        f"expected:{expected_id}",
                        artifact_ref,
                    ],
                }
                for expected_id in expected_ids
            ]
            if all_positive
            else []
        )
        positive_by_expected = {
            row["expected_id"]: row for row in positive_relations
        }
        relation_decisions = [
            positive_by_expected.get(
                expected_id,
                {"expected_id": expected_id, "match": "NO_MATCH"},
            )
            for expected_id in expected_ids
        ]
        has_no_match = not all_positive
        report_judgments.append(
            {
                "report_id": report.report_id,
                "root_cause_cluster_key": "one actionable technical root cause",
                "causal_field_audits": [
                    {
                        "report_field": field_name,
                        "material_assertion_audits": _material_assertion_envelope(
                            report_id=report.report_id,
                            field_name=field_name,
                            field_text=getattr(report, field_name),
                            artifact_ref=artifact_ref,
                        ),
                    }
                    for field_name in causal_fields
                ],
                "causal_certificate_field": certificate_field,
                "relation_decisions": relation_decisions,
                "no_match_closure": (
                    {
                        "reason": "The listed expected issues share no true defect instance, violated obligation, direct symptom, or repair overlap with this valid report.",
                        "basis": "The complete report boundary, every expected issue, and the common artifact closure were compared explicitly.",
                        "source_refs": [
                            f"report:{report.report_id}:claim",
                            artifact_ref,
                        ],
                    }
                    if has_no_match
                    else None
                ),
            }
        )
    return {
        "schema_version": "semantic-judge.response.v11",
        "report_judgments": report_judgments,
        "reason": "Every report and expected issue has complete validity-first sparse relation closure.",
        "basis": "The exact provider schema validates report identity, causal fields, positive relations, and explicit NO coverage.",
        "source_refs": [artifact_ref],
    }


def build_scale_audit(
    judge_input: UnifiedJudgeInput,
    *,
    round_no: int,
    source_format: SourceFormat,
    source_path: str,
    source_hash: str,
    algorithm_source_hash: str,
    model_profile: str,
    model_id: str,
    profile_fingerprint: str,
    context_window_tokens: int,
    profile_max_output_tokens: int,
    generated_at_utc: datetime | None = None,
) -> JudgeScaleAudit:
    """Measure one exact input and two validated sparse response envelopes."""

    response_model = build_exact_response_model(judge_input)
    primary_prompt = build_primary_prompt(judge_input)
    schema_text = json.dumps(
        response_model.model_json_schema(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    all_no_response = response_model.model_validate(
        _structural_response_payload(judge_input, all_positive=False)
    ).model_dump_json(indent=2)
    all_positive_response = response_model.model_validate(
        _structural_response_payload(judge_input, all_positive=True)
    ).model_dump_json(indent=2)
    causal_text_lengths = [
        sum(len(getattr(report, field_name)) for field_name in _causal_field_names(report))
        for report in judge_input.reports
    ]
    assertion_counts = [
        _material_assertion_count(getattr(report, field_name))
        for report in judge_input.reports
        for field_name in _causal_field_names(report)
    ]
    effective_max_output_tokens = min(
        profile_max_output_tokens, JUDGE_MAX_OUTPUT_TOKENS
    )
    system_tokens = _estimated_tokens(SYSTEM_PROMPT)
    primary_tokens = _estimated_tokens(primary_prompt)
    schema_tokens = _estimated_tokens(schema_text)
    request_tokens = system_tokens + primary_tokens + schema_tokens
    all_no_tokens = _estimated_tokens(all_no_response)
    all_positive_tokens = _estimated_tokens(all_positive_response)
    reserved_context_tokens = request_tokens + effective_max_output_tokens
    context_headroom_tokens = context_window_tokens - reserved_context_tokens
    fit_flags = (
        all_no_tokens <= effective_max_output_tokens,
        all_positive_tokens <= effective_max_output_tokens,
        context_headroom_tokens >= 0,
    )
    return JudgeScaleAudit(
        generated_at_utc=generated_at_utc or datetime.now(timezone.utc),
        pair_id=judge_input.pair_id,
        round=round_no,
        source_format=source_format,
        source_path=source_path,
        source_hash=source_hash,
        protocol_version=PROTOCOL_VERSION,
        protocol_sha256=PROTOCOL_SHA256,
        judge_algorithm_version=JUDGE_ALGORITHM_VERSION,
        algorithm_source_hash=algorithm_source_hash,
        prompt_version=PROMPT_VERSION,
        prompt_template_hash=prompt_hash(),
        model_profile=model_profile,
        model_id=model_id,
        profile_fingerprint=profile_fingerprint,
        context_window_tokens=context_window_tokens,
        profile_max_output_tokens=profile_max_output_tokens,
        judge_max_output_tokens=JUDGE_MAX_OUTPUT_TOKENS,
        effective_max_output_tokens=effective_max_output_tokens,
        report_count=len(judge_input.reports),
        expected_count=len(judge_input.expected_issues),
        relation_position_count=(
            len(judge_input.reports) * len(judge_input.expected_issues)
        ),
        report_causal_text_chars=sum(causal_text_lengths),
        maximum_report_causal_text_chars=max(causal_text_lengths, default=0),
        material_assertion_chars_per_row=MATERIAL_ASSERTION_CHARS_PER_ROW,
        material_assertion_envelope_count=sum(assertion_counts),
        maximum_field_material_assertion_envelope_count=max(
            assertion_counts, default=0
        ),
        serialized_input_hash=stable_model_hash(judge_input),
        artifact_closure_hash=judge_input.artifact_closure.closure_hash,
        system_prompt_hash=_sha256_text(SYSTEM_PROMPT),
        primary_prompt_hash=_sha256_text(primary_prompt),
        response_schema_hash=response_schema_hash(response_model),
        system_prompt_chars=len(SYSTEM_PROMPT),
        system_prompt_estimated_tokens=system_tokens,
        primary_prompt_chars=len(primary_prompt),
        primary_prompt_estimated_tokens=primary_tokens,
        response_schema_chars=len(schema_text),
        response_schema_estimated_tokens=schema_tokens,
        request_estimated_tokens=request_tokens,
        all_no_response_hash=_sha256_text(all_no_response),
        all_no_response_chars=len(all_no_response),
        all_no_response_estimated_tokens=all_no_tokens,
        all_positive_response_hash=_sha256_text(all_positive_response),
        all_positive_response_chars=len(all_positive_response),
        all_positive_response_estimated_tokens=all_positive_tokens,
        reserved_context_tokens=reserved_context_tokens,
        context_headroom_tokens=context_headroom_tokens,
        all_no_fits_output_limit=fit_flags[0],
        all_positive_fits_output_limit=fit_flags[1],
        reserved_context_fits_window=fit_flags[2],
        status="pass" if all(fit_flags) else "fail",
        reason="The real unified input, exact dynamic schema, full output allowance, and source-length-derived material-assertion envelopes were checked without a provider call.",
        basis=f"Four-characters-per-token estimates over the frozen prompt, exact payload and schema, plus at least one material assertion row per {MATERIAL_ASSERTION_CHARS_PER_ROW} causal-field characters in both validated response envelopes.",
        source_refs=(
            source_path,
            source_hash,
            algorithm_source_hash,
            stable_model_hash(judge_input),
            judge_input.artifact_closure.closure_hash,
        ),
    )


def _write_model(path: Path, value: JudgeScaleAudit) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = value.model_dump_json(indent=2).encode("utf-8") + b"\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def build_parser() -> argparse.ArgumentParser:
    """Build the provider-free scale-audit command-line contract."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-root", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument(
        "--source-format",
        choices=("x1v2_record", "evidence_discovery_release"),
        required=True,
    )
    parser.add_argument("--source-path", type=Path, required=True)
    parser.add_argument("--pair-id", required=True)
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--profile", default="gpt-5.6-luna")
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Persist a reproducible real-input audit without contacting a provider."""

    args = build_parser().parse_args(argv)
    project_root = Path(__file__).resolve().parents[2]
    verify_snapshot(project_root)
    source_path = args.source_path.expanduser().resolve()
    expected_issues, expected_id_map = load_expected_issues(
        args.ledger.expanduser().resolve(), args.pair_id
    )
    if args.source_format == "x1v2_record":
        reports, adapter_audit, round_no, pair_id = adapt_x1v2_record(
            source_path, expected_id_map
        )
    else:
        reports, adapter_audit, round_no, pair_id = adapt_evidence_discovery_release(
            source_path, expected_id_map
        )
    if pair_id != args.pair_id or round_no != args.round:
        raise ValueError(
            f"source identity mismatch: expected pair={args.pair_id},round={args.round}; "
            f"actual pair={pair_id},round={round_no}"
        )
    closure = build_artifact_closure(args.report_root, pair_id)
    judge_input = build_unified_input(
        reports=reports,
        expected_issues=expected_issues,
        artifact_closure=closure,
    )
    profile = load_llm_registry().require(args.profile)
    if profile.context_window_tokens is None or profile.max_output_tokens is None:
        raise ValueError(
            "scale audit requires explicit context_window_tokens and max_output_tokens"
        )
    audit = build_scale_audit(
        judge_input,
        round_no=round_no,
        source_format=args.source_format,
        source_path=str(source_path),
        source_hash=adapter_audit.source_hash,
        algorithm_source_hash=_algorithm_source_hash(),
        model_profile=args.profile,
        model_id=profile.model,
        profile_fingerprint=profile.fingerprint(),
        context_window_tokens=profile.context_window_tokens,
        profile_max_output_tokens=profile.max_output_tokens,
    )
    _write_model(args.output.expanduser().resolve(), audit)
    print(audit.model_dump_json(indent=2), flush=True)
    return 0 if audit.status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
