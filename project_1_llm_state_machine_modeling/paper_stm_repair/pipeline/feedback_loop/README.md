# feedback_loop：paper1 可执行反馈循环

本路径是 paper1 新的 Discover / Repair / Confirm 方法实现入口。当前 PR 只实现 `B-discover`；后续阶段再增加 Repair、Confirm 和确定性顶层 orchestrator。

## 边界

- 新 package 固定为 `paper_stm_feedback_loop`。
- 运行时禁止 import 旧 `paper_stm_repair_loop` 或把 `pipeline/agent_loop/src` 加入 `PYTHONPATH`。
- 旧 `pipeline/agent_loop/` 只作为一次性代码搬运与 golden fixture 来源，概念上已 deprecated，但本 PR 不删除它。
- 可以直接使用根级 `utils.llm`、pyfcstm 公共 API、LangGraph、LangChain Core、Pydantic 和标准库。
- Issue #166 的 taxonomy、expected issue、描述和 gold assertion 只允许在 graph terminal 后用于 evaluator-side 审计，禁止进入 runtime。

完整节点、遥测、密封结果与学术边界合同见 [Issue #167](https://github.com/HansBug/research_ideas/issues/167)，施工状态见 [PR #168](https://github.com/HansBug/research_ideas/pull/168)。

## 目录

```text
src/paper_stm_feedback_loop/
  common/       输入、source trace、不可变 records 与 telemetry
  assertions/   Discover 与后续 Confirm 共享的可执行断言 runtime
  discover/     StateGraph、direct LLM responder、prompts、schemas、CLI、renderer
fixtures/       自包含 golden/parity 与 manual identity 输入
tests/          route、边界、遥测、断言和真实入口的确定性回归
```

## 入口

运行真实模型前必须先在 shell 执行 `source .env`。

```bash
make -C project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop discover-demo

make -C project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop discover-pair \
  PAIR_ID=llms_emp_feedback_final_0029 PROFILE=gpt-5.5

make -C project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop test
```

等价 Python 入口：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop/src:$PWD \
python -m paper_stm_feedback_loop.discover --help
```

资源限制只允许调用者显式传入；默认不设置业务预算。每次运行必须保存所有 node/LLM/transport attempt 的时间与 usage，并从 immutable records 确定性渲染报告。

## 预注册 pilot

当前双模型验收固定使用：

1. `manual-0000-identity`：非论文 plumbing fixture；
2. 正式 pair `0000`：终止类错误抽查；
3. 正式 pair `0029`：层次、冲突与局部完成压力样例；
4. 正式 pair `0006`：effect/action 样例；
5. 正式 pair `0050`：E0/无支持 finding 负例。

两种 profile 固定为 `gpt-5.5` 与 `claude-opus-4-7`。输入完整 hash、选择规则和禁止泄漏合同以 PR #168 body 为准。
