# ledger_v2 — ⭐ 本论文当前**唯一**有效的台账

> ⭐ **一句话**：`paper_stm_issue_discover` 这篇论文的缺陷台账只有一份，就是本目录下的 [ledger.json](./ledger.json)，**145 条**（D2 98 + D1 47）。⛔ 仓库里出现的其它任何条目数（99、126、319、321、323、380、429）都不是台账数，含义见 [§六](#六-哪些数字不是台账数)。

## 一、这个目录装了什么

本目录同时是**台账**、**台账的学术口径**、**台账上的唯一基线结果**、以及**台账的完整证据链**。四者放在一起，是为了让「某条缺陷凭什么成立、它是第几层、基线在它上面命中没有、当初是谁怎么判的」四个问题都能在同一个目录里闭合，不必跳到归档区。

| 文件 / 目录 | 角色 | 内容 |
| :-- | :-- | :-- |
| [ledger.json](./ledger.json) | ⭐ **真源** | 145 条，**高度自包含**——只看 NL 与 PlantUML 源码即可完全读懂，逐字段见 [§2.3](#23-每条台账带什么) |
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

### 2.3 每条台账带什么

⭐ **判据是「只看 `nl.txt` 与 `stm0.puml` 就能把这条缺陷完全搞明白」**，不需要翻任何别的文件。

| 字段 | 内容 |
| :-- | :-- |
| `id` · `pair` | 条目号与所属 pair |
| `pair_context` | 该 pair 的完整定位：`nl_id`（NL01–NL10）· `nl_sha8`（NL 原文哈希，机械判同用）· `model_source` / `model_name`（上游 xlsx 的 A、B 列）· `generator_llm`（xlsx 的 H 列，即写出这份被评审制品的 6 个 LLM 之一）· `nl_file` / `stm0_file` 相对路径 |
| ⭐ `summary` | **一句话版**：点名具体元素与行号，指出被违反的是哪一条义务 |
| ⭐ `detail` | **长篇版**：现象落在哪几行 · 被违反的义务（逐字引 NL 原句或引建模语言的具体规定）· 后果 · 根因 · 已考虑并排除的第二读法 · 与同 pair 其它条目的分工 |
| ⭐ `D_basis` | 为什么是这个 D 档。`D2` 要说明反驳为何不存活；`D1` 要写出那第二种读法**具体是什么** |
| ⭐ `L_basis` | 为什么是这个 L 档：陈述这个错误具体需要什么（词项比对 / 静态结构导出 / 构造或排除带时间维的行为） |
| `axes` · `origin_family` | 五轴分类与出处族 |
| `worksheet` | 指向 `provenance/relabel/` 下该条裁决所在的工作单 |
| `_source_text` | 原始判读文本**逐字保留**（`statement` / `verdict_reason` / `meta_review` / `L_basis_rule` / `L_decided_by`），供逐条对照审计改写是否忠实 |

⛔ **四段自然语言里不使用只有内部才懂的代号** —— 不写 `D2-lit`、`A2`、`§6.5`、`同族既有处理`、`R45RouteToken` 这类简写；引外部依据一律写全（如 UML 2.5.1 的具体条款内容、issue #189 §1.3.1）。⭐ 这一条由 §五 的复验脚本机械检查。

### 2.4 pair ↔ NL ↔ 生成模型的完整对应

⭐ **pair 号 = 上游 xlsx 行号 − 2**（工作簿 [Experiment Results.xlsx](../../corpora/seed_library/llms-emp-stm-subset/assets/raw/drive_download/)，sheet `STM Results`，表头第 1 行、数据第 2–61 行）。60 个 pair 由 10 份 NL 各交给 6 个 LLM 生成而来。

⛔ **NL 分组按 NL 原文的哈希判定，不按 pair 号末位。** `0002` 与 `0013/0023/0033/0043/0053` 同属 NL06，`0003` 与 `0012/0022/0032/0042/0052` 同属 NL09 —— 上游表在 GPT-4o 那一段把 Pump Control 与 HSUV 的顺序排反了，其余五段顺序一致。

| NL | `nl_sha8` | Model Source | Model Name（xlsx B 列） | 6 个 pair | 台账条数 |
| :-- | :-- | :-- | :-- | :-- | --: |
| NL01 | `3110cbcf` | Real-Time Software Design… | state machine for Train Control | 0004 0014 0024 0034 0044 0054 | 26 |
| NL02 | `abb20a21` | HSTBS | State machine diagram of the base brake subsystem | 0001 0011 0021 0031 0041 0051 | 4 |
| NL03 | `a01c022f` | DSCS | UAV swarm state machine diagram | 0006 0016 0026 0036 0046 0056 | 15 |
| ⛔ NL04 | `6af3966c` | DCS | Digital camera state machine diagrams | 0008 0018 0028 0038 0048 0058 | **0（先验越界，永久排除）** |
| NL05 | `b7425c44` | HLDCS | autonomous mode | 0009 0019 0029 0039 0049 0059 | 31 |
| NL06 | `a391765d` | Real-Time Software Design… | Pump Control state machine | 0002 0013 0023 0033 0043 0053 | 19 |
| NL07 | `49854d04` | HLDCS | Collision avoidance sub-machine state diagram | 0007 0017 0027 0037 0047 0057 | 13 |
| NL08 | `f1c3dc88` | HLDCS | high-level driving module | 0000 0010 0020 0030 0040 0050 | 20 |
| NL09 | `9fe426ba` | HSUV | Hybrid Sport Utility Vehicle, HSUV | 0003 0012 0022 0032 0042 0052 | 5 |
| NL10 | `934e19bd` | MOCV | Microwave Oven Control with entry and exit actions | 0005 0015 0025 0035 0045 0055 | 12 |

**生成模型**按 pair 号末位所在的段落分：`0x` GPT-4o · `1x` GPT-4 · `2x` Llama · `3x` Kimi · `4x` DeepSeek · `5x` Claude（xlsx 的 H 列，每条台账的 `pair_context.generator_llm` 里逐条记着）。台账按生成模型分布：GPT-4o 27 · GPT-4 29 · Llama 25 · Kimi 26 · DeepSeek 20 · Claude 18。

⭐ **NL04 恰好就是 `00x8` 那六个 pair** —— 它的 NL 要求 fork/join 与秒级时间约束，忠实模型在 $M = (S, E, V, Tr, A)$ 里无法表示，故先验永久排除（见 [§七](#七边界不随台账换代而变)）。⭐ 这一点有一条独立交叉验证：第一版台账 126 条里落在 NL04 上的恰好 27 条，与 `126 − 27 = 99` 那个扣除数逐个吻合。

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

当前同模型的 v26-dnorm/X1v2 三轮对照不是这张 145 × 6 历史精确网格；它单独记录在 [paper1 Luna 全量报告](../../reports/2026-08-19-luna-full-x3-v26.md)，两种 baseline 表不得混合。

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

# 自包含性：四段齐全、档位自洽、不含内部代号
python3 - <<'EOF'
import json, re, collections
d = json.load(open('ledger.json', encoding='utf-8'))['items']
F = ('summary', 'detail', 'D_basis', 'L_basis')
assert all(v[f] and v[f].strip() for v in d.values() for f in F), '四段有空'
assert all(v['D_basis'].startswith('判 ' + v['D']) for v in d.values()), 'D_basis 与 D 不符'
assert all(v['L_basis'].startswith('判 ' + v['L']) for v in d.values()), 'L_basis 与 L 不符'
JARGON = r'D2-(lit|lang|impl|dom|norm)|(?<![A-Za-z])(A2|B1|P3)(?![A-Za-z0-9])|同族既有处理|R45RouteToken|NL-[ML]\d|(?<![A-Za-z])E2[ab](?![A-Za-z])'
bad = [(k, f) for k, v in d.items() for f in F if re.search(JARGON, v[f])]
assert not bad, f'四段里残留内部代号: {bad[:5]}'
assert all(re.search(r'`[^`]+`|:\d+|全篇|全文', v['summary']) for v in d.values()), 'summary 不够具体'
print('✅ 145 条四段齐全 · 档位自洽 · 无内部代号')
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
| 2026-08-17 | ⭐ **裁定：v46 主臂不在本台账上重测**（用户裁定）。它是历史臂，重测产出不进当前结论。⚠️ 由此产生的口径限制仍然为真：本文**没有**两臂在同一台账上的对照，X1v2 的数字是单臂读数，⛔ 不可与 v46 的任何历史数字相减 |
| 2026-08-17 | ⭐ 证据链 `provenance/`（原 `manual_review/`，含 `relabel/`）从冷归档搬回台账目录，`worksheet` 字段同步改为 `./provenance/relabel/…`；本 README 建立 |
| 2026-08-17 | 台账建立（145 条），X1v2 逐格判定完成，第一版台账与 v46 主臂转入冷归档 |
