from .edges import ANALYSIS_STAGE, FINAL_STAGE, PREPARATION_STAGE


def ordered_stage_groups() -> list[tuple[str, tuple[str, ...]]]:
    return [
        ("preparation", PREPARATION_STAGE),
        ("analysis", ANALYSIS_STAGE),
        ("finalization", FINAL_STAGE),
    ]


__all__ = ["ordered_stage_groups"]
