# Paper1 发布结构迁移计划

## 目的与边界

本计划只重组已冻结的 current method、Semantic Judge、离线 evaluation、脚本、测试和 legacy。不得修改 LLM prompt、LLM-facing schema、19 个谓词、输入闭包、compiler/backend、W/D 规则、Judge protocol 或 `final_results/`。迁移等价性以基线 manifest、字节哈希、provider-free 测试、归档复算和 clean-install 为证据；不是以新的全量实验取代验证。

基线由 `scripts/release/capture_release_baseline.py` 在开始移动前生成到 `release/baseline_manifest.json`。它保存当前 HEAD、465 个 pytest node ID、生产文件与冻结归档逐文件 SHA-256、运行环境和外部依赖。该脚本不导入 method/Judge，也不发起 provider 调用。

## 所有权表

| 当前位置 | 新归属 | 使用者 | provider-facing | 迁移策略 | 验证 |
| --- | --- | --- | --- | --- | --- |
| `pipeline/evidence_discovery/{inputs,semantics,registry,compiler,backends,evidence,orchestration}` | `method/src/paper_stm_method/` | method CLI | 是 | 保持文件内容的机械迁移；旧 `pipeline.evidence_discovery` 仅作 re-export shim | 465-node 回归、fixture differential、release install |
| `pipeline/evidence_discovery/reporting/export.py` | method artifact writer | method runner | 否 | 移入 method；保留旧 import shim | artifact JSON/Markdown fixture 对拍 |
| 其余 `pipeline/evidence_discovery/reporting/` | `evaluation/src/paper_stm_evaluation/` | evaluator/reporting CLI | 否 | 机械迁移，旧路径作 shim | archive validator、离线复算 |
| `pipeline/semantic_judge/` | `judge/src/paper_stm_judge/` | Judge CLI | 是 | 机械迁移；将 shared runtime 转为 `utils`，固定 pair input 改为只读 adapter | mocked Judge fixture、import boundary |
| `pipeline/evidence_discovery/{replay,route_replay,frontier_replay,execution_probe_replay,structural_rebind_replay}.py`、`inputs/native_projection_audit.py`、`orchestration/cost_correction.py` | `scripts/{method,evaluation}/` 薄入口 + 所属库 | 维护者 | 否 | CLI 包装；库逻辑留所属包 | provider-free CLI tests |
| `pipeline/feedback_loop/` | `archive/legacy/feedback_loop/` | 历史回放 | 是 | `git mv`，不进入默认安装或 current imports | legacy import exclusion scan |
| `utils.agent`、`utils.llm` 与中性 structured runtime | 顶层 `utils/` | method/Judge | 是 | 仅机械下沉共享 runtime | JSON/exception/cost differential |

## Import 方向

`method -> utils`；`judge -> utils`；`evaluation -> method/judge 的公开 artifact schema 或只读 adapters`；`scripts -> method/judge/evaluation`；`legacy -> utils`。反向 import 均禁止。特别是 Judge 不得 import method，method 不得 import Judge 或 evaluation，顶层 `utils` 不得 import paper1 包或实验配置。

## 资源与兼容性

predicate registry、source catalog 和 Judge issue #195 snapshot 保留原始字节与哈希。发布包内的受控副本由资源一致性测试对拍权威来源；加载使用 `importlib.resources` 或显式资源根，不允许依赖仓库深度。旧模块路径可保留无业务逻辑的兼容 re-export，兼容层不进入 method release allowlist。

`build_method_release.py` 与 `build_judge_release.py` 都只能从干净 tracked Git tree
按其机器可读 allowlist 作字节复制，输出必须位于 checkout 外。method 发布清单只含
method 和中立 `utils`；Judge 发布清单只含 Judge、issue #195 snapshot 和同一份中立
`utils`。两者都不复制对方的业务代码、ledger、baseline、final results 或 runs。

## 风险与暂缓项

- `runner.py`、`frontier.py` 不做内部拆分；只允许整体机械迁移。
- 已知 29 个 Pydantic `schema` shadow warning 仅记录，不改变 LLM-facing schema。
- 任一结构改动如果要求修改冻结语义，保留 shim 并登记技术债，不通过重新跑 54x3 掩盖。
- 15x1 live regression 只能在所有离线验收、release-candidate commit 和 clean-install 通过后执行一次。
