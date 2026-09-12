# A1-ext：claude-sonnet-5 / qwen3.8-27b / muse-glimmer-30b 的无检视事实消融事前登记

登记时间：2026-09-11（Asia/Shanghai）。本文件在任何真实 provider 调用之前写入并推送；实际 source commit 是包含本登记的干净、已推送提交，由启动时 `git rev-parse HEAD` 写入每个 method/judge 的 run manifest，本文不预填。合同来源为[伞 PR #179](https://github.com/HansBug/research_ideas/pull/179) §4.8 与用户 2026-09-11 指令：Muse 先跑再切 Qwen，Sonnet 并行；任一模型 method 完成即用 aizzz 通道的 gpt-5.6-luna 启动 judge；纯 provider 失败等待后重跑一次。

## 1. 问题与假设

飞书 O2 文档唯一待决线程：RQ3（无检视事实，A1，对应 C-1）现稿只有 gpt-5.6-luna 一行，RQ4/RQ5 均为四模型表。本实验补齐另三种固定模型配置的无检视事实条件，使 RQ3 可与 RQ4/RQ5 对称，并检验 §7 “检视事实与中间引导相互依赖”的发现是否跨模型成立。

事前假设，均非验收数值要求：H1，关闭检视事实后每个模型的平均覆盖与 L2 覆盖相对同模型 Full 下降，方向与 gpt-5.6-luna 的 A1 一致；H2，L0/L1 变化幅度小于 L2；H3，精确率方向不作预设。结果与假设相反时如实写入结果与讨论，不改 claim 方向，不重跑找叙事。

## 2. 范围与冻结身份

| 项 | 值 |
|---|---|
| 模型与 profile | claude-sonnet-5（Anthropic 直连，profile `claude-sonnet-5`）；muse-glimmer-30b（profile `e1-muse30b`，远程 GPU 4-7 SGLang TP4，权重 revision `a4e59da52a7bc87ae7251dd5545c0dd437c44b68`）；qwen3.8-27b（profile `e1-qwen38-27b`，同一组卡，权重 revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`，1M YaRN、reasoning_effort low） |
| 网格 | 冻结 54 pair × 3 round，每模型 162 格，共 486 格；`00x8` 系列永久排除，台账 145 条 / 435 expected-round 不变 |
| method 协议 | `--ablation no-inspect --rounds 3`，流式，transport retries 8，与 A1 [#205](https://github.com/HansBug/research_ideas/pull/205) 相同；prompt、12 谓词注册表、ledger 与当前伞分支一致 |
| 配对对照 | E2 [#208](https://github.com/HansBug/research_ideas/pull/208) 同模型冻结 Full ours，只读，不重跑 |
| 上游源码基点 | 伞分支 `7c398038d85bbe59a9b7efeab72d0aa59c14f582`（含 `7c398038d` 的 `stream_read_error` 可重试修复） |
| ledger 原文件 SHA-256 | `sha256:b5a38d3d24a51e980e5b9f5afc7c8c66aded59f3b51f16afe67e0deb592d0e36` |
| pyfcstm | `901f30e981c29eb8e304b33d61985652d2e85b2e` |
| judge 协议快照 | `d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`（`semantic-judge.two-stage.v3.11`，与 A1 `judge_aizzz` 批次相同） |
| judge 模型与通道 | `gpt-5.6-luna`，aizzz（`https://api.aizzz.xyz/v1`），与 A1 的 Luna judge 同一提供方；两读、`arbitration`、触发 `any`、`relation_first`、closure `full`，请求预算沿用原协议 |

开放模型 profile 沿用 E1/A3 的隔离配置（`output_budget_mode: remaining_context`、`stream_usage: true`），凭据只在 0700 临时目录的 0600 文件中，通过 `LLM_CONFIG_FILE` 注入，不改共享 `.llmconfig.yml`。

## 3. 并发、顺序与失败处理

| 泳道 | 内容 | 并发 | 启动条件 |
|---|---|---|---|
| 1 | Sonnet method 162 格 | 24 workers | 立即 |
| 2a | Muse method 162 格 | 24 workers | 立即，服务已驻留 |
| 2b | Qwen method 162 格 | 24 workers | 2a 完成且服务端无在途请求后，停止我方 Muse tmux 会话，起 Qwen 服务，经 tunnel 核对 `/v1/models` |
| 3 | Luna judge，按（模型，轮次）排队，同一时刻只跑一个 judge run | 24 workers | 任一模型 method 全部 162 格落盘后冻结 `judge_source/<model>` 并入队 |

失败处理：method 内部保留 8 次 transport retry 与 schema 反馈修订；整格若以 provider 错误结束（`failed_with_receipt` 且 error code 属 provider 侧），等待后按同 run 目录 `--resume` 重跑该格一次，原失败回执保留不删；非 provider 原因的降级格保留诊断，不重跑。Sonnet 若 429/重试记录明显堆积，降到 16 workers；aizzz judge 若失败堆积，降到 16 workers，不换提供方。不冷启动反复抽样，不追加语义发现。

## 4. 产出、指标与退出

每模型 162 格及每格回执；全部发布报告经标准两读与必要仲裁裁定、pending=0；逐模型与同模型 Full 的 hit@1 / hit@3 / hit@all、L0/L1/L2 分层、K/N/I、普通与严格 precision 配对差值及九 NL 簇重采样区间；生成/绑定/执行/发布/judge 漏斗与内容案例；中文报告与可复算归档进入 `final_results/a1_ext_20260911`，原件留本地 `runs/paper1/a1_ext_20260911`。退出门：486 格完整落盘、pending=0、来源 hash 与台账不变、离线复算与 review 通过；不以覆盖必须下降为门槛。是否进入论文及表述在 O2 飞书线程另行裁定，本实验不改 O2 正文。

## 5. 不做什么

不重跑 Luna A1，不重跑任何 Full 或 baseline，不改协议、词表、ledger、裁定口径或评价政策，不为结果方向调整分母，不把 method 完成当作可入稿。
