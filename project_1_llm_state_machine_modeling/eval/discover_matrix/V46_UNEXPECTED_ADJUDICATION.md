# v46 意外发现（unexpected）逐条裁定

对 v46 全量 324 格产出中、**未匹配到任何台账记录**的 293 个同质簇逐条人工裁定。
数据在 [unexpected_verdicts/](./unexpected_verdicts/)，本文件只写结论与判据。

## 一、最重要的一条结论

**293 个簇里只有 26 个（8.9%）是真实的台账漏记，归并到根因后只有 6 条。**
而占比最大的一类（117 簇，39.9%）根本不是模型缺陷，是**我们自己的转换管线的表示债务**。

这条结论推翻了本轮八个判定组中七个组的初判。推翻它的是一个事实：

**`model.fcstm` 不是作者原件，`stm0.puml` 才是。** R4.5 下沉会把 PlantUML 的整条迁移标签
压成一个事件名，该债务在每份制品的 `fcstm_meta.json` → `source_static_reason_codes` 里已声明
（`R45.DEBT.opaque_transition_label_semantics`，全语料 116 次，是最高频的债务码）。

最清楚的证据是 pair 0029 的作者源第 33 行：

```
collision_avoidance_deactive --> collision_avoidance_active :
    pedestrian_detected | dist_to_rear<5 & vel>30 | dist_to_front<15 & highway_mode | dist_to_front<10 & urban_mode
```

作者写的是一条**完全合法的析取守卫**，NL 12 的四个激活源一个不缺。发现模型报的
「四个激活源被压成一个融合事件、模型无法只凭其中一个激活」，指的是**下沉之后**的形态。
[FUSED_EVENT_POLICY.md](./FUSED_EVENT_POLICY.md) 对此已有既定裁定：断言阶段必须接受合并事件
并记录表示限制，而**「表示限制被如实记录、但记录本身不构成发现」**。

同理，`variable_declared(X)=False` 这一族**没有判别力**：PlantUML 无变量声明语法，
全语料 33 份 `model.fcstm` 的 `def` 只有转换器注入的 `R45RouteToken`（`grep -h "^\s*def " */model.fcstm` 可复算）。
既定分界是**作者源有没有表达该量**——0036 的 `/ UAV Count Decreased` 判 E3 表示债务，
0006 的「作者源里连递减文本都没有」才判真缺陷。

## 一之二、⚠️「下沉」指什么——不是置信度分级

**「下沉（lowering）」是数据准备阶段的 PlantUML → FCSTM 编译动作，与 discover 流水线的
置信度、降级、成熟度分级毫无关系。** 容易误读，此处钉死：

```
作者手写 stm0.puml  ──R4.5 转换（下沉）──▶  model.fcstm  ──▶  discover 流水线读这一份
   （真正的作者原件）                        （编译产物）
```

R4.5 是 **PlantUML 表达力 > FCSTM 表达力** 时的有损编译。PlantUML 允许在一条迁移标签里
写 `a | b & c`、写 `trigger / effect`、写 `trigger [guard]`；FCSTM 的 `event` 是一个原子标识符，
装不下这些，于是整条标签被塞进一个事件名。这不是「输出了但不够确信」，而是
**信息在我们自己的编译步骤里被压平了，且压平这件事被如实登记在案**——
每份制品的 `fcstm_meta.json` → `source_static_reason_codes` 里写着债务码。

| 债务码 | 全语料次数 | 含义 |
| :-- | --: | :-- |
| `opaque_transition_label_semantics` | 116 | 整条迁移标签被压成一个不透明事件名 |
| `composite_source_activation_dispatch` | 56 | 复合态出边的激活派发被改写 |
| `opaque_state_body_semantics` | 54 | 状态体描述行被压进状态名 |
| `missing_explicit_initial` | 32 | 缺显式初始，注入伪初始态 |
| `concurrent_region_semantics` | 18 | 并发区语义被改写 |

所以「表示债务」这一裁定的准确含义是：**断言报告的现象在 `model.fcstm` 上客观为真，
但它描述的是我们的编译损失，不是作者建模的缺陷。** 发现模型没做错——它看到什么报什么；
错的是把这类报告计入「模型缺陷」。

## 二、293 簇终态

| 裁定 | 簇数 | 占比 | 含义 |
| :-- | --: | --: | :-- |
| `REPRESENTATION_DEBT` | 117 | 39.9% | 作者源已逐字表达，融合/缺失来自 R4.5 下沉，非模型缺陷 |
| `NO_NL_BASIS` | 90 | 30.7% | 事实成立但 NL 不要求，属过度规定 |
| `FALSE_POSITIVE` | 43 | 14.7% | 断言所指元素其实存在，主张与制品相反 |
| `VALID_UNRECORDED` | 26 | 8.9% | **真实的台账漏记** |
| `MERGE_INTO_LEDGER` | 8 | 2.7% | 是已有台账记录换了个谓词，应归并 |
| `UNCERTAIN` | 6 | 2.0% | 证据不足或仓库自身判据有张力 |
| `OUT_OF_SCOPE` | 3 | 1.0% | 依赖正交并发 / 不变式，在 M 边界外 |

逐 pair 分布见 [unexpected_verdicts/by_pair.tsv](./unexpected_verdicts/by_pair.tsv)。

### 表 A：裁定 × 稳定性

意外发现不带 A/B/C 分层——A/B/C 只作用于**台账记录的命中位**，而意外发现按定义没匹配台账。
这批上真正存在且可比的分级维度是**稳定性**：该簇在 6 个格（2 臂 × 3 轮）中出现了几次，
与仓库既定的 `@k` 口径同源。

| 裁定 | 1/6 | 2/6 | 3/6 | 4/6 | 5/6 | 6/6 | 合计 | ≥4 格 |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| 真漏记 | 17 | 6 | 3 | 0 | 0 | 0 | 26 | **0%** |
| 应并入 | 4 | 2 | 0 | 0 | 2 | 0 | 8 | 25% |
| 表示债务 | 77 | 17 | 8 | 10 | 3 | **2** | 117 | 13% |
| 无 NL 依据 | 53 | 18 | 6 | 13 | 0 | 0 | 90 | 14% |
| 假阳性 | 21 | 14 | 2 | 2 | 4 | 0 | 43 | 14% |
| 越界 | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0% |
| 待定 | 4 | 1 | 0 | 1 | 0 | 0 | 6 | 17% |
| **合计** | **179** | 58 | 19 | 26 | 9 | 2 | 293 | |

两条读法：

1. **179/293（61%）只出现在 1 个格里** —— 绝大多数多报是单次采样噪声，不是系统性行为。
2. **26 条真漏记全部 ≤3 格，无一进入 ≥4 格；而唯二的 6/6 全满格是表示债务。**
   这不奇怪：表示债务是制品的确定性属性，每次都能看见；真正的新发现靠的是采样运气。
   **含义是——即便模型确实找到了台账外的真缺陷，它也找得不稳。**

### 表 B：谓词族 × 裁定

（一个簇可含多个谓词族，故行和 > 293。「有效率」= 真漏记 / 该族簇数）

| 谓词族 | 真漏记 | 应并入 | 表示债务 | 无NL依据 | 假阳性 | 越界 | 待定 | 合计 | 有效率 |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| `reaches` | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 7 | **86%** |
| `event_consumed` | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 50% |
| `initial_target` | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 4 | 25% |
| `event_declared` | 17 | 3 | 66 | 40 | 31 | 0 | 2 | **159** | 11% |
| `state_declared` | 1 | 1 | 3 | 22 | 2 | 0 | 1 | 30 | 3% |
| `variable_declared` | **0** | 1 | **39** | 2 | 7 | 0 | 0 | 49 | **0%** |
| `action_declared` | 0 | 2 | 0 | 14 | 1 | 0 | 0 | 17 | 0% |
| `edge_declared` | 0 | 0 | 4 | 6 | 1 | 0 | 0 | 11 | 0% |
| `persists_until` | 0 | 1 | 0 | 3 | 0 | 0 | 1 | 5 | 0% |
| `cardinality` | 0 | 0 | 3 | 0 | 0 | 1 | 1 | 5 | 0% |
| `effect_declared` | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 4 | 0% |
| `stays_in` / `invariant` / `containment` | 0 | 0 | 0 | 1 | 1 | 2 | 1 | 5 | 0% |

**结论很干净：存在性谓词（`*_declared`）在本语料上几乎全是噪声，可达性 / 结构谓词才有产出。**
原因就是下沉——`*_declared` 问的正是「某标识符在不在」，而这恰恰是 R4.5 压平时最先失真的东西。
`variable_declared` 尤其应当剔除或改造：49 簇零产出，其中 39 簇是纯表示债务。

### 表 C：三大类的内部细分

| 大类 | 子类 | 簇数 | 中位出现 | ≥4 格 |
| :-- | :-- | --: | :-- | --: |
| **表示债务 117** | `D2` 析取守卫被压成单一事件名 | 64 | 1/6 | 7 |
| | `D1` 守卫文本未成为变量声明（PlantUML 无变量声明语法） | 39 | 1/6 | 6 |
| | `D3` `trigger / effect` 标签未被切分，触发与效果焊成一个事件名 | 9 | 1/6 | 0 |
| | `D4` R4.5 注入伪态 / 区语义导致的结构与计数偏移 | 5 | 3/6 | 2 |
| **无 NL 依据 90** | `N1` 命名字面主义：NL 的统称词 / 语境状语被当成必须存在的同名元素 | 24 | 1/6 | 0 |
| | `N2` 相位过度指定：NL 只解释状态含义，却要求 `during`/`entry` 动作 | 20 | 1/6 | 1 |
| | `N4` 合取项被要求拆成独立事件（会把 AND 变 OR，见 R-CONJ） | 19 | 2/6 | 6 |
| | `N3` 范畴错置：变量当事件 / 动作当事件 | 19 | 1/6 | 6 |
| | `N0` **谓词操作化产生的义务，NL 并未要求（谓词侧待修）** | 4 | 1/6 | 0 |
| | `N5` 断言锚在不存在的元素上，结论空洞真 | 4 | 1/6 | 0 |
| **假阳性 43** | `F2` 命名变体：元素已在，仅字面不同 | 21 | 1/6 | 0 |
| | `F4` 作者源已表达，主张与制品相反 | 17 | 2/6 | 6 |
| | `F1` 元素以 `action` 存在，路径清单看不见 | 4 | 2/6 | 0 |
| | `F3` 谓词锚点错置 | 1 | 1/6 | 0 |

`N0` 单列的理由：这 4 条（`0054-1` `0054-5` `0046-8` `0026-3`）的义务来自**谓词被操作化的方式**
而非 NL，其中 `0054-5` 是构造性不可满足（`NL 2/10` 恰恰许可该迁移，谓词却禁止它）——
按 [CLAUDE.md](../../../CLAUDE.md) §13 属「多道门交集为空」类缺陷，应登记为谓词侧待修项，
不能只当成一次过度规定。

## 三、6 条真实台账漏记（根因级）

26 个 VALID 簇归并后只有 6 条。**簇数不是缺陷数**——同一个缺陷会以不同谓词、不同命名、
不同 roll-up 粒度反复产出，压缩比约 4:1。

| 根因 | pair | 缺陷 | 作者源判据 |
| :-- | :-- | :-- | :-- |
| `0017-FUSE` | 0017 | 作者两个区都只写泛化 `collision detected`，三种检测被塌缩 | `stm0.puml:4,9`；对照 0057 作者分立写全三种，证明可分是通行读法；0017 台账 0 条 |
| `0047-FUSE` | 0047 | 作者三个区都只写泛化 `Collision Detected` | `stm0.puml:5,12` |
| `0023-REGION` | 0023 | 三个替代子态写成三个并发区默认入口，区间零迁移 | `stm0.puml:4-8` 无任何区间迁移；台账 0 条 |
| `0022-EXTRA` | 0022 | 自增顶层态 `PoweredOn`，上电未直达 `Operate` | `stm0.puml:2-3`；台账 0 条 |
| `0014-ACT` | 0014 | NL 3「发出 Obstacle Detected 信号」被降级成状态描述行 | `stm0.puml:26` 写 `EmergencyStopping: Obstacle Detected`（描述行），对照 0054 作者写 `do/Send Obstacle Detected`；台账已记同族 EIS-0014-03/04，漏此第三条 |
| `0057-ENTRY` | 0057 | CA 入口用自造聚合事件，单一具体检测无法激活 CA | `stm0.puml:22` `[*] --> CA : Possible collision detected`。⚠️ 谓词形式是弱代理（进入 CA 的边源在 CA 之外），实质结论成立但形式不精确 |

**待裁定 1 条**：`0056-1`（SearchState 多出 `NoIntercept`/`Intercepted` 记账区）。
仓库自身人工复核内部有张力——`0056-review.json` 的 diff#3 把它判为 `extra` 过度规约，
diff#0 又把同一处的 `cardinality(SearchState,3)=False` 归为谓词缺口。两种口径给出相反结论，
不自行裁定。

**应并入已有台账 8 簇 / 10 条根因**：见 [final_rootcause.tsv](./unexpected_verdicts/final_rootcause.tsv)。
其中 `0036-8` 与 `0006-2` 是同一缺陷换谓词（`terminates` → `persists_until`）——
匹配器按谓词签名归并，换谓词就漏配，这是**匹配环节**的问题，不是台账漏记。

## 四、非发现类 267 簇的失效模式

按可改进性排序，这批才是对流水线有价值的信号：

| 失效模式 | 簇数 | 说明 |
| :-- | --: | :-- |
| 表示债务被当成模型缺陷 | 117 | 断言锚在下沉后的形态上。**根治办法是让断言阶段能看到 `stm0.puml`，或在谓词层区分「作者未表达」与「下沉未保留」** |
| 命名字面主义 | ~21 | 把 NL 的统称词/语境状语当成必须存在的同名元素：`Flight`（"During flight"）、`user_actions`（"based on user actions"）、`region`（"three region"）、`collision_avoidance_controls` |
| 相位过度指定 | ~18 | 要求 `during`/`entry` 动作，而 NL 只是在解释状态含义（"indicating that…"、"where the pump is…"）。参考 PlantUML 本身也只用 state description 行 |
| 范畴错置 | ~15 | 把变量当事件、把动作当事件（`dist_to_front` 是被比较的量不是信号；`Send` 是输出动作不是输入事件） |
| 合取项误当独立触发 | 19 | 见下节 R-CONJ |
| 断言锚在不存在的元素上 | 3 | 如 0057-2/3/4 锚在虚构的 `Inactive` 状态，结论是空洞真 |

## 五、本轮确立的两条裁定规则

### R-CONJ：合取融合按变量框架计，不按事件框架计

判据不是「行为是否等价」，而是**这条断言若被采纳去修，修出来的东西对不对**：

- NL 用 `or` 并列备选触发（NL 12）→ 融合后无法只凭其一激活 → 拆开是正确修法 → 事件框架成立。
- NL 用 `and` 连接条件（NL 13）→ 若拆成三个独立事件，任一个都能触发 → **把 AND 变成了 OR，
  比现状更违反 NL** → 事件框架指向错误修法。
- 同一处的真实缺口按 M 的 `V` 计（NL 称之为 condition），**同一缺口只计一次**。

这条规则由 NL 自己的措辞推出（称 condition 就归 `V`，称 alternative trigger 就归 `E`），
不由「哪种算法更方便」决定。四个判定组曾在同一形态上给出两种答案，据此统一。

### 路径清单不含动作，涉及 A 元素的主张必须回读原件

证据包的路径清单只列 `state` / `event` / `variable`，**不列 action**。据此判「模型未声明 X」
在三份 train-control 制品（0004 / 0044 / 0054，同一份 NL）上系统性出错——
`Send`、`SendObstacleDetected`、`EmergencyStopSendObstacleDetected` 全部以状态局部
`during abstract` 存在。本轮因此翻转 5 条，其中 `0054-3` 由「真发现」翻为假阳性。

## 六、可复算路径

```bash
cd project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples
grep -h "^\s*def " */model.fcstm | sort | uniq -c          # → 33× R45RouteToken，无作者变量
grep -ho 'R45\.DEBT\.[a-z_]*' */fcstm_meta.json | sort | uniq -c | sort -rn
sed -n '33p' llms_emp_feedback_final_0029/stm0.puml         # → 合法析取守卫
```

台账权威源是 [manual_review/expected_issue_set.json](./manual_review/expected_issue_set.json)（126 条）；
同目录 `expected_issues_reconstructed.json` 只覆盖 4 个 pair，[HIT_CRITERION.md](./HIT_CRITERION.md) §7
明令禁止用它算命中。

## 七、这次裁定自身的可靠性边界

1. **八个判定组的质量不齐。** 只有 2 组（G1、G7）主动回读了 `model.fcstm`，只有 1 组（G6）
   回读了 `stm0.puml` 并查了 [FUSED_EVENT_POLICY.md](./FUSED_EVENT_POLICY.md)。表示债务这条
   主结论来自 G6 一家，但它给的四条断言我已逐条独立复算（见 §六），全部证实。
2. **`grep` 只能定位不能裁定。** 我自己按 `front_distance` 检索 0010 的作者源、得出「作者源亦无、
   可能真缺陷」，实际作者写的是 `Front Distance > 10`（有空格）。逐条读原文行才改正。
   本文件所有作者源判据都标了行号，可逐条复核。
3. **6 条真发现里有 1 条（`0057-ENTRY`）的谓词形式是弱代理**，已在表中标注。
4. **`UNCERTAIN` 的 6 条没有强行裁定**，其中 `0056-1` 是仓库自身两份判据打架，需人工定夺。
