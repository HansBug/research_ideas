"""⭐ 硬要求：证明对照臂**没有**引入三条 contribution 的任何模块。

伞 PR #179 §4B.6 逐字：「⭐⭐ `tests/` 里那条隔离测试是硬要求，⛔ 不是锦上添花：它是「三条
contribution 一条都没给」这句话的**唯一机械证据**。⚠️ 靠约定隔离的实测遵守率是 **0/2**，
物理隔离是 **2/2**——⛔ 所以要的是一条会失败的测试，不是一句注释。」

⭐ **判据取的是最强形态**：⛔ 不是「不 import 谓词 / schema / 证据链模块」（那要枚举模块名，
漏一个就失效），而是「``paper_stm_feedback_loop`` 一个模块都不进来」。后者一行断言可判、
⛔ 无可漏项。代价是 transport 重试要自己写约 50 行，值得。

两层检查，缺一不可：

* **静态**（AST）：源码里根本没有那条 import。这是主判据——它不依赖运行时状态。
* **动态**（子进程）：干净进程里 import 全部 X1 模块后，``sys.modules`` 里没有它。
  ⚠️ 必须在子进程做：本测试会话里其它测试可能已经 import 过主臂，同进程检查会误报。
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
REPO_ROOT = Path(__file__).resolve().parents[4]

#: 禁止出现在 X1 实现里的顶层包。``paper_stm_feedback_loop`` 是主臂实现的全部；
#: ``pyfcstm`` 也禁，因为「pyfcstm 的 parse / inspect / sim 任何输出」按 §4B.1 归 C-①。
FORBIDDEN_ROOTS = frozenset({"paper_stm_feedback_loop", "pyfcstm"})

#: 允许的外部依赖。⭐ ``utils`` 是仓库根的公共设施（主臂也用它），不属任何 contribution。
ALLOWED_THIRD_PARTY_ROOTS = frozenset({"utils", "pydantic", "langchain_core"})


def _source_files() -> list[Path]:
    files = sorted(SRC.rglob("*.py"))
    assert files, f"no implementation files found under {SRC}"
    return files


def _imported_roots(path: Path) -> set[str]:
    """该文件 import 的全部顶层包名。"""

    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            # level > 0 是包内相对 import，不引入外部包。
            if node.level == 0 and node.module:
                roots.add(node.module.split(".")[0])
    return roots


@pytest.mark.parametrize("path", _source_files(), ids=lambda p: p.name)
def test_source_does_not_import_main_arm(path: Path) -> None:
    """静态判据：源码里没有主臂或 pyfcstm 的 import。"""

    offending = _imported_roots(path) & FORBIDDEN_ROOTS
    assert not offending, (
        f"{path.relative_to(SRC)} imports {sorted(offending)}; the baseline arm must not "
        "carry any C-①②③ capability. See prompt/README.md §2."
    )


def test_no_dynamic_import_of_main_arm() -> None:
    """静态 AST 抓不到 ``importlib`` / ``__import__`` 这类动态绕道，单独查一次文本。

    ⚠️ 这条不是理论洁癖：AST 检查只看 import 语句，一个 ``importlib.import_module`` 调用
    对它完全透明，而那正是「约定隔离」失效的典型路径。
    """

    for path in _source_files():
        text = path.read_text(encoding="utf-8")
        for needle in ("importlib", "__import__"):
            assert needle not in text, (
                f"{path.relative_to(SRC)} contains {needle!r}; dynamic imports would "
                "route around the static isolation check."
            )


def test_third_party_surface_is_declared() -> None:
    """X1 的外部依赖面必须是声明过的那几个。

    ⭐ 这条防的是**渐变**：今天引入一个看似无害的新依赖，明天它自己 import 主臂。把依赖面
    钉死，新增依赖时必须先改这个断言，那一步就是审查点。
    """

    stdlib = set(sys.stdlib_module_names)
    # 本目录内的兄弟模块用绝对 import（`import schema`），不建包——因为动态检查要能
    # `import runner` 而相对 import 在无父包时失败。它们当然不是第三方。
    local = {p.stem for p in _source_files()}
    for path in _source_files():
        external = _imported_roots(path) - stdlib - local
        undeclared = external - ALLOWED_THIRD_PARTY_ROOTS
        assert not undeclared, (
            f"{path.relative_to(SRC)} imports undeclared package(s) {sorted(undeclared)}; "
            "widen ALLOWED_THIRD_PARTY_ROOTS deliberately, after checking what they pull in."
        )


def test_clean_process_never_loads_main_arm() -> None:
    """动态判据：干净子进程里 import 全部 X1 模块后，主臂不在 ``sys.modules``。"""

    modules = [p.stem for p in _source_files() if p.stem != "__init__"]
    program = (
        "import sys\n"
        f"sys.path.insert(0, {str(SRC)!r})\n"
        f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
        + "".join(f"import {name}\n" for name in modules)
        + "leaked = sorted(m for m in sys.modules if m.split('.')[0] in "
        f"{sorted(FORBIDDEN_ROOTS)!r})\n"
        "print('LEAKED=' + ','.join(leaked))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", program],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, f"clean import failed:\n{result.stderr}"
    line = [ln for ln in result.stdout.splitlines() if ln.startswith("LEAKED=")]
    assert line, f"probe produced no verdict:\n{result.stdout}\n{result.stderr}"
    leaked = line[-1].removeprefix("LEAKED=")
    assert leaked == "", f"importing the baseline arm pulled in: {leaked}"
