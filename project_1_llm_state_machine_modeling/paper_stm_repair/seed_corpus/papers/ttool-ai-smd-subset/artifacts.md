# artifacts: ttool-ai-smd-subset

## 资源总览

| 项 | 当前状态 | 证据 / 说明 |
|---|---|---|
| PDF | present | 本地`paper.pdf`存在；SHA-256 `6585a29e5af8977c3a473ce6ec1c92ac1a4e7c135e998982c4391edf14128933`。 |
| paper_content.txt | present | 本地`paper_content.txt`存在；SHA-256 `6f60e41c62e40e881802f9c09e18be7760e817c070f6340b2697bcb4592a18c4`。 |
| BibTeX | present | 本地`bibtex.bib`存在；SHA-256 `cf2c53a9933069fada3e6173b86b6a515375d3341392301c7d943e7833eb5685`；BibTeX给出HAL URL和DOI `10.5220/0012320100003645`。 |
| Paper URL | stable | HAL: <https://telecom-paris.hal.science/hal-04483279>; DOI: <https://doi.org/10.5220/0012320100003645>。 |
| Code / artifact | public, partial | 论文§5.2给出公开GitHub仓库 <https://github.com/zebradile/ttool-ai>；源`ASSETS.md`记录default branch `main`、HEAD `f2c52282cb7a826c31e7ab512356d42230c6d321`。仓库主要是实验工件，不是完整TTool-AI源码。 |
| Dataset / outputs | public | 论文§5.2说明`platooning`、`spacebasedsystem`、`AutomatedBraking`目录包含系统规格和TTool-AI生成的`.xml`模型；源`ASSETS.md`还记录`results.ods`和补充工件目录。 |
| License / redistribution | pending | 本轮允许读取材料未给出GitHub仓库license，不能判定可再分发；R2若要搬运XML/desc到本仓库，需先人工核验license或仅记录URL与hash。 |
| URL stability | medium-high | HAL/DOI稳定；GitHub URL公开，源`ASSETS.md`已记录pinned HEAD和`results.ods` raw ETag，但本轮未重新联网核验。 |
| Conversion readiness | medium | 可从公开`.desc`/`.xml`抽取NL规格与生成SMD；需处理TTool XML结构、SysML SMD动作/信号、`after`时间约束和LLM生成残余错误。 |

## R2可用性判断

R2可用性为**可用但需约束**。公开artifact提供三类核心材料：自然语言系统规格、TTool-AI生成模型和评分结果表。它适合做“固定artifact抽取/审计”，不适合要求完全重跑生成过程得到同一输出。

R2建议入口：

1. 以GitHub pinned HEAD `f2c52282cb7a826c31e7ab512356d42230c6d321`作为冻结artifact版本。
2. 优先抽取`platooning`、`spacebasedsystem`、`AutomatedBraking`中的系统规格和`.xml`模型。
3. 将`results.ods`作为评分与时间结果的辅助证据，而不是状态机结构的唯一来源。
4. 在run record中记录TTool版本、OpenAI模型、调用日期和随机性风险；不要把重新调用GPT得到的结果与论文公开XML混为同一artifact。

## artifact风险

1. **license pending**：从本地`bibtex.bib`、`paper_content.txt`、源`ASSETS.md`和`DESC.md`无法确认artifact license。
2. **完整源码不足**：公开仓库主要保存实验输入/输出/结果，TTool-AI能力在TTool工具中；如要改造baseline，需要另查TTool本体。
3. **provider drift**：论文实验绑定TTool nightly build October 2023与ChatGPT 3.5 turbo，复跑会受模型版本、temperature和API行为变化影响。
4. **SMD语义转换**：公开模型可能包含guards、actions、signals和`after`时间约束；若目标repair pipeline只接受简化FSM，必须显式转换并保留审计记录。
