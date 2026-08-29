"""Write the independent raw-first Track-B proposal for pairs 0020--0059.

The input boundary is deliberately narrow.  This module reads method
``record.json`` files, the author NL/PlantUML closure, the reference ledger,
and the frozen protocol documents only.  It does not inspect any decision,
proposal, register, or Judge output.  The semantic notes below are a manual
review matrix keyed by raw report identity; the code only expands those notes
to all 145 relation rows, hashes the evidence, and checks coverage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PAIR_IDS = [f"{number:04d}" for number in range(20, 60)]
PROTOCOL_FILES = [
    "discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md",
    "discover_matrix/docs/protocol/dtier_triage.md",
    "discover_matrix/docs/protocol/defect_taxonomy.md",
    "discover_matrix/docs/protocol/manual_review_spec.md",
]


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(encoded)


def relative_path(root: Path, path: Path) -> str:
    return str(path.relative_to(root))


def source_ref(root: Path, path: Path, locator: str) -> dict[str, Any]:
    return {
        "repository_path": relative_path(root, path),
        "sha256": sha256_file(path),
        "locator": locator,
    }


def report_id(pair: str, round_number: int, index: int) -> str:
    return f"{pair}:r{round_number}:baseline_issue_{index + 1}"


def load_ledger(path: Path) -> dict[str, dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    items = value.get("items")
    if not isinstance(items, dict) or len(items) != 145:
        raise ValueError(f"reference ledger must contain 145 items, got {len(items) if isinstance(items, dict) else 'invalid'}")
    return items


# These are explicit review annotations, rather than a classifier.  A key is
# a raw report ID and a value is the reviewer conclusion after reading that
# report together with its complete pair source.  The conservative default is
# D1 because the proposal must not turn an unrecorded boundary case into D2.
TIER_OVERRIDES: dict[str, str] = {
    # 0020--0027
    "0020:r1:baseline_issue_1": "D1",
    "0020:r2:baseline_issue_1": "D1",
    "0020:r2:baseline_issue_2": "D1",
    "0020:r2:baseline_issue_3": "D1",
    "0020:r2:baseline_issue_4": "D0",
    "0020:r2:baseline_issue_5": "D1",
    "0020:r3:baseline_issue_1": "D1",
    "0020:r3:baseline_issue_2": "D1",
    "0020:r3:baseline_issue_3": "D1",
    "0021:r1:baseline_issue_1": "D0",
    "0021:r1:baseline_issue_2": "D0",
    "0021:r2:baseline_issue_1": "D0",
    "0021:r2:baseline_issue_2": "D0",
    "0021:r3:baseline_issue_1": "D0",
    "0022:r1:baseline_issue_1": "D2",
    "0022:r1:baseline_issue_2": "D1",
    "0022:r2:baseline_issue_1": "D2",
    "0022:r2:baseline_issue_2": "D1",
    "0022:r3:baseline_issue_1": "D2",
    "0022:r3:baseline_issue_2": "D1",
    "0022:r3:baseline_issue_3": "D1",
    "0023:r1:baseline_issue_1": "D2",
    "0023:r1:baseline_issue_2": "D2",
    "0023:r2:baseline_issue_1": "D2",
    "0023:r2:baseline_issue_2": "D2",
    "0023:r2:baseline_issue_3": "D1",
    "0024:r1:baseline_issue_1": "D1",
    "0024:r1:baseline_issue_2": "D1",
    "0024:r1:baseline_issue_3": "D2",
    "0024:r1:baseline_issue_4": "D2",
    "0024:r1:baseline_issue_5": "D2",
    "0024:r1:baseline_issue_6": "D1",
    "0024:r2:baseline_issue_1": "D1",
    "0024:r2:baseline_issue_2": "D1",
    "0024:r2:baseline_issue_3": "D2",
    "0024:r2:baseline_issue_4": "D2",
    "0024:r2:baseline_issue_5": "D1",
    "0024:r2:baseline_issue_6": "D2",
    "0024:r2:baseline_issue_7": "D1",
    "0024:r3:baseline_issue_1": "D2",
    "0024:r3:baseline_issue_2": "D1",
    "0024:r3:baseline_issue_3": "D2",
    "0024:r3:baseline_issue_4": "D2",
    "0024:r3:baseline_issue_5": "D2",
    "0025:r1:baseline_issue_1": "D1",
    "0025:r1:baseline_issue_2": "D1",
    "0025:r1:baseline_issue_3": "D1",
    "0025:r1:baseline_issue_4": "D1",
    "0025:r1:baseline_issue_5": "D1",
    "0025:r1:baseline_issue_6": "D1",
    "0025:r2:baseline_issue_1": "D1",
    "0025:r2:baseline_issue_2": "D1",
    "0025:r3:baseline_issue_1": "D1",
    "0025:r3:baseline_issue_2": "D1",
    "0025:r3:baseline_issue_3": "D1",
    "0025:r3:baseline_issue_4": "D1",
    "0025:r3:baseline_issue_5": "D1",
    "0025:r3:baseline_issue_6": "D1",
    "0026:r1:baseline_issue_1": "D1",
    "0026:r1:baseline_issue_2": "D2",
    "0026:r2:baseline_issue_1": "D2",
    "0026:r2:baseline_issue_2": "D2",
    "0026:r2:baseline_issue_3": "D1",
    "0026:r3:baseline_issue_1": "D2",
    "0026:r3:baseline_issue_2": "D1",
    "0027:r1:baseline_issue_1": "D2",
    "0027:r1:baseline_issue_2": "D2",
    "0027:r2:baseline_issue_1": "D1",
    "0027:r2:baseline_issue_2": "D2",
    "0027:r2:baseline_issue_3": "D1",
    "0027:r3:baseline_issue_1": "D1",
    "0027:r3:baseline_issue_2": "D2",
    "0027:r3:baseline_issue_3": "D2",
    "0027:r3:baseline_issue_4": "D2",
    # 0029--0039
    "0029:r1:baseline_issue_1": "D2",
    "0029:r1:baseline_issue_2": "D2",
    "0029:r1:baseline_issue_3": "D2",
    "0029:r1:baseline_issue_4": "D2",
    "0029:r1:baseline_issue_5": "D1",
    "0029:r1:baseline_issue_6": "D2",
    "0029:r1:baseline_issue_7": "D1",
    "0029:r2:baseline_issue_1": "D2",
    "0029:r2:baseline_issue_2": "D2",
    "0029:r2:baseline_issue_3": "D2",
    "0029:r2:baseline_issue_4": "D2",
    "0029:r2:baseline_issue_5": "D2",
    "0029:r3:baseline_issue_1": "D2",
    "0029:r3:baseline_issue_2": "D2",
    "0029:r3:baseline_issue_3": "D2",
    "0029:r3:baseline_issue_4": "D2",
    "0029:r3:baseline_issue_5": "D2",
    "0029:r3:baseline_issue_6": "D1",
    "0030:r1:baseline_issue_1": "D2",
    "0030:r1:baseline_issue_2": "D1",
    "0030:r1:baseline_issue_3": "D2",
    "0030:r2:baseline_issue_1": "D2",
    "0030:r2:baseline_issue_2": "D1",
    "0030:r2:baseline_issue_3": "D2",
    "0030:r2:baseline_issue_4": "D1",
    "0030:r3:baseline_issue_1": "D1",
    "0030:r3:baseline_issue_2": "D2",
    "0030:r3:baseline_issue_3": "D2",
    "0031:r1:baseline_issue_1": "D0",
    "0031:r1:baseline_issue_2": "D0",
    "0031:r2:baseline_issue_1": "D0",
    "0031:r2:baseline_issue_2": "D1",
    "0031:r3:baseline_issue_1": "A0",
    "0031:r3:baseline_issue_2": "D0",
    "0031:r3:baseline_issue_3": "D0",
    "0031:r3:baseline_issue_4": "D1",
    "0032:r1:baseline_issue_1": "D1",
    "0032:r1:baseline_issue_2": "D1",
    "0032:r1:baseline_issue_3": "D1",
    "0032:r2:baseline_issue_1": "D2",
    "0032:r2:baseline_issue_2": "D1",
    "0032:r2:baseline_issue_3": "D1",
    "0032:r2:baseline_issue_4": "D1",
    "0032:r3:baseline_issue_1": "A0",
    "0032:r3:baseline_issue_2": "D1",
    "0032:r3:baseline_issue_3": "D1",
    "0033:r1:baseline_issue_1": "D2",
    "0033:r1:baseline_issue_2": "D2",
    "0033:r1:baseline_issue_3": "D2",
    "0033:r1:baseline_issue_4": "D0",
    "0033:r2:baseline_issue_1": "D2",
    "0033:r2:baseline_issue_2": "D2",
    "0033:r2:baseline_issue_3": "D2",
    "0033:r2:baseline_issue_4": "D0",
    "0033:r3:baseline_issue_1": "D2",
    "0033:r3:baseline_issue_2": "D2",
    "0033:r3:baseline_issue_3": "D2",
    "0034:r1:baseline_issue_1": "D2",
    "0034:r1:baseline_issue_2": "D1",
    "0034:r1:baseline_issue_3": "D1",
    "0034:r1:baseline_issue_4": "D2",
    "0034:r1:baseline_issue_5": "D2",
    "0034:r1:baseline_issue_6": "D1",
    "0034:r1:baseline_issue_7": "D1",
    "0034:r1:baseline_issue_8": "D1",
    "0034:r1:baseline_issue_9": "D1",
    "0034:r1:baseline_issue_10": "D2",
    "0034:r2:baseline_issue_1": "D2",
    "0034:r2:baseline_issue_2": "D1",
    "0034:r2:baseline_issue_3": "D2",
    "0034:r2:baseline_issue_4": "D2",
    "0034:r2:baseline_issue_5": "D1",
    "0034:r2:baseline_issue_6": "D2",
    "0034:r2:baseline_issue_7": "D1",
    "0034:r2:baseline_issue_8": "D1",
    "0034:r2:baseline_issue_9": "D1",
    "0034:r2:baseline_issue_10": "D2",
    "0034:r3:baseline_issue_1": "D2",
    "0034:r3:baseline_issue_2": "D1",
    "0034:r3:baseline_issue_3": "D2",
    "0034:r3:baseline_issue_4": "D2",
    "0034:r3:baseline_issue_5": "D2",
    "0034:r3:baseline_issue_6": "D2",
    "0034:r3:baseline_issue_7": "D1",
    "0034:r3:baseline_issue_8": "D1",
    "0034:r3:baseline_issue_9": "D1",
    "0035:r1:baseline_issue_1": "D1",
    "0035:r1:baseline_issue_2": "D2",
    "0035:r1:baseline_issue_3": "D1",
    "0035:r1:baseline_issue_4": "D1",
    "0035:r1:baseline_issue_5": "D1",
    "0035:r1:baseline_issue_6": "D0",
    "0035:r2:baseline_issue_1": "A0",
    "0035:r2:baseline_issue_2": "D2",
    "0035:r2:baseline_issue_3": "D1",
    "0035:r3:baseline_issue_1": "D0",
    "0035:r3:baseline_issue_2": "D1",
    "0036:r1:baseline_issue_1": "D2",
    "0036:r1:baseline_issue_2": "D2",
    "0036:r1:baseline_issue_3": "D2",
    "0036:r1:baseline_issue_4": "D1",
    "0036:r1:baseline_issue_5": "D1",
    "0036:r1:baseline_issue_6": "A0",
    "0036:r1:baseline_issue_7": "D1",
    "0036:r2:baseline_issue_1": "D2",
    "0036:r2:baseline_issue_2": "D1",
    "0036:r2:baseline_issue_3": "D1",
    "0036:r2:baseline_issue_4": "D1",
    "0036:r2:baseline_issue_5": "A0",
    "0036:r2:baseline_issue_6": "D1",
    "0036:r3:baseline_issue_1": "D2",
    "0036:r3:baseline_issue_2": "D1",
    "0036:r3:baseline_issue_3": "D1",
    "0036:r3:baseline_issue_4": "D1",
    "0037:r1:baseline_issue_1": "D2",
    "0037:r1:baseline_issue_2": "D1",
    "0037:r1:baseline_issue_3": "D1",
    "0037:r1:baseline_issue_4": "D1",
    "0037:r2:baseline_issue_1": "D2",
    "0037:r2:baseline_issue_2": "D1",
    "0037:r2:baseline_issue_3": "D1",
    "0037:r3:baseline_issue_1": "D2",
    "0037:r3:baseline_issue_2": "D1",
    "0037:r3:baseline_issue_3": "D2",
    "0039:r1:baseline_issue_1": "D1",
    "0039:r2:baseline_issue_1": "D2",
    "0039:r3:baseline_issue_1": "D1",
    "0039:r3:baseline_issue_2": "D1",
    "0039:r3:baseline_issue_3": "D1",
    # 0040--0059
    "0040:r1:baseline_issue_1": "D2",
    "0040:r2:baseline_issue_1": "D1",
    "0040:r2:baseline_issue_2": "D1",
    "0040:r2:baseline_issue_3": "D2",
    "0040:r3:baseline_issue_1": "D0",
    "0040:r3:baseline_issue_2": "D1",
    "0041:r1:baseline_issue_1": "D0",
    "0041:r1:baseline_issue_2": "D1",
    "0041:r2:baseline_issue_1": "D0",
    "0041:r2:baseline_issue_2": "D0",
    "0041:r2:baseline_issue_3": "D0",
    "0041:r3:baseline_issue_1": "D0",
    "0041:r3:baseline_issue_2": "D0",
    "0041:r3:baseline_issue_3": "D0",
    "0042:r1:baseline_issue_1": "D2",
    "0042:r1:baseline_issue_2": "D2",
    "0042:r2:baseline_issue_1": "D2",
    "0042:r2:baseline_issue_2": "D2",
    "0043:r1:baseline_issue_1": "D2",
    "0043:r1:baseline_issue_2": "D2",
    "0043:r1:baseline_issue_3": "D1",
    "0043:r2:baseline_issue_1": "D2",
    "0043:r2:baseline_issue_2": "D2",
    "0043:r3:baseline_issue_1": "D2",
    "0043:r3:baseline_issue_2": "D2",
    "0044:r1:baseline_issue_1": "D1",
    "0044:r2:baseline_issue_1": "D2",
    "0044:r3:baseline_issue_1": "D2",
    "0044:r3:baseline_issue_2": "D1",
    "0045:r2:baseline_issue_1": "D2",
    "0045:r2:baseline_issue_2": "D2",
    "0045:r2:baseline_issue_3": "D2",
    "0045:r3:baseline_issue_1": "D2",
    "0045:r3:baseline_issue_2": "D2",
    "0045:r3:baseline_issue_3": "D2",
    "0046:r1:baseline_issue_1": "D1",
    "0046:r1:baseline_issue_2": "D2",
    "0046:r1:baseline_issue_3": "D2",
    "0046:r1:baseline_issue_4": "D1",
    "0046:r2:baseline_issue_1": "D1",
    "0046:r2:baseline_issue_2": "D2",
    "0046:r2:baseline_issue_3": "D1",
    "0046:r2:baseline_issue_4": "D1",
    "0046:r3:baseline_issue_1": "D1",
    "0046:r3:baseline_issue_2": "D0",
    "0046:r3:baseline_issue_3": "D1",
    "0046:r3:baseline_issue_4": "D1",
    "0046:r3:baseline_issue_5": "D2",
    "0047:r1:baseline_issue_1": "D2",
    "0047:r1:baseline_issue_2": "D2",
    "0047:r1:baseline_issue_3": "D1",
    "0047:r1:baseline_issue_4": "D1",
    "0047:r2:baseline_issue_1": "D2",
    "0047:r2:baseline_issue_2": "D2",
    "0047:r2:baseline_issue_3": "D1",
    "0047:r3:baseline_issue_1": "D2",
    "0047:r3:baseline_issue_2": "D2",
    "0047:r3:baseline_issue_3": "D1",
    "0047:r3:baseline_issue_4": "D1",
    "0049:r1:baseline_issue_1": "D2",
    "0049:r1:baseline_issue_2": "D1",
    "0049:r1:baseline_issue_3": "D1",
    "0049:r1:baseline_issue_4": "D1",
    "0049:r1:baseline_issue_5": "D1",
    "0049:r1:baseline_issue_6": "D1",
    "0049:r1:baseline_issue_7": "D1",
    "0049:r2:baseline_issue_1": "D2",
    "0049:r2:baseline_issue_2": "D1",
    "0049:r2:baseline_issue_3": "D1",
    "0049:r2:baseline_issue_4": "D1",
    "0049:r2:baseline_issue_5": "D1",
    "0049:r2:baseline_issue_6": "D1",
    "0049:r3:baseline_issue_1": "D2",
    "0049:r3:baseline_issue_2": "D1",
    "0049:r3:baseline_issue_3": "D1",
    "0049:r3:baseline_issue_4": "D1",
    "0049:r3:baseline_issue_5": "D1",
    "0049:r3:baseline_issue_6": "D1",
    "0050:r3:baseline_issue_1": "D1",
    "0051:r1:baseline_issue_1": "D0",
    "0051:r1:baseline_issue_2": "D0",
    "0051:r2:baseline_issue_1": "D0",
    "0051:r2:baseline_issue_2": "D0",
    "0051:r3:baseline_issue_1": "D0",
    "0051:r3:baseline_issue_2": "D0",
    "0052:r2:baseline_issue_1": "D0",
    "0052:r2:baseline_issue_2": "D1",
    "0052:r3:baseline_issue_1": "D0",
    "0052:r3:baseline_issue_2": "D0",
    "0053:r1:baseline_issue_1": "D2",
    "0053:r1:baseline_issue_2": "D2",
    "0053:r1:baseline_issue_3": "D2",
    "0053:r2:baseline_issue_1": "D2",
    "0053:r2:baseline_issue_2": "D2",
    "0053:r2:baseline_issue_3": "D2",
    "0053:r3:baseline_issue_1": "D2",
    "0053:r3:baseline_issue_2": "D2",
    "0054:r2:baseline_issue_1": "D2",
    "0054:r2:baseline_issue_2": "D1",
    "0054:r2:baseline_issue_3": "D1",
    "0054:r2:baseline_issue_4": "D1",
    "0054:r2:baseline_issue_5": "D1",
    "0054:r3:baseline_issue_1": "D2",
    "0054:r3:baseline_issue_2": "D1",
    "0054:r3:baseline_issue_3": "D1",
    "0054:r3:baseline_issue_4": "D1",
    "0055:r2:baseline_issue_1": "D1",
    "0055:r2:baseline_issue_2": "D2",
    "0055:r2:baseline_issue_3": "D2",
    "0055:r2:baseline_issue_4": "D2",
    "0055:r2:baseline_issue_5": "D2",
    "0055:r2:baseline_issue_6": "D1",
    "0055:r3:baseline_issue_1": "D2",
    "0055:r3:baseline_issue_2": "D2",
    "0056:r1:baseline_issue_1": "D1",
    "0056:r1:baseline_issue_2": "D2",
    "0056:r1:baseline_issue_3": "D1",
    "0056:r2:baseline_issue_1": "D1",
    "0056:r2:baseline_issue_2": "D2",
    "0056:r2:baseline_issue_3": "D1",
    "0056:r3:baseline_issue_1": "D1",
    "0056:r3:baseline_issue_2": "D1",
    "0056:r3:baseline_issue_3": "D1",
    "0056:r3:baseline_issue_4": "D2",
    "0057:r1:baseline_issue_1": "D2",
    "0057:r1:baseline_issue_2": "D1",
    "0057:r2:baseline_issue_1": "D1",
    "0057:r2:baseline_issue_2": "D2",
    "0057:r3:baseline_issue_1": "D1",
    "0057:r3:baseline_issue_2": "D2",
    "0059:r1:baseline_issue_1": "D1",
    "0059:r1:baseline_issue_2": "D1",
    "0059:r1:baseline_issue_3": "D1",
    "0059:r1:baseline_issue_4": "D1",
    "0059:r1:baseline_issue_5": "D1",
    "0059:r1:baseline_issue_6": "D1",
    "0059:r1:baseline_issue_7": "D1",
    "0059:r1:baseline_issue_8": "D1",
    "0059:r1:baseline_issue_9": "D1",
    "0059:r1:baseline_issue_10": "D1",
    "0059:r2:baseline_issue_1": "D1",
    "0059:r2:baseline_issue_2": "D1",
    "0059:r2:baseline_issue_3": "D1",
    "0059:r2:baseline_issue_4": "D1",
    "0059:r2:baseline_issue_5": "D1",
    "0059:r2:baseline_issue_6": "D1",
    "0059:r3:baseline_issue_1": "D1",
    "0059:r3:baseline_issue_2": "D1",
    "0059:r3:baseline_issue_3": "D1",
    "0059:r3:baseline_issue_4": "D1",
    "0059:r3:baseline_issue_5": "D1",
    "0059:r3:baseline_issue_6": "D1",
}


A0_REASON = {
    "0031:r3:baseline_issue_1": "原报告自己承认 Brake Signal Received 的方向和来源与规格一致；作者 PlantUML 逐字存在 InitialState --> BrakingState，因此所称缺陷事实不成立。",
    "0032:r3:baseline_issue_1": "原报告把三个普通嵌套 state 说成并行区域，但完整 PlantUML 没有 -- 分隔符；该承重结构事实被作者源反驳。",
    "0035:r2:baseline_issue_1": "原报告称 DoorShut 的 Cancel 自环缺失，但完整 PlantUML 明确写有 DoorShut --> DoorShut : Cancel；所称事实不成立。",
    "0036:r1:baseline_issue_6": "原报告把 Attack --> AttackReady : Attack Complete / UAV Count Decreased 的斜杠后文本说成注释；作者源将其写在迁移 effect 位置，所称“没有动作文本”不成立。",
    "0036:r2:baseline_issue_5": "原报告把 Attack --> AttackReady : Attack Complete / UAV Count Decreased 的斜杠后文本说成没有动作；完整 PlantUML存在该 effect 文本，承重事实不成立。",
    "0046:r3:baseline_issue_2": "原报告把 MissionRegion --> SearchRegion : Start Mission 说成未定义，但完整作者 PlantUML明确存在该边；该具体事实不成立。",
}


# Positive relation notes are also explicit review annotations.  Every ledger
# ID not present in a record's map is a dense NO_MATCH row.  The values are
# relation strengths, not labels copied from any Judge output.
RELATION_OVERRIDES: dict[str, dict[str, str]] = {}


def add_relation(expected_id: str, report_ids: list[str], relation: str = "FULL_MATCH") -> None:
    for rid in report_ids:
        RELATION_OVERRIDES.setdefault(rid, {})[expected_id] = relation


def ids(pair: str, positions: dict[int, list[int]]) -> list[str]:
    return [report_id(pair, round_number, index) for round_number, indexes in positions.items() for index in indexes]


def build_relation_matrix() -> None:
    # 0020
    add_relation("EIS-0020-02", ids("0020", {1: [0], 2: [0, 4], 3: [0, 1]}))
    # 0023: these reports identify the same source omission only partially
    # when they describe the wrong entry shape rather than each dead state.
    add_relation("INS-0023-01", ids("0023", {1: [0], 2: [0, 2]}), "PARTIAL_MATCH")
    add_relation("INS-0023-02", ids("0023", {1: [0], 2: [0, 2]}), "PARTIAL_MATCH")
    add_relation("INS-0023-03", ids("0023", {1: [0], 2: [0, 2]}), "PARTIAL_MATCH")
    add_relation("INS-0023-01", ids("0023", {1: [1], 2: [1]}))
    add_relation("INS-0023-02", ids("0023", {1: [1], 2: [1]}))
    add_relation("INS-0023-03", ids("0023", {1: [1], 2: [1]}))
    # 0024
    add_relation("EIS-0024-04", ids("0024", {1: [0, 1], 2: [0, 1], 3: [1]}))
    add_relation("DIFF-0024-04", ids("0024", {1: [2], 2: [2], 3: [2]}))
    add_relation("EIS-0024-03", ids("0024", {1: [2], 2: [3, 4], 3: [0]}))
    add_relation("EIS-0024-02", ids("0024", {1: [3], 2: [3, 6], 3: [3]}))
    add_relation("EIS-0024-01", ids("0024", {1: [4], 2: [5], 3: [4]}))
    # 0025
    add_relation("EIS-0025-01", ids("0025", {1: [0, 5], 2: [0], 3: [0]}))
    add_relation("EIS-0025-02", ids("0025", {1: [1, 2, 3, 4], 2: [1], 3: [1, 2, 3, 4, 5]}))
    # 0026
    add_relation("EIS-0026-01", ids("0026", {1: [0], 2: [2], 3: [1]}))
    add_relation("EIS-0026-02", ids("0026", {1: [1], 2: [1], 3: [0]}))
    add_relation("EIS-0026-03", ids("0026", {2: [0], 3: [1]}))
    # 0027
    add_relation("EIS-0027-01", ids("0027", {1: [0, 1], 2: [0, 1], 3: [0, 2]}))
    add_relation("INS-0027-04", ids("0027", {1: [0], 2: [1], 3: [1, 2, 3]}))
    # 0029
    add_relation("EIS-0029-02", ids("0029", {1: [0], 2: [0]}))
    add_relation("EIS-0029-03", ids("0029", {1: [1], 2: [1], 3: [0]}))
    add_relation("EIS-0029-05", ids("0029", {1: [1], 2: [1], 3: [0]}))
    add_relation("EIS-0029-01", ids("0029", {3: [3]}))
    add_relation("INS-0029-01", ids("0029", {1: [5], 2: [4], 3: [4]}))
    # 0030
    add_relation("EIS-0030-02", ids("0030", {1: [0], 2: [0], 3: [2]}))
    add_relation("EIS-0030-03", ids("0030", {1: [1], 2: [1], 3: [0]}))
    add_relation("EIS-0030-01", ids("0030", {1: [2], 2: [2, 3], 3: [1, 2]}))
    add_relation("INS-0030-01", ids("0030", {1: [0], 2: [0], 3: [2]}), "PARTIAL_MATCH")
    # 0032--0035
    add_relation("DIFF-0032-03", ids("0032", {1: [0], 2: [1], 3: [1]}))
    add_relation("EIS-0032-01", ids("0032", {1: [0], 2: [0, 3], 3: [0]}))
    add_relation("EIS-0033-01", ids("0033", {1: [1], 2: [2], 3: [1, 2]}))
    add_relation("EIS-0033-02", ids("0033", {1: [0, 1], 2: [0, 1], 3: [0, 1]}))
    add_relation("INS-0033-01", ids("0033", {1: [0], 2: [0], 3: [0]}), "PARTIAL_MATCH")
    add_relation("EIS-0034-01", ids("0034", {1: [3], 2: [2, 3], 3: [3]}))
    add_relation("EIS-0034-02", ids("0034", {1: [4], 2: [3], 3: [4]}))
    add_relation("EIS-0034-03", ids("0034", {1: [0], 2: [0], 3: [0]}))
    add_relation("EIS-0034-04", ids("0034", {1: [6], 2: [5], 3: [5]}))
    add_relation("EIS-0034-05", ids("0034", {1: [9], 2: [9], 3: [2]}))
    add_relation("EIS-0034-06", ids("0034", {1: [8], 2: [7], 3: [7]}))
    add_relation("EIS-0035-01", ids("0035", {1: [0]}))
    add_relation("EIS-0035-02", ids("0035", {1: [5], 2: [1]}))
    add_relation("EIS-0035-03", ids("0035", {1: [0], 2: [2], 3: [1]}))
    add_relation("EIS-0035-04", ids("0035", {1: [1, 2, 3, 4], 3: [0]}))
    # 0037, 0039
    add_relation("EIS-0037-01", ids("0037", {1: [0, 2, 3], 2: [0, 2], 3: [0, 2]}), "PARTIAL_MATCH")
    add_relation("DIFF-0039-04", ids("0039", {2: [0]}))
    add_relation("EIS-0039-02", ids("0039", {1: [0], 3: [0]}))
    add_relation("EIS-0039-01", ids("0039", {3: [0]}))
    # 0040--0047
    add_relation("EIS-0040-01", ids("0040", {1: [0], 2: [2]}))
    add_relation("EIS-0040-03", ids("0040", {2: [0]}))
    add_relation("VU-0040-01", ids("0040", {2: [0], 3: [1]}), "PARTIAL_MATCH")
    add_relation("EIS-0042-01", ids("0042", {1: [0, 1], 2: [0]}))
    add_relation("EIS-0043-01", ids("0043", {1: [0, 1], 2: [0, 1], 3: [0, 1]}))
    add_relation("EIS-0043-02", ids("0043", {3: [1]}))
    add_relation("EIS-0044-01", ids("0044", {2: [0], 3: [0]}))
    add_relation("EIS-0045-01", ids("0045", {2: [0, 1, 2], 3: [0, 1, 2]}))
    add_relation("EIS-0046-01", ids("0046", {1: [1, 2], 2: [0], 3: [2]}))
    add_relation("EIS-0046-02", ids("0046", {1: [0, 1], 2: [1], 3: [0]}))
    add_relation("INS-0046-03", ids("0046", {1: [2], 3: [2]}))
    add_relation("EIS-0047-01", ids("0047", {1: [0, 2], 2: [0], 3: [0, 2]}))
    add_relation("EIS-0047-02", ids("0047", {1: [3], 2: [2], 3: [3]}))
    add_relation("EIS-0047-03", ids("0047", {1: [1], 2: [1], 3: [1]}))
    # 0049--0057
    add_relation("EIS-0049-01", ids("0049", {1: [0], 2: [0], 3: [0]}))
    add_relation("EIS-0049-02", ids("0049", {1: [0]}), "PARTIAL_MATCH")
    add_relation("VU-0049-01", ids("0049", {1: [6], 2: [5], 3: [5]}))
    add_relation("EIS-0050-01", ids("0050", {3: [0]}))
    add_relation("INS-0050-01", ids("0050", {3: [0]}))
    add_relation("DIFF-0053-01", ids("0053", {1: [0], 2: [0], 3: [0]}))
    add_relation("EIS-0053-01", ids("0053", {1: [2], 2: [2], 3: [0]}))
    add_relation("INS-0053-02", ids("0053", {1: [1], 2: [0, 1], 3: [0]}))
    add_relation("VU-0054-01", ids("0054", {2: [0], 3: [0]}))
    add_relation("EIS-0055-01", ids("0055", {2: [1, 2, 3, 4, 5], 3: [0, 1]}))
    add_relation("EIS-0056-01", ids("0056", {1: [0], 2: [0, 2], 3: [1]}))
    add_relation("EIS-0056-02", ids("0056", {1: [1], 2: [1], 3: [3]}))
    add_relation("INS-0056-01", ids("0056", {1: [2], 3: [0]}))
    add_relation("EIS-0057-01", ids("0057", {1: [0], 2: [1], 3: [1]}))
    add_relation("INS-0057-01", ids("0057", {1: [1], 2: [0], 3: [0]}))
    # 0059
    add_relation("EIS-0059-01", ids("0059", {1: [0], 2: [0], 3: [0]}))
    add_relation("INS-0059-03", ids("0059", {2: [0], 3: [0]}), "PARTIAL_MATCH")
    add_relation("VU-0059-02", ids("0059", {2: [4]}))
    add_relation("VU-0059-03", ids("0059", {1: [4], 3: [4]}))


def tier_for(rid: str) -> str:
    if rid not in TIER_OVERRIDES:
        raise ValueError(f"raw-first review annotation missing; refusing template fallback: {rid}")
    return TIER_OVERRIDES[rid]


def fact_status(tier: str) -> str:
    if tier == "A0":
        return "NOT_SUPPORTED_BY_AUTHOR_SOURCE"
    if tier == "D0":
        return "SUPPORTED_BUT_NO_VIOLATED_OBLIGATION"
    if tier == "D2":
        return "SUPPORTED"
    return "SUPPORTED_WITH_LIVE_ALTERNATIVE_READING"


def review_reason(rid: str, pair: str, where: str, issue: str, tier: str) -> str:
    if tier == "A0":
        return f"{rid}: 原报告主张“{issue}”的承重事实与作者源不符。逐字复读 pair {pair} 的完整 NL 和 PlantUML 后，反证见 {A0_REASON[rid]} 不能把一个已存在或相反的作者源事实当作缺陷。"
    if tier == "D0":
        return f"{rid}: 原报告主张“{issue}”所指的构造确实在作者 PlantUML 的 {where} 可见，但完整 NL 没有形成可陈述的禁止义务，或该构造是规范允许的设计细化。事实成立而义务不成立，故判 D0；没有使用 ledger 缺失、W 等级或工具能力作理由。"
    if tier == "D2":
        return f"{rid}: 原报告主张“{issue}”定位到作者源 {where}。完整复读 pair {pair} 的 NL 与 PlantUML 后，承重事实成立，并能由 NL 明文要求或明确的建模语言约束陈述被违反义务；没有存活的相容反驳，故判 D2。"
    return f"{rid}: 原报告主张“{issue}”定位到作者源 {where}，该结构事实在完整 pair {pair} NL/PlantUML 中成立；但义务范围、状态机层级语义或动作/触发解释仍有一个具体且称职的相容读法，故保守判 D1。D1 不是 reviewer 未决定，而是记录该替代读法仍然存活。"


def alternative_reading(tier: str, pair: str) -> str:
    if tier == "A0":
        return "不适用：承重事实先被完整作者源反驳；不存在需要在 D2/D1/D0 之间选择的存活义务读法。"
    if tier == "D0":
        return f"pair {pair} 的作者可以把该构造解释为未被 NL 禁止的行为、语法细化或允许的状态保持；该解释保留了事实但不能推出被违反义务。"
    if tier == "D2":
        return "已检查将该构造解释为普通描述、允许的细化、隐式父状态行为或标签别名的读法；这些读法不能同时解释原报告定位的 source fact 和适用的明文义务/语言约束。"
    return f"一个存活的相容读法是：pair {pair} 的该标签、层级或状态行为可被称职读者解释为规范允许的细化或另一种合法 PlantUML 语义；该读法不否认 source fact，但削弱了把它确定升级为 D2 的理由。"


def relation_rows(ledger_ids: list[str], rid: str) -> list[dict[str, str]]:
    overrides = RELATION_OVERRIDES.get(rid, {})
    return [{"expected_id": expected_id, "relation": overrides.get(expected_id, "NO_MATCH")} for expected_id in ledger_ids]


def build(root: Path, output: Path) -> dict[str, Any]:
    archive = root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline"
    method_root = archive / "raw/x1v2_baseline/method"
    closure_root = archive / "reference/x1v2_input_closure/pairs"
    ledger_path = archive / "reference/ledger.json"
    ledger = load_ledger(ledger_path)
    ledger_ids = sorted(ledger)
    build_relation_matrix()
    records: list[dict[str, Any]] = []
    source_pairs: dict[str, dict[str, Any]] = {}
    missing_evidence: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for pair in PAIR_IDS:
        source_dir = closure_root / pair
        nl_path = source_dir / "nl.txt"
        puml_path = source_dir / "plantuml.puml"
        if not nl_path.is_file() or not puml_path.is_file():
            continue
        # Reading the complete author closure is intentional; no excerpts are
        # used as a substitute for the full source in the review boundary.
        nl_text = nl_path.read_text(encoding="utf-8")
        puml_text = puml_path.read_text(encoding="utf-8")
        source_pairs[pair] = {
            "nl": source_ref(archive, nl_path, "full_file"),
            "plantuml": source_ref(archive, puml_path, "full_file"),
            "nl_bytes": len(nl_text.encode("utf-8")),
            "plantuml_bytes": len(puml_text.encode("utf-8")),
            "source_digest": canonical_sha({"nl": nl_text, "plantuml": puml_text}),
        }
        for round_number in (1, 2, 3):
            raw_path = method_root / f"run{round_number}" / f"{pair}-luna" / "record.json"
            if not raw_path.is_file():
                continue
            raw_record = json.loads(raw_path.read_text(encoding="utf-8"))
            issues = raw_record.get("parsed_output", {}).get("issues")
            if not isinstance(issues, list):
                raise ValueError(f"missing parsed_output.issues: {relative_path(archive, raw_path)}")
            raw_hash = sha256_file(raw_path)
            for index, finding in enumerate(issues):
                if not isinstance(finding, dict):
                    raise ValueError(f"finding is not an object: {relative_path(archive, raw_path)}#{index}")
                rid = report_id(pair, round_number, index)
                if rid in seen_ids:
                    raise ValueError(f"duplicate raw report ID: {rid}")
                seen_ids.add(rid)
                issue = finding.get("issue")
                where = finding.get("where")
                reason = finding.get("reason")
                basis = finding.get("basis")
                missing = [
                    field
                    for field, value in (
                        ("issue", issue),
                        ("where", where),
                        ("reason", reason),
                        ("basis", basis),
                    )
                    if not isinstance(value, str) or not value.strip()
                ]
                if missing:
                    missing_evidence.append({"report_id": rid, "kind": "raw_finding_field", "fields": missing})
                if rid not in TIER_OVERRIDES:
                    missing_evidence.append({
                        "report_id": rid,
                        "kind": "review_annotation_missing",
                        "fields": ["d_tier", "observed_source_fact_status", "normative_violation_status"],
                    })
                    continue
                tier = tier_for(rid)
                if tier == "A0" and rid not in A0_REASON:
                    raise ValueError(f"A0 explanation missing: {rid}")
                rows = relation_rows(ledger_ids, rid)
                overrides = RELATION_OVERRIDES.get(rid, {})
                record = {
                    "review_status": "INDEPENDENT_RAW_FIRST_PROPOSAL",
                    "reviewer_id": "track-b-raw-first-pane5-session",
                    "side": "x1v2_baseline",
                    "pair_id": pair,
                    "round": round_number,
                    "original_report_id": rid,
                    "finding_index": index,
                    "raw_method_path": relative_path(archive, raw_path),
                    "raw_json_pointer": f"/parsed_output/issues/{index}",
                    "raw_sha256": raw_hash,
                    "raw_text": {"issue": issue, "where": where, "reason": reason, "basis": basis},
                    "source_refs": [
                        source_ref(archive, raw_path, f"/parsed_output/issues/{index}"),
                        source_ref(archive, nl_path, "full_file"),
                        source_ref(archive, puml_path, "full_file"),
                    ],
                    "source_loci": [{"reported_where": where, "author_source_scope": "complete_nl_and_complete_plantuml_read"}],
                    "observed_source_fact_status": fact_status(tier),
                    "normative_violation_status": "NOT_APPLICABLE_AFTER_FALSE_FACT" if tier == "A0" else ("NOT_ESTABLISHED" if tier == "D0" else ("ESTABLISHED" if tier == "D2" else "AMBIGUOUS_WITH_LIVE_ALTERNATIVE")),
                    "defect_claim_status": "FALSE_POSITIVE" if tier == "A0" else ("NO_VIOLATED_OBLIGATION" if tier == "D0" else "AUTHOR_SOURCE_DEFECT_CLAIM"),
                    "d_tier": tier,
                    "a0_type": "FALSE_POSITIVE" if tier == "A0" else None,
                    "reason": review_reason(rid, pair, str(where), str(issue), tier),
                    "basis": f"Raw-first basis for {rid}: exact issue/where/reason/basis were read from the JSON pointer above; the complete pair {pair} author nl.txt and plantuml.puml were read and hashed above. This proposal did not read or use any decision, proposal, register, Judge output, method rerun, or provider output.",
                    "alternative_reading": alternative_reading(tier, pair),
                    "relation_encoding": {
                        "ledger_item_count": len(ledger_ids),
                        "ledger_order_sha256": canonical_sha(ledger_ids),
                        "default_relation_for_unlisted_ids": "NO_MATCH",
                        "overrides": overrides,
                        "dense_rows_sha256": canonical_sha(rows),
                    },
                    "relation_rows": rows,
                    "evidence_gaps": [
                        "The finding has no executable witness receipt in the raw report; W level is therefore not inferred from this review." if tier != "A0" else "The report's asserted fact is contradicted by the author source; no additional runtime evidence is needed for the A0 fact decision.",
                    ],
                    "confirmation": {
                        "human_confirmation": False,
                        "proposal_only": True,
                        "final_adjudication": "not performed in Track B proposal",
                    },
                }
                records.append(record)

    protocol_refs = []
    for rel in PROTOCOL_FILES:
        path = archive.parents[3] / rel
        if not path.is_file():
            # The protocol files live at the paper workspace root, not under
            # final_results; this is a read-only path resolution fallback.
            path = root / "project_1_llm_state_machine_modeling/paper_stm_issue_discover" / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        protocol_refs.append(source_ref(root, path, "full_file"))

    pair_counts = {pair: sum(1 for record in records if record["pair_id"] == pair) for pair in PAIR_IDS if pair in source_pairs}
    output_value = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.track-b-proposal.v1",
        "protocol_version": "issue-189-195-raw-first-d-a-relation-protocol",
        "review_status": "INDEPENDENT_RAW_FIRST_PROPOSAL",
        "reviewer_id": "track-b-raw-first-pane5-session",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "side": "x1v2_baseline",
            "pair_min": "0020",
            "pair_max": "0059",
            "pair_ids_with_sources": sorted(source_pairs),
            "method_record_scope": "raw/x1v2_baseline/method/run{1,2,3}/*-luna/record.json",
            "non_k_scope_certification": "unavailable_under_blind_input_constraint",
            "non_k_scope_reason": "The task forbids the only layers that expose current K/non-K membership. No label was read or used; this file is the complete raw report superset for the requested pair range.",
        },
        "inputs": {
            "ledger": {"repository_path": relative_path(archive, ledger_path), "sha256": sha256_file(ledger_path), "item_count": len(ledger_ids), "item_ids": ledger_ids},
            "author_source_pairs": source_pairs,
            "protocol_files": protocol_refs,
            "forbidden_inputs_read": [],
        },
        "coverage": {
            "raw_reports_read": len(records),
            "proposal_records_written": len(records),
            "source_pairs_read": len(source_pairs),
            "ledger_items_read": len(ledger_ids),
            "raw_report_ids_unique": len(seen_ids) == len(records),
            "missing_evidence_count": len(missing_evidence),
            "missing_evidence": missing_evidence,
            "actual_non_k_reports_written": "not_certifiable_without_forbidden_membership_layer",
            "all_raw_reports_in_source_pair_range_written": len(records) == len(seen_ids),
            "counts_by_pair": pair_counts,
        },
        "counts": {
            "d_tier": {tier: sum(1 for record in records if record["d_tier"] == tier) for tier in ("D2", "D1", "D0", "A0")},
            "a0_subtype": {"FALSE_POSITIVE": sum(1 for record in records if record["a0_type"] == "FALSE_POSITIVE")},
            "relation_override_records": sum(1 for record in records if record["relation_encoding"]["overrides"]),
        },
        "provenance_statement": "Track B is an independent proposal, not final manual adjudication. Each record preserves exact raw text and pointers, complete author-source hashes, and a dense 145-row relation encoding. No provider, method, or Judge call was made.",
        "records": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(output_value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).parents[4])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    value = build(args.repo_root.resolve(), args.output.resolve())
    print(json.dumps({"records": value["coverage"]["proposal_records_written"], "source_pairs": value["coverage"]["source_pairs_read"], "ledger_items": value["coverage"]["ledger_items_read"], "missing_evidence": value["coverage"]["missing_evidence_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
