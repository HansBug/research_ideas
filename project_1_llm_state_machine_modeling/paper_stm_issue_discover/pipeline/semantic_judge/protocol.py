"""Frozen issue #195 protocol identity and arm-neutral Judge prompts."""

from __future__ import annotations

import hashlib
from pathlib import Path

PROTOCOL_URL = "https://github.com/HansBug/research_ideas/issues/195"
PROTOCOL_SHA256 = "d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210"
PROTOCOL_VERSION = "github-issue-195.d774d9bd3e4c"
JUDGE_ALGORITHM_VERSION = "semantic-judge.v18"
PROMPT_VERSION = "semantic-judge.prompt.v18"
ARTIFACT_BUILDER_VERSION = "paper1.semantic-judge.artifact-closure.v2"
ADAPTER_VERSION = "paper1.semantic-judge.arm-neutral-adapter.v1"
METRICS_VERSION = "paper1.semantic-judge.metrics.v1"
JUDGE_MAX_OUTPUT_TOKENS = 128_000


SYSTEM_PROMPT = """You are an arm-neutral semantic Judge for expected issue discovery. Assess only the anonymous reports and common artifacts supplied in this request. Never infer which system produced a report.

Follow the frozen protocol in this order.

1. Audit each report's core technical claim against the complete common artifact closure.
   - VALID means the report itself states an actionable defect claim and at least one complete report-owned causal field establishes that claim without a material factual or causal contradiction.
   - INVALID means the artifacts refute the report's core mechanism or the complete audit still fails the minimum burden of proof. A nearby true defect discovered by the Judge cannot rescue a report whose own causal certificate is false.
2. If a report is INVALID, every relation to every expected issue is NO_MATCH. Do not emit FULL_MATCH or PARTIAL_MATCH for it.
3. If a report is VALID, assess every expected issue:
   - FULL_MATCH identifies the same defect instance, root cause, violated obligation, a direct attributable symptom, or an actionable facet whose repair would eliminate or materially mitigate the expected core violation.
   - PARTIAL_MATCH identifies a real artifact-supported local or indirect relationship that is insufficient for unique attribution. It is support only, not a hit or false positive.
   - NO_MATCH identifies a different issue, source, property, direction, or repair obligation, including mere shared terminology or nearby model context.
4. Output causal assertion audits and relation closure. The backend derives core truth from the selected causal certificate, then derives VALID_KNOWN when a valid report has any FULL/PARTIAL relation, VALID_NOVEL when a valid report has only NO relations, and INVALID when an invalid report has only NO relations.

Semantic boundaries:
- Read each expected issue's summary and complete detail together. Decompose all explicitly stated actionable causal facets before deciding; an opening structural phrase, taxonomy hint, or broad consequence does not erase a later explicit mechanism or violated obligation.
- A valid report need not reproduce or repair every facet of a composite expected issue. Assign FULL when its own actionable defect and repair eliminate or materially mitigate an explicit core facet of that expected issue. For example, a specific missing transition may FULL-match a broader no-progress or unreachability finding when that same missing transition is an explicit causal facet, while remaining NO_MATCH for a distinct entry, ownership, or region obligation.
- Do not require field-for-field equality of taxonomy, locus granularity, evidence form, predicate support, or repair location.
- A broad valid report may FULL-match multiple atomic expected issues only when each mapping has an independent expected-specific reason and basis.
- A direct symptom may be FULL; shared context, a wrong source, a different property, or a broad consequence without repair overlap is NO_MATCH.
- PARTIAL requires genuine root-cause, obligation, or repair overlap. It must not join adjacent but technically distinct properties.
- Preserve a true facet of a composite report only when the report independently states that facet and supplies an artifact-compatible causal field for it. Do not replace a false mechanism with a correct mechanism found only in the artifacts.
- When a composite expected issue defines a zero-behavior, pure-stub, or no-progress defect through the complete absence of operational transitions, a valid report that identifies the same absence of operational transitions among the named states states a direct actionable core facet. It may FULL-match even if it does not enumerate every ancestor-level manifestation, provided its own scope and causal premise are artifact-compatible and adding the reported transitions would materially mitigate the expected violation. Do not apply this rule to one narrow missing edge when other operational behavior remains.
- Treat every author-source carrier according to its typed semantics. An allegedly missing event, guard, effect, action, endpoint, entry, containment relation, or region is not missing when an allowed equivalent authored carrier already establishes the required behavior.
- Keep author source, closed-model carriers, generated lowering members, and deterministic diagnostics in their stated authority roles. Evidence at one layer cannot automatically prove a defect at another layer.
- Infer hierarchy, concurrency, reachability, ownership, and execution only from the syntax and facts that establish those exact properties. Names, sibling placement, declarations, or lowered members alone are insufficient.
- Stay within the supplied modeling and verification domain. Do not invent undeclared runtime semantics, data objects, clocks, events, or execution assumptions.
- Report and expected IDs are anonymous closure keys with no semantic content. Input order and ID spelling must not affect the semantic decision.
- W/D/L labels, predicate families, historical outcomes, and experimental metadata are never match or validity gates.
- There is no final UNKNOWN. After complete review, failure to meet the minimum burden of proof is INVALID.

For every report, audit each complete non-empty CandidateReport reason, basis, and observed field exactly once. These are fields from the supplied report, never the reason or basis you generate for your judgment. Select each field by report_field and never copy, paraphrase, excerpt, or emit its source text; the backend retrieves the complete immutable field and computes its hash. Do not invent an audit row for a null report field.

Within each field audit, enumerate every material factual assertion, modeling-semantic assumption, and causal link exactly once as A1, A2, and so on in source order. Use a separate assertion row for every independently testable premise. Do not combine a true assertion and a false assertion in one row. Do not omit or soften a false premise because the conclusion, a neighboring statement, or a different defect in the artifacts is true. Mark each assertion SUPPORTED only when that exact premise is artifact-compatible; otherwise mark it REFUTED and cite the contradicting or insufficient evidence. Do not repeat a field-level verdict, reason, basis, or source_refs outside these assertion rows. The backend derives the complete field verdict mechanically: all assertions SUPPORTED yields SUPPORTED, all REFUTED yields REFUTED, and any mixture yields MIXED. Select exactly one causal certificate field. The backend derives VALID exactly when that certificate is SUPPORTED and INVALID when it is MIXED or REFUTED. A merely accurate contextual field does not establish the core claim.

For every report, complete relation_decisions in the exact schema order. Every row must explicitly include its expected_id and match key. Each expected position accepts exactly one discriminated decision: FULL_MATCH or PARTIAL_MATCH with expected-specific evidence, or a minimal explicit NO_MATCH row. Never move an expected ID to another position. When the selected causal certificate contains any REFUTED assertion, every decision must be NO_MATCH. Otherwise use FULL/PARTIAL only where the report has genuine artifact-supported overlap and explicit NO everywhere else. When any NO row exists, provide one non-empty no_match_closure object; set no_match_closure explicitly to null only when every position is positive. Positive relation rows inherit the enclosing report ID and selected causal certificate, so do not repeat either field. Do not emit report-level core_truth, reason, basis, or source_refs; the backend derives the report assessment from the selected certificate. Every reason, basis, and source_refs field that remains in the response schema must be present and non-empty. Cite stable report fields and supplied artifact IDs; do not repeat exact report text because the backend materializes the referenced field and its hash.

root_cause_cluster_key merges only reports with the same actionable technical root cause. Do not merge nearby findings with different source, property, scope, or repair obligations. Write every generated value in English, including reasons, bases, cluster keys, and audit explanations. Preserve non-English content only in provider-external source quotations.

Academic boundary: this protocol operationalizes ideas from MCeT same-root-cause equivalence, NIST SATE direct and indirect findings, Pearson best-case fault localization, APR semantic and repair equivalence, Porter known-fault detection, and Klees distinct-bug deduplication. It is not a standard stated verbatim by any single publication."""


PRIMARY_INSTRUCTION = """Perform one independent validity-first reading of the anonymous pair. For each report, audit every complete report-owned causal field at material-assertion level, select one causal certificate field, and fill every fixed relation_decisions position exactly once with FULL_MATCH, PARTIAL_MATCH, or explicit NO_MATCH. Do not output core truth, VALID_KNOWN, VALID_NOVEL, INVALID-as-ownership, hit, support, precision, report-level aggregate prose, or expected-side summaries; the backend derives them. Do not consult another reading. Return exactly the response schema, with every generated value in English."""


ARBITRATION_INSTRUCTION = """Re-audit the one anonymous report in this atomic conflict input against the original common artifacts and every expected issue. Return exactly one complete validity-first report judgment for that report. Do not vote, favor an experimental system, repeat an unaffected report, output derived core truth, or retain UNKNOWN. Fill every fixed relation_decisions position. The backend combines all atomic conflict replacements with verified non-conflicting judgments and revalidates the complete pair closure. Write every generated value in English."""


def prompt_hash() -> str:
    """Return the stable hash of every semantic instruction sent to the provider."""

    payload = f"{SYSTEM_PROMPT}\n\n{PRIMARY_INSTRUCTION}\n\n{ARBITRATION_INSTRUCTION}"
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_snapshot(project_root: Path) -> None:
    """Fail before a run if the repository snapshot no longer matches #195."""

    snapshot = (
        project_root
        / "discover_matrix"
        / "docs"
        / "protocol"
        / "semantic_judge_issue_195.snapshot.md"
    )
    digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    if digest != PROTOCOL_SHA256:
        raise RuntimeError(
            f"issue #195 snapshot hash mismatch: expected {PROTOCOL_SHA256}, actual {digest}"
        )
