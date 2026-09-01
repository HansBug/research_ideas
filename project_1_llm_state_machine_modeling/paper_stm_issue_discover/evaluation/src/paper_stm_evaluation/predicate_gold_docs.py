"""Generate and validate the publication-facing predicate-gold v1 documents.

The canonical JSON remains the fact source.  This module renders every count,
cross-tabulation, unsupported row, and expected-vs-actual statement from saved
provider-free JSON inputs so prose cannot silently become a second dataset.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .predicate_gold import (
    GoldStatus,
    PredicateGoldAnnotation,
    PredicateGoldDataset,
    sha256_path,
)
from .predicate_gold_release import PredicateGoldSummary

UNSUPPORTED_SCHEMA_VERSION = "paper1.predicate-gold.unsupported-exact.v1"
DOC_FILENAMES = (
    "README.md",
    "predicate_gold_report_cn.md",
    "unsupported_exact.json",
    "unsupported_exact.tsv",
    "unsupported_exact.md",
    "CHANGELOG.md",
)


@dataclass(frozen=True)
class PublicationInputs:
    """Validated immutable inputs used by the publication renderer."""

    dataset: PredicateGoldDataset
    summary: PredicateGoldSummary
    expected_actual: dict[str, Any]
    canonical_path: Path
    summary_path: Path
    expected_actual_path: Path


def _percent(numerator: int, denominator: int) -> str:
    """Format one count ratio without hiding either operand."""

    if denominator == 0:
        return "N/A"
    return f"{numerator}/{denominator} = {100 * numerator / denominator:.2f}%"


def _md(value: object) -> str:
    """Escape one compact Markdown-table value while preserving semantics."""

    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _cross_tab(
    rows: Iterable[Any],
    *,
    row_dimension: str,
    column_dimension: str,
    row_values: tuple[str, ...],
    column_values: tuple[str, ...],
) -> str:
    """Render one closed summary cross-tabulation as Markdown."""

    counts = {
        (
            row.dimensions[row_dimension],
            row.dimensions[column_dimension],
        ): row.count
        for row in rows
    }
    lines = [
        "| " + row_dimension + " | " + " | ".join(column_values) + " | total |",
        "| --- | " + " | ".join("---:" for _ in column_values) + " | ---: |",
    ]
    for row_value in row_values:
        values = [counts.get((row_value, column_value), 0) for column_value in column_values]
        lines.append(
            f"| `{row_value}` | "
            + " | ".join(str(value) for value in values)
            + f" | {sum(values)} |"
        )
    return "\n".join(lines)


def _selected_property(annotation: PredicateGoldAnnotation) -> Any:
    """Return the selected exact property or nearest executed sound proxy."""

    return annotation.gold_property or annotation.proxy_property


def _unsupported_payload(inputs: PublicationInputs) -> dict[str, Any]:
    """Derive the complete unsupported catalog from canonical annotations."""

    rows: list[dict[str, Any]] = []
    for annotation in sorted(inputs.dataset.items.values(), key=lambda item: item.ledger_id):
        if annotation.gold_status != GoldStatus.UNSUPPORTED_EXACT:
            continue
        proxy = annotation.proxy_property
        rows.append(
            {
                "ledger_id": annotation.ledger_id,
                "pair_id": annotation.pair_id,
                "family": annotation.family,
                "d_tier": annotation.d_tier,
                "l_tier": annotation.l_tier,
                "exactness_relation": annotation.exactness_relation.value,
                "nearest_proxy_property_id": proxy.property_id if proxy is not None else None,
                "nearest_proxy_predicate_ids": list(proxy.predicate_ids) if proxy is not None else [],
                "nearest_proxy_expression": proxy.expression if proxy is not None else None,
                "unsupported_reason": annotation.unsupported_reason,
                "capability_gap": list(annotation.capability_gap),
                "reason": annotation.reason,
                "arbitration_id": annotation.arbitration.arbitration_id,
                "reviewer_ids": list(annotation.reviewer_ids),
            }
        )
    return {
        "schema_version": UNSUPPORTED_SCHEMA_VERSION,
        "canonical_path": inputs.canonical_path.name,
        "canonical_sha256": sha256_path(inputs.canonical_path),
        "total": len(rows),
        "items": rows,
    }


def _unsupported_tsv(payload: dict[str, Any]) -> str:
    """Render the unsupported catalog as a deterministic flat TSV mirror."""

    columns = (
        "ledger_id",
        "pair_id",
        "family",
        "d_tier",
        "l_tier",
        "exactness_relation",
        "nearest_proxy_property_id",
        "nearest_proxy_predicate_ids",
        "unsupported_reason",
        "capability_gap",
        "arbitration_id",
    )
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for row in payload["items"]:
        flat = dict(row)
        flat["nearest_proxy_predicate_ids"] = "|".join(row["nearest_proxy_predicate_ids"])
        flat["capability_gap"] = "|".join(row["capability_gap"])
        writer.writerow({column: flat.get(column) for column in columns})
    return output.getvalue()


def _render_readme(inputs: PublicationInputs) -> str:
    """Render the stable navigation entry for predicate gold v1."""

    summary = inputs.summary
    exact = summary.status_counts[GoldStatus.EXACT_FALSE.value] + summary.status_counts[
        GoldStatus.COMPOSITE_EXACT_FALSE.value
    ]
    return f"""# Predicate gold v1

本目录是当前 145 条 `ledger_v2` issue 的 evaluation-only expected-predicate gold。唯一
canonical 事实源是 [`predicate_gold_v1.json`](predicate_gold_v1.json)；表格、报告和
unsupported 清单均由 provider-free 生成器从该 JSON 机械导出。

当前裁决为：精准可执行 {exact}/145，其中 `EXACT_FALSE={summary.status_counts[GoldStatus.EXACT_FALSE.value]}`、
`COMPOSITE_EXACT_FALSE={summary.status_counts[GoldStatus.COMPOSITE_EXACT_FALSE.value]}`；
`SOUND_FALSE_PROXY={summary.status_counts[GoldStatus.SOUND_FALSE_PROXY.value]}`；
`UNSUPPORTED_EXACT={summary.status_counts[GoldStatus.UNSUPPORTED_EXACT.value]}`；
`BLOCKED_EXECUTION={summary.status_counts[GoldStatus.BLOCKED_EXECUTION.value]}`。精准与 proxy
执行共 {summary.completed_false_count} 条，坏制品 `false`、positive control `true`、replay match
均为 {summary.completed_false_count}/{summary.completed_false_count}。

## 当前入口

- [中文审计报告](predicate_gold_report_cn.md)
- [canonical JSON](predicate_gold_v1.json) / [JSON Schema](predicate_gold_v1.schema.json) / [TSV 镜像](predicate_gold_v1.tsv)
- [状态与交叉分布](summary.json)
- [98 条 unsupported 清单](unsupported_exact.md) / [JSON](unsupported_exact.json) / [TSV](unsupported_exact.tsv)
- [冻结 v60 expected-vs-actual 离线分析](expected_vs_actual_v60.json) / [TSV](expected_vs_actual_v60.tsv)
- [精准性协议](predicate_gold_protocol.md) / [标注指南](annotation_guide.md)
- [19 谓词能力审计](predicate_semantics_capability_audit.md) / [JSON](predicate_semantics_capability_audit.json)
- [claim-to-source matrix](academic_claim_to_source_matrix.json) / [学术横向复核](review/horizontal/academic_review_v2.md)
- [当前 review 选择](review/active_review_manifest.json) / [发布 manifest](manifest.json)
- [变更说明](CHANGELOG.md)

## 边界

这里的 `exact` 指在声明的 FCSTM 语义、scope 和环境假设下，项目逐条确认
`O <=> P`，并不表示存在统一的 `S < G < R < V` 精准度排序。`O => P` 只计
sound falsifier/proxy；`P => O` 和无可证明蕴含不计 exact。

旧 registry 的 `118/145 = 81.4%` 是冻结的
`planned_mapping_not_new_method_measurement` 设计期汇总，不是逐条执行验证过的 gold coverage。
旧 126 条 `provenance/expected_issue_set.json` 只保留作来源证据，不能替代当前 145 条台账或本 overlay。

gold 不改变 hit、W、K/N/I，也不要求 method 复现同一个 predicate ID。它没有进入 method
registry、prompt、routing 或 package data。本次没有运行 method、Judge、provider、15x1 或 54x3。
"""


def _render_report(inputs: PublicationInputs) -> str:
    """Render the human-readable Chinese audit report from structured views."""

    summary = inputs.summary
    expected_actual = inputs.expected_actual
    statuses = (
        GoldStatus.EXACT_FALSE.value,
        GoldStatus.COMPOSITE_EXACT_FALSE.value,
        GoldStatus.SOUND_FALSE_PROXY.value,
        GoldStatus.UNSUPPORTED_EXACT.value,
    )
    exact = summary.status_counts[GoldStatus.EXACT_FALSE.value] + summary.status_counts[
        GoldStatus.COMPOSITE_EXACT_FALSE.value
    ]
    status_rows = "\n".join(
        f"| `{status}` | {summary.status_counts[status]} | {_percent(summary.status_counts[status], summary.total)} |"
        for status in (*statuses, GoldStatus.BLOCKED_EXECUTION.value)
    )
    family_table = _cross_tab(
        summary.status_by_family,
        row_dimension="family",
        column_dimension="gold_status",
        row_values=("EIS", "INS", "VU", "DIFF"),
        column_values=statuses,
    )
    d_table = _cross_tab(
        summary.status_by_d_tier,
        row_dimension="d_tier",
        column_dimension="gold_status",
        row_values=("D2", "D1"),
        column_values=statuses,
    )
    l_table = _cross_tab(
        summary.status_by_l_tier,
        row_dimension="l_tier",
        column_dimension="gold_status",
        row_values=("L2", "L1", "L0"),
        column_values=statuses,
    )
    predicate_rows = "\n".join(
        f"| `{row.predicate_id}` | {row.selected_exact_count} | {row.selected_proxy_count} | {row.unsupported_count} |"
        for row in summary.predicate_usage
    )
    classification_rows = "\n".join(
        f"| `{name}` | {count} |"
        for name, count in sorted(expected_actual["classification_counts"].items())
    )
    return f"""# 145 条台账 expected-predicate gold 审计报告

## 结论和发布边界

本轮对当前 `ledger_v2` 的 145 条 issue 逐条恢复规范义务 `O`，比较可执行性质 `P`，
并在执行前冻结 proposal 和 typed inputs。最终只有 {exact}/145（{100 * exact / summary.total:.2f}%）
满足 `O <=> P` 且通过坏制品 `false`、positive control `true` 和 replay match。另有
{summary.status_counts[GoldStatus.SOUND_FALSE_PROXY.value]} 条只有 `O => P` 的可靠证伪 proxy；
{summary.status_counts[GoldStatus.UNSUPPORTED_EXACT.value]} 条在现有 19 谓词、可审计组合性质和
pyfcstm-native evaluation-only oracle 下仍无法精准表达。`BLOCKED_EXECUTION=0`。

这组结果没有重跑或修改冻结 v60 method、Judge、15x1、54x3、raw、current/baseline canonical
decisions 或 19-predicate runtime。gold 只用于台账说明、离线 evaluation 和人工审计。

## 状态分布

| disposition | count | share of 145 |
| --- | ---: | ---: |
{status_rows}

`EXACT_FALSE` 与 `COMPOSITE_EXACT_FALSE` 合计 {exact} 条，是 exact executable coverage 的分子。
`SOUND_FALSE_PROXY` 和 `UNSUPPORTED_EXACT` 均不进入该分子。

### Family

{family_table}

### D tier

{d_table}

### L tier

{l_table}

## 执行和复核闭合

| check | result |
| --- | ---: |
| completed Boolean `false` | {summary.completed_false_count}/{summary.completed_false_count} |
| completed positive-control `true` | {summary.completed_true_control_count}/{summary.completed_false_count} |
| replay match | {summary.replay_match_count}/{summary.completed_false_count} |
| Track A obligation review | {summary.track_a_coverage}/145 |
| Track B property/input review | {summary.track_b_coverage}/145 |
| Track C execution/semantic review | {summary.track_c_coverage}/145 |
| independent fourth review | {summary.high_risk_coverage}/145 |
| rows retaining disclosed conflicts | {summary.conflict_rows}/145 |
| retained conflict records | {summary.conflict_count} |
| `BLOCKED_EXECUTION` | {summary.blocked_execution_count} |

Track A/B/C 和 fourth review 是内部、hash-bound 的质量复核，不是正式人类 inter-rater study。
Pane5 依据作者 source、正式语义、query、receipt 和并列意见仲裁；多数票和 confidence 都不是
裁决规则。当前选择见 [`review/active_review_manifest.json`](review/active_review_manifest.json)。

早期 31 条 portable Track C packet 绑定历史协议 hash `3762ebf1...`，而同一路径当前保存的冻结
协议 hash 为 `6d91c5d8...`。历史字节已精确恢复并嵌入
[`review/evidence_corrections/protocol_hash_drift_resolution.json`](review/evidence_corrections/protocol_hash_drift_resolution.json)；
current-protocol fourth review 与 pane5 仲裁重新关闭了语义权限。历史 packet 的同路径 hash 不一致仍
作为 provenance limitation 保留，没有重写旧 packet，也没有把两版协议说成相同字节。

## 现有谓词和 evaluation-only 使用

下表是多标签 usage：一个 composite 可以同时使用多个 predicate，因此 exact 列不能横向求和后
当作 issue 数。`EVALUATION_ONLY` 是隔离在 evaluation package 内的 pyfcstm-native oracle，未加入
method registry。

| predicate/bucket | selected exact | selected proxy | unsupported bucket |
| --- | ---: | ---: | ---: |
{predicate_rows}

exact issue 中有 {summary.evaluation_only_exact_count} 条使用 evaluation-only oracle。能力边界和
registry/backend 不一致见 [`predicate_semantics_capability_audit.md`](predicate_semantics_capability_audit.md)：
S2 只检查 direct authored carrier，G1 是 guard-agnostic macro topology；R1 的 registry `step`
不能独立选择 runtime observation；S6 runtime 只接受一个 effect；V1 还需要 registry 未声明的完整
guard multiset。gold protocol 将这些差异限制在 evaluation 层，冻结 runtime 保持不变。

## Unsupported

`UNSUPPORTED_EXACT={summary.status_counts[GoldStatus.UNSUPPORTED_EXACT.value]}` 不表示 issue 无效，也不表示
method 无法命中。它只说明目前没有 source-backed、obligation-equivalent、可执行且可重放的参考性质。
逐条 ID、capability gap、nearest proxy 和 arbitration 见
[`unsupported_exact.md`](unsupported_exact.md)；机器可读版本是
[`unsupported_exact.json`](unsupported_exact.json)。

主要限制来自 source 未给出完整 domain/bound/schedule/initial scope、义务量词或 timing 超出冻结
wrapper、whole-model termination/并发/RTC 语义无法从转换制品获得等价 attribution，以及 direct
carrier/topology/static slot 只能表达更强或更弱的邻近条件。没有为了减少 unsupported 数量而补造
变量、状态、事件、domain 或 bound。

## 冻结 v60 expected-vs-actual 离线分析

该分析只解释 method 的成分，不改写 FULL/PARTIAL hit、W 或 K/N/I。冻结 v60 对 145 个 issue 的
FULL hit 为 {expected_actual['full_hit_issues']}/145，FULL 或 PARTIAL supported 为
{expected_actual['supported_issues']}/145。98 个 unsupported gold 中仍有
{expected_actual['classification_counts']['UNSUPPORTED_GOLD_BUT_FULL_HIT']} 个 FULL hit。因此，
unsupported 不能自动解释成 method miss。

| diagnostic classification | issues |
| --- | ---: |
{classification_rows}

其中 `EXPECTED_ID_INPUT_NOT_OBSERVABLE={expected_actual['classification_counts']['EXPECTED_ID_INPUT_NOT_OBSERVABLE']}`；
冻结 raw 无法可靠恢复输入时，矩阵明确保留不可观察状态，没有猜值，也没有重跑 54x3。完整多标签
矩阵见 [`expected_vs_actual_v60.json`](expected_vs_actual_v60.json)。

## 学术依据和项目 operationalization

[`predicate_gold_protocol.md`](predicate_gold_protocol.md) 与
[`academic_claim_to_source_matrix.json`](academic_claim_to_source_matrix.json) 记录了 12 条经核验的
primary/formal source claim，覆盖 requirements pattern、FRET 字段化、oracle implication、vacuity、
有限测试边界、UML initial/RTC/completion、refinement、trace semantics、bounded model checking 和
spurious counterexample。独立学术复核结论为 `PASS_WITH_LIMITATIONS`，见
[`review/horizontal/academic_review_v2.md`](review/horizontal/academic_review_v2.md)。

`obligation-equivalent executable reference property`、四种 implication label、三 Track + pane5、
五种 disposition 和 positive-control/replay 合同是本项目综合文献形成的 operationalization。
文献不保证这套流程恢复 ground truth，也没有提出统一的“most precise predicate” family 排序；本项目
未声称测量了该 operationalization 的独立有效性。

## 复算和文件

| role | path |
| --- | --- |
| canonical annotations | [`predicate_gold_v1.json`](predicate_gold_v1.json) |
| schema / flat mirror | [`predicate_gold_v1.schema.json`](predicate_gold_v1.schema.json), [`predicate_gold_v1.tsv`](predicate_gold_v1.tsv) |
| mechanical summary | [`summary.json`](summary.json) |
| input inventory | [`inventory.json`](inventory.json) |
| receipts / controls | [`receipts/`](receipts/), [`controls/`](controls/) |
| reviews / arbitration | [`review/`](review/) |
| release manifest | [`manifest.json`](manifest.json) |

Provider-free validation and replay use the evaluation package only. The release manifest binds all selected
inputs, code, receipts, controls, reviews and derived views by repository-relative path and SHA-256.
"""


def _render_unsupported(inputs: PublicationInputs, payload: dict[str, Any]) -> str:
    """Render every unsupported row without collapsing issue-specific gaps."""

    summary = inputs.summary
    lines = [
        "# Unsupported exact properties",
        "",
        f"本清单由 `predicate_gold_v1.json` 机械生成，共 {payload['total']} 条。这里的 unsupported",
        "只表示当前可信语义能力不能给出 `O <=> P` 的可执行 reference property；它不否定",
        "ledger issue，也不把 method 的 FULL/PARTIAL hit 改成 miss。",
        "",
        "汇总分布：",
        "",
    ]
    unsupported_status = GoldStatus.UNSUPPORTED_EXACT.value
    for title, rows, dimension, values in (
        ("family", summary.status_by_family, "family", ("EIS", "INS", "VU", "DIFF")),
        ("D tier", summary.status_by_d_tier, "d_tier", ("D2", "D1")),
        ("L tier", summary.status_by_l_tier, "l_tier", ("L2", "L1", "L0")),
    ):
        counts = {
            row.dimensions[dimension]: row.count
            for row in rows
            if row.dimensions["gold_status"] == unsupported_status
        }
        lines.append(f"- {title}: " + ", ".join(f"`{value}={counts.get(value, 0)}`" for value in values))
    lines.extend(
        [
            "",
            "机器可读字段见 [`unsupported_exact.json`](unsupported_exact.json)；平面镜像见",
            "[`unsupported_exact.tsv`](unsupported_exact.tsv)。",
            "",
        ]
    )
    for row in payload["items"]:
        proxy_ids = row["nearest_proxy_predicate_ids"]
        proxy = "无可靠 executable proxy"
        if row["nearest_proxy_property_id"] is not None:
            predicate_text = ", ".join(f"`{item}`" for item in proxy_ids) or "evaluation-only"
            proxy = f"`{row['nearest_proxy_property_id']}` ({predicate_text})"
        lines.extend(
            [
                f"## `{row['ledger_id']}`",
                "",
                f"- 分类：`{row['family']}` / `{row['d_tier']}` / `{row['l_tier']}`；final relation `{row['exactness_relation']}`",
                f"- 最近 proxy：{proxy}",
                f"- unsupported reason：{_md(row['unsupported_reason'])}",
                "- capability gap：",
                "",
            ]
        )
        lines.extend(f"  - {_md(gap)}" for gap in row["capability_gap"])
        lines.extend(
            [
                "",
                f"- arbitration：`{row['arbitration_id']}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_changelog(inputs: PublicationInputs) -> str:
    """Render a concise version and supersession history."""

    summary = inputs.summary
    exact = summary.status_counts[GoldStatus.EXACT_FALSE.value] + summary.status_counts[
        GoldStatus.COMPOSITE_EXACT_FALSE.value
    ]
    return f"""# Changelog

## predicate gold v1

- 为当前 145 条 `ledger_v2` issue 新增 method-independent canonical overlay、完整 JSON Schema 和 TSV 镜像。
- 最终状态为 exact {exact}、sound false proxy {summary.status_counts[GoldStatus.SOUND_FALSE_PROXY.value]}、
  unsupported exact {summary.status_counts[GoldStatus.UNSUPPORTED_EXACT.value]}、blocked execution 0。
- 为 {summary.completed_false_count} 条 executable exact/proxy 保存坏制品 `false`、positive-control `true`
  和 matching replay；composite 不 short-circuit。
- 每条保存 Track A/B/C、independent fourth review、pane5 arbitration、source/hash/reason/basis 和 typed-input provenance。
- 增加 19-predicate registry/backend/pyfcstm capability audit、primary-source claim matrix 和冻结 v60 expected-vs-actual 离线分析。
- 增加静态防泄漏测试；evaluation-only oracle 未进入 method registry、prompt、routing 或 package data。

## 被取代的口径

- registry 的 `118/145 = 81.4%` 继续保留为历史设计期
  `planned_mapping_not_new_method_measurement`，不能解释为已执行的 exact gold coverage。
- `provenance/expected_issue_set.json` 的旧 126 条记录继续保留作 provenance，不是当前台账，也没有被机械迁移成 gold。
- v60 method/Judge/current-baseline canonical 结果均保持冻结；本版本没有 method、Judge、provider、15x1 或 54x3 rerun。
"""


def build_bundle(inputs: PublicationInputs) -> dict[str, bytes]:
    """Build all deterministic publication files as exact UTF-8 bytes."""

    unsupported = _unsupported_payload(inputs)
    unsupported_json = json.dumps(unsupported, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    text_files = {
        "README.md": _render_readme(inputs),
        "predicate_gold_report_cn.md": _render_report(inputs),
        "unsupported_exact.json": unsupported_json,
        "unsupported_exact.tsv": _unsupported_tsv(unsupported),
        "unsupported_exact.md": _render_unsupported(inputs, unsupported),
        "CHANGELOG.md": _render_changelog(inputs),
    }
    return {name: text.encode("utf-8") for name, text in text_files.items()}


def load_inputs(*, canonical: Path, summary: Path, expected_actual: Path) -> PublicationInputs:
    """Load and cross-bind canonical, summary, and frozen analysis inputs."""

    dataset = PredicateGoldDataset.model_validate_json(canonical.read_text(encoding="utf-8"))
    summary_model = PredicateGoldSummary.model_validate_json(summary.read_text(encoding="utf-8"))
    if summary_model.total != len(dataset.items) or summary_model.canonical_sha256 != sha256_path(canonical):
        raise ValueError("summary does not bind the supplied canonical dataset")
    expected = json.loads(expected_actual.read_text(encoding="utf-8"))
    if expected.get("total_ledger_issues") != len(dataset.items):
        raise ValueError("expected-vs-actual denominator does not match canonical dataset")
    if expected.get("canonical_sha256") != sha256_path(canonical):
        raise ValueError("expected-vs-actual analysis does not bind canonical bytes")
    return PublicationInputs(
        dataset=dataset,
        summary=summary_model,
        expected_actual=expected,
        canonical_path=canonical,
        summary_path=summary,
        expected_actual_path=expected_actual,
    )


def write_bundle(inputs: PublicationInputs, output_root: Path) -> None:
    """Write all publication views generated from structured inputs."""

    output_root.mkdir(parents=True, exist_ok=True)
    for name, content in build_bundle(inputs).items():
        (output_root / name).write_bytes(content)


def validate_bundle(inputs: PublicationInputs, output_root: Path) -> None:
    """Require every saved publication view to match generated bytes exactly."""

    expected = build_bundle(inputs)
    for name in DOC_FILENAMES:
        path = output_root / name
        if not path.is_file():
            raise ValueError(f"missing generated predicate-gold document: {name}")
        if path.read_bytes() != expected[name]:
            raise ValueError(f"generated predicate-gold document drift: {name}")


def main() -> int:
    """Generate or byte-validate predicate-gold publication views."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "validate"))
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--expected-actual", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    inputs = load_inputs(
        canonical=args.canonical,
        summary=args.summary,
        expected_actual=args.expected_actual,
    )
    if args.command == "generate":
        write_bundle(inputs, args.output_root)
    else:
        validate_bundle(inputs, args.output_root)
    print(
        json.dumps(
            {
                "result": "PASS",
                "command": args.command,
                "files": list(DOC_FILENAMES),
                "total": inputs.summary.total,
                "status_counts": inputs.summary.status_counts,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
