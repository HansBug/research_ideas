# X1 朴素基线对照臂 · 事前登记

> ⏰ **本文件必须在跑格之前 push 到远端。** 按仓库根 [CLAUDE.md](../../../CLAUDE.md) §3.5.1：事前登记的**全部价值来自「它写在看到结果之前」**，⛔ 而这一点只有远端时间戳能证明。写完放在本地等于把是否作弊的判断交给作者自述。
>
> **代次标识**：`x1-baseline-v1`　**登记时间**：2026-08-12　**分支**：`paper1/x1-naive-baseline-arm`
>
> ⛔ **本登记一旦 push，第 1–7 节不得修改。** 若跑后发现某项需要改，正确处置是**开新代次**（`x1-baseline-v2`）并在新登记里说明为什么，⛔ 不是就地改本文件。第 8 节（工具适用性）与第 9 节（已知不对称）允许在**跑后**追加新发现的项，但⛔ 不得删改已有项。

---

## 1. 要回答什么

**同样两个执行模型、同样 54 个 pair、同样 3 轮，不走八阶段循环，一个提示直接让它列出模型相对需求的不符之处，在那 98 条台账记录上是多少？**

⛔ **没有这个数，$\mathrm{hit@1} \le 355/588 = 60.4\%$ 没有参照系。** 这是它存在的唯一理由。

**待并排的主臂三个数**（v46，⛔ 一位不动）：

| 口径 | 主臂 v46 | 单位 |
| :-- | :-- | :-- |
| `hit@1` | $355/588 = 60.4\%$ | 判定位（条目 × 臂 × 轮） |
| `hit@3` | $139/196 = 70.9\%$ | (条目, 臂) 单元 |
| `hit@all` | $95/196 = 48.5\%$ | 同上 |

---

## 2. 网格与输入（跑前定死）

| 项 | 值 |
| :-- | :-- |
| pair | **54**（60 减 `00x8` 六个；判据 [nl_scope_rule.md](../discover_matrix/docs/protocol/nl_scope_rule.md)，只读 `nl.txt`、与运行结果无关） |
| 执行模型 | `gpt-5.5` + `claude-opus-4-7`，⛔ **与主臂 v46 完全相同**，⛔ 不降级 |
| 轮次 | 3 |
| 格数 | $54 \times 2 \times 3 = \mathbf{324}$ |
| 输入 | `pairs/<case>/nl.txt` + `pairs/<case>/plantuml.puml`，⭐ **全文、未截断**（record 里存 sha256 与字符数，`truncated: false`） |
| 采样参数 | ⛔ **不显式设置**，用 profile 默认——与主臂同配置（record 里存 `max_output_tokens_override: null` / `temperature_override: null`） |
| 并发 | 16 |
| 产出落点 | `runs/paper1/x1-baseline-v1/run{N}/{case}-{arm}/record.json`（⚠️ `runs/` 被 gitignore；判定表与报告入库） |

⚠️ **12 个 pair 在台账里有 0 条记录**（`0001` `0003` `0011` `0017` `0021` `0022` `0023` `0031` `0041` `0051` `0052` `0054`）。⭐ **它们照样跑**：它们对 `hit@1` 分母贡献 0，但对**多报侧**贡献。⛔ 为省成本跳过它们会使两臂的多报侧分母不同类。

---

## 3. 基线 prompt：全文与冻结证据

**真源**：[prompt/naive_v1.txt](./prompt/naive_v1.txt)，`sha256 = 17e5067b44442ba07fadeb26ed3612ba21bf762c9bde10b3cb162139817fc2d9`。

```
You are an experienced control-systems engineer reviewing a state machine model against the natural-language specification it was built from.

You are given two things, both complete and unmodified:
  1. The natural-language specification.
  2. A state machine model written in PlantUML.

Your task: identify the places where the model does not conform to the specification. Read the specification in full first, then read the model in full, then report what you find.

Report as many or as few issues as you actually find, and organize them however you judge best. For each issue, state what the non-conformance is, which part of the model it concerns, and why you consider it a non-conformance.

Write your findings in {content_language}. Return only the requested structured response.
```

**输出契约**：[src/schema.py](./src/schema.py) —— `issues: [{issue, where, reason}]` 三个自由文本字段 + 可选 `analysis`。⛔ 无枚举、⛔ 无 validator、⛔ 无谓词措辞。

### 3.1 ⛔ prompt 已冻结，且冻结时刻可核验

⚠️ **2026-08-11 20:53 UTC 在 pair 0000 上跑过两格真实 smoke，产出已被查看。** 从那一刻起改 prompt 就等于「按结果调 prompt」，属 §3.5 条款 4「评测口径迁就结果」的同类问题。

⭐ **冻结证据**：[results/smoke/](./results/smoke/) 下两份 record 的 `prompt_sha256` 与上面那个哈希逐字符一致；正式网格每一格的 record 里也有这个字段。⛔ **若正式网格任一格的 `prompt_sha256` 与它不同，该次运行作废。**

⚠️ **必须如实记下 smoke 看到了什么**（否则这条冻结声明不完整）：两个模型在 pair 0000 上都报出了 `[*] --> FinalState : Power Off` 的源端错误，即台账 `EIS-0000-01` 所述的那处缺陷。⭐ **基线在这一格上命中了。** 这个观察⛔ **没有**、也⛔ **不得**用于调整 prompt。

---

## 4. 判定预算：**全量 588 位**（三条路径中选定这一条）

[next_round.md](../experiment_design/next_round.md) §B1 给了三条减负路径，⛔ 必须选定一条。**选定：全量判定。**

| 路径 | 取舍 |
| :-- | :-- |
| ⭐ **全量 588 位** | **选定。** 三口径完整，与主臂逐位同分母 |
| ⛔ 缩网格（1 轮或子集 pair） | 失去 `@k` 三口径——而 X1 的全部价值就是与主臂**同口径**并排，丢了 `@k` 对照就不完整 |
| ⛔ 分层复用 `verdict_tiers.py` A/B 层 | **结构性不可用**，见 §8.1 |

### 4.1 判定的组织方式：**按 pair 分层，pair 内判全 6 格**

⭐ 同一个 pair 的 6 格（3 轮 × 2 模型）共享同一份台账条目、同一份 NL、同一份 PlantUML。最贵的认知成本在「理解这个 pair 的台账条目要求什么、模型长什么样」——那是**每 pair 一次**的成本。

三个收益叠加：

1. 上下文载入 **42 次**（有台账条目的 pair 数）而非 324 次
2. ⭐ **横向一致性天然更好**：同一 pair 的 6 格在同一上下文里判完，判据严格度不会在格之间漂移——这直接服务「同判定者、横向对齐」要求。按格打散反而是不一致的来源
3. fallback 代表性照旧（见 §4.3）

### 4.2 判定者与判据

| 项 | 值 |
| :-- | :-- |
| 判定者 | ⭐ **与 v46 那轮同一判定者**（本会话的 AI agent，在用户口径下逐位做），⛔ 不换人、⛔ 不用脚本代劳 |
| 判据 | [hit_criterion.md](../discover_matrix/docs/protocol/hit_criterion.md) + [verdict_methodology.md](../discover_matrix/docs/protocol/verdict_methodology.md)，⛔ **一字不改** |
| 判定表格式 | 格式 A：键 `"<record_id>\|run<N>/<pair>-<arm>"`，值 `{hit, equivalence_form, argument}` |
| `equivalence_form` 闭集 | `直接对应` / `合取项之一` / `负向命题的正向对偶` / `蕴含更根本的原因`。⛔ **`hit=true` 时必填**，且 `argument` ≥ 20 字 |
| 缺位表示 | ⛔ **不允许**用字段表示未判——未判就是键不存在，且它是硬错误。⚠️ 格未落盘/失败的位用 `null`（⛔ 不是 0：把 null 读成 0 会让分母虚高而分子不变，即无声压低命中率） |
| 读哪份制品 | ⭐ `plantuml.puml`（作者源）。⛔ 不读 `model.fcstm`——否则会把编译债务当成模型缺陷（主臂八组栽七组） |
| 机械代理边界 | ⭐ 脚本**只许并列呈现与定位**，⛔ 裁定必须人工读原文 |

⚠️ **`EIS-0047-03` 的口径裁定**：主臂因一条「引入动机剔除」规则（[conditional_activation.md](../discover_matrix/docs/protocol/rules/conditional_activation.md)）在某一位上「认定应为命中但保持不计入」。⭐ **X1 侧照旧判它的 6 位、照旧计入**——分母必须与主臂完全同一 98 条。⚠️ **后果必须披露**：主臂在该位被自己的规则低估了 1 位，方向是**压低 Δ**（对我方不利），记入 §9。

### 4.3 ⛔ fallback：判定到 T+14h 未完成

⛔ **不许压掉 R1。** 处置：

1. 交**已判完的子集** + 明确的未判余量，完整数字推到 R2 之后
2. ⭐ **子集选法在此写死**：按**四池分层交错**的 pair 顺序推进（池定义见 §4.4），⛔ 不许按「问题最明显」挑。⭐ 这使封存零成本——任何时刻停下，已判子集自动分层代表
3. 未判位一律记 `null`，⛔ 不记 0
4. 报告必须写明：已判 N 位 / 共 588 位，以及已判子集的四池构成

### 4.4 四池（判定顺序的分层依据）

单位是**记录**，满分 6 = 2 臂 × 3 轮。⚠️ 与 `hit@3`/`hit@all` 的单位（196 个 `(记录, 臂)` 单元）不同，⛔ 不得混比。

| 池 | 条数 | 含义 |
| :-- | --: | :-- |
| 满格 6/6 | 37 | 主臂能力已覆盖且稳定 |
| 近满格 5/6 | 13 | 基本覆盖 |
| 不稳定 1–4/6 | 25 | 能力够、稳定性不足 |
| 零命中 0/6 | 23 | 主臂能力缺口 |
| **合计** | **98** | ✅ |

⚠️ **这是主臂的池划分**，用途仅限**排判定顺序**。⛔ 不得据它预期 X1 在某池的表现，也⛔ 不得在判定时让判定者看到某条属于哪个池——那会锚定判定（判定材料的三条禁止见 §8.5）。

---

## 5. 达标档位与可归因阈值

### 5.1 ⛔ 可归因阈值：2.0pp

⚠️ v46 的逐轮 `hit@1` 极差是 **2.0pp**（59.2 / 60.7 / 61.2）。⛔ **任何小于这个量级的臂间差异都不可归因。**

⚠️ **这把尺子的局限必须显式承认**：那 2.0pp **不是方差估计**——$n = 3$、未计需求族聚类。它是一个**代次内极差**，只能当噪声底的粗略下界用。⛔ 不得把「差异大于 2.0pp」表述为统计显著。

### 5.2 ⛔ Δ 的显著性在本仓库工具口径下不可断言

`metrics_at_k.ratio_gate(inferential=True)` 要求独立 NL 簇 $\ge 10$。⚠️ **本语料 `REPORTABLE` 只覆盖 8 个 NL 组**（NL01/03/05/06/07/08/09/10）。

⛔ **所以：只报描述性比率与逐条序列，不报显著性。** 措辞上限是「在本语料上观察到 Δ = X pp」，⛔ 不得写「显著优于」。

### 5.3 事前登记的档位（⛔ 跑后不得改）

⭐ **本节登记的是「什么结果算什么」，⛔ 不是「希望得到什么」。**

| Δ = 主臂 `hit@1` − X1 `hit@1` | 读法 |
| :-- | :-- |
| $\Delta \le 2.0$pp | ⛔ **不可归因。** 必须如实写「在本语料上未观察到可归因的差异」，⛔ 不得声称八阶段循环有效。⚠️ 此时 C-① 的有效性主张需要重新设计证据 |
| $2.0 < \Delta \le 10$pp | 「观察到差异，量级小于一个数量级」。⛔ 不得写「显著」「远超」 |
| $\Delta > 10$pp | 「观察到明显差异」。⭐ 仍⛔ 不得写「显著」（§5.2） |

⭐ **`hit@3` 与 `hit@all` 的 Δ 必须同报**，且⛔ 不得只报三者中最有利的那个。⚠️ 三者可能给出方向不同的图景（例如 X1 的 `hit@1` 低而 `hit@3` 接近，说明基线能碰上但不稳定），⭐ **那本身就是结果的一部分**。

### 5.4 多报侧的登记

⚠️ **v46 根本没有按 `over@1` / `over@any` 的格次口径报多报侧**，而是用**稳定性口径**（簇在 6 格中出现几次；`174/288 = 60%` 只出现在 1 格）。

⛔ **所以 X1 的多报侧并排必须用同一个稳定性口径**，⛔ 不能一臂用稳定性、一臂用格次均值。⭐ 若另要给真 `over@1`，必须**两臂都重新算**。

⭐ **预期方向已登记**（⛔ 这不是希望，是设计的必然推论）：朴素臂**没有任何 gate**，其多报量大概率**显著高于**主臂。⭐ 这不是要去「修」的——⭐ **多报差异本身就是结果的一部分**。⛔ 不许为了让对照臂「干净些」而加 gate，那等于把 C-① 送给它。

---

## 6. 回归红旗（触发即判本次运行作废）

| # | 红旗 | 处置 |
| --: | :-- | :-- |
| 1 | 任一格的 `prompt_sha256` ≠ `17e5067b…` | ⛔ 作废，查明 prompt 何时被改 |
| 2 | 任一格 `inputs.truncated != false`，或 `nl_sha256`/`plantuml_sha256` 与语料不符 | ⛔ 作废 |
| 3 | 任一格 `max_output_tokens_override` 或 `temperature_override` 非 null | ⛔ 作废（这是「把对照臂做弱」的直接证据） |
| 4 | 任一格 `configured_model` 不是那两个 | ⛔ 作废 |
| 5 | `cells_ok < 324` 且失败不属「provider 侧错误」或「schema 穷尽重试」两类 | ⛔ 查明后重跑该格；⚠️ schema 类失败**本身就是必须修的缺陷**，⛔ 不许调大重试次数了事 |
| 6 | 判定表里出现 `00x8` 家族的记录 | ⛔ 网格被改错了，作废 |
| 7 | 判定表缺任一 `REPORTABLE` 记录 | ⛔ 拒算（少一条就是「更改分母 / 剔除不利样本」） |
| 8 | 隔离测试失败（`src/` 引入了主臂模块） | ⛔ 作废：「三条 contribution 一条都没给」这句话失去唯一机械证据 |
| 9 | 泄漏测试失败 | ⛔ 作废 |
| 10 | 发现同一输出目录被两个进程写过（序号重复 / 记录缺失 / `FileExistsError`） | ⛔ 作废该批，按 §3.5.1 先数进程再读代码 |

---

## 7. ⭐ 「基线不是稻草人」的可核验陈述

⛔ **事后补写没有说服力**，所以在此登记。逐条对照表在 [prompt/README.md](./prompt/README.md) §2（给了什么 / 省了什么 / 为什么省了仍说得通，含 worked example 那一格的单独论证），泄漏审查的两个方向在同文件 §4。

**下限判据**：对照臂必须是「**一个称职的实践者手上只有一个 LLM、没有我们的方法时，会真的这么做**」的那个东西。

⛔ **本实现不含以下任何一项**（每项都有机械断言或 record 字段可核）：

| 做弱手法 | 核验方式 |
| :-- | :-- |
| 截断输入 | record 的 `inputs.truncated` + 两个 sha256 + 字符数 |
| 压 `max_output_tokens` | record 的 `max_output_tokens_override: null` + `profile_max_output_tokens` |
| 禁止逐步思考 | schema 有可选 `analysis` 字段**专门**提供全局推理落脚点；`test_prompt_no_leakage.py` 禁 `do not think step` 一类措辞 |
| 降模型档 | record 的 `configured_model` / `observed_model` |
| 任务陈述含糊 | `test_task_statement_is_explicit()` 正向断言 |
| ⚠️ **保守措辞压召回** | `WEAKENING_PATTERNS` 机械禁 `only report ... confident` / `be conservative` / `at most N issues` 等。⚠️ 这一组最容易被忽略：它读起来全是「好的工程实践」 |

⛔ **并且不含放水**（另一个方向）：无台账内容、无谓词名（19 条逐条机械核）、无检查清单、无 worked example、无「注意检查 X」式引导。⚠️ 审查范围含**运行时生成**的 schema 重试反馈——它只携带字段路径与错误类型，`test_retry_feedback_is_purely_structural()` 钉住。

⚠️ **独立审查者签字**：〔用户裁定 2026-08-12〕「独立审查这件事先不用管到时候再说」——⛔ **故本次不作为开跑前置条件**。上面的三栏表与本节陈述照旧写全，留待后续 review 处置。

---

## 8. ⛔ 现有工具在 X1 上的适用性（跑前预判，⛔ 不许事后找理由）

⚠️ **这一节是本登记里最容易被事后美化的部分**，所以在跑前写死。三个关键工具**都不能原样用**。

### 8.1 ⛔ `verdict_tiers.py`：整体不可用

它的 `build()` 依赖 `cell_evidence()` 从 run record 抽 `function_call_trace`（断言的函数调用轨迹）。⛔ X1 无断言、无此产物 → `positions` 为空 → 脚本 `SystemExit`。

⭐ **X1 自建替代，只保留两样**：`EQUIVALENCE_FORMS` 闭集 + `hit=true` 时 `argument` ≥ 20 字的 C 层闸。⛔ A/B 层（自动确认）在 X1 上不存在——⭐ **所以 X1 的 588 位必须 100% 逐位人工填满，一位都不能靠 A 层兜底。**

⚠️ **对照信息**：主臂 588 位中有 **20 位**靠 A 层自动确认、无逐格 `argument`。⭐ 所以 X1 的判定覆盖率反而**更完整**（588/588 有 argument vs 574/588）。⚠️ 但这也意味着两臂的判定机制不同质，记入 §9。

### 8.2 ⛔ `adjudication_recheck.py`：不可用，且失效模式是**静默全 0**

它用 `published_titles()` 读 run record 的 `issues[i]["title"]`。⛔ X1 的 `NaiveIssue` 没有 `title` 字段 → `coverage()` 恒 `0.0` → 一位都过不了阈值 0.5 → **输出「0 对 0 位」**。

⛔⛔ **而「0 对」正是达标判据的形状** —— 于是「检查通过」与「检查根本没作用对象」在终端上完全一样。⚠️ 这正是本仓库反复出现的最坏失败形态（`present_for_judgment.py` 自己的 docstring 记着同类事故：「这个脚本曾经在真实路径上**输出零行并 exit 0**」），而 `adjudication_recheck.py` **没有**非零退出保护。

⚠️ **并且原判据本身就不成立**：v46 实测**不是 0 对**，而是 28 对分属 9 族、经人工裁定为工具假阳性。⛔ 照抄「须为 0 对」会立刻违约。

⭐ **X1 的替代设计（跑前定死）**：

| 检查 | 做法 | 判据 |
| :-- | :-- | :-- |
| **(a) 臂内横向复检** | 把 `published_titles()` 换成拼接 `issue + where + reason` 的 `published_texts()`，其余逻辑（台账侧 `element_forms` / `coverage` / 阈值 0.5）原样复用。⭐ 台账侧一个字不改——⭐ 立论「**同一个缺陷，散文可以换着说，元素名不能**」对 X1 的自由文本**同样成立**，甚至更成立（X1 没有谓词名可依赖，只能写元素名） | ⛔ **不是「0 对」**，而是「**每一对都有书面处置**」（判为工具假阳性 / 判为真不一致并更正） |
| **(b) 跨臂判据一致性** | 对同一 `(record_id, run, pair)`，主臂判命中而 X1 判未命中的位，并列两侧产出文本与两侧 `argument`，人工复核一句：**「若把 X1 这条文本原样放进主臂那一格，我还会判命中吗？」** | ⛔ 不可机械化裁定，只能机械化定位。产出是工作清单，⛔ 不是 pass/fail |
| **(c) 配对条件的改动** | `predicate_of` 那一条配对条件改成**台账 `record_id` 相同**（X1 侧本无谓词） | ⚠️ 文档必须写明「此处 predicate 是**台账侧**属性，⛔ 不是产出侧属性」，否则读者会误以为 X1 有谓词 |

### 8.3 ⛔ `present_for_judgment.py`：14 个区块只剩 4 个

⭐ 保留：表头 issue 计数 · 台账期望 · 模型产出正文 · 尾部分母声明。⛔ 落空的 10 个：`excluded_findings`（归因层）· `excluded_observations`（证据角色制度）· `coverage_gaps`（修订预算）· `rejected_issues` / `rejected_exclusions`（结构门）· `issue_citations_pruned`（引用剪除）· `unaccounted_safe_false_assertions` · `unsupported_issues_dropped` · `thin_merge_warnings` · `misfiled_findings_moved`。X1 一个都没有这些机制。

⚠️⚠️ **这不是「X1 更简单」，而是一个必须放正文的不对称**（见 §9 第 1 条）。

⭐ X1 新写 `src/present.py`，⛔ 不改主臂脚本。

### 8.4 多报侧分析：能做 / 做不了

⭐ **关键发现：判类靠的是「制品 + 作者源 + NL + 台账」，⛔ 不是产出的结构。** 产出只需提供三样：一条能读懂的主张、它落在哪个 pair、它在 6 格中出现几次。⭐ 所以五大类裁定、23 子类中的绝大多数、两级归并、以及 `unexpected_tables.md` 六张表中的**五张**，X1 都能做，且可直接复用 `rebuild_unexpected.py`（写成同 schema 的 `G*.jsonl`）。

⛔ **做不了的四项，及如何交代**：

| 做不了 | 为什么 | ⛔ 报告里必须怎么写 |
| :-- | :-- | :-- |
| 表 3「谓词族 × 裁定」 | X1 无谓词、无断言签名。⭐ 这不是能力缺陷，是**对照臂按设计不携带 C-② 闭合词表** | 「**该表在 X1 上不存在被度量的对象**」。⛔ 不写「X1 未做该分析」，⛔ 更不得拿主臂的表 3 去暗示 X1 的谓词行为 |
| 真阴性剔除（主臂扣了 2 条） | 需把断言在冻结制品上重新求值；X1 的 issue 不是可求值命题 | 「X1 的分母闭合只有两个去向（桶内 + 台账已承载），**没有真阴性档**，这使 X1 桶内分母相对主臂偏大一个未知量」。⚠️ **方向对 X1 不利，必须点明** |
| 进桶前的机械匹配 | 主臂用 `谓词 + 元素` 签名机械匹配台账；X1 只有散文，⛔ 不得按标题相似度对齐 | 必须**全人工**判「这条 issue 有没有被某条台账记录认领」，并明写「X1 的 matched/unmatched 划分由人工做，主臂由机械匹配器做，**两侧划分机制不同**」。⚠️ 放正文，⛔ 不放脚注 |
| `FP-A` / `N-ANCHOR` 形态一 / `N-MODAL` 三个子类 | 三者都以「断言被构造成什么形状」命名 | 「这三个子类在 X1 上**无对应形态**，因为它们描述断言构造的失误，而 X1 不产出断言」 |

⚠️ **另一处不对称**：条目/去重比高有两种解释（缺陷天然被多谓词命中 / 产出侧重复报同一件事）。⭐ **X1 没有谓词，所以第一种解释在 X1 上不成立**——它的高比值只能读作产出侧重复。⛔ 两臂不对称，必须写明。

⚠️ **X1 特有的新裁定路径**（主臂无先例，在此定义）：若一条 issue 的 `issue` + `where` + `reason` 三段合起来**仍不能定位到制品上任一元素或结构**，记为一个独立的**产出可判定性**统计量，⛔ **不塞进五类**。⛔ 且五类里不设「待定」（沿用主臂纪律：取证不足不是判据不足）。

### 8.5 判定材料的泄漏面（X1 新增）

⚠️ 主臂的盲判样本器有一个 `_BAND_WORDS` 黑名单（`调优` / `留出` / `已烧毁` / `可报` / `hold-out` / `tuned` / `burned`）。⛔ **它没有 `基线` / `baseline` / `naive` / `X1` / `对照`。**

⭐ **X1 的判定材料必须满足三条**（由 `tests/test_judge_material_shape.py` 钉住）：

1. ⛔ 不含主臂在同一位的判定结果（`hit` / `equivalence_form` / `argument`）——⚠️ 判定者读到「主臂这一位命中了」会被锚定
2. ⛔ 不含台账的「答案」字段：`replay`（**期望真值**）· `assertions[].measured` · `assertions[].expression` · `upstream.eight_cell_published`（往轮已发布 issue id）
3. ⛔ 不含带方向性的臂标签措辞

⚠️ **判定非盲**：判定者知道自己在判基线臂。⛔ **不做混臂盲判**，三条理由：(i) 混臂盲判必须重判主臂已冻结的位，与 588 冻结冲突；(ii) `hit_criterion.md` 已要求逐位写 `equivalence_form` + `argument`，严格度漂移可逐条事后审计；(iii) §8.2(b) 的跨臂复核已针对同一通道。⭐ **判定非盲这件事记入 Limitations**，⛔ 不隐瞒。

---

## 9. ⭐⭐ 已知的两臂不对称：⛔ 两个方向都必须披露

⚠️⚠️ **这一节是本登记的学术核心。** 已识别的不对称**方向相反**，⛔ **只披露对我方有利的那一侧就是选择性披露**。

### 9.1 压低 Δ 的（⛔ 对我方不利，⛔ 同样必须写）

| # | 不对称 | 机制 |
| --: | :-- | :-- |
| 1 | ⭐ **主臂有「被自己的门吃掉」的发现，X1 没有** | 主臂的「没报」里混有若干「报了但被结构门 / 归因层 / 角色制度 / 预算吃掉」；X1 无任何 gate，它的「没报」是纯粹没报。⛔ 若把两臂 `hit@1` 直接相减而不说明，主臂被自己门吃掉的那部分会被记成「能力不足」 |
| 2 | `EIS-0047-03` 的引入动机剔除 | 主臂有一位被人工认定「应为命中但保持不计入」；X1 无该规则、照旧计入 |
| 3 | X1 无真阴性档 | 主臂多报侧扣了 2 条真阴性，X1 扣 0 条，使 X1 桶内分母偏大一个未知量 |
| 4 | X1 的判定覆盖更完整 | 主臂 20 位靠 A 层自动确认、无逐格 argument；X1 588 位全部有 argument |

### 9.2 抬高 Δ 的（⭐ 对我方有利，⛔ 尤其要写）

| # | 不对称 | 机制 |
| --: | :-- | :-- |
| 1 | ⭐⭐ **判定误差单向低估基线** | 判定者顺着台账 primary 的字面找对应 issue，措辞不同就可能误判成没报。⚠️ X1 侧无 C 层分歧闸（`verdict_tiers` 不可用），⛔ 这个方向的误差没有机械兜底。⭐ **因此必须写「实测 Δ 是真 Δ 的上界」** |
| 2 | 判定非盲 | 判定者知道哪一臂是基线（§8.5） |
| 3 | matched/unmatched 划分机制不同 | X1 全人工、主臂机械匹配器；人工划分的宽严不受机械阈值约束 |

⛔ **报告里必须有一节并列这两组**，且⛔ 不得给出「两者大致抵消」这类未经量化的安抚性结论。

---

## 10. 交付物

| 产物 | 落点 |
| :-- | :-- |
| 逐格 record（324 份，自包含） | `runs/paper1/x1-baseline-v1/`（gitignore） |
| 运行 manifest（格数、失败、usage 汇总） | 同上 `manifest.json` |
| ⭐ 逐位判定表（格式 A，588 位） | [results/verdicts_x1.json](./results/) |
| ⭐ 度量输入表（格式 B） | `results/tiers_x1.json` |
| ⭐ 三口径 + 与主臂并排 | `results/metrics.md` |
| ⭐ 多报侧五类裁定（`G*.jsonl` 同 schema） | `results/unexpected_verdicts/` |
| ⭐ 多报侧六张表（表 3 空表并注明无被度量对象） | `results/unexpected_tables.md` |
| ⭐ 不对称披露节 | `results/asymmetries.md`（或并入 `metrics.md`） |

---

## 11. 登记之外的话（⛔ 不构成承诺）

⚠️ 有一件事必须在这里说清，因为它是本臂最大的**解读风险**：

⭐ smoke 显示基线在 pair 0000 上**命中了核心缺陷**。⛔ **所以不要期待 Δ 来自「基线什么都找不到」**。⭐ 合理的预期是：基线在**显眼的结构缺陷**上能命中，差距出现在**需要系统性检查的地方**——仿真类义务、多条需求的逐条覆盖、以及不显眼的缺陷。⭐ 那正是 C-① 主张的价值所在。

⛔ **但这只是预期，⛔ 不是登记的档位。** §5.3 那张档位表才是判据，⛔ 且它已经写死了「$\Delta \le 2.0$pp 时必须如实说未观察到可归因差异」这一支。
