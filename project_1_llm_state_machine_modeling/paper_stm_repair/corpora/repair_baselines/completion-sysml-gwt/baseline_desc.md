# Completion of SysML state machines from Given-When-Then requirements — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `completion-sysml-gwt` |
| 标题 | Completion of SysML state machines from Given-When-Then requirements |
| 年份 / venue | 2024 / SoSyM |
| 当前角色 | P0 条件 baseline 候选 |
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

## 3. 与本论文 `<NL, STM_0> -> Better STM` 的关系

可作为当前唯一 P0 条件 baseline 候选：`<GWT requirements, partial SysML SMD> -> completed SMD`；但 partial SMD / states 是否严格由同一组 GWT/NL 生成仍需二次核验。它不是 seed，也不是无人化 formal repair loop。

## 4. 证据位置

`paper_content.txt` 摘要、§4--§7、结论与 GPT-3.5 讨论；旁路核验材料复核。

## 5. 主要风险与使用边界

依赖结构化 GWT 与预先给定 SysML 结构/状态；未见公开机读模型、代码或完整数据包；评价偏 case-study。
