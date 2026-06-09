# 面向 BPMN 模型生成的开放权重语言模型指令微调 / Instruction-Tuning Open-Weight Language Models for BPMN Model Generation

## 基本信息

- **标题**：Instruction-Tuning Open-Weight Language Models for BPMN Model Generation
- **中文标题**：面向 BPMN 模型生成的开放权重语言模型指令微调
- **作者**：Gökberk Çelikmasat、Atay Özgövde、Fatma Başak Aydemir
- **单位**：Boğaziçi University；Utrecht University
- **发表**：arXiv:2512.12063，2025-12-12 预印本
- **DOI**：10.48550/arXiv.2512.12063
- **链接**：[arXiv](https://arxiv.org/abs/2512.12063)；[PDF](https://arxiv.org/pdf/2512.12063)；[Zenodo replication package](https://doi.org/10.5281/zenodo.17776444)

**代码/仓库获取方式**：
- 原文称公开分享 trained models and scripts，并在正文脚注给出 HuggingFace 入口 `https://huggingface.co/gcelikmasat-work`；本次建档时该 HuggingFace 根入口返回 404，需人工核验具体模型路径或可见性。
- 原文参考文献 [49] 给出 Zenodo replication package DOI：`10.5281/zenodo.17776444`；本次 HTTP 头检查可解析到 Zenodo DOI 页面，但未下载核验内部文件。

**数据集获取方式**：
- 训练基于 MaD dataset，原始约 30,000 textual business process descriptions / BPMN DOT pairs；作者清洗后约 26,000 high-quality pairs，并按 80/10/10 划分。
- 评测使用 15 个 business domains 中 stratified sampled 180 descriptions；原文称数据、prompts、results 在 replication package 中。

## 简报

本文解决的问题是：能否通过 instruction tuning 让小型开放权重 LLM 在本地/私有环境中直接从自然语言业务流程描述生成高质量 BPMN process models，从而减少对专有大模型和复杂 prompt scaffolding 的依赖。作者提出 InstruBPM：用 Qwen3-4B 作为 backbone，经 LoRA instruction tuning、merge-time alpha scaling 和 post-training quantization，输出 DOT 形式的 BPMN 模型。

- **输入**：自然语言 business process descriptions，主要来自 MaD dataset 的英文流程描述。
- **方法**：将文本-图对整理为 instruction-output schema；对 Qwen3-4B 做 LoRA/PEFT 指令微调；推理时输出 BPMN model code in DOT；用文本相似度、R-GED、BEBoP guideline checks 和专家评审评估。
- **输出**：DOT language 表示的 BPMN process model，可渲染为 BPMN visualization，并可转换为 BPMN 2.0 XML 做 BEBoP 检查。

```text
输入层：自然语言业务流程描述
  -> 方法层：instruction-tuned Qwen3-4B-InstruBPM + 固定 instruction template + DOT post-processing/validation
  -> 输出层：BPMN process model in DOT / rendered BPMN / guideline diagnostics
```

在 180-instance seed set 上，Qwen3-4B-InstruBPM 达到 BLEU 83.06、ROUGE-L 94.43、METEOR 92.82、R-GED 99.44，超过未调优开放权重模型和 GPT-5.1、Gemini 2.5 Pro、Claude 4.5 Sonnet 等 proprietary baselines。它是 BPMN/process 强近邻，不能标为 exact STM direct baseline。

**可比字段快照**：

- **输入**：自然语言业务流程描述。
- **输出**：BPMN process model code in DOT language；可渲染/转换为 BPMN。
- **输出模型类型**：BPMN process model / graph-structured process model；非 STM 族。
- **使用的 LLM**：Qwen3-4B-InstruBPM 为主；比较 Qwen2.5/3 系列、Gemma2-9B-BPMG-IT、GPT-5.1、Gemini 2.5 Flash/Pro、Claude 4.5 Haiku/Sonnet。
- **主要方法**：MaD 数据清洗 + instruction tuning + LoRA + merge-time alpha sweep + HQQ/GGUF quantization + vLLM serving。
- **需求词工程**：中；调优模型使用固定 instruction template，baselines 使用 assisted zero-shot prompt；CoT/ToT 对 tuned model 提升有限。
- **运行仿真/验证**：无业务执行仿真；有 DOT parseability、Graphviz rendering、R-GED、BEBoP guideline checks。
- **形式化验证**：无 model checking；BEBoP 是 guideline/rule-based conformance，不是 temporal property verification。

## 研究问题与动机

### 问题背景

BPMN 是业务流程建模事实标准，但人工建模耗时且需要专业知识。LLM prompt engineering 可生成模型，但依赖上下文窗口、人工 prompt scaffolding 和专有 API；企业场景还存在隐私和部署成本问题。

### 核心问题

本文核心问题是：instruction-tuned open-weight LLM 是否能在 BPMN generation 上达到或超过专有模型，同时保持 on-prem deployment 的可行性、成本效率和可复现性？

### 研究动机

作者认为 prompt engineering、CoT/ToT、RAG 等方法主要优化上下文，而 instruction tuning 能把 BPMN 结构约束内化到模型参数中。相比持续依赖复杂 prompts，PEFT + quantization 更适合企业私有部署。

### 研究意义

对 LLM4Modeling，本文提供了“领域建模任务 instruction tuning”的直接证据：小型开源模型经过任务数据微调后，在结构化模型生成上可显著超过更大但未适配的模型。这对 Project 1 的 baseline 策略有启发：若状态机训练数据足够，可以比较 prompt-only 和 fine-tuning/adapter 路线。

### 现有方法的局限性

规则/NLP BPMN 生成方法难以泛化；prompt-only LLM 方法成本高且结构错误多；RAG 需要外部基础设施且不直接优化结构化输出；作者 prior BPMG-IT 样本较小、未覆盖 guideline conformance 和 deployment trade-offs。

### 研究目标

本文提出 InstruBPM，并验证两个假设：instruction-tuned open-weight LLM 生成结构更准确；输出在专家视角和 BPMN guideline checks 下可用。

## 核心方法

### 方法概述

InstruBPM 包含四部分：

1. **Dataset preparation**：清洗 MaD text-DOT pairs，过滤 malformed DOT、duplicate/disconnected graphs、明显错字和超长输入。
2. **Instruction tuning**：以 Qwen3-4B 为 backbone，用 LoRA/PEFT 做 supervised fine-tuning。
3. **Inference**：自然语言描述经 fixed instruction template 输入模型，输出 DOT code。
4. **Evaluation**：文本/结构指标、专家评审、BEBoP guideline analysis、quantization/alpha ablations。

### 数据集构建

MaD 原始约 30,000 对文本描述和 BPMN DOT 表示，覆盖 15 个 business domains。清洗后约 26,000 pairs，平均每个 BPMN 12.25 nodes、13.44 edges、4.18 gateways，描述平均 132 words / 7.8 sentences。训练/验证/测试按 80/10/10 划分。

### Instruction tuning pipeline

- backbone：Qwen3-4B-Instruct-2507。
- LoRA：rank 16、alpha 32、dropout 0.05。
- 训练：BF16，1 epoch，约 21.5k instances，2×L40S 48GB，约 150 分钟。
- 输入上限：2048 tokens。
- merge-time alpha sweep：8、16、32、64。
- PTQ variants：HQQ 2/3/4/5/6/8-bit 与 BF16 baseline；服务用 vLLM。

### 推理与 prompt

tuned model 使用训练同款 instruction。untuned baselines 使用 strengthened zero-shot prompt，包含 DOT syntax guidance 和示例；否则 performance 大幅下降。采样参数固定 temperature 0.1、top_p 1.0、max generation length 2048。

### 输出与后处理

模型输出 DOT code；后处理提取代码、去除 Markdown fences、修复重复 braces 和少量 attribute typos，但不改变图结构。DOT 既用于 Graphviz 渲染，也用于 quantitative evaluation。

### 评估方法

- text/code metrics：BLEU、ROUGE-L、METEOR。
- structural fidelity：Relative Graph Edit Distance，报告 0-100 accuracy。
- expert evaluation：4 名 BPM 经验 2-10 年的 practitioners 评估 accuracy、structural correctness、usability、understandability。
- BEBoP guideline checks：DOT -> BPMN XML -> BEBoP verifier，检查 selected rules。
- ablations：prompting strategies、quantization、merge-time alpha。

## 实验与评估

### 数据集

固定评测集为 180 descriptions：15 个 domain，每个 domain 按 node-count 选 4 easy、4 medium、4 hard。用于公平比较 tuned/open/proprietary baselines。

### 主要实验结果

表 2 关键结果：

| 模型 | BLEU | ROUGE-L | METEOR | R-GED |
|---|---:|---:|---:|---:|
| Qwen3-4B-InstruBPM | 83.06 | 94.43 | 92.82 | 99.44 |
| Gemma2-9B-BPMG-IT | 82.98 | 94.61 | 92.67 | 97.78 |
| GPT-5.1 | 12.64 | 48.83 | 59.01 | 40.95 |
| Gemini-2.5-Pro | 28.72 | 48.98 | 63.66 | 43.58 |
| Claude-4.5-Sonnet | 22.56 | 49.87 | 61.37 | 41.47 |

Qwen3-4B-InstruBPM 在 14/15 个 domains 达到 R-GED 100%，唯一 mismatch 是 Process for optimizing a process，R-GED 91.67。

### Prompting 与 tuning

CoT/ToT 对 tuned model 的提升有限，反而 sequence metrics 略低；作者据此认为 instruction tuning 已内化 BPMN planning。未调优模型即便有 syntax scaffolding，仍远低于 tuned model。

### Quantization 与 alpha

Q8/Q6/Q5 保持接近 BF16 的 BLEU/ROUGE/METEOR，并显著降低 model size；Q4 及以下明显退化，Q2 几乎失效。merge alpha 以 16-32 最优，过小欠适配、过大过拟合/过应用 adapter。

### BEBoP 与专家评审

BEBoP 中 model size、hierarchical structure、explicit gateways、split/join consistency、meaningful gateways、message flows、activity labeling、orientation 等规则 pass rates 高；activity descriptions 为 0%，default flows 与 XOR gateway labels 约 44%。专家认为 tuned diagrams 可作为 first drafts，但仍需人工 review，主要问题包括 generic labels、gateway logic refinement、多语言支持和 iterative interaction loop。

### 方法优势

- 证明小型开源模型经过任务微调可在 BPMN 结构生成上大幅超过强 proprietary baselines。
- 提供部署维度：quantization、LoRA alpha、throughput/latency/memory trade-offs。
- 评估维度较完整：文本、结构、guideline、专家。
- 对 privacy/on-prem 场景有现实意义。

### 方法的局限性

- 数据集为 English paraphrases，且合成增强/清洗后可能不代表真实企业文档。
- 输出是 DOT 表示的 BPMN，不是直接 executable BPMN XML；semantic equivalence 仍未完全验证。
- R-GED 受 parsing/tool chain 影响，100% 结构匹配不等于业务语义完全正确。
- 没有 multilingual instruction tuning。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：`🟠`。**

四条件建议如下：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 核心任务是 LLM 生成 BPMN 建模工件。 |
| NL输入 | 🟢 | 输入为自然语言业务流程描述。 |
| LLM方法 | 🟢 | Qwen3-4B instruction tuning 是核心方法。 |
| STM族输出 | 🟡 | BPMN process model 是行为/process 强近邻，不是 STM-family。 |

它不能评为 `🟢` direct STM baseline：输出为 BPMN/DOT process model，不含 state/event/transition/guard/action 的 STM 结构目标。它应作为 fine-tuning for model generation 的强近邻。

### 研究定位与差异化

与 Project 1 的共同点是“自然语言 -> 结构化行为模型”的 LLM 建模任务；差异是目标模型为 BPMN 而非状态机，且实验数据为业务流程而非控制系统需求。

### 可借鉴之处

- **instruction tuning vs prompt-only baseline**：Project 1 可在状态机数据上比较开源模型微调和强专有模型 prompt。
- **结构指标优先**：R-GED 类似状态机图结构相似度，但需加上语义/guard/action 维度。
- **guideline diagnostics**：BEBoP 类似 STM reviewer rules，可用于模型质量分类。
- **deployment trade-offs**：量化和 LoRA alpha 对研究成本有参考价值。

### 存在的不足与改进空间

- 没有形式化验证或仿真闭环。
- 没有控制系统/安全关键 case。
- 数据集和输出不覆盖 STM 时间约束、层次状态、并发区域。
- HF 入口当前需人工核验可访问性。

### 对本研究的启发

若 Project 1 后续积累足够 state machine corpus，可尝试 Qwen/DeepSeek/Llama open-weight instruction tuning，并使用 pyfcstm parse/semantic metrics、graph edit distance、review rubric 与专家/LLM judge 共同评估。本文也提醒：高结构相似度不等于语义正确，必须补充 executable semantics 或 verification profiles。

## 重要的相关工作

### 1. 重要的前身类工作

- Sonbol 等 machine-translation-like BPMN generation：早期文本到 BPMN 机器翻译路线。
- Friedrich、Honkisz、Van der Aa 等 rule/NLP process extraction 工作：提供自动 BPMN 生成前史。

### 2. 直接参与实验的baseline

- Qwen2.5/Qwen3 open-weight baselines。
- Gemma2-9B-BPMG-IT prior tuned model。
- GPT-5.1、Gemini 2.5 Flash/Pro、Claude 4.5 Haiku/Sonnet proprietary baselines。

### 3. 提供了重要论证的工作

- Licardo、Nivon/Salaün、Kourani/ProMoAI、BPMN Assistant 等 LLM BPMN/process modeling 工作。
- Prompt engineering、CoT、ToT、RAG、instruction tuning、PEFT/LoRA 文献。

### 4. 在技术上提供了支持的工作

- Qwen technical report；LoRA/PEFT；HQQ/bitsandbytes quantization；vLLM；Graphviz；Pydot；NetworkX；BEBoP。

### 5. 其他重要工作

- MODRE sequence diagram generation、DiagrammerGPT、MatPlotAgent 等通用图/模型生成工作为 structured output 设计提供背景。

## 文献分类总结

本文是开放权重 LLM 指令微调生成 BPMN 的强近邻。它对 Project 1 的 baseline 体系价值在于 fine-tuning methodology、部署成本评估和结构化模型指标，不是 STM exact baseline。建议标记为 `🟠` BPMN/process 强近邻，四条件为 `🟢/🟢/🟢/🟡`。
