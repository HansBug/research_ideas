from __future__ import annotations


def content_to_text(content: object) -> str:
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
    if not text:
        return "[not provided]"
    cleaned = text.strip()
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[:limit]}\n...[truncated {len(cleaned) - limit} chars]"


__all__ = ["artifact_excerpt", "content_to_text"]
