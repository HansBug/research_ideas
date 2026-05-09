"""Pipeline 编排辅助 —— stage 常量 + 共享 state 上下文记录 + 并行执行。

**作用**：

1. 提供 ``PREPARATION_FANOUT`` / ``ANALYSIS_FANOUT`` / ``FINAL_FANIN``
   3 个 stage 元组（与 :mod:`graph.edges` 同名常量内容一致，但本
   包供 agent 内部使用，避免对 :mod:`graph` 的反向依赖）；
2. :func:`record_agent_context` 在 ``state.context_packets`` 中记录
   每个 agent 实际可见的 context keys 与一句话 summary——用于事后
   audit "这个 agent 看到了什么";
3. :func:`record_fanout` 把 stage 内的 fan-out / fan-in 拓扑写到
   ``state.fanout_log``；
4. :func:`run_parallel` 用 ``ThreadPoolExecutor`` 并行跑多个 callable，
   是 PREPARATION 内 input/pred/ref 三个 extractor 与 ANALYSIS 内
   trace/quality/equivalence 三个 agent 并行执行的真正实现。

**设计思路**：

* **轻量并行**：用 ``ThreadPoolExecutor`` 而非 ``asyncio``——agent
  函数本身大多是 IO-bound (LLM call) 或 CPU-bound (parser)，
  Thread pool 简单可靠；
* **不做错误隔离**：``run_parallel`` 不捕获子任务异常，让任一子
  任务失败直接传播——LLM 调用层有自己的 fallback 路径，不需要 pool
  层吞异常；
* **状态写入约定**：``record_*`` 函数对 ``state`` 做 in-place 修改，
  无返回值。
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from ..schemas.graph_state import ReviewGraphState


PREPARATION_FANOUT = (
    "Input Analyst",
    "Prediction Extractor",
    "Reference Extractor",
)

ANALYSIS_FANOUT = (
    "Traceability Agent",
    "Equivalence and Difference Agent",
    "Pragmatic Quality Agent",
)

FINAL_FANIN = (
    "Missing-Evidence Critic",
    # 注：原 "Disagreement Arbiter" 节点已删除（见 graph/edges.py 同位置说明）
    "Score Composer",
    "Final Synthesizer",
)


def record_agent_context(
    state: ReviewGraphState,
    agent_name: str,
    *,
    context_keys: list[str],
    summary: str,
) -> None:
    """把"这个 agent 此时可见的 state 字段"记录到 audit packet。

    :param state: 当前 :class:`ReviewGraphState`
    :param agent_name: agent 标识（如 "Contract Router"）
    :param context_keys: 该 agent 读取的 state 字段名列表
    :param summary: 一句话描述该 agent 此次调用的目的
    """
    state.context_packets[agent_name] = {
        "context_keys": list(context_keys),
        "summary": summary,
    }


def record_fanout(state: ReviewGraphState, stage_name: str, agents: tuple[str, ...]) -> None:
    """记录一次 fan-out / fan-in 的 stage 拓扑到 audit log。

    :param state: 当前 :class:`ReviewGraphState`
    :param stage_name: stage 标识（如 ``"preparation_fanout"``）
    :param agents: 参与该 stage 的 agent 名元组
    """
    state.fanout_log.append(f"{stage_name}: " + " -> ".join(agents))


def run_parallel(
    tasks: dict[str, Callable[[], Any]],
    *,
    max_workers: int | None = None,
) -> dict[str, Any]:
    """用 ``ThreadPoolExecutor`` 并行执行 dict 里的多个 callable。

    :param tasks: 形如 ``{name: callable_no_args}`` 的字典；callable
        必须无参，结果会在返回 dict 中以 name 作 key 存放
    :param max_workers: 线程池上限；``None`` 时取 ``len(tasks)``
    :return: ``{name: callable() 返回值}``
    :rtype: dict[str, Any]

    Examples::

        >>> results = run_parallel({
        ...     "a": lambda: 1 + 1,
        ...     "b": lambda: "hello",
        ... })
        >>> results["a"], results["b"]
        (2, 'hello')
        >>> run_parallel({})
        {}
    """
    if not tasks:
        return {}
    worker_count = max_workers or len(tasks)
    results: dict[str, Any] = {}
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_map = {executor.submit(func): name for name, func in tasks.items()}
        for future, name in list(future_map.items()):
            results[name] = future.result()
    return results


__all__ = [
    "ANALYSIS_FANOUT",
    "FINAL_FANIN",
    "PREPARATION_FANOUT",
    "record_agent_context",
    "record_fanout",
    "run_parallel",
]
