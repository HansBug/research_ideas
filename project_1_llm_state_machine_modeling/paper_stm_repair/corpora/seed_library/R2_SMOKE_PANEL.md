# R2 一手 seed 池裁决与四例 smoke panel

> 本文件是 PR-R2 的主产物：把 [REGISTRY.md](./REGISTRY.md) 的一手资源事实裁决为当前可用 seed 池，并冻结后续 PR-R3--R6 复用的开发 smoke panel。逐条一手资源事实仍以 [REGISTRY.md](./REGISTRY.md)、各条目 `seed_resource_registry.json` 与 `assets/README.md` 为准；本文只记录 R2 裁决、面板选择和后续使用纪律。

## 0. 结论速览

当前 R2 裁决如下：

| 分组 | 条目 | R2 裁决 | 后续作用 |
|---|---|---|---|
| final seed pool | [`llms-emp-stm-subset`](./llms-emp-stm-subset/assets/README.md)、[`sefm-llm-state-machine`](./sefm-llm-state-machine/assets/README.md)、[`unified-uml-multimodal-validation`](./unified-uml-multimodal-validation/assets/README.md) | 进入当前一手 seed 池 | 可作为作者一手 `NL + NL-generated STM_0` 来源；仍需保留各自 caveat。 |
| conditional seed pool | [`ttool-ai-smd-subset`](./ttool-ai-smd-subset/assets/README.md) | 条件进入 smoke panel | 只作为 TTool XML / T1-to-T0 切片压力源；不计现成 final pool。 |
| pipeline-only supplement | [`fsm-bench-20`](./fsm-bench-20/assets/README.md)、[`designing-fsm-gpt4`](./designing-fsm-gpt4/assets/README.md) | 不进入 author first-source final pool | 只作后续本项目复跑构造 seed 的补充来源；复跑必须另建 run record。 |
| paper-reconstructable | `automated-transition-use-cases-uml-sm` 等 10 条 | 不进入本轮 smoke panel | 只作 related work / 手工重建线索。 |

固定 4 个开发 smoke 样本：

| smoke_id | seed_id | R2 角色 | 覆盖意图 | 后续主用途 |
|---|---|---|---|---|
| `r2-smoke-llms-emp-gpt4o-hldcs` | `llms-emp-stm-subset` | final-pool-ready | 强相关 SysML/PlantUML、1xN LLM 输出、reference/checking 泄漏隔离 | R3/R4/R5/R6 全链路基础样本 |
| `r2-smoke-sefm-ssc7-umple` | `sefm-llm-state-machine` | final-pool-ready | 非结构化 reactive-system NL、Umple/HSM-capable 输出、单例小样本 | R3/R4/R5/R6 小样本和系统语义压力 |
| `r2-smoke-unified-uml-synthetic` | `unified-uml-multimodal-validation` | final-pool-ready | synthetic 大规模 PlantUML、non-control-domain caveat、failure sentinel 隔离 | R3/R4/R5/R6 synthetic smoke/stress |
| `r2-smoke-ttool-automatedbraking-xml` | `ttool-ai-smd-subset` | conditional | TTool XML / SysML/AVATAR / T1-to-T0 切片压力 | R3 转换器压力与 R6 降级案例 |

**重要说明**：这 4 个样本只是后续开发 smoke panel，不是最终实验规模上限。若 R3/R4/R5/R6 发现某样本无法继续使用，只能按本文 §5 的替换规则替换，并记录替换原因；不能静默更换。

## 1. R2 裁决标准

| 裁决项 | 进入条件 | 不进入 / 降级条件 |
|---|---|---|
| final seed pool | 作者 / 论文制品已提供一手 `NL + NL-generated STM_0`，且 raw、locator、hash / trace、`pairs.jsonl` 可回溯。 | 只有论文图示、reference model、checking 后结果、旧 parquet、旧 reproduction 或未配对 run artifacts。 |
| conditional seed pool | 一手 `NL + generated artifact` 已可回溯，但 artifact 不是可直接进入 T0 FSM/HSM/EFSM/statechart 的纯净形态。 | 无法定位 NL 与 STM_0 配对，或存在不可隔离的 reference / repair leakage。 |
| pipeline-only supplement | 有一手 NL / prompt / schema / code，可由本项目复跑构造 `STM_0`。 | 作者未公开 generated `STM_0`；在复跑前不得计 author first-source seed。 |
| smoke panel | 至少能覆盖一个后续 R3--R6 风险维度，并有明确证据入口、选择理由、替换策略。 | 无证据入口、不可复用、或只为了凑数但不覆盖任何后续风险。 |

R2 不运行真实 LLM，不运行四例端到端实验；真实运行从 R3/R4/R5/R6 依赖本文件的固定面板开始。

## 2. final seed pool 裁决表

| seed_id | R2裁决 | NL输入 | STM_0输出 | 生成关系 | eligible pair | unique NL | unique STM_0 | T0适配 | 转换需求 | 主实验角色 | 证据入口 | caveat |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|
| [`llms-emp-stm-subset`](./llms-emp-stm-subset/assets/README.md) | 进入 final pool | SysML 行为模型自然语言 requirements descriptions；10 个唯一需求 × 6 个 LLM 输出 | `Generation PlantUML` 中的 SysML/UML state machine PlantUML | workbook 直接给出 `Requirement Description -> Generation PlantUML` | 60 | 10 | 59 | T0；结构化离散，未见 timed/hybrid 目标 | PlantUML 到内部 STM，需隔离 reference/checking 列 | 主 seed pool + smoke panel | [JSON](./llms-emp-stm-subset/seed_resource_registry.json)、[pairs](./llms-emp-stm-subset/assets/extracted/pairs.jsonl)、[preview](./llms-emp-stm-subset/assets/extracted/pairs_preview.md) | reference `PlantUML` 与 checking 后结果不得进入 `STM_0`；1xN 形态需分层抽样。 |
| [`sefm-llm-state-machine`](./sefm-llm-state-machine/assets/README.md) | 进入 final pool | reactive-system 系统描述；当前 eligible 只取 SSC7 自助结账系统 | Claude Sonnet 3.5 single-prompt generated Umple state machine | 4open ZIP 中 NL symbol 与 generated txt 可由 ZIP locator 回溯 | 1 | 9 | 1 | T0 为主；generated 输出含 `after(60)` timer-like transition，R3 需标注 | Umple 到内部 STM；需处理 timer-like syntax | 主 seed pool + smoke panel | [JSON](./sefm-llm-state-machine/seed_resource_registry.json)、[pairs](./sefm-llm-state-machine/assets/extracted/pairs.jsonl)、[preview](./sefm-llm-state-machine/assets/extracted/pairs_preview.md) | 只有 SSC7 有 generated output；其他 8 个 NL 不计 generated pair。 |
| [`unified-uml-multimodal-validation`](./unified-uml-multimodal-validation/assets/README.md) | 进入 final pool | LLaMA-3.2 合成的通用软件 feature descriptions | DeepSeek-R1-Distill-Qwen 生成的 PlantUML UML state diagram | HF parquet 直接给出 `input -> uml_code` | 989 | 999 | 989 | T0；PlantUML state diagram / statechart | PlantUML 到内部 STM；需排除 10 个 failure sentinel | 主 seed pool + synthetic/stress smoke | [JSON](./unified-uml-multimodal-validation/seed_resource_registry.json)、[pairs](./unified-uml-multimodal-validation/assets/extracted/pairs.jsonl)、[preview](./unified-uml-multimodal-validation/assets/extracted/pairs_preview.md) | synthetic / non-control-domain，不可包装成真实控制系统需求。 |

## 3. conditional seed pool 裁决表

| seed_id | R2裁决 | NL输入 | STM_0输出 | eligible pair | unique NL | unique STM_0 | 条件阻塞 | R2 使用方式 | 证据入口 |
|---|---|---|---|---:|---:|---:|---|---|---|
| [`ttool-ai-smd-subset`](./ttool-ai-smd-subset/assets/README.md) | 条件进入；不计现成 final pool | 作者 GitHub 工件中的系统规格：AutomatedBraking、DPS、platooning、spacebasedsystem / incoherency 变体 | generated TTool/SysML/AVATAR XML artifacts | 6 | 4 | 6 | XML 是完整 TTool 工件，非纯 T0；需冻结 SMD/T0 切片、时间/信号/guard/action 规范化与 incoherency 泄漏边界 | 作为 R3 转换器压力和 R6 降级案例；当前 smoke panel 选 1 个主案例，不选 incoherency 变体 | [JSON](./ttool-ai-smd-subset/seed_resource_registry.json)、[pairs](./ttool-ai-smd-subset/assets/extracted/pairs.jsonl)、[preview](./ttool-ai-smd-subset/assets/extracted/pairs_preview.md) |

## 4. pipeline-only 补充资源裁决表

| seed_id | R2裁决 | 可用内容 | 不计 final pool 的原因 | 后续可能用途 | 证据入口 |
|---|---|---|---|---|---|
| [`fsm-bench-20`](./fsm-bench-20/assets/README.md) | 仅复跑补充 | 20 个系统、252 条唯一 NL requirements、prompt、schema、代码；单系统 smoke 已走通 | 作者未公开 generated `STM_0`；`benchmark/gold/*.json` 是空 placeholder | 后续若需要 NL+code 构造 seed，可另开复跑 PR，并按 run record 记录模型、prompt、raw output 与 eligibility | [JSON](./fsm-bench-20/seed_resource_registry.json)、[README](./fsm-bench-20/assets/README.md) |
| [`designing-fsm-gpt4`](./designing-fsm-gpt4/assets/README.md) | 仅复跑补充 | 固定作者源码；初始 generation smoke 可通过 OpenAI-compatible proxy 走通；源码中有未配对 run artifacts | 无冻结 NL corpus、无作者一手 pair index；generated_text.csv / Graphviz outputs 未配对，不计 author pair | 后续可探索“本项目复跑生成 DFSM/Mealy seed”，但必须记录随机种子、生成出的 NL、模型、raw output | [JSON](./designing-fsm-gpt4/seed_resource_registry.json)、[README](./designing-fsm-gpt4/assets/README.md) |

## 5. 固定 smoke panel

| smoke_id | seed_id | pair_locator | NL摘要 | STM_0摘要 | source_coverage_class | input_format_class | conversion_pressure | defect_risk_class | selection_caveat | 选择理由 | 同类替代候选 | 后续使用 | 替换条件 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `r2-smoke-llms-emp-gpt4o-hldcs` | [`llms-emp-stm-subset`](./llms-emp-stm-subset/assets/README.md) | `pairs.jsonl::pair_id=llms_emp_stm_results_0000` | high-level driving module：human driving / autonomous mode / front_distance / steering / brake / power off 等需求 | GPT-4o generated PlantUML，含 HumanDriving、Autonomous、FinalState 等状态和嵌套 state block | final-pool-ready；strong LLM SysML/PlantUML seed | PlantUML / SysML-UML state machine | 轻量 PlantUML 转换；需识别嵌套 state 与 transition labels | reference/checking 泄漏隔离；层次结构解析；guard/action 语义抽取 | 该 workbook 同时有 reference 和 checking outputs；只允许读取 `Generation PlantUML` | 代表最贴近 paper1 原始 `NL -> STM_0` LLM seed 的强相关样本；pair 0000 在 preview 中可人工读懂 | 同一条目内可替换为其他 model output 或其他 requirement；优先保持 GPT-4o/LLM 代表性 | R3 转换冒烟；R4 静态诊断；R5 修正预演；R6 评价协议预演 | 若 PlantUML 转换器无法解析嵌套 state，可先替换为同条目更平坦 PlantUML，但必须记录原因。 |
| `r2-smoke-sefm-ssc7-umple` | [`sefm-llm-state-machine`](./sefm-llm-state-machine/assets/README.md) | `pairs.jsonl::pair_id=sefm_ssc7_single_prompt_claude_sonnet35_0001` | SSC7 自助结账系统：扫描、称重、支付、override、timeout 等 reactive-system 描述 | Claude Sonnet 3.5 generated Umple state machine，含 Ready、SecurityCheck、Payment、Override、Timeout 等 | final-pool-ready；small-realistic reactive-system LLM seed | Umple / UML state machine | 中等转换压力；需 Umple syntax 到内部 STM，且 `after(60)` 需标注 | 小样本单例；timer-like syntax；guard/action 抽取；系统语义较长 | 当前只有 SSC7 有 generated output，其余 8 个 NL 不能当 generated pair | 覆盖真实 reactive-system 长 NL 与 Umple 格式；能测试方法对非 PlantUML 的适配 | 无同条目 generated 替代；若失败，只能降级为 sefm NL-only/reference-only 说明，或由 R2 后续另选 final-pool 条目 | R3 Umple 转换压力；R4 场景/语义诊断；R5 修正预演；R6 小样本局限说明 | 若 R3 不支持 Umple，允许先作为“转换阻塞样本”保留，不得静默替换。 |
| `r2-smoke-unified-uml-synthetic` | [`unified-uml-multimodal-validation`](./unified-uml-multimodal-validation/assets/README.md) | `pairs.jsonl::pair_id=unified_uml_state_train_0000` | restaurant/menu ordering synthetic feature description | PlantUML UML state diagram，含 Menu Created、Adding Items、Viewing Menu、Payment 等状态 | final-pool-ready；synthetic UML smoke/stress | PlantUML UML state diagram | 轻量 PlantUML 转换；需排除 failure sentinel | synthetic/non-control-domain caveat；PlantUML 简化结构；大规模数据一致性抽检 | 不是控制系统真实需求；只能作 synthetic/stress，不支撑工业控制结论 | 覆盖大规模 synthetic PlantUML 与 failure sentinel 隔离；用于测试 pipeline 批量读取与降级写法 | 同条目内可替换为其他 valid row；不得使用 10 个 `No valid PlantUML code found.` 行 | R3 PlantUML 批量读取；R4 结构诊断；R5 简单修正 smoke；R6 synthetic 局限性 | 若 row 0000 过于简单，可替换为同条目更复杂 state diagram，并保留 row id。 |
| `r2-smoke-ttool-automatedbraking-xml` | [`ttool-ai-smd-subset`](./ttool-ai-smd-subset/assets/README.md) | `pairs.jsonl::pair_id=ttool-ai-automatedbraking` | AutomatedBraking：危险驾驶情境、车辆警告消息、附近车辆响应等控制/安全相关系统规格 | generated TTool XML，包含完整 TURTLEGMODELING / SysML/AVATAR 工件 | conditional XML；converter-pressure seed | TTool XML / SysML/AVATAR | 高转换压力；必须先切出 SMD/T0 子集并处理时间/信号/guard/action | T1-to-T0 降级；XML 切片；incoherency 泄漏隔离；非纯 state machine | 条件 pair 不计现成 final pool；AutomatedBraking 是主案例而非 incoherency 变体，泄漏风险低于 `incoherencies/` | 覆盖 TTool XML 与控制/安全相关系统规格，防止 R3 只适配 PlantUML/Umple | DPS 或 platooning 主案例；不优先用 incoherency 变体 | R3 转换器压力；R4 诊断可先干跑 XML 结构；R6 降级案例 | 若 TTool XML 切片不可行，该样本保持 conditional blocker，并在 R6 限制中说明。 |

## 6. 面板级覆盖矩阵

| 覆盖维度 | 当前覆盖 | 缺口 / 降级理由 | impact_on_later_prs |
|---|---|---|---|
| 来源覆盖 | 3 个 final-pool-ready + 1 个 conditional XML；pipeline-only 被排除在 author first-source panel 外 | 当前不含 pipeline-only-placeholder，因为 R2 不复跑 LLM，不应把复跑潜力与一手 pair 混合 | R3--R6 主 smoke 均基于一手 pair；若后续要评估本项目自造 seed，需要另开复跑 PR。 |
| 格式覆盖 | PlantUML/SysML、Umple、PlantUML/UML state diagram、TTool XML | 未覆盖 FSM JSON/CSV，因为 `fsm-bench-20` / `designing-fsm-gpt4` 没有作者一手 generated pair | R3 转换器先覆盖 PlantUML/Umple/XML；FSM JSON/CSV 作为复跑型扩展，不阻塞当前 R2。 |
| 风险覆盖 | reference/checking 泄漏隔离、层次/guard/action、timer-like syntax、synthetic caveat、failure sentinel 排除、TTool XML 切片 | 当前无法用一手 pair 覆盖 “作者冻结 FSM JSON/CSV generated seed” | R4/R5 可先覆盖结构、语义、转换和 synthetic 风险；FSM JSON/CSV 在 R6 作为缺口或后续扩展。 |
| 数据形态覆盖 | 1xN 多模型输出（LLMS-EMP）、单例长 NL（SEFM）、大规模 synthetic（Unified）、条件 XML 多案例（TTool） | final-pool-ready 中真实控制系统一手 generated pair 数量有限，SEFM 仅 1 对 | R6 需要把样本代表性写成限制；不得把 smoke panel 写成充分实验规模。 |
| R3--R6 复用覆盖 | 每个样本均明确 R3/R4/R5/R6 使用角色 | TTool 可能在 R3 转换器阶段阻塞，只能作为 conditional pressure | 若 TTool 阻塞，R3 必须记录转换阻塞；R6 不能把其计入成功端到端样本。 |

## 7. R3--R6 复用和替换规则

1. R3--R6 默认复用 §5 的 4 个 `smoke_id`，不得在无记录情况下替换。
2. 替换必须满足同类优先：PlantUML 替 PlantUML、Umple 替 Umple、TTool XML 替 TTool XML；若同类不可得，必须写明 `coverage_gap_reason`。
3. `pipeline_only` 条目不能直接替换 author first-source final seed；只有另行复跑并形成 run record 后，才可作为“本项目生成 seed”单独进入后续面板。
4. 若 TTool XML 无法切出 T0/SMD 子集，R2 面板不失败；该样本转为 converter blocker，R3/R6 需显式记录。
5. 若某 final-pool-ready 样本在 R3/R4 中发现 trace 或泄漏问题，应先回到对应 `assets/README.md` / `seed_resource_registry.json` 修证据链，再决定是否替换。

## 8. 不跑四例的说明

本 PR 不运行四例，不调用真实 LLM，不执行修正 loop。R2 的完成条件是：样本选择、证据入口、覆盖矩阵、替换规则和后续使用责任可审计。真实运行责任如下：

| 后续 PR | 使用 R2 面板的方式 |
|---|---|
| PR-R3 | 对 4 个 smoke 样本做转换器冒烟；允许 TTool 形成阻塞记录。 |
| PR-R4 | 对转换后或原始可解析对象做诊断 / 场景 / 评价门干跑。 |
| PR-R5 | 使用可转换样本做无人化修正 loop 预演，记录拒绝/回滚/振荡。 |
| PR-R6 | 继承 R4 指标骨架和 R5 预演结果，冻结主实验协议与降级写法。 |

## 9. R2 裁决不变量

后续维护本文件时必须保持以下不变量：

1. final seed pool、conditional pool、pipeline-only supplement 分开记录。
2. `NL+源码可复跑` 不计入 author first-source final pool。
3. 固定 smoke panel 至少 4 个样本，并逐项保留 evidence locator、选择理由、同类替代候选和替换条件。
4. 面板级 coverage matrix 记录来源、格式、风险、数据形态和 R3--R6 复用覆盖。
5. 本文件只记录 R2 裁决，不复制 [REGISTRY.md](./REGISTRY.md) 的全量事实表。
6. 本轮不跑真实四例、不调用真实 LLM；真实运行从 R3--R6 按职责展开。
