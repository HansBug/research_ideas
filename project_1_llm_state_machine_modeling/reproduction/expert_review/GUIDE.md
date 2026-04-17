# Expert Review Guide

## 1. 目录边界

`expert_review/` 只承载本模块自己的三类内容：

1. 可运行代码
2. 模块级测试
3. 模块级设计与阶段文档

不要把以下内容继续混入本目录：

1. `reproduction/` 根级工作流说明
2. 其他 baseline 的实现
3. parquet / json / 临时实验结果落盘
4. 与 `expert_review` 无关的脚本或 notebook

## 2. 阅读入口

推荐阅读顺序：

1. 先读 [README.md](./README.md)，理解根层结构、架构分层与执行方式
2. 再读 [designs/README.md](./designs/README.md)，理解版本文档入口
3. 如果要继续 phase 工作，读 [designs/v1/TODO.md](./designs/v1/TODO.md)
4. 如果要确认 `Phase 6` 收口状态与冻结判断，读 [designs/v1/V1_ALIGNMENT_REPORT.md](./designs/v1/V1_ALIGNMENT_REPORT.md)
5. 最后再进入具体代码目录

## 3. 正式代码组织

当前正式代码主干固定为：

1. [`schemas/`](./schemas/)：内部 request / dossier / graph state / result 结构
2. [`prompts/`](./prompts/)：contract、policy、extraction、analysis、synthesis prompt
3. [`tools/`](./tools/)：artifact probe、lift、merge、validation、policy library 等工具
4. [`agents/`](./agents/)：各 agent 的 deterministic 规则与 LLM refinement
5. [`graph/`](./graph/)：阶段分组、节点包装、编排与运行时
6. [`compatibility/`](./compatibility/)：历史 API 兼容层

根层文件只允许承担以下职责：

1. 包入口与 CLI：
   - [`__init__.py`](./__init__.py)
   - [`__main__.py`](./__main__.py)
2. 对外稳定 schema 与共享 helper：
   - [`schema.py`](./schema.py)
   - [`inventory.py`](./inventory.py)
   - [`utils.py`](./utils.py)
3. 外部 agent 壳层与 provider 初始化：
   - [`agent.py`](./agent.py)
4. 离线 benchmark replay：
   - [`benchmark.py`](./benchmark.py)
5. batch screening 与导出：
   - [`batch.py`](./batch.py)
6. 模块级测试：
   - [`test_review.py`](./test_review.py)
   - [`test_benchmark.py`](./test_benchmark.py)
   - [`test_batch.py`](./test_batch.py)

除上述职责外，新增能力默认不得再落到根层。

## 4. 根层命名规则

根层文件名应保持短、稳、可扫读，避免重新引入 `expert_review_xxx.py` 这类又长又重复的命名。

默认规则：

1. 模块上下文已经由目录名 `expert_review/` 提供，不要再在文件名里重复 `expert_review`
2. 单一职责文件优先使用短名：
   - `agent.py`
   - `schema.py`
   - `inventory.py`
   - `utils.py`
   - `benchmark.py`
3. 如果某类内容已经降级为历史兼容或归档材料，应下沉到 [`legacy/`](./legacy/) 或 [`compatibility/`](./compatibility/)
4. 不要把新的 prompt / rubric / heuristic 聚合大文件重新平铺回根层

## 5. 外部兼容要求

后续重构必须优先保持以下外部入口稳定：

1. `ExpertReviewRequest`
2. `ExpertReviewResult`
3. `review_artifacts()`
4. `review_model()`
5. `python -m expert_review`

历史兼容逻辑统一收敛在 [`compatibility/legacy_api.py`](./compatibility/legacy_api.py)，不要把兼容分支重新散落回其他文件。

## 6. 运行时维护规则

真实主路径以 [`graph/runtime.py`](./graph/runtime.py) 为准。

维护时应遵守：

1. graph 只做编排与阶段连接，不承载大段评分细则
2. agents 负责单节点判断与 refinement 逻辑
3. tools 负责可复用的抽取、校验、merge、policy helper
4. schemas 负责数据结构，不混入 runtime side effect
5. benchmark 不得反向侵入线上运行时依赖

若新增能力涉及多个节点，优先判断它属于：

1. 某个 agent 的职责扩展
2. 某类共享工具的复用能力
3. graph 的编排规则变动

不要把“不知道放哪”的代码继续塞回根层。

## 7. 文档组织规则

设计与演化文档统一放在 [`designs/`](./designs/) 下，并继续按版本分目录维护。

当前重点入口：

1. [designs/v0/README.md](./designs/v0/README.md)
2. [designs/v1/README.md](./designs/v1/README.md)
3. [designs/v1/TODO.md](./designs/v1/TODO.md)
4. [designs/v1/V1_ALIGNMENT_REPORT.md](./designs/v1/V1_ALIGNMENT_REPORT.md)

不要再把新的 `EXPERT_*.md` 平铺回 `reproduction/` 根目录，也不要让 README 与 phase 文档长期失真。

## 8. 测试与回归入口

最低限度的模块级回归入口如下：

1. `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_review.py`
2. `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_benchmark.py`
3. `pytest project_1_llm_state_machine_modeling/reproduction/expert_review/test_batch.py`
4. `python -m expert_review` 的 deterministic smoke
5. [`benchmark.py`](./benchmark.py) 的 `run_benchmark_iteration(llm_mode='off')`
6. `python -m expert_review.benchmark --scope phase7 --llm-mode off --rerun-count 0`
7. `python -m expert_review.batch --input ... --llm-mode off`

只要涉及以下变更，完成后就应至少跑上述三类验证中的相关部分：

1. 根层入口改动
2. graph 编排改动
3. agents 评分或 evidence discipline 改动
4. schema 兼容性改动
5. benchmark harness 改动

## 9. 当前阶段口径

当前目录状态是：

1. `Phase 7` 已完成评测口径固定与 benchmark harness 扩展
2. `Phase 8` 已完成 `record-level` 数值校准、压缩效应修复与 partial-heavy 定向惩罚
3. `Phase 9` 已完成 `summary-level` 排序、public-row score semantics 与高分 public row 收口
4. `Phase 10` 已完成 batch screening 输入协议、triage 阈值、结果导出与 `Milestone A` 验收
5. 当前后续工作的核心目标已转到 `Phase 11+`：`component_level_review`、generalization、evidence reliability 与论文级证据链

因此后续改动默认应优先回答两件事：

1. 这次改动是否真实改善 `CRAS / HAI / RAS / SAS / normalized_mae / unsupported_claim_rate / ece`，并说明它主要影响组件级、`record`、`summary` 还是 batch/generalization surface
2. 这次改动是否会破坏当前已经稳定的 `PDS`、summary evidence discipline、batch triage 口径，以及 `Phase 7` 固定下来的 `full / split / LOFO` 评测框架
