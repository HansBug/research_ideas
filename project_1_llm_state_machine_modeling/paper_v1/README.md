# `paper_v1/` — 第一篇论文工作区

## 0. Current overlay（2026-06-09）

当前第一篇论文已经从 2026-05 的 Direction-Decision Sprint 进入 **Path-1 paper foundation** 阶段。后续第一篇 paper 的默认入口是 [path1_foundation/README.md](./path1_foundation/README.md)。

当前导师定调与执行口径：

1. 第一篇主线优先走 **Path-1 baseline hard comparison**，而不是 Path-2 控制系统差异化主线。
2. Path-2、变量三分法、BMC/LTL 和更深控制系统语义保留为后续论文或 future work。
3. E1 自建 agent-loop 与 E2 mature-agent skill route 是同一底座的不同 agent orchestration 条件，不再主打 Hybrid。
4. 论文贡献应落在形式化状态机表示、形式化检查反馈、可执行仿真反馈、LLM agent 修复与可审计 run record，而不是 `fcstm`、LangGraph、Codex、Claude 等工程名。
5. 投稿计划按 issue [#67](https://github.com/HansBug/research_ideas/issues/67) 的 2026 夏季期刊冲刺口径推进：按 CCF-A 标准打磨，主投 SoSyM regular rolling，ASE Journal / RE Journal regular rolling 作备投。

后续新 session 推荐阅读顺序：

1. [path1_foundation/README.md](./path1_foundation/README.md)
2. [path1_foundation/story/paper_story.md](./path1_foundation/story/paper_story.md)
3. [path1_foundation/dataset_selection/sample_assets.md](./path1_foundation/dataset_selection/sample_assets.md)
4. [path1_foundation/experiment_design/experiment_inventory.md](./path1_foundation/experiment_design/experiment_inventory.md)
5. [path1_foundation/experiment_design/execution_plan.md](./path1_foundation/experiment_design/execution_plan.md)
6. [path1_foundation/dataset_selection/legacy_pr9_assets/README.md](./path1_foundation/dataset_selection/legacy_pr9_assets/README.md)
7. [../talks/2026-06-04-导师-第一篇论文路线与E1E2定位.md](../talks/2026-06-04-导师-第一篇论文路线与E1E2定位.md)

以下历史内容保留用于追溯 2026-05 Direction-Decision Sprint，不再代表当前默认施工入口。


## 1. 目录定位

`paper_v1/` 是 `project_1` 第一篇论文的工作区，负责承载：

1. **Direction-Decision Sprint 阶段**的两路实验决策报告（`PATH1_REPORT.md` / `PATH2_REPORT.md`）
2. **方向定后**的正式 paper 工作产物（`OUTLINE.md` / 各章节 draft / figures / tables / submission package）
3. 两路并行模式下的路线**接管指引**（`PATH1_HARD_COMPARISON_GUIDE.md` / `PATH2_DIFFERENTIATION_GUIDE.md`）

它不收录论文（不属于论文集），所以**不遵循** [CLAUDE.md §2.2](../../CLAUDE.md) 的论文集规范；它的命名约定是"工作产物面向 paper 写作"。

## 2. 历史阶段 — Direction-Decision Sprint（2026-05，已被 current overlay 覆盖）

本目录在 **2026-05 Direction-Decision Sprint 历史阶段** 曾承担以下任务：

1. 在 main 分支稳定 `method/` 共同基础（agent loop + pyfcstm 反馈 + ex1 judge）
2. fork 两个 branch（`dev/path1-hard-comparison` / `dev/path2-differentiation`）
3. 各自跑 quick experiment 产出决策证据
4. 提两个 PR 不合并，等用户综合判断后选定方向

详细 sprint 计划见 [discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md)（**meta-level 路线规划与决策准则**，两路开工前必读）。

## 3. 目录结构

历史 sprint 阶段产物：

```text
paper_v1/
├── README.md                            (本文件，目录定位)
├── PATH1_HARD_COMPARISON_GUIDE.md       (Path 1 硬刚路线接管指引)
├── PATH2_DIFFERENTIATION_GUIDE.md       (Path 2 差异化路线接管指引)
├── PATH1_REPORT.md                      (Path 1 sprint 跑完后由 Phase 6 产出)
└── PATH2_REPORT.md                      (Path 2 sprint 跑完后由 Phase 6 产出)
```

方向定后曾设想的扩展产物（历史计划，当前以 [path1_foundation/](./path1_foundation/) 为准）：

```text
paper_v1/
├── DIRECTION.md                         (最终方向决策记录 + rationale)
├── OUTLINE.md                           (10-12 页 conf paper 骨架)
├── sections/                            (各章节 draft)
├── figures/                             (论文配图)
├── tables/                              (论文配表)
└── submission/                          (投稿 package)
```

## 4. 历史 sprint 新 session 进入顺序

以下顺序仅用于追溯 2026-05 sprint 历史，不是当前默认施工入口。当前默认入口见本文件 §0。

1. 本 [README.md](./README.md)（先读 §0 current overlay）
2. [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md)（历史 meta-level 路线规划与决策准则）
3. 如需追溯历史 branch，再选读：
   - `dev/path1-hard-comparison` 历史材料：[PATH1_HARD_COMPARISON_GUIDE.md](./PATH1_HARD_COMPARISON_GUIDE.md)
   - `dev/path2-differentiation` 历史材料：[PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md)
4. [../method/STATUS.md](../method/STATUS.md) 顶部 current overlay

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

## 7. 历史投稿目标

本节记录 2026-05 sprint 时的旧口径：当时曾按 **ICSE / FSE / ASE 2027 conf paper**（10-12 页）设想推进，journal 投稿作为 fallback。当前投稿口径已经被本文件 §0 覆盖：优先按 issue [#67](https://github.com/HansBug/research_ideas/issues/67) 的 SoSyM / ASE Journal / RE Journal regular rolling 期刊路线推进。
