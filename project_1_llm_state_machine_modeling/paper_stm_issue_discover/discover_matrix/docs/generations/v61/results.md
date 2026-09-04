# v61 结果台账（按迭代追加，最新在上）

## 全量 54×3（method 提交 ea6141607；method run `runs/paper1/method-v61-full-ea6141607/a7b47d84c3cb4377a8009e5018d5b745`；0045 r1 补格 `runs/paper1/method-v61-fill0045-778212b03/0e450e5c6c9d4841820c7d1fd2a888ea`；judge run `runs/paper1/judge-v61-full-ea6141607/current-r*`）

**判定装置**：第六轮 judge（gpt-5.6-luna，`semantic-judge.two-stage.v3.11`，relation-first 闭合，两读 + 分歧仲裁），只判 ours；baseline 沿用同配置的 v3.11 全量 judge 结果（`runs/paper1/judge-full-3a1ba5cf1-iter6cfg/baseline-r*`）；v60 参照也取同一 judge 对 v60 产出的判定，三列全部 judge 对 judge，无人工复核。人工冻结终稿的数字只作参照。

**运行**：method 162 格，161 格 completed / eligible，`0045` 第 1 轮在契约抽取阶段 `limit_exceeded: turns limit exceeded`（结构修复循环耗尽轮次，§10 第 2 类逃生口，登记为待修）后 `failed_with_receipt`；该格用同一方法代码（仅文档提交后的 HEAD 778212b03）单独重采样一次，completed，6 条报告（judge K 3 / N 3，`EIS-0045-01` FULL），判进同一 judge 目录（`current-r1-fill0045`）。method 全量 80 分钟、825 次调用、$7.49、输入 34.3M / 输出 2.79M token（不含补格）；judge 约 4.6 小时（前 1.3 小时 6 并发与 method 并行，其后 14 并发；期间一次约 15 分钟的网关停滞自行恢复）。

### 总表（judge 口径）

| 指标 | baseline | v60 ours | **v61 ours** | v61 对 baseline | v61 对 v60 |
|:--|--:|--:|--:|--:|--:|
| 报告数 / 每格 | 512 / 3.2 | 1271 / 7.8 | **903 / 5.6** | ×1.8 | −29% |
| K / N / I | 293 / 134 / 85 | 628 / 277 / 366 | **561 / 198 / 144** | | I −61% |
| report precision | 83.4% | 71.2% | **84.1%** | +0.7 pp | +12.9 pp |
| finding-level precision（一命中单位一报告） | 81.1% | 63.4% | **79.3%** | −1.8 pp | +15.9 pp |
| hit@1 | 225/435 = 51.7% | 292/435 = 67.1% | **323/435 = 74.3%** | **+22.6 pp** | +7.2 pp |
| hit@3 | 105/145 | 119/145 | **130/145** | +25 | +11 |
| hit@all | 47/145 | 75/145 | **82/145** | +35 | +7 |
| L0 hit@1 | 108/213 (51%) | 134/213 (63%) | **153/213 (72%)** | | |
| L1 hit@1 | 72/105 (69%) | 58/105 (55%) | **73/105 (70%)** | | |
| L2 hit@1 | 45/117 (38%) | 100/117 (85%) | **97/117 (83%)** | +44 pp | −3 单位 |

对照事前登记（§11）：report precision ≥ 80% 达标；hit@3 ≥ 125 达标；报告数 ≤ 1000 达标；hit@1 ≥ 340 未达（323），远高于回归红旗 292。人工口径参照：v60 ours 人工 77.1% / 310；baseline 人工 81.4% / 227。

### 按谓词 × 性质（全部三轮，judge 口径）

| 谓词/性质 | v61 n | v61 K/N/I | v61 命中单位 | v60 n | v60 K/N/I | v60 命中单位 |
|:--|--:|--:|--:|--:|--:|--:|
| S5 guard:missing | 89 | 24/53/12 | 19 | 304 | 35/137/132 | 18 |
| S2 transition_endpoints:wrong_target | 88 | 34/21/33 | 27 | 95 | 40/21/34 | 27 |
| G1 reachability:unreachable | 60 | 45/14/1 | 25 | 105 | 95/9/1 | 45 |
| S3 trigger_set:mismatched | 66 | 55/1/10 | 35 | 88 | 61/2/25 | 37 |
| V4 deadlock_freedom:dead_end | 66 | 59/2/5 | 52 | 85 | 73/0/12 | 58 |
| - effect:wrong_effect | 52 | 30/19/3 | 24 | 55 | 30/20/5 | 20 |
| - event_consumer_coverage:unconsumed | 13 | 12/1/0 | 8 | 56 | 40/14/2 | 27 |
| - trigger_set:mismatched | 47 | 30/6/11 | 27 | 21 | 16/2/3 | 15 |
| S2 initial_entry:missing | 35 | 26/2/7 | 21 | 31 | 21/1/9 | 21 |
| - containment:wrong_scope | 30 | 25/2/3 | 20 | 28 | 18/0/10 | 9 |
| - initial_entry:missing | 28 | 24/2/2 | 23 | 29 | 23/0/6 | 18 |
| - state_action:other | 29 | 9/18/2 | 7 | 25 | 6/15/4 | 4 |
| - initial_entry:wrong_target | 25 | 20/2/3 | 20 | 24 | 20/3/1 | 18 |
| - transition_endpoints:wrong_target | 21 | 4/3/14 | 5 | 27 | 11/3/13 | 8 |
| - state_action:wrong_effect | 19 | 9/8/2 | 5 | 27 | 9/6/12 | 8 |
| - termination:not_completed | 21 | 15/6/0 | 13 | 23 | 20/3/0 | 20 |
| S2 initial_entry:wrong_target | 17 | 11/1/5 | 10 | 26 | 16/3/7 | 15 |
| S5 guard:wrong_guard | 8 | 2/3/3 | 2 | 33 | 1/10/22 | 0 |
| - cardinality:missing | 19 | 15/3/1 | 10 | 19 | 12/6/1 | 8 |
| R2 state_after_stimulus:wrong_target | 0 | 0/0/0 | 0 | 32 | 1/0/31 | 1 |
| - region_structure:wrong_scope | 18 | 8/6/4 | 6 | 14 | 7/4/3 | 5 |
| - cardinality:extra | 13 | 6/5/2 | 6 | 15 | 8/3/4 | 7 |
| - variable_delta:wrong_effect | 11 | 6/5/0 | 6 | 11 | 9/2/0 | 7 |
| - guard_disjointness:wrong_guard | 8 | 5/0/3 | 5 | 12 | 6/0/6 | 6 |

读法：S5 缺守卫 304 → 89 条（186 条聚合进 32 条模态根报告），其中 I 从 132 降到 12，而命中单位不减（18 → 19）；R2 32 → 0；route-token 守卫报告 33 → 8；G1 可达 105 → 60 条，命中单位 45 → 25；事件消费覆盖 56 → 13 条，命中单位 27 → 8——后两者是因果折叠的代价（见下）。分歧审计带来的新家族：containment:wrong_scope 命中单位 9 → 20，initial_entry:mismatched、state_retention、effect:missing 等从 0 起。

### 条目级增减（judge 口径，单位 = 条目 × 轮）

40 条条目轮数增加（**+67 单位**），27 条减少（**−36 单位**），净 +31；15 条三轮均未命中。

增加的主力是源–语义分歧审计直接点名的条目：`EIS-0009-03` / `EIS-0029-05` / `EIS-0049-02`（FinishState 首次提及嵌套，1 → 3 / 1 → 2 / 1 → 3 轮）、`EIS-0010-02`（仅 stereotype 子机，0 → 3）、`INS-0056-01`（无标签闭环，0 → 3）、`DIFF-0039-04`（两条根初始边，0 → 3）、`INS-0039-03`（无标签条件边，0 → 3）、`EIS-0000-02` / `EIS-0020-02` / `EIS-0030-03` / `EIS-0050-01`（复合标签，→ 3）、`EIS-0024-02` / `EIS-0024-03` / `EIS-0024-04` / `DIFF-0024-04`（`exit/Send` 生命周期语法误放到迁移，→ 2–3）、`EIS-0016-02`（跨块同名，0 → 2）、`VU-0014-01`（信号写成描述，1 → 3）、`VU-0054-01`（只守卫无触发，0 → 2）；其余是稳定性提升（`INS-0002-03` / `INS-0002-04` / `INS-0012-01` 等 2 → 3）。

减少的 36 个单位按机制分三类：

1. **因果折叠的关系粒度代价（约 20 单位）**：v60 靠 G1「作用域不可达」或事件消费覆盖报告命中、v61 把它们折成结构根因报告的子主张后，judge 对根报告只给 PARTIAL——`DIFF-0053-01`（L2，3 → 0，v60 由 6 条 G1 命中）、`EIS-0002-02`（L2，3 → 1）、`EIS-0033-01`（3 → 1）、`EIS-0014-01`、`INS-0019-01`、`EIS-0032-01`、`EIS-0046-01`、`INS-0046-03`、`EIS-0047-01/02`、`EIS-0057-01`、`INS-0053-02` 等。判据是子主张里写全了缺陷，但 relation 判定以根报告的主主张为准。
2. **终止前沿仍不稳定（约 8 单位）**：`INS-0029-05`（L2，3 → 0）、`EIS-0039-02`（2 → 0）、`INS-0039-04`（3 → 1）在 v60 都由「Shared termination target FinishState」终止报告命中；v61 这三对三轮里终止契约的 target 未能解析成候选，去掉 `state_role` 依赖不够，需要与 C1 同样的 NL 词元回退锚定。
3. **轮间波动与 judge 噪声（约 8 单位）**：`EIS-0007-01/03`、`INS-0017-01`、`EIS-0013-01`、`EIS-0010-01`、`INS-0057-01` 等 3 → 2，v61 在缺失轮多为 PARTIAL 或同文报告被判 I。

三轮均未命中的 15 条：`INS-0002-02`、`EIS-0005-02`、`EIS-0016-01`、`EIS-0026-01`、`INS-0029-05`、`EIS-0030-01`、`EIS-0030-02`、`DIFF-0032-03`、`EIS-0034-03`、`EIS-0034-06`、`EIS-0039-02`、`INS-0044-03`、`VU-0046-01`、`DIFF-0053-01`、`EIS-0056-01`。其中全称事件义务（`EIS-0030-02`、`VU-0046-01`）与终止边无标签（`INS-0044-03`）是 C2 未做的部分；`DIFF-0053-01`、`INS-0029-05`、`EIS-0039-02` 是上面第 1、2 类。

### 报告量与 precision 的构成

903 条里 32 条是模态聚合根（覆盖 186 条成员）、108 条根报告带 154 条折叠子主张；finding-level（一命中单位一报告）79.3% 对 baseline 81.1%，report-level 84.1% 对 83.4%——两种口径下都与 baseline 拉平，而 v60 是 71.2% / 63.4%。剩余 144 条 I 的最大家族是 LLM 候选的 transition_endpoints wrong_target（33 + 14）、S3 triggers（10 + 11）与 S5 缺守卫剩余 12 条，已无单一确定性规则可拦。

### 结论与下一步（待讨论）

1. 用户设定的两条目标在 judge 口径下都达到：hit@1 对 baseline +22.6 pp（目标 +20，最低 +15），report precision 84.1% 对 83.4%（拉平）；报告量降 29%，I 降 61%。
2. hit@1 未到登记的 340，缺口 17 单位，其中约 20 单位是因果折叠换来的报告量：把 G1 可达与事件消费覆盖从折叠里拿出来（只折死端 / 终止这类行为症状）预计收回大部分，代价约 +60 条报告。这是数量与 hit 的显式权衡，需要用户裁定。
3. 终止前沿补 NL 词元回退锚定（同 C1 / 根可达的做法），预计再收回 6–8 单位，无副作用。
4. 0045 r1 的运行时限失败登记为待修：契约抽取的结构修复循环应把解析错误定向回灌而不是耗尽轮次；用户计划小修后单格重跑，届时替换本次的重采样格。
5. 全称事件义务（C2.2）与终止边无标签（C1.6 扩到终止边）仍是覆盖侧的两块空白。


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
