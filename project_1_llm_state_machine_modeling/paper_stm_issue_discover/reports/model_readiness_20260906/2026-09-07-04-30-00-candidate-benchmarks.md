# E1 全候选公开 benchmark 与任务选型

核验日期：2026-09-07。AA 数据冻结于 2026-09-06 约 23:30 CST，采用 **Intelligence Index v4.2 / AA-LCR v1.1**；这是公开能力背景，与 E1 接入 smoke、Paper1 正式效果实验分别记录。正文 `[src-*]` / `[clm-*]` 指向文末证据链。[src-aa]

## 1. 范围与选型

覆盖本轮已经调查的 17 个模型身份、20 个公开推理变体：Luna、Sonnet、Haiku，Gemini 3.5/3.6/3.7/3.8，Qwen3.8-27B、Qwen3.6-35B-A3B/27B，Muse、Gemma、Nemotron、GLM-4.7-Flash、gpt-oss-20b、Llama3.3，以及因总参数超限被排除的 GLM-5.3-Flash。Gemini 3.6 是辅助网关探针对象；Haiku、Qwen3.6-35B 的非推理行和 Qwen3.8 low 行用于澄清档位。范围来自既有[商用调查](./2026-09-06-11-53-00-commercial-models.md)和[开放调查](./2026-09-06-11-53-00-open-models.md)，不把模型卡中每个背景对手、文献用过的每个历史型号变成新部署候选。[clm-scope]

用户优先组合为 **GPT-5.6 Luna + Claude Sonnet 5 + Qwen3.8-27B + Muse Glimmer-30B**。Luna 保持已有研究锚点，Sonnet 提供另一商用模型族，Qwen 和 Muse 提供两种开放模型族且总参数均小于 100B。选择依据是公开能力、组合覆盖和实际接入可行性；不按 ours 相对 baseline 的有利效果挑模型，也不宣称四款是本任务 SOTA。Haiku 保留备选，Gemini 的公开成绩不能消除当前渠道的 504/schema 缺陷。[clm-choice]

任务真正需要的是：读完长需求与多轮修订历史、遵守精确字段约束、依据给定证据作判断、可靠输出可执行工具参数。因此优先看 LCR、IFBench、知识校准与结构化能力证据；编程和终端 agent 指标只作补充。下面的公开任务与状态机缺陷发现有距离，最终效果仍须由 E2 同 backbone 的 `ours vs baseline` 配对实验回答。[clm-relevance]

## 2. 独立评测矩阵

所有数值由 [AA 原始 HTML/RSC 快照](./evidence/benchmarks_20260906.zip)中的精确 slug 提取，每个数字链接到对应公开模型页；完整精度、effort 元数据、快照来源和哈希保存在 [机器表](./evidence/benchmarks_20260906.json)。发布者/评测者为 **Artificial Analysis，独立评测**。页面标签没有提供不可变的 API revision/权重 commit，不能把 AA 型号与本地 checkpoint 视为已独立认证的同一 revision。[src-aa] [clm-aa]

除 Omni 外本表为百分制，越高越好；Omni 是 [-100,100] 净分，越高越好，保留四位小数。`未取得可核验结果` 表示本次快照缺测，不能记 0，也不能用相邻型号补齐。AA 的 GPQA 和 IFBench 在该快照中是独立列，**不属于 v4.2 Index 的组成项**。[src-methodology]

<!-- aa-task -->
| 精确公开变体 / AA 档位 | LCR v1.1 | IFBench | Omni 净分 | GPQA Diamond | HLE text | SciCode |
|---|---:|---:|---:|---:|---:|---:|
| [GPT-5.6 Luna (max)](https://artificialanalysis.ai/models/gpt-5-6-luna) | [83.7](https://artificialanalysis.ai/models/gpt-5-6-luna) | 未取得可核验结果 | [-10.2833](https://artificialanalysis.ai/models/gpt-5-6-luna) | [91.1](https://artificialanalysis.ai/models/gpt-5-6-luna) | [39.5](https://artificialanalysis.ai/models/gpt-5-6-luna) | [53.6](https://artificialanalysis.ai/models/gpt-5-6-luna) |
| [Claude Sonnet 5 (Adaptive Reasoning, Max Effort)](https://artificialanalysis.ai/models/claude-sonnet-5) | [82.0](https://artificialanalysis.ai/models/claude-sonnet-5) | 未取得可核验结果 | [+16.4500](https://artificialanalysis.ai/models/claude-sonnet-5) | [91.1](https://artificialanalysis.ai/models/claude-sonnet-5) | [41.3](https://artificialanalysis.ai/models/claude-sonnet-5) | [54.3](https://artificialanalysis.ai/models/claude-sonnet-5) |
| [Claude 4.5 Haiku (Reasoning)](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | [74.3](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | [54.3](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | [-4.3667](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | [67.2](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | [10.4](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | [42.2](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) |
| [Claude 4.5 Haiku (Non-reasoning)](https://artificialanalysis.ai/models/claude-4-5-haiku) | [49.7](https://artificialanalysis.ai/models/claude-4-5-haiku) | [42.0](https://artificialanalysis.ai/models/claude-4-5-haiku) | [-7.5667](https://artificialanalysis.ai/models/claude-4-5-haiku) | [64.6](https://artificialanalysis.ai/models/claude-4-5-haiku) | [4.2](https://artificialanalysis.ai/models/claude-4-5-haiku) | 未取得可核验结果 |
| [Gemini 3.5 Flash (high)](https://artificialanalysis.ai/models/gemini-3-5-flash) | [73.3](https://artificialanalysis.ai/models/gemini-3-5-flash) | [76.3](https://artificialanalysis.ai/models/gemini-3-5-flash) | [+21.1833](https://artificialanalysis.ai/models/gemini-3-5-flash) | [92.2](https://artificialanalysis.ai/models/gemini-3-5-flash) | [42.7](https://artificialanalysis.ai/models/gemini-3-5-flash) | [53.9](https://artificialanalysis.ai/models/gemini-3-5-flash) |
| [Gemini 3.6 Flash (high)](https://artificialanalysis.ai/models/gemini-3-6-flash) | [80.0](https://artificialanalysis.ai/models/gemini-3-6-flash) | 未取得可核验结果 | [+22.1333](https://artificialanalysis.ai/models/gemini-3-6-flash) | [92.8](https://artificialanalysis.ai/models/gemini-3-6-flash) | [40.8](https://artificialanalysis.ai/models/gemini-3-6-flash) | [53.4](https://artificialanalysis.ai/models/gemini-3-6-flash) |
| [Gemini 3.7 Flash (high)](https://artificialanalysis.ai/models/gemini-3-7-flash) | [81.7](https://artificialanalysis.ai/models/gemini-3-7-flash) | 未取得可核验结果 | [+26.4833](https://artificialanalysis.ai/models/gemini-3-7-flash) | [94.5](https://artificialanalysis.ai/models/gemini-3-7-flash) | [47.9](https://artificialanalysis.ai/models/gemini-3-7-flash) | [57.2](https://artificialanalysis.ai/models/gemini-3-7-flash) |
| [Gemini 3.8 Flash (high)](https://artificialanalysis.ai/models/gemini-3-8-flash) | [81.3](https://artificialanalysis.ai/models/gemini-3-8-flash) | 未取得可核验结果 | [+29.5500](https://artificialanalysis.ai/models/gemini-3-8-flash) | [95.3](https://artificialanalysis.ai/models/gemini-3-8-flash) | [47.8](https://artificialanalysis.ai/models/gemini-3-8-flash) | [56.6](https://artificialanalysis.ai/models/gemini-3-8-flash) |
| [Qwen3.8 27B (xhigh)](https://artificialanalysis.ai/models/qwen3-8-27b) | [82.0](https://artificialanalysis.ai/models/qwen3-8-27b) | 未取得可核验结果 | [-9.9833](https://artificialanalysis.ai/models/qwen3-8-27b) | [90.5](https://artificialanalysis.ai/models/qwen3-8-27b) | [33.9](https://artificialanalysis.ai/models/qwen3-8-27b) | [46.6](https://artificialanalysis.ai/models/qwen3-8-27b) |
| [Qwen3.8 27B (low)](https://artificialanalysis.ai/models/qwen3-8-27b-low) | [77.3](https://artificialanalysis.ai/models/qwen3-8-27b-low) | 未取得可核验结果 | [-26.6667](https://artificialanalysis.ai/models/qwen3-8-27b-low) | [84.5](https://artificialanalysis.ai/models/qwen3-8-27b-low) | [14.0](https://artificialanalysis.ai/models/qwen3-8-27b-low) | [40.0](https://artificialanalysis.ai/models/qwen3-8-27b-low) |
| [Qwen3.6 35B A3B (Reasoning)](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | [71.7](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | [64.4](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | [-22.1833](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | [84.1](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | [22.2](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | 未取得可核验结果 |
| [Qwen3.6 35B A3B (Non-reasoning)](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | [64.3](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | [36.2](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | [-60.0167](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | [81.7](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | [13.9](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | 未取得可核验结果 |
| [Qwen3.6 27B (Reasoning)](https://artificialanalysis.ai/models/qwen3-6-27b) | [77.3](https://artificialanalysis.ai/models/qwen3-6-27b) | [67.6](https://artificialanalysis.ai/models/qwen3-6-27b) | [-20.0167](https://artificialanalysis.ai/models/qwen3-6-27b) | [84.2](https://artificialanalysis.ai/models/qwen3-6-27b) | [23.1](https://artificialanalysis.ai/models/qwen3-6-27b) | 未取得可核验结果 |
| [Muse Glimmer (high)](https://artificialanalysis.ai/models/muse-glimmer) | [83.3](https://artificialanalysis.ai/models/muse-glimmer) | 未取得可核验结果 | [-32.8500](https://artificialanalysis.ai/models/muse-glimmer) | [83.5](https://artificialanalysis.ai/models/muse-glimmer) | [22.0](https://artificialanalysis.ai/models/muse-glimmer) | [44.9](https://artificialanalysis.ai/models/muse-glimmer) |
| [Gemma 4 31B (Reasoning)](https://artificialanalysis.ai/models/gemma-4-31b) | [69.7](https://artificialanalysis.ai/models/gemma-4-31b) | [75.6](https://artificialanalysis.ai/models/gemma-4-31b) | [-47.9333](https://artificialanalysis.ai/models/gemma-4-31b) | [85.7](https://artificialanalysis.ai/models/gemma-4-31b) | [23.6](https://artificialanalysis.ai/models/gemma-4-31b) | [45.5](https://artificialanalysis.ai/models/gemma-4-31b) |
| [Nemotron 3.5 Lightning (Reasoning, effort 未披露)](https://artificialanalysis.ai/models/nemotron-3-5-lightning) | [60.3](https://artificialanalysis.ai/models/nemotron-3-5-lightning) | 未取得可核验结果 | [-17.7167](https://artificialanalysis.ai/models/nemotron-3-5-lightning) | [74.3](https://artificialanalysis.ai/models/nemotron-3-5-lightning) | [10.6](https://artificialanalysis.ai/models/nemotron-3-5-lightning) | [32.1](https://artificialanalysis.ai/models/nemotron-3-5-lightning) |
| [GLM-4.7-Flash (Reasoning)](https://artificialanalysis.ai/models/glm-4-7-flash) | [41.7](https://artificialanalysis.ai/models/glm-4-7-flash) | [60.8](https://artificialanalysis.ai/models/glm-4-7-flash) | [-62.6167](https://artificialanalysis.ai/models/glm-4-7-flash) | [58.1](https://artificialanalysis.ai/models/glm-4-7-flash) | [7.6](https://artificialanalysis.ai/models/glm-4-7-flash) | 未取得可核验结果 |
| [gpt-oss-20b (high)](https://artificialanalysis.ai/models/gpt-oss-20b) | [34.7](https://artificialanalysis.ai/models/gpt-oss-20b) | [65.1](https://artificialanalysis.ai/models/gpt-oss-20b) | [-63.0500](https://artificialanalysis.ai/models/gpt-oss-20b) | [68.8](https://artificialanalysis.ai/models/gpt-oss-20b) | [11.0](https://artificialanalysis.ai/models/gpt-oss-20b) | 未取得可核验结果 |
| [Llama 3.3 Instruct 70B (Non-reasoning)](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | [15.7](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | [47.1](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | [-54.1667](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | [49.8](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | [3.6](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | 未取得可核验结果 |
| [GLM-5.3-Flash (max)](https://artificialanalysis.ai/models/glm-5-3-flash) | [80.0](https://artificialanalysis.ai/models/glm-5-3-flash) | 未取得可核验结果 | [+7.4667](https://artificialanalysis.ai/models/glm-5-3-flash) | [91.2](https://artificialanalysis.ai/models/glm-5-3-flash) | [39.9](https://artificialanalysis.ai/models/glm-5-3-flash) | [51.6](https://artificialanalysis.ai/models/glm-5-3-flash) |
<!-- /aa-task -->

### 评测设置与可比边界

| 列 | 数据/版本与判分 | 任务参考价值与限制 |
|---|---|---|
| AA-LCR v1.1 | 100 题，约 100K 输入（cl100k_base），跨约 230 份长文档；3 repeats、pass@1，Luna medium 作答案等价判断 | 长文档推理背景；v1.1 修正 16 个答案并改变系统提示与 grader，不能混用 8 月 v1.0 数字；不是输出 schema 测试 |
| IFBench | AllenAI IFBench_test 294 单轮指令，5 repeats，官方规则判分、pass@1 | 精确格式/计数等约束遵循；不等于多阶段 Pydantic/schema 或工具调用成功率 |
| AA-Omniscience | 6,000 问题、42 topics；正确奖励、错误惩罚、不惩罚拒答的净分 | 知识可靠性背景；不是 Paper1 幻觉率或 precision |
| GPQA Diamond | 198 道科学四选一，regex 抽取，pass@1 | 科学推理背景；不能直接推断状态机诊断准确率 |
| HLE text | 2025-05 修订集的 2,158 道 text-only 问题，no tools，等价判断、pass@1 | 不同于 full-set、with-tools、HLE-Verified |
| SciCode | 288 test subproblems，scientist-annotated background prompt，代码执行、pass@1 | 给定背景下的科学编程；不等于严格工具参数能力 |

AA 总体采样为非推理模型 temperature=0、推理模型 temperature=0.6，模型作者另有推荐时采用推荐值；非推理输出通常 16,384，推理模型按作者允许的最大输出逐模型设定。API 失败最多重试 30 次。快照没有为每一个表格单元披露全部实际请求，**不能声称逐模型温度、输出预算与 E1 完全一致**；本轮 E1 是零 transport retries。上述评测细节见[方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking)。[src-methodology] [clm-settings]

Omni 的 `hallucinationRate` 定义为 `incorrect / (incorrect + partial answers + not attempted)`，分母是 non-correct responses，不是全部题目。不得拿该字段与 accuracy 直接相减计算净分；本表直接保留发布者的 `omniscience` 净分字段。[src-omni] [clm-omni]

### 编程与综合背景

Index 为 AA v4.2 发布分数；Terminal-Bench 是 **v2.1**、独立 harness 的 pass@1 百分制，均越高越好。Index 的组成权重见快照方法页，不能与旧 v4.1.1 混排。Terminal-Bench 评估整套终端任务，不作为结构化抽取或工具参数可靠性的直接证据。[src-aa] [src-methodology]

<!-- aa-general -->
| 精确公开变体 / AA 档位 | Intelligence Index v4.2 | Terminal-Bench v2.1 |
|---|---:|---:|
| [GPT-5.6 Luna (max)](https://artificialanalysis.ai/models/gpt-5-6-luna) | [43.4](https://artificialanalysis.ai/models/gpt-5-6-luna) | [80.9](https://artificialanalysis.ai/models/gpt-5-6-luna) |
| [Claude Sonnet 5 (Adaptive Reasoning, Max Effort)](https://artificialanalysis.ai/models/claude-sonnet-5) | [45.1](https://artificialanalysis.ai/models/claude-sonnet-5) | [80.5](https://artificialanalysis.ai/models/claude-sonnet-5) |
| [Claude 4.5 Haiku (Reasoning)](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | [22.5](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | [44.2](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) |
| [Claude 4.5 Haiku (Non-reasoning)](https://artificialanalysis.ai/models/claude-4-5-haiku) | [17.4](https://artificialanalysis.ai/models/claude-4-5-haiku) | 未取得可核验结果 |
| [Gemini 3.5 Flash (high)](https://artificialanalysis.ai/models/gemini-3-5-flash) | [39.7](https://artificialanalysis.ai/models/gemini-3-5-flash) | [78.7](https://artificialanalysis.ai/models/gemini-3-5-flash) |
| [Gemini 3.6 Flash (high)](https://artificialanalysis.ai/models/gemini-3-6-flash) | [40.3](https://artificialanalysis.ai/models/gemini-3-6-flash) | [77.5](https://artificialanalysis.ai/models/gemini-3-6-flash) |
| [Gemini 3.7 Flash (high)](https://artificialanalysis.ai/models/gemini-3-7-flash) | [45.2](https://artificialanalysis.ai/models/gemini-3-7-flash) | [85.8](https://artificialanalysis.ai/models/gemini-3-7-flash) |
| [Gemini 3.8 Flash (high)](https://artificialanalysis.ai/models/gemini-3-8-flash) | [47.1](https://artificialanalysis.ai/models/gemini-3-8-flash) | [87.6](https://artificialanalysis.ai/models/gemini-3-8-flash) |
| [Qwen3.8 27B (xhigh)](https://artificialanalysis.ai/models/qwen3-8-27b) | [41.4](https://artificialanalysis.ai/models/qwen3-8-27b) | [79.8](https://artificialanalysis.ai/models/qwen3-8-27b) |
| [Qwen3.8 27B (low)](https://artificialanalysis.ai/models/qwen3-8-27b-low) | [33.8](https://artificialanalysis.ai/models/qwen3-8-27b-low) | [67.4](https://artificialanalysis.ai/models/qwen3-8-27b-low) |
| [Qwen3.6 35B A3B (Reasoning)](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | [26.2](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | [44.9](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) |
| [Qwen3.6 35B A3B (Non-reasoning)](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | [17.1](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | [41.6](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) |
| [Qwen3.6 27B (Reasoning)](https://artificialanalysis.ai/models/qwen3-6-27b) | [29.0](https://artificialanalysis.ai/models/qwen3-6-27b) | [60.7](https://artificialanalysis.ai/models/qwen3-6-27b) |
| [Muse Glimmer (high)](https://artificialanalysis.ai/models/muse-glimmer) | [24.4](https://artificialanalysis.ai/models/muse-glimmer) | [51.7](https://artificialanalysis.ai/models/muse-glimmer) |
| [Gemma 4 31B (Reasoning)](https://artificialanalysis.ai/models/gemma-4-31b) | [22.2](https://artificialanalysis.ai/models/gemma-4-31b) | [43.4](https://artificialanalysis.ai/models/gemma-4-31b) |
| [Nemotron 3.5 Lightning (Reasoning, effort 未披露)](https://artificialanalysis.ai/models/nemotron-3-5-lightning) | [16.4](https://artificialanalysis.ai/models/nemotron-3-5-lightning) | [24.3](https://artificialanalysis.ai/models/nemotron-3-5-lightning) |
| [GLM-4.7-Flash (Reasoning)](https://artificialanalysis.ai/models/glm-4-7-flash) | [16.6](https://artificialanalysis.ai/models/glm-4-7-flash) | 未取得可核验结果 |
| [gpt-oss-20b (high)](https://artificialanalysis.ai/models/gpt-oss-20b) | [9.1](https://artificialanalysis.ai/models/gpt-oss-20b) | [13.9](https://artificialanalysis.ai/models/gpt-oss-20b) |
| [Llama 3.3 Instruct 70B (Non-reasoning)](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | [3.7](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | [4.9](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) |
| [GLM-5.3-Flash (max)](https://artificialanalysis.ai/models/glm-5-3-flash) | [46.2](https://artificialanalysis.ai/models/glm-5-3-flash) | [84.3](https://artificialanalysis.ai/models/glm-5-3-flash) |
<!-- /aa-general -->

### 严格结构化与工具参数的公开缺测

以下专门保留本轮没有取得**精确变体、同版本、同 harness、同 effort**成绩的项目。已定位评测入口或论文，不等于拿到了这些模型的可比较结果。E1 的真实 function/tool、schema 修正和 method 回执是接入证据，不填进这些公开榜单空位。[clm-structure]

<!-- aa-structure -->
| 精确公开变体 / AA 档位 | 严格 JSON Schema | SOB | LEDGER | 同口径 BFCL |
|---|---|---|---|---|
| [GPT-5.6 Luna (max)](https://artificialanalysis.ai/models/gpt-5-6-luna) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Claude Sonnet 5 (Adaptive Reasoning, Max Effort)](https://artificialanalysis.ai/models/claude-sonnet-5) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Claude 4.5 Haiku (Reasoning)](https://artificialanalysis.ai/models/claude-4-5-haiku-reasoning) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Claude 4.5 Haiku (Non-reasoning)](https://artificialanalysis.ai/models/claude-4-5-haiku) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Gemini 3.5 Flash (high)](https://artificialanalysis.ai/models/gemini-3-5-flash) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Gemini 3.6 Flash (high)](https://artificialanalysis.ai/models/gemini-3-6-flash) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Gemini 3.7 Flash (high)](https://artificialanalysis.ai/models/gemini-3-7-flash) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Gemini 3.8 Flash (high)](https://artificialanalysis.ai/models/gemini-3-8-flash) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Qwen3.8 27B (xhigh)](https://artificialanalysis.ai/models/qwen3-8-27b) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Qwen3.8 27B (low)](https://artificialanalysis.ai/models/qwen3-8-27b-low) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Qwen3.6 35B A3B (Reasoning)](https://artificialanalysis.ai/models/qwen3-6-35b-a3b) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Qwen3.6 35B A3B (Non-reasoning)](https://artificialanalysis.ai/models/qwen3-6-35b-a3b-non-reasoning) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Qwen3.6 27B (Reasoning)](https://artificialanalysis.ai/models/qwen3-6-27b) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Muse Glimmer (high)](https://artificialanalysis.ai/models/muse-glimmer) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Gemma 4 31B (Reasoning)](https://artificialanalysis.ai/models/gemma-4-31b) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Nemotron 3.5 Lightning (Reasoning, effort 未披露)](https://artificialanalysis.ai/models/nemotron-3-5-lightning) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [GLM-4.7-Flash (Reasoning)](https://artificialanalysis.ai/models/glm-4-7-flash) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [gpt-oss-20b (high)](https://artificialanalysis.ai/models/gpt-oss-20b) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [Llama 3.3 Instruct 70B (Non-reasoning)](https://artificialanalysis.ai/models/llama-3-3-instruct-70b) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
| [GLM-5.3-Flash (max)](https://artificialanalysis.ai/models/glm-5-3-flash) | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 |
<!-- /aa-structure -->

## 3. 作者发布数字，单独保留口径

下列数字来自 09-06 已存档的一手模型卡/发布页，核验于 09-07。每个单元链接至原发布者。表中均为百分制、越高越好；不同版本在单元明确列出。没有明确 effort 的单元保留“作者未统一披露”，不据部署默认值补写。作者自测、作者转引 AA、AA 独立矩阵是三种来源关系，不能合成排行榜。[src-vendor] [clm-vendor]

| 精确模型 / 发布评测档位 | IFBench | GPQA Diamond | HLE | SWE-bench Verified | SWE-bench Pro | Terminal-Bench | 其他已调查指标 |
|---|---|---|---|---|---|---|---|
| GPT-5.6 Luna / 未统一披露 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 模型/API 能力声明不转成分数 |
| Sonnet 5 / 发布页设置 | 未取得可核验结果 | 未取得可核验结果 | no tools [43.2][sonnet]；with tools [57.4][sonnet] | [85.2][sonnet] | [63.2][sonnet] | v2.1 [80.4][sonnet] | SWE Multilingual [78.3][sonnet]；OSWorld Verified [81.2][sonnet] |
| Haiku 4.5 / launch thinking | 未取得可核验结果 | [73.0][haiku] | 未取得可核验结果 | [73.3][haiku] | 未取得可核验结果 | 版本未注明：no thinking [40.21][haiku]；32K thinking [41.75][haiku] | 其余 launch 评测使用 128K thinking budget，与当前 64K API 输出规格分开 |
| Gemini 3.5 Flash / model card | 未取得可核验结果 | 未取得可核验结果 | full-set [40.2][gemini35] | 未取得可核验结果 | single attempt [55.1][gemini35] | v2.1/Terminus-2 [76.2][gemini35] | MRCR v2 8-needle/128K [77.3][gemini35]；MCP Atlas [83.6][gemini35]；Toolathlon [56.5][gemini35]；OSWorld Verified [78.4][gemini35]；ARC-AGI-2 [72.1][gemini35] |
| Gemini 3.6 Flash / 未统一披露 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 辅助渠道有 API 记录，不据渠道 ID 推定官方规格 |
| Gemini 3.7 Flash / 未统一披露 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 公开 AA 行与网关身份分开记录 |
| Gemini 3.8 Flash / 发布产品页 | 未取得可核验结果 | 未取得可核验结果 | HLE-Verified [54.9][gemini38] | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | Vals Finance Agent v2 [61.4][gemini38]；Harvey Legal Agent [10.0][gemini38]；DeepSWE 图未标精确值，不估读 |
| Qwen3.8-27B / 卡片默认 xhigh，逐项预算见脚注 | [79.5][qwen38] | [89.2][qwen38] | [30.8][qwen38]（卡片 HLE，未视为 AA text 口径） | 未取得可核验结果 | 作者修订集 [61.7][qwen38] | v2.1/Terminus [73.0][qwen38] | 作者与 AA 的独立测值不同，均保留 |
| Qwen3.6-35B-A3B / thinking | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | [73.4][qwen36] | 作者修订集 [49.5][qwen36] | v2.0 [51.5][qwen36] | AIME26 [92.7][qwen36]；MCP-Atlas [62.8][qwen36] |
| Qwen3.6-27B / Muse 卡的 thinking 对照 | [70.8][muse] | [84.2][muse]（转引 AA） | text [23.1][muse]（转引 AA） | [77.2][muse] | [50.2][muse] | v2.1/terminus2 [60.7][muse] | Muse 作者对照列；并非本轮另做部署验收 |
| Muse Glimmer-30B / high | [77.0][muse] | [83.5][muse]（转引 AA） | text [22.0][muse]（转引 AA） | [76.0][muse] | [51.2][muse] | v2.1/terminus2 [51.7][muse] | AIME26 [94.7][muse]；SciCode [43.6][muse]；OSWorld Verified [65.9][muse] |
| Gemma4-31B-it / thinking，Google 卡 | 未取得可核验结果 | [84.3][gemma] | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | MMLU Pro [85.2][gemma]；AIME26 [89.2][gemma]；LiveCodeBench v6 [80.0][gemma] |
| Nemotron-3.5-Lightning-30B-A3B-BF16 / reasoning | loose [71.88][nemotron] | no tools [75.44][nemotron] | text/no tools [11.72][nemotron] | [51.56][nemotron] | 未取得可核验结果 | v2.1 [24.58][nemotron] | MMLU Pro [81.94][nemotron]；SWE Multilingual [39.33][nemotron]；PinchBench [85.37][nemotron] |
| GLM-4.7-Flash / 作者卡 | 未取得可核验结果 | [75.2][glm47] | 未取得可核验结果 | [59.2][glm47] | 未取得可核验结果 | 未取得可核验结果 | AIME25 [91.6][glm47] |
| gpt-oss-20b / 官方指南已调查 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 上面的 AA high 行提供精确变体的公开成绩，不挪用 120B |
| Llama3.3-70B-Instruct / 未重新抽取作者分数 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 上面的 AA 行保留已取得的比较背景 |
| GLM-5.3-Flash / max，排除锚点 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 未取得可核验结果 | 320B total / 18B active，不满足 <100B 门槛；AA max 行保留 |

[sonnet]: https://www-cdn.anthropic.com/9e6a1044980d8c4ed85669faf9c2a8342e2e9f1e/Claude%20Sonnet%205%20System%20Card.pdf
[haiku]: https://www.anthropic.com/news/claude-haiku-4-5
[gemini35]: https://deepmind.google/models/model-cards/gemini-3-5-flash/
[gemini38]: https://deepmind.google/models/gemini/flash/
[qwen38]: https://huggingface.co/Qwen/Qwen3.8-27B
[qwen36]: https://huggingface.co/Qwen/Qwen3.6-35B-A3B
[muse]: https://huggingface.co/meta-models/Muse-Glimmer-30B
[gemma]: https://huggingface.co/google/gemma-4-31B-it
[nemotron]: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
[glm47]: https://huggingface.co/zai-org/GLM-4.7-Flash

作者数字的必要限制：Qwen3.8 SWE-Pro 使用 Claude Code、temperature=1、top_p=0.95、256K context，并修订问题后重测对手；Qwen3.6 的 SWE-Pro 也有作者修订集说明。Muse 卡明确 high，推荐 temperature=1/top_p=0.95，但未逐列披露完整 harness 版本和输出预算。Nemotron 使用 NeMo Gym / NeMo Evaluator 的各项 recipes，`IFBench loose` 不能与未核齐同一判分设置的 AA 数字合排；卡片中另有标为 AA-Omniscience 的 17.50，但本轮未取得足以把它认定为 AA 净分的同口径说明，因此未填入净分列。Sonnet/Haiku 发布评测的各项 thinking/harness 以存档 system card/脚注为准，不能仅按产品档位名推定当前 API 行为。[src-vendor] [clm-vendor]

链接复核发现原 Sonnet research landing URL 返回 404；上表改连已存档来源 receipt 中的官方 CDN system card PDF。该入口变化不用于否定已有 PDF/图片快照中的事实。[src-vendor]

## 4. 公开档位与本轮实际档位

| 优先模型 | 本轮实际接入 | 可引用的公开行 | E2 冻结前必须明确的差异 |
|---|---|---|---|
| Luna | profile `gpt-5.6-luna`；不传 reasoning/采样 override，provider default | AA max | 未指定不等于 max 或 think-off；不能把 max 成绩写成当前默认档实测能力 |
| Sonnet 5 | `claude-sonnet-5`；stream ToolStrategy；不传 thinking/effort/采样 override | AA adaptive/max | 需在 E2 明确实际 thinking 与 effort；不能静默切到 max 后复用旧验收身份 |
| Qwen3.8-27B | `e1-qwen38-27b`；服务模板 `reasoning_effort=low`，完整输入、remaining_context | AA low 与 xhigh 各一行 | 当前 low 的 LCR/GPQA/HLE 为 **77.3/84.5/14.0**；xhigh 的 82.0/90.5/33.9 仅是该公开档位背景，不是当前 low 的能力证据 |
| Muse Glimmer-30B | `e1-muse30b`；官方模板默认 high、function/tool、remaining_context | AA high；作者 high | 名称同 high 仍有服务/约束解码/采样/预算/harness 差异，须冻结部署版本 |

任务选型判断：Sonnet 的 LCR 和科学推理有公开能力支持，Omni 净分也提供知识校准的参考；Muse 的长文档成绩并不意味着其严格结构输出没有缺陷。接入可靠性须看完整 method 阶段、schema 修正和降级原因。公开成绩与 E1 发现条数均不能替代 E2 的 hit/precision，也不能据此预先断言谓词消融会出现“hit 略升、precision 暴跌”。该预测仍是待验证假设。[clm-choice] [clm-settings]

模型发布、参数、context/output、官方价格等可复用规格继续维护在根目录 [llm_model_landscape](../../../../llm_model_landscape/README.md)。本报告的 benchmark 与任务分析属于 Paper1 reports；不把 leaderboard 搬入规格文库。E2 交接另见[接入证据入口](./README.md)，judge 与 A1/A2 始终固定 Luna。[clm-choice]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本报告，新建 | `git log --diff-filter=A --follow -- <本文件>` | 09-07 本轮分析冻结时间 | 首次引入全候选 AA 矩阵、缺测和档位映射 | 无迁移 | `benchmarks_20260906.zip/json`；已有 `sources.zip` |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-aa] | aa_snapshot | [ZIP](./evidence/benchmarks_20260906.zip)、[机器表](./evidence/benchmarks_20260906.json) | zip/json | 全候选独立分数 | `aa-qwen38.html` RSC model slug；`models[*]` 完整数值；逐 member hash |
| [src-methodology] | aa_methodology | [ZIP](./evidence/benchmarks_20260906.zip) | zip | 版本、单位、采样、harness | `aa-methodology.html` Index v4.2 / LCR v1.1 / Sampling / GPQA / IFBench / HLE / SciCode；`aa-lcr.html` |
| [src-omni] | aa_omniscience | [ZIP](./evidence/benchmarks_20260906.zip) | zip | 净分和分母限制 | `aa-omniscience.html` Index 与 hallucinationRate 定义 |
| [src-vendor] | vendor_cards | [已有来源 ZIP](./evidence/sources.zip)、[manifest](./evidence/manifest.json) | zip/json | 作者矩阵和脚注 | `qwen38_27b_card.raw`、`qwen36_card.raw`、`muse30_card.raw`、`gemma4_31_card.raw`、`nemotron35_card.raw`、`glm47_flash_card.raw`、`glm53_flash_card.raw`、`sonnet5_system_pdf.*`、`*_benchmark_png.raw`、`gemini35_card.*`、`gemini38_product.*` |
| [src-config] | accepted_profiles | [stream 验收](./2026-09-07-03-36-18-stream-model-max-acceptance.md)、[stream manifest](./evidence/stream_20260907/manifest.json) | md/json | 当前档位与公开档位区分 | `probe.json` profile 指纹、wire thinking/采样、server 默认模板 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-scope] | E1-BENCH-SCOPE | 17 身份、20 公开档位覆盖既有调查 | count | [src-aa] `models[*].slug` 与既有调查范围 | [cmd-bench] | high | 文献背景模型不自动成为部署候选 |
| [clm-aa] | E1-BENCH-AA | 独立矩阵逐值可从 RSC 重建 | trace | [src-aa] 原始 HTML 与派生 JSON 对拍 | [cmd-bench] | high | AA 未提供不可变 serving revision；不混旧版本 |
| [clm-settings] | E1-BENCH-SETTINGS | AA 和 E1 的推理/采样/预算不完全同口径 | risk | [src-methodology] settings；[src-config] wire/server | [cmd-bench]；人工读脚注 | high | E2 尚需协议冻结，不把公开 max 替换本轮默认 |
| [clm-omni] | E1-BENCH-OMNI | 净分不能当本任务幻觉率 | prohibition | [src-omni] Index、hallucinationRate 定义 | 人工核验两个分母 | high | 不由 accuracy 减错误分母推导 |
| [clm-vendor] | E1-BENCH-VENDOR | 作者数字单列、版本与转引保留 | trace | [src-vendor] 精确模型列、图例和脚注 | [cmd-vendor]；人工复读表格 | high | 非统一排行榜；卡片没有逐项披露的设置保留未知 |
| [clm-structure] | E1-BENCH-STRUCTURE | 四类精确变体同口径成绩未取得 | classification | 本轮来源快照和查找范围 | [cmd-bench]；人工确认缺测 | medium | 仅表示本轮未取得，不断言评测不存在 |
| [clm-relevance] | E1-BENCH-RELEVANCE | 长文本、约束、证据可靠性更贴近任务 | narrative | [src-methodology] 任务定义；导师 talk 的同 backbone 比较目的 | 人工核验适用边界 | medium | 公开任务不是状态机缺陷发现 |
| [clm-choice] | E1-BENCH-CHOICE | 用户优先四款以能力背景/组合/可用性选择 | decision | [clm-aa]、[src-config]、用户 Sonnet-ready 指令 | 人工复核选型理由与协议 | medium | 不按效果差值选型，不预先声称 SOTA 或消融结论 |

### A.4 复验命令

[cmd-bench] 重解析归档 HTML，与原调查 `aa-models.json` 和 committed JSON 全精度对拍，再逐字检查三个生成矩阵；离线运行，不调用 provider：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_benchmark_evidence.py
```

[cmd-vendor] 验证原始来源归档；作者表需按 member 中的精确型号列和脚注人工复核，不能用“数字字符串存在”代替判断：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_evidence.py
```
