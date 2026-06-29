# ai-native-se-roadmap · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，并读取 `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`。审计口径采用 claim-evidence、禁止愿景升级为结果、Reviewer gate。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md`。审计口径采用“严格贴合原文方法 / 配置 / 不清楚则显式标记”。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。审计口径采用 artifact-gated completion，不以口头完成替代可检查制品。
- 是否完整阅读 `paper_content.txt`：是；逐段阅读 `paper_content.txt` 1--1146 行，覆盖摘要、Introduction、§2 SE 2.0 分析、§3 SE 3.0 技术栈、§4 Challenges、§5 Conclusion 与参考文献区。
- 是否核对 `paper.pdf`：是，做了必要视觉核对；使用 `pdfinfo` 确认 PDF 为 25 页，并用 `pdftoppm` 渲染/视觉查看 PDF 第 3 页 Fig. 1、第 6 页 Fig. 3、第 13 页 Fig. 6。未逐页视觉核对 Fig. 2/4/5/7；本次结论中涉及这些图时仍以 `paper_content.txt` 文本为主，标为后续精核入口。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文没有 SLR/SMS 式显式 RQ，也没有 population / intervention / outcome / context、检索问题或数据抽取表。其根目标来自题名、摘要和引言：提出 Software Engineering 3.0，即 AI-native SE，从 SE 2.0 的 AI-assisted、task-driven、code-centric 模式转向 intent-centric、conversation-oriented 的人类开发者与 AI teammate 协作模式。原文声称的贡献是：概述 SE 3.0 技术栈，并提出实现该愿景需要解决的 challenge roadmap。

关键原文锚点：

- `paper_content.txt:8-21`：摘要声明 SE 3.0、技术栈组件和挑战路线图。
- `paper_content.txt:51-60`：引言中提出从 SE 2.0 转向 SE 3.0。
- `paper_content.txt:61-69`：说明愿景来源是 academic/gray literature surveys、社区活动、客户/内部团队讨论、作者 FMware 与 SE 3.0 stack 研发经验、OPEA 40+ 工业伙伴互动。
- `paper_content.txt:70-73`：章节结构说明：§2 critical analysis，§3 vision/technology stack，§4 challenges，§5 conclusion。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文不是系统综述、系统映射或三级研究。它没有可审计检索流程、数据库、检索式、筛选分母、纳排理由、质量评价、数据抽取表、编码方案、inter-rater agreement 或统计合成。原文的方法更准确地说是 vision synthesis / roadmap argumentation：作者把文献 surveys、社区讨论、工业交互和自身 prototype / companion works 组织为 SE 3.0 愿景与挑战。

finding 形成方式也不是“统计观察 -> 领域 finding”。原文的主张路径是：

1. 先提出 SE 2.0 的局限：human cognitive overload、inefficient/ineffective model training、suboptimal code quality/additive bias，以及 autonomous software engineers 的边界。
2. 再提出 SE 3.0 的原则：intent-centric、conversation-oriented、AI-native、human-AI complementarity、knowledge-driven FMs。
3. 再用五层技术栈组织愿景：Teammate.next、IDE.next、Compiler.next、Runtime.next、FM.next。
4. 最后按 challenge template 给出开放问题与作者愿景：Description、Affects、Open question、Our vision。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文没有 extraction form、coding scheme、quality rubric 或 evidence table。它有多个显式模型 / taxonomy / roadmap 图和报告模板，当前维度树应优先复原这些结构：

| 原文结构 | 真实内容 | 证据定位 | 对维度树的含义 |
|---|---|---|---|
| Fig. 1 软件工程演化模型 | SE 1.0 / SE 2.0 / SE 3.0 三时代；每个时代有 code/AI/intent 中心性、支撑技术、时间线 | `paper_content.txt:97-131`；PDF 第 3 页视觉核对 | 应作为 `era_transition_model`，不是普通背景。 |
| Fig. 3 SE 3.0 技术栈 | Teammate.next、IDE.next、Compiler.next、Runtime.next、FM.next；每层都有 SE 2.0 -> SE 3.0 转换对 | `paper_content.txt:243-279`；PDF 第 6 页视觉核对 | 应作为封闭/半封闭层级枚举和关系边。 |
| Fig. 4 intent-centric development flow | Provide intent (+ examples/data) -> search best solution -> reflect/ask clarification -> conversation -> react to output | `paper_content.txt:343-396` | 应作为流程/关系型维度，而不是只写“method”。 |
| §3.6 curriculum recipe | objectives/scope、domain/subdomain、core concepts/tasks/I-O specs、hierarchical taxonomy、examples/templates/evaluation rules、teacher FM synthetic data、internal consistency、iterative refinement、pilot testing、community contributions、data flywheel | `paper_content.txt:521-543` | 这是最像 Paper2 维度模式工程的结构，应单独保留。 |
| Fig. 6 FM 系统工程生态图 | configuration、data collection、data verification、machine resource management、serving infrastructure、monitoring、feature extraction、analysis tools、process management tools 等 | `paper_content.txt:550-578`；PDF 第 13 页视觉核对 | 应作为 SE 3.0 生态 / artifact / operational concern 字段。 |
| §4 challenge template | 每个挑战包含 Description、Affects、Open question、Our vision；OQ1--OQ6 有详细 vision，OQ7--OQ14 是未展开开放问题 | `paper_content.txt:579-586`、`595-640`、`641-676`、`677-718`、`719-752`、`753-797`、`798-823` | 应作为 roadmap finding path 的核心 schema。 |
| scattered validity/quality signals | visionary nature、challenge list not extensive、ToM not silver bullet、whole-stack prototypes needed、only time will tell、welcome opposing views、author/companion-work dependence | `paper_content.txt:303-306`、`584-586`、`637-640`、`840-856` | 应作为 vision-paper validity / maturity / risk 字段。 |

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文没有统计字段或统计观察；因此不能形成可统计 finding。原文 conclusion 的形成路径是 roadmap argument：

- SE 2.0 limitations 被用作动机。
- SE 3.0 stack 被用作解决愿景。
- §4 challenge template 把 gap/action 明确化，尤其通过 `Affects -> Open question -> Our vision` 连接 stack component 与研究议题。
- §5 进一步降级：五个组件需要并行推进，IDE.next 依赖其他组件；只有当所有组件 prototype 都开发后，SE 3.0 vision 才能整体评估和验证；商业 vibe coding 平台只是 early glimpses；作者欢迎 opposing views。

对 Paper2 来说，本篇只能作为 roadmap / boundary anchor 和 challenge schema seed；不能作为 AI-native SE 领域趋势、覆盖率或效果统计证据。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但需收紧 | `review.md:270` 把根定义为 roadmap/challenge 树并明确不进主统计池，这是正确的；但 `review.md:278-280` 仍写“研究目标 / RQ / 贡献声明”，容易暗示存在原文 RQ。原文没有 RQ，应统一为“目标 / 贡献声明 / roadmap 对象”。 | M |
| 主干分支是否覆盖原文 schema | 未充分覆盖 | 当前主干只有愿景对象、技术栈、challenge、action roadmap、boundary risk。它漏掉 Fig.1 时代演化模型、Fig.4 intent-centric 流程、Fig.6 FM 系统工程生态、§3.6 curriculum recipe、§4 的 Description/Affects/OQ/Our vision 模板。尤其 `review.md:317` 把技术栈候选取值写成“需求、设计、编码、测试、维护、协作或平台层”，与 Fig.3 的 Teammate.next / IDE.next / Compiler.next / Runtime.next / FM.next 不一致。 | C |
| 叶子维度是否足够具体 | 不足 | `review.md:274` 已声明六个 `leaf-*` 是通用接口，不是原文叶子全集，这个降级是正确的；但后续“原文模式候选叶子映射”只有 5 个粗叶子，未拆出 stack layer、transition pair、challenge template、OQ、affected component、vision maturity、evidence source type、artifact/prototype status 等原文可抽字段。 | C |
| 取值空间是否可执行 | 不可直接执行 | 多数候选取值写成开放文本或“待 A2a”，而原文已经给出若干可执行半封闭取值：Fig.3 五层 stack、SE2.0->SE3.0 转换对、OQ1--OQ14、Affects 组件集合、challenge template 字段、curriculum recipe 节点。当前取值空间不足以指导 A2a 回填。 | I |
| 关系边是否缺失 | 缺失 | 原文是关系型 roadmap：challenge 影响 stack components；stack layer 有 from-state/to-state 转换；intent 流程连接人、AI teammate、Compiler.next；companion evidence 支撑某些 vision；risk 限制可迁移性。当前 `review.md` 没有关系边表，只把关系压成粗叶子。 | I |
| 统计用途 / 分母是否正确 | 大体正确 | `metadata.json` 中 `eligible_for_statistical_synthesis=false`，`review.md:270`、`review.md:326-328` 均明确不进入主统计池，这是正确的。需保留“只能统计为文库中的 vision/roadmap 类型条目，不能统计原文内部 finding”的口径。 | 通过 |
| 候选 finding 路径是否完整 | 不完整 | 原文候选 finding / roadmap path 是 `SE2.0 limitation -> stack component -> challenge description -> affected components -> OQ -> our vision -> evidence/maturity/risk`。当前只用 `orig-challenge` 和 `orig-roadmap-action` 两个粗叶子承接，无法保留 OQ1--OQ14、Affects 和 Our vision 的路径。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，但证据粒度不足 | A.1--A.4 表头齐全，且证据强度均降级为 `not_verified` / 结论为 `weak`，避免了升级风险；但 A.2 仍大量使用“见释义”“待 A2a 精确页码复核”“方法 / 结果页”等泛定位。对本文这种没有 Method/Results 的 vision paper，A.2 的章节标签也不够忠实。 | I |
| 是否存在可能误导 A2a 的强主张 | 存在中等风险 | `review.md:274` 的声明可避免最危险的“六叶接口 = 原文 schema”误读；但 A.3 中 C02--C07 反复写“来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构”，与原文无 RQ、无方法/评价结构不符。若 A2a 只读 A.3，可能把通用接口误认为原文来源叶子。 | I |

## 4. 建议维度树骨架

当前 `review.md` 尚不足够。建议把通用六叶接口保留为跨论文检查层，但在其下增加真正来自原文的 roadmap / vision schema。以下是更忠实的最小骨架。

根节点：`[dim-ai-native-se-roadmap-root] SE 3.0 vision and challenge roadmap`

单位对象：vision claim、era transition item、stack component、process step、challenge item、open question、roadmap vision、evidence/maturity/risk signal。

统计池资格：不进入主统计池；仅作为 `boundary_anchor` / `schema_seed` / `candidate_finding`。缺失值语义必须区分 `not_applicable_no_slr_protocol`、`not_reported`、`not_verified_pdf`、`vision_only`、`companion_work_not_read`、`fast_drifting_fact`。

| 主干分支 | 叶子维度 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| 证据来源与降级边界 | source_basis | academic/gray literature surveys；community/workshop discussion；customer/internal meetings；author R&D experience；OPEA industrial interactions | 不进主统计池；可记录 source type | not_reported；vision_only | `paper_content.txt:61-69` |
| 证据来源与降级边界 | systematic_protocol_status | no_database；no_search_string；no_screening_denominator；no_quality_rubric；no_extraction_form | 可作为排除理由统计 | not_applicable_no_slr_protocol | `paper_content.txt:61-69` 反证；全文无 Method/Results |
| 时代演化模型 | era | SE 1.0；SE 2.0；SE 3.0 | 只作图模型字段，不作经验统计 | not_verified_pdf | Fig.1，`paper_content.txt:97-131`；PDF 第 3 页 |
| 时代演化模型 | era_attributes | code-centric；AI models supporting traditional SE；intent-centric；AI-native；knowledge-driven efficient models 等 | 只作 schema seed | not_verified_pdf | Fig.1，PDF 第 3 页 |
| SE 2.0 limitation | limitation_category | high cognitive overload；inefficient/ineffective model training；suboptimal code quality/additive bias；autonomous SE boundary | 不作覆盖率统计；可作 challenge seed | not_reported | §2.2--§2.3，`paper_content.txt:138-236` |
| SE 3.0 principle | principle | intent-centric；conversation-oriented；AI-native；human-AI complementarity；knowledge-driven training；code as means | 不作统计；可作 concept seed | not_reported | §3.1，`paper_content.txt:280-306` |
| 技术栈层级 | stack_component | Teammate.next；IDE.next；Compiler.next；Runtime.next；FM.next | 不作主统计；可作内部枚举 | not_verified_pdf | Fig.3，`paper_content.txt:243-279`；PDF 第 6 页 |
| 技术栈层级 | transition_pair | static/impersonal -> self-evolving/personalized mentor；code-centric/editing -> intent-centric/conversations；logic-rule realization -> search-space exploration；serving models -> serving compound apps；data-driven inefficient FMs -> knowledge-driven efficient FMs | 不作主统计；可作关系边 | not_verified_pdf | Fig.3，PDF 第 6 页 |
| intent-centric 流程 | process_step | provide intent；examples/data；search best solution；reflect/ask clarification；conversation；react to output | 不作统计；可作 process schema | not_verified_pdf | Fig.4，`paper_content.txt:343-396` |
| Compiler.next / Runtime.next / FM.next 机制 | mechanism | multi-objective optimization；goal-tracking tests from intents；DAG workflow；SLA slack routing；uni-cluster；edge extension；curriculum engineering；observability data | 不作主统计；可作 method/intervention seed | companion_work_not_read | §3.4--§3.6，`paper_content.txt:375-543` |
| curriculum recipe | curriculum_node | objectives/scope；domain/subdomain；concept/task/I-O specs；hierarchical taxonomy；examples/templates/evaluation rules；teacher FM synthetic data；internal consistency；pilot testing；community contribution；data flywheel | 可迁移为 Paper2 schema-engineering seed；不作领域统计 | not_reported；vision_only | §3.6，`paper_content.txt:521-543` |
| FM 系统工程生态 | ai_system_component | configuration；data collection；data verification；machine resource management；serving infrastructure；monitoring；feature extraction；analysis tools；process management tools；FM code | 不作主统计；可作 artifact/operational concern seed | not_verified_pdf | Fig.6，`paper_content.txt:550-578`；PDF 第 13 页 |
| challenge roadmap | challenge_item | C1 speeding human-AI alignment；C2 code synthesis efficiency；C3 runtime performance；C4 FM understanding；C5 eliminating prompt engineering；other OQ7--OQ14 | 不作主统计；可作 candidate finding scaffold | not_reported | §4，`paper_content.txt:579-823` |
| challenge roadmap | challenge_template_fields | description；affects；open_question_id；open_question_text；our_vision | 不作主统计；这是原文报告 schema | not_reported | §4 开头，`paper_content.txt:579-586` |
| challenge roadmap | affected_component_relation | challenge -> IDE.next / Teammate.next / Compiler.next / Runtime.next / whole stack | 关系边，不作主统计 | no_linked_component；not_reported | §4.1--§4.5，`paper_content.txt:594-595`、`645-646`、`681-682`、`728-729`、`761-762` |
| challenge roadmap | open_question | OQ1--OQ14 的 id 与文本 | 不作主统计；可作 roadmap seed | not_reported | `paper_content.txt:595-823` |
| evidence / maturity | support_type | citation；website/tool example；companion prototype；benchmark result；industrial interaction；author opinion；community discussion | 不作统计；支撑 evidence strength | companion_work_not_read；fast_drifting_fact | 全文引用和 `paper_content.txt:61-69`、`405-415`、`448-459`、`632-636`、`672-676`、`714-718` |
| validity / quality / artifact | limitation_or_risk | visionary nature；not extensive challenge list；no systematic protocol；ToM not silver bullet；requires all prototypes; only time will tell；opposing views welcomed；author ecosystem bias；rapidly drifting tool/model facts；no replication package reported | 可作为 risk_only / boundary anchor | not_reported；not_applicable | `paper_content.txt:303-306`、`584-586`、`637-640`、`840-856` |

建议关系边表至少包含：

| 关系边 | 源节点 | 关系类型 | 目标节点 / 取值 | 证据定位 |
|---|---|---|---|---|
| stack-transition | stack_component | has_transition_pair | SE2.0 state -> SE3.0 state | Fig.3 |
| challenge-affects-component | challenge_item | affects | stack_component | §4 Affects 字段 |
| oq-belongs-to-challenge | open_question | belongs_to | challenge_item | §4 |
| vision-addresses-oq | our_vision | addresses | open_question | §4 |
| evidence-supports-vision | support_type | supports_or_limits | our_vision / claim | §3--§4 companion evidence |
| risk-limits-claim | limitation_or_risk | limits | root / challenge / support_type | §3.1、§4、§5 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 修正技术栈候选取值错误 | `review.md` 原文模式候选叶子映射，尤其 `leaf-ai-native-se-roadmap-orig-stack-layer` | 将“需求、设计、编码、测试、维护、协作或平台层”改为原文 Fig.3 的五层：Teammate.next、IDE.next、Compiler.next、Runtime.next、FM.next，并补每层 SE2.0 -> SE3.0 transition pair。 | Fig.3；`paper_content.txt:243-279`；PDF 第 6 页 | C |
| 扩展原文候选叶子，不要只保留 5 个粗叶子 | `## 维度树复原` 的“原文模式候选叶子映射” | 至少新增 era transition、SE2.0 limitation、SE3.0 principle、stack transition、intent flow、curriculum recipe、FM system landscape、challenge template、OQ、evidence/maturity、validity/risk、artifact/link status。 | Fig.1、Fig.3、Fig.4、Fig.6、§4；`paper_content.txt:97-131`、`243-279`、`343-396`、`521-543`、`550-586`、`595-823` | C |
| 增加关系边表 | `## 维度树复原` 中叶子表后 | 增加 `challenge -> affected component`、`OQ -> challenge`、`our vision -> OQ`、`stack component -> transition pair`、`evidence source -> claim`、`risk -> claim` 等边。 | §4 Affects / OQ / Our vision；Fig.3 | I |
| 把 A.2 泛定位替换为精确页 / 图 / 行号 | A.2 维度树证据账本 | 不要写“方法 / 结果页”“见释义”。本文没有 Method/Results；应写 “Fig.3 / PDF p.6 / §3 / paper_content lines 243--279”等。仍未核对的图保留 `not_verified`。 | 当前 A.2：`review.md:351-354`；原文图与章节 | I |
| 修正 A.3 C02--C07 的来源措辞 | A.3 结论-证据映射 | 将“来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构”改为“来自跨论文通用接口，本文只提供降级后的 vision/roadmap 证据入口”；对原文叶子另建 C12+ 结论。 | `review.md:362-367`；原文无 RQ/Method/Evaluation | I |
| 显式加入 evidence source / maturity / artifact 字段 | 原文模式候选叶子和 A.2/A.3 | 区分 citation、companion prototype、benchmark、industry/community signal、author opinion、tool webpage；记录 companion work 是否已读、是否独立验证、是否快速漂移、是否有 replication package。 | `paper_content.txt:61-69`、`405-415`、`448-459`、`632-636`、`672-676`、`714-718` | I |
| 增加 vision-paper validity / quality 字段 | boundary risk 分支 | 把 no systematic protocol、challenge list not extensive、ToM not silver bullet、requires all components prototypes、only time will tell、opposing views welcomed、自引用生态、快速漂移作为显式风险取值，而不是只留在叙述段落。 | `paper_content.txt:303-306`、`584-586`、`637-640`、`840-856` | I |
| 更新 PDF 核对状态 | 快速卡片、A.4 | 当前 `review.md` 写未人工打开 PDF；本次审计已核对 Fig.1/Fig.3/Fig.6，但未全图核对。若后续修改 review，应改成“已部分核对关键图，Fig.2/4/5/7 待核对”。 | 本审计使用 `pdfinfo`、`pdftoppm`、视觉查看 PDF 第 3/6/13 页 | M |
| 根节点命名去掉 RQ 暗示 | 根问题 / RQ 到主干分支映射 | 改为“目标 / 贡献声明 / roadmap 对象到主干分支映射”；本文无 RQ。 | `paper_content.txt:8-21`、`51-73` | M |

## 6. C/I/M 结论

- C：2 项。第一，原文 schema 候选叶子过小，且技术栈取值与 Fig.3 明显不一致；这会直接破坏 Paper2 对 roadmap/challenge 树的模式复原目标。第二，当前树遗漏 Fig.1/Fig.4/Fig.6、§3.6 curriculum recipe 和 §4 challenge template 等核心结构，导致 A2a 无法从本 review 可靠回填原文维度模式。
- I：6 项。主要是取值空间不可执行、关系边缺失、candidate finding path 不完整、A.2 泛定位、A.3 通用接口来源措辞可能误导、evidence/maturity/artifact/validity 字段未进入维度树。
- M：2 项。根节点用语需要去掉 RQ 暗示；PDF 核对状态需要在后续 review 修订时更新。
- 最终建议：NEEDS FIX。

总体判断：当前 `review.md` 的降级纪律是对的，已经避免把该 vision/roadmap 文献写成 SLR/SMS 统计证据，也明确说明六个通用 `leaf-*` 不是原文 schema。但“维度树复原”仍没有达到完整、准确、可追溯的原文 schema 复原标准；它目前更像“通用接口 + 粗候选索引”。在进入 A2a 之前，至少需要按 Fig.1/Fig.3/Fig.4/Fig.6 和 §4 challenge template 重建原文叶子与关系边，并把所有候选叶子绑定到精确页面、图号、章节或行号。
