# 卡片 · **LLM-FSM**（反向合成 FSM benchmark）

⭐ 全文可得：[arXiv HTML v1](https://arxiv.org/html/2602.07032v1) 实际抓取成功（257 KB HTML，本轮 2026-08-13 取）。⭐ 本卡的 M 级断言全部来自该 HTML 全文，逐字片段附在各条后面。

⚠️ **这不是一篇缺陷检测工作，是一篇 benchmark 合成工作。** ⭐ 它对我们的价值集中在 **B1 的前半段（怎么造出「NL 规约 + 金标模型」配对）** 与 **B4 的裁决者构成**，⛔ 不在缺陷检测形态上。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `llm-fsm-benchmark-synthesis` |
| `title` | LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation |
| `year` | 2026（v1 提交 2026-02-03） |
| `venue` | ⛔ **arXiv preprint**，⛔ 原文无 comments 行、无 journal-ref、无投稿去向 |
| `ccf` | ⛔ **未收录**（预印本，无 venue） |
| `arxiv` | [arXiv:2602.07032](https://arxiv.org/abs/2602.07032)（⭐ 本轮实际访问；DOI `10.48550/arXiv.2602.07032`） |
| 作者 / 机构 | Yuheng Wu, Berk Gokmen, Zhouhua Xie, Peijing Li, Caroline Trippel, Priyanka Raina, Thierry Tambe —— ⭐ 全部 Stanford University |
| `artifact_type` | ⭐ **FSM**（Moore/Mealy，$\mathcal{M} = (S, s_0, I, O, \delta, \lambda)$）+ 其 fsm2sv YAML DSL 表示 + SystemVerilog RTL |
| `task` | ⭐ **benchmark 合成**（NL 规约 ← FSM 反向生成）+ **生成**（NL → RTL 评测） |
| `boundary` | ⭐ `界内` —— ⭐ 原文的机器元组逐字为 $\mathcal{M}=(S,s_{0},I,O,\delta,\lambda)$（§3.4），⛔ **无时钟变量、无不变式、无正交并发区**。⚠️ 但它有**同步时钟域的 cycle-level 时序语义**（失败模式之一逐字是 "Incorrect timing semantics"），⛔ 那与 TA 的时钟约束不是一回事，⛔ 也不等于我们的 $M=(S,E,V,Tr,A)$ 完全同构 |

---

## B. LLM 应用形态

### B1 · ⭐⭐ 流水线阶段（**反向合成链**，⛔ 这是本卡最有信息量的一格）

```
[确定性] 相位化拓扑采样（随机图生成器）
   → [LLM] 语义化 + 产出 fsm2sv YAML（起名 / 选场景 / 设计信号）
   → [确定性] 图同构校验（拓扑必须保持）        ← 门 ①：不过就丢弃
   → [确定性] fsm2sv 编译出参考 RTL
   → [确定性] 自研 testbench 合成器（覆盖全 state + 全 transition）
   → [LLM] 从 YAML 反向写 NL 规约 Σ = (Σ_IO, Σ_req)
   → [LLM] 从 Σ 再反推回 YAML  Ỹ（round-trip）    ← 门 ②：结构不一致就丢弃
   → [sound oracle] Yosys 序列等价检查 M vs M̃    ← 门 ③：找到反例就丢弃
   → [人] 20 例四准则人工审计
```

⭐ **阶段总数 9（含人工审计），⛔ 其中 LLM 阶段 3**（语义化 / 写 NL / round-trip 反推）。⭐ 其余 6 个全是确定性或人。

⭐⭐ **对 M1 最关键的观察**：⛔ **三道门全是「不过就丢弃」（rejection sampling），⛔ 没有任何一道是「不过就打回修订」。** ⭐ 这与我们的修订循环是**相反的形状** —— 详见 B4 与 E。

**M · 逐字（§3.1 Topology generation algorithm）**：
> "For each phase, we generate a minimal chain from entry to exit to ensure reachability, then add forward branches, back edges, and self-loops under user-controlled probabilities while capping the out degree. We add a reset block and connect phases in a simple cycle to guarantee global reachability. This ensures that every sampled abstract FSM is structurally valid."

**M · 逐字（§3.1 Phase-based abstract graph structure）**：
> "We represent each FSM using a two-level structure organized into phases. A phase corresponds to a coherent stage of operation, such as initialization, data transfer, or error handling. Each phase is a subgraph with a single entry and exit, and all internal states lie on paths between them."

**M · 逐字（§3.2，LLM 在语义化阶段被给了什么）**：
> "The prompt exposes the phase structure, the exact edge list, and asks the model to choose a realistic hardware scenario, assign descriptive names to all states, and design input and output signals. The model then produces an fsm2sv-compatible semantic FSM YAML file that specifies reset behavior, input and output declarations, and for each state, a list of guarded transitions and outputs that follow the provided connectivity."

⭐ **回答任务问题 1 的四个子问：**

| 子问 | 答案 | 级别 |
| :-- | :-- | :-: |
| ⭐ FSM 怎么随机生成？ | ⭐ **两级拓扑采样**：先在 phase 内造 entry→exit 最小链保证可达，再按概率加 forward branch / back edge / self-loop 并限制出度；再加 reset block、把 phase 串成简单环保证全局可达；最后采样 phase 间跳转边 | **M** |
| ⭐ 可配参数有哪些？ | ⭐ **state 数**、**transition 密度**、⭐ 各类边的**采样概率**（forward branch / back edge / self-loop）、⭐ **出度上限**、phase 数。⛔ 原文逐字只说 "a small set of topology parameters"，⛔ **未给完整参数清单与取值** | **M**（存在）/ ⛔ 清单**原文未提供** |
| ⭐ YAML 里有什么？ | ⭐ reset 行为、input/output 声明、⭐ 每个 state 的**带守卫迁移列表**与输出。⭐ 另外 LLM 还附一段 workflow 短故事（"the model also generates a short story of the workflow"） | **M** |
| ⛔ NL 规约由谁写？ | ⛔⛔ **由 LLM 写（`gpt-5` 经 OpenAI API），⛔ 不是人写。** ⭐ prompt 只暴露 I/O、reset 配置与迁移表，⛔ **刻意隐藏 state 名** | **M** |

**M · 逐字（§3.4 NL specification synthesis）**：
> "we first ask an LLM to produce an NL specification Σ = (Σ_IO, Σ_req). The prompt exposes only the inputs/outputs, reset configuration, and transition table, and requires: (1) an Inputs and Outputs section (Σ_IO) that lists every signal using the exact YAML names; and (2) a Requirements section (Σ_req) that paraphrases each group of transitions into requirements. This defines a forward map F : 𝒴 → Σ that hides state names but keeps the transition semantics."

**M · 逐字（§3.5 Generation runtime）**：
> "All semantic FSMs and NL specifications are generated using gpt-5 through the OpenAI API."

### B2 · 每次 LLM 调用的角色

| 阶段 | 角色 |
| :-- | :-- |
| 语义化 + YAML | ⭐ **生成器** + **解释者**（给无意义拓扑赋硬件语义） |
| NL 规约合成 | ⭐ **翻译器**（形式化 → 自然语言，⛔ 方向与我们相反） |
| round-trip 反推 YAML | ⭐ **翻译器**（NL → 形式化）+ ⛔ 事实上充当**一致性裁决者的前置**（它自己不裁决，只把候选交给 Yosys 裁） |
| 被评测的 18 个模型 | ⭐ **生成器**（NL → RTL / YAML / SystemC） |

⛔ **没有评审者、没有修复者、没有 LLM 自评裁决者。**

### B3 · prompt 策略

⭐ 合成侧：`zero-shot` + ⭐ **结构化输出约束**（必须产出 fsm2sv-compatible YAML；必须用 YAML 里的**原样信号名**；必须分 Inputs/Outputs 与 Requirements 两节）。评测侧：`zero-shot`，⛔ max output token 固定 **16,384**，⛔ temperature / top-p 用各模型默认值，指标 `Pass@1`。

⛔ **无 few-shot、无 CoT 显式提示、无 RAG、无工具调用、无多智能体辩论。** ⭐ 测试时扩展（§4.5）用的是 **multi-trace TTS（重复采样 + pass@k）**，⛔ 不是自我批判循环。

⛔ **prompt 全文未公开**（见 D）。

### B4 · ⭐⭐ 循环与裁决者

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无循环 | ⭐ **有，但是「丢弃并重采样」型（rejection sampling），⛔ 不是「打回修订」型** | **S**（从三道门都写 "discarded" / "the sample is discarded" 推出，⛔ 全文无任何 revise / feedback / repair 环节） |
| ⭐⭐ **裁决者是谁** | ⭐⭐ **三个裁决者串联，⛔ 各是不同类型**：<br>① ⭐ **确定性规则** —— 抽象图 vs YAML 的**图同构**校验<br>② ⛔ **LLM**（round-trip 反推 YAML；⚠️ 但它只负责产出候选，⛔ 判定权交给 ③）<br>③ ⭐⭐ **sound oracle** —— **Yosys 序列等价检查**（`equiv_make` / `equiv_simple` / `equiv_struct` / `equiv_status`），构造 sequential miter 搜索输出发散的输入序列<br>④ ⭐ **测试执行** —— 评测阶段用合成 testbench 做 **cycle-accurate** 比对 | **M** |
| 终止条件 | ⭐ **单次通过或丢弃**（无迭代预算概念）；⭐ 生成 1,500 候选 → 留 1,085 → 随机抽 1,000 | **M** |
| 最大轮数 | ⛔ **不适用**（无修订轮次概念） | **S** |
| ⭐ 有无报**循环边际收益** | ⛔ **无逐轮数字** —— ⭐ 但报了**逐门通过率**，⭐ 这是我们能拿到的最接近的东西（见下表） | **M** |

⭐ **逐门通过率（§3.5 Filtering statistics，逐字抄）**：

| 门 | 通过 | 率 |
| :-- | :-- | :-- |
| 输入候选 | 1,500 | — |
| ① 图同构 | 1,411 | ⭐ **94.1%** |
| ③ Yosys RTL 等价 | 1,085 | ⭐ **76.9%**（累积） |
| 最终随机抽取 | 1,000 | — |

⭐ **等价门通过率按难度衰减：Low 95.7% · Medium 82.1% · High 62.4%。**

**M · 逐字**：
> "Out of 1,500 generated candidates, 1,411 (94.1%) pass the isomorphism test, and 1,085 (76.9%) also pass RTL equivalence. Equivalence-check pass rates decrease with FSM size (95.7%, 82.1%, 62.4% across the three tiers)"

⭐ **成本结构（§3.5）**：⛔ 瓶颈**不在 LLM 而在形式化验证** —— 单个 FSM 的 Yosys 等价检查约 **30 秒**。逐字：
> "The dominant computational cost lies in verification: running Yosys's equivalence check on a single FSM typically takes ∼30 seconds, making formal checking the primary bottleneck of the pipeline."

### B5 · 中间表示

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无 | ⭐ **有** —— ⭐ **fsm2sv 兼容的 YAML FSM** 是全链路的枢轴表示（参考 RTL、testbench、NL 规约、round-trip 校验全部以它为源） | **M** |
| 形态 | ⭐ **DSL / JSON-schema 类**（YAML：reset 行为 + I/O 声明 + 每 state 的带守卫迁移与输出） | **M** |
| ⭐ **是否闭合** | ⚠️ **schema 闭合、内容开放** —— ⭐ YAML 的**字段结构**是固定的（必须 fsm2sv 可编译，否则丢弃），⛔ 但 state 名 / 信号名 / 守卫表达式 / 应用场景**全部由 LLM 自由生成**。⛔ **没有闭合谓词词表，没有缺陷类型学** | **S**（从 §3.2「asks the model to choose a realistic hardware scenario, assign descriptive names to all states, and design input and output signals」推出：内容侧无候选集约束） |
| ⭐ **谁定的** | ⭐ schema 由**外部既有工具 fsm2sv 定**（⛔ 不是本文发明）；⭐ 内容由 **LLM 自由生成** | **M** |

⭐⭐ **对我们「闭合 19 条 + LLM 自动选」这个组合，本文提供 0 个先例。** ⭐ 它证明的是另一件事：**把一个既有工具的 schema 当闭合约束用，然后让编译器/求解器当门**，这条路能把 76.9% 的产出留下来。

### B6 · 模型

| 用途 | 模型 |
| :-- | :-- |
| ⭐ **合成侧**（造 YAML + 造 NL） | ⭐ `gpt-5`（经 OpenAI API）—— ⛔ 原文未给日期版本号 |
| ⭐ **被评测**（18 个） | Claude-4.5-Sonnet · Claude-4.5-Haiku · gpt-5 · gpt-5-mini · gpt-5-nano · Gemini-2.5-Pro · Gemini-2.5-Flash · grok-4-fast-reasoning · DeepSeek-V3.1-Terminus · DeepSeek-R1-0528 · Qwen3-4B/8B/14B/32B · gpt-oss-20B/120B · Llama4-Scout / Llama4-Maverick |
| ⭐ **SFT 实验** | Qwen3-4B / 8B / 14B（QLoRA），⭐ 训练数据是 **Claude-4.5-Sonnet 的正确思维轨迹** |
| 教师 / 蒸馏来源 | Claude-4.5-Sonnet |

⭐ **有多模型对照，⭐ 且覆盖前沿与开源两侧 —— 这一点比我们（2 个模型）扎实得多。** ⚠️ 但**造数据的模型（gpt-5）也在被评测名单里**，⛔ 原文未讨论这构不构成偏袒（见 F）。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | 是否 sound |
| :-- | :-- | :-: |
| 拓扑采样器 | ⭐ 自研随机图生成器（相位化两级） | — |
| ⭐ 图同构校验 | ⭐ 确定性图算法（要求 $(u,v) \in E \iff (f(u), f(v)) \in \hat{E}$） | ⭐ 是 |
| ⭐ **fsm2sv 编译器** | ⭐ 第三方 YAML → SystemVerilog 生成器（⭐ 已核验：[github.com/mohamed/fsm2sv](https://github.com/mohamed/fsm2sv)，HEAD `c6a43f3f63`，18 文件，BSD-3-Clause） | ⭐ 是（机械翻译） |
| ⭐ testbench 合成器 | ⭐ 自研扩展：对每条边 $e=(u,v)$ 找 $s_0 \leadsto u$ 的路径并产出满足 $e$ 守卫的输入；⭐ 多项式时间；⭐ 保证全迁移覆盖 | ⭐ 是（覆盖保证） |
| ⭐⭐ **Yosys 等价检查** | ⭐⭐ **SAT 求解器**（sequential miter + 反例搜索） | ⚠️ **有条件** —— 见下 |
| 评测执行 | ⭐ cycle-accurate testbench 比对；SystemC 侧用 Questa 做 SystemC-SystemVerilog 联合仿真 | ⭐ 是 |

⚠️⚠️ **Yosys 那道门的 soundness 有明确的原文限定，⛔ 不是完全 sound。** 逐字（§3.4）：
> "If Yosys completes the check without reporting a mismatch, we accept the pair as behaviorally equivalent **for all executions explored by the checker**."

⭐ **这就是任务问题 2 的答案落点，⛔ 也是这篇的可信度天花板** —— 详见下一节。

---

## B-bis. ⭐⭐ 任务问题 2：「correct-by-construction」到底 correct 在哪一环？

⭐ **原文只在一处用这个词，⭐ 且它的辖域比标题里听起来的窄得多。** 逐字（§3.3 Reference RTL）：

> "Because the YAML format fully specifies each state, its outputs, and the ordered conditional transitions, the translation to synthesizable SystemVerilog is mechanical: every YAML transition becomes a guarded branch in the `always_comb` block, and state encodings are assigned in a consistent one-hot or counter style. **Since the YAML itself has already passed the topology-preserving isomorphism check, the resulting RTL is correct-by-construction relative to the input FSM.**"

⭐⭐ **所以 correct-by-construction 的确切含义是：**

$$\text{参考 RTL} \equiv \text{YAML}$$

⭐ **仅此一环。** ⭐ 它保证的是 **YAML → RTL 这一步是机械翻译，不引入错误**，⛔ 保证的**不是** NL 规约与 FSM 一致。

⭐⭐ **金标的可信度边界（逐环列，⛔ 这是本卡最该被 M1 读到的一段）：**

| 环 | 靠什么保证 | ⭐ 可信度 | ⛔ 漏在哪 |
| :-- | :-- | :-: | :-- |
| 拓扑 → YAML | ⭐ 图同构校验（确定性） | ⭐⭐ **高** | ⛔ 只管**边集**，⛔ **不管守卫语义**：LLM 可以给出连通性正确但守卫互斥/不完备的迁移，⛔ 同构门看不见 |
| YAML → 参考 RTL | ⭐ fsm2sv 机械编译 | ⭐⭐ **高**（这就是 "correct-by-construction" 那一环） | ⛔ 依赖 fsm2sv 自身正确；⛔ 原文未对 fsm2sv 做验证 |
| YAML → testbench | ⭐ 全迁移覆盖构造 | ⭐ **中高** | ⚠️ 覆盖 ≠ 充分：⭐ 保证每条边至少被走一次，⛔ **不保证暴露所有偏差**（评测判正误全靠它） |
| ⛔⛔ **YAML → NL 规约** | ⛔ **LLM 生成 + LLM round-trip + Yosys 等价** | ⛔⛔ **这一环是薄弱点** | 见下三条 |
| NL → RTL（被评测） | ⭐ cycle-accurate testbench | ⭐ **中高** | 同 testbench 那条 |

⛔⛔ **NL 那一环的三个具体漏洞：**

1. ⛔ **round-trip 的两端都是 LLM。** ⭐ 写 NL 的是 LLM，⭐ 从 NL 反推 YAML 的**也是** LLM。⚠️ 若两次调用**共享同一套隐含约定**（同一个 `gpt-5`、同一批 prompt 惯例），⛔ 一份对人类工程师**歧义**的规约完全可以被它自己**无歧义地**反推回去 —— ⭐ 于是 round-trip 通过，⛔ 但规约对人并不完备。⛔ **原文未讨论这个自一致性风险。**
2. ⚠️ **Yosys 检查的是两份 RTL，⛔ 不是「NL 是否说清楚了」。** ⭐ 它验证 $\mathcal{M} \equiv \widetilde{\mathcal{M}}$；⛔ 而 $\widetilde{\mathcal{M}}$ 来自 LLM 对 NL 的**一种**读法。⛔ 别的读法没被枚举。
3. ⚠️ **Yosys 自己也有限定** —— 逐字 "for all executions explored by the checker"，⛔ 即**未穷尽**。⚠️ 而它在 High tier 只有 **62.4%** 通过率，⛔ 原文未说未通过的是「NL 真的不等价」还是「求解器没跑完」。

⭐⭐ **一句话结论**：⭐ **「correct-by-construction」这个标签只覆盖 YAML→RTL 一环；⛔ 真正决定 benchmark 有效性的 NL→FSM 一致性，靠的是「LLM 写 + LLM 读 + SAT 校验两份 RTL」的组合，⛔ 那不是 correct-by-construction，⭐ 而是一个较强的 round-trip 过滤器。**

---

## B-ter. ⛔⛔ 任务问题 3：realism gap —— 原文讨论了，⛔ 但讨论得很薄

⭐⭐ **结论先给：⭐ 原文有一节专门讨论（§3.6 Alignment with Real-World Applications），⛔ 但它给出的全部证据是「一个协议的定性对照 + 一个词数对照」，⛔ 且⛔ 完全没有触及「模糊 / 遗漏 / 隐含约定」这三件我们真正在处理的事。**

⭐ **原文的全部 realism 证据（逐字抄，⛔ 一条不漏）：**

**① 定性 —— 一个 I2C 对照（§3.6 NL Distribution）**：
> "Qualitatively, our specifications share the narrative structure found in real-world datasheets. For instance, we compare the example in Figure 3 with a standard I2C-Master/Slave Core specification (32): • **LLM-FSM Spec**: 'After reset, the controller stays idle until the host asserts a read request (rd_req = 1), at which point it enters the mode-validation phase.' • **Real-World I2C Spec**: 'In the idle state, the core leaves the buses free and will be waiting for command. If there is a transaction in MODE bit from '0' to '1', the core will go to start, and will act as Master.' Both descriptions utilize a similar narrative structure."

**② 定量 —— 词数（§3.6）**：
> "Quantitatively, the real-world I2C specification, which describes a 7-state machine, contains 346 words. In our dataset, the subset of 7-state FSMs (41 problems) has an average length of 373.1 words. This consistency is also observed in other protocols. These comparisons confirm that our generated specifications closely mirror real-world application standards in terms of verbosity and information density."

**③ 人工审计 —— 20 例四准则（§3.7 全文抄）**：
> "(1) **State Coverage**: the specification must describe every YAML state with no missing or spurious behaviors. (2) **Transition Coverage**: every YAML transition must be reflected in the specification, with no extra or altered edges. (3) **Specification-FSM Alignment**: the narrative must allow an unambiguous mapping from each described behavior back to the YAML-specified FSM. (4) **Hardware Plausibility**: state names, signal names, and contextual descriptions must form a coherent and realistic hardware scenario. All 20 inspected samples satisfy these criteria"

**④ 间接 —— 与人写 benchmark 的相关性（§4.3）**：⭐ Pearson / Spearman 与 VerilogEval 为 **0.83 / 0.87**，与 RTLLM 为 **0.84 / 0.83**（overall avg 列）。

⭐⭐ **我方评估：⛔ 这四条证据一条都不能证明「合成规约像真实工程需求」，⭐ 而第 ③ 条实际上**反向**证明了 gap 的存在。**

| ⭐ 我们关心的真实需求特征 | ⛔ 原文的处理 | ⛔ 后果 |
| :-- | :-- | :-- |
| ⭐⭐ **模糊**（一句话可有多种读法） | ⛔⛔ **准则 ③ 逐字要求 "unambiguous mapping"**，⭐ 即**歧义被当成缺陷主动剔除** | ⛔⛔ **合成语料里的规约是被筛成无歧义的。⭐ 这不是 gap 没被讨论，⭐ 是 gap 被设计进去了 —— 它构造的恰恰是我们处理对象的补集** |
| ⭐⭐ **遗漏**（规约没说完） | ⛔⛔ **准则 ①② 逐字要求全 state / 全 transition 覆盖，"no missing or spurious"**；⭐ round-trip + Yosys 门在流水线层面把不完备样本**全部丢弃** | ⛔⛔ **合成语料里结构性遗漏被系统性清零** |
| ⭐⭐ **隐含约定**（工程师默认不写的领域常识） | ⛔⛔ **原文完全未提。** ⭐ 恰恰相反：prompt 强制规约"lists every signal using the exact YAML names" —— ⛔ 即**所有信息都显式写出，且用词与模型内部标识符逐字一致** | ⛔⛔ **合成语料里没有隐含约定，⭐ 而真实需求里最难的部分正是这些** |
| ⭐ 叙述风格与长度 | ⭐ **这一条原文确实给了证据（① ②），⭐ 且结论可信** | ⭐ 风格与信息密度像；⛔ 但**信息完备度不像** |
| ⭐ 术语 / 场景合理性 | ⭐ 准则 ④ + LLM 自选"realistic hardware scenario" | ⭐ 表面像 |

⭐⭐ **一句话给 M1**：⭐ **它像「机器把 FSM 翻译成英文，然后把翻译得不够干净的都扔了」——⭐ 而这正是任务里的猜测，⛔ 且原文自己的四条人工准则逐字确认了这一点。** ⛔ 风格像、长度像、术语像；⛔ **完备度、歧义度、隐含度三个维度都被主动清洗掉了。**

⭐⭐ **对我们能不能用的裁定：**

| 用途 | 可否 | 理由 |
| :-- | :-: | :-- |
| ⭐ 反向合成**技法**（拓扑采样 → 语义化 → 编译金标 → round-trip 过滤） | ⭐⭐ **可以搬** | ⭐ 这套形状与我们的语料无关，是纯工程手法 |
| ⭐ 用它造**「NL 需求 + 模型」配对**来扩我们的 54 pair | ⛔⛔ **不可以直接用** | ⛔ 造出来的 NL 在**歧义 / 遗漏 / 隐含**三个维度上被清洗过，⛔ 而我们 discover 任务的**全部难度就在这三个维度上**。⭐ 拿它扩库会系统性地把任务变简单，⛔ 且这种简化**不可见**（表面词数与风格都对） |
| ⭐ 用它当**难度可控的压力测试**（只测结构推理，不测需求理解） | ⭐ **可以，但要声明** | ⭐ 它能回答「模型在 60 个 state 的 FSM 上还能不能保持结构一致」，⛔ 回答不了「模型能不能读懂人写的需求」 |
| ⛔ 若要用，**必须补一步反向脏化** | ⚠️ **待设计** | ⭐ 即在干净规约上**注入**歧义 / 删除 / 隐含化，并把注入记录当 ground truth。⛔ 原文没有这一步，⛔ 也没有任何人做过（本轮未找到） |

---

## C. 实验

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `baseline` | ⭐ **有** —— ⭐ 两个人写的 RTL benchmark 作对照：**VerilogEval v2** 与 **RTLLM v2**。⛔ 但注意：它们是**相关性对照**，⛔ 不是同任务上的方法 baseline（本文不提方法，只提 benchmark） | **M** |
| `dataset` | ⭐ **LLM-FSM，1,000 题**，三难度档：**Low 334 · Medium 333 · High 333**。⭐ **分母怎么定的**：1,500 候选 → 图同构留 1,411 → 等价留 1,085 → ⭐ **随机抽 1,000** 定档 | **M** |
| 规模与难度（⭐ 任务问题 4） | 见下表 | **M** |
| `metrics` | ⭐ **`Pass@1`** 为主（"counting a sample as correct only if the generated RTL compiles and passes the reference testbench"）；⭐ TTS 实验另报 **`pass@k`**（k 到 16）| **M** |
| ⭐ `judged_by` | ⭐⭐ **自动执行判定**（编译 + cycle-accurate testbench 比对，⛔ **不是 LLM-as-judge**）。⭐ 数据质量侧另有 **20 例作者人工审计**。⛔⛔ **无标注者间一致性、无 $\kappa$、⛔ 未说审计者是谁、⛔ 未说是几个人** | **M**（自动判定）/ ⛔ 一致性**原文未提供** |
| `human_baseline` | ⛔ **无** —— ⛔ 没有「人类工程师在这些题上能拿多少分」的对照 | **S** |
| `runs` | ⛔⛔ **主表是单次采样（Pass@1），⛔ 无重复、⛔ 无方差、⛔ 无置信区间。** ⭐ 只有 §4.5 的 TTS 实验做了多次采样（pass@k），⛔ 但那是**另一个实验**，⛔ 不是给主表加误差棒 | **M / S** |
| ⭐ `adverse_results` | ⭐ **不利结果报得相当坦率**（见下） | **M** |

⭐ **任务问题 4 · 规模与难度分级（Table 2 逐字抄）**：

| Tier | Count | States | Avg. Edges | Avg. Phases | Avg. Spec Word Count | Avg. Ref Code Lines |
| :-- | --: | :-- | --: | --: | --: | --: |
| Low | 334 | 4–14 | 11.95 | 2.71 | 409.3 | 154.8 |
| Medium | 333 | 14–27 | 32.17 | 5.24 | 780.3 | 301.8 |
| High | 333 | 27–59 | 65.39 | 8.83 | 1265.1 | 501.3 |
| **Overall** | **1000** | **4–59** | **36.48** | **5.59** | **817.8** | **319.1** |

⭐ **难度怎么控**：⭐ **靠 state 数分档**（"partitioned into three difficulty tiers based on the number of FSM states"），⭐ 而 state 数、边密度、结构约束都是拓扑采样器的**可配参数**。⭐ 原文明确把「难度可随模型变强而上调」当成本文的一个卖点。

⭐⭐ **`adverse_results` 的处理（⭐ 这一格对我们直接可借鉴）**：

1. ⭐ **主结果对自己不利也照写**：18 个模型 × 3 条评测管线，**总体平均 Pass@1 只有 41.1%**。逐字：
> "across 18 frontier models and three evaluation pipelines, the overall average Pass@1 is only 41.1%"
2. ⭐ **最好的模型也报它掉下去的那一档**：Claude-4.5-Sonnet 总分 **80.3%**，⛔ 但 hard tier **65.6%**。逐字：
> "Claude-4.5-Sonnet achieves the highest score of 80.3%, yet its performance drops to 65.6% on the hard tier."
3. ⭐⭐ **管线间的巨大不一致被单独立成一个 finding，⛔ 没有藏**：Gemini-2.5-Pro 在 Spec→YAML→RTL 上 **70.4%**，在 Spec→SystemC 上只有 **17.9%**。⭐ 原文把它写成小节标题："Different evaluation pipelines lead to sharply different outcomes across models"。
4. ⭐⭐ **一个「削弱自己动机」的结论也照写**：⭐ Spec→RTL 与 Spec→YAML→RTL 平均分接近，⭐ 原文据此说**模型不需要显式重建 FSM 结构**。⛔ 这实际上削弱了「中间表示有用」这条叙事，⭐ 但他们照写了。逐字：
> "the Spec → RTL and Spec → YAML → RTL pipelines yield similar average accuracies, indicating that modern LLMs are able to perform finite-state reasoning directly in RTL without explicitly reconstructing the FSM structure in YAML."
5. ⭐ **等价门通过率随难度下滑（95.7% → 82.1% → 62.4%）照写，⛔ 未粉饰**，⭐ 只补一句「仍足以靠加预算或分层生成扩展」。
6. ⚠️ **Yosys soundness 的限定语照写**（"for all executions explored by the checker"）—— ⭐ 这是主动标注自己方法的上界。
7. ⭐ **四类失败模式逐类列出**（§4.3 Error analysis）：⛔ Syntax errors · ⛔ **Incorrect timing semantics** · ⛔ **State or transition mistakes** · ⛔ Formatting errors。

⛔ **但也有两处不利面**没**处理**：⛔ 主表无方差（单次采样就下结论），⛔ 造数据的 `gpt-5` 也在被评测名单里而未讨论偏袒（见 F）。

⭐ **相关性（Table 4）**：与人写 benchmark 的 overall avg 相关 —— VerilogEval **P 0.83 / S 0.87**，RTLLM **P 0.84 / S 0.83**；⛔ 但 Spec→SystemC 那条管线相关性明显低（**0.66/0.62** 与 **0.59/0.52**）。

⭐ **SFT（Table 5，⛔ 训练只用 Easy/Medium 的 80%，Hard 全部留作 OOD）**：Qwen3-14B overall **27.9% → 62.2%**，Hard(OOD) **4.5% → 34.3%**；Qwen3-4B overall **6.5% → 15.4%**，Hard **0.0% → 4.5%**。

⭐ **TTS（§4.5）**：⭐ **multi-trace TTS（重复采样）有效，⛔ 单轨「先想再答」明显更弱** —— Qwen3-14B 的 thinking-mode `pass@1` 远低于它自己 multi-trace 的 `pass@16`。⚠️ **这条与我们「自我批判 loop 零收益」是同向证据**：⛔ **在同一条轨上反复加思考不如换一条轨重采样。**

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [arxiv.org/html/2602.07032v1](https://arxiv.org/html/2602.07032v1) | ⭐ 本轮实际下载：257,869 字节 HTML，⭐ 正文全节可读（§1–§5 + References）。⭐ abs 页提供 "HTML (experimental)" 与 TeX Source |
| ⭐ **实验代码**（拓扑采样器 / testbench 合成器 / 评测脚本） | ⛔ ⚪ | — | ⛔⛔ **原文明确未提供任何代码入口**。⭐ 全文机械检索：`available` **0 次** · `release` **0 次** · `artifact` **0 次** · `reproduc*` **0 次** · `anonymous` **0 次** · `huggingface` **0 次**；⭐ `github` 5 次**全部出现在 References 里**（fsm2sv 的 venue 字段写作 "GitHub"）。⛔ **无 data/code availability statement** |
| ⭐ **数据集 / Benchmark**（1,000 题） | ⛔ ⚪ | — | ⛔⛔ **未放出。** ⭐ 论文只给统计表（Table 2），⛔ 无下载入口、⛔ 无 HF dataset、⛔ 无 Zenodo DOI。⚠️ **这是本卡最大的可用性缺口** —— ⭐ 方法可读，⛔ 数据拿不到 |
| ⭐ **依赖工具 `fsm2sv`**（第三方，⭐ 是它的确定性底座） | ⭐ 🟢 | [github.com/mohamed/fsm2sv](https://github.com/mohamed/fsm2sv) | ⭐ `tools.verify_assets` 输出逐字：`HEAD c6a43f3f63 · 文件 18（非文档 16）· release 2 · license BSD-3-Clause` → ⭐ 机械判 🟢，⭐ 人工复核同意（⭐ 有实际源码、有 release、有 license）。⚠️ **但本文对它的 testbench 扩展未放出** |
| 依赖工具 `Yosys` | ⭐ 🟢 | [github.com/YosysHQ/yosys](https://github.com/YosysHQ/yosys) | ⭐ 原文逐字点名 `equiv_make` / `equiv_simple` / `equiv_struct` / `equiv_status` 四个命令，⭐ 均为 Yosys 公开 equiv 流程；⛔ 本轮未对该仓库单独跑 verify_assets（⭐ 属公认成熟工具，⛔ 但按纪律记为未机械核验） |
| 依赖工具 `Questa` | 🔒 | — | ⛔ 商业 EDA（SystemC-SV 联合仿真用），⛔ 需许可证 |
| 实验结果细则 | 🟠 | 论文内 Table 2–5 + Figure 4–5 | ⭐ 有完整的**汇总表**（18 模型 × 3 管线 × 3 难度档），⛔ **无逐题结果**、⛔ 无逐次采样记录、⛔ 无 raw output |
| Artifact / 复现包 | ⛔ ⚪ | — | ⛔ 无 Zenodo / 4open / OSF DOI |
| ⭐ **prompt 是否公开** | ⛔ ⚪ | — | ⛔⛔ **未公开。** ⭐ 原文只**描述** prompt 暴露了什么（"The prompt exposes the phase structure, the exact edge list…"、"The prompt exposes only the inputs/outputs, reset configuration, and transition table"），⛔ **无附录、⛔ 无逐字 prompt 文本** |
| 拓扑参数取值 | ⛔ ⚪ | — | ⛔ 逐字只说 "a small set of topology parameters"，⛔ **概率值、出度上限、phase 数分布全部未给** → ⛔ **无法复现生成分布** |

⭐⭐ **D 节一句话**：⭐ **论文本身 🟢 且写得清楚，⛔ 但方法链上凡是「我们自己做的」部分（采样器 · testbench 合成器 · prompt · 参数 · 1,000 题数据）全部 ⚪，⛔ 只有两个第三方依赖（fsm2sv / Yosys）是 🟢。** ⛔ **这意味着「照它的方法造一批」要从零重写，⛔ 且分布不可能对齐。**

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处（⭐ 具体到哪个设计决定可以搬）

1. ⭐⭐ **「不过就丢弃」替代「不过就打回修订」。** ⭐ 这是本卡对 M1 最直接的一条。⭐ 他们的三道门（同构 / round-trip / Yosys）**没有一道**给生产者回灌反馈让它改；⛔ 一律丢弃并重采样，⭐ 用 **1,500 → 1,000** 的产出率换掉整套修订机器。⭐ 对照我们的实测（修订机器吃 **79%** token、覆盖净变化 ≈ 0、第 3–5 轮零收益）：⭐ **在同样的 token 预算下，把「一次生成 + 硬门 + 丢弃 + 重采样」跑 N 遍，很可能优于把一份产物修 5 轮。** ⭐ 而且丢弃路径的实现复杂度远低于修订路径。
2. ⭐⭐ **裁决者分层：便宜的确定性门放前面，贵的 sound oracle 放后面。** ⭐ 图同构（近乎零成本）先滤掉 5.9%，⭐ 再让 30 秒/例 的 Yosys 处理剩下的。⭐ 我们现在是 `precheck_and_seal` 一道门包办；⭐ **可以拆成「零成本结构门 → pyfcstm 求值门」两级**，⭐ 把最贵的检查留给已经过了廉价门的候选。
3. ⭐⭐ **拿既有工具的 schema 当闭合约束，而不是自己发明。** ⭐ 他们把 `fsm2sv` 的 YAML 格式直接当输出契约 —— ⭐ 好处是**编译器天然成为门**（编不过就是不合法），⛔ 而且这个契约的正当性来自外部工具而非本文自述。⭐ 我们的 pyfcstm DSL 已经具备同样的性质，⛔ 但我们目前把它放在**求值端**；⭐ 这篇提示可以把它更早地当**生成契约**用。
4. ⭐ **难度轴要是**可配参数**而不是**固定语料**。** ⭐ 他们把 state 数 / 边密度 / 出度上限做成生成器参数，于是「难度」可以随模型变强而上调。⛔ 我们的 54 pair 是固定的，⛔ 一旦模型变强就会饱和。⭐ 这条对我们**后续代次**有价值，⛔ 对当前 G1 无直接作用。
5. ⭐ **「多轨重采样 > 单轨深思」这条实测与我们同向。** §4.5 逐字给出 Qwen3-14B thinking-mode `pass@1` 远低于其 multi-trace `pass@16`。⭐ 这为我们「拆掉两个 LLM 自评 reviewer、把 token 换成多轮独立采样」提供了一条**外部同向证据**（⛔ 但它是 RTL 生成任务上的，⛔ 不是缺陷检测任务上的）。
6. ⭐ **不利结果的写法可直接借鉴。** ⭐ 他们把「管线间 70.4% vs 17.9% 的巨大不一致」和「中间表示其实没帮上忙」都**单独立成 finding 小节**而不是塞进 limitations。⭐ 我们手上的 **−15.82pp** 可以照这个写法处理：⭐ **把它写成一个 finding（「自我批判循环在本任务上不产生正收益」），⛔ 而不是一个致歉。**

### 2. ⛔ 不可取 / 陷阱（⭐ 尤其：它有没有踩我们已经踩过的坑）

1. ⛔⛔ **它踩了一个我们必须避开的坑：用 LLM 检验 LLM 的产出，两端同源。** ⭐ round-trip 的写方与读方都是 `gpt-5`。⛔ 虽然最终裁决交给了 Yosys（这救了它一半），⛔ 但**「NL 是否对人足够清楚」这个问题从头到尾没有任何非 LLM、非同源的检验**。⚠️ 这与我们两个 LLM 自评 reviewer 的失效**是同一类结构性问题**：⛔ **裁决者与被裁决者共享同一套隐含约定时，通过率不度量质量。**
2. ⛔⛔ **它的人工审计规模不足且口径不明。** ⭐ **20 例 / 1,000 题 = 2%**，⛔ 全部通过（20/20），⛔ 未说审计者是谁、⛔ 未说几个人、⛔ 无 $\kappa$、⛔ 无分歧记录。⚠️ **「全部通过」在 20 例上几乎不含信息**（若真实合格率是 90%，抽 20 例全过的概率约 12%）。⛔ **不要照抄这个规模** —— ⭐ 我们自己 574 位逐位判定的做法比它扎实得多，⛔ 不要因为「别人只做 20 例」而退让。
3. ⛔⛔ **主表单次采样就下结论，⛔ 无方差。** ⛔ 18 模型 × 3 管线 × 1000 题全是 `Pass@1` 单跑。⚠️ 而我们已经用 `hit@1 / hit@3 / hit@all` 证明单轮数字**区分不了「稳定」与「碰上」**。⛔ **不要退回单轮口径。**
4. ⛔ **造数据的模型在被评测名单里，⛔ 原文未讨论。** ⭐ `gpt-5` 既写 YAML 又写 NL 规约，⛔ 同时又作为 18 个被评测模型之一（`gpt-5` 总分 75.4%，第二名）。⛔ 原文对这是否构成分布偏袒**一字未提**。⚠️ **这在我们仓库的 §3.5 口径下会被判 C 级（实验公平性）。** ⭐ 若我们借用它的合成技法，**必须避免用同一个模型既造语料又当被测对象**。
5. ⛔ **"correct-by-construction" 这个词被用得比它保证的范围宽。** ⭐ 它只覆盖 YAML→RTL 一环，⛔ 但标题式表述容易被读者理解成「整个 benchmark 的金标是构造正确的」。⚠️ **我们自己写论文时不要犯同一个措辞错误** —— ⭐ 凡说「构造正确」必须写清 correct **relative to what**。
6. ⛔ **难度只用 state 数一个轴。** ⭐ Table 2 里边密度、phase 数与 state 数几乎完全共线（11.95/32.17/65.39 与 2.71/5.24/8.83 同步涨），⛔ 于是「难度上升导致准确率下降」这个结论**无法归因到具体哪一维**。⛔ 别照搬这个分档方式。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么它的做法不能直接照搬）

1. ⛔⛔ **任务方向相反。** ⭐ 我们做 **NL + 模型 → 找出模型里的缺陷**；⭐ 它做 **NL → 造出正确的模型**。⛔ 于是它**根本不需要缺陷类型学、不需要谓词词表、不需要判定「这是不是一条发现」** —— ⭐ B5 那格对我们的问题给不出答案（⭐ 我们「闭合 19 条 + LLM 自动选」在本卡里先例数 **0**）。
2. ⛔⛔ **它的 NL 是被清洗过的，⛔ 我们的 NL 是脏的 —— ⭐ 而脏就是我们的问题本身。** ⭐ 见 B-ter：⛔ 歧义被准则 ③ 主动剔除、⛔ 遗漏被准则 ①② 与 round-trip 门清零、⛔ 隐含约定被「用原样信号名」的 prompt 约束消灭。⛔ **拿它的语料测我们的方法，会测出一个偏高且不可见的分数。**
3. ⚠️ **它有一个我们没有的东西：一个能判「两个模型是否行为等价」的 sound oracle（Yosys）。** ⭐ RTL 有商业级序列等价检查；⛔ pyfcstm DSL 状态机没有对应工具。⭐ 我们的 `precheck_and_seal` 能求值单个谓词，⛔ 但不能回答「这两份状态机是否等价」。⛔ **所以它「用等价检查当终审门」的做法我们照搬不了**，⭐ 只能搬「把最强的确定性检查放在最后一道门」这个**位置安排**。
4. ⚠️ **成本结构相反。** ⭐ 它的瓶颈在验证（Yosys 30 秒/例），LLM 便宜；⛔ 我们的瓶颈在 LLM（修订机器 79% token），确定性检查近乎免费。⛔ **所以它「多生成、多丢弃」的策略在我们这边更划算，⛔ 而不是更不划算** —— ⭐ 这一点反而加强了 E1.1 那条建议。
5. ⚠️ **资产不可得，⛔ 所以「照它做一批」的成本被严重低估。** ⭐ 见 D 节：⛔ 采样器 / testbench 合成器 / prompt / 参数 / 1,000 题**全部 ⚪**。⛔ **不要在 M1 的计划里把「复用 LLM-FSM 的合成流水线」当成低成本选项** —— ⭐ 那是从零重写，⛔ 且分布无法对齐、结果不可与本文比较。

---

## F. 存疑与未核项

1. ⚠️ **拓扑采样器的具体参数取值未知** —— 已试过：⭐ 全文检索 `probabilit*` / `parameter` / `degree` / `Appendix`；⛔ 结果：原文逐字只说 "a small set of topology parameters" 与 "user-controlled probabilities"，⛔ **无数值、无附录、无补充材料链接**。⛔ **后果：生成分布不可复现。**
2. ⚠️ **1,000 题数据集与全部代码是否会放出，未知** —— 已试过：⭐ 全文机械检索 `available`(0) / `release`(0) / `artifact`(0) / `reproduc*`(0) / `github.com`(0 处正文命中) / `huggingface`(0) / `anonymous`(0)；⛔ 结果：**无任何 availability statement**。⛔ 未试：给作者发信（超出本轮范围）。
3. ⚠️ **摘要说 "human review on a subset"，⛔ 但审计者身份、人数、是否有第二审、有无分歧全部未知** —— 已试过：⭐ 通读 §3.7 全文（该节仅 6 句）；⛔ 结果：只有「All 20 inspected samples satisfy these criteria」，⛔ **无 $\kappa$、无一致率、无审计者描述**。⚠️ **按我方 schema 的 `judged_by` 口径，这一格只能记「作者自审、无一致性证据」。**
4. ⚠️ **造数据的 `gpt-5` 同时是被评测模型之一，⛔ 原文未讨论是否构成偏袒** —— 已试过：⭐ 全文检索 `contamination` / `leak` / `bias` / `fair`；⛔ 结果：**0 命中**。⛔ 这是我方判断（**I 级**），⛔ 不是原文承认的问题。
5. ⚠️ **`gpt-5` 的具体版本日期未知** —— ⛔ 原文逐字只写 `gpt-5`，⛔ 无 snapshot 日期。⚠️ 按 schema B6 的要求（"GPT-4o (2024-05)" 那样），⛔ **这一格无法填全**。
6. ⚠️ **Yosys 未通过的 23.1% 里，「NL 真的不等价」与「求解器未跑完」的比例未知** —— 已试过：⭐ 读 §3.4 与 §3.5 全文；⛔ 结果：原文只给通过率与 "for all executions explored by the checker" 的限定，⛔ **未区分 SAT / UNSAT / timeout / inconclusive**。⚠️ **这直接影响「金标有多硬」的判断，⛔ 但无法从原文解决。**
7. ⚠️ **Figure 3 的完整合成规约样例只在图里，⛔ HTML 文本提取拿不到图内文字** —— 已试过：⭐ arXiv HTML 抽文本；⛔ 结果：图为图像/复杂排版，⛔ 正文只引了其中一句（B-ter 里那句 rd_req 例）。⛔ 未试：下载 PDF 或 TeX source 逐字取图内规约全文（⚠️ 本轮时间预算内未做）。⚠️ **后果：无法对合成规约做逐句的歧义/完备度审查，⛔ B-ter 的裁定依据的是原文自述的四条准则而非样例实物。**
8. ⚠️ **"This consistency is also observed in other protocols" 这句无数据支撑** —— ⛔ 原文只给了 I2C 一个协议的词数对照（346 vs 373.1），⛔ 其余协议**一个数字都没给**。⚠️ 按我方口径这属于**无证据的概括**。
9. ⚠️ **Yosys 仓库本轮未跑 `tools.verify_assets`** —— ⭐ 只核了 `fsm2sv`。⛔ 按纪律记为未机械核验（⭐ 虽属公认成熟工具）。
