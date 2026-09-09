# Qwen / Muse A2 全量运行登记（2026-09-10）

按用户追加授权，在 Sonnet A2 method/judge 均完成 162 格后，合入伞分支的 E1/E2/A1，再运行 Qwen3.8-27B 和 Muse Glimmer-30B 的原 A2 `no-predicates`。Sonnet 全量结果见[报告](../reports/2026-09-10-a2-sonnet5-full-results.md)，其普通 precision 没有出现局部 pilot 中的下降；后续两模型不以追求指定结果为调参目标。

## 条件与输入

- 每模型均为相同 54 个 frozen pair × round 1/2/3，共 162 method cells。使用完整原始输入闭包；不使用 15-pair/stress 子集，不新增 ours/baseline 调用。
- A2 边界沿用 method README 的 `no-predicates`：删除谓词相关生成、执行及回执过滤；保留需求义务、普通 grounding、检查事实和语义评估等，不解释为删除全部语义引导。
- 同模型 full ours/baseline 复用 E2 冻结的 162+162 格。Qwen/Muse 使用合并后的同一 method/运行环境；Sonnet 已完成结果保留旧源码身份，不跨模型强行混算单一净效果。

## 模型与调度

| 条件 | 配置 | 并发 |
|---|---|---|
| Qwen A2 | `e1-qwen38-27b`，Qwen3.8-27B，revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`；E2 已用 YaRN 1,000,000 context，模板 low，remaining_context 输出 | method 16 workers，三轮完整执行 |
| Muse A2 | `e1-muse30b`，Muse Glimmer-30B，revision `a4e59da52a7bc87ae7251dd5545c0dd437c44b68`；131,072 context，模板默认 high，原 serving 适配，remaining_context 输出 | method 16 workers，三轮完整执行 |
| 两模型 judge | `gpt-5.6-luna`，v3.11，两读、arbitration、trigger any、relation_first、full closure；24,000 judge 输出上限 | r1/r2/r3 同时运行，每轮 8 workers；同一时段最多 24 |

远程 `xai` 只使用授权 GPU 4–7/TP4；两款模型顺序复用已有 conda prefix、权重和 8100 端口，不重建环境或下载权重。本地复用现有 SSH tunnel。Qwen 生成完成并确认 162 eligible 后，可启动其三轮 judge，同时切换远程服务生成 Muse；Muse 的 judge 等 Qwen judge 完成后启动，避免两个模型叠加为 48 judge workers。只停止本次新建的服务 tmux session，不干预其他 session、GPU 或服务。

本地使用 pane9 已安装的 E2 venv，显式 PYTHONPATH 指向当前 A2 checkout。method 配置从 pane9 的私有配置冻结复制，judge 配置从本轮 Luna 配置冻结复制，均以 600 权限留在 ignored run 目录；不输出凭据，不改其他 session 的配置。连接前沿用 `source ~/enable_proxy`，loopback/SSH tunnel 使用 no_proxy。开放模型生成沿用 E2 的 `LANGCHAIN_OPENAI_STREAM_CHUNK_TIMEOUT_S=300`；judge 不继承该生成端覆盖。不增加 temperature/top_p/seed/reasoning 覆盖。

## 核销与失败

独立目录为 `runs/paper1/a2_open_models_20260910/`，每模型保留 native run manifest、输入与 hash、配置身份、prompt/raw output/usage、错误和重试；调度器记录启动提交、命令、时间与终态。每模型的 included/excluded manifest 必须覆盖全部 162 格；eligible 不足时暂停后续派发并留下具体诊断，不缩小分母。provider/schema 失败保留原件，正常内部证据缺口按既有降级规则落盘。

成功 method 不因 judge 失败重跑；成功 judge 不因指标方向重裁。恢复须匹配原始输入、round、模型与协议；不覆盖旧失败回执，不用其他模型替代。三轮均有 54 个完成裁定、输出报告与判定覆盖闭合后，才发布该模型正式统计。

结果按总体、round、pair 报告 reports、K/N/I、普通 precision、strict precision 和 FULL hit，并与同模型 E2 ours/baseline 对照。保留九簇统计与历史日期/provider/运行差异的限制，不宣称少量模型上的普遍性或严格单因素因果识别。人工确认数只按实际工作更新。
