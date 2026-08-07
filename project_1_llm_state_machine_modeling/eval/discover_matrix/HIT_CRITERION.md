# 命中判据：语义同一性优先于标签一致

本文件是 Discover effectiveness 实验中「一条已发布 issue 是否命中某条 expected issue」的**裁决原则**。它是长期规则，不是某一轮的施工状态；施工进度与 review 状态在对应 GitHub PR / issue 中维护。

相关：[README.md](./README.md)、[GROUND_TRUTH_LIMITATIONS.md](./GROUND_TRUTH_LIMITATIONS.md)（分母的已知缺口）、Issue [#166](https://github.com/HansBug/research_ideas/issues/166)（expected issue 台帐）、Issue [#170](https://github.com/HansBug/research_ideas/issues/170)（谓词设计）、PR [#169](https://github.com/HansBug/research_ideas/pull/169)（Discover 验收）。

---

## 1. 唯一裁决标准

**判定命中的标准是：我们的 assert 所表达的命题，与台帐那条 expected issue 的 `eval_assert` 所表达的命题，是否指向同一个作者源缺陷。**

不是：
- 两者用的谓词是否相同
- 两者的 `evidence_family` / `required_function_families` 是否相同
- 两者的路径集合是否完全相同

## 2. 为什么不看 family 标签

Issue #166 的台帐建立于当前谓词体系**之前**。那时 19 个谓词的定位尚未形成，`required_function_families` 是当时对「需要哪类证据」的粗略标注，用的是 `relation` / `structure` / `effect` 这套早期口径。

台帐 47 条 E1 的 `eval_assert` 全部调用当时的底层查询原语（`transition_exists` 22 次、`transitions` 11 次、`states` 9 次、`initial_child` 6 次、`effect_deltas` 2 次、`path` 2 次），**没有一条使用模拟**。而当前 Discover 产出的是 19 个封闭谓词的调用，其 family 由谓词表查得。

**两套标签之间存在信息代差，不是同一码事。** 因此 family 不一致本身不构成未命中的理由，也不构成方法论问题。这一点已经裁决：代差是预期的。

## 3. 语义同一性的四种成立形态

以 matrix-v18 的 10 条命中为实例，同一性可以合法地以下列任一形态成立：

| 形态 | 含义 | 实例 |
| --- | --- | --- |
| **直接对应** | 两个命题说同一件事，只是谓词不同 | `EXP-0029-GC-001`：台帐「该触发下只应一条迁移且目标是 `lane_change`」，我们「该触发下到不了 `lane_change`」 |
| **合取项之一** | 台帐命题是 `all(...)`，我们证明其中一个合取项为假 | `EXP-0000-IT-001`：台帐要求两个运行模式都有 `Power_Off → FinalState`，我们证明 `HumanDrivingMode` 那一半没有 |
| **负向命题的正向对偶** | 台帐说「不应存在错的边」，我们说「应存在对的边」 | `EXP-0029-IT-001`：台帐 `not transition_exists(cruise, dist_to_exit_2, FinishState)`，我们 `occupancy_after(cruise, dist_to_exit_2, exit_hwy)` |
| **蕴含更根本的原因** | 我们的命题为假蕴含台帐命题为假，且定位到更上游 | `EXP-0006-EA-001`：台帐「攻击完成边应有变量下降」，我们「模型根本没声明 `uav_count`」——无变量则不可能有下降 |

后三种都算命中。判据是逻辑关系，不是形式相同。

## 4. 不成立的形态

以下不算命中，即使路径大量重叠：

- **不同缺陷共用状态名**：一条关于 `HighwayMode` 子状态计数的发现，不能算作关于 `HighwayMode` 内某条迁移目标错误的 expected issue 的命中
- **更弱的命题**：台帐要求「这条边的目标是 X」，我们只证明「这个状态存在」——存在性不蕴含目标正确
- **反向蕴含**：台帐命题为假**不**蕴含我们的命题为假

## 4.5 ⚠️ 已知判据歧义：伪状态的**运行代理**式主张（未裁定，双读法都报）

### 现象

19 谓词闭词表无法把结构主张绑定到**瞬时伪状态**（`Junction*` / `Join*` / `fork*` / `choice*`）。产出方
于是改用**下游可占据后继**作运行代理。实测 **14 / 249 = 5.6%** 的已发布 issue 属此形态，集中在
`0038`(6) / `0018`(4) / `0035`(2) / `0050`(2)。

典型（`run3/0038-gpt` 的 `ISSUE-chargedflash-chargedtrue-no-junction3-flow`）：

> `REQ-011` 要求 ChargedFlash 在 `Charged_true` 条件成立时进入 `Junction3`；**由于 Junction3/Join2 是
> 瞬时伪状态，断言以其后续可占据结果 Fork2 为运行代理**，但 primary 结果为 False。

对应台账 `EIS-0038-03` 的 primary 是
`edge_declared(ChargedFlash, Charged_true, Junction3)` —— **结构主张**。

### 歧义所在

一条 issue 的「命题」该读成哪个？

| 读法 | 判定 | 依据 |
| :-- | :-- | :-- |
| **A：读它引用的 `requirement`** | **算命中**（形态 ①，同一命题、不同谓词） | `REQ-011` 逐字要求的就是台账那个命题 |
| **B：读断言的字面主张** | **不算**（§4「更弱的命题」） | 「运行时到不了」是「边不存在」的更弱形式（边不存在 ⇒ 到不了，反之不成立） |

两种读法都有正当依据，**本文件此前未规定走向**。

### 处置：双读法都报，不单方面裁定

**上限已算**（顺序固定为「先算上限 → 再逐条人工裁定 → 再看活体激活分布」，且后两步只在增量非 0 时做）：

    读法 B（当前，盲判所用）      105/204 = 51.5%
    读法 A 的**极宽上限**          115/204 = 56.4%    增量 +4.9pp
    （上限口径：把代理式 issue 所在格该轮的**全部**未命中位都算命中，实际逐条匹配远低于此）

涉及 10 个位，全在 `EIS-0018-03`(2) 与 `0038` 的四条(8)。

📌 **两条理由使「现在不裁定」是正确处置：**

1. **+4.9pp 不足以让任何结论翻转**（56.4% 仍远低于 70% 目标），所以我在这条歧义上没有达标动机 ——
   而这恰恰是现在把走向写死的最好时机：**在它可能对我有利之前**。
2. 但增量非 0，所以歧义本身必须记录，否则下一代次会重复同一次争论。

**规则（从本版起生效）**：报告中凡涉及覆盖率，**必须并列给出两读法的数**，并标明盲判所用读法。
不得只报对自己有利的那个。若将来某一读法使结论翻转，**必须先由独立裁定给出走向、并说明为什么该走向
不是为了达标**，再使用。

### 相关但**不同**的一件事

`0050-gpt` 的 `ISSUE-M004-front-distance-missing` 也含「代理」一词，但那是另一回事：它说
「不能由路由变量或仅以事件名代理替代」—— 是**拒绝**用代理，不是**使用**代理。统计时不应混入。

## 5. 已知的机械判据风险面（需人工复核的部分）

自动判据（`build_gist.py` 的 `expected_verdicts`）用路径重叠近似语义同一性：

- 台帐 `eval_assert` 含 `event=` 时（**20 / 47**）：要求触发器精确绑定 + 至少一个状态重叠，**不检查 family**
- 不含 `event=` 时（**27 / 47**）：要求期望的每个状态都匹配（容忍一级父子）**且 family 交集非空**

第二支存在代差风险：那 27 条里有 **10 条要求 `relation`**，若系统用 `containment` / `state_declared`（family = `structure`）检出同一缺陷，family 交集为空而被判未命中。这 10 条分布在 9 个 pair：`0008 0009 0010 0018 0020 0038 0047 0049 0058`（category：TR 5、IT 4、GC 1）。

**处理方式**：机械判据的结果不是终局。凡出现下列情形，必须按 §1 人工复核并在运行记录中写明理由：

1. 判为未命中，但该格确实发布了关于同一缺陷的 issue
2. 判为命中，但两个命题经 §4 检查其实不是同一缺陷
3. 台帐条目走无-trigger 分支且 family 不一致

## 6. 已用此原则修正过的结论

- **matrix-v16 / v18 均为 10/10 命中**。此前记录的「v16 9/10 → v18 10/10 改善」不成立：那次未命中来自一份仅覆盖 4 个 pair 的重建 ledger，其中 `EXP-0029-SH-001` 被写成要求 `{AutonomousMode, InitialState}` 两个状态都匹配，而原件只涉及 `AutonomousMode` 一个。
- 六处谓词修复的实测价值在**精度侧**（捏造的已发布 issue 由 5 条降至 0 条，按证据重算、不依赖 ledger），召回侧两轮都是满的。
- 台帐 `EXP-0029-SH-001` 用的正是 `states(path='AutonomousMode.InitialState', exact=True)`，即 **提案路径的存在性检查**。因此「必须绑已声明路径才能命中」这一说法不成立；`containment(AutonomousMode, InitialState)` 与 `state_declared(AutonomousMode.InitialState)` 两种写法都命中同一条。

## 7. ledger 的权威来源

原始 ledger 曾一度被认为丢失，实际一直在 Issue #166 正文所链接的证据 gist 中：

- gist `024ff833314ea6c3d30342290eda5906`，文件 `ledger.json`（370994 字节）
- SHA-256 `03d8756650c079229dacb7fc2d7700ca98fda44f3c4648fd308e4f8e24ac955e`，与 #166 正文「机器总账 SHA-256」逐字符一致
- 已安装于 `.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json`，来源记录见同目录 `PROVENANCE.md`

`expected_issues_reconstructed.json` 自此仅作历史记录。代码在 frozen ledger 存在时一律优先使用它（`expected_ledger_provenance()` 返回 `frozen`）。**不要再基于重建版计算或引用任何命中数字。**
