# 卡片 · AutoSpec（NL RFC → I/O grammar，两阶段 + 执行制导修复）

⭐ **全文可得**：arXiv HTML 全文（8 节）已完整读过。⭐ 另外 —— ⭐ **本卡的部分关键字段不是从论文读来的，⭐ 而是从作者放在 Google Drive 的实现里读来的**（⭐ `models.py` 的 Pydantic `Literal` 枚举、⭐ `prompts_s1.py`），⛔ 因为论文里的 prompt 是**带省略号的截图**。⭐ 这类断言我标 **M(code)**。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `synthesizing-protocol-specs` |
| `title` | Synthesizing Precise Protocol Specs from Natural Language for Effective Test Generation |
| 系统名 | ⭐ **AutoSpec**（⭐ 论文自解为 "**A**uthor **U**tterances **to** **Spec**ifications"） |
| `year` | 2025（arXiv v1，⭐ 2025-11-22 提交；⛔ **未发表**） |
| `venue` | ⛔ **无** —— ⭐ arXiv 预印本，⛔ HTML 无 comments、无 journal-ref、无会议信息 |
| `ccf` | ⛔ **未收录**（⭐ 无 venue 可查） |
| `arxiv` | [arXiv:2511.17977](https://arxiv.org/abs/2511.17977)（⭐ 我实际访问过 abs 页与 `https://arxiv.org/html/2511.17977v1`） |
| `doi` | [10.48550/arXiv.2511.17977](https://doi.org/10.48550/arXiv.2511.17977)（arXiv 自发 DOI） |
| 作者 / 单位 | ⭐ Kuangxiangzi Liu · Dhiman Chakraborty（**Volkswagen AG**, Wolfsburg）· ⭐ Alexander Liggesmeyer · **Andreas Zeller**（**CISPA**, Saarbrücken） |
| `artifact_type` | ⭐⭐ **I/O grammar**（⭐ Liggesmeyer/Amaya/Zeller [arXiv:2509.20308](https://arxiv.org/abs/2509.20308) 的形式化：⭐ 带 `Client:` / `Server:` party 前缀的会话级语法 + `where` 语义约束）。⭐ 中间制品是**协议状态机 multigraph** $G = \langle S, C, E, \Phi \rangle$ |
| `task` | ⭐ **生成**（NL RFC → 形式规约）+ ⭐ **修复**（执行制导迭代精化）+ ⭐ 下游 **测试生成** |
| `boundary` | ⭐ **邻域** —— ⭐ 协议状态机（⭐ [README.md](../README.md) §2.1 明列为邻域）。⚠️ ⭐ 注意 `models.py` 里有一个 `Timer(name, duration_seconds, scope)` 模型，⭐ 即抽取阶段**会抽定时器**，⛔ 但论文正文与评测**从不提 timer**，⛔ 也没有任何时间语义的度量 —— ⭐ 所以实际评测的是无时间的协议 FSM |

---

## B. LLM 应用形态

### B1 · 流水线阶段

⭐ 论文自称「**two-stage**」（Abstract），⭐ Fig 2 画了 6 个编号框，⭐ Fig 3 画了 3 个。⭐ 按实现里真正各自成阶段的环节数：

```
【Stage A · RFC 预处理（§3）】
[确定性] crawler 清洗 RFC HTML（去 boilerplate / TOC / footer，⭐ 保留 section ID + 段落索引）→ 每节一个 JSON
  → [LLM] 节分类 / 过滤（label ∈ 4 类，action ∈ 3 类；⭐ 只有 extract 的节继续往下）
  → [LLM] 结构化抽取（→ Pydantic `SectionPayload`）
  → [确定性] Pydantic 运行时校验（⛔ 失败则丢弃并重发一次）
  → [LLM] 节内 multigraph 合成（名字归一 / 去重 / 补边）
  → [确定性] acceptance filter（⭐ 强制节点边类型 + ⭐ 强制 provenance 锚 + ⭐ 冲突按「normative > examples/overviews」定序）
  → [确定性] 规则合并器（全局 union，⛔ 完全无 LLM）→ G = ⟨S, C, E, Φ⟩
  → [确定性] 最短路算法 → Minimal Transition Paths（MTPs）

【Stage B · 合成与修复（§4–5）】
  → [确定性] BM25 检索（按 MTP 当检索键取 RFC 子句）
  → [LLM] Grammar Generator Agent（MTP + 检索文本 → I/O grammar）
  → [确定性] Pydantic schema 检查 + ⭐ MTP generatability 检查
  → [确定性] Fandango grammar fuzzer 生成会话 → 打**真实 SUT**（容器里的 Dovecot / Postfix / vsFTPd / Pigeonhole）
  → [确定性] 缺陷分类决策树：Parsing Succeeds? → Constraints Satisfied? → Message-Form Coverage?
  → [LLM] Grammar Repair Agent（选 error_class ∈ 3 类，产出最小 patch）
  ⇄ 回到 Generator（⭐ 至多 7 轮）
```

⭐⭐ **13 个阶段 · 5 个 LLM 阶段 · 8 个确定性阶段。** ⭐ LLM 占比 **5/13 ≈ 38%**，⛔ 且**没有任何一个 LLM 阶段负责判定「过不过」**。

### B2 · 每次 LLM 调用的角色

| 阶段 | 角色 | 证据 |
| :-- | :-- | :-- |
| 节分类 | ⭐ **分类器**（⭐ 4×3 闭合标签） | **M** · §3.1.1「assigns a semantic label (state machine, overview, example, other) plus an action (extract, copy, summarize)」 |
| 结构化抽取 | ⭐ **抽取器**（NL → JSON） | **M** · §3.1.2「the model lifts states, commands, transitions, and syntax/constraint rules into normalized JSON」 |
| multigraph 合成 | ⭐ **规划者 / 抽取器**（⭐ 名字归一、节内合并、⭐ 补跨句蕴含的边） | **M** · §3.1.3「(i) name harmonization... (ii) intra-section consolidation... (iii) edge completion (recovering implied transitions or dependencies mentioned across sentences)」 |
| Grammar Generator | ⭐ **翻译器**（MTP + RFC 文本 → I/O grammar） | **M** · §4「turns the preprocessed RFC specifications from Section 3 into an executable I/O grammar」 |
| Grammar Repair | ⭐ **分类器 + 修复者**（⭐ 判 error_class，⭐ 产最小 patch） | **M** · §5.1.1「maps it to an error class (or None). It records the `error_class` and a short `reason`」 |

⛔ **没有评审者、没有裁决者。** ⭐ 这是本卡与我们 v46 最尖锐的形态差别 —— ⭐ 见 B4。

### B3 · prompt 策略

`结构化输出约束`（⭐⭐ 全链条 Pydantic schema-constrained JSON，⭐ 失败即拒并 bounded retry）· `角色扮演`（⭐「act as a domain-specific RFC expert」/「You are a TLA+... 」式设定）· ⭐ **多智能体分工**（⛔ 不是辩论：⭐ classifier / extractor / synthesizer / generator / fixer 各跑各的，⭐ 且**每个 agent 各自 sandbox 以免串味**）· `RAG`（⭐ BM25 检索 RFC 子句）· ⭐ **guardrails**（见下）· ⛔ **无 few-shot**（⭐ RQ4 里 few-shot 是被消融的对照组，⛔ 不是主流水线）· ⛔ **无 CoT、无 self-consistency 投票**。

⭐ **guardrails 逐字**（**M** · §4.2）：「Guardrails enforce **literal symbol names, section-local scope, normative-over-example precedence, provenance quoting, and schema checks**. Each output is validated by a Pydantic schema; invalid outputs are rejected and the prompt is re-issued once.」

⚠️ ⭐ **`section-local scope` 这条值得单独标出**：**M(code)** · `prompts_s1.py` L129「If zero items meet the above, the corresponding list MUST be [].」+ Fig 4「**Scope.** Extract from **this section only**」 —— ⭐ 即**明确允许模型交白卷**，⛔ 不逼它编。⭐ 这与我们的契约门「必须产出断言」的取向相反，⭐ 值得 M1 考虑。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 | 证据 |
| :-- | :-- | :-- |
| 有无循环 | ⭐⭐ **有，两层** | — |
| ⭐⭐ **裁决者是谁** | ⭐⭐ **① 测试执行 + ② 确定性规则。⛔ 零个 LLM 自评。** | 见下表 |
| 终止条件 | ⭐ **收敛 或 预算耗尽**（二者取先） | **M** · §5.2 逐字「The loop stops when **schema checks pass and all MTPs can be generated**, or when a **repair budget is exhausted**.」 |
| 最大轮数 | ⭐⭐ **7** | **M** · §7.2「we generate tests with at most **7 iterations** per MTP per protocol」；§7.4「a survival curve showing the fraction of grammars not yet fixed versus repair round (**0–7**)... grammars unfixed after round 7 are treated as **censored**」 |
| ⭐ 逐轮边际收益 | ⭐ **有报告，⛔ 但只有定性描述 + 两张图，⛔ 无逐轮数字表** | 见下 |

⭐ **两层循环的裁决者分工**：

| 层 | 裁决者 | 类型 | 判什么 |
| :-- | :-- | :-- | :-- |
| ⭐ 内层（每次 LLM 调用） | Pydantic schema | ⭐ **确定性规则** | 结构合法否；⛔ **失败只重发一次**（§3.1.2「we discard the instance and re-issue the prompt once; this resolves most cases」） |
| ⭐⭐ 外层（主修复环） | ⭐ **Fandango fuzzer + 真实 SUT 的响应** + ⭐ MTP generatability 检查 + ⭐ 三道确定性缺陷判据 | ⭐⭐ **测试执行 + 确定性规则** | grammar 能不能生成、⭐ 生成的会话打真实实现被不被接受（⭐ POP3 `+OK` / SMTP `2xx`） |

⭐⭐ **三道确定性缺陷判据（Fig 2 的决策树，⭐ 逐条抄）**，⭐ 顺序执行、⭐ 每道 No 各走一个 patch 类：

| 门 | 判据 | 归入的缺陷 | 对应 patch 类 |
| :-: | :-- | :-- | :-- |
| 1 | `Parsing Succeeds?` | Syntax Defect | ⭐ Syntax Fix |
| 2 | `Constraints Satisfied?` | Constraint-Mismatch | ⭐ Constraint Fix |
| 3 | `Message-Form Coverage?` | Coverage-Gap | ⭐ Form Addition |

⭐ 三门全过 → 输出最终 I/O grammar。⭐ **LLM 只在门已经拒了之后，被叫来判「这属于 3 类里的哪一类」并写 patch** —— ⛔ **它不决定要不要再来一轮**。

⭐⭐ **逐轮边际收益 —— 逐字抄下来（⛔ 这是 parent 点名要对照「第 3–5 轮零收益」那条的地方）**：

> **M** · §7.4「Interpretation. **The loop is most effective early, converting many Grammar Syntax Error to successes by round 2–3. What remains are semantic/behavioral mismatches that are harder to resolve automatically.** This suggests prioritizing syntax-aware repairs in early rounds and introducing trace-semantics aids (e.g., exemplar alignment, stricter oracle checks, or targeted prompts) for later rounds.」

> **M** · §7.4「Most errors are Grammar Syntax Error and fixable quickly; **the hard tail is T-Trace Mis-match.** The figure quantifies both the *when* (early vs late) and the *what* (error class) of repair effectiveness, **explaining the survival curve's early drop and late flattening.**」

⛔⛔ **但注意：逐轮的具体数字只在 Fig 8（survival curve）与 Fig 9（每轮堆叠柱）里，⛔ 论文没有对应的数字表。** ⭐ 我核过 arXiv HTML：这两张图是 LaTeX/tikz 渲染，⛔ HTML 里只剩坐标轴刻度（`$0$ $1$ … $7$`、`$0$ $50$ $100$`）与图例，⛔ **没有任何可抄的数据点**。⛔ **所以不能说「他们报了第 N 轮的收益是 X」。**

⭐⭐ **整个循环的净收益倒是有硬数字（RQ3 消融，Table 5/6）** —— ⭐ T0 = 无修复环，T1 = 完整；⭐ 表里给的是 T0 的值与相对 T1 的 Δ：

| 协议 | Client Msg Type（T0，Δ） | Server Msg Type（T0，Δ） |
| :-- | :-- | :-- |
| POP3 | 12/14 = 85.7%（⛔ **Δ −14.3pp**） | 6/9 = 66.7%（⛔ **Δ −33.3pp**） |
| SMTP | 11/11 = 100.0%（Δ 0） | 5/11 = 45.5%（⛔ **Δ −18.2pp**） |
| IMAP | 25/30 = 83.3%（Δ 0） | 10/17 = 58.8%（⛔ **Δ −11.8pp**） |
| FTP | 25/31 = 80.6%（Δ 0） | 4/15 = 26.7%（⛔ **Δ −40.0pp**） |
| ManageSieve | 14/14 = 100.0%（Δ 0） | 6/6 = 100.0%（Δ 0） |

⭐ precision 侧几乎全 **Δ = 0**（⛔ 唯一例外 FTP server −14.3pp）。

⭐⭐ **这张表的读法（⛔ 别读错）**：⭐ 修复环的收益**几乎全部落在 server 侧 message type 的 recall 上**（⭐ 4/5 个协议有 −11.8 到 −40.0pp 的损失），⛔ 而 client 侧除 POP3 外**完全不受影响**（Δ = 0），⛔ precision 也基本不受影响。⭐ 即：**这个循环补的是「漏了什么」，⛔ 不是「写错了什么」。**

⭐⭐ **与我们 v46 的对照（⭐ 这一格是本卡最大的价值）**：

| 维度 | ⭐ AutoSpec | ⛔ 我们 v46 |
| :-- | :-- | :-- |
| 外层裁决者 | ⭐⭐ **测试执行（真实 SUT）+ 确定性门** | ⛔ **LLM 自评**（`review_requirements` / `review_assertions`） |
| 谁决定要不要再来一轮 | ⭐⭐ **执行结果 + 三道确定性门** | ⛔ **LLM reviewer** |
| 循环净收益 | ⭐ **正**（server recall +11.8 ~ +40.0pp） | ⛔ **零**（⭐ 台账谓词覆盖净变化 ≈ 0，⛔ 吃 79% token） |
| 逐轮形状 | ⭐ **早期陡降、后期走平**（⭐ 2–3 轮消掉多数 syntax error，⛔ 剩语义 mismatch 难自动修） | ⛔ **第 3–5 轮零收益** |

⭐ **形状是同一个**（⛔ 后期走平），⛔ **但起点不同**：⭐ 他们早期有真实收益，⛔ 我们连早期都没有。⭐⭐ **这条差别把「循环该不该留」这个问题从「循环无用」精确成了「LLM 自评当裁决者无用」** —— ⭐ 因为同样的循环形状，换成执行当裁决者就付钱了。

⚠️⚠️ ⭐ **但必须扣一句重要的限定：⛔ 他们的 oracle 不 sound。** ⭐ SUT 是**实现**而非规约，⭐ 作者自己在 §7.6.2 承认：

> **M** · §7.6.2「The execution-guided repair loop updates the specification based on SUT responses. **This can drift toward an implementation-specific formal specification that validates the tested SUT rather than the RFC.** We mitigate this by keeping clause-level trace links and validating each repair against the source RFC text. **Residual overfitting may remain**, especially when multiple implementations share the same deviation.」

⭐ 而且 Table 4 的失败归因把非接受事件分成四类 —— `Needs-TLS` / `Impl-Missing` / `Data-State` / `Grammar-Bug`，⛔ **前三类是 SUT 侧限制而非规约错误**（⭐ 例如 SMTP 的 27.3% 非接受全部归 `Impl-Missing`）。⭐⭐ **即这个裁决者有系统性假阴性：SUT 没实现的东西会被误判成规约错。** ⭐ 所以它是「可执行、廉价、**有偏**」的裁决者，⛔ **不是** TLA+-Bench 那种 sound oracle。⭐ 两篇正好构成两极，⭐ 见 E 节。

### B5 · ⭐ 中间表示（⛔ 这是本文的卖点，⭐ 也是 parent 点名要问的第 2 条）

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐⭐ **有，而且是分层的**（⭐ 这就是「两阶段」的实质） |
| 形态 | ⭐ ① Pydantic JSON schema（`SectionPayload`）· ⭐ ② 类型化 multigraph $G = \langle S, C, E, \Phi \rangle$ · ⭐ ③ Minimal Transition Paths（MTP 集合）· ⭐ ④ I/O grammar（⭐ 终态制品，⭐ 但本身也被当作「可检视中间物」）· ⭐ ⑤ 修复端的 3 类 `error_class` |
| ⭐⭐ **是否闭合** | ⭐⭐ **混合 —— 容器闭合、内容开放。** ⭐ 字段集与全部 `type` / `action` / `response_type` / 边类型都是 Pydantic `Literal` **硬闭合枚举**；⛔ **但元素清单本身（状态名、命令名、约束文本）是自由生成的开放集** |
| ⭐ 谁定的 / 谁选类 | ⭐⭐ **预编 schema（作者定），LLM 在每一节自动选闭合处的类**（⭐ label / action / response_type / node type / edge type / error_class 全是 LLM 选）；⭐ **元素值 LLM 自由生成**；⛔ 全局合并与边类型规范化**由确定性规则做** |

⭐⭐ **闭合枚举逐条抄（M(code) · Drive 上的 `agents/stage1/models.py`，3,261 bytes，⭐ 我实际下载并通读）**：

| 枚举 | 取值 | 几类 |
| :-- | :-- | :-: |
| `ClassificationRec.section_type` | `"overview"` \| `"state_machine"` \| `"example"` \| `"other"` | ⭐ **4** |
| `ClassificationRec.action` | `"extract"` \| `"copy"` \| `"summarize"` | ⭐ **3** |
| `Command.response_type` | `"single-line"` \| `"multi-line"` | ⭐ **2** |
| `MultigraphNode.type` | `"state"` \| `"command"` \| `"response"` | ⭐ **3** |
| `MultigraphEdge.type` | `"dependency"` \| `"transition"` \| `"command_flow"` \| `"response_flow"` | ⭐ **4** |
| `MultigraphCluster.type` | `"state_group"` \| `"command_group"` | ⭐ **2** |
| ⭐ 修复端 `error_class`（**M** · Fig 7） | `"G-SYN"` \| `"T-MISM"` \| `"G-MISS"`（⭐ = Grammar Syntax Error / Trace Mismatch / Grammar Coverage Miss） | ⭐ **3** |

⭐ **`Command` 的完整字段（M(code)）**：`name` · `allowed_states: List[str]` · `success_transition: Optional[{from, to}]` · `response_type: Literal[...]` · `multiline_termination: Optional[{octet, pattern}]` · `arguments: List[{name, regex}]` · `depends_on: List[str]` · `notes: str`。⭐ 另有 `State{name, description}` · `Transition{from, to, trigger, note}` · `Timer{name, duration_seconds, scope}` · `SectionPayload{section_title, states, commands, transitions, timers, syntax_rules, examples, remarks}`。

⭐ **`MultigraphEdgeProperties.weight` 还带数值范围约束**：`Field(default=1, ge=1, le=10)` —— ⭐ 一个纯词法可判定的 validator，⭐ 完全符合本仓库 §11 的准入边界。

⭐⭐ **这与我们的 19 条闭合谓词是什么关系（⭐ parent 问的对位）**：

⭐ **不在同一层，⛔ 不能直接类比。**

- ⭐ 他们闭合的是**容器形状**：「一个命令必须有 name / allowed_states / response_type / …」，⭐ 以及少量枚举槽位（⛔ 最大的一个才 4 类）。⭐ **要抽哪些命令、每个命令叫什么，完全开放。**
- ⛔ 我们闭合的是**可问的问题种类**：19 条谓词是「能对制品提哪些问」的全集，⛔ 模型不能自造谓词。
- ⭐⭐ **真正与我们同层的是他们的 `error_class` 3 类**：⭐ 闭合集合 + **LLM 自动选类** —— ⭐ 这正是我们「闭合 19 条 + LLM 自动选」那个组合的一个先例，⛔ 但**只有 3 类而不是 19 条**，⛔ 且它分类的对象是「失败原因」而不是「该问什么」。

⭐ **所以对 [pipeline_forms.md](../pipeline_forms.md) 的「闭合 + LLM 选类」这一列，本篇应记「⭐ 有，但类目基数极小（2–4 类），⛔ 且没有一处闭合集合的规模接近 19」。**

### B6 · 模型

⛔⛔ **只写了「a GPT-4-class model」，⛔ 没有精确型号、⛔ 没有快照日期、⛔ 没有调用日期。** ⭐ 逐字 **M** · §6：「Unless noted otherwise, we use a **GPT-4-class model** (23) with fixed decoding settings (`temperature`=0, `top_p`=1.0, and no stop sequences) for reproducibility. We use a low temperature for determinism—`temperature`=0.1 for generation and `temperature`=0.0 for lightweight classification—and allow up to `max_tokens`=4000 for non-streaming long generations (grammar synthesis)」

⭐ 引用 (23) 我核过，是 **OpenAI, GPT-4 technical report, arXiv:2303.08774** —— ⭐ 即「GPT-4-class」这个说法挂的是 **2023 年 3 月**的技术报告。

⛔ **无多模型对照。** ⚠️ 论文自己承认 §6 里写的解码设置**前后矛盾**（⭐ 先说 `temperature=0`，⭐ 紧接一句又说生成用 `0.1`、分类用 `0.0`）。

⭐⭐ **按 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) B6 的告示，这一条要重罚**：⛔ 一篇 2025-11 的论文用「GPT-4-class」跑主结果，⛔ 距我们主臂（`gpt-5.5` / `claude-opus-4-7`）差了大约两代。⭐ **它的绝对数字（92.8% / 80.2% / 81.5%）对我们几乎没有参考价值；⭐ 有价值的是它的流水线形态与消融的方向。**

### B7 · ⭐ 确定性成分（⭐ 本篇的确定性底座相当厚）

| 环节 | 是什么 | 证据 |
| :-- | :-- | :-- |
| RFC 摄取 | ⭐ crawler 清洗 HTML，⭐ 保留 section ID + 段落索引 | **M** · §6 |
| ⭐ schema 校验 | ⭐ **Pydantic**，⭐ 全链条；⛔ 拒后重发一次 | **M** · §3.1.2 / §4.2 / §6 |
| ⭐ acceptance filter | ⭐ **不接受 LLM 输出原样**：⭐ 强制节点/边类型 · ⭐ 强制 provenance 锚（section ID + 段落索引，⭐ 节点与边都要）· ⭐ 冲突按 normative > examples/overviews 定序 | **M** · §3.1.3 逐字「**For reproducibility, we do not accept the LLM output verbatim.** We apply a deterministic acceptance filter」 |
| ⭐⭐ 全局合并器 | ⭐ **完全确定性、规则式**：标签归一（`USER`/`User`/`user` → `USER`；`Auth` → `AUTHORIZATION`）· ⭐ 边类型规范化 · ⭐ 节点边取 union 并保留 provenance · ⭐ 约束按交集传播、⭐ 矛盾则打 flag | **M** · §3.2「this merger is **fully deterministic and rule-based**」/「This rule-based consolidation **avoids hallucinations** and provides a reproducible baseline」 |
| ⭐ MTP 计算 | ⭐ **图算法**：从 $S_0$ 起对每个目标命令/迁移求最短边序列，⭐ 满足依赖 + 累积前置条件 + 目标态后置条件 | **M** · §3.2.2 |
| 检索 | ⭐ **BM25**（off-the-shelf） | **M** · §7.6.1 |
| ⭐ 门（合成后） | ⭐ Pydantic schema 检查 + ⭐ **MTP generatability 检查** | **M** · §4.1.5 / §5.2 |
| ⭐⭐ 测试生成与执行 | ⭐ **Fandango** grammar-based fuzzer（ICSE 2025）→ ⭐ 打容器里的真实 SUT | **M** · §6 |
| ⭐ 缺陷分类 | ⭐ 三道判据的决策树（Fig 2） | **M** · Fig 2 |
| 规范化 | ⭐ 去重 / 分组 / alias 一致性 / `<terminals>` 完整性 | **M** · §4.1.4 / §4.1.5 |
| 隔离 | ⭐ 每个 agent 各自 sandbox「to avoid cross-talk between roles」 | **M** · §6 |

⭐⭐ **一句总结**：⭐ **LLM 在这条流水线上只做「提议」，⭐ 每一次提议后面都跟着一道确定性的「接受/拒绝」。** ⭐ 论文把这条设计原则写成了明文（§3.1.3 的「we do not accept the LLM output verbatim」）。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **两组消融，⛔ 零个外部 baseline**：⭐ ① **RQ3 · T0**（去掉修复环，留 generator）；⭐ ② **RQ4 · 三种 naïve prompting**（⭐ 无 RFC 输入：zero-shot 只给 grammar schema / few-shot 给 schema + 两个域外迷你语法例 / 只给命令名列表）。⛔⛔ **没有与端到端 LLM 测试生成对照**（见下方「两阶段 > 端到端」）；⛔ 没有与 PROSPER / rfc2fsm / HDiff / Sage 等相关系统对照 |
| `dataset` | ⭐ **5 个互联网协议**：POP3（RFC 1939，23 页）· SMTP（5321，95 页）· IMAP（3501，108 页）· FTP（959，69 页）· ManageSieve（5804，49 页）。⭐ SUT：Dovecot 2.3.19.1（POP3/IMAP）· Postfix 3.7.11（SMTP）· vsFTPd 1.3.7a（FTP）· Pigeonhole 0.5.19（ManageSieve），⭐ 均容器化（`docker-mailserver:latest`, Debian 12, OpenSSL 3.0.15）。⚠️ **FTP 只覆盖控制通道**，⛔ 数据通道语义与载荷 out of scope |
| ⭐ 分母怎么定的 | ⭐⭐ **分母 = 作者自己写的 golden grammar 里的元素数**。⭐ 五个协议的 golden 规模：msg types 21–48、⭐ 独立约束 5–14、⭐ 依赖约束 0–3、⭐ LoC 295–676、⭐ **专家撰写墙钟 3.5–14 小时** |
| `metrics` | ⭐ **RQ1** precision / recall（⭐ 按元素集合求交，四类元素：Client Msg Type / Server Msg Type / IndepC / DepC）· ⭐ **RQ2** Message Acceptance（MA）· Trace Acceptance（TA）· ⭐ 以及限制到 golden 的 canonical route 子集的 RtCMA / RtCTA。⛔ **无 `@k` 口径**，⛔ 无多轮聚合指标 |
| ⭐ `judged_by` | ⭐⭐ **作者自己**（⛔ 见下，⛔ 这是本篇最弱的一格） |
| `human_baseline` | ⭐ **算有，但不是当 baseline 报的**：⭐ golden grammar 的**专家撰写工时**（3.5h / 9.5h / 14h / 5.5h / 5h）在 Table 1 里列了，⛔ 但**没有与 AutoSpec 的墙钟或成本做对照** |
| `runs` | ⛔ **主结果看不出跑了几次**（⭐ 每协议一份产出，⛔ 无方差、⛔ 无均值说明），⭐ `temperature=0.1` 即**并非确定性**。⭐ **唯一报多次的是 RQ4**：`0/5` · `2/5` · `3/5`（⭐ 5 次试验的 syntactically valid 计数） |
| ⭐ `adverse_results` | ⭐ **报了，⛔ 但摘要里没有** —— ⛔ 见下 |

### ⛔⛔ `judged_by` —— 本篇最弱的一格

> **M** · §7.1 逐字：「We evaluate AutoSpec on five Internet protocols... **against "golden grammars" written by one of us as protocol experts.** We execute each golden grammar once for sanity checks.」

- ⛔ **ground truth 是作者之一写的**，⛔ **无第三方**、⛔ **无标注者间一致性**（⛔ 没有 $\kappa$、⛔ 没有一致率、⛔ 没有双人独读）。
- ⭐ 唯一的质量控制是「each golden grammar 执行一次做 sanity check」。
- ⛔ **precision / recall 的元素匹配是谁做的、怎么判「两个元素算同一个」—— 原文未提供。** ⭐ 只有一句口径「collapsing purely lexical aliases」（⭐ 合并纯词法别名），⛔ 但没说谁来判别名。
- ⛔ **Table 4 的四类失败归因（Needs-TLS / Impl-Missing / Data-State / Grammar-Bug）是谁标的 —— 原文未提供**，只写「Failure causes are labeled per non-acceptance event」。

⭐⭐ **与我们的直接对照**：⭐ 我们的 574 位逐位 + 288 簇五类裁定虽然贵，⛔ 但它至少是**显式的、可审计的、成规模的**。⭐ 这篇的判定规模是「一个人写了 5 份 golden，共 2,369 LoC，用了 37.5 小时」，⛔ 之后的所有 precision/recall 都锚在这 5 份上，⛔ **没有任何一致性证据**。⭐ **换言之：如果拿这篇当「别人也不做人工复核」的挡箭牌，⛔ 那是拿一篇更弱的做法给自己背书。**

### ⭐ 主结果

⭐ **RQ1 recall（Table 2）**：Client Msg Type 平均 **92.8%**（POP3/SMTP/ManageSieve 100%，IMAP 83.3%，FTP 80.6%）· Server Msg Type 平均 **80.2%**（POP3/ManageSieve 100%，IMAP 70.6%，FTP 66.7%，SMTP 63.6%）· ⛔⛔ **IndepC 平均 16.7%** · ⛔⛔ **DepC 平均 0.0%**。

⭐ **RQ1 precision（Table 3）**：Client 平均 **99.2%** · Server **94.3%** · IndepC **42.3%** · ⛔ **DepC 0.0%**。

⭐ **RQ2 执行侧（Table 4）**：MA 71.4%–92.9%（⭐ 加权约 81.5%）· TA 57.1%–90.0%。⭐ RtC 口径几乎都比 raw 高（⭐ SMTP TA 57.1% → RtCTA 66.7%；⭐ ManageSieve 69.2% → 81.8%），⭐ 作者据此论证「grammars 在核心流程上是 sound 的，剩下的掉分对应 SUT 限制或前置条件而非系统性语法错」。

⭐ **RQ4（Table 7）**：⛔ 三种 no-RFC 设置**全部失败** —— syntactically valid `0/5` · `2/5` · `3/5`，⛔ **Executable 全是 No**，⛔ command coverage `0%` / `<10%（generic）` / `~40%`，⛔ state transitions `None` / `Hallucinated` / `Incorrect`，⛔ **semantic constraints 三个全是 `None`**。

### ⭐ `adverse_results` —— ⭐ 报了，⛔ 但表述有方向性偏斜

⭐ **报得干净的部分**：

1. ⭐⭐ **`DepC recall = 0.0%` 与 `IndepC recall = 16.7%` 明明白白印在主表的 Average 行**，⛔ 没有藏。⭐ 且给了归因：「Constraint extraction is weaker: IndepC and especially DepC are predominantly expressed as dispersed normative prose (ranges, conditioned enums, cross-field/temporal relations), leading the agent to **mirror surface syntax while under-extracting such semantics**.」
2. ⭐ **明说 server 侧落后**并给机制解释（⭐ client 命令在 RFC ABNF 里显式枚举，⛔ server 回复常常只给 schema）。
3. ⭐ **§7.6 四条 threats 逐条自认**：检索质量（⭐ 用的是未调优的 off-the-shelf BM25，⛔ 「important clauses may be missed or misranked」）· ⭐⭐ **修复环对实现过拟合**（见 B4）· 先验知识/污染 · 协议范围（⛔ 只有 5 个 ASCII 会话协议，⛔ 二进制/加密/实时栈未覆盖）。
4. ⭐ **明说不用大众化数据**并给理由：「we do not use proprietary Volkswagen specifications in this paper due to confidentiality and system maturity」。

⛔⛔ **偏斜的部分（⭐ 这条对我们写报告是一条反面教材）**：

⭐ 摘要与 §1 反复给的三个数是 **92.8% / 80.2% / 81.5%**，⛔ **一次都没提 `DepC recall = 0.0%` 与 `IndepC recall = 16.7%`**。⛔ 而依赖约束恰恰是 I/O grammar 相对 CFG 的**核心增值**（⭐ §1 自己说「semantic constraints... a property that cannot be expressed in a context-free grammar alone」「In protocols, satisfying such constraints is crucial」）。⭐⭐ **也就是说：论文把「这个形式化最值钱的那一层，我们抽取率是 0」这件事只写在正文表格里，⛔ 摘要一字不提。** ⭐ 这与本仓库 [talks/GUIDE.md](../../../../../talks/GUIDE.md) §9 的「方向性松紧要一致」正是同一条纪律，⛔ 而这篇违反了它。

---

## D. ⭐ 资产（⛔ 全部实际去取过）

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [arxiv.org/html/2511.17977v1](https://arxiv.org/html/2511.17977v1) | ⭐ HTML 全文 345,227 bytes 已下载并通读；⭐ 8 张图（含 3 张 prompt 截图）逐张下载并读图 |
| ⭐ **实验代码（完整实现）** | ⭐ 🟠 | Google Drive `AUTOSPEC/repository/src/autospec/` | ⭐ 机械核验：`python3 -m tools.verify_assets --url https://drive.google.com/drive/folders/1TFRsOUbNby-tg3SIDORk5tZr21GsFiZV` → `🟢 HTTP 200 · text/html`（⛔ 该工具对 Drive 只能查存在性，⛔ 查不了内容）。⭐ **我逐层展开核过**：`repository/src/autospec/` 有 `main.py`（**33 KB**）· `config.ini`（2 KB）· `config_rfc.ini`（408 B）· `agents/{stage1, stage2}`；⭐ 两个 agents 子目录共 **9 个 `.py`，约 187 KB**（`rfc_summarizer_agent.py` 38 KB · `tree_based_retriever_grammar_generator.py` 38 KB · `fandango_fixer_agent.py` 27 KB · `prompts_s2.py` 23 KB · `build_mtp.py` 22 KB · `retriever_agent.py` 16 KB · `prompts_s1.py` 15 KB · `build_cmd_dict.py` 3 KB · `models.py` 3 KB）。⭐ 我**实际下载并读过** `models.py`(3,261 B)、`prompts_s1.py`(15,064 B)、`build_mtp.py`(22,451 B)、`rfc_summarizer_agent.py`(39,275 B)。⛔ **判 🟠 而非 🟢 的三个理由**：① ⛔ Drive 上的 `README.md` 自称 `src/` 是「**minimal method-supporting code (context only)**」，② ⛔ 论文结尾自称「**we plan to make AutoSpec publicly available as well**」（⭐ 即当前不是完整发布），③ ⛔ **无 license · 无版本控制 · Drive 内容可变**（⚠️ 两个文件显示修改于 **Apr 13**，⛔ 晚于 2025-11 的论文 —— ⭐ 即我今天取到的**不是论文那一版**） |
| ⭐ **数据集 / Benchmark** | ⭐ 🟢 | Drive `repository/RFC/` + `repository/evaluation/experiments/` | ⭐ 逐层核过：`RFC/{rfc_text, protocol_spec_artifacts}` · `evaluation/experiments/<protocol>/{manual_grammars, generated_grammars}` · ⭐ `Prototols_and_CMDs_List.txt`（2,151 B，⭐ 我下载并读过全文：⭐ **五个协议逐命令的 ok/untested 标注**，例如 IMAP 25 条命令逐条状态、⭐ FTP 多条标 `ok (untested) data connection required`）。⭐ **条目数**：5 个协议 · ⭐ 21–48 msg types / 协议 · ⭐ golden grammar 295–676 LoC。⭐ **有 ground truth**：`manual_grammars/` 即作者手写的 golden I/O grammar |
| ⭐ 实验结果细则 | ⭐ 🟢 | Drive `evaluation/experiments/<protocol>/generated_grammars/` | ⭐⭐ **有可下载逐迭代结果，⛔ 不只是论文内表格**。⭐ README 逐字给了命名约定：`grammar_iterN.fan`（第 N 轮生成的语法）· `fandango_output_iterN.txt`（执行日志）· `evaluation_iterN.json`（第 N 轮的 fix/evaluation 报告）· `FINAL_REPORT_iterK.md`（收敛时的最终摘要）。⭐⭐ **这意味着 Fig 8/9 缺的逐轮数字，理论上可以从这批 `evaluation_iterN.json` 自己算出来** —— ⭐ 见 F 节 |
| Artifact / 复现包 | ⭐ ⚪ | — | ⛔ **无 Zenodo / OSF / 4open / figshare DOI**，⛔ 无归档快照，⛔ 无 release tag。⭐ 唯一入口是一个 Google Drive 文件夹（⛔ 可变、⛔ 无版本、⛔ 无 DOI、⛔ 无 license） |
| ⭐ **prompt 是否公开** | ⭐ 🟢 | Drive `agents/stage1/prompts_s1.py` + `agents/stage2/prompts_s2.py` | ⭐ **仓库里有完整 prompt 源码**：`prompts_s1.py` **15,064 bytes（我实际下载并读过）** + `prompts_s2.py` 23 KB。⚠️ ⭐ **论文里的 Fig 4 / 6 / 7 只是截图且带省略号**（⭐ 例如 Fig 4 的 Output Schema 末尾直接写 `"…": "…"`，⭐ Fig 4 的 Guidelines 末尾是 `Deps. List prerequisites in "depends_on"….`）—— ⛔ **只看论文拿不到完整 prompt，⭐ 必须去 Drive** |

### ⛔ 三个交叉核验发现（⭐ 论文里读不到）

1. ⭐⭐ **`models.py` 的边类型枚举与论文正文不一致。** ⭐ 论文 §3.2.1 说边类型是 `invokes`（state→command）· `yields`（command→state/response）· 以及 command 间的依赖「later normalized into `requires` / `enables`」。⛔ **但 `models.py` 里 `MultigraphEdge.type` 是 `Literal["dependency", "transition", "command_flow", "response_flow"]`** —— ⛔ 两套名字**一个都不重合**。⚠️ 可能是实现演进后论文未同步（⭐ 或反之），⛔ **原文未说明**。
2. ⭐ **`Timer` 模型存在但从不出现在论文里**（⭐ `Timer{name, duration_seconds: int, scope}`，⭐ 且 `SectionPayload.timers: List[Timer]` 是必填字段）。⛔ 论文正文、评测、golden grammar 度量里**一次都没提定时器**。⭐ 说明抽取层已经预留了时间维，⛔ 但未被评测 —— ⭐ 这一点对我们判 boundary 有意义。
3. ⭐ **Drive 上有文件的修改日期是 `Apr 13`（2026），⛔ 晚于论文提交（2025-11-22）** —— ⭐ 具体是 `fandango_fixer_agent.py` 与 `tree_based_retriever_grammar_generator.py`。⛔ **即当前 Drive 内容不等于论文那一版**，⛔ 而 Drive 没有版本历史可回溯。

---

## E. ⭐ 对 M1 的意义

### 1. ⭐ 可取之处

1. ⭐⭐⭐ **「每次 LLM 提议后面必须跟一道确定性的接受/拒绝」这条原则，⭐ 本篇写成了明文并落实到了每一格。** ⭐ 逐字可引：§3.1.3「**For reproducibility, we do not accept the LLM output verbatim.** We apply a deterministic acceptance filter」+ §3.2「this merger is **fully deterministic and rule-based**... **avoids hallucinations**」。⭐ 我们 v46 的 5 个 LLM 节点里，⛔ 只有 `convert_assertions` 后面接了确定性门（`precheck_and_seal`），⛔ `split_requirements` 与 `adjudicate_results` 后面接的都是 LLM。⭐ **M1 可以直接把这条当结构原则：每个 LLM 节点后必须有一道确定性 acceptance filter。**
2. ⭐⭐ **裁决者用「执行」而不是「LLM 自评」，⭐ 而且这次有净收益数字。** ⭐ RQ3 消融给了 server recall +11.8 ~ +40.0pp。⭐ 结合 B4 那张对照表，⭐ M1 手上现在有一个**受控的形态对照**：⭐ 同样形状的修复环（⭐ 早期陡降、后期走平），⛔ 裁决者是执行 → 付钱；⛔ 裁决者是 LLM 自评 → 不付钱。⭐ **这比「循环无用」精确得多，⭐ 也更好写。**
3. ⭐⭐ **「后期走平」这个形状拿到了一个外部同形观察。** ⭐ 逐字：「The loop is most effective early, converting many Grammar Syntax Error to successes by round 2–3. What remains are semantic/behavioral mismatches that are harder to resolve automatically.」⭐ 我们的「第 3–5 轮零收益」不再是孤例，⭐ 而且它给出了**下一步该做什么**的建议（⭐ 早轮做 syntax-aware 修复、⭐ 晚轮上 trace-semantics 辅助：exemplar alignment / stricter oracle checks / targeted prompts）。
4. ⭐⭐ **provenance 锚做成了硬门。** ⭐ acceptance filter「requires **provenance anchors (section ID and paragraph indices) for both nodes and edges**」；⭐ 冲突按「**normative text > examples/overviews**」定序；⭐ patch 阶段「maintain a minimal diff while **preserving provenance (RFC_ID/section/paragraph)**」。⭐⭐ **这是「可检视性」在工程上真正落地的那一半** —— ⛔ 不是「让人能读」，⭐ 而是**每个元素都必须能指回它是从哪一段来的，指不回来就不收**。⭐ 我们的 `named_elements` 层如果要主张可检视，⛔ **缺的正是这条硬门**（⭐ 目前 `nl_cue` 是描述性的，⛔ 不是拒收判据）。
5. ⭐ **「允许交白卷」这条纪律**：Fig 4「Extract from **this section only**」+ `prompts_s1.py`「If zero items meet the above, the corresponding list **MUST be []**」。⭐ 我们的契约门倾向于**逼出产出**，⛔ 这可能正是多报的一个来源。⭐ 值得做一次对照实验。
6. ⭐ **`weight: Field(default=1, ge=1, le=10)` 这类 validator 是本仓库 §11 准入边界的正面样例**：⭐ 纯数值范围、⭐ 只看字段值就能唯一判定。⭐ 全套 schema 里**没有一条**需要语义解释的 validator —— ⭐ 语义纪律全在 prompt 的 Guidelines 与 Guardrails 里。⭐ 这与我们 §11 的裁定完全一致，⭐ 可作为一个外部佐证。
7. ⭐ **RQ4 那个消融值得抄形状**：⭐ 把「不给外部资料、只靠模型先验」当对照组，⭐ 结果三档全崩（⛔ Executable 全 No、⛔ semantic constraints 全 None）。⭐ 我们的 X1 朴素基线是「单提示直接通读发现」，⭐ 但**没有「不给 NL 只给制品」这一档** —— ⭐ 补上这一档可以证明我们的方法确实在用 NL，⛔ 而不是在用模型对状态机的先验。

### 2. ⛔ 不可取 / 陷阱

1. ⛔⛔ **它的 oracle 不 sound，⭐ 而且作者自己知道。** ⭐ SUT 是实现不是规约，⛔ 修复环会往「验证这个 SUT」而不是「符合 RFC」漂（§7.6.2）。⭐ 更要紧的是 Table 4 的失败归因里 3/4 类（`Needs-TLS` / `Impl-Missing` / `Data-State`）**是 SUT 侧限制而非规约错**（⭐ SMTP 的 27.3% 非接受全部是 `Impl-Missing`）—— ⛔ **即这个裁决者有系统性假阴性**。⭐⭐ **对 M1 的直接含义：把裁决者换成「执行」不等于换成 sound oracle。⭐ 我们手上的 pyfcstm 求值器比 SUT 强（⭐ 它对规约本身可判定），⭐ 应该用它，⛔ 而不是照抄「打真实实现」。**
2. ⛔⛔ **ground truth 是作者一人写的，⛔ 无一致性证据。** ⭐ 见 C 节。⛔ **不要拿这篇当「别人也不做人工复核」的挡箭牌** —— ⭐ 那是拿更弱的做法给自己背书，⭐ 而且它在任何严格审稿下都会被打。
3. ⛔ **它踩了「自由生成语义约束」的坑，⭐ 而且代价被量化了：`DepC recall = 0.0%`。** ⭐ 依赖约束（跨字段、时序、"must follow"）是完全开放自由生成的 —— ⛔ **没有闭合词表、⛔ 没有类目、⛔ 没有谓词族**，⛔ 结果一条都抽不出来。⭐⭐ **这是「闭合词表 vs 自由生成」这个设计选择目前最硬的一个反面证据，⭐ 而且落在与我们最相关的那一层（语义 / 跨元素 / 时序）。** ⭐ 值得写进 M1 的论证。
4. ⛔ **模型代际差两代**（GPT-4-class，挂 2023-03 的技术报告）。⛔ 它的绝对数字对我们无参考价值。
5. ⛔ **「两阶段优于端到端」这个主张没有实验支撑**（见 F 节第 1 条）。⛔ **不要把它当硬证据引。**
6. ⛔ **摘要选择性报数**（⛔ 只报 92.8/80.2/81.5，⛔ 不报 DepC 0.0%）。⭐ 这正是我们 §3.6 与 talks §9 要避免的那种写法 —— ⭐ 反面教材，⛔ 别学。
7. ⛔ **无方差、无重复运行**（⛔ 除 RQ4 的 5 次），⛔ 而 `temperature=0.1` 并非确定性。⭐ 我们的三口径 `hit@1/@3/@all` 在这一格上强于它。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| 维度 | ⭐ AutoSpec | ⛔ 我们 v46 |
| :-- | :-- | :-- |
| 任务方向 | ⭐ **NL → 制品**（造规约） | ⛔ **NL + 制品 → 缺陷**（挑毛病） |
| 裁决者能不能执行 | ⭐ **能** —— ⭐ grammar 可以生成会话去打真实实现，⭐ 接受/拒绝有客观信号（`+OK` / `2xx`） | ⛔ **没有等价物** —— ⭐ 「这是不是一条真发现」没有可执行的接受信号，⛔ 参照物是人写的台账 |
| 循环修的是什么 | ⭐ **规约本身的缺漏**（⭐ 补 server 侧漏掉的消息类型） | ⛔ **断言的形式合法性与选题** —— ⭐ 而选题赤字（「根本没问」69 位）**没有任何执行信号能指出来** |
| 闭合集合的层次 | ⭐ 闭合**容器形状**（⭐ 2–4 类的小枚举），⛔ 元素清单开放 | ⛔ 闭合**可问的问题种类**（19 条谓词） |
| 中间制品给谁看 | ⛔ **谁都没看**（见 F 节第 4 条） | ⛔ 同样没有外部读者 |

⭐⭐ **所以本卡对我们的正确读法**：⭐ **可以搬的是「LLM 提议 + 确定性 acceptance filter」这个结构原则、⭐ provenance 锚做硬门、⭐ 允许交白卷、⭐ 以及「自由生成语义约束 → 0.0%」这个反面证据。** ⛔ **不能搬的是「拿实现当 oracle」** —— ⭐ 我们的任务里没有那个实现，⭐ 而且他们那个 oracle 本身就有系统性偏差。

---

## F. ⛔ 存疑与未核项

1. ⚠️⚠️ ⭐⭐ **parent 点名要查清的第 1 条 —— 答案是：「两阶段优于端到端」⛔ 只是设计理由，⛔ 不是实验对照。⭐ 这一条我核得很实，可以定论。**
   - ⭐ 论文给了**四条理由**（Abstract 与 §1 各列一遍，措辞略异）：① inspectable specification + 句级 traceability（⭐ 挂引用 (6)）· ② 「the generation of actual test cases **no longer requires an LLM**」/「All subsequent testing steps are reproducible and free of LLM nondeterminism, hallucinations, or cost」· ③ human-readable，可 review / version-control / 增量精化（⭐ 挂引用 (16)）· ④ 攒 NL→formal 语料以便日后微调。
   - ⛔ **但论文里没有任何端到端 LLM 测试生成的 baseline。** ⭐ 我逐节核过全部四个 RQ：⭐ RQ1 = 对 golden 的 precision/recall；⭐ RQ2 = 对真实 SUT 的接受率；⭐ RQ3 = **消融修复环**（⛔ 不是消融两阶段架构）；⭐ RQ4 = **消融 RFC 输入**（⛔ 三种 no-RFC 的 grammar 生成，⛔ 仍然是「生成 grammar」这个任务，⛔ 不是「直接生成测试」）。
   - ⛔ 支撑「端到端不行」的全是**转引**：§1「our experience asking LLMs to generate test cases reveals well-known weaknesses: hallucinated inputs, missed corner cases, poor traceability... —problems observed in multiple studies (14; 3; 19; 15)」——⛔ **「our experience」没有数据**，⛔ 四个引用是别人的。§2.5「naïve end-to-end prompting over long documents such as RFCs yields incomplete, misaligned, and non-executable artifacts... (14)」同样是转引。
   - ⭐⭐ **结论：对我们是「软论据」。** ⭐ 它能用来支持「为什么要有可检视中间制品」这个**设计取向**，⛔ 但**不能**用来说「已有实验证明两阶段优于端到端」。⚠️ ⭐ 若 M1 要给 `named_elements` 那层补 why，⭐ 这篇能提供的是**一组清晰表述的理由 + 一个真实工业动机（Volkswagen 的持续交付需要可审计的测试）**，⛔ 不是数字。
2. ⚠️⚠️ ⭐ **逐轮边际收益的数字拿不到。** ⭐ Fig 8（survival curve）与 Fig 9（每轮堆叠柱）是 LaTeX/tikz 渲染，⛔ HTML 里只有坐标轴刻度与图例，⛔ 无数据点。⭐ **已试过**：arXiv HTML 全文抽取（⭐ 只得到 `$0$ $1$ … $7$` 与 `$0$ $50$ $100$`）· 全文 grep「round」「survival」「censored」（⭐ 只有定性句）。⛔ **未试过**：下载 PDF 从矢量图里解坐标、⭐ 或从 Drive 的 `evaluation_iterN.json` 自己重算。⭐⭐ **后者看起来可行且值得做**（⭐ 5 协议 × 至多 7 轮的 fix 报告都在），⛔ 但那是新工作而非阅读。
3. ⚠️ ⭐ **`models.py` 的边类型与论文 §3.2.1 的 `invokes` / `yields` / `requires` / `enables` 完全不重合**（⭐ 代码是 `dependency` / `transition` / `command_flow` / `response_flow`）。⛔ **原文未说明**。⚠️ ⭐ 我不能判定哪一版是论文实验用的 —— ⭐ 而 Drive 上有文件修改于 2026-04（晚于论文），⛔ 所以「代码即论文实现」这个假设**不成立**。⭐ **已试过**：读 `models.py` 全文、⭐ 比对论文 §3.1.3/§3.2.1；⛔ **未试过**：读 `build_mtp.py`(22 KB) 与 `rfc_summarizer_agent.py`(39 KB) 确认实际用的是哪套（⭐ 两份我都下载了，⛔ 但未逐行读）。
4. ⚠️⚠️ ⭐⭐ **parent 点名要查的第 4 条 —— 「可检视性」⛔ 从未被兑现或度量。⭐ 这一条我也核得很实。**
   - ⛔ **没有用户研究、⛔ 没有专家评审、⛔ 没有可读性度量、⛔ 没有「人看了中间规约之后发现了什么」的数据。**
   - ⭐ 唯一出现的人是**写 golden grammar 的那位作者**，⛔ 而他的角色是**提供 ground truth**，⛔ 不是**审阅生成的规约**。
   - ⭐ 兑现的只有可检视性的**机器可核那一半**：provenance 锚（section ID + 段落索引）被做成了 acceptance filter 的硬门、⭐ patch 阶段强制保留 `RFC_ID/section/paragraph`。⭐ 即「**能指回原文**」是真的、⭐ 可机械校验的；⛔ 「**人真的会读、读了有用**」完全没证。
   - ⭐⭐ **对我们的含义**：⭐ 若 M1 拿这篇给 `named_elements` 补 why，⭐ 能拿到的是「**可指回性可以做成硬门**」这个工程做法，⛔ **拿不到「可检视性有收益」这个结论**。⛔ **别把后者写成引用。**
5. ⚠️ **`GPT-4-class model` 到底是哪个型号 —— 原文未提供。** ⭐ 已试过：全文 grep `gpt`/`GPT`/`model`（⭐ 只得到「GPT-4-class」与引用 (23) = arXiv:2303.08774）· ⛔ 未试过：读 `config.ini`（2 KB，⭐ 在 Drive 上，⭐ 里面**极可能写着确切 model id**）。⭐ **这是一个便宜且值得补的核验动作**，⛔ 我没做是因为它需要再一次 Drive 文件下载而收益边际。
6. ⚠️ **§6 的解码设置自相矛盾**：先写 `temperature=0, top_p=1.0`，⭐ 紧接一句写「`temperature`=0.1 for generation and `temperature`=0.0 for lightweight classification」。⛔ 无法判定主结果实际用的哪个。
7. ⚠️ **Table 3 的 precision 分母有多处 `0/0(-)`**（⭐ SMTP/IMAP/FTP 的 IndepC 与 DepC）—— ⭐ 即「一条都没抽出来，所以 precision 无定义」。⛔ 而 Average 行仍给了 IndepC 42.3% / DepC 0.0%。⛔ **这个平均是怎么算的（⭐ 是否把 `-` 当 0、⭐ 还是只对有定义的取平均）—— 原文未提供。** ⚠️ ⭐ 我按「Average 行不可复算」处理，⛔ 引用时应只引逐协议格，⛔ 不引 Average。
8. ⚠️ **`I/O grammar` 这个形式化本身我没读原文**（⭐ Liggesmeyer, Amaya, Zeller, [arXiv:2509.20308](https://arxiv.org/abs/2509.20308)，⭐ 我核过这条引用在参考文献里真实存在，⛔ 但未读）。⛔ 所以本卡对 I/O grammar 表达力的一切陈述都是**本文的转述**。⭐ 同理 Fandango（Amaya, Zeller, Smytzek, ICSE 2025）也未读原文。
9. ⚠️ **未核 PROSPER (HotNets'23) / rfc2fsm / HDiff (DSN'22) / Sage (SIGCOMM'21) / Zheng et al. (arXiv:2504.18050) 原文。** ⭐ 本文对它们的定位（⛔「most target a single layer (syntax or FSM)」「**they universally require manual verification and lack execution-guided repair**」）全是转述。⚠️ ⭐ **特别提醒**：若 M1 要引「别人都需要人工核验」这句当我们的差异化，⛔ **必须回那几篇原文核** —— ⭐ 这正是本仓库 §3.8 那条纪律的适用场景。
