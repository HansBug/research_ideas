# 博士研究工作区

这是我的博士论文研究内容集散中心，用于管理和组织整个博士研究过程中的所有材料。

## 研究主题

**基于大语言模型（LLM）的控制系统状态机建模与验证方法**

构建覆盖“生成-验证-修复”全生命周期的自动化、迭代式闭环方法，系统性解决从非形式化需求到高可信度形式化模型的转化难题。

## 仓库用途

这个仓库是我的：

- **文献调研中心**：存放阅读的论文、基线方法分析和专题文库。
- **研究笔记本**：记录研究想法、讨论摘要、技术方案，以及与导师/他人的讨论纪要。
- **开题材料库**：博士开题报告、文献综述等正式文档。
- **工具箱**：研究过程中开发的辅助工具、实验脚本和运行记录。
- **外部情报入口**：维护 LLM 模型现状、CCF venue、投稿时间线、博士毕业要求等会随时间变化且影响研究决策的信息。

## 目录结构

```text
.
├── phd_proposal/                               # 博士开题相关文档
│   ├── phd_proposal_report/                    # 开题报告（LaTeX）
│   └── phd_proposal_literature_review/         # 文献综述（LaTeX）
│
├── project_1_llm_state_machine_modeling/       # 研究内容一：LLM 状态机结构化建模
│   ├── paper_stm_issue_discover/               # 第一篇论文（STM issue discover）完整工作区
│   └── archive/agent_loop_method/              # 已停用但完整保留的旧 agent-loop 方法基础设施
├── project_2_verification_scenario_generation/ # 研究内容二：验证场景与性质生成
├── project_3_profile_based_verification/       # 研究内容三：基于验证剖面的状态机验证
├── project_4_iterative_model_repair/           # 研究内容四：迭代式模型修复
├── project_ex1_llm_judge_for_stm/              # 计划外项目：状态机制品 LLM-as-Judge 评审方法
│
├── llm_model_landscape/                        # LLM 模型能力、价格、上下文窗口与 baseline 情报库
├── ccf_venues/                                 # CCF venue、deadline、年度主页与投稿 TIMELINE 情报库
├── degree_requirements/                        # 博士毕业要求、政策文件、邮件证据与加密 raw 档案情报库
├── open_explore/                               # 探索型专题入口（暂未归属具体 project 的专题文库）
├── talks/                                      # 与导师/同门/合作者等人类对象的讨论纪要工作区
├── runs/                                       # 实验、smoke、handoff 等运行记录与可复现证据链入口
│
├── tools/                                      # 研究辅助工具
│   ├── pdf_extractor.py                        # PDF 文本提取工具
│   └── init_talk_workspace.py                  # 讨论工作区初始化工具
│
├── TARGET.md                                   # 研究内容总结（核心参考文档）
├── CLAUDE.md                                   # 仓库级 AI / Claude Code 使用指南
├── AGENTS.md                                   # 指向 CLAUDE.md 的软链接
└── requirements.txt                            # Python 依赖
```

**论文组织方式**：论文可以出现在任何路径下（如各个 project 目录、专门的文献目录等）。每篇论文都应遵循所属论文集的本地 `README.md` / `GUIDE.md` / `SUMMARY.md` 约束；若暂不属于论文集，默认至少维护：

- `paper.pdf` - 论文原文；
- `paper_content.txt` - 自动提取的文本；
- `bibtex.bib` - BibTeX 引用信息；
- `desc.md` 或所属论文集要求的其他派生文件。

详细规范见 [CLAUDE.md](./CLAUDE.md) 中的“论文文件管理规范”部分。

## 核心文档说明

### [TARGET.md](./TARGET.md)

研究内容的完整总结，包括：

- 四大研究主题的详细描述；
- 技术方案和形式化定义；
- 文献调研内容；
- 工作计划和时间表。

**这是最重要的参考文档，想快速回忆研究内容就看这个。**

### [CLAUDE.md](./CLAUDE.md)

给 Claude Code / Codex / 后续 AI agent 的仓库级使用指南，包含：

- 仓库结构说明；
- 常用工具与环境使用方法；
- 论文集、情报库和讨论纪要工作区规范；
- 研究基础设施 PR、review、run record、LLM `.env`、外部情报 dry-run 等通用流程；
- 核心技术概念。

`AGENTS.md` 是 [CLAUDE.md](./CLAUDE.md) 的软链接，更新仓库级 AI 指南时只改 [CLAUDE.md](./CLAUDE.md)。

### [project_1_llm_state_machine_modeling/archive/agent_loop_method/README.md](./project_1_llm_state_machine_modeling/archive/agent_loop_method/README.md)

`project_1` 旧 agent-loop 方法基础设施入口（**已停用，完整保留可复活**），覆盖 NL → pyfcstm DSL 的阶段化建模、反馈、修复、run record 和 smoke / handoff 工作。它不参与第一篇论文（STM issue discover）的任何结论；需要回溯旧 agent loop、Path 1 / Path 2 共享基础设施或历史 run record 时才从这里进入。

### [llm_model_landscape/README.md](./llm_model_landscape/README.md)、[llm_model_landscape/GUIDE.md](./llm_model_landscape/GUIDE.md) 与 [llm_model_landscape/SUMMARY.md](./llm_model_landscape/SUMMARY.md)

用于维护 LLM 模型现状、价格、上下文窗口、最大输出、发布时间、API / 开放权重可获取性和 baseline 模型矩阵。涉及模型选型、模型能力边界、价格或上下文窗口时，应先读这三个入口，再进入对应编号分册。

### [ccf_venues/README.md](./ccf_venues/README.md)、[ccf_venues/GUIDE.md](./ccf_venues/GUIDE.md)、[ccf_venues/SUMMARY.md](./ccf_venues/SUMMARY.md) 与 [ccf_venues/TIMELINE.md](./ccf_venues/TIMELINE.md)

用于维护 CCF 会议 / 期刊、年度主页、CFP、important dates、投稿窗口、论文名录、核心人员情报与跨 venue 时间线。涉及投稿决策、deadline、special issue、accepted papers、proceedings 或年度状态更新时，应按本库 GUIDE 与 TIMELINE 的常态化刷新流程处理。

### [degree_requirements/README.md](./degree_requirements/README.md)、[degree_requirements/GUIDE.md](./degree_requirements/GUIDE.md) 与 [degree_requirements/SUMMARY.md](./degree_requirements/SUMMARY.md)

用于维护 2022 级学术型博士毕业 / 学位申请创新成果要求、政策版本、邮件往来证据、2014 版缺口、2024 版 / 新版候选政策文件和加密 raw 原始档案。涉及毕业成果规划、政策适用、外部论文是否可计入或向老师索取原文时，应先读这三个入口，再进入具体证据目录。

### [talks/README.md](./talks/README.md) 与 [talks/GUIDE.md](./talks/GUIDE.md)

用于维护与导师、同门、合作者等人类对象的讨论纪要，强调：

- 每次讨论必须使用 `yyyy-mm-dd-对象-主题` 一类子目录；
- 子目录中同时维护 `prep/`、`ppt/`、`raw.md`、`minutes.md`、`todo.md`；
- `ppt/` 内统一用 Python 的 `generate_ppt.py` 维护 `deck.pptx`；
- 默认借助本机已安装的 `deck-workflow` skill 做 guide-first 工作流。

## 四大研究主题

1. **基于控制系统软件需求的 LLM 状态机结构化建模方法**
   - 从非结构化需求到形式化状态机模型；
   - 支持层次化状态、时间属性建模。

2. **基于模型元素的验证场景与待验证性质生成方法**
   - 自动生成验证剖面和形式化性质；
   - 融合领域知识库。

3. **基于验证剖面的状态机验证方法**
   - 混合验证策略（场景驱动测试 + 形式化验证）；
   - 反例生成与缺陷根因分析。

4. **面向已知缺陷的迭代式模型修复方法**
   - 基于验证反馈的自动修复；
   - 形成“验证-修复”迭代闭环。

## 常用操作

### 添加新论文分析

```bash
# 1. 在合适的位置创建论文目录（如相关 project 目录下）
mkdir -p project_1_llm_state_machine_modeling/related_work/论文关键词

# 2. 放入 PDF 文件，文件名优先统一为 paper.pdf

# 3. 提取文本
python -m tools.pdf_extractor \
  -i "path/to/paper/paper.pdf" \
  -o "path/to/paper/paper_content.txt" \
  -m text

# 4. 按所属论文集 GUIDE 编写 desc.md 或其他派生文件
```

### 记录一次讨论纪要

```bash
# 1. 初始化单次讨论目录
python -m tools.init_talk_workspace 2026-04-14-导师-讨论主题

# 2. 先完善准备材料与 PPT 指南
# talks/2026-04-14-导师-讨论主题/prep/notes.md
# talks/2026-04-14-导师-讨论主题/ppt/PPT_GUIDE.md

# 3. 生成并 review deck
python talks/2026-04-14-导师-讨论主题/ppt/generate_ppt.py
python ~/.codex/skills/deck-workflow/scripts/render_review.py \
  talks/2026-04-14-导师-讨论主题/ppt/deck.pptx \
  --output-dir talks/2026-04-14-导师-讨论主题/ppt/rendered

# 4. 讨论后记录 raw.md，再扩写 minutes.md
```

### 更新快速变化外部情报

- LLM 模型、价格、上下文窗口：先读 [llm_model_landscape/README.md](./llm_model_landscape/README.md)，再读 [llm_model_landscape/GUIDE.md](./llm_model_landscape/GUIDE.md)，最后读 [llm_model_landscape/SUMMARY.md](./llm_model_landscape/SUMMARY.md)。
- CCF venue、deadline、投稿窗口：先读 [ccf_venues/README.md](./ccf_venues/README.md)，再读 [ccf_venues/GUIDE.md](./ccf_venues/GUIDE.md)，并结合 [ccf_venues/SUMMARY.md](./ccf_venues/SUMMARY.md) 与 [ccf_venues/TIMELINE.md](./ccf_venues/TIMELINE.md)。
- 外部事实默认官方来源优先；WAF、403、404、CAPTCHA、candidate URL 或第三方聚合页只能降级记录，不能写成已核验官方事实。
- 博士毕业要求、政策文件、邮件证据与加密 raw 档案：先读 [degree_requirements/README.md](./degree_requirements/README.md)，再读 [degree_requirements/GUIDE.md](./degree_requirements/GUIDE.md)，最后读 [degree_requirements/SUMMARY.md](./degree_requirements/SUMMARY.md)。

### 环境设置

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# 安装依赖
pip install -r requirements.txt

# 初始化 pyfcstm submodule（初次 clone 或 submodule 缺失时）
git submodule update --init --recursive
pip install -e ./pyfcstm
```

涉及真实 LLM 调用时，配置真源是仓库根的 **`.llmconfig.yml`**（`600` 权限，不入库）。它是一份 profile 表，每个 profile 直接写 `adapter` / `base_url` / `api_key` / `model` 等字段；样例见 [.llmconfig.example.yml](./.llmconfig.example.yml)。

**切换模型靠 `--profile <名字>`，不靠环境变量。** 运行时刻意拒绝从环境变量静默取凭据，所以**不需要 `source .env`**（仓库也没有 `.env`）。自检：

```bash
python -m utils.llm list              # 有哪些 profile
python -m utils.llm validate          # 校验配置
python -m utils.llm show <profile>    # 看单个 profile
```

⚠️ `.llmconfig.yml` 内含明文凭据，不要 `cat` 它、不要把内容贴进任何输出。

⛔ **已归档的旧 agent loop（`project_1_llm_state_machine_modeling/archive/agent_loop_method/`）走的是另一套**：它直接读 `os.environ` 的 `LLM_ENDPOINT` / `LLM_API_KEY` / `LLM_MODEL`。两套机制并存，判据是——代码走 `utils/llm/` 就用 `.llmconfig.yml`，直接 `os.environ[...]` 取三件套的才是旧 loop。

## 关键技术栈

- **形式化方法**：时间自动机、模型检查、时序逻辑（LTL/CTL）；
- **工具**：UPPAAL、pyfcstm（自研 DSL）；
- **数据集**：101 条功能安全需求，9 个控制系统（BSN、CARA、Elevator 等）；
- **标准**：ISO 26262、IEC 61499。

## 研究时间线

- 2025.09 - 2025.10：数据集整理；
- 2025.11 - 2026.02：多步式建模方法；
- 2026.03 - 2026.06：验证场景与性质生成；
- 2026.07 - 2026.10：基于剖面的验证方法；
- 2026.11 - 2027.01：迭代修复方法；
- 2027.02 - 2027.04：论文撰写与答辩。

## 备注

- 所有文档使用中文撰写；
- LaTeX 文档使用 XeLaTeX 编译；
- 优先使用 `tools/pdf_extractor.py` 处理 PDF 文件；
- 讨论材料优先使用 `python -m tools.init_talk_workspace` 初始化；
- 文献分析、外部情报维护、PR review 与真实运行记录按照 [CLAUDE.md](./CLAUDE.md) 中的规范编写。

---

**最后更新**：2026年6月
