from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FeedbackLoopConfig:
    records_path: Path
    llm_profile: str | None = None
    llm_config_path: Path | None = None
    max_attempts: int = 1
    timeout_s: float | None = None

    @classmethod
    def from_env(cls, prefix: str = "PAPER_STM_FEEDBACK_") -> "FeedbackLoopConfig":
        records_path = Path(os.environ.get(prefix + "RECORDS_PATH", "feedback_loop_records.jsonl")).expanduser().resolve()
        llm_config = os.environ.get(prefix + "LLM_CONFIG_PATH") or os.environ.get("LLM_CONFIG_FILE")
        max_attempts_raw = os.environ.get(prefix + "MAX_ATTEMPTS", "1")
        timeout_raw = os.environ.get(prefix + "TIMEOUT_S")
        return cls(
            records_path=records_path,
            llm_profile=os.environ.get(prefix + "LLM_PROFILE"),
            llm_config_path=Path(llm_config).expanduser().resolve() if llm_config else None,
            max_attempts=max(1, int(max_attempts_raw)),
            timeout_s=float(timeout_raw) if timeout_raw else None,
        )

    def public_summary(self) -> dict[str, object]:
        return {
            "records_path": str(self.records_path),
            "llm_profile": self.llm_profile,
            "llm_config_path": str(self.llm_config_path) if self.llm_config_path else None,
            "max_attempts": self.max_attempts,
            "timeout_s": self.timeout_s,
        }
