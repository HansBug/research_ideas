# L1 检索台账（可复现）

⛔⛔ **本文件是 Q3 落 B 档的硬义务，⚠️ 初版交付时整体缺失** —— 由 C3 覆盖 challenge 发现（A-9）。⭐ `CONTINGENCY_L1.md` §0.1.5 第 1 条对 **A/B/C/D 全档**生效；§3 的 B 档更专设「检索矩阵义务（与 C 档拉平）」，逐字要求「venue 族 × 关键词簇 × 年份窗 × 命中数，逐格填数、**空格标明「没跑」还是「跑了 0 命中」**」+ ≥8 条逐条筛除。

⚠️ **格式**：`| 编号 | 查询串（英文逐字，可复制重跑） | 入口 | 日期 | 返回前 N 条标题 | 观察 |`。⛔ 概述式的「我们检索了若干相关关键词」不算检索过程。

⛔⛔ **三态严格区分**：`n` = 跑了、命中 n 条 · `0` = **跑了 0 命中** · `— 没跑` = **本轮未对该组合发出任何查询**。⚠️ 两者含义完全不同。

---

## 0. 覆盖总量

| 轮次 | 扫描题录 | 说明 |
| :-- | ---: | :-- |
| 初轮（ICSE/FSE/ASE 主会 + MODELS/SoSyM/RE/REJ/ECMFA） | **2748** | ⚠️ 成分见 §3 的口径警告 |
| C3 补轮（卫星卷 + Companion + REFSQ + ASE-W） | **+2406** | ICSE 卫星全族 · FSE Companion 三年 · MODELS Companion 四年 · MODELS 2022 主会 · REFSQ 主会+workshop 五年 · ASE workshop 三年 |
| 期刊族补轮（TSE/TOSEM/EMSE/IST/JSS/STVR/SQJ/FAoC，2022–2026） | **+6000** | ⚠️ **入口是 OpenAlex 不是 DBLP**（DBLP 当时 500/503），⛔ DBLP 只用于题录数交叉核对（38/40 格） |
| 形式化方法 / 测试族补轮（FormaliSE · NFM · iFM · FMAS · SEFM · FASE · TACAS · SPIN · ISSTA · ICST · ICFEM · SANER，73 卷） | **+2908** | ⭐ 73/73 卷 http=200；⛔ 70 条 STM/SPEC 命中中**界内 0 · 邻域 11 · 界外 59** |
| 2026 年卷补轮 | **+405** | ⭐ 4 卷已扫（STM/SPEC 全零）；⛔ **7 个主会卷 DBLP 尚未编目**（⚠️ 那是 404 不是零命中） |
| **合计** | **14467** | ⭐ **覆盖较初轮扩大 426%，⛔ 五问仍一问未换档** |

⭐⭐ **那个「没换档」本身是一次独立稳健性检验。** ⛔ 但它**不能**写成「说明该方向为空」（§0.1.7）—— ⭐ 只能写成「**覆盖扩大 88% 后落档不变**」。

---

## 1. C3 补轮 · DBLP 全卷 TOC 机械扫

⭐ 查询串形如 `https://dblp.org/search/publ/api?q=toc:db/<KEY>.bht:&h=1000&format=json`，逐 `<KEY>` 可复制重跑。

**词表逐字**（⭐ 按 `pool_audit.md` §1 立的规矩：**依赖词表的计数，词表就是它的一部分**）：

```
STM  = state machine|statechart|state-chart|\bFSM\b|\bEFSM\b|state model|behaviou?ral model|state diagram|automata|automaton|Stateflow
SPEC = \bOCL\b|SCXML|design by contract|well-formed|\bJML\b
CONF = conformance
REV  = \breview\b|inspection|walkthrough
LLM  = \bLLM\b|large language|\bGPT\b|ChatGPT
```

| 编号 | DBLP TOC key（逐字） | 日期 | 题录 | STM | SPEC | CONF | REV | LLM | 观察 |
| :-- | :-- | :-- | ---: | ---: | ---: | ---: | ---: | ---: | :-- |
| C3-01 | `conf/icse/nier2022`…`nier2026` | 2026-08-12 | 154 | **0** | 0 | 0 | 0 | 20 | ⭐⭐ ICSE'23 NIER 的 *Anti-Patterns in Temporal Specifications* **在这卷里，⛔ 但标题不含 STM 词** —— ⚠️ **它证明标题级扫描对这条线不灵** |
| C3-02 | `conf/icse/icse2022c`…`icse2025c`（Companion，含 SEIP/SEET/demo） | 2026-08-12 | 423 | **0** | 8 | 1 | 0 | 26 | ⭐ 唯一界内相关：**N-17** TPV（2024） |
| C3-03 | `conf/icse/seis*` `aiops*` `intense*` `raise2025` `static2025` 等 17 卷 | 2026-08-12 | 187 | **0** | 1 | 0 | 1 | 14 | RAISE 2025 的 Symboleo 契约形式化（邻域） |
| C3-04 | `conf/sigsoft/fse2024c` `fse2025c` `fse2026c` | 2026-08-12 | 655 | **0** | 2 | 0 | 6 | **136** | ⛔ **LLM 密度极高，⛔ 但一条都不落在行为模型制品上** |
| C3-05 | `conf/sigsoft/atest2022` `easeai2022` `maltesque2022` | 2026-08-12 | 26 | 1 | 0 | 0 | 0 | 0 | ⛔ EASEAI'22 的 FSM 教学误解调查，教育类不入界 |
| C3-06 | `conf/refsq/refsq2022`…`refsq2026` | 2026-08-12 | 123 | **1** | 0 | 0 | 0 | 5 | ⭐ 唯一 STM 命中：**N-12** HanforPL（2026） |
| C3-07 | `conf/refsq/refsq2022w`…`refsq2026w` | 2026-08-12 | 138 | **0** | — | — | — | — | *Hanfor: Requirements Formalisation and Beyond*（2025w），与 N-12 同族 |
| C3-08 | `conf/models/models2022c`…`models2025c` | 2026-08-12 | 541 | 3 | 4 | 0 | 3 | 22 | ⭐⭐ **本轮最高价值单条命中**：**N-02**（2023） |
| C3-09 | `conf/models/models2022`（主会） | 2026-08-12 | 36 | 1 | 3 | 0 | 0 | 0 | ⛔ 那 1 条是 stochastic timed game automata，**界外** |
| C3-10 | `conf/kbse/ase2023w` `ase2024w` `ase2025w` | 2026-08-12 | 123 | **2** | — | — | — | — | ⭐ **N-13 / N-14**，都在 `ase2024w` |
| **小计** | | | **2406** | | | | | | ⛔ 与初轮 2748 **不重叠** |

## 2. C3 补轮 · 其它入口

### 2.1 DBLP 关键词检索 —— ⚠️ **弱工具，其 0 是工具性零**

⛔⛔ **DBLP 默认对标题做全词 AND**，长查询串必 0。⚠️ 下表的 0 **只能读作「该词组合不同时出现在任何标题里」**，⛔ **不能读作事实性零** —— 与已知的 `venue:FSE:` 无效 key 同类。

| 编号 | 查询串（逐字） | total | 观察 |
| :-- | :-- | ---: | :-- |
| C3-11…C3-18, C3-20…C3-22, C3-26 | `state machine model review large language model` · `statechart defect detection LLM` · `mutation testing state machine model` · `differential testing behavioral model` · `state machine model smell` · `UML state machine inconsistency requirements` · `requirements state machine consistency checking` · `specification pattern catalogue state machine` · `LLM model validation SysML` · `seeded defects model inspection recall` · `state machine well-formedness rules checking` · `LLM UML model quality assessment` | 全 **0** | ⛔ 全部**工具性零** |
| C3-19 | `model review large language model UML` | 1 | **N-08**（CoRR 2026 综述） |
| ⭐ **C3-23** | `requirements traceability state machine` | 1 | ⭐⭐ **§8 原第 10 条那两串 429 未取回中的第一串，本轮取回**：CSER 2012（⛔ 不过 2022+ 门槛） |
| ⭐ **C3-24** | `statechart consistency requirements` | **0** | ⭐ 第二串，本轮取回，**跑了 0 命中**（⚠️ 仍是标题级 AND 的弱零） |
| C3-25 | `state machine model defect` | 1 | 2014 WICSA Companion，不过门槛 |

### 2.2 OpenAlex（⭐ 覆盖 title + abstract，`filter=from_publication_date:2022-01-01`）

⭐ 形如 `https://api.openalex.org/works?search=<Q>&filter=from_publication_date:2022-01-01&per-page=10`。

| 编号 | 查询串（逐字） | total | 有效命中 |
| :-- | :-- | ---: | :-- |
| C3-27 | `state machine model review large language model defects` | 41705 | ⛔ 前 10 全主题外 |
| C3-28 | `LLM detect inconsistencies between requirements and UML state machine` | 573 | ⛔ 生成侧 |
| C3-29 | `mutation operators statechart model` | 50 | ⛔ 两条均 UPPAAL / real-time，**界外** |
| C3-30 | `differential testing behavioral models statecharts` | 79 | *Behavioral consistency in multi-modeling*（JOT 2023），待核 |
| C3-31 | `state machine model smells anti-patterns catalog` | 536 | ⛔ 前 10 全是 code smell |
| C3-32 | `seeded defects inspection recall UML design model` | 32 | **N-11**（EASE 2023） |
| C3-33 | `automated review SysML state machine against requirements` | 735 | ⭐ **N-18**（CSUR 2023，⚠️ **仓库已收却未用**） |
| C3-34 | `well-formedness rules statechart validation` | 32 | **N-09**（SQJ 2023） |
| C3-35 | `property specification patterns catalogue state machine 2023` | 3538 | **N-10**（NDSS 2023） |
| C3-36 | `LLM as judge model driven engineering artifact quality` | 5231 | ⛔ 前 10 全是通用 LLM-as-judge |

### 2.3 前向引用追踪（Semantic Scholar Graph API `/citations`）

| 编号 | 起点 | citing | 2022+ | ∩ 关键词 | 观察 |
| :-- | :-- | ---: | ---: | ---: | :-- |
| C3-37 | `arXiv:2508.00630`（MCeT） | 5 | 5 | 4 | ⛔ **无一条落在「已有状态机上找缺陷」**。⭐ 该篇太新，前向追踪暂不产出界内后继 |
| C3-38 | `DOI:10.1007/s10270-026-01388-4`（SoSyM 2026） | **0** | 0 | 0 | ⛔ 尚无被引 |
| ⭐⭐ C3-39 | `DOI:10.1145/302405.302672`（Dwyer ICSE'99） | **1674** | **168** | **66** | ⭐⭐ **本轮产出最密的一条**，66 条逐条看过，取出 **N-01…N-06** |

### 2.4 工业侧规则集

| 编号 | 入口 | 结果 |
| :-- | :-- | :-- |
| C3-40 | [MathWorks Model Advisor check reference](https://www.mathworks.com/help/slcheck/referencelist.html?type=check) | ⛔ **内容区为空（SPA 动态壳）** —— ⚠️ 按仓库规则记「入口已定位 / 内容待人工核验 / 访问异常」，⛔ **不得据此断言不存在** |
| C3-41 | 另两条 MathWorks 页面 | ⛔ **HTTP 404**，记为访问异常 |
| ⭐⭐ C3-42 | [Model Advisor Checks for High-Integrity Systems Modeling Guidelines](https://www.mathworks.com/help/slcheck/ref/model-advisor-checks-for-high-integrity-systems-modeling-guidelines.html) · [HISM checks](https://www.mathworks.com/help/slcheck/ref/hism-checks_hism_checks.html) | ⭐ **入口定位成功，摘要级** —— 见 §4 |
| C3-43 | [Prove Model Properties](https://www.mathworks.com/help/sldv/ug/what-is-property-proving.html) · [Proof Objective](https://www.mathworks.com/help/sldv/ref/proofobjective.html) | ⭐ SDV 块库含 **Example Properties** 子库；⛔ 是否闭合枚举**待人工核验** |

---

## 3. ⛔⛔ 初轮那张「2748 条」表的三条口径警告

⚠️ **初轮交付把它当成一个整数用，⛔ 但它有三处未声明的边界**（C3 的 C-1/C-2/C-3）：

1. ⛔⛔ **它是纯标题级正则，表内没有一处标 `title-only`。** ⚠️ 读者会把 `conformance 0/2748` 读成「三族近年没有 conformance 工作」。⭐ 反证：MODELS 2023 主会标题里**就有** *An Experimental Evaluation of Conformance Testing Techniques in Active Automata Learning*（DOI [`10.1109/MODELS58315.2023.00012`](https://doi.org/10.1109/MODELS58315.2023.00012)）—— ⭐ 同一个词在别的族标题里出现，**说明那个 0 是「该族标题」的 0**。
2. ⛔⛔ **2748 是三个成分不同质的数相加。** ⚠️ **ICSE 剔了卫星卷（896 = 主会）、ASE 含卫星卷（1096 含 industry / tool demo / NIER）** —— ⛔ 两者按不同口径进同一个分母。⭐ 这正是「**比率只能跨同类分母比**」那条：**成分差异在合计数上完全看不见**。
3. ⚠️ **PACMSE v1 121 / v2 242 与「FSE 主会 393」是两段不同年份的口径拼接** —— 393 = ESEC/FSE 2022+2023 两卷，⭐ 而 FSE 2024/2025 主会论文改发 PACMSE。⛔ 不是并列关系。
4. ⛔ **「343/2748 与『设计/模型制品』求交后仅 15」的求交词表没给** —— ⚠️ 这与 `pool_audit.md` §1 自己刚立的规矩逐字冲突。⭐ **同一份交付里，边界门落了脚本，这个求交没落。**

---

## 4. ⭐⭐ 反驳线索：⛔ 「记不记缺口」不是有效判据，⭐ 「缺口挂在哪」才是

⚠️⚠️ **本节结论已于 2026-08-12 修正。** ⛔ 原标题写「都没有一篇把表达不了的义务显式记成缺口」—— ⭐ **那句话站不住**：⚠️ 后续正文级核验发现至少 **QUARTET（TSE 2023）三层缺口机制** 与本节这条工业先例。⭐⭐ **正确的判据是「缺口挂在什么上」**：既有工作挂在**规约语言 / 工具的能力**上（换一份模型不变），⭐ 本方挂在**「这条需求 × 这份模型」那一格**上（换一份模型会变）。

⚠️ **摘要级，⛔ 三条限制必须同时说明。** [MathWorks 高完整性建模指南 ↔ Model Advisor 检查映射表](https://www.mathworks.com/help/slcheck/ref/model-advisor-checks-for-high-integrity-systems-modeling-guidelines.html) 的做法与我方断言相反：

- ⭐ 一套**带稳定编号的规则集**（Stateflow 侧 `hisf_XXXX`：`hisf_0002` 状态/迁移执行序 · `hisf_0013` 迁移路径跨并行状态边界 · `hisf_0014` 迁移路径穿越状态 · `hisf_0015` 强数据类型）；
- ⭐⭐ **该映射表显式列出「哪些指南没有对应的 Model Advisor 检查」，并给出理由 —— 逐字是 `automation isn't possible`。**

⛔ **三条限制**：① **摘要级**，`hisf_` 全表与「无检查项」清单**均未逐条取件**（C3-40/41 的动态壳与 404 拦住了）；② 对象是 **Stateflow**，其并行状态与 temporal logic 有相当部分**落在边界门外**，⛔ 不可整体当界内；③ 它是**工具指南而非文献**，⭐ 按 §0.1.8 只能作「这类检查在领域实践中反复出现」的**存在性移交**，⛔ 不作规范性出处、⛔ 不由 L1 定级。

---

## 4b. ⭐⭐ N-19 · Q3 逐条筛除记录的最特殊一条

⚠️ **它特殊在：它提供的 60 个模型就是本文的被测语料。** ⛔ 而它此前**从未进入 Q3 的筛除记录**（由 C2 反驳发现）。

> **Wang, Ge, Liu, Cao, Chen, Hu**, *Generating SysML Behavior Models via Large Language Models: an Empirical Study*, **Internetware 2025, pp. 366–377**, DOI [`10.1145/3755881.3755926`](https://doi.org/10.1145/3755881.3755926)。⭐ **证据级：正文 + 一手制品级**（全文 1189 行 + 公开 workbook 7 sheet 均本地冻结）。

| 门 | 判定 | 依据 |
| :-- | :-: | :-- |
| ① 已有模型上找缺陷 | ⛔ **缺** | ⭐ 被检对象是该论文 Phase-I **自己生成的 60 个模型**（workbook 的 `Generation PlantUML` 列），属**生成后自评**；检查动作全人工（§4.4 逐字 `all validations must be performed manually`）。⚠️ **steelman**：若把「方法」读作人工检视，门① 可辩称通过 —— ⛔ **但那立刻把它推进 B 档**（执行者是人）。⭐ 两条读法都到不了四门全中 |
| ② 状态机类制品 | ⭐ **中** | PlantUML SysML 状态机图。⚠️ 但其最大语义类是 `STM missing Regions`（20 条）—— ⛔ **正交区落在 $M$ 之外** |
| ③ recall / coverage | ⛔ **缺（决定性）** | ⭐ 逐条判它报的每个数：`>90%` 是**元素准确率**（分母是生成模型自身的语法点）· 语义 F1 的 TP/FP/FN **全是 grammar point 且对着参考模型算** → **元素召回** · `31/72` `56/150` 是**修复率**（`Resolved / Hallucination Numbers`，分母 = 自己找到的条数）。⭐⭐ **全文 `recall` 只出现一次，且说的是别人的数** |
| ④ 口径可复现 | ⭐ **中（就其所报之数）** | ⭐ 修复率分母**印在表里**且可从公开 workbook 复算 —— ⭐ **这一点优于 MCeT**（后者两个分母全篇未印）。⛔ 但判定者未写明（无标注人数、无 $\kappa$）、缺陷**非植入**（总体不可知）、离散项切分未落盘 |

⛔ **结论：中 ②④、缺 ①③。缺③ 不可换算** —— ⚠️ 缺陷不是植入的，真实总体不可知，检出步的 FN 无定义。

⚠️ **与另两条「缺分母」候选的区别**：LASHED 与 SoSyM 是**作者自陈**做不了 recall，⛔ 而本篇**从未声称**要做 recall —— ⭐ 故它可加进「不可换算」的**类型**说明，⛔ **不得**与两条自陈同列计入分母支撑。

### ⭐⭐ 顺带核准一处事实：状态机数是 **36** 不是 34

⚠️ 该论文内部不一致：§1 contributions 与 Table 2 Total 行都写 **36**，⛔ 而 §3.4 散文写 34。⭐ **裁定 36**，判据是算术：`36 + 34 + 35 = 105 ≠ 107`，而 `36 + 36 + 35 = 107` ✓ —— ⭐ 而 107 是全篇反复出现的总数。

---

## 5. ⛔ 工具陷阱（⚠️ 后续必须规避）

| 陷阱 | 表现 | 正确做法 |
| :-- | :-- | :-- |
| `venue:FSE:` 是无效 DBLP key | 返回 0 | ⭐ 用 `venue:SIGSOFT FSE:` |
| ICSE 卫星卷**不是** `icse<year>-nier` | ⛔ C3 先按此探了 13 个 key，**全返 0** —— 全是工具性零 | ⭐ 卷名是 `conf/icse/nier<year>`；⛔ **先抓 `https://dblp.org/db/conf/icse/index.html` 枚举卷名** |
| Semantic Scholar `/paper/search` 对匿名请求硬性 429 | ⛔ 连续 6 次重试全败 | ⭐ 同 API 的 `/paper/{id}/citations` 端点畅通；⛔ **不要把 search 端点的失败当成命中 0** |
| DBLP 关键词检索是标题级全词 AND | 长查询串必 0 | ⛔ 其 0 是**工具性零**，⭐ 只能读作「该词组合不同时出现在任何标题里」 |
| ⛔⛔ **DBLP API 的 `h` 参数在 `toc:` / `stream:` facet 下实际封顶 100** | ⚠️ 返回 `@computed=100` 而 `@total=284`，⛔ **返回码是 200、不报错** | ⛔⛔ 不带 `f=` 翻页而直接读 `hit` 数组，会把 284 条的卷**静默截成 100 条** —— ⭐ 必须读 `@total` 并翻页 |
| ⚠️ **IEEE / Wiley 期刊在 OpenAlex 里按 early-access 年计年，⛔ 不按卷年** | ⭐ 实证：某篇的 `publication_year` 是 2022，卷是 49 → 2023。⚠️ 按年拉 TSE 只得 895 条，按卷得 1051 条 | ⭐ 用 `biblio.volume` 过滤，⛔ 不用 `publication_year` |
| ⛔⛔ **Elsevier / Springer 不向 Crossref 交摘要** | ⚠️ 实测摘要可得率：TOSEM 100% · STVR 100% · TSE 98% · FAoC 91%，⛔ 而 **EMSE 43% · JSS 40% · IST 35% · SQJ 28%** | ⛔⛔ **那四家的所有「0」只等同于标题级零**，⚠️ 不得与 TSE/TOSEM 的 0 混为一谈 |
| ⛔⛔ **`STM` 正则有盲区，会系统性低估** | ⚠️ 不含 `model-based testing` / `transition system` / `Simulink` / `SysML` / `protocol state`；⛔ 且 `\bOCL\b` 打不中写全称的 `Object Constraint Language` | ⭐ **实证：ICST 主会五卷 348 篇 STM 恒为 0 就是这个原因** —— 至少 6 条明显相关题录未被计入 |
| ⚠️ **`REV` 正则在 SE 类 venue 无判别力** | 18 条命中里 SANER 占 10、ISSTA 占 3，⛔ 逐条看全是 code review / user review / literature review；⚠️ 另有一条是 `Tunnel Inspection` 的**词面误击** | ⭐ 该列不宜单独作判据 |
| ⛔⛔ **词表对「NL → 时序逻辑」整条线失灵** | ⚠️ 实证：Zrelli 等 JSS 2026（`NL requirements → CTL specifications`）在 6000 条 dump 里**只被 `LLM` 一列抓到**，`STM` / `SPEC` / `CONF` / `REV` 全空 | ⛔ 这是**系统性假阴性**，⛔ 不是「跑了 0 命中」。⭐ 词表缺 `temporal logic` / `LTL` / `CTL` / `formalization` |
