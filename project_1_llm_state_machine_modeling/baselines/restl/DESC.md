# RESTL：多方面奖励强化学习引导的 STL 转换 / RESTL

## 基本信息

- **标题**：RESTL: Reinforcement Learning Guided by Multi-Aspect Rewards for Signal Temporal Logic Transformation
- **中文标题**：RESTL：多方面奖励强化学习引导的信号时序逻辑转换
- **作者**：Yue Fang, Zhi Jin, Jie An, Hongshen Chen, Xiaohong Chen, Naijun Zhan
- **单位**：Peking University；Key Laboratory of High Confidence Software Technologies；Institute of Software, Chinese Academy of Sciences；JD.com；East China Normal University
- **发表**：arXiv preprint, 2025-11-11；PDF 页脚含 AAAI 2026 copyright 字样，正式录用/出版信息待人工核验
- **年份**：2025
- **DOI**：10.48550/arXiv.2511.08555
- **链接**：https://arxiv.org/abs/2511.08555

**代码/仓库获取方式**：
- 原文未提供公开代码/仓库获取链接。
- 实验实现细节充分说明了 LLaMA 3-8B、reward models、PPO steps、GPU 设置与超参数，但不能替代可运行 artifact。

**数据集获取方式**：
- 原文使用 DeepSTL 和 STL-DivEn 两个 NL-to-STL 数据集；正文未给出直接下载链接。
- 每个数据集随机选择 14,000 samples 用于训练、2,000 samples 用于测试。
- DeepSTL 是 grammar/template synthetic dataset；STL-DivEn 是 GPT-4-based generation + human verification 的混合构造数据集。

## 简报

本文解决的是自然语言 CPS requirements 到 Signal Temporal Logic (STL) 公式的自动转换问题。它指出 supervised fine-tuning 只用 paired NL-STL 数据，缺少细粒度语义/可读性反馈，容易产生 atomic proposition、temporal operator、threshold/value 和 redundancy 错误。因此提出 RESTL：先 fine-tune LLaMA 3-8B 得到初始 STL generator，再训练四个 reward models，以 PPO 强化学习优化生成器。

- **输入**：自然语言 CPS/STL requirement description。
- **方法**：LLaMA 3-8B SFT 初始化 STL generator；基于候选公式构造 preference pairs；分别训练 atomic proposition alignment、templated NL similarity、formula succinctness、STL-level similarity reward models；聚合 reward 后用 PPO 优化 generator。
- **输出**：Signal Temporal Logic formula。

```text
自然语言 CPS requirement
  -> SFT LLaMA 3-8B STL generator
  -> 多候选 STL formulas
  -> 4 个 curriculum-trained reward models
  -> 聚合 reward + KL penalty
  -> PPO 优化后的 STL generator
  -> 更准确/简洁的 STL formula
```

实验在 DeepSTL 与 STL-DivEn 上显示 RESTL 优于 DeepSTL、GPT-3.5、GPT-4、DeepSeek、KGST 等 baseline。STL-DivEn 上 Formula Accuracy 68.38%、Template Accuracy 69.74%、BLEU 0.3347；DeepSTL 上 Formula Accuracy 59.85%、Template Accuracy 63.27%、BLEU 0.6783。

## 研究问题与动机

### 问题背景

STL 能描述 cyber-physical systems 的 dense-time、real-valued signal requirements，广泛用于 CPS model checking 与 runtime monitoring。但 CPS 文档中的 timing constraints 往往以自然语言书写，人工写 STL 既费时又需要专家。

### 核心问题

论文关注：在已经能通过 SFT 学到基本 NL-to-STL 映射的前提下，如何进一步降低以下错误：

1. atomic proposition 错误或遗漏；
2. temporal semantics 与 operator 误解；
3. numerical threshold / value 错误；
4. 公式冗余、过长、可读性差。

### 研究动机

现有 rule/pattern 方法依赖人工模板，不易泛化；SFT LLM 方法虽有进步，但目标函数只看 paired sequence likelihood，不能直接告诉模型公式是否语义对齐、AP 是否正确、公式是否简洁。因此作者引入多 reward models，把细粒度评价转为强化学习信号。

### 研究意义

对 Project 1，RESTL 的价值不在于状态机输出，而在于证明“formal artifact generation 需要多维 reward/gate”。状态机生成也会遇到类似问题：元素覆盖、guard/action 语义、结构简洁性、与需求一致性可能需要独立 reward/reviewer，而不是一个总分。

## 核心方法

### 方法概述

RESTL pipeline 包含三步：

1. **STL Generator Initialization**：用 NL-STL pairs fine-tune LLaMA 3-8B，得到初始 generator。
2. **Reward Model Training**：对每个 reward metric 训练单独 LLaMA 3-8B-based reward model，并用 curriculum learning 从易到难排序训练样本。
3. **Reinforcement Learning**：将四个 reward models 输出聚合为统一标量，用 PPO 和 KL penalty 优化 STL generator。

### 四类 reward metrics

1. **Atomic Proposition Alignment**：用 LLM 抽取 generated formula 和 ground truth 的 AP 集合，计算 ground truth AP 被覆盖的比例。
2. **Templated NL Similarity**：把 generated STL 反向映射为 templated natural language，用 encoder 计算与原始输入的语义相似度。
3. **Formula Succinctness**：根据 generated formula 与 reference 长度差奖励接近参考长度的公式，减少冗余或遗漏。
4. **STL-level Similarity**：用 ROUGE-L 衡量 generated STL 与 ground truth 的结构/序列相似度。

论文把这些 metric 对应为独立 reward models，而不是直接把启发式分数用于最终评价。Reward models 基于 candidate formulas 之间的 preference pairs 训练。

### Curriculum learning

每个 reward model 使用不同 difficulty 排序：

- AP reward 按 ground-truth AP 数从少到多。
- NL similarity reward 按候选 STL back-translation 与原始 NL 的平均相似度难度排序。
- Formula length reward 按 formula length 从短到长。
- STL similarity reward 按候选与 ground truth 的 ROUGE-L 平均得分定义难度。

### PPO 优化

总 reward 是四个 reward model 的加权和，权重为 `λ1=0.2`、`λ2=0.25`、`λ3=0.35`、`λ4=0.2`，并加入 KL penalty 稳定训练，避免偏离初始 SFT policy。论文使用 PPO 训练 80,000 steps。

### LLM 设置

- Initial generator 与 reward models 均基于 LLaMA 3-8B。
- Baselines 包括 GPT-3.5、GPT-4、DeepSeek、KGST、DeepSTL。
- 原文具体采用 `gpt-4-0125-preview`、`gpt-3.5-turbo-1106` 和 `DeepSeek-V1`。

## 实验与评估

### 数据集

- **DeepSTL**：grammar-based generator 从 predefined templates 和 operator distributions 采样 STL formulas 并生成 NL。
- **STL-DivEn**：结合 GPT-4-based generation 与 human verification 构造。
- **规模**：每个数据集随机取 14,000 train / 2,000 test。

### 评估指标

- Formula Accuracy。
- Template Accuracy。
- BLEU。
- Human evaluation：从两个测试集各随机抽取 NL-STL pairs，5 名熟悉 STL 的 annotators 盲评 readability、syntactic correctness、semantic consistency，RESTL 与 baseline 比较标为 win/loss/tie。
- Error analysis：AP、operator、value、redundancy 四类错误计数。

### 主要实验结果

- **STL-DivEn**：RESTL 达到 Formula Acc. 0.6838、Template Acc. 0.6974、BLEU 0.3347；最强 baseline KGST 为 0.5587、0.5627、0.2142。
- **DeepSTL**：RESTL 达到 Formula Acc. 0.5985、Template Acc. 0.6327、BLEU 0.6783；KGST 为 0.4538、0.4939、0.5686。
- **Human evaluation**：RESTL 相对 DeepSeek/GPT-4/KGST 在 STL-DivEn 上 win rates 分别为 64.2%、61.0%、58.7%；DeepSTL 上分别为 56.3%、54.7%、52.8%。
- **Ablation**：移除任一 reward 都下降；移除 STL-level similarity reward 影响最大，formula succinctness reward 对自动指标影响较小但提升可读性。
- **Error analysis**：RESTL 的 AP/operator/value/redundancy 错误数低于 fine-tuned LLaMA3-8B 与 KGST。

### 方法优势

1. 将 formal formula generation 的错误拆成多个可训练 reward 维度。
2. 通过 back-translation 到 templated NL 检查语义对齐，避免只看公式 token overlap。
3. PPO + KL penalty 让模型在保持原始生成能力的同时优化 reward。
4. 同时提供自动指标、人评、消融和错误分析。

### 方法的局限性

- 原文未给出公开代码/仓库链接。
- DeepSTL 与 STL-DivEn 虽是代表 benchmark，但与真实工业 CPS 文档仍可能有差距。
- 输出是 STL 公式，不含系统状态、事件、迁移结构。
- 评估指标仍主要依赖 token/template similarity 与人工抽样，不等同于在真实控制模型上的 model checking 完整闭环。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠（STL 需求形式化强近邻；非 exact STM direct baseline）
- **四条件证据**：`LLM4Modeling=🟢`，`NL输入=🟢`，`LLM方法=🟢`，`STM族输出=🟡`。
- **为什么是强近邻**：STL 是 CPS/控制系统行为性质语言，直接关联 runtime monitoring、model checking 和 temporal constraints；自然语言需求到 STL 与 Project 1 的时序/安全约束抽取高度相邻。
- **为什么不是直接 baseline**：RESTL 输出 STL formula，而非状态机族模型；它生成性质/规格，不生成状态、事件、guard/action 或 transition relation。

### 可借鉴之处

1. Project 1 可把 STM 质量拆成多 reward：状态/事件/AP 覆盖、guard/action 语义、结构简洁性、仿真 trace 一致性。
2. Back-translation 思路可用于把生成的状态机迁移/guard 反译为自然语言，再与原需求比对。
3. Curriculum reward model training 可启发从简单需求到复杂嵌套需求逐步训练 LLM-as-Judge 或 repair reviewer。
4. Human evaluation 维度可借鉴为 readability / syntactic correctness / semantic consistency。

### 存在的不足与改进空间

- 没有把 STL 进一步编译为状态机或监控自动机，因此不能直接作为 NL-to-STM baseline。
- 需要大量 NL-STL pairs 与训练资源，不适合作为轻量 prompt baseline。
- 数据和代码可获取性不足会影响 Project 1 复现实验。

### 对本研究的启发

RESTL 支持一个重要设计方向：对形式工件生成，单一 exact match 或 parser pass 不足以指导模型。Project 1 的状态机生成可以采用“多维 reward + verifier/reviewer feedback”的评价与修复机制。

## 重要的相关工作

### 1. 重要的前身类工作

- **Maler and Ničković, 2004, Signal Temporal Logic**：STL 理论来源，定义 dense-time real-valued signals 上的 temporal specification。
- **Pnueli, 1977, Temporal Logic of Programs**：TL/LTL 基础。
- **Lignos et al., 2015 / Ghosh et al., 2016 / Kulkarni et al., 2013**：rule-based 或 pattern-based NL-to-temporal-logic/STL 早期路线，用于说明模板方法依赖专家规则。

### 2. 直接参与实验的baseline

- **DeepSTL**：grammar-guided synthetic data + Transformer 的 NL-to-STL baseline。
- **GPT-3.5 / GPT-4 / DeepSeek**：直接 LLM baseline。
- **KGST**：SOTA 两阶段方法，先 fine-tune LLaMA 3-8B 生成初始 STL，再检索相似 NL-STL pairs 并用 GPT-4 refine。
- **Fine-tuned LLaMA3-8B**：作为 SFT 初始 generator 与消融参照。

### 3. 提供了重要论证的工作

- CPS model checking / runtime monitoring 相关文献，如 Maierhofer et al.、Tellex et al.，用于说明 STL 在 CPS 分析中的价值。
- Supervised fine-tuning 与 RLHF/PPO 相关工作，用于说明为什么 reward-based optimization 可改进 SFT。

### 4. 在技术上提供了支持的工作

- **Bradley-Terry model**：用于 preference pair reward model training。
- **PPO / Schulman et al., 2017**：用于优化 STL generator。
- **ROUGE-L / BLEU / BERT-style encoders**：用于 reward 或评价指标。

### 5. 其他重要工作

- 原文还引用 NL2TL、KGST、DeepSeek 等 LLM/formal translation 工作，形成从 rule-based、SFT、RAG/refinement 到 reward-guided RL 的研究链条。

## 文献分类总结

- **类别**：自然语言到 STL；需求形式化强近邻。
- **BASELINE评估**：🟠（强近邻，非 exact STM direct baseline）。
- **输入**：自然语言 CPS/STL requirements。
- **输出**：Signal Temporal Logic formulas。
- **输出模型类型**：STL temporal logic formula，属于验证性质/形式规约，不是 STM-family exact artifact。
- **使用的LLM**：LLaMA 3-8B generator/reward models；baselines 包括 GPT-3.5、GPT-4、DeepSeek、KGST。
- **主要方法**：SFT 初始化 + multi-aspect reward model + curriculum learning + PPO 强化学习。
