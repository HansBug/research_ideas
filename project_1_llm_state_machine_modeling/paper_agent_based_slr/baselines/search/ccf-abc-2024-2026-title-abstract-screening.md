# CCF A/B/C 2024-2026 title-level 粗筛记录

> 检索时间：`2026-06-13 01:20:00` 初筛，`2026-06-13 12:40:00` 补齐审计记录（Asia/Shanghai）
> 来源：本仓库 `ccf_venues/` 年度 README 的 official / publisher / DBLP 入口；DBLP search/API 命中作为 title-level discovery。
> 注意：多数 CCF venue 不提供可批量获取 abstract，本表不能替代全文或 abstract-level systematic screening；coverage 缺口见 [ccf-venue-coverage-gaps.md](./ccf-venue-coverage-gaps.md)，DBLP 原始命中快照见 [ccf-dblp-title-scan-raw.md](./ccf-dblp-title-scan-raw.md)。

## 1. 直接相关候选

| 年份 | Venue | 标题 | 来源 | 分层 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | 处理 |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2025 | WSESE@ICSE | On the Difficulties of Conducting and Replicating Systematic Literature Reviews Studies Using LLMs in Software Engineering | [DBLP](https://dblp.org/rec/conf/wsese/FelizardoDCGMGS25) | P1 | 🟢 | 🟡 | 🟡 | 🟡 | 🟠 | 🟢 | 🟡 | 待人工下载；写入 [manual-download-needed.bib](./manual-download-needed.bib)。 |

## 2. ASE 2024/2025 title-level 审计摘要

ASE 是本轮少数自动抓取成功的 CCF A 主会样本。下表保留 LLM / agent / review 相关 title 命中与排除理由，用于证明“未发现 SLR 自动化主会论文”的判定不是空白断言。

| 年份 | Venue | 标题 | 来源 | 关键词层级 | 本轮处理 |
|---:|---|---|---|---|---|
| 2024 | ASE | Towards LLM-augmented multiagent systems for agile software engineering. | [DBLP](https://dblp.org/db/conf/kbse/ase2024.html#CinkuszC24) | L2 / llm | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2024 | ASE | Unity Is Strength: Collaborative LLM-Based Agents for Code Reviewer Recommendation. | [DBLP](https://dblp.org/db/conf/kbse/ase2024.html#WangZZLCZ024) | L2 / llm, code review | 排除：是代码审查 / reviewer recommendation，不是 SLR/SMS 文献综述流程。 |
| 2025 | ASE | A Characterization Study of Bugs in LLM Agent Workflow Orchestration Frameworks. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#XueZWCW25) | L2 / llm | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | An LLM-based multi-agent framework for agile effort estimation. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#BuiDH25) | L2 / llm, multi-agent | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | Beyond Static GUI Agent: Evolving LLM-based GUI Testing via Dynamic Memory. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#ChenLCWXWHWW25) | L2 / llm | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | BuilDroid: A Self-Correcting LLM Agent for Automated Android Builds. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#KimRA25) | L2 / llm | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | LAURA: Enhancing Code Review Generation with Context-Enriched Retrieval-Augmented LLM. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#ZhangZSJL25) | L2 / llm, code review | 排除：是代码审查 / reviewer recommendation，不是 SLR/SMS 文献综述流程。 |
| 2025 | ASE | LLM-Powered Multi-Agent Collaboration for Intelligent Industrial On-Call Automation. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#FuZCWZRZWSLLZ25) | L2 / llm, multi-agent | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | SGCR: A Specification-Grounded Framework for Trustworthy LLM Code Review. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#WangMJDHMC25) | L2 / llm, code review | 排除：是代码审查 / reviewer recommendation，不是 SLR/SMS 文献综述流程。 |
| 2025 | ASE | Security Debt in LLM Agent Applications: A Measurement Study of Vulnerabilities and Mitigation Trade-offs. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#ShenDZY25) | L2 / llm | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | Watson: A Cognitive Observability Framework for the Reasoning of LLM-Powered Agents. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#RombautMVLH25) | L2 / llm | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | Wired for Reuse: Automating Context-Aware Code Adaptation in IDEs via LLM-Based Agent. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#WangJDZL25) | L2 / llm | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2024 | ASE | Can Cooperative Multi-Agent Reinforcement Learning Boost Automatic Web Testing? An Exploratory Study. | [DBLP](https://dblp.org/db/conf/kbse/ase2024.html#FanWFQL024) | L3 / multi-agent | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2024 | ASE | GPP: A Graph-Powered Prioritizer for Code Review Requests. | [DBLP](https://dblp.org/db/conf/kbse/ase2024.html#YangX0WLLB24) | L3 / code review | 排除：是代码审查 / reviewer recommendation，不是 SLR/SMS 文献综述流程。 |
| 2024 | ASE | Understanding Developer-Analyzer Interactions in Code Reviews. | [DBLP](https://dblp.org/db/conf/kbse/ase2024.html#SchafCLMTSZZ24) | L3 / code review | 排除：是代码审查 / reviewer recommendation，不是 SLR/SMS 文献综述流程。 |
| 2025 | ASE | AgentDroid: A Multi-Agent Tool for Detecting Fraudulent Android Applications. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#PanZJH25) | L3 / multi-agent | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | Agentic Specification Generator for Move Programs. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#FuXK25) | L3 / agentic | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | Envisioning Intelligent Requirements Engineering via Knowledge-Guided Multi-Agent Collaboration. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#HuangJSLJ25) | L3 / multi-agent | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | Requirements Development and Formalization for Reliable Code Generation: A Multi-Agent Vision. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#LuSZHTJL25) | L3 / multi-agent | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | Taming Uncertainty via Automation: Observing, Analyzing, and Optimizing Agentic AI Systems. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#MoshkovichZ25) | L3 / agentic | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | Triangle: Empowering Incident Triage with Multi-Agent. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#YuFMWZCLCZWBRLZPH25) | L3 / multi-agent | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |
| 2025 | ASE | What Types of Code Review Comments Do Developers Most Frequently Resolve? | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#GoldmanLPTTWZBJSJBJW25) | L3 / code review | 排除：是代码审查 / reviewer recommendation，不是 SLR/SMS 文献综述流程。 |
| 2025 | ASE | iCodeReviewer: Improving Secure Code Review with Mixture of Prompts. | [DBLP](https://dblp.org/db/conf/kbse/ase2025.html#PengKML25) | L3 / code review | 排除：是代码审查 / reviewer recommendation，不是 SLR/SMS 文献综述流程。 |
| 2024 | ASE | A Conceptual Framework for Quality Assurance of LLM-based Socio-critical Systems. | [DBLP](https://dblp.org/db/conf/kbse/ase2024.html#BaresiCDQ24) | L4 / llm | 排除：LLM/agent for SE 任务相关，但 title 不涉及 SLR/SMS/evidence synthesis。 |

## 3. 逐 venue 最低审计记录

| 文件 | 作用 |
|---|---|
| [ccf-venue-coverage-gaps.md](./ccf-venue-coverage-gaps.md) | 42 个 venue × 2024/2025/2026 的 coverage / gap；标注 🔵/🟠/🔴 与风险。 |
| [ccf-dblp-title-scan-raw.md](./ccf-dblp-title-scan-raw.md) | DBLP mirror 自动扫描命中和 coverage 原始快照；含 ASE 2024/2025 的 LLM/agent title 命中。 |
| [manual-download-needed.bib](./manual-download-needed.bib) | CCF-adjacent 但未自动获取全文的论文。 |

## 4. 初步判断

- 本轮 CCF 主会 / 期刊 title-level 粗筛没有发现已经明显覆盖“agent-based + SLR 多阶段 + audit / traceability / evaluation”完整组合的 CCF A/B/C 正式论文。
- 但 ICSE co-located workshop 已出现 “LLM + SE SLR conducting / replication” 相关命中，说明软件工程社区正在讨论该方向，后续 related work 不能只依赖医学 / 通用 arXiv baseline。
- 由于 CCF 部分 abstract coverage 不足、DBLP / publisher 自动抓取存在访问缺口，所有“未命中”只表示本轮 title-level 未发现直接近邻，不是最终负证据。
