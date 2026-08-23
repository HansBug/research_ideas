# [paper1] 统一 expected-issue 语义 Judge：`FULL / PARTIAL / NONE` × `VALID_KNOWN / VALID_NOVEL / INVALID`

> **结论先行**：冻结台账仍是 expected-issue recall/hit 的唯一分母；谓词与 W 等级只描述证据强度，不进入语义命中门槛。Judge 分成两个职责清楚的维度：维度 A 只判断候选与台账的语义匹配强度，维度 B 只判断候选是否成立及其是否属于已知台账。`PARTIAL` 不算主 hit，也不算 FP；只有 `INVALID` 算语义 FP。最终计分不保留 `UNKNOWN`。

本 issue 是 #189 的评测协议 follow-up，并以 #172/#189 冻结的 D2+D1 台账作为 expected issue 集合。它同时给出固定六 pair 上当前 evidence-discovery、重构前 v27、X1v2 baseline 的单轮同模型初步复评，目的是先消除三套 Judge 口径不一致，再讨论方法优劣。

---

## 1. 为什么第二维不再拆 `VALID_KNOWN_HIT / VALID_KNOWN_PARTIAL`

`FULL/PARTIAL` 已经是维度 A 的职责。若维度 B 再写 `KNOWN_HIT/KNOWN_PARTIAL`，会把匹配强度复制一遍，使两个维度职责重叠，并容易让实现把 `PARTIAL` 直接转成 FP。这里追求的是职责不重复；由于 `KNOWN/NOVEL` 需要读取维度 A 的最佳关系，它不是数学意义上的完全独立随机变量。

因此最终格局是：

1. **维度 A：expected-issue 语义匹配强度**：`FULL_MATCH / PARTIAL_MATCH / NO_MATCH`。
2. **维度 B：报告有效性与台账归属**：`VALID_KNOWN / VALID_NOVEL / INVALID`。
3. `VALID_KNOWN` 只表示报告可归属某条冻结台账；它是否形成 hit，完全由维度 A 是否为 `FULL_MATCH` 决定。
4. `VALID_NOVEL` 必须对所有台账都是 `NO_MATCH`，但报告自身经审计成立。
5. `INVALID` 是报告核心主张不成立或无法承担预注册的最低举证责任。

形式上，冻结 expected issue 集合记为 \(E\)，某臂最终发布且由方法自裁为 D2/D1 的原子 issue 报告集合记为 \(R\)。D0 是方法内部淘汰项，不进入 \(R\)，也不参与 hit/FP；但方法自报的 D2/D1 只是发布准入，不是 Judge 真值。W0/W1/W2 不出现在匹配函数中。

---

## 2. 维度 A：Expected-Issue 语义匹配强度

| 档位 | 严谨学术定义 | 可执行定义 | 主要学术依据 | 是否算主 hit |
| :-- | :-- | :-- | :-- | :--: |
| **`FULL_MATCH`** | 候选与 expected issue 描述同一 defect instance、root cause、violated obligation，或同一根因的直接且可归因表现；允许措辞、抽象层级、taxonomy、定位粒度和证据形式不同 | 位置/行为上下文相容，且满足至少一条：①同一根因；②同一被违反需求/property；③直接症状足以归因于同一问题；④按候选修复会消除或实质缓解 expected 的核心违反。复合台账中，一个独立且具有诊断性的核心 facet 即可，不要求复述全部合取项 | MCeT 的 same-root-cause equivalence；NIST SATE 的 directly related finding；Pearson 的 best-case fault localization；APR 的 semantic/repair equivalence；Porter 的 fault-level detection | **是** |
| **`PARTIAL_MATCH`** | 候选与 expected 存在真实、可审计的局部或间接关系，但不足以确定同一缺陷身份 | 仅给出非唯一后果、宽泛区域、非诊断性 facet，或只能说明“可能相关”，无法建立根因、违反义务或修复重叠 | NIST SATE 的 indirectly related finding；Pearson 的 best/average/worst-case 分层 | **否**，只进入 supported coverage |
| **`NO_MATCH`** | 候选与该 expected 不属于同一缺陷，或者是台账外独立问题 | 不同根因、方向相反、仅提到同名元素、只作背景提及；修复候选后 expected 仍完整成立 | NIST SATE 的 unrelated/disregarded warning；Porter 的 known-fault key | **否** |

### 2.1 `FULL_MATCH` 的适度放宽

以下均**不是** full hit 的必要条件：

- 不要求候选复述台账全部机制与后果；
- 不要求 `property/scope/direction` 四元组逐字段相同；
- 不要求使用相同谓词、分类名或自然语言；
- 不要求 W2、编译谓词、反例轨迹或工具诊断；
- 不要求与人工参考使用同一个修复位置或补丁语法。

W1 自由文本只要具有具体 `where` 与可审计 `reason/basis`，并能建立上述任一直接关系，就可以 `FULL_MATCH`。W2 只提高证据强度与审计便利性，不获得额外 hit 权重。这一点是保证 X1v2（单 prompt、无工具、几乎没有 W2）可以公平参评的必要条件。

### 2.2 `FULL` 与 `PARTIAL` 的边界

- “细节少”不自动是 partial。局部症状若已经足以识别同一根因，按 MCeT 应为 full。
- “同一个复合台账只说了一个核心 facet”不自动是 partial。若该 facet 本身是可行动、可诊断的同一缺陷表现，按 Pearson best-case 与本项目旧 X1v2 协议，判 full。
- 只有无法唯一归因、不能建立修复重叠的相关提示才是 partial。
- `PARTIAL_MATCH` 不算主 hit，但也不是错误报告，不能进入 FP。

---

## 3. 维度 B：报告有效性与台账归属

| 档位 | 严谨学术定义 | 可执行定义 | 主要学术依据 | 是否可能贡献 hit | 是否算语义 FP |
| :-- | :-- | :-- | :-- | :--: | :--: |
| **`VALID_KNOWN`** | 报告核心主张成立，并与至少一条冻结台账具有 `FULL_MATCH` 或 `PARTIAL_MATCH` | 先用 NL、作者 PlantUML、FCSTM、inspect、执行结果或人工语义审计确认主张成立；再能归属一个 expected issue。是否命中由维度 A 决定 | MCeT FBench recall；Porter known-fault detection；SATE direct/indirect related finding | 仅当存在 `FULL_MATCH` | 否 |
| **`VALID_NOVEL`** | 报告核心主张成立，但与全部冻结台账均为 `NO_MATCH` | 必须有独立制品证据或人工审计确认是真实、独立、可行动的新问题；不能只因没进台账就判 FP | MCeT `New true issues`；SATE 对 incomplete ground truth 的限制；生产代码人工 finding validation | 否 | 否 |
| **`INVALID`** | 报告核心技术主张不成立，或在完整仲裁后仍无法达到最低举证责任 | 被 NL、作者源、UML 语义、inspect/运行结果反驳；误读事件/guard/effect/region；错误因果或方向；虚构路径；只有无可验证猜测 | Porter `False Positive`；SATE `False`；MCeT false positives | 否 | **是** |

维度 B 必须由统一 Judge 根据制品证据独立裁决，不能直接采信方法自报的 D 等级、W 等级或“这是 valid”的自然语言结论。D2/D1 报告同样可能在复核后成为 `INVALID`；W1 也可以成为 `VALID_KNOWN + FULL_MATCH`。

### 3.1 为什么最终不保留 `UNKNOWN`

`UNKNOWN` 可作为内部 `PENDING_REVIEW` 工作流状态，但不得进入发布数字。争议必须依次经过制品复核、第二次独立判读和仲裁。若 benchmark 自身缺少裁定所需材料，应在冻结前修正或排除评价单元；若候选在完整材料下仍无法承担最低证明责任，最终判 `INVALID`。

这保留了 SATE/APR 使用 unknown 防止草率误判的动机，但不把“无法完成 Judge 工作”固化成论文结果类别。

---

## 4. 派生分类与计分

每条 valid 报告先取它对全部台账的最佳关系：

```text
存在 FULL_MATCH    -> VALID_KNOWN，且可贡献 expected hit
否则存在 PARTIAL   -> VALID_KNOWN，但不贡献主 hit
全部 NO_MATCH      -> VALID_NOVEL
报告核心主张不成立 -> INVALID
```

对每个 expected issue \(e\)：

```text
hit(e) = 1，当且仅当存在一条 VALID_KNOWN 报告 r，使 match(r, e) = FULL_MATCH
Hit Rate = sum(hit(e)) / |E|
FN = |E| - sum(hit(e))
Supported Rate = 被 FULL_MATCH 或 PARTIAL_MATCH 覆盖的 expected issue 数 / |E|
```

同一 expected 被多条报告发现仍只贡献一次 hit；一条足够宽且证据完整的报告可以命中多个原子 expected issue，但必须分别给出映射理由。

报告侧：

```text
FP = INVALID 报告数
有效报告精确率（Semantic Precision） = (VALID_KNOWN + VALID_NOVEL) / 全部已裁定发布报告
Ledger-Unmatched = 只有 PARTIAL 的 VALID_KNOWN + VALID_NOVEL + INVALID
```

`Ledger-Unmatched` 只用于兼容旧的 closed-ledger 统计，不能再命名为 semantic FP。

重复的 valid 报告不增加 expected hit，也不算 FP；另报 redundancy rate。本文六 pair 初步表先按原始 release-report 口径统计 validity/FP，与三个历史产物的发布单元保持一致；论文终表还应补 root-cause cluster 版本。

---

## 5. 文献事实核验

### 5.1 直接支持宽语义 full 的一手证据

1. **Ahmed et al., MCeT, MODELS 2025**, DOI [`10.1109/MODELS67397.2025.00014`](https://doi.org/10.1109/MODELS67397.2025.00014)，§V-B：
   > “We define equivalent issues as issues that describe the same root cause of the problem in the diagram, even if they have different levels of details.”

   Fig. 5 进一步把“全图缺条件”和“某一条 message 缺条件”判为 equivalent，称后者是 “a symptom of the same root issue”。同节把不等价于任何 FBench issue、但人工确认真实的报告单列为 `New true issues`。

2. **Okun, Delaitre, Black, SATE IV, NIST SP 500-297**, DOI [`10.6028/NIST.SP.500-297`](https://doi.org/10.6028/NIST.SP.500-297)：§2.4/2.7/2.9 不要求 exact CWE 或 exact fix line；source、sink、path、different perspective 可直接 related；较弱关系按原文单列为 `Indirectly related (or coincidental)`；§2.8.1 按 same root cause 合并 weakness。

3. **Pearson et al., ICSE 2017**, DOI [`10.1109/ICSE.2017.62`](https://doi.org/10.1109/ICSE.2017.62)，§II-A/B：multi-statement fault 明确并列 best-case（任一 defective statement）、average-case（50%）、worst-case（全部）；omission fault 接受任一人工确认的合法插入位置。

4. **Martinez et al., EMSE 2017**, DOI [`10.1007/s10664-016-9470-4`](https://doi.org/10.1007/s10664-016-9470-4)：APR 中通过测试只说明 test-suite adequate；正确补丁可以与开发者补丁完全相同，也可以语法不同但语义等价。这支持用修复效果辅助操作化“同一缺陷”，而不是要求复刻参考表达。

5. **Porter, Votta, Basili, TSE 1995**, DOI [`10.1109/32.391380`](https://doi.org/10.1109/32.391380)：fault detection rate 是发现的 known faults / specification 中 known faults；Fault Report Form 另分 True Fault 与 False Positive，taxonomy 用于责任分配而不是命中字段硬门。

6. **Klees et al., CCS 2018**, DOI [`10.1145/3243734.3243804`](https://doi.org/10.1145/3243734.3243804)，§7：最终单位是 distinct bugs，不是 crash/input；同一个 sufficiently minimal fix 消除的多个症状属于同一 bug。

### 5.2 必须公开的限制

- MCeT 的 same-root-cause 判据本身偏宽，会提高 recall；论文由两位作者完成判定，前 20% 样本双人独立标注的 Cohen's $\kappa=0.79$，其余 80% 由两人分工、每条只有一位判读者。它没有第三方复核，本项目采用该口径时必须同时报告 strict/partial 诊断与本项目自己的判读一致性。
- SATE 的 exact/机械口径只在 Juliet 这类单 CWE、完整 closed-world oracle 中成立；生产代码 ground truth 不完整时，报告明确警告不能把所有 unmatched finding 当真实 FP。
- Pearson 证明的是多位置 fault 的评价场景依赖性，不是命令所有任务都采用 best-case；本项目选择 best-case 必须预注册并对所有臂一致。
- 当前两维枚举是本项目综合以上先例形成的 operationalization，不应写成某一篇论文逐字提出了这套枚举。

证据等级：上述 MCeT、SATE IV、Pearson、Martinez、Porter、Klees 均已取得全文或正式存档稿并核对对应定义；DOI 与出版元数据已交叉核验。其余领域旁证不作为协议成立的必要前提。

---

## 6. 固定六 pair 的三臂初步统一复评

### 6.1 可比范围

固定 pair：`0004、0023、0029、0035、0046、0053`，冻结 D2+D1 expected issue 共 `25` 条，其中 L2 `11` 条。当前快照指 **2026-08-23 创建本 issue 时最新已完整结束**的统一六 pair run；后续新 run 不静默覆盖本表。

为避免拿单轮和三轮能力上界混比，本表只比较同为 `gpt-5.6-luna` 的 **run1**：

| 臂 | 真源 | 轮次 | 发布报告数 |
| :-- | :-- | :--: | --: |
| 当前 evidence-discovery | run `b288a54c000400230029003500460053`，source commit `b288a54c233e0c25a42ec094ec4bcdb881fe4481` | 1 | 75 |
| 重构前 v27 | 已归档 `2026-08-20-luna-full-x3-v27-stream` 的 `method_run1`；归档 commit `2accd7213bad43955314efc6daec8b74e614b03f` | 1 | 77 |
| X1v2 baseline | 同一 v27 pair-wide judge 中的 `baseline_run1`，原始产物为 `baseline-v2/run1/*-luna/record.json` | 1 | 26 |

这不是 hit@3 比较。历史 v27/X1v2 虽有三轮，本节不使用后两轮弥补当前臂只有一轮的问题。

### 6.2 按 pair 复评结果

表中 `K/N/I` 分别为 report-level `VALID_KNOWN / VALID_NOVEL / INVALID`；hit 是 unique expected-issue hit。

| pair | expected / L2 | 当前 hit；K/N/I | v27 run1 hit；K/N/I | X1v2 run1 hit；K/N/I |
| :-- | :--: | :-- | :-- | :-- |
| `0004` | 3 / 2 | **3/3**；4/0/10 | **3/3**；3/0/9 | **2/3**；2/1/1 |
| `0023` | 3 / 3 | **3/3**；3/4/2 | **3/3**；3/2/0 | **3/3**；1/1/0 |
| `0029` | 8 / 3 | **7/8**；10/0/14 | **4/8**；8/0/17 | **4/8**；4/2/1 |
| `0035` | 4 / 0 | **4/4**；8/0/2 | **4/4**；15/0/2 | **2/4**；3/1/2 |
| `0046` | 4 / 1 | **2/4**；3/1/2 | **3/4**；4/1/0 | **1/4**；1/0/3 |
| `0053` | 3 / 2 | **3/3**；9/3/0 | **3/3**；10/3/0 | **2/3**；1/0/2 |
| **合计** | **25 / 11** | **22/25；L2 11/11；37/8/30** | **20/25；L2 10/11；43/6/28** | **14/25；L2 7/11；12/5/9** |

派生指标：

| 臂 | Expected hit | L2 hit | Semantic FP | 有效报告精确率 |
| :-- | --: | --: | --: | --: |
| 当前 evidence-discovery | **22/25 = 88.0%** | **11/11 = 100%** | **30/75 = 40.0%** | **45/75 = 60.0%** |
| v27 run1 | **20/25 = 80.0%** | **10/11 = 90.9%** | **28/77 = 36.4%** | **49/77 = 63.6%** |
| X1v2 baseline run1 | **14/25 = 56.0%** | **7/11 = 63.6%** | **9/26 = 34.6%** | **17/26 = 65.4%** |

### 6.3 相对旧 Judge，改变数字的关键裁断

1. **当前 `0035 / EIS-0035-04`：miss → full hit。** `0035:r1:issue:8` 同时引用 NL5+NL6，主张 cooking time 缺少 data-side representation，并给出没有 variable/state action/effect carrier 的 basis。现有 strict judge 因没有单条复述全部 display/update/cancel 组件而判 partial；按同根因 + diagnostic facet 口径应 full。W1 不构成降级理由。
2. **当前 `0046 / INS-0046-03`：miss → full hit。** issue 4/6 分别给出整个 `UAVSwarmStateMachine` 不可达和声明的 event consumers 不可达，是冻结“六事件消费者因 region 进不去而不可达”的直接根因/后果，不应因 typed property 名不同而拒绝。
3. **v27 `0053 / DIFF-0053-01`：miss → full hit。** `zero_behavior`、wrapper 间无运行迁移和主状态互不可达是同一断连根因的直接表现；旧 judge 要求单条完整复述三个 wrapper，过严。
4. **X1v2 `0023`：0/3 → 3/3。** baseline issue 2 明确指出三个状态之间没有任何运行期转移、模型不能表示状态切换；这直接建立三条 known dead-end expected issue 的共同故障行为。一条报告可分别映射三条原子 ledger，不需要 W2 或 `deadlock` 字样。
5. **X1v2 `0029`：3/8 → 4/8。** baseline issue 5 明确指出跨模式转移没有定义目标复合态的入口子状态，直接覆盖 `EIS-0029-04` 的 default-entry 缺失；另两条 `exit_hwy/exit_urban` 终止抱怨本身可成立，但修复不消除 `INS-0029-05` 的嵌套 FinishState 根因，记 novel 而非 hit。
6. **X1v2 `0053`：1/3 → 2/3。** baseline issue 2 的“主状态之间没有任何条件转移”既命中 wrapper 断连，也直接建立零行为表现；它不需要 inspect 或谓词见证。

### 6.4 INVALID 的主要来源

- 当前与 v27 的 `0004/0029` 大量把已有 transition label 中的 event/condition 再报成“缺 guard/缺 transition”，属于表示层误读；
- `0035` 的 timer start/stop 超出当前冻结模型对象的时钟语义边界；
- `0046/0053` 中把没有 `--` 的 sibling composites 误读成并发 region，或否认 PlantUML `/ effect` 已表达动作；
- X1v2 的主要 invalid 是要求 UML 状态显式 self-loop 才能保持、误读并发区域，以及把正确的全 inactive 合取条件批评为过强。

`VALID_NOVEL` 的典型项包括：未入台账但可成立的状态动作表示不足、额外 MissionRegion 生命周期、未定义的局部退出状态等。它们不增加 expected hit，也不能算 FP。

### 6.5 validity 计数的逐项复核索引

为避免只给汇总数而无法定位，下面列出所有 `INVALID` 与 `VALID_NOVEL`；同一 pair 其余 release 均为 `VALID_KNOWN`。current 使用 `pair:r1:issue:n` 的尾号，v27 使用 finding 语义组，baseline 使用 `baseline_issue_n`。

| 臂 / pair | `INVALID` | `VALID_NOVEL` |
| :-- | :-- | :-- |
| current `0004` | `1,2,3,7,8,9,10,16,17,18` | 无 |
| current `0023` | `1,2`（把顺序叙事过度具体化成两条特定跨 region 边） | `0,3,4,5`（入口解释与缺少可执行 state action，均按 D1 保留） |
| current `0029` | `9-20,24,25`（已有 label/edge 被误报缺失） | 无 |
| current `0035` | `3,9`（冻结模型边界外的 timer 数据/启停语义） | 无 |
| current `0046` | `1,3`（`/ UAV Count Decreased` effect 与 area/state 类型误配） | `0`（目标搜索只有状态描述、无可执行 action） |
| current `0053` | 无 | `2,4,6`（只有状态描述、无可执行 state action，按 D1 保留） |
| v27 `0004` | 旧 emission 中 9 条 unmatched transition/guard/action 误读 | 无 |
| v27 `0023` | 无 | 初始配置解释、PumpState action 表达各 1 条 |
| v27 `0029` | 旧 emission 中 17 条已有 transition/condition 被误报缺失 | 无 |
| v27 `0035` | `Cooking` timer start/stop 两条 | 无；旧判 unmatched 的 6 条 unreachable-component 改归 known |
| v27 `0046` | 无 | target-search action 1 条；旧 root-unreachable 改归 known |
| v27 `0053` | 无 | Pump/Water/Methane state-action 三条；其余旧 unmatched 改归 known |
| baseline `0004` | `baseline_issue_3`（UML 状态保持不要求显式自环） | `baseline_issue_2`（`do/Send` 与一次性发送的 D1 语义差异） |
| baseline `0023` | 无 | `baseline_issue_1`（三 region 同时初始与“首先 PumpState”的 D1 冲突） |
| baseline `0029` | `baseline_issue_7`（“全部 danger inactive”使用 AND 是正确合取） | `baseline_issue_3,4`（局部退出状态无后续，但不是冻结 FinishState 根因） |
| baseline `0035` | `baseline_issue_4,5`（冻结边界外 timer 启停） | `baseline_issue_6`（无物品时 Item Removed 自环） |
| baseline `0046` | `baseline_issue_2,3,4`（并发语义误读、由其派生的初始组合、否认 `/ effect`） | 无 |
| baseline `0053` | `baseline_issue_1,3`（没有 `--` 却判成三个并发 region） | 无 |

---

## 7. 当前数字的证据等级与禁止误读

上述六 pair 表是**一轮单判读者、逐条回看原始 report 与冻结台账后的初步复评**，不是论文终值：

- hit 调整逐条检查了 current `reason/basis`、v27 joint judge 与 X1v2 原始 `issue/where/reason`；
- report validity 使用作者 NL、PlantUML 与 #189 的 D1/D2 边界裁决；D1 仍属于有效发现；
- current run 在 `/runs/` 下，按仓库策略未跟踪；表中保留精确 run id、commit 与报告计数供本机复核；
- 当前没有第二位独立判读者，也没有 Cohen's kappa/一致率；
- 表按 raw release report 统计 FP/precision，尚未补 root-cause deduplicated precision；
- 因此这些数字只能作为协议 sanity check 和六 pair 调试基线，不能直接写成正式实验结论。

历史旧数字（如 current strict `20/25、52/75 FP`，v27 old run1 `19/25、44/77 unmatched`，X1v2 old run1 `8/25、17/26 unmatched`）测量的是不同且更严格/closed-ledger 的关系，不能与本 issue 的 semantic FP 混报。

---

## 8. 落地验收合同

- [ ] 将最终 Pydantic Judge schema 固定为维度 A `FULL/PARTIAL/NONE`、维度 B `VALID_KNOWN/VALID_NOVEL/INVALID`，每项都有 `reason/basis` 与 source refs。
- [ ] Judge prompt 不可见 arm 名、W 等级、谓词族和历史 ledger 命中结果；三臂使用同一输入投影与同一规则。
- [ ] W0/W1/W2 不作为 match gate；W1/X1v2 自由文本允许 full。
- [ ] `PARTIAL` 不进入主 hit，也不进入 FP；单报 Supported Rate。
- [ ] 只有 `INVALID` 进入 semantic FP；另报 Ledger-Unmatched，禁止混名。
- [ ] 对本组六 pair 做第二次独立盲审和冲突仲裁，最终结果不得有 UNKNOWN/PENDING。
- [ ] 同时报 raw-report 与 root-cause-cluster precision、redundancy rate。
- [ ] 完成一致性统计与逐条 audit artifact 后，再将本 issue 初步表升级为正式六 pair 结果。
- [ ] 若用于 v27/X1v2 对比，必须统一重判原始输出，不得复用不同口径旧 FP 数直接相减。

## 9. 决策摘要

1. expected ledger 保留，是 hit/recall 的必要固定分母。
2. 第一维独占 full/partial/none；第二维不再越俎代庖重复 hit/partial。
3. `VALID_KNOWN` 可以是 full 或 partial；是否 hit 只看第一维。
4. `VALID_NOVEL` 是台账外真实问题，不算 hit，不算 FP。
5. `INVALID` 是唯一 semantic FP。
6. 最终结果取消 UNKNOWN；争议在出数前仲裁完成。
7. 当前、v27、X1v2 全部按同一宽语义关系重判，且 W 不参与资格门槛。
