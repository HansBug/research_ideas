# A Comparison of LLMs for UML State Diagrams Generation

## R1.6 strict seed 全文核验结论

| 字段 | 结论 |
|---|---|
| bibliographic_id | DOI `10.38124/ijisrt/26feb1435`，2026-03-13 |
| strict_seed_grade | `SS-A` for task relation |
| artifact_usability | `SA-3` |
| 是否计入主 seed | 不计入。全文和 PDF 有 prompt、PlantUML listing 与结果图，但未见公开代码、数据包、原始输出 release 或 license。 |

## P1/P2/P3/P4 核验

| 谓词 | 判定 | 证据 |
|---|---|---|
| `P1_NL_INPUT` | 通过 | 摘要和方法明确从 textual system descriptions / natural-language prompts 生成 UML 2.5 state diagrams；案例为 traffic light、ATM、smart home lighting。 |
| `P2_T0_STM_FAMILY` | 通过 | 输出是 UML 2.5 state diagrams in PlantUML format；全文多处给出 PlantUML state code 与渲染图。 |
| `P3_GENERATION_RELATION` | 通过 | ChatGPT 4.1、Grok 3、Qwen3.5-Plus 接收 prompt 后生成 PlantUML state diagram。 |
| `P4_EVIDENCE_POINTER` | 论文级通过 / artifact 不足 | `paper_content.txt` lines around methodology、prompts、figures；但无机器可读完整实验包。 |

## 使用边界

该文适合作为 recent LLM state-diagram generation related work 和 prompt/评价维度证据；若要抽 seed，只能手工转写 PDF 中的 prompt 与 PlantUML 输出，并另记 reconstruction provenance，不得当作公开可复验 artifact。

## 风险

- 案例偏 toy / tutorial，不是控制系统 benchmark。
- 模型版本和 Web 工具环境依赖强；`Qwen3.5-Plus` 等命名应照原文记录，不外推官方模型谱系。
- 无原始 prompt/output 数据包；`SA-3` 不计四例下限。
