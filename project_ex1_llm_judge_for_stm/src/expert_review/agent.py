"""``ExpertReviewAgent`` —— LLM-as-STM-Judge pipeline 的对外主入口。

**作用**：

1. 装配 fallback LLM chain（多 provider 链路 + cooldown 状态机），
   屏蔽 provider 选择 / 切换 / 超时控制等底层细节；
2. 把 :class:`schema.ExpertReviewRequest` 交给
   :func:`graph.runtime.run_expert_review_workflow` 跑完整 3-stage
   pipeline，返回 :class:`schema.ExpertReviewResult`；
3. 暴露与 ``compatibility/legacy_api.review_artifacts`` 等历史 API
   等价的入口，但内部走的是新版 graph runtime。

**设计思路**：

1. **薄壳**：本 class 不做业务判断（不算 score、不调度 agent），
   只负责 LLM client 装配 + 一次 ``run_expert_review_workflow`` 调用；
2. **provider 链路对外不可见**：构造时下发 ``provider_order`` 列表，
   :class:`fallback_llm.FallbackLLMClient` 在 chain 内部按 cooldown
   状态机自动切换；外部只通过 ``last_provider_used`` 观察实际命中
   的 provider；
3. **LLM 不可用降级路径**：当 chain 装配为空（无任何可用 provider /
   API key 缺失）时，``self._llm = None``，``review()`` 走
   ``backend_label += "_deterministic"`` 的 deterministic-only
   路径——所有 6 维度仍会产出 score，但来自启发式 / trace_ratio 等
   信号而非 LLM；
4. **strict-llm 不在本 class 实现**：``benchmark.py`` 提供的
   ``strict_llm`` flag 是 eval 时的 task skip 控制，不是 agent 级
   开关；本 class 默认行为是"LLM 抛异常时 raise 上层"，与 strict
   语义协同。

**关键约束 / 不变式**：

* :func:`__init__` 必须能在 LLM 缺失时也成功构造（用于 dry-run /
  CI 测试 / strict_llm=False 的兜底实验）；不允许构造时硬抛；
* :meth:`review` **不会静默 fallback** 到 deterministic—— 一旦
  ``self._llm is not None`` 但 LLM 调用过程抛异常，异常会上抛到
  调用方；
* ``self._provider_key`` 是 *primary* provider（chain 第一个）的
  标识，仅用于回填 :attr:`ExpertReviewResult.llm_provider` 字段；
  实际命中的 provider 由 telemetry 维护。

**已知 caveat**：

* 见 issue I-4 ：``rubric_scorer`` 内部对 LLM 失败仍有 deterministic
  fallback（与本 class "不静默 fallback" 的纪律存在层级差异）；
* 见 issue I-7 ：k-rep noise floor 协议未在 agent 层实现，由
  ``benchmark.py::_rerun_subset`` 在 eval 层做 2-rep。

参考：

* 主讨论 §3 / §3.7 final products
* 实现 issue I-4 / I-7 / I-13
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from .fallback_llm import FallbackLLMClient, build_fallback_chain
from .schema import ExpertReviewRequest, ExpertReviewResult
from .utils import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER_ORDER,
    PROVIDER_CONFIGS,
    PROVIDER_COOLDOWN_SECONDS,
    PROVIDER_FALLBACK_TIMEOUT,
    DEFAULT_COOLDOWN_SECONDS,
    resolve_api_env,
)
from .graph.runtime import run_expert_review_workflow


class ExpertReviewAgent:
    """LLM-as-STM-Judge pipeline 的同步入口 Agent。

    本 class 是用户侧 API 的 "薄壳"——只做两件事：
    (a) 在 :meth:`__init__` 中装配 fallback LLM chain；
    (b) 在 :meth:`review` 中把请求转给 graph runtime。

    :ivar model_name: LLM model 标识符（如 ``"gpt-4o-2024-08-06"``）
    :ivar provider_order: provider 优先级列表，按本顺序尝试 fallback；
        默认 ``DEFAULT_PROVIDER_ORDER``
    :ivar temperature: LLM 调用温度（默认 0.0 贪心解码，仍存在
        残余非确定性，见 noise floor 协议 issue I-7）
    :ivar timeout: 整个 fallback 链上限秒数（默认 180）；单次 attempt
        受 ``PROVIDER_FALLBACK_TIMEOUT`` 约束更紧

    Examples::

        >>> # 注：实际构造需要环境中存在 provider API key；这里只演示 API 形态
        >>> agent_class_doc = ExpertReviewAgent.__doc__
        >>> "LLM-as-STM-Judge" in agent_class_doc
        True
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        provider_order: list[str] | None = None,
        temperature: float = 0.0,
        timeout: int = 180,
    ) -> None:
        """构造一个 ExpertReviewAgent；不可用 provider 时不会抛错。

        :param model: LLM model 标识符
        :param provider_order: provider 优先级列表；``None`` 时使用
            ``DEFAULT_PROVIDER_ORDER``
        :param temperature: LLM 调用温度（默认 0.0）
        :param timeout: 整个 fallback chain 调用上限秒数（默认 180）

        构造流程：
            1. 复制 ``provider_order`` 到实例字段（避免共享可变 default）
            2. 计算 ``_per_attempt_timeout = min(timeout, PROVIDER_FALLBACK_TIMEOUT)``
            3. 调用 :meth:`_build_llm` 装配 chain
            4. 若 chain 为空（无可用 provider），``_llm`` 设为 ``None``
               —— :meth:`review` 后续走 deterministic-only 路径

        .. note::
            构造**不会**因缺少 API key / 缺少 provider 配置而抛错；
            这是为了让 CI / dry-run / strict_llm=False 兜底实验
            都能成功构造 agent 实例。
        """
        self.model_name = model
        self.provider_order = list(DEFAULT_PROVIDER_ORDER) if provider_order is None else list(provider_order)
        self.temperature = temperature
        self.timeout = timeout
        # 使用更短的 per-attempt 超时让 fallback chain 能 fail-fast 切换；
        # 用户传入的 ``timeout`` 视作整链路上限。
        self._per_attempt_timeout = min(int(timeout), PROVIDER_FALLBACK_TIMEOUT)
        self._provider_key, self._llm = self._build_llm()

    def _build_llm(self) -> tuple[str | None, FallbackLLMClient | None]:
        """内部辅助：解析环境变量并装配 fallback chain。

        :return: 二元组 ``(primary_provider_key, FallbackLLMClient)``；
            chain 为空时返回 ``(None, None)``
        :rtype: tuple[str | None, FallbackLLMClient | None]

        步骤：
            1. ``resolve_api_env()`` 读环境变量
            2. ``build_fallback_chain()`` 按 ``provider_order``
               逐个试装；缺 API key 的 provider 自动跳过
            3. 用 ``PROVIDER_COOLDOWN_SECONDS`` /
               ``DEFAULT_COOLDOWN_SECONDS`` 包裹为 ``FallbackLLMClient``
            4. 返回 chain 第一个 provider 的 key（用于回填 result
               的 ``llm_provider`` 字段，做 backward-compat）
        """
        env = resolve_api_env()
        chain = build_fallback_chain(
            model=self.model_name,
            provider_order=self.provider_order,
            provider_configs=PROVIDER_CONFIGS,
            env=env,
            temperature=self.temperature,
            timeout=self._per_attempt_timeout,
        )
        if not chain:
            return None, None
        client = FallbackLLMClient(
            chain,
            cooldown_seconds=PROVIDER_COOLDOWN_SECONDS,
            default_cooldown=DEFAULT_COOLDOWN_SECONDS,
        )
        # 向后兼容：把 chain 第一个 provider 作为 "provider_key"。
        # telemetry 可通过 ``client.last_provider_used`` 读真实命中的 provider。
        return client.primary_provider_key, client

    def review(self, request: ExpertReviewRequest) -> ExpertReviewResult:
        """同步执行一次完整评审 pipeline，返回结构化结果。

        :param request: 待评审的请求（NL 需求 + 制品 + 可选 reference
            + metadata）
        :return: :class:`schema.ExpertReviewResult` 实例
        :rtype: ExpertReviewResult
        :raises Exception: 当 ``self._llm is not None`` 时，LLM 调用链
            抛出的任何异常会上抛——本方法 **不静默 fallback**。当
            ``self._llm is None`` 时则走 deterministic-only 路径，不会
            因 LLM 不可用而失败。

        backend_label 后缀规则：

        - ``self._llm is None`` → ``"langgraph_multi_agent_v1_deterministic"``
        - ``self._llm is not None`` → ``"langgraph_multi_agent_v1_llm"``

        这个标签会写入 :attr:`ExpertReviewResult.used_review_backend`
        供 benchmark 区分实验配置。
        """
        backend_label = "langgraph_multi_agent_v1"
        if self._llm is None:
            return run_expert_review_workflow(
                request,
                llm=None,
                llm_model_name=None,
                llm_provider=None,
                backend_label=f"{backend_label}_deterministic",
            )
        # 2026-05-08: 默认不再静默 fallback 到 deterministic。
        # LLM workflow 抛异常时直接 raise，由 caller (例如 strict_llm 校验)
        # 决定如何处理；这避免了 "silent degrade to deterministic" 造成的
        # 实验数据失真。
        return run_expert_review_workflow(
            request,
            llm=self._llm,
            llm_model_name=self.model_name,
            llm_provider=self._provider_key,
            backend_label=f"{backend_label}_llm",
        )
