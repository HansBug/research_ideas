# LLM 模型现状总账

> 核验日期：2026-06-04。价格默认是 **USD / 1M tokens**，除非单元格明确说明。模型可用性、上下文窗口、最大输出、官方价格、preview/stable/retired 状态、折扣和区域可用性会变化；正式实验必须记录精确 `model_id`、provider、region、调用日期和官方链接。

## 1. 文库整体概况

| 项 | 当前状态 |
|---|---:|
| 当前维护文件数 | 3 |
| 模型/模型族表格数 | 6 |
| `project_1/baselines` LLM 相关条目数 | 34 |
| hosted/frontier API 条目数 | 28 |
| Qwen 专项条目数 | 8 |
| Llama 专项条目数 | 6 |
| Grok 专项条目数 | 7 |
| 其他开源/开放权重系列条目数 | 13 |
| 本轮新增数量 | 1 个微型文库 |
| 尚待复查项 | Gemini 3.x/3.5 精确 ID、Kimi K2.x、部分云厂商价格、Qwen3.7 国内/国际价差 |

## 2. 检索关键词簇分析

### 2.1 当前推荐关键词簇

1. `site:provider-docs model pricing context output tokens model id`。
2. `site:huggingface.co/<org> <model-family> context length model card`。
3. `site:github.com/<official-org> <model-family> release tech report`。
4. `project_1 baselines paper_content GPT Claude Gemini Qwen Llama DeepSeek Grok`。
5. `model lifecycle retired alias preview stable pricing`。

### 2.2 高命中特征

1. Provider 官方模型页通常最适合核验 context、output、tool/vision/structured-output 能力。
2. Pricing 页通常最适合核验 hosted API 价格，但要注意折扣、长上下文加价和 cache 价格。
3. Hugging Face 官方 org 的 model card 最适合核验开放权重发布时间、上下文与许可证。
4. Release notes 最适合发现 alias、retired、reroute、preview -> stable 等状态变化。
5. baseline 文献模型提及最好回到 `paper_content.txt` 与 `bibtex.bib` 双核验。

### 2.3 低命中特征

1. 只搜模型家族名容易混入第三方托管、社区量化和非官方镜像。
2. 只看博客标题容易漏掉 pricing、max output、region-specific 限制。
3. 只看 issue/PR comment 容易保留过期价格或 preview 状态。
4. “最新模型”这类关键词容易命中营销页，不一定有可复现实验 model ID。
5. 开放权重模型的第三方 API 价格不能当作模型官方价格。

### 2.4 检索倾向调整

1. 每轮先查 provider 官方 docs/pricing，再查 HF/GitHub 官方 org。
2. 对 Qwen、DeepSeek、GLM、Kimi 等中英文双入口模型，要同时查英文/中文官方文档。
3. 对 Grok、Gemini、DeepSeek 这类 alias/preview 变化快的模型，必须查 release notes 或 lifecycle。
4. 对开放权重模型，重点记录 checkpoint、context、license，不强行写统一 token 价。
5. 对 hosted API，必须记录价格单位、cache 价、长上下文加价和折扣状态。

---

## 3. `project_1/baselines` 文献模型清单（按 year 降序）

> 证据链接固定到当前 commit：`1af5d0a597cd076fb85b918b99ecd0bca3fe80e7`。`paper` 用于核验模型提及，`bibtex` 用于核验年份与出版信息。该表仅列出本轮识别到的 LLM / foundation-model 相关 baseline；传统非 LLM 需求工程/状态机合成论文未强行列入模型清单。

| Year | baseline 目录 | 简短标题 | 文献中出现/提到的模型 | 可核验出处 |
|---:|---|---|---|---|
| 2026 | `class-model-generation-from-requirements-llm` | Class Model Generation from Requirements | GPT-5；Claude Sonnet 4；Gemini 2.5 Flash Thinking；Llama-3.1-8B；Grok；Mistral Small 3.1 24B | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/class-model-generation-from-requirements-llm/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/class-model-generation-from-requirements-llm/bibtex.bib) |
| 2026 | `LLM-FSM` | LLM-FSM / RTL FSM reasoning | Llama4 Scout/Maverick；Qwen3；GPT-5/nano/mini；gpt-oss；DeepSeek-R1/V3.1；Gemini-2.5；Grok；Claude-4.5 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/LLM-FSM/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/LLM-FSM/bibtex.bib) |
| 2026 | `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | Structure/Event-Driven SM Modeling | GPT-4o；Claude 3.5 Sonnet | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/bibtex.bib) |
| 2026 | `workflow-level-design-principles-trustworthy-genai-automotive` | Trustworthy GenAI Workflow for Automotive SE | Qwen3:32B；Nemotron3:30B；GPT-OSS:20B/120B | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/workflow-level-design-principles-trustworthy-genai-automotive/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/workflow-level-design-principles-trustworthy-genai-automotive/bibtex.bib) |
| 2025 | `behavioral-augmentation-uml-class-diagrams` | Behavioral Augmentation UML Class Diagrams | Claude 3.7；Qwen 3；ChatGPT-o3；Gemini 2.5 Pro；DeepSeek R1；Mistral/Mixtral；Grok 3；GPT-4o；Llama 4 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/behavioral-augmentation-uml-class-diagrams/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/behavioral-augmentation-uml-class-diagrams/bibtex.bib) |
| 2025 | `fsm-gen-iec-61499` | LLM iterative FSM refinement + IEC 61499 | LLM 未指定具体型号 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/fsm-gen-iec-61499/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/fsm-gen-iec-61499/bibtex.bib) |
| 2025 | `generating-software-architecture-description-source-code-llm` | SAD from Source Code via RE + LLM | GPT-4o；DeepSeek；Phi-4；ChatGPT；Gemini | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/generating-software-architecture-description-source-code-llm/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/generating-software-architecture-description-source-code-llm/bibtex.bib) |
| 2025 | `I4.0` | I4.0 State Machine Diagram Recognition | gpt-4o-2024-08-06；Claude-3-Sonnet；Llama-3.2-11B-Vision | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/I4.0/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/I4.0/bibtex.bib) |
| 2025 | `inference-time-intervention-requirement-verification` | Requirement Verification | Llama-3.1-8B；Claude 3.5 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/inference-time-intervention-requirement-verification/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/inference-time-intervention-requirement-verification/bibtex.bib) |
| 2025 | `leveraging-llms-for-use-case-model-generation` | Use Case Model Generation | Llama 3.1 70B | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/leveraging-llms-for-use-case-model-generation/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/leveraging-llms-for-use-case-model-generation/bibtex.bib) |
| 2025 | `llm-assisted-semantic-alignment-sysml-v2` | SysML v2 Semantic Alignment | ChatGPT-based assistant；GPT-4o | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/llm-assisted-semantic-alignment-sysml-v2/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/llm-assisted-semantic-alignment-sysml-v2/bibtex.bib) |
| 2025 | `llms_emp` | SysML Behavior Models via LLMs | GPT-4/4o；Kimi；Claude 3 Haiku；Llama 3.1；DeepSeek-v3 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/llms_emp/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/llms_emp/bibtex.bib) |
| 2025 | `mcet` | MCeT | GPT-4o-mini；GPT-4o；DeepSeek-v3；DeepSeek-R1 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/mcet/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/mcet/bibtex.bib) |
| 2025 | `mermaidseqbench` | MermaidSeqBench | Qwen 2.5；Llama 3.1/3.2；Granite 3.3；DeepSeek-V3；GPT-OSS；Mistral Large | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/mermaidseqbench/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/mermaidseqbench/bibtex.bib) |
| 2025 | `nomad-uml-class-diagram-generation` | NOMAD | GPT-4o；DeepSeek-V3 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/nomad-uml-class-diagram-generation/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/nomad-uml-class-diagram-generation/bibtex.bib) |
| 2025 | `pushing-the-generative-envelope-mbse-artifacts` | MBSE artifacts | Mixtral-8x7B-Instruct；Llama-3-Smaug-8B；ChatGPT-4/GPT-3.5 背景 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/pushing-the-generative-envelope-mbse-artifacts/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/pushing-the-generative-envelope-mbse-artifacts/bibtex.bib) |
| 2025 | `req` | Automated Statechart Generation | GPT-3.5-turbo；GPT-4；GPT-4o；Azure OpenAI / AI Foundry | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/req/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/req/bibtex.bib) |
| 2025 | `spec2control` | Spec2Control | GPT-5；OpenAI LLM on Azure AI Foundry | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/spec2control/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/spec2control/bibtex.bib) |
| 2025 | `STPA` | FSM refinement with STPA | OpenAI GPT models；ChatGPT 背景 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/STPA/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/STPA/bibtex.bib) |
| 2025 | `sysmbench-system-model-generation-benchmark` | SysMBench | GPT-4.1；Claude 3 Opus；DeepSeek R1；Mistral/Codestral；Qwen3；Gemma2；Llama；InternLM；Baichuan；ChatGLM | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/sysmbench-system-model-generation-benchmark/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/sysmbench-system-model-generation-benchmark/bibtex.bib) |
| 2025 | `text-to-model-via-sysml` | Text-to-model via SysML | Llama 3.1-8B；Llama 3.2-3B；GPT-4o；GitHub Copilot/GPT-4o | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/text-to-model-via-sysml/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/text-to-model-via-sysml/bibtex.bib) |
| 2025 | `umple` | Llama3 for Umple | Llama 3 / Llama 3 8B；Nomic embedding；GPT-3/4 背景 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/umple/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/umple/bibtex.bib) |
| 2024 | `enhance` | FSM Design Automation | Claude 3 Opus；ChatGPT-4；ChatGPT-4o | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/enhance/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/enhance/bibtex.bib) |
| 2024 | `from-image-to-uml` | Image to UML | GPT-4V；Gemini Pro/Ultra；CogVLM；OpenAI API | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/from-image-to-uml/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/from-image-to-uml/bibtex.bib) |
| 2024 | `from-requirements-to-architecture` | Requirements to Architecture | LLaMA2 70B；GPT-3.5；LLaMA/Falcon/Yi；latest GPT | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/from-requirements-to-architecture/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/from-requirements-to-architecture/bibtex.bib) |
| 2024 | `how-llms-aid-uml-modeling` | UML Modeling | ChatGPT | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/how-llms-aid-uml-modeling/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/how-llms-aid-uml-modeling/bibtex.bib) |
| 2024 | `MIG` | Domain Modeling | GPT-4；OpenAI | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/MIG/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/MIG/bibtex.bib) |
| 2024 | `requirements-to-uml-sequence-diagrams` | Requirements to Sequence Diagrams | ChatGPT / GPT-3.5 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/requirements-to-uml-sequence-diagrams/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/requirements-to-uml-sequence-diagrams/bibtex.bib) |
| 2024 | `safety` | State Diagram Extension | ChatGPT；LLaMA；QWEN；Qwen2-72B-Instruct LoRA | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/safety/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/safety/bibtex.bib) |
| 2024 | `ttool-ai` | TTool-AI | OpenAI GPT；ChatGPT；gpt-3.5-turbo；gpt-3.5-turbo-16k-0613 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/ttool-ai/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/ttool-ai/bibtex.bib) |
| 2023 | `chatgpt-uml-assessment` | ChatGPT and UML | ChatGPT；OpenAI；Copilot；Codex；GPT-3 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/chatgpt-uml-assessment/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/chatgpt-uml-assessment/bibtex.bib) |
| 2023 | `few-shot-model-completion` | Few-shot Model Completion | GPT-3；text-davinci-002 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/few-shot-model-completion/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/few-shot-model-completion/bibtex.bib) |
| 2023 | `gpt4-goal-models` | GPT-4 Goal Models | GPT-4 API；ChatGPT web/GPT-4 | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/gpt4-goal-models/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/gpt4-goal-models/bibtex.bib) |
| 2022 | `tech-report-neural-language-models-few-shot-mdse` | Neural LMs + Few-shot MDSE | GPT-J-6B；GPT-3；GPT-Neo | [paper](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/tech-report-neural-language-models-few-shot-mdse/paper_content.txt) / [bibtex](https://github.com/HansBug/research_ideas/blob/1af5d0a597cd076fb85b918b99ecd0bca3fe80e7/project_1_llm_state_machine_modeling/baselines/tech-report-neural-language-models-few-shot-mdse/bibtex.bib) |

---

## 4. Hosted / frontier API 模型规格与官方价格（按发布时间降序）

| 发布时间/排序键 | Provider/系列 | 代表 model ID | 状态 | context / max output | 输入 / cached / 输出价 | 来源 |
|---:|---|---|---|---:|---:|---|
| 2026-current | xAI Grok | `grok-4.3` | 当前 docs-visible latest；首发日待精确核验 | 1M / 按模型页 | 1.25 / 0.20 / 2.50 | [model](https://docs.x.ai/developers/models/grok-4.3) / [pricing](https://docs.x.ai/developers/pricing) |
| 2026-06-01 | Alibaba/Qwen Cloud | `qwen3.7-plus` | hosted API | 1M；Max Input 991.80K；Max Output 65.53K | list 0.4 / 0.08 implicit cache / 1.6；页面显示 20% off 后 0.32/0.064/1.28 | [Qwen3.7-Plus](https://www.qwencloud.com/models/qwen3.7-plus) |
| 2026-05-28 | Anthropic Claude | Claude Opus 4.8 | 当前 Opus | 1M / 官方未统一列 output | 5 / 0.5 read / 25；cache write 6.25/10 | [news](https://www.anthropic.com/news/claude-opus-4-8) / [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| 2026-05-21 | Alibaba/Qwen Cloud | `qwen3.7-max` | hosted API | 1M；Max Input 991.80K；Max Output 65.53K | list 2.5 / 0.5 implicit cache / 7.5；页面显示 50% off 后 1.25/0.25/3.75 | [Qwen3.7-Max](https://www.qwencloud.com/models/qwen3.7-max) |
| 2026-05-19 | Google Gemini | Gemini 3.5 Flash / Gemini 3.5 Nano Banana | 官方 models 页 current 新线 | 按精确 ID 查；多为 1M 级 | 按 Gemini pricing 当前页 | [models](https://ai.google.dev/gemini-api/docs/models) / [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| 2026-04-24 | DeepSeek | `deepseek-v4-pro` | V4 Preview hosted API | 1M / 384K | cache hit 0.003625；miss 0.435；output 0.87 | [release](https://api-docs.deepseek.com/news/news260424) / [pricing](https://api-docs.deepseek.com/quick_start/pricing/) |
| 2026-04-24 | DeepSeek | `deepseek-v4-flash` | V4 Preview hosted API | 1M / 384K | cache hit 0.0028；miss 0.14；output 0.28 | [release](https://api-docs.deepseek.com/news/news260424) / [pricing](https://api-docs.deepseek.com/quick_start/pricing/) |
| 2026-04-23 | OpenAI GPT | `gpt-5.5` | 当前 GPT 强线 | 1,050K / 128K | 5 / 0.5 / 30；长上下文价另列 | [model](https://developers.openai.com/api/docs/models/gpt-5.5) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2026-04-16 | Anthropic Claude | Claude Opus 4.7 | 旧 Opus 线 | 1M / 官方未统一列 output | 同 Opus 4.8 | [news](https://www.anthropic.com/news/claude-opus-4-7) / [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| 2026-03-17 | OpenAI GPT | `gpt-5.4-mini` | 低价 GPT-5.4 线 | 400K / 128K | 0.75 / 0.075 / 4.5 | [model](https://developers.openai.com/api/docs/models/gpt-5.4-mini) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2026-03-10 | xAI Grok | `grok-4.20-0309-*` / multi-agent | API 新线 | 1M / 按模型页 | 1.25 / 0.20 / 2.50 | [release notes](https://docs.x.ai/developers/release-notes) / [4.20](https://docs.x.ai/developers/models/grok-4.20) / [pricing](https://docs.x.ai/developers/pricing) |
| 2026-03-05 | OpenAI GPT | `gpt-5.4` | GPT-5.4 线 | 1,050K / 128K | 2.5 / 0.25 / 15；长上下文价另列 | [model](https://developers.openai.com/api/docs/models/gpt-5.4) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2026-02-17 | Anthropic Claude | Claude Sonnet 4.6 | 当前 Sonnet | 1M / 官方未统一列 output | 3 / 0.3 read / 15；cache write 3.75/6 | [news](https://www.anthropic.com/news/claude-sonnet-4-6) / [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| 2026-02-05 | Anthropic Claude | Claude Opus 4.6 | 旧 Opus 线 | 1M / 官方未统一列 output | 同 Opus 4.8 | [news](https://www.anthropic.com/news/claude-opus-4-6) / [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| 2026-02-05 | OpenAI Codex | `gpt-5.3-codex` | Codex 专项 | 400K / 128K | 1.75 / 0.175 / 14 | [model](https://developers.openai.com/api/docs/models/gpt-5.3-codex) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2025-12-17 | Google Gemini | Gemini 3 Flash | preview/较新线 | 1,048K / 65K 级 | 按 Gemini 3 pricing | [Gemini 3](https://ai.google.dev/gemini-api/docs/gemini-3) / [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| 2025-11-24 | Anthropic Claude | Claude Opus 4.5 | older Opus | 200K / 官方未统一列 output | 5 / 0.5 read / 25 | [news](https://www.anthropic.com/news/claude-opus-4-5) / [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| 2025-11-18 | Google Gemini | Gemini 3 Pro | preview/较新线 | 1,048K / 65K 级 | 按 Gemini 3 pricing | [Gemini 3](https://ai.google.dev/gemini-api/docs/gemini-3) / [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| 2025-11-13 | OpenAI GPT | `gpt-5.1` | GPT-5.1 线 | 400K / 128K | 1.25 / 0.125 / 10 | [model](https://developers.openai.com/api/docs/models/gpt-5.1) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2025-10-15 | Anthropic Claude | Claude Haiku 4.5 | 低价 Claude | 200K / 官方未统一列 output | 1 / 0.1 read / 5 | [news](https://www.anthropic.com/news/claude-haiku-4-5) / [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| 2025-09-29 | Anthropic Claude | Claude Sonnet 4.5 | older Sonnet | 200K / 官方未统一列 output | 3 / 0.3 read / 15 | [news](https://www.anthropic.com/news/claude-sonnet-4-5) / [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| 2025-08 | OpenAI GPT | GPT-5 / GPT-5-mini / GPT-5-nano | GPT-5 历史线 | 400K / 128K | GPT-5 1.25/0.125/10；mini/nano 更低 | [models](https://developers.openai.com/api/docs/models) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2025-06-17 | Google Gemini | Gemini 2.5 Pro / Flash / Flash-Lite | GA/常用线 | 1,048K / 65K 级 | Pro/Flash/Flash-Lite 按 current pricing | [models](https://ai.google.dev/gemini-api/docs/models) / [pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| 2025-04-14 | OpenAI GPT | GPT-4.1 / o3 / o4-mini | GPT-4.1 与 reasoning 线 | 1,047K/32K；o3/o4 200K/100K | GPT-4.1 2/0.5/8；o3 2/0.5/8；o4-mini 1.1/0.275/4.4 | [models](https://developers.openai.com/api/docs/models) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2024-07-18 | OpenAI GPT | GPT-4o-mini | baseline 高频低价历史线 | 128K / 16K | 0.15 / 0.075 / 0.6 | [model](https://developers.openai.com/api/docs/models/gpt-4o-mini) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2024-05-13 | OpenAI GPT | GPT-4o | baseline 高频历史线 | 128K / 16K | 2.5 / 1.25 / 10 | [model](https://developers.openai.com/api/docs/models/gpt-4o) / [pricing](https://developers.openai.com/api/docs/pricing) |
| 2024-02 | Google Gemini | Gemini 1.5 / 1.0 | historical/retired 风险 | 1M-2M 级历史长上下文 | 旧 Vertex 计价 | [lifecycle](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions) / [pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| 2023-03 | OpenAI GPT | GPT-4 / GPT-4 Turbo / GPT-3.5 Turbo | legacy/historical | 8K-128K 历史线 | legacy 价；不建议新 baseline | [models](https://developers.openai.com/api/docs/models) / [deprecations](https://developers.openai.com/api/docs/deprecations) |

---

## 5. Qwen 系列专项表（按发布时间降序）

本轮核验结论：Hugging Face `Qwen` 官方 org 中未找到 `Qwen3.7` 开放权重模型；但 Qwen Cloud 侧已有 `qwen3.7-max` 与 `qwen3.7-plus` hosted API。因此实验记录要区分“开放权重 Qwen”与“Qwen 官方 hosted API”。

| 发布时间/排序键 | 系列 | 代表模型 | context / max output | 价格口径 | 来源 |
|---:|---|---|---:|---|---|
| 2026-06-01 | Qwen3.7 hosted | `qwen3.7-plus` | 1M；Max Input 991.80K；Max Output 65.53K | list 0.4/0.08 cache/1.6；页面有折扣价 | [Plus](https://www.qwencloud.com/models/qwen3.7-plus) |
| 2026-05-21 | Qwen3.7 hosted | `qwen3.7-max` | 1M；Max Input 991.80K；Max Output 65.53K | list 2.5/0.5 cache/7.5；页面有折扣价 | [Max](https://www.qwencloud.com/models/qwen3.7-max) |
| 2026-04-23 | Qwen3.6 | Qwen3.6-35B-A3B / 27B | 262,144 原生、可扩 1,010,000 | 开放权重无统一 token 价；API 另计 | [HF 35B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) / [HF 27B](https://huggingface.co/Qwen/Qwen3.6-27B) |
| 2026-02-15 | Qwen3.5 | Qwen3.5-397B-A17B / 122B-A10B / 35B-A3B / 27B | 多数 262,144 原生、可扩 1,010,000；hosted 1M | 开放权重无统一 token 价；API 另计 | [HF 397B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) / [HF 35B](https://huggingface.co/Qwen/Qwen3.5-35B-A3B) |
| 2025-07-22 | Qwen3-Coder | Qwen3-Coder-480B-A35B / 30B-A3B / Next | 262,144 原生；材料称可扩到 1M | 开放权重无统一 token 价 | [blog](https://qwenlm.github.io/blog/qwen3-coder/) / [HF 480B](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct) |
| 2025-04-29 | Qwen3 | Qwen3-235B-A22B / 30B-A3B | 32,768 原生；YaRN 到 131,072；部分后续线到 1M | 开放权重无统一 token 价 | [blog](https://qwenlm.github.io/blog/qwen3/) / [HF 235B](https://huggingface.co/Qwen/Qwen3-235B-A22B) |
| 2025-01-26 | Qwen2.5-1M | Qwen2.5-14B/7B-Instruct-1M | up to 1M | 开放权重无统一 token 价 | [blog](https://qwenlm.github.io/blog/qwen2.5-1m/) |
| 2024-09-19 | Qwen2.5 | Qwen2.5-72B-Instruct | 131,072 / 8,192 | 开放权重无统一 token 价 | [blog](https://qwenlm.github.io/blog/qwen2.5/) / [HF](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) |

---

## 6. Llama 系列专项表（按发布时间降序）

| 发布时间/排序键 | 系列 | 代表模型 | context / max output | 价格口径 | 来源 |
|---:|---|---|---:|---|---|
| 2025-04-05 | Llama 4 | Scout 17B×16E；Maverick 17B×128E；Behemoth preview | Scout 10M；Maverick 1M / 官方未统一列 max output | 开放权重；Meta 无统一 token API 价 | [Meta blog](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) / [HF Maverick](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct) |
| 2024-12-06 | Llama 3.3 | Llama-3.3-70B-Instruct | 128K / 官方未统一列 max output | 同上 | [HF](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) / [org](https://huggingface.co/meta-llama) |
| 2024-09-25 | Llama 3.2 | 1B/3B text；11B/90B vision | 128K / 官方未统一列 max output | 同上 | [Meta blog](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/) / [HF vision](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct) |
| 2024-07-23 | Llama 3.1 | 8B/70B/405B | 128K / 官方未统一列 max output | 同上 | [Meta blog](https://ai.meta.com/blog/meta-llama-3-1/) / [HF blog](https://huggingface.co/blog/llama31) |
| 2024-04-18 | Llama 3 | 8B/70B instruct/base | 8K / 官方未统一列 max output | 同上 | [Meta blog](https://ai.meta.com/blog/meta-llama-3/) / [HF](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) |
| 2023-07-18 | Llama 2 | 7B/13B/70B chat/base | 4K / 官方未统一列 max output | 开放权重；Meta 无统一 token API 价 | [Meta blog](https://ai.meta.com/blog/llama-2/) / [HF](https://huggingface.co/meta-llama/Llama-2-70b-hf) |

截至本轮官方核验，未找到 Llama 4 之后的新主系列；Meta/HF 官方页仍以 Llama 4 为 current 主系列，Llama 3.3 作为 70B Instruct 更新线存在。

---

## 7. Grok 系列专项表（按发布时间降序）

| 发布时间/排序键 | 系列 | 代表模型 | context / max output | 官方价 | 来源 |
|---:|---|---|---:|---:|---|
| 2026-current | Grok-4.3 | `grok-4.3` | 1M / 按模型页 | 1.25 / 0.20 / 2.50 | [model](https://docs.x.ai/developers/models/grok-4.3) / [pricing](https://docs.x.ai/developers/pricing) |
| 2026-03-10 | Grok-4.20 | `grok-4.20-0309-*`；multi-agent | 1M / 按模型页 | 1.25 / 0.20 / 2.50 | [release notes](https://docs.x.ai/developers/release-notes) / [4.20](https://docs.x.ai/developers/models/grok-4.20) / [pricing](https://docs.x.ai/developers/pricing) |
| 2025-11 | Grok-4 / 4 fast / 4.1 fast | grok-4 legacy / 4.1 Fast 系列 | 多数迁移到 4.3/4.20 | legacy/reroute | [release notes](https://docs.x.ai/developers/release-notes) / [migration](https://docs.x.ai/developers/migration/may-15-retirement) |
| 2025-04 | Grok-3 | Grok-3 | 按旧页 | 历史/alias 到新线风险 | [migration](https://docs.x.ai/developers/migration/may-15-retirement) |
| 2024-08 | Grok-2 | Grok-2 / vision | 按旧页 | 非当前主稳定 API | [xAI news](https://x.ai/news/grok-2) |
| 2024-03-28 | Grok-1.5 | Grok-1.5 | 128K | 历史 | [xAI news](https://x.ai/news/grok-1.5) |
| 2023-11-03 | Grok-1 | Grok-1；2024-03 开权重 | 8K 级 | 历史/无当前 API 主价 | [xAI release](https://x.ai/news/grok-os) / [GitHub](https://github.com/xai-org/grok-1) |

---

## 8. 其他开源/开放权重与 baseline 高频系列（按发布时间降序）

| 发布时间/排序键 | 系列 | 代表/最新可获取线 | context 概况 | 价格口径 | 来源 |
|---:|---|---|---:|---|---|
| 2026 | NVIDIA Nemotron | Nemotron-3 Nano/Super 等 | 4K-1M，按 checkpoint | NIM/云托管按当前页 | [Nemotron](https://developer.nvidia.com/nemotron) / [Build](https://build.nvidia.com/nvidia) |
| 2026 | GLM/ChatGLM | GLM-4.7 / GLM-5 | 128K-200K/1M 版本并存 | Z.AI/BigModel API 另计 | [BigModel docs](https://docs.bigmodel.cn/cn/guide/models/text/glm-4.7) / [pricing](https://docs.z.ai/guides/overview/pricing) |
| 2026 | DeepSeek open weights | V4 / V3.2 / R1 updates | 128K-1M 级，按 checkpoint | 开权重无统一价；hosted 见 V4 表 | [V4 release](https://api-docs.deepseek.com/news/news260424) / [V3 GitHub](https://github.com/deepseek-ai/DeepSeek-V3) / [R1](https://api-docs.deepseek.com/news/news250120) |
| 2026 | Mistral/Mixtral/Codestral | Large/Small/Magistral/Codestral 新线 | 128K-256K，按模型 | Mistral API 按当前页 | [models](https://docs.mistral.ai/models) / [pricing](https://docs.mistral.ai/platform/pricing/) |
| 2025 | Gemma | Gemma3 | 128K 级 | 开放权重无统一价；Vertex/AI Studio 另计 | [Gemma](https://ai.google.dev/gemma) / [HF Google](https://huggingface.co/google) |
| 2025 | Microsoft Phi | Phi-4/Phi-4-mini/multimodal | 16K-131K，按型号 | Azure AI Foundry / open weights | [Phi](https://azure.microsoft.com/en-us/products/phi/) / [HF Microsoft](https://huggingface.co/microsoft) |
| 2025 | IBM Granite | Granite 3.x/3.3 | 4K-128K 级，按 checkpoint | 开放权重/IBM 平台另计 | [IBM Granite](https://www.ibm.com/granite) / [HF IBM](https://huggingface.co/ibm-granite) |
| 2025 | InternLM | InternLM2.5/3 | 按 checkpoint | 开放权重无统一 token 价 | [GitHub](https://github.com/InternLM/InternLM) / [HF](https://huggingface.co/internlm) |
| 2025 | Baichuan | Baichuan-M1 / Baichuan2 | 按 checkpoint | 开放权重/平台计价不统一 | [GitHub](https://github.com/baichuan-inc/Baichuan2) / [HF](https://huggingface.co/baichuan-inc) |
| 2024 | Yi / 01.AI | Yi-1.5 / Yi-6B/34B | 4K-200K，按 checkpoint | 开放权重无统一 token 价 | [01.AI](https://www.01.ai/) / [HF](https://huggingface.co/01-ai) |
| 2024 | CogVLM | CogVLM2 | 视觉语言，按 checkpoint | 开放权重无统一 token 价 | [GitHub](https://github.com/THUDM/CogVLM) / [HF](https://huggingface.co/THUDM) |
| 2023 | Falcon | Falcon 7B/40B/180B/Mamba | 按 checkpoint | 开放权重无统一 token 价 | [HF TII](https://huggingface.co/tiiuae) |
| 2022 | GPT-J / GPT-Neo | GPT-J-6B、GPT-Neo | 历史小上下文 | 历史/开源 | [EleutherAI](https://github.com/EleutherAI/gpt-neox) / [HF GPT-J](https://huggingface.co/EleutherAI/gpt-j-6b) |

---

## 9. 风险项、待复查与失败记录

### 9.1 风险项与待复查记录

| 项 | 状态 | 建议 |
|---|---|---|
| Qwen3.7 | hosted API 已见；HF `Qwen` org 本轮未见同名开权重 | issue/实验中写 `qwen3.7-max` / `qwen3.7-plus` 并标 hosted；不要写成开源权重 |
| Qwen3.5/3.6 | HF 开权重已见，很多卡片是 262K 原生、可扩 1.01M | 若自托管，必须记录 checkpoint、量化、推理框架、YaRN/rope scaling 设置 |
| Llama 4 | 当前 Meta 主系列上界；Llama 3.3 是 70B Instruct 更新线 | 若用 Llama baseline，优先 Llama 4 Scout/Maverick 或 Llama 3.3/3.1 作为可复现对照 |
| Gemini 3.x / 3.5 | 官方页存在较新/preview/stable 条目，生命周期变化快 | 实验必须写精确 model ID 与调用日期，不只写 Gemini |
| DeepSeek aliases | `deepseek-chat` / `deepseek-reasoner` 有兼容/退役风险 | 正式 baseline 写 V4-Pro/Flash 或具体 open-weight checkpoint |
| GPT legacy / davinci / old Codex | 多数已停用或 legacy | 只作为历史相关工作，不作为新实验 baseline |
| 开源模型 API 价格 | 多数开放权重无统一官方 token 价 | 自托管记录硬件、量化、框架、吞吐；云托管记录云厂商、region、价格页 |

### 9.2 失败与阻塞记录

| 时间 | 对象 | 类型 | 记录 | 后续处理 |
|---|---|---|---|---|
| 2026-06-04 15:31:19 | Qwen3.7 开放权重 | 未发现/待复查 | 本轮在 Hugging Face `Qwen` 官方 org 未发现同名 `Qwen3.7` 开放权重集合；仅确认 Qwen Cloud hosted API 线 | 后续若 Qwen 官方发布开权重，应新增独立条目并更新 hosted/open-weight 区分 |
| 2026-06-04 15:31:19 | Grok-4.3 首发日 | 证据不足 | 本轮确认 xAI docs-visible latest 与模型页规格/价格，但未找到像 Grok-4.20 release notes 一样清晰的单页首发日 | 暂用 `2026-current` 排序键，后续补精确官方发布日期 |
| 2026-06-04 15:31:19 | Gemini 3.x/3.5 精确 ID | 待复查 | Gemini 官方 models/pricing 页面变化快，部分条目需按实验前精确 model ID 再核 | 实验前重新核验 lifecycle、pricing、preview/stable 状态 |

## 10. 对 `proj1` Path-1 / Path-2 的直接影响

1. baseline 不能只选旧 GPT-4o / Claude 3.5：baseline 文献已经出现 GPT-5、Claude 4.x、Gemini 3.x、DeepSeek V4、Qwen3.x、Llama4、Grok4.x 这类新线；新实验至少应覆盖“强闭源 + 成本平衡 + 开权重/自托管”三层。
2. Qwen 要双轨记录：开放权重最新可核验到 Qwen3.6/3.5 与 Qwen3-Coder；Qwen3.7 当前是 hosted API 线。
3. Llama 4 是当前 Meta 主系列上界：Llama 3.3 存在但只是 70B Instruct 更新；未核验到 Llama 5 或 Llama 4 后继主系列。
4. 价格敏感实验优先 DeepSeek V4-Flash / Gemini Flash / Qwen3.7-Plus / GPT-5.4-mini；强能力上界优先 GPT-5.5 / Claude Opus 4.8 / Gemini 3.x / DeepSeek V4-Pro / Grok-4.3。
5. 所有 run record 必须保存 model ID：不要只写“Claude”“Gemini”“Qwen”“Grok”，否则后续无法解释上下文长度、输出上限、价格和退役差异。

## 11. 更新日志

| 时间 | 更新内容 | 备注 |
|---|---|---|
| 2026-06-04 15:31:19 | 初始化根目录 LLM 模型现状微型文库，建立 README/GUIDE/SUMMARY 三件套，并把 issue #32 调研内容整理为长期总账 | 各模型表按发布时间降序；后续仍需持续核验价格与生命周期 |

## 12. 后续建议

- [ ] 选定 `proj1` 第一轮模型矩阵：强/平衡/低价/开源各 2-4 个。
- [ ] 为每个模型固定精确 `model_id`、provider、region、调用日期、价格链接。
- [ ] 把本目录的 baseline 文献模型清单择要回填到 `project_1_llm_state_machine_modeling/baselines/SUMMARY.md` 的模型盘点部分。
- [ ] 对 Gemini 3.x、Qwen3.7、Kimi K2.x、Grok 4.x 等 2026 新模型定期做精确 model ID 级核验。
