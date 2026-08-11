# 起点池审计（层 1 产出）

⭐ 本文件是 L1 层 1 的**起点池预筛结果与失配报告**。⛔ 它不下任何档位结论 —— 落档要等层 1′ 的外检索补完、且需正文佐证（`CONTINGENCY_L1.md` §0.1.5 第 3 条）。

⛔ **本文件的一切判断都是「表格级」的**，即只读 `SUMMARY.md` 的逐篇表，⛔ 未读任何一篇正文。按 `CONTINGENCY_L1.md` §0.1.5 第 3 条，「正文读了没」一律计为**未读**。

---

## 1. 边界门：⛔ 「形式主义」列不是充分判据

⭐ 判据用**双条件**，对 **669 行主表**逐行判，任一为真即剔除：① 「形式主义」列命中界外关键词；② 「主类」列 emoji ∈ {⏱️ 时间/时钟自动机, 🌊 混成/随机, 🕸️ Petri 网}。

| 判据 | 剔除行数 |
| :-- | ---: |
| 仅「形式主义」列命中 | 76 |
| 仅「主类」emoji 命中 | 18 |
| 两者同时命中 | 148 |
| **合计剔除** | **242 / 669（36.2%）** |
| **界内候选池** | **427** |
| ⚠️ 其中 2022 年起 | **34** |

剔除集的「主类」分布：⏱️ 94 · 📦 68 · 🌊 45 · 🕸️ 27 · 🔣 5 · 🔌 3。剔掉的主要是：时间自动机及其工具生态（UPPAAL 系、TIOA、参数化/代价/博弈 TA 变体）· 概率与统计模型检查器（PRISM、MRMC、VESTA、Ymer）· Petri 网全族（P/T、CPN、GSPN、PNML/ISO 15909）· 进程代数与 BIP 系（mCRL2、BIP/D-Finder）· 混成自动机与 CPS 连续动力学。

### ⛔⛔ 单靠那一列会漏 40 行

⚠️ 实测 **40 行**「形式主义」列干净、却在**标题 / 论文角色 / 关键特性**里含界外词。逐条看过，分三类：

| 类 | 例 | 后果 |
| :-- | :-- | :-- |
| ⛔ **真界外、被门漏掉** | `turtle-a-real-time-uml-profile`（RT-LOTOS + RTL）· `translating-uml-state-machines-to-coloured-petri-nets`（目标是 CPN）· `a-runtime-environment-for-contract-automata`（用 UPPAAL 做 validation）· `modelling-and-verification-of-timed-robotic-controllers` · `towards-verifying-safety-properties-of-real-time-probabilistic`（PTA/PRISM） | ⛔ 若只按列过滤，这些会**混进界内池** |
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

界内那 3 篇全为「部分」：`automating-verification-of-state-machines-with-reactive-designs-and-isabelle-utp`（RoboChart 的 well-formedness 机械化，⚠️ CSP 语义分支界外）· `robochart-modelling-and-verification-of-robotic-applications`（metamodel + well-formedness，⚠️ timed primitives 界外）· `modelling-system-of-systems-interface-contract-behaviour`（SysML/OCL 契约视图，⚠️ 是本池**唯一**沾 OCL 的界内条目）。

### ⚠️ 类目 ⑥ 只有三处「附属」出现，⛔ 不能计为代表作

`constabl`（fuzz-testing workflow 是可执行语义论文的子模块）· `a-model-based-test-script-generation-framework`（mutation analysis 作测试脚本质量的评估手段）· `baselines/designing-fsm-specifications-from-requirements-gpt4`（mutation machine repair）。⛔ 三者主贡献都不在这一类。

---

## 3. Q2 · ⭐ 检查侧 $k$ 的计数，与「对象越界」这个关键事实

⭐ 按 `CONTINGENCY_L1.md` §2 前置纪律 ① 的**第一层两问**判：① 输入里有没有一份**别人给的**模型？② 输出锚不锚在**需求条目**上？

⛔ **`state_machine_types/` 侧 = 0 篇。** 在 669 行的标题+角色+核心功能+关键特性上扫 `自然语言|natural language|traceab|追溯`，只有 3 命中，逐条看过全部不相关（`ltlmop` 是 structured English → LTL 综合属生成侧 · `atac` 是时间自动机构造属界外 · `dsd` 的 "traceable stack" 指运行时决策历史）。

⭐ 检查侧候选全部来自 `baselines/`，**$k = 3$**：

| slug | 年份 | 侧别 | 形式主义 | 关键事实 |
| :-- | :-- | :-- | :-- | :-- |
| `inference-time-intervention-requirement-verification` | 2025 | ⭐ **检查侧**（两问皆是） | ⚠️ **邻域**（Capella/SysML 架构模型图，⛔ 非 $M$） | 输入 = 需求文本 + **已存在**的模型表示，输出 = 逐需求 `fulfilled / not fulfilled` |
| `mcet` | 2025 | ⭐ **检查侧**（两问皆是） | ⚠️ **邻域**（sequence diagram，⛔ 非 $M$） | requirement atoms 逐条比对 + 多检查器 + self-consistency + issue aggregation。⚠️ 自陈「没有处理状态机特有语义」 |
| `ai-driven-consistency-sysml-diagrams` | 2024 | ⭐ **检查侧**（⚠️ 但需求侧是**形式化规则**不是 NL 条款） | ⚠️ **邻域**（SysML UCD/BD） | 输出 = **JSON 不一致列表** + 自动修复 |

⚠️⚠️ **三篇没有一篇的对象是 $M$。** ⛔ 层 1 **无权**判定它们计不计入界内 $k$ —— 这取决于层 2 读正文后能否找到讲界内对象的段落。⭐ 因此层 3 会面对两种可能：**界内 $k=0$**（→ 由两段式是否存在决定 B/C 档）或 **界内 $k=1\ldots3$**（→ B 档专设子情况 / A 档）。

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

### 5.2 ⛔ 失配的结构性原因（已实测确认）

`state_machine_types/DESC_GUIDE.md` §3 明写「主要创新在算法、验证、综合或转换方法，但对形式主义本体没有新增证据的论文」**默认不建 `desc.md`** —— ⚠️ **而那正是 Q1 的整个 ①②③④ 四类**。

⭐ 后果：起点池按「**模型本体谱系**」建库。所以「一篇给出新语义的验证工作」进得来，而「一篇纯粹用 SPIN 检查某类状态机的方法论文」**按规则本该被拒**。⚠️ 池子里那 12 篇 ① 类，多半是因为**顺带提出了新形式主义或新语义**才进来的。

⛔⛔ **因此这条失配对 Q1 的伤害不是「篇数不够」，而是「按现有池子归纳出来的类目分布会失真」**：⚠️ 它**偏向**「带本体贡献的验证工作」，**系统性遗漏**「纯方法 / 纯工具的缺陷发现工作」。⭐ 层 3 若直接按起点池篇数给各类目排大小，会得出「模型检查最大、LLM 评审不存在」的结论 —— ⛔ **那反映的是建库口径，不是领域。**

⭐ 同一原因解释了 ⑤ 与 ⑥ 的整片为 0：LLM 评审、mutation / 差分测试**从不产出新形式主义**。

### 5.3 ⚠️ 对 Q1-D 档（换轴）的一条观察，⛔ 不构成换轴条件

`CONTINGENCY_L1.md` §1-D 档判据第一条是「同一篇论文同时落进 ≥3 个候选类目」。⭐ 本轮筛选中**已出现至少 1 例**：`designing-fsm-specifications-from-requirements-gpt4` 同时落 ②⑤⑥。另有两例落 2 类（`verifying-and-monitoring-uml-models-with-observer-automata` 落 ①④ · `constabl` 落 ④⑥）。

⚠️ 筛选过程中确实需要反复回答「**这一篇的判据从哪来**」才能归类。⛔ 一例不构成换轴条件，记录在此供层 3 判断。

---

## 6. ⛔ 层 1 答不了的（一律标「层 1 无法判定」）

1. ⛔ **一切数值判断。** 实测 `grep -l '^##.*\(实验\|评测\|评估\|Evaluation\)' state_machine_types/*/desc.md` = **0** —— `DESC_GUIDE.md` 的 9 个必答问题里**没有一条**问「它测了什么、得了什么数」。
   - ⚠️ **例外与陷阱**：`baselines/*/DESC.md` 有「实验结果总结」段。⛔ 但本文件引用的 69/6/92%/87%、85%/77%、100%/0%/40% 等数字**全部出自我方 DESC.md 的转述**，⛔ **不是原文核验过的** —— 层 2 必须回 `paper_content.txt` 逐条复核。
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

⚠️ **口径提醒**：⛔ 不要引用「692 行里 212 行（31%）」这个数 —— 它无法复现，且这个百分比同时取决于「哪些行算表格行 / 用哪个关键词集 / 扫整行还是只扫那一列」，⭐ 实测在不同口径下有五个值（801 行上 306 · 801 行上 260 · 738 行上 261 · 669 行主表形式主义列上 157 · 双判据 242）。⭐ 请改用本文件 §1 的**双判据 242 / 669 = 36.2%，界内池 427**。
