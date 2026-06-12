# Agent Provenance

## 1. Plan-stage review

| 身份 | Comment | 结论 | 主要建议 |
|---|---|---|---|
| claude reviewer | [#102 comment](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692556772) | C=0 / I=0 | 避免 fact ledger 重复形成双真源；`evaluation_gate.md` 需声明不是 R4 v0；claim map 与 forbidden wording 互链。 |
| deepseek reviewer | [#102 comment](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692562174) | C=0 / I=0 | `path1_foundation/` 只存在于 PR #93 分支；记录 `paper_v1/README.md` 旧入口共存风险。 |
| codex reviewer | [#102 comment](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692594023) | C=0 / I=0 | 只提出措辞级 M 建议，plan ready。 |

> 说明：PR #102 上存在若干重复或超时前 comment；本表记录最终可用的三路 plan review 结论。

## 2. Sidecar 调研

| 子代理 | 任务 | 结论 |
|---|---|---|
| 旧 Path-1 路径结构调研 | 只读查找 PR #93/#96/S0a 路径结构 | 建议复用 `README + story + evidence + experiment_design + plan` 分层；不继承旧 `NL -> STM` story；新路径使用 `paper_v1/better_stm_repair_loop/`。 |
| story 草拟 sidecar | 为 story/ 文件提供章节建议 | 用于主 session 起草，不直接写入论文事实。 |

## 3. Main-session 处理

1. 创建 PR #102 empty PR。
2. 完成三路 plan review，确认 C=0/I=0。
3. 按 reviewer M 建议补充：
   - `path1_foundation/` 仅为 PR #93 分支局部历史路径；
   - `paper_v1/README.md` 旧入口需最小同步；
   - `evaluation_gate.md` 不等于 R4 v0；
   - `claim_evidence_map.md` 与 forbidden wording 互链。
4. 落地 R0 文档结构。

## 4. 不作为论文内容的事项

本文件仅服务 PR 审计和协作，不进入 manuscript 的 Method、Contribution 或 Results。任何 agent review、CI、run record 或工程执行记录都不能被包装成论文方法贡献。
