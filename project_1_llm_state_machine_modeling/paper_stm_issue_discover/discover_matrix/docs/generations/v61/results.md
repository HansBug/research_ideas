# v61 结果台账（按迭代追加，最新在上）

判定装置：第六轮 judge（gpt-5.6-luna，`semantic-judge.two-stage.v3.11`，relation-first 闭合），judge 对 judge 比较同一 15 对、同一轮次的 v60 产出；人工数字仅作参照（见 [preregistered.md](./preregistered.md) §3）。评测脚本 [evaluate_run.py](./evaluate_run.py)。

## 迭代 1（method 提交 7be9261f9；method run `runs/paper1/method-v61-7be9261f9/0af895b0b3114674a2f2f1df0fce2d1c`，judge run `runs/paper1/judge-v61-7be9261f9/current-r1`）

生效改动：载体归属门（S3 / 初始迁移不变量 / INITIAL_ENTRY_CONDITIONAL 只在作者拥有的载体上判定）、S5 方括号守卫前置条件、S2 源侧祖先闭包、R2 源状态前置条件、源–语义分歧审计 C1.1–C1.9、因果折叠 C4.2（UML 蕴含链 + 后代闭包）、作者源锚点。15 格全部 completed / eligible，0 失败；method 约 14 分钟，judge 约 38 分钟。

### 对照事前登记档位（judge 口径）

| 指标 | v60 同轮 | v61 迭代 1 | 达标线 | 结果 |
|:--|--:|--:|--:|:--|
| 锚定组 FULL 条目 | 17/19 | **17/19** | ≥ 16 | 达标 |
| 锚定组 judge precision | 95.7% | **97.4%** | ≥ 88% | 达标 |
| 收益组 FULL 条目 | 22/47 | **32/47** | ≥ 31 | 达标 |
| 收益组 judge precision | 66.1% | **81.1%** | ≥ 74% | 达标 |
| 收益组点名 16 条命中 | 2 | **13** | ≥ 10 | 达标 |
| 子集 L2（18 条）/ 点名 L2 | 14 / 1 | **15 / 4（0009-03、0029-05、0049-02、INS-0056-01 全中）** | 4 条全中 | 达标 |
| 子集报告数（一轮） | 173 | **150（10.0 条/格）** | ≤ 125（及格 ≤ 140） | **未达** |
| 子集 judge precision | 74.0% | **85.3%** | ≥ 78% | 达标 |
| 子集 K/N/I | 82/46/45 | **91/37/22** | — | — |
| 格失败 | 0 | 0 | 0 | 达标 |

### 按谓词 × 性质（同 15 对同轮）

| 谓词/性质 | v61 n | v61 K/N/I | v61 FULL ids | v60 n | v60 K/N/I | v60 FULL ids |
|:--|--:|--:|--:|--:|--:|--:|
| S5 guard:missing | 54 | 7/30/17 | 2 | 60 | 3/36/21 | 2 |
| S3 trigger_set:mismatched | 12 | 10/0/2 | 6 | 14 | 11/0/3 | 7 |
| G1 reachability:unreachable | 7 | 7/0/0 | 3 | 14 | 14/0/0 | 6 |
| S2 transition_endpoints:wrong_target | 7 | 5/2/0 | 3 | 11 | 7/1/3 | 6 |
| — initial_entry:missing | 7 | 7/0/0 | 6 | 6 | 4/0/2 | 4 |
| — event_consumer_coverage:unconsumed | 3 | 2/1/0 | 0 | 8 | 8/0/0 | 6 |
| — termination:not_completed | 5 | 5/0/0 | 7 | 5 | 5/0/0 | 5 |
| S5 guard:wrong_guard（route token） | 0 | — | 0 | 9 | 1/2/6 | 0 |
| — containment:wrong_scope（含 C1.1） | 8 | 8/0/0 | 4 | 1 | 0/0/1 | 0 |
| S2 initial_entry:missing | 6 | 5/0/1 | 5 | 3 | 2/1/0 | 3 |
| — trigger_set:mismatched | 5 | 5/0/0 | 5 | 3 | 3/0/0 | 3 |
| V4 deadlock_freedom:dead_end | 3 | 3/0/0 | 4 | 5 | 4/0/1 | 3 |
| — initial_entry:mismatched（C1.7） | 3 | 3/0/0 | 3 | 0 | — | 0 |
| — state_after_stimulus:wrong_target | 1 | 0/0/1 | 0 | 3 | 1/0/2 | 1 |
| R2 state_after_stimulus | 0 | — | 0 | 2 | — | 0 |

### 丢失与收回

v60 同轮命中而 v61 未命中的 5 条：`EIS-0007-01`（锚定对 0007，v60 靠 G1「CollisionAvoidance 不可达」命中；v61 这轮的两条抽取契约 state_role 不满足根可达前沿的准入，前沿无从展开）、`EIS-0039-02` 与 `INS-0039-04`（v60 靠「Shared termination target FinishState」命中；v61 这轮 termination 契约的 state_role 未标为 termination_state，终止前沿被跳过；C1.7 报告对两者拿到 PARTIAL）、`VU-0010-01`（报告存在，judge 关系判 PARTIAL）、`INS-0002-03`（同文报告「Initial transition transition:line:10 has a trigger」v60 judge 判 K FULL、v61 judge 判 I——judge 噪声）。四个由结构性原因丢失的条目都指向同一件事：确定性前沿把 LLM 的软字段 `state_role` 当准入条件。

v61 新收回 15 条，其中 13 条是点名条目（源–语义分歧审计与作者锚点直接贡献 0009-03 / 0029-05 / 0049-02 / 0010-02 / 0016-02 / 0056-01 / 0039-03 / 0039-04 / 0000-02 / 0030-02 / 0030-03 / 0014-03 / VU-0014-01）。

折叠：14 条症状折为子主张；8 条根报告里 judge 给 7 条 FULL、多条同时命中多个条目（0002 根报告 FULL 3 条），说明子主张文本能被 judge 读到。首次实跑曾发现按任意共享元素名折叠会把独立 K 报告折进人工判 N 的 S2 报告（0011），已在运行前改为 UML 蕴含链加后代闭包。

### 未达项与第二轮改动

报告数 150 未达 125。S5「omits its required guard」54 条占 36%，其中 28 条作者标签是布尔表达式（judge 判 N 23 / K 2 / I 3），3 条与需求守卫同名（全 I），8 条是其他事件（I 5）。第二轮：(a) 根可达与终止前沿去掉对 `state_role` 的依赖（结构事实决定准入）；(b) 布尔标签与同名标签的 S5 缺守卫报告按格聚合为一条模态报告，子主张保留每条迁移；其他事件标签的 S5 报告不动。
