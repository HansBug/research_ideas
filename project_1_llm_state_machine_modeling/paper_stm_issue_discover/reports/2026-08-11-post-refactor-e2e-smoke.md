# 重构后端到端 smoke：`0000` × 双执行模型

> **目的**：验证 2026-08-11 那次大规模目录重构（`paper_stm_repair/` 更名、实验资产收归、旧路线归档、43 份文档树化）**没有破坏流水线的可运行性与语义**。
>
> **性质**：这是一次**工程验证**，不是研究性运行。⛔ 本文的数字**不得进入任何论文统计**——它只有两个用途：证明重构后跑得通，以及证明找到的还是同一批东西。

## 1. 运行设定

| 项 | 值 |
| :-- | :-- |
| 代码版本 | `paper1/pr-discover` @ `213462f2`（重构与审计修正全部完成之后） |
| pair | `llms_emp_feedback_final_0000` |
| 执行模型 | `claude-opus-4-7` 与 `gpt-5.5`，两格并发 |
| 轮数 | 各 1 轮 |
| 重试 | **不设**（正式启动器有 `MAXTRY=6`，smoke 刻意不用——目的就是看它第一次能不能跑通，重试会掩盖失败） |
| 入口 | `python -m paper_stm_feedback_loop.discover --pair-id … --profile … --content-language zh-CN` |

⚠️ 输出落在 `/tmp`，未入库——`runs/` 全目录被 `.gitignore` 排除，而这本就不是研究性运行。本文即其审计记录。

## 2. 结果

两格均 `status = completed`、`coverage_status = full`、**零降级、零覆盖缺口、零重试**；两份 log 中 `Traceback` / `Error:` / `CRITICAL` 出现次数均为 **0**。

| | claude-opus-4-7 | gpt-5.5 |
| :-- | --: | --: |
| 发布 issue | **4** | **4** |
| LLM 调用 | 8 | 8 |
| 传输尝试 / 重试 | 8 / **0** | 8 / **0** |
| 节点数 | 15 | 14 |
| 落盘记录 | 48 条 | 46 条 |
| 节点耗时 | 412 s | 501 s |
| 已满足需求项 | 6 | 9 |
| 被排除的发现 / 观察 | 1 / 2 | 1 / 2 |

## 3. 与重构前（v46 全量运行）的同格对比

v46 的 `0000` 三轮见 `discover_matrix/v46/telemetry/v46_cells.json`。

| | smoke | v46 三轮 | 判定 |
| :-- | --: | :-- | :-- |
| claude issue | 4 | 4 / 3 / 6（均 4.3） | ✅ 落在区间内 |
| claude 调用 | 8 | 10 / 8 / 8（均 8.7） | ✅ |
| claude 耗时 | 412 s | 463 / 349 / 361 s（均 391 s） | ✅ |
| gpt issue | 4 | 4 / 3 / 4（均 3.7） | ✅ |
| gpt 调用 | 8 | 15 / 16 / 8（均 13.0） | ✅（v46 亦有一轮为 8） |
| gpt 耗时 | 501 s | 1011 / 1064 / 439 s（均 838 s） | ✅（v46 亦有一轮为 439 s） |

📌 **判定口径**：v46 同一格三轮的 issue 数本就在 3–6 之间波动（LLM 采样随机性），所以 smoke 只要落在该区间内即为正常；落在区间外才需追查。**不得把单轮吻合读作"复现了 v46"。**

## 4. 比数字更有说服力的两条

### 4.1 输入字节未变

两格的 `input_hashes` 完全相同，且 `natural_language` 的 SHA-256 为 `f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8`——与按 `nl.txt` 内容对 60 个 pair 分组时算出的那份「高层驾驶模块」需求哈希一致（该组即 `0000` / `0010` / `0020` / `0030` / `0040` / `0050`）。**语料搬迁后，流水线读到的输入与搬迁前逐字节相同。**

### 4.2 找到的是同一批东西

两个执行模型**各自独立**给出 4 条，且逐条对应：

| # | claude | gpt |
| --: | :-- | :-- |
| 1 | 缺失作者变量 `front_distance` | 未声明 `front_distance` 跟踪量 |
| 2 | 缺失独立事件 `human_steering_cmd` 及其承载 `AutoFinal -> HumanDrivingMode` 的迁移边 | 未声明独立的 `human_steering_cmd` 事件 |
| 3 | 缺失独立事件 `brake_pressed` | 未声明独立的 `brake_pressed` 事件 |
| 4 | 缺失从运行时状态经 `Power_Off` 到 `FinalState` 的迁移边 | `Power_Off` 未作为运行模式中的终止响应生效 |

这 4 条在 v46 的分析里都有出处：`front_distance` 是那个不具判别力谓词的来源（PlantUML 无变量声明语法，故该断言对任何模型都为真）；`Power_Off` 到终态那条正是缺陷台账首条记录的双侧原文；`human_steering_cmd` 与 `brake_pressed` 是需求第 4 句三个并列触发中的两个。

**所以重构不只是"跑得通"，语义也没漂。**

## 5. 这次 smoke 不能证明什么

1. **不能证明覆盖率未变。** 单 pair 单轮，且 issue 数落在采样波动区间内——区间内的吻合是**必要条件不是充分条件**。要证明覆盖率，需要重跑全量网格。
2. **不能替代回归测试。** 它验的是端到端可运行性，不验任何具体判据。测试侧的证据是：`feedback_loop` **1860 passed**（重构前 1749 + 1 failed）、`discover_matrix` 412 passed / 0 skip、`archive/agent_loop_method` 2 failed / 414 passed（恰为搬迁前基线）。
3. **不能说明其余 53 个 pair 也正常。** `0000` 是最常用的诊断 pair，可能不具代表性。

## 6. 顺带发现的一处文档脱节（已修）

跑这次 smoke 时发现 `CLAUDE.md` §5 与仓库根 `README.md` 都在教「运行真实 LLM 前必须 `source .env`；代码只读 `os.environ`」——那描述的是**已归档的旧 agent loop**。当前运行时读仓库根的 `.llmconfig.yml`，且 `utils/llm/config.py` 明确写了「运行时刻意拒绝从环境变量静默取凭据」，仓库根本没有 `.env`。

该脱节此前已实际造成误导：一次把「`.env` 不存在」误判为鉴权失败、**杀掉了 4 个正在正常运行的格子**。两处文档已按实测机制更正。
