#!/usr/bin/env python3
"""2026-04-15 讨论 deck 生成器。"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


WORKSPACE = Path(__file__).resolve().parent
GUIDE = WORKSPACE / "PPT_GUIDE.md"
OUTPUT = WORKSPACE / "deck.pptx"
TITLE = "2026-04-15-讨论"

FONT_SERIF = "Noto Serif CJK SC"
FONT_SANS = "Noto Sans CJK SC"
FONT_MONO = "Noto Sans Mono CJK SC"

SLIDE_IDS = [
    "s01-cover",
    "s02-agenda",
    "s03-summary",
    "s04-why-project1-now",
    "s05-four-project-map",
    "s06-project1-evidence-chain",
    "s07-baselines-overview",
    "s08-baseline-evidence",
    "s09-sources-curation",
    "s10-sources-stats",
    "s11-sources-main-types",
    "s12-sources-time-structure",
    "s13-sources-examples",
    "s14-sm-family",
    "s15-control-state-definition",
    "s16-pyfcstm-progress",
    "s17-pyfcstm-role",
    "s18-pyudbm-progress",
    "s19-infra-feedback",
    "s20-decisions-next-steps",
]


def rgb(hex_value: str) -> RGBColor:
    hex_value = hex_value.replace("#", "")
    return RGBColor.from_string(hex_value)


COLORS = {
    "bg": rgb("#F5F1EA"),
    "panel": rgb("#FFFDFC"),
    "panel_alt": rgb("#F0EBE2"),
    "ink": rgb("#1F2430"),
    "muted": rgb("#68707E"),
    "navy": rgb("#203354"),
    "teal": rgb("#1D6F73"),
    "rust": rgb("#A04B39"),
    "gold": rgb("#C8912C"),
    "sage": rgb("#73876C"),
    "sand": rgb("#D8C4A3"),
    "line": rgb("#D7CFC3"),
    "white": rgb("#FFFFFF"),
    "green": rgb("#3F8F6B"),
    "amber": rgb("#D3A72A"),
    "orange": rgb("#C96B2C"),
    "blue_soft": rgb("#DDE9EE"),
    "teal_soft": rgb("#DCEDEA"),
    "rust_soft": rgb("#F2E4DE"),
    "gold_soft": rgb("#F6ECD8"),
    "sage_soft": rgb("#E3EBDD"),
}

SECTION_THEME = {
    "总体判断": COLORS["navy"],
    "project_1": COLORS["teal"],
    "文库证据": COLORS["teal"],
    "基础设施": COLORS["rust"],
    "待拍板事项": COLORS["gold"],
}


def set_paragraph_font(paragraph, *, name=FONT_SANS, size=12, bold=False, color=None, align=None):
    if align is not None:
        paragraph.alignment = align
    for run in paragraph.runs:
        run.font.name = name
        run.font.size = Pt(size)
        run.font.bold = bold
        if color is not None:
            run.font.color.rgb = color


def set_cell_text(cell, text, *, size=11, bold=False, color=None, align=PP_ALIGN.LEFT, fill=None, font=FONT_SANS):
    cell.text = text
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Pt(6)
    cell.margin_right = Pt(6)
    cell.margin_top = Pt(4)
    cell.margin_bottom = Pt(4)
    if fill is not None:
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
    paragraph = cell.text_frame.paragraphs[0]
    paragraph.alignment = align
    for run in paragraph.runs:
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color or COLORS["ink"]


def add_textbox(
    slide,
    x,
    y,
    w,
    h,
    text,
    *,
    font=FONT_SANS,
    size=12,
    bold=False,
    color=None,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = valign
    frame.clear()
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        paragraph = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.alignment = align
        for run in paragraph.runs:
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color or COLORS["ink"]
    return shape


def add_paragraph_box(
    slide,
    x,
    y,
    w,
    h,
    lines,
    *,
    font=FONT_SANS,
    size=12,
    color=None,
    bullet=False,
    bold_first=False,
    line_space_after=2,
):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.word_wrap = True
    frame.clear()
    for idx, line in enumerate(lines):
        paragraph = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        paragraph.text = f"• {line}" if bullet else line
        paragraph.space_after = Pt(line_space_after)
        for run in paragraph.runs:
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold_first and idx == 0
            run.font.color.rgb = color or COLORS["ink"]
    return shape


def add_panel(slide, x, y, w, h, *, fill, line=None, radius=True):
    kind = SHAPE.ROUNDED_RECTANGLE if radius else SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    shape.line.width = Pt(1)
    return shape


def add_chip(slide, x, y, w, h, text, *, fill, color=None):
    add_panel(slide, x, y, w, h, fill=fill, line=fill, radius=True)
    add_textbox(
        slide,
        x,
        y + 0.03,
        w,
        h - 0.02,
        text,
        size=11,
        bold=True,
        color=color or COLORS["ink"],
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )


def add_card(slide, x, y, w, h, title, body_lines, *, accent, fill=None, title_size=16, body_size=11, badge=None):
    fill = fill or COLORS["panel"]
    add_panel(slide, x, y, w, h, fill=fill, line=COLORS["line"], radius=True)
    if h < 1.05:
        strip_h = min(0.1, h * 0.16)
        add_panel(slide, x, y, w, strip_h, fill=accent, line=accent, radius=True)
        if badge:
            add_chip(slide, x + 0.16, y + strip_h + 0.06, 0.46, 0.24, badge, fill=accent, color=COLORS["white"])
            title_x = x + 0.72
            title_w = w - 0.9
        else:
            title_x = x + 0.16
            title_w = w - 0.32
        add_textbox(slide, title_x, y + strip_h + 0.04, title_w, 0.22, title, font=FONT_SERIF, size=max(12, title_size - 1), bold=True, color=COLORS["navy"])
        add_paragraph_box(slide, x + 0.16, y + strip_h + 0.28, w - 0.32, max(0.22, h - strip_h - 0.32), body_lines, size=max(9.4, body_size - 0.2), color=COLORS["ink"], bullet=False)
        return
    add_panel(slide, x, y, w, 0.12, fill=accent, line=accent, radius=True)
    if badge:
        add_chip(slide, x + 0.18, y + 0.18, 0.55, 0.33, badge, fill=accent, color=COLORS["white"])
        title_x = x + 0.82
        title_w = w - 1.0
    else:
        title_x = x + 0.18
        title_w = w - 0.36
    add_textbox(slide, title_x, y + 0.18, title_w, 0.38, title, font=FONT_SERIF, size=title_size, bold=True, color=COLORS["navy"])
    add_paragraph_box(slide, x + 0.18, y + 0.63, w - 0.36, h - 0.8, body_lines, size=body_size, color=COLORS["ink"], bullet=False)


def add_context_bar(slide, x, y, w, h, cause, effect, *, accent):
    add_panel(slide, x, y, w, h, fill=COLORS["panel"], line=COLORS["line"], radius=True)
    add_chip(slide, x + 0.16, y + 0.07, 0.7, h - 0.14, "前因", fill=accent, color=COLORS["white"])
    add_textbox(slide, x + 0.96, y + 0.1, w * 0.42, h - 0.18, cause, size=10.2, color=COLORS["ink"])
    add_chip(slide, x + w * 0.54, y + 0.07, 0.7, h - 0.14, "因此", fill=COLORS["gold"], color=COLORS["ink"])
    add_textbox(slide, x + w * 0.54 + 0.82, y + 0.1, w * 0.34, h - 0.18, effect, size=10.2, color=COLORS["ink"])


def add_big_number_card(slide, x, y, w, h, value, label, detail, *, accent):
    add_panel(slide, x, y, w, h, fill=COLORS["panel"], line=COLORS["line"], radius=True)
    add_panel(slide, x, y, 0.14, h, fill=accent, line=accent, radius=True)
    add_textbox(slide, x + 0.28, y + 0.18, w - 0.45, 0.44, value, font=FONT_SERIF, size=25, bold=True, color=accent)
    add_textbox(slide, x + 0.28, y + 0.7, w - 0.45, 0.26, label, size=11, bold=True, color=COLORS["ink"])
    add_textbox(slide, x + 0.28, y + 0.98, w - 0.45, h - 1.12, detail, size=10, color=COLORS["muted"])


def add_section_background(slide, *, section, accent):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = COLORS["bg"]
    add_panel(slide, 0.0, 0.0, 13.333, 0.12, fill=accent, line=accent, radius=False)
    shape = slide.shapes.add_shape(SHAPE.OVAL, Inches(11.4), Inches(-0.9), Inches(3.0), Inches(3.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLORS["gold_soft"]
    shape.line.color.rgb = COLORS["gold_soft"]
    shape.fill.transparency = 0.22
    shape2 = slide.shapes.add_shape(SHAPE.OVAL, Inches(-0.85), Inches(5.4), Inches(2.8), Inches(2.8))
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = COLORS["blue_soft"]
    shape2.line.color.rgb = COLORS["blue_soft"]
    shape2.fill.transparency = 0.12
    add_chip(slide, 11.48, 0.22, 1.35, 0.34, section, fill=accent, color=COLORS["white"])


def add_title_block(slide, title, subtitle, *, section):
    accent = SECTION_THEME[section]
    add_section_background(slide, section=section, accent=accent)
    add_textbox(slide, 0.62, 0.33, 10.8, 0.46, title, font=FONT_SERIF, size=23, bold=True, color=COLORS["navy"])
    add_textbox(slide, 0.64, 0.86, 10.7, 0.28, subtitle, size=11, color=COLORS["muted"])


def add_footer(slide, page_num, refs):
    add_panel(slide, 0.62, 6.9, 12.08, 0.01, fill=COLORS["line"], line=COLORS["line"], radius=False)
    add_textbox(slide, 0.64, 6.94, 8.8, 0.18, f"依据 {refs}", size=8.5, color=COLORS["muted"])
    add_textbox(slide, 11.95, 6.9, 0.75, 0.2, f"{page_num:02d}/20", font=FONT_MONO, size=8.5, color=COLORS["muted"], align=PP_ALIGN.RIGHT)


def add_table(slide, x, y, w, h, headers, rows, *, header_fill, col_widths=None, font_size=10.5):
    table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(x), Inches(y), Inches(w), Inches(h))
    table = table_shape.table
    if col_widths:
        for idx, width in enumerate(col_widths):
            table.columns[idx].width = Inches(width)
    for idx, header in enumerate(headers):
        set_cell_text(
            table.cell(0, idx),
            header,
            size=font_size,
            bold=True,
            color=COLORS["white"],
            align=PP_ALIGN.CENTER,
            fill=header_fill,
        )
    for row_idx, row in enumerate(rows, start=1):
        fill = COLORS["panel"] if row_idx % 2 else COLORS["panel_alt"]
        for col_idx, value in enumerate(row):
            set_cell_text(
                table.cell(row_idx, col_idx),
                value,
                size=font_size,
                color=COLORS["ink"],
                align=PP_ALIGN.LEFT if col_idx != len(headers) - 1 else PP_ALIGN.CENTER,
                fill=fill,
            )
    return table


def add_chart(
    slide,
    x,
    y,
    w,
    h,
    categories,
    values,
    *,
    chart_type,
    accent,
    second_colors=None,
    max_scale=None,
):
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series("数量", values)
    chart = slide.shapes.add_chart(
        chart_type,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h),
        chart_data,
    ).chart
    chart.has_legend = False
    chart.value_axis.has_major_gridlines = True
    chart.value_axis.major_gridlines.format.line.color.rgb = COLORS["line"]
    chart.value_axis.tick_labels.font.size = Pt(9)
    chart.value_axis.tick_labels.font.name = FONT_SANS
    chart.value_axis.minimum_scale = 0
    chart.category_axis.tick_labels.font.size = Pt(9)
    chart.category_axis.tick_labels.font.name = FONT_SANS
    if max_scale is not None:
        chart.value_axis.maximum_scale = max_scale
    plot = chart.plots[0]
    plot.gap_width = 60
    series = chart.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = accent
    series.format.line.color.rgb = accent
    if second_colors:
        for idx, color in enumerate(second_colors):
            point = series.points[idx]
            point.format.fill.solid()
            point.format.fill.fore_color.rgb = color
            point.format.line.color.rgb = color
    return chart


def add_horizontal_segments(slide, x, y, w, h, segments, *, label_y_offset=0.18):
    total = sum(value for _, value, _, _ in segments)
    current_x = x
    for label, value, fill, text_color in segments:
        seg_w = w * value / total
        add_panel(slide, current_x, y, seg_w, h, fill=fill, line=fill, radius=False)
        add_textbox(
            slide,
            current_x,
            y + label_y_offset,
            seg_w,
            h - 0.1,
            f"{label}\n{value}",
            size=12,
            bold=True,
            color=text_color,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        current_x += seg_w


def add_arrow(slide, x, y, w, h, *, fill, direction="right"):
    shape_type = {
        "right": SHAPE.CHEVRON,
        "left": SHAPE.LEFT_ARROW,
        "up": SHAPE.UP_ARROW,
        "down": SHAPE.DOWN_ARROW,
    }[direction]
    shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = fill
    return shape


def parse_notes_from_guide(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8").splitlines()
    notes_map: dict[str, list[str]] = {}
    current_slide = None
    current_field = None
    speaker_lines: list[str] = []
    supplement_lines: list[str] = []

    def flush():
        nonlocal speaker_lines, supplement_lines, current_slide
        if current_slide:
            chunks = []
            if speaker_lines:
                chunks.append("\n\n".join(speaker_lines))
            filtered = [item for item in supplement_lines if item and item.lower() != "none"]
            if filtered:
                chunks.append("补充：\n" + "\n".join(filtered))
            notes_map[current_slide] = ["\n\n".join(chunks).strip()]
        speaker_lines = []
        supplement_lines = []

    for line in text:
        heading = re.match(r"^###\s+(s\d{2}-[a-z0-9-]+)\s*$", line)
        if heading:
            flush()
            current_slide = heading.group(1)
            current_field = None
            continue
        if current_slide is None:
            continue
        if line.startswith("- Speaker Notes:"):
            current_field = "speaker"
            continue
        if line.startswith("- Notes Supplement:"):
            current_field = "supplement"
            continue
        if line.startswith("- ") and not line.startswith("  - "):
            current_field = None
            continue
        item = re.match(r"^  - (.+)$", line)
        if item and current_field == "speaker":
            speaker_lines.append(item.group(1).strip())
        elif item and current_field == "supplement":
            supplement_lines.append(item.group(1).strip())
    flush()

    notes = []
    for slide_id in SLIDE_IDS:
        if slide_id not in notes_map:
            raise ValueError(f"Missing notes for {slide_id} in {path}")
        notes.append(notes_map[slide_id][0])
    return notes


def apply_notes(output: Path, notes: list[str]) -> None:
    prs = Presentation(output)
    for slide, note in zip(prs.slides, notes, strict=True):
        slide.notes_slide.notes_text_frame.text = note
    prs.save(output)


def validate_notes(output: Path, expected_notes: list[str]) -> None:
    prs = Presentation(output)
    if len(prs.slides) != len(expected_notes):
        raise ValueError("Slide count and note count mismatch")
    for idx, (slide, expected) in enumerate(zip(prs.slides, expected_notes, strict=True), start=1):
        actual = slide.notes_slide.notes_text_frame.text.strip()
        if actual != expected.strip():
            raise ValueError(f"Notes mismatch on slide {idx}")
    with zipfile.ZipFile(output) as zf:
        notes_parts = [name for name in zf.namelist() if name.startswith("ppt/notesSlides/notesSlide")]
    if len(notes_parts) != len(expected_notes):
        raise ValueError("notesSlides part count mismatch")


def validate_slide_count(output: Path, expected: int) -> None:
    prs = Presentation(output)
    if len(prs.slides) != expected:
        raise ValueError(f"Expected {expected} slides, got {len(prs.slides)}")


def build_cover(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = COLORS["bg"]
    add_panel(slide, 0.0, 0.0, 13.333, 0.12, fill=COLORS["navy"], line=COLORS["navy"], radius=False)
    add_panel(slide, 8.55, 0.9, 3.8, 5.2, fill=COLORS["panel"], line=COLORS["line"], radius=True)
    add_panel(slide, 8.55, 0.9, 0.16, 5.2, fill=COLORS["gold"], line=COLORS["gold"], radius=True)
    add_textbox(slide, 0.75, 1.1, 6.8, 0.62, "2026-04-15-讨论", font=FONT_SERIF, size=28, bold=True, color=COLORS["navy"])
    add_textbox(slide, 0.78, 1.85, 6.5, 0.65, "当前进展、问题收束\n与下一步投稿判断", font=FONT_SERIF, size=22, bold=True, color=COLORS["ink"])
    add_textbox(slide, 0.8, 2.85, 5.8, 0.45, "这次汇报只做三件事：给出现状判断、解释为什么先收束 project_1、以及明确需要拍板的问题。", size=12, color=COLORS["muted"])
    add_chip(slide, 0.8, 4.0, 1.75, 0.38, "project_1 优先级", fill=COLORS["teal"], color=COLORS["white"])
    add_chip(slide, 2.7, 4.0, 1.6, 0.38, "pyfcstm vs pyudbm", fill=COLORS["rust"], color=COLORS["white"])
    add_chip(slide, 4.45, 4.0, 1.75, 0.38, "control-state 定义", fill=COLORS["gold"], color=COLORS["ink"])
    add_textbox(slide, 0.8, 5.2, 2.5, 0.28, "博士研究进展对齐", size=10.5, bold=True, color=COLORS["navy"])
    projects = [
        ("project_1", "建模主线 / 当前优先级最高", COLORS["teal"]),
        ("project_2", "性质与场景生成 / 接口层", COLORS["gold"]),
        ("project_3", "verification backend / 地基已起", COLORS["rust"]),
        ("project_4", "iterative repair / 依赖前置成熟", COLORS["sage"]),
    ]
    y = 1.15
    for name, desc, accent in projects:
        add_card(slide, 8.85, y, 3.1, 0.95, name, [desc], accent=accent, fill=COLORS["panel"], title_size=15, body_size=10.5)
        y += 1.1
    add_textbox(slide, 8.9, 5.62, 2.9, 0.25, "日期 2026-04-15", size=10.5, color=COLORS["muted"], align=PP_ALIGN.RIGHT)
    add_footer(slide, 1, "[1][2][7]")


def build_agenda(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "明天这次讨论，我最希望先对齐三个决策", "先拍板问题边界，再决定论文如何写和接下来 6 周怎么推", section="总体判断")
    cards = [
        ("01", "本学期主投稿是否明确锁定 `project_1`", "先做 focused paper，而不是一次性拉四个 project。", COLORS["navy"]),
        ("02", "论文对象是否先限定为离散 `control-state layer`", "把模式、阶段、互锁、恢复、局部定时这一层先讲透。", COLORS["teal"]),
        ("03", "`pyfcstm` 与 `pyudbm` 是否分担建模基座与验证地基", "一个回答目标对象，一个沉淀 timed backend。", COLORS["rust"]),
    ]
    x_positions = [0.72, 4.48, 8.24]
    for x, (badge, title, detail, accent) in zip(x_positions, cards, strict=True):
        add_card(slide, x, 1.55, 3.48, 2.0, title, [detail], accent=accent, badge=badge, title_size=15, body_size=11)
    add_textbox(slide, 0.78, 4.05, 3.2, 0.26, "后续展开顺序", size=11, bold=True, color=COLORS["navy"])
    flow = [
        ("结论先给", COLORS["navy"]),
        ("project_1 文库证据", COLORS["teal"]),
        ("基础设施与仓库进展", COLORS["rust"]),
        ("拍板事项与倒排计划", COLORS["gold"]),
    ]
    x = 0.78
    for idx, (label, fill) in enumerate(flow):
        add_panel(slide, x, 4.45, 2.85, 0.72, fill=COLORS["panel"], line=COLORS["line"], radius=True)
        add_panel(slide, x, 4.45, 0.12, 0.72, fill=fill, line=fill, radius=True)
        add_textbox(slide, x + 0.22, 4.67, 2.35, 0.2, f"{idx + 1}. {label}", size=12.5, bold=True, color=COLORS["ink"])
        if idx < len(flow) - 1:
            add_arrow(slide, x + 2.96, 4.63, 0.4, 0.34, fill=COLORS["sand"])
        x += 3.02
    add_card(
        slide,
        0.8,
        5.55,
        11.75,
        0.9,
        "一句话主线",
        ["不是再去找更多材料，而是让现有材料收敛成一篇问题边界清楚、对象清楚、基础设施落点清楚的会议论文。"],
        accent=COLORS["navy"],
        fill=COLORS["gold_soft"],
        title_size=15,
        body_size=11.5,
    )
    add_footer(slide, 2, "[1][2][7][15]")


def build_summary(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "当前最缺的不是材料，而是把问题对象收束清楚", "一页结论先给出来，后面逐页用文库与仓库证据补强", section="总体判断")
    cards = [
        ("1", "先发 `project_1`", "本学期第一优先级应先把 focused paper 发出去。", COLORS["navy"]),
        ("2", "真正缺的是收束", "`project_1` 当前不缺样本，缺的是问题定义。", COLORS["teal"]),
        ("3", "先做离散 control-state", "目标对象先落到模式、阶段、互锁、恢复、局部 timer。", COLORS["gold"]),
        ("4", "`pyfcstm` 是研究答案", "它应被写成 executable control-state infrastructure。", COLORS["rust"]),
        ("5", "`project_3` 有地基但未成型", "`pyudbm` 已推进很深，但 verifyta 核心搜索仍缺。", COLORS["sage"]),
        ("6", "反馈基础设施最关键", "LLM-based modeling 的杀手锏是持续反馈，而不只是 prompt。", COLORS["navy"]),
    ]
    positions = [
        (0.74, 1.45),
        (4.42, 1.45),
        (8.1, 1.45),
        (0.74, 3.56),
        (4.42, 3.56),
        (8.1, 3.56),
    ]
    for (x, y), (badge, title, detail, accent) in zip(positions, cards, strict=True):
        add_card(slide, x, y, 3.15, 1.72, title, [detail], accent=accent, fill=COLORS["panel"], badge=badge, title_size=15, body_size=10.5)
    add_card(
        slide,
        0.82,
        5.65,
        11.68,
        0.9,
        "Take-home",
        ["先收束对象，再拉厚实验；只要定义稳住，现有文库和仓库推进已经足以支撑一篇 conference-style 论文。"],
        accent=COLORS["navy"],
        fill=COLORS["teal_soft"],
        title_size=15,
        body_size=11.5,
    )
    add_footer(slide, 3, "[1][2][4][5][7][9][12][17]")


def build_why_project1_now(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "站在本学期投稿窗口看，只有 project_1 适合先冲出去", "近端会议时间窗口 + 当前准备度 两条线必须同时看", section="总体判断")
    add_textbox(slide, 0.78, 1.35, 3.2, 0.2, "prior-year deadline 参考", size=10.5, bold=True, color=COLORS["navy"])
    add_panel(slide, 0.8, 1.62, 11.75, 1.3, fill=COLORS["panel"], line=COLORS["line"], radius=True)
    add_panel(slide, 1.15, 2.23, 10.9, 0.04, fill=COLORS["line"], line=COLORS["line"], radius=False)
    month_x = [1.1, 3.8, 6.45, 9.1, 11.55]
    month_labels = ["2026-03", "2026-04", "2026-05", "2026-06", ""]
    for x, label in zip(month_x[:-1], month_labels[:-1], strict=True):
        add_textbox(slide, x, 1.88, 0.9, 0.18, label, font=FONT_MONO, size=9.5, color=COLORS["muted"], align=PP_ALIGN.CENTER)
    venue_bands = [
        (1.35, 1.86, 1.0, 0.24, "RE 2025\n03-10", COLORS["rust_soft"], COLORS["rust"]),
        (2.55, 1.86, 1.1, 0.24, "MoDELS 2025\n04-03", COLORS["teal_soft"], COLORS["teal"]),
        (6.1, 1.86, 1.0, 0.24, "FM 参考\n4 月下旬", COLORS["gold_soft"], COLORS["gold"]),
        (7.65, 1.86, 1.3, 0.24, "ASE 2025\n05-30", COLORS["blue_soft"], COLORS["navy"]),
        (9.45, 1.86, 1.9, 0.24, "SoSyM / STVR\nrolling", COLORS["sage_soft"], COLORS["sage"]),
    ]
    for x, y, w, h, label, fill, accent in venue_bands:
        add_panel(slide, x, y, w, h, fill=fill, line=accent, radius=True)
        add_textbox(slide, x, y + 0.01, w, h - 0.01, label, size=8.8, bold=True, color=COLORS["ink"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_panel(slide, 4.78, 1.6, 0.03, 0.98, fill=COLORS["navy"], line=COLORS["navy"], radius=False)
    add_textbox(slide, 4.2, 1.55, 1.2, 0.18, "当前点\n2026-04-14", font=FONT_MONO, size=8.5, color=COLORS["navy"], align=PP_ALIGN.CENTER)
    add_textbox(slide, 0.78, 3.15, 3.2, 0.2, "当前准备度", size=10.5, bold=True, color=COLORS["navy"])
    readiness = [
        ("project_1", 0.92, COLORS["teal"], "问题、文库、baseline、pyfcstm 都已具备"),
        ("project_2", 0.56, COLORS["gold"], "接口层有意义，但当前不适合单独先发"),
        ("project_3", 0.44, COLORS["rust"], "backend 地基较深，验证原型尚未成型"),
        ("project_4", 0.24, COLORS["sage"], "依赖前几项更成熟后再起飞"),
    ]
    y = 3.5
    for label, ratio, accent, note in readiness:
        add_textbox(slide, 0.9, y, 1.35, 0.22, label, font=FONT_MONO, size=11, bold=True, color=COLORS["ink"])
        add_panel(slide, 2.2, y + 0.02, 4.4, 0.18, fill=COLORS["panel_alt"], line=COLORS["panel_alt"], radius=True)
        add_panel(slide, 2.2, y + 0.02, 4.4 * ratio, 0.18, fill=accent, line=accent, radius=True)
        add_textbox(slide, 6.8, y - 0.03, 5.0, 0.25, note, size=9.8, color=COLORS["muted"])
        y += 0.56
    add_card(
        slide,
        7.15,
        3.35,
        5.45,
        2.15,
        "页面结论",
        [
            "RE / MoDELS 风格窗口基本已过。",
            "ASE-style automation + infrastructure 写法仍是近端最现实目标。",
            "所以这学期不宜再把主问题做散。",
        ],
        accent=COLORS["navy"],
        fill=COLORS["panel"],
        title_size=16,
        body_size=11,
    )
    add_footer(slide, 4, "[1][15]")


def build_four_project_map(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "四个 project 是一条闭环，但近端主线必须先落在 project_1", "先把建模对象和目标形式主义立住，后面的 scenario、verification、repair 才有共同基座", section="总体判断")
    labels = [
        ("需求 / 描述", COLORS["panel_alt"]),
        ("建模", COLORS["teal_soft"]),
        ("性质 / 场景", COLORS["gold_soft"]),
        ("验证", COLORS["rust_soft"]),
        ("修复", COLORS["sage_soft"]),
    ]
    x = 0.85
    for idx, (label, fill) in enumerate(labels):
        add_panel(slide, x, 2.05, 2.0, 0.9, fill=fill, line=COLORS["line"], radius=True)
        add_textbox(slide, x, 2.32, 2.0, 0.2, label, size=14, bold=True, color=COLORS["ink"], align=PP_ALIGN.CENTER)
        if idx < len(labels) - 1:
            add_arrow(slide, x + 2.08, 2.31, 0.42, 0.34, fill=COLORS["sand"])
        x += 2.48
    cards = [
        (1.08, 3.55, 2.55, 1.6, "project_1", ["目标对象", "baseline", "样本与 `pyfcstm`"], COLORS["teal"]),
        (3.86, 3.55, 2.55, 1.6, "project_2", ["性质与场景", "生成接口层"], COLORS["gold"]),
        (6.64, 3.55, 2.55, 1.6, "project_3", ["profile-based verification", "timed backend"], COLORS["rust"]),
        (9.42, 3.55, 2.55, 1.6, "project_4", ["缺陷驱动", "iterative repair"], COLORS["sage"]),
    ]
    for x, y, w, h, title, lines, accent in cards:
        add_card(slide, x, y, w, h, title, lines, accent=accent, fill=COLORS["panel"], title_size=16, body_size=11)
    add_card(
        slide,
        0.85,
        5.55,
        11.8,
        0.88,
        "当前判断",
        ["博士主线仍然是生成-验证-修复闭环；只是本学期要先把建模对象与目标形式主义打稳，后续几项才有共同基座。"],
        accent=COLORS["navy"],
        fill=COLORS["gold_soft"],
        title_size=15,
        body_size=11.2,
    )
    add_footer(slide, 5, "[1][2]")


def build_project1_evidence_chain(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "project_1 的说服力来自三条文库线加上一条基础设施线", "不是平行摆设，而是共同回答“该建什么、凭什么、如何落地”", section="project_1")
    add_card(slide, 0.92, 1.75, 2.55, 1.45, "`baselines/`", ["62 篇比较集", "回答“该和谁比”"], accent=COLORS["navy"], fill=COLORS["panel"], title_size=16, body_size=11)
    add_card(slide, 9.85, 1.75, 2.55, 1.45, "`sources/`", ["787 篇 / 746 条正例", "回答“数据从哪里来”"], accent=COLORS["teal"], fill=COLORS["panel"], title_size=16, body_size=11)
    add_card(slide, 0.92, 4.0, 2.55, 1.45, "`state_machine_types/`", ["669 + 10 条目", "回答“到底选哪类状态机”"], accent=COLORS["gold"], fill=COLORS["panel"], title_size=15, body_size=11)
    add_card(slide, 9.85, 4.0, 2.55, 1.45, "`pyfcstm`", ["executable IR", "回答“如何落地并形成闭环”"], accent=COLORS["rust"], fill=COLORS["panel"], title_size=16, body_size=11)
    add_panel(slide, 4.15, 2.55, 5.05, 2.15, fill=COLORS["navy"], line=COLORS["navy"], radius=True)
    add_textbox(slide, 4.55, 2.88, 4.2, 0.32, "中央结论", size=12, bold=True, color=COLORS["sand"], align=PP_ALIGN.CENTER)
    add_textbox(slide, 4.45, 3.25, 4.45, 0.78, "三条文库线共同把论文对象\n压向 control-state problem", font=FONT_SERIF, size=19, bold=True, color=COLORS["white"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_textbox(slide, 4.45, 4.05, 4.45, 0.34, "而 `pyfcstm` 则把这个对象变成可执行、可反馈、可持续迭代的模型空间。", size=10.5, color=COLORS["white"], align=PP_ALIGN.CENTER)
    add_arrow(slide, 3.55, 2.7, 0.45, 0.32, fill=COLORS["sand"], direction="right")
    add_arrow(slide, 8.76, 2.7, 0.45, 0.32, fill=COLORS["sand"], direction="left")
    add_arrow(slide, 3.55, 4.55, 0.45, 0.32, fill=COLORS["sand"], direction="right")
    add_arrow(slide, 8.76, 4.55, 0.45, 0.32, fill=COLORS["sand"], direction="left")
    add_footer(slide, 6, "[2][3][4][5][7]")


def build_baselines_overview(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "`baselines/` 解决的是“该和谁比，以及差距究竟在哪里”", "这不是领域均匀采样，而是围绕 project_1 可比性刻意筛出的比较集", section="文库证据")
    add_textbox(slide, 0.82, 1.52, 2.0, 0.22, "状态分布", size=11, bold=True, color=COLORS["navy"])
    add_big_number_card(slide, 0.85, 1.86, 2.45, 1.2, "62", "baseline 条目", "直接比较对象已经够用", accent=COLORS["navy"])
    add_panel(slide, 0.85, 3.35, 5.3, 0.85, fill=COLORS["panel"], line=COLORS["line"], radius=True)
    add_horizontal_segments(
        slide,
        1.02,
        3.63,
        4.95,
        0.26,
        [
            ("🟢", 14, COLORS["green"], COLORS["white"]),
            ("🟡", 19, COLORS["amber"], COLORS["ink"]),
            ("🟠", 29, COLORS["orange"], COLORS["white"]),
        ],
    )
    add_textbox(slide, 1.05, 4.08, 5.0, 0.18, "绿色条目不多，但它们正是明天汇报该重点讲的几篇。", size=10.5, color=COLORS["muted"])
    role_cards = [
        ("direct baseline", "正面回答“自由文本 -> 状态机”", COLORS["navy"]),
        ("邻近任务", "需求 -> 行为模型 / model checking 修复", COLORS["teal"]),
        ("方法启发", "workflow、反馈闭环、工具链集成", COLORS["rust"]),
    ]
    y = 1.78
    for title, detail, accent in role_cards:
        add_card(slide, 6.45, y, 5.75, 1.15, title, [detail], accent=accent, fill=COLORS["panel"], title_size=15, body_size=11)
        y += 1.37
    add_card(
        slide,
        6.45,
        5.95,
        5.75,
        0.55,
        "页面结论",
        ["baseline 文库已经够厚，关键是挑最硬的绿色条目来支撑主张。"],
        accent=COLORS["navy"],
        fill=COLORS["gold_soft"],
        title_size=14,
        body_size=10.5,
    )
    add_footer(slide, 7, "[3]")


def build_baseline_evidence(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "baseline 的共同趋势不是更花的 prompt，而是更强的工具反馈", "几篇最值得讲的绿色条目给出的实证指向相当一致", section="文库证据")
    add_textbox(slide, 0.82, 1.38, 3.0, 0.2, "2026 direct baseline F1", size=10.5, bold=True, color=COLORS["navy"])
    add_chart(
        slide,
        0.82,
        1.62,
        3.75,
        2.45,
        ["Claude\n单提示", "GPT-4o\n单提示", "GPT-4o\nHybrid"],
        [0.7029, 0.5431, 0.6559],
        chart_type=XL_CHART_TYPE.COLUMN_CLUSTERED,
        accent=COLORS["navy"],
        second_colors=[COLORS["navy"], COLORS["sand"], COLORS["teal"]],
        max_scale=0.85,
    )
    add_textbox(slide, 4.75, 1.38, 3.0, 0.2, "SysML empirical study 修复率 (%)", size=10.5, bold=True, color=COLORS["navy"])
    add_chart(
        slide,
        4.75,
        1.62,
        3.75,
        2.45,
        ["格式", "语法", "语义", "需求一致"],
        [94.6, 88.0, 43.1, 37.3],
        chart_type=XL_CHART_TYPE.COLUMN_CLUSTERED,
        accent=COLORS["teal"],
        second_colors=[COLORS["teal"], COLORS["gold"], COLORS["rust"], COLORS["sage"]],
        max_scale=100,
    )
    add_card(
        slide,
        8.75,
        1.6,
        3.72,
        1.55,
        "TTool AI",
        ["状态机评分 63 vs 58", "速度快 15.2x", "块图评分 81 vs 70", "速度快 67.5x"],
        accent=COLORS["rust"],
        fill=COLORS["panel"],
        title_size=15,
        body_size=11,
    )
    add_card(
        slide,
        8.75,
        3.35,
        3.72,
        1.55,
        "IEC 61499 / workflow principles",
        ["一旦接上仿真、代码生成和 sanity checks，方法论就不再是一次 prompt。"],
        accent=COLORS["gold"],
        fill=COLORS["panel"],
        title_size=15,
        body_size=11,
    )
    add_card(
        slide,
        0.82,
        5.3,
        11.7,
        0.9,
        "Take-home",
        ["纯 prompt 可以给出骨架，但真正把质量拉上去的，是 model checking、仿真、编译检查和 workflow feedback。"],
        accent=COLORS["navy"],
        fill=COLORS["rust_soft"],
        title_size=15,
        body_size=11.5,
    )
    add_footer(slide, 8, "[12][13][14][16][17]")


def build_sources_curation(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "`sources/` 不是自然分布样本，而是面向数据集建设的治理后主集", "如果不先说明这一点，后面的统计就很容易被误读", section="文库证据")
    add_context_bar(
        slide,
        0.82,
        1.28,
        11.7,
        0.42,
        "如果不先讲治理口径，后面所有 EFSM/HSM/T0/T1 的比例都会被误读成自然分布。",
        "所以这一页先解释筛选逻辑，再看统计。",
        accent=COLORS["rust"],
    )
    add_card(
        slide,
        0.82,
        1.82,
        11.7,
        0.88,
        "Warning",
        ["后面所有 EFSM / HSM / T0 / T1 的比例，首先反映的是收录策略与数据集治理目标，其次才是领域文献现象本身。"],
        accent=COLORS["rust"],
        fill=COLORS["rust_soft"],
        title_size=15,
        body_size=11,
    )
    add_textbox(slide, 0.86, 2.78, 2.6, 0.2, "治理流程", size=10.5, bold=True, color=COLORS["navy"])
    add_card(slide, 0.86, 3.02, 2.8, 0.96, "广撒网检索", ["先把真实控制系统状态逻辑的文献面铺开。"], accent=COLORS["navy"], fill=COLORS["panel"], title_size=15, body_size=10.3)
    add_arrow(slide, 3.8, 3.32, 0.42, 0.34, fill=COLORS["sand"])
    add_card(slide, 4.28, 3.02, 2.8, 0.96, "标准化治理", ["按论文级、案例级、主类型、时间级别等口径做筛。"], accent=COLORS["teal"], fill=COLORS["panel"], title_size=15, body_size=10.3)
    add_arrow(slide, 7.22, 3.32, 0.42, 0.34, fill=COLORS["sand"])
    add_card(slide, 7.7, 3.02, 3.1, 0.96, "主集保留", ["优先保留 EFSM/HSM、T0/T1、细节高、不强趋同的案例。"], accent=COLORS["gold"], fill=COLORS["panel"], title_size=15, body_size=10.3)
    add_textbox(slide, 6.1, 4.0, 2.6, 0.2, "五套治理口径", size=10.5, bold=True, color=COLORS["navy"])
    add_table(
        slide,
        4.22,
        4.25,
        8.3,
        1.95,
        ["口径", "作用"],
        [
            ("论文级可用性", "判断单篇论文整体上能否形成可靠样本"),
            ("案例级角色", "区分核心保留、清洗后保留、降采样保留"),
            ("细节充实度", "判断是否足以支撑高质量建模与评测"),
            ("主类型", "回答“默认应把它理解成哪类状态机”"),
            ("时间级别", "回答时间语义到底只是局部 timer 还是强实时/连续耦合"),
        ],
        header_fill=COLORS["teal"],
        col_widths=[2.0, 6.3],
        font_size=10.2,
    )
    add_card(
        slide,
        0.86,
        4.25,
        3.0,
        1.95,
        "治理目标",
        [
            "优先保留 `EFSM/HSM`。",
            "优先保留 `T0/T1`。",
            "优先保留细节充实、可转为可执行样本的案例。",
            "对强趋同簇做降采样控制。",
        ],
        accent=COLORS["navy"],
        fill=COLORS["panel"],
        title_size=15,
        body_size=10.5,
    )
    add_footer(slide, 9, "[4][6]")


def build_sources_stats(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "`sources/` 的总体统计已经足以支撑数据集和问题边界判断", "统计项必须带定义列，否则数字没有解释力", section="文库证据")
    add_context_bar(
        slide,
        0.88,
        1.24,
        11.74,
        0.42,
        "样本主链已经够厚，不再是“先去找样本”的阶段。",
        "所以这页要把数量和定义一起说清楚。",
        accent=COLORS["navy"],
    )
    cards = [
        ("787", "论文总数", "正式入账论文目录", COLORS["navy"]),
        ("715", "论文级 🟢", "可直接支撑可靠样本", COLORS["green"]),
        ("746", "正例案例", "当前样本主链总量", COLORS["teal"]),
        ("685", "核心保留 `💎`", "主数据集主链", COLORS["gold"]),
    ]
    x = 0.78
    for value, label, detail, accent in cards:
        add_big_number_card(slide, x, 1.82, 2.86, 1.05, value, label, detail, accent=accent)
        x += 3.02
    add_table(
        slide,
        0.8,
        3.08,
        6.0,
        2.75,
        ["指标", "定义", "数量"],
        [
            ("论文总数", "当前 `sources/` 已正式入账的论文目录总数", "787"),
            ("论文级 `🟢`", "单篇论文整体上可直接支持可靠样本抽取", "715"),
            ("论文级 `🟡`", "单篇论文仍有价值，但需要额外整理或局部补证", "16"),
            ("论文级 `⚪`", "单篇论文最终未形成可靠样本", "56"),
        ],
        header_fill=COLORS["navy"],
        col_widths=[1.25, 3.85, 0.9],
        font_size=10.1,
    )
    add_table(
        slide,
        6.95,
        3.08,
        5.6,
        2.75,
        ["类别", "定义", "数量"],
        [
            ("正例案例总数", "正式入账、可作为控制状态样本讨论的案例条目", "746"),
            ("`💎` 核心保留", "细节和分布都足够好，适合进入主数据集主链", "685"),
            ("`🧰` 清洗后保留", "有价值，但需要进一步清洗、补证或统一口径", "20"),
            ("`🪫` 降采样保留", "本身可用，但因分布控制原因不应过量进入主集", "41"),
        ],
        header_fill=COLORS["teal"],
        col_widths=[1.35, 3.35, 0.9],
        font_size=10.1,
    )
    add_card(
        slide,
        0.82,
        6.0,
        11.7,
        0.55,
        "Take-home",
        ["主链样本已经够厚；现在真正该做的是围绕它定义论文对象、baseline 口径和可执行实验。"],
        accent=COLORS["navy"],
        fill=COLORS["gold_soft"],
        title_size=14,
        body_size=10.8,
    )
    add_footer(slide, 10, "[4][6]")


def build_sources_main_types(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "主类型分布说明真实样本主链是 `FSM / EFSM / HSM`", "713 / 746 条正例都落在离散控制状态层附近", section="文库证据")
    add_context_bar(
        slide,
        0.84,
        1.22,
        11.62,
        0.42,
        "主类型分布不只是数字，它直接决定论文对象该落在哪条主链上。",
        "所以这页要读成“control-state 占绝对主体”。",
        accent=COLORS["teal"],
    )
    add_chart(
        slide,
        0.85,
        1.78,
        5.2,
        3.75,
        ["FSM", "EFSM", "HSM", "Protocol", "Resource", "Hybrid"],
        [127, 429, 157, 4, 13, 16],
        chart_type=XL_CHART_TYPE.BAR_CLUSTERED,
        accent=COLORS["teal"],
        second_colors=[COLORS["navy"], COLORS["teal"], COLORS["gold"], COLORS["sand"], COLORS["sage"], COLORS["rust"]],
        max_scale=460,
    )
    add_table(
        slide,
        6.35,
        1.8,
        6.12,
        2.95,
        ["主类型", "定义"],
        [
            ("FSM", "普通离散阶段机，少量条件并入状态也不会明显失真"),
            ("EFSM", "离散状态仍是主体，但关键语义依赖 guard / effect 数据面"),
            ("HSM", "高层模式和低层子状态关系本身就是主要结构事实"),
            ("Protocol", "多角色请求、授权、接管等交互顺序是核心语义"),
            ("Resource-flow", "正确性主要由资源占用、互斥、释放关系决定"),
            ("Hybrid", "连续动力学或连续控制律是语义不可删的一部分"),
        ],
        header_fill=COLORS["teal"],
        col_widths=[1.45, 4.67],
        font_size=10.2,
    )
    add_card(
        slide,
        6.38,
        4.95,
        6.08,
        0.9,
        "关键比例",
        ["713 / 746 = 95.6% 的主集正例都落在 `FSM + EFSM + HSM` 这条离散控制状态主链上。"],
        accent=COLORS["navy"],
        fill=COLORS["teal_soft"],
        title_size=15,
        body_size=11.2,
    )
    add_footer(slide, 11, "[4]")


def build_sources_time_structure(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "时间级别与结构标签说明“离散控制”不等于“扁平简单 FSM”", "T0/T1 占主导，但显式时钟与层次结构都不是小噪声", section="文库证据")
    add_context_bar(
        slide,
        0.82,
        1.22,
        11.64,
        0.42,
        "离散主链并不意味着“模型可以极简化”。",
        "所以 timer、显式时钟和 hierarchy 都必须被保留下来。",
        accent=COLORS["navy"],
    )
    add_textbox(slide, 0.82, 1.72, 2.2, 0.2, "时间级别分布", size=10.5, bold=True, color=COLORS["navy"])
    add_chart(
        slide,
        0.82,
        2.0,
        5.0,
        2.9,
        ["T0", "T1", "T2", "T3"],
        [352, 367, 15, 12],
        chart_type=XL_CHART_TYPE.COLUMN_CLUSTERED,
        accent=COLORS["navy"],
        second_colors=[COLORS["navy"], COLORS["teal"], COLORS["gold"], COLORS["rust"]],
        max_scale=400,
    )
    add_textbox(slide, 6.25, 1.72, 2.2, 0.2, "结构标签覆盖", size=10.5, bold=True, color=COLORS["navy"])
    add_chart(
        slide,
        6.25,
        2.0,
        5.95,
        2.9,
        ["显式时钟", "层次", "连续耦合"],
        [243, 160, 71],
        chart_type=XL_CHART_TYPE.BAR_CLUSTERED,
        accent=COLORS["teal"],
        second_colors=[COLORS["teal"], COLORS["gold"], COLORS["rust"]],
        max_scale=270,
    )
    add_card(slide, 0.84, 5.15, 5.15, 0.88, "结论 1", ["`T0 + T1 = 719 / 746`，短期最稳的对象仍是离散控制 + 局部工程定时。"], accent=COLORS["navy"], fill=COLORS["panel"], title_size=15, body_size=10.6)
    add_card(slide, 6.25, 5.15, 5.95, 0.88, "结论 2", ["显式时钟与层次结构必须保留，所以目标形式主义不能退回最平的 FSM。"], accent=COLORS["teal"], fill=COLORS["panel"], title_size=15, body_size=10.6)
    add_footer(slide, 12, "[4][6]")


def build_sources_examples(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "代表样本显示：真实控制系统里至少并存五类不同建模难点", "同样都叫“状态机”，但它们的主难点并不相同", section="文库证据")
    add_card(
        slide,
        0.82,
        1.22,
        11.65,
        0.62,
        "Framing",
        ["这些样本不是用来“凑例子”，而是用来证明“状态机”一词背后其实罩着不同问题，因此论文对象必须主动收束。"],
        accent=COLORS["navy"],
        fill=COLORS["gold_soft"],
        title_size=14.5,
        body_size=10.6,
    )
    add_table(
        slide,
        0.82,
        2.02,
        11.65,
        4.12,
        ["场景", "标签", "关键建模难点", "对论文对象的启发"],
        [
            ("洗衣机 PLC", "EFSM / T1", "阶段链 + timer + guard", "真实工业控制里“阶段 + timer”是高频对象"),
            ("电梯 PLC", "EFSM / T1", "请求队列、方向优先、门控时长", "顺序控制与门控规则构成主问题"),
            ("铁路联锁", "Resource / T1-T2", "资源互斥、锁闭、释放", "有些“状态机”本质上更像强 guard / 资源系统"),
            ("UAV 分层任务", "HSM / T0-T1", "mission supervisor + 子层任务控制", "层次任务控制是另一条高频主线"),
            ("外骨骼步态控制", "Hybrid / T3", "连续相变量与模式切换强耦合", "确实存在第二类连续/混成问题"),
        ],
        header_fill=COLORS["navy"],
        col_widths=[1.55, 1.55, 3.45, 5.1],
        font_size=10.0,
    )
    add_card(
        slide,
        7.08,
        5.82,
        5.36,
        0.78,
        "结论",
        ["离散顺序控制、层次任务、资源互锁、连续耦合至少是四类不同问题。"],
        accent=COLORS["rust"],
        fill=COLORS["rust_soft"],
        title_size=13.5,
        body_size=9.8,
    )
    add_footer(slide, 13, "[4][6]")


def build_sm_family(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "`state_machine_types/` 证明“状态机”是一整个家族而不是单对象", "问题不在于有没有状态机，而在于我们到底主动选择其中哪一支", section="文库证据")
    add_context_bar(
        slide,
        0.84,
        1.22,
        11.62,
        0.42,
        "既然“状态机”本来就是家族，project_1 就不能假装目标对象天然唯一。",
        "所以必须主动选 control-state + infrastructure 这条分支。",
        accent=COLORS["navy"],
    )
    add_chart(
        slide,
        0.84,
        1.84,
        5.05,
        3.68,
        ["离散", "Timed", "Hybrid", "Petri", "契约", "DSL", "标准/元模型"],
        [160, 96, 46, 28, 31, 59, 264],
        chart_type=XL_CHART_TYPE.BAR_CLUSTERED,
        accent=COLORS["navy"],
        second_colors=[COLORS["navy"], COLORS["teal"], COLORS["rust"], COLORS["sage"], COLORS["sand"], COLORS["gold"], COLORS["navy"]],
        max_scale=290,
    )
    add_panel(slide, 6.35, 1.86, 6.0, 3.62, fill=COLORS["panel"], line=COLORS["line"], radius=True)
    add_textbox(slide, 8.65, 2.02, 1.4, 0.22, "状态机家族", font=FONT_SERIF, size=17, bold=True, color=COLORS["navy"], align=PP_ALIGN.CENTER)
    branches = [
        (6.75, 2.68, 2.0, 0.78, "control-state", "FSM / EFSM / HSM", COLORS["teal"]),
        (9.15, 2.68, 2.0, 0.78, "timed", "TA / clocks", COLORS["gold"]),
        (6.75, 3.74, 2.0, 0.78, "hybrid", "continuous coupling", COLORS["rust"]),
        (9.15, 3.74, 2.0, 0.78, "resource / contract", "Petri / contract", COLORS["sage"]),
    ]
    for x, y, w, h, title, detail, accent in branches:
        add_card(slide, x, y, w, h, title, [detail], accent=accent, fill=COLORS["panel_alt"], title_size=13.5, body_size=9.8)
    add_card(slide, 8.0, 4.76, 2.7, 0.92, "infrastructure", ["DSL / 标准 / 元模型 / 执行载体"], accent=COLORS["navy"], fill=COLORS["gold_soft"], title_size=14.5, body_size=10)
    add_card(slide, 0.84, 5.52, 11.62, 0.88, "因此", ["对 project_1 来说，最自然的选择不是“任意状态机”，而是 control-state profile 加执行基础设施。"], accent=COLORS["navy"], fill=COLORS["teal_soft"], title_size=14, body_size=10.4)
    add_footer(slide, 14, "[5][7]")


def build_control_state_definition(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "这篇论文更稳的对象应是控制系统的离散 control-state layer", "离散监督 / 顺序控制 与 连续 / 混成控制 在建模视角上其实是两类问题", section="project_1")
    add_table(
        slide,
        0.82,
        1.52,
        11.65,
        4.65,
        ["维度", "离散监督 / 顺序控制 / 模式管理", "连续 / 混成控制中的模式切换"],
        [
            ("典型系统", "PLC、电梯、铁路联锁、门控、任务控制、异常恢复链", "ABS / BBW、外骨骼步态、强时序医疗控制、动力学模式切换"),
            ("状态的主要含义", "模式、阶段、权限、流程位置、故障恢复位置", "控制律区间、相变量阶段、连续动力学运行区间"),
            ("核心建模难点", "guard、事件、互锁、局部 timer、异常链", "时钟组合、连续变量、动力学耦合、hybrid semantics"),
            ("更自然的模型", "FSM / EFSM / HSM / control-state DSL", "Timed / Hybrid 一类对象"),
            ("更自然的反馈基础设施", "parser、simulator、结构校验、可执行 trace", "timed/hybrid verification、数值仿真、symbolic reachability"),
        ],
        header_fill=COLORS["navy"],
        col_widths=[1.4, 5.0, 5.25],
        font_size=10.2,
    )
    add_card(
        slide,
        0.82,
        6.25,
        11.65,
        0.42,
        "论文对象建议",
        ["project_1 第一篇论文先解左列问题；右列问题不否认其重要性，但放到后续延展更稳。"],
        accent=COLORS["teal"],
        fill=COLORS["teal_soft"],
        title_size=13.5,
        body_size=10.2,
    )
    add_footer(slide, 15, "[4][5][6][7]")


def build_pyfcstm_progress(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "`pyfcstm` 从 2 月底到现在已经具备可执行基础设施的骨架", "它已经不是单文件 demo 级 DSL，而是在往工程可维护对象走", section="基础设施")
    add_big_number_card(slide, 0.85, 1.48, 2.25, 1.1, "dcf1f70", "main HEAD", "截至 2026-04-14", accent=COLORS["rust"])
    add_panel(slide, 3.35, 1.68, 8.95, 0.18, fill=COLORS["panel_alt"], line=COLORS["panel_alt"], radius=True)
    add_panel(slide, 3.35, 1.68, 8.95, 0.18, fill=COLORS["rust"], line=COLORS["rust"], radius=True)
    add_textbox(slide, 3.25, 1.98, 1.35, 0.2, "2026-02-28", font=FONT_MONO, size=9.5, color=COLORS["muted"], align=PP_ALIGN.LEFT)
    add_textbox(slide, 11.15, 1.98, 1.35, 0.2, "2026-04-14", font=FONT_MONO, size=9.5, color=COLORS["muted"], align=PP_ALIGN.RIGHT)
    cards = [
        ("import / 模块化", "import 语法、模型组装、目录入口、editor support", COLORS["navy"]),
        ("执行语义", "`if` 语句、运行时递归执行、symbolic if-block execution", COLORS["teal"]),
        ("代码生成", "Python / C 模板、`c_poll` 路线、template tests", COLORS["gold"]),
        ("工具支持", "PlantUML 导出、文档、教程、VS Code 支持", COLORS["sage"]),
        ("验证预备", "solver / verify groundwork、symbolic witness 方向", COLORS["rust"]),
    ]
    x = 0.85
    for title, detail, accent in cards:
        add_card(slide, x, 2.55, 2.25, 2.6, title, [detail], accent=accent, fill=COLORS["panel"], title_size=14.5, body_size=10.5)
        x += 2.4
    add_card(
        slide,
        0.85,
        5.52,
        11.65,
        0.72,
        "页面结论",
        ["`pyfcstm` 现在最值得强调的不是 feature 数量，而是它已经形成了一条从模型表达、执行、代码生成到后续验证接口的连续能力带。"],
        accent=COLORS["rust"],
        fill=COLORS["rust_soft"],
        title_size=14.5,
        body_size=11,
    )
    add_footer(slide, 16, "[8]")


def build_pyfcstm_role(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "`pyfcstm` 在论文里应被写成目标形式主义与闭环基座", "把“自然语言生成状态机”提升成“自然语言生成可执行形式模型”", section="基础设施")
    add_panel(slide, 3.1, 2.3, 7.15, 1.38, fill=COLORS["panel"], line=COLORS["line"], radius=True)
    steps = [
        (3.15, "需求文本", COLORS["panel_alt"]),
        (4.6, "LLM", COLORS["gold_soft"]),
        (5.75, "`pyfcstm`\ncontrol-state DSL", COLORS["teal_soft"]),
        (7.6, "parser /\nruntime", COLORS["blue_soft"]),
        (9.25, "simulation /\ncodegen /\nverification hooks", COLORS["rust_soft"]),
    ]
    for x, label, fill in steps:
        add_panel(slide, x, 2.58, 1.1 if x != 5.75 else 1.55, 0.82, fill=fill, line=COLORS["line"], radius=True)
        add_textbox(slide, x, 2.78, 1.55 if x == 5.75 else 1.1, 0.26, label, size=10.5, bold=True, color=COLORS["ink"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_arrow(slide, 4.23, 2.82, 0.28, 0.26, fill=COLORS["sand"], direction="right")
    add_arrow(slide, 5.42, 2.82, 0.28, 0.26, fill=COLORS["sand"], direction="right")
    add_arrow(slide, 7.32, 2.82, 0.28, 0.26, fill=COLORS["sand"], direction="right")
    add_arrow(slide, 8.92, 2.82, 0.28, 0.26, fill=COLORS["sand"], direction="right")
    add_card(slide, 0.82, 1.58, 2.1, 1.28, "target profile", ["不直接追求宽语义 UML/SCXML，而是主动收束成 control-state profile。"], accent=COLORS["navy"], fill=COLORS["panel"], title_size=14, body_size=10.2)
    add_card(slide, 0.82, 3.1, 2.1, 1.28, "executable semantics", ["一生成就可解析、可执行、可继续进入 parser/runtime 反馈。"], accent=COLORS["teal"], fill=COLORS["panel"], title_size=14, body_size=10.2)
    add_card(slide, 10.35, 1.58, 2.1, 1.28, "formal core", ["形式化核心与外部 action 显式隔离，方便验证与后续修复。"], accent=COLORS["gold"], fill=COLORS["panel"], title_size=14, body_size=10.2)
    add_card(slide, 10.35, 3.1, 2.1, 1.28, "cross-project base", ["它为 project_2/3/4 提供共同模型对象，而不是一次性 demo。"], accent=COLORS["rust"], fill=COLORS["panel"], title_size=14, body_size=10.2)
    add_card(
        slide,
        0.84,
        5.52,
        11.62,
        0.72,
        "结论",
        ["`pyfcstm` 回答的是“LLM 到底该生成什么对象，为什么这个对象既可执行又适合闭环”这个研究问题，而不是简单实现问题。"],
        accent=COLORS["rust"],
        fill=COLORS["gold_soft"],
        title_size=14.5,
        body_size=11,
    )
    add_footer(slide, 17, "[7][8]")


def build_pyudbm_progress(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "`project_3` 的实质推进主要在 `pyudbm`，但核心搜索仍缺", "backend 不是空白，只是还没长成第一版 profile-guided verifier", section="基础设施")
    add_context_bar(
        slide,
        0.82,
        1.22,
        11.64,
        0.42,
        "project_3 很容易被看成“目录还空，所以几乎没动”。",
        "所以这页要把“地基已做很多”和“完整 verifier 仍未成型”分开说。",
        accent=COLORS["rust"],
    )
    add_big_number_card(slide, 0.82, 1.76, 2.3, 1.02, "a8d0649", "main HEAD", "本地 clone 于 `~/oo-projects/pyudbm`", accent=COLORS["rust"])
    stack_items = [
        ("符号核", "UDBM API 与 UCDD 路线已立住", COLORS["navy"]),
        ("模型前端", "UTAP 绑定、`load_xml`、`parse_query` 已有", COLORS["teal"]),
        ("query + corpus", "roundtrip 与 178 个官方样本已成体系", COLORS["gold"]),
        ("文献与路线", "TA / UPPAAL 阅读地图与 roadmap 持续维护", COLORS["sage"]),
    ]
    y = 2.95
    for idx, (title, detail, accent) in enumerate(stack_items):
        width = 3.1 + idx * 0.34
        add_panel(slide, 0.98, y, width, 0.52, fill=COLORS["panel"], line=accent, radius=True)
        add_textbox(slide, 1.18, y + 0.15, width - 0.3, 0.22, f"{title}  |  {detail}", size=10.2, bold=True, color=COLORS["ink"])
        y += 0.64
    add_table(
        slide,
        6.15,
        1.88,
        6.3,
        4.18,
        ["层", "已有", "仍缺 / 影响"],
        [
            ("基础符号层", "已有", "不是主要瓶颈"),
            ("模型 / query 接口", "已有", "官方样本和 roundtrip 已成体系"),
            ("symbolic reachability", "仍缺", "无法形成真正 verifier"),
            ("A[] / E<> 求值", "仍缺", "性质检查闭环还接不上"),
            ("witness / counterexample", "仍缺", "反馈链条不完整"),
            ("verifyta 核心搜索", "仍缺", "这才是 project_3 真正未过的门槛"),
        ],
        header_fill=COLORS["rust"],
        col_widths=[1.8, 1.0, 3.5],
        font_size=10.0,
    )
    add_card(
        slide,
        0.84,
        6.02,
        11.62,
        0.74,
        "页面结论",
        ["`project_3` 现在最合理的定位，是继续让 `pyudbm` 沉淀 timed backend，而不是抢在 `project_1` 之前承担主投稿。"],
        accent=COLORS["rust"],
        fill=COLORS["rust_soft"],
        title_size=13.5,
        body_size=10.2,
    )
    add_footer(slide, 18, "[9][10][11]")


def build_infra_feedback(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "我越来越相信基础设施反馈才是 LLM-based modeling 的真正杀手锏", "parser、runtime、simulation、model checking 和 regression traceability 会把问题性质彻底改变", section="基础设施")
    add_context_bar(
        slide,
        0.82,
        1.22,
        11.64,
        0.42,
        "单次生成很快会碰到 action、语义一致性和可执行性瓶颈。",
        "所以真正把质量拉高的，不是 prompt 花样，而是反馈基础设施。",
        accent=COLORS["navy"],
    )
    add_panel(slide, 3.55, 2.42, 6.15, 2.18, fill=COLORS["panel"], line=COLORS["line"], radius=True)
    loop_boxes = [
        (4.0, 2.78, 1.1, 0.56, "LLM", COLORS["gold_soft"]),
        (5.38, 2.78, 1.55, 0.56, "control-state\nDSL", COLORS["teal_soft"]),
        (7.28, 2.78, 1.55, 0.56, "parser /\nruntime", COLORS["blue_soft"]),
        (7.28, 3.48, 1.75, 0.64, "simulator /\nchecker /\ntests", COLORS["rust_soft"]),
        (5.15, 3.48, 1.75, 0.64, "structured\nfeedback", COLORS["sage_soft"]),
    ]
    for x, y, w, h, label, fill in loop_boxes:
        add_panel(slide, x, y, w, h, fill=fill, line=COLORS["line"], radius=True)
        add_textbox(slide, x, y + 0.12, w, h - 0.08, label, size=10.3, bold=True, color=COLORS["ink"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_arrow(slide, 5.08, 2.95, 0.24, 0.22, fill=COLORS["sand"], direction="right")
    add_arrow(slide, 6.98, 2.95, 0.24, 0.22, fill=COLORS["sand"], direction="right")
    add_arrow(slide, 7.88, 3.28, 0.22, 0.22, fill=COLORS["sand"], direction="down")
    add_arrow(slide, 6.88, 3.74, 0.26, 0.22, fill=COLORS["sand"], direction="left")
    add_arrow(slide, 4.38, 3.12, 0.22, 0.36, fill=COLORS["sand"], direction="up")
    evidence_cards = [
        (0.82, 1.82, 2.3, 1.12, "2026 direct baseline", ["0.7029 vs 0.5431", "Hybrid 流程能明显拉回弱模型"], COLORS["navy"]),
        (10.2, 1.82, 2.25, 1.18, "SysML empirical", ["94.6 / 88.0 / 43.1 / 37.3", "规则反馈有效，但还不够"], COLORS["teal"]),
        (0.82, 4.7, 2.3, 1.12, "TTool AI", ["63 vs 58，15.2x", "81 vs 70，67.5x"], COLORS["rust"]),
        (10.2, 4.62, 2.25, 1.2, "workflow principles", ["可信 GenAI 依赖 decomposition、sanity checks、traceability"], COLORS["gold"]),
    ]
    for x, y, w, h, title, lines, accent in evidence_cards:
        add_card(slide, x, y, w, h, title, lines, accent=accent, fill=COLORS["panel"], title_size=13.5, body_size=10)
    add_card(
        slide,
        3.15,
        5.42,
        7.1,
        0.88,
        "Take-home",
        ["与其继续拼 prompt，不如把模型输出放进能持续打分、回传反例、约束格式和校验语义的环境里。"],
        accent=COLORS["navy"],
        fill=COLORS["gold_soft"],
        title_size=14.5,
        body_size=11,
    )
    add_footer(slide, 19, "[12][13][14][16][17]")


def build_decisions_next_steps(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_block(slide, "如果明天拍板这五件事，后续 6 周的推进路径会更稳", "收束问题对象、拉厚实验、准备 conference-style 论文", section="待拍板事项")
    add_textbox(slide, 0.84, 1.35, 2.0, 0.2, "6 周倒排", size=10.5, bold=True, color=COLORS["navy"])
    phases = [
        ("第 1-2 周", "收束问题定义与论文主张", COLORS["teal"]),
        ("第 3-4 周", "固化样本与 baseline 实验", COLORS["gold"]),
        ("第 5-6 周", "完成初稿与 venue 策略", COLORS["rust"]),
    ]
    x = 0.86
    for idx, (label, detail, accent) in enumerate(phases):
        add_card(slide, x, 1.62, 3.55, 1.08, label, [detail], accent=accent, fill=COLORS["panel"], title_size=15, body_size=11)
        if idx < len(phases) - 1:
            add_arrow(slide, x + 3.65, 1.95, 0.38, 0.32, fill=COLORS["sand"])
        x += 3.95
    decisions = [
        "本学期主投稿是否锁定 `project_1`",
        "论文对象是否先限定为离散 `control-state layer`",
        "`pyfcstm` 是否正面写成 target formalism / executable IR",
        "`pyudbm` 是否继续做 backend 地基而不抢主线",
        "近端写法是否按 ASE-style automation + feedback infrastructure 组织",
    ]
    x_positions = [0.86, 4.05, 7.24, 0.86, 4.05]
    y_positions = [3.2, 3.2, 3.2, 4.86, 4.86]
    accents = [COLORS["navy"], COLORS["teal"], COLORS["gold"], COLORS["rust"], COLORS["sage"]]
    for idx, (x, y, text, accent) in enumerate(zip(x_positions, y_positions, decisions, accents, strict=True), start=1):
        add_card(slide, x, y, 2.95, 1.35, f"决策 {idx}", [text], accent=accent, fill=COLORS["panel"], title_size=14.5, body_size=10.5)
    add_card(
        slide,
        10.22,
        4.08,
        2.25,
        2.15,
        "Closing",
        ["如果这五件事里有三四件能拍板，后面 6 周就可以沿着“对象收束 -> 实验拉厚 -> 初稿成型”稳步推进。"],
        accent=COLORS["navy"],
        fill=COLORS["gold_soft"],
        title_size=15,
        body_size=10.5,
    )
    add_footer(slide, 20, "[1][7][15]")


def build_presentation() -> Path:
    notes = parse_notes_from_guide(GUIDE)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    prs.core_properties.title = TITLE
    prs.core_properties.subject = "讨论 deck"
    prs.core_properties.author = "Codex"

    build_cover(prs)
    build_agenda(prs)
    build_summary(prs)
    build_why_project1_now(prs)
    build_four_project_map(prs)
    build_project1_evidence_chain(prs)
    build_baselines_overview(prs)
    build_baseline_evidence(prs)
    build_sources_curation(prs)
    build_sources_stats(prs)
    build_sources_main_types(prs)
    build_sources_time_structure(prs)
    build_sources_examples(prs)
    build_sm_family(prs)
    build_control_state_definition(prs)
    build_pyfcstm_progress(prs)
    build_pyfcstm_role(prs)
    build_pyudbm_progress(prs)
    build_infra_feedback(prs)
    build_decisions_next_steps(prs)

    prs.save(OUTPUT)
    validate_slide_count(OUTPUT, 20)
    apply_notes(OUTPUT, notes)
    validate_notes(OUTPUT, notes)
    return OUTPUT


if __name__ == "__main__":
    result = build_presentation()
    print(result)
