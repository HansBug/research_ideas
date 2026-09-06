# x1-split-intervention · 把 H-SPLIT 从观察性结论变成干预性结论

**事前登记**：`discover_matrix/docs/generations/x1-split-intervention/preregistered.md`，运行前 push（commit `f610f2a3`，2026-08-12 18:28:28 +0800）。修订 A 与 A.2 均写在任何 hit 数据产生之前，判据一字未改。

**产物**：`runs/paper1/x1-split-intervention/{control,treatment}/` 与 `runs/paper1/x1-split-intervention-v2/treatment_v2/`，30 格完整 run record。

---

## 0 · 一页结论

| 问题 | 答案 |
|:--|:--|
| 干预被真正实施了吗？ | **v1 否，v2 是。** v2 把「台账谓词进入最终需求集」从对照的 21.4% 提到 54.5%；`edge_declared` 供给 1/10 → 4/6 |
| TARGET 命中动了吗？ | **没有。** 对照 3/14、v1 4/14、v2 3/14 |
| ⭐ H-SPLIT 是因果的吗？ | **强形式不成立；完全的 H-REVERSE 也不成立；二者之间的中等效应——数据不足。** 见 §5 |
| 副作用 | 无多报（v2 每格 issue 反而**更少**）、零降级、零 coverage gap；代价是**结构化输出崩格**：对照 0/10、v1 2/10、v2 1/10 |
| 成本 | 30 格，input 10.39M / output 1.08M token，挂钟 43m57s（两批重叠） |

⭐ **本轮最有价值的产出不是那几个百分点，而是查明了 `edge_declared` 供给缺口的成因**：它不是 splitter「没想到」，而是**闭词表自己在往反方向指路**。见 §3。这是一条可以直接修的设计缺陷，且与命中数无关地成立。

---

## 1 · 设计

**待判命题。** 观察性分层（谓词写进需求集的 345 位：主臂 71.0% vs X1 72.5%；没写进的 177 位：41.8% vs 80.2%）有两种读法：

- **H-SPLIT**：验证机器没问题，损失来自 splitter 没提问。
- **H-REVERSE**：splitter 不问，**恰恰因为**那些现象在下游也难以断言。

分层变量是流水线自己的输出，观察性数据区分不了。本实验**只加宽提问侧、不动验证机器**。

**三条臂**（同 10 个 pair × `claude-opus-4-7` × 1 轮）：

| 臂 | splitter prompt | 落盘 |
|:--|:--|:--|
| `control` | 与干预前 git HEAD 逐字节相同 | 10/10 |
| `treatment_v1` | 四条结构扫描追加到 prompt **末尾** | 8/10 |
| `treatment_v2` | 同样四条**插到最终契约节之前** + 调和段 + 词表 routing 冲突化解 | 9/10 |

**位集（跑前固定，事后未增删）**：TARGET 14 条、REGRESSION 12 条。

**pair 选择**：v46 中 claude 臂在「谓词没写进需求集」层命中最差、X1 证明缺陷可发现、涉及谓词落在四条扫描射程内。⚠️ 这是刻意挑的最差子集，所以绝对数字低于全量，⛔ 不可与全量 41.8% 直接比。

---

## 2 · 干预边界的机械证据

五个 LLM 角色的 system prompt sha256[:12]，**直接读自 run record**：

| role | control | treatment_v1 | treatment_v2 | |
|:--|:--|:--|:--|:--|
| `assertion_converter` | `72cbf5eb8995` | `72cbf5eb8995` | `72cbf5eb8995` | 逐字节相同 |
| `assertion_reviewer` | `12c494de99e1` | `12c494de99e1` | `12c494de99e1` | 逐字节相同 |
| `result_adjudicator` | `723e83415918` | `723e83415918` | `723e83415918` | 逐字节相同 |
| `requirement_splitter` | `41a1795c1318` | `4044419f4541` | `dbd03de8e28f` | **改动** |
| `requirement_reviewer` | `6c7f0b0ea83e` | `29f64ea8ea5e` | `29f64ea8ea5e` | **改动** |

⭐ 这张表就是「只动提问侧」的全部含义。谓词求值、断言封存、release、attribution 是确定性代码，三臂共用同一 commit（`pipeline_src_diff_vs_commit: 0 files`）。对照臂的 splitter 哈希与干预前 HEAD 逐字节相同。

⚠️ **归类声明**：requirement reviewer 被归入「提问侧」，理由是它决定哪些问题活到被问、且不产出也不评估任何断言。⛔ 这是本实验的一个前提而非公理；不同意的读者应把「验证机器未动」读成「断言层及其之后未动」。

---

## 3 · ⭐ 最重要的发现：供给缺口是词表自己造成的

事前只知道现象：`edge_declared` 是 7 条 REPORTABLE 记录（42 位）的 primary，v46 的 324 格里写进需求集的是 **0**；同期 `occupancy_after` 被写了 2256 条。此前记作「splitter 没想到」。

**v1 干预跑完，`edge_declared` 仍是 0/8。** 查因发现的不是提示词强度问题。`predicates.py` 中 `occupancy_after` 的 `nl_cue` 字段写着：

> `the sentence describes what the running system does when a named stimulus arrives. This is the default for event-driven behaviour; edge_declared is only for claims about what the artifact contains.`

这段经 `vocabulary_prompt()` 渲染进 splitter prompt（`prompts.py:546`）与 requirement reviewer prompt（`:563`），而 prompt 又要求「**先扫这张表再读目录**」。

⛔ **那个 0 不是疏忽，是词表照着教的结果。** 事件驱动的句子被系统性路由到 `occupancy_after`；而「句子点名一条迁移、模型里没有」**既是**行为主张**也是**制品主张，词表的二分把它挤掉了。

按 CLAUDE.md §13（审计单位是交集，说清哪条让步）：**两条都不让步**——两个谓词问的是不同问题，句子点名一条迁移时两条都欠。`occupancy_after` 为假只说「运行没到那儿」，与「边缺失 / 守卫恒闭 / 源态不可达 / 竞争边胜出」四种情形都相容；`edge_declared` 为假才指认边不存在，而它的**真**又是让前者的假读成「声明了但没走」的前提。

**v2 加入这段后立刻生效**：`edge_declared` 供给 1/10 → **4/6**，这是它在本实验中第一次进入需求集。

⚠️ 边界核查：`nl_cue` 只渲染进 splitter 与 requirement reviewer；converter / asserter 读 `callable_prompt()`，不含 `nl_cue`。⛔ 未改 `predicates.py`，冲突在 prompt 层化解（§2 表中三行「逐字节相同」即为证据）。

---

## 4 · 结果

### 4.1 操纵检查（预登记 §4.2 的前置闸）

「台账那条记录的 `primary_predicate` 是否出现在该格**最终**需求集里」：

| 臂 | 进最终需求集 | 下限 50% |
|:--|:--|:--|
| control | 3/14 = **21.4%** | — |
| treatment_v1 | 3/11 = **27.3%** | ⛔ 未过 |
| treatment_v2 | 6/11 = **54.5%** | ✔ 过 |

📌 对照臂的 21.4% 与 v46 claude 三轮在同一 14 条上的基线 **9/42 = 21.4%** 完全一致——「对照臂没跑歪」的独立佐证。

**四条扫描谓词的供给**（写进最终需求集的格数 / 落盘格数）：

| predicate | control | treatment_v1 | treatment_v2 |
|:--|:--|:--|:--|
| `edge_declared` | 1/10 | 0/8 | **4/6** |
| `reaches` | 2/10 | 3/8 | **4/6** |
| `event_consumed` | 2/10 | 2/8 | 1/6 |
| `guard_distinguishable` | 0/10 | 0/8 | **0/6** |
| `occupancy_after` | 8/10 | 6/8 | 6/6 |

⛔ **`guard_distinguishable` 在三条臂上全部为 0** —— 四条扫描里有一条完全没被执行。涉及的两条 TARGET 记录（`EIS-0049-03`、`EIS-0056-01`）因此**不承载任何关于 H-SPLIT 的信息**，本轮对它们只能记「干预未实施」。

### 4.2 命中：TARGET 逐位 before/after

| record | pair | predicate | control | treatment_v1 | treatment_v2 |
|:--|:--|:--|:--|:--|:--|
| `EIS-0005-01` | 0005 | `edge_declared` | 未命中 | 未命中 | 未命中 |
| `EIS-0005-02` | 0005 | `containment` | 未命中 | **命中** | 未命中 |
| `EIS-0009-01` | 0009 | `edge_declared` | 未命中 | 未命中 | 未命中 |
| `EIS-0010-04` | 0010 | `reaches` | 命中 | 命中 | 命中 |
| `EIS-0010-05` | 0010 | `event_consumed` | 未命中 | **命中** | 未命中 |
| `EIS-0026-03` | 0026 | `reaches` | 未命中 | 未命中 | 未命中 |
| `EIS-0027-01` | 0027 | `reaches` | 未命中 | 未命中 | 未命中 |
| `EIS-0037-01` | 0037 | `reaches` | 未命中 | 未命中 | **命中** ⬅ v2 追回 |
| `EIS-0039-01` | 0039 | `edge_declared` | 命中 | 未命中（崩格） | 未命中（崩格） ⬅ 崩格丢失 |
| `EIS-0040-01` | 0040 | `event_consumed` | 未命中 | 未命中 | 未命中 |
| `EIS-0049-01` | 0049 | `edge_declared` | 未命中 | 未命中（崩格） | 未命中 |
| `EIS-0049-03` | 0049 | `guard_distinguishable` | 未命中 | 未命中（崩格） | 未命中 |
| `EIS-0056-01` | 0056 | `guard_distinguishable` | 未命中 | 未命中 | 未命中 |
| `EIS-0056-02` | 0056 | `effect_declared` | 命中 | 命中 | 命中 |
| **合计** | | | **3/14 = 21.4%** | **4/14 = 28.6%** | **3/14 = 21.4%** |

**REGRESSION（12 条）**：control 9/12 = 75.0%、v1 7/12 = 58.3%、v2 8/12 = 66.7%。v2 相对对照低 1 位，在预登记红线（低 > 2 位）之内。

**TARGET 内部拆分**：扫描射程内 12 条 —— 三臂**同为 2/12 = 16.7%**；射程外 2 条 —— control 1/2、v1 2/2、v2 1/2。⛔ 即 v1 那 +1 位完全来自**射程外**的 `containment`，与四条扫描无关。

### 4.3 对照预登记判据（阈值跑前写死，⛔ 未改动）

| 臂 | TARGET | Δ vs 对照 | 操纵检查 | 预登记判定 |
|:--|:--|:--|:--|:--|
| `treatment_v1` | 4/14 | +1 | 27.3% < 50% | **数据不足 —— 干预未被有效实施** |
| `treatment_v2` | 3/14 | **0** | 54.5% ≥ 50% | **H-SPLIT 不成立（H-REVERSE 得到支持）** |

**红旗核查**（预登记 §4.1）：

| 红旗 | 红线 | 实测 | 触发？ |
|:--|:--|:--|:--|
| 多报暴增 | > 2.5× 对照 | 每格 issue 均值：对照 3.50、v1 3.25、**v2 2.75** | ⛔ 未触发（v2 反而更少） |
| REGRESSION 退化 | 低 > 2 位 | v1 −2、v2 −1 | ⛔ 未触发 |
| 降级格增多 | 多 > 3 格 | 三臂 `degraded_stages` 全为 0 | ⛔ 未触发 |
| 整格失败 | > 2/10 | control 0、v1 **2**、v2 **1** | ⛔ 未触发（v1 恰在线上） |
| 断言不可执行率 | > 2× 对照 | 三臂 `coverage_gaps` 全为 0 | ⛔ 未触发 |

---

## 5 · ⭐ H-SPLIT 是因果的吗

### 5.1 三个互相独立的事实

1. **操纵成功了。** v2 把提问率从 21.4% 提到 54.5%，`edge_declared` 从近乎不存在提到 4/6。这不是猜测，是从需求集里数出来的。
2. **命中没动。** 3/14 → 3/14，配对不一致格是 1 对 1（v2 追回 `EIS-0037-01`，因崩格丢掉 `EIS-0039-01`）。McNemar 精确检验 p = 1.0。
3. **但在同一条臂内部，问到了的位命中率远高于没问到的。** v2：问到了 3/6 = 50%，没问到 0/5 = 0%。三臂合并：问到了 6/12 = 50%，没问到 4/24 = 17%（Fisher p = 0.053）。

### 5.2 ⛔ 三值回答：**数据不足**

但「数据不足」有明确的方向性内容，不是「什么都没学到」：

- ⛔ **H-SPLIT 的强形式被否证。** 强形式说「问了就能答」。v2 多问了 3 个位，一个额外命中都没换来（净 0）。若转化率接近 X1 在这批位上的 85.7%，多问 3 个应当带来约 +2.5 位。没有出现。
- ⛔ **完全的 H-REVERSE 同样不成立。** H-REVERSE 说 splitter 回避的正是下游答不了的。可 v2 问到的 6 个位里有 3 个命中（50%），下游显然答得了其中一部分。
- ⭐ **正确读法：提问是必要条件，但远不是充分条件。** §5.1 的第 3 条说明「没问到」几乎必然不命中（0/5、合并 4/24），而「问到了」也只有一半能走完断言 → 发布链路。

### 5.3 ⛔ 为什么必须诚实说「数据不足」：本设计几乎没有功效

在 14 个位、对照 3 命中的条件下：

| 若真实效应是 | Fisher 双侧 p |
|:--|:--|
| 预登记**强档**（3/14 → 9/14） | **0.054** |
| 预登记**部分档**（3/14 → 6/14） | **0.42** |

⛔ **也就是说，即使干预真的达到预登记的强档，本设计也只能勉强擦到 0.05。** 部分档则完全测不出。所以「Δ = 0」既与「无效应」相容，也与「中等效应」相容——⛔ 这个实验没有能力区分它们。预登记把阈值定在 14 个位上是**设计缺陷**，写的时候没做功效计算。

### 5.4 还有三件事压低了本轮的信息量

1. **`guard_distinguishable` 的干预完全没落地**（三臂全 0/N），2 条 TARGET 记录白占分母。
2. **崩格吃掉了一个真实命中**：`EIS-0039-01` 在对照臂命中，两条干预臂都因崩格丢失。剔除崩格后 v2 = 3/13 = 23.1%，仍与对照持平。
3. **`primary` 不可机械解析的位有 4 条**（`EIS-0005-02`、`0009-01`、`0037-01`、`0049-01`），操纵检查在它们上面只能按谓词名近似判断。

---

## 6 · 副作用量化

| 指标 | control | treatment_v1 | treatment_v2 |
|:--|:--|:--|:--|
| 落盘 / 崩格 | 10 / **0** | 8 / **2** | 9 / **1** |
| 每格已发布 issue（均值 / 中位 / 最大） | 3.50 / 3.5 / 8 | 3.25 / 3.0 / 8 | **2.75** / 3.0 / 5 |
| `degraded_stages` 非空格数 | 0 | 0 | 0 |
| `coverage_gaps` 非空格数 | 0 | 0 | 0 |
| `excluded_findings` 均值 | 1.50 | 1.38 | **2.50** |
| 每格需求条数（中位） | 14 | 13 | 17 |

⭐ **没有多报暴增**——这很重要，因为它排除了「霰弹效应」：v2 的命中不是靠多撒 issue 换来的，它每格 issue 反而**比对照少**。

⚠️ **唯一实质副作用是崩格。** 三次崩格（v1 的 0039 / 0049，v2 的 0039）**失败签名相同**：`DiscoverGraphFailed at split_requirements: ValidationError for RequirementSet`——模型把 `requirements` 返回成 JSON 字符串而不是数组，或 `edge_declared` 漏掉 `trigger` 绑定。按 CLAUDE.md §12，**相同失败签名 = 结构性死路，不是采样波动**。按 §10，schema 解析失败属「逃生口」而非常态，本身就是待修缺陷：**加长 prompt 提高了结构化输出失败率，而节点内没有把解析错误定向回灌重试**。⛔ 对照臂 0/10 崩格，说明这是干预引入的。

`excluded_findings` 在 v2 升到 2.50——判定材料里可见多条**逐字命中台账却被 `representation_debt` 归因策略拦下未发布**的发现（0026-03、0037-01、0056-01 均有）。⭐ 这提示下一步该查的可能不是提问侧，而是**归因策略的拦截面**。

---

## 7 · 成本

| 项 | 数值 |
|:--|:--|
| 格数 | 30（control 10 + v1 10 + v2 10） |
| input token | 10,390,747 |
| output token | 1,082,765 |
| 节点墙钟合计 | 3.88 h |
| 实际挂钟 | run1 35m32s + v2 27m28s，重叠执行，**总跨度 43m57s** |
| 判定 | 7 个判定组，78 位逐位判定 |

---

## 8 · 方法学缺陷与已修事项（本轮自查）

1. ⛔ **判定材料竞态（已修）**：pair 0009 的第一次判定用的是**第三条臂落盘之前**生成的材料，于是 treatment_v2 被判成「未落盘」= 0/3。该判定已作废（`STALE_verdicts_C_pair0009_DISCARDED.json`），用完整材料重判后为 2/3。⭐ 若不发现，v2 会平白少 2 位。事后加了 `ready.sh` 闸：只有三条臂全部终态的 pair 才允许判定，且材料必须在派发前重新生成。
2. ⛔ **预登记未做功效计算**（§5.3）。14 个位撑不起它自己写的阈值。下次必须先算功效再定档位。
3. ⚠️ **v1 的失败是操纵缺陷而非假设证据**（修订 A/A.2 已记录）：扫描块被 append 在自称「覆盖以上全部」的最终契约节之后，且与「不要从模型读出义务」表面冲突。
4. 判定全程盲判（甲/乙/丙 每 pair 独立随机），判定者不知道实验在比什么，也没看到达标判据。

---

## 9 · 下一步（按预期信息量排序）

1. ⭐ **修 `occupancy_after` 的 `nl_cue`**（§3）。这条与命中数无关地成立，是一处可直接消除的系统性供给缺口；改完应在全量 324 格上复测 `edge_declared` 供给。
2. ⭐ **查 `representation_debt` 归因策略的拦截面**（§6）。判定材料里反复出现「逐字命中却被拦下」，这可能是比提问侧更大的一段损失。
3. **修 splitter 的结构化输出健壮性**（§6）：把 schema 解析错误定向回灌重试，而不是让整格崩掉——这正是 CLAUDE.md §10 要求的降级。
4. **若要重做本实验**：先算功效。要在 α=0.05 下检出 21.4% → 50%，每臂约需 40–50 个 TARGET 位，即 3 轮 × 更多 pair。本轮的 14 位撑不起任何结论。
5. **`guard_distinguishable` 的干预要单独设计**——四条扫描里只有它一条完全没落地。

---

## 附 · 复现

```bash
# 三臂共用一份源码，仅环境变量不同
X1_STRUCTURAL_SWEEP=<未设|1|2> PYTHONPATH=<src>:<repo> \
  python -m paper_stm_feedback_loop.discover --pair-id <pair> \
    --profile claude-opus-4-7 --output-dir <dir>
```

脚本：`/tmp/x1intervene/{select_pairs,present_blind,analyze,evidence_probe,score}.py`；判定指令 `JUDGE_INSTRUCTIONS.md`；盲化映射 `blind_key.json`；逐位判定 `verdicts_[A-H].json` 与合并后的 `verdicts_merged.json`。
