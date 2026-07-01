# mdse-modelling-assistants-mapping · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：否。该 SKILL.md 位于 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/`，是 codex 个人技能目录，不属于本仓库内 ARS 插件或 survey_of_surveys 文库的约束事实源。本次审计未消费该文件；不冒充使用其口径。
- 是否读取 `$research-planning`：否，理由同上。
- 是否读取 `$oh-my-codex:autoresearch`：否，理由同上。
- 实际强口径来源：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/README.md`（已熟悉）、`GUIDE.md`（已读全文）、`patterns/pattern-field-schema.md`（已读全文）、`story/paper_story.md`（已熟悉于历史会话上下文；本次未重读全文）。审计判断以这三份合同 + 单篇原文为依据。
- 是否完整阅读 `paper_content.txt`：是。覆盖 §1 引言、§2 相关工作分组、§3 SMS 设计（含 §3.1 RQs、§3.2 PICO/搜索串/时间范围、§3.3 I/E、§3.4 quality assessment 10-item Likert、§3.5 抽取规则）、§4.1 协议执行结果与 PRISMA flow、§4.2 RQ1 六个 strategy clusters 含子型、§4.3 RQ2 七个 goal + 六个 limitation cluster、§4.4 RQ3 三个 metric + 三个 user cluster、§5.1 GMQ 17 工具分布 LE/C/V/NP、§5.2 RQ4 实践抽取 quotes、§6 三组交叉分析、§7 三类 validity threat、§8 conclusion + future framework + Zenodo 仓库、references [1]–[103]。
- 是否核对 `paper.pdf`：否。本轮以 `paper_content.txt` 为主，未人工打开 PDF 核对 Fig.4–15 视觉细节、bubble chart 数值版面、Fig.1/2/3/14/15 路线图与可视化原型。该限制不影响本审计对“维度树是否复原原文 schema”的核心判断。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

- MRQ：What proposals exist in the literature and practice to assist humans during modelling tasks in MDSE tools?
- RQ1：How is software modelling assisted?（抽取 strategy keywords）
- RQ2：What goals and limitations do existing modelling assistance proposals report?
- RQ3：Which evaluation metrics and target users do existing modelling assistance proposals consider?
- RQ4：What is the state of the practice on modelling assistance?（从 GMQ MDSE 工具的公开文档抽取 strategy/goal/limitation/metric/user）

显式定义：modelling assistance = any strategy（method / technique / framework / guideline）assisting humans during software modelling tasks in MDSE tools。本定义把 strategy 当作 umbrella 概念，并通过 cluster 把其下位类型再划分。

### 2.2 方法流程

- 检索：5 库（IEEE Xplore / ACM DL / Scopus / Springer Link / WoS）database search + Wohlin snowballing（B/F，4 轮，初始集为 quality assessment top-12）。
- 时间范围：1985–2024。
- PICO 搜索串：Population（MDD/MDE/MDA/MDSE/MBSE/Low code/No-code）AND Intervention（support*/assist*/help*/ease/facilitate*/simplify*）NEAR TO（user/developer/tester/software engineer/analyst/architect/usability/usage）AND（approach/proposal/concept/idea/method/manner/technique/procedure/program/assistant）。
- I/E：I1（is single proposal, not a compilation）/ I2（assists users during modelling tasks in MDSE tools）/ E1–E5（main contribution mismatch / not SE / not English / not peer-reviewed / not full-text available）。
- Quality assessment：10-item 3-point Likert（Q1–Q8 subjective + Q9 venue rank by CORE/JCR + Q10 citation count threshold ≥4 / 2–4 / <2）；top-12 进入 snowballing。
- 数据抽取：按 RQ 提取原文文本片段；未报告则留空；抽取后基于作者术语 clustering；R4 对 clustering 复核。
- 协议执行流：1996 db hits + 5 external = 2001 init screen → 51 first candidates → top-12 seed → 4 轮 snowball + 1175 new records → 3176 total screened → 77 candidates → R3/R4/R1 复核 → 58 final proposals。
- inter-rater：selection K=0.634（substantial），clustering K=0.651（substantial）。data extraction K 未计算（文本为主）。
- 复现包：Zenodo 10262145（含原始抽取、clustering 数据，以及未进入正文的 practice bubble charts）。

### 2.3 显式 extraction form / classification schema / taxonomy / coding scheme / 模型 / 图表 / roadmap / quality rubric

**RQ1 strategy（Table 2 / Fig.4）**：6 cluster
- Tools 39.7%（含子型：domain modelling recommender system, AI-empowered software assistant, domain modelling bot, modelling assistant, modelling plugin, view manager with meta layout, modelling environment, virtual reality environment, reactive system, semantic discrepancy modelling environment, model testing tool, transformation-based tool, collaborative management tool）
- Guidelines 6.9%（ISO-based standardisation, flexible workflow, refactoring process, multi-modelling architecture）
- Techniques 15.5%（model development, model validation, model repair）
- Methods 13.8%（consistency validation, model repair, task-driven reuse, MDE alignment）
- Frameworks 19.0%（agent-based change propagation, testing, collaborative modelling, co-evolution, formal, modelling）
- Languages 5.2%（mega-modelling language, language extension, modelling template）
- 全局复合属性：software_based proposals = 93.1%；single-label 强制（multi-属性 proposals 按作者 keyword 归一 cluster）。

**RQ2 goals（Table 3 + Fig.5 bubble）**：7 cluster
- G1 addressing change propagation；G2 enhancing consistency checking；G3 ensuring model compatibility（N=1）；G4 improving model quality（N=1）；G5 improving user interaction；G6 easing model evolution；G7 supporting vulnerability detection（N=1）。
- 创建/精炼角色统计：G6 单独 = 31.0%（创建）；G1+G2+G3+G4+G7 = 43.1%（精炼）；G5 = 25.9%（兼有）。

**RQ2 limitations（Table 3）**：6 cluster（正文摘要写 "five"，实际表与 §4.3 详述均给 6 个，本审计以表为准）
- L1 accuracy；L2 effort；L3 generality；L4 learnability；L5 scope；L6 usability（N=1）；L-NS = 29 篇 / 50.0%。
- L-NS 作为一等显式编码项，进入分布统计。

**RQ3 metrics（Table 4 + Fig.6 bubble）**：3 cluster + NE
- M1 effectiveness 23.6%；M2 efficiency 23.6%；M3 user perception 4.2%；NE = 48.6%。
- 一篇可有多个 metric（multi-label）。
- 框架依据：Davis TAM（Technology Acceptance Model）。

**RQ3 users（Table 4）**：3 cluster + U-NS
- U1 designers/modellers 27.6%；U2 domain experts 13.8%；U3 软件开发者s 29.3%；U-NS = 17 / 29.3%。
- U-NS 编码规则：仅写 "user" / "he/she" 即归 U-NS（而非"用户类型未知"）。

**RQ4 实践（§5.1 + §5.2 + Table 5 + Fig.7–10、13）**：
- GMQ 2023 17 工具按 4 类划分：Leaders 5（OutSystems, Mendix, MS Power Apps, Salesforce, ServiceNow）；Challengers 1（Oracle APEX）；Visionaries 3（Appian, Zoho Creator, PegaSystems）；Niche Players 8（Retool, NewGen, Unqork, Huawei Astro Zero, Creatio, YiDA, Kintone, Quickbase）。
- documented vs not_found：7 documented（41.2%）vs 10 not_found（58.8%）；LE 中 4 / 5 documented；每个 GMQ class 至少 1 个 documented。
- 共抽到 15 个 practice proposals；strategy 标注 = 80.0%；goal = 100%；limitation = 20.0%（其余 80% NS）；metric = 26.7%（其余 73.3% NS）；target user = 26.7%（其余 73.3% NS）；practice 全部 strategy 为 Tool 子类；practice 全部 user 为 U3（developers）。
- "you" 第二人称隐藏 target user 被显式编码为方法学风险。

**交叉分析（§6, Fig.11–13）**：
- Fig.11 S × G × L：Tools→G5/G6 优势；Tools→L1/L3/L5 分布均衡；Frameworks→G1 优势 + L5 偏多；Methods→G2 优势；Languages→G1/G5/G6；Guidelines→G1/G5。
- Fig.12 G × M × U：G6→U1+U3+M1+M2；G5→U1 + M2；G2→U1/U2/U3 均衡 + M1；G1→U3+U2 + M1/M2；G7/G4/G3/M3 数据稀疏不画。
- Fig.13 lit vs practice：两侧 G6 共同；G1/G5 学界多、实践少；L2/L4/L5 实践无；M3 实践无；U3 实践独占。

**Validity（§7）**：
- Internal：selection bias / data extraction bias / subjective interpretation（terminology + ontological background）/ inter-rater reliability（含 reviewer fatigue 子风险）。
- Construct：grey literature bias / search bias（含 database 选择 + snowballing 初始集 + GMQ 单源）。
- External：language bias（仅英文）。

**Roadmap / future framework（§8 + Fig.14, Fig.15）**：
- 提出 unified framework，整合 IMA framework [103]（quality / semantic / confidence / autonomy）+ assisted-modelling requirements framework [81]（target-user input）。
- Fig.14 给出 public repository 可视化原型（用 cluster 连接新 assistant 与既有 work）。
- Fig.15 给出 research agenda。

### 2.4 finding / gap / recommendation 的形成路径

paper 的 finding 形成链条：（i）从 single-axis 分布得到“以 software-based 为主、Tools 占优”；（ii）从 L-NS / NE / U-NS 高比例得到“limitations / metrics / users 报告缺失是跨学界 + 实践的共同 gap”；（iii）从 bubble cross-axes 得到 strategy-goal-limitation / goal-metric-user 的对应关系；（iv）从 lit vs practice 比较得到 G5/G1 学界偏多、practice 偏 G6+U3+Tool；（v）从 AI/LLM/GPT 既有引用 [101] + IMA [103] + 用户需求框架 [81] 得到 future framework 需求（被作者明确标注为 "expectation / future work"，不是已验证 finding）。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-...root]` 写为 “Understanding the landscape of software modelling assistants for MDSE tools”，与 paper 标题 / MRQ 一致。 | 通过 |
| 主干分支是否覆盖原文 schema | 不通过 | 5 主干 b1–b5（scope / corpus / taxonomy / method / evidence-finding）是 A1-M0–M6 通用接口的镜像，没有为原文 RQ1（strategy）/ RQ2（goal+limitation）/ RQ3（metric+user）/ RQ4（practice）单独建立主干。整篇论文的核心 schema 是“5 个 RQ-clusters + 3 个跨轴 bubble + lit-vs-practice 对照”，但当前主干只能反向猜测在 b3+b4+b5 之内。 | C |
| 叶子维度是否足够具体 | 不通过 | 6 个正式 leaf（scope/corpus/taxonomy/method/evidence/finding）是跨论文通用接口；review.md §维度树复原 line 401 已自承“不是原文叶子全集”。但补救的 5 个“原文模式候选叶子映射（A1 种子）”仍严重欠拟合：① strategy 候选取值写成“推荐、生成、补全、检测、修复、可视化、解释” —— 这是 reviewer 杜撰的 modelling-subtask 词，**不是原文 Table 2 的 6 cluster（Tools/Guidelines/Techniques/Methods/Frameworks/Languages）**；② goal 候选写成“创建模型、refinement、一致性、演化、交互、漏洞检测” —— 把 G1–G7 七类压缩为口语化短语，丢失 G3/G4/G7 的 N=1 关键信号；③ “modeling-artifact”是 reviewer 自造叶子，原文 RQs/extraction form 并无该字段，是对 Project1 STM 的迁移投射；④ limitation 取值是 6 类 + L-NS，唯一接近忠实复原的叶子；⑤ metric/user 被合并成单一 leaf “metric-user”，把 RQ3 的两个独立分类（M1/M2/M3+NE 与 U1/U2/U3+U-NS）压扁。 | C |
| 取值空间是否可执行 | 不通过 | 候选取值未给出枚举封闭性、不写缺失值语义在叶子层级、不写 multi-label vs single-label、不写分母（58 / 15 / 17）。`schema_seed` + `not_verified` 的统一标签让所有叶子都不可统计，但当前缺口不只是“待 A2a 精核”，而是 schema 本身没有从原文 Table 2/3/4/5 抽出来。 | I |
| 关系边是否缺失 | 不通过 | 当前只有 2 条 edge：method↔evidence、taxonomy↔finding，均为通用接口边。原文核心关系是 5 条 bubble cross-axes：S × G、G × L（Fig.5）、G × M、G × U（Fig.6）、S × G × L（Fig.11）、G × M × U（Fig.12）、lit × practice × 5-dim（Fig.13）。这些都是 paper 的 headline finding 载体，但在关系边表中完全缺失。 | C |
| 统计用途 / 分母是否正确 | 部分通过 / 不通过 | 统计与候选发现链路表里只写“当前 19 篇 survey-of-surveys 样本”作为分母，**但该分母是文库层面的元统计，不是本文内部的分母**。本文的分母应明确写：58（research proposals）、17（GMQ tools）、7（documented tools）、15（practice proposals）；这些分母在叶子表层缺位，导致后续 A2a 无法对接本文的频次。 | I |
| 候选 finding 路径是否完整 | 不通过 | 缺 paper 显式给出的 5 类 finding 路径：①分布观察→缺口（L-NS=50.0% / NE=48.6% / U-NS=29.3%）；②S×G×L 交叉→Tools 优势但 L 分布均衡；③G×M×U 交叉→G6 偏 U1+U3+M1+M2；④lit×practice 对照→实践无 M3/L2/L4/L5/U1/U2；⑤AI disruption + IMA[103] + req-framework[81]→future unified framework 需求。当前 `[clm-...finding-boundary]` 只是一句保守降级说明，未保留任何候选 finding 路径的字段轨迹。 | I |
| A.1--A.4 证据链是否足够 | 部分通过 / 不通过 | A.1 三个本地源齐全，good。A.2 五条证据（root / taxonomy / stat / risk / relation）覆盖太粗：5 条证据要覆盖 7 RQ-clusters + 4 cross-axes + 实践抽取 + validity + roadmap，颗粒度严重不足；页码全部写“待 A2a 精确页码复核”，邻近段落只指方向。A.3 全部 `weak` + `schema_seed`，符合 GUIDE §6.3.7 临时降级规则，但 12 条结论中 7 条是“叶子来自本文 RQ/方法/分类/评价/讨论结构 → 可作 Paper2 候选” —— 这是模板化重复，**没有任何一条结论是关于本文具体 schema 复原是否成功的可审计判断**。A.4 只有 2 条复验：结构脚本 passed + PDF 视觉 needs_manual_check。 | I |
| 是否存在可能误导 A2a 的强主张 | 通过（边界） | 全部 claim 已降到 `weak` / `schema_seed`，不存在虚假强统计；C12 显式声明候选叶子只表示 A2a 入口、不代表已复原。这部分合规。 | 通过 |

## 4. 建议维度树骨架

下方骨架严格基于 §2 复原的原文结构。建议作为 A2a 精核入口，A1-DT 阶段仍可全部标 `not_verified`，但 schema 形状应当先到位。

```text
[dim-mdse-modelling-assistants-mapping-root] MDSE modelling assistants landscape
├── [dim-...b0] 综述定义与边界
│   ├── [leaf-...definition] modelling assistance 定义 = strategy (method/technique/framework/guideline) assisting humans in modelling tasks in MDSE tools
│   ├── [leaf-...scope-exclusion] 排除：generic drawing / meta-modelling tool development
│   └── [leaf-...mrq-rq-mapping] MRQ → RQ1/2/3/4 显式拆分
├── [dim-...b1] 文献语料链条
│   ├── [leaf-...search-source] 数据库枚举 {IEEE, ACM, Scopus, SpringerLink, WoS}
│   ├── [leaf-...search-string-pico] PICO 词组 + NEAR TO 句法
│   ├── [leaf-...time-range] 1985–2024
│   ├── [leaf-...snowballing] B/F 轮数 = 4 / 初始集 = QA top-12
│   ├── [leaf-...ie-criteria] I1 / I2 / E1–E5 + 文本 + 摘要 + 全文级筛选阶段
│   ├── [leaf-...qa-likert] 10-item 3-point Likert（8 subjective + Q9 venue rank by CORE/JCR + Q10 citation threshold）
│   ├── [leaf-...prisma-flow] 1996 + 5 → 2001 → 51 → top-12 → +1175 snowball → 3176 screened → 77 candidates → 58 final
│   ├── [leaf-...inter-rater] selection K=0.634；clustering K=0.651；data-extraction K not measured
│   └── [leaf-...replication-package] Zenodo 10262145（含未发表 practice bubble charts）
├── [dim-...b2] RQ1 strategy 分类（per-proposal single-label cluster）
│   ├── [leaf-...strategy-cluster] {Tools=39.7%, Frameworks=19.0%, Techniques=15.5%, Methods=13.8%, Guidelines=6.9%, Languages=5.2%}
│   ├── [leaf-...tool-subtype] 13 个 Tool 子型枚举（recommender, AI assistant, bot, plugin, view manager, modelling environment, VR env, reactive system, semantic-lift env, model testing tool, transformation-based tool, collaborative management tool）
│   ├── [leaf-...software-based] software_based ∈ {totally, partially, no}；93.1% totally/partially
│   └── [leaf-...terminology-basis] cluster ← author keywords（reviewer 复核降级到作者 keyword）
├── [dim-...b3] RQ2 goal 分类（multi-label 实操但作者倾向 single-label cluster）
│   ├── [leaf-...goal-cluster] G1–G7 七项 + 定义 + 子项关键词
│   ├── [leaf-...goal-cardinality] G3=1, G4=1, G7=1（N=1 关键信号）
│   ├── [leaf-...create-refine-role] {create=G6=31.0%, refine=G1∪G2∪G3∪G4∪G7=43.1%, both=G5=25.9%}
├── [dim-...b4] RQ2 limitation 分类
│   ├── [leaf-...limitation-cluster] L1–L6（注意正文摘要写 five，表给 six）
│   ├── [leaf-...limitation-reporting] {specified=29 (50.0%), L-NS=29 (50.0%)} —— L-NS 作一等编码项
│   └── [leaf-...l6-cardinality] L6 usability N=1
├── [dim-...b5] RQ3 metric 分类（multi-label per proposal）
│   ├── [leaf-...metric-cluster] M1=23.6%, M2=23.6%, M3=4.2%, NE=48.6%
│   ├── [leaf-...metric-framework] 引用框架：TAM (Davis)
│   └── [leaf-...metric-evaluation-status] {empirically_evaluated, NE}
├── [dim-...b6] RQ3 target user 分类
│   ├── [leaf-...user-cluster] U1=27.6%, U2=13.8%, U3=29.3%, U-NS=29.3%
│   └── [leaf-...user-specificity-rule] "user" / "he/she" → U-NS（编码规则）
├── [dim-...b7] RQ4 实践链条
│   ├── [leaf-...gmq-class] {LE=5, C=1, V=3, NP=8}
│   ├── [leaf-...documented-status] documented=7 (41.2%), not_found=10 (58.8%)
│   ├── [leaf-...practice-proposal-count] 15 practice proposals across 7 tools
│   ├── [leaf-...practice-strategy] 全部 Tool 子型（80% 显式 strategy）
│   ├── [leaf-...practice-goal] 100% 报告 goal
│   ├── [leaf-...practice-limitation] 20% 报告（其余 80% NS）
│   ├── [leaf-...practice-metric] 26.7% 报告
│   ├── [leaf-...practice-user] 26.7% 报告 + 全部 U3
│   └── [leaf-...practice-second-person] "you" 隐藏 user 的编码风险
├── [dim-...b8] 交叉关系（bubble charts）
│   ├── [edge-...s-g] S × G（Fig.11）
│   ├── [edge-...g-l] G × L（Fig.5, Fig.11）
│   ├── [edge-...g-m] G × M（Fig.6, Fig.12）
│   ├── [edge-...g-u] G × U（Fig.6, Fig.12）
│   ├── [edge-...m-u] M × U（Fig.6）
│   └── [edge-...lit-practice] lit × practice × 5-dim（Fig.13）
├── [dim-...b9] Validity threats
│   ├── [leaf-...internal-validity] selection bias / data extraction bias / subjective interpretation (terminology + ontological) / inter-rater reliability (含 reviewer fatigue)
│   ├── [leaf-...construct-validity] grey literature bias / search bias
│   └── [leaf-...external-validity] language bias
└── [dim-...b10] Roadmap / future framework / candidate findings
    ├── [leaf-...candidate-finding] 5 类 candidate finding 路径（§2.4）
    ├── [leaf-...future-framework] IMA [103] + assisted-modelling requirements [81] → unified framework
    └── [leaf-...visualization-prototype] Fig.14 public repository 可视化
```

每个 leaf 默认 `not_verified` + `schema_seed`；缺失值语义按 paper 既有约定：`L-NS` / `NE` / `U-NS` / `not_found` 已是原文一等编码项，应直接迁入；其它字段用 `not_reported`。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干分支需对齐原文 RQ 而非通用接口 | review.md §维度树结构（line 411–424）+ 根问题表 | 把 b1–b5 重组为本审计 §4 的 b0–b10，至少为 RQ1/RQ2-goal/RQ2-limitation/RQ3-metric/RQ3-user/RQ4-practice 各建一个主干。当前 b1–b5 可作为跨论文 A1-M0–M6 接口表的“侧轴”保留，但不应替代原文 schema 主干。 | paper §3.1 RQ definitions；Table 2/3/4/5 | C |
| RQ1 strategy 候选叶子取值必须复原 6 cluster + 13 Tool 子型 | review.md §原文模式候选叶子映射 leaf-...orig-assistant-strategy 行 | 候选取值改为 `{Tools, Guidelines, Techniques, Methods, Frameworks, Languages}`，并增子叶 `tool_subtype` 枚举 13 项。删除当前“推荐、生成、补全、检测、修复、可视化、解释”这组 reviewer 自造词或明确标注为 Paper2 modelling-subtask 映射而非原文叶子。 | paper §4.2 Table 2 + 子型枚举段落 | C |
| RQ2 goal 候选叶子必须列 G1–G7 + N=1 信号 | review.md §原文模式候选叶子映射 leaf-...orig-assistant-goal 行 | 候选取值改为 `{G1 change propagation, G2 consistency checking, G3 model compatibility, G4 model quality, G5 user interaction, G6 model evolution, G7 vulnerability detection}` + 标注 G3/G4/G7 N=1。 | paper §4.3 Table 3 + Fig.5 数值 | C |
| 拆分 metric-user 单叶子为两个独立叶子 | review.md §原文模式候选叶子映射 leaf-...orig-metric-user 行 | 拆为 `leaf-...orig-metric`（M1/M2/M3/NE，TAM 框架）与 `leaf-...orig-user`（U1/U2/U3/U-NS，含 "user / he/she" 编码规则）。 | paper §4.4 Table 4 | C |
| 删除或重标注 "modeling-artifact" leaf | review.md §原文模式候选叶子映射 leaf-...orig-modeling-artifact 行 | 该叶子并非原文 RQ / 抽取项；应整段删除，或重标注为 “Paper2 / Project1 STM 投射候选，非原文叶子，证据强度 weak / risk_only”。当前位置会误导 A2a。 | paper §3.5 抽取规则 + §4.x 全部 cluster 表 | I |
| 必须新增 RQ4 实践主干 | review.md 维度树结构 | 新增 `[dim-...b7]` 与其 9 个 leaf（GMQ 4 类、documented/not_found 比例、15 practice proposals、5 维 vendor quote 分布、第二人称 hidden user 编码）。当前整篇 practice 体系（占 paper §5 + §6）在维度树中无主干。 | paper §5.1, §5.2, Table 5, Fig.9, Fig.10, Fig.13 | C |
| 必须新增交叉关系边（bubble charts） | review.md §关系边表 | 增至少 6 条 edge：S×G、G×L、G×M、G×U、M×U、lit×practice。当前只有 method↔evidence、taxonomy↔finding 两条通用边，没有承载 paper headline finding。 | paper §4.3, §4.4, §6, Fig.5/6/11/12/13 | C |
| 必须新增 PRISMA flow / QA / K-statistic 字段 | review.md §维度树结构 b1 corpus 或新建 b1 子叶 | 增加 leaf 记录 1996+5/2001/51/12/1175/3176/77/58 数值链条 + 10-item QA Likert + K=0.634/0.651。当前 b1 corpus 只有一行通用语，丢失全部数值证据链。 | paper §3.4 Table 1, §4.1 Fig.3 | I |
| 必须新增 validity threat 主干 | review.md 维度树结构 | 新增 `[dim-...b9]` validity 主干，内部至少分 internal / construct / external 三个叶子，并枚举 7 类具体威胁；当前 review.md §1.9 已对 validity 做了表格整理，但未进入维度树。 | paper §7.1–§7.3；review.md §1.9 已有素材 | I |
| 必须新增 future framework / roadmap 主干 + 降级 | review.md 维度树结构 | 新增 `[dim-...b10]` 记录 Fig.14/Fig.15 + IMA [103] + req-framework [81]；同时显式声明 future framework 是 author future work / expectation，结论强度 ≤ `weak`，允许用途仅 `boundary_anchor` / `risk_only`。当前 review.md §1.8 已有素材但未进入维度树或结论映射。 | paper §8 conclusion + Fig.14/15 + refs [81][103] | I |
| 分母字段应记录本文内部分母而非文库元分母 | review.md §统计与候选发现链路表（line 458–462） | 把 “当前 19 篇 survey-of-surveys 样本” 替换为本文分母：58 research proposals / 17 GMQ tools / 7 documented / 15 practice proposals。这是 A2a 频次统计的必备字段。 | paper §4.1 + §5.1 | I |
| L1–L6 vs five-vs-six 口径要进入叶子语义 | review.md §原文模式候选叶子映射 leaf-...orig-limitation | 在该叶子注释中显式记录：正文摘要写 five clusters，Table 3 + §4.3 详述给 6 个（含 L6 usability N=1）；这是 paper 自身的口径不一致，A2a 必须按 Table 3 复原。当前 review.md §1.6/§7.2 待复核已有记录但未绑定到叶子语义。 | paper Abstract + §4.3 + Table 3 | M |
| A.3 结论必须给出 schema-specific 而非模板化重复 | review.md §A.3 结论-证据映射 C02–C07 | 当前 C02–C07 六条都是 “该叶子来自本文 RQ / 方法 / 分类 / 评价 / 讨论结构” 模板化重复，没有 schema-specific 判断。应替换为对每个原文 cluster 是否被正确复原的具体结论（例如 “strategy 候选叶子已复原 6 cluster + 13 子型 / strategy 候选叶子未复原，使用了 reviewer 自造词”）。 | review.md A.3 现状 | I |
| A.2 证据应至少按 RQ1/2/3/4 + cross + validity + roadmap 拆分 | review.md §A.2 证据账本 | 当前 5 条证据 EV-001 到 EV-005 颗粒度过粗；建议拆为 ≥10 条，分别对应 RQ1 strategy、RQ2 goal、RQ2 limitation、RQ3 metric、RQ3 user、RQ4 practice、PRISMA flow、K-statistic、validity、roadmap。 | review.md A.2 现状 | I |

## 6. C/I/M 结论

- **C（critical，影响 Paper2 学术目标 / 维度树证据链 / A2a 下游可靠性）**：
  1. 主干分支未对齐原文 RQ。
  2. RQ1 strategy 候选取值用 reviewer 自造词替换了 Table 2 的 6 cluster + 13 Tool 子型。
  3. RQ2 goal 候选取值压扁 G1–G7。
  4. metric 与 user 被合并成单叶 `metric-user`。
  5. RQ4 整个 practice 主干缺失。
  6. paper 的 5 条 bubble cross-axes（S×G、G×L、G×M、G×U、lit×practice）作为 headline finding 载体，在关系边表中完全缺失。
- **I（important，影响维度树可用性 / 原文 schema 复原度 / 证据可审计性）**：
  1. 取值空间未给枚举封闭性 / multi-label 标记 / 缺失值语义到叶子层。
  2. 分母字段写了文库元分母而非本文内部分母（58/17/7/15）。
  3. PRISMA 流 + 10-item QA Likert + inter-rater K-statistic 全部未进维度树。
  4. validity threat 主干缺失（素材已有，未进入树）。
  5. future framework / roadmap 主干缺失。
  6. A.2 证据颗粒度过粗（仅 5 条覆盖整篇 paper schema）；A.3 结论模板化、未给 schema-specific 判断。
  7. 候选 finding 路径缺失 paper 显式给出的 5 类路径。
  8. "modeling-artifact" 是 reviewer 自造叶子，对 A2a 有误导风险（虽然程度低于上面几条，可视为 I 偏 M）。
- **M（minor，不阻塞）**：
  1. L1–L6 vs five-clusters 口径不一致已在 §1.6 / §7.2 待复核中记录，但建议绑定到叶子语义。
  2. 部分 leaf 标识命名可保持现状（命名一致性是次要问题）。

### 最终建议：**NEEDS FIX**

理由：当前维度树确实如用户怀疑的那样，**把 6 个跨论文通用接口当成了主干**，而把原文真实的 RQ1/2/3/4 schema + bubble cross-axes + RQ4 practice + validity + roadmap 全部压在 5 个粗颗粒候选叶子里，且其中 strategy / goal / metric-user / modeling-artifact 4 个候选叶子取值是 reviewer 投射而非原文复原。这会直接破坏 A2a 对本 paper 的字段频次统计、候选 finding 路径回溯，以及 Paper2 在 paper2_dimension_tree_inventory 中对 “MDSE assistant landscape” 这一脚手架样本的可信迁移。修复路径不需要回滚 A1-DT 的 `not_verified` 降级纪律，而是在不升级证据强度的前提下，**先把 schema 形状改对**，再让 A2a 按 §4 骨架做精核。
