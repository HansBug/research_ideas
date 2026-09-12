"""Build the explicit, conservative N-group and invalid-cluster archive.

The merge table below is an auditable human register.  The script performs
only membership closure, pair boundaries, source-link copying, and Pydantic
validation; it does not infer groups from text or identifiers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import (
    DATier,
    GroupKind,
    GroupingCriterion,
    GroupSetV3,
    InvalidClusterV3,
    NonMergeReasonV3,
    NGroupV3,
    SourceRef,
    canonical_json_sha256,
)


# Only these pairs have a documented source-backed merge.  All other final N
# reports are intentionally conservative singleton groups.  This is a
# grouping decision, never a semantic classifier.
MERGES: tuple[dict[str, object], ...] = (
    {
        "group_id": "N-G-0004-01",
        "members": ("0004:r2:baseline_issue_2", "0004:r3:baseline_issue_3"),
        "obligation": "Approaching must send Send while representing continued approach; do/Send versus an ordinary state action is the same source-level action modeling issue.",
        "locus": "Approaching state Send behavior in the pair 0004 PlantUML and its corresponding NL clause.",
        "root": "The Approaching Send behavior is assigned an unsupported do-action interpretation and lacks one coherent representation of the required continuing behavior.",
        "repair": "Choose one source-faithful representation of the Approaching Send/continue-approach behavior.",
        "reason": "The two reports describe the same obligation, the same Approaching source locus, the same modeling interpretation, and the same minimal repair intent; merging retains both report pointers.",
    },
    {
        "group_id": "N-G-0009-01",
        "members": ("0009:r1:baseline_issue_5", "0009:r3:baseline_issue_5"),
        "obligation": "Mode-specific collision-avoidance activation must use the corresponding forward-distance condition and mode guard.",
        "locus": "HighwayMode/UrbanMode forward-distance activation guards in pair 0009.",
        "root": "The two mode-specific guards do not express the required mutually exclusive mode-conditioned activation semantics.",
        "repair": "Repair the two mode-specific activation guards as one coherent guard specification.",
        "reason": "Both reports diagnose the same pair-level guard obligation and the same transition's two mode-specific condition branches; their different wording does not add an independent repair intent.",
    },
    {
        "group_id": "N-G-0019-01",
        "members": ("0019:r1:baseline_issue_4", "0019:r3:baseline_issue_4"),
        "obligation": "Collision-avoidance activation must expose a decidable mode-specific forward-distance condition.",
        "locus": "HighwayMode/UrbanMode activation guard expressions in pair 0019.",
        "root": "The same mode-conditioned distance predicate is represented ambiguously across the activation transitions.",
        "repair": "Make the single pair's mode-specific distance guards explicit Boolean conditions.",
        "reason": "The two retained final-N reports point to the same pair-level obligation, guard family, and repair action; the round variation is repeated observation, not a second defect. The separately reclassified K report is intentionally excluded from N grouping.",
    },
    {
        "group_id": "N-G-0022-01",
        "members": ("0022:r1:baseline_issue_1", "0022:r2:baseline_issue_1", "0022:r3:baseline_issue_1"),
        "obligation": "Power-on must enter Operate directly as required by the author NL.",
        "locus": "Power-on initial transition through PoweredOn in pair 0022.",
        "root": "The model inserts the same PoweredOn/start detour before Operate.",
        "repair": "Remove the unsupported power-on detour or otherwise represent the direct power-on entry required by the NL.",
        "reason": "The three reports identify the same extra PoweredOn detour, same source locus, and same minimal repair; cross-round repetition is explicitly allowed.",
    },
    {
        "group_id": "N-G-0041-01",
        "members": ("0041:r2:baseline_issue_3", "0041:r3:baseline_issue_3"),
        "obligation": "Braking-state feedback return behavior must follow the specified signal condition.",
        "locus": "Braking and caliper-clamping feedback return transitions in pair 0041.",
        "root": "The model adds or extends the same unsupported feedback-release return behavior to braking states.",
        "repair": "Align the braking-state feedback transition set with the author NL.",
        "reason": "The two retained final-N reports are repeated descriptions of one pair's braking feedback transition error and one repair intention; the reclassified I report is intentionally excluded from N grouping.",
    },
    {
        "group_id": "N-G-0057-01",
        "members": ("0057:r1:baseline_issue_1", "0057:r2:baseline_issue_2"),
        "obligation": "The three collision-avoidance regions must be modeled as concurrent orthogonal regions.",
        "locus": "Collision Avoidance region declaration in pair 0057.",
        "root": "The same region declaration omits orthogonal/concurrent structure.",
        "repair": "Declare the three regions as one orthogonal concurrent composite structure.",
        "reason": "Both rounds identify the same region declaration and repair intent; this is a repeated report of one source defect.",
    },
)


def load(path: Path) -> dict:
    """Load one JSON artifact."""
    return json.loads(path.read_text(encoding="utf-8"))


def source_ref_key(source_ref: dict) -> tuple[object, ...]:
    """Return the stable identity used to deduplicate one source reference."""
    return (
        source_ref.get("repository_path"),
        source_ref.get("json_pointer"),
        source_ref.get("line"),
        source_ref.get("sha256"),
    )


def merged_source_refs(by_id: dict[str, dict], members: tuple[str, ...]) -> tuple[SourceRef, ...]:
    """Return the ordered union of every member's source refs."""
    result: list[SourceRef] = []
    seen: set[tuple[object, ...]] = set()
    for member in members:
        for source_ref in by_id[member]["source_refs"]:
            key = source_ref_key(source_ref)
            if key not in seen:
                seen.add(key)
                result.append(SourceRef(**source_ref))
    return tuple(result)


def main() -> None:
    """Generate groups and clusters with exact report closure."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = load(args.decisions)
    decisions = document["decisions"]
    by_id = {row["original_report_id"]: row for row in decisions}
    final_n = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "N"}
    final_i = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "I"}
    assigned: dict[str, str] = {}
    groups: list[NGroupV3] = []

    for merge in MERGES:
        members = tuple(str(x) for x in merge["members"])
        # The merge register is versioned evidence from an earlier pane5
        # snapshot.  A later re-adjudication may migrate one member to K/I;
        # in that case the old merge is no longer admissible and each surviving
        # final-N member falls through to the conservative singleton pass.
        if not set(members) <= final_n:
            continue
        if len({by_id[x]["pair_id"] for x in members}) != 1:
            raise ValueError(f"merge crosses pair: {members}")
        if set(members) & set(assigned):
            raise ValueError(f"overlapping N merge: {members}")
        first = by_id[members[0]]
        groups.append(NGroupV3(
            group_id=str(merge["group_id"]), group_kind=GroupKind.SUBSTANTIVE_N,
            side="x1v2_baseline", pair_id=first["pair_id"], canonical_group_key=str(merge["group_id"]),
            member_report_ids=members, cross_round_merge=len({by_id[x]["round"] for x in members}) > 1,
            normative_obligation=str(merge["obligation"]), author_source_locus=str(merge["locus"]),
            substantive_root_cause=str(merge["root"]), repair_intent=str(merge["repair"]),
            d_tiers=tuple(sorted({DATier(by_id[x]["d_tier"]) for x in members}, key=lambda x: x.value)),
            reason=f"{merge['group_id']}: {merge['reason']}",
            basis=f"{merge['group_id']}: member source refs were read from each canonical decision; no cross-pair or cross-side merge is permitted.",
            source_refs=merged_source_refs(by_id, members),
            member_source_refs={
                member: tuple(SourceRef(**source_ref) for source_ref in by_id[member]["source_refs"])
                for member in members
            },
            non_merge_reasons=(),
        ))
        assigned.update({member: str(merge["group_id"]) for member in members})

    for rid in sorted(final_n - set(assigned)):
        row = by_id[rid]
        group_id = f"N-G-{row['pair_id']}-S-{rid.replace(':', '-') }"
        neighbors = sorted(x["original_report_id"] for x in decisions if x["pair_id"] == row["pair_id"] and x["corrected_kni"] == "N" and x["original_report_id"] != rid)
        non_merge_reasons = tuple(
            NonMergeReasonV3(
                neighbor_report_id=neighbor,
                decision="CONSERVATIVE_NO_MERGE",
                unestablished_criteria=(
                    GroupingCriterion.NORMATIVE_OBLIGATION,
                    GroupingCriterion.SOURCE_LOCUS,
                    GroupingCriterion.ROOT_CAUSE,
                    GroupingCriterion.REPAIR_INTENT,
                ),
                reason=(
                    f"{rid} and {neighbor} remain separate conservatively: the archived evidence does not establish "
                    "all required homogeneity criteria together. This is not a claim that either report is a distinct "
                    "defect; no cross-round merge is asserted without source-backed equivalence."
                ),
                basis=(
                    f"Compared the final-N source loci and report-specific source evidence for {rid} and {neighbor}; "
                    "the pair-local record establishes neither a complete common obligation/locus/root-cause/repair-intent "
                    "proof nor a lossless merge."
                ),
                source_refs=merged_source_refs(by_id, (rid, neighbor)),
            )
            for neighbor in neighbors
        )
        groups.append(NGroupV3(
            group_id=group_id, group_kind=GroupKind.SUBSTANTIVE_N, side="x1v2_baseline", pair_id=row["pair_id"],
            canonical_group_key=group_id, member_report_ids=(rid,), cross_round_merge=False,
            normative_obligation=f"The report-specific obligation stated by {rid}: {row['raw_text']['issue']}",
            author_source_locus="; ".join(row["source_loci"]),
            substantive_root_cause=f"The report-specific source-level defect claimed at {row['raw_text']['where']}",
            repair_intent=f"Repair the source-level behavior identified by {rid} without merging it with another obligation.",
            d_tiers=(DATier(row["d_tier"]),),
            reason=f"{group_id}: conservative singleton. The source review did not establish the same normative obligation, source locus, root cause, and repair intent with any neighboring report.",
            basis=f"{group_id}: neighboring final N reports retained separately with one structured conservative non-merge record per neighbor: {', '.join(neighbors) if neighbors else 'none'}; this singleton is not evidence of distinctness.",
            source_refs=tuple(SourceRef(**x) for x in row["source_refs"]),
            member_source_refs={rid: tuple(SourceRef(**x) for x in row["source_refs"])},
            non_merge_reasons=non_merge_reasons,
        ))
        assigned[rid] = group_id

    clusters: list[InvalidClusterV3] = []
    for rid in sorted(final_i):
        row = by_id[rid]
        group_id = f"I-C-{row['pair_id']}-S-{rid.replace(':', '-') }"
        clusters.append(InvalidClusterV3(
            group_id=group_id, group_kind=GroupKind.INVALID_DIAGNOSTIC_CLUSTER, side="x1v2_baseline",
            pair_id=row["pair_id"], canonical_group_key=group_id, member_report_ids=(rid,),
            reason=f"{group_id}: singleton invalid-claim diagnostic cluster; this is not an independent defect count.",
            basis=f"{group_id}: {row['d_tier']} was closed to I from the source-backed decision; no invalid cluster merge was asserted without a common false-claim root cause.",
            source_refs=tuple(SourceRef(**x) for x in row["source_refs"]),
            member_source_refs={rid: tuple(SourceRef(**x) for x in row["source_refs"])},
        ))
        assigned[rid] = group_id

    if set(assigned) != final_n | final_i:
        raise ValueError("N/I group closure failed")
    envelope = GroupSetV3(
        n_groups=tuple(sorted(groups, key=lambda x: x.group_id)),
        invalid_clusters=tuple(sorted(clusters, key=lambda x: x.group_id)),
        report_to_group=assigned,
        grouping_basis="Operationalization: same side, same pair, same normative obligation/property, same source locus or inseparable modeling cause, and same minimal repair intent. Cross-round merge is allowed; cross-pair and cross-side merge is forbidden. Singleton groups are conservative and are not claimed to prove distinctness beyond the recorded evidence.",
    )
    args.output.write_text(json.dumps({"schema": "paper1.manual-adjudication.v3-baseline-ni.groups", "decisions_sha256": canonical_json_sha256(document), "groups": envelope.model_dump(mode="json")}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"n_reports": len(final_n), "n_groups": len(groups), "i_reports": len(final_i), "i_clusters": len(clusters)}, sort_keys=True))


if __name__ == "__main__":
    main()
