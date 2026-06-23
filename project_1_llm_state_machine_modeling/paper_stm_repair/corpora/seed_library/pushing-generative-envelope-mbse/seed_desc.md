# Pushing the Generative Envelope: Prompt Technique and Temperature for MBSE Artifacts

## R1.7 seed 方法编码

| 字段 | 当前判断 |
|---|---|
| candidate_id | `pushing-generative-envelope-mbse` |
| source_batch | direct baseline / local fulltext |
| local_source | [`baselines/pushing-the-generative-envelope-mbse-artifacts/`](../../../../baselines/pushing-the-generative-envelope-mbse-artifacts/) |
| paper | Crabb et al., RANLP 2025 |
| strict_seed_grade | `SS-B/ES-C` |
| artifact_usability | `SA-3` |
| seed 方法角色 | 上游 `NL -> SysML v2 state machine diagram` prompt/temperature 方法证据；不作为当前可直接冻结的 PR-R2 主样本。 |
| 当前结论 | 必须纳入 seed 文库，因为它明确研究自然语言题项经本地 LLM 生成 state machine diagrams；但由于只有两个题项、无公开逐次输出包/代码/数据包，只能作为 paper-only seed 方法证据与 prompt/temperature 变量参考。 |

## P1/P2/P3/P4 核验

| 谓词 | 结论 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | pass | 源目录 [`DESC.md`](../../../../baselines/pushing-the-generative-envelope-mbse-artifacts/DESC.md) 记录输入为 air purifier 与 vacuum 两个简短自然语言系统描述 / 任务说明；本地 `paper_content.txt` 记录实验围绕 MBSE artifact generation 的 prompt 输入。 |
| P2_STM_FAMILY | pass | 输出包括 SysML v2 requirements list 与 **state machine diagrams**；`DESC.md` 的“文献分类总结”明确输出模型类型为 SysML v2 state machine。 |
| P3_GENERATION_RELATION | pass | 方法是 local LLM prompting：zero-shot、one-shot、few-shot、CoT 与 temperature 设置直接生成 SysML v2 state machine diagrams；属于 `NL -> STM-family` 上游 seed 生成方法。 |
| P4_EVIDENCE_POINTER | pass for literature / weak for artifact | 本目录保存 `paper.pdf`、`paper_content.txt`、`bibtex.bib`；源目录 [`ASSETS.md`](../../../../baselines/pushing-the-generative-envelope-mbse-artifacts/ASSETS.md) 明确未发现公开代码、supplement、数据包或逐次输出。 |

## 方法与模型信息

| 项 | 记录 |
|---|---|
| generation actor | LLM。 |
| 模型 | Mixtral-8x7B-Instruct-v0.1、Llama-3-Smaug-8B。 |
| prompt / 流程 | zero-shot、one-shot、few-shot、CoT；temperature 为 0.2、0.6、0.95；对 air purifier 与 vacuum 两个题项重复生成。 |
| feedback / agent loop | 无自动 repair / verification feedback loop；主要是 prompt technique 与 temperature 的消融比较。 |
| 评价 | METEOR 与 SME feedback；偏工件级相似度/人工反馈，不是状态机语义验证。 |

## SS / SA 判定

- **作为 seed 方法集合：必须纳入。** 它回答的是“如何从自然语言题项生成 SysML v2 state machine diagram”，正属于当前 `<NL, STM_0> -> Better STM` 问题之前的上游 `NL -> STM_0` 生成方法。
- **作为 PR-R2 主样本：暂不计数。** 公开资产不足：没有 paper-specific code、raw prompt/output bundle、逐次 generated STM、独立 dataset 或结果 workbook；只能从论文正文手工重建。
- **当前等级：`SS-B/ES-C + SA-3`。** 文献关系成立，但 artifact 是 paper-only，样本仅 2 个题项，外部效度和可复验性都弱。

## R2 / R3 使用建议

1. 在 PR-R2 中可作为 seed 方法清单与 prompt/temperature 设计参考，而不是主四例样本的首选来源。
2. 若后续需要复用，应先人工转写两个题项、重建 prompt 设置、重新生成或手工录入论文示例输出，并把这一路径标为 `project-reconstructed`，不得声称获得作者原装 `<NL, STM>` 输出包。
3. 在论文写作中可用于说明：已有上游 `NL -> STM` 方法覆盖 prompt engineering、local LLM 与 temperature 变量；本文贡献应定位在拿到这些 seed 之后的反馈驱动改进。
