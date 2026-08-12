# 事前登记 · `x1-split-intervention` —— 把 H-SPLIT 从观察性结论变成干预性结论

**登记时间**：2026-08-12，**写在任何一格开跑之前**。本文件与实现改动同批 push；远端时间戳是「事前」的唯一证据。

**一句话**：主臂输给朴素基线 14.97pp，损失几乎全部落在「台账谓词没被写进需求集」那一层。该分层是**观察性**的（分层变量是流水线自己的输出），无法排除反向解释。本次**只加宽 splitter 的提问范围、不动验证机器**，看那批位能不能追上。

---

## 1 · 背景与待判命题

### 1.1 已确立的观察性结论

两臂对照，98 条 REPORTABLE 台账记录 × 2 模型 × 3 轮 = 588 位：

| 臂 | hit@1 |
|:--|:--|
| 主臂（八阶段 feedback loop + 19 谓词 + 形式断言） | 355/588 = 60.4% |
| X1（单次朴素提示、自然语言输出） | 443/588 = 75.3% |
| Δ | **−14.97pp** |

按「台账那条缺陷的 `primary_predicate` 是否出现在该格 splitter 产出的 requirement 集合里」分层（本次已独立复算，三层数字逐一吻合）：

| 分层 | 位数 | 主臂 | X1 | Δ |
|:--|--:|--:|--:|--:|
| 谓词**写进了**需求集 | 345 | 71.0% | 72.5% | −1.4pp |
| 谓词**没写进**需求集 | 177 | **41.8%** | 80.2% | **−38.4pp** |
| 台账无 `primary_predicate` | 66 | 54.5% | 77.3% | −22.7pp |

复算脚本 `/tmp/x1intervene/select_pairs.py`，输入为 `discover_matrix/v46/verdicts/v46_tiers.json`、`baseline_arm/results/tiers_x1.json`、`manual_review/expected_issue_set.json`，以及姊妹 clone `~/oo-projects/research_ideas/runs/paper1/matrix-v46-full/<run>/<cell>/records/*requirement-splitter-llm-call-completed*/record.json` 的 **`parsed_output.requirements[].predicate`**（⛔ 不对整条记录做正则——`system_prompt` 里含谓词词表的 worked example，那正是 `loss_stages.py` 文件头记载的、曾经翻掉一个已发布结论的 bug）。

### 1.2 两个互斥解释

- **H-SPLIT（提问侧瓶颈）**：验证机器本身没问题，损失来自 splitter 没把这些问题提出来。
- **H-REVERSE（下游也吃力）**：splitter 之所以不问某些问题，**恰恰因为**那些现象在下游也难以断言。若如此，「机器没问题」是分层变量内生带来的假象。

⛔ 观察性分层**无法**区分这两者。本实验的唯一目的就是区分。

---

## 2 · 干预是什么

### 2.1 边界：只动提问侧

改动**只**发生在两处 prompt 常量：`REQUIREMENT_SPLITTER_PROMPT` 与 `REQUIREMENT_REVIEWER_PROMPT`。

**未改动**（逐一列出，构成「验证机器不变」的具体含义）：`ASSERTION_CONVERTER_PROMPT`、`ASSERTION_REVIEWER_PROMPT`、`RESULT_ADJUDICATOR_PROMPT`、`predicates.py` 的 19 个谓词及其求值、`schemas.py`、`nodes.py` 的全部确定性门与 gate、`graph.py` 的 11 个节点与路由、断言封存与求值、release / attribution / adjudication。

requirement reviewer 归入「提问侧」，因为它决定哪些问题活到被问；它不产出、不评估任何断言。这条归类在报告中必须显式说明，不得默认读者同意。

### 2.2 为什么必须同时改 reviewer

reviewer prompt 现有两条会删掉结构扫描需求：

- `prompts.py:87`：`Do not add a semantic distinction merely because the current FCSTM exposes a convenient state, event, transition, or variable.`
- `prompts.py:90` 末：`A requirement **without** `derivation` is judged by your normal rule -- an addition with no NL source is deleted as before.`

确定性层**不会**拒绝无 NL 锚的需求（已核查：`source_segment_ids` 无 validator、`default_factory=tuple`；覆盖投影只做 segment→requirement 单向检查；`named_elements` 无反向检查；需求条数无上限）。唯一的拦截者是 reviewer 这个 LLM。因此只改 splitter 会让干预**在 reviewer 处被静默吃掉**，测到的将是「reviewer 会不会删」而不是「加宽提问有没有用」。

### 2.3 逐字改动

以环境变量 `X1_STRUCTURAL_SWEEP=1` 开关，**两臂共用同一份源码**。已验证：

| 条件 | splitter prompt sha256[:16] | reviewer prompt sha256[:16] |
|:--|:--|:--|
| git HEAD（改动前） | `41a1795c131857c0` | `6c7f0b0ea83e99ee` |
| `X1_STRUCTURAL_SWEEP` 未设 / `=0`（**对照臂**） | `41a1795c131857c0` | `6c7f0b0ea83e99ee` |
| `X1_STRUCTURAL_SWEEP=1`（**干预臂**） | `4044419f4541193f` | `29f64ea8ea5e5c0b` |

对照臂与改动前**逐字节相同**，这是「对照臂没有被污染」的机械证据。

追加到 splitter 的整块（`X1_STRUCTURAL_SWEEP_SPLITTER`）与追加到 reviewer 的整块（`X1_STRUCTURAL_SWEEP_REVIEWER`），全文见同批提交的 `discover/prompts.py` 末尾，此处不复制以免两份漂移。要点：

1. **`edge_declared`**：把既有的「句子点名了哪些元素」扫描，同方向延伸到「句子点名了哪条迁移」。
2. **`reaches`**：NL 要求机器能占据的状态，问模型是否到得了。
3. **`event_consumed`**：NL 说机器在某作用域内响应某事件，问该作用域是否接受它。
4. **`guard_distinguishable`**：NL 要求某触发下结果确定，而模型有多条同触发出边。

四条共同纪律：**仍然是 NL 锚定的**——模型只提供候选绑定（这与 `declared_model_vocabulary` 为其它每一条需求提供候选绑定是同一件事），NL 提供主张；`source_segment_ids` 照填；没有句子支撑就不发。

### 2.4 ⚠️ 公平性自陈：本干预是 oracle-informed 的

**引入动机**（CLAUDE.md §3.5.-1 要求与领域出处分开记）：这四个谓词是**看着台账选的**——`edge_declared` 是 7 条 REPORTABLE 记录（42 位）的 primary 而 324 格里写进需求集的位数为 **0**，`reaches` / `event_consumed` / `guard_distinguishable` 是紧随其后的三个缺口。这是用答案指挥注意力。

**因此三条硬约束，写在跑之前：**

1. ⛔ 本干预**不得**作为方法改进对外表述，任何情况下都不行。它是定位瓶颈的探针。
2. prompt 全文**不含**任何 pair、状态名、事件名、台账条目或缺陷描述；对 324 格中的每一格文本完全一致。四条扫描各自有独立的领域出处（有限状态机的可达性分析、迁移声明检查、同触发出边的确定性、事件未消费检测），不依赖本批任何样本。
3. oracle-informed 这件事**对因果问题反而是增强而非削弱**：若连「直接告诉 splitter 该问什么」都救不回来，H-REVERSE 就得到强支持；若救得回来，瓶颈确实在提问侧。两个方向的结论都成立，只是前者更强。

---

## 3 · 网格

**10 个 pair × `claude-opus-4-7` × 1 轮 × 2 条件（对照 / 干预）= 20 格。**

选 pair 的判据（**跑前写死**）：v46 中 claude 臂在「谓词没写进需求集」层命中最差、且 X1 证明该缺陷可被发现、且涉及的 primary 谓词落在四条扫描的射程内。

| pair | 该层位数(claude,3轮) | 主臂 | X1 | 涉及谓词 |
|:--|--:|--:|--:|:--|
| 0049 | 6 | 0% | 67% | edge_declared, guard_distinguishable |
| 0009 | 3 | 0% | 100% | edge_declared |
| 0027 | 3 | 0% | 100% | reaches |
| 0040 | 3 | 0% | 100% | event_consumed |
| 0037 | 2 | 0% | 100% | reaches |
| 0005 | 5 | 0% | 60% | edge_declared, containment |
| 0026 | 4 | 25% | 100% | reaches, effect_declared |
| 0056 | 5 | 40% | 100% | guard_distinguishable, effect_declared |
| 0039 | 4 | 50% | 100% | edge_declared, guard_distinguishable |
| 0010 | 6 | 50% | 83% | reaches, event_consumed |

选 claude 而非 gpt：v46 中位墙钟 258s vs 1123s，token 约一半；时间预算下这是唯一能跑完对照+干预两臂的选择。⚠️ 代价是结论只对 claude 臂成立，报告中必须写明。

### 3.1 两个位集（跑前固定，⛔ 事后不得增删）

**TARGET（14 条）**——v46 claude 三轮中 ≥2 轮属「谓词没写进需求集」：

`EIS-0005-01` `EIS-0005-02` `EIS-0009-01` `EIS-0010-04` `EIS-0010-05` `EIS-0026-03` `EIS-0027-01` `EIS-0037-01` `EIS-0039-01` `EIS-0040-01` `EIS-0049-01` `EIS-0049-03` `EIS-0056-01` `EIS-0056-02`

v46 claude 三轮基线：**9/42 = 21.4%**；同批 X1：36/42 = 85.7%。

**REGRESSION（12 条）**——同 10 个 pair 内其余 REPORTABLE 记录：

`EIS-0005-03` `EIS-0009-02` `EIS-0009-03` `EIS-0010-01` `EIS-0010-02` `EIS-0010-03` `EIS-0026-01` `EIS-0026-02` `EIS-0039-02` `EIS-0040-02` `EIS-0040-03` `EIS-0049-02`

v46 claude 三轮基线：28/36 = 77.8%。

**主比较对象是同批跑出的对照臂，不是 v46 数字**：当前分支的 `prompts.py` / `nodes.py` / `schemas.py` / `predicates.py` / `capability.py` 相对 v46 的 `ca41369e` 有 20–126 行改动（含一次泄漏清理：v46 的 splitter prompt 里 worked example 用的是语料原句 `"human steering cmd, brake pressed"`）。v46 数字只作次要参照，用于检测漂移。

---

## 4 · 达标判据（⛔ 跑前写死，事后不得调整）

以同批**对照臂**为基准，TARGET 14 位（1 轮，故 14 位 = 14 格·记录）：

| 判定 | 条件 |
|:--|:--|
| **H-SPLIT 成立** | 干预 TARGET 命中 **≥ 9/14（64.3%）** 且比对照臂多 **≥ 5 位** |
| **H-SPLIT 部分成立** | 干预 TARGET 命中 **≥ 6/14（42.9%）** 且比对照臂多 **≥ 3 位** |
| **H-SPLIT 不成立（H-REVERSE 得到支持）** | 干预比对照臂多 **≤ 1 位** |
| **数据不足** | 落在上述之间，或红旗触发导致命中数不可采信 |

**9/14 = 64.3% 的来历**：v46 claude 在 TARGET 上是 21.4%，X1 是 85.7%，缺口 64.3pp；64.3% 恰是**追回缺口的三分之二**（21.4 + 0.67 × 64.3 = 64.4）。**6/14 = 42.9% 的来历**：追回缺口的三分之一，数值上也正好等于全量该层的观察均值 41.8%——即「这批最差的 pair 被拉到该层平均水平」。

### 4.1 回归红旗（任一触发，命中增益按「受污染」报告，不得直接宣称 H-SPLIT 成立）

| 红旗 | 红线 |
|:--|:--|
| **多报暴增** | 干预臂每格已发布 issue 均值 > 对照臂 **2.5 倍**。v46 claude 在这 10 个 pair 上是 4.03 issue/格（中位 3，最大 10）。⭐ 这是最重要的一条：若干预只是把 issue 撒得更多，命中率上升是霰弹效应而非提问变准 |
| **REGRESSION 退化** | 干预臂 REGRESSION 命中比对照臂低 **> 2 位** |
| **降级格增多** | 干预臂 `degraded_stages` 非空的格数比对照臂多 **> 3 格**。v46 claude 这 30 格降级数为 **0** |
| **整格失败** | 干预臂落盘失败 **> 2/10 格** |
| **断言不可执行率上升** | 干预臂 `coverage_gaps` 条目均值 > 对照臂 2 倍 |

### 4.2 ⛔ 不达标说明什么

若干预臂在 TARGET 上**没有**明显超过对照臂（多 ≤1 位），则：

- **H-REVERSE 得到支持**：即使把问题直接塞进 splitter 的提问范围，下游也产不出可发布的命中。那么「验证机器没问题、只是没问」这个读法**站不住**，§1.1 的分层结论只能作为相关性陈述，⛔ 不得在论文中写成「瓶颈在需求层」。
- 此时须进一步区分两种失败机制，用产物直接判读、不靠推测：
  1. **提问没进去**：干预臂的需求集里根本没多出这些谓词（reviewer 删了 / splitter 没照做）→ 那么这次实验**没有真正实施干预**，结论是「数据不足」而非 H-REVERSE，须记为实验失败并说明。
  2. **提问进去了但下游产不出**：需求集里有了，但断言层 / 发布层没跟上 → 这才是 H-REVERSE 的真正证据。
- 因此**必须报告一个中间量**：干预臂 TARGET 对应谓词写进需求集的比例（即分层变量本身被干预推动了多少）。这是区分 1 与 2 的唯一依据，也是本实验的**操纵检查（manipulation check）**。⛔ 没有它，任何方向的结论都不成立。

**操纵检查的下限**：若干预臂 TARGET 位中「谓词写进需求集」的比例 **< 50%**，则无论命中如何，本次一律判「数据不足 —— 干预未被有效实施」。

---

## 5 · 执行与记录

- 配置真源 `.llmconfig.yml`，`--profile claude-opus-4-7`。⛔ 不 source 任何 `.env`。
- 输出目录 `runs/paper1/x1-split-intervention/{control,treatment}/<pair>-claude`，⛔ 不覆盖既有任何 run。
- 开跑前 `ps -eo pid,lstart,args | grep -i discover` 确认无残留工作进程。
- 每格保留完整 run record；两臂的 `CODE_VERSION.txt` 记录同一 commit，仅环境变量不同。

## 6 · 判定

- 用 `discover_matrix/docs/judges/hit_criterion_for_judges.md` 的四种语义同一性形态逐位判定，与 v46 / X1 同一套口径。
- ⚠️ 判定材料用**完整信息**：完整 NL + 作者源 + 未截断的 issue 三段。⛔ 不用 `--compact`——那是 v46 判定的已知缺陷。
- 判定者不得看到本文件的达标判据。

## 7 · 已知局限（跑前即可写出，⛔ 不因结果好坏改动）

1. **样本量小**：TARGET 14 位、单轮、单模型。能支持「有没有明显方向性效应」，⛔ 不能支持效应量的精确估计，也不能给出可信区间意义上的显著性。
2. **只测 claude 臂**，不外推到 gpt-5.5。
3. **pair 是按主臂最差挑的**，存在向均值回归的成分；对照臂同批同 pair 正是为控制这一项——⛔ 因此绝不能拿 v46 数字当主对照。
4. **单轮无法区分能力与稳定性**：⛔ 不报 `hit@3` / `hit@all`。
5. **干预是 oracle-informed 的**（§2.4），⛔ 不是方法改进。
6. **同时改了 splitter 与 reviewer 两处**，本实验不能区分二者各自的贡献。

---

## 8 · 修订 A（v2 干预）—— 只修操纵，不动判据

**登记时间**：2026-08-12 18:4x，**写在 v1 的任何命中判定产生之前**。此刻手上只有 v1 的操纵检查中间数据（各格需求集里出现了哪些谓词），⛔ 没有任何 hit 数据。

### 8.1 为什么修

v1 把扫描块 append 到 splitter prompt 的**最末尾**，于是它排在两样东西**后面**：

1. 一节自称 `=== Binding output contract (final, overrides anything above) ===`；
2. 一段 `Derive the Requirement from the natural language, not from the model. You are shown the model so you can spell its identifiers correctly and see what it declares -- not so you can read the obligation off it.`

v1 跑到一半时的中间观察：干预臂需求条数确实变多（如 0005 的 22 vs 18），但四条扫描谓词几乎没多出来；且 0010 的**两条臂**都在 rev1 写了 `reaches`、rev2 又都被 reviewer 删掉。

⭐ **一个排在「自称最终且覆盖以上全部」的小节后面、又与一条反复强调的规则表面冲突的指令，如果没被执行，那是操纵本身的缺陷，⛔ 不是关于假设的证据。** 按 §4.2 的操纵检查下限，这种情况本来就只能判「数据不足」。

### 8.2 改了什么

`X1_STRUCTURAL_SWEEP=2`：

1. **位置**：扫描块从「prompt 末尾」改为**插到 `=== Binding output contract (final...) ===` 之前**。
2. **新增一段**（`X1_SWEEP_RECONCILIATION`）：显式调和「不要从模型读出义务」那条规则——它禁止的是把**义务**读自制品，而不是禁止用制品判断 NL 的哪些要求值得检查；每条扫描仍是句子给主张、模型只给候选绑定。

⛔ **没有改**：四条扫描的内容、reviewer 追加块、§4 的全部达标判据与红旗、TARGET / REGRESSION 位集、pair 选择、模型、轮数。

### 8.3 纪律

| 约束 | 内容 |
|:--|:--|
| 判据不动 | §4 的 9/14、6/14、≤1 位、五条红旗、50% 操纵下限**逐字不变** |
| v1 不作废 | v1 结果**全量报告**，⛔ 不得替换、不得只报 v2 |
| 对照臂复用 | 对照臂 prompt 在三种模式下逐字节相同（`41a1795c131857c0`），故 v2 复用同一份对照臂产出，不重跑 |
| 哈希留证 | 对照 `41a1795c131857c0` · v1 `4044419f4541193f`（len 99782）· v2 `9ecadc392a23a20c`（len 100652）。v1 哈希不变，即 v1 数据仍可复现 |

⚠️ **这是一次操纵强化，不是假设修改**：操纵检查失败允许加强操纵，⛔ 不允许改结果判据。若 v2 的操纵检查仍 < 50%，则本实验对 H-SPLIT 与 H-REVERSE **都不给结论**，如实记为「干预无法被有效实施」。
