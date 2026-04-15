from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


REPRO_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = REPRO_ROOT.parent
REPO_ROOT = PROJECT_ROOT.parent
DATA_ROOT = REPRO_ROOT / "data"
RAW_ROOT = DATA_ROOT / "raw"
DERIVED_ROOT = DATA_ROOT / "derived"
CACHE_ROOT = DATA_ROOT / "cache"
RESULTS_ROOT = REPRO_ROOT / "results"

DISCUSSION_MD = (
    PROJECT_ROOT
    / "discussions"
    / "2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md"
)
DISCUSSION_ASSET_DIR = PROJECT_ROOT / "discussions" / (
    "2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets"
)

NUTSTORE_SM_ROOT = Path("/home/zhangshaoang/Nutstore/work/202508博士开题/sm")
CODEX_CONFIG = Path.home() / ".codex" / "config.toml"
CODEX_ENV_FILES = [
    Path.home() / ".codex" / "api68886868.env",
    Path.home() / ".codex" / "findcg.env",
]

DEFAULT_MODEL = "gpt-5.4"
DEFAULT_PROVIDER_ORDER = ["airouter", "findcg", "miaocg"]


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str
    env_keys: tuple[str, ...]


PROVIDERS = {
    "airouter": ProviderConfig(
        name="AIRouter",
        base_url="https://airouter.service.itstudio.club/v1",
        env_keys=("AIROUTER_API_KEY",),
    ),
    "findcg": ProviderConfig(
        name="FindCG",
        base_url="https://www.findcg.com/v1",
        env_keys=("FINDCG_API_KEY",),
    ),
    "miaocg": ProviderConfig(
        name="MiaoCG",
        base_url="https://api.miaocg.cn/v1",
        env_keys=("MIAOCG_API_KEY", "FINDCG_API_KEY"),
    ),
    "api68886868": ProviderConfig(
        name="68886868",
        base_url="https://api.68886868.xyz/v1",
        env_keys=("API68886868_API_KEY",),
    ),
}


def ensure_runtime_dirs() -> None:
    for path in (RAW_ROOT, DERIVED_ROOT, CACHE_ROOT, RESULTS_ROOT):
        path.mkdir(parents=True, exist_ok=True)


def load_export_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'").strip('"')
    return values


def resolve_api_env() -> dict[str, str]:
    resolved = dict(os.environ)
    for env_file in CODEX_ENV_FILES:
        for key, value in load_export_file(env_file).items():
            resolved.setdefault(key, value)
    return resolved
