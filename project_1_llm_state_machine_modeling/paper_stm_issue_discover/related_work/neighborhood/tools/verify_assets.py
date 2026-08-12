"""资产可获取性的**机械核验**：⛔ 不看论文怎么说，⭐ 只看实际能不能取到。

⛔ **为什么必须机械核验。** 论文里写「code available at ...」是一句声明，⛔ 不是一个事实。
⭐ 本仓库 `baselines/` 已经撞到过实例：FlowFSM 的 GitHub 仓库**存在且返回 200**，
⛔ 但里面只有 `README.md` 和 `.gitignore`，README 自己写着 source code will be shared
later。⭐ 只查 HTTP 状态码会把它判成 🟢，⛔ 而它实际是 🟠。

⭐ 因此本脚本对 GitHub 仓库**不只查存在性，还查内容**：文件数、是否只剩文档、
有无 release、有无 license、HEAD commit。⭐ 判 🟢 的门槛是「**取下来有东西**」。

⚠️ **本脚本只做机械判定，⛔ 不做终裁。** 例如「有 30 个文件但全是图片」它判 🟢，
⭐ 而人看了应该判 🟠。机械结果进 `assets.md` 的「核验证据」列，⭐ emoji 由写卡的人定。

用法::

    python -m tools.verify_assets --urls urls.txt
    python -m tools.verify_assets --url https://github.com/foo/bar --json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

_GH = re.compile(r"github\.com/([\w.\-]+)/([\w.\-]+?)(?:\.git)?(?:/|$)", re.I)

#: ⭐ 只有这些后缀算「文档」。⛔ 一个仓库若**全部**文件都落在这里，就是空壳。
_DOC_ONLY = {".md", ".txt", ".rst", ".gitignore", ".gitattributes", ".license"}


def _gh_api(path: str) -> dict | list | None:
    """走 `gh api`（⭐ 复用已登录 token，避免 60/h 的匿名限流）。

    ⛔ 这是**只读**调用。⚠️ 本仓库规定 subagent 不得做 `gh` 写操作；
    ⭐ `api GET` 不在此列，但仍不要用它去 POST/PATCH。
    """
    try:
        r = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            return json.loads(r.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass
    return None


def http_probe(url: str, timeout: int = 30) -> dict:
    """⭐ 只取头与前若干字节 —— 判活即可，⛔ 不要把整个数据集拖下来。"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research asset check)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            head = resp.read(2048)
            return {
                "status": resp.status,
                "final_url": resp.geturl(),
                "content_type": resp.headers.get("Content-Type", ""),
                "content_length": resp.headers.get("Content-Length", ""),
                #: ⚠️ SPA 壳与 WAF 页都会返回 200 —— 留一个片段供人判。
                "head_snippet": head[:200].decode("utf-8", "replace").replace("\n", " "),
            }
    except urllib.error.HTTPError as e:
        return {"status": e.code, "error": f"HTTPError {e.code}"}
    except Exception as e:  #: noqa: BLE001 —— 网络异常形态太多，⭐ 一律如实记下类型
        return {"status": None, "error": f"{type(e).__name__}: {e}"}


def probe_github(owner: str, repo: str) -> dict:
    meta = _gh_api(f"repos/{owner}/{repo}")
    if meta is None:
        return {"kind": "github", "reachable": False, "note": "⛔ gh api 取不到（不存在 / 私有 / 限流）"}
    branch = meta.get("default_branch", "main")
    tree = _gh_api(f"repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
    files: list[str] = []
    truncated = False
    if isinstance(tree, dict):
        truncated = bool(tree.get("truncated"))
        files = [t["path"] for t in tree.get("tree", []) if t.get("type") == "blob"]
    releases = _gh_api(f"repos/{owner}/{repo}/releases")
    n_rel = len(releases) if isinstance(releases, list) else 0

    def _ext(p: str) -> str:
        n = p.rsplit("/", 1)[-1]
        return ("." + n.rsplit(".", 1)[-1]).lower() if "." in n else n.lower()

    non_doc = [f for f in files if _ext(f) not in _DOC_ONLY]
    #: ⭐⭐ 空壳判据：没有任何非文档文件。⛔ 这正是 FlowFSM 那一类。
    shell = len(files) > 0 and not non_doc
    return {
        "kind": "github",
        "reachable": True,
        "default_branch": branch,
        "head_sha": (_gh_api(f"repos/{owner}/{repo}/commits/{branch}") or {}).get("sha", ""),
        "pushed_at": meta.get("pushed_at", ""),
        "size_kb": meta.get("size", 0),
        "license": ((meta.get("license") or {}) or {}).get("spdx_id", ""),
        "n_files": len(files),
        "n_files_truncated": truncated,
        "n_non_doc_files": len(non_doc),
        "n_releases": n_rel,
        "is_shell": shell,
        "sample_files": sorted(files)[:12],
        #: ⭐ 机械建议，⛔ 不是终裁
        "suggest": "🟠 空壳" if shell else ("🟢" if non_doc else "🟠"),
    }


def verify(url: str) -> dict:
    url = url.strip()
    if not url:
        return {}
    if m := _GH.search(url):
        out = probe_github(m.group(1), m.group(2))
        out["url"] = url
        return out
    out = {"kind": "http", "url": url, **http_probe(url)}
    st = out.get("status")
    out["suggest"] = "🟢" if st == 200 else ("🟠" if st in (301, 302, 403) else "⚪")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--urls", type=Path, help="每行一个 URL")
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    urls = list(args.url)
    if args.urls:
        urls += [l for l in args.urls.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    if not urls:
        print("⛔ 没有输入 URL。", file=sys.stderr)
        return 2

    res = [verify(u) for u in urls]
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    print("| URL | 机械建议 | 关键证据 |")
    print("| :-- | :-: | :-- |")
    for r in res:
        if r.get("kind") == "github":
            ev = (
                f"HEAD `{(r.get('head_sha') or '')[:10]}` · 文件 {r.get('n_files')}"
                f"（非文档 {r.get('n_non_doc_files')}）· release {r.get('n_releases')}"
                f" · license {r.get('license') or '无'}"
                + ("⛔ **空壳**" if r.get("is_shell") else "")
                + ("⚠️ 树被截断" if r.get("n_files_truncated") else "")
            ) if r.get("reachable") else r.get("note", "")
        else:
            ev = f"HTTP {r.get('status')} · {r.get('content_type','')} · {r.get('error','')}"
        print(f"| {r.get('url','')} | {r.get('suggest','')} | {ev} |")

    n_green = sum(1 for r in res if r.get("suggest") == "🟢")
    print(f"\n⭐ **产出率：{n_green} / {len(res)} 机械判可取**（⛔ 终裁仍需人看内容）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
