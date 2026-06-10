# ClarifySTL：通过需求澄清进行 STL 转换的交互式 LLM Agent 框架 / ClarifySTL

## 基本信息

- **标题**：ClarifySTL: An Interactive LLM Agent Framework for STL Transformation through Requirements Clarification
- **中文标题**：ClarifySTL：通过需求澄清进行 STL 转换的交互式 LLM Agent 框架
- **作者**：Yue Fang, Zhi Jin, Jie An, Jia Li, Hongshen Chen, Xiaohong Chen, Naijun Zhan
- **单位**：Peking University；Institute of Software Chinese Academy of Sciences；Wuhan University；JD.com；East China Normal University
- **发表**：arXiv preprint, 2026-05-02；PDF 首页含 ACM TOSEM 2025 占位元数据和 `https://doi.org/XXXXXXX.XXXXXXX`，正式 DOI/卷期信息待人工核验
- **年份**：2026
- **DOI**：10.48550/arXiv.2605.01209
- **链接**：https://arxiv.org/abs/2605.01209

**代码/仓库获取方式**：
- 原文脚注说明 supplementary file and project available at：[Zenodo record 17561877](https://zenodo.org/records/17561877)。
- 本轮未进一步打开 Zenodo record 核验其中是否包含完整可运行代码、训练数据、prompt templates 和实验输出；因此这里只按原文写作“作者提供的 supplementary/project 入口”。

**数据集获取方式**：
- 原文使用 DeepSTL 与 STL-DivEn 两个代表性 NL-to-STL benchmark，并构造 AmbiEval 用于 vagueness/ambiguity detection 与 query generation。
- AmbiEval 从 DeepSTL 与 STL-DivEn 的 training split 构造，原文说明其与 2,000 个 NL-to-STL test samples 无重叠；公开获取入口仍以 Zenodo supplementary/project 为准，需人工核验具体文件。

## 简报

本文解决的问题是：自然语言 STL requirements 中常有 vague 或 ambiguous 信息，直接把这些需求交给 LLM 转 STL 会导致公式不忠实；ClarifySTL 先检测并询问用户澄清需求，再把澄清后的需求转为 STL。它属于 NL-to-STL requirement formalization 强近邻，不是状态机直接生成论文。

- **输入**：自然语言 CPS/STL requirement，可能包含 temporal/numerical/conditional vagueness 或 referential/semantic ambiguity；交互阶段还接收用户对 clarification query 的回答。
- **方法**：两阶段交互式 agent：Vagueness Detector + CoT Vagueness Inquirer 先补全缺失信息；Ambiguity Detector + Ambiguity Inquirer 再解析多重解释；最后用 LLM 将 clarified requirement 转为 STL。
- **输出**：澄清后的自然语言 requirement、clarification queries、最终 Signal Temporal Logic formula，以及 detection/query generation 评估结果。

```text
含模糊/歧义的自然语言 requirement
  -> Vagueness Detector + CoT Vagueness Inquirer + 用户补充
  -> 非模糊 refined requirement
  -> Ambiguity Detector + multi-sample STL candidates + back-translation + 用户澄清
  -> 非歧义 refined requirement
  -> LLM NL-to-STL transformation
  -> STL formula
```

实验在 DeepSTL、STL-DivEn 和 AmbiEval 上进行。ClarifySTL 在 DeepSTL 上 Formula Accuracy 67.12%、Template Accuracy 70.03%、semantic robustness 82.7%；在 STL-DivEn 上 Formula Accuracy 70.74%、Template Accuracy 72.28%、semantic robustness 84.9%，均优于 KGST 和多种 closed/open LLM baseline。检测任务中 Vagueness Detector 与 Ambiguity Detector 平均达到约 90% 以上准确率。

## 研究问题与动机

### 问题背景

STL 是 CPS 实时行为规格语言，能表达 dense-time、real-valued signal 上的 temporal constraints。现有 NL-to-STL 方法假设输入需求足够明确，但真实需求常缺时间区间、数值阈值、条件关系，或存在指代与时序解释歧义。LLM 直接转换时容易把输入歧义放大成错误公式。

### 核心问题

论文设计三类研究问题：

1. ClarifySTL 与既有 STL transformation methods 相比，能否提升 NL-to-STL accuracy。
2. ClarifySTL 的 Vagueness Detector 与 Ambiguity Detector 能否有效发现自然语言需求中的 vagueness / ambiguity。
3. ClarifySTL 生成的 clarification queries 是否正确、清晰，并能让用户提供有效澄清。

### 研究动机

作者认为，错误不只来自模型能力不足，也来自输入需求本身不完整或多义。与其让 LLM 猜测缺失信息，不如在 formalization 前显式定位缺失/歧义片段，通过有针对性的 query 获取用户意图，再生成 STL。该思路与 requirements engineering 中“先澄清再形式化”一致。

### 研究意义

对 Project 1，ClarifySTL 的价值在于它把需求质量控制前置到形式工件生成之前。状态机生成同样会受“soon”“after”“it”“normal mode”等模糊表达影响；ClarifySTL 可为 Project 1 的 requirement clarification、agent-loop ask-user gate 和 ambiguity-aware repair 提供强方法学参照。

## 核心方法

### 方法概述

ClarifySTL 分两大阶段，每个阶段都由 detector 与 inquirer 组成：

1. **Vagueness clarification**：检测 requirement 是否缺少 STL 所需信息，并生成 targeted query 让用户补充。
2. **Ambiguity clarification**：检测 requirement 是否有多重解释，并通过候选 STL、back-translation 和 discrepancy analysis 生成澄清问题。
3. **NL-to-STL transformation**：当 requirement 被判定为 non-vague 且 unambiguous 后，再用 LLM 转成 STL。

每轮澄清后都重新检测，直到当前阶段不再发现问题。

### Vagueness Detector

论文把 vagueness 定义为构造 STL 所需信息未被充分说明，分为三类：

- **Temporal Information Vagueness**：时间间隔、开始时间、持续时间缺失或用 “soon”“later” 等模糊词描述。
- **Numerical Information Vagueness**：速度、温度、阈值等数值缺失或被 qualitative descriptor 替代。
- **Conditional Logic Information Vagueness**：条件逻辑关系不完整，影响 logical operators 推断。

作者用 GPT-4o 作为 teacher model，对 DeepSTL/STL-DivEn 中需求按 type-specific mutation prompts 构造 AmbiEval Part A，并 fine-tune LLM 得到 Vagueness Detector。

### Vagueness Inquirer

Vagueness Inquirer 使用 CoT prompting。Prompt 包含 instruction、原始 requirement 与 vagueness type、以及 `<Reference Requirement, Incompleteness Reason, Reference Query>` demonstrations。它只允许围绕 detector 报告的 vague segment 和 missing component 提问，避免引入与用户意图无关的信息。若用户回答无效，系统要求用户重新表述。

### Ambiguity Detector

论文把 ambiguity 分为：

- **Referential ambiguity**：例如多个 signal 时用 “it” 等指代导致 referent underdetermined。
- **Semantic ambiguity**：同一句话可能对应多种 temporal/logical/STL 解释。

Ambiguity Detector 用 LLaMA 3-8B hidden states 作为 frozen semantic encoder，结合 projector、classification head 和 triplet/contrastive learning 学习 ambiguous 与 unambiguous requirements 的表示边界。AmbiEval Part B 通过 GPT-4o mutation 生成候选歧义句，再由两名有至少三年 STL 经验的 annotators 人工确认。

### Ambiguity Inquirer

Ambiguity Inquirer 不直接让 LLM 解释符号公式，而是利用自然语言更强的比较能力：

1. 对同一 requirement 多次采样生成 candidate STL formulas。
2. 将候选 STL back-translate 成自然语言描述。
3. 把原始 requirement 与多个 back-translated descriptions 交给 GPT-based difference analysis，生成 discrepancy report。
4. 基于 discrepancy report 生成 concise clarification queries。

Prompt 同样限制问题只能围绕 discrepancy report 中定位的 divergence points，避免无约束改写需求。

### LLM 与实现设置

- GPT-4o 用于 vagueness query generation、ambiguity query generation 和 requirement refinement。
- 框架使用四个 LLaMA 3-8B models：Vagueness Detector、两个 NL-to-STL transformation models，以及 Ambiguity Detector 的 frozen encoder。
- 训练使用 PyTorch、HuggingFace Transformers、LLaMA-Factory；8 张 NVIDIA A100 40GB；trainable models 训练 10 epochs，Adam lr=5e-5，batch size=16。
- Query generation max tokens 300；默认 temperature 0；ambiguity candidate STL sampling temperature 0.9。

## 实验与评估

### 数据集

- **DeepSTL**：代表性 NL-to-STL benchmark。
- **STL-DivEn**：包含更丰富语言表达与信号模式的 NL-to-STL benchmark。
- **AmbiEval**：本文构造，用于 vagueness/ambiguity detection 与 query generation。
- **规模**：AmbiEval Part A 为 5,400 train / 600 test；Part B 为 2,800 train / 400 test。NL-to-STL evaluation 使用 DeepSTL/STL-DivEn 的 2,000 test samples。
- **缺陷分布示例**：DeepSTL subset 中 temporal/numerical/conditional vagueness 分别为 87/39/103，referential/semantic ambiguity 为 83/117；STL-DivEn 中对应为 67/56/43 和 71/212。

### Baselines

论文比较 16 个 baselines，分为：

- **Direct transformation open-source**：DeepSTL、KGST、Qwen 3-8B/14B、LLaMA 3-8B/14B。
- **Direct transformation closed-source**：DeepSeek-V3、GPT-4o、GPT-4o-mini、Gemini-2.5-Pro、Claude-4-Sonnet。
- **Interactive transformation**：使用 closed-source LLM 的统一 few-shot prompt 来检测 vagueness/ambiguity 与生成 queries，不使用 ClarifySTL 的专门 detector/strategy。

### 评估指标

- NL-to-STL：Formula Accuracy、Template Accuracy、BLEU、semantic robustness。生成公式先过 STL syntax checker，无法通过者直接算错误。
- Detection：Accuracy、Precision、Recall、F1-score。
- Query generation：ROUGE、BERTScore、human correctness、human clarity。
- User study：10 名有至少 3 年 STL 编写/解释经验的 CPS 方向研究生或研究者回答 clarification queries；Fleiss' Kappa 和 pairwise match rate 用于一致性检查。

### 主要实验结果

- **NL-to-STL 主结果**：ClarifySTL 在 DeepSTL 上 Formula Acc. 67.12%、Template Acc. 70.03%、BLEU 0.5736、semantic robustness 82.7%；在 STL-DivEn 上 Formula Acc. 70.74%、Template Acc. 72.28%、BLEU 0.2612、semantic robustness 84.9%。
- **相对 KGST**：DeepSTL 上 Formula Accuracy 提升 14.31%、Template Accuracy 提升 12.90%、semantic robustness 提升 12.4%；STL-DivEn 上分别提升 13.50%、13.45%、11.3%。
- **Human evaluation**：ClarifySTL 在各类 vagueness/ambiguity 上 accuracy 普遍 90% 以上，如 DeepSTL 上 temporal/numerical/conditional vagueness 为 91.5%/95.2%/93.7%，referential/semantic ambiguity 为 96.1%/92.8%。
- **Detection**：Vagueness Detector 在 DeepSTL accuracy 92.2%，Ambiguity Detector 在 AmbiEval accuracy 93.1%、DeepSTL 92.5%、STL-DivEn 91.2%。
- **Query generation**：Vagueness Inquirer human correctness 最高 92.6%、clarity 最高 92.1%；Ambiguity Inquirer human correctness 最高 94.6%、clarity 最高 91.4%。

### 方法优势

1. 将需求缺陷显式分为 vagueness 与 ambiguity，并为 STL formalization 设计具体类别。
2. 检测、询问、用户回答、重检测形成闭环，避免一次性要求用户重写整条需求。
3. Ambiguity Inquirer 用多候选 STL + back-translation 定位歧义，避免直接在符号公式层面让 LLM 做困难比较。
4. 同时评估 transformation accuracy、检测性能、query 质量与人机交互一致性。

### 方法的局限性

- 主要处理 single-sentence requirements，文档级、多需求依赖与跨句上下文是未来工作。
- AmbiEval 基于 DeepSTL/STL-DivEn mutation 构造，虽然避免与 test samples 重叠，但与真实工业 ambiguity 分布仍可能不同。
- 依赖 GPT-4o 与 LLaMA 3-8B，prompt/hyperparameter/provider drift 可能影响稳定性。
- 输出仍是 STL formula，不包含状态机结构；semantic robustness 基于 sampled traces，不等同于完整系统级模型检查。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠（需求澄清 + STL 形式化强近邻；非 exact STM direct baseline）
- **四条件证据**：`LLM4Modeling=🟢`，`NL输入=🟢`，`LLM方法=🟢`，`STM族输出=🟡`。
- **为什么是强近邻**：ClarifySTL 输入是自然语言 CPS requirements，输出 STL formal specifications，处理 temporal intervals、numeric thresholds、conditional logic 等与控制系统状态机 guard/time constraints 高度相关的问题。
- **为什么不是直接 baseline**：它不生成状态机、Statechart、FSM、SysML 状态机或 transition system artifact；STL 是性质/监控公式，不是系统行为模型本体。

### 可借鉴之处

1. Project 1 可在 NL-to-STM 前加入需求缺陷检测：时间模糊、数值阈值缺失、条件逻辑省略、指代歧义、模式范围歧义。
2. Clarification query 应只围绕定位到的缺陷片段，避免 LLM 自行扩写需求。
3. “生成多个候选 formal artifacts -> back-translate -> 比较差异 -> 生成澄清问题”可用于状态机 guard/transition 歧义定位。
4. Re-check loop 可映射为 agent-loop 的 ask-user / repair-review gate。

### 存在的不足与改进空间

- 不能直接替代状态机生成 baseline，因为没有状态/迁移结构输出。
- 交互式流程需要用户参与，和 Project 1 的 fully automatic path 需要区分。
- Zenodo artifact 具体可复现性需人工核验。

### 对本研究的启发

ClarifySTL 强化了一个重要研究判断：很多 formalization 错误不是生成器后处理能完全解决，而是输入需求本身不完整或多义。Project 1 若要提升状态机可靠性，应显式建模“何时需要澄清”，并把澄清记录写入 run record / trace evidence。

## 重要的相关工作

### 1. 重要的前身类工作

- **Maler and Ničković, 2004, Monitoring Temporal Properties of Continuous Signals**：STL 基础。
- **Pnueli, 1977, The Temporal Logic of Programs**：temporal logic 基础。
- **Berry and Kamsties, 2004 / Berry et al., 2003**：requirements ambiguity 研究背景，用于说明自然语言需求歧义的工程风险。

### 2. 直接参与实验的baseline

- **DeepSTL**：首个将 deep learning 用于从 English requirements 到 STL 的代表方法。
- **KGST**：当前 SOTA，先 fine-tune LLM 生成初始 STL，再用 external knowledge/refinement 改善结果。
- **Qwen、LLaMA、DeepSeek-V3、GPT-4o、GPT-4o-mini、Gemini-2.5-Pro、Claude-4-Sonnet**：直接 transformation 或 interactive transformation baselines。

### 3. 提供了重要论证的工作

- **Buzhinsky, 2019, Formalization of Natural Language Requirements into Temporal Logics: A Survey**：自然语言到 temporal logic 形式化综述背景。
- **ARSENAL / Ghosh et al., 2016**：NLP + predefined rules 生成 formal specifications，包括 TL，用于对比规则方法限制。
- **nl2spec / Cosler et al., 2023**：human feedback + LLM 的 temporal logic translation，用于说明交互式 formalization 方向。

### 4. 在技术上提供了支持的工作

- **Triplet Network / Hoffer and Ailon, 2015**：Ambiguity Detector 的 contrastive learning 基础。
- **SimCSE / Xu et al. contrastive learning work**：支撑 sentence representation 与 ambiguity detection。
- **ROUGE、BERTScore、Fleiss' Kappa**：query generation 与人评一致性指标。
- **PyTorch、HuggingFace Transformers、LLaMA-Factory**：实现框架。

### 5. 其他重要工作

- **ClarifyGPT / Mu et al., 2024**：面向 LLM code generation 的 requirements clarification 框架，与 ClarifySTL 的“澄清输入再生成”思想相邻。
- **Dialogue-based NL-to-STL approaches**：原文指出这些方法依赖 LLM 内部知识，难以稳定识别 STL-specific vagueness/ambiguity；ClarifySTL 通过 fine-tuned detectors 与 task-specific prompts 改进。

## 文献分类总结

- **类别**：需求澄清 + 自然语言到 STL；需求形式化强近邻。
- **BASELINE评估**：🟠（强近邻，非 exact STM direct baseline）。
- **输入**：自然语言 CPS/STL requirements + 用户澄清回答。
- **输出**：澄清后的自然语言需求、clarification queries、STL formula。
- **输出模型类型**：Signal Temporal Logic formula，属于验证性质/形式规约，不是 STM-family exact artifact。
- **使用的LLM**：GPT-4o；LLaMA 3-8B detectors/transformers；baselines 包括 Qwen、LLaMA、DeepSeek-V3、Gemini-2.5-Pro、Claude-4-Sonnet 等。
- **主要方法**：vagueness/ambiguity detection + targeted query generation + user clarification loop + NL-to-STL transformation。
