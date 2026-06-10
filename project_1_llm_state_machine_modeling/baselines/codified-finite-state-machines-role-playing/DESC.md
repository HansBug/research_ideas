# Codified Finite-State Machines for Role-Playing / 面向角色扮演的编码有限状态机

## 基本信息

- **标题**：Codified Finite-State Machines for Role-Playing
- **中文标题**：面向角色扮演的编码有限状态机
- **作者**：Letian Peng, Yupeng Hou, Kun Zhou, Jingbo Shang
- **单位**：University of California, San Diego
- **发表**：ICLR 2026
- **DOI**：10.48550/arXiv.2602.05905
- **链接**：[arXiv](https://arxiv.org/abs/2602.05905)

**代码/仓库获取方式**：
- 原文 PDF 中未在正文显著位置提供公开代码仓库链接。
- 论文包含较多 prompt 与代码示例附录，可作为方法复现线索，但本轮未核验完整 artifact。

**数据集获取方式**：
- 实验使用合成状态机验证任务，以及 Fandom Benchmark 中的角色 profile / story scenes。
- Fandom 来源公开可访问，但论文未在正文中提供本工作专用数据打包下载链接；需后续核验作者是否另有 artifact。

## 简报

这篇论文解决的问题是：LLM role-playing agent 容易在长交互中丢失角色内部状态，prompt-only 方法缺少可解释、可执行、可持续更新的状态迁移机制。作者重新引入 FSM，把文本角色 profile 编码成可执行状态机逻辑，并进一步扩展成 probabilistic FSM，以支持开放式角色扮演中的不确定状态演化。

- 输入：角色 textual profiles、场景和 actions。
- 方法：LLM 抽取关键状态，LLM 生成可执行 `get_next_state` / condition-checking code，并用 helper LLM 判断场景条件。
- 输出：Codified Finite-State Machines (CFSM) 与 Codified Probabilistic Finite-State Machines (CPFSM)，用于驱动角色状态更新。

```text
角色 profile / scene / action
  -> LLM state extraction + LLM code generation + condition checking
  -> executable CFSM / probabilistic CPFSM for role-playing state tracking
```

这篇论文在形式上是非常明确的 `NL -> FSM`，但任务域是角色扮演与叙事一致性，而不是软件/控制系统需求建模。因此它对 Project 1 的价值主要是“LLM 把自然语言状态规则编译成可执行 FSM”的方法近邻，而不是可直接公平对比的控制系统 STM baseline。

## 研究问题与动机

### 问题背景

角色扮演任务要求角色在长故事或多轮交互中保持一致的心理、身份和能力状态。传统 prompt-only LLM 方法容易随着上下文增长而发生 state drift。FSM 在游戏设计中长期用于清晰表示状态和迁移，但手写 FSM 难以覆盖开放式自然语言角色设定。

### 核心问题

论文试图回答：能否让 LLM 从角色 profile 自动抽取状态并生成可执行迁移逻辑，从而把自然语言角色约束转成可解释、可跟踪、可执行的 finite-state structure。

### 研究动机

作者认为，FSM 的显式状态与 transition rules 能解决 RP agent 的长期一致性问题；LLM 则能补足手工 FSM 在开放语义空间中难以扩展的问题。Project 1 可以借鉴这种“LLM 生成可执行 transition function”的思路，但必须注意其需求对象不是软件系统行为规格。

## 核心方法

### 方法概述

论文提出 CFSM 与 CPFSM：

1. CFSM：用 LLM 从 profile 中抽取状态集合，再生成 `get_next_state(state, scene, action)` 形式的 transition function。
2. 条件判断：生成的 transition code 可调用 `binary_question(text, question)` 等 helper，由 LLM 或训练好的 discriminator 判断场景是否满足某个条件。
3. CPFSM：把确定性 next state 扩展为状态分布，通过 logits 或概率矩阵表达多种可能状态。

### 形式化对象

论文给出 FSM tuple：状态集合、动作/事件集合、迁移函数和初始状态。角色的 latent state 被建模为随 action 变化的序列，CFSM 将这一过程显式化为有限状态机。

### Mario 示例

论文用 Mario power-up 例子解释：small Mario 获得 mushroom 后到 super Mario，被 Goomba 击中可能死亡；super Mario 获得 fire flower 到 fire Mario，被击中退回 small Mario。LLM 被要求把这种文本 transition rule 编码为可执行 `if` / `elif` 状态转移函数。

### CPFSM 扩展

CPFSM 不是只返回一个 next state，而是维护状态分布，适合叙事里多个状态都合理的情形。它增强了不确定性表达和解释性，但也依赖 logit 或判别器支持。

## 实验与评估

### 数据集 / benchmark

实验包括两类：

1. 合成验证：Mario power-up、Call of Duty enemy reaction、Tyrion 等状态机任务，用于比较 LLM prompt-only 是否能稳定跟踪状态。
2. 真实 role-playing：Fandom Benchmark，覆盖多个 artifact、角色 profiles 和 story scenes，用 NLI score 等指标评估角色响应一致性。

### 评估指标

论文使用 state correctness rate、NLI score、Best@K、效率/成本分析、ablation、不同 step length 分析等指标。

### 主要结果

论文报告 prompt-only LLM 随路径长度增加会发生明显状态混淆；CFSM/CPFSM 通过显式状态注册和 codified transition logic 改善一致性和可解释性。真实 RP 实验中，CFSM/CPFSM 相比 prompt / state-modeling baselines 提升角色行为一致性，CPFSM 对多潜在状态响应更有优势。

### 方法优势

- 把自然语言角色状态约束编译为可执行 FSM。
- 输出结构可解释，便于 debug。
- 可通过 probabilistic extension 支持开放世界中的不确定状态。
- 提供合成和真实 RP 两类评估。

### 方法局限性

- 任务域是 role-playing，不是软件或控制系统需求。
- transition code 的正确性依赖 LLM code generation 与 condition checker。
- Fandom Benchmark 和角色 profiles 与工程状态机 benchmark 不同，不能直接用于 Project 1 公平实验。
- 原文未提供清晰公开仓库入口，本轮复现仍有 artifact 阻塞。

## 与本研究的关系

### 四条件与综合评估

| 条件 | 评估 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 论文核心是用 LLM 建模显式 FSM / probabilistic FSM |
| NL 输入 | 🟢 | 主输入是 textual character profile、scene、action |
| LLM 方法 | 🟢 | LLM 抽取状态并生成 transition code，是核心组件 |
| STM族输出 | 🟢 | 输出明确是 CFSM / CPFSM，形式上是 FSM-family |
| BASELINE评估 | 🟠 | 形式高度同构，但任务域是 role-playing / narrative state tracking，不是软件需求到 STM 的 direct baseline |

### 对 Project 1 的启发

1. **transition code 生成**：可以把自然语言迁移规则转成可执行函数，作为状态机 DSL 或 pyfcstm 的中间桥梁。
2. **显式状态注册**：先枚举状态集合再生成迁移，避免 LLM 每步自由生成状态名。
3. **条件 helper**：对 guard 条件可用受控 query / classifier 判断，而不是完全由 LLM 端到端输出。
4. **概率状态机思路**：在需求模糊时，可以先保留多个候选状态/迁移概率，再通过验证或人类反馈收敛。

### 不应混淆的边界

虽然它是 `NL -> FSM`，但输出不是软件系统设计模型，而是角色扮演 agent 的内部状态控制机制。Project 1 若引用它，应作为“LLM 编码 FSM 的强方法近邻”，不能作为控制系统状态机建模 direct baseline。

## 重要的相关工作

论文相关工作覆盖 role-playing、state modeling、LLM for coding。值得注意的是，作者明确提到近期 LLM 也可从自然语言 instructions 修改 FSM 或生成 transition logic，这和 Project 1 的 baseline 线索相通。

本论文也提示一个学术趋势：FSM 不只作为传统软件模型，也正在被 LLM agent、游戏、RP、RL 等领域重新用作可解释状态控制结构。因此 Project 1 需要在 related work 中区分“FSM 作为目标建模工件”和“FSM 作为 agent 内部控制机制”。

## 文献分类总结

- **任务类型**：角色 profile 到可执行 CFSM / CPFSM。
- **输入类型**：自然语言角色设定、场景、动作。
- **输出类型**：Codified FSM / Codified Probabilistic FSM。
- **LLM 角色**：状态抽取、迁移逻辑代码生成、条件判断。
- **Project 1 关系**：形式上强同构、方法上有借鉴价值，但任务域不匹配。
- **建议总账评估**：`BASELINE评估=🟠`，四条件为 `🟢/🟢/🟢/🟢`。
