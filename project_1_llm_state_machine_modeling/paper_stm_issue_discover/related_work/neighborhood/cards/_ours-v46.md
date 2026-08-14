# 卡片 · **我们自己**（v46 discover 流水线）

⚠️ **这不是一篇外部工作。** ⭐ 它按 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 的同一套字段写，⭐ 目的是让 [pipeline_forms.md](../pipeline_forms.md) 的对照表有「我们」这一行 —— ⛔ 没有这一行就没法比。

⭐ **证据级别在本卡里全部是 M**：数据来自本仓库自己的实现与 v46 运行记录，⛔ 不是从论文里读来的。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `_ours-v46` |
| 名称 | paper1 · `discover` 反馈循环 v46 |
| 实现 | [`pipeline/feedback_loop/src/paper_stm_feedback_loop/discover/`](../../../pipeline/feedback_loop/src/paper_stm_feedback_loop/discover/) |
| `artifact_type` | ⭐ pyfcstm DSL 状态机（FSM / HSM / EFSM） |
| `task` | ⭐ **缺陷检测**（模型 vs 自然语言需求） |
| `boundary` | ⭐ `界内`（$M = (S,E,V,Tr,A)$，⛔ 无时钟无并发） |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ LangGraph，**10 个节点**）

```
[确定性] prepare
   → [LLM] split_requirements  ⇄  [LLM] review_requirements
   → [LLM] convert_assertions  ⇄  [确定性] precheck_and_seal
                               ⇄  [LLM] review_assertions
   → [确定性] release_results → [确定性] bind_attribution
   → [LLM] adjudicate_results → [确定性] publish
```

⭐ **10 个节点 · 5 个 LLM · 5 个确定性。**

⚠️ 伞 PR 里习称「八阶段循环」，⛔ 那个数不含 `prepare` 与 `publish`。⭐ 本卡按实现里的节点数报 **10**，⛔ 与外部工作对照时用这个数。

### B2 · 每次 LLM 调用的角色

| 节点 | 角色 |
| :-- | :-- |
| `split_requirements` | ⭐ **抽取器**（NL → 原子需求）+ **规划者**（给每条选谓词） |
| `review_requirements` | ⛔ **评审者**（LLM 自评） |
| `convert_assertions` | ⭐ **翻译器**（需求 → 形式化断言脚本） |
| `review_assertions` | ⛔ **评审者**（LLM 自评） |
| `adjudicate_results` | ⭐ **裁决者**（把求值结果判成「是不是一条发现」） |

### B3 · prompt 策略

`few-shot`（worked example）· `结构化输出约束`（Pydantic schema，⭐ 解析失败原地重试并把错误回灌）· `契约门`（多道确定性门，⛔ 拒绝时把报错文案回灌当反馈）。⛔ **无 RAG · 无工具调用 · 无多智能体辩论 · 无 self-consistency 投票。**

### B4 · ⭐⭐ 循环与裁决者（⛔ 本卡最重要的一格）

⭐⭐ **我们的流水线里同时存在两种裁决者，⭐ 这构成一次内部受控对照。**

| 循环 | 裁决者 | 类型 | ⭐ v46 实测收益 |
| :-- | :-- | :-- | :-- |
| `split ⇄ review_requirements` | `review_requirements` | ⛔ **LLM 自评** | ⛔ **零收益** |
| `convert ⇄ review_assertions` | `review_assertions` | ⛔ **LLM 自评** | ⛔ **零收益** |
| `convert ⇄ precheck_and_seal` | `precheck_and_seal` | ⭐ **确定性检查器**（pyfcstm 求值 + 契约门） | ⭐ **0 token，性价比最高** |
| `convert` 内部契约重试 | 解析器 / schema | ⭐ **确定性** | ⭐ **唯一净 +1118 条断言** |

⭐⭐ **逐轮边际收益**：⛔ 修订机器吃掉 **79% 的 token** 而台账谓词覆盖**净变化 ≈ 0**；⛔ **第 3–5 轮零收益**。⭐ 那些 token **够跑 168 次 X1 全网格**。

⭐⭐ **这一格的结论**：⛔ **同一条流水线上，确定性裁决者付钱、LLM 自评裁决者不付钱。**

### B5 · 中间表示

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有** |
| 形态 | ⭐ **19 条闭合谓词词表** + 断言脚本（`AssertionScript`） |
| ⭐ 是否闭合 | ⭐⭐ **闭合** —— ⛔ 模型只能从 19 条里选，不能自造谓词 |
| ⭐ 谁定的 | ⭐ **预编词表**，⭐ 由 LLM 在每条需求上**自动选**（⛔ 不是人挑） |

⭐ 分族：结构 S 10 条 · 仿真 B 6 条 · BMC P 3 条。⭐ 出处三类分级 **① 有领域证据 12 · ② 元模型定义性 6 · ③ 无外部依据 1**（详见 [../../provenance/](../../provenance/)）。

⚠️ **v46 实测只用到 15/19** —— ⛔ 变量维与时序性质几乎为空。⚠️ 那**可能是台账的问题而非词表的问题**，⛔ G1 完成前无法判断。

### B6 · 模型

⭐ **两个模型 × 3 轮**：`gpt-5.5` 与 `claude-opus-4-7`。⭐ 全网格 `54 pair × 2 模型 × 3 轮 = 324 格`。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 |
| :-- | :-- |
| `precheck_and_seal` | ⭐ **pyfcstm 求值器**（parse / semantic / design / sim facade）+ 契约门 |
| `release_results` | 封存与去重 |
| `bind_attribution` | 证据绑定 |
| `convert` 的 schema 校验 | Pydantic + 契约门 |

⭐⭐ **我们已经有一个 sound oracle（pyfcstm），⛔ 但它被放在了求值端而不是裁决端** —— ⭐ 这正是 M1 第二条设计原则要动的地方。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **X1 朴素基线**（单提示直接通读发现），⛔ 自建 —— ⚠️ L1 实测外部可比数字 **0 条** |
| `dataset` | ⭐ 54 pair（⛔ `00x8` 系列 6 个因界外永久排除）· 台账 98 条能力分母 |
| `metrics` | ⭐ `hit@1` / `hit@3` / `hit@all` + 五类多报分类 |
| ⭐ `judged_by` | ⭐ **人工逐位判定**（574 位逐位判据 + 288 簇五类裁定）—— ⛔ 本项目最贵的人工投入 |
| `human_baseline` | ⛔ **无** |
| `runs` | ⭐ 3 轮，⭐ 三口径同时报 |
| ⭐ `adverse_results` | ⭐⭐ **主结果对我方不利且已如实公布**：`hit@1` 主臂 **60.4%** vs 朴素基线 **76.2%**，⛔ **Δ = −15.82pp**，⛔ 而成本是 **212.6×** |

---

## D. 资产

| 资源类型 | 状态 | 说明 |
| :-- | :-: | :-- |
| 实验代码 | ⭐ 🟢 | 本仓库，1860 项测试 |
| 数据集 | ⭐ 🟢 | 54 pair + 台账（⚠️ **正在 G1 全量人工重标**） |
| 实验结果细则 | ⭐ 🟢 | 逐格逐轮逐位判定台账 |
| prompt | ⭐ 🟢 | 源码内 |
| 对外公开 | ⚪ | ⛔ 尚未 —— 论文未投 |

---

## E. 对 M1 的意义

1. ⛔⛔ **两件事并列，⛔ 不是「形状对、内容错」。**（⚠️ **本条 2026-08-14 就地改写** —— ⭐ 原文断言「闭合词表 + 自动选类**这个形状本身是对的**」，⛔ 而 [issue #189](https://github.com/HansBug/research_ideas/issues/189) §4.2 已把词表从「闭合词表 + 门」**降级为「常见形状库 + worked example」、不再是准入条件**；⭐ 判据见 [`../CRITERIA_MIGRATION.md`](../CRITERIA_MIGRATION.md)）
   - ⭐ **词表内容确有缺陷，且已实测**：`occupancy_after` 的 `nl_cue` 逐字在教模型别用 `edge_declared`，⛔ 324 格里 `edge_declared` 被问 **0.0%**；⭐ 30 格三臂事前登记的干预实测 **0 → 4/6**。⭐ 同形态的第二例（`occupancy_after` 的 `trigger` 字段说明吸收了 `event_consumed`）见 [`predicate_routing_defects.md`](../../../discover_matrix/docs/findings/predicate_routing_defects.md)。
   - ⛔ **而形状本身已被降级**：⭐ 新口径下 19 条谓词的角色从「准入词表」变为「**领域公认普遍检查的下界** —— 自由表达层必须能表达全部」。⭐⭐ **这两条互不抵消**：⛔ 内容缺陷是这一版实现的 bug，⛔ 形状降级是问题定义变更的后果。
2. ⛔ **不可取**：⛔ **两个 LLM 自评 reviewer 应当拆掉或改形态** —— ⭐ 它们零收益却吃 79% 的 token。
3. ⚠️ **关键差别（待外部工作回答）**：⭐ 我们把 sound oracle 放在**求值端**；⛔ 别人放在哪？⭐ **这正是 L3 要去数的那一格。**

---

## F. 存疑与未核项

1. ⚠️ **「八阶段」与「10 节点」两个说法并存** —— ⭐ 本卡取 10（按实现），⛔ 但伞 PR 与 X1 报告用的是 8。⛔ **对照表统一用 10，并在表注说明。**
2. ⚠️ **15/19 的谓词使用率归因未定** —— ⛔ 台账问题还是词表问题，G1 完成前无法判断。
