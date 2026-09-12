# 论文术语规范

正文首次引入研究术语写作“中文（English）”；缩写在同一处定义，此后用固定中文或缩写。题名与章节标题可保持简洁，定义落在首次正文使用处。所有图内文本、图例和 Figure 题注均用英文。模型名始终采用冻结请求 ID：`gpt-5.6-luna`、`claude-sonnet-5`、`qwen3.8-27b`、`muse-glimmer-30b`。原始代码、路径与历史文献中的名字不改写。

| 中文术语 | 固定英文 / 缩写 |
| --- | --- |
| 状态机 | state machine |
| 迁移 | transition |
| 事件响应 | event response |
| 自然语言描述 | natural-language description |
| 大语言模型 | large language model，LLM |
| 模型检视事实 | model inspection facts |
| 结构化中间引导 | structured intermediate guidance |
| 执行反馈 | execution feedback |
| 义务 | obligation |
| 候选问题 | candidate issue |
| 类型化谓词 | typed predicate |
| 后端 | backend |
| 参考问题 | reference issue |
| 完整方法 | full method，Full |
| 直接发现基线 | direct-discovery baseline |
| 平均覆盖率 | mean coverage |
| 消融实验 | ablation study |
| 报告精确率 | precision |
| 状态 | state |
| 事件 | event |
| 守卫 | guard |
| 可达性 | reachability |
| 变量 | variable |
| 一致性检查 | consistency checking |
| 行为模型正确性评价方法 | Behavioral Model Correctness Evaluation，MCeT |
| 模型检查 | model checking |
| 源制品 | source artifact |
| 来源映射 | source mapping |
| 拓扑 | topology |
| 语义复核 | internal semantic assessment |
| 问题层级 | problem level |
| 点状或表面对齐问题 | surface-alignment issue，L0 |
| 结构或局部状态问题 | structural or local-state issue，L1 |
| 行为或全局问题 | behavioral or global issue，L2 |
| 终止 | termination |
| 统一建模语言 | Unified Modeling Language，UML |
| 证据强度 | witness strength |
| 可执行证据 | executable evidence |
| 需求异味 | requirements smell |
| 反例 | counterexample |
| 追踪关系恢复 | traceability link recovery |
| 形式化方法 | formal methods |
| 完整性 | completeness |
| 性质模式 | property pattern |
| 形式化需求获取工具 | Formal Requirements Elicitation Tool，FRET |
| 测试预言问题 | oracle problem |
| 有限控制状态机 | finite control state machine，FCSTM |
| 单区层次片段 | single-region hierarchical fragment |
| 复合状态 | composite state |
| 动作 | action |
| 运行配置 | configuration |
| 宏步 | macro-step |
| 有限轨迹 | finite trace |
| 有界验证 | bounded verification |
| 时钟 | clock |
| 时间事件 | time event |
| 正交区域 | orthogonal region |
| 历史伪状态 | history pseudostate |
| 分叉/汇合 | fork/join |
| 分析诊断 | analysis diagnostic |
| 候选身份 | candidate identity |
| 有界运行前沿 | bounded execution frontier |
| 仿真 | simulation |
| 可满足性模理论 | satisfiability modulo theories，SMT |
| 状态图可扩展标记语言 | State Chart XML，SCXML |
| 领域不变量 | domain invariant |
| 受限修订 | bounded revision |
| 结构检查 | structural check |
| 拓扑检查 | topological check |
| 轨迹检查 | trace check |
| 元模型 | metamodel |
| 执行返回值 | verdict |
| 执行回执 | execution receipt |
| 根报告 | root report |
| 子主张 | subclaim |
| 外部评价 | external evaluation |
| 研究问题 | research question，RQ |
| 描述簇 | description cluster |
| 输入对 | input pair |
| 提示 | prompt |
| 末端重放 | terminal replay |
| 缺陷状态 | defect status |
| 充分匹配 | full match，FULL |
| 部分匹配 | partial match，PARTIAL |
| 无匹配 | no match，NO |
| 静态分析工具评测 | Static Analysis Tool Exposition，SATE |
| 参考真值 | ground truth |
| 已知有效报告 | valid known report，K |
| 集合外有效报告 | valid novel report，N |
| 无效报告 | invalid report，I |
| 关系优先规则 | relation-first policy |
| 报告评阅 | manual review |
| 评阅者 | reviewer |
| 内容等价 | content equivalent |
| 三轮并集覆盖率 | union coverage |
| 三轮稳定覆盖率 | stable coverage |
| 严格报告精确率 | strict precision |
| 配对簇重采样 | paired cluster bootstrap |
| 用户研究 | user study |
| 案例研究 | case study |
| 适配器 | adapter |
| 基于规则的确定性候选加工 | rule-based candidate processing |
| 清单候选 | inventory candidate |
| 执行探测 | execution probe |
| 不成立的报告 / 无效报告 | invalid report |
| 配置进展检查 | progress check |
| D2-only 覆盖 | D2-only coverage（沿用 hit@1 的命中定义，只统计 98 条 D2 参考问题，分母 294，不限制报告缺陷状态） |
| 严格覆盖 | strict coverage（只计 D1/D2 报告提供的 FULL 匹配，限制的是报告） |
| 严格覆盖 | strict coverage |
| 有限控制状态机 | finite control STate Machine，FCSTM（STM 首字母大写解释缩写来源） |

## 对外口径映射：内部材料用语 → 论文表述

依据 [story/README.md](./README.md) 的论文对外口径铁律。从实验报告、归档、judge/ 与 evaluation/ 目录改写进论文时逐项转换，不得直接抄句。

| 内部材料用语 | 论文表述 |
| --- | --- |
| judge、semantic judge、语义 judge、评价器、固定 Luna 评价、外部评价器 | 评阅者（reviewer）、人工评阅（manual review） |
| 两读、双读、两次判读 | 两位评阅者独立判读 |
| 仲裁（由模型完成） | 第三位评阅者仲裁 |
| validity 步与 relation 步 | 语义判断与参考匹配分步进行、材料隔离 |
| human_confirmations、人工确认数、作者确认 | 不出现 |
| relation_first policy | 关系优先规则（保留） |
| 台账、ledger | 参考问题集合、参考数据集 |
| 公开仓库、GitHub 链接、HansBug/research_ideas | 复现材料以匿名复现包随评审提供，录用后公开 |

⛔ 论文禁词（中英文正文、题注、补充材料、审稿回复一律适用）：judge、LLM-as-judge、评价器 / evaluator、自动裁定、裁判、人工确认、github.com、research_ideas、HansBug，以及"gpt-5.6-luna 判读 / 评价 / 评阅 / 裁定"这类把模型名与评阅动作连写的句子。机械门为 [check_paper_wording.py](./check_paper_wording.py)。

图题一律中文（“图 N：”），图内文字、图例与坐标轴一律英文；表题中文。谓词第四族在论文中称“配置进展检查”，不再使用“有界验证”作为族名；论文只出现 12 条谓词，不出现旧注册表条目数或“历史”“冻结记录”“请求身份”等实验日志用语。hit@k 保留记法但须解释为三轮均值、并集、交集。P 只称“普通报告精确率”，不引入“接纳率”等第二名称；模型检视事实（model inspection facts）中的“检视”与形式化“模型检查（model checking）”区分，全文不再写“模型检查事实”。RQ5 只写“冻结上游候选、屏蔽执行反馈、同一协议评阅”，不写任何核算路径；图 4 只保留关系优先规则一个面板。V1 写为在 SMT 求解器上执行的有界模型检查查询（变量取初始赋值），与 §4.2 的 SMT 表述一致。不报调用预算、具体调用次数或 token，只允许 §5.3 一句“基线为单次调用，Full 为多阶段多轮调用，两臂未匹配调用次数”；阶段表用“轮数上限”。不用“冻结”“刻画”等模板腔词：协议写“事先确定的协议”，标注写“此后不再修改”，A4 上游写“固定 Full 的上游候选”，结果与规则直接说结果与规则；回写飞书前按 shuorenhua 口径通读一遍。飞书评论纪律：一个决策只开一条评论，不在多处重复；整段回写后检查未决评论的锚定是否失效。

图内受版面限制可将 model inspection facts、structured intermediate guidance 缩为 inspection facts、intermediate guidance；候选复核（candidate review and correction）为内部语义复核节点的图示说明。统一采用 relation-first policy，不混用 validity-first。K/N/I 的有效性按冻结归属规则定义，普通精确率与严格精确率并列。

| 内部条件 | 正文名称 | 对应 RQ |
| --- | --- | --- |
| X1v2 baseline | 直接发现基线 / direct-discovery baseline | RQ1、RQ2 |
| v61 / E2 ours | 完整方法 / full method (Full) | 共同对照 |
| A1 | 无检视事实 / no inspection facts | RQ3 |
| A3 | 无中间引导 / no intermediate guidance | RQ4 |
| A4 | 无执行反馈 / no execution feedback | RQ5 |
| A2 | 不进入本文叙事 | 无 |

C-4 固定为人工标注数据集 / manually annotated dataset；不再称多模型实证贡献。C-1/C-2/C-3 按 [2026-09-10 导师聊天](../../talks/2026-09-10-导师-paper1三项技术贡献定稿与A4精确率口径.md)定稿：检视事实→行为问题的更强发现；中间引导 + 基于规则的候选加工→覆盖与精确率双重提高；类型化谓词→证据升级，执行结果排除不成立的报告并提高精确率。全文不用“幻觉”一词，改写为“不成立的报告 / 无效报告”。方法面向通用状态机，PlantUML 只称案例研究。评价口径按 2026-09-04 导师决定与 2026-09-11 用户批注统一：145 条参考问题的标注与全部输出报告的评阅均写为博士生人工完成（两位独立判读、第三位仲裁），正文任何位置不出现 LLM-as-judge、评价器模型名或人工确认数；数据集写“构建并随论文提供”，不写仓库名与链接。谓词是有类型、可执行的检查模板，不指自由逻辑中的完备证明系统。当前 12 项与历史 19 项注册身份分别追溯，不写成历史重跑。

语言修改保护数值、公式、模型 ID、文献题名、来源和条件。点估计写明幅度与适用范围，不用“显著”替代统计证据；A3 的整组干预与 A4 的固定候选及标签政策保留。
