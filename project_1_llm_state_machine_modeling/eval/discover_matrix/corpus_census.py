"""Structural census of all 60 FCSTM STM_0 models, read via pyfcstm."""
import json, pathlib, re, sys

R = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/reports/llms_emp_r45_java_60")
sys.path.insert(0, "/home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop/src")
from paper_stm_feedback_loop.assertions import build_eval_environment


def main():
    # 60 例是 10 份 NL spec x 6 个 LLM 的全因子设计，不是 60 个独立需求。
    # 谓词选择由 NL 措辞驱动，所以覆盖度的主约束在 NL 轴（只有 10 格），不在 LLM 轴。
    import hashlib
    nl_group = {}
    for nl in sorted(R.glob("pairs/*/nl.txt")):
        h = hashlib.md5(nl.read_bytes()).hexdigest()[:8]
        nl_group.setdefault(h, []).append(nl.parent.name)
    group_of = {c: h for h, cs in nl_group.items() for c in cs}

    rows = []
    for path in sorted((R / "fcstm").glob("*.fcstm")):
        case = path.stem.replace("llms_emp_feedback_final_", "")
        text = path.read_text()
        trace = json.loads((R / f"source_traces/{path.stem}.json").read_text())
        excl = trace.get("attribution_exclusions") or []
        env = build_eval_environment(model_text=text, source_mappings=trace.get("mappings") or [],
            source_exclusions=excl, timeout_seconds=60, fbmcq_solver_timeout_ms=5000,
            fbmcq_max_bound=3, fbmcq_process_wall_seconds=15.0)
        entry = env._raw_functions["occupancy_after"]
        api = next(x.__self__ for x in (entry if isinstance(entry, tuple) else (entry,)) if hasattr(x, "__self__"))
        states = list(api.structure.states())
        # 层数：路径点数的最大值
        depths = [str(getattr(s, "path", "")).count(".") for s in states]
        composites = [s for s in states if getattr(s, "is_composite", False)]
        events = list(api.structure.events())
        try:
            variables = list(api.structure.variables())
        except Exception:
            variables = []
        # transition / action 从文本统计（结构 facade 无直接聚合）
        n_tr = len(re.findall(r"^\s*\S.*->", text, re.M))
        n_eventless = len(re.findall(r"^\s*\w+\s*->\s*\w+\s*;\s*$", text, re.M))
        n_star = len(re.findall(r"\[\*\]", text))
        n_guard = len(re.findall(r"\bif\s*\[", text))
        n_effect = len(re.findall(r"\beffect\s*\{", text))
        # FCSTM 的 action 语法是 `enter abstract Accelerate;`，没有花括号。
        # 早先用 `enter\s*\{` 统计，于是 60 例全报 0，据此得出"无从验证
        # action_declared"的结论——那是错的：0004/0034/0044/0054 各声明 3-5 条，
        # 且是唯一能验证该谓词的样本。按该错误结论筛除"无 action"的 pair，
        # 恰好会把这 4 个全部排除。
        n_action = len(re.findall(r"^\s*(?:enter|exit|during)\s+", text, re.M))
        n_enter = len(re.findall(r"^\s*enter\s+", text, re.M))
        n_exit = len(re.findall(r"^\s*exit\s+", text, re.M))
        n_during = len(re.findall(r"^\s*during\s+", text, re.M))
        n_unspec = len(re.findall(r"UnspecifiedInitial", text))
        n_finalwait = len(re.findall(r"FinalWaittr_", text))
        rows.append({
            "case": case, "nl_group": group_of.get(case, "?"), "states": len(states), "composites": len(composites),
            "depth": max(depths) if depths else 0, "events": len(events),
            "vars": len(variables), "transitions": n_tr, "eventless": n_eventless,
            "star": n_star, "guards": n_guard, "effects": n_effect,
            "actions": n_action, "enter": n_enter, "exit": n_exit, "during": n_during, "unspec_initial": n_unspec,
            "final_wait": n_finalwait, "exclusions": len(excl), "bytes": len(text),
        })
    pathlib.Path("/tmp/fcstm_stats.json").write_text(json.dumps(rows, indent=2))
    print(f"wrote {len(rows)} rows -> /tmp/fcstm_stats.json")


if __name__ == "__main__":
    main()
