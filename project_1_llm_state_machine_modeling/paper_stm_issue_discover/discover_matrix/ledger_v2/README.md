# ledger_v2 — ⭐ 本论文当前**唯一**有效的台账

> ⭐ **一句话**：`paper_stm_issue_discover` 这篇论文的缺陷台账只有一份，就是本目录下的 [ledger.json](./ledger.json)，**145 条**（D2 98 + D1 47）。⛔ 仓库里出现的其它任何条目数（99、126、319、321、323、380、429）都不是台账数，含义见 [§六](#六-哪些数字不是台账数)。

## 一、这个目录装了什么

本目录同时是**台账**、**台账的学术口径**、**台账上的唯一基线结果**、以及**台账的完整证据链**。四者放在一起，是为了让「某条缺陷凭什么成立、它是第几层、基线在它上面命中没有、当初是谁怎么判的」四个问题都能在同一个目录里闭合，不必跳到归档区。

| 文件 / 目录 | 角色 | 内容 |
| :-- | :-- | :-- |
| [ledger.json](./ledger.json) | ⭐ **真源** | 145 条，每条内联 `D` / `L` / `L_basis` / `statement` / 五轴 / 出处族 / 人工裁决理由 / meta review / 工作单指针 |
| [l_tier.json](./l_tier.json) | 派生·可复算 | 逐条 L 档判定与依据（33 条人工逐条判 · 112 条按定义规则档），含已废止规则的记录 |
| [JUDGING_PROTOCOL.md](./JUDGING_PROTOCOL.md) | ⭐ 口径 | 命中判定协议。**写定于判定开始之前，判定期间未改动** |
| [x1v2_hits.json](./x1v2_hits.json) | 原始判定 | 本轮 56 条逐格人工新判，每条带 6 格布尔与中文判定依据 |
| [x1v2_grid.json](./x1v2_grid.json) | 派生 | 合并后的 145 × 6 真值网格 |
| [X1V2_RESULTS.md](./X1V2_RESULTS.md) | 报告 | 全部命中表、分档拆分、零命中清单、⚠️ 五条必读限制 |
| [provenance/](./provenance/) | ⭐ **证据链** | 台账是怎么被判出来的：第一版台账、60 份逐 pair 复审、54 份工作单（含全部人工裁决与逐条 meta review）、三方判读包、去重台账、生成与校验工具 |

⚠️ 学术口径文档（判定协议之外的：缺陷分类学、边界裁定、出处政策、历代事前登记）不在本目录，在同级的 [../docs/](../docs/)。

## 二、台账本身

| 项 | 值 |
| :-- | :-- |
| 条目数 | **145** = `D2` **98** + `D1` **47** |
| L 档分布 | `L0` **71** · `L1` **35** · `L2` **39** —— ⭐ 145 条**全部**落在这三档，无第四类 |
| D × L | `D2`: 48 / 16 / 34 　`D1`: 23 / 19 / 5 |
| 出处族 | `EIS` **90** · `INS` **35** · `VU` **12** · `DIFF` **8** |
| 携带人工裁决理由 | 65 条 |

它由 **321 条**三方 D 档判读（`codex` / `claude` / `dsh` 三臂独立判）经人工逐条 meta review 与人工逐条裁决产出；判为 `D2` 或 `D1` 的全部条目构成本台账，`D0` 与三个 `A0` 出口（`FALSE_POSITIVE` / `NOT_A_DEFECT_CLAIM` / `OUT_OF_SCOPE`）不入账。

### 2.1 D 档 —— 这条缺陷主张站不站得住

`D2` = 有一条可陈述的被违反义务，且拿不出站得住的反驳。`D1` = 两读并立（存在一种与结构事实相容的第二种称职读法，构成 undercutting defeater）。定义与判定程序见 [issue #189](https://github.com/HansBug/research_ideas/issues/189) §1.3.3 与 `D_PROTOCOL.md`。

### 2.2 L 档 —— 陈述这个错误需要哪一层

⭐ **L 档只描述「陈述这个错误需要什么」，⛔ 与 scope 无关。** `D` 与 `L` 两个体系里不存在 scope 的概念 —— 即便换一套方法、换一篇论文，两者也应当同样定义、同样可判。定义与逐档文献锚点见 issue #189 §1.3.1：

| 档 | 判据 | 文献锚 |
| :-- | :-- | :-- |
| **L0 · 表面对齐** | 只需比对 NL 词项与模型词项，不做分析 | syntactic consistency（Torre 等 EASE'14）· pattern-matching（Emanuelsson & Nilsson）· 纯词法（Chess & McGraw） |
| **L1 · 结构导出** | 需从模型结构导出一个静态事实，只看单个系统状态 | Structural Verification Task「a single system state」（Hilken 等）· invariant（Baier & Katoen Def. 3.20） |
| **L2 · 行为构造** | 必须给出或排除一条带时间维的行为（轨迹 / 可达性 / 有界检查） | Behavioral Verification Task「a sequence of system states as well as their transitions」· 非 invariant safety 需 finite path fragments（同上 §3.3.2） |

⛔ **旧的「`element/region` → 界外」规则已废止** —— 它把 scope 混进了 level。废止记录与逐条判定在 [l_tier.json](./l_tier.json)。

## 三、X1v2 基线在该台账上的结果

被测臂是 **X1v2**（朴素基线第二版：单次提示、无循环、无工具）。网格 = 145 × 6 格（2 个生成模型 × 3 轮）= **870** 位。

| 子集 | 条 | `hit@1` | `hit@3` | `hit@all` |
| :-- | --: | --: | --: | --: |
| **全台账** | 145 | **59.8%** | **70.3%** | **47.9%** |
| L0 表面对齐 | 71 | 62.7% | 71.8% | 50.7% |
| L1 结构导出 | 35 | 71.9% | 81.4% | 61.4% |
| ⛔ **L2 行为构造** | 39 | **43.6%** | **57.7%** | **30.8%** |
| ⛔ **D2 × L2** | 34 | **40.2%** | **52.9%** | **29.4%** |

⭐ 完整表、按出处族拆分、26 条零命中清单、以及**必须随数字一起报的五条限制**见 [X1V2_RESULTS.md](./X1V2_RESULTS.md)。

⚠️ **读这三个数之前必须知道的两件事**（完整五条在报告里）：

1. ⚠️ **判定来源不齐**：89 条 `EIS-` 沿用既有 588 网格判定（判定人 J1–J8），其余 **56** 条为本轮逐格人工新判（336 个判定，**单人、无第二判读者、无一致性系数**）。两部分口径差异无法量化，故报告按出处族分别给出。
2. ⚠️ **`VU-` 一族（12 条）的命中带构造性** —— 该族本身就是从各臂未认领产出里提取的台账漏记，其中 9 条出自 X1 自己。⛔ 不可与其它族混成一个独立测量。

## 四、⭐ 证据链怎么闭合

```
NL 需求（corpora/）+ 6 个 LLM 生成的 PlantUML
        │
        ├── 60 份逐 pair 人工复审 ──→ provenance/<pair>-review.json
        │        └── 汇总 ──→ provenance/expected_issue_set.json（第一版台账 99 条）──→ EIS 族 90 条
        │
        └── v46 主臂未认领产出（archive/r10_ledger_v1_and_v46/v46/）──→ INS / VU / DIFF 三族 55 条
                 │
                 ▼
        provenance/relabel/  —— 54 份工作单，每份印出该 pair 的候选条目
                 │
                 ├── 三臂独立 D 档判读 ──→ relabel/dtier_rulings.json（321 条）
                 ├── 人工逐条 meta review ──→ relabel/dtier_meta.json
                 └── 人工逐条裁决 ──────→ 工作单 .md 内
                          │
                          ▼
                 ledger.json（145 条 D2+D1）  ←── l_tier.json 给出每条的 L 档
                          │
                          ▼
                 JUDGING_PROTOCOL.md ──→ x1v2_hits.json ──→ x1v2_grid.json ──→ X1V2_RESULTS.md
```

⭐ **台账每一条的 `worksheet` 字段直接指向它的工作单**，例如 `./provenance/relabel/nl_0000/0010.md`。145 条全部指向存在的文件（可用下面 §五 的命令复验）。

⭐ **台账自身是自包含的** —— `statement`、五轴、`D`、`L`、`L_basis`、`verdict_reason`、`meta_review` 全部内联。读数与复算都不需要进 `provenance/`；`provenance/` 只在要追问「这一条当初是怎么定下来的」时才需要。

## 五、复验命令

```bash
cd project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2

# 台账计数、L 档全覆盖、worksheet 全部存在
python3 - <<'EOF'
import json, os, collections
d = json.load(open('ledger.json', encoding='utf-8'))['items']
assert len(d) == 145
assert collections.Counter(v['D'] for v in d.values()) == {'D2': 98, 'D1': 47}
assert collections.Counter(v['L'] for v in d.values()) == {'L0': 71, 'L1': 35, 'L2': 39}
assert not [k for k, v in d.items() if not os.path.exists(v['worksheet'])]
print('✅ 145 条 · D 98/47 · L 71/35/39 · worksheet 全部存在')
EOF

# 证据链可重跑：54 份工作单重新渲染后应逐字节无变化
cd provenance/relabel && python3 generate.py && git status --porcelain . | grep -c '^ M' # 期望 0
python3 -m pytest test_relabel.py -q   # 期望 151 passed / 21 skipped
```

## 六、⛔ 哪些数字**不是**台账数

⚠️ 这些数在仓库历史与归档里都能查到，容易被误当成台账条目数。逐个钉死：

| 数 | 它其实是什么 | 现在还有效吗 |
| :-- | :-- | :-- |
| **145** | ⭐ **台账条目数（D2 98 + D1 47）** | ⭐ **是，唯一有效** |
| 321 | 进入三方 D 档判读的条目数（含最终判 D0 / A0 的） | 是，但它是**判读输入数**，不是台账数 |
| 323 / 380 | 工作单待裁决总览的去重前 / 中间口径 | ⛔ 否，见 [provenance/relabel/DEDUP_ACCOUNTING.md](./provenance/relabel/DEDUP_ACCOUNTING.md) |
| 99 | **第一版**台账 `expected_issue_set.json` 的条目数 | ⛔ 否，已被本台账取代 |
| 126 / 429 / 319 | v46 时代的各种中间口径 | ⛔ 否，来历见 [../../archive/r10_ledger_v1_and_v46/README.md](../../archive/r10_ledger_v1_and_v46/README.md) |
| 54 | pair 数（60 减去 `00x8` 六个先验越界 pair） | 是，但它是 pair 数不是条目数 |

⛔ **本目录不含任何 v46 数字。** 历史上出现过的 `hit@1 60.4%`、`76.2%` 一律不是当前口径。

## 七、边界（不随台账换代而变）

建模对象是 $M = (S, E, V, Tr, A)$：**无时钟变量 $C$、无不变式 $Inv$、无正交区并发语义**。由此导出的两项永久裁定 —— `00x8` 六个 pair 永久排除（故全量网格恒为 54 pair）、hold-out 永久不用 —— 见 [../docs/protocol/nl_scope_rule.md](../docs/protocol/nl_scope_rule.md) 与 [../docs/protocol/method_provenance_policy.md](../docs/protocol/method_provenance_policy.md)。

## 八、变更

| 时间 | 变更 |
| :-- | :-- |
| 2026-08-17 | ⭐ 证据链 `provenance/`（原 `manual_review/`，含 `relabel/`）从冷归档搬回台账目录，`worksheet` 字段同步改为 `./provenance/relabel/…`；本 README 建立 |
| 2026-08-17 | 台账建立（145 条），X1v2 逐格判定完成，第一版台账与 v46 主臂转入冷归档 |
