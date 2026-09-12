"""Pydantic contract and renderer for the 19-predicate capability audit."""

from __future__ import annotations

import argparse
import json
from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from .predicate_gold import SHA256_PATTERN, SourceRef, StrictModel

CAPABILITY_SCHEMA_VERSION = "paper1.predicate-gold.capability-audit.v1"


class CheckResult(str, Enum):
    """Outcome of comparing registry, typed schema, backend, and native semantics."""

    PASS = "PASS"
    FAIL = "FAIL"
    BOUNDARY = "BOUNDARY"


class FindingResolution(str, Enum):
    """Resolution state of an audit finding without rewriting frozen runtime."""

    NO_ACTION_REQUIRED = "NO_ACTION_REQUIRED"
    CONTAINED_BY_GOLD_PROTOCOL = "CONTAINED_BY_GOLD_PROTOCOL"
    OPEN_HIGH_SEVERITY = "OPEN_HIGH_SEVERITY"


class CapabilityFinding(StrictModel):
    """One source-level contract difference or semantic boundary."""

    finding_id: str = Field(description="Stable capability-audit finding identity.", min_length=1)
    predicate_id: str = Field(description="Frozen predicate ID affected by this finding.", min_length=1)
    result: CheckResult = Field(description="PASS, FAIL, or non-failing semantic BOUNDARY result.")
    severity: Literal["HIGH", "MEDIUM", "LOW"] = Field(description="Impact severity for predicate-gold construction.")
    title: str = Field(description="Concise source-level finding title.", min_length=1)
    observed_contract: str = Field(description="Actual typed/backend/native behavior established from source.", min_length=1)
    declared_contract: str = Field(description="Registry or public typed contract being compared.", min_length=1)
    gold_impact: str = Field(description="How this difference constrains issue-level exactness or typed inputs.", min_length=1)
    resolution_status: FindingResolution = Field(description="Whether the finding is contained, requires no action, or remains high severity.")
    resolution: str = Field(description="Evaluation-only containment or explicit remaining action; never a silent runtime rewrite.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Registry, typed-schema, backend, native API, or test evidence.", min_length=2)


class PredicateCapability(StrictModel):
    """Source-audited executable semantics and limitations of one frozen predicate."""

    predicate_id: str = Field(description="Frozen public predicate identity.", pattern=r"^[SGRV][1-6]$")
    family: Literal["structure", "topology", "trajectory", "bounded_verification"] = Field(description="Frozen predicate family.")
    registry_name: str = Field(description="Frozen registry predicate name.", min_length=1)
    registry_semantics: str = Field(description="Frozen registry semantics text.", min_length=1)
    registry_inputs: tuple[str, ...] = Field(description="Input names declared by the frozen registry.")
    typed_input_model: str = Field(description="Concrete Pydantic input model used before backend dispatch.", min_length=1)
    typed_acceptance: str = Field(description="Actual legal typed values and backend-specific checks.", min_length=1)
    backend_entrypoint: str = Field(description="Repository path and function that dispatch this predicate.", min_length=1)
    backend_domain: str = Field(description="Native model, topology, runtime, or FBMCQ domain actually evaluated.", min_length=1)
    native_apis: tuple[str, ...] = Field(description="pyfcstm public classes/functions used to obtain the result.", min_length=1)
    quantifier: str = Field(description="Existential, universal, equality, membership, or scenario-local quantification actually implemented.", min_length=1)
    scope: str = Field(description="Closed model, exact owner, state set, trace window, hot/cold scope, or other actual scope.", min_length=1)
    timing_rtc: str = Field(description="Direct authored fact, topology path, sampled macrostep, RTC, or bounded-frame timing semantics.", min_length=1)
    observable: str = Field(description="Exact state, transition, event, action, guard/effect AST, path, call, or termination observable.", min_length=1)
    approximation: str = Field(description="Over-approximation, under-approximation, vacuity, or exact local-fragment boundary.", min_length=1)
    bound_domain: str = Field(description="Finite horizon/domain behavior or an explicit not-applicable statement.", min_length=1)
    boolean_boundary: str = Field(description="Conditions for completed true/false and all outcomes that remain unknown/error/timeout.", min_length=1)
    evaluation_only_reuse: str = Field(description="Exact obligation fragments for which evaluation may reuse this frozen backend.", min_length=1)
    semantic_gaps: tuple[str, ...] = Field(description="Obligation dimensions this predicate cannot establish by itself.")
    check_result: CheckResult = Field(description="Overall source audit result for registry/backend agreement and semantic limits.")
    finding_ids: tuple[str, ...] = Field(description="Capability finding IDs associated with this predicate.")
    existing_test_refs: tuple[SourceRef, ...] = Field(description="Existing conformance or boundary tests read during the audit.")
    missing_test_cases: tuple[str, ...] = Field(description="Targeted tests still required before final Gate C/F closure.")
    source_refs: tuple[SourceRef, ...] = Field(description="Registry, typed-schema, backend, and native-semantics evidence.", min_length=3)


class PredicateCapabilityAudit(StrictModel):
    """Complete source-level capability audit for all 19 frozen predicates."""

    schema_version: Literal[CAPABILITY_SCHEMA_VERSION] = Field(default=CAPABILITY_SCHEMA_VERSION, description="Capability audit schema version.")
    registry_path: str = Field(description="Repository-relative frozen predicate registry path.", min_length=1)
    registry_sha256: str = Field(description="SHA-256 of the frozen registry bytes.", pattern=SHA256_PATTERN)
    source_commit: str = Field(description="Repository commit whose frozen code was audited.", pattern=r"^[0-9a-f]{40}$")
    reviewer_id: str = Field(description="Independent source-audit reviewer identity.", min_length=1)
    reviewed_at: str = Field(description="UTC audit completion time.", min_length=1)
    input_paths_sha256: dict[str, str] = Field(description="Repository-relative audited source paths mapped to exact SHA-256 digests.", min_length=1)
    predicates: tuple[PredicateCapability, ...] = Field(description="Exactly one capability row for each frozen public predicate.", min_length=19, max_length=19)
    findings: tuple[CapabilityFinding, ...] = Field(description="All source-level contract differences and their evaluation-only containment.")
    actual_commands: tuple[str, ...] = Field(description="Read-only commands used by the independent audit.", min_length=1)
    method_runtime_modified: Literal[False] = Field(description="The frozen registry and runtime remain unchanged.")
    v60_outputs_read_for_assignment: Literal[False] = Field(description="v60 actual outputs were not used to assign expected predicate gold.")
    provider_calls: Literal[0] = Field(description="No provider was called by this source-level audit.")
    reason: str = Field(description="Why this audit describes capability rather than assigning issue-level gold.", min_length=1)
    basis: str = Field(description="Registry, typed-schema, backend, tests, and pyfcstm source basis.", min_length=1)

    @model_validator(mode="after")
    def validate_complete_registry(self) -> PredicateCapabilityAudit:
        """Require exactly S1-S6, G1-G4, R1-R4, and V1-V5 once each."""

        expected = {*(f"S{i}" for i in range(1, 7)), *(f"G{i}" for i in range(1, 5)), *(f"R{i}" for i in range(1, 5)), *(f"V{i}" for i in range(1, 6))}
        observed = [row.predicate_id for row in self.predicates]
        if len(observed) != len(set(observed)) or set(observed) != expected:
            raise ValueError("capability audit must contain each frozen predicate exactly once")
        finding_ids = {finding.finding_id for finding in self.findings}
        if any(not set(row.finding_ids).issubset(finding_ids) for row in self.predicates):
            raise ValueError("predicate rows reference unknown capability findings")
        if any(finding.result == CheckResult.FAIL and finding.resolution_status == FindingResolution.NO_ACTION_REQUIRED for finding in self.findings):
            raise ValueError("FAIL findings require containment or an open high-severity disposition")
        return self


def render_markdown(audit: PredicateCapabilityAudit) -> str:
    """Render a compact human-readable table from the canonical audit JSON."""

    lines = [
        "# Predicate Semantics Capability Audit",
        "",
        f"Schema: `{audit.schema_version}`. Registry: `{audit.registry_sha256}`. Source commit: `{audit.source_commit}`.",
        "",
        "This is a source-level capability audit. It does not assign any ledger issue to a predicate and does not alter the frozen runtime.",
        "",
        "| ID | Actual quantifier/scope | Timing/observable | Approximation and exact-use boundary | Result |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in audit.predicates:
        boundary = f"{row.approximation} Exact reuse: {row.evaluation_only_reuse}"
        lines.append(f"| {row.predicate_id} | {row.quantifier}; {row.scope} | {row.timing_rtc}; {row.observable} | {boundary} | {row.check_result.value} |")
    lines.extend(["", "## Contract Findings", ""])
    if not audit.findings:
        lines.append("No registry/schema/backend contract differences were found.")
    for finding in audit.findings:
        lines.extend(
            [
                f"### {finding.finding_id}: {finding.title}",
                "",
                f"Result: `{finding.result.value}`; severity: `{finding.severity}`; resolution: `{finding.resolution_status.value}`.",
                "",
                finding.observed_contract,
                "",
                f"Gold impact: {finding.gold_impact}",
                "",
                f"Containment: {finding.resolution}",
                "",
            ]
        )
    lines.extend(["## Boolean Boundary", "", "A backend result counts only when the receipt is terminal `completed` with Boolean `true` or `false`. Invalid input, unsupported backend, timeout, worker failure, solver failure, and replay mismatch are not `false`.", ""])
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    """Build the capability-audit validation and render parser."""

    parser = argparse.ArgumentParser(description="Validate and render the predicate capability audit.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--markdown", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate canonical capability JSON and optionally render Markdown."""

    args = _parser().parse_args(argv)
    audit = PredicateCapabilityAudit.model_validate_json(args.input.read_text(encoding="utf-8"))
    if args.markdown is not None:
        args.markdown.write_text(render_markdown(audit), encoding="utf-8")
    print(json.dumps({"predicates": len(audit.predicates), "findings": len(audit.findings), "open_high_severity": sum(finding.resolution_status == FindingResolution.OPEN_HIGH_SEVERITY for finding in audit.findings)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
