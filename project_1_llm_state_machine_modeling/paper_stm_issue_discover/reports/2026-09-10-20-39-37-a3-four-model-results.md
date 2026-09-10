# A3 四模型中间引导消融：有效发现、覆盖与报告准确性

> 结论冻结：2026-09-10 20:39:37（Asia/Shanghai）。本报告解释四模型完成后的冻结结果，保留[Sonnet/Luna 两模型历史报告](./2026-09-10-a3-direct-report-results-cn.md)。面向导师讨论的连贯学术解释见[A3 talk](../../talks/2026-09-10-实验-A3中间引导消融与论文叙事.md)。正文稳定引用键指向文末证据链；机器判定优先于本文。

## 1. A3 检验整套中间引导对发现的贡献

状态机缺陷发现既要找出自然语言需求与作者模型之间的不一致，也要避免把工具的表示差异解释成源模型错误。完整方法（Full）先把需求组织为待检查义务，再分阶段生成、扩充和核对候选。A3 将这组中间引导替换为一次大语言模型（LLM）直接生成，检验已有自然语言需求（NL）、作者状态机（STM）与确定性检查事实（inspection）是否足以维持发现能力。冻结假设 H1 是有效报告和台账命中下降，H2 是报告准确性可能下降；实验不以符合预期作为结果准入条件。[clm-design]

四个固定模型配置均出现有效报告量与去重命中下降。Sonnet、Luna、Muse 在两种报告有效比例口径下均下降；Qwen 在普通口径下接近 Full，在较严格口径下反而上升（两者定义见第三节）。因而结果支持中间引导提高有效发现和覆盖，准确性收益则具有模型差异。这是整组环节的消融，不是单个环节或等调用预算的效应估计。[clm-main]

## 2. 单次直接生成保留执行反馈与确定性发布

A3 正常方法链为 `NL + 作者 STM + inspection → 一次 LLM 生成报告与可选谓词 → 同实例绑定/编译/执行 → 确定性发布`，其后才进行独立外部评价。谓词是注册表中的类型化检查及其参数，不是任意生成代码；可选意味着具体来源主张也能在没有适用谓词时保留未验证状态。内部 D 指方法在发布前对主张成立程度的语义判定。表中移除项逐项对应冻结协议的消费者关闭表。[clm-design]

| 环节 | Full 的功能 | A3 处置 |
| --- | --- | --- |
| 义务提取、补全与片段覆盖 | 把需求分解为可追踪的检查对象，补足尚未覆盖部分 | 移除；不把义务清单压回单次提示 |
| 分阶段发现与两路发现视角 | 将义务与源模型对应，形成候选 | 替换为单次直接报告生成 |
| 未检查候选边界（frontier）、领域不变量、源迁移闭合、候选扩充 | 扩大候选范围，追踪尚未检查的结构与行为 | 移除 |
| 确定性清单（inventory）候选、额外执行探针（probe）、未解缺口转候选 | 从模型和执行信息补充发现 | 移除；inspection 仅作已有输入 |
| 内部 D 语义判定、纠错、反驳与语义反馈修订 | 复核主张与义务，处理反读法并修订 | 移除 |
| 输入、作者源、inspection、十二谓词定义 | 提供同一被测对象和检查接口 | 保留 |
| 精确引用、同实例绑定、编译与真实后端执行 | 检查已经生成的主张 | 保留；不猜补对象、不另生主张 |
| 真值拦截、证据资格、来源资格、精确去重与发布 | 形成最终唯一报告集合 | 保留 A3 适配；不依赖虚构内部 D |
| 独立外部评价 | 决定报告有效性、外部 D 与台账关系 | 保留原 Luna 双读与必要仲裁 |

这里“移除确定性部分”专指确定性补充发现与 probe，不能扩大到绑定、执行和发布。真实谓词结果 true 表示相应检查成立，发布端拦截同一缺陷主张；false 提供检查失败证据，仍需外部判断主张是否有效；unknown 表示未获确定结果。unsupported、谓词为空或无法闭合时，具体 source-backed 主张可保留 W1，无法具体定位则记 W0/coverage gap，不假造执行确认。W2 表示满足身份、来源和绑定资格的机械执行证据；W0/W1/W2 是方法证据资格，与外部 D 等级分开。[clm-design]

生成端不读取台账、Full 报告或外部标签。正常方法只有一个生成节点；异常传输和结构纠正不增加语义发现任务，异常恢复另见附录。发布的实质主张必须能回溯到这次生成，不能借适配或折叠扩大内容。A3 仍利用执行反馈；A4 则在固定 Full 上游候选后撤去末端执行反馈，两者干预位置不同。[clm-design] [clm-limits]

## 3. 匹配输入与独立评价固定了比较单位

### 3.1 每个模型都有完整的 54 对、三轮结果

四模型分别为 Claude Sonnet 5、GPT-5.6 Luna、Qwen3.8-27B、Muse Glimmer-30B。每个模型使用同一冻结集合的 54 个 NL/STM 输入对，每对三轮，共 162 格；A3 总计 648 格、2207 份最终报告，全部完成裁定，pending 为 0。输入来自既有源状态机语料，54 对仅涉及九个不同 NL 簇，因此轮次和同需求下的模型不能视为独立任务。[clm-main] [src-ledger]

| 配置 | A3 方法身份 | 同模型 Full 来源 | 必须保留的可比性条件 |
| --- | --- | --- | --- |
| Sonnet | `claude-sonnet-5` | E2 `sonnet/cells.json` 的 ours | 同 profile hash；历史日期和随机性仍不同 |
| Luna | `gpt-5.6-luna` | E2 `luna_history.json` 所引 v61 ours | 0045/r1 使用冻结 fill 来源；历史阶段输出上限 10000，A3 为 128000 |
| Qwen | `e1-qwen38-27b`，low，1,000,000 上下文 YaRN | E2 qwen ours | 沿用冻结权重/部署参数；历史 Full 与新 A3 非同步运行 |
| Muse | `e1-muse30b`，high，131,072 上下文 | E2 muse ours | 沿用冻结权重/部署参数；不外推到其他 serving 配置 |

模型简称只表示这些冻结配置，不构成模型家族排名。Full 逐格方法与 judge 来源都有 hash，本轮只读复用，没有新增 Full 或全量重判。Luna 历史谓词 ID 按冻结映射展示；不能仅据旧注册表版本名断言实际使用了不同数量的检查，具体 ID/定义保留在 predicate view。[src-full] [src-method] [clm-limits]

### 3.2 外部 judge 与方法中的判定不同

最终报告使用原 Luna 外部 judge 的两个独立读数，分歧触发必要仲裁，采用关系判定优先协议（relation_first），并完成全部判定步骤。报告有效性判定（validity）只读取报告、NL、作者源及允许的制品事实，不注入执行 verdict、内部标签、Full 裁定或台账答案；台账关系判定在隔离步骤读取待匹配台账项（expected）。A3 不使用 A4 的 true→I 指定政策或跨 Full 内容等价标签复用。外部模型与 method 的 Luna 即使同名，仍是不同角色和调用；“独立”指材料与流程隔离，不代表不同模型家族或人工金标准。[clm-eval]

所有已发布报告进入分母，零报告格也保留完成记录。有效但证据不足的报告不为改善指标而删掉。自动裁判仍可能误判，新增人工确认数为 0；这里的机器可复算指冻结标签及算术可复算，不等于语义真值已经人工确证。[clm-eval] [clm-limits]

### 3.3 报告有效比例与去重覆盖回答不同问题

设 R 为最终唯一报告数。K 是与台账存在 FULL 或 PARTIAL 关系的有效报告，N 是有效但无上述关系的报告，I 是无效报告，V=K+N。普通 precision 为 V/R。strict precision 的分子只包含有效且外部 D 属于 D1/D2 的报告，分母仍为 R。D2 表示支持主张的关键事实与被违反要求成立，且没有与现有证据相容、能使该设计合法的替代解释；D1 表示事实成立，但仍有此类替代解释；D0 表示违反要求未建立或设计读法正当。strict 是原核算的敏感性口径，不能拿内部 D 替代外部 D，也不能先删 D0 再缩小分母。[clm-eval]

hit@1 计每模型、每轮台账项是否至少获得一份 K 报告的 FULL 匹配，同一项在同轮多次报告只计一次，PARTIAL 不计。台账共 145 项，三轮分母为 435；hit@3 为三轮至少一次命中，hit@all 为三轮均命中，后两者分母均为 145。L0/L1/L2 分别描述点状对齐、结构或局部状态、跨迁移或路径行为，台账数量为 71/35/39，三轮分母为 213/105/117。L 等级与算法、谓词及 W 等级无一一对应关系。[clm-eval] [src-ledger]

V 衡量有效报告产出，hit 衡量固定台账覆盖，precision 衡量交付报告的有效比例。报告粒度会影响 V；hit 用台账内部去重缓解这一点。N 是台账外有效报告数，既不是跨报告去重的新缺陷数，也不是新人工确认数。以下主表先合并三轮分子、分母再算比率；模型等权平均和跨模型 pooled 比率另列，均不冒充按 pair 宏平均。[clm-eval]

## 4. 四模型有效发现和覆盖一致下降

### 4.1 完整主表保留 Qwen 的反向 strict 结果

表 1：各模型三轮 pooled 结果，所有分子、分母均来自冻结报告和关系。[clm-main]

| 模型 | 条件 | 报告 R | K/N/I | 普通 precision | strict precision | hit@1 |
| --- | --- | --- | --- | --- | --- | --- |
| Sonnet | FULL | 823 | 536/183/104 | 719/823（87.36%） | 650/823（78.98%） | 291/435（66.90%） |
| Sonnet | A3 | 684 | 463/91/130 | 554/684（80.99%） | 508/684（74.27%） | 230/435（52.87%） |
| Luna | FULL | 903 | 561/198/144 | 759/903（84.05%） | 678/903（75.08%） | 323/435（74.25%） |
| Luna | A3 | 670 | 404/90/176 | 494/670（73.73%） | 458/670（68.36%） | 245/435（56.32%） |
| Qwen | FULL | 958 | 599/256/103 | 855/958（89.25%） | 781/958（81.52%） | 311/435（71.49%） |
| Qwen | A3 | 358 | 262/56/40 | 318/358（88.83%） | 310/358（86.59%） | 193/435（44.37%） |
| Muse | FULL | 910 | 544/229/137 | 773/910（84.95%） | 712/910（78.24%） | 322/435（74.02%） |
| Muse | A3 | 495 | 233/70/192 | 303/495（61.21%） | 277/495（55.96%） | 175/435（40.23%） |

表 2：Full → A3 的有效产出与无效报告变化；pp 表示百分点，I/格以各自 162 格为分母。[clm-main]

| 模型 | 有效报告 Full → A3 | 相对变化 | ΔI | I/格 Full → A3 | Δ普通 pp | Δstrict pp |
| --- | --- | --- | --- | --- | --- | --- |
| Sonnet | 719 → 554 | -22.95% | +26 | 0.642 → 0.802 | -6.37 | -4.71 |
| Luna | 759 → 494 | -34.91% | +32 | 0.889 → 1.086 | -10.32 | -6.72 |
| Qwen | 855 → 318 | -62.81% | -63 | 0.636 → 0.247 | -0.42 | +5.07 |
| Muse | 773 → 303 | -60.80% | +55 | 0.846 → 1.185 | -23.73 | -22.28 |

三个模型的无效报告绝对数上升，因此 Full 的质量收益不只体现为更多有效报告扩大分母。Qwen 则同时少报有效和无效报告，普通 precision 几乎保持，strict 比例提高。这种反向比例与有效发现损失可以同时成立，不能以某一项比例代替全套结果。[clm-main]

### 4.2 合计损失以有效发现减少为主

表 3：跨模型计数、模型等权比率和报告 pooled 比率。P 指普通 precision。[clm-main]

| 条件 | 报告 | K | N | I | 有效 | hit/1740分子 | 模型等权P | 模型等权hit | 模型等权strict | pooled P | pooled strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FULL | 3594 | 2240 | 866 | 488 | 3106 | 1247 | 86.40% | 71.67% | 78.46% | 86.42% | 78.49% |
| A3 | 2207 | 1362 | 307 | 538 | 1669 | 843 | 76.19% | 48.45% | 71.29% | 75.62% | 70.37% |

有效报告减少 1437（46.27%），I 增加 50（10.25%）；在绝对数量上，有效发现损失更突出。台账项/模型/轮次命中从 1247 降至 843，减少 404（32.40%）。分母 1740=145×4×3，不是 1740 个独立研究样本；843 也不是跨模型去重后的独立缺陷。[clm-main]

模型等权普通 precision 下降 10.21 pp，strict 下降 7.16 pp，hit 下降 23.22 pp。这里对四个模型的三轮 pooled 比率各赋四分之一权重；不同报告量造成 pooled precision 与等权平均不相同。上述总数之差只描述两批报告的组成变化，没有逐条语义匹配就不能称为“1437 份有效报告转成了无效”。[clm-main]

### 4.3 十二组逐轮命中方向一致

表 4：四模型×两条件×三轮，共 24 行；每行 54 格，hit 分母 145。[clm-rounds]

| 模型 | 条件 | 轮次 | 格数 | 报告 | K/N/I | precision | hit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sonnet | FULL | 1 | 54 | 283 | 174/79/30 | 253/283（89.40%） | 92/145（63.45%） |
| Sonnet | FULL | 2 | 54 | 265 | 169/60/36 | 229/265（86.42%） | 99/145（68.28%） |
| Sonnet | FULL | 3 | 54 | 275 | 193/44/38 | 237/275（86.18%） | 100/145（68.97%） |
| Sonnet | A3 | 1 | 54 | 219 | 152/33/34 | 185/219（84.47%） | 76/145（52.41%） |
| Sonnet | A3 | 2 | 54 | 238 | 167/27/44 | 194/238（81.51%） | 75/145（51.72%） |
| Sonnet | A3 | 3 | 54 | 227 | 144/31/52 | 175/227（77.09%） | 79/145（54.48%） |
| Luna | FULL | 1 | 54 | 325 | 207/76/42 | 283/325（87.08%） | 113/145（77.93%） |
| Luna | FULL | 2 | 54 | 287 | 166/61/60 | 227/287（79.09%） | 98/145（67.59%） |
| Luna | FULL | 3 | 54 | 291 | 188/61/42 | 249/291（85.57%） | 112/145（77.24%） |
| Luna | A3 | 1 | 54 | 224 | 135/31/58 | 166/224（74.11%） | 86/145（59.31%） |
| Luna | A3 | 2 | 54 | 226 | 142/30/54 | 172/226（76.11%） | 82/145（56.55%） |
| Luna | A3 | 3 | 54 | 220 | 127/29/64 | 156/220（70.91%） | 77/145（53.10%） |
| Qwen | FULL | 1 | 54 | 315 | 201/84/30 | 285/315（90.48%） | 100/145（68.97%） |
| Qwen | FULL | 2 | 54 | 327 | 192/94/41 | 286/327（87.46%） | 103/145（71.03%） |
| Qwen | FULL | 3 | 54 | 316 | 206/78/32 | 284/316（89.87%） | 108/145（74.48%） |
| Qwen | A3 | 1 | 54 | 112 | 78/19/15 | 97/112（86.61%） | 58/145（40.00%） |
| Qwen | A3 | 2 | 54 | 126 | 90/22/14 | 112/126（88.89%） | 67/145（46.21%） |
| Qwen | A3 | 3 | 54 | 120 | 94/15/11 | 109/120（90.83%） | 68/145（46.90%） |
| Muse | FULL | 1 | 54 | 315 | 193/77/45 | 270/315（85.71%） | 108/145（74.48%） |
| Muse | FULL | 2 | 54 | 310 | 179/83/48 | 262/310（84.52%） | 109/145（75.17%） |
| Muse | FULL | 3 | 54 | 285 | 172/69/44 | 241/285（84.56%） | 105/145（72.41%） |
| Muse | A3 | 1 | 54 | 171 | 80/20/71 | 100/171（58.48%） | 62/145（42.76%） |
| Muse | A3 | 2 | 54 | 165 | 77/25/63 | 102/165（61.82%） | 57/145（39.31%） |
| Muse | A3 | 3 | 54 | 159 | 76/25/58 | 101/159（63.52%） | 56/145（38.62%） |

每个模型三轮的 A3 hit 均低于匹配 Full，共 12/12 组方向一致。Muse 三轮普通 precision 和有效报告数也均下降。轮次一致性表明结论并非由单次重复独自造成，但同一 NL 的相关性仍需在统计解释中保留。[clm-rounds]

### 4.4 重复覆盖与各层级也发生损失

表 5：跨轮命中与 L 分层。hit@3、hit@all 分母 145，各层 hit@1 分母见表头数值。[clm-coverage]

| 模型 | 条件 | hit@3 | hit@all | L0 hit@1 | L1 hit@1 | L2 hit@1 |
| --- | --- | --- | --- | --- | --- | --- |
| Sonnet | FULL | 122/145（84.14%） | 69/145（47.59%） | 133/213（62.44%） | 65/105（61.90%） | 93/117（79.49%） |
| Sonnet | A3 | 98/145（67.59%） | 56/145（38.62%） | 113/213（53.05%） | 42/105（40.00%） | 75/117（64.10%） |
| Luna | FULL | 130/145（89.66%） | 82/145（56.55%） | 153/213（71.83%） | 73/105（69.52%） | 97/117（82.91%） |
| Luna | A3 | 110/145（75.86%） | 55/145（37.93%） | 123/213（57.75%） | 44/105（41.90%） | 78/117（66.67%） |
| Qwen | FULL | 125/145（86.21%） | 81/145（55.86%） | 165/213（77.46%） | 68/105（64.76%） | 78/117（66.67%） |
| Qwen | A3 | 85/145（58.62%） | 39/145（26.90%） | 100/213（46.95%） | 38/105（36.19%） | 55/117（47.01%） |
| Muse | FULL | 124/145（85.52%） | 88/145（60.69%） | 165/213（77.46%） | 79/105（75.24%） | 78/117（66.67%） |
| Muse | A3 | 90/145（62.07%） | 31/145（21.38%） | 92/213（43.19%） | 43/105（40.95%） | 40/117（34.19%） |

表 6：按同一台账 ID 与同一轮次建立的命中集合交、差；单位是去重后的台账项/轮次。[clm-coverage]

| 模型 | 共有命中单元 | Full独有 | A3独有 |
| --- | --- | --- | --- |
| Sonnet | 179 | 112 | 51 |
| Luna | 201 | 122 | 44 |
| Qwen | 157 | 154 | 36 |
| Muse | 144 | 178 | 31 |

A3 存在 Full 没有命中的单元，不能把 A3 报告集描述为 Full 的严格子集。每个模型 Full 独有命中均多于 A3 独有，且 hit@3、hit@all 与 L0/L1/L2 的 pooled 命中均下降。这些差集刻画台账覆盖迁移，不是全部 K/N 报告的语义一一配对。[clm-coverage]

## 5. 输出收缩与无效发布呈现两种模式

### 5.1 Qwen 的较高 strict 比例伴随覆盖收缩

Qwen 的报告从 958 减至 358，有效报告从 855 减至 318，I 从 103 减至 40。strict 分子也从 781 减至 310，比例却从 81.52% 升至 86.59%。可以确认的是，剩余报告较集中在 strict 计分范围内；不能据此推断模型更善于发现问题，因为 hit 从 311 降至 193，跨轮覆盖也下降。[clm-main] [clm-coverage]

这组结果与直接生成聚焦于较少主张的解释一致。生成和发布计数显示收缩并非由大量末端拦截独自造成：Qwen A3 仅生成 379 条，发布 358 条，true 拦截 4 条。Full 与 A3 的生成机制和预算不同，因此不能据此拆出单个阶段的作用，更不能猜测模型隐藏推理或意图。[clm-funnel] [clm-limits]

### 5.2 Muse 同时损失发现范围与发布质量

Muse 有效报告从 773 减至 303，I 从 137 增至 192，普通 precision 从 84.95% 降至 61.21%。三轮均出现低于 Full 的 precision 和 hit，说明这个配置的变化同时涉及有效发现与无效发布。Sonnet、Luna 也呈现有效报告下降、I 上升，只是幅度较小。[clm-main] [clm-rounds]

移除中间引导后，来源核对、义务明确化、候选扩充和内部纠错都发生变化。最终标签不能确定其中哪一个独自造成 Muse 的下降；第七节的来源混淆案例只展示一种可观察的失败路径，不能当作全部 192 条 I 的解释。[clm-case-muse] [clm-limits]

## 6. 条件与行为类命中减少，不可达类保留

表 7：按冻结台账轴筛选后统计四模型三轮 FULL 命中；各模型单元格为 Full → A3。trigger/guard/effect 属 `defect_element`，其余属于 `defect_logic_kind`，跨轴不可相加为总命中。[clm-content]

| 台账分类 | 分母 | Full hit | A3 hit | Sonnet | Luna | Qwen | Muse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| trigger | 300 | 249 | 134 | 64 → 40 | 66 → 32 | 60 → 28 | 59 → 34 |
| guard | 48 | 45 | 15 | 11 → 5 | 12 → 5 | 11 → 1 | 11 → 4 |
| nondeterminism | 60 | 43 | 9 | 12 → 1 | 12 → 5 | 8 → 2 | 11 → 1 |
| nontermination | 60 | 36 | 2 | 10 → 0 | 10 → 1 | 7 → 0 | 9 → 1 |
| unreachable | 96 | 73 | 81 | 21 → 21 | 17 → 22 | 16 → 19 | 19 → 19 |
| effect | 216 | 171 | 131 | 30 → 34 | 43 → 46 | 48 → 32 | 50 → 19 |

触发条件、守卫、非确定性与不终止类命中均减少，与中间引导帮助条件核对、行为组合及覆盖展开的解释一致。不终止类从 36/60 降至 2/60，尤其显示直接报告没有维持这类台账覆盖；它不证明所有复杂行为都需要同一种技术。[clm-content]

不可达类从 73/96 增至 81/96，提供了反向模式：A3 保留 inspection，部分显式拓扑问题仍能进入直接报告。effect 合计从 171 降至 131，但 Sonnet、Luna 分别上升，Qwen、Muse 下降，不能总括为“局部 effect 都保留”。这些是探索性分层，没有多重检验校正，也没有为每个环节建立独立因果对照。[clm-content] [clm-limits]

## 7. 三个来源可核查的案例限定机制解释

按分析目的选择三组同模型、同 pair、同轮次的 Full/A3 对照，共六格；不是随机抽样，不估计各机制占比。下文区分作者源、工具派生表示、生成主张及外部裁定。全部报告原文与理由在冻结 JSON；原始方法和 judge 文件的十二个 hash 已按附录命令核对。[clm-case-loss] [clm-case-muse] [clm-case-qwen]

### 7.1 接管行为遗漏：仍能发现结构错误，却没有覆盖规定路径

Muse 的 0010/r1 使用高层驾驶需求。NL 原句为 “transit to human driving mode when receive human steering cmd, brake pressed, in (auto final)”。冻结台账保留了原句的歧义：三个条件是并列选择还是合取，不能单从这段残缺文字定案。作者 STM 将两条返回边放在 `AutonomousActive`，分别标 `Human Steering Cmd` 和 `Brake Pressed`。`AutonomousFinal` 只有来自 `HumanDriving` 的 Power Off 入边，没有返回边。Full 报告 `0010:r1:issue:1` 主张所需 `AutonomousFinal → HumanDriving` 迁移缺失，冻结外部裁定接受该读法、判为 K/D2，FULL 命中 `DIFF-0010-08` 与 `EIS-0010-04`。台账说明这两个 ID 指向同一处缺失，不能解释为两个独立缺陷。[clm-case-loss]

A3 同格只发布两个 K/D2：autonomous 子状态未嵌套，以及 Power On 边目标错误；没有主张缺失的 auto-final 返回路径。这里的丢失能由全格报告集合及台账匹配共同确认。A3 保持两份报告有效，却没有提出冻结裁定所接受的 auto-final 接管缺失，说明单格高 precision 与这套评价中的需求覆盖可以分离。这个例子支持系统性展开义务的解释，但不能分辨缺失源自义务提取、扩充还是内部复核中的某一步。[clm-case-loss]

### 7.2 Muse 无效主张：把转换表示差异归给作者

Muse 的 0003/r1 使用车辆运行状态需求，NL 明确系统通过 `start` 开启、通过 `keyOff` 关闭。作者 STM 第 12 行已经写出 `Operate --> PoweredOff : keyOff`。A3 报告 `0003:r1:issue:0` 却依据 inspection 中派生迁移的空 trigger 与 `R45RouteToken == 7`，称该迁移缺少 keyOff。外部裁定理由指出，作者标签已表达 keyOff，单独类型化 trigger 载体的缺失是表示细节，没有相应源级义务，故为 I/D0。[clm-case-muse]

同格另外两份 A3 报告分别把派生 token guard/effect、子状态退出边当作作者缺陷，外部也判 I。Full 同格仅发布一份台账外有效报告，讨论系统初始进入 Operate 的问题；本文不将其与上述三份报告强行配对。可观察的错误是来源层次混淆：准确描述工具表示，并不自动建立作者 STM 违反需求。A3 的执行反馈仍存在，但它不能替代源级语义核对。[clm-case-muse]

### 7.3 Qwen 保留不可达命中：收缩没有抹去所有结构发现

Qwen 的 0009/r1 使用自主驾驶与避碰需求。NL 第 12、13 条要求避碰系统从 deactive 状态开始，响应危险并在安全时恢复；作者 STM 的顶层初始边只进入 `AutonomousMode`，同级的 `CollisionAvoidanceSystem` 没有外部入边。避碰复合状态内部虽有到 deactive 的局部初始边，它不能自行激活尚未进入的同级复合状态。本研究不采用“同级复合状态隐式并行”的解释，作者文件也没有声明并发区；这是该例成立的语义边界。[clm-case-qwen]

Full 的 `0009:r1:issue:2` 和 A3 的 `0009:r1:issue:1` 都指出此不可达问题，外部均为 K/D2，FULL 命中 `VU-0009-01`。同格 Full 发布 13 份有效报告，A3 仅 2 份；A3 另一份保留城市退出目标错误。去重后 Full 命中五项台账，A3 命中两项。这既展示 Qwen 的覆盖收缩，也保留 A3 能直接发现的结构反例；13→2 不能解释为减少了 11 个独立缺陷。[clm-case-qwen]

## 8. 九个 NL 簇区间限定推断强度

表 8：配对 bootstrap 的 95% 百分位区间，差值均为 A3−Full，单位 pp；九个 NL 簇，10000 次重采样，冻结 seed=20260906。同簇保留各 pair 与三轮相关结构。[clm-ci]

| 模型 | Δprecision 95%区间 pp | Δhit@1 95%区间 pp |
| --- | --- | --- |
| Sonnet | [-15.99, 2.72] | [-27.02, 0.00] |
| Luna | [-20.10, -1.74] | [-30.42, -5.01] |
| Qwen | [-8.09, 6.78] | [-38.81, -9.63] |
| Muse | [-33.33, -13.95] | [-43.20, -23.12] |

命中下降的方向比准确率下降更一致；Sonnet hit 区间上端到 0.00，不能统一宣称四模型均显著下降。Sonnet、Qwen precision 区间跨零，Luna、Muse 在此重采样口径下为负。区间只反映这九簇组成的敏感性，不能消除历史运行差异；未计算的 strict 区间、p 值或多重检验校正均不补造。[clm-ci]

组合消融、调用预算不等、历史 Full 与 A3 的服务/日期/随机性、Luna 输出上限差异和共享自动 judge 都限制因果与外推范围。即使可复算，当前标签也不等于独立人工金标准；样本来自固定语料，不能据此泛化到任意工业模型或所有语言适配器。[clm-limits]

## 9. A3 支持预期的发现贡献，准确性假设获得部分支持

事前 H1 预期有效报告与台账命中下降，四模型的 V、hit@1/@3/@all 以及十二组逐轮 hit 均呈现这一方向。因此，A3 支持预期的核心结论：在这些固定配置与输入上，完整中间引导相对单次直接报告提高了有效发现与台账覆盖。事前 H2 预期 precision 可能下降，Sonnet、Luna、Muse 的普通/strict 口径同降，但 Qwen 普通近乎持平、strict 提高，故 H2 只获得部分、依模型配置而异的支持。[clm-main] [clm-rounds] [clm-coverage]

学术上应使用“支持中间引导的联合发现贡献”，而非“证明每个中间步骤必不可少”或“四模型准确性统一改善”。前者由预先登记的组合干预与完整结果支撑，后两者超出本次干预和数据范围。方向一致也不等于四模型都达到统一的显著性门槛，区间解释仍按第八节保留。[clm-design] [clm-ci] [clm-limits]

## 10. A3 与 A4 分别约束发现与末端选择的论证

Paper1 的 C-2 讨论类型化谓词及执行证据如何约束问题发现。A3 保留谓词定义、绑定执行和末端资格，同时撤除整套中间引导，观察到有效发现和覆盖收缩；A4 固定 Full 已有候选，撤去末端执行反馈以检验发布选择和误报抑制。二者分别补充“形成有价值主张”和“利用证据决定发布”的证据，但 A3 没有单独消融谓词定义，A4 也没有消除执行反馈对上游材料可能已有的影响。[clm-design] [clm-limits]

论文可写为：在四个固定配置上，相较完整方法，直接报告消融一致减少有效产出与台账覆盖；报告准确性变化依赖模型，其中 Qwen 的 strict 比例提高但有效分子和覆盖均下降。这支持中间引导的发现贡献，并要求同时报告数量、覆盖和质量。两项消融的交互效应仍未单独测量，不能将差值相加作为 C-2 的净因果贡献。[clm-main] [clm-limits]

## 审计附录：证据链与事实源

### A.1 来源考据表

本报告是四模型结果的新解释快照，没有迁移或覆写旧报告。前缀对应本次核心结论冻结时间；首次提交可用下方 git 命令获得，避免文件自引尚未生成的 commit。

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
| --- | --- | --- | --- | --- | --- |
| 本报告 | 本文件首次提交，见 `[cmd-history]` | 同首次提交；2026-09-10 20:39:37 CST 冻结 | 首次整合四模型、模型差异和三例来源分析 | 无迁移 | 下列两份 results 与四模型 summary |
| `final_results/a3_20260910/results.json` | `585e55d1f` | 不适用 | Sonnet/Luna 冻结标签与分析 | 本报告未修改 | [旧 results][src-old] |
| `final_results/a3_open_judge_20260910/results.json` | `a390c1275` | 不适用 | Qwen/Muse 完整裁定与四模型汇总 | 本报告未修改 | [新 results][src-open] |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
| --- | --- | --- | --- | --- | --- |
| [src-protocol] | a3_protocol | [冻结协议](../discover_matrix/docs/generations/a3_20260910/preregistered.md) | md | 移除/保留、假设、模型身份、恢复 | §1至6，消费者关闭表与公开配置 |
| [src-old] | old_results | [Sonnet/Luna results](../final_results/a3_20260910/results.json) | json | 两模型冻结标签 | `/models/{sonnet,luna}/{a3,full}/{reports,cells,metrics,per_round}` |
| [src-open] | open_results | [Qwen/Muse results](../final_results/a3_open_judge_20260910/results.json) | json | 两模型标签、主张与案例 | `/models/{qwen,muse}/{a3,full}`；reports 的 `original_report_id` |
| [src-summary] | four_summary | [四模型 summary](../final_results/a3_open_judge_20260910/four_model_summary.json) | json | 紧凑结果与旧结果 hash | `/models`；不复制旧报告数组 |
| [src-ledger] | ledger | [ledger.json](../discover_matrix/ledger_v2/ledger.json)、[L 定义](../discover_matrix/ledger_v2/l_tier.json) | json | 145 项分母、内容轴、层级 | `/items/{ledger_id}/{pair,axes,L,pair_context}` |
| [src-full] | full_sources | [E2 入口](../final_results/e2_20260907/README.md)、[Luna 历史源](../final_results/e2_20260907/luna_history.json) | md/json | Full 配对与历史身份 | 新旧 results 的 full/cells 的 `method_source/judge_source/*sha256` |
| [src-method] | method_archive | [开放模型方法归档](../final_results/a3_open_method_20260910/README.md) | md/json | 权重、环境、纯方法运行与恢复边界 | 入口链接的 manifest、results、raw index |
| [src-raw] | raw_archive | [raw index](../final_results/a3_open_judge_20260910/raw_index.json)、[manifest](../final_results/a3_open_judge_20260910/archive_manifest.json) | json | 原件、版本、哈希、脱敏配置、费用来源 | 逐文件路径/size/SHA-256；`judge_profile` |
| [src-inputs] | case_inputs | [0010 NL](../selected_seed_examples/llms_emp_feedback_final_0010/nl.txt)/[STM](../selected_seed_examples/llms_emp_feedback_final_0010/stm0.puml)，[0003 NL](../selected_seed_examples/llms_emp_feedback_final_0003/nl.txt)/[STM](../selected_seed_examples/llms_emp_feedback_final_0003/stm0.puml)，[0009 NL](../selected_seed_examples/llms_emp_feedback_final_0009/nl.txt)/[STM](../selected_seed_examples/llms_emp_feedback_final_0009/stm0.puml) | source-code | 三例的直接源证据 | 0010 STM:15/16/19；0003 STM:12；0009 STM:2/51至59，NL:12/13 |
| [src-a4] | a4_design | [A4 学术解释（固定 umbrella commit）](https://github.com/HansBug/research_ideas/blob/8b4715200d85140a07294fd2aacd29fb31f51ed4/project_1_llm_state_machine_modeling/talks/2026-09-10-实验-A4谓词执行反馈消融与论文叙事.md) | md/git-commit | 互补干预与限制，不引入 A4 数字 | §2.1/2.2，固定候选与末端屏蔽 |
| [src-code] | arithmetic | [原分析器](../discover_matrix/docs/generations/a3_20260910/analyze_a3.py)、[开放模型分析器](../discover_matrix/docs/generations/a3_20260910/analyze_open_judge.py)、[表格导出](../discover_matrix/docs/generations/a3_20260910/summarize_four_models.py) | source-code | 复算过滤、集合操作和全部表格 | `per_round/content_breakdown`；`tables` |

### A.3 Claim-evidence map

表内强度区分冻结事实与机制推断。病例采用目的选样；人工阅读此处指本次 AI 对源文本的逐条核对，不是新增人类标签。

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <a id="clm-design"></a>[clm-design] | A3-DESIGN | A3 移除中间引导，保留可选谓词执行/发布 | classification | [src-protocol] §1至3 消费者关闭表 | [cmd-verify]；人工对照关闭表与 runner | high | 组合消融，非等预算 |
| <a id="clm-eval"></a>[clm-eval] | A3-EVAL | 外部双读/仲裁与 K/N/I、strict/hit 定义 | classification | [src-protocol] §5至6；[src-code] `per_round` 及归档 verifier | [cmd-verify] [cmd-tables] | high | 自动标签不等于人工金标准；人工确认 0 |
| <a id="clm-main"></a>[clm-main] | A3-MAIN | 完整主表、有效量/I、模型等权与 pooled | count | [src-old]/[src-open] `/models/*/{a3,full}/reports` 与 metrics | [cmd-verify] [cmd-tables] | high | 同一模型三轮 pooled；计数差非语义迁移 |
| <a id="clm-rounds"></a>[clm-rounds] | A3-ROUND | 24 行逐轮及 12/12 命中下降 | count | 同上 `/per_round/{1,2,3}`；reports 按 round 筛选 | [cmd-tables] | high | 轮次相关 |
| <a id="clm-coverage"></a>[clm-coverage] | A3-COVER | hit@3/@all、L 分层和共有/独有 | count | 同上 metrics/tiers 与 comparison/content/partitions | [cmd-verify] [cmd-tables] | high | 集合键为 ledger ID+round，不是报告配对 |
| <a id="clm-funnel"></a>[clm-funnel] | A3-FUNNEL | 生成、绑定、执行、发布计数 | count | 同上 a3/cells/*/generation_mapping 与 funnel | [cmd-tables] | high | binding_precise 不等于适用或执行成功 |
| <a id="clm-content"></a>[clm-content] | A3-CONTENT | 条件/行为减少、不可达保留、effect 异质 | count | 同上 comparison/content/axes；[src-ledger] axes | [cmd-verify] [cmd-tables] | high（计数）/medium（解释） | 探索性分层，无单组件因果识别 |
| <a id="clm-case-loss"></a>[clm-case-loss] | A3-CASE-LOSS | Muse 0010/r1 遗漏 auto-final 接管路径 | trace | [src-open] muse/full report `0010:r1:issue:1`，a3 同格全部两报告；[src-inputs] 0010 | [cmd-cases]；人工核对 NL/STM 与理由 | high（样例）/medium（机制） | 同格全枚举证实遗漏；不能拆分各删除阶段 |
| <a id="clm-case-muse"></a>[clm-case-muse] | A3-CASE-MUSE | Muse 0003/r1 三个来源混淆 I | trace | [src-open] muse/a3 reports `0003:r1:issue:0/1/2`；full 同格；[src-inputs] 0003 | [cmd-cases]；人工核对作者边与派生表示 | high（冻结裁定） | 该 pair 台账为空，I 由核心有效性判断；不据此推断全部 I |
| <a id="clm-case-qwen"></a>[clm-case-qwen] | A3-CASE-QWEN | Qwen 0009/r1 保留不可达、报告13→2、hit5→2 | trace | [src-open] qwen full/a3 reports 同格，`VU-0009-01`；[src-inputs] 0009 | [cmd-cases] | high（样例） | 13 份报告含重复关系，非13个缺陷 |
| <a id="clm-ci"></a>[clm-ci] | A3-CI | 九簇区间及不统一显著的边界 | count/risk | [src-old]/[src-open] comparison/cluster_bootstrap_95pct、bootstrap_seed | [cmd-verify] [cmd-tables] | high | 10000 次，九簇；无 strict 区间、p值、多重校正 |
| <a id="clm-limits"></a>[clm-limits] | A3-LIMIT | 历史配置、预算、判定误差与 A4 互补边界 | risk/narrative | [src-protocol] §4至6；[src-a4] §2；上述主结果 | 人工对照协议、配置与干预；[cmd-verify] | medium | 单组件作用及 A3×A4 交互未知；需独立干预才能补齐，不削弱冻结计数事实 |

### A.4 复验命令

以下均从仓库根执行，无 provider 调用。先运行 `[cmd-verify]`，再输出 `[cmd-tables]`；校验器重算逐报告/关系、分层和 bootstrap，表格脚本按同一冻结数组导出本文全部数值表，不写回结果。

<a id="cmd-verify"></a>**[cmd-verify]：新旧归档核验**

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a3_20260910/verify_archive.py
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a3_20260910/verify_archive.py --archive project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/a3_open_judge_20260910 --model qwen --model muse
```

<a id="cmd-tables"></a>**[cmd-tables]：主表、24 行、分层、区间及合计**

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a3_20260910/summarize_four_models.py
```

<a id="cmd-cases"></a>**[cmd-cases]：三组案例全格报告、关系与原件 hash**

公开 JSON 包含主张、裁定和理由，足以核对本文样例解释。下段同时核验原方法/judge hash，后半部分需本地受限原件；fresh clone 缺原件时不能声称完成该项验证。`full/cells` 给出完整相对路径，A3 原绝对路径按稳定 runs 后缀解析。

```python
from pathlib import Path
import hashlib, json
p = Path('project_1_llm_state_machine_modeling/paper_stm_issue_discover')
root = Path('runs/paper1/a3_open_judge_20260910')
d = json.loads((p/'final_results/a3_open_judge_20260910/results.json').read_text())
for model, pair in [('muse','0010'), ('muse','0003'), ('qwen','0009')]:
    for arm in ['full','a3']:
        data = d['models'][model][arm]
        reports = [r for r in data['reports'] if r['pair_id']==pair and r['round']==1]
        hits = {e for r in reports if r['validity']=='VALID_KNOWN' for e in r['full_ledger_ids']}
        print(model, pair, arm, len(reports), sorted(hits))
        for r in reports:
            print(r['original_report_id'], r['published_claim'], r['validity'], r['reason'])
        c = next(c for c in data['cells'] if c['pair_id']==pair and c['round']==1)
        for kind in ['method','judge']:
            if arm=='a3' and kind=='method':
                f = root/Path(c['source']).relative_to(Path(c['source']).parents[4])
                expected = c['sha256']
            else:
                f = (root if arm=='a3' else p)/c[kind+'_source']
                expected = c[kind+'_sha256']
            assert 'sha256:'+hashlib.sha256(f.read_bytes()).hexdigest()==expected, f
```

案例作者源 NL/STM 的 SHA-256（按 0010、0003、0009 顺序）如下，可用 `sha256sum` 对 A.2 的六个输入文件复核：

| pair | NL SHA-256 | STM SHA-256 |
| --- | --- | --- |
| 0010 | `f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8` | `73021d0499bdbbc34299e07733dda58162aefdf297e57bd6aae76da940aaed53` |
| 0003 | `9fe426ba761d5a52c3b670f35410502a5289bdd9489c4a9bfa983e34d565040c` | `c82a800174e833df461aa14837651ad835a7ae146f84a9939cacac05e643e821` |
| 0009 | `b7425c44960b36c3534f118279e347786d4074191efea7bf9a7c5ba032c9e82c` | `fa210ede8e3af220ab1c96a5504e93dd8bccf4d4e06af68d15c988654c76ef53` |

<a id="cmd-history"></a>**[cmd-history]：冻结与后续修改考据**

```bash
git log --follow --date=iso -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/2026-09-10-20-39-37-a3-four-model-results.md
```

**生成、执行、发布复算表。** 表内各列不是全都构成顺序相减的漏斗：精确绑定标记描述同一实例身份，谓词为空时也可能为真；executed 只计 `execution_status=executed`，其余 unknown 包含 unsupported 等降级；W 列覆盖全部生成候选，也包括随后拦截的报告。[clm-funnel]

| 模型 | 生成 | 精确绑定标记 | executed | true/false/unknown | true拦截 | coverage gap | 发布 | W0/W1/W2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sonnet | 803 | 800 | 372 | 34/338/431 | 34 | 85 | 684 | 85/372/346 |
| Luna | 902 | 894 | 404 | 116/288/498 | 116 | 116 | 670 | 126/416/360 |
| Qwen | 379 | 378 | 215 | 4/211/164 | 4 | 17 | 358 | 17/155/207 |
| Muse | 509 | 506 | 235 | 2/233/274 | 2 | 12 | 495 | 12/262/235 |

四模型均满足生成数=发布数+true 拦截+coverage gap。true/false/unknown 总和等于生成数，W 总和也等于生成数，但 W2 不等于 false 数量或外部有效数。公开 generation_mapping 支持逐项核销，不能把 unknown 或 W1 写成已验证缺陷。

**运行、恢复与原件边界。** 方法依次运行开放模型，总 method 并发上限 16；共享 judge 总额度 24，在 page9 A4 占用 8 时 A3 上限 16，确认其无 Luna worker 后才使用 24。开放模型复用远端 GPU 4至7、既有权重与独立 conda；部署命令、版本和推理参数见[E1 复现附录](./model_readiness_20260906/2026-09-07-11-55-00-reproduction.md)及 [src-method]。调度不改变 54×3 分母。

Qwen 0002/r2 method 从首次原始回复的相邻精确字段块无损恢复，保留六次失败，不新增模型调用。Qwen 0000/r1 judge 保留四个成功阶段，仅续接失败关系节点的六轮历史及中性形状反馈；没有手选标签。Sonnet/Luna 的既有绑定重放与包裹恢复按 [src-protocol] 保留，不能统称全部正常一次成功。归档含开放 judge 原件 6182 个、1869223111 字节；完整原件及 method 索引在本地 ignored runs，公开 JSON 只保证冻结标签算术可复算。[src-raw]

费用、endpoint、配置白名单和历史价格来源保存在 manifest；这些是声明费率与用量审计，不是代理实际账单。本报告不推算未记录费用，也不据此建立等成本对照。历史 26 项定向测试及篡改反例见[核验原件](../final_results/a3_open_judge_20260910/verification/a3-final-tests.xml)和[篡改检查](../final_results/a3_open_judge_20260910/verification/adversarial-checks.json)，不等于本轮新跑全仓库测试。

[src-protocol]: ../discover_matrix/docs/generations/a3_20260910/preregistered.md
[src-old]: ../final_results/a3_20260910/results.json
[src-open]: ../final_results/a3_open_judge_20260910/results.json
[src-summary]: ../final_results/a3_open_judge_20260910/four_model_summary.json
[src-ledger]: ../discover_matrix/ledger_v2/ledger.json
[src-full]: ../final_results/e2_20260907/README.md
[src-method]: ../final_results/a3_open_method_20260910/README.md
[src-raw]: ../final_results/a3_open_judge_20260910/raw_index.json
[src-inputs]: ../selected_seed_examples/README.md
[src-code]: ../discover_matrix/docs/generations/a3_20260910/summarize_four_models.py
[src-a4]: https://github.com/HansBug/research_ideas/blob/8b4715200d85140a07294fd2aacd29fb31f51ed4/project_1_llm_state_machine_modeling/talks/2026-09-10-实验-A4谓词执行反馈消融与论文叙事.md
[clm-design]: #clm-design
[clm-eval]: #clm-eval
[clm-main]: #clm-main
[clm-rounds]: #clm-rounds
[clm-coverage]: #clm-coverage
[clm-funnel]: #clm-funnel
[clm-content]: #clm-content
[clm-case-loss]: #clm-case-loss
[clm-case-muse]: #clm-case-muse
[clm-case-qwen]: #clm-case-qwen
[clm-ci]: #clm-ci
[clm-limits]: #clm-limits
[cmd-verify]: #cmd-verify
[cmd-tables]: #cmd-tables
[cmd-cases]: #cmd-cases
[cmd-history]: #cmd-history
