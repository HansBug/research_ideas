# v46 全量 324 格：结果与判定证据（长期留存）

**报告与明细**：
[PR #169 comment](https://github.com/HansBug/research_ideas/pull/169#issuecomment-5235520318)
｜ [gist](https://gist.github.com/HansBug/277ee557d44f1a6d5859f0f386760b7b)

本文件只保留**长期有效的结论、口径与证据入口**；施工过程、中断经过、review 状态见
GitHub PR（CLAUDE.md §9）。

## 1. 结果

代码 `ca41369e`（`src` 启动时零脏改动）｜54 pair × 2 模型 × 3 轮 = 324 格｜7h05m｜落盘 324/324、耗尽 0
分母：**98 条**台账记录 × 2 臂 × 3 轮 = **588 位**。扣除 28 条：27 条 `00x8` NL 越界
（[NL_SCOPE_RULE.md](../NL_SCOPE_RULE.md)）+ 1 条 `boundary_ruling: out_of_scope`
（`EIS-0043-02`，独立边界裁定，见 [audit.md](./audit.md) §3）。

| 口径 | v37 | v46 |
| :-- | --: | --: |
| `hit@1` | 274/588 = 46.6% | **355/588 = 60.4%** |
| `hit@3` | 106/196 = 54.1% | **139/196 = 70.9%** |
| `hit@all` | 77/196 = 39.3% | **95/196 = 48.5%** |
| claude / gpt `hit@1` | 44.9% / 48.3% | 62.6% / 58.2% |

⚠️ **`hit@k` 只能作为上界读。** 命中侧尚未做与多报侧对称的表示债务审计
（[REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md) §4.7）。已量化的规模：**人工表覆盖的
346 个命中位中，51 位（14.7%）在判据里引用「变量未声明」，其中 10 位（2.9%）不依赖其它事实**。
PlantUML 无变量声明语法、作者变量全语料 0/60，故「变量缺失」本身不能区分缺陷模型与忠实模型。
逐位清单见 [verdicts/variable_grounded_hits.json](./verdicts/variable_grounded_hits.json)。

📌 **第三条通道（本代次结果产出后才定位，已在代码侧关闭）**：pydantic 会把**类 docstring**
折进 `model_json_schema()`，经 `get_format_instructions()` 进入需求拆分器的 system prompt。
`schemas.py` 中三个类的 docstring 曾含设计依据性文字（含跨代次的谓词形成率一类聚合观察），
因此进入过该 prompt。边界：只影响 `RequirementSet` 一棵树，`AssertionScript` /
`RequirementReview` / `AssertionReview` 未受影响；文本**不含任何 pair 标识、台账记录 id 或
逐样本答案**，是聚合量而非样本级信息。现已把这些文字移出 docstring（改为 `#:` 注释，pydantic
不读），复扫全部 pydantic 模型的 `format_instructions` 无残留。**该通道计入上界的理由与前两条
相同：它使 `hit@k` 只能作为上界读。**

⛔ **这是上界，不是区间估计。** 已知扣除项有两档：仅靠变量缺失成立的 10 位 → `345/588 = 58.7%`；引用了变量缺失的全部 51 位 → `304/588 = 51.7%`。此外**谓词拒答文案**那条通道尚未量化，命中侧的表示债务审计亦未做。因此可写的只有 `hit@1 ≤ 60.4%`，真实下界未知。

📌 **另一条不经 prompt 的通道**：谓词拒答文案会进入生成者的下一轮上下文。实测
`predicate_api.py:1524` 的 `UnsupportedEvidence` 原文——「variable 'uav_count' is not
observable in the simulation state. **If the NL requires a quantity this model has no variable
for, assert that variable's existence as a `precondition`**」——出现在 `run1/0006-claude` 的
`findings` 里，而 `EIS-0006-02` 是 6/6。它交出的不是元素名（那是生产者自己先绑的），是
**极性**与**「把它发布出去」的指示**。计入上界的理由与变量缺失同源，故上界应按两条通道
一起读，而不是只按 `variable_declared` 一条。

📌 **351 与 360 的换算**：人工表覆盖 594 位中的 574 位，含 351 个命中判定；其中 6 位属被剔出
分母的 `EIS-0043-02`，故分母内 346；另有 15 个命中位无人工条目，`345 + 15 = 360`。上界性的
量化以 351 为分母，因为只有人工表带逐位 `argument`。

## 2. ⚠️ 两代判定口径不同，本对比是**下界**

三条记录 v37 为 6/6、v46 为 0/6，查证为 **v37 判定过宽**——一条 issue 被同时记给多条台账记录，
包括它并未陈述其命题的那条：

| 记录 | v37 所依据的产出 | 该产出实际陈述的是 |
| :-- | :-- | :-- |
| `EIS-0009-01` | `state_declared(UrbanMode.exit_urban)=False` | `EIS-0009-02` 的命题 |
| `EIS-0033-02` | `cardinality(PumpControl,3)=False` | `EIS-0033-01` 的命题 |
| `EIS-0047-01` | `initial_target(CAS, Frontend)=False` | `EIS-0047-02` 的命题（两步蕴含） |

v46 口径：**一条 issue 只记给它确实陈述了其命题的那条记录**。在同一个 98 记录分母上扣除这 18 位，v37 为 `(274 − 18) / 588 = 256/588 = 43.5%`，差距扩大到 **+17.7pp**。**未据此改写基线**（需按新口径全量重判 v37），仅标注上表为下界。

## 3. 本代确立并反复应用的判定口径

| 口径 | 判定 | 应用次数 |
| :-- | :-- | --: |
| 动作类 issue 逐字点名该信号 | 命中 | 8+ |
| 只报「缺少该**事件**」而台账说该事件被**错误创建** | 未命中 | 6 |
| issue 点名 Autonomous 等**作用域** | 命中（蕴含成因） | 5 |
| 变量缺失 ⇒ 该变量上的 effect 不成立 | 命中（蕴含成因） | 10 条记录 / 51 位 |
| 完成事件缺失 ⇒ 无法终止 | 命中（蕴含成因） | 6 |
| 父状态未占据 ⇒ 其默认子态未占据 | 命中（蕴含成因） | 4 |
| 非复合状态 ⇒ 无嵌套初始边 | 命中（蕴含成因） | 3 |
| 「多」与「缺」方向相反 | 未命中 | 9 |

⚠️ 「变量缺失」那一行的规模逐位可查（[verdicts/variable_grounded_hits.json](./verdicts/variable_grounded_hits.json)）：
51 个命中位引用了它，其中 10 位不依赖其它事实。它正是上文 `hit@k` 上界声明所指的那条判据——
PlantUML 无变量声明语法，作者变量全语料 0/60，故该谓词的 False 在本语料上不具判别力。

## 4. 审计

完整审计（溯源冻结、数据完整性、抽查判定、边界裁定、成本、盲区）见
[audit.md](./audit.md)。

## 5. 判定证据

- [verdicts/v46_human.json](./verdicts/v46_human.json)：**575 条人工判定，每条带 `argument`；
  其中 346 条判为命中，且这 351 条全部带 `equivalence_form`**（命中位与等价论证一一对应）
- [verdicts/v46_tiers.json](./verdicts/v46_tiers.json)：99 记录 × 2 臂 × 3 轮的 1/0/null 判定表
  （`EIS-0043-02` 由边界裁定剔出能力分母，度量时按 98 条计）
- [verdicts/variable_grounded_hits.json](./verdicts/variable_grounded_hits.json)：命中位中
  引用「变量未声明」者的逐位清单，即上文 `hit@k` 上界口径的量化依据
- 同形态横向复检（`adjudication_recheck`）：28 对分属 9 族，均为工具按元素重合度配对的假阳性。

## 6. 复算

```bash
python audit_to_verdicts.py --generation matrix-v46-full --audit <audit> --out /tmp/v46_verdicts.json
python metrics_at_k.py /tmp/v46_verdicts.json --no-direction-check
python full_tables.py --generation v46-full --verdicts /tmp/v46_verdicts.json
python loss_stages.py --generation matrix-v46-full --audit <audit>
python degradation_audit.py --generation matrix-v46-full
python adjudication_recheck.py --generation matrix-v46-full --audit <audit>
```

## 7. 残留缺陷（v47 入口）

1. **需求集规模失控**——中位 15 条，最大 **99**；按末次修订计超 60 的 13 格里 **4 格降级**
   （30.8%，全局 2.8%），全部 gpt 臂，
   全部落在同一份 NL 的六个 pair（条件从句最密集）。因果链：NL 条件密集 → 每个原子条件拆成
   独立需求 → 需求数爆炸 → 每条都要凑 primary → 撞门概率随条数线性累积。
   **应加需求集规模约束或合并策略，而不是继续修单个门。**
2. **schema 校验失败缺节点内原地重试**——`responder._retryable_error` 对 `ValueError` 返回
   `False`，而 pydantic 的 `ValidationError` 是其子类，于是结构错误整格冷启动重跑；本代 7 次整格冷启动重跑里 **6 次**由此而来。
   ⛔ **第 7 次是另一回事，必须分开记**：`run2/0019-gpt` 抛的是
   `ValueError: no-progress gate rejected repeated AssertionScript semantics` ——
   内部阶段的配额/门耗尽，按 [CLAUDE.md](../../../../CLAUDE.md) §10 属**必须降级、不得抛出**的一类，
   与 schema 那条逃生口不同源。并进同一条统计会让它彻底看不见。
   违反 CLAUDE.md §10，不污染结果。
3. **「多」与「缺」方向相反的系统性盲区**——模型看到异常却把「多余」读成「缺失」；
   9 处未命中同属此形态（`EIS-0014-03` / `0024-02` / `0024-04` / `0034-03`）。
