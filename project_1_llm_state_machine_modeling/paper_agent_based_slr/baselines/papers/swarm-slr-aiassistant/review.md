# SWARM-SLR AIssistant: A Unified Framework for Scalable Systematic Literature Review Automation

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | SWARM-SLR AIssistant: A Unified Framework for Scalable Systematic Literature Review Automation |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Tim Wittenborg、Allard Oelen 等；arXiv:2603.05177; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P0 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)；未人工逐页打开 PDF 图表 |
| 研究脉络 | agent式 SLR 工作流与评价基准 |
| 引用角色 | 直接新颖性门槛 / 强 baseline |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | SWARM-SLR requirements、research interest、research questions、keywords、search queries、local corpus/metadata、工具注释 schema |
| 输出 | AIssistant 中的 guided workflow、persistent data layer、中间/最终结果、tool registry metadata、用户可选工具目录 |
| 方法/系统形态 | 将 SWARM-SLR 的结构化 SLR 方法接入 agent-based AIssistant，并提出 centralized tool registry |
| 覆盖阶段 | 当前实现主要覆盖 SWARM-SLR stage I 的前 5 个步骤；论文还讨论 literature search 和 corpus creation 支持，但不是完整系统评价 |
| 不覆盖阶段 | 不覆盖阶段需按全文方法章节复核；当前不得据此写“完整覆盖 SLR 生命周期”。 |
| 人审/审计机制 | persistent storage 支持人机共享中间结果；工具 registry 有 submitted/verified 等状态概念；未见 claim-level provenance 或正式 人工审计 gate |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | persistent storage / tool registry 级；无 claim-level provenance。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | 18 名参与者基于截图/问卷评价前 5 个步骤；UEQ-S、free-text feedback、参与者意愿统计 |
| 模型/API 设置 | 原文未给出或本轮未抽取模型清单 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | 参与者总体认为 AIssistant 比 Jupyter Notebook 更易用/支持性更强；作者承认样本小、系统未发布、缺少长期真实部署 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | workflow/tool registry 近邻 baseline：威胁 paper2 的 SLR workflow guidance 与 tool integration claim，但评价和证据链弱于 LatteReview/Elhuyar |
| 受影响主张 ID | C1,C2,C5,C7 |
| 威胁类型 | 局部覆盖 |
| 威胁的 paper2 主张 | workflow/tool registry 近邻 baseline：威胁 paper2 的 SLR workflow guidance 与 tool integration claim，但评价和证据链弱于 LatteReview/Elhuyar |
| 支持的 paper2 主张 | 支持 paper2 将贡献收窄到可审计 evidence workflow、run record、人工审计 gate 与 claim-to-source trace，而非泛称自动综述生成。 |
| paper2 应避免的主张 | 避免写“首次 agentic SLR / 首次自动化 evidence synthesis”；必须承认跨域强近邻并收窄到 SE 场景和可审计证据包。 |
| baseline 可用性 | 定性强baseline；若代码/数据可得，后续再判定是否可运行复现。 |
| 对比方式 | 定性强baseline |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 定性强baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟡 | 🟡 | 🟠 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Page 1 lines 9--28、29--68 | 论文直接讨论 Systematic Literature Reviews、SWARM-SLR 和 SLR automation，主题贴合。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | `paper_content.txt` Page 1 lines 70--85；Page 2 lines 161--171；Page 4 lines 312--316 | SWARM-SLR 原方法覆盖 4 stages/8 tasks/19 steps，但本文实现只集成 stage I 前 5 个步骤，如研究兴趣、相关 RQ、搜索查询和相关文献 refinement；全文未展示筛选、抽取、综合、报告全链路实现。 |
| D3 LLM/agent 自动化深度 | 🟡 | `paper_content.txt` Page 2 lines 125--155 | AIssistant 通过 LLM tool calling 调用 ORKG ASK、Semantic Scholar、arXiv 等工具，并把 SWARM-SLR steps 分离成 agents；但作者明确目标是 AI-supported guidance，不是 fully automated approach，因此自动化深度低于完整 multi-agent execution。 |
| D4 人工审计与可追踪性 | 🟡 | `paper_content.txt` Page 1 lines 54--57；Page 3 lines 223--235；Page 4 lines 287--295 | persistent data layer、shared metadata schema 和 tool registry 能改善过程透明度；评价也指出越抽象越需要质量监督。但未见决策日志、claim-to-source trace、per-cell provenance 或审计协议。 |
| D5 评价严谨性 | 🟠 | `paper_content.txt` Page 3 lines 236--310；Page 4 lines 391--397 | 评价是早期可用性问卷，N=18，只基于截图和未发布系统；无真实 SLR 任务 benchmark、无金标、无自动化输出准确率，因此只能弱评。 |
| D6 SE/CCF 相关性 | 🟠 | `bibtex.bib` arXiv cs.DL；正文为通用 SLR/研究软件工具生态 | 不是 SE/CCF venue，也不直接面向软件工程 SLR；但 workflow automation 和 research software registry 对 paper2 有方法背景价值。 |
| D7 对本文 novelty 的威胁 | 🟡 | `paper_content.txt` Page 1 lines 49--63；Page 4 lines 413--428 | 覆盖 agent-based assistant、SLR workflow guidance、persistent storage 和 tool registry，威胁 paper2 的 workflow/interface claim；但不覆盖 paper2 若主打的 evidence extraction、claim provenance、LLM-as-reviewer accuracy evaluation。 |

## 3. 论文解决的问题与背景

论文的问题不是“让 LLM 自动完成整篇系统综述”，而是解决已有 SLR 工具生态碎片化、难集成、难使用的问题。SWARM-SLR 曾经将 machine-actionable SLR 需求整理为结构化 workflow，但实际采用受限于 Jupyter Notebook、安装多个工具、切换界面和工具标注成本。

AIssistant 提供 LLM-based guidance 和 tool calling 能力，SWARM-SLR 提供 SLR 方法结构。本文把二者合并，并提出一个 tool registry，使工具开发者能用共享 metadata schema 标注工具，让用户在统一界面里按 SLR step 找到工具、运行工具并保存中间结果。

## 4. 方法 / 系统拆解

输入包括 SWARM-SLR requirements、用户研究兴趣、RQ、关键词、检索式、相关文献、document annotation、evidence answers、local data 和外部工具 metadata。输出不是单篇综述文本，而是 AIssistant 中的 workflow guidance、工具目录、persistent data layer 里的中间/最终资产，以及可由人和机器共同访问的结果。

系统由三部分构成。AIssistant 是 workspace，支持 human-machine collaboration、模块化工具调用和中间资产保存。SWARM-SLR AIssistant 将 SWARM-SLR steps 做成独立 agents，每个 agent 有自己的 system prompt、enabled tools、input/output assets。Tool Registry 则是概念设计，允许工具开发者提交统一 metadata，未来通过 submitted/verified/officially supported 等状态降低工具接入成本。

LLM/agent 角色主要是 workflow guidance 和 tool invocation，而不是自动审稿员。人机协作较强：用户控制每个 step、中间数据可被人工修改、工具贡献需要 review/confirmation。证据/审计层面，persistent storage 和 metadata schema 是过程透明性的基础，但尚未达到 paper2 需要的 claim-level traceability。

## 5. 实验 / 评价设计

原文评价对象是当前 AIssistant 中的 SWARM-SLR layout，而不是 SLR 输出质量。设计上，作者使用 survey：页面包含 data protection、general information、steps 1.1 到 2.4 的截图、demographic questions 和 future work。问题形式包括 UEQ-S semantic differential 和 free-text comment。

样本为 18 名参与者，其中 10 名 PhD、8 名 Master。平均完成时间约 22 分钟，中位数约 18:34。评价基于前 5 个 SWARM-SLR steps 的界面/截图，不包含完整真实 SLR 执行、金标输出对比、LLM 准确率或 agent tool-call failure analysis。

## 6. 主要结果与结论

作者报告参与者总体倾向正面。Figure 3 的 UEQ-S 结果显示，AIssistant 相比 Jupyter Notebook 引导步骤被认为更 supportive、easy、interesting 等；文本反馈包括 UI 建议、MCP/local IDE 可能替代部分功能，以及对透明性、幻觉、可复现性、能源/成本的担忧。

结论部分说本文展示了把 conversational LLM framework 与 SWARM-SLR stage I requirements 对齐的可行性，并用 persistent data layer 与 tool registry 降低 workflow extension 门槛。但作者也明确指出还需要大量 future work 才能达成 accessible、modular、transparent SLR automation。

## 7. 局限与可复现性

局限很明确：AIssistant 未发布，没有 public large-scale test；评价样本只有 18 人，可能存在 selection bias；问卷基于截图和早期实现，没有 real-world deployment 或 long-term usage feedback。作者还指出完整系统评价会非常耗时，可能需要 task-based benchmarks。

可复现性方面，论文给出 survey design 的 GitHub 路径和工具生态引用，但没有提供可直接复现实验的完整公开系统、运行脚本或真实任务输出。该文是 arXiv preprint，不能按 peer-reviewed CCF/SE 结论使用。

## 8. 对 paper2 story / 实验设计的影响

paper2 不能简单声称“提出统一 SLR workflow assistant”作为主要 novelty，因为 SWARM-SLR AIssistant 已经在这个方向上有明确工作。更稳妥的差异化是：paper2 如果关注 agent review，应证明不是仅做界面 guidance 或 tool registry，而是完成可审计的文献筛选、抽取、综合和写作证据链。

实验设计上，该文提醒 paper2 需要加入 usability 和 transparency 维度，但不能只做问卷。若 paper2 讨论人机协作，需要量化人工复核负担、错误拦截率、claim provenance 完整率，以及 agent 输出被 human gate 修改/驳回的比例。

## 9. 可用于写作的引用角度

- 可引用 SWARM-SLR AIssistant 说明 SLR automation 不仅是 LLM prompt 问题，还涉及工具生态、metadata schema、persistent storage 和 workflow guidance。
- 可用作“workflow-level assistant”对照：它改善流程可用性，但尚未证明自动抽取/综合结果的准确性。
- 可引用其 discussion 中关于 transparency、reproducibility 和 oversight 的担忧，支撑 paper2 设置 evidence audit gate。
- 写作时避免把它描述成完整自动 SLR 系统；全文证据显示当前实现主要是 stage I guidance 和 registry 设计。

## 10. 待复核清单

- 打开 GitHub survey 路径，确认问卷材料、截图和数据是否仍可访问。
- 人工查看 Figure 1--3，核实 tool registry 和 UEQ-S 图中的具体 step 与数值。
- 检查 AIssistant 是否后来公开发布，是否已有后续论文或代码仓库。
- 若用于实验 baseline，需要确认是否存在可运行版本；否则只能作为 conceptual/workflow baseline。
