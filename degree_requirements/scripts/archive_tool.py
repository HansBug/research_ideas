#!/usr/bin/env python3
"""加密 raw 档案读取工具。

用法：
  source .env
  python degree_requirements/scripts/archive_tool.py list
  python degree_requirements/scripts/archive_tool.py test
  python degree_requirements/scripts/archive_tool.py show --member MANIFEST.txt
  python degree_requirements/scripts/archive_tool.py extract --output /tmp/degree_raw_check

脚本只从环境变量 DEGREE_REQUIREMENTS_ARCHIVE_PASSWORD 读取口令；不要把口令写进命令行或仓库文档。
"""
from __future__ import annotations

import argparse
import os
import sys
import zipfile
from pathlib import Path

ARCHIVE = Path(__file__).resolve().parents[1] / "encrypted_archives" / "2026-06-16-degree-requirements-raw-archive.zip"
ENV_NAME = "DEGREE_REQUIREMENTS_ARCHIVE_PASSWORD"


def archive_password() -> bytes:
    value = os.environ.get(ENV_NAME)
    if not value:
        raise SystemExit(f"缺少环境变量 {ENV_NAME}；请先在仓库根目录执行：source .env")
    return value.encode("utf-8")


def open_archive() -> zipfile.ZipFile:
    if not ARCHIVE.exists():
        raise SystemExit(f"找不到归档文件：{ARCHIVE}")
    return zipfile.ZipFile(ARCHIVE)


def list_archive() -> int:
    # 即便 zip 文件名目录理论上可无密码读取，本库仍要求所有 archive 操作先由 .env 提供口令，
    # 以避免形成“未加载本地档案口令也可操作 raw 档案”的维护习惯。
    archive_password()
    with open_archive() as zf:
        for info in zf.infolist():
            print(f"{info.file_size:>8}  {info.filename}")
    return 0


def test_archive() -> int:
    pwd = archive_password()
    ok = True
    with open_archive() as zf:
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
            print(f"OK {ARCHIVE}")
            return 0
        return 1


def _safe_output_path(base: Path, member_name: str) -> Path:
    target = (base / member_name).resolve()
    base_resolved = base.resolve()
    if target != base_resolved and base_resolved not in target.parents:
        raise SystemExit(f"拒绝解压可疑路径：{member_name}")
    return target


def show_member(member: str) -> int:
    pwd = archive_password()
    with open_archive() as zf:
        try:
            with zf.open(member, pwd=pwd) as fh:
                data = fh.read()
        except KeyError as exc:
            raise SystemExit(f"zip 内不存在文件：{member}") from exc
    sys.stdout.buffer.write(data)
    return 0


def extract_archive(output: str) -> int:
    pwd = archive_password()
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    with open_archive() as zf:
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
    print(f"extracted to {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="读取 degree_requirements 加密 raw 档案")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="列出 zip 内文件")
    sub.add_parser("test", help="测试 zip 口令和完整性")
    p_show = sub.add_parser("show", help="读取 zip 内单个文本/原始文件并输出到 stdout")
    p_show.add_argument("--member", required=True, help="zip 内文件路径，例如 MANIFEST.txt")
    p_extract = sub.add_parser("extract", help="解压到指定目录")
    p_extract.add_argument("--output", required=True, help="输出目录")
    args = parser.parse_args()

    if args.cmd == "list":
        return list_archive()
    if args.cmd == "test":
        return test_archive()
    if args.cmd == "show":
        return show_member(args.member)
    if args.cmd == "extract":
        return extract_archive(args.output)
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
