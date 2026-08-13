# AA Intelligence Index v4.1.1：我们引用的分数中哪些是实测、哪些是估计

**核验日期**：2026-08-13 · **口径**：Artificial Analysis Intelligence Index **v4.1.1** · **数据源**：`artificialanalysis.ai` 官方页面内嵌 Next.js RSC flight payload（563 模型 × 134 字段），本轮**独立重新抓取并重新解析**，与前一轮缓存逐字段比对**零差异**。

## 0. 一句话结论（我们在用的分数里几条是估计值）

**清单 A–D 中被引用的 AA 总分，全部 0 条是估计值——逐条都是 AA 实测。** 具体：清单 A 的 5 条、清单 B 的 4 条总分、清单 C 的 18 行总分，共 **27 条 AA Index v4.1.1 总分全部为实测**（`intelligence_index_is_estimated = false`，且 9 项成分全部非空）。清单 B 的分维度数字（Opus 5 / Qwen3.6-27B / Muse Glimmer 各 9 项）也全部来自这三个模型的实测记录。

**但有三条必须单独标注的例外，它们都不是「估计值」而是别的问题**：

1. **`Nemotron Cascade 2 30B A3B` IFBench 80.4 与 `Grok 4.3 (medium)` IFBench 83.3**：这两个 IFBench 数值本身是 AA 跑出来的（payload 中为 80.41 / 83.33，非空），⛔ **但这两个模型的 AA Index 总分是估计值**（`is_estimated = true`，缺 $\tau^3$-Banking 等成分）。引用它们的 IFBench 分没问题，⛔ 但不得顺手引用它们的总分。
2. **`Muse Glimmer` IFBench 77.0 与 `Qwen3.6-27B` IFBench 70.8**：⛔ **这两个数不在 AA 数据里**——AA 对 Muse Glimmer 的 `ifbench` 字段为 **空**。[benchmark_open_weights.md](./benchmark_open_weights.md) §0 第 2 条已标明它们是「**M**，⛔ Meta 自报」，即**厂商自报**，既非 AA 实测也非 AA 估计。⛔ 不得与 AA 的 IFBench 数（如 67.6 / 80.4 / 83.3）放在同一列比较。⭐ **本轮顺带量出：该自报表在唯一两个能与 AA 对照的行上差 0.42 与 3.25 点，⛔ 超过它主张的 1.0 点领先，故「Glimmer 77.0 > Gemma 76.0」这个排序不稳**（详见 §2.D）。
3. **全部 IFBench 数值都不是 v4.1.1 口径**：IFBench 已在 **v4.1 因饱和被移出 Index**，权重 0%。实测覆盖边界：**447/563 个模型有 IFBench 分，其中最晚发布日恰为 2026-07-09，其后发布的 30 个模型一律为空**（已逐一确认 Opus 5 / Kimi K3 / Qwen3.8 Max / Grok 4.6 全无分）。故 IFBench 值是**真实测量但属 v4.0 时代**，与任何 v4.1.1 数字无版本对应关系。

**查不到的条目：0 条。** 清单 A–D 中每一个被点名的数字都在官方 payload 中定位到了对应字段（含「本应为空」的那几个，空值本身即为事实）。

## 1. 估计值的标注机制与判据（含 AA 自己怎么描述）

### 1.1 有机读字段，且它就是权威判据

payload 中有两个与估计相关的字段，另有一个承载实测值的字段：

| 字段 | 类型 | 非空数 | 含义 |
| :-- | :-- | --: | :-- |
| `intelligence_index_is_estimated` | **bool** | 563/563 | ⭐ **权威标志位**：`true` = 该模型的 Index 是估计值 |
| `intelligence_index_v4_1` | float | **149**/563 | v4.1.1 **实测**总分；`null` 即 AA 未完成实测 |
| `estimated_intelligence_index_v4_1` | float | 553/563 | 估计出来的总分 |
| `intelligence_index` | float | 561/563 | **页面显示值**：实测时取实测值，否则取估计值 |

分布：`is_estimated = true` 共 **412** 个，`false` 共 **151** 个（其中 2 个是 `Cogito v2.1 (Reasoning)` 与 `Mi:dm K 2.5 Pro Preview`，两者全部索引字段皆空、布尔位仅是默认 `false`，⛔ 不可当作实测）。**故真正的实测模型数是 149。**

### 1.2 三重一致性，机制是双条件的

本轮机械验证了三条恒等关系，全部零反例：

1. `is_estimated = false` 且有实测值的 149 个模型，其 `intelligence_index` 与 `intelligence_index_v4_1` **逐个完全相等**（0 处不符）。
2. `is_estimated = true` 的 412 个模型，其 `intelligence_index` 与 `estimated_intelligence_index_v4_1` **逐个完全相等**（0 处不符）。
3. ⭐ **双条件成立**：`is_estimated = false`（149 个）⟺ v4.1.1 的 **9 项成分全部非空**（149/149）；`is_estimated = true`（412 个）⟺ **至少缺 1 项成分**（412/412）。

第 3 条揭示了估计值的**产生原因**：不是 AA 随手推一个数，而是**该模型没跑完 v4.1.1 的完整评测套件**。缺失最集中的三项恰是 v4.1.1 新增的昂贵 agentic 项——412 个估计模型中，缺 `gdpval_v2` + `tau_banking` + `terminalbench_v2_1` 三项的有 **270** 个，另有 63 个再缺 `lcr` / `omniscience` / `critpt`，40 个只缺 `tau_banking`。反过来说，**便宜的核心项（HLE 412/412、GPQA 411/412、SciCode 409/412）在估计模型上基本都有真实分**——这也是下面 §2 里「模型总分是估计值、但某个分维度是实测」能同时成立的原因。

### 1.3 UI 的「(estimated)」标注就是这个布尔位渲染出来的

前端 JS bundle 中逐字如下（出现于 `_next/static/chunks/53161-*.js` 与 `58375-*.js` 两处，内容一致）：

```js
let n = { estimateIndependentEvaluationForthcoming: "Estimate (independent evaluation forthcoming)" }
...
s = { striped: n.I.estimateIndependentEvaluationForthcoming };
function i(e) { return e.intelligenceIndexIsEstimated ? "striped" : void 0 }
```

即：**柱状条渲染成 striped 当且仅当 `intelligenceIndexIsEstimated` 为真，而 striped 的图例文字就是 `Estimate (independent evaluation forthcoming)`。** 全站 JS 中 `IsEstimated` 一共只出现 4 次，全部是这一个字段；payload 中含 `estimat` 的字段也只有上表那两个。⭐ **结论：不存在第二套标注机制，机读字段与 UI 文字是同一个事实的两种呈现，判据完全确定。**

### 1.4 AA 自己对估计值产生方式的描述：⛔ 没有找到

AA 官方文字**只给出「(independent evaluation forthcoming)」这一句**，即「独立评测尚未进行」。逐字检索 [methodology/intelligence-benchmarking](https://artificialanalysis.ai/methodology/intelligence-benchmarking) 全文（609 KB，去标签后按 `stimat` / `forthcoming` / `interpolat` / `extrapolat` 四个词根穷举）**没有任何一段解释估计值如何算出**——命中的段落全部是别的意思（置信区间、Bradley-Terry 最大似然估计、GDPval Elo 归一化、token 成本估算）。⛔ **故「是插值还是按同族模型推」无官方答案，本文不猜。**

同一页给出的一条相关事实是 v4.1.1 的构成：逐字「**Artificial Analysis Intelligence Index v4.1.1 incorporates 9 evaluations: GDPval-AA v2, 𝜏³-Banking, Terminal-Bench v2.1, SciCode, AA-LCR, AA-Omniscience, Humanity's Last Exam, GPQA Diamond, CritPt**」，并称 Index 的 95% 置信区间小于 ±1%。⚠️ **这是 9 项，而 [h200x4_envelope.md](./h200x4_envelope.md) 更新日志记的是「官方十项权重」——该处措辞应更正为 9 项。** 本轮用这 9 项对 149 个实测模型最小二乘反解权重，得 `gdpval .206 / tau3-banking .148 / terminal-bench .155 / scicode .105 / aa-lcr .040 / omniscience .039 / hle .109 / gpqa .120 / critpt .051`，和为 **0.972**，平均绝对误差 **0.38 分**、最大 1.87 分（GDPval Elo 按官方 `clamp((Elo-500)/2000)` 归一）。⚠️ 该拟合只作版本佐证，⛔ 不作为判定依据——判定一律以 §1.1 的布尔位为准。

## 2. 逐条判定表

判定口径：**实测** = `intelligence_index_is_estimated = false` 且 `intelligence_index_v4_1` 非空（等价于 9 项成分齐全）；**估计** = 该布尔位为 `true`；**非 AA** = 该数字在 AA payload 中不存在。「payload 名」为 AA 官方模型名，与我们文档里的简称对应关系一并列出，因为**effort 档与 reasoning 变体不同则判定可能不同**（见 A.5 与 B.4 的注）。

### 2.A 候选模型表（[SUMMARY.md](./SUMMARY.md) §0b.1 与 [h200x4_envelope.md](./h200x4_envelope.md)）

| # | 我们写的 | 数字 | payload 名 | payload 值 | 判定 | 依据 |
| :-: | :-- | --: | :-- | --: | :-- | :-- |
| A.1 | `GLM-5.2` | **52.64** | `GLM-5.2 (max)` | 52.6383 | ⭐ **实测** | `is_estimated=false`，9 项齐 |
| A.2 | `DeepSeek V4-Flash-0731` | **51.77** | `DeepSeek V4 Flash 0731 (Reasoning, Max Effort)` | 51.7704 | ⭐ **实测** | 同上 |
| A.3 | `MiniMax M2.7` | **38.87** | `MiniMax-M2.7` | 38.8700 | ⭐ **实测** | 同上 |
| A.4 | `Claude Opus 5 (max)` | **63.05 / 63.1** | `Claude Opus 5 (Adaptive Reasoning, Max Effort)` | 63.0532 | ⭐ **实测** | 同上；63.1 是 63.05 的一位小数舍入，同一条记录 |
| A.5 | `Qwen3.6-27B` | **37.70** | `Qwen3.6 27B (Reasoning)` | 37.7025 | ⭐ **实测** | 同上 |

⚠️ **A.5 的档位注意**：`Qwen3.6 27B` 在 AA 有两个变体，**(Reasoning) 37.70 与 (Non-reasoning) 31.33，两者皆为实测**。我们引用的 37.70 对应 Reasoning 档，与 [benchmark_landscape.md](./benchmark_landscape.md) §5 的表述一致。⚠️ 同理 A.1 的 `GLM-5.2` 也有 `(Non-reasoning) 34.81`（亦实测），而 `GLM-5.1 (Non-reasoning) 36.26` 与 `GLM-5 (Reasoning) 40.55` 则**是估计值**——⛔ 引 GLM 系时必须写明档位，否则会跨实测/估计边界。

### 2.B 差距结构表（[benchmark_landscape.md](./benchmark_landscape.md) §5 与 [SUMMARY.md](./SUMMARY.md) §7）

**B-1：四条总分**

| # | 我们写的 | 数字 | payload 名 | payload 值 | 判定 |
| :-: | :-- | --: | :-- | --: | :-- |
| B.1 | `Kimi K3 (max)` | **59.7** | `Kimi K3 (max)` | 59.6995 | ⭐ **实测** |
| B.2 | `Muse Glimmer (high)` | **35.1** | `Muse Glimmer (high)` | 35.0642 | ⭐ **实测** |
| B.3 | `Gemma 4 31B` | 29.7 | `Gemma 4 31B (Reasoning)` | 29.6900 | ⭐ **实测** |
| B.4 | `Gemma 4 26B A4B` | 26.1 | `Gemma 4 26B A4B (Reasoning)` | 26.0700 | ⭐ **实测** |

⚠️ **B.4 的档位是硬约束**：`Gemma 4 26B A4B` 的 **(Reasoning) 26.07 是实测，而 (Non-reasoning) 20.38 是估计值**。我们引的 26.1 落在实测那一档，但表里没写档位——⛔ **建议补「(Reasoning)」**。⚠️ Gemma 4 系其余全部为估计值（12B 两档、E2B 两档、E4B 两档共 6 条），⛔ 不得引用。

**B-2：分维度（三个模型，各 9 项 v4.1.1 成分 + IFBench）**

⭐ **下表三个模型的 `is_estimated` 全部为 `false`、9 项成分全部非空，故 9 项分维度值逐个都是 AA 实测。** 括号内为 payload 原始值（成绩为 0–1 分数者已 ×100，GDPval 为原始 Elo，Omni 为净分）。

| 分维度 | payload 字段 | `Opus 5 (max)` | `Qwen3.6-27B (Reasoning)` | `Muse Glimmer (high)` | 判定 |
| :-- | :-- | --: | --: | --: | :-- |
| AA Index v4.1.1 | `intelligence_index_v4_1` | **63.05** | **37.70** | **35.06** | ⭐ 实测 |
| AA-LCR | `lcr` | **75.67**（文档 75.7） | 73.33 | 80.00 | ⭐ 实测 |
| HLE | `hle` | **54.87**（文档 54.9） | 23.08 | 21.96 | ⭐ 实测 |
| GPQA Diamond | `gpqa` | **93.23**（文档 93.2） | 84.24 | 83.54 | ⭐ 实测 |
| SciCode | `scicode` | **55.67**（文档 55.7） | 39.81 | 43.63 | ⭐ 实测 |
| Terminal-Bench v2.1 | `terminalbench_v2_1` | **89.14**（文档 89.1） | 60.67 | 51.69 | ⭐ 实测 |
| CritPt | `critpt` | **29.14**（文档 29.1） | 1.14 | 2.57 | ⭐ 实测 |
| $\tau^3$-Banking | `tau_banking` | **42.06**（文档 42.1） | 16.70 | 23.51 | ⭐ 实测 |
| GDPval-AA v2 Elo | `gdpval_v2` | **1848.77**（文档 1849） | 1139.96 | 953.00 | ⭐ 实测 |
| AA-Omniscience 净 | `omniscience` | **+37.07**（文档 +37.1） | −20.02 | −32.85 | ⭐ 实测 |
| IFBench | `ifbench` | ⛔ **空** | 67.55（文档 67.6） | ⛔ **空** | 见下 |

⭐ **§5 表里 Opus 5 与 Muse Glimmer 的 IFBench 写「未测」是正确的**——payload 中确为空。⚠️ **但 `Muse Glimmer` 的 77.0（[benchmark_open_weights.md](./benchmark_open_weights.md) §0/§249/§368）与 §5 的「未测」是同一模型的两种说法**，前者是 Meta 自报、后者是 AA 未跑，两处都对但**必须写明出处不同**，否则读者会以为其中一处错了。

### 2.C 闭源前沿刻度表（[benchmark_landscape.md](./benchmark_landscape.md) §7，18 行逐行）

⭐ **18 行的 AA Index 总分全部为实测，零条估计值**——该表标题写的「AA 独立实测 v4.1.1 口径」经机械核验**成立**。

| # | 我们写的 | 文档值 | payload 名 | payload 值 | 判定 |
| :-: | :-- | --: | :-- | --: | :-- |
| C.1 | Grok 4.6 (high) | **60.9** | `Grok 4.6 (high)` | 60.92 | ⭐ 实测 |
| C.2 | Muse Spark 1.2 (xhigh) | **56.8** | `Muse Spark 1.2 (xhigh)` | 56.76 | ⭐ 实测 |
| C.3 | Qwen3.8 Max | **58.1** | `Qwen3.8 Max` | 58.08 | ⭐ 实测 |
| C.4 | Claude Opus 5 (max) | **63.1** | `Claude Opus 5 (Adaptive Reasoning, Max Effort)` | 63.05 | ⭐ 实测 |
| C.5 | Gemini 3.6 Flash | 51.6 | `Gemini 3.6 Flash (high)` | 51.58 | ⭐ 实测 |
| C.6 | GPT-5.6 Sol (max) | **60.9** | `GPT-5.6 Sol (max)` | 60.93 | ⭐ 实测 |
| C.7 | GPT-5.6 Terra (max) | 56.6 | `GPT-5.6 Terra (max)` | 56.58 | ⭐ 实测 |
| C.8 | GPT-5.6 Luna (max) | 52.3 | `GPT-5.6 Luna (max)` | 52.32 | ⭐ 实测 |
| C.9 | Muse Spark 1.1 (xhigh) | 53.2 | `Muse Spark 1.1 (xhigh)` | 53.20 | ⭐ 实测 |
| C.10 | Grok 4.5 (high) | 55.8 | `Grok 4.5 (high)` | 55.76 | ⭐ 实测 |
| C.11 | Claude Sonnet 5 (max) | 55.3 | `Claude Sonnet 5 (Adaptive Reasoning, Max Effort)` | 55.26 | ⭐ 实测 |
| C.12 | Claude Fable 5 | **62.1** | `Claude Fable 5 (Adaptive Reasoning, Max Effort, Opus 4.8 Fallback)` | 62.07 | ⭐ 实测 |
| C.13 | Claude Opus 4.8 (max) | 57.3 | `Claude Opus 4.8 (Adaptive Reasoning, Max Effort)` | 57.33 | ⭐ 实测 |
| C.14 | Gemini 3.5 Flash | 52.0 | `Gemini 3.5 Flash (high)` | 51.96 | ⭐ 实测 |
| C.15 | GPT-5.5 (xhigh) | 56.3 | `GPT-5.5 (xhigh)` | 56.31 | ⭐ 实测 |
| C.16 | Claude Opus 4.7 (max) | 55.0 | `Claude Opus 4.7 (Adaptive Reasoning, Max Effort)` | 54.96 | ⭐ 实测 |
| C.17 | GPT-5.4 (xhigh) | 53.1 | `GPT-5.4 (xhigh)` | 53.12 | ⭐ 实测 |
| C.18 | Gemini 3.1 Pro Preview | **47.7** | `Gemini 3.1 Pro Preview` | 47.74 | ⭐ 实测 |

⚠️ **两条命名对应关系需在表中补明，否则复算者会对不上**：① 我们写的 `Gemini 3.6 Flash` / `Gemini 3.5 Flash` 在 AA 是 **`(high)` 档**——⛔ 而 `Gemini 3.5 Flash` 的 `(minimal)` 与 `(medium)` 两档**是估计值**，故省略档位有跨界风险。② 我们写的 `Claude Opus 4.7 (max)` 对应 `(Adaptive Reasoning, Max Effort)` 实测 54.96，⛔ 而同名模型的 `(Non-reasoning, High Effort)` 档**是估计值**。

### 2.D 其它分维度引用

| # | 我们写的 | 数字 | payload 字段与值 | 该模型总分是否实测 | 判定 |
| :-: | :-- | --: | :-- | :-- | :-- |
| D.1 | `MiniMax M3` AA-LCR | **80.3** | `lcr` = 80.33 | ⭐ 是（45.40 实测） | ⭐ **AA 实测** |
| D.2 | `Muse Spark 1.2` AA-LCR | **83.3** | `lcr` = 83.33 | ⭐ 是（56.76 实测） | ⭐ **AA 实测**（全库 `lcr` 最高值） |
| D.3 | `Nemotron Cascade 2 30B A3B` IFBench | **80.4** | `ifbench` = 80.41 | ⛔ **否，总分是估计值** | ⚠️ **IFBench 为 AA 实测，⛔ 但总分不可引** |
| D.4 | `Grok 4.3 (medium)` IFBench | **83.3** | `ifbench` = 83.33 | ⛔ **否，总分是估计值** | ⚠️ **IFBench 为 AA 实测，⛔ 但总分不可引** |
| D.5 | `Qwen3.6-27B` IFBench | **67.6** | `ifbench` = 67.55 | ⭐ 是（37.70 实测） | ⭐ **AA 实测** |
| D.6 | `Qwen3.6-27B` IFBench | **70.8** | ⛔ AA 无此值 | — | ⛔ **非 AA（厂商自报）** |
| D.7 | `Muse Glimmer` IFBench | **77.0** | ⛔ `ifbench` = **空** | ⭐ 总分 35.06 实测 | ⛔ **非 AA（Meta 自报）** |

⛔⛔ **D.3 / D.4 是本轮最需要留意的一处**：[benchmark_landscape.md](./benchmark_landscape.md) §4 里「IFBench 参考值：前沿最高 **Grok 4.3 (medium) 83.3%**；≤32B 开放权重最高 **Nemotron Cascade 2 30B A3B 80.4%**——只差 2.9 个百分点（≈0.97）」这句里的**两个 IFBench 数都是 AA 真跑的，比值 0.97 站得住**；⛔ 但这两个模型的 **AA Index 总分都是估计值**，故⛔ **不得在同一段里顺势引用它们的总分做对照**。补充事实：`Grok 4.3` 的 `(high)` 档总分 37.95 **是实测**、IFBench 81.29，而我们引的 `(medium)` 档总分为估计值——⛔ **同一模型两档一实一估，档位不可省。**

⭐ **D.6 / D.7 顺带量出一条新事实：Meta 自报的 IFBench 与 AA 实测在可对照处差到 3.25 点，而 Meta 主张的领先只有 1.0 点。** [benchmark_open_weights.md](./benchmark_open_weights.md) §249 的三模型对照表本身**标注清楚是「Meta 报」，同源排序无误**，我此前的混排质疑不成立。⛔ **但把这三个自报值与 AA 实测并置后，可检验的两项都对不上**：

| 模型 | Meta 自报 IFBench | AA 实测 IFBench | 差 |
| :-- | --: | --: | --: |
| `Muse Glimmer-30B`（Meta 自家） | **77.0** | ⛔ **AA 从未跑** | ⛔ **无法对照** |
| `Gemma4-31B` | 76.0 | 75.58 | 0.42 |
| `Qwen3.6-27B` | 70.8 | **67.55** | ⛔ **3.25** |

⛔⛔ **结论：`benchmark_open_weights.md` §0 第 2 条「`Muse Glimmer 30B` 77.0 > `Gemma4-31B` 76.0」这个排序不稳。** 它主张的领先幅度是 **1.0 点**，⛔ 而同一张自报表在**唯一能与 AA 对照的两行上偏差达 0.42 与 3.25 点**——⛔ **偏差量级超过主张的领先量级，且偏差最大的那一行恰是被比较的对手，而 Meta 自家模型这一项 AA 根本没跑、无从校准。** 建议该结论降级为「⏳ 自报口径下 Meta 称领先 1.0 点，⛔ AA 未跑其自家模型故不可独立核验」。⚠️ 对照：同表的 **AA-LCR 行三值（80.0 / 68.3 / 73.3）与 AA 实测（80.00 / 68.33 / 73.33）逐个吻合**，故不能把 IFBench 的偏差推广成「Meta 全表都不可信」——**只有 IFBench 这一行有问题。**

## 3. 受影响的本项目结论（哪些表要加标注）

⭐ **首要结论：没有任何一条已发表的能力判断需要因「用了估计值」而撤回或修改。** [SUMMARY.md](./SUMMARY.md) §137 里那条预警——「§0b.1 与 §7 里引用的 AA 分数须逐条回查是否为实测，⛔ 未查明前不得当实测引用」——**现已查明，结果是全部实测**，该预警可以解除（改写为「已于 2026-08-13 逐条核验，27 条总分全为实测，判据为 `intelligence_index_is_estimated = false`」）。

需要**加标注**而非改数字的地方，按优先级：

| # | 文件与位置 | 该改什么 | 为什么 |
| :-: | :-- | :-- | :-- |
| 1 | [benchmark_landscape.md](./benchmark_landscape.md) §4 「IFBench 参考值」段 | 给 `Grok 4.3 (medium)` 与 `Nemotron Cascade 2 30B A3B` 各加一句「⛔ 该模型 AA Index 总分为估计值，本处只引其 IFBench 实测分」 | ⛔ 这是全库中**唯一**引用了「总分为估计值」模型的两处；⛔ 不加标注后人极易顺手去取其总分 |
| 2 | [benchmark_open_weights.md](./benchmark_open_weights.md) §0 第 2 条 · §249 IFBench 行 · §368 | 把「`Muse Glimmer 30B` 77.0 最高」降级为 ⏳ 不可独立核验，并补上 AA 实测对照（Gemma 75.58 / Qwen 67.55 / Glimmer 未跑） | ⛔ 自报偏差（3.25）大于主张领先（1.0），⛔ 且 Meta 自家那一项 AA 未跑、无从校准 |
| 3 | [benchmark_landscape.md](./benchmark_landscape.md) §5 表 · §7 表 | 补 effort / reasoning 档位：`Gemma 4 26B A4B` → `(Reasoning)`；`Gemini 3.6/3.5 Flash` → `(high)`；`Claude Opus 4.7 (max)` → `(Adaptive Reasoning, Max Effort)` | ⛔ 这些模型的**另一档是估计值**，省略档位会让复算者取到估计值并以为我们引错 |
| 4 | [h200x4_envelope.md](./h200x4_envelope.md) 更新日志「官方十项权重」 | 改为 **9 项** | 官方 methodology 逐字写「incorporates **9** evaluations」 |
| 5 | 本目录所有引 AA 分数处 | 统一加一句机读判据说明：**实测 ⟺ `intelligence_index_is_estimated = false`** | ⭐ 让后续任何人可在 30 秒内自查，⛔ 不必再依赖「页面顶部裸数字」这条不可靠路径 |

⚠️ **一条口径澄清，避免把两个不同的「26 条估计值」混谈**：[open_weights_2025.md](./open_weights_2025.md) §0 第 1 条与 §212 第 3 条说的「38 条里 26 条是估计值」是**关于该文件自己那张 2025 世代表**的统计，⛔ **不是关于本目录全部 AA 引用的统计**。这两个集合几乎不重叠：2025 世代表里的估计值集中在 DeepSeek V3.x 全系、Nemotron 全系、MiniMax M2/M2.1/M2.5、旧 Kimi 等**较早模型**；而 §0b.1 / §5 / §7 引用的是 **2026 年的前沿与候选模型，AA 已跑完整套件**。⛔ **故不得由「26/38 是估计值」推出「我们的候选模型表也有估计值」——这是不同分母下的比率误读**（参见 CLAUDE.md 关于比率只能跨同类分母比的口径）。

⭐ **一条正面的方法学收获**：既然存在机读布尔位，后续**不必再靠读页面顶部数字或 FAQ 文字来判断实测/估计**。⛔ 原先记录的陷阱「页面顶部 summary 卡片写裸数字、只有 FAQ 才写 `(estimated)`」依然成立（它描述的是**人工读页**的失效模式），⭐ 但已被 §4 的取数路径彻底绕过——**payload 里两者是同一个字段，不存在读漏的可能**。

## 4. 方法与入口（可复算）

**入口**：任一 AA 评测页的 HTML 内嵌完整数据集，本轮用 [artificialanalysis.ai/evaluations/humanitys-last-exam](https://artificialanalysis.ai/evaluations/humanitys-last-exam)（10.6 MB）。⛔ **WebFetch 会因超 10 MB 上限失败，必须 `curl`。** ⛔ 官方 REST `GET /api/v2/data/llms/models` 返回 **HTTP 401 `{"error":"API key is required"}`**，故走页面内嵌路径；⭐ 这仍是官方站点自己的数据，不是镜像。

**步骤一：取页**

```bash
curl -sL --compressed -m 240 \
  -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36' \
  'https://artificialanalysis.ai/evaluations/humanitys-last-exam' -o fresh_aa.html
```

**步骤二：重建 RSC flight payload 并切出模型数组**。数据被切成 **99 段** `self.__next_f.push([1,"<escaped>"])`，需先把每段的 JSON 字符串解转义再拼接（拼出 9,522,767 字符），然后用括号配对扫描切出那个含 `intelligence_index_is_estimated` 的数组。本轮所用脚本为 `/tmp/aa_parse.py`，核心是：

```python
chunks = re.findall(r'self\.__next_f\.push\(\[1,\s*("(?:[^"\\]|\\.)*")\]\)', html)
flight = ''.join(json.loads(c) for c in chunks)   # 99 段 → 9.52 M 字符
# 从首个 marker 向前找 '[', 再做 string-aware 括号配对扫描，取出 563 元素数组
```

产出：**563 条记录 × 134 字段**，marker 在 flight 中出现 **563 次**（每模型恰一次）。

**步骤三：判定**。单条判定就是读一个布尔位：

```python
verdict = '估计' if m['intelligence_index_is_estimated'] else '实测'
# 交叉校验：实测 ⟺ m['intelligence_index_v4_1'] is not None
#           ⟺ 9 项成分 gdpval_v2/tau_banking/terminalbench_v2_1/scicode/
#              lcr/omniscience/hle/gpqa/critpt 全部非空
```

**步骤四：UI 侧佐证**（确认布尔位就是「(estimated)」的来源）：

```bash
grep -o '/_next/static/chunks/[a-zA-Z0-9._/-]*\.js' fresh_aa.html | sort -u > js.list   # 64 个
while read u; do curl -sL "https://artificialanalysis.ai$u" -o "aajs/$(echo $u|tr / _)"; done < js.list
grep -ho 'Estimate ([^)]*)' aajs/*        # → Estimate (independent evaluation forthcoming)
grep -ho '[A-Za-z]*IsEstimated' aajs/*    # → intelligenceIndexIsEstimated ×4，无其他
```

**新鲜度与自洽性检查**（本轮全部通过）：① 新抓 payload 与 12:40 的缓存 `/tmp/aa_models.json` 在 `intelligence_index_is_estimated` / `intelligence_index` / `intelligence_index_v4_1` 三字段上 **563 条逐条零差异**，id 集合完全相同；② 实测/估计计数 149 / 412 两次一致；③ 9 项权重反解误差 0.38 分，反证版本为 v4.1.1；④ IFBench 覆盖边界（447 个有分、最晚发布日 2026-07-09、其后 30 个全空）与 [h200x4_envelope.md](./h200x4_envelope.md) 既有记录逐字吻合。

⚠️ **单位口径**：payload 中 `hle` / `gpqa` / `scicode` / `lcr` / `terminalbench_v2_1` / `critpt` / `tau_banking` / `ifbench` 为 **0–1 小数**（乘 100 得文档中的百分数）；`gdpval_v2` 是**原始 Elo**（范围 −121.83 至 1848.77）；`omniscience` 是**净分**（−77.07 至 43.30，可为负）。⛔ 直接把它们混在一起做最小二乘会得到荒谬权重。

## 5. 查不到的条目

**清单 A–D 中查不到的条目：0 条。** 逐项清点：**27 条总分**（A 5 + B-1 4 + C 18）＋ **34 个分维度值**（B-2 的 3 模型 × 9 项 = 27，B-2 的 IFBench 列 3，D.1–D.4 另 4 项）全部在官方 payload 中定位到对应字段并给出判定。其中：

- **32 个分维度值非空且为 AA 实测**。
- **2 处为「字段存在但值为空」**：`Opus 5 (max)` 与 `Muse Glimmer (high)` 的 `ifbench`。⭐ **空值本身即为已核实的事实（AA 未跑该项），不属查不到**——且它与 [benchmark_landscape.md](./benchmark_landscape.md) §5 写的「未测」一致。
- **2 处判定为「非 AA」**：D.6 的 70.8 与 D.7 的 77.0，均为厂商自报，⛔ AA 数据中无对应值（不是「查不到」，是**本来就不在这个来源里**）。
- D.5 的 `Qwen3.6-27B` IFBench 67.6 与 B-2 的 IFBench 列同为一个字段，未重复计数。

以下三项**属于本轮未能查明，但都不影响任何逐条判定**：

| # | 未查明的 | 状态 | 影响 |
| :-: | :-- | :-- | :-- |
| 1 | ⛔ **AA 估计值的具体算法**（是插值？按同族模型外推？按已有成分回归？） | ⛔ **官方无任何说明**。methodology 页按四个词根穷举检索无果，唯一官方措辞只有「(independent evaluation forthcoming)」 | ⛔ 无影响——我们引用的 27 条**全部是实测**，不依赖估计算法的可信度。⚠️ 但若日后要引用任何估计值，⛔ **必须先解决这一项** |
| 2 | ⏳ 9 项权重的**官方精确数值** | 官方只列出 9 个评测名，⛔ 未公布权重表；本轮最小二乘反解得和为 0.972、误差 0.38 分，⚠️ 属**近似**而非官方值 | ⛔ 无影响——判定只读布尔位，⛔ 不依赖权重 |
| 3 | ⏳ **分维度是否也存在估计** | payload 中**只有 index 级布尔位，无任何 per-eval 估计标志**（全站 JS 中 `IsEstimated` 仅 4 次、全指同一字段）。观察到的模式是「未跑即为 `null`」而非填入推算值 | ⚠️ 故「非空分维度值 = AA 实测」是**基于该模式的强推论，而非机读事实**。⛔ 对 D.3 / D.4 两条（总分估计、IFBench 非空）应保留这一层不确定性 |

⚠️ 另有一项**不是查不到、而是已确认为空**，单独记以免误读：`Grok 4.3 (medium)` 缺 `terminalbench_v2_1` / `tau_banking` / `gdpval_v2` 三项，⭐ **这正是它的总分被判为估计值的机制原因**（§1.2 第 3 条）。

## 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-13 | 建档。⭐ **找到机读判据 `intelligence_index_is_estimated`（bool），并逐字证明它就是 UI「Estimate (independent evaluation forthcoming)」striped 标注的唯一来源**——故判定完全确定，⛔ 不再依赖读页面顶部数字。⭐ **逐条判定清单 A–D 共 27 条总分 + 30 个分维度值，估计值 0 条、查不到 0 条**，[SUMMARY.md](./SUMMARY.md) §137 的回查预警可解除。⭐ **机制查明是双条件的**：实测（149）⟺ 9 项成分齐全，估计（412）⟺ 至少缺 1 项，⛔ 缺的集中在 v4.1.1 新增的三项昂贵 agentic 评测（270/412 恰缺这三项）。⛔ **三条必须标注的例外**：① `Nemotron Cascade 2 30B A3B` 与 `Grok 4.3 (medium)` 的 IFBench 是实测但**总分为估计值**；② `Muse Glimmer` 77.0 / `Qwen3.6-27B` 70.8 是**厂商自报、不在 AA 数据里**；③ 全部 IFBench 值属 **v4.0 时代**（v4.1 已移出 Index，447 个有分、最晚发布日 2026-07-09）。⭐ **新量出一条**：Meta 自报 IFBench 与 AA 实测在可对照两行差 0.42 与 3.25 点，⛔ **超过其主张的 1.0 点领先**，故「Glimmer 77.0 最高」排序不稳；⚠️ 而同表 AA-LCR 三值与 AA 实测逐个吻合，⛔ 不可推广成全表不可信。⛔ **两处待更正**：官方 methodology 逐字为 **9 项**评测（[h200x4_envelope.md](./h200x4_envelope.md) 日志误记「十项权重」）；§5/§7 多处缺 effort/reasoning 档位而**另一档恰为估计值**。⛔ **AA 估计值的算法官方零说明**，四词根穷举检索无果，⛔ 本文不猜 |
