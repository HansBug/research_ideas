#!/usr/bin/env python3

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SUMMARY_PATH = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "SUMMARY.md"
SECTION_PATH = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "manual_audit" / "efsm_hsm_t0_double_a_summary_section.md"

BEGIN = "<!-- BEGIN EFSM_HSM_T0_DOUBLE_A_SUBLEDGER -->"
END = "<!-- END EFSM_HSM_T0_DOUBLE_A_SUBLEDGER -->"


def main() -> None:
    summary = SUMMARY_PATH.read_text(encoding="utf-8")
    section = SECTION_PATH.read_text(encoding="utf-8").rstrip() + "\n"

    start = summary.index(BEGIN) + len(BEGIN)
    end = summary.index(END)
    updated = summary[:start] + "\n\n" + section + summary[end:]
    SUMMARY_PATH.write_text(updated, encoding="utf-8")
    print(SUMMARY_PATH)


if __name__ == "__main__":
    main()
