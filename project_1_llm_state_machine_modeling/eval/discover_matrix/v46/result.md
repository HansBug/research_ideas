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
| `hit@1` | 274/588 = 46.6% | **360/588 = 61.2%** |
| `hit@3` | 106/196 = 54.1% | **140/196 = 71.4%** |
| `hit@all` | 77/196 = 39.3% | **97/196 = 49.5%** |
| claude / gpt `hit@1` | 44.9% / 48.3% | 62.9% / 59.5% |

⚠️ **`hit@k` 只能作为上界读。** 命中侧尚未做与多报侧对称的表示债务审计
（[REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md) §4.7）。已量化的规模：**351 个命中位中
51 位（14.5%）在判据里引用「变量未声明」，其中 10 位（2.8%）不依赖其它事实**。PlantUML 无
变量声明语法、作者变量全语料 0/60，故「变量缺失」本身不能区分缺陷模型与忠实模型——一个
完美模型在同一条断言上也会给出 `False`。逐位清单见
[verdicts/variable_grounded_hits.json](./verdicts/variable_grounded_hits.json)。

📌 **判定覆盖的缺口**：588 位中有 **19 位**在
[verdicts/v46_human.json](./verdicts/v46_human.json) 里没有对应条目（15 位判为命中、
4 位判为未命中），涉及 `EIS-0002-01` / `EIS-0002-03` / `EIS-0009-02` / `EIS-0029-02` /
`EIS-0029-04` / `EIS-0037-01` / `EIS-0039-01` / `EIS-0057-01`。**这 19 位无逐格 `argument`
可复核**，只有 `v46_tiers.json` 中的 1/0 值。

**成本**：output token 9.91M → **17.18M（1.73×）**，节点耗时 50.8 → **88.0 机时**。
每百万 output token 命中位数 27.6 → **21.0（−24%）**——提升有相当部分是多花算力换来的。
详见 [audit.md](./audit.md) §5。

**多报侧**：未被任何台账记录认领的产出归并为 293 簇，其中 13 簇内容已被台账记录承载、
2 簇的断言在冻结制品上求值为真（真阴性），均按定义移出，本侧分母
**278 条目 / 117 去重 / 42 pair**。结论是**净增量只有 1 条**（`0014-4`），而占比最大的一块
（表示债务）不是模型缺陷，是我们自己 R4.5 编译（PlantUML → FCSTM）的信息损失。
全部分布表与交叉表由 [rebuild_unexpected.py](../rebuild_unexpected.py) 从
`unexpected_verdicts/G*.jsonl` 机器生成于唯一产地
[unexpected_tables.md](./unexpected_tables.md)，**本文件不留副本**；判据与定义见
[unexpected_evidence.md](./unexpected_evidence.md) 与
[REPRESENTATION_DEBT.md](../REPRESENTATION_DEBT.md)。

⚠️ **由此产生一条口径要求**：引用本代次任何多报数字时**必须分解**为
「真漏记 / 表示债务 / 无 NL 依据 / 假阳性 / 越界」五类，且条目与去重两套分母必须同时给。
只报总多报率会同时高估模型的乱报程度、又掩盖编译链的问题。**覆盖侧结论不受实质影响**——
真漏记只有 1 条；但补入台账仍会使 `hit@all` 略降（该簇只出现在 6 格中的 2 格），
不可只说「分母不变」。

## 2. ⚠️ 两代判定口径不同，本对比是**下界**

三条记录 v37 为 6/6、v46 为 0/6，查证为 **v37 判定过宽**——一条 issue 被同时记给多条台账记录，
包括它并未陈述其命题的那条：

| 记录 | v37 所依据的产出 | 该产出实际陈述的是 |
| :-- | :-- | :-- |
| `EIS-0009-01` | `state_declared(UrbanMode.exit_urban)=False` | `EIS-0009-02` 的命题 |
| `EIS-0033-02` | `cardinality(PumpControl,3)=False` | `EIS-0033-01` 的命题 |
| `EIS-0047-01` | `initial_target(CAS, Frontend)=False` | `EIS-0047-02` 的命题（两步蕴含） |

v46 口径：**一条 issue 只记给它确实陈述了其命题的那条记录**。扣除这 18 位后 v37 进一步降至约 44.2%，差距扩大到约 +17.0pp。**未据此改写基线**（需按新口径全量重判 v37），仅标注上表为下界。

## 3. 本代确立并反复应用的判定口径

| 口径 | 判定 | 应用次数 |
| :-- | :-- | --: |
| 动作类 issue 逐字点名该信号 | 命中 | 8+ |
| 只报「缺少该**事件**」而台账说该事件被**错误创建** | 未命中 | 6 |
| issue 点名 Autonomous 等**作用域** | 命中（蕴含成因） | 5 |
| 变量缺失 ⇒ 该变量上的 effect 不成立 | 命中（蕴含成因） | 7 |
| 完成事件缺失 ⇒ 无法终止 | 命中（蕴含成因） | 6 |
| 父状态未占据 ⇒ 其默认子态未占据 | 命中（蕴含成因） | 4 |
| 非复合状态 ⇒ 无嵌套初始边 | 命中（蕴含成因） | 3 |
| 「多」与「缺」方向相反 | 未命中 | 9 |

## 4. 审计

完整审计（溯源冻结、数据完整性、抽查判定、边界裁定、成本、盲区）见
[audit.md](./audit.md)。

## 5. 判定证据

- [verdicts/v46_human.json](./verdicts/v46_human.json)：**575 条人工判定，每条带 `argument`；
  其中 351 条判为命中，且这 351 条全部带 `equivalence_form`**（命中位与等价论证一一对应）
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

1. **需求集规模失控**——中位 15 条，12 格超 60、最大 100；超 60 条的格降级率 25%（全局 2.8%），
   全部落在同一份 NL 的六个 pair（条件从句最密集）。因果链：NL 条件密集 → 每个原子条件拆成
   独立需求 → 需求数爆炸 → 每条都要凑 primary → 撞门概率随条数线性累积。
   **应加需求集规模约束或合并策略，而不是继续修单个门。**
2. **schema 校验失败缺节点内原地重试**——`responder._retryable_error` 对 `ValueError` 返回
   `False`，而 pydantic 的 `ValidationError` 是其子类，于是结构错误整格冷启动重跑（本代 7 次）。
   违反 CLAUDE.md §10，不污染结果。
3. **「多」与「缺」方向相反的系统性盲区**——模型看到异常却把「多余」读成「缺失」；
   9 处未命中同属此形态（`EIS-0014-03` / `0024-02` / `0024-04` / `0034-03`）。
