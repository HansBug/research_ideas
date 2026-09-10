# 论文图表与来源

所有图内文字、图例与 Figure 题注为英文。示意图以可编辑飞书画板协作，仓库保留从飞书导出的 SVG 及原生节点；数据图由 matplotlib 从冻结 JSON 生成。SVG 用于论文矢量排版，PNG 用于预览。源数据以 S0–S6 为准，不手工调整图中数字。

| 对象 | 正文位置 | 文件 / 来源 | 版面预算 |
| --- | --- | --- | ---: |
| Figure 1：方法与说明性案例 | §4.1 | [method.svg](./figures/method.svg)；S6 | 0.50 页 |
| Figure 2：冻结 K/N/I 与 A4 核算路径 | §5.4 | [adjudication.svg](./figures/adjudication.svg)；S4/S7 | 0.60 页 |
| Figure 3：四模型分层覆盖 | §6.1–6.2 | [coverage.svg](./figures/coverage.svg)、[PNG](./figures/coverage.png)、[PDF](./figures/coverage.pdf)；S1 | 0.45 页 |
| 表 1：语料与参考问题 | §5.2 | S0；54 行结构统计，145 条台账 | 0.25 页 |
| 表 2：基线与消融条件 | §5.3 | S1–S4 的真实干预合同 | 0.22 页 |
| 表 3：完整方法与基线 | §6.2 | S1/S5；8 行，三覆盖、两精确率 | 0.35 页 |
| 表 4：三项消融 | §6.3–6.5 | S2/S3/S4；9 行 | 0.40 页 |

总浮动体预算 2.77 页，包含在 [正文十页预算](./README.md) 内。实际英文模板排版仍需验证，不将 SVG 尺寸换算成已实现的页数。

Figure 1 的 Idle→Running→Halt 为说明性案例，不计入实验。Start/Stop 是迁移事件；Halt 无出口，描述要求 Stop 后返回 Idle。`may_reach(Halt, {Idle})` 与 `transition_exists(Running, Stop, Halt)` 是论文层面的查询简写，后者 true 只反驳完全对应的缺边主张。

Figure 2 使用冻结 relation-first policy：非 A0 且 FULL/PARTIAL 可以计 K，包括 D0；严格分子限 K/N 且 D1/D2。右侧先处理原 true 同主张指定 I，再内容等价复用，最后新增评价，不能交换顺序。

## 数据图复现

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/story/figures/plot_coverage.py
```

命令核验 24 组原始比例及分母，生成 SVG/PNG/PDF，不调用模型。四面板共用 0–100% 横轴，右侧为 Full−Baseline 百分点差；线段表示条件配对。误差区间按九描述簇计算并在正文说明，不以报告级误差条替代。

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
