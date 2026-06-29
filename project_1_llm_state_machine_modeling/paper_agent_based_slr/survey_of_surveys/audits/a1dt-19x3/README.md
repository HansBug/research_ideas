# A1-DT 19×3 全文审计批次

本目录记录 PR-A1-DT 对 `survey_of_surveys/` 19 篇论文的三路全文学术审计。

## 目标

每篇论文分别由三类 agent 独立审计：

1. `codex`：`codex exec`
2. `claude`：`claude -p`
3. `deepseek`：`codex-deepseek exec`

每个 agent 必须阅读全文文本，并审查当前 `review.md` 中“维度树复原”的完整性、准确性和证据链可靠性。重点问题是：当前树是否过小、是否错位、是否遗漏原文 RQ / extraction form / taxonomy / coding scheme / roadmap figure / evidence table / finding path，是否把通用接口误写成原文 schema。

## 技能使用要求

每个 agent 的 prompt 都要求使用并体现以下技能口径：

- `$ai-research-writing-skill`：claim-evidence、reviewer gate、story / contribution / evidence 对齐。
- `$research-planning`：把论文中的 RQ、方法、实验 / 分析、任务结构和后续修复计划拆成可执行结构。
- `$oh-my-codex:autoresearch`：把审计当作 validator-gated research loop，输出 pass/fail、证据、阻塞项和下一步验证要求。

## 输出约束

- 每份审计输出一个 Markdown 文件：`results/<slug>__<agent>.md`。
- 审计 agent 不直接修改仓库内容。
- 审计必须给 C/I/M 分级；C/I 必须说明如何影响 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性。
- 审计必须给出“建议维度树骨架”和“必须补的叶子维度 / 关系边 / 证据项”。

## 当前状态

- 批次创建时间：2026-06-29
- 任务数：19 篇 × 3 agent = 57 份审计
- 当前状态：57/57 份审计已完成，任务清单见 [TASKS.tsv](./TASKS.tsv)，逐篇汇总见 [SUMMARY.md](./SUMMARY.md)。
- 当前用于修复 PR：#135
- 返修边界：本批次已用于把 19 篇 `review.md` 从“通用接口树”返修为“原文 schema 主树 + 跨论文投影”；但未声称完成 A2a 的逐页 / 表图 / supplementary 精核。
- 确定性门禁：运行 `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-19x3/check_structure.py`。

## 稳定运行命令

后续若需要补跑某个任务，优先使用本目录的 [run_audit.py](./run_audit.py)，它已经把 codex / claude 路径接到 `$sub-agents` 的稳定 runner，并把 deepseek 路径保留为 `codex-deepseek exec`：

```bash
python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-19x3/run_audit.py \
  --slugs <paper-slug> \
  --agents codex,claude,deepseek \
  --max-workers 3 \
  --timeout 2400 \
  --skip-existing
```

若只是做 PR 级审查，应按仓库老规矩分别运行 `codex-reviewer`、`claude-reviewer` 和 `codex-deepseek exec`，并要求 reviewer 直接在 PR 上 comment。
