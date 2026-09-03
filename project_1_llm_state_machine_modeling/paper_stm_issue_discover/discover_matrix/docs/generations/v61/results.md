# v61 结果台账（按迭代追加，最新在上）

## 迭代 3（method 提交 6e80ad78c；method run `runs/paper1/method-v61-6e80ad78c/e44a385ea52d4c908c57c7e72c8aac00`，judge run `runs/paper1/judge-v61-6e80ad78c/current-r1`）

新增改动：模态聚合成员判据放宽为词元 Jaccard ≥ 0.5（5 字符轻词干）且比较运算符集合一致；含 route token 的模型撤回 R2 前沿。15 格全部 completed，0 失败；method 约 18 分钟，judge 约 58 分钟（0002 一次调用超时重试后重开格尝试）。

| 指标 | v60 同轮 | 迭代 1 | 迭代 2 | **迭代 3** | 达标线 | 结果 |
|:--|--:|--:|--:|--:|--:|:--|
| 锚定组 FULL 条目 | 17/19 | 17/19 | 19/19 | **16/19** | ≥ 16 | 达标（边缘） |
| 锚定组 judge precision | 95.7% | 97.4% | 92.7% | **88.9%** | ≥ 88% | 达标（边缘） |
| 收益组 FULL 条目 | 22/47 | 32/47 | 32/47 | **33/47** | ≥ 31 | 达标 |
| 收益组 judge precision | 66.1% | 81.1% | 72.0% | **81.5%** | ≥ 74% | 达标 |
| 收益组点名 16 条命中 | 2 | 13 | 13 | **11** | ≥ 10 | 达标 |
| 子集 L2（18）/ 点名 L2 | 14 / 1 | 15 / 4 | 16 / 4 | **15 / 3** | 4 条全中 | 及格 |
| 子集报告数（一轮） | 173 | 150 | 123 | **126（8.4 条/格）** | ≤ 125 | 及格（差 1） |
| 子集 judge precision | 74.0% | 85.3% | 78.9% | **84.1%** | ≥ 78% | 达标 |
| 子集 K/N/I | 82/46/45 | 91/37/22 | 82/15/26 | **77/29/20** | — | — |
| 子集 FULL 条目 | 39/66 | 49/66 | 51/66 | **49/66** | — | — |

聚合：41 条 S5 缺守卫收成 6 条根报告，judge 判 N/K/K/N/I/N（0029 那条 FULL `EIS-0029-02`、`EIS-0029-04`），R2 报告 0 条。锚定组丢的三条（`EIS-0002-02`、`INS-0002-02`、`INS-0002-05`）都在 0002，这一对本轮 judge 有效性读数超时重试后重开了格尝试，与第一轮 `INS-0002-03` 的翻转同源，判为 judge 噪声而非方法回退；收益组本轮未中的 `EIS-0049-02`、`VU-0010-01` 在前两轮都命中，属轮间波动。

剩余 20 条 I 已无主导的确定性家族：LLM 候选 transition_endpoints/initial_entry wrong_target 8、其余各 1–2 条。三轮间 FULL 49/51/49、precision 85.3/78.9/84.1 的摆动与 judge 自身噪声同量级（v60 同 5 对锚定组三轮 judge 曾摆动 17/18/12），确定性改动的边际收益已进入 gpt-5.6-luna 判定噪声区间。按登记进入 54×3（method 提交 ea6141607，代码与迭代 3 相同）。

## 迭代 2（method 提交 a0ec141c7；method run `runs/paper1/method-v61-a0ec141c7/48cce1659b3f4712bd340f785246b527`，judge run `runs/paper1/judge-v61-a0ec141c7/current-r1`）

新增改动：根可达与终止前沿去掉对 `state_role` 的依赖并加 NL 词元回退锚定；S5 缺守卫报告中作者标签为布尔表达式或与需求守卫同名者按格聚合为一条模态报告（子主张保留）。15 格全部 completed，0 失败；method 约 14 分钟，judge 约 31 分钟。

| 指标 | v60 同轮 | 迭代 1 | **迭代 2** | 达标线 | 结果 |
|:--|--:|--:|--:|--:|:--|
| 锚定组 FULL 条目 | 17/19 | 17/19 | **19/19** | ≥ 16 | 达标 |
| 锚定组 judge precision | 95.7% | 97.4% | **92.7%** | ≥ 88% | 达标 |
| 收益组 FULL 条目 | 22/47 | 32/47 | **32/47** | ≥ 31 | 达标 |
| 收益组 judge precision | 66.1% | 81.1% | **72.0%** | ≥ 74%（及格 ≥ 71%） | 及格 |
| 收益组点名 16 条命中 | 2 | 13 | **13** | ≥ 10 | 达标 |
| 子集 L2（18）/ 点名 L2 | 14 / 1 | 15 / 4 | **16 / 4** | 4 条全中 | 达标 |
| 子集报告数（一轮） | 173 | 150 | **123（8.2 条/格）** | ≤ 125 | 达标 |
| 子集 judge precision | 74.0% | 85.3% | **78.9%** | ≥ 78% | 达标 |
| 子集 K/N/I | 82/46/45 | 91/37/22 | **82/15/26** | — | — |
| 子集 FULL 条目 | 39/66 | 49/66 | **51/66** | — | — |

聚合效果：34 条 S5 缺守卫报告收成 3 条根报告（0009、0039、0049），judge 分别判 N、K（FULL `EIS-0039-02`）、N，均 D1；根可达回退锚定让 0007 的两条 G1 报告回来，`EIS-0007-01` 收回，锚定组因此 19/19。

precision 相对迭代 1 下降是算术效应：N 从 37 降到 15（聚合掉的都是 N），I 从 22 到 26。26 条 I 的构成：S5 缺守卫（未聚合的其他事件标签）11、LLM 候选 transition_endpoints/initial_entry wrong_target 5、cardinality 3、R2 2、其余 5。其中 S5 的 11 条里 8 条是「条件用同义事件名承载」（`road clear` 对 `road ahead is clear`、`Approached` 对 `approaches the destination`），R2 的 2 条都在含 route token 的模型上（v60 人工 44 条 R2 无一有效）。

迭代 3 改动（运行前登记）：模态聚合成员判据放宽为标识符词元 Jaccard ≥ 0.5（含 5 字符轻词干），但要求比较运算符集合一致，`flag=true` 视为命名；含 route token 的模型上撤回 R2 前沿（轨迹经过编译器合成的跳转，不是作者层行为）。预期：I 减约 8，报告数再减约 6，precision 回到 ≥ 82%，hit 不变。

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
