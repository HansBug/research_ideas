from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

from pydantic import BaseModel

from paper_stm_feedback_loop.assertions import AssertionChecker, InMemorySealedStore

from . import nodes
from .schemas import (
    AssertionReview,
    DiscoverCompleted,
    DiscoverGraphState,
    DiscoverInput,
)
from .utils import sha256_data

Route = Literal[
    "split_requirements",
    "convert_assertions",
    "precheck_and_seal",
    "review_assertions",
    "release_results",
    "bind_attribution",
    "adjudicate_results",
    "publish",
    "run_failed",
]


def route_after_prepare(state: DiscoverGraphState) -> Route:
    return "run_failed" if "failure" in state else "split_requirements"


def route_after_requirement_review(state: DiscoverGraphState) -> Route:
    if "failure" in state:
        return "run_failed"
    review = state["requirement_review"]
    return "split_requirements" if review.decision == "revise" else "convert_assertions"


def route_after_assertion_check(state: DiscoverGraphState) -> Route:
    if "failure" in state:
        return "run_failed"
    public = state["assertion_check_public"]
    return "convert_assertions" if public.status == "invalid" else "review_assertions"


def route_after_assertion_review(state: DiscoverGraphState) -> Route:
    if "failure" in state:
        return "run_failed"
    review = state["assertion_review"]
    return "convert_assertions" if review.decision == "revise" else "release_results"


def route_after_linear_node(state: DiscoverGraphState, next_node: Route) -> Route:
    return "run_failed" if "failure" in state else next_node


class _HashPatchingResponder:
    """Small fake-run helper; real responders must not need output patching."""

    def __init__(self, inner: nodes.StructuredResponder) -> None:
        self._inner = inner
        self.current_script_hash: str | None = None

    def invoke_structured(
        self, *, role: str, schema: type[Any], system_prompt: str, user_input: str
    ) -> Any:
        output = self._inner.invoke_structured(
            role=role, schema=schema, system_prompt=system_prompt, user_input=user_input
        )
        if (
            isinstance(output, AssertionReview)
            and output.reviewed_script_hash == "TO_BE_PATCHED"
            and self.current_script_hash
        ):
            return output.model_copy(
                update={"reviewed_script_hash": self.current_script_hash}
            )
        return output

    def take_last_observation(self) -> Any:
        take = getattr(self._inner, "take_last_observation", None)
        return take() if callable(take) else None


def build_discover_graph(
    responder: nodes.StructuredResponder | None = None,
    *,
    assertion_checker: AssertionChecker | None = None,
) -> Any:
    """Build the explicit LangGraph StateGraph for Discover.

    LLM nodes are direct structured-response call sites. They do not create legacy agent runtimes
    or business-tool loops. Deterministic nodes call prepare, assertions,
    release, attribution, and publish functions.
    """

    try:
        from langgraph.graph import END, START, StateGraph
    except (
        ImportError
    ) as exc:  # pragma: no cover - langgraph is available in CI/dev envs
        raise RuntimeError(
            "langgraph is required to build the Discover StateGraph"
        ) from exc

    active_responder = responder or nodes.CallableStructuredResponder(
        nodes.default_fake_responder
    )
    patching_responder = _HashPatchingResponder(active_responder)
    sealed_store = InMemorySealedStore()

    def _prepare(state: DiscoverGraphState) -> DiscoverGraphState:
        return nodes.prepare(state)

    def _split(state: DiscoverGraphState) -> DiscoverGraphState:
        return nodes.split_requirements(state, patching_responder)

    def _review_requirements(state: DiscoverGraphState) -> DiscoverGraphState:
        return nodes.review_requirements(state, patching_responder)

    def _convert(state: DiscoverGraphState) -> DiscoverGraphState:
        return nodes.convert_assertions(state, patching_responder)

    def _check(state: DiscoverGraphState) -> DiscoverGraphState:
        patching_responder.current_script_hash = sha256_data(state["assertion_script"])
        return nodes.precheck_and_seal(
            state, sealed_store=sealed_store, assertion_checker=assertion_checker
        )

    def _review_assertions(state: DiscoverGraphState) -> DiscoverGraphState:
        patching_responder.current_script_hash = sha256_data(state["assertion_script"])
        return nodes.review_assertions(state, patching_responder)

    def _release(state: DiscoverGraphState) -> DiscoverGraphState:
        return nodes.release_results(state, sealed_store=sealed_store)

    def _attribution(state: DiscoverGraphState) -> DiscoverGraphState:
        return nodes.bind_attribution(state)

    def _adjudicate(state: DiscoverGraphState) -> DiscoverGraphState:
        return nodes.adjudicate_results(state, patching_responder)

    def _publish(state: DiscoverGraphState) -> DiscoverGraphState:
        return nodes.publish(state)

    def _run_failed(state: DiscoverGraphState) -> DiscoverGraphState:
        return state

    graph = StateGraph(DiscoverGraphState)
    graph.add_node("prepare", _prepare)
    graph.add_node("split_requirements", _split)
    graph.add_node("review_requirements", _review_requirements)
    graph.add_node("convert_assertions", _convert)
    graph.add_node("precheck_and_seal", _check)
    graph.add_node("review_assertions", _review_assertions)
    graph.add_node("release_results", _release)
    graph.add_node("bind_attribution", _attribution)
    graph.add_node("adjudicate_results", _adjudicate)
    graph.add_node("publish", _publish)
    graph.add_node("run_failed", _run_failed)
    graph.add_edge(START, "prepare")
    graph.add_conditional_edges("prepare", route_after_prepare)
    graph.add_edge("split_requirements", "review_requirements")
    graph.add_conditional_edges("review_requirements", route_after_requirement_review)
    graph.add_edge("convert_assertions", "precheck_and_seal")
    graph.add_conditional_edges("precheck_and_seal", route_after_assertion_check)
    graph.add_conditional_edges("review_assertions", route_after_assertion_review)
    graph.add_edge("release_results", "bind_attribution")
    graph.add_edge("bind_attribution", "adjudicate_results")
    graph.add_conditional_edges(
        "adjudicate_results", lambda state: route_after_linear_node(state, "publish")
    )
    graph.add_edge("publish", END)
    graph.add_edge("run_failed", END)
    return graph.compile()


def run_discover(
    discover_input: DiscoverInput,
    responder: nodes.StructuredResponder
    | Callable[[str, type[BaseModel], str, str], BaseModel]
    | None = None,
    *,
    assertion_checker: AssertionChecker | None = None,
) -> DiscoverCompleted:
    final_state = run_discover_state(
        discover_input,
        responder,
        assertion_checker=assertion_checker,
    )
    return final_state["final_output"]


def run_discover_state(
    discover_input: DiscoverInput,
    responder: nodes.StructuredResponder
    | Callable[[str, type[BaseModel], str, str], BaseModel]
    | None = None,
    *,
    assertion_checker: AssertionChecker | None = None,
    on_update: Callable[[str, DiscoverGraphState], None] | None = None,
) -> DiscoverGraphState:
    if responder is None:
        structured_responder: nodes.StructuredResponder = (
            nodes.CallableStructuredResponder(nodes.default_fake_responder)
        )
    elif callable(responder) and not hasattr(responder, "invoke_structured"):
        structured_responder = nodes.CallableStructuredResponder(responder)  # type: ignore[arg-type]
    else:
        structured_responder = responder  # type: ignore[assignment]
    graph = build_discover_graph(
        structured_responder, assertion_checker=assertion_checker
    )
    if on_update is None:
        final_state: DiscoverGraphState = graph.invoke(
            {"_input": discover_input}, config={"recursion_limit": 10_000}
        )
    else:
        final_state = {"_input": discover_input}
        for event in graph.stream(
            {"_input": discover_input},
            config={"recursion_limit": 10_000},
            stream_mode="updates",
        ):
            for node_name, update in event.items():
                final_state.update(update)
                on_update(node_name, update)
    if "failure" in final_state:
        failure = final_state["failure"]
        raise RuntimeError(
            f"Discover graph failed at {failure.node_name}: {failure.message}"
        )
    return final_state
