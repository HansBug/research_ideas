"""结构谓词的 False 是发现，不是编码错误 —— 这条在 prompt 里曾经自相矛盾。

v22 的根因分析在同一份进入模型的材料里找到两条直接冲突的规则，相隔 126 行：

    predicates.py   containment(parent="Sys.Outer", child="Sys.Outer.Inner.Deep")  # False: not direct
    prompts.py      `containment` and `initial_target` are the exception ... Their False *is* the finding

评审员照前者执行，其反馈的形态是「child 是某容器的孙状态…因此该要求会把它判为不满足」——
「会返回 False」被直接当成「所以编码错了」。修订纪律「do not reintroduce a previously removed
semantic distortion」再把这次否定锁死，后续版本的 rationale 会明写沿用了上一轮的决定。

代价是可量化的：以「同一 pair 同一绑定 → 同一真值」建经验 oracle（641 个 key，跨格零例不一致），
比对多修订格的首版与终版，**35 条已知返回 False 的绑定被修订回路删除**，其中约 13 条是台账
primary 的形态 —— 即第一稿写对了、被改掉了。

⚠️ 这里不写具体是哪个 pair、哪条记录。灼烧检测在本文件的第一版就抓到了那次引用：论证只需要机制与
总量，样本标识对它没有贡献，而写进来会消耗 hold-out 资格。

机制上这条错误指引会把断言推向**重言式**：路径词表由模型层级生成，所以 `A.B.C` 的直接父按定义就是
`A.B`。全 66 格实测 `containment` 自前缀锚点 75 次调用、75 次 True，零例外；而 NL 层锚点 45 次、
45 次 False。按锚点两分全部 1519 次调用，模型锚点 False 率 2.3%、NL 锚点 46.2%。

这些断言本身不作断言 —— 本模块只钉住 prompt 材料里的**规则不再互相矛盾**，因为矛盾本身是可检测的，
而它造成的损失要跑一整代次才看得见。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import predicates, prompts  # noqa: E402

#: 结构族里 False 承载发现的三个谓词。行为族（`reaches` / `response_within`）不在此列 ——
#: 它们的 False 注释说的是「模型做不到」，本来就正确。
STRUCTURAL = ("containment", "initial_target", "cardinality")


def _spec(name: str):
    for predicate in predicates.PREDICATES:
        if predicate.name == name:
            return predicate
    raise AssertionError(f"{name} not in PREDICATES")


def _text(name: str) -> str:
    spec = _spec(name)
    parts = [spec.meaning or "", spec.proves or "", spec.caveat or ""]
    parts += [f"{k}: {v}" for k, v in (spec.field_specs or ())]
    parts += list(spec.examples or ())
    return "\n".join(str(p) for p in parts)


def test_no_structural_predicate_calls_its_own_false_a_mis_encoding() -> None:
    """`# False: not direct` 读起来就是「你绑错了」，而它恰恰是发现。"""
    for name in STRUCTURAL:
        text = _text(name)
        assert "False: not direct" not in text, name
        # 「非直接子状态 → False」这个事实可以说，但不能只说它而不说它是发现。
        if "False" in text:
            assert any(
                marker in text for marker in ("finding", "FINDING", "the model put it", "the model")
            ), f"{name} 提到 False 却没说它意味着模型做错了什么"


def test_structural_predicates_warn_against_re_anchoring() -> None:
    """把锚点挪到模型自己声明的那一层，断言就变成重言式（75/75 True）。"""
    for name in STRUCTURAL:
        text = _text(name)
        assert any(
            marker in text
            for marker in ("do not re-anchor", "Do not move", "do not move", "Do not re-anchor")
        ), f"{name} 没有警告不要把锚点下移"


def test_the_reviewer_is_told_the_inference_is_forbidden() -> None:
    """评审员是执行那条错误指引的地方，所以禁令必须在它的 prompt 里。"""
    text = prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "therefore it is" in text and "mis-encoded" in text, "缺少对该推理的显式禁令"
    for name in STRUCTURAL:
        assert name in text, f"禁令没有点名 {name}"
    # 禁令必须同时说清它不豁免什么，否则会被读成「结构断言一律不许驳回」。
    assert "wrong about what the sentence says" in text


def test_the_two_sources_no_longer_contradict() -> None:
    """splitter 侧的正面表述仍在，且与谓词目录同向。

    这条测的是**一致性**而非任一侧的措辞：矛盾是可检测的，而它造成的损失要跑一整代次才看得见。
    """
    assert "Their False *is* the finding" in prompts.REQUIREMENT_SPLITTER_PROMPT or \
           "their False *is* the finding" in prompts.REQUIREMENT_SPLITTER_PROMPT
    catalogue = "\n".join(_text(n) for n in STRUCTURAL)
    assert "mis-encoding" in catalogue or "finding" in catalogue
