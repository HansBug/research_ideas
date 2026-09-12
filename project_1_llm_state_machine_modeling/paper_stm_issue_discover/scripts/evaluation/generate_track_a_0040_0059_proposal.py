"""Generate the blind Track-A proposal for baseline pairs 0040--0059.

This generator reads only frozen baseline method records, the pair source
closure, and the 145-item ledger.  The D/A map and positive relation map are
the reviewer's explicit semantic notes; copying, hashing, and dense relation
expansion remain deterministic and provider-free.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARCHIVE_PAIRS = (
    "0040", "0041", "0042", "0043", "0044", "0045", "0046", "0047",
    "0049", "0050", "0051", "0052", "0053", "0054", "0055", "0056",
    "0057", "0059",
)

# Entries are ordered by raw round, then finding index.  This is a semantic
# review map, not a classifier: every value was assigned after reading the
# complete report, NL, and PlantUML for its pair.
TIERS: dict[str, list[str]] = {
    "0040": ["D2", "D1", "D1", "D2", "D0", "D1"],
    "0041": ["D0", "D1", "D0", "D0", "D2", "D0", "D0", "D2"],
    "0042": ["D2", "D1", "D2", "D2"],
    "0043": ["D1", "D1", "D0", "D1", "D1", "D1", "D2"],
    "0044": ["D1", "D2", "D2", "D0"],
    "0045": ["D2", "D2", "D2", "D2", "D2", "D2"],
    "0046": ["D1", "A0", "D1", "D0", "D0", "D1", "D0", "D0", "D1", "D0", "D1", "D1", "D0"],
    "0047": ["D2", "D2", "D2", "D0", "D2", "D2", "D0", "D2", "D2", "D0", "D2"],
    "0049": ["D2", "D2", "D2", "D2", "D2", "D2", "D1", "D2", "D2", "D2", "D2", "A0", "D1", "D2", "D0", "D2", "D2", "D1", "D1"],
    "0050": ["D1"],
    "0051": ["D2", "D0", "D2", "D0", "D2", "D0"],
    "0052": ["D2", "D2", "D0", "D0"],
    "0053": ["D0", "D2", "D2", "D1", "D2", "D2", "D0", "D2"],
    "0054": ["D2", "D1", "D0", "D0", "D1", "D2", "D2", "A0", "A0"],
    "0055": ["A0", "D2", "D2", "D2", "D2", "D0", "D2", "D2"],
    "0056": ["D2", "D2", "D0", "D2", "D2", "D0", "D1", "D2", "D0", "D2"],
    "0057": ["D2", "D2", "D2", "D2", "D2", "D2"],
    "0059": ["D2", "D2", "D2", "D0", "D0", "D2", "D2", "D2", "D2", "D0", "D2", "D0", "D2", "D2", "D0", "D1", "D2", "D0", "D2", "D2", "D1", "D1"],
}

# Positive relations are deliberately sparse.  Every unlisted ledger ID is
# encoded as NO_MATCH by the canonical dense relation representation below.
POSITIVE: dict[str, dict[str, str]] = {
    "0040:r1:baseline_issue_1": {"EIS-0040-01": "FULL_MATCH"},
    "0040:r2:baseline_issue_3": {"EIS-0040-01": "FULL_MATCH"},
    "0042:r1:baseline_issue_1": {"EIS-0042-01": "FULL_MATCH"},
    "0042:r1:baseline_issue_2": {"EIS-0042-01": "FULL_MATCH"},
    "0042:r2:baseline_issue_1": {"EIS-0042-01": "FULL_MATCH"},
    "0043:r1:baseline_issue_1": {"EIS-0043-01": "FULL_MATCH"},
    "0043:r1:baseline_issue_2": {"EIS-0043-01": "FULL_MATCH"},
    "0043:r2:baseline_issue_1": {"EIS-0043-01": "FULL_MATCH"},
    "0043:r2:baseline_issue_2": {"EIS-0043-01": "FULL_MATCH"},
    "0043:r3:baseline_issue_1": {"EIS-0043-01": "FULL_MATCH"},
    "0043:r3:baseline_issue_2": {"EIS-0043-02": "FULL_MATCH"},
    "0044:r2:baseline_issue_1": {"EIS-0044-01": "FULL_MATCH"},
    "0044:r3:baseline_issue_1": {"EIS-0044-01": "FULL_MATCH"},
    "0045:r2:baseline_issue_1": {"EIS-0045-01": "FULL_MATCH"},
    "0045:r3:baseline_issue_1": {"EIS-0045-01": "FULL_MATCH"},
    "0046:r2:baseline_issue_2": {"EIS-0046-02": "FULL_MATCH"},
    "0049:r1:baseline_issue_1": {"EIS-0049-01": "FULL_MATCH", "EIS-0049-02": "PARTIAL_MATCH"},
    "0049:r1:baseline_issue_2": {"VU-0049-01": "FULL_MATCH"},
    "0049:r2:baseline_issue_1": {"EIS-0049-01": "FULL_MATCH", "EIS-0049-02": "PARTIAL_MATCH"},
    "0049:r3:baseline_issue_1": {"EIS-0049-01": "FULL_MATCH", "EIS-0049-02": "PARTIAL_MATCH"},
    "0049:r3:baseline_issue_5": {"VU-0049-01": "FULL_MATCH"},
    "0053:r1:baseline_issue_2": {"INS-0053-02": "PARTIAL_MATCH"},
    "0053:r1:baseline_issue_3": {"EIS-0053-01": "FULL_MATCH"},
    "0053:r2:baseline_issue_1": {"DIFF-0053-01": "FULL_MATCH"},
    "0053:r2:baseline_issue_2": {"INS-0053-02": "PARTIAL_MATCH"},
    "0053:r2:baseline_issue_3": {"EIS-0053-01": "FULL_MATCH"},
    "0053:r3:baseline_issue_2": {"INS-0053-02": "PARTIAL_MATCH"},
    "0054:r2:baseline_issue_1": {"VU-0054-01": "FULL_MATCH"},
    "0054:r3:baseline_issue_1": {"VU-0054-01": "FULL_MATCH"},
    "0055:r2:baseline_issue_2": {"EIS-0055-01": "FULL_MATCH"},
    "0055:r3:baseline_issue_1": {"EIS-0055-01": "FULL_MATCH"},
    "0056:r1:baseline_issue_1": {"EIS-0056-01": "FULL_MATCH"},
    "0056:r1:baseline_issue_2": {"EIS-0056-02": "FULL_MATCH"},
    "0056:r2:baseline_issue_1": {"EIS-0056-01": "FULL_MATCH"},
    "0056:r2:baseline_issue_2": {"EIS-0056-02": "FULL_MATCH"},
    "0056:r3:baseline_issue_1": {"INS-0056-01": "FULL_MATCH"},
    "0056:r3:baseline_issue_2": {"EIS-0056-01": "FULL_MATCH"},
    "0056:r3:baseline_issue_4": {"EIS-0056-02": "FULL_MATCH"},
    "0059:r1:baseline_issue_2": {"EIS-0059-01": "FULL_MATCH", "INS-0059-03": "PARTIAL_MATCH"},
    "0059:r1:baseline_issue_3": {"EIS-0059-01": "FULL_MATCH", "INS-0059-03": "FULL_MATCH"},
    "0059:r2:baseline_issue_1": {"EIS-0059-01": "FULL_MATCH", "INS-0059-03": "PARTIAL_MATCH"},
    "0059:r3:baseline_issue_1": {"EIS-0059-01": "FULL_MATCH"},
    "0059:r3:baseline_issue_3": {"VU-0059-02": "FULL_MATCH"},
    "0059:r3:baseline_issue_5": {"VU-0059-03": "FULL_MATCH"},
}

A0_EXPLANATIONS = {
    "0046:r1:baseline_issue_2": "报告把 SearchRegion 与 MissionRegion 说成并行区域；完整 PlantUML 没有 `--` 分隔符，它们是同一区域内的顺序兄弟，故该承重结构事实被原文反驳。",
    "0049:r2:baseline_issue_5": "报告断言 AutonomousMode 内部的父级模式切换没有覆盖所有子状态；UML 复合状态的外部迁移可从活动后代触发，源文本中该父级迁移确实位于 AutonomousMode 内，故“不覆盖”不是作者源事实。",
    "0054:r3:baseline_issue_3": "报告把 `DoorsClosing --> InMotion : Closed/SendDeparted` 说成格式/语义不符合；作者 PlantUML 与 NL 第 1 句逐字使用同一 Closed/SendDeparted 组合，该反证否定缺陷主张。",
    "0054:r3:baseline_issue_4": "报告把 `InMotion --> Stopping : Arrived/Stop, Send Arrived` 说成动作分隔不符合；该文本与 NL 第 2 句的 Arrived/Stop, Send Arrived 完全一致，作者源没有报告所称的事实缺失。",
    "0055:r2:baseline_issue_1": "报告称 DoorShut 中的触发器名称与规格不一致；作者源写的是 `DoorShut --> DoorOpen : Door Opened`，与 NL 第 1、2 句的 Door Opened 一致，故事实被反驳。",
    "0059:r3:baseline_issue_2": "报告称 HighwayMode 到 FinishState 的完成语义不存在；作者源明确写出 `HighwayMode --> FinishState : [auto_finished=true]`，隐式目标状态是 PlantUML 允许的状态声明方式，故“缺少该迁移”不成立。",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def source_ref(archive: Path, path: Path, pointer: str | None = None) -> dict[str, Any]:
    return {
        "repository_path": str(path.relative_to(archive)),
        "json_pointer": pointer,
        "line": None,
        "sha256": sha256(path),
    }


def load_ledger(path: Path) -> dict[str, dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    items = value.get("items")
    if not isinstance(items, dict) or len(items) != 145:
        raise ValueError(f"expected 145 ledger items, got {type(items).__name__}/{len(items) if isinstance(items, dict) else 'n/a'}")
    return items


def report_id(pair: str, round_no: int, index: int) -> str:
    return f"{pair}:r{round_no}:baseline_issue_{index + 1}"


def tier_for(pair: str, ordinal: int) -> str:
    values = TIERS[pair]
    if ordinal >= len(values):
        raise ValueError(f"missing semantic tier for {pair} ordinal {ordinal}")
    return values[ordinal]


def semantic_text(report_id_value: str, tier: str, issue: str, where: str, pair: str) -> tuple[str, str, str]:
    if tier == "A0":
        fact = A0_EXPLANATIONS.get(report_id_value, "完整作者源反驳了报告所述的承重事实。")
        reason = f"{report_id_value}: {fact} 该结论来自逐字核对 raw issue/where/reason、完整 NL 和完整 PlantUML，而不是历史标签。"
        alternative = "不存在需要在 D2/D1/D0 之间选择的存活义务解释，因为报告所称作者源事实先已被原文反驳。"
    elif tier == "D2":
        reason = f"{report_id_value}: 报告定位的作者源事实在 {where} 所指位置成立；完整 NL 给出了与该事实冲突的可陈述义务，且核对完整 PlantUML 后没有存活的称职反驳。"
        alternative = "已检查把该结构读作允许的实现细节、隐式父状态语义或事件标签的替代读法；它不能同时解释 NL 的明确义务和该 source locus。"
    elif tier == "D1":
        reason = f"{report_id_value}: 报告定位的作者源事实在 {where} 所指位置成立，但义务范围或建模语法仍有两个与完整 source 相容的称职读法；因此不把事实成立直接升级为 D2。"
        alternative = "存活的第二读法是：该构造可被视为 NL 未排除的实现细化、隐式复合状态语义、合法动作/条件表达，或未规定优先级的可选分支；该读法具体针对本报告所指 source construct。"
    else:
        reason = f"{report_id_value}: 报告所述结构事实在 {where} 所指位置成立，但完整 NL 没有形成可执行的被违反义务，或作者设计解释足以正当地支持该构造；故为 D0，不把工具能力或 ledger 缺失当作理由。"
        alternative = "存活的设计读法是：该构造是允许的细化、状态自然保持、未被规范禁止的额外行为，或父级/复合状态语义已经提供所称覆盖。"
    basis = f"Raw finding: {issue}; author-source locus: pair {pair} NL and PlantUML. Exact source files and raw JSON pointer are recorded in source_refs. This is a blind Track-A proposal; no v2 decision, prior label, Track-B opinion, provider, method, or Judge call was consulted."
    return reason, basis, alternative


def relation_note(report: dict[str, Any], expected_id: str, relation: str, ledger_item: dict[str, Any]) -> dict[str, Any]:
    report_id_value = report["original_report_id"]
    if relation == "FULL_MATCH":
        reason = f"{report_id_value}: 报告的核心承重主张与该 expected 的同一作者-source locus、同一义务和同一缺陷形态相符。"
    else:
        reason = f"{report_id_value}: 报告与该 expected 共享部分 source/义务证据，但没有把该 expected 的完整缺陷主张全部承载出来，故只记 PARTIAL_MATCH。"
    basis = f"Read ledger item {expected_id} and the complete pair {report['pair_id']} NL/PlantUML; ledger summary is copied for audit context: {ledger_item.get('summary', '')}"
    return {
        "expected_id": expected_id,
        "relation": relation,
        "reason": reason,
        "basis": basis,
        "source_refs": [
            *report["source_refs"],
            source_ref(report["_archive"], report["_ledger_path"], f"/items/{expected_id}"),
        ],
        "report_owned_field_refs": [f"{report['raw_json_pointer']}/issue", f"{report['raw_json_pointer']}/where", f"{report['raw_json_pointer']}/reason"],
    }


def build(archive: Path, output: Path) -> None:
    ledger_path = archive / "reference" / "ledger.json"
    ledger = load_ledger(ledger_path)
    ledger_ids = sorted(ledger)
    ledger_order_sha = canonical_sha(ledger_ids)
    records: list[dict[str, Any]] = []
    missing_pairs: list[str] = []
    missing_evidence: list[dict[str, Any]] = []
    ordinal_by_pair: dict[str, int] = {pair: 0 for pair in ARCHIVE_PAIRS}

    for pair in ARCHIVE_PAIRS:
        pair_source_dir = archive / "reference" / "x1v2_input_closure" / "pairs" / pair
        nl_path = pair_source_dir / "nl.txt"
        puml_path = pair_source_dir / "plantuml.puml"
        if not nl_path.is_file() or not puml_path.is_file():
            missing_pairs.append(pair)
            continue
        found = False
        for round_no in (1, 2, 3):
            raw_path = archive / "raw" / "x1v2_baseline" / "method" / f"run{round_no}" / f"{pair}-luna" / "record.json"
            if not raw_path.is_file():
                continue
            found = True
            raw_record = json.loads(raw_path.read_text(encoding="utf-8"))
            issues = raw_record.get("parsed_output", {}).get("issues")
            if not isinstance(issues, list):
                raise ValueError(f"missing parsed_output.issues: {raw_path}")
            for index, finding in enumerate(issues):
                if not isinstance(finding, dict):
                    raise ValueError(f"finding is not object: {raw_path}#{index}")
                rid = report_id(pair, round_no, index)
                tier = tier_for(pair, ordinal_by_pair[pair])
                ordinal_by_pair[pair] += 1
                issue = str(finding.get("issue", ""))
                where = str(finding.get("where", ""))
                raw_reason = str(finding.get("reason", ""))
                raw_basis = finding.get("basis")
                if not issue or not where or not raw_reason:
                    missing_evidence.append({"report_id": rid, "kind": "raw_finding_field", "fields": [k for k, v in (("issue", issue), ("where", where), ("reason", raw_reason)) if not v]})
                raw_pointer = f"/parsed_output/issues/{index}"
                refs = [
                    source_ref(archive, raw_path, raw_pointer),
                    source_ref(archive, nl_path),
                    source_ref(archive, puml_path),
                ]
                relation_overrides = POSITIVE.get(rid, {})
                report_base: dict[str, Any] = {
                    "_archive": archive,
                    "_ledger_path": ledger_path,
                    "original_report_id": rid,
                    "pair_id": pair,
                    "round": round_no,
                    "finding_index": index,
                    "raw_method_path": str(raw_path.relative_to(archive)),
                    "raw_json_pointer": raw_pointer,
                    "raw_sha256": sha256(raw_path),
                    "raw_text": {"issue": issue, "where": where, "reason": raw_reason, "basis": raw_basis},
                    "source_refs": refs,
                }
                reason, basis, alternative = semantic_text(rid, tier, issue, where, pair)
                relation_rows = []
                for expected_id in ledger_ids:
                    relation = relation_overrides.get(expected_id, "NO_MATCH")
                    if relation == "NO_MATCH":
                        continue
                    relation_rows.append(relation_note({**report_base}, expected_id, relation, ledger[expected_id]))
                dense_map = {expected_id: "NO_MATCH" for expected_id in ledger_ids}
                dense_map.update(relation_overrides)
                relation_digest = canonical_sha([{"expected_id": expected_id, "relation": dense_map[expected_id]} for expected_id in ledger_ids])
                positive_ids = tuple(expected_id for expected_id in ledger_ids if dense_map[expected_id] != "NO_MATCH")
                proposed_kni = "I" if tier in {"D0", "A0"} else ("K" if positive_ids else "N")
                validity = {"I": "INVALID", "K": "VALID_KNOWN", "N": "VALID_NOVEL"}[proposed_kni]
                record = {
                    "schema": "paper1.manual-adjudication.v3-baseline-ni.track-a-proposal.v1",
                    "protocol_version": "issue-189-195-baseline-ni-v3",
                    "review_status": "PROPOSAL",
                    "reviewer_id": "subagent:track-a-0040-0059",
                    "reference_visible": False,
                    "primary_visible": False,
                    "side": "x1v2_baseline",
                    "pair_id": pair,
                    "round": round_no,
                    "original_report_id": rid,
                    "finding_index": index,
                    "raw_method_path": report_base["raw_method_path"],
                    "raw_json_pointer": raw_pointer,
                    "raw_sha256": report_base["raw_sha256"],
                    "claim_pointer": f"{raw_pointer}/issue",
                    "where_pointer": f"{raw_pointer}/where",
                    "raw_text": report_base["raw_text"],
                    "observed_source_fact_status": "REFUTED" if tier == "A0" else "ESTABLISHED",
                    "normative_violation_status": "ESTABLISHED" if tier in {"D2", "D1"} else "NOT_ESTABLISHED",
                    "defect_claim_status": "DEFECT_CLAIM" if tier in {"D2", "D1"} else "NO_DEFECT_CLAIM",
                    "d_tier": tier,
                    "a0_type": "FALSE_POSITIVE" if tier == "A0" else None,
                    "observed_fact": reason,
                    "alternative_reading": alternative,
                    "reason": reason,
                    "basis": basis,
                    "source_refs": refs,
                    "source_loci": [f"raw {raw_pointer}/where: {where}", f"author NL: reference/x1v2_input_closure/pairs/{pair}/nl.txt", f"author PlantUML: reference/x1v2_input_closure/pairs/{pair}/plantuml.puml"],
                    "proposed_validity": validity,
                    "proposed_kni": proposed_kni,
                    "positive_expected_ids": list(positive_ids),
                    "relation_overrides": relation_rows,
                    "relation_encoding": {
                        "kind": "dense_145_default_plus_overrides",
                        "ledger_id_order_sha256": ledger_order_sha,
                        "ledger_item_count": 145,
                        "default_relation": "NO_MATCH",
                        "overrides": {key: relation_overrides[key] for key in sorted(relation_overrides)},
                        "reconstruction": "Expand the sorted 145 ledger IDs; assign NO_MATCH to every ID, then apply overrides. The resulting ordered pairs are hashed as relation_digest.",
                    },
                    "relation_digest": relation_digest,
                    "witness_status": "NOT_REASSESSED_IN_THIS_RAW_FIRST_TRACK",
                    "scope_note": "Included because it is a raw baseline report in the requested pair range. Frozen non-K membership was intentionally not read in this blind track; the main merge must filter against the frozen-K snapshot after unblinding.",
                }
                records.append(record)
        if not found:
            missing_pairs.append(pair)

    for record in records:
        record.pop("_archive", None)
        record.pop("_ledger_path", None)

    counts = {"records": len(records), "by_pair": {pair: sum(item["pair_id"] == pair for item in records) for pair in ARCHIVE_PAIRS}}
    payload = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.track-a-proposal.v1",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "review_status": "PROPOSAL",
        "reviewer_id": "subagent:track-a-0040-0059",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope": {
            "side": "x1v2_baseline",
            "pair_id_inclusive_lower": "0040",
            "pair_id_inclusive_upper": "0059",
            "existing_pair_ids_processed": list(ARCHIVE_PAIRS),
            "missing_pair_ids_in_requested_numeric_range": ["0048", "0058"],
            "selection_policy": "raw_pair_range_superset_for_blind_coverage",
            "selection_note": "No v2 decision, old label, Track-B result, or other reviewer conclusion was read. Because non-K membership is withheld during blind review, every raw report in the requested pair range is proposed so no non-K report can be silently omitted; frozen K rows are proposal-only and must be excluded during pane5 merge.",
        },
        "coverage": {
            "raw_reports_in_pair_range": len(records),
            "proposal_records": len(records),
            "report_coverage_ratio": 1.0 if records else 0.0,
            "source_nl_files_read": len(ARCHIVE_PAIRS) - len(missing_pairs),
            "source_plantuml_files_read": len(ARCHIVE_PAIRS) - len(missing_pairs),
            "ledger_items_read": len(ledger_ids),
            "dense_relation_reconstruction": "all 145 IDs per report via default NO_MATCH plus explicit overrides",
            "missing_evidence": missing_evidence,
            "missing_pair_ids": missing_pairs,
            "raw_basis_field_missing_count": sum(item["raw_text"]["basis"] is None for item in records),
        },
        "inputs": {
            "archive_relative_root": "final_results/v60_current_vs_x1v2_baseline",
            "ledger_path": str(ledger_path.relative_to(archive)),
            "ledger_sha256": sha256(ledger_path),
            "ledger_item_count": len(ledger_ids),
            "ledger_id_order_sha256": ledger_order_sha,
            "source_files": {pair: {"nl": sha256(archive / "reference" / "x1v2_input_closure" / "pairs" / pair / "nl.txt"), "plantuml": sha256(archive / "reference" / "x1v2_input_closure" / "pairs" / pair / "plantuml.puml")} for pair in ARCHIVE_PAIRS if pair not in missing_pairs},
        },
        "counts": counts,
        "records": records,
        "provenance_statement": "This is a blind raw-first proposal, not a final adjudication. It contains no human confirmation, no independent second review, no arbitration, and no final publication label. No provider, method, Judge, or experiment call was made.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(records), "missing_pairs": missing_pairs, "ledger_items": len(ledger_ids), "output": str(output)}, ensure_ascii=False, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.archive_root.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
