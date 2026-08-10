# v46 全量 324 格：结果与判定证据（长期留存）

**报告与明细**：
[PR #169 comment](https://github.com/HansBug/research_ideas/pull/169#issuecomment-5235520318)
｜ [gist](https://gist.github.com/HansBug/277ee557d44f1a6d5859f0f386760b7b)

本文件只保留**长期有效的结论、口径与证据入口**；施工过程、中断经过、review 状态见
GitHub PR（CLAUDE.md §9）。

## 1. 结果

代码 `ca41369e`（`src` 启动时零脏改动）｜54 pair × 2 模型 × 3 轮 = 324 格｜7h05m｜落盘 324/324、耗尽 0
分母：99 条台账记录 × 2 臂 × 3 轮 = **594 位**（`00x8` 先验越界，见 [NL_SCOPE_RULE.md](./NL_SCOPE_RULE.md)）

| 口径 | v37 | v46 |
| :-- | --: | --: |
| `hit@1` | 280/594 = 47.1% | **366/594 = 61.6%** |
| `hit@3` | 108/198 = 54.5% | **142/198 = 71.7%** |
| `hit@all` | 79/198 = 39.9% | **99/198 = 50.0%** |
| claude / gpt `hit@1` | 45.5% / 48.8% | 63.3% / 59.9% |

判定来源：A 层自动 153 位 + 人工 213 位（A 层要求谓词与绑定逐字相符，不受人工口径影响）。

## 2. ⚠️ 两代判定口径不同，本对比是**下界**

三条记录 v37 为 6/6、v46 为 0/6，查证为 **v37 判定过宽**——一条 issue 被同时记给多条台账记录，
包括它并未陈述其命题的那条：

| 记录 | v37 所依据的产出 | 该产出实际陈述的是 |
| :-- | :-- | :-- |
| `EIS-0009-01` | `state_declared(UrbanMode.exit_urban)=False` | `EIS-0009-02` 的命题 |
| `EIS-0033-02` | `cardinality(PumpControl,3)=False` | `EIS-0033-01` 的命题 |
| `EIS-0047-01` | `initial_target(CAS, Frontend)=False` | `EIS-0047-02` 的命题（两步蕴含） |

v46 口径：**一条 issue 只记给它确实陈述了其命题的那条记录**。扣除这 18 位后 v37 为 44.1%，
差距扩大到 +17.5pp。**未据此改写基线**（需按新口径全量重判 v37），仅标注上表为下界。

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

## 4. 判定证据

- [verdicts/v46_human.json](./verdicts/v46_human.json)：**579 条人工判定，每条带 `argument`；
  命中的 351 条另带 `equivalence_form`**
- [verdicts/v46_tiers.json](./verdicts/v46_tiers.json)：99 记录 × 2 臂 × 3 轮的 1/0/null 判定表
- `adjudication_recheck` 终检 28 对「同形态判出两种结果」，逐对读完、**0 处改判**；
  28 对分属 9 族，均为工具按元素重合度配对的假阳性。运行期该工具抓到过一处真判错
  （`EIS-0034-02`，方向为「命中被判成未命中」，与 v41 那 6 位同向），已就地更正。

## 5. 复算

```bash
python audit_to_verdicts.py --generation matrix-v46-full --audit <audit> --out /tmp/v46_verdicts.json
python metrics_at_k.py /tmp/v46_verdicts.json --no-direction-check
python full_tables.py --generation v46-full --verdicts /tmp/v46_verdicts.json
python loss_stages.py --generation matrix-v46-full --audit <audit>
python degradation_audit.py --generation matrix-v46-full
python adjudication_recheck.py --generation matrix-v46-full --audit <audit>
```

## 6. 残留缺陷（v47 入口）

1. **需求集规模失控**——中位 15 条，12 格超 60、最大 100；超 60 条的格降级率 25%（全局 2.8%），
   全部落在同一份 NL 的六个 pair（条件从句最密集）。因果链：NL 条件密集 → 每个原子条件拆成
   独立需求 → 需求数爆炸 → 每条都要凑 primary → 撞门概率随条数线性累积。
   **应加需求集规模约束或合并策略，而不是继续修单个门。**
2. **schema 校验失败缺节点内原地重试**——`responder._retryable_error` 对 `ValueError` 返回
   `False`，而 pydantic 的 `ValidationError` 是其子类，于是结构错误整格冷启动重跑（本代 7 次）。
   违反 CLAUDE.md §10，不污染结果。
3. **「多」与「缺」方向相反的系统性盲区**——模型看到异常却把「多余」读成「缺失」；
   9 处未命中同属此形态（`EIS-0014-03` / `0024-02` / `0024-04` / `0034-03`）。
