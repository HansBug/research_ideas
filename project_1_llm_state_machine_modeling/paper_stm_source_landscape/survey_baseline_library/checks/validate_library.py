from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - old Python fallback
    ZoneInfo = None

VALID_SCORES = {"🟢", "🟡", "🟠", "🔴"}
TIMESTAMP_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b")
REQUIRED_SINGLE_PAPER_FILES = [
    "paper.pdf",
    "paper_content.txt",
    "bibtex.bib",
    "fulltext_review.md",
]
REQUIRED_REVIEW_ANCHORS = [
    "## 2. 最终全文级判断",
    "## 5. D1--D7 全文级证据链",
    "## 6. 负证据检索",
    "## 9. 可写与不可写声明",
]
README_ANCHORS = [
    "维护路线图与工作入口",
    "七维独立评分总原则",
    "D1 控制系统领域贴近度",
    "D7 对 #85 证据门支撑度",
]
GUIDE_ANCHORS = [
    "四件套硬规则",
    "七维独立打分硬规则",
    "评分降级与升级判定",
    "CSV 与 SUMMARY 字段合同",
    "证据链最低密度",
    "可写 / 不可写声明模板",
    "时间戳审计规则",
]
REQUIRED_MATRIX_COLS = [
    "paper_dir",
    "paper_pdf_path",
    "paper_content_path",
    "bibtex_path",
    "fulltext_review_path",
    "source_material_committed",
    "repo_paper_pdf_path",
    "repo_paper_content_path",
    "paper_content_sha256_16",
    "extraction_command",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def now_china_naive() -> datetime:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("Asia/Shanghai")).replace(tzinfo=None)
    return datetime.now()


def find_future_timestamps(path: Path, now: datetime) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    future: list[str] = []
    for match in TIMESTAMP_RE.finditer(text):
        value = match.group(0)
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if parsed > now:
            future.append(value)
    return future


def validate_summary_main_table(summary: str, expected_rows: int) -> list[str]:
    errors: list[str] = []
    marker = "## 3. 全文级 baseline 初检矩阵"
    if marker not in summary:
        return ["SUMMARY 缺少全文级 baseline 初检矩阵章节"]
    section = summary.split(marker, 1)[1].split("## 3.1", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("| ")]
    data_rows = [line for line in rows if not line.startswith("| # ") and not line.startswith("|---")]
    if len(data_rows) != expected_rows:
        errors.append(f"SUMMARY 主表数据行数 {len(data_rows)} != 单论文目录数 {expected_rows}")
    for idx, row in enumerate(data_rows, start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != 15:
            errors.append(f"SUMMARY 主表第 {idx} 行列数 {len(cells)} != 15: {row[:120]}")
            continue
        if cells[0] != str(idx):
            errors.append(f"SUMMARY 主表第 {idx} 行编号为 {cells[0]!r}，期望 {idx}")
    return errors


def validate(lib_root: Path, expected_count: int | None = None) -> list[str]:
    errors: list[str] = []
    repo_root = lib_root.parents[3]
    baseline_data = lib_root.parent / "baselines" / "data"

    for name in ["README.md", "GUIDE.md", "SUMMARY.md"]:
        if not (lib_root / name).exists():
            errors.append(f"缺少入口文件: {lib_root / name}")

    readme = (lib_root / "README.md").read_text(encoding="utf-8")
    guide = (lib_root / "GUIDE.md").read_text(encoding="utf-8")
    summary = (lib_root / "SUMMARY.md").read_text(encoding="utf-8")
    audit_now = now_china_naive()
    for anchor in README_ANCHORS:
        if anchor not in readme:
            errors.append(f"README 缺少 roadmap / 评分入口锚点: {anchor}")
    for anchor in GUIDE_ANCHORS:
        if anchor not in guide:
            errors.append(f"GUIDE 缺少可执行规则锚点: {anchor}")

    papers_dir = lib_root / "papers"
    paper_dirs = sorted(p for p in papers_dir.iterdir() if p.is_dir()) if papers_dir.exists() else []
    if expected_count is not None and len(paper_dirs) != expected_count:
        errors.append(f"单论文目录数 {len(paper_dirs)} != 期望 {expected_count}")
    for paper_dir in paper_dirs:
        for filename in REQUIRED_SINGLE_PAPER_FILES:
            file_path = paper_dir / filename
            if not file_path.exists() or file_path.stat().st_size == 0:
                errors.append(f"缺少或为空: {file_path}")
        review_path = paper_dir / "fulltext_review.md"
        if review_path.exists():
            review_text = review_path.read_text(encoding="utf-8", errors="ignore")
            for anchor in REQUIRED_REVIEW_ANCHORS:
                if anchor not in review_text:
                    errors.append(f"{paper_dir.name} 的 fulltext_review.md 缺少章节: {anchor}")

    matrix_path = lib_root / "data" / "fulltext_review_matrix.csv"
    receipt_path = lib_root / "data" / "local_fulltext_receipt.csv"
    matrix = read_csv(matrix_path)
    receipt = read_csv(receipt_path)
    if len(matrix) != len(paper_dirs):
        errors.append(f"fulltext_review_matrix.csv 行数 {len(matrix)} != 单论文目录数 {len(paper_dirs)}")
    if len(receipt) != len(paper_dirs):
        errors.append(f"local_fulltext_receipt.csv 行数 {len(receipt)} != 单论文目录数 {len(paper_dirs)}")
    if matrix:
        for col in REQUIRED_MATRIX_COLS:
            if col not in matrix[0]:
                errors.append(f"fulltext_review_matrix.csv 缺少字段: {col}")

    for row in matrix:
        review_id = row.get("fulltext_review_id") or row.get("title") or "<unknown>"
        for path_col in ["paper_pdf_path", "paper_content_path", "bibtex_path", "fulltext_review_path"]:
            rel = row.get(path_col, "")
            if not rel or not (lib_root / rel).exists():
                errors.append(f"{review_id}: 路径字段 {path_col} 不存在或无法解析: {rel}")
        if row.get("source_material_committed") != "yes_paper_pdf_and_paper_content_txt":
            errors.append(f"{review_id}: source_material_committed 不是 yes_paper_pdf_and_paper_content_txt")
        for dim in range(1, 8):
            score = row.get(f"D{dim}_fulltext_score", "")
            if score not in VALID_SCORES:
                errors.append(f"{review_id}: D{dim} 分数非法或为空: {score!r}")
            for suffix in ["fulltext_evidence_locator", "fulltext_paraphrase", "negative_evidence", "writing_action", "confidence"]:
                if not row.get(f"D{dim}_{suffix}"):
                    errors.append(f"{review_id}: D{dim}_{suffix} 为空")

    errors.extend(validate_summary_main_table(summary, len(paper_dirs)))

    for local_link in re.findall(r"\]\((\.\/[^)]+)\)", summary):
        target = lib_root / local_link[2:]
        if not target.exists():
            errors.append(f"SUMMARY 本地链接失效: {local_link}")

    old_patterns = [
        "不提交 PDF",
        "不保存 PDF",
        "PDF/全文提交 | 0",
        "不得在单论文目录中放置",
        "private_copy_committed,no",
    ]
    for path in lib_root.parent.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".csv"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in old_patterns:
                if pattern in text:
                    errors.append(f"发现旧口径 {pattern!r}: {path.relative_to(repo_root)}")

    # 上游初筛数据的最小闭合检查；未来若行数变化，应显式传入新的 expected-count 并更新 README/SUMMARY。
    upstream_expected = [
        (baseline_data / "screening_audit.csv", 438),
        (baseline_data / "issue85_narrowed_related_candidates_preliminary.csv", 69),
        (baseline_data / "auto_fulltext_light_review_gate.csv", 21),
        (baseline_data / "targeted_search_audit.csv", 19),
    ]
    for path, count in upstream_expected:
        if path.exists():
            rows = read_csv(path)
            if len(rows) != count:
                errors.append(f"{path.relative_to(repo_root)} 行数 {len(rows)} != {count}")

    manual_bib = baseline_data / "manual_download_needed.bib"
    if manual_bib.exists():
        entries = sum(1 for line in manual_bib.read_text(encoding="utf-8").splitlines() if line.lstrip().startswith("@"))
        if entries != len(paper_dirs):
            errors.append(f"manual_download_needed.bib 条目 {entries} != 单论文目录数 {len(paper_dirs)}")

    for path in lib_root.rglob("*"):
        if path.is_file() and path.stat().st_size >= 100 * 1024 * 1024:
            errors.append(f"单文件超过或等于 100MB: {path} ({path.stat().st_size} bytes)")

    for path in lib_root.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".csv"}:
            for value in find_future_timestamps(path, audit_now):
                errors.append(f"发现未来时间戳 {value}: {path.relative_to(repo_root)}；本文库时间默认 Asia/Shanghai")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 #85 综述 baseline 文库四件套、D1--D7 与总账同步规则。")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="survey_baseline_library 根目录，默认取脚本上级目录。",
    )
    parser.add_argument("--expected-count", type=int, default=25, help="期望单论文目录数量。")
    args = parser.parse_args()

    lib_root = args.root.resolve()
    errors = validate(lib_root, args.expected_count)
    if errors:
        print("校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {lib_root} 四件套、D1--D7、SUMMARY 链接与维护规则校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
