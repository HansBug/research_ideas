# 全 CCF A/B/C 与重点 AI/DL/IR/NLP/SE 方向扩展粗筛记录

> 检索时间：`2026-06-14 18:14:00`--`2026-06-14 18:35:00`（Asia/Shanghai）  
> CCF 分母来源：`ccf-all-abc-2026-scope-snapshot.json` / [ccf-all-abc-2026-scope-snapshot.md](./ccf-all-abc-2026-scope-snapshot.md)。  
> 扩展检索入口：OpenAlex API；原始结果见 [ccf-all-abc-openalex-expanded-raw.json](./ccf-all-abc-openalex-expanded-raw.json)，去重候选见 [ccf-all-abc-openalex-expanded-ranked.jsonl](./ccf-all-abc-openalex-expanded-ranked.jsonl)。

## 1. 本轮为什么重点看 cs.AI / cs.DL / cs.IR / cs.CL / cs.SE

前一轮 arXiv 候选池中，主分类和交叉分类高频集中在 `cs.AI`、`cs.CL`、`cs.SE`、`cs.IR`、`cs.DL` 等方向；用户要求本轮不要只看本仓库已建档 CCF venue，而要重点补查这些方向对应的 CCF A/B/C 会议期刊。分类中文释义如下：

| arXiv 分类 | 中文释义 | 本轮对应 CCF 重点 |
|---|---|---|
| `cs.AI` | 人工智能 | AAAI、NeurIPS、IJCAI、ICML、ICLR、JMLR、AI、JAIR 等人工智能 venue |
| `cs.DL` | 数字图书馆 | JASIST、IPM、SIGIR/TOIS/WWW/CIKM/WSDM 等数字图书馆与检索 venue |
| `cs.IR` | 信息检索 | SIGIR、TOIS、CIKM、WSDM、ECIR、IPM 等检索 venue |
| `cs.CL` | 计算与语言 / 自然语言处理 | ACL、EMNLP、NAACL、COLING、TACL、TASLP 等 NLP venue |
| `cs.SE` | 软件工程 | ICSE、FSE、ASE、TOSEM、TSE、IST、JSS、ESE 等 SE venue |

## 2. CCF 2026 全量目录分母

| 范围 | 数量 | 本轮用途 |
|---|---:|---|
| CCF A/B/C 全量条目 | 681 | 扩展检索分母，不等同本地已建档 venue |
| 人工智能领域 | 107 | 对应 `cs.AI` / `cs.CL` 方向重点观察 |
| 数据库/数据挖掘/内容检索领域 | 65 | 对应 `cs.DL` / `cs.IR` 方向重点观察 |
| 软件工程/系统软件/程序设计语言领域 | 82 | 对应 `cs.SE` 与 paper2 目标场景 |
| 人机交互与普适计算领域 | 41 | 对应 CHI / PACMHCI 等 LLM-ification / human-AI review 线索 |
| 交叉/综合/新兴领域 | 57 | 对应 WWW、JAMIA、Bioinformatics 等跨域 evidence synthesis 线索 |

## 3. 扩展候选与处理建议

| 年份 | Venue/来源 | 标题 | DOI/URL | 分层建议 | 本地状态 | 为什么相关 / 处理建议 |
|---:|---|---|---|---|---|---|
| 2026 | Information and Software Technology | LLM4SCREENLIT: Recommendations on assessing the performance of large language models for screening literature in systematic reviews | [DOI](https://doi.org/10.1016/j.infsof.2026.108204) | P0/P1 | 未建库；待题摘/全文复核决定 | 直接涉及 SLR/SLS screening / selection，优先作为 SE 局部强 baseline 或评价协议补充。 |
| 2025 | Information and Software Technology | Exploring the use of LLMs for the selection phase in systematic literature studies | [DOI](https://doi.org/10.1016/j.infsof.2025.107757) | P0/P1 | 未建库；待题摘/全文复核决定 | 直接涉及 SLR/SLS screening / selection，优先作为 SE 局部强 baseline 或评价协议补充。 |
| 2024 | 来源待核验 | Data extraction for systematic mapping study using a large language model - a proof-of-concept study in software engineering | [DOI](https://doi.org/10.1145/3674805.3690743) | P0/P1 | 未建库；待题摘/全文复核决定 | 直接涉及 SE systematic mapping 的 LLM data extraction，建议后续补全文建库。 |
| 2025 | ACM Transactions on Software Engineering and Methodology | LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision, and the Road Ahead | [DOI](https://doi.org/10.1145/3712003) | P2 | 未建库；待题摘/全文复核决定 | TOSEM SE 综述/vision，非自动化 SLR 工具，但会影响 agent/SE related work 定位。 |
| 2024 | ACM Transactions on Software Engineering and Methodology | Large Language Models for Software Engineering: A Systematic Literature Review | [DOI](https://doi.org/10.1145/3695988) | P2 | 未建库；待题摘/全文复核决定 | SE 领域正式期刊/会议 SLR，主要作为背景或领域边界，不一定是 paper2 直接 baseline。 |
| 2025 | 来源待核验 | Understanding the LLM-ification of CHI: Unpacking the Impact of LLMs at CHI through a Systematic Literature Review | [DOI](https://doi.org/10.1145/3706598.3713726) | P2 | 未建库；待题摘/全文复核决定 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2025 | ACM Transactions on Knowledge Discovery from Data | Automating Research Synthesis with Domain-Specific Large Language Model Fine-Tuning | [DOI](https://doi.org/10.1145/3715964) | P2 | 未建库；待题摘/全文复核决定 | AI/DL/KDD-like research synthesis 自动化线索，需核验是否有可审计 evidence workflow。 |
| 2025 | 来源待核验 | SurveyGen: Quality-Aware Scientific Survey Generation with Large Language Models | [DOI](https://doi.org/10.18653/v1/2025.emnlp-main.136) | P1/P2 | 已在本地文库 | 自动 survey generation / report generation 方向，威胁报告生成 claim，但通常不覆盖 SLR/SMS 审计流程。 |
| 2024 | 来源待核验 | Evaluating Large Language Models on Wikipedia-Style Survey Generation | [DOI](https://doi.org/10.18653/v1/2024.findings-acl.321) | P1/P2 | 未建库；待题摘/全文复核决定 | 自动 survey generation / report generation 方向，威胁报告生成 claim，但通常不覆盖 SLR/SMS 审计流程。 |
| 2024 | arXiv (Cornell University) | AutoSurvey: Large Language Models Can Automatically Write Surveys | [DOI](https://doi.org/10.48550/arxiv.2406.10252) | P1/P2 | 未建库；待题摘/全文复核决定 | 自动 survey generation / report generation 方向，威胁报告生成 claim，但通常不覆盖 SLR/SMS 审计流程。 |
| 2024 | Journal of the American Medical Informatics Association | A question-answering framework for automated abstract screening using large language models | [DOI](https://doi.org/10.1093/jamia/ocae166) | P1/P2 | 未建库；待题摘/全文复核决定 | evidence synthesis 局部阶段强相关，可转化为评价/审计指标。 |
| 2025 | Journal of the American Medical Informatics Association | High-performance automated abstract screening with large language model ensembles | [DOI](https://doi.org/10.1093/jamia/ocaf050) | P1/P2 | 已在本地文库 | evidence synthesis 局部阶段强相关，可转化为评价/审计指标。 |
| 2025 | Research Synthesis Methods | Generative artificial intelligence use in evidence synthesis: A systematic review | [DOI](https://doi.org/10.1017/rsm.2025.16) | PX/P2 | 未建库；待题摘/全文复核决定 | evidence synthesis 局部阶段强相关，可转化为评价/审计指标。 |
| 2025 | Journal of Clinical Epidemiology | Large language models for conducting systematic reviews: on the rise, but not yet ready for use—a scoping review | [DOI](https://doi.org/10.1016/j.jclinepi.2025.111746) | P1/P2 | 未建库；待题摘/全文复核决定 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2024 | Artificial Intelligence Review | Artificial intelligence for literature reviews: opportunities and challenges | [DOI](https://doi.org/10.1007/s10462-024-10902-3) | P1/P2 | 未建库；待题摘/全文复核决定 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2024 | Information and Software Technology | On the road to interactive LLM-based systematic mapping studies | [DOI](https://doi.org/10.1016/j.infsof.2024.107611) | PX/P2 | 未建库；待题摘/全文复核决定 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2026 | arXiv (Cornell University) | AgentSLR: Automating Systematic Literature Reviews in Epidemiology with Agentic AI | [URL](http://arxiv.org/abs/2603.22327) | P0/P1 | 未建库；待题摘/全文复核决定 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2026 | arXiv (Cornell University) | Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews | [DOI](https://doi.org/10.48550/arxiv.2603.22327) | P1/P2 | 已在本地文库 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2026 | ArXiv.org | Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle | [URL](https://arxiv.org/abs/2605.15245) | PX/P2 | 已在本地文库 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2025 | IEEE Access | A Systematic Literature Review of Hallucinations in Large Language Models | [DOI](https://doi.org/10.1109/access.2025.3601206) | PX/P2 | 未建库；待题摘/全文复核决定 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2025 | Trepo - Institutional Repository of Tampere University | DESIGNING A HUMAN-AI COLLABORATIVE MODULAR APPROACH TO AUTOMATING SYSTEMATIC LITERATURE REVIEWS: FROM OBJECTIVES TO REPORTING | [URL](https://trepo.tuni.fi/handle/10024/232027) | P0/P1 | 未建库；待题摘/全文复核决定 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |
| 2026 | International Journal of Advanced Computer Science and Applications | The Impact of Modern AI on Software Development: A Systematic Literature Review | [DOI](https://doi.org/10.14569/ijacsa.2026.0170478) | PX/P2 | 未建库；待题摘/全文复核决定 | 主题相关但需题摘/全文复核，当前不升级为强 baseline。 |

## 4. 初步结论

1. 全 CCF A/B/C 扩搜把分母从本地已建档 `42` 个 venue 扩展到 CCF mirror `681` 条 A/B/C venue 条目；但本轮仍是 OpenAlex / title-abstract 级 discovery，不是逐 venue accepted-paper exhaustive audit。
2. 在重点方向中，最需要后续补建库或全文复核的新增正式发表线索集中在：`Information and Software Technology` 的 SLS selection / interactive mapping，`ACM TOSEM` 的 LLM4SE / LLM-based MAS 综述，`CHI / PACMHCI` 的 LLM-ification SLR，`ACM TKDD` 的 research synthesis automation，以及 `ACL/EMNLP Findings` 的 automatic survey generation。
3. 这些新增线索进一步说明：AI / DL / IR / NLP / SE 社区已经分别在做 survey generation、screening / extraction、research synthesis 与 SE LLM 综述；paper2 不能讲宽泛 firstness。
4. 当前仍未观察到能同时覆盖“SE SLR/SMS 场景 + agent 多阶段流程 + evidence package / claim trace + 人审 gate + 可复现实验”的完整组合；该判断只可写成扩展粗筛下的保守观察，不能写成全 CCF 负证据。
