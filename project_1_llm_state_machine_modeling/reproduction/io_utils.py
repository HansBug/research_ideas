from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from config import DERIVED_ROOT, DISCUSSION_ASSET_DIR, RESULTS_ROOT


def load_discussion_parquet(name: str) -> pd.DataFrame:
    path = DISCUSSION_ASSET_DIR / f"{name}.parquet"
    return pd.read_parquet(path)


def load_derived_parquet(name: str) -> pd.DataFrame:
    path = DERIVED_ROOT / f"{name}.parquet"
    if path.exists():
        return pd.read_parquet(path)
    return load_discussion_parquet(name)


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)


def write_json(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def baseline_result_dir(name: str) -> Path:
    path = RESULTS_ROOT / name
    path.mkdir(parents=True, exist_ok=True)
    return path
