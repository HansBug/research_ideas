# `paper_v1/` — 第一篇论文工作区

## 0. 2026-06-12 后当前第一篇新主线入口

> **重要更新**：2026-06-12 导师讨论后，本目录保留为 2026-05 Direction-Decision Sprint / Path-1 / Path-2 历史工作区。第一篇论文主线已经从早期 Path-1 hard comparison / `NL -> STM` 生成口径，转向 **`<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动状态机修正任务**。当前新主线入口请读 [../paper_stm_repair/README.md](../paper_stm_repair/README.md)；本目录旧 `NL -> STM` / hard comparison 口径不再作为当前第一篇事实真源。

若需要追溯导师定调，先读 [../talks/SUMMARY.md](../talks/SUMMARY.md) 与 [../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md](../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md)。

## 1. 目录定位

`paper_v1/` 是 `project_1` 第一篇论文的工作区，负责承载：

1. **Direction-Decision Sprint 阶段**的两路实验决策报告（`PATH1_REPORT.md` / `PATH2_REPORT.md`）
2. **方向定后**的正式 paper 工作产物（`OUTLINE.md` / 各章节 draft / figures / tables / submission package）
3. 两路并行模式下的路线**接管指引**（`PATH1_HARD_COMPARISON_GUIDE.md` / `PATH2_DIFFERENTIATION_GUIDE.md`）

它不收录论文（不属于论文集），所以**不遵循** [CLAUDE.md §2.2](../../CLAUDE.md) 的论文集规范；它的命名约定是"工作产物面向 paper 写作"。

## 2. 当前阶段 — Direction-Decision Sprint

本目录**当前阶段**（2026-05-26 起 30 小时窗口）承担的核心任务是：

1. 在 main 分支稳定 `method/` 共同基础（agent loop + pyfcstm 反馈 + ex1 judge）
2. fork 两个 branch（`dev/path1-hard-comparison` / `dev/path2-differentiation`）
3. 各自跑 quick experiment 产出决策证据
4. 提两个 PR 不合并，等用户综合判断后选定方向

详细 sprint 计划见 [discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md)（**meta-level 路线规划与决策准则**，两路开工前必读）。

## 3. 目录结构

当前阶段产物：

```text
paper_v1/
├── README.md                            (本文件，目录定位)
├── PATH1_HARD_COMPARISON_GUIDE.md       (Path 1 硬刚路线接管指引)
├── PATH2_DIFFERENTIATION_GUIDE.md       (Path 2 差异化路线接管指引)
├── PATH1_REPORT.md                      (Path 1 sprint 跑完后由 Phase 6 产出)
└── PATH2_REPORT.md                      (Path 2 sprint 跑完后由 Phase 6 产出)
```

方向定后的扩展产物（推迟创建，sprint 阶段不建）：

```text
paper_v1/
├── DIRECTION.md                         (最终方向决策记录 + rationale)
├── OUTLINE.md                           (10-12 页 conf paper 骨架)
├── sections/                            (各章节 draft)
├── figures/                             (论文配图)
├── tables/                              (论文配表)
└── submission/                          (投稿 package)
```

## 4. 新 session 进入顺序

任何新 Claude / codex session 进入本目录后，按以下顺序读：

1. 本 [README.md](./README.md)（理解目录定位与当前阶段）
2. [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md)（meta-level 路线规划与决策准则）
3. 根据当前所在 branch 选读：
   - 若在 `dev/path1-hard-comparison`：读 [PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md)
   - 若在 `dev/path2-differentiation`：读 [PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md)
   - 若在 `main`：两份 GUIDE 都读，但**只能动 `method/` 共同基础**，不能动 path 特有的 evaluation 代码
4. `method/STATUS.md`（如果存在，查 sprint 当前进度）

## 5. 与 project_1 其他目录的关系

1. [../sources/](../sources/) — Path 2 的数据来源（控制系统真实样本，T0 子集）
2. [../baselines/](../baselines/) — Path 1 的数据来源（structure_event T0 子集 + llms_emp stm T0 子集）
3. [../reproduction/](../reproduction/) — sprint 结果落盘位置（`results/sprint_path1/` / `results/sprint_path2/`），不在 `paper_v1/` 下
4. [../discussions/](../discussions/) — 历史讨论稿，sprint 计划在此（不在 `paper_v1/` 下，因为它是"决策"而不是"论文产物"）
5. [../../project_ex1_llm_judge_for_stm/](../../project_ex1_llm_judge_for_stm/) — Judge 来源（ex1 `ExpertReviewAgent`）

## 6. Sprint LLM 接入标准（v3 新增）

Sprint 阶段所有 LLM 调用统一走仓库根 `.env`（已 gitignore）中的三件套环境变量：

- `LLM_ENDPOINT`（OpenAI-compatible proxy）
- `LLM_API_KEY`
- `LLM_MODEL`

**运行前必须 shell `source .env`**；代码**绝不直接读** `.env` 文件，只读 `os.environ`。切换模型（GPT-5.5 → GPT-5.4 → Claude → Qwen → DeepSeek）只改 `LLM_MODEL` + 重新 source，代码不动。

`method/gpt_client.py` 是 sprint 中唯一允许实例化 OpenAI-compatible client 的位置；所有 agent / baseline replication 都 inject 这个 client。

详细约束见 [PATH1_HARD_COMPARISON_GUIDE.md §4.2a](./PATH1_HARD_COMPARISON_GUIDE.md#42a-methodgpt_clientpy-统一-llm-clientv3-新增--必须实现在-phase-0) 与 [PATH2_DIFFERENTIATION_GUIDE.md §4.3](./PATH2_DIFFERENTIATION_GUIDE.md#43-methodgpt_clientpy-统一-llm-clientv3-新增--必须实现在-phase-0)。

## 7. 投稿目标

按用户 2026-05-26 对齐讨论：**ICSE / FSE / ASE 2027 conf paper**（10-12 页），截稿 2026 年 7-8 月。journal 投稿是 fallback。
