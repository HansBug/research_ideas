# E1 模型调研与推理接入证据

核验日期：2026-09-06 至 2026-09-07。本文档组记录 Paper1 多模型实验的选型依据、官方资料、远程 H200 部署和有限兼容性 smoke。它不包含正式命中率、precision 或方法优越性结论；完整 baseline/ours 实验需要独立冻结协议与运行身份。研究范围来源为 [E1 合同](https://github.com/HansBug/research_ideas/pull/204)；施工状态以 GitHub 为准。

## 结论

09-07 新预算、大输入 stream 验收覆盖 Gemini 3.8、Sonnet 5、Haiku 4.5、Qwen3.8 和 Muse，各三个真实 method cell。15 格均按现有规则 eligible，其中 5 格带降级诊断；不能解释成所有阶段无错误。商业配对建议为 **Luna + Sonnet 5**，Haiku 作为较低价备选；Gemini 本轮仍有 11 次网关 504，不能仅凭 eligible 宣称渠道健康。完整数字、逐格缺口、预算和证据见[09-07 验收报告](./2026-09-07-03-36-18-stream-model-max-acceptance.md)。

开放模型按用户决定固定为 **Qwen3.8-27B + Muse Glimmer 30B**。两款各自独立 conda、GPU 4-7、新预算 stream 大格和迁移后的约 0.9 窗口及 16K/16-worker 均已有证据；Qwen 三格无 errors，Muse 0049 的 D 阶段结构修正耗尽后降级，保留待改进限制。原生与扩展容量、高并发和完整 method 分开验收，不宣称 16 个最大窗口同时驻留。09-06 的五款近期 <100B 主候选、三款生态对照及旧环境实测仍见[开放模型报告](./2026-09-06-11-53-00-open-models.md)与[部署报告](./2026-09-06-11-53-00-serving-evidence.md)，其余候选后置。E2 正式模型名单和协议尚未冻结。

## 证据入口

- [protocol.md](./protocol.md)：事前协议、context 0.9 边界、隐私和验收条件。
- [09-07 最大输出与 stream 大格验收](./2026-09-07-03-36-18-stream-model-max-acceptance.md)：15 格、独立环境迁移负载、三层同请求、预算修复与商业替代建议。
- [evidence/stream_20260907/manifest.json](./evidence/stream_20260907/manifest.json) 与 [verify_stream_evidence.py](./verify_stream_evidence.py)：新旧 stream/诊断制品的脱敏归档、逐调用 wire、阶段回执及离线核验。
- [商用模型](./2026-09-06-11-53-00-commercial-models.md)：发布时间、价格、context/output、公开 benchmark 和可用性。
- [开放模型](./2026-09-06-11-53-00-open-models.md)：100B 以下候选、官方启动方式、许可证、benchmark 和选型。
- [近期 LLM4SE](./2026-09-06-11-53-00-llm4se-recent.md)：2026-03-06 至 2026-09-06 的 arXiv 样本和模型使用统计。
- [部署与负载](./2026-09-06-11-53-00-serving-evidence.md)：tunnel、并发、长上下文和 thinking 结果、失败记录与交接缺口。
- [evidence/manifest.json](./evidence/manifest.json)：脱敏归档的逐 member SHA-256 与 redaction 策略。
- [verify_evidence.py](./verify_evidence.py)：离线验证哈希，并从原始逐请求记录复算全部负载结果；不会调用 provider。
- [../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md](../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)：导师讨论正式纪要。

## 选型原则

每个 backbone 在 E2 中应配对比较 `LLMx + FCSTM + 谓词` 与 `LLMx`。论文主张是方法提高不同模型在规定任务上的效果，不是击败最新模型。价格只用于工程可行性记录，不作为论文贡献。A1/A2 继续使用 Luna 单模型；E1 不启动 E2，也不启动伞 PR O2。

Muse 的推荐接入限定为 function/tool 路径；旧 JSON response-format 占位符、新大格 D 结构错误及同请求远端 schema 反例均保留。Claude timeout/客户端生命周期和实时接入修复已有新 stream 证据，旧失败材料不覆盖。Gemini 3.7/3.8 的真实 method 成功只证明所测 native ToolStrategy 路径可运行，不能覆盖网关原生 JSON Schema 和所有强制工具场景；09-07 的网关 504 仍是实际可靠性限制。

## 证据等级

容量、API 和 workflow 分开判断：容量通过只表示对应负载成功；`completed_with_diagnostics` 不是无缺口完成；`failed_with_receipt` 不是成功；`untested` 不能写成已部署。所有 smoke 的 `formal_result_eligible=false`。原始 usage、stage receipts 和失败保留，公开包对 secret、端点、节点、用户名和私人路径脱敏；内嵌原始 run hash 不会因脱敏而伪造重签。`protocol.md` 是事前协议与后续用户约束记录，四份秒级命名报告是冻结的人类分析入口。
