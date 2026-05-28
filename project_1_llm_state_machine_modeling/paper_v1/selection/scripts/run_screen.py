"""Concurrent codex screening driver.

Reads candidates.jsonl, dispatches review_one.review_sample() concurrently
across N workers. Resume-safe (skips already-existing reviews/<id>.json).
Emits progress JSON every PROGRESS_INTERVAL seconds to progress.json.

Usage:
    source .env
    python -m scripts.run_screen --workers 10 --max-attempts 3 --timeout 600
    python -m scripts.run_screen --workers 16 --only-failed   # retry pass
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import sys
import threading
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from review_one import (  # noqa: E402
    CANDIDATES, REVIEWS_DIR, LOGS_DIR, SELECTION_ROOT,
    already_done, review_sample,
)

PROGRESS_PATH = SELECTION_ROOT / "progress.json"
PROGRESS_LOCK = threading.Lock()


def load_all_candidates() -> list[str]:
    ids: list[str] = []
    with CANDIDATES.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ids.append(row["sample_id"])
    return ids


def write_progress(state: dict) -> None:
    with PROGRESS_LOCK:
        PROGRESS_PATH.write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def worker(sample_id: str, timeout_s: int, max_attempts: int) -> tuple[str, str, str]:
    try:
        if already_done(sample_id):
            return sample_id, "skip", "already_done"
        result = review_sample(sample_id, timeout_s=timeout_s, max_attempts=max_attempts)
        verdict = result.get("verdict", "?")
        return sample_id, "ok", verdict
    except Exception as e:
        return sample_id, "err", f"{type(e).__name__}: {str(e)[:200]}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--max-attempts", type=int, default=3)
    ap.add_argument("--only-failed", action="store_true",
                    help="Only retry samples without a valid review JSON")
    ap.add_argument("--limit", type=int, default=0, help="Cap total samples (0=all)")
    args = ap.parse_args()

    all_ids = load_all_candidates()
    pending = [sid for sid in all_ids if not already_done(sid)]
    if args.only_failed:
        # Same set, but verbose mode for clarity
        pass
    if args.limit > 0:
        pending = pending[: args.limit]
    total_target = len(all_ids)
    print(f"[run_screen] total_candidates={total_target} pending={len(pending)} workers={args.workers}")
    if not pending:
        print("[run_screen] nothing to do")
        return

    state = {
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "workers": args.workers,
        "total_candidates": total_target,
        "pending_at_start": len(pending),
        "done": 0,
        "ok": 0,
        "err": 0,
        "skip": 0,
        "last_err": None,
        "in_flight": [],
    }
    write_progress(state)

    in_flight_set: set[str] = set()
    in_flight_lock = threading.Lock()
    counter_lock = threading.Lock()

    def wrapped(sid: str) -> tuple[str, str, str]:
        with in_flight_lock:
            in_flight_set.add(sid)
        try:
            return worker(sid, args.timeout, args.max_attempts)
        finally:
            with in_flight_lock:
                in_flight_set.discard(sid)

    t0 = time.time()
    last_progress = t0

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(wrapped, sid): sid for sid in pending}
        for fut in cf.as_completed(futures):
            sid = futures[fut]
            try:
                _, status, info = fut.result()
            except Exception as e:
                status, info = "err", f"unhandled: {e}"
            with counter_lock:
                state["done"] += 1
                state[status] = state.get(status, 0) + 1
                if status == "err":
                    state["last_err"] = f"{sid}: {info}"
                # Snapshot
                with in_flight_lock:
                    state["in_flight"] = sorted(in_flight_set)[:20]
                state["elapsed_s"] = round(time.time() - t0, 1)
                rate = state["done"] / max(state["elapsed_s"], 1.0)
                state["rate_per_s"] = round(rate, 3)
                if rate > 0:
                    remaining = len(pending) - state["done"]
                    state["eta_s"] = round(remaining / rate, 1)
                write_progress(state)
            # Print every completion (lean): one line per sample
            print(f"  [{state['done']}/{len(pending)}] {sid} → {status} ({info[:60]})", flush=True)

    state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    write_progress(state)
    print(f"[run_screen] done. ok={state.get('ok',0)} err={state.get('err',0)} skip={state.get('skip',0)} elapsed={state['elapsed_s']}s")


if __name__ == "__main__":
    main()
