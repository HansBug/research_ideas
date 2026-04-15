# Expert Review Agent 调研笔记

本文档用于约束 `reproduction` 下拟实现的通用化“模拟专家评审 agent”。目标不是凭经验拍分，而是把状态机/行为建模领域中较稳定的学术判断口径，转成可执行的 agent rubric、tool 使用策略和结构化 reason text 模板。

## 1. 为什么不能只做 ref/pred 文本比较

在状态机建模里，“好模型”不等于“和参考解长得像”。

至少要区分四层：

1. **语法/记法层**
   模型是否符合 UML / SysML / PlantUML / Umple / TTool 对应语法与记法约束。
2. **语义/需求层**
   模型是否覆盖了需求中的关键状态、触发、条件、动作、异常分支和约束。
3. **行为层**
   即便结构不同，只要对外可观察行为一致或近似一致，也可能是合理设计。
4. **可理解/可维护层**
   一个模型可能“能跑”，但因为结构过度复杂、命名混乱、不可追踪，仍然是低质量模型。

因此 expert-review agent 不能只问“pred 和 ref 是否完全一致”，而要问：

1. 它是否是合法模型。
2. 它是否满足该论文真正关心的评审维度。
3. 当结构不同但行为合理时，应该给多少 credit。
4. 结论能否回溯到具体 requirement / state / transition / evidence。

## 2. 建模质量的基础框架

### 2.1 SEQUAL / 概念模型质量框架

建模质量领域很经典的一条线是 Lindland / Krogstie 的概念模型质量框架。

- `Defining quality aspects for conceptual models` 将模型质量拆成至少三条主线：**syntactic**, **semantic**, **pragmatic**，并进一步扩展到 social 维度。
- 其中：
  - **Syntactic quality**：模型与建模语言的对应程度，也就是语法/记法是否正确。
  - **Semantic quality**：模型与领域事实/问题域的一致程度，核心关注 **validity** 与 **completeness**。
  - **Pragmatic quality**：模型与读者理解的一致程度，核心是 **comprehension**。

这对 agent 设计的直接影响：

1. 评分维度不能只放一个“overall quality”。
2. 至少要显式拆出：
   - `notation_syntax`
   - `semantic_validity`
   - `semantic_completeness`
   - `pragmatic_clarity`
3. 对于需要多人一致认可的场景，还要补一个 `social_agreement_risk` 或 `reviewer_disagreement_risk`，表示当前判断是否容易引发专家分歧。

相关来源：

- Krogstie, Lindland, Sindre, *Defining quality aspects for conceptual models*:
  https://folk.idi.ntnu.no/krogstie/publications/1995/ISCO3/fulltext.pdf
- 其中 `syntactic / semantic / pragmatic` 与 `validity / completeness / comprehension` 的框架可在文中对应位置看到。

### 2.2 状态机不是孤立对象，行为模型还要看完整性/一致性/健全性

`Evaluating Behavioral Correctness of a Set of UML Models` 把一组 UML 行为模型的正确性拆成：

1. **completeness**
2. **consistency**
3. **soundness**

这很适合 `Nimbus` 这类不是“单一图对单一图打分”的论文，也适合我们做通用 agent 时的高层判断：

1. **Completeness**
   必要元素是否都出现了，是否缺少关键状态/消息/约束。
2. **Consistency**
   不同工件之间有没有冲突；同一工件内部是否自洽；需求叙述与状态迁移是否一致。
3. **Soundness**
   模型内部行为是否合理，前置/后置条件、状态不变量、异常路径是否说得通。

对 agent 的影响：

1. 通用入口里应允许 `review_mode=single_model` 与 `review_mode=model_set`。
2. 在 `model_set` 或 `req+pred(+ref)` 场景下，必须能产出：
   - `completeness_subscore`
   - `consistency_subscore`
   - `soundness_subscore`
3. 这些子分都要带 requirement-level 或 element-level 的 reason text。

相关来源：

- Shinkawa, *Evaluating Behavioral Correctness of a Set of UML Models*:
  https://www.scitepress.org/Papers/2012/40822/40822.pdf

## 3. “两个状态机是否算合理接近”不能只靠图形相似

### 3.1 行为比较应至少区分结构等价、行为等价、近似行为兼容

状态机比较的经典形式化方法不是“字符串一样”，而是 **trace equivalence / simulation / bisimulation** 这一类行为关系。

- `The Equivalence of Statecharts` 把 Statecharts 的等价性建立在 **bisimulation on configurations** 上。
- `Model-checking process equivalences` 明确指出：动态系统“行为相同”没有唯一标准，从 **bisimulation** 到 **trace equivalence** 存在一条谱系。
- Uppsala 的 bisimulation 页面也强调：bisimulation 用于把**行为等价**的系统关联起来，并能做 state-space reduction。

这对 agent 的影响非常直接：

1. `comparison_policy` 不能只有 `exact_match`。
2. 至少要支持：
   - `exact_structure_match`
   - `component_semantic_match`
   - `trace_compatible`
   - `bisimulation_like`
   - `rubric_only`
3. agent 提示词里必须明确：
   - 结构不同但可观察行为等价时，不应直接判错。
   - 若论文评审是人工语义比对，则允许“名称不同但语义同义”的 credit。
   - 若论文评审强调专家设计质量，则要额外考虑是否引入多余复杂性。

相关来源：

- `The Equivalence of Statecharts`:
  https://durham-repository.worktribe.com/output/1168092/the-equivalence-of-statecharts
- `Model-checking process equivalences`:
  https://www.sciencedirect.com/science/article/pii/S0304397514006574
- Uppsala `Bisimulation`:
  https://www.it.uu.se/research/docs/fm/apv/bisim.html
- NASA `Statecharts Via Process Algebra`:
  https://ntrs.nasa.gov/citations/19990116905

### 3.2 在工程评审里，形式等价通常需要降级成“可观察行为兼容 + 要点覆盖”

论文里的人工评审大多不会真的做形式化 bisimulation 证明，但它们隐含地在看这些东西：

1. 核心状态是否都被表达了。
2. 关键触发和异常路径是否被保留。
3. 守卫和动作是否改变了系统可观察行为。
4. 是否把不该出现的行为也加进去了。

所以 agent 更现实的做法是：

1. **先做 element-level 抽取**
   状态、迁移、事件、守卫、动作、层次、并发区域、消息、块、变量。
2. **再做 requirement-level trace**
   每条需求是否有对应元素支持。
3. **最后做 behavior-level judgement**
   当前 pred 是否引入、遗漏或改变关键行为。

也就是说，agent 要从“形式等价证明器”降级为“有工程依据的行为兼容评审器”。

## 4. 可读性/可维护性不是附属项，而是状态机质量的重要部分

### 4.1 结构复杂度会显著影响状态机可理解性

`The impact of structural complexity on the understandability of UML statechart diagrams` 的实验结果很明确：

1. 状态图的**状态数、事件数、守卫数、迁移数**等控制流复杂度会显著影响可理解性。
2. **entry/exit actions** 会形成单独的复杂度维度。
3. **do/activities** 数量也会显著降低可理解性。

换句话说，一个模型就算“功能覆盖多”，如果：

1. 状态爆炸，
2. 无必要地引入大量 guard/action，
3. 层级深但没有清晰模块边界，

那它在专家评审里也不应拿高分。

相关来源：

- Cruz-Lemus et al., *The impact of structural complexity on the understandability of UML statechart diagrams*:
  https://alarcos.esi.uclm.es/ALARNET2/FILES/Articulos/2010-Information%20Sciences-CruzLemus.pdf

### 4.2 状态机理解性可以作为独立质量信号

`A metric towards evaluating understandability of state machines: An empirical study` 提出 SUM，并显示其与理解效率/正确率显著相关。

这意味着 agent 不应该只给“正确/错误”，还要给：

1. `understandability`
2. `design_simplicity`
3. `maintainability_risk`

这几类判断。

虽然我们不会在当前版本里完整复刻 SUM 数学定义，但 prompt 和工具层应该显式考虑：

1. cohesion / coupling 风险，
2. 过多跨状态耦合，
3. 过多无解释动作，
4. 为了覆盖需求而引入不必要复杂结构。

相关来源：

- Chang et al., *A metric towards evaluating understandability of state machines: An empirical study*:
  https://www.sciencedirect.com/science/article/pii/S0950584913001572

### 4.3 一些 statechart 特征和维护缺陷有关

`Statechart features and pre-release maintenance defects` 指出，某些 statechart 结构特征会和 pre-release maintenance defects 相关，并给出避免坑点的建议。

这对 agent 的意义是：

1. 如果 pred 明显引入高风险复杂结构，不能因为“元素更多”就给高分。
2. expert-review 结果里需要单独保留：
   - `overmodeling_risk`
   - `unnecessary_complexity_risk`
   - `maintainability_risk`

相关来源：

- Heidenberg et al., *Statechart features and pre-release maintenance defects*:
  https://www.sciencedirect.com/science/article/pii/S1045-926X%2808%2900030-X

## 5. 需求到模型的可追踪性必须进入 agent

状态机从需求生成时，一个高分模型应该能回答：

1. 这条状态/迁移是由哪条需求支持的？
2. 这条需求在模型里落到了哪里？
3. 哪些需求没有落到模型里？
4. 哪些模型元素没有需求依据，可能是 hallucination？

这条线来自 requirements traceability 的经典研究。Gotel/Finkelstein 对需求可追踪性的定义强调：要能沿着 requirement 的生命周期向前向后追踪。

对 agent 的设计要求：

1. 输入不只收 `pred_model` 和 `ref_model`。
2. 必须允许输入：
   - `requirements_text`
   - `requirements_items_json`
   - `traceability_policy`
3. 输出必须包含：
   - `requirement_trace_results`
   - `unsupported_model_elements`
   - `unrealized_requirements`

这也是 `llms_emp` 里 semantic hallucination 和 `ttool-ai` 里 adequacy to specification 的共同基础。

相关来源：

- Gotel & Finkelstein 相关 traceability 文献入口：
  https://csis.pace.edu/~ogotel/research/GOTEL93%20An%20Analysis%20of%20the%20Requirements%20Traceability%20Problem.pdf

## 6. 官方规范给 agent 的最低底线

无论论文怎么打分，状态机评审首先不能脱离 UML / SysML 的基本规范。

- UML 2.5.1 官方规范页面：
  https://www.omg.org/spec/UML/2.5.1/About-UML
- SysML 1.6 官方规范页面：
  https://www.omg.org/spec/SysML/1.6/

这对 agent 的约束是：

1. 语法类评审时要区分“工具语法”和“概念语法”。
   - 例如 PlantUML 合法，不代表 SysML/UML 语义就合理。
2. 结构类评审时要区分：
   - 初始状态、终止状态、普通状态、复合状态、历史状态、并发区、触发、守卫、效果。
3. 出现明显违反常规状态机建模规则的情况时，要单列出来而不是混到 overall reason 里。

## 7. 四个 baseline 对应的真实评审方式

这一段直接服务后续 agent preset。

### 7.1 `Structure/Event-Driven`

本质上是**人工语义比对后的组件 TP / FP / FN 统计**。

论文和公开实验资源把评估拆到组件层：

1. `States`
2. `Transitions`
3. `Guards`
4. `Actions`
5. `Hierarchical states`
6. `History States`
7. `Parallel Regions`

因此这个 baseline 的 agent preset 应该采用：

1. `component_semantic_match`
2. 允许同义命名与近义行为描述
3. 输出 TP / FP / FN 风格的结构化结果
4. 每个组件必须有 reason text，解释为什么算 matched / missing / extra

本地论文整理入口：

- [structure-event paper content](../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper_content.txt)

### 7.2 `llms_emp`

本质上是**多阶段质量检查**：

1. PlantUML/格式正确性
2. SysML grammar 正确性
3. semantic correctness / hallucination 检查
4. 与参考模型的 TP / FP / FN / F1

因此该 preset 不应该只输出一个 F1，而要拆成：

1. `format_compliance`
2. `grammar_compliance`
3. `semantic_alignment`
4. `hallucination_risk`
5. `reference_match`

并且要明确：这篇论文的评价本来就不是纯人工单次打分，而是**半自动 + 人工语义检查**的混合流程。

本地论文整理入口：

- [llms_emp paper content](../baselines/llms_emp/paper_content.txt)

### 7.3 `ttool-ai`

本质上是**人工 rubric 评分**，而且非常像课程/建模作业评分。

论文明说 grading criteria 包括但不限于：

1. 图是否符合 specification
2. 在 TTool simulator 中观察到的行为是否与 specification 一致
3. blocks 间 exchanges 是否合理
4. 图的可读性
5. blocks / states 数量是否合理
6. 命名是否一致
7. 是否存在声明了但未在状态机中使用的 attributes
8. TTool syntax checker 的 errors / warnings

因此这个 preset 不能硬套 TP/FP/FN，而要采用 `rubric_only` 或 `rubric_plus_counts`。

本地论文整理入口：

- [ttool-ai paper content](../baselines/ttool-ai/paper_content.txt)

### 7.4 `Nimbus`

这篇工作更偏**需求捕获、建模、验证与评估**，不是一个纯生成 benchmark。

更适合的 expert-review 方式是：

1. requirement completeness
2. state/rule consistency
3. abstraction/refinement quality
4. traceability
5. verification/simulation readiness

也就是说，这个 baseline 应采用 `completeness + consistency + soundness + traceability` 风格的 rubric，而不是强行对齐到单图 F1。

本地论文整理入口：

- [Nimbus paper content](../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/paper_content.txt)

## 8. 由调研反推 agent 的评审维度

### 8.1 通用维度

后续 agent 默认应支持以下维度集合中的任意子集：

1. `notation_syntax`
2. `grammar_conformance`
3. `semantic_validity`
4. `semantic_completeness`
5. `requirement_traceability`
6. `behavioral_consistency`
7. `behavioral_soundness`
8. `reference_alignment`
9. `hallucination_risk`
10. `design_simplicity`
11. `pragmatic_clarity`
12. `maintainability_risk`
13. `simulation_readiness`
14. `verification_readiness`

### 8.2 每个维度的最小输出要求

每个维度都必须输出：

1. `dimension_name`
2. `score` 或 `judgement`
3. `reason_text`
4. `evidence_items`
5. `trace_links`
6. `confidence`

其中 `reason_text` 不能只写“looks good / partially matched”，必须说明：

1. 依据了哪些 requirement / model element / tool finding
2. 为什么加分
3. 为什么扣分
4. 如果结构不同但仍给分，依据是什么

## 9. 对 prompt 设计的直接约束

基于以上调研，expert-review prompt 必须满足以下硬要求。

### 9.1 先明确 review contract，再开始评分

prompt 必须先要求 agent 内部确认：

1. 当前任务是 `syntax check` / `reference comparison` / `rubric grading` / `model-set review` 中哪一种。
2. 当前使用的比较政策是：
   - exact
   - semantic component
   - trace compatible
   - rubric only
3. 当前输出 schema 必须是什么。

### 9.2 评分前必须先做证据抽取

prompt 不能直接说“请评分”，而要要求 agent 先完成：

1. requirement extraction
2. model element extraction
3. trace candidate generation
4. mismatch inventory
5. risk inventory

只有完成 inventory 后，才进入评分。

### 9.3 对“合理差异”必须给正当 credit

prompt 必须明确写出：

1. 不要因为命名不同就直接判错。
2. 不要因为状态拆分更细就直接判错。
3. 若 pred 比 ref 更复杂，必须判断这种复杂度是必要细化还是无依据膨胀。
4. 若 pred 与 ref 结构不同但需求覆盖和行为后果一致，应给部分或大部分 credit，并在 reason text 中说明。

### 9.4 对 hallucination 必须单列

在需求到模型生成任务中，以下内容应被显式视为 hallucination 候选：

1. 无需求依据的状态
2. 无需求依据的 transition
3. 无需求依据的 guard/action
4. 违反领域约束的 block/signal/attribute

### 9.5 对可理解性必须单列而不是混入总体分

prompt 必须要求 agent 区分：

1. “模型可能是对的”
2. “模型设计得是否清晰、易懂、易维护”

这两件事。

## 10. 对后续实现的具体要求

后续 expert-review agent 代码应据此满足：

1. **入口通用化**
   不只输入 `ref_model` 和 `pred_model`，还要允许输入：
   - `requirements_text`
   - `rubric_text`
   - `dimension_defs`
   - `comparison_policy`
   - `output_schema`
2. **工具分层**
   至少要有：
   - 结构抽取工具
   - 计数与复杂度工具
   - traceability 工具
   - mismatch inventory 工具
   - hallucination inventory 工具
3. **评分分层**
   先抽证据，再按维度评分，最后聚合 overall。
4. **结果结构化**
   overall 和每个 subscore 都必须有可追溯 `reason_text`。
5. **允许 baseline preset**
   但 preset 只能是对通用框架的参数化，不能写成四套彼此割裂的硬编码 judge。

## 11. 结论

后续 agent 的 prompt 和 rubric 不应再基于“猜一个专家会怎么想”，而应明确站在以下几条线上：

1. **SEQUAL 质量框架**
   语法、语义、可理解性至少三层。
2. **UML 行为正确性**
   completeness / consistency / soundness。
3. **需求可追踪性**
   requirement-to-model coverage 与 unsupported element 检查。
4. **状态机行为比较**
   结构相似不等于行为相同，结构不同也不必然错误。
5. **复杂度与可维护性**
   状态、迁移、guard、action、entry/exit/doActivity 的膨胀会显著降低理解性并增加缺陷风险。

基于这份笔记，下一步 expert-review agent 的 prompt 将采用“先证据抽取、再分维度评分、最后聚合”的结构，而不是一步到位给一个模糊总分。
