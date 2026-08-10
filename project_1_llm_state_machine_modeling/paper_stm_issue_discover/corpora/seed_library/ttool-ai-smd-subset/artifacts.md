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
| 引用 / 来源说明 | citation note | 公开 GitHub artifact 可作为论文引用与来源入口；R2 若搬运 XML/desc 到本仓库，重点记录 URL、commit/hash 与引用原作，许可 / 再分发不作为升绿阻塞。 |
| URL stability | medium-high | HAL/DOI稳定；GitHub URL公开，源`ASSETS.md`已记录pinned HEAD和`results.ods` raw ETag，但本轮未重新联网核验。 |
| Conversion readiness | boundary | 可从公开 `.desc` / `.xml` 抽取 NL 规格与生成 SMD；但 `after` 时间约束、signal send/receive、guard/action 赋值和 LLM 生成残余错误是 PR-R3 converter blocker。当前不计入 PR-R2 主 seed 下限。 |

## R2 / R3 可用性判断

R2 可用性为**不计主 seed 的 converter pressure / timed boundary**。公开 artifact 提供自然语言系统规格、TTool-AI 生成模型和评分结果表，适合做“固定 artifact 抽取 / 审计”和 PR-R3 转换压力测试；但在完成 case-level T0 isolation 或 timed-SMD 规范化合同前，不适合作为 PR-R2 四例主 seed。

R2建议入口：

1. 以GitHub pinned HEAD `f2c52282cb7a826c31e7ab512356d42230c6d321`作为冻结artifact版本。
2. 优先抽取`platooning`、`spacebasedsystem`、`AutomatedBraking`中的系统规格和`.xml`模型。
3. 将`results.ods`作为评分与时间结果的辅助证据，而不是状态机结构的唯一来源。
4. 在run record中记录TTool版本、OpenAI模型、调用日期和随机性风险；不要把重新调用GPT得到的结果与论文公开XML混为同一artifact。

## artifact风险

1. **引用说明待补**：从本地 `bibtex.bib`、`paper_content.txt`、源 `ASSETS.md` 和 `DESC.md` 尚未整理出完整引用 / commit / hash 说明；这不作为许可阻塞。
2. **完整源码不足**：公开仓库主要保存实验输入/输出/结果，TTool-AI能力在TTool工具中；如要改造baseline，需要另查TTool本体。
3. **provider drift**：论文实验绑定TTool nightly build October 2023与ChatGPT 3.5 turbo，复跑会受模型版本、temperature和API行为变化影响。
4. **SMD语义转换**：公开模型可能包含guards、actions、signals和`after`时间约束；若目标repair pipeline只接受简化FSM，必须显式转换并保留审计记录。

## 主 seed 排除说明

当前不计入 `SS-A/SS-B + SA-1/SA-2` 主 seed 下限。若未来要升级，必须补一份 case-level 记录，说明选定 `.xml` 中的 `after` / timeout / signal / guard-action 是否保留、抽象或剔除，以及该处理是否影响后续 source-level issue discovery / repair / closure 评价。
