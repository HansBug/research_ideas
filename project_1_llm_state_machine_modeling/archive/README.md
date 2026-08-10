# `archive/` — project_1 弃用路线归档区（复活导引总入口）

> **一句话**：这里的每条路线都**没有被删除**，只是停用。本目录的职责不是"介绍历史"，
> 而是**保证必要时能把它们重新跑起来**——所以每条路线都配一份「复活导引」，写明
> 前置条件、入口命令、以及**动它之前必须知道的地雷**。

## 0. 纪律（两条，都是硬约束）

1. **这里的内容不参与当前论文（STM issue discover）的任何结论。**
   不进指标、不进分母、不进台账、不作为方法主张的证据。当前论文的实现、语料、
   评测口径一律以 [../paper_stm_issue_discover/](../paper_stm_issue_discover/) 为唯一事实源。
2. **不得删除。** 归档 ≠ 废弃。这些路线包含大量已验证的设计资产（stage 契约、
   评测协议、mutation 自校验思路、证据边界纪律），后续研究内容二/三/四以及
   第二篇论文都可能直接取用。删掉等于把这些资产连同复活可能性一起丢弃。

补充一条现实提醒：**归档区不是纯死代码。**
[path1_evaluation/](./path1_evaluation/) 与 [path1_path2_guides/](./path1_path2_guides/)
仍被 `project_1_llm_state_machine_modeling/tests/` 里的活测试 import（见各自导引），
所以改动它们会直接影响 CI。

## 1. 三条路线一览

| 路线 | 目录 | 是什么 | 冻结时间 | 为什么弃用 | 复活导引 |
|---|---|---|---|---|---|
| Agent Loop 建模方法 | [agent_loop_method/](./agent_loop_method/) | NL → pyfcstm 状态机建模的 16-stage LangGraph agent loop | 2026-06-08 17:37:26（`1a66e7e9`） | 论文任务从 `NL -> STM` 生成转为 `<NL, STM_0> -> issue discover`；当前实现与它零代码耦合 | [agent_loop_method/ARCHIVE_README.md](./agent_loop_method/ARCHIVE_README.md) |
| Path-1 评测链 | [path1_evaluation/](./path1_evaluation/) | LLM 初审 + 人类签字的 5 阶段 component-level P/R/F1 评测流水线 | 2026-06-01 13:43:01（`52535008`） | 语料是两个 mock case，与当前 60-pair `llms_emp` 语料无交集；评测口径也已换成 issue 台账命中制 | [path1_evaluation/ARCHIVE_README.md](./path1_evaluation/ARCHIVE_README.md) |
| Path-1 / Path-2 路线指南 | [path1_path2_guides/](./path1_path2_guides/) | 旧「硬刚路线」与「差异化路线」的实验接管指引（原 `paper_v1/`） | 2026-06-12 23:44:52（`4d46b7ea`） | 2026-06-12 导师讨论后论文整体转舵，两条路线的 framing 均作废 | [path1_path2_guides/ARCHIVE_README.md](./path1_path2_guides/ARCHIVE_README.md) |

三条路线的关系：`path1_path2_guides` 是**路线级 framing**，`agent_loop_method` 是它的
**生成侧实现**，`path1_evaluation` 是它的**评测侧实现**。三者原本是一套；转舵时一起停用，
所以一起归档。

## 2. 当前活代码在哪（防误认）

未来 session 最容易犯的错是把归档区当成现行基础设施。当前真正在跑的东西是：

| 关注点 | 当前路径 |
|---|---|
| discover 主实现 | [../paper_stm_issue_discover/pipeline/feedback_loop/](../paper_stm_issue_discover/pipeline/feedback_loop/) |
| discover 运行入口 | `python -m paper_stm_feedback_loop.discover --pair-id ...` |
| 评测矩阵与判定 | [../paper_stm_issue_discover/discover_matrix/](../paper_stm_issue_discover/discover_matrix/) |
| 语料（60 pair，网格 54 pair） | [../paper_stm_issue_discover/selected_seed_examples/](../paper_stm_issue_discover/selected_seed_examples/) |
| 导师路线与实验边界 | [../talks/](../talks/) |

判别口诀：**目录名里带 `archive/` 的一律不是现行实现。**

## 3. 复活一条路线的通用流程

不管哪条路线，都按同一顺序走，不要跳步：

1. **读该路线的 `ARCHIVE_README.md`**（本文件表格第 6 列），先看「复活地雷」一节。
   有些地雷（例如依赖 git 历史而非工作树）会让"看起来正常"的复活静默失败。
2. **确认 submodule 与依赖**：`git submodule update --init --recursive`，
   然后 `venv/bin/pip install -e ./pyfcstm`。当前 pin 为
   `901f30e981c29eb8e304b33d61985652d2e85b2e`（`v0.6.0-181-g901f30e9`）。
3. **先跑离线 gate**（各导引给出具体命令），确认代码本身还能 import、还能过测试，
   再考虑接真实 LLM。
4. **再接真实 provider**：shell 里 `set -a; source .env; set +a`。
   注意三条路线的 env 契约**不一样**——`agent_loop_method` 用 `LLM_*` 三件套，
   `path1_evaluation` 用 `CLAUDE_CMD` / `CLAUDE_MODEL` / `CODEX_CMD` / `CODEX_MODEL`
   四件套（走 CLI 子进程，不走 OpenAI-compatible endpoint）。
5. **把复活当成新实验对待**：按 [../../CLAUDE.md](../../CLAUDE.md) §6 的 run record 要求
   留证据链，并按 §3.5 先做运行前的公平性 review。归档代码的旧结论不能直接搬进新论文。

## 4. 阅读顺序

1. 本文件：确认三条路线各是什么、纪律是什么、当前活代码在哪。
2. 目标路线的 `ARCHIVE_README.md`：复活前置条件与地雷。
3. 该目录**原有**的文档（`README.md` / `ARCHITECTURE.md` / `STATUS.md` / `PROTOCOL.md` 等）：
   设计细节与历史 provenance。⚠️ 这些是**冻结时的原件**，其中的路径、模块名和命令
   多数已随归档失效；各 `ARCHIVE_README.md` 里都有一节列出已知的文档腐烂项，
   先读那一节再读原件。
