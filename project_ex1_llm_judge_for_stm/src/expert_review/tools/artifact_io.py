"""``artifact_io`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.tools` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations


def content_to_text(content: object) -> str:
    """``content_to_text`` 函数。

    :param content: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str):
                parts.append(text)
            else:
                parts.append(str(item))
        return "".join(parts)
    return "" if content is None else str(content)


def artifact_excerpt(text: str | None, limit: int = 4200) -> str:
    """``artifact_excerpt`` 函数。

    :param text: 见函数签名与上下文。
    :param limit: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not text:
        return "[not provided]"
    cleaned = text.strip()
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[:limit]}\n...[truncated {len(cleaned) - limit} chars]"


__all__ = ["artifact_excerpt", "content_to_text"]