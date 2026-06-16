#!/usr/bin/env python3
"""degree_requirements 加密 raw 档案读取工具。

用法：
  source .env
  python degree_requirements/scripts/archive_tool.py archives
  python degree_requirements/scripts/archive_tool.py list
  python degree_requirements/scripts/archive_tool.py test
  python degree_requirements/scripts/archive_tool.py show --member MANIFEST.txt
  python degree_requirements/scripts/archive_tool.py extract --output /tmp/degree_raw_check

多档案场景：
  python degree_requirements/scripts/archive_tool.py --archive 2026-06-16-degree-requirements-raw-archive.zip list
  也可以在本地 .env 中配置 DEGREE_REQUIREMENTS_ARCHIVE_FILE 指定默认档案；仓库文档不写可复制赋值样式。

脚本只从环境变量 DEGREE_REQUIREMENTS_ARCHIVE_PASSWORD 读取口令；不要把口令写进命令行或仓库文档。
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

import pyzipper

ARCHIVE_DIR = Path(__file__).resolve().parents[1] / "encrypted_archives"
PASSWORD_ENV = "DEGREE_REQUIREMENTS_ARCHIVE_PASSWORD"
ARCHIVE_FILE_ENV = "DEGREE_REQUIREMENTS_ARCHIVE_FILE"


def archive_password() -> bytes:
    value = os.environ.get(PASSWORD_ENV)
    if not value:
        raise SystemExit(f"缺少环境变量 {PASSWORD_ENV}；请先在仓库根目录执行：source .env")
    return value.encode("utf-8")


def available_archives() -> list[Path]:
    if not ARCHIVE_DIR.exists():
        return []
    return sorted(p for p in ARCHIVE_DIR.glob("*.zip") if p.is_file())


def _resolve_archive_name(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (ARCHIVE_DIR / candidate).resolve()
    archive_root = ARCHIVE_DIR.resolve()
    if resolved != archive_root and archive_root not in resolved.parents:
        raise SystemExit(f"拒绝读取 encrypted_archives 外部档案：{value}")
    if not resolved.exists():
        raise SystemExit(f"找不到归档文件：{resolved}")
    if resolved.suffix.lower() != ".zip":
        raise SystemExit(f"只允许读取 .zip 归档：{resolved}")
    return resolved


def resolve_archive(cli_archive: str | None) -> Path:
    chosen = cli_archive or os.environ.get(ARCHIVE_FILE_ENV)
    if chosen:
        return _resolve_archive_name(chosen)

    archives = available_archives()
    if not archives:
        raise SystemExit(f"{ARCHIVE_DIR} 下没有可读取的 .zip 档案")
    if len(archives) == 1:
        return archives[0]
    names = ", ".join(p.name for p in archives)
    raise SystemExit(
        f"发现多个档案，请使用 --archive 或 {ARCHIVE_FILE_ENV} 指定一个：{names}"
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def open_archive(path: Path) -> pyzipper.AESZipFile:
    if not path.exists():
        raise SystemExit(f"找不到归档文件：{path}")
    return pyzipper.AESZipFile(path)


def list_available_archives() -> int:
    # 与 list/test/show/extract 保持一致：所有档案相关操作都必须先加载本地 .env。
    archive_password()
    archives = available_archives()
    if not archives:
        print(f"{ARCHIVE_DIR} 下暂无 .zip 档案")
        return 0
    for path in archives:
        print(f"{path.name}	{path.stat().st_size}	{sha256_file(path)}")
    return 0


def list_archive(path: Path) -> int:
    # 即便 zip 文件名目录理论上可无密码读取，本库仍要求所有 archive 操作先由 .env 提供口令，
    # 以避免形成“未加载本地档案口令也可操作 raw 档案”的维护习惯。
    archive_password()
    with open_archive(path) as zf:
        for info in zf.infolist():
            print(f"{info.file_size:>8}  {info.filename}")
    return 0


def test_archive(path: Path) -> int:
    pwd = archive_password()
    ok = True
    with open_archive(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            try:
                with zf.open(info, pwd=pwd) as fh:
                    while fh.read(1024 * 1024):
                        pass
            except Exception as exc:  # noqa: BLE001 - CLI diagnostics
                ok = False
                print(f"FAIL {info.filename}: {exc}", file=sys.stderr)
        if ok:
            print(f"OK {path}")
            return 0
        return 1


def _safe_output_path(base: Path, member_name: str) -> Path:
    target = (base / member_name).resolve()
    base_resolved = base.resolve()
    if target != base_resolved and base_resolved not in target.parents:
        raise SystemExit(f"拒绝解压可疑路径：{member_name}")
    return target


def show_member(path: Path, member: str) -> int:
    pwd = archive_password()
    with open_archive(path) as zf:
        try:
            with zf.open(member, pwd=pwd) as fh:
                data = fh.read()
        except KeyError as exc:
            raise SystemExit(f"zip 内不存在文件：{member}") from exc
    sys.stdout.buffer.write(data)
    return 0


def extract_archive(path: Path, output: str) -> int:
    pwd = archive_password()
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    with open_archive(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                _safe_output_path(out, info.filename).mkdir(parents=True, exist_ok=True)
                continue
            target = _safe_output_path(out, info.filename)
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info, pwd=pwd) as src, target.open("wb") as dst:
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    dst.write(chunk)
    print(f"extracted {path.name} to {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="读取 degree_requirements 加密 raw 档案")
    parser.add_argument(
        "--archive",
        help=(
            "要读取的 zip 文件名或 encrypted_archives/ 下相对路径；"
            f"多档案时也可用环境变量 {ARCHIVE_FILE_ENV} 指定"
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("archives", help="列出 encrypted_archives/ 下可用 zip 档案及 SHA256")
    sub.add_parser("list", help="列出所选 zip 内文件")
    sub.add_parser("test", help="测试所选 zip 口令和完整性")
    p_show = sub.add_parser("show", help="读取所选 zip 内单个文本/原始文件并输出到 stdout")
    p_show.add_argument("--member", required=True, help="zip 内文件路径，例如 MANIFEST.txt")
    p_extract = sub.add_parser("extract", help="解压所选 zip 到指定目录")
    p_extract.add_argument("--output", required=True, help="输出目录")
    args = parser.parse_args()

    if args.cmd == "archives":
        return list_available_archives()

    archive = resolve_archive(args.archive)
    if args.cmd == "list":
        return list_archive(archive)
    if args.cmd == "test":
        return test_archive(archive)
    if args.cmd == "show":
        return show_member(archive, args.member)
    if args.cmd == "extract":
        return extract_archive(archive, args.output)
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
