# 商用模型候选

核验日期：2026-09-06。价格单位均为 USD / 1M tokens，按本轮访问到的官方页面记录；价格和 lifecycle 变化时，E2 run record 必须保存调用日期和精确 model ID。公开 benchmark 是能力背景，不是 Paper1 状态机缺陷发现结果。

## 比较表 [clm-commercial-table]

| 模型 | 官方发布时间 | 精确 ID / 可用性 | context / max output | 官方价格（标准输入/输出） | 本轮公开 benchmark 摘要 | 初步判断 |
|---|---|---|---|---|---|---|
| Gemini 3.8 Flash | 2026-09-02 | `gemini-3.8-flash`；Gateway B native profile 可用，method smoke 已通过 | 1M；64K output | 2026-12-31 前 $0.75 / $3.75；2027-01-01 起 $1.50 / $7.50 | HLE-Verified 54.9；Vals Finance Agent v2 61.4；Harvey Legal Agent 10.0；DeepSWE v1.1 官方图 >70（未转写无标注的精确数值） | 已具备 method 接入证据；价格未核验，成本不具资格 |
| GPT-5.6 Luna | 2026-07-09 | `gpt-5.6-luna`；当前 profile 可用 | 1,050,000 context；922,000 max input；128,000 max output | 短上下文 $0.20 / $1.20；长上下文 $0.40 / $1.80；cache read $0.02/$0.04，cache write $0.25/$0.50 | 官方模型页未给与本任务直接对应的统一 benchmark 表；公开定位是高吞吐、低延迟 | **必须保留**；A1/A2 和主实验的固定商用锚点 |
| Claude Sonnet 5 | 2026-06-30 | `claude-sonnet-5`；本轮 API 探针可用 | 1M；128K output（当前 API 文档） | $2 / $10；官方说明 2026-08-10 起该 introductory price 永久有效 | SWE-bench Verified 85.2；SWE-bench Pro 63.2；SWE-bench Multilingual 78.3；Terminal-Bench 2.1 80.4；OSWorld-Verified 81.2；HLE no tools 43.2、with tools 57.4 | 能力强、价格高于 Luna；按用户偏好优先级较低；作为备选，不替换 Gemini 主候选 |
| Gemini 3.5 Flash | 2026-05-19 | `gemini-3.5-flash`；用户可获取；现有网关兼容接口和 Google 原生探针均失败（404/500/timeout） | 1M；64K output | 标准 $1.50 / $9.00；Batch $0.75 / $4.50；以 2026-09 官方 pricing 页为准 | Terminal-Bench 2.1 76.2；SWE-Bench Pro 55.1；MCP Atlas 83.6；Toolathlon 56.5；OSWorld-Verified 78.4；MRCR v2 128K 77.3；HLE 40.2；ARC-AGI-2 72.1 | 保留为目标候选；当前接入仍 blocked |
| Gemini 3.7 Flash | 2026-08-13 | `gemini-3.7-flash`；Gateway B native profile 可用，method smoke 已通过 | 1M；64K output | 本轮未取得可核验价卡 | 本轮不补写未核验 benchmark | 当前可运行；成本 eligible=false，不能解释为免费 |
| Claude Haiku 4.5 | 2025-10-15 | `claude-haiku-4-5-20251001`；本轮 API 探针可用 | 200K；64K output（当前 API 文档）；launch benchmark 的 128K thinking 设置是独立评测口径 | $1 / $5；cache read $0.10，write $1.25（5m）/$2（1h） | SWE-bench Verified 73.3；Terminal-Bench 40.21（无 thinking）/41.75（32K thinking），发布页未注明 benchmark 版本；GPQA Diamond 73.0 | 低价、低延迟备选；不代表 Claude 能力上界 |

来源： [OpenAI GPT-5.6 changelog](https://developers.openai.com/api/docs/changelog)、[OpenAI models](https://developers.openai.com/api/docs/models)、[OpenAI pricing](https://developers.openai.com/api/docs/pricing)、[Gemini 3.5 model card](https://deepmind.google/models/model-cards/gemini-3-5-flash/)、[Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)、[Gemini 3.8 model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/)、[Claude Sonnet 5 launch](https://www.anthropic.com/news/claude-sonnet-5)、[Claude Sonnet 5 system card](https://www.anthropic.com/research/claude-sonnet-5-system-card)、[Claude Haiku 4.5 launch](https://www.anthropic.com/news/claude-haiku-4-5)、[Anthropic pricing](https://docs.anthropic.com/en/docs/about-claude/pricing)。

## 解读和限制

1. Luna 的 context/output 和价格来自官方模型/价格页；其当前调用 profile 仍是内部可用性事实，不能把内部 profile 当成公开 benchmark 证据。
2. Gemini 和 Claude 的 agentic benchmark 依赖各自 harness、推理预算、工具和采样参数。表中数字只帮助判断能力层级，不能跨 provider 直接排序，也不能代替 Paper1 的 hit/precision。
3. Gemini 3.8 在旧渠道的“暂时无法获取”是访问状态，不是模型不存在或质量失败；Gateway B 已提供新的可访问 native profile，正式 method 结果以该路径单独记录。不同渠道的身份、计量和结构化能力不能混写。
4. Luna 仍是固定商用锚点；Gemini 3.7/3.8 已有 native method 接入证据，Gemini 3.5 仍是旧渠道 blocked。E2 名单和第二商用模型尚未冻结；Sonnet/Haiku 保持低优先级备选，不因价格写成论文结论。[clm-commercial-selection]

## 共同 benchmark 列与缺测

没有核验到覆盖五个候选、同一 harness 的统一榜单。以下横向列保留公开缺测；`—` 是本轮官方来源未报告，不能记 0。HLE、HLE-Verified、text-only/full-set、with-tools 是不同口径。[clm-commercial-table]

| 模型 | SWE-bench Verified | SWE-bench Pro | Terminal-Bench | HLE / HLE-Verified | 长上下文 / 工具 |
|---|---:|---:|---|---|---|
| Gemini 3.8 Flash | — | — | — | HLE-Verified 54.9 | 当前产品页：Finance Agent v2 61.4；Legal Agent 10.0 |
| GPT-5.6 Luna | — | — | — | — | 官方 API 支持 structured outputs / function calling；无统一分数 |
| Claude Sonnet 5 | 85.2 | 63.2 | 2.1：80.4 | HLE no tools 43.2 / with tools 57.4；Google 产品图的 HLE-Verified 31.0 为另一口径 | OSWorld-Verified 81.2 |
| Gemini 3.5 Flash | — | 55.1（single attempt） | 2.1：76.2（Terminus-2） | full-set HLE 40.2 | MRCR v2 8-needle 128K 77.3；MCP Atlas 83.6 |
| Gemini 3.7 Flash | — | — | — | — | 本轮未取得可核验统一 benchmark |
| Claude Haiku 4.5 | 73.3 | — | 版本未注明：40.21（无 thinking）/41.75（32K thinking）；图表汇总 41.0 | — | Terminus 2 是 harness 名，不等于 benchmark 2.1；其余 launch 评测使用 128K thinking budget，不等于 API max output |

补充官方入口：[Sonnet specs](https://platform.claude.com/docs/en/models/sonnet-5/overview)、[Haiku specs](https://platform.claude.com/docs/en/models/haiku-4-5/overview)、[Gemini 3.8 product](https://deepmind.google/models/gemini/flash/)。官方“能力背景”和本轮私有网关可调用性是两条证据线；`/chat/completions` 返回网页的 HTTP 200 也不算推理成功。

Sonnet 5 的 cache read 为 $0.20，cache write 为 $2.50（5m）/$4（1h）。Gemini 3.5 context caching 为 $0.15/1M tokens，存储 $1/1M tokens/hour；Gemini 3.8 的缓存价格本轮未取得独立明确行，不沿用 3.5 的值。Luna 长上下文价以输入超过 272K 为界，缓存写入、读取和输出各自按对应档位记录。[src-commercial-prices]

## 接入边界

Luna 的 profile、baseline 和 method smoke 均通过；Sonnet 5 / Haiku 4.5 的普通生成、JSON schema、tool call 和 streaming usage 均通过。Sonnet 5 的 method smoke 仍为 `failed_with_receipt`，Haiku 尚未额外运行 method。Gemini 3.5 的兼容和原生路径仍保留失败回执；Gemini 3.7/3.8 通过 Gateway B 的 native profile、ToolStrategy method smoke，但严格 `responseJsonSchema` 与复杂 forced-tool canary 仍不稳定。[clm-commercial-access]

## Gateway B Gemini native method update

`gateway-b-gemini-3.7-native` 的 pair `0001` 运行 `3e63559c0b9a4c70b643c1209d306bbb`：90.40 秒、9 次模型调用、5/5 stage success、4 次节点内 schema 修正后收敛、1/1 method eligible、3 条 W2、method/audit error 为 0。`gateway-b-gemini-3.8-native` 的 pair `0001` 运行 `c3ae4aae335a434e90410bc93b0917e3`：83.25 秒、8 次调用、5/5 stage success、3 次节点内 schema 修正后收敛、1/1 method eligible、2 条 W2、method/audit error 为 0。两次运行均为一轮、一 worker、streaming、零 provider transport retries，judge 调用数为 0；judge 仍固定 Luna。W2 数量不用于模型能力排名，且只覆盖一个诊断 pair。

两个 native profile 的成本资格均为 false：本轮没有可核验价卡，运行记录中的 `0.0` 仅是未计价结果，不能解释为免费。Gateway B 的严格 native JSON Schema、最小 enum schema 和复杂 forced-tool canary 仍有失败或不稳定记录；已通过的 method 依赖当前 ToolStrategy/function-tool 路径，不能外推为全面 schema 健康。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本文件，新建调查 | 首次提交由 `git log --diff-filter=A --follow -- <本文件路径>` 定位 | 时间前缀为本轮调查冻结时间 | 新增官方事实与访问结论；不以 smoke 源码提交冒充报告创建提交 | 无历史迁移 | `evidence/sources.zip`、`evidence/probes.zip` |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-commercial-specs] | commercial_specs | [sources.zip](./evidence/sources.zip) | zip | 日期、规格、模型身份 | `luna_announcement.*`、`luna_specs.*`、`gemini35_announcement.*`、`gemini35_api.*`、`gemini38_card.*`、`sonnet5_specs.*`、`haiku45_specs.*`、`claude_*_news.*`；receipt 的 URL / retrieved_at / sha256 |
| [src-commercial-prices] | commercial_prices | [sources.zip](./evidence/sources.zip) | zip | 价格与分档 | `openai_pricing.*`、`gemini_pricing.*`、`claude_pricing.*`、`gemini38_product.*`；精确型号的 pricing 行 |
| [src-commercial-bench] | commercial_bench | [sources.zip](./evidence/sources.zip) | zip | benchmark、版本与 harness | `gemini35_card.*`、`gemini35_model.*`、`gemini38_product.*`、`sonnet5_system_pdf.*`、`sonnet5_benchmark_png.raw`、`haiku45_benchmark_png.raw`、`claude_haiku_news.*` |
| [src-commercial-probes] | commercial_probes | [probes.zip](./evidence/probes.zip) | zip | 可调用性和 method 缺口 | `probes/{gpt-5.6-luna,claude-*,e1-gemini-*}/*.json`、`workflows/*/*/artifacts/*/summary.json`、`gateway_routes.json` |
| [src-advisor] | advisor | [正式导师纪要](../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md) | md | 同 backbone 配对与研究边界 | 导师意见、用户决策、未验证推测分栏 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-commercial-table] | E1-COM-TABLE | 商用模型的官方日期、规格、价格及公开分数 | trace | [src-commercial-specs]、[src-commercial-prices]、[src-commercial-bench] 对应型号行/图片列 | [cmd-commercial-sources] 人工复验 | high | 独立来源的 harness 不统一；缺测不补零；发布评测预算不等于 API 输出上限 |
| [clm-commercial-access] | E1-COM-ACCESS | 单调用通过与 method 完成分开；Gemini 3.7/3.8 native method 已通，Gemini 3.5 仍缺接入 | classification | [src-commercial-probes] 与 Gateway B native method receipts；`per_pair/0001/status` | [cmd-commercial-probes] | high | 网关回显不证明上游身份；strict schema/canary 仍受网关限制；只代表本轮路径 |
| [clm-commercial-selection] | E1-COM-CHOICE | 保留 Luna；Gemini 3.5/3.7/3.8 和 Claude 作为待定商用候选 | decision | [src-advisor]、[clm-commercial-table]、[clm-commercial-access] | 人工复验：核对偏好、来源和访问回执 | medium | E2 名单尚未冻结；不同渠道的 Gemini 能力与价格资格需分别记录 |

### A.4 复验命令

[cmd-commercial-sources] 校验来源归档哈希后，按上表 member 打开原文，复核日期、价格行、benchmark 图片列及脚注。在线来源可能变化，因此以本次 receipt 时间和原始响应为本报告依据。

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/verify_evidence.py
```

[cmd-commercial-probes] 在仓库根目录列出实测路径的完成/失败状态；method 需读 pair 状态，不能只看 CLI exit code。

```bash
python - <<'PY'
import json, zipfile
from pathlib import Path
p = Path('project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/model_readiness_20260906/evidence/probes.zip')
with zipfile.ZipFile(p) as z:
    for name in sorted(z.namelist()):
        if name.startswith('probes/') and name.endswith('.json'):
            r = json.loads(z.read(name))
            if 'status' in r:
                print(name, r['status'], r.get('schema_valid'), r.get('usage_observed'))
        if name.startswith('workflows/') and name.endswith('/summary.json'):
            r = json.loads(z.read(name))
            print(name, {k: v['status'] for k, v in r.get('per_pair', {}).items()})
PY
```
