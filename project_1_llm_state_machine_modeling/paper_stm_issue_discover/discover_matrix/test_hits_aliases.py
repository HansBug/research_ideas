"""`hits:A+B` 的解析必须在两个读取器里一致。

⚠️ 为什么这个函数值得单独测：它的失效模式是**静默的且方向误导**。若读取器写成
`label == f"hits:{alias}"`，则 `hits:A+B` 既不匹配 `A` 也不匹配 `B` —— 覆盖率**下降**，
而下降看起来像一个真实结果（「这一轮没命中」），不像 bug。判定口径的修正会被静默吃掉。

多别名形式本身是判据的修正：两位标注者**独立**报告了「一条 issue 同时陈述两条期望缺陷，
而一标签制度迫使二选一，另一条被记未命中」这一系统性低估。
"""

from __future__ import annotations

import importlib.util
import pathlib

import pytest

HERE = pathlib.Path(__file__).resolve().parents[1] / "discover_matrix"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


READERS = ["instrument_ablation", "onepass_merge"]


def exact_hits_comparisons(path: pathlib.Path) -> list[int]:
    """返回所有「把某个 label 直接与 `hits:...` 相等比较」的行号。

    用 AST 而不是 tokenize / grep，两条理由：

    1. **grep 会命中文档。** `hits_aliases` 的 docstring 里逐字写着这个反例，直接搜源文会让一条
       有效的闸永久失败。
    2. **tokenize 的 f-string 形态随版本变。** 3.12+ 拆成 `FSTRING_START/MIDDLE/END`，3.10 是**单个
       `STRING` token**。按 token 归一化的版本在 3.10 上把整个 f-string 替换成 `""`，于是闸**绿着
       却抓不到退回** —— 实测如此，是负对照发现的。

    AST 层面 `f"hits:{alias}"` 稳定是一个 `JoinedStr`，其首个 `Constant` 以 `hits:` 开头。
    """
    import ast

    bad: list[int] = []

    def is_hits_literal(node: ast.expr) -> bool:
        if isinstance(node, ast.JoinedStr):
            head = next((v for v in node.values if isinstance(v, ast.Constant)), None)
            return bool(head and isinstance(head.value, str) and head.value.startswith("hits:"))
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value.startswith("hits:")
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return is_hits_literal(node.left)
        return False

    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Compare) and any(isinstance(o, (ast.Eq, ast.NotEq)) for o in node.ops):
            if any(is_hits_literal(c) for c in node.comparators) or is_hits_literal(node.left):
                bad.append(node.lineno)
    return bad


@pytest.mark.parametrize("module", READERS)
@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("hits:PAIR-Z-REC-01", {"PAIR-Z-REC-01"}),
        ("hits:PAIR-Z-REC-01+PAIR-Z-REC-02", {"PAIR-Z-REC-01", "PAIR-Z-REC-02"}),
        ("hits:A+B+C", {"A", "B", "C"}),
        # 空白容错：标注者手写，`+` 两侧可能带空格
        ("hits: A + B ", {"A", "B"}),
        # 其余四个标签一律空集 —— `+` 例外只给 hits
        ("grounded-extra", set()),
        ("boundary", set()),
        ("fabricated", set()),
        ("duplicate-of:C999-I01", set()),
        (None, set()),
        ("", set()),
    ],
)
def test_hits_aliases(module: str, label: str | None, expected: set[str]) -> None:
    assert set(_load(module).hits_aliases(label)) == expected


@pytest.mark.parametrize("module", READERS)
def test_no_reader_still_compares_labels_exactly(module: str) -> None:
    """⛔ 回归闸：任何读取器都不得退回精确比较。

    这是本文件的实际防护点 —— 上面的单元测试只证明 `hits_aliases` 自己对，不证明读取器**用了**它。
    """
    lines = exact_hits_comparisons(HERE / f"{module}.py")
    assert not lines, (
        f"{module}.py:{lines} 退回了与 `hits:...` 的精确比较，`hits:A+B` 会既不匹配 A 也不匹配 B，"
        f"表现为覆盖率下降而非报错"
    )


def test_the_guard_actually_catches_a_regression() -> None:
    """⭐ 负对照：把读取器改回精确比较，闸必须报警。

    没有这一条，上一版的闸**绿着却抓不到退回** —— 它按 token 归一化，而 3.10 把 f-string 当单个
    `STRING` token，整段被替成 `""`。测试通过不等于测试有效。
    """
    import tempfile

    src = (HERE / "instrument_ablation.py").read_text()
    reverted = src.replace(
        'alias in hits_aliases(labels.get(i["issue_uid"], {}).get("label"))',
        'labels.get(i["issue_uid"], {}).get("label") == f"hits:{alias}"',
    )
    assert reverted != src, "负对照的替换没生效，说明被替换的表达式已改名，本测试需同步更新"
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "reverted.py"
        p.write_text(reverted)
        assert exact_hits_comparisons(p), "闸抓不到退回版 —— 闸本身失效"


def test_both_readers_agree() -> None:
    """两个读取器的解析必须逐字一致，否则同一批标注在两处得出不同覆盖率。"""
    fns = [_load(m).hits_aliases for m in READERS]
    for label in ("hits:A", "hits:A+B", "hits: A + B ", "boundary", None, ""):
        results = [set(f(label)) for f in fns]
        assert len(set(map(frozenset, results))) == 1, f"{label!r} 解析不一致: {results}"
