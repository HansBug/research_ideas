# Legacy Asset Inheritance

## 1. 目的

本文件说明旧 Path-1 / PR #93 / PR #94 / PR #96 / 2026-05 Direction-Decision Sprint 资产如何被 R0 使用。核心原则是：**复用结构经验和事实线索，不继承旧 `NL -> STM` story。**

## 2. 旧资产清单

| 资产 | 当前状态 | 可复用内容 | 不可继承内容 |
|---|---|---|---|
| `paper_v1/README.md` | `main` 已有 | 作为历史入口和旧 sprint 背景。 | 当前阶段、投稿目标、Path-1/Path-2 决策口径不能作为第一篇最新事实。 |
| `PATH1_HARD_COMPARISON_GUIDE.md` | `main` 已有 | 旧 Path-1 hard comparison 风险和基线意识。 | 把第一篇写成 direct `NL -> STM` hard comparison。 |
| `PATH2_DIFFERENTIATION_GUIDE.md` | `main` 已有 | 控制系统差异化样本和 Path-2 背景。 | 把 Path-2 压回第一篇主线。 |
| PR #93 `path1_foundation/` | 仅在 #93 head 分支存在 | “入口 + story + evidence + experiment_design + plan”的分层方式。 | 旧 foundation 的 task、venue、S0/S1/S2 计划不能机械继承。 |
| PR #94 | 合入 #93 分支 | baseline 反证、close works、claim-to-avoid 线索。 | 将九大 baseline 结论写成 `main` 已落盘完整事实。 |
| PR #96 | 合入 #93 分支 | claim gate、terminology policy、outline 结构经验。 | 旧 S0a 仍围绕 Path-1 hard comparison 的 story。 |

## 3. 可复用结构

R0 复用旧 path1_foundation 的以下结构模式：

```text
README.md
story/
evidence/
experiment_design/
plan/
```

但 R0 将其落在新路径：

```text
project_1_llm_state_machine_modeling/paper_v1/better_stm_repair_loop/
```

不在 `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/` 下新增、移动或修改文件。

## 4. 旧 story supersede 规则

以下旧口径已被 2026-06-12 导师定调和 PR #100 覆盖：

1. 第一篇主线是 `NL -> STM` 生成。
2. 第一篇主要靠 Path-1 direct baseline hard comparison 取胜。
3. `fcstm` / DSL 可作为论文主贡献。
4. E1/E2 可写成 Hybrid 方法贡献。
5. 过程性工程材料可进入 Method 主线。
6. baseline 只作为被击败竞品，不作为 seed / converter / related work 资产。

## 5. `paper_v1/README.md` 入口同步说明

`paper_v1/README.md` 是 `main` 上已有旧入口，仍保留 2026-05 Direction-Decision Sprint 信息。R0 实现阶段会在该 README 顶部增加“当前第一篇新主线入口”提示，避免读者误把旧 Path-1/Path-2 口径当成最新事实。

若后续需要彻底重写 `paper_v1/README.md`，应作为单独 follow-up 或 R7 写作阶段处理；R0 只做最小入口同步。
