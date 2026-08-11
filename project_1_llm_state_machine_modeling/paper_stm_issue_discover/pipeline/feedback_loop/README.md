# feedback_loop/ — 当前活的 discover 实现

> 🟢 **这里是 paper1 唯一在跑的方法实现。** 改方法、改谓词、改提示词都在本目录。上一版实现在 [../agent_loop/](../agent_loop/)，已退出运行路径，别改错地方。

## 1. 它做什么

给定 `<NL, STM_0>`，把 NL 全覆盖拆成需求条目，为每条转换成**可机械求值的断言**，求值为假的挂钩 issue、为真的构成回归防护。全程只读 `STM_0`，**不修改模型、不做 repair**。

断言只能取自一份**先验闭合的谓词词表**——19 个谓词，按求值机制分结构 `S`（10）/ 仿真 `B`（6）/ 有界模型检查 `P`（3）三族。词表定义在 [`discover/predicates.py`](./src/paper_stm_feedback_loop/discover/predicates.py) 的 `PREDICATES`。

⚠️ **repair 不在本目录的职责内，也不在 paper1 内。** 历史文档里的「Discover / Repair / Confirm 三阶段」「B-final」「closure / regression 作为主线」均已作废：paper1 收窄为 issue discover 单独成篇，repair 另立后续论文。

## 2. StateGraph 阶段

节点与路由定义在 [`discover/graph.py`](./src/paper_stm_feedback_loop/discover/graph.py)：

```text
prepare
  → split_requirements   ──契约不过──▶ 打回自身（带定向反馈）
  → review_requirements  ──revise──▶ split_requirements
  → convert_assertions   ──契约不过──▶ 打回自身
  → precheck_and_seal    ──invalid──▶ convert_assertions
  → review_assertions    ──revise──▶ convert_assertions
  → release_results → bind_attribution → adjudicate_results → publish
```

每个生产阶段配一个审查者，不合格就带**定向反馈**打回重写。任一阶段进入 `failure` 即转 `run_failed`，但仍带着当时的 state 落盘——崩掉的格连「为什么没做到」都不留，这是仓库根 `CLAUDE.md` §10 明令禁止的。

## 3. Discover v2 合同

- Splitter 为每条 Requirement 冻结 `verification_kind=structure/behavior/property`、量词、触发、结果、时序与 coverage obligation。
- 确定性门禁按 kind 限定 primary evidence 族：`structure` 用静态结构/关系/effect/topology/provenance，`behavior` 用 simulation，`property` 用 FBMCQ。
- Assertion 显式区分 `primary` / `supporting`，记录 `coverage_key` 与 `aggregation_group`；只有 attribution-safe 的 primary `False` 能创建 confirmed issue。
- producer 小循环重复 invalid 时先做一次定向恢复；仍无进展则**只隔离坏 item**、保留可执行 peers，并发布 append-only coverage gap。
- `DiscoverCompleted@v2` 始终包含 `coverage_status=full/partial`、`coverage_gaps`、confirmed issues、satisfied requirements 与 excluded observations。`partial + 0 issue` **不是**完整成功。
- 旧 v1 `checkability` 与缺省 Assertion role 只保留读兼容；真实 prompt 与新记录用 v2 字段。

## 4. 有什么

| 路径 | 内容 |
| :-- | :-- |
| [`src/paper_stm_feedback_loop/common/`](./src/paper_stm_feedback_loop/common/) | 输入装载、NL 分段、source trace、不可变 records、telemetry、配置 |
| [`src/paper_stm_feedback_loop/assertions/`](./src/paper_stm_feedback_loop/assertions/) | 断言求值 runtime：parser、checker、结构/仿真/FBMCQ 三族谓词实现、provenance、密封 |
| [`src/paper_stm_feedback_loop/discover/`](./src/paper_stm_feedback_loop/discover/) | StateGraph、节点、prompts、schemas、谓词词表、CLI、渲染器、replay responder |
| [`fixtures/manual_0000_identity/`](./fixtures/manual_0000_identity/) | 自包含 identity 样例，`discover-demo` 用；**不占正式语料** |
| [`fixtures/selected_models/`](./fixtures/selected_models/) | 4 个只读 `.fcstm`（`0000/0006/0029/0050`），确定性工具测试用，带副本 SHA-256 |
| [`tests/`](./tests/) | 1755 个测试：路由、边界、遥测、断言语义、门禁、降级路径、真实入口 |
| [`Makefile`](./Makefile) | 本目录入口；根 `Makefile` 的 `discover*` 目标转发到此 |

`discover/` 里体量最大的三个文件是 `nodes.py`（约 5800 行，全部节点逻辑）、`capability.py`（约 2300 行，证据能力与门禁）、`schemas.py` 与 `prompts.py`（各约 1000–1300 行）。

## 5. 输入从哪来

`--pair-id` 模式下，输入根**不是** [../../selected_seed_examples/](../../selected_seed_examples/)，而是由 [`discover/cli.py`](./src/paper_stm_feedback_loop/discover/cli.py) 的 `REPORT_ROOT` 硬指向：

```text
../representation/reports/llms_emp_r45_java_60/
  pairs/<NNNN>/            nl.txt、plantuml.puml、fcstm.fcstm
  source_traces/<pair_id>.json
  working_contracts/<pair_id>.json
```

路径按模块文件位置解析，不依赖进程工作目录，因此 `make -C` 与直接 `python -m` 落在同一个根上。`--report-root` 可覆盖。`selected_seed_examples/` 是逐字节相同的人读镜像，只有退役的 `paper_stm_repair_loop.inputs.load_pair()` 读它。

## 6. 怎么用

运行真实模型前必须先在 shell 执行 `source .env`。代码只读 `os.environ`，不解析 `.env`。

```bash
# 仓库根目录（推荐）
make discover-demo
make discover-pair DISCOVER_PAIR=llms_emp_feedback_final_0029 DISCOVER_PROFILE=gpt-5.5
make discover-test

# 本目录 Makefile
make -C .../pipeline/feedback_loop discover-demo
make -C .../pipeline/feedback_loop discover-pair PAIR_ID=llms_emp_feedback_final_0029 PROFILE=gpt-5.5
make -C .../pipeline/feedback_loop test        # 亦有 lint / compileall / help
```

等价 Python 入口：

```bash
PYTHONPATH=.../pipeline/feedback_loop/src:$PWD \
python -m paper_stm_feedback_loop.discover --help
```

`Makefile` 变量：`PROFILE`（默认 `gpt-5.5`）、`CONTENT_LANGUAGE`（默认 `zh-CN`）、`PAIR_ID`（默认 `llms_emp_feedback_final_0000`）、`OUT`（默认 `runs/paper1/feedback-loop/discover`）、`ARGS`（透传 CLI 参数）。

### 有默认值的 FBMCQ 上限是策略，不是「未设资源限制」

`--fbmcq-solver-timeout-ms=30000`、`--fbmcq-max-bound=8`、`--fbmcq-process-wall-seconds=60`、`--fbmcq-canary-bound=3`、`--fbmcq-canary-wall-seconds=45`、`--transport-retries=4` 均有默认值，且**逐次记入 run record**。原因写在 `cli.py` 注释里：有界模型检查没有自然终止保证，公式构造本身在稠密迁移关系上随 bound 指数增长，`process.join(None)` 曾把 pair `0029` 的一条坏断言变成 495 秒 precheck 与一次人工 kill。

`--max-output-tokens`、`--assertion-timeout-seconds` 无默认值，只在调用者显式传入时生效。

## 7. 学术边界

- 台账里的 taxonomy、expected issue、缺陷描述与 gold assertion **只允许在 graph terminal 之后** 用于 evaluator 侧审计，禁止进入 runtime 与任何 prompt 通道。
- 泄漏审查覆盖**全部进入模型的文本**，包括门禁报错文案、revision feedback、渲染器插入的说明——这些是**运行时生成**的，静态 grep prompt 常量抓不到。
- 报告由确定性 Python renderer 从不可变 records 生成，LLM 不写报告结构。
- 每次运行必须保存所有 node / LLM / transport attempt 的时间与 usage。

## 8. 相关入口

- [../README.md](../README.md)：pipeline 导航与「哪个目录在跑」判定表
- [../../discover_matrix/](../../discover_matrix/)：评测、台账、判定口径、代次结果
- [../../discover_matrix/docs/protocol/](../../discover_matrix/docs/protocol/)：判定口径文档；**改它们等于改研究规则**
- [../agent_loop/README.md](../agent_loop/README.md)：上一版实现的设计记录
