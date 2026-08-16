# 逐 pair 人工审阅规范

## 你在判断什么

对每个 pair，判断**作者生成的 STM_0**（`pairs/<case>-author.puml`）相对**参考 STM_0**（`refs/<group>-reference.puml`）有哪些**真实问题**。

**核心要求：不做机械的元素存在性比对。** 名字不同、结构不同、拆分方式不同，只要**语义上说得通**，就必须标为 `correct` 或 `similar`，不能算问题。例如：

- `human_mode` vs `HumanDrivingMode` → 同一状态，`similar`（仅命名风格差异）
- `avoid_frontend_collision` vs `F` → 同一状态，`similar`（缩写）
- 参考用两条边 `A→B`、`B→C`，生成用一条 `A→C` 并把 B 的语义并入 → 判断这是否丢失了 NL 要求的中间状态；若 NL 未要求 B 可观测，标 `similar`
- 参考把三个区域写成 `--` 并发区，生成写成三个顺序子状态 → 这是**语义差异**（并发 vs 顺序），标为问题，但要注明它属于正交并发类
- 参考 `[*] --> A : power_on`，生成 `[*] --> A`（无触发）→ **真问题**（丢失触发条件）

## 判定档位（每条差异一个）

| 档位 | 含义 |
| --- | --- |
| `correct` | 生成方与参考在该点语义等价，写法不同而已 |
| `similar` | 有差异但语义上说得通、不违反 NL；记录差异内容 |
| `problem` | 真实问题：违反 NL 或丢失参考模型所承载的语义 |
| `extra` | 生成方多出参考模型没有、NL 也未要求的元素（over-specification） |
| `uncertain` | 证据不足以判定，说明卡在哪 |

## 每个 pair 必须产出

1. **逐条差异清单**：每条给出 `档位` + 参考侧内容 + 生成侧内容 + **理由**（为什么这样判）
2. **该 pair 的问题总数**（只数 `problem` 与 `extra`）
3. **每个 `problem` 的可断言性**：能否用当前 19 个谓词写出一条正向断言（给出建议的断言形式；不必实测，但要说明该谓词是否存在）
4. **与三份既有记录的对照**：
   - 论文的 per-case 记录（`paper_reported_problems.json` 里该 case 的 `format_hallucinations` / `grammar_hallucinations` / `semantic_hallucinations` 与各 `resolved`）
   - 论文的 Phase-I / Phase-II F1（同文件的 `f1_phase1` / `f1_phase2`）
   - 台帐的 E1（`ledger.json` 的 `findings` 中 `issue_id` 含该 case 号的条目）逐条说明：你判的 `problem` 里哪些已被论文记录、哪些已被台帐记为 E1、哪些**两者都没有**

## 重要背景（避免误判）

- 语料的 `pairs/<case>-author.puml` 是论文 **Phase-II 语义检查后**的产物（workbook 列 AE），不是 Phase-I 原始生成。所以论文 `semantic_hallucinations` 里记的问题**可能已在这份制品中被修好**，`semantic_resolved = 1.0` 即论文声称已修。你审的是**这份最终制品**。
- 参考模型是论文作者**人工重建**的。原论文 §3.3 说 "All reconstructed models were cross-validated against the original sources"，§4.2 第 (4) 项说 "we **assume** the reference model is semantically correct"——其正确性未经独立验证。（**注意**：§7 那句 "we manually created them, which is subjective" 的先行词是 **requirements（NL 文本）**，不是参考模型；且原文紧接着写了 cross-check。不要把它引成对参考模型的自认。）**若你认为参考模型本身有问题或与 NL 不一致，必须记录**（档位用 `uncertain` 并说明）。已知实例：HLDCS 参考的 `brake_pressed` 与 `in (auto_final)` 方向与 NL 相反、`human_steering_cmd` 双向并存、完全缺 NL 点名的 `front_distance > 10`；NL05 参考有五条无标签 completion 边使其自己声明的分支不可达。

### 范围外（`out_of_scope`）的边界 —— 硬规则

本研究的建模对象是 **FSM / HSM / EFSM**（$M = (S, E, V, Tr, A)$），**不含时钟与正交并发**。并发类与时间类差异要**照实记录**，但在档位后额外标 `out_of_scope: concurrency` / `out_of_scope: timing`。

上一轮因为没写死边界，出现了**同一现象被反向裁定**：`0006`(NL03) 把「参考用区域承载的三路分解在生成侧塌缩」判 `problem` **未标 tag**（理由：这是数量/结构问题），`0033`(NL06) 把同一现象判 `problem` **标了 concurrency**（理由：并发结构超出范围）——两者用的还是**同一个谓词** `cardinality(count=3)`。后果是「计入问题」只能报区间而非确定值。**按下表重判后可以说清哪边对：`0006` 判对了，错在 `0033` 整条打 tag 而没拆**（见 [manual_review/RESCOPE.md](../../ledger_v2/provenance/RESCOPE.md)，重判后「计入问题」收敛为 157）。因此现在按下表执行：

| 现象 | 归属 | 理由 |
| --- | :-: | --- |
| NL 或参考说「有 N 个 X」而模型只有 M 个 | **范围内** | 这是**数量 / 结构**断言，落在 $S$ 内，与是否并发无关 |
| 区域之间是否**同时活跃**（并发执行语义） | **范围外** `concurrency` | 正交区语义不在 $M$ 内 |
| 定时器**动作**（`Start Timer`） | **范围内** | 属 $A$ |
| 定时器**事件**（`Timer Expired`） | **范围内** | 属 $E$ |
| 零时 / 剩余时间**守卫**（`[Zero Time]`） | **范围内** | 是 over $V$ 的普通守卫 |
| 真正的**时长约束**（`execTime=[(2,s,max)]`） | **范围外** `timing` | 属时间自动机的 $C$，$M$ 里没有 |

**并且：一条 diff 不得同时承载范围内与范围外两个方面。** `problems_in_scope` 按**整条 diff** 扣除，所以给一条兼有两面的 diff 打 tag 会**静默丢掉其中的范围内缺陷**。上一轮有 3 条如此（`0033`d2、`0039`d4 的理由明写「这是**独立于并发议题**的确定性缺陷」、`0053`d1 明写「三主子态从可同时活跃退化为互斥且互不可达」**是真实的语义损失**）。遇到这种情况**必须拆成两条 diff**：范围内那条不打 tag，范围外那条打 tag。

### 比较级断言 —— 两条硬约束

自由文本里的「唯一」「最…」「全库」「本组」「六例中」「并列」「第 n」是最容易出错的一类：上一轮 141 条这类断言中有 **9 条被证伪**（勘误见 [manual_review/COMPARATIVE_CLAIMS_AUDIT.md](../../ledger_v2/provenance/COMPARATIVE_CLAIMS_AUDIT.md)）。它们不改变计数，但会被逐字渲染进人读报告、成为论文叙事的上游，其中一条还把「论文口径最优制品其实问题最多」这个方法论论点挂在了错误样本上。

**(a) 任何比较级断言必须写明范围词。** 范围超出你负责的 NL 组时，必须附上机械核验命令或明确标注「未核验」。上一轮 8 条全库级断言里 3 条为假（37.5%），因为没有任何环节聚合过跨组事实——「全库唯一用方括号守卫」的 `0050` 实际排第 7，`0059` 有 19 条。

**(b) 交稿前对本组 6 份记录跑一次互斥性回扫。** 同一判据下，「唯一」「最好」「并列」不能同时给两个 case。上一轮 6 条组内假断言**全部是同一单元自己打自己**：`0019`↔`0059` 各写了一条互斥的「唯一」、`0048`↔`0058` 一个说「唯一最完整」另一个说「与它并列」、`0002`↔`0013` 事件数搞反、`0053`↔`0023` 与自己录进 `index.tsv` 的 extra 计数冲突。**这一步能拦住 9 条里的 6 条。**

### 引用式理由（「同 XXXX#N」）—— 必须解引用

写理由时可以引用另一条已写完的分析，但**归类与统计时不得把引用文本当作陈述来匹配**。引用只说「我的情况和那条一样」，它自己**不含**任何关于缺陷类型的信息。

上一轮的实际后果：30 条不可表述发现里有 5 条的缺口分析只写了「同 `0005`#3」。归类脚本把这串字面量写进了「过度指定」族的正则（因为它们在文件里恰好紧邻几条过度指定的条目），于是 5 条**动作类**缺口被记成了过度指定类。修正后最大缺口族从「缺过度指定判据」变成「缺动作内容谓词」——**结论的重心被一个字面匹配改掉了**。

两条要求：

1. **写的时候**，引用之后仍要补一句本条自己的缺口归属（「同 `0005`#3，属动作内容族」），不要只留引用。
2. **统计的时候**，必须解引用到被引条目的族，并对「引用了一条查不到的分析」显式报错而不是默默归入兜底族。互相引用要有深度上限，否则会死循环。

### 两个计数口径不得混比

同一批事实常有两种合法计数：**已发布条目数**与**去重后缺陷数**（多条 issue 可以描述同一个缺陷）。两者都对，但**分母属于哪个口径就必须用哪个口径的分子**。

上一轮的实际后果：8 格审计里 `hit = 20` 是已发布 issue 条数、`distinct_manual_defects_hit = 16` 是去重缺陷数，而应命中分母 `22` 是缺陷口径。用 `20 + 6 = 26` 去对 `22` 会得出「数据有错」的结论，实际两个数各自都对，错的是拿着 issue 口径的分子去对缺陷口径的分母。这类错误最危险的地方是：**它看起来像数据出了问题，于是下一步很容易去改数据。**

要求：凡在同一表格或同一句话里出现两个口径的数，必须显式标注各自口径；跨口径的加减必须先换算。

## 输出格式

对你负责的每个 pair，输出一个 JSON 对象（全部 pair 汇成一个 JSON 数组），字段：

```json
{
  "case": "0000",
  "group": "NL08",
  "llm": "GPT-4o",
  "diffs": [
    {"verdict": "problem", "ref": "human_mode --> [*] : power_off",
     "gen": "[*] --> FinalState : Power Off",
     "reason": "NL 第5句要求运行模式在断电时进入终态；生成模型唯一的 Power_Off 边从伪初始发出，任何运行态都无断电出边",
     "assertable": "occupancy_after(source=HumanDrivingMode, trigger=Power_Off, target=FinalState)",
     "predicate_exists": true, "out_of_scope": null}
  ],
  "problem_count": 3, "extra_count": 1,
  "vs_paper": "论文语法栏记 transition does not connect two state（已 resolved）；语义栏 None。我判的 3 个 problem 中 0 个被论文记录",
  "vs_ledger": "台帐有 EXP-0000-IT-001，对应我的第 1 条 problem",
  "notes": "自由文本，记录你对该 pair 的整体判断与任何存疑处"
}
```

同时输出一段**该组的总体分析**（自由文本）：这 6 个 LLM 在同一份 NL 上的表现差异、共性问题、参考模型本身的可疑处。
