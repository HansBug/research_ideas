# TTool-AI: SMD subset strict seed核验

## R1.5 strict seed编码

| 字段 | 当前判断 |
|---|---|
| candidate_id | `ttool-ai-smd-subset` |
| source_batch | baseline / local fulltext |
| local_source | [`baselines/ttool-ai/`](../../../../baselines/ttool-ai/) |
| paper | Ludovic Apvrille and Bastien Sultan, "System Architects Are not Alone Anymore: Automatic System Modeling with AI", MODELSWARD 2024 |
| strict_seed_grade | `ES-C` |
| 主 seed 计数 | 不计入 PR-R2 主 seed 下限，除非后续完成 case-level T0 isolation 或 PR-R3 timing 规范化合同。 |
| artifact_usability | `SA-2` |
| exclusion_code | `EX-none`; hard-for-main risk: `R-TIME-AFTER`; soft risk: `R-REPAIR-SCOPE`, `R-LICENSE-PENDING`, `R-LLM-DRIFT` |
| 当前结论 | 可作为“自然语言系统规格到SysML State Machine Diagram初始生成/反馈修正”的 extended seed / converter pressure；当前不计入主 seed，因为示例和公开 SMD 含 `after (5, 5)` 等时间语义，尚未证明可抽取 T0-only case。 |

## P1/P2/P3/P4核验

| 谓词 | 结论 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | `paper_content.txt` Page 2/Introduction称LLM可从system specification抽取components、interconnections、behaviors；Page 6 §4.1给出coffee machine自然语言规格；Page 10 §5.2说明公开仓库中的测试系统目录包含system specifications。 |
| P2_T0_STM_FAMILY | pass with caveat | `paper_content.txt` Page 2说明设计最终依赖state machines描述block behavior；Page 8 §4.3明确“identify the state machine of block”；Figure 4给出CoffeeMachine state machine。注意示例SMD包含guards、actions、signals和`after (5, 5)`，更接近SysML/TTool EFSM/SMD；若R2只接受纯T0 FSM，需在转换时规范化或标注timeout语义。 |
| P3_GENERATION_RELATION | pass | `paper_content.txt` Page 4 §3.1说明从system specification自动创建SysML diagrams；Page 8 §4.3给出问题模板“From the system specification ... identify the state machine of block”；Page 10 §5.1.2说明从GPT JSON生成或修改SysML model。 |
| P4_EVIDENCE_POINTER | pass | 本文件已记录页码/章节/图表指针；artifact证据见[artifacts.md](./artifacts.md)。 |

## SS/SA结论

**ES-C**：该候选满足 NL 输入、SMD 输出和生成关系，且全文有明确方法、示例、评估和公开实验工件；但 strict seed hard gate 要求 T0（无关键时间语义），而 TTool SMD 示例含 `after (5, 5)`、signal send/receive、guard/action 赋值等语义。当前只能作为 extended seed / converter pressure，不计入 `SS-A/SS-B + SA-1/SA-2` 主 seed 下限。若后续逐 case 证明所选公开模型不依赖时间语义，或 PR-R3 冻结了可审计的 timed-SMD 规范化策略，才可重新评估为条件 `SS-B`。

**SA-2**：公开artifact可支撑R2复查：GitHub仓库含测试系统规格、TTool XML模型和`results.ods`。但从允许读取材料中无法核验license；真实重跑依赖TTool nightly、OpenAI key、GPT-3.5 turbo和随机性，不能保证bit-for-bit复现。

## 适用边界

- 可用作Project 1中“LLM生成SysML state machine diagram”的强相关baseline/seed。
- 可用于抽取公开 NL 规格与生成后的 TTool XML 模型，研究生成错误、语法约束反馈、状态机质量评分；但在完成 T0 isolation 前不作为 PR-R2 主 seed。
- 不宜单独作为Project 4“已知缺陷驱动迭代修复”的核心SS-A样本；若纳入repair corpus，应标注为“feedback-based generation correction / syntactic-semantic constraint repair”，而非counterexample-driven repair。
- 若后续只处理T0 FSM，需对TTool SMD中的`after`、signal send/receive、guard/action赋值做转换策略，不应默认它们已经是纯T0 FSM。

## Pending / blocker

1. `R-LICENSE-PENDING`：允许读取的本地材料未给出artifact仓库license；不能写成license已核验。
2. `R-LLM-DRIFT`：论文实验使用TTool nightly build October 2023与ChatGPT 3.5 turbo；真实复跑会受provider/model漂移影响。
3. `R-REPAIR-SCOPE`：论文反馈环能修正格式、约束和部分语法/语义错误，但不是以已知缺陷或模型检查反例为输入的repair pipeline。
4. `R-TIME-AFTER`：示例 state machine 带 `after (5, 5)` 时间约束；这是当前不计主 seed 的直接原因。PR-R3 converter 需要明确保留、抽象或剔除时间语义，并记录信息损失。

## 全文阅读状态

- `bibtex.bib`：已读；确认题名、DOI、HAL URL、MODELSWARD 2024。
- `paper_content.txt`：已读；证据足够，未额外读取PDF正文。
- `paper.pdf`：本地存在；本轮未打开，因为文本提取已覆盖所需证据。
- 源目录`ASSETS.md` / `DESC.md`：已读；用于artifact与baseline上下文核对。
