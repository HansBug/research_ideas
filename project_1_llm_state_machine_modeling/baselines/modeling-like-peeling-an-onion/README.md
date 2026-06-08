# Modeling Like Peeling an Onion：本地原文已补齐记录

## 当前状态

- **标题**：Modeling Like Peeling an Onion: Layerwise Analysis-Driven Automatic Behavioral Model Generation
- **作者**：Yike Huang, Ming Hu, Xiaohong Chen, Zhi Jin, Shuyuan Xiao
- **年份 / Venue**：ICSE 2026 Research Track / ICSE '26
- **官方页面**：[ICSE 2026 official page](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/278/Modeling-Like-Peeling-an-Onion-Layerwise-Analysis-Driven-Automatic-Behavioral-Model-)
- **DOI**：`10.1145/3744916.3787806`，当前可能尚未激活，需后续复核 ACM/DOI/publisher/author page。
- **PDF 来源记录**：用户于 2026-06-08 提供本地原文 PDF；当前不宣称有公开下载 URL，若后续确认 ACM/DOI/publisher/author page 再补。
- **本目录文件**：已包含 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`DESC.md`。
- **状态更新时间**：2026-06-08

## 阻塞解除说明

本条此前因缺少合法 PDF 原文而被记录为待补全文阻塞项。当前用户已提供本地原文 PDF，并已完成 `paper_content.txt` 提取，因此可以生成 `DESC.md` 并进入单篇可比分析。

本轮只记录本地原文来源，不声明公开 PDF 下载 URL。后续如果确认 ACM、DOI、publisher page 或 author page 提供公开入口，再补入 `bibtex.bib` 与 `DESC.md`。

## Project 1 初步关系

这篇论文提出 LATO，从自然语言 / textual requirements 自动生成可执行 UML activity diagrams。其方法是 LLM layerwise analysis：先抽取关键活动，再逐层解析嵌套关系，最后生成 PlantUML 活动图并通过语法检查闭环修复。

它属于 Project 1 的近邻行为模型工作：输入与 Project 1 高度相近，LLM 方法也有直接借鉴价值，但输出是 UML activity diagram / PlantUML activity diagram，不是状态机、Statechart 或 SysML state machine。因此不能标为 exact STM direct baseline，也不建议评为 `🟢`。

四条件初步建议：

| 条件 | 建议 | 说明 |
|---|---|---|
| LLM4Modeling | 🟢 | 明确使用 LLM 自动化生成建模工件 |
| NL 输入 | 🟢 | 输入为自然语言 / textual requirements |
| LLM 方法 | 🟢 | 使用 layerwise LLM pipeline、few-shot / CoT 和工具反馈 |
| STM 族输出 | 🟡 | 输出是可执行 UML activity diagrams，属于近邻行为模型，不是 exact STM |

`BASELINE评估` 建议为 `🟠`：弱相关但有方法借鉴价值。若后续总表将 UML activity diagram 明确纳入“状态机族近邻行为模型”口径，也可谨慎考虑 `🟡`，但不应评为 `🟢`。
