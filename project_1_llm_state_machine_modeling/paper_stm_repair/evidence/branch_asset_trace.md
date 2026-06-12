# branch asset trace：#93/#94/#96 分支局部资产追踪

## 1. 原则

PR #93 仍 open；PR #94 / #96 虽已 merged，但合入目标是 `paper/project1-path1-foundation`，不是 `main`，也不是当前 PR-R1 分支。因此这些资产只能作为 branch-local reusable assets，不能写成 main 已有事实。

## 2. 分支局部资产表

| asset_id | source PR | source branch / commit | merge target | main status | 核心路径 | reuse decision | 是否复制到 R1 | 使用限制 |
|---|---:|---|---|---|---|---|---|---|
| `foundation-pr93-head` | [#93](https://github.com/HansBug/research_ideas/pull/93) | `paper/project1-path1-foundation @ 7affa1d9...` | intended `main`, PR open | not in main | `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/**` | cite-only | 否 | 只作为历史 foundation 线索；当前新主线以 `paper_stm_repair/` 为准。 |
| `s1a-nine-baselines` | [#94](https://github.com/HansBug/research_ideas/pull/94) | merge `820453d1...` | `paper/project1-path1-foundation` | not in main | `path1_foundation/baselines/**` | cite-only + re-summarize from current main | 否 | baseline facts 可借鉴，但必须回到当前 `baselines/` 与 `ASSETS.md` 复核；旧 `NL -> STM` wording 不继承。 |
| `s0a-story-reframe` | [#96](https://github.com/HansBug/research_ideas/pull/96) | merge `4b6a51a8...` | `paper/project1-path1-foundation` | not in main | `path1_foundation/story/**` | cite-only | 否 | claim gate / terminology 弱化可参考；当前事实真源是 PR-R0 [#102](https://github.com/HansBug/research_ideas/pull/102)。 |
| `legacy-pr9-assets` | #93 branch history | foundation branch | `paper/project1-path1-foundation` | not in main | `dataset_selection/legacy_pr9_assets/**` | defer-to-R2 | 否 | 323 sample pool、30 NL expansion、early reference drafts 是 historical sprint evidence，不是当前 frozen seed registry。 |
| `current-r1-missing-foundation` | PR-R1 audit | `paper1/r1-baseline-asset-audit` | #100 | missing | key `path1_foundation/**` paths missing in current branch | record-only | 不适用 | 明确当前 R1 没有也不拥有 `path1_foundation/`。 |

## 3. 对 PR-R1 的实际决策

1. 不 cherry-pick `path1_foundation/**`，避免把旧 Path-1 story 和当前 `paper_stm_repair/` 形成第二事实源。
2. 对九大 baseline 资产，只重新汇总当前 main 的 [baselines/SUMMARY.md](../../baselines/SUMMARY.md) 与各 `ASSETS.md`；旧 #94 逐篇文件只作为交叉核验线索。
3. 对旧 S0a story，只保留“不要突出 `fcstm` / 不要宣称 first NL-to-STM / 不要把 run record 写成方法贡献”等警戒；具体表述以 R0 文档为准。
4. 对 PR #9 legacy sample pool，不在 R1 冻结；R2 若需要 stress-test seed，可另开样本登记并重新 hash / 复核 / 排除。
