# formal-re-llm-roadmap · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude（claude reviewer，单篇全文级审计）
- 是否读取 `$ai-research-writing-skill`：是；已确认 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/` 目录与 `SKILL.md` / `references/paper-story.md` / `references/reviewer-guidelines.md` / `references/reviewer-self-review.md` 存在，并按其 reviewer 口径（声明范围、证据可追溯、不超越文本证据、避免强主张升级）执行
- 是否读取 `$research-planning`：是；已确认 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md` 存在，并按其 planning-prompt 口径检查 review 是否对 A2a 提供可执行的下游精核任务
- 是否读取 `$oh-my-codex:autoresearch`：是；已确认 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` 存在，按其"原文 schema 复原 -> 候选叶子取值空间 -> 候选发现降级"分层口径审计本篇
- 是否完整阅读 `paper_content.txt`：是；覆盖 Page 1 摘要 / 引言、Page 2--6 background（LLM 谱系、formal RE / temporal logic / formal models / formal analysis）、Page 6--8 sender-receiver 示例与 PROMELA/Spin 代码、Page 8--11 Roadmap A 与 Fig. 2 总结、Page 11--14 LLM-driven RE 8 项任务示例、Page 14--16 Roadmap B 与 Fig. 4 总结、Page 16--17 practical considerations 7 项、Page 17--18 conclusion 与作者优先方向；同时 grep 验证 12 个 Action Point 锚点段落位置
- 是否核对 `paper.pdf`：未做视觉级核对；本轮限制为文本级与版式锚点级（页码、章节、Fig./Listing 编号），Fig. 2 / Fig. 4 视觉层结构以 review.md 中已记录释义为准；任何升级到统计或 finding 用途前需 A2a 回 PDF 复核

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

原文摘要 Objective 与 §1 contributions 给出四点贡献（paper_content.txt Page 1 ln 26--43；Page 2 ln 90--108）：

1. LLMs 与 formal RE 综述 + background（§2）。
2. Roadmap A：以 LLMs 让 FM-based development 更可用（§4），由 §3 sender-receiver 形式化开发示例驱动。
3. Roadmap B：以 formal RE 克服 LLM-based RE 的局限（§6），由 §5 LLM-driven RE 示例驱动。
4. 实施 practical considerations 与风险（§7）。

§1 明确声明这是 vision paper，不提供 sound empirical evidence，roadmap 不应视为 exhaustive；§8 conclusion 重述这一边界并列出作者将优先推进的三个方向（NL→formal logic、LLM 生成/分析 SW artefact、LLM 解释 formal artefact）。原文没有 SLR/SMS 风格的 RQ 列表、PRISMA 流程或纳排数字。

### 2.2 方法流程与综述形态

不是 SLR / SMS / tertiary study。原文方法是"example-driven vision synthesis"：

1. §3 形式化开发示例：sender-receiver handshaking protocol，PROMELA 模型 + Spin 验证 LTL 性质 + counterexample + Python 实现 + Dafny/Nagini 候选验证。
2. §4 Roadmap A：基于 §3 的 5 个 action point + Fig. 2 三层结构（Formal Development / Conventional Development / LLM Layer）。
3. §5 LLM-driven RE 示例：ChatGPT 3.5 在 8 项 RE/SE 任务上的输出与作者点评。
4. §6 Roadmap B：基于 §5 的 7 个 action point + Fig. 4 三层结构（Formal / SW Artifact / LLM Layer）。
5. §7 practical considerations：7 项实施风险与限制。

### 2.3 原文显式可枚举的 schema

下列枚举均可直接在原文文本中定位，是原文 schema 的事实清单，而非通用接口模板：

1. **Roadmap A 五个 action point**（§4，Page 8--11，由 §3 形式化示例驱动）：
   - Generating FM and SE Artifacts（specification-to-code、code-to-model、NL-to-logic 三个子方向）。
   - Explaining FM Artifacts（model、formula、counterexample 三类对象）。
   - Translating Formal Languages（model-to-model、logic-to-logic、不同抽象级视图）。
   - Supporting Iterations and Evolution（trace-link、code-specific LLM + NL-oriented LLM 组合）。
   - Automating Knowledge Engineering（ontology 构建、artefact 一致性、artefact 间互通）。
2. **Roadmap B 七个 action point**（§6，Page 14--16，由 §5 LLM-driven RE 示例驱动）：
   - Ensuring Correctness through Formal Requirements and Argumentation。
   - Improving Mathematical Reasoning with Formal LLMs（含数学/FM 专用模型、RAG、agent + calculator/reasoner）。
   - Formal Prompt Engineering（formal notation、controlled NL、pre/post-conditions、UML-like prompt architecture）。
   - Formal Domain Knowledge and Explainability（formal ontology / knowledge graph）。
   - Ensure LLM Output Consistency through Formal Verification（abstract interpretation / abstraction of NN）。
   - Regulatory Compliance at Runtime（runtime verification）。
   - Mitigate Bias and Address Ethical Concerns（formalised ethical requirements）。
3. **Fig. 2 三层结构**（§3.4 / §4 Summary, Page 9, ln 1203--1222）：Formal Development Layer、Conventional Development Layer、LLM Layer（含多个 LLM agents，标号 1--5 对应 5 个 action point）。
4. **Fig. 4 三层结构**（§6 Summary, Page 16, ln 1780--1807）：Formal Layer、SW Artifact Layer、LLM Layer；formal layer 通过 7 条边（formal verification、FM/logical knowledge for training、formal prompts、formal ontology、verify LLMs、runtime verification、ethical requirements）接入 LLM 与 SW artefact。
5. **§5 LLM-driven RE 八项任务示例**（Page 11--14）：Requirements Generation、User Feedback Analysis、Smell Detection（anaphoric ambiguity / nocuous-innocuous / generality）、Completeness Check and Requirements Completion、Model Generation（PlantUML sequence diagram, Fig. 3）、Requirements Classification、Requirements Tracing、Code-related Tasks。
6. **§7 七项 practical considerations**（Page 16--17）：Collaboration Between LLM and FM Experts、Empirical Evaluation、Overreliance on LLM Output、Diminishing Role of Human Creativity、Limited Training on FM datasets、Proliferation and Maintainability of Artefacts、Deployment / Scalability / Technological Evolution。
7. **§6 Action Point 7（Mitigate Bias）显式 trustworthiness threats 八项**（Page 16, ln 1768--1771）：toxicity、stereotype bias、adversarial robustness、out-of-distribution robustness、robustness on adversarial demonstrations、privacy、machine ethics、fairness。
8. **§2 LLM 机制族**（Page 2--6）：BoW/tf-idf、word embeddings、BERT-family（含 RoBERTa/XLNet/Electra）、LLM（GPT/Llama/Mixtral/Gemini）、prompting strategies（含 CoT、generated knowledge prompting）、instruction tuning、RAG、LoRA、distillation、LLM agents。
9. **§2 formal RE / formal model / formal analysis 族**：formal specification language、temporal logic（LTL/CTL/RTCTL/μ-calculus）、formal models（LTS/FSM/Büchi automata、Timed Automata、Probabilistic/Stochastic state machines、Statecharts、Petri Nets）、formal analysis（abstract interpretation、static analysis、model checking、proof assistant、deductive verification、refinement）。

### 2.4 原文如何形成 finding / gap / recommendation

原文不形成"经验 finding"，而是从示例的限制（formal 难写难解释 / LLM 输出不可靠）抽出 action point；每个 action point 给出 concern → mechanism → 已知 seminal works → 局限。结论部分（§8）仅声明 roadmap 服务于"激发研究"，并指明作者三项优先方向。§7 不是 threats-to-validity 章节，而是实施风险清单。

原文没有：extraction form、coding scheme、taxonomy with frequency、quality rubric、evidence table、validity threats matrix、artifact availability statement（仅末尾 "No data was used"）。这一点是 vision/roadmap 类型的天然边界，不应"凑全"。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | [dim-formal-re-llm-roadmap-root] 限定在"本文内部 schema 复原"，结论强度 weak，类型标 boundary_anchor / vision/roadmap，未越界 | 通过 |
| 主干分支是否覆盖原文 schema | 部分覆盖；I 级 | [b1] roadmap direction、[b2] layer、[b3] task family、[b4] assurance concern、[b5] human gate / limitation 五个主干能映射原文双向 roadmap + 层级图 + concern；但 [b3]/[b4] 未拆开"FM 强化 LLM"与"LLM 强化 FM"两侧任务，§4 与 §6 的不对称结构在主干层被压成一棵 | I |
| 叶子维度是否足够具体 | 不足；I 级 | "叶子维度表"仅 6 个跨论文通用接口叶子（scope/corpus/taxonomy/method/evidence/finding）；"原文模式候选叶子映射"只补 4 个抽象 seed（roadmap-direction / task-family / assurance-concern / human-gate），原文已显式枚举的 5+7=12 个 action point、Fig.2/4 各 3 个 layer、§5 八项 LLM-RE 任务、§7 七项 practical considerations、§6 八项 trustworthiness threats、LLM/FM 机制族和 formal model 族均未固化为可执行取值空间 | I |
| 取值空间是否可执行 | 不足；I 级 | 候选叶子取值空间仍为自由文本（如 "需求抽取、形式化、分析、验证、追踪、修复等"），未列原文标号 action point；A2a 必须重读原文复原，造成"已做过的 schema seed 工作丢弃"，与历史草稿 §6.1--6.3 中已经枚举的 roadmap_id / direction / layer / task_family / artifact_in / artifact_out / mechanism / action_point / maturity / evaluation_need / FM_usability_concern / LLM_output_concern / process_concern / trustworthiness_target / trustworthiness_property / assurance_mechanism / human_gate / evidence_strength 直接矛盾 | I |
| 关系边是否缺失 | 部分；I 级 | Fig. 2 标号 1--5 与 Fig. 4 标号 1--7 是原文显式 layer↔action 关系边；当前维度树没有 relation 列；候选发现路径"action point → concern → mechanism → limitation → evaluation_need"在历史草稿中已存在但未迁入正式表 | I |
| 统计用途 / 分母是否正确 | 通过 | 主统计池正确标"否"；[dim-root] 显式写 not_eligible_for_statistical_synthesis；分母用 "当前 19 篇 survey-of-surveys 样本"，仅用于 schema 分布而非领域统计 | 通过 |
| 候选 finding 路径是否完整 | 不足；M/I 边界 | [leaf-finding] 只提供"统计观察 → 候选发现 → 研究者裁决"通用链路，但未把原文 12 个 action point 的"concern → mechanism → evaluation_need → human gate"具体路径写成候选发现台账模板；考虑到 boundary_anchor 角色不要求完整 finding，倾向 I 而非 C | I |
| A.1--A.4 证据链是否足够 | 部分；I 级 | A.1 来源三件套齐全；A.2 仅 4 行（EV-001--004），全部 `not_verified`，且页码字段写 "待 A2a 精确页码复核"；原文 §3/§4/§5/§6/§7 实际页码（Page 6--8 / 8--11 / 11--14 / 14--16 / 16--17）与 Fig. 2 Page 9、Fig. 4 Page 16、Action Point 标号位置（grep 已定位 ln 955/975/1111/1143/1167/1599/1633/1668/1710/1744/1765/1777）完全可在本轮文本级核验补齐；A.3 9 条结论引用键齐全但全部 weak / boundary_anchor / schema_seed | I |
| 是否存在可能误导 A2a 的强主张 | 通过 | review §3--§7 prose 与 [clm-tree-type] / [clm-transfer] / [clm-finding-boundary] / [clm-source-schema-candidates] 反复声明 vision/roadmap、boundary_anchor、schema_seed、not_eligible_for_statistical_synthesis、final research finding 需研究者裁决；§7.2 风险列出"roadmap 不能混入统计池"、"action point 不是 empirical finding"、"过度形式化风险"；未发现把作者愿景写成已验证发现的语句 | 通过 |

## 4. 建议维度树骨架

当前根节点与五个主干分支方向合理，但叶子层应同时保留"跨论文通用接口"（用于 A2a 统一收口）与"原文模式实测叶子"（用于 schema seed），并对后者补取值空间和原文页码锚点。建议骨架：

```text
[dim-root] Formal RE + LLM two-way roadmap（vision / roadmap，boundary_anchor）
├── [b1] roadmap_direction
│   ├── [leaf-scope]  通用接口叶子（保留现状）
│   └── [leaf-orig-direction]  取值：{LLM_for_FM_usability, FM_for_LLM_trustworthiness, bidirectional/feedback}；证据：摘要 Objective + §1 contributions + §4 / §6 标题
├── [b2] layer（Fig. 2 / Fig. 4 三层结构）
│   ├── [leaf-corpus]  通用接口叶子（roadmap 写 not_applicable）
│   └── [leaf-orig-layer]  取值：{Formal Development Layer, Conventional Development Layer, Formal Layer, SW Artifact Layer, LLM Layer (含 LLM agents 子角色)}；证据：§4 Summary ln 1203--1222 / §6 Summary ln 1780--1807
├── [b3] task_family（拆双侧）
│   ├── [leaf-taxonomy]  通用接口叶子
│   ├── [leaf-orig-roadmapA-action]  取值：5 项 Roadmap A action point 全枚举；证据：Page 8--11 ln 955 / 1048 / 1114 / 1147 / 1171
│   ├── [leaf-orig-roadmapB-action]  取值：7 项 Roadmap B action point 全枚举；证据：Page 14--16 ln 1556 / 1604 / 1639 / 1675 / 1714 / 1748 / 1777
│   └── [leaf-orig-llm-re-task]  取值：8 项 §5 LLM-driven RE 任务全枚举；证据：Page 11--14
├── [b4] assurance_concern（含 trustworthiness 子树）
│   ├── [leaf-method]  通用接口叶子
│   ├── [leaf-orig-fm-usability-concern]  取值：{formal language difficulty, modularity, counterexample interpretability, tool diversity, state-space explosion, traceability, expert accessibility}；证据：§3 / §4 Explaining / Translating / Iterations 段
│   ├── [leaf-orig-llm-output-concern]  取值：{correctness/hallucination, ambiguity/incompleteness, logical coherence, math reasoning, prompt ambiguity, domain grounding, output consistency under perturbation, predictability, overreliance}；证据：§5 各任务点评 + §7
│   ├── [leaf-orig-trustworthiness-threat]  取值：8 项原文显式枚举（toxicity, stereotype bias, adversarial robustness, OOD robustness, robustness on adversarial demonstrations, privacy, machine ethics, fairness）；证据：Page 16 ln 1768--1771
│   └── [leaf-orig-assurance-mechanism]  取值：{formal requirements & properties, formal verification, formal argumentation, formal prompts + pre/post-conditions, formal ontology / KG, abstract interpretation of NN, runtime verification, formalised ethical requirements}；证据：§6 各 action point
├── [b5] human_gate / limitation
│   ├── [leaf-evidence]  通用接口叶子（roadmap 全部 evidence_role = author_claim / worked_example，不进入主统计池）
│   ├── [leaf-finding]  通用接口叶子（候选发现台账）
│   ├── [leaf-orig-human-gate]  取值：{ambiguity clarification, expert review of non-unique output, QC checklist, hallucination pattern challenge, accept/downgrade/reject}；证据：§7 Overreliance / Empirical Evaluation / Human Creativity
│   └── [leaf-orig-practical-consideration]  取值：7 项 §7 practical considerations 全枚举；证据：Page 16--17
└── [关系边] Fig. 2 1..5 与 Fig. 4 1..7 标号映射 action point ↔ layer
```

所有 `leaf-orig-*` 叶子统一标 `not_eligible_for_statistical_synthesis = true`、`evidence_role = schema_seed`、`evidence_strength = weak`、`证据要求 = 文本级 + 页码 + 段落锚点`、`缺失值语义 = vision/roadmap not_applicable`。其作用是把 A2a 精核工作量从"重读原文复原 schema"压成"逐条页码核验是否被作者明确表述"。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 把 Roadmap A 5 个 action point 显式枚举为候选叶子取值空间 | review.md "原文模式候选叶子映射（A1 种子）"表 | 新增 `[leaf-formal-re-llm-roadmap-orig-roadmapA-action]`，取值空间填入 5 项 action point 全名 + Fig. 2 标号 1--5 | paper_content.txt ln 955 / 1048 / 1114 / 1147 / 1171；§4 Summary | I |
| 把 Roadmap B 7 个 action point 显式枚举为候选叶子取值空间 | 同上 | 新增 `[leaf-formal-re-llm-roadmap-orig-roadmapB-action]`，取值空间填入 7 项 action point 全名 + Fig. 4 标号 1--7 | paper_content.txt ln 1556 / 1604 / 1639 / 1675 / 1714 / 1748 / 1777；§6 Summary | I |
| 把 §5 八项 LLM-driven RE 任务固化为候选叶子 | 同上 | 新增 `[leaf-...-orig-llm-re-task]`，取值空间填入 8 项任务名 | paper_content.txt Page 11--14 | I |
| 把 §7 七项 practical considerations 固化为候选叶子 | 同上 | 新增 `[leaf-...-orig-practical-consideration]` | paper_content.txt Page 16--17 ln 1816 起 | I |
| 把 §6 Action Point 7 显式 8 项 trustworthiness threats 固化为候选叶子 | 同上 | 新增 `[leaf-...-orig-trustworthiness-threat]`，取值空间填入 8 项 | paper_content.txt ln 1768--1771 | I |
| 把 Fig. 2 / Fig. 4 三层结构与 layer↔action 关系边写入维度树 | "维度树结构"代码块 + 候选叶子表 | 新增 `[leaf-...-orig-layer]`，并在维度树代码块加一行关系边说明（Fig. 2 标号 1--5、Fig. 4 标号 1--7） | §4 Summary ln 1203--1222；§6 Summary ln 1780--1807 | I |
| 把 A.2 证据账本中"待 A2a 精确页码复核"替换为本轮已可定位的页码 / 行号 | review.md §A.2 EV-001--004（必要时新增 EV-005--010） | EV-002 拆分为 EV-roadmapA-action / EV-roadmapB-action / EV-llm-re-task / EV-trustworthiness-threat / EV-practical-consideration，各自填具体 Page 与 ln 区间；EV-001 摘要锚点改为 Page 1 ln 26--43 + Page 2 ln 90--108 | grep 已定位的行号 | I |
| 在历史草稿迁移说明中显式回写候选叶子 | review.md §"历史草稿（已迁移）" 节 | 在每段迁移说明末尾加一句："本节内容已下沉为 [leaf-...-orig-*] 候选叶子，详见原文模式候选叶子映射表" | review.md 当前 §6.1--6.3 历史草稿 | I |
| 修正主干 [b3] task_family 单侧表达 | "根问题 / RQ 到主干分支映射"表 | 在 [b3] 说明中显式区分 LLM→FM（Roadmap A）与 FM→LLM（Roadmap B）两侧，避免 A2a 误认为单向 | §4 / §6 不对称结构 | M |
| 补一行 boundary 提示：作者背景偏置 | review §A.4 或 §9 待复核 | 注明作者 Ferrari & Spoletini 自承"reflects the opinions and experience of the authors"，roadmap 选择存在背景偏置 | paper_content.txt Page 2 ln 108--114 | M |

## 6. C/I/M 结论

- **C（critical）**：无。当前 review 已正确将本文标为 vision/roadmap、`not_eligible_for_statistical_synthesis`、boundary_anchor，所有结论强度均 weak，未发现把作者愿景升级为已验证 finding 的语句，对 Paper2 学术目标与证据链没有破坏性误导。
- **I（important）**：共 8 项（见 §5 表），核心是"形式化维度树过度依赖跨论文通用接口（6 个 leaf），原文已经显式枚举的 5+7=12 个 action point、3+3 个 layer、8 项 LLM-RE 任务、7 项 practical considerations、8 项 trustworthiness threats、Fig. 2/4 标号关系边均未固化为候选取值空间"。这会让 A2a 在精核时被迫"重读原文复原 schema"，等于把 review §3--§7 prose 与历史草稿 §6.1--6.3 已经做过的 schema seed 工作丢失。同时 §A.2 证据账本中的"待 A2a 精确页码复核"在本轮文本级审计阶段已可补齐，不应再留作下游负担。这些问题影响 schema seed 复用与证据可审计性，但不破坏边界判定与统计池资格，因此为 I 而非 C。
- **M（minor）**：主干 [b3] task_family 单侧表达；作者背景偏置说明。可与 I 一并 follow-up，不阻塞。
- **最终建议：NEEDS FIX**。建议在本 PR 内（或紧随其后的 follow-up）补完候选叶子枚举与 §A.2 页码锚点；C 级无问题，主干、边界判定、统计池资格、强主张防火墙均通过，不阻塞 PR 主线推进，但作为 A1-DT 单篇维度树成品仍未达到"原文 schema 可执行复原"标准。

### 审计自检

1. 未把 `not_verified` 升级为统计结论。
2. 未把 roadmap / vision / proposal 写成完成型 finding。
3. 未臆造原文没有的字段；所有补充建议均可在 paper_content.txt 中按行号定位。
4. 已在 §3 表中明确指出当前树确实"过小且偏向通用接口"，并在 §4 给出最小修复骨架。
5. 所有 I 级问题均说明对 Paper2 schema seed 复用与证据可审计性的影响，符合仓库"学术研究仓库 Review 口径"中 I 级判定标准。
