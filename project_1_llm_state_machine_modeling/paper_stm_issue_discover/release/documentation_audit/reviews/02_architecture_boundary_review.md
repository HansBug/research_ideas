# 架构与边界独立审查

审查范围：current method runner/workflow、Judge schema、evaluation 入口、release import boundary、resources，以及 package 和 pipeline 文档。

## 复核方法

```bash
rg -n 'stage_name=' method/src/paper_stm_method/orchestration/runner.py
nl -ba method/src/paper_stm_method/evidence/witness_levels.py | sed -n '1,80p'
nl -ba judge/src/paper_stm_judge/schema.py | sed -n '1434,1565p'
nl -ba scripts/release/validate_release_structure.py | sed -n '142,163p'
find scripts -type f -name '*.py' -printf '%P\n' | sort
```

| 严重度 | Finding | Evidence | 处理 |
| --- | --- | --- | --- |
| High | `pipeline/evidence_discovery/README.md` 把兼容 namespace 写成当前 method 唯一入口。 | `method/src/paper_stm_method/` 是权威实现，pipeline README 已声明 compatibility。 | pending: 改为 compatibility/provenance 导航，默认链接 `method/` 与 `evaluation/`。 |
| High | `pipeline/representation/README.md` 把自己写成 current discover 路径且链接失效 `pipeline/feedback_loop`；`pipeline/conversion/README.md` 同样指向旧 loop。 | pipeline 子 README 与 archive/legacy 路径。 | pending: 改为冻结输入 preparation/provenance，显式链接 `method/` 与 `archive/legacy/feedback_loop/`。 |
| Medium | `judge/README.md` 把 validity 第一阶段误写为直接产出 `VALID_KNOWN`、`VALID_NOVEL`、`INVALID`。 | 第一阶段产出 `FrozenValidityCertificate.core_truth`；relation 在冻结 valid certificate 后执行，backend 再 materialize 最终 validity。 | pending: 按实际两阶段与 materialization 顺序改写。 |
| Medium | `pipeline/evaluation/README.md` 与 `story/blueprint_proposal.md` 仍把旧路径作为当前评测或谓词来源。 | v0 schema 目录、`method/` stable resources、protocol docs。 | pending: 前者降级为 historical v0 schema，后者指向 `method/` 和冻结 protocol。 |

顶层 README、GUIDE、method/evaluation README、scripts README、当前 story 的输入闭包、W/D/L、谓词非准入门、W2 条件、D1/D2 publication 与 no-leakage 描述均与代码一致。审查为只读；provider 调用与 billable 调用均为 0。

结论：修复表中 4 项后可作 targeted rereview。

## 2026-08-28 第一次定向复审

首轮修复后，reviewer 继续检查兼容 README，发现两项中严重度残留：`pipeline/evidence_discovery/README.md` 仍展开 current method 运行规则；`pipeline/representation/README.md` 仍把冻结表示目录写成 discover runner，并把 current evaluation 归给 `discover_matrix`。这两项均不涉及生产代码或冻结制品。

处理：前者收缩为 compatibility 导航，只链接 method、Judge、evaluation 与 final_results；后者明确为冻结输入/provenance，删除 runner/evaluation 所有权表述，并把 current evaluation 指向 `evaluation/` 和 final archive。

## 2026-08-28 第二次定向复审

reviewer 直接复核上述两个 README 与 current package 边界：`pipeline.evidence_discovery` 已明确排除 current method 权威性，`pipeline.representation` 已明确排除 runner/evaluation 所有权；历史 `Discover/Repair/Confirm` 段落保留为历史路线，不再构成默认入口。

结论：通过。无剩余高/中严重度 finding；未修改文件，provider 与 billable 调用均为 0。
