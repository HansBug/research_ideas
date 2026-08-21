# 方法原则与审查契约

本文档是 `four-family-19-core.v1` 的现行政策。它约束注册表、实现、实验和论文叙事；
旧目录中的设计说明只具有历史意义。

## 1. 方法对象和证据升级

输入是自然语言需求与待审查的状态机模型。系统先拆分需求义务，再做源句、模型元素和
语义关系的绑定，最后才尝试编译为可执行或可验证的证据计划。谓词支持是证据升级，
不是问题提出的资格门：

- **W2**：谓词后端正常终止，产生可复核、带源归因的执行回执，并且结果落在该谓词
  声称的 soundness fragment 内；
- **W1**：需求义务和模型元素已精确绑定，可以定位问题，但没有适用的 sound 谓词或
  后端。W1 仍是 `semantic_hit`，必须进入命中和覆盖统计；
- **W0**：无法形成足够精确、可复现的绑定。W0 记录为 coverage gap，不算命中；
- **UNKNOWN**：后端不知道，不能改写成 violation，也不能用“没有结果”代替反例。

这条分层同时保护两个事实：没有谓词不能压制一个合理的问题；没有可执行回执也不能
把语义判断冒充成高等级证明。

谓词不支持不是发 issue 的资格门。只要义务与模型元素已经精确绑定，方法仍必须发出
该问题；若当前 19 个谓词或后端无法表达，则确定性状态机将其记为 W1，并计入
`semantic_hit`。只有绑定本身不足以复现时才是 W0。模型不得因为“没有谓词”而静默丢弃
问题，也不得为了覆盖率临时创造谓词。

后端不得调用 Python `inspect` 或任何旧的 `inspect_*` 后端。需要源位置、字段、签名或
调用关系时，必须在 `inputs`/`backends` 中实现有明确输入、输出和测试的独立算法，并把
算法版本与输入哈希写入回执；禁止以改名、包装或间接导入规避此门。

所有模型辅助步骤的每条结构化输出都必须带非空的 `reason` 或 `basis` 自然语言字段。
该字段解释本条结果所依据的输入、规则、边界和不确定性，供调试、审计和提示词迭代；
它不能替代确定性裁定，也不能被用来声称 W 或 D 等级。

### 1.1 D 裁定、W 裁定与 L 边界

`D2/D1/D0` 是方法对自己拟发布主张的裁定，不能读取或复制台账侧 D 标签。定义遵循
[`issue #189`](https://github.com/HansBug/research_ideas/issues/189) 的口径：

- **D2**：明确违反义务，且最强反驳不成立；
- **D1**：存在与事实相容的两种称职读法，两读并立；
- **D0**：可以合理解释为设计选择，或没有可陈述的违反义务。

只有 D2 与 D1 可以形成 release issue，并参与 hit、FP 和 precision；D0 只保留审计，
不参与结果。D 裁定必须由方法自己的 `semantics/adjudication.py`（或等价的确定性
裁定边界）给出理由、反驳及依据，不能让台账标签或模型口头标签代裁。

W2/W1/W0 同样由确定性逻辑根据绑定状态、谓词计划、后端状态、终止回执和来源归因
计算。模型输出中的 `witness_level` 只是候选字段，不能提升或覆盖状态机的裁定；
UNKNOWN、超时、资源耗尽和错误不得改写为 violation 或 W2。

L0/L1/L2 是台账侧属性。方法不生成、不裁定、不在 release issue 中声称自己的 L 等级；
评测时仅读取冻结台账的 L 字段并按台账分母切片统计。

### 1.2 v27 等价输入闭包与阶段信息流

新方法不能把 v27 的多阶段输入压缩成三个文本文件和一个自有 ModelIR。每个
PairInput 必须同时保留并在 ContextManifest 中记录哈希、schema version、algorithm
version、producer、reason 和 basis：

| 输入 | 方法中的唯一角色 |
|---|---|
| 编号 NL | 提取源需求义务和原句锚点 |
| PlantUML 与 canonical source IR | 作者源定位、源状态/迁移身份和源归因 |
| exact source/transition inventory | 从 canonical source IR 投影的精确源清单 |
| working contract、mapping、source trace | 映射、归属、边界和来源链约束 |
| FCSTM 与 owned ModelIR | 被测闭合模型、精确绑定和后端执行 |
| v27 inspect-derived facts | 只读的历史结构化事实上下文 |
| inspection-equivalent facts | 新包自有算法生成的版本化 inventory/diagnostic |
| verify facts | 新包自有有限图检查的结构化事实，不是 D/W 结论 |
| SMT/formal summary | 归一化的守卫/公式输入；solver_status=not_run 时不是求解器结果 |

PlantUML/canonical source IR 不能冒充 FCSTM 执行模型；FCSTM 不能冒充作者源定位；
inspection、verify 和 SMT facts 只能陈述确定性事实，不能直接生成 violation、W2 或 D。
后端和输入解析禁止 Python inspect、pyfcstm.inspect 和旧 inspect_* 后端；当前自有算法
版本为 inspection-equivalent.fcstm-graph.v2、verify-equivalent.finite-graph.v2 和
smt-input-normalization.v1。

方法编排保留以下固定阶段边界和信息流：

prepare -> nl_contract_extraction -> source_grounding -> model_grounding ->
exact_binding -> predicate_compilation -> backend_execution -> d_adjudication ->
w_publication

两个 grounding 分支互补：source branch 负责作者源身份和位置，model branch 负责闭合
FCSTM 元素、确定性 facts 和 19 谓词最小输入。方法 prompt 只接受该闭包，不接受冻结
台账答案、baseline 命中/FP、judge 示例或历史 release 输出。case report 只把身份、哈希
和状态 projection 放入 prompt；其完整文件仍以哈希保留在 receipt 中，历史
stage lineage/LLM/comparison/review payload 不进入生成上下文。

所有输入模型、LLM 响应和阶段 receipt 都使用 Pydantic model；字段必须有约束、完整
description 和非空 reason/basis。LLM 不输出 W/D/L；D 阶段只输出封闭的 semantic
grounding/defeater facts，方法代码将这些 typed facts 映射为 D2/D1/D0，W 则完全由
确定性状态机裁定。

### 1.3 确定性方法的准入边界

沿用 v27 已验证的边界：开放世界的自然语言语义必须由具名 LLM 节点判断，不能由文本
启发式伪装成确定性事实。NL 同义、指代、义务是否成立、条件作用域、NL 概念对应哪个
formal element、最强反驳以及台账外的语义同一性都属于 LLM semantic grounding 或
D adjudication。确定性代码只可处理公开语法和 typed AST、精确 ID/mapping、枚举与
引用闭包、版本化图/轨迹/SMT 算法、hash、预算和后端终止状态。

禁止使用关键词、substring、正则、词干、编辑距离、embedding、identifier 形状、唯一
候选补全或字符串相似度从自然语言推出语义结论。自由文本 `claim`、`expected`、
`observed`、`strongest_rebuttal` 只能保存为审计和 prompt 材料，不得进入 assertion
source/hash、D/W 或 source-attribution 的确定性语义裁定。逐字 quote 的 span 校验只
核对出处，不证明语义蕴含。任何无法由形式语法、模型 AST、精确引用关系或预先声明
soundness fragment 完美判定的步骤，都必须有 Pydantic 输出、非空 `reason`/`basis`、
模型调用和 usage/retry receipt。

这里的“禁止正则”针对自然语言语义代理，不禁止 parser 对公开 FCSTM/guard grammar
做语法识别。语法 parser 只能生成 typed AST/fragment；bounded backend 只在预先声明的
有限数值 guard grammar 内求值，无法解析的表达式必须返回 `UNKNOWN`。状态是否终止只
能来自 exact formal final-pseudostate edge，不能从 `final`、`terminal` 等状态名猜测。

## 2. 四族的学术叙事

四族按证据的产生方式，而不是按本台账中的标签划分：

| 谓词族 | 证据对象 | 能够声称什么 | 明确不能声称什么 |
|---|---|---|---|
| 结构 | 封闭作者源模型的元素、迁移、触发、守卫和挂接事实 | 模型中是否存在或等于指定结构事实 | 运行时消费、可达性、并发调度或变量后值 |
| 拓扑 | 从模型抽取的封闭图及其路径 | 存在/必经/避开/共可达等图性质 | 路径一定可执行、公平、时间满足或无死锁 |
| 轨迹仿真 | 一条场景、输入和调度完全落地的执行轨迹 | 某个事件被消费、状态到达、行为发生或状态保持 | 对所有调度的普遍结论、结构静态事实或终止证明 |
| 有界验证 | 闭合域上的守卫、状态空间或有界响应检查 | 在声明域、边界和假设下的量化反例/证明 | 把有限搜索视界当规范界限，或把未知当违反 |

结构、拓扑、轨迹和有界验证的后端必须在回执中声明其输入闭合条件、调度假设、搜索
边界、反例格式和 `UNKNOWN` 处理方式。图路径不能写成运行可行性；单条轨迹不能写成
全称性质；有限无反例不能自动写成无界证明。

## 3. 19 个谓词冻结与 W1-only 边界

现行公开 ID 只能来自注册表的 19 行：Structure 6、Topology 4、Trajectory 4、
Bounded Verification 5。派生宏必须展开为这些原子，不得新增公开语义。

以下命题暂时是 W1-only：containment、exact cardinality、initial existence/outdegree、
consumer scope、orthogonal runtime、hierarchy priority、trace variable delta，以及
其他需要额外外部规约的命题。它们可以在语义层提出，但不能为了覆盖率换名挤进核心表。

`deadlock_free` 只处理声明边界内的可达稳定配置；不能把 termination、livelock、fairness
或“最终一定到达”混成同一个谓词。`state_retained` 只描述轨迹区间的保持，不承担终止
分解。

## 4. 三类来源和严格准入

每个谓词至少要有命题匹配的来源登记，并把来源类型与实现边界分开：

1. **领域来源**：真实控制系统、状态机工程或需求分析中反复出现的检查命题；
2. **形式来源**：UML/状态机语义、性质模式、模型检查和相关标准中的正式定义；
3. **技术来源**：可复核的工具语义、算法定义或实现规范，用于说明后端怎样产生回执。

来源审查不是简单数引用。每个来源必须能回答“它是否真的提出了这个命题”，并记录
适用边界、是否 timed/parallel/hybrid、是否与当前 M=(S,E,V,Tr,A) 模型一致、是否
属于方法自身资料。逐条来源落点和状态见
[`related_work/provenance/CURRENT_SOURCE_AUDIT.md`](../../related_work/provenance/CURRENT_SOURCE_AUDIT.md)。
当前仍有部分候选集合未完成 T0、非并发、命题匹配和多源门槛，因此只能写“候选依据已
登记，严格准入待修复”，不能宣称全部通过。UML 2.5.1 明确没有把同事件守卫互斥列为
状态机强制约束；`guards_disjoint` 必须依赖独立且命题匹配的来源，不能从该标准反推。

来源数量不是 prevalence 分母，台账/v27 的出场量也不是学术证据。任何来源不足的命题
都应保持 W1-only，不能由 benchmark 频率反推学术普世性。

## 5. 变更审批门

新增谓词或修改定义必须同时提交以下材料，并在新版本注册表中记录迁移：

1. 独立于本台账的来源，且三类来源中的命题与拟议语义逐字匹配；
2. 一句话命题、最小输入、适用模型边界、soundness fragment、反例和 `UNKNOWN` 契约；
3. 学术叙事 review：说明它为何是领域通用检查，而不是单个 pair、字段名或台账模式的包装；
4. 兼容性报告：旧输入能否继续解析、旧结果如何解释、是否会改变 W1/W2 分层；
5. 注册表 schema 校验、来源审计、W1 命中契约、后端契约、mutation 和 prose non-interference 测试；
6. 独立审查者批准，并在变更记录中写出被拒绝的替代方案。

覆盖率不得设成凌驾于学术可靠性的硬门。默认目标是覆盖大部分 L2，但低频边角需求
可以诚实地 W1；“达到 90%”不能成为新增谓词的理由。

## 6. 发布前自审清单

- [ ] 19 个 ID 唯一，族计数为 6/4/4/5，宏没有新增语义。
- [ ] 每条命题都有最小输入、soundness 边界和 `UNKNOWN` 处理。
- [ ] 每个来源 ID 都能回到原始档案，且来源类型、命题匹配和并发/计时边界已核对。
- [ ] 没有把 containment、cardinality、图路径、单轨迹或有限搜索写成更强的命题。
- [ ] 没有谓词时仍输出 W1；W1 计入 `semantic_hit`；W0 和 UNKNOWN 不被静默升级。
- [ ] 设计覆盖数字标明是 expressibility snapshot，不冒充新实现实测结果。
- [ ] 论文叙事不使用“从 54 pair 归纳”“来源数量代表普遍率”等循环或过强说法。
- [ ] 旧实现只通过 archive 指针出现，现行入口不把 `prototype` 当方法名。
- [ ] D2/D1/D0 由方法自行裁定；只有 D2/D1 进入 release、hit 和 FP，D0 仅审计。
- [ ] W0/W1/W2 由确定性状态机计算，模型不能自报等级；L 只从台账读取，方法不输出 L。
- [ ] 每一步、每一条模型结构化输出都有非空 `reason` 或 `basis`，且说明输入、规则和边界。
- [ ] 后端及输入解析不调用 `inspect`；类似能力使用自有、可测试且有版本的算法。
- [ ] 正式运行复用公共 `utils.agent`/`utils.llm` 与 LangGraph/respond，不从 `feedback_loop`
      私有实现反向导入；19 个谓词保持冻结。
- [ ] provider error 原地重试且前序 attempt 不计费；格子因此死亡时原地重试该格一次；
      其它错误及 retry 计费并按 bug 修复，不以重跑掩盖故障。
- [ ] 每条 W2 都有完整谓词逻辑、绑定输入、编译源码及哈希、真实后端结果、终止状态、
      反例/轨迹、来源归因和 `reason`/`basis`。

## 7. 迁移后的效果目标

新实现的工程目标是：在相同台账、相同 54 个 pair、相同最终发布边界和可比的独立
judge 下，使用本注册表和新规则取得与历史 v27 正式结果**大体相当或更好**的 hit 与
FP/precision 表现。v27 只是量级参照，不是逐格相等或绝对完美的硬门；达到大体相当即可，
若超过 v27 则如实记录为更好。这里不承诺逐格、逐轮或逐个数字复现，也不要求每个边角
案例都覆盖；不得为了追平或超过历史数字放宽学术来源、把 W1 冒充 W2、把 `UNKNOWN`
改成 violation，或新增覆盖专用谓词。

正式对账必须同时报告整体、L2、D2×L2 的 `hit@1`/`hit@3`/`hit@all`、release FP/
precision、eligible rate、W0/W1/W2/`UNKNOWN` 分布和成本。比较前先冻结 v27 的具体报告、
台账版本、judge 和分母；若新实现与 v27 有差异，优先按绑定、证据等级、后端边界和
表示债务解释，不能事后改比较口径。新实现即使 semantic hit 与历史相当，也必须单独
证明其 W2 回执和来源归因闭合。
