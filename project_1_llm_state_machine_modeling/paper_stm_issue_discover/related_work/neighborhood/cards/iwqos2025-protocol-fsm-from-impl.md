# 卡片 · ProtocolGPT（IWQoS 2025）

⭐ **全文可得**：arXiv v4 HTML + PDF 全文均已取到并通读（256 KB HTML / 11 页 PDF），⭐ **三张 prompt 模板图的文字也已从 PDF 提出**（Fig. 3 / 4 / 5），⛔ 本卡**没有任何一节是「仅据摘要」**。⚠️ 唯一未取到的是 IEEE camera-ready（见 F1）。

⭐ 另有一项**超出论文**的核验：⭐ 作者的 GitHub 仓库已实际 clone 级检视（逐文件读源码），⛔ 结论与论文描述**不一致** —— 见 D 节与 E2。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `iwqos2025-protocol-fsm-from-impl` |
| `title` | Unleashing the Power of LLM to Infer State Machine From the Protocol Implementation（工具名 **ProtocolGPT**） |
| `year` | **2025**（Crossref `issued` = `2025-07-02`；⚠️ arXiv v1 是 2024-05-01 且**标题不同** —— `Inferring State Machine from the Protocol Implementation via Large Language Model`，引用时别混） |
| `venue` | IWQoS 2025 · 2025 IEEE/ACM 33rd International Symposium on Quality of Service，Gold Coast, Australia，**pp. 1–10**（正式长文，非 poster） |
| `ccf` | **B**（计算机网络）—— ⚠️ 本库 [ccf_venues/](../../../../../ccf_venues/) **未收录该 venue**（`grep -i iwqos` 零命中），等级据 CCF 官方目录领域分类，证据级别 **S** |
| `doi` | [`10.1109/IWQoS65803.2025.11143461`](https://doi.org/10.1109/IWQoS65803.2025.11143461) —— ⭐ **已过 Crossref API 核验**，返回 title / container / event / page 全部对得上 |
| `arxiv` | [`2405.00393`](https://arxiv.org/abs/2405.00393)（本卡引用的是 **v4，2025-03-27**） |
| `url` | 代码：[github.com/s1awwhy/ProtocolGPT](https://github.com/s1awwhy/ProtocolGPT) |
| `artifact_type` | ⭐ **协议状态机**（非确定性 FSM，五元组 $(\Sigma, S, S_0, E, \delta)$，⛔ 无时钟、无并发区、无层次） |
| `task` | ⭐ **生成 / 抽取**（源码 → FSM）；⭐ 副产物两项：实现间一致性比对（⛔ 人工）+ 下游测试生成（AFLNet 种子） |
| `boundary` | ⭐ `邻域`（协议状态机，按 [README.md](../README.md) §2.1 三档表） |

---

## B. LLM 应用形态

### B1 · 流水线阶段

```
[人] 逐协议手写关键词正则集
  → [确定性] code filter：regex 匹配文件、按命中率选出 FSM 模块子目录
  → [确定性] syntax-aware 分块（MaxChunkSize / MinChunkSize / overlap，语言相关分隔符）
  → [确定性] OpenAI embedding → FAISS 向量库（ANN 检索）
  → [LLM · RAG] ① 问「哪些文件定义了 message types / states / transitions」
  → [LLM · RAG] ② 问「{code_path} 里定义了哪些 states」「哪些 messages」
  → [LLM · RAG] ③ **逐 state 展开**：把 {current_state} 依次替换成 ② 抽出的每个状态，各问一次
  → [确定性] 20 次采样 · 出现率 > 80% 才保留
  → [确定性] JSON 解析
→ [下游] AFLNet 种子生成（⛔ 不在环内）
```

⭐ **阶段总数 9（不含下游）· LLM 阶段 3 · 确定性阶段 5 · 人工阶段 1。**

⚠️ ③ 是**扇出**不是循环：`ProtocolGPT generates multiple prompts using the extracted states. Then it iteratively replaces the current_state with all previously identified states.`（§IV-B3，**M**）—— 一个状态一次调用，互不依赖，没有谁看谁的结果。

### B2 · 每次 LLM 调用的角色

| 阶段 | 角色 |
| :-- | :-- |
| ① code paths | ⭐ **检索改写器 / 抽取器**（定位相关文件） |
| ② states & messages | ⭐ **抽取器**（从 struct / enum 里读出符号） |
| ③ transitions | ⭐ **生成器**（给定 state 推可能的迁移） |

⛔ **没有评审者、没有修复者、没有裁决者、没有规划者。** ⭐ 三次调用全是「问一次、拿一次」，⛔ 没有任何一次 LLM 调用的输入包含「上一次输出被判为不合格」这类反馈。

### B3 · prompt 策略

`CoT`（三阶段分解 + 模板里逐字写 `You can do this step by step`）· `结构化输出约束`（**prompt 内给 Desired format 的 JSON 形状**，⛔ 不是受限解码、⛔ 不是 function calling）· `self-consistency`（20 次采样 + 80% 阈值）· `BAP`（background-augmented prompting，把状态描述 $s$ 与任务指令 $i$ 拼接）· `角色扮演`（⚠️ 只在**仓库代码**里见到 `As a IKE protocol specialist`，⛔ 论文正文的三张模板图里没有角色句）。

⛔ **无 few-shot**（三张模板图里没有任何 worked example）· ⛔ **无多智能体辩论** · ⛔ **无工具调用**。

⭐ 三张模板**逐字**（**M**，出自 §IV-B Fig. 3 / 4 / 5，从 PDF 提取）：

- Fig. 3：`Which files in this codebase define {protocol} message types, protocol states, and state transitions? You can do this step by step by looking for the files that define message types, protocol states, and state transitions.` / `Desired format: {"Related files": ["/path/to/messages", "/path/to/states", "/path/to/transitions"]}`
- Fig. 4(a)：`Can you provide a list of all the {protocol} states defined in the {code_path} within the codebase, formatted as a JSON object with the key "States"?` / `{"States": ["state1", "state2",......]}`
- Fig. 5：`The server in the {protocol} protocol has many states, such as {states}. Many kinds of messages are also defined in the codebase, such as {messages}. When the server receives different messages, the server's state will transition to different states. The file {code_path} in the codebase is likely to contain information about the relevant logic for state transitions. What are the possible state transitions and corresponding message types that the server can transition to from the {current_state} state? You can complete this task step by step.` / `{"{current_state}": [{"receive_message": "message1", "next_state": "state1"}, ...]}`

### B4 · ⭐⭐ 循环与裁决者（本轨最关键的一格）

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⛔ **无修订循环**（**S**：全文无 revise / retry / feedback / iterate-until 类描述；三次 LLM 调用严格前向） |
| ⭐ **裁决者是谁** | ⭐ **确定性规则** —— 20 次采样中出现率 `> 80%` 才进最终 FSM |
| 终止条件 | ⭐ **固定次数**（20），⛔ 不是收敛判据、⛔ 不是预算耗尽 |
| 最大轮数 | **20**（采样次数，非修订轮数） |
| ⭐ 逐轮边际收益 | ⛔ **原文未提供** —— ⭐ 只给了端到端 P/R 的 10 次运行均值，⛔ 没有「第 k 次采样带来多少净增」这类曲线，⛔ 也没有 80% 阈值的敏感性分析 |

⭐ 裁决规则逐字（**M**，§IV-B「Mitigation of the LLM Hallucination」）：`we conduct 20 iterations of dialogue using the augmented model to extract states, message types, and state transitions. We then select the responses that appear with a probability greater than 80% across all iterations as the final result.`

⭐⭐ **这一格对我们最有用的一点**：⭐ 他们把多次采样当作**精度工具**（取近似交集、砍掉不稳定项），⛔ 而我们把多轮当作**能力度量**（`hit@3` 取并集）。⭐ 同一个「多次采样」机制，两种完全相反的用法 —— ⚠️ 而他们在 80% 这么苛刻的共识阈值下，recall 仍有 **87.09%**（**M**，Table IV Avg.）。⭐ 这是一条对「取交集会不会毁掉 recall」的外部反证据。

⛔⛔ **全流水线没有 sound oracle。** ⚠️ 这一点值得单独强调：被分析对象是**能编译、能运行、自带测试套件的协议实现**（strongSwan / s2n-tls / openbgpd / feng / openl2tp），⛔ 但编译器、类型检查、测试执行、AFLNet **一个都没被拉进环内当裁决者**。⭐ AFLNet 只在 §V-D 作为**下游消费者**出现，⛔ 它的覆盖率结果**不会回流**去修正 FSM。

⚠️ **仓库侧的循环形态与论文不同（M，我逐文件读了源码）**：`llm.py` 的 `chat_loop()` 是 `while True: query = input("👉 ")` 的**人工交互 REPL**，配 `ConversationSummaryMemory`。⭐ 也就是说，**已释放的制品里，决定「下一轮问什么」的是坐在终端前的人**，⛔ 而不是脚本。

### B5 · ⭐ 中间表示

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有，三层** |
| 形态 | ① **关键词 / 正则集**（code filter 用）② **JSON schema**（迁移三元组 `current_state` / `receive_message` / `next_state`）③ **运行时状态与消息候选集**（阶段 ② 的输出） |
| ⭐ 是否闭合 | ① ⭐ **闭合，但逐协议手写** ② ⭐ 形状闭合、内容开放 ③ ⭐⭐ **运行时闭合** —— 阶段 ③ 的 prompt 把 `{states}` 与 `{messages}` 整个灌进去，模型只能在这个集合里挑 |
| ⭐ 谁定的 | ① ⭐ **人**（论文说 derived from RFCs + expert knowledge）② **人** ③ ⭐⭐ **LLM 自己生成**（阶段 ② 产出、阶段 ③ 消费） |

⭐⭐ ③ 是这篇最值得我们注意的结构：**「让 LLM 先自造一个闭合集，再在这个集合上做受限生成」**。⭐ 与我们「预编 19 条固定词表 + LLM 自动选」的差别是：⛔ 他们的闭合集**每个样本一份、由模型自己造**，⭐ 我们的闭合集**全语料共用一份、由人预编**。⚠️ 代价对称：他们的集合错了就整格连带错（阶段 ② 的 states 漏一个，阶段 ③ 永远问不到它），⛔ 我们的集合错了是全语料系统性偏差（正是 `occupancy_after` 那次事故的形状）。

⚠️ ① 的**论文说法与代码实现不符**（**M**）。论文写：`we define a comprehensive set of keywords related to protocol state machines, derived from both RFCs and expert knowledge` 且 `our keyword set can be extended to accommodate additional protocols with negligible engineering effort`。⛔ 仓库 `code_filter.py` 里实际是一个**逐协议手写的 5 条正则字典**：

```python
patterns = {
    "ikev2": r'ike_sa_state|exchange_type',
    "tls":   r'message_type|state_machine',
    "bgp":   r'session_state|session_events|msg_type',
    "rtsp":  r'RTSP_Server_State|cur_state',
    "l2tp":  r'state_machine|L2TP_LAIC_STATE|fsm_table',
}
```

⚠️ 逐条对着 benchmark 表看，**这 5 个 key 与 6 个被评测协议一一对应**（TLS 1.2 / 1.3 共用 `tls`）。⭐ 有几条（`RTSP_Server_State`、`L2TP_LAIC_STATE`、`fsm_table`）是**具体实现里的标识符**，⛔ 不是 RFC 术语 —— ⭐ 按本仓库 §3.5 的判据抽象化自问「它表达的是通用建模原则还是这个样本的答案」，⛔ 这几条只能落到**后者**。⚠️ 这是**我方判断（I）**，⛔ 论文并未承认按样本调参；⭐ 但 D 节的消融数字让它变得重要：**code filter 单独贡献了 +41.02pp precision / +55.57pp recall**（V3 vs V2，**M**），⛔ 即整套方法最大的单项增益来自这个逐协议手写的部件。

### B6 · 模型

⭐ **GPT-4，单模型**（**M**：`We select the widely acclaimed GPT-4 model (the latest model at the time of our experiment), renowned for its extensive 1.7 trillion parameters`），`temperature = 0.2`。⭐ Embedding 用 OpenAI 的 embedding 模型；⭐ 向量检索用 FAISS。⛔ **无多模型对照**（GPT-QA 是同一个 GPT-4 的**无增强**版本，属消融不属跨模型）。

⚠️ **代次很旧**：论文 §III-B 自己写 `GPT-4 has only a context window of 8,192 tokens`，⭐ 即实验用的是 2023–2024 那一代；⭐ 仓库 `model_list` 里是 `gpt-3.5-turbo` / `gpt-4` / `gpt-4-1106-preview`。⛔ 按 X1 的教训（SOTA 与上一代不是一个量级），⚠️ **这篇的绝对数字对今天的参考价值要打折**；⭐ 但「多次采样取共识」「让模型自造闭合集」这两条**形态结论**不随模型代次失效。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | ⭐ 是不是 sound |
| :-- | :-- | :-: |
| code filter | 正则匹配 + 命中率最高子目录选择 | ⛔ 否（启发式） |
| syntax-aware segmentation | 语言相关分隔符递归切分 + Min/Max 阈值 + overlap | ⛔ 否 |
| 检索 | OpenAI embedding + FAISS 近似最近邻 | ⛔ 否（近似） |
| 共识过滤 | 20 采样 · `> 80%` 出现率 | ⛔ 否（统计规则） |
| 输出解析 | JSON 解析 | ⭐ 是（但只判形状，⛔ 不判内容） |

⛔⛔ **没有任何一个环节是 sound oracle**：⛔ 无 parser（对 FSM 本身）、⛔ 无类型检查、⛔ 无模型检查器、⛔ 无求解器、⛔ 无测试执行。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **四个**：RFCNLP（S&P'22，学习型）· Netzob（ASIACCS'14，动态）· NetPlier（NDSS'21，动态）· **GPT-QA**（同款 GPT-4 只给 prompt、不给源码）。⭐ 另有 4 档消融 V0–V3。⚠️ 静态分析类**找不到可比工具**（**M**：`We fail to find any open-source tools capable of inferring FSMs`） |
| `dataset` | ⭐ 6 个协议实现，**commit 级 pin**：strongSwan `f994e0a`（IKEv2）· s2n-tls `025f3b2`（TLS 1.3 与 1.2 共用）· openbgpd `08b59c1` · feng `d302a1c`（RTSP）· openl2tp `be6c288`。⭐ 另取 4 个 IKEv2 实现做实现间差异分析。⭐ **分母 = 人工 ground truth 的迁移数**：IKEv2 23 · TLS 1.3 31 · TLS 1.2 31 · BGP 88 · RTSP 22 · L2TP 53（Table V） |
| `metrics` | ⭐ 迁移四分类：`correct` / `partially correct` / `incorrect` / `not found`。$Precision = \frac{C}{C+PC+IC}$，$Recall = \frac{C}{C+PC+NF}$。⚠️ **`PC` 同时进两个分母而永不进分子** —— 三元组 $(S_i, M, S_t)$ 里错一个就整条不得分。⛔ **无任何 `@k` 口径**（20 次采样被折叠进单一共识产物，⛔ 不作为指标报告） |
| ⭐ `judged_by` | ⭐ ground truth：**3 名专家、> 72 人时**，先独立审、后合议 refine（**M**：`we recruited three knowledgeable experts with over 72 hours human effort, to independently audit the protocols' repository code and summarize the state machines. Subsequently, the experts collaborated to discuss and refine`）。⛔ **四分类判定由谁做、怎么做，原文未提供**；⛔ **无 $\kappa$、无一致率**（只说「合议 refine」，属共识而非可测一致性） |
| `human_baseline` | ⛔ **无**（人工只用于建 ground truth，⛔ 不作为对照臂） |
| `runs` | ⭐ **10 次运行取均值**，`maximum p values less than 0.05`（**M**）；⛔ **无方差 / 无置信区间**（⭐ 只有 §V-D 的 fuzzing 折线图给了 5 次 × 24 小时的 95% CI） |
| ⭐ `adverse_results` | ⭐⭐ **报得相当诚实，两处**（见下） |

⭐ **不利结果的两处处理（直接可借鉴）**：

1. ⭐ **被 baseline 打败也照写**：RTSP 上 RFCNLP 的 precision **84.62** 高于自己的 **70.59**；正文不回避，改为在**同一格换指标论证**：`in the case of RTSP, RFCNLP identify 11 correct transitions, while our method identify 12`（**M**，§V-A）。⭐ 同时把自己的 RTSP recall **54.54**（全表最低）原样留在表里。
2. ⭐ **消融里的反向台阶也照写**：V1（只加 embedding）的 **22.63 / 19.24** 反而**低于** GPT-QA 的 **35.83 / 24.14**，论文直接给出归因：`We attribute this decline to the different dependent knowledge used by V0 and V1`（**M**，§V-B Strategy 1）。⚠️ 归因本身可疑（⛔ 它把 V0 与 V1 对比，⭐ 而实际比较对象是 GPT-QA），⛔ 但**没有把这一格藏起来**。

⭐ **主结果**（Table IV Avg.）：ProtocolGPT **P 91.42 / R 87.09**；GPT-QA 35.83 / 24.14；RFCNLP 55.04 / 29.03；Netzob 42.30 / 28.65；NetPlier 61.06 / 28.03。

---

## D. ⭐ 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文（arXiv） | 🟢 | [arxiv.org/abs/2405.00393](https://arxiv.org/abs/2405.00393) | ⭐ `curl` HTTP 200；HTML v4 **256 888 字节**、PDF **897 387 字节 / 11 页**，⭐ 均已通读；⭐ 三张 prompt 模板图文字**已从 PDF 成功提取** |
| 论文全文（IEEE） | 🟠 | [ieeexplore.ieee.org/document/11143461](https://ieeexplore.ieee.org/document/11143461) | ⛔ `curl -L` 返回 **HTTP 202 / size=0**（bot 拦截或需鉴权）；⭐ 元数据经 **Crossref API** 核实（pp. 1–10，event Gold Coast 2025-07-02） |
| ⭐ **实验代码** | 🟠 | [github.com/s1awwhy/ProtocolGPT](https://github.com/s1awwhy/ProtocolGPT) | ⭐ `verify_assets` 机械建议 🟢：HEAD **`df3fceb053`** · 文件 **12**（非文档 **11**）· release **0** · **license 无**。⛔ **我方终裁降为 🟠**，理由见下 |
| ⭐ **数据集 / ground truth** | ⚪ | — | ⛔ 仓库里**没有**任何 ground truth、状态机标注或 `test_code/`；⭐ 论文只在 Table V 给汇总数字。⚠️ 论文原话：`The source code and the experimental data will be released immediately after the work is accepted.`（⭐ 论文已于 2025-07 发表，⛔ 数据仍未见） |
| 实验结果细则 | ⚪ | — | ⛔ 只有论文内表格（Table IV/V/VI/VII）；⛔ 无逐条可下载结果、⛔ 无 10 次运行的原始记录 |
| Artifact / 复现包 | ⚪ | — | ⛔ 无 Zenodo / 4open / OSF DOI；⛔ 无 IEEE artifact badge |
| ⭐ **prompt 是否公开** | 🟢 | 论文 Fig. 3 / 4 / 5 | ⭐ **三张模板逐字可读**（B3 已全文抄录）。⚠️ 仓库里另有两条 IKE 专用 prompt（`IKE_States` / `IKE_Pathrule`），⛔ **与论文模板不是同一批** |

### ⛔ 为什么代码判 🟠 而不是 🟢

⭐ 仓库**不是空壳**（11 个真实 Python 文件、约 31 KB 源码，⛔ 与 FlowFSM 那次的「只有 README + .gitignore」不同类），⛔ 但**它不是论文那条流水线的实现**。逐项对照（全部 **M**，我读了每个文件）：

| 论文说有 | 仓库里 |
| :-- | :-- |
| 三阶段 CoT（code paths → states/messages → transitions） | ⛔ **没有**。只有两条 IKE 专用 prompt 常量，⛔ 与 Fig. 3/4/5 的模板**都不匹配** |
| 逐 state 展开 `{current_state}` | ⛔ **没有**任何遍历状态生成 prompt 的代码 |
| 20 次采样 · 80% 共识 | ⛔ **没有**投票、计数或阈值逻辑 |
| JSON 后处理 | ⛔ **没有**。`chat_loop()` 只把 answer 打印并写 log |
| 关键词集「可低成本扩展到新协议」 | ⛔ 5 条逐协议手写正则（见 B5） |
| FAISS 向量库 | ⭐ `llm.py` 确实用 FAISS；⛔ 但 `chatProtocol.py` / `chatIKE.py` 用 **Chroma**，⚠️ 两套并存 |
| 自动化流水线 | ⛔ `main.py` 的入口是 `chat` → `llm.chat_loop()` → `while True: query = input("👉 ")`，⭐ **人工 REPL** |

⭐ 另有若干「实验脚手架未清理」的痕迹：⛔ 作者本机绝对路径 `/home/why/sec_sea/...` 硬编码在多处、⛔ `chatProtocol.py` 里留着一个向第三方代理 `oa.api2d.net` 发「讲个笑话」的 `test()` 函数、⛔ `main.py` 的 `create_vectores()` 里 codebase 列表被注释成只剩一个、⛔ `consts.py` 里 `OPENAI_API_KEY = "****"`、⛔ README 仅 **99 字节**（一行标题，⛔ 无安装、⛔ 无运行、⛔ 无复现说明）、⛔ 无 license。

⭐ **结论**：⭐ 拿它**读设计意图**可以，⛔ 拿它**复现表 IV 的数字不可能** —— ⭐ 缺 ground truth、缺共识逻辑、缺驱动脚本。

---

## E. ⭐ 对 M1 的意义

### 1 · ⭐ 可取之处

1. ⭐⭐ **「让 LLM 自造闭合集，再在其上受限生成」这个两段式，值得作为我们闭合词表的补充形态考虑。** ⭐ 具体搬法：⭐ 我们的 19 条谓词词表是**全语料共用**的，⛔ 因此单条需求里「该问哪个元素」仍然是开放的；⭐ 可以照他们阶段 ② → ③ 的做法，**先用一次调用把这份制品里的元素名 / 事件名 / 变量名抽成一个显式集合，再把这个集合整体灌进断言构造的 prompt**，⛔ 让模型不能引用集合外的名字。⚠️ 这直击我们「问了没答对」那 52 位里的一部分（引用了不存在的元素）。
2. ⭐⭐ **多次采样取近似交集，是 precision 工具而非只是度量工具 —— 而且 recall 代价可能远小于直觉。** ⭐ 他们用 20 采样 / 80% 阈值（≈ 至少 16/20 命中）过滤，⭐ recall 仍有 87.09%。⭐ 对 M1 的直接含义：⭐ 我们的 `hit@all`（3/3）目前只是**报告口径**，⛔ 但完全可以反过来当**多报抑制器**用 —— ⚠️ 而这条外部证据说明它不一定把 recall 砍到见骨。⛔ 必须自己测，⛔ 不能照抄他们的阈值。
3. ⭐ **不利结果的写法可以直接抄。** ⭐ 被 baseline 在某格打败时，他们的做法是「保留不利指标 + 在同一格换一个更细的绝对数字论证鲁棒性」（RTSP：precision 输、correct 条数赢 12 vs 11）。⚠️ 我们手上正有 **−15.82pp**，⭐ 这个「不改口径、不删格子、换粒度补充论证」的写法是可用的范式。
4. ⭐ **prompt 模板全文进正文**（三张图逐字），⭐ 而不是塞进不存在的附录或「见仓库」。⭐ 这是低成本高可信的做法，⭐ 我们的 prompt 也应当这样处理。

### 2 · ⛔ 不可取 / 陷阱

1. ⛔⛔ **手上有 sound oracle 却不用 —— 与我们犯的是同一类错，而且更彻底。** ⭐ 我们至少把 pyfcstm 放在了**求值端**；⛔ 他们的被测对象是能编译能跑的 C 代码，⛔ 编译器 / 测试 / 符号执行**一个都没进环**，⛔ AFLNet 也只在下游消费而不回流。⭐ 这条反过来加强了 M1 第二条设计原则：⭐ **有 oracle 不放进裁决端，是这一带的普遍缺陷，不是我们独有的疏忽。**
2. ⛔ **「按样本手写规则」这个坑，他们踩了而且踩在最要紧的部件上。** ⛔ 贡献最大的 code filter（+41pp / +55pp）是逐协议手写的正则，⛔ 其中若干条是**具体实现的标识符**而非 RFC 术语。⚠️ 对我们的警示是双向的：⭐ 一方面这说明「方法的主要增益来自一个按样本调过的部件」在这一带能通过评审，⛔ 另一方面**我们不能这么干** —— 本仓库 §3.5 把这类东西定为 C 级，⭐ 而且我们**没有 hold-out**，⛔ 一旦被指出就无从辩护。
3. ⛔ **20 次采样 / 80% 阈值一个敏感性分析都没有。** ⛔ 两个数字都是拍的，⛔ 没有「10 次够不够」「70% 会怎样」。⚠️ 我们若引入类似机制，⭐ 必须把阈值扫描连同结果一起报，⛔ 否则就是同一个洞。
4. ⛔ **`partially correct` 一律记为错，同时进 precision 与 recall 的分母。** ⭐ 口径本身可辩（严格），⛔ 但它让「差一点」与「完全错」不可区分 —— ⚠️ 我们的五类多报分类比这个更细，⭐ **不要为了对齐外部口径而退化。**

### 3 · ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⛔⛔ **输入侧完全不同，C-③ 那一格在这篇里是空的。** ⭐ 他们的输入是**源码**，⛔ 不是规约文本；⭐ FSM 元素的溯源锚点是「文件路径」（`{code_path}`），⛔ 不是「规约的哪一句」。⛔ **全文没有任何「规约文本 ↔ 状态机元素」的对应关系机制。** ⚠️ 唯一涉及 RFC 的地方是 Table I：⛔ **两名领域专家手工**比对 4 个 IKEv2 实现与 RFC 7296 的状态 / 迁移**总数**（RFC 8/17 · strongSwan 8/23 · libopenikev2 22/65 · Libreswan 22/29 · openswan 12/19），⛔ 只有计数、⛔ 没有逐条对应、⛔ 没有自动化。⭐ §V-C 的实现间差异同样是**人工对读**两张推出来的 FSM（举了 Child SA 的例子），⛔ 不是机械 diff。
2. ⛔ **覆盖缺口只以评测量存在，不是流水线产物。** ⭐ `not found`（NF）确实就是「ground truth 有而推出的 FSM 没有」，⭐ 且逐协议给了数（IKEv2 NF=4 · TLS 1.3 NF=1 · TLS 1.2 NF=2 · BGP NF=1 · RTSP NF=6 · L2TP NF=2）。⛔ **但这是评测时对着答案数出来的，流水线自己不知道自己漏了什么** —— ⛔ 它没有任何「我读到了这段但没能产出迁移」的结构化诊断。⭐ 我们要的 coverage gap 是**运行时自报**的，⛔ 这篇给不出先例。
3. ⚠️ **模型代次差两代。** ⭐ GPT-4（8K 上下文那一代）· 单模型 · `temperature 0.2`。⛔ 他们那三个挑战里有两个（上下文窗口不够、需要分块）在今天的 SOTA 上已大幅缓解，⛔ 所以**他们的 RAG 架构的必要性论证今天不一定成立**，⚠️ 但「让模型自造闭合集」与「多采样取共识」两条不依赖窗口大小。
4. ⚠️ **他们的任务没有「制品是错的」这个前提。** ⭐ 他们要的是**忠实**还原实现里的 FSM（实现即真值）；⛔ 我们要的是**指出制品与需求不符**。⭐ 因此他们的 precision 惩罚的是「编造」，⛔ 而我们的多报惩罚的是「误报缺陷」—— ⛔ 两个 precision 不是同一个东西，⛔ 数字不可比。

---

## F. ⛔ 存疑与未核项

1. ⚠️ **IEEE camera-ready 未取到** —— 已试过 `curl -L https://ieeexplore.ieee.org/document/11143461`（返回 **HTTP 202 / 0 字节**，bot 拦截）。⭐ 本卡所有 **M** 级逐字片段**全部出自 arXiv v4（2025-03-27）**；⭐ 元数据（标题 / venue / 页码 / 日期 / 作者列表）经 Crossref 核实与 arXiv 一致，⚠️ 但**正文措辞、表格数字是否在 camera-ready 中被改动，无法排除**。
2. ⚠️ **「20 次采样」与「10 次运行取均值」的嵌套关系不明** —— 是「10 × (20 采样 + 投票)」共 200 次调用，还是这两个数字指同一批采样的不同切法，⛔ 原文两处（§IV-B 与 §V-A）**没有交代**。⚠️ 这影响成本估算与「多采样收益」的解读。⛔ 论文全文无 token / 费用数据，⛔ 无法反推。
3. ⚠️ **四分类判定（C / PC / IC / NF）的执行者与流程未提供** —— 原文只说 ground truth 由 3 名专家建。⛔ 判定是同一批专家做的、还是作者自己做的、⛔ 是否盲判、⛔ 有无第二人复核，**全部未提供**；⛔ 无 $\kappa$、⛔ 无一致率。⚠️ 而 PC 与 IC 的分界（`If more than two elements of T are incorrect`）本身在三元组上就有歧义（⛔ 三个元素里「多于两个错」= 三个全错？那「恰好两个错」落哪一档？⛔ 原文未定义）。
4. ⚠️ **80% 阈值与 `MaxChunkSize` / `MinChunkSize` / overlap / `k` 的具体取值未在论文给出** —— ⭐ 仓库 `consts.py` 的 `DEFAULT_CONFIG` 给了 `chunk_size 2056` / `chunk_overlap 256` / `k 4` / `temperature 0.5`，⛔ 但 `temperature` 与论文说的 0.2 **不一致**，⚠️ 所以**不能认定这份 config 就是实验用的配置**。
5. ⚠️ **CCF 等级未经本库核验** —— [ccf_venues/](../../../../../ccf_venues/) 里 **IWQoS 无条目**（`grep -riE "iwqos"` 零命中）。⭐ 「B 类 · 计算机网络」来自 CCF 官方目录的领域分类，⛔ 但我**没有直连 ccf.org.cn 的官方 PDF 逐条核对**，⭐ 故标 **S**。⚠️ 另注：2026-03 CCF 完成了新一轮目录公示修订，⛔ 等级可能已变。
6. ⚠️ **仓库与论文不匹配的原因无法判定** —— ⛔ 无法区分「作者只放了早期探索代码」与「真实流水线本就是人工 REPL 驱动、论文把它描述成了自动化」。⭐ 仓库 HEAD `df3fceb053`、⛔ 无 tag、⛔ 无 release、⛔ 无 commit 说明可查投稿对应版本。⚠️ 这两种可能对「这套方法的自动化程度」判断完全不同，⛔ **本卡不下结论**。
7. ⚠️ **Fig. 1（系统总览）、Fig. 2（分块流程）、Fig. 6（实现差异）、Fig. 7（覆盖率曲线）为位图，文字未提取** —— ⭐ 已从 PDF 成功提取 Fig. 3/4/5 的 prompt 文字（那三张是文本层），⛔ 但上述四张图内的标签、数值与图例**未读**。⚠️ 因此 §V-D 的覆盖率**绝对值**只有正文给的相对提升（31.80% / 30.39% / 22.66% / 21.99%），⛔ 曲线本身与置信区间宽度未核。
