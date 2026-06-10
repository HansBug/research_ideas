# CIR+CVN：连接 LLM 语义理解与 Petri 网并发验证 / CIR+CVN

## 基本信息

- **标题**：CIR+CVN: Bridging LLM Semantic Understanding and Petri-Net Verification for Concurrent Programs
- **中文标题**：CIR+CVN：连接 LLM 语义理解与 Petri 网并发验证的并发程序验证方法
- **作者**：Kaiwen Zhang, Guanjun Liu
- **单位**：Tongji University
- **发表**：arXiv preprint, 2026-04-10；PDF 使用 ACM `Conference '26` 占位模板，正式会议/出版信息待核验
- **年份**：2026
- **DOI**：10.48550/arXiv.2604.09318
- **链接**：https://arxiv.org/abs/2604.09318

**代码/仓库获取方式**：
- 原文未提供公开代码/仓库获取链接。
- 论文给出 CIR/CVN 定义、静态规则表、translation table 和 evaluation patterns，但未见可直接下载实现或 artifact URL。

**数据集获取方式**：
- 原文未提供公开数据集下载链接。
- 实验使用作者构造的 9 个 bounded-concurrency patterns，其中 6 个含 bug/repair 目标，3 个 bug-free baseline；具体 pattern、CIR size、CVN state counts 和 repair results 在正文表格中给出。

## 简报

本文解决的是：在 LLM 从自然语言需求/系统规格构造并发程序或并发设计时，如何不直接验证任意源码，而是让 LLM 先生成一个 alias-free 的并发中间表示 CIR，再机械翻译为 Petri net 近邻 CVN，最后通过穷尽状态探索发现 deadlock、signal loss 等问题并驱动 repair。它是 LLM + formal verification 的强行为模型近邻，但目标产物是 Petri-net-style concurrency artifact，不是显式状态机。

- **输入**：自然语言 concurrency requirement / system specification，实验中每个 pattern 使用短自然语言描述让 LLM 生成 CIR。
- **方法**：LLM 生成 statement-level alias-free CIR；61 条 static rules 检查 CIR；validated CIR 机械翻译到 weighted place/transition Petri net CVN；CVN exhaustive exploration 执行 deadlock、signal-loss、goal reachability 等检查；counterexample 映射回 statement identifiers 进行迭代修复。
- **输出**：CIR artifact、CVN Petri net、structured diagnostics / counterexamples、repair report，以及通过或拒绝的修复后 CIR。

```text
自然语言并发需求 / 系统规格
  -> LLM 生成 CIR（显式资源、锁保护关系、statement id）
  -> 61 条 static validation rules
  -> deterministic CIR-to-CVN translation
  -> Petri-net exhaustive verification + goal reachability
  -> sid-anchored counterexample / repair report
  -> 修复后的 CIR 或拒绝结果
```

实验显示，方法可在 9 个 bounded-concurrency patterns、5 个 LLM 上进行 bug detection 和 iterative repair；论文结论强调 trust boundary 位于 generated CIR，而不是 arbitrary source code。

## 研究问题与动机

### 问题背景

并发 bug 往往来自线程交互、锁顺序、条件变量、信号丢失和资源保护关系。直接从源码验证并发程序需要解决 aliasing、ownership、API idioms、closure capture 等复杂问题；动态工具覆盖有限，静态分析又常在精度和扩展性之间取舍。

### 核心问题

论文不试图证明源码到模型的等价性，而是提出一个 model-first 的验证边界：

1. LLM 能否从自然语言规格生成一个显式资源身份和保护关系的并发模型。
2. 该模型能否被 deterministic translator 转换为可穷尽探索的 Petri net。
3. 形式检查的 counterexample 能否映射回稳定 statement id，引导 LLM 做 targeted repair。
4. 如何避免 repair 仅仅“删行为”导致 bug-free but behavior-dropping 的假通过。

### 研究动机

LLM 擅长从自然语言和代码习惯中恢复意图，但不能穷尽分析线程 interleavings；Petri net/model checking 擅长穷尽探索，但需要结构化模型。CIR+CVN 的动机是把 LLM 放在 intent recovery/model construction 端，把 exhaustive reasoning 留给 formal backend。

### 研究意义

对 Project 1，它提供了一个非常清晰的“LLM 生成结构化行为工件 -> deterministic validation/translation -> formal analysis -> counterexample-guided repair”范式。虽然输出不是状态机，但 CIR 的 `sid`、guard、资源操作和 control points 与 guarded transition model 高度近似，CVN 又是 Petri-net 形式的状态空间模型。

## 核心方法

### 方法概述

CIR+CVN 架构包含五个关键阶段：

1. **CIR generation**：LLM 从自然语言规格生成 alias-free concurrency artifact。
2. **Static validation**：对 CIR 执行 9 类 61 条规则，发现 missing fields、undefined resources、unprotected access、double lock、missing return 等问题。
3. **CIR-to-CVN translation**：将 statements、locks、semaphores、condvars、channels、threads 等转换为 weighted place/transition Petri net。
4. **Formal analysis**：在 bounded state space 中做 deadlock、signal loss、livelock advisory、goal reachability 检查。
5. **Repair loop**：将 structured diagnostic 映射到 statement id，提示 LLM 局部修改 CIR，再重新验证。

### CIR：并发中间表示

CIR 是 statement-level、alias-free 的并发模型：

- shared resources 全局命名；
- protection map 显式说明变量由哪个 lock/atomic 保护；
- 每条 statement 带稳定 `sid`，用于 diagnostics 与 repair；
- 同步语义包含 lock/drop、condvar wait/notify、channel op、semaphore、atomic、spawn/join、function summary 等；
- 普通计算和 I/O 逻辑被抽象，重点保留 concurrency skeleton。

这使 LLM 不必生成完整源码，而是生成便于验证的并发规格。

### CVN：验证网

CVN 是 weighted place/transition Petri net，包含有限 global store 与 three-valued guards，用于处理 data-dependent branching。资源 identity 在 CIR 中已由全局命名解决，因此 CVN 不承担源码 alias analysis。论文给出 translation correspondence results，支持 deadlock 和 signal-loss analysis。

### Static rules 与 diagnostics

附录表给出 9 类共 61 条 CIR error categories：

- E0xx Structural。
- E1xx Name resolution。
- E2xx Type。
- E3xx Resource compatibility/protection。
- E4xx Concurrency。
- E5xx Lock safety。
- E6xx Control flow。
- E7xx Protection map。
- E8xx Function summary。

这部分对 Project 1 的 DSL diagnostics 很有价值：上游工具报告事实，本项目再决定哪些 diagnostic 阻塞模型进入正式数据。

### Analysis 与 repair

分析层不仅检查 definite bug，也执行 lightweight goal reachability。原因是简单修复可能删除关键行为，从而让 deadlock/signal loss 消失但业务目标也不可达。Goal reachability 只在安全检查之后执行，用 designated critical outcomes 过滤语义不完整 repair。

Repair report 包含 blame anchor、diagnostic、相关 sid、反例状态/资源信息与建议修复方向。LLM 在 default 5 rounds 内尝试局部修复；若未收敛则报告失败。

## 实验与评估

### 数据集 / 案例系统

实验包含 9 个代表性 bounded-concurrency patterns：

1. Two-mutex deadlock。
2. Condvar signal loss。
3. Channel + mutex deadlock。
4. Three-lock circular deadlock。
5. Partial deadlock / livelock advisory。
6. Dual condvar cross deadlock。
7. Semaphore throttle bug-free baseline。
8. CAS contention bug-free baseline。
9. Function summary propagation bug-free baseline。

### LLM 设置

论文评估 5 个 LLM：GPT-5、Claude 4.6 Opus、Gemini 3 Pro、Qwen 3.5、DeepSeek-V3。所有模型 temperature 0，output limit 4096 tokens。每个 pattern 用短自然语言 prompt 让模型生成或修复 CIR。

### 评估指标

- 是否生成 statically valid CIR。
- CVN 是否检测出预期 deadlock/signal-loss/livelock advisory。
- Repair rounds、regressions、是否被 goal reachability 接受/拒绝。
- Bug-free baseline 是否产生 false positives。
- Counterexample/diagnostic 是否能定位到 sid 并支撑修复。

### 主要实验结果

- 6 个 bug patterns 的 definite bugs 能通过 CVN diagnostic 暴露，3 个 bug-free baselines 不产生 false positives。
- Claude 4.6 Opus 平均 repair rounds 最低，部分复杂 pattern 下 DeepSeek-V3 生成或修复失败。
- Goal reachability 对防止 semantic regression 有必要：某些 repair 虽然消除了 bug diagnostic，但会让关键目标不可达，因此不被接受。
- 结论强调：Across 9 patterns and 5 LLMs, no CIR containing a definite bug or violating a business goal is accepted。

### 方法优势

1. Trust boundary 清晰：验证 generated CIR，不声称验证 arbitrary source code。
2. 将 LLM 和形式引擎职责分离：LLM 做结构化建模/修复，formal backend 做穷尽检查。
3. `sid` anchoring 让 counterexample 可回映到 LLM 可修改位置。
4. Goal reachability 避免“删行为式修复”。

### 方法的局限性

- 不证明自然语言/源码到 CIR 的等价性；CIR 是信任边界。
- 实验规模是 9 个 bounded patterns，尚不是大规模真实并发软件 benchmark。
- Livelock 只作为 advisory warning，不等同于完整 liveness verification。
- 未提供公开代码/数据包，复现实验需等待作者 artifact 或手工重建。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠（强并发验证近邻；非 exact STM direct baseline）
- **四条件证据**：`LLM4Modeling=🟢`，`NL输入=🟢`，`LLM方法=🟢`，`STM族输出=🟡`。
- **为什么是强近邻**：CIR/CVN 都是强行为模型；CIR 有 statement/control/resource 状态，CVN 是 Petri-net 状态空间，可检测 deadlock/signal loss 并产生 counterexample。
- **为什么不是直接 baseline**：输出不是 STM/Statechart/FSM/SysML 状态机，而是 concurrency IR + Petri net；任务主轴是 concurrent program verification/repair，不是控制系统 NL-to-STM 建模。

### 可借鉴之处

1. Project 1 的 LLM 输出也可先落到结构化、可诊断的中间模型，再机械翻译或验证。
2. 稳定 statement/transition id 对 repair-review、counterexample mapping 和 run record 审计非常重要。
3. Goal reachability 类似 Project 1 中“修复后不能删掉需求覆盖/业务场景”的 eligibility gate。
4. Static diagnostic codes 可启发 pyfcstm/agent-loop 的 parse/semantic/design/sim diagnostics 分层。

### 存在的不足与改进空间

- 该文不处理自然语言需求到 explicit STM 元素的完整 traceability。
- Petri net 并发语义强，但和控制系统状态/事件/guard/action 的结构字段不完全同构。
- 没有公开 artifact，短期只能作为方法论参照而非可运行 baseline。

### 对本研究的启发

Project 1 可以把 CIR+CVN 作为“LLM-generated formal behavioral artifact + verifier-mediated repair”的强近邻，尤其用于论证：强可验证性来自结构化语义边界与确定性 backend，而不是 LLM 本身声称的推理能力。

## 重要的相关工作

### 1. 重要的前身类工作

- **Murata, 1989, Petri Nets: Properties, Analysis and Applications**：Petri net 理论基础，支撑 CVN formalism。
- **Jensen et al., 2007, Coloured Petri Nets and CPN Tools**：Petri net with data 的代表工具线索；本文选择 finite global store + three-valued guards 以降低复杂度。
- **Esparza and Heljanko, 2008 / Esparza et al., 2002**：partial-order/unfolding model checking 背景。

### 2. 直接参与实验的 baseline

- 实验 baseline 不是外部论文方法，而是 5 个 LLM 在 9 个 concurrency patterns 上的生成/修复表现，以及 3 个 bug-free patterns 用于 false-positive 检查。

### 3. 提供了重要论证的工作

- **Boyapati et al., 2002 / Naik et al., 2006 / LOCKSMITH 等静态分析线索**：用于说明 source-level alias/resource reasoning 的困难。
- **Burckhardt et al., 2010 / Musuvathi and Qadeer, 2008 / VeriSoft**：用于说明 dynamic/systematic schedule exploration 的覆盖与边界。
- **Clarke et al., 2000, CEGAR**：作为 counterexample-driven refinement/repair 的形式化背景。

### 4. 在技术上提供了支持的工作

- **RepairAgent / Bouzenia et al., 2025** 与 **Xia et al., 2023**：LLM program repair 背景，用于定位本文 repair loop 与 LLM 修复工作的关系。
- **Translation validation / Necula, 2000** 与 SLAM/BLAST/CPAchecker：用于讨论模型/代码 trust boundary 与 conformance checking。

### 5. 其他重要工作

- 原文还综述了 LLM for program analysis、verification、test generation、static-analysis assistance 等方向；这些工作说明 LLM 能辅助识别 intent，但不能替代穷尽 interleaving reasoning。

## 文献分类总结

- **类别**：LLM 生成并发形式模型 + Petri-net 验证修复；形式方法强近邻。
- **BASELINE评估**：🟠（强近邻，非 exact STM direct baseline）。
- **输入**：自然语言并发需求/系统规格；实验为 9 个 bounded concurrency pattern 的短描述。
- **输出**：CIR concurrency artifact、CVN Petri net、diagnostics、counterexamples、修复后 CIR。
- **输出模型类型**：Petri net / concurrency IR，强行为模型近邻，不是 STM-family exact artifact。
- **使用的LLM**：GPT-5、Claude 4.6 Opus、Gemini 3 Pro、Qwen 3.5、DeepSeek-V3。
- **主要方法**：LLM 生成 alias-free CIR + static rules + deterministic CVN translation + exhaustive verification + goal reachability + sid-guided repair。
