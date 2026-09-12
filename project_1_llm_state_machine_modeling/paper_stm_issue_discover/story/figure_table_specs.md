# 论文图表与来源

所有图内文字与图例为英文；图题与表题一律中文（用户 2026-09-11 决定）。示意图以可编辑飞书画板协作，仓库保留从飞书导出的 SVG 及原生节点；数据图由 matplotlib 从冻结 JSON 生成。SVG 用于论文矢量排版，PNG 用于预览。源数据以 S0–S6 为准，不手工调整图中数字。

| 对象 | 正文位置 | 文件 / 来源 | 版面预算 |
| --- | --- | --- | ---: |
| 图 1：方法与说明性案例（画板） | §4.1 | [method.svg](./figures/method.svg)；S6 | 0.50 页 |
| 图 2：中间引导生命周期示例（mermaid 画板） | §4.3 | [guidance_lifecycle.svg](./figures/guidance_lifecycle.svg)，源 [guidance_lifecycle.mmd](./figures/guidance_lifecycle.mmd)；S6 | 0.40 页 |
| 图 3：语料规模与参考问题分布 | §5.2 | [corpus.svg](./figures/corpus.svg)；S0 | 0.35 页 |
| 图 4：冻结的关系优先判定规则（画板，2026-09-11 第六轮起只保留单面板，原 (b) 路径面板按用户决定删除） | §5.4 | [adjudication.svg](./figures/adjudication.svg)；S7 | 0.45 页 |
| 图 5：四模型分层覆盖 | §6.1 | [coverage.svg](./figures/coverage.svg)；S1 | 0.45 页 |
| 图 6：四模型配对差值与九簇区间 | §6.2 | [main_delta.svg](./figures/main_delta.svg)；S1 | 0.35 页 |
| 图 7：四模型关闭检视事实的配对差值（RQ3；2026-09-12 起含 A1-ext 三模型） | §6.3 | [rq3_delta.svg](./figures/rq3_delta.svg)；S2 | 0.35 页 |
| 图 8：移除中间引导的配对差值（RQ4） | §6.4 | [rq4_delta.svg](./figures/rq4_delta.svg)；S3 | 0.35 页 |
| 图 9：屏蔽执行反馈（RQ5；纵轴从 60% 起，用户 2026-09-11 决定保持） | §6.5 | [rq5_execution.svg](./figures/rq5_execution.svg)；S4 | 0.35 页 |
| 表 1：最接近工作四维比较 | §2.2 | S7 closest-work 矩阵 | 0.35 页 |
| 表 2：中间引导阶段表（阶段、执行者、输入、输出、停止条件） | §4.3 | S6 method | 0.30 页 |
| 表 3：12 种类型化谓词及其领域来源 | §4.4 | S6；[predicate_provenance.md](../related_work/provenance/predicate_provenance.md) 与注册表 `four-family-12-core.v1` | 0.35 页 |
| 表 4：语料与参考问题 | §5.2 | S0；54 行结构统计，145 条台账 | 0.27 页 |
| 表 5：基线与消融条件 | §5.3 | S1–S4 的真实干预合同 | 0.22 页 |
| 表 6：gpt-5.6-luna 基线与 Full 完整结果（含严格覆盖与 D2-only 覆盖） | §6.1 | S1/S5；D2-only 与严格覆盖由 cells.json 与 raw 逐报告重算 | 0.30 页 |
| 表 7：四模型基线与 Full（含严格与 D2-only 覆盖） | §6.2 | S1/S5；8 行 | 0.40 页 |
| 表 8：四模型关闭检视事实（8 行，含 L2 hit@1 与 L2 hit@all） | §6.3 | S2（A1 + A1-ext） | 0.40 页 |
| 表 9：移除中间引导 | §6.4 | S3；8 行 | 0.35 页 |
| 表 10：Full 各阶段产出计数 | §6.4 | E2 raw 逐格 `stage_outputs.execute_batch` 计数器与 v61 raw method 输出；候选总数 = admitted_llm + frontier（含 unresolved 与 domain_invariant）+ exact_s2_scout + execution_probe，源迁移闭合不计入 | 0.30 页 |
| 表 11：屏蔽执行反馈 | §6.5 | S4；8 行 | 0.30 页 |
| 表 12：各谓词族的执行回执与 W2 报告 | §6.6 | E2 `cells.json` 的 predicate_receipts / candidate_evidence；gpt-5.6-luna 用 evaluate_rq3 输出；旧 ID 按 G4→G3、R4→R3、V4→V1 映射，论文只出现 12 条谓词 | 0.40 页 |

按用户 2026-09-11 第二轮批注，每个 RQ 各配一张表和一张 matplotlib 柱状图，主结果另配覆盖与精确率两张柱状图，语料另配分布图；第三轮批注再加谓词表。九图十二表（第五轮 AI 审稿批注后）的版面占用不再估算，而是用 IEEEtran 10pt 双栏会议模板（letter，与 overleaf/ 工程同一 IEEEtran 1.8b）实测：把九张图的 PDF（画板图经 PyMuPDF 转 PDF，柱状图按 `\textwidth`、分层覆盖图与判定图按 `\columnwidth`）与八张表（中文单元格按 5 个拉丁字符/汉字换成等宽英文占位）排入模板，只放浮动体、标题与摘要时为 6 页；填充 2000/4000/6000/8000 个英文单词的正文分别得到 9/10/13/15 页，不放浮动体时 4000/8000 词为 6/11 页。据此当前图表约占 5 页多，十页版面只剩约 4000 个英文单词的正文容量。按摘要中英对照实测的 0.59 词/汉字换算，约合 6800 个汉字正文；当前中文稿正文（不含表格、题注与参考文献）为 10454 个汉字，折合约 6200 词，排成英文约 13 页。把 Figure 5/6 叠成一图、Figure 7–9 叠成一图并把表 4 并入表 5 后重排，页数几乎不变（0/4000/6000 词分别为 6/10/12 页），说明省版面必须缩小图幅或删表，而不是合并题注。测试工程在 `/tmp/saner_budget/`，不入库；数字随图幅设计变化，英文排版阶段以 `overleaf/` 工程的 `make check` 为准。实际英文模板排版仍需验证，不将 SVG 尺寸换算成已实现的页数。

图 1 与图 2 的 Idle→Running→Halt 为说明性案例，不计入实验。Start/Stop 是迁移事件；Halt 无出口，描述要求 Stop 后返回 Idle。`may_reach(Halt, {Idle})` 与 `transition_exists(Running, Stop, Halt)` 是论文层面的查询简写，后者 true 只反驳完全对应的缺边主张。

图 4 使用冻结 relation-first policy：非 A0 且 FULL/PARTIAL 可以计 K，包括 D0；严格分子限 K/N 且 D1/D2。无执行反馈条件的报告与其余条件一样按同一协议评阅，图中不再单列路径。

## 数据图复现

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/story/figures/plot_coverage.py
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/story/figures/plot_bars.py --tables
```

第一条命令核验 24 组原始比例及分母并生成图 5；第二条从冻结归档生成图 3、6–9 的 SVG/PNG/PDF，断言各图所用数字与正文表格的冻结锚点一致，并打印表 3、表 5–7 的 Markdown 行以供逐字对拍。两条命令都不调用模型。四面板共用 0–100% 横轴，右侧为 Full−Baseline 百分点差；线段表示条件配对。误差区间按九描述簇计算并在正文说明，不以报告级误差条替代。

| 模型 | 层级 | 基线 | Full | 差值 pp |
| --- | --- | ---: | ---: | ---: |
| gpt-5.6-luna | L0 | 108/213 | 153/213 | +21.13 |
| gpt-5.6-luna | L1 | 72/105 | 73/105 | +0.95 |
| gpt-5.6-luna | L2 | 45/117 | 97/117 | +44.44 |
| claude-sonnet-5 | L0 | 111/213 | 133/213 | +10.33 |
| claude-sonnet-5 | L1 | 74/105 | 65/105 | -8.57 |
| claude-sonnet-5 | L2 | 56/117 | 93/117 | +31.62 |
| qwen3.8-27b | L0 | 110/213 | 165/213 | +25.82 |
| qwen3.8-27b | L1 | 66/105 | 68/105 | +1.90 |
| qwen3.8-27b | L2 | 49/117 | 78/117 | +24.79 |
| muse-glimmer-30b | L0 | 131/213 | 165/213 | +15.96 |
| muse-glimmer-30b | L1 | 77/105 | 79/105 | +1.90 |
| muse-glimmer-30b | L2 | 39/117 | 78/117 | +33.33 |

## 画板位置与导出

- 方法图：[飞书原生画板](https://scngnprmusv9.feishu.cn/docx/EGHDdqeV4om9mKxTiyxcBYU8nAh#doxcnlUgnwrSIS2RzQL8A94PZCd)，token `BnXpw4gl0hntpZbDALXckLJynhe`，原生源为 [method.whiteboard.json](./figures/method.whiteboard.json)。
- 判定图：[飞书原生画板](https://scngnprmusv9.feishu.cn/docx/EGHDdqeV4om9mKxTiyxcBYU8nAh#doxcn7eaqxUoaprxyfVtTfLG9gg)，token `TTlFwM8DlhOYqjbZoXbcliGUnCd`，原生源为 [adjudication.whiteboard.json](./figures/adjudication.whiteboard.json)。

后续修改同一画板后，用 `lark-cli --profile hansbug whiteboard +export --as user --whiteboard-token TOKEN --output-type svg --output ./PATH.svg --overwrite` 导出，并以 `--output-type raw` 保存原生节点；勿新建重复画板。导出后核验文本完整性、箭头、图例和裁切。本文两图 SVG 均含可选取的文本与矢量形状，可直接用于矢量排版。
