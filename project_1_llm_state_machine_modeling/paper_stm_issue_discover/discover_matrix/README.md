# discover_matrix — 当前有效的台账与基线结果

⭐ **本目录 2026-08-17 整体清空重建。** 活跃区只保留三样东西：**第二版台账**、**它的学术口径文档**、**X1v2 基线在该台账上的结果**。⛔ 第一版台账、v46 主臂、relabel 生产链与全部 v46 时代评测脚本已转入 [archive/r10_ledger_v1_and_v46/](../archive/r10_ledger_v1_and_v46/)（归档不是删除，那里有复活导引）。

## 一、目录

| 路径 | 内容 |
| :-- | :-- |
| [ledger_v2/](./ledger_v2/) | ⭐ **当前唯一有效的台账**（145 条）+ X1v2 在其上的精确命中结果 |
| [docs/](./docs/) | 学术口径：`protocol/`（判定协议、边界裁定、出处政策）· `findings/`（已裁定的发现）· `generations/`（历代事前登记） |

## 二、第二版台账

| 项 | 值 |
| :-- | :-- |
| 条目数 | **145** = D2 **98** + D1 **47** |
| 真源 | [ledger_v2/ledger.json](./ledger_v2/ledger.json) |
| 每条携带 | `D` 档 · `L` 档 · L 档判定依据 · `statement` · 五轴 · 出处族 · 人工裁决理由 · meta review · 所在工作单（指向归档） |
| 出处构成 | `EIS` 90 · `INS` 35 · `VU` 12 · `DIFF` 8 |

它由 321 条三方 D 档判读（`codex` / `claude` / `dsh`）+ 人工逐条 meta review + 人工逐条裁决产出，判为 `D2` 或 `D1` 的全部条目构成；`D0` 与三个 `A0` 出口不入台账。

### 2.1 D 档

`D2` = 有一条可陈述的被违反义务，且拿不出站得住的反驳。`D1` = 两读并立（存在一种与结构事实相容的第二种称职读法）。定义与判定程序见 [issue #189](https://github.com/HansBug/research_ideas/issues/189) §1.3.3 与 `D_PROTOCOL.md`。

### 2.2 ⭐ L 档 —— 145 条全部落在 L0/L1/L2，无例外

**L 档只描述「这个错误处在哪一层」，⛔ 与 scope 无关** —— `D` 与 `L` 两个体系里不存在 scope 的概念，即便换一套方法与论文，两者也应当同样定义、同样可判。定义与逐档文献锚点见 issue #189 §1.3.1：

| 档 | 判据（陈述这个错误需要什么） | 文献锚 |
| :-- | :-- | :-- |
| **L0 · 表面对齐** | 只需比对 NL 词项与模型词项，不做分析 | syntactic consistency（Torre 等 EASE'14）· pattern-matching（Emanuelsson & Nilsson）· 纯词法（Chess & McGraw） |
| **L1 · 结构导出** | 需从模型结构导出一个静态事实，只看单个系统状态 | Structural Verification Task「a single system state」（Hilken 等）· invariant（Baier & Katoen Def. 3.20） |
| **L2 · 行为构造** | 必须给出或排除一条带时间维的行为（轨迹 / 可达性 / 有界检查） | Behavioral Verification Task「a sequence of system states as well as their transitions」· 非 invariant safety 需 finite path fragments（同上 §3.3.2） |

⛔ **旧的「`element/region` → 界外」规则已废止** —— 它把 scope 混进了 level。逐条判定与依据在 [ledger_v2/l_tier.json](./ledger_v2/l_tier.json)（33 条人工逐条判、112 条按定义规则档）。

分布：**L0 71 · L1 35 · L2 39**。D×L：`D2` 48/16/34 · `D1` 23/19/5。

## 三、X1v2 基线在该台账上的结果

被测臂是 **X1v2**（朴素基线第二版：单次提示、无循环、无工具）。网格 = 145 × 6 格（2 个生成模型 × 3 轮）= **870** 位。

| 子集 | `hit@1` | `hit@3` | `hit@all` |
| :-- | --: | --: | --: |
| **全台账（145）** | **59.8%** | **70.3%** | **47.9%** |
| L0（71） | 62.7% | 71.8% | 50.7% |
| L1（35） | 71.9% | 81.4% | 61.4% |
| ⛔ **L2（39）** | **43.6%** | **57.7%** | **30.8%** |
| ⛔ **D2 × L2（34）** | **40.2%** | **52.9%** | **29.4%** |

完整表、按出处族拆分、26 条零命中清单、以及**必须随数字一起报的五条限制**，见 [ledger_v2/X1V2_RESULTS.md](./ledger_v2/X1V2_RESULTS.md)。判定协议（判定前写定）见 [ledger_v2/JUDGING_PROTOCOL.md](./ledger_v2/JUDGING_PROTOCOL.md)，逐条判定依据见 [ledger_v2/x1v2_hits.json](./ledger_v2/x1v2_hits.json)。

## 四、⚠️ 读这些数字前必须知道的

1. ⚠️ **89 条 `EIS-` 沿用既有 588 网格判定**（判定人 J1–J8），其余 **56** 条为本轮逐格人工新判（336 个判定，单人、无第二判读者、无一致性系数）。两部分口径差异无法量化，故报告按出处族分别给出。
2. ⚠️ **`VU-` 一族（12 条）的命中带构造性** —— 该族本身就是从各臂未认领产出里提取的台账漏记，其中 9 条出自 X1 自己。⛔ 不可与其它族混为一个独立测量。
3. ⭐ 本目录**不含任何 v46 数字**。历史上出现过的 `hit@1 60.4%`、`76.2%`、`429`、`380`、`319` 等数一律不是当前口径 —— 它们的来历见归档目录。

## 五、边界（不随台账换代而变）

建模对象是 $M = (S, E, V, Tr, A)$：**无时钟变量 $C$、无不变式 $Inv$、无正交区并发语义**。由此导出的两项永久裁定 —— `00x8` 六个 pair 永久排除（故全量网格恒为 54 pair）、hold-out 永久不用 —— 见 [docs/protocol/nl_scope_rule.md](./docs/protocol/nl_scope_rule.md) 与 [docs/protocol/method_provenance_policy.md](./docs/protocol/method_provenance_policy.md)。
