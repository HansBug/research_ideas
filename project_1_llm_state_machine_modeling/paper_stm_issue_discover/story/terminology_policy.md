# 论文术语规范

正文首次引入研究术语写作“中文（English）”；缩写在同一处定义，此后用固定中文或缩写。题名与章节标题可保持简洁，定义落在首次正文使用处。所有图内文本、图例和 Figure 题注均用英文。模型名始终采用冻结请求 ID：`gpt-5.6-luna`、`claude-sonnet-5`、`qwen3.8-27b`、`muse-glimmer-30b`。原始代码、路径与历史文献中的名字不改写。

| 中文术语 | 固定英文 / 缩写 |
| --- | --- |
| 状态机 | state machine |
| 迁移 | transition |
| 事件响应 | event response |
| 自然语言描述 | natural-language description |
| 大语言模型 | large language model，LLM |
| 模型检查事实 | model inspection facts |
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
| 外部评价器 | external evaluator |
| 内容等价 | content equivalent |
| 三轮并集覆盖率 | union coverage |
| 三轮稳定覆盖率 | stable coverage |
| 严格报告精确率 | strict precision |
| 配对簇重采样 | paired cluster bootstrap |
| 用户研究 | user study |

图内受版面限制可将 model inspection facts、structured intermediate guidance 缩为 inspection facts、intermediate guidance；候选复核（candidate review and correction）为内部语义复核节点的图示说明。统一采用 relation-first policy，不混用 validity-first。K/N/I 的有效性按冻结归属规则定义，普通精确率与严格精确率并列。

| 内部条件 | 正文名称 | 对应 RQ |
| --- | --- | --- |
| X1v2 baseline | 直接发现基线 / direct-discovery baseline | RQ1、RQ2 |
| v61 / E2 ours | 完整方法 / full method (Full) | 共同对照 |
| A1 | 无检查事实 / no inspection facts | RQ3 |
| A3 | 无中间引导 / no intermediate guidance | RQ4 |
| A4 | 无执行反馈 / no execution feedback | RQ5 |
| A2 | 不进入本文叙事 | 无 |

C-4 固定为人工标注数据集 / manually annotated dataset；不再称多模型实证贡献。谓词是有类型、可执行的检查模板，不指自由逻辑中的完备证明系统。当前 12 项与历史 19 项注册身份分别追溯，不写成历史重跑。

语言修改保护数值、公式、模型 ID、文献题名、来源和条件。点估计写明幅度与适用范围，不用“显著”替代统计证据；A3 的整组干预与 A4 的固定候选及标签政策保留。
