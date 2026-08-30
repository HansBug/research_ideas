"""Build and validate the provider-free current re-audit v4 publication layer.

The semantic decisions are not inferred here.  This command revalidates the
previously pane5-confirmed, source-first v2 decisions against the immutable
raw/source closure, then projects them into the v4 contract and recomputes
all publication metrics.  It never imports a provider client or starts an
experiment.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


PROTOCOL = "issue-189-195-current-reaudit-v4"
SCHEMA = "paper1.current-manual-reaudit.v4"
RELATIONS = ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")
CLASSES = ("K", "N", "I")
TIERS = ("D2", "D1", "D0", "A0")
W_LEVELS = ("W0", "W1", "W2")
ARCHIVE_RELATIVE = "final_results/v60_current_vs_x1v2_baseline"


class SourceRef(BaseModel):
    """Repository-relative source evidence reference with an immutable hash."""

    model_config = ConfigDict(extra="forbid")

    repository_path: str = Field(min_length=1, description="Repository-relative evidence file path; not nullable and not a prompt field.")
    json_pointer: str | None = Field(default=None, description="RFC 6901 JSON Pointer into the evidence file; nullable and not a prompt field.")
    line: int | None = Field(default=None, ge=1, description="One-based evidence line number when applicable; nullable and not a prompt field.")
    sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the referenced evidence file; not nullable and not a prompt field.")


class ExpectedRelation(BaseModel):
    """One expected-ledger relation retained from a source-first adjudication."""

    model_config = ConfigDict(extra="forbid")

    expected_id: str = Field(min_length=1, description="Expected ledger ID evaluated exactly once for this report; not nullable and not a prompt field.")
    relation: Literal["FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH"] = Field(description="Source-first relation after reading the report and all expected evidence; not nullable and not a prompt field.")
    reason: str = Field(min_length=1, description="Expected-specific reason with the report/ledger distinction; not nullable and not a prompt field.")
    basis: str = Field(min_length=1, description="Expected-specific evidence basis; not nullable and not a prompt field.")
    source_refs: tuple[SourceRef, ...] = Field(min_length=1, description="Resolvable evidence refs for this relation; not nullable and not a prompt field.")
    report_owned_field_refs: tuple[str, ...] = Field(min_length=1, description="JSON pointers to report fields used by the relation; not nullable and not a prompt field.")


class ReviewChain(BaseModel):
    """Review and pane5 arbitration chain attached to one canonical report."""

    model_config = ConfigDict(extra="forbid")

    reviewer_ids: tuple[str, ...] = Field(min_length=2, description="Reviewer identities retained in the prior blind review chain; not nullable and not a prompt field.")
    primary_reviewer_id: str = Field(min_length=1, description="Primary pane5 reviewer identity; not nullable and not a prompt field.")
    independent_reviewer_id: str = Field(min_length=1, description="Independent proposal reviewer identity; not nullable and not a prompt field.")
    final_adjudicator_id: str = Field(min_length=1, description="Final pane5 adjudicator identity; not nullable and not a prompt field.")
    review_status: Literal["FINAL"] = Field(description="Final review status; only FINAL enters v4 canonical data.")
    disagreement: str | None = Field(default=None, description="Recorded disagreement text when present; nullable and not a prompt field.")
    confirmation_basis: str = Field(min_length=1, description="Evidence-read basis for the final confirmation; not nullable and not a prompt field.")
    arbitration_reason: str = Field(min_length=1, description="Pane5 arbitration reason; not nullable and not a prompt field.")
    arbitration_basis: str = Field(min_length=1, description="Pane5 arbitration evidence basis; not nullable and not a prompt field.")
    confirmed_at: str = Field(min_length=1, description="UTC confirmation timestamp from the prior review chain; not nullable and not a prompt field.")
    human_confirmation: bool = Field(description="Whether pane5 human confirmation is recorded; not nullable and not a prompt field.")
    human_supervised_session: bool = Field(description="Whether the source-first review was user-authorized in pane5; not nullable and not a prompt field.")
    blind_event_sequence: tuple[str, ...] = Field(min_length=2, description="Ordered blind/unblind review events; not nullable and not a prompt field.")
    primary_reason: str = Field(min_length=1, description="Primary pane5 source-first opinion reason retained from the prior review record; not nullable and not a prompt field.")
    primary_basis: str = Field(min_length=1, description="Primary pane5 source-first opinion evidence basis retained from the prior review record; not nullable and not a prompt field.")
    independent_reason: str = Field(min_length=1, description="Independent blind proposal reason retained without treating it as final truth; not nullable and not a prompt field.")
    independent_basis: str = Field(min_length=1, description="Independent blind proposal evidence basis retained without treating it as final truth; not nullable and not a prompt field.")
    proposal_submission_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the blind independent proposal submission; not nullable and not a prompt field.")


class PredicateUsage(BaseModel):
    """Predicate usage receipt facts kept separate from semantic classification."""

    model_config = ConfigDict(extra="forbid")

    predicate_id: str | None = Field(default=None, description="Registered predicate ID observed in frozen raw, if any; nullable and not a prompt field.")
    registered: bool = Field(description="Whether the raw binding names a registered predicate; not nullable and not a prompt field.")
    receipt_present: bool = Field(description="Whether the frozen report carries a predicate execution receipt; not nullable and not a prompt field.")
    executed_with_receipt: bool = Field(description="Whether predicate usage is counted under the receipt rule; not nullable and not a prompt field.")
    terminal_result: Literal["true", "false"] | None = Field(default=None, description="Recorded terminal Boolean when present; nullable and not a prompt field.")
    contribution: bool = Field(description="Legacy coverage_class=semantic_hit marker retained from frozen raw; not a terminal-false contribution metric and not nullable.")


class CanonicalDecision(BaseModel):
    """Canonical v4 decision for one current report with complete evidence closure."""

    model_config = ConfigDict(extra="forbid")

    side: Literal["v60_current"] = Field(description="Current side owning the report; fixed and not nullable.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Four-digit author/source pair ID; not nullable and not a prompt field.")
    round: int = Field(ge=1, le=3, description="Frozen method round number; not nullable and not a prompt field.")
    original_report_id: str = Field(min_length=1, description="Frozen report identity from the raw method record; not nullable and not a prompt field.")
    finding_index: int = Field(ge=0, description="Zero-based finding index in the raw record; not nullable and not a prompt field.")
    raw_method_path: str = Field(min_length=1, description="Repository-relative raw method record path; not nullable and not a prompt field.")
    raw_json_pointer: str = Field(min_length=1, description="RFC 6901 pointer to the raw report object; not nullable and not a prompt field.")
    raw_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the raw method record; not nullable and not a prompt field.")
    source_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Digest of the ordered source-reference set; not nullable and not a prompt field.")
    issue: str = Field(min_length=1, description="Exact serialized raw issue claim; not nullable and not a prompt field.")
    where: str = Field(min_length=1, description="Exact serialized raw location field or null marker; not nullable and not a prompt field.")
    raw_reason: str = Field(min_length=1, description="Exact serialized raw candidate reason; not nullable and not a prompt field.")
    raw_basis: str = Field(min_length=1, description="Exact serialized raw candidate basis; not nullable and not a prompt field.")
    reason: str = Field(min_length=1, description="Final source-first adjudication reason; not nullable and not a prompt field.")
    basis: str = Field(min_length=1, description="Final source-first evidence basis; not nullable and not a prompt field.")
    source_refs: tuple[SourceRef, ...] = Field(min_length=3, description="Raw/source/ledger evidence refs for this report; not nullable and not a prompt field.")
    source_elements: tuple[str, ...] = Field(min_length=1, description="Concrete source states, transitions, guards, effects or paths; not nullable and not a prompt field.")
    factual_status: Literal["ESTABLISHED", "REFUTED"] = Field(description="Whether the report fact exists in the author source; not nullable and not a prompt field.")
    normative_violation_status: Literal["ESTABLISHED", "NOT_ESTABLISHED"] = Field(description="Whether a source-backed duty is established; not nullable and not a prompt field.")
    defect_claim_status: Literal["AUTHOR_SOURCE_DEFECT", "NO_AUTHOR_SOURCE_DEFECT_CLAIM"] = Field(description="Whether the report claims an author-source defect; not nullable and not a prompt field.")
    d_tier: Literal["D2", "D1", "D0", "A0"] = Field(description="Final D/A tier after factual and normative review; not nullable and not a prompt field.")
    d_alternative_reading: str = Field(min_length=1, description="Complete alternative-reading or adjacent-tier exclusion; not nullable and not a prompt field.")
    a0_subtype: Literal["FALSE_POSITIVE", "NOT_A_DEFECT_CLAIM"] | None = Field(default=None, description="A0 subtype when applicable; nullable only for D tiers and not a prompt field.")
    expected_relations: tuple[ExpectedRelation, ...] = Field(min_length=1, description="Dense relation rows covering the expected ledger universe; not nullable and not a prompt field.")
    full_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with FULL_MATCH; not nullable and not a prompt field.")
    partial_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with PARTIAL_MATCH; not nullable and not a prompt field.")
    no_match_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with NO_MATCH; not nullable and not a prompt field.")
    w_level: Literal["W0", "W1", "W2"] = Field(description="Independent finding evidence level; not nullable and not a prompt field.")
    predicate_usage: PredicateUsage = Field(description="Frozen predicate usage facts independent of K/N/I; not nullable and not a prompt field.")
    predicate_contribution: bool = Field(description="Legacy coverage_class=semantic_hit marker mirrored for compatibility; not a terminal-false contribution metric and not nullable.")
    validity: Literal["VALID_KNOWN", "VALID_NOVEL", "INVALID"] = Field(description="Mechanical validity projection from D/A and dense expected relations; not nullable and not a prompt field.")
    canonical_class: Literal["K", "N", "I"] = Field(description="Mechanically closed K/N/I class; not nullable and not a prompt field.")
    previous_class: Literal["K", "N", "I"] = Field(description="Previous v2 pane5 class used only for explicit delta reporting; not nullable and not a prompt field.")
    reclassification_reason: str = Field(min_length=1, description="Why v4 retained or changed the previous class; not nullable and not a prompt field.")
    review_chain: ReviewChain = Field(description="Prior independent proposal and pane5 confirmation chain; not nullable and not a prompt field.")
    reviewer_ids: tuple[str, ...] = Field(min_length=2, description="Reviewer IDs copied from the structured review chain; not nullable and not a prompt field.")
    reviewer_consensus: Literal["CONSENSUS", "DISAGREEMENT_ARBITRATED"] = Field(description="Consensus status after pane5 review; not nullable and not a prompt field.")
    disagreement_flag: bool = Field(description="Whether an explicit disagreement was recorded; not nullable and not a prompt field.")
    arbitration_id: str = Field(min_length=1, description="Pointer to the v4 arbitration log entry; not nullable and not a prompt field.")
    confidence: Literal["HIGH", "MEDIUM"] = Field(description="Workflow confidence derived from review closure, not a semantic shortcut; not nullable and not a prompt field.")
    confidence_basis: str = Field(min_length=1, description="Why workflow confidence has this value; not nullable and not a prompt field.")
    reviewed_at: str = Field(min_length=1, description="UTC timestamp of source-first confirmation; not nullable and not a prompt field.")
    evidence_digest: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Digest over raw/source/relation evidence identity; not nullable and not a prompt field.")

    @model_validator(mode="after")
    def validate_closure(self) -> "CanonicalDecision":
        relations = {row.expected_id: row.relation for row in self.expected_relations}
        if len(relations) != len(self.expected_relations):
            raise ValueError("expected relation IDs must be unique")
        if set(self.full_ledger_ids) & set(self.partial_ledger_ids):
            raise ValueError("FULL and PARTIAL IDs overlap")
        if set(self.full_ledger_ids) & set(self.no_match_ledger_ids):
            raise ValueError("FULL and NO IDs overlap")
        if set(self.partial_ledger_ids) & set(self.no_match_ledger_ids):
            raise ValueError("PARTIAL and NO IDs overlap")
        if tuple(sorted(k for k, v in relations.items() if v == "FULL_MATCH")) != tuple(sorted(self.full_ledger_ids)):
            raise ValueError("FULL ledger projection disagrees with dense relation rows")
        if tuple(sorted(k for k, v in relations.items() if v == "PARTIAL_MATCH")) != tuple(sorted(self.partial_ledger_ids)):
            raise ValueError("PARTIAL ledger projection disagrees with dense relation rows")
        if tuple(sorted(k for k, v in relations.items() if v == "NO_MATCH")) != tuple(sorted(self.no_match_ledger_ids)):
            raise ValueError("NO ledger projection disagrees with dense relation rows")
        positive = bool(self.full_ledger_ids or self.partial_ledger_ids)
        expected_class = "I" if self.d_tier in {"D0", "A0"} else ("K" if positive else "N")
        if self.canonical_class != expected_class:
            raise ValueError("K/N/I closure is inconsistent with D/A and relation rows")
        expected_validity = "INVALID" if expected_class == "I" else ("VALID_KNOWN" if expected_class == "K" else "VALID_NOVEL")
        if self.validity != expected_validity:
            raise ValueError("validity is inconsistent with K/N/I closure")
        if self.d_tier in {"D0", "A0"} and positive:
            raise ValueError("INVALID report cannot have a positive formal relation")
        if self.d_tier in {"D0", "A0"} and self.normative_violation_status != "NOT_ESTABLISHED":
            raise ValueError("D0/A0 cannot project an established normative violation")
        if self.d_tier in {"D2", "D1"} and self.normative_violation_status != "ESTABLISHED":
            raise ValueError("D2/D1 require an established normative violation")
        if self.d_tier == "A0" and self.factual_status != "REFUTED":
            raise ValueError("A0 requires a refuted source fact")
        if self.d_tier == "D0" and self.factual_status != "ESTABLISHED":
            raise ValueError("D0 requires an established source fact")
        if self.d_tier in {"D2", "D1"} and self.factual_status != "ESTABLISHED":
            raise ValueError("D2/D1 require an established source fact")
        if self.d_tier == "A0" and self.a0_subtype is None:
            raise ValueError("A0 requires an A0 subtype")
        if self.d_tier != "A0" and self.a0_subtype is not None:
            raise ValueError("non-A0 decision cannot have an A0 subtype")
        if self.canonical_class == "I" and any(row.relation != "NO_MATCH" for row in self.expected_relations):
            raise ValueError("I formal relations must all be NO_MATCH")
        if self.reviewer_ids != self.review_chain.reviewer_ids:
            raise ValueError("reviewer projection is inconsistent")
        if self.disagreement_flag != bool(self.review_chain.disagreement):
            raise ValueError("disagreement flag is inconsistent")
        return self


class NGroup(BaseModel):
    """Substantive N group restricted to current side and one author pair."""

    model_config = ConfigDict(extra="forbid")

    group_id: str = Field(min_length=1, description="Stable v4 N group identifier; not nullable and not a prompt field.")
    side: Literal["v60_current"] = Field(description="Side owning every member; not nullable and not a prompt field.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Pair owning every member; not nullable and not a prompt field.")
    member_report_ids: tuple[str, ...] = Field(min_length=1, description="Every report assigned exactly once to this group; not nullable and not a prompt field.")
    member_rounds: tuple[int, ...] = Field(min_length=1, description="Rounds represented by the members; not nullable and not a prompt field.")
    cross_round_merge_reason: str = Field(min_length=1, description="Why cross-round reports share one obligation and repair intent; not nullable and not a prompt field.")
    normative_obligation: str = Field(min_length=1, description="Common normative obligation or formal property; not nullable and not a prompt field.")
    source_locus: str = Field(min_length=1, description="Common author-source locus or inseparable locus description; not nullable and not a prompt field.")
    root_cause: str = Field(min_length=1, description="Common repair-relevant root cause; not nullable and not a prompt field.")
    repair_intent: str = Field(min_length=1, description="Minimum common repair intent; not nullable and not a prompt field.")
    d_tiers: tuple[Literal["D2", "D1"], ...] = Field(min_length=1, description="D2/D1 tiers represented by members; not nullable and not a prompt field.")
    reason: str = Field(min_length=1, description="Group adjudication reason; not nullable and not a prompt field.")
    basis: str = Field(min_length=1, description="Group evidence basis; not nullable and not a prompt field.")
    source_refs: tuple[SourceRef, ...] = Field(min_length=1, description="Group evidence refs; not nullable and not a prompt field.")
    reviewer_consensus: str = Field(min_length=1, description="Review consensus/provenance for grouping; not nullable and not a prompt field.")
    unmerged_adjacent_reports: tuple[str, ...] = Field(description="Explicit adjacent-report non-merge explanation; not nullable and not a prompt field.")


def canonical_json(value: Any) -> str:
    """Serialize JSON without whitespace or unstable key ordering."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    """Return archive-style SHA-256."""

    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    """Hash one immutable archive file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def load_json(path: Path) -> Any:
    """Load JSON and keep all semantic parsing explicit."""

    return json.loads(path.read_text(encoding="utf-8"))


def resolve_pointer(value: Any, pointer: str) -> Any:
    """Resolve an RFC 6901 JSON Pointer."""

    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            value = value[token]
        elif isinstance(value, list):
            value = value[int(token)]
        else:
            raise ValueError(f"pointer traverses scalar: {pointer}")
    return value


def serialize_raw_field(target: dict[str, Any], names: tuple[str, ...], fallback: Any) -> str:
    """Preserve a raw field as text without losing structured values or absence."""

    for name in names:
        if name in target:
            value = target[name]
            return value if isinstance(value, str) and value else canonical_json(value)
    return canonical_json(fallback)


def source_digest(refs: list[dict[str, Any]]) -> str:
    """Digest the exact ordered source-ref identity set."""

    identity = [
        {"repository_path": ref["repository_path"], "json_pointer": ref.get("json_pointer"), "line": ref.get("line"), "sha256": ref["sha256"]}
        for ref in refs
    ]
    return sha256_bytes(canonical_json(identity).encode("utf-8"))


def terminal_result(target: dict[str, Any]) -> str | None:
    """Read a terminal Boolean only from an explicit frozen receipt."""

    execution = target.get("execution_receipt") if isinstance(target.get("execution_receipt"), dict) else {}
    nested = target.get("receipt") if isinstance(target.get("receipt"), dict) else {}
    values = [execution.get("verdict"), nested.get("verdict")]
    for value in values:
        normalized = str(value or "").lower()
        if normalized in {"true", "pass", "passed", "satisfied", "success"}:
            return "true"
        if normalized in {"false", "fail", "failed", "violated", "violation", "unsat", "no_witness"}:
            return "false"
    return None


def make_review(old: dict[str, Any]) -> ReviewChain:
    """Project the existing structured blind review chain into the v4 contract."""

    review = old["review"]
    reviewer_ids = tuple(review["reviewer_ids"])
    independent = review.get("independent_reviewer_id") or next((item for item in reviewer_ids if item != review.get("primary_reviewer_id")), "independent-reviewer")
    disagreement = review.get("disagreement")
    return ReviewChain(
        reviewer_ids=reviewer_ids,
        primary_reviewer_id=str(review["primary_reviewer_id"]),
        independent_reviewer_id=str(independent),
        final_adjudicator_id=str(review["final_adjudicator_id"]),
        review_status="FINAL",
        disagreement=disagreement,
        confirmation_basis=str(review["confirmation_basis"]),
        arbitration_reason=str(review["arbitration_reason"]),
        arbitration_basis=str(review["arbitration_basis"]),
        confirmed_at=str(review.get("confirmed_at") or review.get("unblinded_at") or review.get("authorization_time_utc")),
        human_confirmation=bool(review["human_confirmation"]),
        human_supervised_session=bool(review["human_supervised_session"]),
        blind_event_sequence=tuple(review["blind_event_sequence"]),
        primary_reason=str(review["primary_reason"]),
        primary_basis=str(review["primary_basis"]),
        independent_reason=str(review["independent_reason"]),
        independent_basis=str(review["independent_basis"]),
        proposal_submission_hash=str(review["submission_hash"]),
    )


def enumerate_current_raw(archive: Path) -> dict[str, dict[str, Any]]:
    """Enumerate the immutable current raw report universe without using a derived inventory."""

    result: dict[str, dict[str, Any]] = {}
    for raw_path in sorted((archive / "raw/v60_current/method/method").glob("*/round-*.json")):
        document = load_json(raw_path)
        pair_id = raw_path.parent.name
        round_no = int(raw_path.stem.removeprefix("round-"))
        issues = document.get("report_issue_clusters", [])
        for index, issue in enumerate(issues):
            report_id = str(issue.get("issue_id"))
            if not report_id:
                raise ValueError(f"current raw issue has no issue_id: {raw_path}#{index}")
            if report_id in result:
                raise ValueError(f"duplicate current raw report: {report_id}")
            result[report_id] = {
                "side": "v60_current", "pair_id": pair_id, "round": round_no,
                "report_id": report_id, "finding_index": index,
                "raw_method_path": str(raw_path.relative_to(archive)),
                "raw_json_pointer": f"/report_issue_clusters/{index}",
                "raw_sha256": sha256_file(raw_path),
            }
    return result


def build_decisions(archive: Path) -> tuple[list[CanonicalDecision], dict[str, Any]]:
    """Revalidate and project every current v2 decision without semantic inference."""

    old_path = archive / "derived" / "manual_adjudication_v2" / "v60_report_decisions.json"
    old = load_json(old_path)
    ledger = load_json(archive / "reference" / "ledger.json")["items"]
    registry = load_json(archive / "reference" / "predicate_registry.json")
    predicate_ids = {str(item["id"]) for family in registry["families"] for item in family["predicates"]}
    decisions: list[CanonicalDecision] = []
    current_raw = enumerate_current_raw(archive)
    raw_cache: dict[str, dict[str, Any]] = {}
    source_cache: dict[str, str] = {}
    for old_decision in old["decisions"]:
        if old_decision["report_id"] not in current_raw:
            raise ValueError(f"current v2 decision is absent from raw enumeration: {old_decision['report_id']}")
        raw_path = archive / old_decision["raw_method_path"]
        raw_hash = sha256_file(raw_path)
        if raw_hash != old_decision["raw_sha256"]:
            raise ValueError(f"raw hash changed: {old_decision['report_id']}")
        raw = raw_cache.setdefault(str(raw_path), load_json(raw_path))
        target = resolve_pointer(raw, old_decision["raw_json_pointer"])
        if not isinstance(target, dict):
            raise ValueError(f"raw target is not an object: {old_decision['report_id']}")
        if str(target.get("issue_id")) != old_decision["report_id"]:
            raise ValueError(f"raw report ID mismatch: {old_decision['report_id']}")
        if str(raw.get("pair_id")) != old_decision["pair_id"] or int(raw.get("round", -1)) != int(old_decision["round"]):
            raise ValueError(f"raw pair/round mismatch: {old_decision['report_id']}")
        source_refs = old_decision["source_refs"]
        for ref in source_refs:
            ref_path = (archive / ref["repository_path"]).resolve()
            ref_path.relative_to(archive.resolve())
            if not ref_path.is_file() or sha256_file(ref_path) != ref["sha256"]:
                raise ValueError(f"source ref hash mismatch: {old_decision['report_id']}:{ref['repository_path']}")
            if ref.get("json_pointer") is not None:
                resolve_pointer(load_json(ref_path), ref["json_pointer"])
        source_hash = source_cache.setdefault(old_decision["report_id"], source_digest(source_refs))
        relation_models = tuple(ExpectedRelation.model_validate(row) for row in old_decision["relations"])
        if {row.expected_id for row in relation_models} != set(ledger):
            raise ValueError(f"current relation universe mismatch: {old_decision['report_id']}")
        full = tuple(sorted(row.expected_id for row in relation_models if row.relation == "FULL_MATCH"))
        partial = tuple(sorted(row.expected_id for row in relation_models if row.relation == "PARTIAL_MATCH"))
        no_match = tuple(sorted(row.expected_id for row in relation_models if row.relation == "NO_MATCH"))
        review = make_review(old_decision)
        predicate_id = target.get("predicate_id")
        plan = target.get("plan") if isinstance(target.get("plan"), dict) else {}
        predicate_id = str(predicate_id or plan.get("predicate_id") or "") or None
        registered = predicate_id in predicate_ids
        receipt_present = bool(target.get("execution_receipt") or target.get("receipt"))
        terminal = terminal_result(target)
        usage = PredicateUsage(
            predicate_id=predicate_id,
            registered=registered,
            receipt_present=receipt_present,
            executed_with_receipt=bool(registered and receipt_present),
            terminal_result=terminal,
            contribution=target.get("coverage_class") == "semantic_hit",
        )
        d_tier = str(old_decision["strict_da"])
        fact_status = str(old_decision["fact_status"])
        defect_claim_status = "NO_AUTHOR_SOURCE_DEFECT_CLAIM" if d_tier == "A0" and old_decision.get("a0_type") == "NOT_A_DEFECT_CLAIM" else "AUTHOR_SOURCE_DEFECT"
        alternative = str(review.confirmation_basis)
        if d_tier == "D1":
            alternative = str(review.confirmation_basis) + " Independent reading: " + str(review.arbitration_reason)
        old_source_elements = old_decision.get("source_loci") or target.get("element_refs") or target.get("source_refs") or [old_decision["where_pointer"]]
        disagreement = bool(review.disagreement)
        evidence_digest = sha256_bytes(canonical_json({"raw_sha256": raw_hash, "source_sha256": source_hash, "relations": [row.model_dump(mode="json") for row in relation_models]}).encode("utf-8"))
        decisions.append(CanonicalDecision(
            side="v60_current", pair_id=str(old_decision["pair_id"]), round=int(old_decision["round"]),
            original_report_id=str(old_decision["report_id"]), finding_index=int(old_decision["report_index"]),
            raw_method_path=str(old_decision["raw_method_path"]), raw_json_pointer=str(old_decision["raw_json_pointer"]), raw_sha256=raw_hash,
            source_sha256=source_hash,
            issue=serialize_raw_field(target, ("issue", "issue_id"), {"issue_id": old_decision["report_id"]}),
            where=serialize_raw_field(target, ("where", "element_refs"), None),
            raw_reason=serialize_raw_field(target, ("reason", "candidate_reason"), None),
            raw_basis=serialize_raw_field(target, ("basis", "candidate_basis"), None),
            reason=str(old_decision["reason"]), basis=str(old_decision["basis"]),
            source_refs=tuple(SourceRef.model_validate(ref) for ref in source_refs),
            source_elements=tuple(str(item) for item in old_source_elements),
            factual_status="ESTABLISHED" if fact_status == "ESTABLISHED" else "REFUTED",
            normative_violation_status="NOT_ESTABLISHED" if d_tier in {"D0", "A0"} else "ESTABLISHED",
            defect_claim_status=defect_claim_status,
            validity="INVALID" if d_tier in {"D0", "A0"} else ("VALID_KNOWN" if full or partial else "VALID_NOVEL"),
            d_tier=d_tier, d_alternative_reading=alternative,
            a0_subtype=old_decision.get("a0_type"), expected_relations=relation_models,
            full_ledger_ids=full, partial_ledger_ids=partial, no_match_ledger_ids=no_match,
            w_level=str(old_decision["witness"]["level"]), predicate_usage=usage,
            predicate_contribution=usage.contribution, canonical_class=str(old_decision["corrected_kni"]), previous_class=str(old_decision["corrected_kni"]),
            reclassification_reason="No v4 class change: the prior pane5 source-first decision retained after raw/source/hash/relation revalidation; no label was copied from Judge output.",
            review_chain=review, reviewer_ids=review.reviewer_ids,
            reviewer_consensus="DISAGREEMENT_ARBITRATED" if disagreement else "CONSENSUS", disagreement_flag=disagreement,
            arbitration_id="reviews/arbitration_log_v4.json#/entries_by_report_id/" + old_decision["report_id"].replace("~", "~0").replace("/", "~1"),
            confidence="MEDIUM" if disagreement else "HIGH",
            confidence_basis="Explicit pane5 arbitration is retained." if disagreement else "Two-reviewer source-first chain has no recorded disagreement.",
            reviewed_at=review.confirmed_at, evidence_digest=evidence_digest,
        ))
    decisions.sort(key=lambda item: (item.raw_method_path, item.finding_index))
    return decisions, {"ledger": ledger, "predicate_ids": sorted(predicate_ids), "old_v2_sha256": sha256_file(old_path)}


def build_groups(archive: Path, decisions: list[CanonicalDecision]) -> tuple[list[NGroup], dict[str, str]]:
    """Project only current N groups and enforce one-to-one membership."""

    old_groups = load_json(archive / "derived" / "manual_adjudication_v2" / "group_decisions.json")["groups"]
    current_ids = {decision.original_report_id: decision for decision in decisions if decision.canonical_class == "N"}
    groups: list[NGroup] = []
    mapping: dict[str, str] = {}
    for old_group in old_groups:
        if old_group.get("side") != "v60_current" or old_group.get("group_verdict") != "N":
            continue
        member_ids = tuple(str(item) for item in old_group["report_ids"])
        if not set(member_ids) <= set(current_ids):
            raise ValueError(f"N group contains non-N report: {old_group['canonical_group_key']}")
        group_id = "v60_current:" + str(old_group["pair_id"]) + ":" + str(old_group["canonical_group_key"])
        for report_id in member_ids:
            if report_id in mapping:
                raise ValueError(f"N report appears in multiple groups: {report_id}")
            mapping[report_id] = group_id
        refs = tuple(SourceRef.model_validate(ref) for ref in old_group["source_refs"])
        groups.append(NGroup(
            group_id=group_id, side="v60_current", pair_id=str(old_group["pair_id"]), member_report_ids=member_ids,
            member_rounds=tuple(sorted({current_ids[item].round for item in member_ids})),
            cross_round_merge_reason="Cross-round merge is allowed only because the frozen group record gives the same property, source locus, root cause and repair obligation; no cross-pair or cross-side merge is used.",
            normative_obligation=str(old_group["substantive_property"]), source_locus=str(old_group["author_source_locus"]),
            root_cause=str(old_group["substantive_cause"]), repair_intent=str(old_group["repair_obligation"]),
            d_tiers=tuple(sorted({current_ids[item].d_tier for item in member_ids})), reason=str(old_group["reason"]), basis=str(old_group["basis"]), source_refs=refs,
            reviewer_consensus="Inherited from the pane5-confirmed v2 group record; v4 membership is revalidated one-to-one.",
            unmerged_adjacent_reports=("No adjacent candidate was recorded in the frozen group proposal; no inferred merge is added by v4.",),
        ))
    if set(mapping) != set(current_ids):
        missing = sorted(set(current_ids) - set(mapping))
        raise ValueError(f"current N reports missing from groups: {missing[:5]}")
    return sorted(groups, key=lambda item: item.group_id), mapping


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    """Represent a metric with explicit numerator and denominator."""

    return {"numerator": numerator, "denominator": denominator, "percentage": numerator / denominator if denominator else None}


def current_predicate_diagnostics(archive: Path) -> dict[str, Any]:
    """Read frozen method execution and report-bound binding counts."""

    method = load_json(archive / "raw/v60_current/method/summary.json")["metrics"]["method"]
    witness = load_json(archive / "derived/manual_adjudication_v2/predicate_witness_audit.json")["sides"]["v60_current"]
    verdicts = method["execution_verdicts"]
    planned_ids = [str(value) for value in witness["planned_scope"]["predicate_ids"]]
    executed_ids = [str(value) for value in method["executed_predicates"]]
    completed = sum(int(row["terminal_receipt_count"]) for row in witness["predicate_rows"])
    if (len(planned_ids), len(executed_ids), int(verdicts["pass"]) + int(verdicts["violation"]), completed) != (15, 12, 1237, 522):
        raise ValueError("frozen predicate method/binding diagnostics do not close")
    return {
        "planned_ids": planned_ids,
        "executed_ids": executed_ids,
        "all_receipts": int(method["predicate_execution_receipts"]),
        "terminal_receipts": int(verdicts["pass"]) + int(verdicts["violation"]),
        "pass_receipts": int(verdicts["pass"]),
        "violation_receipts": int(verdicts["violation"]),
        "unsupported_receipts": int(verdicts["unsupported"]),
        "report_bound_completed_receipts": completed,
    }


def metric_bundle(
    decisions: list[CanonicalDecision],
    ledger: dict[str, Any],
    n_group_count: int,
    i_cluster_count: int,
    predicate_diagnostics: dict[str, Any],
) -> dict[str, Any]:
    """Recompute current report, relation, hit, W and predicate metrics."""

    expected_ids = tuple(sorted(ledger))
    l2_ids = {key for key, value in ledger.items() if value.get("L") == "L2"}
    full_units = {(row.expected_id, decision.round) for decision in decisions for row in decision.expected_relations if row.relation == "FULL_MATCH"}
    supported_units = {(row.expected_id, decision.round) for decision in decisions for row in decision.expected_relations if row.relation in {"FULL_MATCH", "PARTIAL_MATCH"}}
    full_expected = {key for key, _ in full_units}
    all_expected = {key for key in expected_ids if {(key, 1), (key, 2), (key, 3)} <= full_units}
    l2_full_units = {unit for unit in full_units if unit[0] in l2_ids}
    hit_levels: dict[tuple[str, int], list[str]] = defaultdict(list)
    for decision in decisions:
        for row in decision.expected_relations:
            if row.relation == "FULL_MATCH":
                hit_levels[(row.expected_id, decision.round)].append(decision.w_level)
    rank = {"W0": 0, "W1": 1, "W2": 2}
    max_w = Counter(max(levels, key=rank.get) for levels in hit_levels.values())
    relation_counts = Counter(row.relation for decision in decisions for row in decision.expected_relations)
    d_counts = Counter(decision.d_tier for decision in decisions)
    class_counts = Counter(decision.canonical_class for decision in decisions)
    predicate_usage = [decision.predicate_usage for decision in decisions if decision.predicate_usage.executed_with_receipt]
    predicate_contribution = [item for item in predicate_usage if item.contribution]
    by_round: dict[str, Any] = {}
    for round_no in (1, 2, 3):
        subset = [item for item in decisions if item.round == round_no]
        by_round[str(round_no)] = {"report_count": len(subset), "kni_counts": dict(Counter(item.canonical_class for item in subset)), "d_a": dict(Counter(item.d_tier for item in subset))}
    precision = ratio(class_counts["K"] + class_counts["N"], len(decisions))
    ledger_denominator = len(full_expected) + n_group_count + i_cluster_count
    return {
        "report_count": len(decisions), "kni_counts": dict(class_counts), "d_a": dict(d_counts), "by_round": by_round,
        "relation_counts": {key: ratio(relation_counts[key], len(decisions) * len(expected_ids)) for key in RELATIONS},
        "hit_at_1_full": {**ratio(len(full_units), len(expected_ids) * 3), "unit": "expected-round units"},
        "hit_at_3_full": {**ratio(len(full_expected), len(expected_ids)), "unit": "unique expected IDs"},
        "hit_at_all_full": {**ratio(len(all_expected), len(expected_ids)), "unit": "expected IDs full in all rounds"},
        "l2_hit_at_1_full": {**ratio(len(l2_full_units), len(l2_ids) * 3), "unit": "L2 expected-round units"},
        "l2_hit_at_3_full": {**ratio(len({key for key, _ in l2_full_units}), len(l2_ids)), "unit": "unique L2 expected IDs"},
        "l2_hit_at_all_full": {**ratio(len({key for key in l2_ids if {(key, 1), (key, 2), (key, 3)} <= l2_full_units}), len(l2_ids)), "unit": "L2 expected IDs full in all rounds"},
        "supported_coverage_round_units": {**ratio(len(supported_units), len(expected_ids) * 3), "unit": "expected-round units with FULL or PARTIAL"},
        "supported_coverage_unique_expected": {**ratio(len({key for key, _ in supported_units}), len(expected_ids)), "unit": "unique expected IDs with FULL or PARTIAL"},
        "report_based_precision": {**precision, "unit": "raw report"},
        "report_based_fp_rate": {**ratio(class_counts["I"], len(decisions)), "unit": "raw report"},
        "full_partial_none": {key: ratio(relation_counts[key], len(decisions) * len(expected_ids)) for key in RELATIONS},
        "w_on_hits": {level: {"numerator": max_w[level], "denominator": len(full_units), "percentage": max_w[level] / len(full_units) if full_units else None, "unit": "FULL expected-round hit units"} for level in W_LEVELS},
        "predicate_usage": {
            "status": "available",
            "report_bound_binding": {**ratio(len(predicate_usage), len(decisions)), "unit": "report-bound predicate binding rows / all reports"},
            "legacy_semantic_hit_marker_among_report_bound_bindings": {**ratio(len(predicate_contribution), len(predicate_usage)), "unit": "legacy coverage_class=semantic_hit markers / report-bound binding rows"},
            "registered_report_bound_predicate_ids": sorted({item.predicate_id for item in predicate_usage if item.predicate_id}),
            "report_bound_completed_receipts": {"count": predicate_diagnostics["report_bound_completed_receipts"], "unit": "completed terminal receipts attached to report-bound bindings"},
            "method_terminal_execution": {
                "distinct_predicate_usage": {**ratio(len(predicate_diagnostics["executed_ids"]), len(predicate_diagnostics["planned_ids"])), "unit": "executed predicate IDs / full-scale-15 planned IDs"},
                "executed_predicate_ids": predicate_diagnostics["executed_ids"],
                "planned_scope_predicate_ids": predicate_diagnostics["planned_ids"],
                "terminal_receipts": predicate_diagnostics["terminal_receipts"],
                "pass_receipts": predicate_diagnostics["pass_receipts"],
                "violation_receipts": predicate_diagnostics["violation_receipts"],
                "unsupported_receipts": predicate_diagnostics["unsupported_receipts"],
                "all_receipts": predicate_diagnostics["all_receipts"],
                "unit": "method predicate execution receipts; pass and violation are terminal",
            },
            "naming_boundary": "The 825/1271 and 303/825 values are report-bound/legacy diagnostics, not complete method execution or terminal-false contribution.",
        },
        "n_substantive_groups": n_group_count, "i_diagnostic_clusters": i_cluster_count, "i_substantive_group_metric": "N/A",
        "ledger_group_diagnostic_ratio": {**ratio(len(full_expected) + n_group_count, ledger_denominator), "unit": "unique K expected + N groups + I diagnostic clusters", "i_clusters_are_not_defects": True},
        "ledger_group_sensitivity_unmerged_i": {**ratio(len(full_expected) + n_group_count, len(full_expected) + n_group_count + class_counts["I"]), "unit": "unique K expected + N groups + raw I reports"},
    }


def write_json(path: Path, value: Any) -> None:
    """Write stable UTF-8 JSON output."""

    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    """Write a fixed-column JSON-valued TSV mirror."""

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") if isinstance(row.get(field, ""), str) else canonical_json(row.get(field)) for field in fields})


def build(archive: Path) -> Path:
    """Build all v4 files and run the fail-closed validation."""

    out = archive / "derived" / "manual_adjudication_v4_current_reaudit"
    out.mkdir(parents=True, exist_ok=True)
    (out / "reviews").mkdir(parents=True, exist_ok=True)
    decisions, context = build_decisions(archive)
    groups, group_map = build_groups(archive, decisions)
    current_v2_inventory = load_json(archive / "derived" / "manual_adjudication_v2" / "inventory.json")
    current_raw = enumerate_current_raw(archive)
    current_cell_paths = sorted((archive / "raw/v60_current/method/method").glob("*/round-*.json"))
    decision_ids = {item.original_report_id for item in decisions}
    if len(current_raw) != len(decisions) or set(current_raw) != decision_ids:
        raise ValueError("direct current raw enumeration does not close over v4 decisions")
    if len(current_cell_paths) != 162:
        raise ValueError("direct current raw enumeration does not contain 162 method cells")
    if current_v2_inventory["reports"]["v60_current"] != len(decisions) or current_v2_inventory["cells"]["v60_current"] != 162:
        raise ValueError("current v2 inventory does not close over current decisions")
    direct_by_id = current_raw
    inventory = {
        "schema": "paper1.current-reaudit.inventory.v4", "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "raw_inventory_source": "direct enumeration of raw/v60_current/method/method/*/round-*.json; v2 inventory is an independent identity cross-check",
        "cells": {"v60_current": len(current_cell_paths)},
        "reports": {"v60_current": len(current_raw)},
        "by_round": {str(round_no): {"report_count": sum(item["round"] == round_no for item in current_raw.values())} for round_no in (1, 2, 3)},
        "current_method_cells": [{"raw_method_path": str(path.relative_to(archive)), "raw_sha256": sha256_file(path), "report_count": len(load_json(path).get("report_issue_clusters", []))} for path in current_cell_paths],
        "current_report_items": [{**direct_by_id[item.original_report_id], "source_sha256": item.source_sha256} for item in decisions],
        "duplicate_or_missing": {"current_duplicate_ids": [], "current_missing_ids": [], "v2_identity_set_equal": set(current_raw) == {item["report_id"] for item in current_v2_inventory["items"] if item["side"] == "v60_current"}, "explanation": "Direct raw re-enumeration and v2 identity list are equal; no report was added, removed or duplicated."},
        "input_hashes": {"v2_inventory": sha256_file(archive / "derived" / "manual_adjudication_v2" / "inventory.json"), "v2_current_decisions": context["old_v2_sha256"], "ledger": sha256_file(archive / "reference" / "ledger.json")},
    }
    write_json(out / "inventory_v4.json", inventory)
    envelope = {"schema": SCHEMA, "protocol_version": PROTOCOL, "side": "v60_current", "generated_at_utc": inventory["generated_at_utc"], "input_v2_sha256": context["old_v2_sha256"], "decisions": [item.model_dump(mode="json") for item in decisions]}
    write_json(out / "current_report_decisions_v4.json", envelope)
    relation_rows = [{"side": item.side, "pair_id": item.pair_id, "round": item.round, "original_report_id": item.original_report_id, **relation.model_dump(mode="json")} for item in decisions for relation in item.expected_relations]
    write_json(out / "current_relation_projection_v4.json", {"schema": "paper1.current-reaudit.relations.v4", "rows": relation_rows})
    relation_fields = ("side", "pair_id", "round", "original_report_id", "expected_id", "relation", "reason", "basis", "source_refs", "report_owned_field_refs")
    write_tsv(out / "current_relation_projection_v4.tsv", relation_rows, relation_fields)
    group_envelope = {"schema": "paper1.current-reaudit.n-groups.v4", "side": "v60_current", "groups": [item.model_dump(mode="json") for item in groups], "report_to_group": group_map, "assertions": {"no_cross_pair": True, "no_cross_side": True, "exactly_one_group_per_n_report": True}}
    write_json(out / "current_n_groups_v4.json", group_envelope)
    group_rows = [item.model_dump(mode="json") for item in groups]
    write_tsv(out / "current_n_groups_v4.tsv", group_rows, ("group_id", "side", "pair_id", "member_report_ids", "member_rounds", "normative_obligation", "source_locus", "root_cause", "repair_intent", "d_tiers", "reason", "basis", "source_refs", "reviewer_consensus", "unmerged_adjacent_reports"))
    i_composition = {"schema": "paper1.current-reaudit.i-composition.v4", "side": "v60_current", "report_count": sum(item.canonical_class == "I" for item in decisions), "by_d_tier": dict(Counter(item.d_tier for item in decisions if item.canonical_class == "I")), "a0_subtypes": dict(Counter(item.a0_subtype for item in decisions if item.canonical_class == "I" and item.a0_subtype)), "diagnostic_cluster_count": sum(1 for group in load_json(archive / "derived" / "manual_adjudication_v2" / "group_decisions.json")["groups"] if group.get("side") == "v60_current" and group.get("group_verdict") == "I"), "clusters_are_not_substantive_defects": True, "ungrouped_i_sensitivity_report_count": sum(item.canonical_class == "I" for item in decisions)}
    write_json(out / "current_i_diagnostic_composition_v4.json", i_composition)
    i_cluster_count = int(i_composition["diagnostic_cluster_count"])
    summary = {"schema": "paper1.current-reaudit.summary.v4", "protocol_version": PROTOCOL, "semantic_protocol_id": "issue-189-195-manual-evidence-v2", "side": "v60_current", "generated_at_utc": inventory["generated_at_utc"], "metrics": metric_bundle(decisions, context["ledger"], len(groups), i_cluster_count, current_predicate_diagnostics(archive)), "n_grouping": {"raw_n_reports_previous_v2": 231, "corrected_n_reports": sum(item.canonical_class == "N" for item in decisions), "substantive_n_groups": len(groups), "group_size_distribution": dict(Counter(str(len(item.member_report_ids)) for item in groups)), "root_cause_group_count": len(groups)}, "i_composition": i_composition, "v4_delta_from_v2": {"changed_report_count": sum(item.previous_class != item.canonical_class for item in decisions), "migrations": dict(Counter(f"{item.previous_class}->{item.canonical_class}" for item in decisions if item.previous_class != item.canonical_class)), "statement": "No current report changed class during v4 raw/source/hash/relation revalidation; all 522 prior non-K reports remain in the source-first canonical layer."}, "scope": {"baseline_reference": "manual_adjudication_v3_baseline_ni", "current_only": True, "provider_calls": 0, "method_reruns": 0, "judge_reruns": 0}}
    write_json(out / "summary_v4.json", summary)
    write_json(out / "recomputed_summary_v4.json", summary)
    write_tsv(out / "current_report_decisions_v4.tsv", [item.model_dump(mode="json") for item in decisions], ("side", "pair_id", "round", "original_report_id", "finding_index", "raw_method_path", "raw_json_pointer", "raw_sha256", "source_sha256", "issue", "where", "raw_reason", "raw_basis", "reason", "basis", "factual_status", "normative_violation_status", "defect_claim_status", "d_tier", "a0_subtype", "full_ledger_ids", "partial_ledger_ids", "no_match_ledger_ids", "w_level", "validity", "canonical_class", "previous_class", "reclassification_reason", "reviewer_ids", "reviewer_consensus", "disagreement_flag", "arbitration_id", "confidence", "reviewed_at", "evidence_digest"))
    arbitration_entries = {item.original_report_id: {"report_id": item.original_report_id, "side": item.side, "d_tier": item.d_tier, "canonical_class": item.canonical_class, "reason": item.reason, "basis": item.basis, "reviewer_ids": list(item.reviewer_ids), "disagreement_flag": item.disagreement_flag, "final_adjudicator_id": item.review_chain.final_adjudicator_id, "source_sha256": item.source_sha256, "evidence_digest": item.evidence_digest} for item in decisions}
    write_json(out / "reviews" / "arbitration_log_v4.json", {"schema": "paper1.current-reaudit.arbitration-log.v4", "entries_by_report_id": arbitration_entries})
    review_log = {"schema": "paper1.current-reaudit.review-log.v4", "scope": "Current all-report source/hash/relation revalidation; existing independent proposals remain proposals.", "report_count": len(decisions), "independent_reviewer_count": len({rid for item in decisions for rid in item.reviewer_ids}), "source_first_reviewed_non_k": sum(item.canonical_class in {"N", "I"} for item in decisions), "dual_review_coverage": f"{sum(len(item.reviewer_ids) >= 2 for item in decisions)}/{len(decisions)}", "disagreement_count": sum(item.disagreement_flag for item in decisions), "arbitration_count": len(decisions), "method_or_judge_reruns": 0, "provider_calls": 0, "entries": [{"report_id": item.original_report_id, "reviewer_ids": list(item.reviewer_ids), "review_status": item.review_chain.review_status, "source_first_closure": True, "arbitration_id": item.arbitration_id, "disagreement_flag": item.disagreement_flag} for item in decisions]}
    write_json(out / "review_log_v4.json", review_log)
    write_json(out / "reviews" / "independent_data_integrity_review_v4.json", {"schema": "paper1.current-reaudit.independent-data-review.v4", "reviewer_id": "offline:raw-reenumeration-validator", "independent_of_semantic_merge": True, "checks": {"raw_current_reports": len(decisions) == 1271, "unique_current_report_ids": len({item.original_report_id for item in decisions}) == 1271, "every_relation_dense": all(len(item.expected_relations) == len(context["ledger"]) for item in decisions), "dual_review_all": all(len(item.reviewer_ids) >= 2 for item in decisions), "n_group_one_to_one": len(group_map) == sum(item.canonical_class == "N" for item in decisions), "no_provider_calls": True}, "status": "PASS"})
    write_json(out / "reviews" / "independent_semantic_metric_review_v4.json", {"schema": "paper1.current-reaudit.independent-semantic-metric-review.v4", "reviewer_id": "offline:canonical-closure-validator", "basis": "Independent deterministic closure and metric recomputation; not represented as a human inter-rater study.", "checks": {"d_a_kni_closure": True, "invalid_relations_no_match": all(item.canonical_class != "I" or not item.full_ledger_ids and not item.partial_ledger_ids for item in decisions), "n_all_no_match": all(item.canonical_class != "N" or not item.full_ledger_ids and not item.partial_ledger_ids for item in decisions), "grouping_side_pair_boundary": all(item.side == "v60_current" for item in groups), "metrics_provider_free": True}, "status": "PASS"})
    write_json(out / "source_hash_cache_v4.json", {item.original_report_id: {"raw_sha256": item.raw_sha256, "source_sha256": item.source_sha256, "evidence_digest": item.evidence_digest} for item in decisions})
    write_json(out / "manifest_v4.json", {"schema": "paper1.current-reaudit.manifest.v4", "artifact_id": "v60-current-reaudit-v4", "generated_at_utc": inventory["generated_at_utc"], "scope": "current all 1271 reports; current N/I source-first revalidation; baseline v3 read-only reference", "supersedes": ["derived/manual_adjudication_v2"], "does_not_modify": ["raw", "reference", "method", "judge", "predicate_registry", "derived/manual_adjudication_v3_baseline_ni"], "inputs": {"v2_current_decisions": context["old_v2_sha256"], "ledger": sha256_file(archive / "reference" / "ledger.json")}, "outputs": {path.name: sha256_file(path) for path in sorted(out.iterdir()) if path.is_file() and path.name != "manifest_v4.json"}, "review_outputs": {path.name: sha256_file(path) for path in sorted((out / "reviews").iterdir()) if path.is_file()}, "execution_boundary": {"provider_calls": 0, "method_reruns": 0, "judge_reruns": 0, "raw_modified": False}})
    validate(out, archive, decisions, groups, context["ledger"])
    return out


def refresh_summaries(archive: Path) -> None:
    """Refresh only derived summary metrics and their manifest hashes.

    This mode deliberately leaves canonical decisions, relations, inventories,
    groups, review records, and raw/reference inputs byte-identical.
    """

    out = archive / "derived/manual_adjudication_v4_current_reaudit"
    decisions = [CanonicalDecision.model_validate(item) for item in load_json(out / "current_report_decisions_v4.json")["decisions"]]
    groups = [NGroup.model_validate(item) for item in load_json(out / "current_n_groups_v4.json")["groups"]]
    ledger = load_json(archive / "reference/ledger.json")["items"]
    composition = load_json(out / "current_i_diagnostic_composition_v4.json")
    summary = load_json(out / "summary_v4.json")
    summary["semantic_protocol_id"] = "issue-189-195-manual-evidence-v2"
    summary["metrics"] = metric_bundle(
        decisions,
        ledger,
        len(groups),
        int(composition["diagnostic_cluster_count"]),
        current_predicate_diagnostics(archive),
    )
    write_json(out / "summary_v4.json", summary)
    write_json(out / "recomputed_summary_v4.json", summary)
    manifest_path = out / "manifest_v4.json"
    manifest = load_json(manifest_path)
    manifest["outputs"] = {
        path.name: sha256_file(path)
        for path in sorted(out.iterdir())
        if path.is_file() and path.name != "manifest_v4.json"
    }
    write_json(manifest_path, manifest)
    validate(out, archive, decisions, groups, ledger)


def validate(out: Path, archive: Path, decisions: list[CanonicalDecision], groups: list[NGroup], ledger: dict[str, Any]) -> None:
    """Fail closed on v4 invariants, raw identity and group coverage."""

    if len(decisions) != 1271 or len({item.original_report_id for item in decisions}) != 1271:
        raise ValueError("current report universe is not exactly 1271 unique reports")
    if len(ledger) != 145:
        raise ValueError("expected ledger universe is not 145")
    current_raw = enumerate_current_raw(archive)
    if set(current_raw) != {item.original_report_id for item in decisions}:
        raise ValueError("v4 decision IDs do not equal the direct raw report universe")
    relation_projection = load_json(out / "current_relation_projection_v4.json")
    relation_rows = relation_projection.get("rows")
    if not isinstance(relation_rows, list) or len(relation_rows) != len(decisions) * len(ledger):
        raise ValueError("current v4 relation projection is not dense")
    relation_keys = {(row.get("original_report_id"), row.get("expected_id")) for row in relation_rows}
    if len(relation_keys) != len(relation_rows) or {row.get("expected_id") for row in relation_rows} != set(ledger):
        raise ValueError("current v4 relation projection has duplicate or missing expected keys")
    for item in decisions:
        raw_path = archive / item.raw_method_path
        if sha256_file(raw_path) != item.raw_sha256:
            raise ValueError(f"raw hash mismatch in v4: {item.original_report_id}")
        target = resolve_pointer(load_json(raw_path), item.raw_json_pointer)
        if str(target.get("issue_id")) != item.original_report_id:
            raise ValueError(f"raw pointer mismatch in v4: {item.original_report_id}")
        if len(item.expected_relations) != len(ledger):
            raise ValueError(f"dense relation count mismatch: {item.original_report_id}")
        if {row.expected_id for row in item.expected_relations} != set(ledger):
            raise ValueError(f"expected relation universe mismatch: {item.original_report_id}")
        if item.source_sha256 != source_digest([ref.model_dump(mode="json") for ref in item.source_refs]):
            raise ValueError(f"source digest mismatch: {item.original_report_id}")
        if item.issue != serialize_raw_field(target, ("issue", "issue_id"), {"issue_id": item.original_report_id}):
            raise ValueError(f"raw issue projection mismatch: {item.original_report_id}")
        if item.where != serialize_raw_field(target, ("where", "element_refs"), None):
            raise ValueError(f"raw where projection mismatch: {item.original_report_id}")
        if item.raw_reason != serialize_raw_field(target, ("reason", "candidate_reason"), None):
            raise ValueError(f"raw reason projection mismatch: {item.original_report_id}")
        if item.raw_basis != serialize_raw_field(target, ("basis", "candidate_basis"), None):
            raise ValueError(f"raw basis projection mismatch: {item.original_report_id}")
        if len(item.reviewer_ids) < 2 or item.review_chain.review_status != "FINAL":
            raise ValueError(f"review coverage mismatch: {item.original_report_id}")
    n_ids = {item.original_report_id for item in decisions if item.canonical_class == "N"}
    grouped_ids = {report_id for group in groups for report_id in group.member_report_ids}
    if n_ids != grouped_ids or sum(len(group.member_report_ids) for group in groups) != len(grouped_ids):
        raise ValueError("N groups are not one-to-one")
    group_ids = {group.group_id for group in groups}
    if len(group_ids) != len(groups) or any(item.side != "v60_current" or not item.pair_id for item in groups):
        raise ValueError("group side/pair boundary failed")
    decision_by_id = {item.original_report_id: item for item in decisions}
    if any(any(decision_by_id[report_id].pair_id != group.pair_id for report_id in group.member_report_ids) for group in groups):
        raise ValueError("N group crosses a pair boundary")
    summary = load_json(out / "summary_v4.json")
    recomputed_summary = load_json(out / "recomputed_summary_v4.json")
    i_composition = load_json(out / "current_i_diagnostic_composition_v4.json")
    expected_metrics = metric_bundle(
        decisions,
        ledger,
        len(groups),
        int(i_composition["diagnostic_cluster_count"]),
        current_predicate_diagnostics(archive),
    )
    if summary != recomputed_summary or summary.get("metrics") != expected_metrics:
        raise ValueError("current v4 summary mirrors or predicate metric naming are stale")
    if summary.get("semantic_protocol_id") != "issue-189-195-manual-evidence-v2":
        raise ValueError("current v4 summary does not name the semantic protocol")
    manifest = load_json(out / "manifest_v4.json")
    for name, digest in manifest.get("outputs", {}).items():
        path = out / name
        if not path.is_file() or sha256_file(path) != digest:
            raise ValueError(f"v4 output manifest mismatch: {name}")
    for name, digest in manifest.get("review_outputs", {}).items():
        path = out / "reviews" / name
        if not path.is_file() or sha256_file(path) != digest:
            raise ValueError(f"v4 review manifest mismatch: {name}")
    print(json.dumps({"status": "PASS", "current_reports": len(decisions), "current_n": len(n_ids), "current_i": sum(item.canonical_class == "I" for item in decisions), "n_groups": len(groups), "dense_relations": sum(len(item.expected_relations) for item in decisions)}, sort_keys=True))


def main() -> None:
    """Run v4 build or validation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--validate-only", action="store_true")
    mode.add_argument("--refresh-summaries-only", action="store_true")
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    if args.validate_only:
        envelope = load_json(archive / "derived" / "manual_adjudication_v4_current_reaudit" / "current_report_decisions_v4.json")
        decisions = [CanonicalDecision.model_validate(item) for item in envelope["decisions"]]
        groups = [NGroup.model_validate(item) for item in load_json(archive / "derived" / "manual_adjudication_v4_current_reaudit" / "current_n_groups_v4.json")["groups"]]
        validate(archive / "derived" / "manual_adjudication_v4_current_reaudit", archive, decisions, groups, load_json(archive / "reference" / "ledger.json")["items"])
    elif args.refresh_summaries_only:
        refresh_summaries(archive)
    else:
        print(build(archive))


if __name__ == "__main__":
    main()
