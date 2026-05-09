# `ttool_ai/` — System Architects Are not Alone Anymore (2024)

## 论文与上游引用

- **论文**：Apvrille & Sultan, *System Architects Are not Alone Anymore: Automatic System Modeling with AI*, **MODELSWARD 2024**. [会议页](https://www.scitepress.org/PublishedPapers/2024/123917/)
- **baselines 单篇分析**：[`../../../baselines/ttool-ai/`](../../../baselines/ttool-ai/)
- **数据集公开入口**：[GitHub zebradile/ttool-ai](https://github.com/zebradile/ttool-ai)
- **可获取性**：🟢（GitHub 公开）

## 任务

NL 系统规范 → AVATAR (TTool 元模型) 设计模型，含 block diagrams + 状态机 panels。

**关键特性**：transition 字段含 `after_min` / `after_max` / `delay_distribution_law` / `probability` —— 直接编码**时间自动机语义**与**概率迁移**。

## 文件清单

| 文件 | 行数 | 列数 | 内容 |
|------|------|------|------|
| [`models.parquet`](./models.parquet) | 15 | 21 | 15 个 AVATAR 设计模型（system spec + raw_xml + panel 计数） |
| [`state_machine_panels.parquet`](./state_machine_panels.parquet) | 122 | 15 | 122 个状态机面板（panel-level XML + state/transition 计数） |
| [`states.parquet`](./states.parquet) | 708 | 17 | 摊平后的 708 状态节点（含坐标 / 类型 / 连接点） |
| [`transitions.parquet`](./transitions.parquet) | 798 | 26 | 摊平后的 798 迁移（**含时间约束 + 概率字段**） |
| [`human_review.parquet`](./human_review.parquet) | 116 | 29 | 公开人评结果（多类记录：case-level / split-level / overall） |
| [`raw/`](./raw/) | — | — | 原始 ods + spec markdown 等（**当前为空**，详见 §`原始资源现状`） |

## 关键字段

`models.parquet`：

- `case_name`（`Platooning` / `Space-based` / `Automated Braking`）+ `variant_name`
- `input_spec_text`（输入 NL 系统规范）
- `raw_xml`（输出完整 AVATAR XML，含所有 block + state machine panel）
- `state_count` / `transition_count` / `state_machine_panel_count`

`transitions.parquet` 时间约束字段：

- `guard_or_trigger`、`actions`
- `after_min`、`after_max`（时间下/上界）
- `extra_delay_1`、`extra_delay_2`
- `delay_distribution_law`（分布律）
- `compute_min`、`compute_max`、`probability`

## 真实样本（一条）

Platooning Platoon1 变体（23 状态 47 迁移 6 SM panel）：

```
INPUT (input_spec_text):
  Platooning is a transportation technique that consists in grouping trucks or
  vehicles together to reduce CO2 emissions. A platoon consists of one or several
  vehicles, the first one in the platoon playing the role of the platoon leader,
  the other ones playing the role of followers. ...

OUTPUT (raw_xml):
  完整 AVATAR XML，含 6 个 SM panel + 每个 panel 的 state coordinates +
  每条 transition 的 (guard, action, after_min, after_max, distribution, probability)
```

## 原始资源现状（⚠️ P0 待补）

build 脚本读取的原始资源：

- `raw/ttool-ai/platooning/platoonings.md`
- `raw/ttool-ai/AutomatedBraking/automatedbraking.md`
- `raw/ttool-ai/SpaceBasedSystem/specification_spacebasedsystem.md`
- `raw/ttool-ai/results.ods` —— 公开人评 ods 表
- 以及 GitHub 仓库克隆的 spec/XML 树

**当前 `/tmp/baseline_double_green/raw/ttool-ai/` 已失效**。若要重跑 build：

```bash
git clone https://github.com/zebradile/ttool-ai raw/repo
# 然后把对应 spec / ods 路径复制到 raw/ 子目录里，路径与 build_*.py 中保持一致
```

## 复用性建议

- ⚠️ **summary-level human review，无 reference output**：人评 116 行只有 input + pred + 评分，没有 gold reference；**不适合**做严格 1:1 input/ref/pred 对齐
- ✅ **最适合做时间约束 + 层次状态机 baseline**：transitions 表的 `after_min/after_max` 字段直接对应时间自动机语义
- ✅ 适合方法对比：把"3 个真实欧洲项目案例 → 解析后 15 model 变体"作为人工总评分协议的 ground truth 流程
- ⚠️ 案例规模小（3 个 system），不适合做大规模数据驱动训练
