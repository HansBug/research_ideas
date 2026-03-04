# 博士研究工作区

这是我的博士论文研究内容集散中心，用于管理和组织整个博士研究过程中的所有材料。

## 研究主题

**基于大语言模型（LLM）的控制系统状态机建模与验证方法**

构建覆盖"生成-验证-修复"全生命周期的自动化、迭代式闭环方法，系统性解决从非形式化需求到高可信度形式化模型的转化难题。

## 仓库用途

这个仓库是我的：
- **文献调研中心**：存放阅读的论文、基线方法分析
- **研究笔记本**：记录研究想法、讨论摘要、技术方案
- **开题材料库**：博士开题报告、文献综述等正式文档
- **工具箱**：研究过程中开发的辅助工具

## 目录结构

```
.
├── phd_proposal/              # 博士开题相关文档
│   ├── phd_proposal_report/          # 开题报告（LaTeX）
│   └── phd_proposal_literature_review/  # 文献综述（LaTeX）
│
├── project_1_llm_state_machine_modeling/      # 研究内容一
├── project_2_verification_scenario_generation/ # 研究内容二
├── project_3_profile_based_verification/      # 研究内容三
├── project_4_iterative_model_repair/          # 研究内容四
│
├── tools/                     # 研究辅助工具
│   └── pdf_extractor.py              # PDF文本提取工具
│
├── TARGET.md                  # 研究内容总结（核心参考文档）
├── CLAUDE.md                  # Claude Code 使用指南
└── requirements.txt           # Python依赖
```

**论文组织方式**：论文可以出现在任何路径下（如各个project目录、专门的文献目录等）。每篇论文都应遵循统一的文件结构：
- `*.pdf` - 论文原文
- `paper_content.txt` - 自动提取的文本
- `desc.md` - 论文总结与分析
- `bibtex.bib` - BibTeX引用信息（可选，便于快速生成参考文献）

详细规范见 [CLAUDE.md](CLAUDE.md) 中的"论文文件管理规范"部分。

## 核心文档说明

### TARGET.md
研究内容的完整总结，包括：
- 四大研究主题的详细描述
- 技术方案和形式化定义
- 文献调研内容
- 工作计划和时间表

**这是最重要的参考文档，想快速回忆研究内容就看这个。**

### CLAUDE.md
给 Claude Code 的使用指南，包含：
- 仓库结构说明
- 常用工具使用方法
- 文献管理规范
- 核心技术概念

## 四大研究主题

1. **基于控制系统软件需求的LLM状态机结构化建模方法**
   - 从非结构化需求到形式化状态机模型
   - 支持层次化状态、时间属性建模

2. **基于模型元素的验证场景与待验证性质生成方法**
   - 自动生成验证剖面和形式化性质
   - 融合领域知识库

3. **基于验证剖面的状态机验证方法**
   - 混合验证策略（场景驱动测试 + 形式化验证）
   - 反例生成与缺陷根因分析

4. **面向已知缺陷的迭代式模型修复方法**
   - 基于验证反馈的自动修复
   - 形成"验证-修复"迭代闭环

## 常用操作

### 添加新论文分析

```bash
# 1. 在合适的位置创建论文目录（如相关project目录下）
mkdir -p project_1_llm_state_machine_modeling/related_work/论文关键词

# 2. 放入PDF文件

# 3. 提取文本
python -m tools.pdf_extractor -i "path/to/paper/论文.pdf" -o "path/to/paper/paper_content.txt" -m text

# 4. 编写 desc.md（按照 CLAUDE.md 中的规范）
```

### 环境设置

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# 安装依赖
pip install -r requirements.txt
```

## 关键技术栈

- **形式化方法**：时间自动机、模型检查、时序逻辑（LTL/CTL）
- **工具**：UPPAAL、pyfcstm（自研DSL）
- **数据集**：101条功能安全需求，9个控制系统（BSN、CARA、Elevator等）
- **标准**：ISO 26262、IEC 61499

## 研究时间线

- 2025.09 - 2025.10：数据集整理
- 2025.11 - 2026.02：多步式建模方法
- 2026.03 - 2026.06：验证场景与性质生成
- 2026.07 - 2026.10：基于剖面的验证方法
- 2026.11 - 2027.01：迭代修复方法
- 2027.02 - 2027.04：论文撰写与答辩

## 备注

- 所有文档使用中文撰写
- LaTeX文档使用XeLaTeX编译
- 优先使用 `tools/pdf_extractor.py` 处理PDF文件
- 文献分析按照 `CLAUDE.md` 中的规范编写

---

**最后更新**：2026年3月
