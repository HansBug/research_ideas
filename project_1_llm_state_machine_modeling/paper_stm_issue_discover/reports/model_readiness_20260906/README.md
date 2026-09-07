# E1 模型调研与推理接入证据

核验日期：2026-09-06 至 2026-09-07。本文档组记录 Paper1 多模型实验的选型依据、官方资料、远程 H200 部署和有限兼容性 smoke。它不包含正式命中率、precision 或方法优越性结论；完整 baseline/ours 实验需要独立冻结协议与运行身份。研究范围来源为 [E1 合同](https://github.com/HansBug/research_ideas/pull/204)；施工状态以 GitHub 为准。

## 结论

用户优先组合为 **Luna + Sonnet 5 + Qwen3.8-27B + Muse Glimmer-30B**。四款均有最终 profile 的 stream baseline/ours 接入证据。Luna 更换用户提供的连接后，普通生成、共用 structured runtime、baseline 及 0001/r1 method 通过；最终 method 8 阶段完成，5 次调用 usage 齐全，errors/audit errors/schema 修正均 0，见[Luna 新连接与 adapter 修复](./2026-09-07-11-10-00-luna-connection-recovery.md)。旧 503、首次 method 的 SSE 过载和漏报反例均保留，不据有限成功声称持续 SLA。Sonnet、Qwen 和修复后的 Muse 各有最终 profile 的 stream baseline 与 0019/0029/0049 method 证据；Sonnet 0029 保留正常证据降级，Muse 原结构耗尽已在 serving adapter 修复，最终三格 errors/audit errors 全 0。精确配置、逐格解释及部署复现见[四模型交接证据](./2026-09-07-06-12-00-four-model-handoff.md)。

两开放模型各自独立 conda、GPU 4-7，使用最大允许输出的剩余窗口模式，迁移后约 0.9 窗口和 16K/16-worker 均有证据；Muse 最新 serving 修复后再次通过 32/32 并发请求和 118375-token 输入 2/2。原生与扩展容量、高并发和完整 method 分开验收，不宣称 16 个最大窗口同时驻留。09-06 的五款近期 <100B 主候选、三款生态对照及旧环境实测仍见[开放模型报告](./2026-09-06-11-53-00-open-models.md)与[部署报告](./2026-09-06-11-53-00-serving-evidence.md)，其余候选后置。E2 正式协议与各模型实验档位仍需独立冻结。

覆盖口径：`0019/0029/0049` 的最终配置 method 证据来自 Sonnet/Qwen/Muse，共 9 格；新 Luna 连接只补测 `0001/r1`。这符合当时协议对 Luna 的复用安排，但不等于四款都通过同样三大格。Muse ATEM 原生格式有官方依据，额外解码语法及嵌套放宽属于本地兼容方案；新版 XGrammar `any_order` 的能力、必填/重复键限制和未实测边界已补入[总报告 §3](./2026-09-07-06-12-00-four-model-handoff.md#3-大输入-stream-method)，并附官方/社区来源。

## 证据入口

- [四模型总报告](./2026-09-07-06-12-00-four-model-handoff.md)：最终配置、baseline/ours 的样本与数字、容量/16-worker、主要故障与修复、正常降级和 E2 协议边界。
- [复现附录](./2026-09-07-11-55-00-reproduction.md)：独立 conda、精确依赖与 revision、Qwen YaRN/Muse serving、共享缓存与 tunnel、真实入口和核心校验；历史原件另行提供的边界。
- [Luna 新连接、Responses 错误修复与交接](./2026-09-07-11-10-00-luna-connection-recovery.md)：仅连接两字段变化，128K wire cap、完整阶段/usage、漏报修复及旧失败并存。Luna baseline 省略 reasoning、method 显式 none，E2 需冻结两臂设置。
- [Luna 旧路由复核](./2026-09-07-06-55-00-luna-route-recheck.md)：06:39 baseline 单次成功及后续 503，保留同 payload、wire 上限、provider 错误与终态的历史事实。
- [全候选公开 benchmark 与任务选型](./2026-09-07-04-30-00-candidate-benchmarks.md)：17 个已调查模型身份、20 个公开档位，AA v4.2 / LCR v1.1 与作者自报分表、结构化缺测、当前 low/default 与公开 max/xhigh 的差异。
- [protocol.md](./protocol.md)：事前协议、context 0.9 边界、隐私和验收条件。
- [09-07 最大输出与 stream 大格验收](./2026-09-07-03-36-18-stream-model-max-acceptance.md)：15 格、独立环境迁移负载、三层同请求、预算修复与商业替代建议。
- [商用模型](./2026-09-06-11-53-00-commercial-models.md)：发布时间、价格、context/output、公开 benchmark 和可用性。
- [开放模型](./2026-09-06-11-53-00-open-models.md)：100B 以下候选、官方启动方式、许可证、benchmark 和选型。
- [近期 LLM4SE](./2026-09-06-11-53-00-llm4se-recent.md)：2026-03-06 至 2026-09-06 的 arXiv 样本和模型使用统计。
- [部署与负载](./2026-09-06-11-53-00-serving-evidence.md)：tunnel、并发、长上下文和 thinking 结果、失败记录与交接缺口。
- [../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md](../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)：导师讨论正式纪要。

## 选型原则

每个 backbone 在 E2 中应配对比较 `LLMx + FCSTM + 谓词` 与 `LLMx`。论文主张是方法提高不同模型在规定任务上的效果，不是击败最新模型。价格只用于工程可行性记录，不作为论文贡献。A1/A2 继续使用 Luna 单模型；E1 不启动 E2，也不启动伞 PR O2。

Muse 的推荐接入限定为 function/tool 路径；最终 required-tool serving 修复不覆盖旧 JSON response-format 占位符、D 结构错误和同请求远端反例。Claude timeout/客户端生命周期修复已有 stream 证据。Gemini 3.7/3.8 的 native ToolStrategy 成功不覆盖严格 JSON Schema/canary，09-07 Gemini 3.8 的 11 次网关 504 仍是可靠性限制，保留为备选资料；Haiku 也保留其 D 结构耗尽，不阻塞 Sonnet 方案。

## 证据等级

容量、API 和 workflow 分开判断：容量通过只表示对应负载成功；`completed_with_diagnostics` 不是无缺口完成；`failed_with_receipt` 不是成功；`untested` 不能写成已部署。所有 smoke 的 `formal_result_eligible=false`。

2026-09-07 用户调整交付边界：**原始 usage、stage receipts、失败、网页快照、审计 ZIP/JSON 及历史辅助脚本仅本地保留，不随 Git 提供**。关键数字和可点击公开来源完整落在 Markdown；生产 adapter 与必要回归继续跟踪。需要逐条重放历史结果时，须另行取得相应原件/manifest/当时校验器；fresh clone 不具备这些审计原件。导出 hash 与原始 hash 分开，不伪造重签；取消跟踪也未清除旧提交中的大 blob。详情见复现附录 §1，动态收尾状态仍以 #204/#179 为准。
