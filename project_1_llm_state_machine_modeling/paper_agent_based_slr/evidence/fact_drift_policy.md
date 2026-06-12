# Fact Drift Policy：PR #97 与证据层级

## 1. 目的

第二篇 agent-based SLR 论文会复用 `sources/`、PR #97、issue #85、PR #101、导师讨论记录等多层证据。不同证据的当前性和可靠性不同。本文档规定 A0 后续所有文档和 PR 如何引用这些事实，避免把未合入资产写成 `main` fact。

## 2. 证据层级

| Tier | 名称 | 定义 | 可用于 |
|---|---|---|---|
| T0 | `main` fact | 已合入 `main` 的文件、正式导师讨论记录、当前仓库可复查总账。 | 稳定背景、正式路径引用、后续 PR 默认事实。 |
| T1 | PR #97 snapshot fact | PR #97 当前 OPEN / 未合入分支上的资产和 comment，例如 438→69→25、25 篇全文文库。 | 设计线索、case 候选、A1 待复核资产。 |
| T2 | historical comment | issue / PR comment 中的历史规划、阶段性汇报或 reviewer 判断。 | 背景线索、设计 rationale；不能替代数据文件。 |
| T3 | planned evidence | A0 计划但尚未构造的 gold / silver fact、trap papers、benchmark scenarios、run records。 | 只能写成待构造。 |

## 3. PR #97 当前快照

当前 A0 记录的 PR #97 状态：

| 字段 | 当前值 |
|---|---|
| PR | [#97](https://github.com/HansBug/research_ideas/pull/97) |
| 状态 | OPEN / 未合入 |
| snapshot SHA | `b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727` |
| 证据角色 | PR #97 snapshot fact / 分支局部证据 |
| 可引用内容 | 438→69→25 阶段性筛选链、25 篇 P0/P1 全文文库、D1--D7 fulltext review 作为 case 候选。 |
| 禁止写法 | “main 已有 25 篇全文 baseline 文库”“已合入的 438→69→25 数据集”。 |

## 4. 引用格式

引用 PR #97 资产时，必须写清：

```text
PR #97 (OPEN / 未合入 / snapshot: b8b7e72 / 分支局部证据)
```

若只写 `PR #97` 而没有状态或 snapshot，视为事实漂移风险。

## 5. 数字引用规则

| 数字 | 当前允许写法 | 禁止写法 |
|---|---|---|
| 787 / 746 | 需从 `main` 当前 `sources/SUMMARY.md` 复核后写为 `main` fact。 | 沿用历史 comment 数字而不复核。 |
| 438→69→25 | 只能写为 PR #97 snapshot evidence。 | 写成 `main` 已合入筛选结果。 |
| 25 篇全文 | 只能写为 PR #97 snapshot evidence。 | 写成当前仓库主线已有文库。 |
| gold / silver facts | A0 还未构造，只能写 planned evidence。 | 写成已存在评价集。 |

## 6. 漂移触发条件

出现以下任一情况，必须更新本文件和 [project_inventory.md](./project_inventory.md)：

1. PR #97 merge 到 `main`。
2. PR #97 head SHA 变化。
3. PR #97 被关闭但未合入。
4. `sources/SUMMARY.md` 的数量或状态口径变化。
5. 后续 A1 对 PR #97 资产做 fact-union、裁剪、重命名或版权扫描。
6. issue #85 / #101 出现新的上游定调 comment。

## 7. Review gate

reviewer 检查任何后续 PR 时，应 grep：

```bash
grep -R "438→69→25\|25 篇\|PR #97\|787\|746" project_1_llm_state_machine_modeling/paper_agent_based_slr
```

若命中行没有明确 `main`、`OPEN`、`未合入`、`snapshot`、`分支局部`、`待构造` 等证据层级，至少列为 I 级问题。
