# 当前状态总账

本文件回答“现在 paper1 到底做到哪一步”。它只汇总稳定研究结论；完整事实仍以对应 JSON、registry 和 report 为准。

## 1. 总体结论

当前完成的是 **修正前准备度审计**，不是正式修正实验。

| 项 | 状态 | 说明 |
|---|---|---|
| 一手 seed registry | 已建立 | 入口：[corpora/seed_library/REGISTRY.md](./corpora/seed_library/REGISTRY.md) |
| 四例静态冒烟样例 | 已建立 | 入口：[selected_seed_examples/README.md](./selected_seed_examples/README.md) |
| 原始模型到规范化 JSON | 已跑通四例，并完成 PlantUML 全量恢复摸排 | 入口：[pipeline/conversion/README.md](./pipeline/conversion/README.md) |
| 规范化 JSON 到 `.fcstm` | 四例均可导出并通过 parse / inspect | 入口：[pipeline/representation/README.md](./pipeline/representation/README.md) |
| 评价门 v0 | 已定义并 dry-run 四例 | 入口：[pipeline/evaluation/README.md](./pipeline/evaluation/README.md) |
| R5 全量摸排 | 已完成 | 入口：[pipeline/smoke/README.md](./pipeline/smoke/README.md) |
| R5.5 `llms-emp` 主 seed 池深度画像 | 已完成 | 入口：[pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md](./pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md)、[pipeline/smoke/seed_library_sweep/llms_emp_r56_handoff.md](./pipeline/smoke/seed_library_sweep/llms_emp_r56_handoff.md) |
| 真实修正循环 | 未完成 | 后续阶段实现；当前没有 `STM_k` 主实验结果 |
| Better STM 主结果 | 未完成 | 需要真实修正、回归、人工/结构化裁决后才能判定 |

## 2. Seed 资源现状

R5 全量摸排后的方向性结论：后续主实验优先围绕 `llms-emp-stm-subset` 展开。它是当前最符合 `<NL, LLM-generated STM_0>` 硬边界的一手资源，且具备 10 个唯一 NL × 6 个 LLM 输出的可比较结构。完整 60 case 状态表与问题谱系见 [pipeline/smoke/seed_library_sweep/llms_emp_main_seed_analysis.md](./pipeline/smoke/seed_library_sweep/llms_emp_main_seed_analysis.md)；R5.5 深度画像与边界交接见 [pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md](./pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md) 与 [pipeline/smoke/seed_library_sweep/llms_emp_r56_handoff.md](./pipeline/smoke/seed_library_sweep/llms_emp_r56_handoff.md)。

| 角色 | 条目 | 可用数量 / 特征 | 当前处理 |
|---|---|---|---|
| 可直接复验的一手 `NL + STM_0` | `llms-emp-stm-subset` | 60 个 LLM-generated PlantUML pair；10 个唯一 NL × 6 个 LLM 输出；R5/R5.5：16 converted / 41 partial / 3 blocked；cluster 时间等级为 8 个 T0、1 个 T0.5、1 个 T1 | 作为 R6/R7 主实验优先 seed 池；必须隔离 reference / checking 后结果，并按 10 个 NL cluster 报告；Digital Camera 作为 supplementary stress，不支撑 T0 主 claim |
| 可直接复验的一手 `NL + STM_0` | `sefm-llm-state-machine` | 9 个 NL description，但只有 1 个 SSC7 generated Umple 输出 | 可作可读冒烟 / 小样例；不能按 8 或 9 个 generated pair 计算 |
| 可直接复验的一手 `NL + STM_0` | `unified-uml-multimodal-validation` | 999 行 raw；989 个有效 generated PlantUML pair；10 个 generation failure | 可作 synthetic stress；不能包装成真实控制系统需求 |
| 条件候选 | `ttool-ai-smd-subset` | 6 个 `NL + generated TTool XML` 条件 pair，4 个唯一 NL | 可作转换压力源；进入主实验前需冻结 T0/SMD 切片和泄漏边界 |
| 需本项目复跑 | `fsm-bench-20` | 20 个系统、252 条 NL requirements；作者未公开 generated `STM_0` | 后续若使用，必须另建 generation run record |
| 需本项目复跑 | `designing-fsm-gpt4` | 作者源码可用，但未公开冻结 `<NL, generated STM_0>` pair | 后续若使用，必须另建 generation run record |
| 相关工作 / 论文可重建 | 其余条目 | 当前没有一手机读 generated pair | 不进入现成 seed 池 |

完整主表见 [corpora/seed_library/REGISTRY.md](./corpora/seed_library/REGISTRY.md)。

## 3. 转换与表示现状

### 3.1 四例转换

| 样例 | 来源 | 原始格式 | R3 conversion | R4.5 `.fcstm` | 备注 |
|---|---|---|---|---|---|
| `llms-emp-gpt4o-hldcs` | LLMS-EMP | PlantUML | `converted` | parse / inspect `ok` | 官方 SCXML 可用 |
| `llms-emp-deepseek-microwave` | LLMS-EMP | PlantUML | `converted` | parse / inspect `ok` | 依赖 R3.1 转换前规范化 replay；raw 不覆盖 |
| `llms-emp-kimi-autonomous-collision` | LLMS-EMP | PlantUML | `converted` | parse / inspect `ok` | 较复杂 HSM / 条件标签 caveat |
| `sefm-ssc7-umple` | SEFM | Umple | `partial` | parse / inspect `ok` | `after(60)` timing loss 保留 |

### 3.2 PlantUML 全量恢复

| 指标 | 数量 |
|---|---:|
| 一手 PlantUML pair 总数 | 1049 |
| 原始官方 SCXML 已可转换 | 550 |
| 原始失败 | 499 |
| all-rules 技术通过 | 476 |
| low-risk / main eligibility 通过 | 466 |
| normalization 后仍失败 | 23 |
| source-level semantic audit 总数 | 490 |
| semantic audit pass | 481 |
| semantic audit fail | 9 |
| low-risk semantic fail | 0 |

解释：这些数字只说明 conversion eligibility，不说明 修正循环改善。

## 4. R5 全量摸排结果

事实源：[pipeline/smoke/seed_library_sweep/sweep_report.json](./pipeline/smoke/seed_library_sweep/sweep_report.json)。

| 指标 | 数量 |
|---|---:|
| seed entry directories | 36 |
| registry entries | 16 |
| unregistered entries | 20 |
| pair records total | 1078 |
| asset records total | 16 |
| archives | 2 |

### 4.1 entry 状态

| 状态 | entries |
|---|---:|
| `partial` | 4 |
| `needs_generation` | 2 |
| `not_applicable` | 30 |

### 4.2 pair 状态

| 状态 | pairs | 解释 |
|---|---:|---|
| `converted` | 529 | 可进入修正前 `.fcstm` 表示，但仍需保留归因 |
| `partial` | 504 | 可进入 R7 eligibility review，不能无条件进入主实验 |
| `blocked` | 23 | 当前转换负证据，进入 R8 negative evidence 或 转换器 follow-up |
| `needs_generation` | 2 | 有 NL+code / pipeline，但作者未公开 generated `STM_0` |
| `not_applicable` | 20 | 不是作者一手 generated seed，或不属于目标形式 |


### 4.3 R5.5 `llms-emp` 深度画像

事实源：[pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md](./pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md)。

| 指标 | 数量 / 结论 |
|---|---|
| raw pair | 60 = 10 个唯一 NL cluster × 6 个 LLM 输出 |
| pair 状态 | 16 converted / 41 partial / 3 blocked |
| cluster 时间等级 | 8 个 T0、1 个 T0.5、1 个 T1 |
| pair 时间等级 | 48 T0 / 6 T0.5 / 6 T1 |
| cluster story role | 9 个 main_candidate、1 个 supplementary_stress |
| boundary_decision | `proceed_with_supplementary` |

R5.5 的结论是：主线可以继续围绕 T0/T0.5 离散 FSM/HSM/statechart artifacts 推进；`condition_like_label_lowered_as_event` 只能作为 R5.7 候选 repair target，必须逐例回到 NL 与 raw `STM_0` 判定，不能把 representation symptom 直接写成已确认语义缺陷。

## 5. 四例冒烟结果

事实源：[pipeline/smoke/selected_examples/smoke_report.json](./pipeline/smoke/selected_examples/smoke_report.json)。

| 指标 | 数量 |
|---|---:|
| examples | 4 |
| pass | 0 |
| partial | 4 |
| blocked | 0 |

四例全部通过 R5 contract checks，但都保留为 `partial`，因为上游 R3/R4/R4.5 已记录 conversion 或 representation caveat。`partial` 不表示 smoke 未跑通；它表示后续使用时不能把这些损失当作修正收益清零。

## 6. 当前不能写的结论

1. 不能写修正循环已经有效。
2. 不能写已经生成 `STM_k` 或得到 Better STM 主结果。
3. 不能把 PlantUML normalization、canonical conversion 或 `.fcstm` lowering 的收益计入 修正循环收益。
4. 不能把 选定四例写成最终实验集合或样本上限。
5. 不能把 Unified synthetic 数据包装成真实控制系统需求。
6. 不能把 TTool XML 当成已经切好的纯 T0 状态机。

## 7. 下一步决策入口

| 后续方向 | 需要做什么 | 依赖当前产物 |
|---|---|---|
| R6 修正循环骨架 | 优先围绕 `llms-emp-stm-subset` 选 12–18 条分层样本，真正跑 `<NL, STM_i> -> feedback -> candidate -> regression` 的最小闭环 | [pipeline/smoke/handoff/r5_to_r6_repair_inputs.json](./pipeline/smoke/handoff/r5_to_r6_repair_inputs.json)、[pipeline/smoke/handoff/llms_emp_main_seed_handoff.md](./pipeline/smoke/handoff/llms_emp_main_seed_handoff.md) |
| R5.6 story / model scope 回填 | 基于 R5.5 冻结 T0/T0.5 主线、Digital Camera supplementary stress、blocked negative evidence 与 EFSM-lite/guard/action caveat 写法 | [pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md](./pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md)、[pipeline/smoke/seed_library_sweep/llms_emp_r56_handoff.md](./pipeline/smoke/seed_library_sweep/llms_emp_r56_handoff.md) |
| R7 协议 / eligibility freeze | 冻结 `llms-emp-stm-subset` A/B/C/D 分层、10-NL clustered reporting 与 conversion-aware attribution；再决定 supplementary seed 角色 | [pipeline/smoke/handoff/r5_to_r7_seed_eligibility.json](./pipeline/smoke/handoff/r5_to_r7_seed_eligibility.json)、[pipeline/smoke/seed_library_sweep/llms_emp_main_seed_analysis.md](./pipeline/smoke/seed_library_sweep/llms_emp_main_seed_analysis.md)、[pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md](./pipeline/smoke/seed_library_sweep/llms_emp_deep_profile.md) |
| R8 负证据 / 主实验前清理 | 处理 blocked、missing、not_applicable、needs_generation | [pipeline/smoke/handoff/r5_to_r8_negative_evidence.json](./pipeline/smoke/handoff/r5_to_r8_negative_evidence.json) |
| generation follow-up | 对 `fsm-bench-20` / `designing-fsm-gpt4` 这类 NL+code 来源复跑并建立 run record | seed registry 中的 仅流水线 条目 |
