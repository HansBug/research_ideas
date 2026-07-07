# Completion of SysML state machines from Given-When-Then requirements — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `completion-sysml-gwt` |
| 标题 | Completion of SysML state machines from Given-When-Then requirements |
| 年份 / venue | 2024 / SoSyM |
| 当前角色 | P0 路线近邻 / 条件对照 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | GWT/Gherkin 需求 |
| 模型 / STM 输出 | SysML SMD；已有 states，补 transitions |
| 修正 / 补全 / refinement 方法 | Detect-and-translate：解析 GWT，匹配 MetaReq / MetaFragment / refinement rules，生成 source/target/trigger/guard/effect 与 traceability |
| feedback 来源 | grammar / feasibility / role / model-aware semantic checks + analyst review |
| 自动化程度 | 半自动 |
| LLM / agent 角色 | GPT-3.5 只辅助需求预处理，非核心 repair |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

当前只能作为唯一 P0 路线近邻 / 条件对照：`<GWT requirements, partial SysML SMD> -> completed SMD`；但 partial SMD / states 是否严格由同一组 GWT/NL 生成仍需二次核验。它不是 seed，也不是无人化 formal repair loop。

### 3.1 为什么不能直接升级为严格 baseline

| 证据点 | 论文原文位置 | 对当前任务的含义 |
|---|---|---|
| 只明确“partial SysML model + requirements” | `paper_content.txt` lines 10--16 | 起点是部分 SysML 模型而不是完整、可追溯的 `<NL, STM_0>` 成对证据。 |
| states 由 analyst 已知，transitions 再补全 | `paper_content.txt` lines 417--451 | `STM_0` 更像预置骨架；不足以单凭论文证明它由同一 NL 严格生成。 |
| 原始需求要先重写成 GWT | `paper_content.txt` lines 988--1003 | healthcare case 中 ChatGPT 重写 + 人工精炼需求，说明 NL 预处理本身不是无人化闭环 repair。 |
| 评估是与 literature model 做近似对照 | `paper_content.txt` lines 1148--1170 | 结果证明“接近性 / 更丰富 transitions”，但不是 `<NL, STM_0> -> STM_k` 的严格 baseline 复现实验。 |
| 作者把方法定位为 semi-automatic completion | `paper_content.txt` lines 1171--1226 | 论文自述为半自动补全，并讨论 AI 可认证性问题；不能直接写成无人化 repair loop。 |

### 3.2 当前可写法

- 可以写成：`GWT/NL + partial SysML SMD -> completed SMD transitions` 的**路线近邻 / 条件对照**。
- 不能写成：严格 baseline、全绿 baseline、无人化 repair loop，或 `<NL, STM_0> -> STM_k` 已被充分证明。

## 4. 证据位置

`paper_content.txt` 摘要、§4--§7、§11、§12 与 GPT-3.5 讨论；旁路核验材料复核。

## 5. 主要风险与使用边界

依赖结构化 GWT 与预先给定 SysML 结构/状态；未见公开机读模型、代码或完整数据包；评价偏 case-study。
