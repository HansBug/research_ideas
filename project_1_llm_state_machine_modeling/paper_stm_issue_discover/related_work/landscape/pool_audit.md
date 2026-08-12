# 起点池审计（层 1 产出）

⭐ 本文件是 L1 层 1 的**起点池预筛结果与失配报告**。⛔ 它不下任何档位结论 —— 落档要等层 1′ 的外检索补完、且需正文佐证（`CONTINGENCY_L1.md` §0.1.5 第 3 条）。

⛔ **本文件的一切判断都是「表格级」的**，即只读 `SUMMARY.md` 的逐篇表，⛔ 未读任何一篇正文。按 `CONTINGENCY_L1.md` §0.1.5 第 3 条，「正文读了没」一律计为**未读**。

---

## 1. 边界门：⛔ 「形式主义」列不是充分判据

⭐ 判据用**双条件**，对 **669 行主表**逐行判，任一为真即剔除：① 「形式主义」列命中界外关键词；② 「主类」列 emoji ∈ {⏱️ 时间/时钟自动机, 🌊 混成/随机, 🕸️ Petri 网}。

⛔⛔ **本节数字于 2026-08-12 经独立核验更正，⭐ 并落盘为可复现脚本 [boundary_gate.py](./boundary_gate.py)。**

| 判据 | 剔除行数 |
| :-- | ---: |
| 仅「形式主义」列命中 | **99** |
| 仅「主类」emoji 命中 | **14** |
| 两者同时命中 | **152** |
| **合计剔除** | **265 / 669（39.6%）** |
| **界内候选池** | **404** |
| ⭐ 其中 2022 年起 | **34**（⭐ 这一个数初版就是对的） |

⚠️ **初版报的是 `242 / 427`、拆分 `76 / 18 / 148`，⛔ 那组数不可复现。** ⭐ 病因不是算错，是**只用散文描述界外关键词**（「UPPAAL 系、PRISM/MRMC、CPN/GSPN、mCRL2/BIP、混成」）而不给词表、不给脚本。⚠️ 独立复核者按那段散文反推得 `261 / 408`，且 `仅emoji` 与 `两者同时` 两项**无论怎么收窄词表都到不了 18 / 148**。

⛔⛔ **而这恰恰是初版自己用来批评上一版「692 行里 212 行」的同一条罪状** —— ⭐⭐ **一个依赖词表的计数，词表就是它的一部分**；把百分比写进文档而把词表留在脑子里，等于交出一个不可复核的数。⭐ 现已把词表与判据全部落进脚本，`python3 boundary_gate.py --audit` 可逐项复现。

剔除集的「主类」分布（⭐ 脚本实测）：⏱️ **94** · 📦 **86** · 🌊 **45** · 🕸️ **27** · 🔣 **6** · 🔌 **6** · 🧩 **1**。⚠️ 那 1 行 🧩（界内 emoji）是被**关键词判据**捞走的 —— ⭐ 说明两条判据确实各自独立起作用。剔掉的主要是：时间自动机及其工具生态（UPPAAL 系、TIOA、参数化/代价/博弈 TA 变体）· 概率与统计模型检查器（PRISM、MRMC、VESTA、Ymer）· Petri 网全族（P/T、CPN、GSPN、PNML/ISO 15909）· 进程代数与 BIP 系（mCRL2、BIP/D-Finder）· 混成自动机与 CPS 连续动力学。

### ⚠️ 「单靠那一列会漏」这个诊断只**部分**成立

⚠️ 初版称实测 **40 行**「形式主义」列干净、却在**标题 / 论文角色 / 关键特性**里含界外词。逐条看过，分三类：

| 类 | 例 | 后果 |
| :-- | :-- | :-- |
| ⚠️ **原列为「真界外、被门漏掉」，⛔ 但两个举例是错的** | ⛔ `translating-uml-state-machines-to-coloured-petri-nets` 的形式主义列**逐字含 `CPN`**；⛔ `towards-verifying-safety-properties-of-real-time-probabilistic` 的该列**同时含 `PTA` 与 `PRISM`` —— ⭐ 三个词都在词表里，**这两行本就该被判据①捞走**，⛔ 不是「列干净」的反例。⚠️ `turtle-a-real-time-uml-profile` 的该列含 `RT-LOTOS`，它能逃掉只说明初版实际词表**不含 LOTOS**（现已补入）。⭐ 只有 `a-runtime-environment-for-contract-automata` 的列确实干净（`Contract Automata / CARE`），⚠️ **但判它「真界外」也可疑** —— 形式主义本体是 Contract Automata（无时钟），UPPAAL 只是外挂的 validation 手段，⛔ 「用了 UPPAAL」≠「对象是时间自动机」 | ⭐⭐ **诊断因此要改**：至少部分漏网是**词表不全**，⛔ 不是「那一列不够」。⚠️ **两者的修法完全不同**：前者补词（已做），后者才需要多列判据 |
| ⭐ **部分可用** | HUGO（`model-checking-and-code-generation-for-uml-state-machines-and-collaborations`）：PROMELA/SPIN 分支**界内**、UPPAAL 分支界外 · RoboChart 系：本体界内、`timed primitives` 与 CSP 语义分支界外 · `institution-based-encoding...CASL-SPASS`：界内（"simple UML" 已排除并发） | ⭐ 必须**落到具体章节**才能用 |
| ⚠️ **误报** | `counter-machines-and-counter-languages`（术语是 `real-time counter machine`）· `difference-decision-diagrams`（服务时钟约束但对象是 BDD 变体） | ⚠️ 不应剔除 |

⭐ **结论**：层 1 的剔除只是**初筛**。⛔ 每一篇仍须由层 1b / 层 2 落到具体章节再判。

---

## 2. Q1 · 六个候选类目的起点池覆盖

| 类目 | 起点池界内篇数 | 其中 2022+ | 判定 |
| :-- | ---: | ---: | :-- |
| ① 模型检查（LTL/CTL/BMC） | ≥ 12 | 3 | ⭐ 满 3 篇 |
| ② 一致性与 conformance testing | ≥ 9 | 2 | ⭐ 满 3 篇 |
| ③ 静态规约检查（OCL / well-formedness） | **3，且全为「部分」** | **0** | ⛔ 不满足 2022+ 门槛，须外检索 |
| ④ 仿真与执行 | ≥ 10 | 3 | ⭐ 满 3 篇 |
| ⑤ **LLM 辅助评审 / 缺陷检测** | **0** | 0 | ⛔ **起点池根本没有** |
| ⑥ **变形 / 差分测试** | **0** | 0 | ⛔ **起点池根本没有** |

⛔ **不落 A/B/C 档** —— 落档要看外检索补完后的总数。

### ⭐ 类目 ⑤ 的那个 0 是可信的，⛔ 且比已知陷阱更强

已知陷阱是：`grep -li 'LLM' state_machine_types/*/desc.md` 命中 296 篇，抽查全是我方在「对本研究的启发」里写的推测。⭐ **本轮换了口径**：对 669 行 × **17 列全字段**扫 `\bLLM\b|large language|GPT|大语言模型|ChatGPT|Codex|prompt`，命中 **0**。⛔ 也就是说总表这一侧**连注释都没有**，是干净的 0。

⚠️ ⛔ **但这是关于起点池的事实，不是关于领域的事实**（`CONTINGENCY_L1.md` §0.1.7）。

### ⚠️ 类目 ③ 的实况

全仓目录名匹配 `ocl|well.?form|constraint` 只有 9 个，其中 6 个是时间自动机 / Petri 网（界外）、2 个是 `well-formed CRSM`（fork-join 并发，界外）。⛔ **OCL 本体、UML well-formedness rule 检查器、模型 smell / anti-pattern 检测在起点池里一篇都没有。**

界内那 3 篇全为「部分」：`automating-verification-of-state-machines-with-reactive-designs-and-isabelle-utp`（RoboChart 的 well-formedness 机械化，⚠️ CSP 语义分支界外）· `robochart-modelling-and-verification-of-robotic-applications`（metamodel + well-formedness，⚠️ timed primitives 界外）· `modelling-system-of-systems-interface-contract-behaviour`（SysML/OCL 契约视图）。⛔⛔ **初版称它是「本池唯一沾 OCL 的界内条目」，那是错的**，⚠️ 且错因是**同一份文件里用了两套检索方法论** —— 对 LLM 用 17 列全字段扫（还特意宣传），对 OCL 却退回目录名 grep。⭐ 用 17 列扫 `\bOCL\b|well.?formed|smell|anti-pattern` 得 **9** 行，界内的除上述 3 篇外还有：`coordinating-robotic-tasks-and-systems-with-rfsm-statecharts`（🔣 2012，构造方式含 **Ecore/OCL**，⭐ 比那篇 SysML 契约视图更贴近类目③）· `verification-of-succinct-hierarchical-state-machines`（🧩 2007）· `compatibility-checking-for-asynchronously-communicating-software`（🔌 2014）。⭐ **行动结论不受影响**：新增的 3 篇全在 2022 年以前，故「不满足 2022+ 门槛、须外检索」仍然成立。

### ⚠️ 类目 ⑥ 只有三处「附属」出现，⛔ 不能计为代表作

`constabl`（fuzz-testing workflow 是可执行语义论文的子模块）· `a-model-based-test-script-generation-framework`（mutation analysis 作测试脚本质量的评估手段）· `baselines/designing-fsm-specifications-from-requirements-gpt4`（mutation machine repair）。⛔ 三者主贡献都不在这一类。

⚠️⚠️ **一处 population 不一致，已更正**：⛔ 初版 §2 说类目⑤「起点池根本没有 = 0」（口径 = 669 行主表），⚠️ 却在 §5.3 把 `baselines/designing-fsm-...-gpt4` 算作**同时落 ②⑤⑥** —— ⛔ 两处口径打架（后者把 `baselines/` 也算进起点池）。⭐ **且按 §5-A 判据第一问，该篇修的是它自己生成的 DFSM，属生成后自评，⑤ 这一格本就不该给它。** ⛔ **连带后果**：§5.3 那条「D 档判据已出现至少 1 例」的观察**唯一例证消失**，⭐ 该观察已相应下调（见 §5.3）。

⚠️ 另注：`constabl` 的形式主义是 `concurrent statecharts / arbitrary interleaving`，⛔ 按 §0.1.1「正交区并发语义」**本应界外**，⚠️ 却被当作界内池条目参与了类目④的计数。

---

## 3. Q2 · ⭐ 检查侧 $k$ 的计数，与「对象越界」这个关键事实

⭐ 按 `CONTINGENCY_L1.md` §2 前置纪律 ① 的**第一层两问**判：① 输入里有没有一份**别人给的**模型？② 输出锚不锚在**需求条目**上？

⛔ **`state_machine_types/` 侧 = 0 篇。** 在 669 行的标题+角色+核心功能+关键特性上扫 `自然语言|natural language|traceab|追溯`，只有 3 命中，逐条看过全部不相关（`ltlmop` 是 structured English → LTL 综合属生成侧 · `atac` 是时间自动机构造属界外 · `dsd` 的 "traceable stack" 指运行时决策历史）。

⭐ 检查侧候选全部来自 `baselines/`，⛔⛔ **$k = 2$（2026-08-12 更正，初版报 3）**：

| slug | 年份 | 侧别 | 形式主义 | 关键事实 |
| :-- | :-- | :-- | :-- | :-- |
| `inference-time-intervention-requirement-verification` | 2025 | ⭐ **检查侧**（两问皆是） | ⚠️ **邻域**（Capella/SysML 架构模型图，⛔ 非 $M$） | 输入 = 需求文本 + **已存在**的模型表示，输出 = 逐需求 `fulfilled / not fulfilled` |
| `mcet` | 2025 | ⭐ **检查侧**（两问皆是） | ⚠️ **邻域**（sequence diagram，⛔ 非 $M$） | requirement atoms 逐条比对 + 多检查器 + self-consistency + issue aggregation。⚠️ 自陈「没有处理状态机特有语义」 |
| ~~`ai-driven-consistency-sysml-diagrams`~~ | 2024 | ⛔⛔ **误判，已剔除（2026-08-12）** | ⚠️ 邻域（SysML UCD/BD） | ⛔ **两问全败。** ⚠️ 初版的「需求侧是形式化规则不是 NL 条款」这句措辞把**问②失败**粉饰成了「问②的一种变体」—— ⭐ 实际是**根本没有需求侧**：全文 `requirement` 只出现 3 次，且全在 related work / future work / 参考文献（L157 · L1256「extending our framework for additional diagram types such as **requirement** [diagrams]」· L1293），任务是 **UCD↔BD 两图互检**。⛔ **问①同样失败**：L75「ensure the internal consistency of **LLM-generated** diagrams」· L531-535「stages U1-5 and B1-5 … focusing on **generating** … following this, stages C1-3 are dedicated to **verifying**」· L1106「We evaluated the outlined processes of **diagram generation**, inconsistency identification, and inconsistency resolution」—— ⭐⭐ **三案例评测检的每一张图都是它自己用 TTool-AI 生成的**，这就是「生成后自评」 |

⚠️⚠️ **三篇没有一篇的对象是 $M$。** ⛔ 层 1 **无权**判定它们计不计入界内 $k$ —— 这取决于层 2 读正文后能否找到讲界内对象的段落。⭐ 因此层 3 会面对两种可能：**界内 $k=0$**（→ 由两段式是否存在决定 B/C 档）或 **界内 $k \in \{1, 2\}$**（→ B 档专设子情况）。

⛔⛔ **初版还写了「A 档」这条分支，那是错的**：⚠️ §2 判据是 `k ≥ 3 → A 档`，⭐ 而正确计数是 **$k = 2$** —— **A 档分支在正确计数下根本不可达**。⛔ 若不更正，层 3 会为一个不存在的分支做预案。

⚠️⚠️ **加重情节，且这一条比算错更严重**：⛔ 同一条「生成后自评不算评审侧」的判据（§5-A 判据第一问），初版用它**踢掉了** `chatgpt-uml-assessment`，却对 `ai-driven` **网开一面** —— ⭐ 而后者「自评」的程度更彻底（连检查者都是 LLM 自己）。⛔⛔ **判定标准的选择性执行本身就是学术可靠性问题**，⛔ 不是分类口味问题。

### ⭐ 离「界内检查侧」最近的一篇，⛔ 但第二层判据不成立

`completion-of-sysml-state-machines-from-gwt-requirements`（2024）—— ⭐ **界内**（SysML 状态机），输入 = **部分**状态机 + GWT 需求，且**保持需求到模型元素的可追溯性**。⛔ 但输出是**补全后的模型**，不是满足性判定。⭐ 外检索应沿这条线找「输出是判定而非模型」的变体。

### ⭐ 两段式路线确凿存在且近年密集，⛔ 但逐个越界或半越界

| slug | 年份 | 链路 | 边界门 |
| :-- | :-- | :-- | :-- |
| `pat-agent-autoformalization-model-checking` | 2025 | NL → CSP# + assertions → PAT → 反例引导修复 | ⛔ **界外**（进程代数 CSP#） |
| `event-b-agent` | 2026 | NL → Event-B + 不变式 → ProB + 定理证明 | ⚠️ 部分 / 邻域（⭐ 带 refinement chain，是两段式里最完整的一例） |
| `llm-aided-security-protocol-verification` | 2025 | NL → SAPIC+ → Tamarin | ⛔ 界外（符号协议） |
| `cir-cvn-llm-petri-net-verification` | 2026 | NL → Petri 网 → 验证 | ⛔ **界外** |
| `req2ltl` / `formal-requirements-elicitation-with-fret` | 2025 / 2020 | NL → LTL（⛔ 不接模型） | 界内（LTL 是 $M$ 上的性质语言） |

⭐ §2-B 档判据要求「输入含 NL / 中间产物是形式化性质或结构化需求 / 最终判定由模型检查器给出」—— ⭐ 这四篇字面全中，⛔ 但边界门会砍掉 CSP# 与 Petri 网两篇。

---

## 4. Q5 · ⭐ 界内评审侧 = 0，且全部候选对象越界

`state_machine_types/` = **0**。`baselines/` 91 篇中 2022 年起 65 篇。

### 评审侧候选（⛔ 全部对象越界）

| slug | 年份 | 形式主义 | 关键事实 |
| :-- | :-- | :-- | :-- |
| `mcet` | 2025 | ⚠️ 邻域（sequence diagram） | ⭐ 唯一一篇把「自动查错」做成公开工具 + 公开数据集 + 公开 prompt |
| `ai-driven-consistency-sysml-diagrams` | 2024 | ⚠️ 邻域（SysML UCD/BD） | ⭐ 评测分母说得清；MODELS 2024，DOI `10.1145/3640310.3674079`，Zenodo 工件齐 |
| `inference-time-intervention-requirement-verification` | 2025 | ⚠️ 邻域（Capella/SysML 架构图） | precision 导向评测；⛔ 无公开代码 / 数据 |
| `chatgpt-uml-assessment` | 2023 | ⚠️ 邻域（类图 + OCL） | ⛔ **是「生成后自评」** —— 按 §5-A 档判据第一问「输入里的模型是不是别人给的」为**否**，⛔ 不应计入评审侧 |

⭐⭐ **本轮最硬的一条事实**：在起点池里，「LLM + 对象是 $M$（状态机族）+ 任务是在已有模型上找缺陷」的论文 = **0 篇**。⛔ 上面几篇**全部对象越界**（顺序图 / UCD-BD / 架构图）。

⚠️ ⛔ **这个 0 是关于起点池的事实**：`baselines/` 是按「NL→STM 生成 baseline」口径建的，评审侧本就不在其收录范围内。

### ⭐ 生成侧带自动检查回路的（⛔ 不计入评审侧，⭐ 但可作失败类型的外部佐证）

| slug | 年份 | 形式主义 | 它自报的失败类型 / 检查机制 |
| :-- | :-- | :-- | :-- |
| `llms_emp` | 2025 | ⭐ **界内**（SysML STM/ACT/SD） | ⭐ 幻觉四分类：**格式错误 / 语法错误 / 语义错误 / 需求不一致**；Phase-II 用模型检查规则做反馈式迭代修复；107 案例公开数据集 |
| `designing-fsm-specifications-from-requirements-gpt4` | 2026 | ⭐ **界内**（DFSM/Mealy） | ⭐ 常见错误：**missing transition / output fault**；四种修复反馈的成功率对照 |
| `chatgpt-uml-state-diagrams-to-rebeca` | 2025 | ⚠️ 部分（输入=**已有**状态图，输出=Rebeca 界外） | Afra 编译 + model checking 对照 ground truth |
| `sysmbench` / `mermaidseqbench` / `llm-business-process-modeling-benchmark` | 2024–2025 | ⚠️ 邻域 | ⭐ 三份 benchmark，是「生成侧评测口径」的直接取数处 |

⛔ **不得把生成侧的 P/R 当成 Q3 的参照系** —— 分母不同质。

---

## 5. ⭐⭐ 起点池失配：⛔ 伤害不是「篇数不够」，是「类目分布会失真」

### 5.1 逐问覆盖率

| 问 | 起点池内可用 | 覆盖率 | ⛔ 必须外检索的部分 |
| :-- | :-- | :-- | :-- |
| Q1 ① | ≥ 12 | 2.8% | 补 2022+ 的 BMC / SMT 侧 |
| Q1 ② | ≥ 9 | 2.1% | 补 2022+ 的 EFSM conformance |
| Q1 ③ | **3，全「部分」，2022+ = 0** | 0.7% | ⛔ **整片** |
| Q1 ④ | ≥ 10 | 2.3% | 基本够 |
| Q1 ⑤ | **0** | **0%** | ⛔ **整片** |
| Q1 ⑥ | **0** | **0%** | ⛔ **整片** |
| Q2 检查侧 | 3（**全部对象越界**）；界内 **0** | ⛔ 界内 **0%** | ⛔ **整片** |
| Q5 评审侧 2022+ | 3–4（**全部对象越界**）；界内 **0** | ⛔ 界内 **0%** | ⛔ **四路 venue 族全要跑** |

### 5.2 ⛔⛔ 初版的因果论证**不成立**，⭐ 且它错在我漏引了两个词

⚠️⚠️ **初版在这里写了一整套解释**：`DESC_GUIDE.md` §3 拒收「纯方法/纯工具的缺陷发现工作」→ 起点池按「模型本体谱系」建库 → **系统性遗漏**那一类 → 类目分布失真。⛔ **该论证已于 2026-08-12 经独立核验推翻。**

#### ⛔ 病因一：漏引改变了规则含义

⭐ `DESC_GUIDE.md` §3 第 4 条**逐字**是：

> ```
> 4. 主要创新在算法、验证、综合或转换方法，但对形式主义本体、构造方式和基础设施没有新增可用证据的论文。
> ```

⛔⛔ **初版引用时丢掉了「、构造方式和基础设施」与「可用」。** ⚠️ 而丢掉的那两项**正是工具论文的立身之处**。⭐ 同一份 `README.md` §1 更把「**标准/基础设施**：交换格式、Schema、XML/JSON 载体、元模型承载、运行时、**工具链**、互操作设施」列为**第 3 优先收录**。

#### ⛔ 病因二：结论被池子本身证伪

⭐ 实测：论文角色含工具类词 **163** 行 · 论文角色/核心功能含验证/检查 **178** 行 · 两者交集且主类界内 **62** 行。⭐ 本方抽验，以下**全部在池子里**：`the-model-checker-spin` · `nusmv-a-new-symbolic-model-verifier` · `uppaal-40` · `torx-automated-model-based-testing`（另有 `kronos` `hytech` `mrmc` `vesta` `ymer` `tina` `tapaal-20` `fdr3` `aalpy` `sismic` 等）。

⛔⛔ **纯工具的缺陷发现工作在池子里成堆，⛔ 不是被系统性遗漏。**

#### ⭐⭐ 真实的偏斜是另一回事

⭐ 那些工具论文**压倒性地是 2018 年以前、且形式主义界外**（时间自动机 / Petri 网 / 概率）。⭐ 所以起点池对 Q1 的真实缺口是 **「近年 × 界内」这一格**，⛔ 不是「方法/工具类整体缺席」。

⚠️⚠️ **为什么这个更正很重要**：⭐ §5 是本文件唯一的**解释性**章节，层 3 会据它决定外检索的靶子。⛔ 按错误诊断去补「纯方法/纯工具」，会补到一堆池子里**已经有**的东西，而 **2022+ 的真缺口照旧**。

⭐ **仍然成立的部分**：类目 ⑤（LLM 评审）与 ⑥（变形/差分）在池子里为 0 —— ⛔ 但正确的解释是**时间**（2022 年后才兴起的方向，而池子的重心在 2018 年前），⛔ **不是**「它们不产出新形式主义所以被规则拒收」。

### 5.3 ⚠️ 对 Q1-D 档（换轴）的一条观察，⛔ 不构成换轴条件

`CONTINGENCY_L1.md` §1-D 档判据第一条是「同一篇论文同时落进 ≥3 个候选类目」。⛔⛔ **初版称「已出现至少 1 例」（`designing-fsm-...-gpt4` 落 ②⑤⑥），⭐ 该例证已于 2026-08-12 撤回** —— ⚠️ 它落 ⑤ 是靠把「生成后自评」算成评审侧，而 §5-A 判据第一问明确排除（见上节的 population 更正）。⭐ 去掉 ⑤ 后它只落 2 类。

⭐ **现状：无一例落 ≥3 类。** 落 2 类的有两例（`verifying-and-monitoring-uml-models-with-observer-automata` 落 ①④ · `constabl` 落 ④⑥）。⛔ **D 档判据第一条未被满足。**

⚠️ 筛选过程中确实需要反复回答「**这一篇的判据从哪来**」才能归类。⛔ 一例不构成换轴条件，记录在此供层 3 判断。

---

## 6. ⛔ 层 1 答不了的（一律标「层 1 无法判定」）

1. ⛔ **一切数值判断。** 实测 `grep -l '^##.*\(实验\|评测\|评估\|Evaluation\)' state_machine_types/*/desc.md` = **0** —— `DESC_GUIDE.md` 的 9 个必答问题里**没有一条**问「它测了什么、得了什么数」。
   - ⛔⛔ **初版此处的免责声明与本文件内容不对应，已更正。** ⚠️ 它写「本文件引用的 69/6/92%/87%、85%/77%、100%/0%/40% 等数字全部出自我方转述」—— ⛔ **那些数字在本文件里一个都没出现**（grep 全文零命中）；⚠️ 而它**漏标了本文件真正转述的那个数**：`llms_emp` 的 **107** 案例。
   - ⭐ **好消息**：独立核验已把那四组数**全部回 `paper_content.txt` 核过，全部与原文一致** —— `ai-driven` 的 Table 4 `Total 36 33 6 69 30 30.5 60.5/69` 与 L1119「92% of detected inconsistencies were relevant … automatic resolution of 87%」· `rebeca` 的 L771-779「39 correct lines out of 48, achieving an 85% success rate … Ticket Service shows 77%」· `designing-fsm` 的 Table 2/3/4（100%/100% · 100%/0% · 40%）。⭐ **层 2 对这四组的复核义务可就地销账。**
   - ⚠️ **但 `ai-driven` 论文自身有内部不一致**：L1119 写 false positive 率 8%（→92%），L1194 又写 **7%**（→93%）。⛔ 引用时必须指明取哪一处。
2. ⛔ **「形式主义」判定全是表格级的。** 凡标「部分」的，具体哪一节界内、哪一节界外，⛔ 层 1 给不出章节号。
3. ⛔ **Q2 三篇检查侧工作的第二层五列表**（义务提取人工 / 自动、判据锚定粒度、可否重放、覆盖缺口怎么处理）—— ⛔ 层 1 全部答不了。⚠️ 且按 §2 前置纪律 ①，这四列**只进对照表、不进计数**。

---

## 7. ⛔ 交给层 1′ / 层 2 的检索缺口清单（按优先级）

1. ⛔ **Q1 ⑤（LLM 评审）与 ⑥（变形 / 差分）** —— 起点池 0%，两个类目整片外检索。⚠️ 按 §0.1.5 第 1、2 条必须留可复现检索痕，⛔ 不因最终落在哪一档而豁免。
2. ⛔ **Q1 ③（OCL / well-formedness）** —— 3 篇且 2022+ = 0，按 §0.1.6 第 1 条**不计为满 3 篇**。
3. ⛔ **Q2 界内检查侧** —— 界内 0 篇。⭐ 沿 `completion-of-sysml-state-machines-from-gwt-requirements` 这条线找「输出是判定而非模型」的变体。
4. ⛔ **Q5 四路 venue 族全部** —— 界内 0 篇。
5. ⚠️ **`baselines/mcet/` 的评级重估** —— 现有评级是按**旧的 NL→STM 生成口径**打的，⛔ 在 issue-discover 口径下必须重估。⭐ 本轮层 1 只做了定位（它是检查侧、对象是 sequence diagram），⛔ 重估须待层 2 取全文。

---

## 8. 复现口径

⭐ 本文件所有数字的 population 与命令：

```bash
cd project_1_llm_state_machine_modeling

# 三套文件名的真实计数（⭐ 并证明没有目录缺派生文件）
ls -d state_machine_types/*/ | wc -l          # 679
ls state_machine_types/*/desc.md | wc -l      # 669
ls state_machine_types/*/survey.md | wc -l    # 10
comm -12 <(ls state_machine_types/*/desc.md   | xargs -n1 dirname | sort) \
         <(ls state_machine_types/*/survey.md | xargs -n1 dirname | sort) | wc -l   # 0
for d in state_machine_types/*/; do [ -f "$d/desc.md" ] || [ -f "$d/survey.md" ] || echo "$d"; done  # 空

# 起点池是否存在任何 LLM 论文（⭐ 全 17 列扫描，⛔ 非只扫 desc.md）
# 对 669 行主表全字段扫 \bLLM\b|large language|GPT|大语言模型|ChatGPT|Codex|prompt  →  0
```

⚠️ **口径提醒**：⛔ 不要引用「692 行里 212 行（31%）」这个数 —— 它无法复现，且这个百分比同时取决于「哪些行算表格行 / 用哪个关键词集 / 扫整行还是只扫那一列」，⭐ 实测在不同口径下有五个值（801 行上 306 · 801 行上 260 · 738 行上 261 · 669 行主表形式主义列上 157 · 双判据 242）。⭐ 请改用本文件 §1 的**双判据 265 / 669 = 39.6%，界内池 404**，⭐ 并直接跑 [boundary_gate.py](./boundary_gate.py) 复现。⚠️ ⛔ **本句初版写的是「242 / 669 = 36.2%，界内池 427」—— 那正是 §1 已经作废的那组数**：⭐ 同一份文件在末尾指示读者使用它在开头刚刚撤回的数字。⚠️ 这类「改了正文忘了改指路句」的残留由 C2 反驳发现。
