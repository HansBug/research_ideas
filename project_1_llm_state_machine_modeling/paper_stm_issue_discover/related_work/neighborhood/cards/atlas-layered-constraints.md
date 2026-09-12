# 卡片 · ATLAS（arXiv 2025/2026）· 分层约束制导的结构化制品生成

⭐ 本卡按 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 的 A–F 六节写。⭐ **全文可得**（arXiv HTML v3，113,845 字符），所以本卡**不是**「仅据摘要」。

⚠️ **本篇未经同行评审**（arXiv 预印，v1 2025-10-29 · v2 2025-12-30 · v3 2026-04-05）。⛔ 引它的分层判据可以，⛔ 但不得把它的实验数字当作已被审稿背书的结论。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `atlas-layered-constraints` |
| `title` | ATLAS: A Layered Constraint-Guided Framework for Structured Artifact Generation in LLM-Assisted MDE |
| `year` | ⭐ **2025**（arXiv v1 2025-10-29；⭐ 本卡内容基于 v3 2026-04-05） |
| `venue` | ⛔ **无**（arXiv 预印，cs.SE + cs.AI；ACM class D.2.4, I.2.2；⛔ arXiv `Comments` 字段为空，⛔ 未标投稿目标） |
| `ccf` | ⛔ **未收录**（预印本无 venue） |
| `arxiv` | [`arXiv:2510.25890`](https://arxiv.org/abs/2510.25890) —— ⭐ 已实际访问，⭐ 并实取 HTML 全文 |
| 作者 | Tong Ma, Hui Lai, Hui Wang, Zhenhu Tian, Chaochao Li, Fengjie Xu, Ling Fang（7 人；⛔ 原文 HTML 未给机构） |
| `artifact_type` | ⭐ **AUTOSAR ARXML 结构化工程制品**（软件组件 / 端口 / 接口 / runnable / 信号 / timing 属性及其 containment、cardinality、reference 关系） |
| `task` | ⭐ **生成** + **一致性检查**（XSD / SHACL / SMT 三层校验）+ **修复**（AGR） |
| `boundary` | ⚠️⚠️ **三档都不贴合，见 F.1** —— ⭐ 勉强归 `邻域`，⛔ 但必须带说明：⛔ AUTOSAR ARXML 是**架构 / 配置类结构化制品**，⛔ 不是行为模型（无状态、无迁移、无守卫）。⚠️ 它确实带 timing 与 temporal 约束（由 SMT 检），⭐ 这一维偏 `界外` |

⚠️⚠️ **本篇与本轨硬门 2 的关系必须写明**：⛔ [README.md](../README.md) §2 硬门 2 要求「行为类模型制品」，⭐ 并给了枚举（状态机 / statechart / 活动图 / 时序图 / BPMN / LTS / Event-B / CSP / Petri / 时间自动机 / Stateflow）。⛔ **AUTOSAR ARXML 不在这个枚举里，且它确实不是行为模型。** ⭐ 收它的理由是**它对硬门 1（LLM 是方法核心）与本轨的核心问题（LLM 该被放在流水线哪一环、裁决者是谁）给出了最干净的一个答案**，⛔ 而不是因为它过了硬门 2。⛔ **这条要在本轨的 `SUMMARY.md`（⚠️ 本卡写作时尚未建立）与 [pipeline_forms.md](../pipeline_forms.md) 里显式标注为破门条目**，⛔ 不得默默混进「N 篇行为类模型工作」的统计分母。

---

## B. LLM 应用形态

### B1 · 流水线阶段

⭐ ATLAS 自述由**三个组件**构成（metamodel integration · ICM · CVG），⭐ 但展开后的可执行阶段更多。⭐ 按 RQ2 的实际部署（图 8 的两阶段流水线）画：

```
[确定性] 官方 AUTOSAR XSD / XMI → 域元模型（Path S1，确定性变换）
[确定性] Channel 1：从 schema 抽结构约束 → ICM
[LLM]    Channel 2：从 AUTOSAR PDF 规约抽候选语义 / 逻辑约束
[确定性] 准入三道门：α 锚定 → 语义兼容 → 可编译性；⛔ 不过则 quarantine
[确定性] 约束编译：κ_struct → 前缀自动机 · κ_sem → SHACL · κ_logic → SMT
[LLM+确定性] Phase 1 Blueprint 合成（JSON Schema 受限解码）
[LLM+确定性] Phase 2 逐组件生成（JSON Schema 受限解码）→ [确定性] JSON → ARXML 序列化
[确定性] L2 校验：xmllint XSD → SHACL → SMT（⭐ 固定顺序）
[LLM 或 人] AGR：LLM 最小补丁 / 人在 typed editor 里改
[确定性] 局部重校验；⛔ 反复失败 → MANUAL_REVIEW
```

⭐ **阶段总数约 10 · LLM 阶段 4**（Channel 2 抽取 · blueprint · component 生成 · patch），⭐ 其中最后一个可由人替代。

⚠️ **RQ1 的配置更短**（单文件，无 blueprint 阶段，⛔ 也无 SHACL / SMT —— ⭐ 原文逐字：「Semantic consistency (SHACL) and logic verification (SMT) metrics are reserved for the system-level evaluation in RQ2, as single-file generation lacks the necessary cross-reference context」）。

### B2 · 每次 LLM 调用的角色

| 环节 | 角色 |
| :-- | :-- |
| Channel 2 约束抽取 | ⭐ **抽取器**（NL 规约 → 结构化 JSON 约束候选） |
| Phase 1 Blueprint | ⭐ **规划者**（组件清单 / 依赖图 / 文件布局 / 跨组件接口契约） |
| Phase 2 Component | ⭐ **生成器** |
| AGR 自动修补 | ⭐ **修复者**（「produce a **minimal patch** for the affected region」） |

⭐⭐ **这一格最重要的是缺了什么：⛔ 没有任何一个 LLM 扮演「评审者」或「裁决者」。** ⭐ 判定权全部归确定性校验器。⭐ **这正是 M1 要找的外部先例。**

### B3 · prompt 策略

`RAG`（⭐ **ICM-complete retrieval** —— ⭐ 不是普通向量检索，⭐ 而是从元模型确定性地取出该组件的类型 / containment / 字段线索）· ⭐⭐ **结构化输出约束（真正的受限解码，见 B4/B7）** · ⭐ 分阶段温度（Phase 1 = 0.7 鼓励架构多样性 · Phase 2 = 0.3 · 接口文件 = 0.2）。⛔ **无 few-shot 说明 · 无 CoT 说明 · 无 self-consistency 投票 · 无多智能体辩论。**

⭐ 值得单独记的一条（M，§4.3.3 逐字）：⭐ **他们把「prompt 端引导」与「解码端强制」明确当成两种不同机制并分别测量**：

> ICM-complete prompting makes valid continuations more probable, whereas constrained decoding makes invalid continuations unreachable with respect to the compiled structural contract.

### B4 · ⭐⭐ 循环与裁决者（本轨最关键的一格）

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⭐ **有**（AGR：Audit-Guided Intelligent Repair，算法 2） |
| ⭐⭐ **裁决者是谁** | ⭐⭐ **`sound oracle` 组合，⛔ 零 LLM 自评**：xmllint 的 **XSD 校验器** + **SHACL 图校验器**（794 node shapes）+ **SMT 求解器**（1005 assertions）。⭐ 接受判据逐字：「Operationally, an artifact is accepted only when the structural, semantic, and logic validators all pass.」⭐ 另有一条明确的反向声明：「**Audit metadata does not by itself turn a failed artifact into an accepted one**」 |
| 终止条件 | ⭐ 局部重校验通过；⛔ 或 **转人**（逐字：「if revalidation fails repeatedly then return MANUAL_REVIEW」） |
| 最大轮数 | ⛔ **原文未提供** —— ⭐ 只写 `repeatedly`，⛔ 无具体阈值 |
| ⭐ 有无报**循环的边际收益** | ⛔⛔ **原文未提供，且这是本篇最大的空洞**（见下方专段） |

#### ⛔⛔ AGR 的收益一次都没量化

⛔ **RQ2 报的全部是 first-pass（首遍）结果，AGR 从未被打开测过。** ⭐ 原文自己写明（M，§4.4.2 逐字）：

> This 0% result shows that large-scale system consistency was **not achieved by the evaluated first-pass constrained generation workflow** on this benchmark, and therefore marks the point at which structural success no longer translates into system-level correctness. ... **That distinction motivates the iterative repair workflow supported in ATLAS** and points naturally toward stronger design-time guidance, validator-guided revision, and selective human intervention in later stages of the pipeline.

⭐ 逐字读法：⛔ AGR 在本文里是**被这个负结果「motivate」的东西**，⛔ 不是被评测的东西。⛔ 算法 2 是接口描述，⭐ 作者自己称之为 workflow-level interface（逐字：「are likewise workflow-level interfaces for violation extraction, local revalidation, and patch application **rather than a claim of a closed repair calculus**」）。

⭐⭐ **对我们的直接含义**：⛔ **不能引 ATLAS 当「sound oracle 做裁决者的修复回路有收益」的证据** —— ⭐ 它只能证明「**把裁决者换成 sound oracle 后，问题被精确定位出来了**」。⭐ 后者本身仍是重要的（见 E.1），⛔ 但两件事不能混。

### B5 · ⭐ 中间表示

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有，而且是本篇的核心贡献** |
| 形态 | ⭐ **ICM**（Integrated Constraint Model）$\mathcal{I} = (\mathcal{M}, \mathcal{R}, \mathcal{P}, \Gamma)$：$\mathcal{M}$ 域元模型 · $\mathcal{R}$ 准入约束仓库 · $\mathcal{P}$ 出处与编译元数据 · $\Gamma$ 依赖序（用于排修复顺序）。⭐ $\mathcal{R}$ 三分为 $(\mathcal{R}_{\mathrm{struct}}, \mathcal{R}_{\mathrm{sem}}, \mathcal{R}_{\mathrm{log}})$ |
| ⭐ **是否闭合** | ⭐⭐ **闭合，但通道开放**：生成与校验**只用已准入的约束**（M，逐字：「**No claim is made for constraints that were not admitted into the ICM**」），⛔ 但准入通道常开（Channel 2 持续抽 + AGR 的 constraint promotion 可回灌），⭐ **每次增长都过同一套三道门** |
| ⭐ **谁定的** | ⭐⭐ **不是人手编、也不是 LLM 自由生成，而是「确定性导出 + LLM 抽取候选 + 确定性准入」三段式**（见下方专段） |

#### ⭐⭐ 约束从哪来（M，§3.3 + §4.2 逐字）

**Channel 1（确定性）**：

> Channel 1 extracts constraints from structured engineering assets and authoritative schemas. **It is deterministic** and supplies the initial structural backbone of the ICM.

⭐ 元模型本身逐字：「we derive the integrated AUTOSAR metamodel **deterministically from official AUTOSAR XSD and XMI artifacts**」。

**Channel 2（LLM 抽候选，⛔ 但绝不直接采信）**：

> Channel 2 extracts candidate semantic and logic constraints from natural-language documents using an LLM, but **every candidate must pass an admission workflow** before it becomes persistent.

⭐ 三道准入门逐字（Definition 3.0 Semantic Compatibility）：⭐ ① 操作数能被 $\alpha(c)$ 返回的锚点定型；⭐ ② 不与已准入的结构事实（cardinality / containment / reference kind）矛盾；⭐ ③ 能编译进目标后端（SHACL / SMT / validator 接口）且**不留未解析符号**。⛔ 不过门的处理逐字：「Candidates with $\alpha(c)=\bot$ **are not admitted into the persistent ICM and are instead quarantined for review**」，⭐ 总纲一句：「**LLM-extracted rules are never admitted directly**」。

**⭐ 数量（M，§4.2 逐字）**：

> Applying this process to the AUTOSAR Software Component Template specification **yielded 1,161 normative constraints**, of which **1,045 were anchored to verified metamodel entities (90.0% anchoring rate)**. In the present AUTOSAR instantiation, these admitted constraints are compiled into **794 SHACL node shapes** for graph-structural checks and **1,005 SMT assertions** for logic and value checks; purely informational hints are excluded from the automated pipeline.

⭐⭐ **我实际下载了仓库里的约束集核对**（见 D 节）：⭐ `src/kg_builder/data/constraints_linked.json` 恰好 **1161 条**，⭐ 与论文数字**逐字吻合**。⚠️ **但有两处对不上，必须记下来**：⛔ ① 该文件里 **1161/1161 条都有非空 `targetRefs`（100%）**，⛔ 而论文说 1045 条锚定（90.0%）—— ⭐ 说明「anchored to **verified** metamodel entities」是比「有 targetRefs」更严的一道检查，⛔ 而放出的文件是哪一版未标明；⛔ ② 文件里的 `constraint_type` 分类是 **10 类开放式**（`behavioral` 350 · `relationship` 344 · `value_restriction` 220 · `existence` 96 · `definition` 61 · `cardinality` 43 · `naming_convention` 21 · `ordering` 14 · `other` 8 · `format` 4），⛔ **与论文的 3 族划分（struct / sem / log）不是 1:1**，⛔ 且映射关系在我读到的正文里没写。

⚠️ **另一处值得记的观察（S，从实际抽样推出）**：⭐ 我抽看的第一条 `definition` 类约束，其 `expression` 字段是**一整段带项目符号的规约散文**（讲 calibration parameter 有哪三种定义方式），⛔ 显然不可编译。⭐ 这与论文「purely informational hints are excluded from the automated pipeline」是一致的 —— ⭐ 即 **1161 是「抽出来的」，⛔ 不是「全部生效的」**；⭐ 真正生效的是 794 + 1005 那两组编译产物。

### B6 · 模型

| 用途 | 模型 |
| :-- | :-- |
| RQ1（机制隔离） | ⭐ **DeepSeek-R1-Distill-Qwen-32B**，vLLM 本地服务，⭐ 固定 seed **42 / 1001 / 20250701**，temperature 0.7，top-p 0.9 |
| RQ1 外部参考 | ⭐ **GPT-5**（unconstrained API，⛔ 只报 XSD 通过率，⛔ 不进延迟 / audit 对照） |
| RQ2（规模压力测试） | ⭐ **GPT-5**（Phase 1 与 Phase 2 都用） |
| 多模型对照 | ⭐ **有，但两个 RQ 的用法刻意不同** |

⭐⭐ **模型选择的理由值得逐字记（M，§4.3.1）**，⭐ 因为它是一份「为什么固定 backbone」的现成论证：

> RQ1 is designed as a **mechanism-isolation study**: its purpose is to measure how much structural reliability comes from ATLAS itself ... rather than from switching among model families. We therefore fix the backbone to DeepSeek-R1-Distill-Qwen-32B served through vLLM and treat it as a **controlled constant**. This choice is methodological rather than doctrinal. An open-weight local model gives us a fully instrumented inference stack for tokenizer-level masking, deterministic replay, latency/token measurement, and stepwise audit capture ...

⭐ RQ2 换 GPT-5 的理由则是**边界问题**：⭐ 逐字「when raw model capability is increased in a deployment-oriented setting, which defects still remain at multi-file system scale」。⛔ 作者明说「The goal is **not** a same-backbone comparison with RQ1」。

⭐⭐ **一条与本仓库 X1 结论对撞的观察**：⛔ **GPT-5 在无 ATLAS 控制下 XSD 通过率只有 50%，而 32B 开源模型 + ICM-RAG 是 100%。** ⭐ 作者的结论句逐字：「**Greater model capability alone did not substitute for structural control**」。⚠️ 但要小心读：⛔ 这只说明**语法合规**这一维可以被便宜地机械保证，⛔ 不说明语义维也如此 —— ⭐ RQ2 里 GPT-5 的 SMT 系统级通过率是 **0%**。

### B7 · ⭐ 确定性成分（⭐ 极多，⭐ 本篇是本轨确定性底座最厚的一篇）

| 环节 | 是什么 |
| :-- | :-- |
| 元模型构建 | ⭐ AUTOSAR XSD / XMI → 类型化图（确定性变换） |
| Channel 1 约束抽取 | ⭐ 确定性 |
| 准入三道门 | ⭐ $\alpha$ 锚定 · 语义兼容（含矛盾检查）· 可编译性 |
| ⭐⭐ 约束编译 | ⭐ $\kappa_{\mathrm{struct}} \to \mathcal{A}_{\mathrm{prefix}}$（JSON-Schema / Regex / GBNF 派生自动机；⭐ 有限状态片段确定化为**前缀闭 DFA**，⭐ 递归文法片段走 **PDA / LR** 并按深度 $d$ **有界展开**成等价 DFA）· $\kappa_{\mathrm{sem}} \to$ SHACL · $\kappa_{\mathrm{logic}} \to$ SMT |
| ⭐⭐ 解码期强制 | ⭐ 逐 token 掩码：$M_t = \{y \in \Sigma \mid \delta(s_t, y) \neq \bot \land \mathrm{ReachAccept}(\delta(s_t,y))\}$，⭐ 掩掉非法 logits、采样、推进状态 |
| ⭐ 结构闭合 | ⭐ 解码提前停时，控制器可在编译图上**算出一条到接受态的续写**当作补全 |
| ⭐ audit trail | ⭐ 每步记 $\tau_t = \langle s_t, |M_t|, y_t, s_{t+1}, \Delta t \rangle$ |
| L2 校验 | ⭐ xmllint（XSD）· SHACL 校验器（`shacl_validator.py` 58 KB）· SMT（`smt_validator.py` 130 KB） |
| 其它 | ⭐ JSON → ARXML 序列化 · 跨文件引用解析统计 · $\Gamma$ 依赖排序 · ⭐ **商业工具导入验证（Etas ISOLAR-A）** |

⭐⭐ **这一格的结论**：⭐ **ATLAS 的 LLM 只负责「写」与「补」，「判」全部归确定性。** ⭐ 它甚至把「判」拆成三层递进：⭐ 解码期前缀可判定的结构（DFA）→ 完工后的图级语义（SHACL）→ 数值 / 时序（SMT）→ ⭐ 最后再加一道商业工具导入。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **有，4 个受控本地配置 + 1 个外部参考**：⭐ ① `vLLM`（纯 prompt）· ② `vLLM+ICM-RAG` · ③ `vLLM+ICM-RAG+JSON Schema` · ④ `vLLM+ICM-RAG+GBNF`，⭐ **四者同一 backbone**；⭐ 外加 `LLM-API`（GPT-5 无约束）作为 frontier 参考。⭐ **这是一条干净的递进消融**（prompt → +检索 → +受限解码两种实现） |
| `dataset` | ⭐ **RQ1**：60 个「representative」AUTOSAR 组件 × 3 个 prompt regime（`Min` 最简需求 / `Std` 标准文档 / `Full` 含 timing 与行为约束的完整规约）。⭐ **RQ2**：自建 20 个 AUTOSAR 系统 / 126 组件 / **284 个 ARXML 文件**，⭐ 三档拓扑复杂度 —— `Simple` 7 例 27 组件 52 文件（链式）· `Middle` 7 例 45 组件 108 文件（多分支树）· `Complex` 6 例 54 组件 124 文件（含双向依赖的 mesh）。⛔ **两个数据集都是自建，⛔ 无公开 benchmark，⛔ 无 ground-truth 参考制品** —— ⭐ 判据全部来自**校验器**而非参考答案 |
| `metrics` | ⭐ ① XSD 通过率（xmllint）· ② **audit coverage**（记到 $\tau_t$ 的生成步比例）· ③ 端到端延迟 + input / output token · ④ file completeness（是否全部 blueprint 声明的文件都产出且未截断）· ⑤ **跨文件引用解析率**（可解析 `<REF>` / 总 `<REF>`）· ⑥ SHACL 通过 · ⑦ SMT 通过 · ⑧ 商业工具导入（ISOLAR-A，二值）· ⑨ 5 分制人工评分 rubric（A1 功能覆盖 / A2 接口完整 / A3 需求可追溯；B1 依赖-角色一致 / B2 局部类型正确；C1 命名文档质量 / C2 结构模块化 / C3 预估修复工作量；D1 工具导入）。⛔ **无 `@k` 类多轮口径** |
| ⭐ `judged_by` | ⭐⭐ **两分**：⭐ ①–⑧ 全部由**确定性校验器 / 商业工具**判（⭐ 这是本篇最强的一点）；⛔ ⑨ 的 5 分制 rubric 是 **作者自评**，⛔ **无标注者间一致性、无 $\kappa$**。⭐ 作者在 threats 里自己承认（M，逐字）：「Because the analysis is **not positioned as an external independent assessment**, its judgments should be interpreted accordingly.」 |
| `human_baseline` | ⛔ **无**。⭐ 作者在 Limitations 里明确承认（逐字）：「Human-factors evidence is still limited. The current result analysis is diagnostic rather than a controlled productivity or usability study, so stronger claims about engineering effort reduction must wait for future work.」 |
| `runs` | ⚠️ **RQ1 有 3 个固定 seed（42 / 1001 / 20250701）**，⛔ 但正文表 3–5 未报方差、⛔ 未说明报的是均值还是单次。⛔ **RQ2 的重复次数原文未提供，也无方差** |
| ⭐ `adverse_results` | ⭐⭐ **本篇最值得学的地方：把一个 0% 的负结果做成了论文的核心论点**（详见下方专段） |

### ⭐⭐ 不利结果的处理方式（⭐ 直接可借鉴，⭐ 且比 LADEX 那篇更极端）

**① 逐层递减，且最深那层是 0%。**（M，§4.4.2 逐字）

> At Layer 1, all 20 systems across all complexity tiers achieved **100% XSD pass rates** ... At Layer 2, local semantics checked via SHACL **degrade sharply**. Among the instantiated checks for the generated systems—57, 113, and 63 effective checks across the Simple, Middle, and Complex tiers, drawn from a validator inventory of 794 node shapes—the pass rates fall to **2/57 (about 3.5%), 16/113 (about 14.2%), and 6/63 (about 9.5%)**, respectively ... When SMT constraints are added to verify cross-file consistency ... the system-level pass rate **drops to 0% across all tiers**.

**② 并且明确指出「看起来对」的指标是假的。**（M，同节逐字）

> While the model often generated references that resolved to existing IDs, as shown by the high reference-resolution rate in Table 6, **SMT validation revealed that these connections were frequently semantically invalid**, for example by connecting incompatible ports or creating circular dependencies.

⭐⭐ **这一句是本卡对 M1 最有用的单句**：⭐ 引用解析率 **96.4%**（Simple 100% / Middle 99.4% / Complex 92.8%）看着极漂亮，⛔ 但 SMT 一上就是 **0%** —— ⛔ **一个浅层指标可以近乎满分而深层判据全灭。**

**③ 把负结果提炼成论点，而不是弱化它。**（M，§4.4.3 与 §4.3.3 逐字）

> The same experiments also show a sharp boundary: **structural validity does not imply system-level correctness.**

> The significance of ATLAS therefore lies in how it **reorganizes the problem**: structural admissibility becomes routine, while the genuinely difficult part of system construction is **surfaced explicitly at the validation and repair boundary**.

⭐ 摘要里对应的自我定位词是 **「bounded automation」**，⭐ Limitations 里三条（语义覆盖仅部分 · 人因证据不足 · 只在 AUTOSAR 一个域上评过）全部自陈。

**④ 还主动缩了自己的形式化主张范围。**（M，Proposition 6 之后逐字）

> **No claim is made** for constraints that were not admitted into the ICM, that exceed the chosen unfolding bound, or that are only partially approximated by the backend encoding.

⭐ 另有一条工程限制自陈：⛔ GBNF 那条流水线**没接 audit recorder**（逐字：「was not instrumented with the same audit recorder in our current implementation, representing an engineering limitation rather than fundamental incompatibility」）。

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | 🟢 | [arxiv.org/html/2510.25890v3](https://arxiv.org/html/2510.25890v3) | ⭐ 实取 HTML 并转文本 **113,845 字符**，⭐ 含全部正文、Table 2–7、Algorithm 1–2、Proposition 6、Threats、Conclusion 与 Data Availability |
| ⭐ **实验代码** | 🟢 | [github.com/Abandooon/ATLAS](https://github.com/Abandooon/ATLAS) | ⭐ `verify_assets` 逐字：`HEAD 9fef63d169 · 文件 1342（非文档 1192）· release 0 · license Apache-2.0`。⭐ 我另实列全树：`src/kg_builder/`（元模型 / 约束解析，含 `doc_constr_parser/` 107 文件、`uml_metadata_parser/` 33 文件）· `src/llm_generation/`（生成、`json_to_xml.py`、`generator_schema.py`、`promote/`）· `src/validation/`（见下行）· `src/vllm/`（`constraint_preparer.py`、`gbnf_fsm_design_doc_v3.md`、`implementation_V1/V2`、`vllm_modify/` 14 文件）· 顶层 `completeness_checker.py` / `cross_reference_checker.py` / `run_validation.py` / `vllm_local_main.py`。⛔ **`.idea/` 12 个 IDE 文件也提交了**（⭐ 无害，⛔ 但说明未清理） |
| ⭐⭐ **L2 校验器（sound oracle 本体）** | 🟢 | `src/validation/` | ⭐ 实取文件与字节数：`structure/xsd_validator.py` **6,127 B** · `semantic/shacl_validator.py` **58,024 B** · `constraints/smt_validator.py` **129,627 B** · `orchestrator/config_driven_orchestrator.py` 79,080 B + `validation_orchestrator.py` 16,872 B · `cross_file_resolver.py`。⭐⭐ **三层校验器全部在库，⛔ 不是「code available later」** |
| ⭐⭐ **ICM 约束集** | 🟢 | `src/kg_builder/data/constraints_linked.json` | ⭐⭐ **我实际下载并解析**：JSON 数组，**`len == 1161`**，⭐ 与论文 §4.2 的 1,161 逐字吻合。⭐ 字段：`constraint_type` / `expression` / `id` / `id_type` / `scope_path` / `targets` / `title` / `is_active` / `references` / `value` / `xml_example_content` / `targetRefs` / `confidence`。⚠️ 与论文的两处不一致见 B5 专段 |
| ⭐ **元模型 / schema 资产** | 🟢 | `src/kg_builder/data/` | ⭐ `AUTOSAR_4-2-2.xsd` **4,872,036 B** · `unified_metadata.json` **5,207,609 B** · `unified_metadata_with_inlines.json` **5,283,500 B** · `constraints_types_sample.json` 13,872 B |
| ⭐ **数据集 / Benchmark** | 🟠 | `nlp_require/`（3 文件）+ `experimental_data/`（811 文件）+ `generated_arxml/`（251 文件） | ⚠️ **判 🟠 而不是 🟢**：⛔ 库里有大量**产出**（含逐 seed 的 `01_seed42.arxml` / `01_seed1001.arxml` / `01_seed20250701.arxml` 三件套，⭐ 与论文声明的 3 个 seed 对得上），⛔ 但 **`nlp_require/` 只有 3 个文件** —— ⛔ 无法对应 RQ1 的 60 个组件 × 3 regime 与 RQ2 的 20 个系统输入规约。⛔ **且全程无 ground-truth 参考制品**（本方法论上不需要，⭐ 但意味着这不是可被第三方独立评分的 benchmark） |
| 实验结果细则 | 🟢 | `experimental_data/data_analysis/{analysis_llm.py, analysis_vllm.py}` + 逐 seed 的 `.arxml` / `.txt` 对 | ⭐ 实取目录名样例：`experimental_data/llm/full_promote_No Guard/` 下每个 case 都有 `.arxml` + `.txt` 两份 × 3 seed。⭐ **是可下载逐条产出，⛔ 不只有论文表格** |
| Artifact / 复现包 DOI | ⚪ | —— | ⛔ **无 Zenodo / 4open / OSF DOI**；⛔ 只有 GitHub（⛔ 无 release，⛔ 可被改写；⭐ 本卡已钉 HEAD `9fef63d169`） |
| ⭐ **prompt 是否公开** | 🟢 | `src/llm_generation/llm/prompt_templates.py` + `src/vllm/implementation_V2/prompt_mapper.py` + `src/vllm/implementation_V2/gbnf_template` | ⭐ 实际 grep 全树命中这三处。⭐ **连 GBNF 文法模板都在** |

⭐ **Data Availability 原文逐字**：「The data and materials associated with this study are available at: https://github.com/Abandooon/ATLAS」。

⭐ **终裁说明**：⭐ 代码 / 校验器 / 约束集 / 元模型 / 结果 / prompt 六项 🟢，⛔ 数据集入口 🟠（产出全、输入侧不足）、⛔ 归档 DOI ⚪。⚠️ ⭐ 这是本轨到目前为止**资产最实的一篇**（连 SMT 校验器 130 KB 和 1161 条约束 JSON 都放了），⛔ 但**未经同行评审**这一点要与资产质量分开评价。

---

## E. 对 M1 的意义

### 1. ⭐⭐ 可取之处

**⭐⭐ 第一条（本卡的核心输出）：分层判据是「prefix-checkability（前缀可判定性）」，⛔ 不是「语义清晰度」。**

⭐ 逐字判据（M，Definition 3.0 Operational Constraint Partition + §3.4 Rationale）：

> $\mathcal{R}_{\mathrm{struct}}$ contains **prefix-checkable** structural obligations such as containment, field presence, ordering, and local typing patterns; $\mathcal{R}_{\mathrm{sem}}$ contains **graph-level or reference-level obligations that require the completed artifact**; and $\mathcal{R}_{\mathrm{log}}$ contains **numeric, temporal, or solver-backed** domain conditions. **This partition is operational rather than ontological**: one domain rule may contribute a structural fragment to L1 and a richer semantic or logical fragment to L2.

> Local structural conditions such as nesting, token class, field presence, and ordering **are prefix-checkable and can therefore be compiled into a decoder-side controller**. Cross-reference integrity, graph acyclicity, type compatibility across distant elements, or numeric timing constraints **require the completed artifact and belong in L2**.

> Item (i) states the **admission policy: only prefix-checkable structural fragments are sent to L1.**

⭐⭐ **这条判据比本仓库 §11 的「能被完美判定」更操作化，且两者是正交的两个维度**：

| 维度 | 问题 | 本仓库 §11 | ⭐ ATLAS |
| :-- | :-- | :-- | :-- |
| **可判定性** | ⭐ 只看值能否唯一判断？ | ⭐⭐ **这就是 §11 的判据** | ⭐ 隐含前提（三族都要求可编译成可执行判据） |
| ⭐ **可判定的时机** | ⭐ 只看**前缀**能否判断？ | ⛔ **§11 没有这一维** | ⭐⭐ **这就是 L1/L2 的判据** |

⭐⭐ **加上这一维，我们那次事故就能被更早地拦住。** ⭐ 回看 `named_elements` 那条 validator：⭐ 「句子点名了几个要素」既**不是**可判定的（要语义解释），⭐ 也**不是**前缀可判定的（要读完整句才知道并列结构）；⛔ 而它被实现成了「字符串里有没有逗号」—— ⛔ 一个**前缀可判定但语义错误**的近似。⭐⭐ **ATLAS 的判据恰好解释了这次失败的机制：⛔ 当一条约束只在完工后才可判，⛔ 却被塞进生成期的门里，⛔ 实现者就必然被迫用词法近似去替代语义判断。** ⭐ 而 ATLAS 明确禁止这件事（「only prefix-checkable structural fragments are sent to L1」），⭐ 并给了正确出路：**放到 L2，⛔ 用完工后的图级 / 求解器判据。**

**⭐ 落地建议（→ M1）**：⭐ 把本仓库 §11 的准入门从**一问**改成**两问**：
1. ⭐ 这条约束能否只看字段值就唯一判定？（⛔ 不能 → 迁 prompt + reviewer，⭐ 现有规则）
2. ⭐⭐ **它能否在只看到部分产出时就判定？**（⛔ 不能 → ⛔ **它不属于生成期的门，只属于封存后的检查**，⭐ 即我们的 `precheck_and_seal` 而非 `convert_assertions` 的内联 validator）

**⭐⭐ 第二条：整条流水线里没有一个 LLM 评审者节点，判定权 100% 归确定性校验器。** ⭐ 这是我们「拆掉两个 LLM 自评 reviewer」这个动作的**最直接外部先例**。⭐ 而且他们把「audit 元数据」与「接受判据」显式分开（逐字：「Audit metadata does not by itself turn a failed artifact into an accepted one」）—— ⭐ 我们的 `adjudicate_results` 节点值得照这条重审：⛔ 它现在是 LLM 在判「这算不算一条发现」，⭐ 而 pyfcstm 的求值结果只是它的输入。

**⭐ 第三条：约束仓库的「准入三道门 + quarantine + promotion」流程可直接照搬到我们的谓词词表增长上。** ⭐ 三道门 = 能否锚到元模型实体 / 是否与已准入事实矛盾 / 能否编译成可执行判据；⛔ 不过则 quarantine 待人审；⭐ 修复中发现的可复用规则可 promote 回仓库，⭐ **但过同一套门**（逐字：「Promotion is gated by the same provenance and compatibility checks used during initial ICM construction, so repair does not become an uncontrolled source of new global rules」）。⭐⭐ **这条与本仓库 §3.5.-1 的「按领域出处反查」是同一件事的工程化版本**：⭐ 他们的 $\mathcal{P}$（provenance）字段就是我们 [provenance/](../../provenance/) 那份三类分级的机器可读形态。

**⭐ 第四条：修复走「最小补丁 + 依赖序」，⛔ 不走自由重生成。** ⭐ 逐字：「AGR therefore focuses on **evidence-driven correction rather than free-form regeneration**」；⭐ 校验器被要求「emit failure objects that identify **where** the problem is, **which** obligation was violated, and **which** metamodel or ICM item that obligation came from」；⭐ 修复顺序按 $\Gamma$ 排（先解引用、再类型 / cardinality、最后数值）。⭐ 这与本仓库 §10 的「把解析错误的具体位置回灌」是同一原则，⭐ 且他们给了更完整的形态（三元组定位 + 依赖排序）。

### 2. ⛔ 不可取 / 陷阱

**⛔ 第一条：不能引它当「修复回路有收益」的证据。** ⛔ AGR 一次都没被量化（见 B4 专段）。⛔ 若把 ATLAS 写成「别人的 sound oracle 回路是有效的」，那是**读错了论文** —— ⭐ 它自己说 RQ2 是 first-pass 结果，⭐ 且 AGR 是被这个负结果 motivate 的未来工作。

**⛔ 第二条：5 分制人工评分是作者自评、无 $\kappa$。** ⛔ Table 7 的 A1–D1 全部由作者打分，⛔ 作者自己在 construct validity 里承认不是独立评估。⭐ 对比 LADEX 那篇（2 名标注者 + Cohen $\kappa$ = 0.888/0.916 + 与自动 judge 比 P/R/F1）—— ⭐ **同一批材料里两种做法的差距很直观，⭐ 我们该学后者。**

**⛔ 第三条：L1 的强制会扭曲分布，⛔ 他们只有工程缓解、没有形式保证。** ⛔ 逐字：「L1 enforcement changes the model's token distribution and **can over-favor short valid completions**」；⭐ 缓解手段是 minimum-coverage guards、有界展开校准、两阶段分工，⛔ 而作者自称「These are **engineering controls rather than formal guarantees**」。⚠️ **这条对我们有直接警示**：⭐ 我们的契约门若把生成空间压得太紧，⛔ 模型会倾向产出**最短的合法答案** —— ⛔ 而在断言生成里，「最短合法」往往等于「覆盖不足」。⭐ 这与本仓库 §13 的门交集审计是配套的第二种失效模式：⛔ 不是**无解**，而是**有解但退化**。

**⛔ 第四条：Layer 2 的保证完全外挂后端，⛔ 有边界声明。** ⛔ Proposition 6 后逐字免责「No claim is made for constraints that were not admitted into the ICM, that exceed the chosen unfolding bound, or that are only partially approximated by the backend encoding」。⭐ 这个免责写法本身值得学，⛔ 但也意味着「SHACL / SMT 全过」并不等于「AUTOSAR 语义全对」。

**⛔ 第五条：单域、无外部 benchmark、RQ2 无方差。** ⛔ 只在 AUTOSAR 上评过，⛔ 作者自陈「supports transfer only by architectural plausibility, not by direct empirical evidence outside AUTOSAR」。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

**⚠️ 第一条：他们能做受限解码，是因为制品的**语法**是前缀可判定的；⛔ 我们要判的**不是语法**。** ⭐ ARXML / JSON 是树，⭐ 树语法天然前缀可判定，⭐ 所以 L1 能压到 XSD 100%。⭐ 我们的 pyfcstm DSL 同样可解析（⭐ 我们已有 Pydantic schema + 解析失败原地重试），⛔ **但我们的核心判据是「断言是否忠实于 NL 需求」** —— ⛔ 那既不是前缀可判定，⛔ 也不是完工后图级可判定，⛔ 它需要外部真值。⛔ **ATLAS 的 L1 那一层我们基本已经有了，⛔ 再投入的边际收益很低。**

**⚠️⚠️ 第二条（本卡最重要的差别）：ATLAS 的 L2 有 sound oracle，⛔ 我们的核心判定没有。** ⭐ 他们的 SMT 能判定「端口类型是否兼容」「依赖是否成环」，⛔ 因为**这些性质完全内蕴于制品自身**（不需要问 NL）。⛔ 而我们的台账命中判定问的是「模型 vs NL 需求是否一致」，⛔ **NL 一侧没有形式语义，⛔ 所以原则上不存在这样的 oracle** —— ⭐ 这正是我们花 574 位人工逐位判定的原因。⛔ **ATLAS 帮不上这个缺口。**

⭐⭐ **但它给出了一个可行的分层落点**：⭐ 把我们的判定也拆成两层 ——
- ⭐ **L2a（有 oracle）**：断言脚本在模型上求值的结果、引用完整性、谓词适用性、覆盖闭包 —— ⭐ **这些全部内蕴于制品，⭐ pyfcstm 就是这一层的 sound oracle。** ⭐⭐ 而我们现在把 pyfcstm 放在**求值端**（`precheck_and_seal`），⛔ 判定端（`adjudicate_results`）却是 LLM —— ⭐⭐ **ATLAS 的形态说明这两个位置该换**。
- ⛔ **L2b（无 oracle）**：「这条发现是否对应台账里那一条」—— ⛔ 只能人工或 LLM，⛔ 且必须像 LADEX 那样做 $\kappa$ 校准。

**⚠️ 第三条：任务方向不同。** ⭐ ATLAS 是**生成**（把制品造出来并证明它合规），⭐ 我们是**缺陷检测**（在给定制品里找出它哪里不对）。⛔ 因此他们的「接受 = 三层校验全过」在我们这里没有对应物 —— ⛔ 我们的产出**本来就应该报告不一致**。⭐ 可迁移的是**机制**（谁判、判什么、判据放哪一层），⛔ 不是**判据本身**。

**⚠️ 第四条：制品类型差得远。** ⛔ AUTOSAR ARXML 是配置 / 架构制品，⛔ 无状态无迁移；⭐ 我们是 FSM / HSM / EFSM。⛔ 他们的 794 SHACL shapes / 1005 SMT assertions **一条也不能直接用**。⭐ 可迁移的只有**这套约束是怎么被导出、准入、编译、分层的流程**。

---

## F. 存疑与未核项

1. ⚠️⚠️ **`boundary` 三档都不贴合** —— ⭐ [README.md](../README.md) §2.1 的三档（`界内` = FSM/HSM/EFSM · `邻域` = 活动图/时序图/BPMN/协议状态机/LTS · `界外` = 时间自动机/混成/Petri/进程代数/正交并发）**没有一档覆盖「AUTOSAR ARXML 配置制品」**。⛔ 且它**未过本轨硬门 2**（不是行为类模型制品）。⭐ 本卡权且标 `邻域` 并在 A 节写明破门，⛔ **但需要主 session 裁定**：⭐ 是给三档加一档（如 `结构化工程制品`），⭐ 还是把本篇标为「破门收录、单列不进分母」。
2. ⚠️ **AGR 的最大轮数 / `repeatedly` 的具体阈值原文未提供。**
3. ⚠️ **AGR 的收益原文未提供** —— ⛔ 不是「我没找到」，⭐ 是作者自陈 RQ2 为 first-pass。⭐ 仓库里有 `promote/`（6 文件）与顶层 `llm_rag_generator_auto.py` / `llm_rag_generator_human.py`，⭐ 疑似两条修复路的实现，⛔ 但**本轮未读代码确认**，⛔ 也无对应实验数据。
4. ⚠️ **RQ2 的重复次数与方差原文未提供** —— ⭐ RQ1 有 3 个 seed（且仓库里的 `01_seed42/1001/20250701` 三件套与之吻合），⛔ RQ2 未说明。
5. ⚠️ **仓库约束集与论文数字有两处不一致（已在 B5 记录，此处只列未核部分）**：⛔ ① `constraints_linked.json` 的 1161 条全部有 `targetRefs`（100%），⛔ 论文说 1045 条（90.0%）锚定 —— ⛔ 放出的是准入前还是准入后的版本未标明；⛔ ② 文件里 10 类 `constraint_type` 与论文 3 族 $(\mathcal{R}_{\mathrm{struct}}, \mathcal{R}_{\mathrm{sem}}, \mathcal{R}_{\mathrm{log}})$ 的映射关系我在正文里没找到。⛔ **我未在库里定位到 794 个 SHACL node shapes 与 1005 条 SMT assertions 的独立产物文件** —— ⭐ 它们可能由 `shacl_validator.py`（58 KB）与 `smt_validator.py`（130 KB）在运行时从 JSON 编译生成，⛔ 但未读代码确认。
6. ⚠️ **RQ1 的「60 representative AUTOSAR components」与 RQ2 的 20 个系统，其输入规约在库里对不上** —— ⭐ `nlp_require/` 只有 3 个文件；⛔ 也可能藏在 `experimental_data/` 或 `src/llm_generation/knowledge/` 里，⛔ 未逐目录核。
7. ⚠️ **两个 GPT-5 用法的精确 model id / 调用日期原文未提供** —— ⛔ 只写 `GPT-5`，⛔ 无 snapshot 版本、无调用月份。⚠️ 按本仓库 §5.2 的口径这是记录不足。
8. ⚠️ **v1 / v2 / v3 三版的差异未核** —— ⭐ 本卡全部基于 v3（2026-04-05，1,175 KB）；⛔ v1（2025-10-29）与 v2（2025-12-30）的数字是否相同未比对。⚠️ ⭐ LADEX 那篇的经验（v2 与 v3 统计口径不同）说明这不是空担心。
9. ⚠️ **无归档 DOI、无 release** —— ⭐ 已钉 HEAD `9fef63d169`，⛔ 但仓库可被改写。
