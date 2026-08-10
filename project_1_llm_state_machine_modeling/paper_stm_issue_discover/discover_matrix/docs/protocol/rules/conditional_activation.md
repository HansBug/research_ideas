# 「条件激活」措辞的谓词选型规则：provenance 与通用性

改动位置：`REQUIREMENT_SPLITTER_PROMPT` 的「NL 措辞 → 谓词」映射表，新增一条。

## 一、规则

> 「X becomes active when \<trigger\>」/「X is entered on \<trigger\>」→ 句子把进入**条件化**了，
> 所以首先要确立的是「制品在该 scope 上到底有没有对该触发作出反应」：
> `event_consumed(source=X, trigger=<事件>)`。**它的 False 就是发现** —— 一个不以该事件为触发的
> scope 不可能在其上加条件，而这正是「仅当…才激活」所禁止的。
>
> `source` **就是 X 本身**，一条需求足够。不得绑 `[*]`（伪初始把主张锚在机器进入任何状态之前，
> 回答的是冷启动问题）。也不得绑 X **内层**的区或子态（内层可能消费该事件而 X 自身进入仍无条件，
> 绑内层会取 True 并恰好掩盖缺陷）。可达性检查（`occupancy_after` / `reaches`）不能作 primary ——
> 它问的是运行能否到达 X，而这对合规模型与无条件模型**都为真**。

## 二、Provenance：引入动机是 `EIS-0047-03` 漏检

按 `CLAUDE.md` §3.5.-1「按引入动机反向标注」：本规则的引入动机确实是 `EIS-0047-03`
（`0047` 的 2/6，claude 臂 0/3）在单 pair 诊断中反复不被发现。**动机据此登记在案。**

⛔ **登记动机不改分母。** 台账全部 126 条记录同等参与度量，没有哪一条因为参与过规则编写
而被单独成带、降级或剔出分母——见
[docs/protocol/method_provenance_policy.md](../method_provenance_policy.md) §一.1，以及仓库根
[CLAUDE.md](../../../../../../CLAUDE.md)「hold-out 永久不用」这条永久裁定。规则站不站得住由
下一节的**通用性**回答（措辞激活面覆盖 30 条格集外记录、横跨 14 个 pair），不由把该
样本挪出分母来回答；挪出分母既不能增加规则的通用性，也会让 `hit@k` 失去跨代次可比性。

## 三、通用性：措辞激活面覆盖 30 条格集外记录，横跨 14 个 pair

度量对象是 **60-pair 语料的 NL 原文**（`representation/reports/llms_emp_r45_java_60/pairs/<pair>/nl.txt`），
不是台账 statement —— 原表标题写「台账 126 条中…的记录」也是错的，措辞出现在 NL 里而非台账文本里。
用同一组正则（`becomes active` / `is entered on` / `only when` /
`when … detected|received|occurs|is met` / 「才激活」）复算：

| 范围 | pair 数 | 其上台账记录数 |
| :-- | --: | --: |
| 60-pair 语料中 NL 含该措辞（已扣 6 个 `00x8`；不扣为 24 pair / 64 条） | **18** | 37 |
| 筛选后格集内 | **2**（`0035` `0047`） | 7 |
| **格集外** | **16** | **30**（其中 14 个 pair 有台账记录） |

格集外有台账记录的 14 个 pair（附记录数）：
`0034`(6) `0014`(4) `0024`(4) `0005`(3) `0007`(3) `0025`(2) `0004` `0015` `0027` `0037` `0044` `0045` `0055` `0057`。

⚠️ 按记忆纪律「回测证明不了通用性」：上表是**措辞的静态分布**，只说明规则不会只对一个样本生效；
**它不证明规则在那些 pair 上有效**。有效性只能由活体运行判定。

本节的 30 条是**通用性证据**，说明这条规则的措辞激活面不限于引入它的那个样本；它们不是
一份可报告的能力分母，能力分母始终是台账的 98 条可判记录。

## 四、迭代过程（三次，前两次的失败原因值得记）

| 代次 | 改动 | 需求里 `event_consumed` | `0047` 命中 |
| :-- | :-- | --: | :-- |
| 基线 | 无 | 0 | **0/3**（其中 1 轮整格崩溃） |
| v26 | 只说「别绑 `[*]`，绑运行时占据的状态」 | **0** | 0/3 |
| v27 | **点名 `event_consumed` 作 primary** | **24** | **1/3** |
| v28 | `source` 收紧到 X 本身，排除 `[*]` 与内层 scope | —— | 见下 |

### v26 为什么完全无效

它只约束了**绑定**，没约束**谓词**。splitter 于是选了 `occupancy_after`（运行可达性），
那条要么被 `initialization_anchored` 门拦、要么被判 `representation_debt` 排除。

⚠️ 更糟的是：它把那条需求**丢弃**了而不是改绑 —— 连基线里那个可见的 `representation_debt`
记录都没留下。**「让模型别那样做」若不同时说「该怎样做」，模型会选择不做。**

### v27 为什么部分有效但不稳定

三轮分别绑了 `[*]`、根复合态、两者都有 —— 规则给了「被进入的复合态，或包含它的那个」两个选项。
命中的那一轮绑的是能取 False 的那个；另两轮绑错。**选项数就是方差来源。**

## 五、这条规则依赖的实测事实（`0047` 上）

模型把 `Collision_Detected` 声明为事件却当**效果**用：

    Idle -> Braking : /Collision_Detected;      ← `/` 前缀是效果，不是触发
    Braking -> Clamping : /Brake_Applied;
    Clamping -> Idle : /Collision_Avoided;
    Idle -> Braking : /Collision_Detected;      ← 同一批迁移重复声明
    Idle -> Braking : /Collision_Detected;      ← 三次

因此没有任何迁移以它为触发，逐 scope 实测：

| scope | `event_consumed(scope, Collision_Detected)` |
| :-- | :-- |
| 根 | **False** ← 发现 |
| `CollisionAvoidanceSystem`（= X） | **False** ← 发现 |
| `CollisionAvoidanceSystem.Frontend`（内层） | **True** ← 若绑这里会掩盖缺陷 |

📌 最后一行是「不得绑内层」那条禁令的实测依据，不是推测。
