# Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering

## R1.5 strict seed 全文核验结论

| 字段 | 当前判断 |
|---|---|
| candidate_id | `req-mermaid-statechart` |
| source_batch | baseline / local fulltext |
| local_source | [`baselines/req/`](../../../../baselines/req/) |
| paper_title | `Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering` |
| strict_seed_grade | `SS-B` |
| artifact_usability | `SA-4` |
| R2 可用性 | `related-work-only / private-data-boundary` |
| 当前结论 | 论文任务与 `NL requirements -> Mermaid.js statechart` 高度贴合，但核心 Volvo Cars / Car Weaver 需求、人工 statecharts、专家测试与微调数据均未公开；只能作为任务边界、related work 和不可复现工业私有 seed 证据，不能计入 PR-R2 主 seed 可交接下限。 |

## P1/P2/P3/P4 核验

| 谓词 | 判断 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | `paper_content.txt` Page 1--2 摘要和引言说明从自然语言需求生成 statechart；`DESC.md` 与 `ASSETS.md` 记录输入为 Volvo Cars / Car Weaver product function requirements。 |
| P2_T0_STM_FAMILY | pass with caveat | `paper_content.txt` Page 15 左右描述模型生成 Mermaid.js syntax 并渲染 visual statecharts；输出是 Mermaid.js statechart / state machine family。caveat：论文级输出偏可视化 statechart，缺少公开机器可读样本来核验 guard/action/time 语义。 |
| P3_GENERATION_RELATION | pass | `paper_content.txt` Page 7--15 描述需求预处理、合成数据扩充、GPT-3.5/GPT-4/GPT-4o 微调或调用，以及基于输入需求生成 Mermaid.js statechart 的流程。 |
| P4_EVIDENCE_POINTER | pass | 本目录保存 `paper.pdf`、`paper_content.txt`、`bibtex.bib`；源目录 [`ASSETS.md`](../../../../baselines/req/ASSETS.md) 已核到无公开代码 / 无公开数据 / 无公开复现包。 |

## SS / SA / 排除码

| 维度 | 判断 | 说明 |
|---|---|---|
| SS | `SS-B` | 论文层面满足 NL 输入、statechart 输出和生成关系；但主数据为工业私有需求和人工 statecharts，公开论文只能支持任务存在性与方法描述，不能支持可复验样本冻结。 |
| SA | `SA-4` | 论文 PDF 公开，但核心数据、训练集、专家测试、输出样本、代码和逐样本评估表均未公开；原始数据属于 Volvo Cars / Car Weaver 私有资产。 |
| 排除码 | none for literature relation | 不触发 protocol、process、formal-spec-only 或 repair-only；但触发 `R_PRIVATE_DATA` / `R_NO_REPRODUCIBLE_ARTIFACT`，因此不得进入主 R2 seed 下限。 |

## 可抽取 seed 边界

可用于论文叙述的内容：

1. 证明工业汽车软件中存在 `natural language product function requirements -> Mermaid.js statechart` 的高度贴近任务。
2. 证明仅有论文级描述和专家评审不足以支持可复验 `<NL, STM_0>` seed 冻结。
3. 作为 PR-R2 样本选择的反例：任务贴合不等于 artifact 可用。

不可用于 PR-R2 主样本的内容：

1. Volvo Cars / Car Weaver 原始需求。
2. 人工 statecharts、专家测试用例和评分表。
3. GPT 微调训练数据、合成扩充数据、prompt-completion 对和代码。

## R2 可用性

`related-work-only / private-data-boundary`。该文不应计入 `SS-A/SS-B + SA-1/SA-2` 主 seed 下限。若后续需要类似工业风格样本，应在本项目另行构造可公开、可授权、可追踪的 `<NL, STM_0>` pair，而不是声称复现该论文私有数据。

## 待补 / 主要阻塞

- 主要阻塞：核心需求、人工 statecharts、专家测试与评分表未公开。
- 主要阻塞：无公开代码、训练脚本、模型版本锁定或 artifact DOI；许可 / 再分发不再单独作为升绿阻塞。
- 待补：若未来作者公开数据或给出明确申请渠道，可重新评估 `SA-4 -> SA-2/SA-1`；当前不得主动假定可获取。
