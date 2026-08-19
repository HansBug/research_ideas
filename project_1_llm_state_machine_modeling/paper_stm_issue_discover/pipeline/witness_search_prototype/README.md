# 证据携带式 issue discovery 原型

本目录是 paper1 核心方法的探索性实现。它与已归档的 v46 loop 分离，运行时不加载缺陷台账或 X1v2 结果。

领域来源、五类 typed obligation、完整节点合同、W2 Evidence Program、D/W/L 与完整54 pair统一评测协议见 [DOMAIN_DERIVED_METHOD.md](./DOMAIN_DERIVED_METHOD.md)；逐 operator 的 PR #183 复用、新增补检与证据缺口见 [TYPED_OBLIGATION_PROVENANCE.md](./TYPED_OBLIGATION_PROVENANCE.md)。

当前固定设计包含三个 pair 级 LLM 角色。LLM-A 调用一次；LLM-B 在同一冻结输入上运行 `contract_structure_contrast` 与 `behavior_consequence` 两个互补分支；LLM-C 读取整格压缩 dossier，一次为全部 finding 输出独立 D 决策。节点内只对 structured-output/schema 错误做一次携带具体错误的定向修复。迭代目标按“全量 hit 显著领先 → L2 大部分命中且显著领先 → FP 不劣于 baseline → 全量总体成本不超过 25x”排序，完整定义见 [final_output_metrics_policy.md](../../discover_matrix/docs/protocol/final_output_metrics_policy.md)：

1. `paper1_contract_extraction` 只读取 numbered NL，抽取 initial、containment、按 source 分组的 direct-transition、required-state、required-event-scope contract 和跨句复用的 concept ID。
2. 两个 `paper1_discovery_grounding` 分支读取完全相同的 raw contract、NL、作者源 PlantUML、带语义映射注释的 FCSTM、压缩后的 `pyfcstm inspect` 事实和精确 source inventory，分别偏重契约/结构/跨边对照与可达性/响应/终止后果；开放候选取 exact structured union，确定性 formal scout 与执行后端只运行一次。
3. `paper1_d_adjudication` 首轮读取整格全部 finding facet，一次为每条 facet 独立输出 `D2/D1/D0`，并在同一次调用中用 exact `finding_key` 标记报告级语义重复；validator 冻结合法 decision，若存在非法 decision，`paper1_d_targeted_repair` 至多再调用一次且只读取非法子集、对应 dossier、逐条错误和只读的冻结 decision 摘要，失败时仅该子集降为 `D_UNRESOLVED`。

LLM 不选择 Python、pyfcstm 谓词、证明模板、证明后端、W 或最终 L。每个 B 分支先为所有已实现的语义概念输出一次全局 exact-ID `concept_bindings`；initial/containment raw contract 使用稀疏 `rejected/unresolved` veto，而 transition raw contract 必须对每个 target 穷尽返回 exact normative endpoint 与 `observed_transition_id` 或 unresolved。这个区别来自问题本身：概念映射后可以机械检查 containment，但“哪条作者边语义上实现了某个 NL 条件或动作”不能用字符串规则判定，必须由 LLM 显式落账。确定性 assembler 只按 concept ID、索引和 exact formal ID 合并，并保护原始 `nl_line`、`condition`、`priority` 和 concept ID 不被改写；已满足 transition contract 会在真实执行后机械过滤。确定性编译器将每个语义关系映射到 13 个证明模板和 4 个物理后端之一：源/制品静态检查、守卫 SMT、拓扑证明或 FCSTM trace/有界形式执行。断言必须真实运行后才能得到 W2；新增 `transition_target_consistency` 允许 LLM 先语义判定两个 NL 行为具有相同目标角色，再选择被测边、参照边和规范目标，确定性层只核验 exact ID、正式端点与 FCSTM 映射并执行双边断言，绝不从 label、条件字符串或名字推导等价。

论文一等表达面是 `ElementObligation`、`AttachmentObligation`、`GuardSetObligation`、`GraphObligation` 与 `TemporalObligation` 五类 Pydantic discriminated union。旧 `EvidenceGoal=(relation, bindings, expected)` 仅保留为 compiler lowering record；exact operator 与 relation 的兼容性由确定性表校验，后端仍完全由 compiler 选择。执行支持不作为第六类义务，而由 compiler 产生 `SupportDisposition`：`executable/W2 ceiling`、`located_only/W1 ceiling` 或 `prose_only/W0 ceiling`。relation-specific 必需字段由 compiler 而非 schema 检查，使单个非法 Goal 降级而不杀整格；候选必须同时携带 `basis` 与 `observed_fact`，D dossier 必须携带 `rationale` 和 defeater 说明，但这些自然语言字段只供审计/debug，不得参与确定性语义控制。候选只有在编译后真实运行并获得 terminal counterexample、artifact/assertion hash、source certificate 和 semantic receipt 时才可能成为 W2。

LLM-B 不再逐条复述全部 initial/containment `grounded` contract。被省略的这两类普通 contract 只有在其 concept ID 已获得全局 exact-ID binding 时才可由 assembler 接受；`rejected` 表示 LLM-A 把 NL 关系抽错，`unresolved` 表示仍有多种称职读法，二者都是执行 veto。transition contract 例外地要求穷尽 indexed binding，但只输出 source、target index、normative target 与 observed transition ID，不复述 claim/obligation；这是用少量结构化字段换取语义明确和后续 satisfied-filter，而不是恢复冗长全文。fresh 分支必须对 raw group 和 target index 完整、唯一且不越界，纯结构合同失败会让该分支整体隔离并禁止执行，绝不靠 concept 名或文本猜回缺失 binding；旧 replay 走单独兼容路径。assembler 只消费结构化枚举与 exact ID，绝不从 reason 文本中搜索“错误”“歧义”等字样。

## 语义判定纪律

运行时严禁用正则、关键词、`and/or` 等连接词、词干、编辑距离、embedding 相似度阈值、substring 或 identifier 形状去替代 NL 语义判断。NL 的同义关系、指代、条件作用域、义务成立与 source-element 对应关系必须由明确的 LLM 节点输出并进入审计记录；确定性代码只处理可完美判定的问题，例如 schema、精确正式 ID 是否存在、transition 端点是否一致、AST/inspect/trace/SMT 结果、hash、预算和逐字引用完整性。若 LLM 无法可靠绑定，则必须保留 unresolved/coverage gap 并降为 W1/W0，不能用字符串启发式补答案。

这是一条方法准入纪律，不是代码风格建议：任何 deterministic stage 只要从 NL、claim、obligation、identifier 名称或自由 label 的词面内容推导同义、因果、义务、缺陷类别或 finding-to-ledger 等价关系，该 stage 就不能进入正式方法。最直接的机械审计是 prose non-interference：formal goal、exact binding 和正式制品不变时，改写所有散文不得改变 assertion、verdict、W、L 或 source certificate；若改变，说明确定性层越权读取了文本语义。

任何不能由形式语法、模型 AST、精确引用关系或已声明 proof fragment 完美判定的步骤，都必须显式归属某个 LLM 角色，并在 run record 中保存其模型、prompt、raw output、structured output 和 usage。不得把隐藏的字符串代理包装成“预处理”“召回增强”或“候选缩减”；逐字 quote span 校验只能证明引用来自输入，不能证明该 quote 支持某项义务。正式论文应据此向 reviewer 陈述为“LLM 负责开放世界语义判断，确定性 proof compiler 只负责闭合世界形式求值”，而不是声称代码从文本中推导了语义。

Schema/validator 也受同一边界约束：它只能检查枚举、必填、精确 ID、引用闭包、数值预算和正式语法等可完美判定的合同，不得把自由文本长度、特定词出现与否、解释措辞或 reason 内容变成语义准入门。特别是 `grounded/rejected/unresolved` 的含义由 LLM 枚举字段承载，确定性 assembler 只能读取枚举，不能解析 reason，也不能因为一段正确解释较长而触发整次 schema repair。

形式语言的词法解析不属于上述禁用项，但边界必须可审计：正则或 parser 只能按公开语法把 PlantUML、FCSTM、guard expression、正式引用或 schema ID 解析成 token/AST，后续结论必须来自 AST、精确 ID、图算法、trace 或 SMT；它们不得在原始 NL 上搜索某个单词后直接产生语义结论。换言之，允许 guard lexer 解析 `&&` 后送入 SMT，不允许搜索英文 `and` 来猜两个自然语言条件是否属于同一迁移。

当前 L0 scout 新增一个失败闭合的 `paper1.uml251_transition_label.guard_only.v1` profile。它只消费 canonical source AST 中 transition 的 `raw_label` 字段，只接受完整形状为 `[ guard_body ]` 的形式片段，并且把 guard body 当作不透明载荷；它不读取 NL、不解释 guard 内部单词、不声称 PlantUML 自身提供了 guard parser。根据声明的 UML 2.5.1-derived profile，该片段可确定为“无显式 trigger、有 guard、无 effect、隐式 completion trigger”；随后由 source AST 图结构判定 composite 是否存在到自身 final pseudostate 的边。超出该片段一律不分类，不使用近似规则补全。

若上述 source 断言得到反例，但 FCSTM working contract 与 `pyfcstm inspect` 又显示转换器已经把 opaque label 投影成实际声明并消费的 event，原型会保存已执行的 source assertion、FCSTM projection audit 和 `representation_debt`，但机械定级仍是 W1。原因是 W2 的被求值介质必须是当前 FCSTM，而转换已经改变或修复了待检 source 语义；任何 source-only 反例都不得借转换后的可执行行为冒充 W2。

W2 证明的是“在已记录的语义绑定前提下，编译后的断言在确切 FCSTM 上得到 terminal verdict”，不是“确定性代码证明了 NL 与形式元素同义”。每份相关 certificate 都必须保存 v2 `semantic_binding_receipt`：LLM authority 必须回指真实 `llm_call_id`，并以 hash chain 绑定模型/profile、system/user prompt、raw/parsed output、semantic plan、grounded contract/evidence plan、候选和 formal binding transforms；formal authority 必须明确标成 `formal_fact_only` 且 `semantic_decision_claimed=false`。run-level audit 会把 receipt 与同一 record 的 immutable observation 和当前 plans 逐项对拍，缺失、篡改或错链都不能通过 W2/实验资格门。后续 D 裁决与环外 blind precision judge 负责继续约束“真实 LLM 作出了绑定但绑定本身仍然错误”的 false positive。

确定性执行遵守可回归验证的语义非干涉合同：formal `EvidenceGoal`、exact binding 与模型制品不变时，任意改写 `claim`、`obligation`、`observed_fact` 都不得改变 compiled assertion、terminal verdict、W 或 source certificate。散文不进入 assertion code/hash，只进入报告和 D dossier；改变 formal goal 或 binding 必须来自新的 LLM 语义决策与 receipt。

每个保留的“技术原因 × 规范义务”facet 记录三条相互独立的轴：

- `witness_level`：机械派生的 `W2/W1/W0`。
- `l_level`：根据证明关系机械派生的 `L0/L1/L2`。
- `d_decision`：以整格一次调用、逐条独立给出的 `D2/D1/D0`；只有 schema/合同非法的 decision 子集可进入一次 targeted repair。

W2 还必须带有 terminal counterexample certificate，其中包含确切 FCSTM hash 和 compiled assertion hash。source attribution 是另一份独立证书，因为 FCSTM 上的反例本身不能证明作者源 PlantUML 有缺陷；静态 FCSTM 缺失若没有作者源证书只能标为 unattributed，不能借用 `safe_runtime_path`。W1/W0 假设会作为 coverage-gap facet 保留并接受 D 裁决，但不能进入 `confirmed_issues`。

最终报告采用两级去重。确定性层先按 source certificate 导出的 exact cause key 合并同一技术原因下的 facets；随后只消费 LLM-C 在整格 D 中给出的 `duplicate_of=<earlier finding_key>` 边。LLM-C 负责判断“相同 exact source elements/transition set、相同 violated property、相同最小修复”；确定性层只检查 earlier-key 引用方向、exact source-certificate cause 约束和 canonical `GoalRelation + bindings` property signature，绝不从 claim 措辞推断语义或最小修复。cluster 保存全部 `cause_keys`、`facet_keys` 和 `deduplicated_by_d` receipt，因此合并不会覆盖每个 facet 自己的 D/W/L。

完整的阶段契约、后端策略、pilot 证据、评测设计和泄漏边界见 [METHOD_DESIGN.md](./METHOD_DESIGN.md)。

面向论文写作的实验结果与限制汇总见 [PILOT_REPORT.md](./PILOT_REPORT.md)。

当前尚未证明 145 条台账全部或大多数可表达。本轮只完成全部 `id/D/L/axes/summary` 的粗粒度通览，已经确认 region/正交并发、具名 action/effect、精确 condition、state kind、层次优先级/history 和独立 trigger 集等缺口；逐条 feasibility 矩阵仍待完成。表达面唯一审计真源和“领域来源 → obligation taxonomy → Goal algebra → sound backend → 冻结后 54 pair 评测”的构建纪律见 [EXPRESSION_SURFACE_AUDIT.md](./EXPRESSION_SURFACE_AUDIT.md)。

## 使用方法

从仓库根目录运行：

```bash
# 使用 utils.llm、三个 LLM 角色和 immutable stage record 运行 LangGraph；D 对整格一次裁决。
python -m \
  project_1_llm_state_machine_modeling.paper_stm_issue_discover.pipeline.witness_search_prototype.graph \
  --case 0000 --profile claude-opus-4-7 \
  --output-dir runs/paper1/witness-search/0000-opus47

# 复用已成功的 contract/discovery-grounding plan，但在当前 FCSTM 上重新执行全部断言，并重新调用 D。
python -m \
  project_1_llm_state_machine_modeling.paper_stm_issue_discover.pipeline.witness_search_prototype.graph \
  --case 0000 --profile claude-opus-4-7 \
  --replay-plans-from runs/paper1/witness-search/0000-opus47 \
  --output-dir runs/paper1/witness-search/0000-replay

# 确定性回归测试。
PYTHONPATH=. python -m pytest \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/witness_search_prototype/tests \
  -q
```

真实调用通过 `utils.llm` 使用仓库 `.llmconfig.yml` 中的 profile；环境变量不是运行时凭据入口。

## 工程调试记录

`runs/paper1/witness-search/` 保留原型迭代的完整输入、调用、usage、候选、证书、异常与 replay 记录。这些运行只用于检查既定方法合同是否被实现，例如 structured output 是否可恢复、单候选异常是否降级、W2 是否真实执行、source attribution 是否闭合、D 是否逐 finding 输出，以及四类 token 成本是否完整；它们不参与方法语义归纳，也不提供论文效果结论。

调试中发现的错误只能触发实现修复或回到领域文献重新取证。任何新的 obligation、relation、D 纪律或 prompt 语义约束都必须先有独立领域来源和合成测试，不能由某个真实 pair 的命中或漏报直接推出。方法效果只在完整 54 pair、145 条台账的统一 benchmark evaluation 中报告。

## 原型边界

- 全部输出仍属探索性结果，不是论文实验结果。
- source graph 检查只在声明的顺序片段内保证精确；并发和不支持的守卫语义会降级，不会被提升为 source issue。
- mapping contract 证明局部因果关系，不证明整个 converter 的行为等价。
- progressive formal scout 只能输出 exact diagnostic `FormalFact` 和事前登记的 `OracleRule`；它不解析 diagnostic message，也不把规则直接当作 NL-derived obligation，规则对当前需求是否构成缺陷必须由 LLM-C/reference judge 裁决。
- `(cause, obligation)` facet 是 D 的判定单元，报告级只按精确 cause key 聚类并保留全部 obligation facet；正式实验前仍需冻结聚类协议和 matching 口径。
- 正式成本口径是同一 configured model 内的美元倍率，不做跨模型 `<25×` 比较。`.llmconfig.yml` 只配置 input、output、cache read、cache write 四个 USD/M token 单价及来源；当前不模拟峰谷、长上下文、TTL 或供应商账单的全部细节。schema、output-limit、内容返工和其他非 provider 错误的所有 prototype attempt 都累计费用；只有 typed provider/transport failure 之后确实发起下一次 retry 时，前序失败 attempt 才可标为 `provider_error_retry_exempt`，未发生下一次调用的 provider failure 仍计费，且所有 attempt 都保留审计。成本硬门唯一作用于完整实验的 `prototype issue-generation / X1v2 issue-generation`，原则上不超过 25×，不要求每个 pair 或单次运行各自低于 25×；独立 LLM semantic judge 的 token、cache、retry 与美元成本独立审计但不计入该倍率，也不做 method 侧计费优化；任何应计 attempt 的 usage/price 缺失或 semantic provenance audit 失败仍会使对应 run 不具备实验资格。200K raw token 只保留为防失控安全上限，不是论文成本口径。最终口径见 [final_output_metrics_policy.md](../../discover_matrix/docs/protocol/final_output_metrics_policy.md)。
- 方法生成阶段的 provider 失败或无法修复的 structured-output 失败可以让方法格失败；内部执行失败和 D 修复耗尽必须带诊断降级落盘。独立 semantic judge 不允许缺格：provider failure 在同一次请求上下文内退避重发且前序失败 attempt 免计费；pair-wide structured contract 无法修复时转为逐个 ledger-emission 关系的原子 LLM judge。任何 fallback 都必须得到真实 LLM 语义裁定与 reason/confidence，严禁用全 miss 或确定性文本规则补结果。
