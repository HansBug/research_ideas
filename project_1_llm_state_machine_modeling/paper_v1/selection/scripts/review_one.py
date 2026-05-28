"""Run one codex review for a single candidate sample.

Usage:
    python -m scripts.review_one <sample_id>

Reads candidates.jsonl, builds a codex prompt that instructs codex to
read the paper_content.txt (and optionally paper.pdf) from absolute
paths, then score H/G/A/F dimensions. Writes JSON to reviews/<id>.json.

Idempotent: skips if review already exists and is valid JSON.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SELECTION_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SELECTION_ROOT.parents[2]
CANDIDATES = SELECTION_ROOT / "candidates.jsonl"
REVIEWS_DIR = SELECTION_ROOT / "reviews"
LOGS_DIR = SELECTION_ROOT / "logs"


SYSTEM_PROMPT = """You are an academic reviewer specialized in industrial control state-machine synthesis. Your task is to judge whether a specific sample (one 条目 from a paper) is a strong "stress-test" candidate for benchmarking an LLM-based state-machine modeling method against the prior strongest Umple-style baseline (Apvrille et al. 2025 — structure_event_driven Hybrid SMF).

You score each sample on FOUR dimensions, each from 0 to 3, where the dimensions correspond to components on which the Apvrille 2025 paper reports the LOWEST baseline F1 (actions ≈ 0.34, guards ≈ 0.42, hierarchical_states ≈ 0.50). Selecting samples that score high on these dimensions is a METHOD-INDEPENDENT stress test of baseline weakness, NOT cherry-picking.

You MUST read the actual paper content before scoring. Use the Read tool on paths provided.

You MUST output a single JSON object — no prose, no markdown fences. Output format is locked.
"""


SCORING_RUBRIC = """## Scoring rubric

H/G/A/F dimensions are each scored 0/1/2/3 with this universal legend:

  - 0 = ❌ absent (no signal in NL or paper)
  - 1 = 🟡 minor / superficial (mentioned but trivial)
  - 2 = 🟢 clearly present (multiple instances, meaningful complexity)
  - 3 = 💎 strong / definitional (this sample is FUNDAMENTALLY about this feature)

### Dimension H — Hierarchical / composite states
Does the controller exhibit nested modes, sub-states inside a parent mode, or composite states with internal sub-FSMs?
  - 3: explicit parent-with-children architecture (e.g., "Operating mode is split into Normal / Degraded / Emergency, with Normal further containing Idle / Active / Pause")
  - 2: at least one composite state with ≥2 sub-states
  - 1: mode-grouping mentioned but flat
  - 0: pure flat FSM, no hierarchy

### Dimension G — Guarded arithmetic / multi-variable guards
Does the controller exhibit guards that combine multiple variables with arithmetic / comparison / boolean composition?
  - 3: guards with >2 variables, arithmetic (e.g., `x + delta > threshold`), or boolean combinators
  - 2: multiple guards each referencing 1-2 variables
  - 1: simple comparison guards on a single threshold
  - 0: no guards (transitions purely event-driven)

### Dimension A — Non-trivial transition actions / variable updates / cross-cutting outputs
Does the controller perform meaningful state/variable updates or cross-cutting outputs (log/publish/alert/monitor) on transitions or per-tick?
  - 3: multiple actions per transition, with variable updates AND I/O side-effects; or per-mode continuous-monitoring outputs (`during` actions)
  - 2: actions present but mostly direct command outputs (open/close)
  - 1: trivial set-flag actions
  - 0: no meaningful actions

### Dimension F — Fault recovery / global escape paths
Does the controller exhibit emergency-stop, fault-rollback, abort-from-any-state, or other cross-cutting escape patterns?
  - 3: explicit "from any state, on fault X go to safe state" or layered fault hierarchy
  - 2: at least one dedicated fault/recovery transition
  - 1: error mentioned but recovery vague
  - 0: no fault model

## Dimension BD — baseline-trap density (redesigned 2026-05-27)

BD is NOT a generic "difficulty" feeling. It is derived from a fixed list of 6 trap signals,
each of which is a DOCUMENTED failure mode of prior LLM-to-state-machine baselines:

  - Apvrille et al. 2025 §IV-C (Hybrid SMF on Umple): actions F1=0.00 (GPT-4o) / 0.16 (Claude),
    guards F1=0.23-0.42 — "Single-prompt loses overall context, multi-step loses single-aspect context"
  - Wang et al. 2025 llms_emp §Phase II (PlantUML + rule-based feedback): rules fixed 35/37 syntax
    + 22/25 grammar, but only 31/72 semantic and 56/150 consistency — rules cannot synthesize semantics
  - Apvrille & Sultan 2024 TTool-AI: JSON-loop catches syntax errors only, semantic errors yield
    infinite-loop retries

You must first identify which trap signals are present (binary present/absent, with brief evidence
quote/summary), then derive BD from the count + critical-trap rule:

  T1 cross_section_element     : information about one specific state (its name, guards, and actions)
                                  is split across 2+ non-adjacent NL locations. Adjacent paragraphs
                                  in the same subsection are NOT split. Examples of T1=True:
                                    * State name in §III, but its entry actions are listed in §IV
                                      Implementation table without restating the state-to-action map
                                    * Guards introduced in figure caption, actions in unrelated
                                      results discussion paragraph
                                    * State enumeration on page 3, behavior details on page 5+
                                  Example of T1=False:
                                    * All state info (name, guards, actions) within a single
                                      subsection or a single labeled figure
                                  Calibration: industrial papers commonly have moderate splits;
                                  expect ~40% of samples to be T1=True.
  T2 implicit_domain_term      : NL uses a domain term that implies AT LEAST ONE state-transition
                                  rule the LLM must DECODE from outside domain knowledge (not from
                                  the NL itself).
                                  T2=True examples:
                                    * "limp mode" → implies reduced power + ignore non-critical
                                    * "interlock" → implies blocking on multi-condition AND
                                    * "safe state" / "fail-safe" → implies actuator-stop + position-hold
                                    * "manual override" → implies operator priority over automatic
                                    * "fault recovery" without spelling out the recovery path
                                  T2=False examples:
                                    * "pressure booster" is just a STATE NAME, not implicit ruleset
                                    * "active mode" is a name, the rules are spelled out in NL
                                  Calibration: industrial NL commonly uses ≥1 such domain term;
                                  expect ~50% of samples to be T2=True.
  T3 implicit_action_from_prose: actions for a state are described in narrative prose, NOT
                                  co-located with the state's explicit definition. This forces the
                                  LLM to ATTRIBUTE actions back to states by inference.
                                  T3=True examples:
                                    * State list in §III.A; actions like "the pump cycles 500 ms
                                      during pressure release" appear in §IV.B discussion
                                    * "When entering hover, the controller also initializes the
                                      altitude PID" — but PID init is mentioned only in a control-
                                      theory background section, not in the state spec
                                  T3=False examples:
                                    * State table directly lists actions per state (e.g.,
                                      `Increase: k1=1, k2=0, n=0`)
                                    * Each state's actions are stated in the same paragraph as the
                                      state name and guards
                                  Calibration: expect ~30-40% of samples to be T3=True.
  T4 multivar_arith_guard      : at least one guard combines ≥2 variables with arithmetic / boolean
                                  composition → Apvrille guards F1 ≤ 0.42
  T5 composite_internal_behavior: parent/composite state has its own entry/during/exit behavior
                                  beyond its sub-states → Umple superstate-action recall failure
  T6 global_cross_cutting_recovery: NL declares "from any state on fault X go to safe Y" or other
                                  cross-cutting rule baselines must duplicate across N transitions

BD score derivation (revised 2026-05-27 v3 — balanced):

  - bd=0 ⚪ : 0 traps present
  - bd=1 🟡 : 1 trap present
  - bd=2 🟢 : 2 traps present
  - bd=3 💎 : ≥3 traps present, OR T6 present (T6 is the hardest single trap — global
              cross-cutting rules force baselines to duplicate N transitions)

CRITICAL: BD must NOT be derived from H/G/A/F. It is derived ONLY from the 6 trap-signal booleans.
A sample with H=3 but all info in one tight paragraph can have bd=0. A sample with H=1 but
heavy cross-section splits plus implicit domain terms can have bd=3.

EXPECTED DISTRIBUTION over a large sample pool: bd 0/1/2/3 ≈ 15/25/30/30 (%). If you find yourself
flagging 0 traps on most samples, you are too conservative; if you flag ≥4 on most samples, you are
too liberal. Use the calibration percentages above (T1≈40%, T2≈50%, T3≈30-40%) as anchors.

## Dimension FT — pyfcstm primitive uniqueness advantage (redesigned 2026-05-27)

FT is NOT "can pyfcstm express this?" (the answer is almost always yes). FT measures the
*UNIQUENESS strength* of pyfcstm's 4 contribution primitives on THIS sample — how much shorter
or more reliable would the encoding be in pyfcstm vs. Umple/PlantUML.

You identify which primitive advantages are present + strength, then derive FT:

  C1 advantage: speculative-DFS validation of composite-state init/pseudo chains.
                Strong (2) iff NL has ≥1 deep composite state with non-trivial init transition that
                a single-prompt LLM would plausibly mis-route.
                Weak (1) iff one shallow composite state with default init.
                None (0) otherwise.

  C2 advantage: unified Expr IR + Z3 over guards.
                Strong (2) iff ≥3 guards with arithmetic+boolean composition where SMT-style guard
                consistency check would catch contradiction.
                Weak (1) iff 1-2 such guards.
                None (0) otherwise.

  C3 advantage: forced transitions `!` + aspect `>> during` save N→1 line ratio.
                Strong (2) iff ≥1 cross-cutting rule applies to ≥3 substates simultaneously
                (forced `!` writes 1 line, Umple writes ≥3 explicit transitions)
                OR ≥1 per-mode continuous monitor declared once on parent (aspect `>> during`).
                Weak (1) iff ≥1 cross-cutting rule applies to 1-2 substates.
                None (0) otherwise.

  C4 advantage: abstract action + read-only context decouples effector.
                Strong (2) iff NL describes effector-agnostic outputs ("log event", "publish status",
                "notify operator") that don't commit to a specific I/O channel.
                Weak (1) iff some side-effects are abstract but most are concrete.
                None (0) otherwise.

FT score derivation (revised 2026-05-27 v3 — by breadth, avoiding sum=3-4 dead zone):

Let breadth_weak = count of C1..C4 with strength ≥ 1
Let breadth_strong = count of C1..C4 with strength == 2

  - ft=0 ⚪ : breadth_weak == 0  (no primitive offers any uniqueness)
  - ft=1 🟡 : breadth_weak == 1  (exactly one primitive offers advantage)
  - ft=2 🟢 : breadth_weak == 2, OR (breadth_weak ≥ 3 AND breadth_strong == 0)
              (multiple weak advantages, or 3+ weak ones)
  - ft=3 💎 : breadth_weak ≥ 3 AND breadth_strong ≥ 1
              (broad multi-primitive advantage AND at least one is strong)

CRITICAL: ft=3 should mark samples where pyfcstm primitives offer MULTIPLE uniqueness advantages
(not just C2 — most industrial NL has guards, so C2 alone is too common). Expect ft 0/1/2/3 ≈
20/35/30/15 (%). If you find C2 is the only primitive ever advantaged, you're undervaluing C1/C3/C4.

## Hard exclusions (independent booleans)
  - has_parallel: NL describes concurrent / parallel regions
  - has_history_restore: NL describes resume-where-left-off behavior requiring history pseudo-state
  - only_io_no_stm: NL is just hardware I/O wiring with no state-machine abstraction
  - too_thin_for_stm: NL is too vague to construct a state machine reference

## Verdict
  - "candidate" — strong stress-test sample, recommend for top-15
  - "backup" — meaningful but secondary signal, recommend for backup-15
  - "exclude" — fails hard exclusion OR sum(H+G+A+F) < 4 OR no meaningful complexity

## OUTPUT (JSON only, no fences, no preamble):
{
  "sample_id": "<echo>",
  "scores": {
    "H_hierarchical":      {"score": 0|1|2|3, "evidence": "<short quote or summary>"},
    "G_guards_arith":      {"score": 0|1|2|3, "evidence": "<short quote or summary>"},
    "A_actions_nontrivial":{"score": 0|1|2|3, "evidence": "<short quote or summary>"},
    "F_fault_recovery":    {"score": 0|1|2|3, "evidence": "<short quote or summary>"}
  },
  "bd_trap_signals": {
    "T1_cross_section_element":      {"present": true|false, "evidence": "<quote or summary>"},
    "T2_implicit_domain_term":       {"present": true|false, "evidence": "<quote or summary>"},
    "T3_implicit_action_from_prose": {"present": true|false, "evidence": "<quote or summary>"},
    "T4_multivar_arith_guard":       {"present": true|false, "evidence": "<quote or summary>"},
    "T5_composite_internal_behavior":{"present": true|false, "evidence": "<quote or summary>"},
    "T6_global_cross_cutting_recovery":{"present": true|false, "evidence": "<quote or summary>"}
  },
  "ft_primitive_advantage": {
    "C1_speculative_dfs":     {"strength": 0|1|2, "evidence": "<quote or summary>"},
    "C2_expr_ir_smt":         {"strength": 0|1|2, "evidence": "<quote or summary>"},
    "C3_forced_and_aspect":   {"strength": 0|1|2, "evidence": "<quote or summary>"},
    "C4_abstract_action":     {"strength": 0|1|2, "evidence": "<quote or summary>"}
  },
  "exclusions": {
    "has_parallel": false,
    "has_history_restore": false,
    "only_io_no_stm": false,
    "too_thin_for_stm": false
  },
  "baseline_difficulty": 0|1|2|3,
  "fcstm_fit": 0|1|2|3,
  "key_nl_quotes": ["<quote 1>", "<quote 2>"],
  "one_line_pitch": "<one-sentence English pitch why this is a hard stress-test case>",
  "verdict": "candidate|backup|exclude",
  "rationale": "<2-4 sentence justification grounded in paper evidence>"
}
"""


def load_candidate(sample_id: str) -> dict | None:
    with CANDIDATES.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if row["sample_id"] == sample_id:
                return row
    return None


def build_user_prompt(c: dict) -> str:
    paper_txt = (REPO_ROOT / c["paper_txt_path"]).resolve() if c.get("paper_txt_path") else None
    paper_pdf = (REPO_ROOT / c["paper_pdf_path"]).resolve() if c.get("paper_pdf_path") else None
    stm_md = (REPO_ROOT / c["stm_md_path"]).resolve()

    pdf_line = f"  - paper_pdf (use only if paper_content.txt is unclear): {paper_pdf}\n" if paper_pdf else ""
    return f"""## Task

Score the following sample on H/G/A/F + BD + FT per the rubric below.

## Sample identity
  - sample_id: {c['sample_id']}
  - paper_slug: {c['paper_slug']}
  - entry_idx: {c['entry_idx']}
  - entry_title: {c['entry_title']}
  - control_object: {c['entry_meta'].get('control_object', '?')}
  - stm_type: {c['entry_meta'].get('stm_type') or c['file_meta'].get('stm_type', '?')}
  - structure_tag: {c['entry_meta'].get('structure_tag') or c['file_meta'].get('structure_tags', '?')}

## Required reading (you MUST read these before scoring)

  - stm_md (file with the structured extraction, entry block at offsets [{c['entry_text_offsets']['start']}, {c['entry_text_offsets']['end']}]):
    {stm_md}
  - paper_content.txt (PRIMARY source; read FULLY): {paper_txt}
{pdf_line}
You MUST use the Read tool on stm_md and paper_content.txt BEFORE scoring. Cross-check the §2 NL description against the paper's actual control architecture (sections describing states, transitions, guards, modes, fault handling). If §2 looks accurate, score based on it; if §2 omits hierarchy/guards/actions that the paper actually has, score on the paper's reality, not §2's compression.

{SCORING_RUBRIC}

Now output ONLY the JSON object."""


def already_done(sample_id: str) -> bool:
    out_path = REVIEWS_DIR / f"{sample_id}.json"
    if not out_path.exists():
        return False
    try:
        data = json.loads(out_path.read_text(encoding="utf-8"))
        return isinstance(data, dict) and "scores" in data
    except Exception:
        return False


def _strip_fence(text: str) -> str:
    s = text.strip()
    if not s.startswith("```"):
        return s
    first_nl = s.find("\n")
    if first_nl >= 0:
        s = s[first_nl + 1:]
    if s.endswith("```"):
        s = s[:-3]
    return s.strip()


def _extract_final_message(jsonl_stdout: str) -> tuple[str, dict]:
    final_text = ""
    usage: dict = {}
    for line in jsonl_stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line)
        except json.JSONDecodeError:
            continue
        if evt.get("type") == "item.completed":
            item = evt.get("item", {}) or {}
            if item.get("type") == "agent_message":
                final_text = item.get("text", "")
        elif evt.get("type") == "turn.completed":
            usage = evt.get("usage", {}) or {}
    return final_text, usage


def run_codex(system_prompt: str, user_prompt: str, timeout_s: int = 600) -> dict:
    cmd_bin = os.environ.get("CODEX_CMD", "codex")
    model = os.environ.get("CODEX_MODEL", "gpt-5.5").strip() or "gpt-5.5"
    full = f"<SYSTEM>\n{system_prompt}\n</SYSTEM>\n\n{user_prompt}"
    cmd = [cmd_bin, "exec", "--json", "--skip-git-repo-check",
           "--sandbox", "read-only", "-m", model]
    result = subprocess.run(
        cmd, input=full, capture_output=True, text=True,
        timeout=timeout_s, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"codex exit={result.returncode} stderr_tail:\n{result.stderr[-800:]}"
        )
    final_text, usage = _extract_final_message(result.stdout)
    if not final_text:
        raise RuntimeError(f"codex empty agent_message; stdout head:\n{result.stdout[:600]}")
    cleaned = _strip_fence(final_text)
    # codex often emits prose before JSON; isolate the first balanced {...}
    if not cleaned.startswith("{"):
        m = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if m:
            cleaned = m.group(0)
    parsed = json.loads(cleaned)
    parsed["_meta"] = {"annotator": "codex", "model": model, "usage": usage}
    return parsed


def review_sample(sample_id: str, timeout_s: int = 600, max_attempts: int = 3) -> dict:
    c = load_candidate(sample_id)
    if c is None:
        raise KeyError(f"sample {sample_id} not in candidates.jsonl")
    user_prompt = build_user_prompt(c)
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            t0 = time.time()
            parsed = run_codex(SYSTEM_PROMPT, user_prompt, timeout_s=timeout_s)
            parsed["sample_id"] = sample_id  # enforce
            parsed["_meta"]["duration_s"] = round(time.time() - t0, 1)
            parsed["_meta"]["attempt"] = attempt
            REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
            (REVIEWS_DIR / f"{sample_id}.json").write_text(
                json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            return parsed
        except Exception as e:
            last_err = e
            LOGS_DIR.mkdir(parents=True, exist_ok=True)
            (LOGS_DIR / f"{sample_id}.attempt{attempt}.err").write_text(
                f"{type(e).__name__}: {e}\n", encoding="utf-8"
            )
            time.sleep(2 ** attempt)
    raise RuntimeError(f"codex review failed after {max_attempts} attempts: {last_err}") from last_err


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: python -m scripts.review_one <sample_id>")
        sys.exit(2)
    sample_id = sys.argv[1]
    if already_done(sample_id):
        print(f"[skip] {sample_id} already reviewed")
        return
    out = review_sample(sample_id)
    print(json.dumps({"sample_id": sample_id,
                      "verdict": out.get("verdict"),
                      "scores": {k: v.get("score") for k, v in out.get("scores", {}).items()}},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
