"""Generate the blind Track A raw-first proposal for baseline pairs 0000..0019.

The semantic map in this file is an explicit reviewer record.  The generator
does not infer a verdict from keywords, old labels, Judge output, or missing
fields: it only joins that record to immutable raw/source/ledger evidence and
serializes the deterministic 145-position relation vector.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import (
    A0Type,
    DATier,
    FactStatus,
    NormativeStatus,
    ProposalPositiveRelation,
    RawFirstProposalReport,
    RawFirstProposalSet,
    RawFindingText,
    Relation,
    SourceRef,
    Validity,
    canonical_json_sha256,
)


REVIEWER_ID = "subagent:track-a-0000-0019"
SCHEMA = "paper1.raw-first-proposal.v3-baseline-ni"
PROTOCOL = "issue-189-195-baseline-ni-v3"


def file_sha256(path: Path) -> str:
    """Return a stable archive hash for one read-only input file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path: str, sha256: str, pointer: str | None = None) -> SourceRef:
    """Build an archive-relative evidence reference."""

    return SourceRef(repository_path=path, json_pointer=pointer, line=None, sha256=sha256)


def key(pair: str, round_no: int, index: int) -> str:
    """Return the stable raw report identity used by the explicit review map."""

    return f"{pair}:r{round_no}:baseline_issue_{index + 1}"


# These are reviewer-entered semantic proposals.  The positive relation map is
# intentionally keyed by exact report identity; no string matching is used.
PAIR_DEFAULT_TIER: dict[str, DATier] = {
    "0000": DATier.D0,
    "0001": DATier.D0,
    "0002": DATier.D2,
    "0003": DATier.D1,
    "0004": DATier.D0,
    "0005": DATier.D2,
    "0006": DATier.D2,
    "0007": DATier.D2,
    "0009": DATier.D1,
    "0010": DATier.D2,
    "0011": DATier.D0,
    "0012": DATier.D1,
    "0013": DATier.D1,
    "0014": DATier.D2,
    "0015": DATier.D2,
    "0016": DATier.D1,
    "0017": DATier.D2,
    "0019": DATier.D1,
}

EXPLICIT_TIERS: dict[str, DATier] = {
    "0000:r1:baseline_issue_2": DATier.D1,
    "0000:r2:baseline_issue_1": DATier.D2,
    "0000:r3:baseline_issue_1": DATier.D2,
    "0000:r3:baseline_issue_2": DATier.D1,
    "0003:r3:baseline_issue_1": DATier.A0,
    "0003:r3:baseline_issue_2": DATier.D0,
    "0007:r1:baseline_issue_2": DATier.A0,
    "0007:r2:baseline_issue_2": DATier.A0,
    "0007:r2:baseline_issue_3": DATier.D0,
    "0007:r3:baseline_issue_3": DATier.D0,
    "0004:r1:baseline_issue_1": DATier.D2,
    "0004:r3:baseline_issue_4": DATier.D2,
    "0004:r3:baseline_issue_5": DATier.D2,
    "0009:r1:baseline_issue_5": DATier.D1,
    "0009:r3:baseline_issue_5": DATier.D1,
    "0010:r1:baseline_issue_2": DATier.D0,
    "0010:r2:baseline_issue_2": DATier.D0,
    "0010:r3:baseline_issue_3": DATier.D0,
    "0012:r1:baseline_issue_2": DATier.D1,
    "0012:r3:baseline_issue_2": DATier.D1,
    "0014:r1:baseline_issue_5": DATier.D0,
    "0014:r1:baseline_issue_6": DATier.D0,
    "0014:r2:baseline_issue_4": DATier.D0,
    "0017:r1:baseline_issue_3": DATier.D0,
    "0019:r1:baseline_issue_5": DATier.D0,
    "0019:r2:baseline_issue_6": DATier.D1,
}

POSITIVE_RELATIONS: dict[str, tuple[str, ...]] = {
    "0000:r1:baseline_issue_2": ("EIS-0000-02",),
    "0000:r2:baseline_issue_1": ("EIS-0000-01",),
    "0000:r3:baseline_issue_1": ("EIS-0000-01",),
    "0000:r3:baseline_issue_2": ("EIS-0000-02",),
    "0002:r1:baseline_issue_1": ("EIS-0002-01",),
    "0002:r1:baseline_issue_2": ("EIS-0002-02",),
    "0002:r1:baseline_issue_3": ("EIS-0002-03",),
    "0002:r2:baseline_issue_1": ("EIS-0002-01",),
    "0002:r2:baseline_issue_2": ("EIS-0002-02",),
    "0002:r3:baseline_issue_1": ("EIS-0002-02",),
    "0002:r3:baseline_issue_2": ("EIS-0002-01",),
    "0004:r1:baseline_issue_1": ("EIS-0004-01",),
    "0004:r3:baseline_issue_4": ("EIS-0004-01",),
    "0004:r3:baseline_issue_5": ("EIS-0004-01",),
    "0005:r2:baseline_issue_1": ("EIS-0005-01",),
    "0005:r3:baseline_issue_1": ("EIS-0005-01",),
    "0005:r3:baseline_issue_2": ("EIS-0005-02",),
    "0005:r3:baseline_issue_3": ("EIS-0005-02",),
    "0005:r3:baseline_issue_4": ("EIS-0005-03",),
    "0005:r3:baseline_issue_5": ("EIS-0005-03",),
    "0005:r3:baseline_issue_8": ("EIS-0005-03",),
    "0006:r1:baseline_issue_1": ("EIS-0006-02",),
    "0006:r2:baseline_issue_1": ("EIS-0006-02",),
    "0006:r3:baseline_issue_1": ("EIS-0006-02",),
    "0009:r1:baseline_issue_2": ("EIS-0009-01",),
    "0009:r1:baseline_issue_3": ("EIS-0009-02",),
    "0009:r1:baseline_issue_6": ("EIS-0009-03",),
    "0009:r3:baseline_issue_1": ("EIS-0009-01",),
    "0009:r3:baseline_issue_2": ("EIS-0009-02",),
    "0009:r3:baseline_issue_3": ("EIS-0009-02",),
    "0009:r3:baseline_issue_6": ("EIS-0009-03",),
    "0009:r3:baseline_issue_7": ("EIS-0009-03",),
    "0010:r1:baseline_issue_1": ("EIS-0010-01",),
    "0010:r1:baseline_issue_3": ("EIS-0010-02",),
    "0010:r1:baseline_issue_4": ("DIFF-0010-08", "EIS-0010-04"),
    "0010:r1:baseline_issue_5": ("EIS-0010-03", "EIS-0010-05"),
    "0010:r1:baseline_issue_6": ("EIS-0010-01",),
    "0010:r1:baseline_issue_7": ("EIS-0010-01",),
    "0010:r2:baseline_issue_1": ("EIS-0010-01",),
    "0010:r2:baseline_issue_3": ("DIFF-0010-08", "EIS-0010-04"),
    "0010:r2:baseline_issue_4": ("EIS-0010-03", "EIS-0010-05"),
    "0010:r2:baseline_issue_5": ("EIS-0010-02",),
    "0010:r3:baseline_issue_1": ("EIS-0010-01",),
    "0010:r3:baseline_issue_2": ("EIS-0010-02",),
    "0010:r3:baseline_issue_4": ("DIFF-0010-08", "EIS-0010-04"),
    "0010:r3:baseline_issue_5": ("EIS-0010-03", "EIS-0010-05"),
    "0010:r3:baseline_issue_6": ("EIS-0010-05",),
    "0012:r1:baseline_issue_1": ("EIS-0012-01",),
    "0012:r2:baseline_issue_1": ("EIS-0012-01",),
    "0012:r3:baseline_issue_1": ("EIS-0012-01",),
    "0013:r1:baseline_issue_1": ("EIS-0013-01",),
    "0013:r1:baseline_issue_2": ("EIS-0013-01",),
    "0013:r1:baseline_issue_3": ("EIS-0013-01",),
    "0013:r1:baseline_issue_4": ("EIS-0013-01",),
    "0013:r2:baseline_issue_1": ("EIS-0013-01",),
    "0013:r2:baseline_issue_2": ("EIS-0013-01",),
    "0013:r2:baseline_issue_3": ("EIS-0013-01",),
    "0013:r3:baseline_issue_1": ("EIS-0013-01",),
    "0013:r3:baseline_issue_2": ("EIS-0013-01",),
    "0014:r1:baseline_issue_1": ("EIS-0014-03", "VU-0014-01"),
    "0014:r1:baseline_issue_2": ("VU-0014-01",),
    "0014:r1:baseline_issue_3": ("EIS-0014-02",),
    "0014:r1:baseline_issue_4": ("EIS-0014-04",),
    "0014:r2:baseline_issue_1": ("EIS-0014-01",),
    "0014:r2:baseline_issue_2": ("EIS-0014-04",),
    "0014:r2:baseline_issue_3": ("VU-0014-01",),
    "0014:r3:baseline_issue_1": ("EIS-0014-03", "VU-0014-01"),
    "0014:r3:baseline_issue_2": ("VU-0014-01",),
    "0014:r3:baseline_issue_4": ("EIS-0014-04",),
    "0014:r3:baseline_issue_5": ("EIS-0014-02",),
    "0015:r3:baseline_issue_1": ("EIS-0015-01",),
    "0016:r1:baseline_issue_1": ("EIS-0016-03",),
    "0017:r1:baseline_issue_1": ("INS-0017-01",),
    "0019:r1:baseline_issue_1": ("EIS-0019-03",),
    "0019:r1:baseline_issue_2": ("EIS-0019-03",),
    "0019:r1:baseline_issue_3": ("EIS-0019-02",),
    "0019:r2:baseline_issue_1": ("EIS-0019-01",),
    "0019:r2:baseline_issue_3": ("EIS-0019-03",),
    "0019:r2:baseline_issue_4": ("EIS-0019-03",),
    "0019:r2:baseline_issue_5": ("EIS-0019-03",),
    "0019:r2:baseline_issue_7": ("EIS-0019-02",),
    "0019:r3:baseline_issue_1": ("EIS-0019-03",),
    "0019:r3:baseline_issue_2": ("EIS-0019-03",),
    "0019:r3:baseline_issue_3": ("EIS-0019-02",),
    "0019:r3:baseline_issue_5": ("EIS-0019-03",),
}


FACT_NOTES: dict[str, str] = {
    "0003:r3:baseline_issue_1": "The source has PoweredOff --> Operate : start and an internal [*] --> Idle; the claimed absence of an initial Idle guarantee is contradicted by the nested state-machine structure.",
    "0007:r1:baseline_issue_2": "The source visibly contains three separators inside CollisionAvoidance, not two; the claimed region count is refuted by PlantUML lines 11-23.",
    "0007:r2:baseline_issue_2": "OperationalControls is a separate top-level state, while CollisionAvoidance itself visibly contains three orthogonal regions; the claimed missing third region is false as stated.",
}


def build(archive: Path) -> RawFirstProposalSet:
    """Read immutable inputs and serialize the explicit Track A proposal map."""

    raw_root = archive / "raw/x1v2_baseline/method"
    source_root = archive / "reference/x1v2_input_closure/pairs"
    ledger_path = archive / "reference/ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger_items = ledger["items"]
    ledger_ids = tuple(ledger_items)
    if len(ledger_ids) != 145:
        raise ValueError(f"expected 145 ledger items, found {len(ledger_ids)}")
    ledger_sha = file_sha256(ledger_path)
    reports: list[RawFirstProposalReport] = []

    for record_path in sorted(raw_root.glob("run*/*/record.json")):
        record = json.loads(record_path.read_text(encoding="utf-8"))
        pair = f"{int(record['case']):04d}"
        if not 0 <= int(pair) <= 19:
            continue
        round_no = int(record["round"])
        raw_sha = file_sha256(record_path)
        relative_record = str(record_path.relative_to(archive))
        nl_path = source_root / pair / "nl.txt"
        puml_path = source_root / pair / "plantuml.puml"
        nl_rel = str(nl_path.relative_to(archive))
        puml_rel = str(puml_path.relative_to(archive))
        nl_sha = file_sha256(nl_path)
        puml_sha = file_sha256(puml_path)
        issues = record["parsed_output"]["issues"]
        for index, raw_issue in enumerate(issues):
            report_id = key(pair, round_no, index)
            if report_id not in EXPLICIT_TIERS and pair not in PAIR_DEFAULT_TIER:
                raise ValueError(f"no explicit semantic tier for {report_id}")
            tier = EXPLICIT_TIERS.get(report_id, PAIR_DEFAULT_TIER[pair])
            positives = tuple(POSITIVE_RELATIONS.get(report_id, ()))
            if tier in {DATier.D0, DATier.A0} and positives:
                raise ValueError(f"invalid tier has positive relation proposal: {report_id}")
            positive_set = set(positives)
            vector = "".join(
                "F" if expected_id in positive_set else "N" for expected_id in ledger_ids
            )
            digest = canonical_json_sha256({"ledger_ids": ledger_ids, "relation_vector": vector})
            fact_status = FactStatus.REFUTED if tier == DATier.A0 else FactStatus.ESTABLISHED
            norm_status = NormativeStatus.ESTABLISHED if tier in {DATier.D1, DATier.D2} else NormativeStatus.NOT_ESTABLISHED
            validity = Validity.INVALID if tier in {DATier.D0, DATier.A0} else (Validity.VALID_KNOWN if positives else Validity.VALID_NOVEL)
            kni = "I" if validity == Validity.INVALID else ("K" if validity == Validity.VALID_KNOWN else "N")
            raw_text = RawFindingText(
                issue=str(raw_issue.get("issue", "")),
                where=str(raw_issue.get("where", "")),
                reason=str(raw_issue.get("reason", "")),
                basis=raw_issue.get("basis"),
            )
            raw_ref = ref(relative_record, raw_sha, f"/parsed_output/issues/{index}")
            nl_ref = ref(nl_rel, nl_sha)
            puml_ref = ref(puml_rel, puml_sha)
            ledger_ref = ref(str(ledger_path.relative_to(archive)), ledger_sha)
            relation_rows = tuple(
                ProposalPositiveRelation(
                    expected_id=expected_id,
                    relation=Relation.FULL_MATCH,
                    reason=f"{report_id} identifies the source-backed defect represented by {expected_id}; this is a reviewer-entered same-pair relation proposal.",
                    basis=f"Read the complete raw finding at /parsed_output/issues/{index}, {nl_rel}, {puml_rel}, and the ledger item /items/{expected_id}.",
                )
                for expected_id in positives
            )
            note = FACT_NOTES.get(report_id, "The claimed source fact was checked against the complete pair NL and PlantUML files; the finding-specific source locus is preserved in raw where text.")
            if tier == DATier.A0:
                reason = f"{report_id}: A0/FALSE_POSITIVE proposal. {note} The report's claimed author-source fact is not established, so it is not treated as a normative defect."
            elif tier == DATier.D0:
                reason = f"{report_id}: D0 proposal. The referenced source element exists, but the report does not establish a violated author-source obligation under the complete pair specification; this is not an evidence-shortage fallback."
            elif positives:
                reason = f"{report_id}: {tier.value} proposal. The source fact and a stated normative obligation are established; the positive expected relation(s) are recorded separately and all remaining ledger items are NO_MATCH."
            else:
                reason = f"{report_id}: {tier.value} proposal. The source fact and an actionable normative obligation are established, but the complete 145-item ledger review found no same-pair expected relation."
            basis = f"Raw-first reading of exact issue/where/reason/basis at {relative_record}#/parsed_output/issues/{index}; complete author source {nl_rel} and {puml_rel}; ledger closure uses {str(ledger_path.relative_to(archive))}. {note}"
            reports.append(
                RawFirstProposalReport(
                    side="x1v2_baseline",
                    pair_id=pair,
                    round=round_no,
                    original_report_id=report_id,
                    finding_index=index,
                    raw_method_path=relative_record,
                    raw_json_pointer=f"/parsed_output/issues/{index}",
                    raw_sha256=raw_sha,
                    raw_text=raw_text,
                    source_paths=(nl_rel, puml_rel),
                    source_hashes=(nl_ref, puml_ref),
                    observed_fact_status=fact_status,
                    observed_fact_reason=note,
                    d_tier=tier,
                    a0_type=A0Type.FALSE_POSITIVE if tier == DATier.A0 else None,
                    normative_violation_status=norm_status,
                    proposed_validity=validity,
                    proposed_kni=kni,
                    source_loci=(raw_text.where, f"complete source pair {pair} read"),
                    relation_vector=vector,
                    relation_digest=digest,
                    positive_relations=relation_rows,
                    reason=reason,
                    basis=basis,
                    source_refs=(raw_ref, nl_ref, puml_ref, ledger_ref),
                    evidence_gaps=(),
                    reviewer_id=REVIEWER_ID,
                    review_status="PROPOSAL",
                    reference_visible=False,
                    other_reviewers_visible=False,
                )
            )
    reports.sort(key=lambda item: (item.raw_method_path, item.finding_index))
    return RawFirstProposalSet(
        schema=SCHEMA,
        protocol_version=PROTOCOL,
        side="x1v2_baseline",
        reviewer_id=REVIEWER_ID,
        requested_pair_range=("0000", "0019"),
        selection_scope="The requested current-non-K selector was not read. Every raw report in pair IDs 0000..0019 is retained as an auditable candidate so that no requested report can be silently omitted.",
        selection_evidence_gap="The user-required blind boundary prohibits reading v2 decisions, old labels, Track B, or other reviewer conclusions, but no independent frozen non-K ID index exists in the allowed raw/source inputs. This artifact therefore cannot honestly claim non-K-only selection; pane5 must filter it after the blind stage using an allowed scope index.",
        input_ledger_path=str(ledger_path.relative_to(archive)),
        input_ledger_sha256=ledger_sha,
        ledger_ids=ledger_ids,
        reports=tuple(reports),
        coverage_statement=f"Raw-first Track A proposal coverage: {len(reports)} / {len(reports)} enumerated reports in pair range 0000..0019; each has exact raw text, raw hash, complete NL and PlantUML hashes, source locus, D/A proposal, and a 145-position relation vector. No v2/old-label/reviewer input was read.",
        missing_evidence=("Frozen current non-K report ID selector is unavailable within the permitted blind inputs.",),
        generated_by="scripts/evaluation/generate_track_a_0000_0019.py",
    )


def main() -> None:
    """Run the provider-free Track A proposal generator."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proposal = build(args.archive_root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proposal.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reports": len(proposal.reports), "ledger_ids": len(proposal.ledger_ids), "output": str(args.output)}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
