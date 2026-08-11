"""Join hard-wrapped lines inside Markdown paragraphs.

Hard wrapping a paragraph at some column is a habit from plain-text mail; in Markdown it
does two bad things. CommonMark renders a soft line break as a space, so a break between
two CJK characters injects a space that should not be there ("比对。 60/60"). And the
source becomes hostile to edit: changing one word reflows nothing, so the wrap drifts.

Rules applied, in order of precedence:

  * fenced code (``` or ~~~), including ```mermaid, is copied byte for byte
  * indented code (4+ spaces after a blank line) is left alone
  * table rows, headings, thematic breaks, HTML block tags and link-reference
    definitions each stay on their own line
  * a list item starts a new logical line; its continuation lines fold into it
  * blockquote runs fold together, keeping one `> ` prefix
  * everything else folds until a blank line

Joining two lines inserts a space unless the characters on both sides of the break are
CJK, in which case they are joined directly -- that is the case where the rendered space
was an artifact rather than a separator.

Usage:
    unwrap_markdown.py <file>...            rewrite in place
    unwrap_markdown.py --check <file>...    exit 1 if any file would change
    unwrap_markdown.py --stdout <file>      write result to stdout
"""

from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
SETEXT = re.compile(r"^\s{0,3}(=+|-{2,})\s*$")
BREAK = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
TABLE = re.compile(r"^\s*\|")
LIST = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])\s+")
QUOTE = re.compile(r"^\s{0,3}>\s?")
HTML = re.compile(r"^\s{0,3}</?[A-Za-z][^>]*>")
LINKDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s")
INDENTED_CODE = re.compile(r"^(\s{4,}|\t)\S")


def _is_cjk(ch: str) -> bool:
    """CJK ideographs plus the fullwidth punctuation that behaves like them.

    `unicodedata.east_asian_width` returns 'W' for ideographs and 'F' for fullwidth
    forms; both are cases where a space at a line break is noise rather than a word
    separator.
    """
    return unicodedata.east_asian_width(ch) in {"W", "F"}


#: Fullwidth punctuation already carries its own trailing space visually, so a break
#: after one of these needs no separator even when Latin text follows -- `因此：\n154 条`
#: should fold to `因此：154 条`, not `因此： 154 条`.
_CLOSERS = "，。、；：！？…）〉》」』】〕｝’”"
#: The mirror case: an opening fullwidth bracket takes no space before it.
_OPENERS = "（〈《「『【〔｛‘“"

#: Punctuation Unicode calls Ambiguous-width but Chinese text uses fullwidth: the em dash
#: (as in `——`), the middle dot, the wave dash. `east_asian_width` returns 'A' for these,
#: so without listing them `理由——\n因为` folds to `理由—— 因为` with a stray space.
#: Only consulted when the character on the other side is itself CJK, which is what keeps
#: an English `word -- word` from losing its spaces.
_CJK_AMBIGUOUS = "—―…·～"


def _join(left: str, right: str) -> str:
    if not left or not right:
        return left + right
    a, b = left[-1], right[0]
    cjk_a = _is_cjk(a) or (a in _CJK_AMBIGUOUS and _is_cjk(b))
    cjk_b = _is_cjk(b) or (b in _CJK_AMBIGUOUS and _is_cjk(a))
    if a in _CLOSERS or b in _OPENERS:
        glue = ""
    elif cjk_a and cjk_b:
        glue = ""
    else:
        glue = " "
    return left + glue + right


def _standalone(line: str) -> bool:
    """Lines that must not absorb a following line, nor be absorbed.

    `INDENTED_CODE` is deliberately absent: per CommonMark an indented chunk cannot
    interrupt a paragraph, so a wrapped continuation that happens to be indented four
    spaces is still part of the paragraph. Treating it as code left it on its own line
    and defeated the whole point on any file wrapped with hanging indents. The genuine
    indented-code case is handled separately, where a preceding blank line proves it.
    """
    return bool(
        TABLE.match(line)
        or HEADING.match(line)
        or BREAK.match(line)
        or HTML.match(line)
        or LINKDEF.match(line)
    )


def unwrap(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    buf: str | None = None          # paragraph or list item being accumulated
    quote_buf: str | None = None    # blockquote run being accumulated
    fence: str | None = None
    prev_blank = True

    def flush() -> None:
        nonlocal buf, quote_buf
        if quote_buf is not None:
            out.append(quote_buf)
            quote_buf = None
        if buf is not None:
            out.append(buf)
            buf = None

    for raw in lines:
        line = raw.rstrip()

        if fence is not None:
            out.append(raw)
            if line.strip().startswith(fence):
                fence = None
            continue

        m = FENCE.match(line)
        if m:
            flush()
            fence = m.group(1)[0] * 3
            out.append(raw)
            prev_blank = False
            continue

        if not line.strip():
            flush()
            out.append("")
            prev_blank = True
            continue

        if QUOTE.match(line):
            body = QUOTE.sub("", line, count=1)
            if quote_buf is None:
                flush()
                if body.strip():
                    quote_buf = "> " + body
                else:
                    out.append(">")
            elif not body.strip():
                # A bare `>` is the blockquote's paragraph separator. Emitting it and
                # clearing the buffer keeps the two paragraphs apart; folding it in
                # would merge them into one.
                out.append(quote_buf)
                out.append(">")
                quote_buf = None
            else:
                # A table, heading **or list item** inside a quote still needs its own
                # line. Omitting LIST here folded `> - a` / `> - b` into one line and
                # destroyed the list -- the rendered output became a single paragraph
                # reading "- a - b". Blockquoted lists are common in these docs
                # (口径表、优先级说明), so this was not a corner case.
                if _standalone(body) or LIST.match(body):
                    out.append(quote_buf)
                    quote_buf = "> " + body
                else:
                    quote_buf = _join(quote_buf, body)
            prev_blank = False
            continue
        if quote_buf is not None:
            flush()

        # Setext underline belongs to the paragraph above it, so emit both verbatim.
        if buf is not None and SETEXT.match(line) and not LIST.match(line):
            out.append(buf)
            out.append(raw)
            buf = None
            prev_blank = False
            continue

        if INDENTED_CODE.match(line) and prev_blank:
            flush()
            out.append(raw)
            prev_blank = False
            continue

        if _standalone(line):
            flush()
            out.append(line)
            prev_blank = False
            continue

        if LIST.match(line):
            flush()
            buf = line
            prev_blank = False
            continue

        if buf is None:
            buf = line
        else:
            buf = _join(buf, line.strip())
        prev_blank = False

    flush()
    result = "\n".join(out)
    if text.endswith("\n") and not result.endswith("\n"):
        result += "\n"
    return result


def main(argv: list[str]) -> int:
    check = "--check" in argv
    to_stdout = "--stdout" in argv
    paths = [pathlib.Path(a) for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2

    changed: list[pathlib.Path] = []
    for path in paths:
        original = path.read_text()
        folded = unwrap(original)
        if to_stdout:
            sys.stdout.write(folded)
            continue
        if folded == original:
            continue
        changed.append(path)
        if not check:
            path.write_text(folded)

    if to_stdout:
        return 0
    verb = "需要处理" if check else "已处理"
    if changed:
        print(f"{verb} {len(changed)} 个文件:")
        for path in changed:
            print(f"  {path}")
    else:
        print("没有需要处理的文件")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
