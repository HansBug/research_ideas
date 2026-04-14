#!/usr/bin/env python3
"""与导师讨论：当前进展、现状与一些思考 PPT 生成器。"""

from pathlib import Path

from pptx import Presentation


WORKSPACE = Path(__file__).resolve().parent
OUTPUT = WORKSPACE / "deck.pptx"
TITLE = "与导师讨论：当前进展、现状与一些思考"
SUBTITLE = "2026-04-15 / 导师讨论 / 初始骨架"


def add_bullets(text_frame, bullets: list[str]) -> None:
    text_frame.clear()
    for index, bullet in enumerate(bullets):
        paragraph = text_frame.paragraphs[0] if index == 0 else text_frame.add_paragraph()
        paragraph.text = bullet
        paragraph.level = 0


def build_cover(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = TITLE
    slide.placeholders[1].text = SUBTITLE


def build_title_and_bullets(prs: Presentation, title: str, bullets: list[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    add_bullets(slide.placeholders[1].text_frame, bullets)


def build_progress_overview(prs: Presentation) -> None:
    build_title_and_bullets(
        prs,
        "当前整体进展",
        [
            "最近一段时间已经完成了哪些关键工作",
            "当前有哪些阶段性产物或可回溯材料",
            "哪些部分已经较稳定，哪些还在推进中",
        ],
    )


def build_current_status(prs: Presentation) -> None:
    build_title_and_bullets(
        prs,
        "当前情况与主要卡点",
        [
            "现在整体处于什么状态",
            "最影响推进效率的卡点是什么",
            "这些问题是认知问题、材料问题还是节奏问题",
        ],
    )


def build_my_thoughts(prs: Presentation) -> None:
    build_title_and_bullets(
        prs,
        "我的一些思考",
        [
            "我对当前研究主线的理解",
            "我认为下一阶段应优先推进的方向",
            "哪些内容可能需要收缩、延后或换一种做法",
        ],
    )


def build_feedback_needed(prs: Presentation) -> None:
    build_title_and_bullets(
        prs,
        "希望请导师重点反馈",
        [
            "近期最值得优先推进的部分是哪一块",
            "当前思考中哪些是值得继续展开的，哪些需要收住",
            "接下来一到两周最建议我交付什么",
        ],
    )


def build_presentation() -> Path:
    prs = Presentation()
    prs.core_properties.title = TITLE
    build_cover(prs)
    build_progress_overview(prs)
    build_current_status(prs)
    build_my_thoughts(prs)
    build_feedback_needed(prs)
    prs.save(str(OUTPUT))
    return OUTPUT


if __name__ == "__main__":
    print(build_presentation())
