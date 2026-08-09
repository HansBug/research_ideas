# v44 事前登记（写于启动前，随代码一同推送）

## 为什么有这一代

v43 作废。它加的 `NamedElement._one_element_per_row` validator 用词法判据冒充语义判断，
在 `0014` 上打死一个**完全正确的回答**（规范逐字引用的信号名 `"Arrived/Stop, Send Arrived"`
天然含逗号，其 `declared_match` 非 null 且正确），18/18 撞死、5 格耗尽。落盘的 24 格也可能是
被迫改写 `named_elements` 才通过的，因此**整代数据不可用**。

v44 = v43 的两项改动**保留**，但把「一行一个要素」从 validator 迁到
description + 生成端 prompt + **评审端 prompt**（CLAUDE.md §11）。

## 基线：v41，同 6 pair

97 判定位，**命中 57 = 58.8%**；全分母 102 位则 57/102 = 55.9%。
分段（修好的 `loss_stages`，按绑定与期望真值判）：① 6 ｜ ② 14 ｜ ③ 0 ｜ ④ 1 ｜ ⑤ 7 ｜ ⑥ 0 ｜ ⑦ 12。

## 本轮改动

1. `named_elements` 一行一个要素——**纪律**在 `name_in_sentence` / `declared_match` 的
   description 与 splitter prompt，**检查**在 requirement reviewer prompt（新增条款），
   纠正走既有修订循环。**schema 里没有任何相关 validator。**
2. 关系缺失类主张用结构谓词（converter prompt 例外条款，v43 未验证，本轮继续）。
3. responder：`parsed` 缺失时从 `raw.tool_calls` 重放校验，让被库吞掉的真实 `ValidationError`
   浮出来且不被误判为可重试。

## 判据（分母 102，基线 57）

| 档 | 位数 | 判定 |
|:--|:--|:--|
| ≤ 61 | 基线 +4（一倍噪声底） | **无效** |
| 62 – 66 | | 弱效 |
| 67 – 71 | | 部分成立 |
| **≥ 72（70.6%）** | | **达标** |

## 机制判据（优先于分数；机制未动则总分变化不得归因于本轮）

| # | 判据 | v41 | 达成线 |
|:-:|:--|--:|:--|
| 1 | `0020` 格里 `human steering cmd` 与 `brake pressed` **各占一行且 `declared_match` 均 null** | 0/6 | **≥ 4/6** |
| 2 | `EIS-0020-02` 命中 | **0/6** | **≥ 3/6** |
| 3 | `0014` 六格全部落盘（v43 全耗尽） | — | **6/6** |
| 4 | `0014` 的 `named_elements` 里 `"Arrived/Stop, Send Arrived"` 仍作为**一行**出现且 `declared_match` 非 null | — | **≥ 4/6**（撤门后它必须被当成正确答案接受） |
| 5 | `0039` 三个 v41 静默格发布 issue ≥1 | 0/3 | **≥ 2/3** |
| 6 | 降级格数 | 0 | **= 0** |

## 回归红旗

- 任一在 v41 达 `hit@all = 1` 的记录掉下来即为回归，不论总分。
- 耗尽格 > 2 即判本轮某项改动过紧，须定位并降级后重跑。

## 本轮射程外（其变化不得归因于本轮）

- ⑦ 的 12 位（`EIS-0014-03`×6、`EIS-0049-01`×5、`EIS-0014-04`×1）：台账写法机械不可判，
  已人读确认为真未命中。
- ② 里的 `guard_distinguishable` 9 位（`EIS-0039-02`×5、`EIS-0049-03`×4）：无针对性改动。
