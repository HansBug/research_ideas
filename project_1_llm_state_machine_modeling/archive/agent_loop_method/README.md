# `method/` — Agent Loop method package（功能入口与证据边界）

> **位置**：`project_1_llm_state_machine_modeling/method/`
>
> **服务对象**：Project 1 的 NL → pyfcstm / FCSTM 状态机建模 agent-loop 基础设施，供 Path 1 hard comparison、Path 2 differentiation、repo-local skill/ref-model 生产与后续 verification/repair 研究复用。
>
> **当前状态（PR39 / LG-M1-G final，2026-06-08）**：LG-M1-A/B/C1/C2/D1/D2/D3/E/F/G 已完成并 merge 回 umbrella [PR #64](https://github.com/HansBug/research_ideas/pull/64)，随后通过 [PR #39](https://github.com/HansBug/research_ideas/pull/39) 合入 PR #22 伞形分支。本目录已完成 stage API、实验入口功能命名、LangGraph runtime 模块化、测试树镜像迁移、docs/provenance 收口和最终四例 retained evidence；当前最终验证基线为 `432 passed, 6 warnings`。
>
> **历史说明**：早期 `dev/method-agent-implementation`、PR-B2、PR-C、PR-E1、PR-E2 等 marker 保留为 historical provenance，不再代表当前推荐入口。读者应优先从本文件、[ARCHITECTURE.md](./ARCHITECTURE.md) 与 [STATUS.md](./STATUS.md) 顶部 current overlay 进入。

## 0. 当前功能入口地图

| 领域 | 当前推荐入口 | 用途 | 历史 / compatibility 说明 |
|---|---|---|---|
| 默认完整 agent loop | [`loop.py`](./loop.py) 中 `method.loop.run_agent_loop(...)` | Path1/Path2 主 agent-loop runtime；默认 LangGraph full staged path | 旧 A0-A4 loop 已退出 active API；不要调用 `method.legacy_loop` |
| Stage deterministic / control API | [`stages/api.py`](./stages/api.py)、[`stages/sc_control.py`](./stages/sc_control.py) | Codex/Claude skill、工具箱、单 stage 检查与外部流程编排 | LG-M1-B 后的稳定 Pythonic API；不读 `.env`、不调用 provider |
| SL prompt facade | [`stages/sl_prompt_api.py`](./stages/sl_prompt_api.py) | 生成 `SL-*` prompt / schema 输入，供外部 agent 自行调用 LLM | skill/ref-model producer 应走 prompt facade，而不是直接调用 full loop |
| Real run matrix | [`experiments/real_run_matrix.py`](./experiments/real_run_matrix.py) | 真实四例/多样本运行与 evidence 汇总 | [`pr_e1_real_runs.py`](./pr_e1_real_runs.py) 仅为 compatibility shim |
| Checkpoint / resume experiment | [`experiments/checkpoint_resume.py`](./experiments/checkpoint_resume.py) | checkpoint/resume smoke 与相关实验 | [`pr_lg_f1_resume_experiment.py`](./pr_lg_f1_resume_experiment.py) 仅为 compatibility shim |
| Representative cases | [`experiments/representative_cases.py`](./experiments/representative_cases.py) | ABS / Elevator / CARA / LNG 等代表样本 catalog | [`pr_d_representative.py`](./pr_d_representative.py) 仅为 compatibility shim |
| Deterministic ablation | [`experiments/ablation/deterministic_loop.py`](./experiments/ablation/deterministic_loop.py) | replay / deterministic / ablation 对照 | [`pr2a_loop.py`](./pr2a_loop.py) 仅为 compatibility shim |
| LangGraph implementation | [`langgraph/`](./langgraph/) 与 [`langgraph_runtime.py`](./langgraph_runtime.py) | nodes、subgraphs、instrumentation、checkpoint、core runtime | `method.langgraph_runtime` 保持 public compatibility facade 与 run-record identity |
| Tests | [`tests/`](./tests/) | method 单元/表征/contract 测试总入口 | LG-M1-E 后按 `stages/`、`langgraph/`、`experiments/`、`llm/`、`crosscutting/`、`handoff_smoke/`、`agent_loop_skill/` 镜像组织 |
| Repo-local skill | [`agent_loop_skill/AGENT_LOOP_SKILL.md`](./agent_loop_skill/AGENT_LOOP_SKILL.md) | 给 Codex / Claude Code 使用 stage tools 与 prompt 规范 | skill 侧不得调用 `method.loop.run_agent_loop(...)` 作为一键 ref-model 生成器 |
| Handoff smoke | [`handoff_smoke/`](./handoff_smoke/) | 历史 PR-3 Path1/Path2 infrastructure compatibility smoke | 真实 provider 命令只用于显式 handoff smoke；当前最终四例 evidence 以 `experiments/real_run_matrix.py` retained runs 为准 |

## 1. 当前默认 runtime 语义

`method.loop.run_agent_loop(nl, LoopConfig())` 是 canonical full staged runtime，默认解析为 `experiment_default/full_staged_v1` 并调用 LangGraph full staged path。默认 stage graph：

```text
SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SC-12 -> SC-13
```

当前 repair 主链为：

```text
SD-8 FixRequestBatch -> SL-9 per-request accept/reject + repair -> SL-10(NL + FixLog + local_check_evidence) -> SC-11 -> SD-2 full revalidation
```

关键证据边界：

1. 默认入口不回退 fake / mock / replay provider；缺少 provider 配置、provider/schema retry 耗尽或 schema invalid 时，会写出 `AgentLoopRunRecord` 并以 `provider_error` / `invalid` 等可审计 verdict 退出。
2. `AgentLoopRunRecord` 记录 resolved config、condition hash、environment、provider/model 脱敏标识、stage/iteration/repair/scenario/LLM trace、eligibility、redaction report 与 final artifacts。
3. 非默认/weak oracle/provider error/schema invalid/write failure 不得进入高可信主结果。
4. 消融实验必须显式声明非默认 `condition_id` 与 `changed_factors`；关闭 stage、改 budget、改 oracle、禁用 review、切 fake/replay provider 等配置不得污染 `LoopConfig()` 默认路径。

## 2. LLM env 接入约束

真实 LLM 调用统一走仓库根 `.env` 三件套，但代码只读进程环境变量，不直接读取 `.env` 文件：

```text
LLM_ENDPOINT  — OpenAI-compatible proxy URL
LLM_API_KEY   — Bearer token
LLM_MODEL     — 主跑模型名
```

约束：

1. **只有真实 provider run**（例如 LG-M1-G 四例、handoff smoke `--real-llm`、正式 Path1/Path2 实验）才需要在 shell 中 `set -a; source .env; set +a`。
2. docs/provenance scan、pytest collection、unit tests、skill health check 默认不得读取 `.env`、不得调用真实 provider。
3. `method/gpt_client.py` 是仓库中唯一允许实例化 OpenAI-compatible client 的位置；所有 agent / baseline replication / judge adapter 均应注入或复用该 client。
4. stream 纪律、retry/timeout policy 与 `max_tokens=None` 口径属于 runtime/evidence contract；最终四例 retained evidence 已按该 contract 留档。

## 3. pyfcstm 集成方式

`pyfcstm` 作为 git submodule pin 到仓库根 `pyfcstm/`。首次 clone 或更新后：

```bash
git submodule update --init --recursive
venv/bin/pip install -e ./pyfcstm
```

method 代码内一律以 `from pyfcstm.dsl import parse_with_grammar_entry` 等正常 import 使用。

## 4. 当前目录结构

```text
method/
├── README.md
├── ARCHITECTURE.md
├── STATUS.md
├── loop.py                         # public run_agent_loop entry
├── langgraph_runtime.py            # public compatibility facade / run-record identity
├── langgraph/                      # LangGraph implementation modules
│   ├── constants.py
│   ├── state.py
│   ├── registry.py
│   ├── checkpointing.py
│   ├── core.py
│   ├── nodes/
│   ├── subgraphs/
│   └── instrumentation/
├── stages/                         # SC/SD/SL deterministic tools + prompt/control API
│   ├── api.py
│   ├── sc_control.py
│   ├── sl_prompt_api.py
│   └── docs/
├── experiments/                    # 功能命名实验入口
│   ├── real_run_matrix.py
│   ├── checkpoint_resume.py
│   ├── representative_cases.py
│   └── ablation/deterministic_loop.py
├── agent_loop_skill/               # repo-local skill docs/tools
├── handoff_smoke/                  # historical Path1/Path2 handoff smoke
├── feedback/                       # parse / semantic / sim / cascade helpers
├── agents/                         # older single/multistep/scenariogen agents
├── prompts/                        # grammar / prompt assets
├── eval/                           # component extraction/evaluation helpers
└── tests/                          # LG-M1-E mirror test tree
    ├── stages/
    ├── langgraph/
    ├── experiments/
    ├── llm/
    ├── crosscutting/
    ├── handoff_smoke/
    └── agent_loop_skill/
```

Compatibility shim（例如 [`pr_e1_real_runs.py`](./pr_e1_real_runs.py)、[`pr_lg_f1_resume_experiment.py`](./pr_lg_f1_resume_experiment.py)、[`pr_d_representative.py`](./pr_d_representative.py)、[`pr2a_loop.py`](./pr2a_loop.py)）只用于旧 PR comment reproduction path 和历史脚本兼容；新代码和新文档应优先使用 `experiments/` 下的功能命名入口。

## 5. 本地验证入口

### 5.1 docs / tests-only gate（不读 `.env`，不调用 provider）

```bash
source venv/bin/activate
PYTHONPATH=project_1_llm_state_machine_modeling \
  python -m pytest --collect-only -q project_1_llm_state_machine_modeling/method/tests
PYTHONPATH=project_1_llm_state_machine_modeling \
  python -m pytest -q project_1_llm_state_machine_modeling/method/tests
```

LG-M1-F 的历史验收重点是 docs/provenance scan、旧路径清理、pytest collection/full method tests。当前 PR39/LG-M1-G final 已在其后补齐最终四例真实 provider retained evidence；不要再把 LG-M1-F 的 no-provider 边界误读为当前最终状态。

### 5.2 真实四例 / provider run（仅显式需要时）

最终 integrated 四例已由 LG-M1-G / PR39 retained evidence 负责。若后续需要复跑或扩展实验，运行前必须显式加载环境变量：

```bash
source venv/bin/activate
set -a; source .env; set +a
# 之后再调用 method.experiments.real_run_matrix 等真实 provider runner
```

PR comment 中不得回显 raw key / endpoint；必须报告脱敏 provider/model、run_id、artifact path、record status、verdict、eligibility 与 secret scan 结果。

## 6. 新 session 接管入口

建议阅读顺序：

1. 本 [README.md](./README.md)：快速确认当前功能入口与禁改边界。
2. [ARCHITECTURE.md](./ARCHITECTURE.md)：查看 LG-M1 当前事实、命名 provenance 分类、runtime/module/test 边界。
3. [STATUS.md](./STATUS.md)：只看顶部 current overlay；下方 Phase A-J 是历史 sprint 记录。
4. 如处理 skill/ref-model：读 [agent_loop_skill/AGENT_LOOP_SKILL.md](./agent_loop_skill/AGENT_LOOP_SKILL.md)。
5. 如处理真实四例或 final integration：读 [`experiments/real_run_matrix.py`](./experiments/real_run_matrix.py) 与 #64 / 对应子 PR 的最新 body/comment。

## 7. 历史进度说明

早期 Phase A-J、PR-B2、PR-C、PR-E1、PR-E2、PR-3 handoff smoke 等记录仍保留在 [STATUS.md](./STATUS.md)、[EXAMPLES.md](./EXAMPLES.md) 与 [handoff_smoke/](./handoff_smoke/) 中，用于解释 agent-loop 的演化来源与历史 evidence。它们不应覆盖当前功能入口地图；凡涉及新实验、新文档或 skill 使用，默认以本 README 与 [ARCHITECTURE.md](./ARCHITECTURE.md) 的 LG-M1 current facts 为准。
