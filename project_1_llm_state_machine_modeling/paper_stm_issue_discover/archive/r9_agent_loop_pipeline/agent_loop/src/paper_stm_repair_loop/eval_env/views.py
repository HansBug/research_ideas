from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from typing import Any, Callable


class UntrackedDependency(RuntimeError):
    """Raised when an eval expression reaches an unregistered field or method."""


def stable_json(value: Any) -> str:
    """Return deterministic JSON for provenance hashing of frozen observations."""

    return json.dumps(_jsonable(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_hash(value: Any) -> str:
    """Return a SHA-256 digest for a JSON-stable value."""

    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def _jsonable(value: Any) -> Any:
    if isinstance(value, FrozenView):
        return value.to_json()
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        try:
            return _jsonable(value.model_dump(mode="json"))
        except Exception:
            pass
    if hasattr(value, "to_json"):
        try:
            return _jsonable(value.to_json())
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        return {str(k): _jsonable(v) for k, v in vars(value).items() if not str(k).startswith("_")}
    return str(value)


class FrozenView:
    """Immutable registered observation/view exposed to direct assertion eval.

    Parameters: ``kind`` names the view type for audit records; ``data`` is a
    JSON-like snapshot copied at construction; ``allowed_fields`` and
    ``allowed_methods`` are the only attributes available through ``.field`` or
    ``.method(...)``.  ``methods`` maps registered method names to pure callables
    that receive this view as their first argument.

    Returns: attribute/item access yields recursively frozen values; method calls
    return their callable result, usually another ``FrozenView`` or bool.

    Execution: the view never reads files, environment, time, random state, or
    network; it serves only the already frozen ``data`` snapshot.  Mutation APIs
    are intentionally absent and ``__setattr__`` rejects writes after init.

    Failure semantics: unknown fields, dunder attributes, and unregistered
    methods raise ``UntrackedDependency`` so the runtime can produce an
    ``untracked_dependency`` result instead of treating the access as model
    evidence.

    Evidence limitations: the view is only as complete as the controller-bound
    snapshot used to construct it; it cannot prove global semantic coverage or
    source attribution.

    Permissions: read-only in-memory access to registered fields/methods only;
    no arbitrary paths, shell, import, environment, network, mutation, or hidden
    reference/gold data.

    Example: ``FrozenView("state", {"path": "Root.Idle"}, {"path"}, {})`` allows
    ``view.path`` and rejects ``view.__class__`` or ``view.secret``.
    """

    __slots__ = ("_kind", "_data", "_allowed_fields", "_allowed_methods", "_methods", "_frozen")

    def __init__(
        self,
        kind: str,
        data: Mapping[str, Any],
        *,
        allowed_fields: set[str] | frozenset[str],
        allowed_methods: set[str] | frozenset[str] | None = None,
        methods: Mapping[str, Callable[..., Any]] | None = None,
    ) -> None:
        object.__setattr__(self, "_kind", str(kind))
        object.__setattr__(self, "_data", copy.deepcopy(dict(data)))
        object.__setattr__(self, "_allowed_fields", frozenset(allowed_fields))
        object.__setattr__(self, "_allowed_methods", frozenset(allowed_methods or set()))
        object.__setattr__(self, "_methods", dict(methods or {}))
        object.__setattr__(self, "_frozen", True)

    @property
    def view_kind(self) -> str:
        return self._kind

    @property
    def allowed_fields(self) -> frozenset[str]:
        return self._allowed_fields

    @property
    def allowed_methods(self) -> frozenset[str]:
        return self._allowed_methods

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_frozen", False):
            raise TypeError("FrozenView is immutable")
        object.__setattr__(self, name, value)

    def __deepcopy__(self, _memo: dict[int, Any]) -> "FrozenView":
        return self

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str) or key.startswith("__"):
            raise UntrackedDependency(f"unregistered item access: {key!r}")
        if key not in self._allowed_fields:
            raise UntrackedDependency(f"unregistered field for {self._kind}: {key}")
        return self._wrap(self._data.get(key))

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__"):
            raise UntrackedDependency(f"dunder attribute rejected: {name}")
        if name in self._allowed_fields:
            return self._wrap(self._data.get(name))
        if name in self._allowed_methods and name in self._methods:
            def registered_method(*args: Any, **kwargs: Any) -> Any:
                return self._methods[name](self, *args, **kwargs)

            return registered_method
        raise UntrackedDependency(f"unregistered field/method for {self._kind}: {name}")

    def _wrap(self, value: Any) -> Any:
        if isinstance(value, FrozenView):
            return value
        if isinstance(value, Mapping):
            return FrozenView(
                f"{self._kind}.field",
                value,
                allowed_fields=set(str(k) for k in value.keys()),
            )
        if isinstance(value, list):
            return tuple(self._wrap(item) for item in value)
        return copy.deepcopy(value)

    def to_json(self) -> dict[str, Any]:
        return {
            "view_kind": self._kind,
            "data": _jsonable(self._data),
            "allowed_fields": sorted(self._allowed_fields),
            "allowed_methods": sorted(self._allowed_methods),
        }

    def __repr__(self) -> str:
        return f"FrozenView(kind={self._kind!r}, hash={stable_hash(self.to_json())[:12]})"


__all__ = ["FrozenView", "UntrackedDependency", "stable_hash", "stable_json"]
