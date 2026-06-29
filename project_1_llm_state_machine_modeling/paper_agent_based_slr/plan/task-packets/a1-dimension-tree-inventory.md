# PR-A1-DT 任务包：逐篇复原综述维度树

## 1. 目标

本任务包对应 PR [#135](https://github.com/HansBug/research_ideas/pull/135)：在 PR-A1 已建立的 [../../survey_of_surveys/](../../survey_of_surveys/) 文库上，把 19 篇全文级 `review.md` 从“平铺 pattern / A1-M0--M6 矩阵”升级为可审计的维度树资产。

核心目标是让每篇论文都能回答：原文的 RQ / 贡献声明如何形成维度树，叶子维度的取值空间是什么，字段如何支撑统计观察和候选发现，结论如何回链到原文证据。

## 2. 上游与范围

| 项 | 内容 |
|---|---|
| 当前 PR | [#135](https://github.com/HansBug/research_ideas/pull/135) |
| 直接上游 | [#132](https://github.com/HansBug/research_ideas/pull/132) |
| 伞 PR | [#101](https://github.com/HansBug/research_ideas/pull/101) |
| 当前分支 | `paper2/a1-dimension-tree-inventory` |
| 直接 base | `paper2/a1-survey-of-surveys-scaffold` |
| 是否运行真实 LLM | 否 |
| 是否读取 `.env` | 否 |
| 是否跑四个真实例子 | 否；本 PR 只做文库结构与证据链实现 |

## 3. 允许修改范围

- [../../survey_of_surveys/GUIDE.md](../../survey_of_surveys/GUIDE.md)
- [../../survey_of_surveys/SUMMARY.md](../../survey_of_surveys/SUMMARY.md)
- [../../survey_of_surveys/patterns/pattern-field-schema.md](../../survey_of_surveys/patterns/pattern-field-schema.md)
- [../../survey_of_surveys/papers/](../../survey_of_surveys/papers/) 下 19 篇 `review.md`
- 本任务包与 [../progress.md](../progress.md)

## 4. 必须交付

- [x] GUIDE 新增维度树复原、关系边、roadmap 降级、审计附录和 SUMMARY 回链纪律。
- [x] schema 新增维度树、节点、叶子取值空间、关系边、证据链、结论映射和 SUMMARY 归纳合同。
- [x] 19/19 篇 `review.md` 新增 `## 维度树复原` 小节。
- [x] 19/19 篇 `review.md` 有叶子维度表、统计与候选发现链路、可迁移 / 不可迁移边界。
- [x] 19/19 篇 `review.md` 有 A.1--A.4 审计附录，正式表头纯中文。
- [x] 关系型样本补充关系边表；roadmap / vision / proposal / guideline 样本显式降级。
- [x] SUMMARY 新增维度树模式总览、维度树类型与 Paper2 L0--L7 关系、SUMMARY 结论-证据映射。
- [x] 所有 SUMMARY `[sum-A1DT-*]` 归纳回链单篇 A.3 结论标识。

## 5. 拒收检查

1. 如果任一 `review.md` 缺少 `维度树复原` 或 A.1--A.4 审计附录，应拒收。
2. 如果 A.1--A.4 正式表头出现 `ID`、`PDF`、snake_case 或中英对照，应拒收。
3. 如果 A.3 支撑证据不能回链 A.2，或 A.2 来源标识不能回链 A.1，应拒收。
4. 如果 `weak` / `not_verified` 被允许进入主统计池、SUMMARY 定量统计或 final research finding，应拒收。
5. 如果 roadmap / vision / proposal 的 action point 被写成系统综述统计 finding，应拒收。
6. 如果 DevSecOps 等关系型 schema 被压平成普通树而没有关系边表，应拒收。
7. 如果 SUMMARY 跨论文归纳没有 `[sum-A1DT-*]` 证据映射或无法回链单篇结论标识，应拒收。
8. 如果合流后覆盖上游 PR-A1 已核验事实、统计池口径或 CCF 复核状态，应拒收。

## 6. 验证命令

```bash
git diff --check origin/paper2/a1-survey-of-surveys-scaffold...HEAD -- \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys

git ls-files -u
rg -n '^(<<<<<<<|=======|>>>>>>>)' \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/plan || true
python /tmp/check_a1dt.py
```

其中 `/tmp/check_a1dt.py` 是本轮按 PR body §7.5 固化的结构检查脚本副本；它只验证结构闭环，不替代 reviewer 对原文证据准确性的学术审计。

## 7. 当前验证记录

| 时间 | 命令 / 检查 | 结果 |
|---|---|---|
| 2026-06-29 21:48:00 | 内部 verifier 复核后 I 级修复 | 已修 SUMMARY `[sum-A1DT-tree-types]` / `[sum-A1DT-boundary-anchor]` 中“过滤 weak”与纳入 weak boundary 结论的口径冲突：树型总览改为非定量索引，boundary 行显式允许弱证据但禁止进入主统计池、SUMMARY 定量统计或 final finding；同时修复 schema 示例链接占位。 |
| 2026-06-29 21:10:00 | `python /tmp/check_a1dt.py` | 通过；19 篇均具备维度树、叶子表、A.1--A.4、A.2→A.1、A.3→A.2、SUMMARY→单篇 A.3 回链。 |
| 2026-06-29 21:10:00 | `git diff --check origin/paper2/a1-survey-of-surveys-scaffold...HEAD -- survey_of_surveys` | 通过；未发现行尾空白或 diff 格式问题。 |

## 8. Capability-use audit

- Required references/scripts: `$ai-research-writing-skill` 的 story / reviewer gate，`$research-planning` 的可执行计划口径，`$sub-agents`，PR body §7.5 结构检查脚本。
- Inputs consumed: PR #135 body、PR #132 / #101 上游关系、`survey_of_surveys` 现有 GUIDE / SUMMARY / schema / 19 篇 review / metadata。
- Artifacts produced: GUIDE 维度树规则、schema 字段合同、19 篇单篇维度树复原和审计附录、SUMMARY 维度树总览与结论映射、本任务包。
- Verification run: 上游 clean 状态核验、结构检查、diff check、冲突标记检查。
- Remaining risk: 当前证据定位多为全文文本级和 section / 页码待核对；A2a 仍需对表格、图、supplementary 和页码做视觉级精核。
