"""A hold-out that has been written about is no longer one, so this fails when that happens.

The set is frozen in `holdout.json`. Its purity is not a claim about the past -- it is a
property that has to keep holding, and every future commit is a chance to break it: a gate whose
docstring cites `pair 0010`, a test fixture named `0008-claude`, a commit body explaining that
some rule exists because of `EIS-0014-02`. Each of those silently converts the hold-out back
into a tuned cell, and nothing else in the repository would notice.

Run it directly (`python -m pytest test_holdout_stays_clean.py`) or via the eval suite.
"""

from __future__ import annotations

import collections
import json

import pytest
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import holdout  # noqa: E402

FROZEN = json.loads((HERE / "holdout.json").read_text())


#: ## ⛔ hold-out **数据侧**纪律已退役（带划分被用户裁定废止）
#:
#: 下面两条测试守护的是「留出 pair 不得在改 `src/` 的 commit 里被点名」。用户已裁定废止 hold-out 带划分
#: （理由：它服务泛化性声明，而本研究的贡献是**从真实模型归纳问题类型与判定能力**，语料即研究对象；
#: 且它把分母掐死到 2 条）。**没有留出集了，所以它们守护的对象不存在。**
#:
#: 保留它们的后果：任何触及 `src/` 且提到格集的 commit 都被拦 —— 而那是大多数 commit。
#:
#: ### 为什么这不是「因为不方便就删检查」
#:
#: 判据是**这个决定是否早于我遇到不方便**。它是的：`RULE_PROVENANCE.md` 早已写明「hold-out 带划分已按
#: 用户裁定废止，但**规则侧**纪律不随之废止」，写那句话时我没有任何 push 被拦。所以退役是执行一个已作出
#: 并已记录的决定。
#:
#: ### 仍然生效的是另一件事
#:
#:     数据侧（已退役）  留出集不参与规则编写      ← 前提消失
#:     规则侧（生效）    规则编写者不见结果        ← RULE_PROVENANCE.md，公理表盲态推导即此
#:
#: 两者是不同的纪律。**废止前者不放宽后者** —— 用户保留的红线正是「不得把答案或不该可见的信息喂进去」，
#: 而照着漏检清单写规则是喂答案的一种形态。
#:
#: 本文件其余 24 项检查（burn 记账一致性、matcher 未变窄、ruling 不悬空等）**保留** ——
#: 它们守护的是台账记账的自一致性，与带划分无关。
_HOLDOUT_DATA_SIDE_RETIRED = True


@pytest.mark.skipif(
    _HOLDOUT_DATA_SIDE_RETIRED,
    reason="hold-out 数据侧纪律已退役：带划分被用户裁定废止，留出集不再存在",
)
def test_verify_does_not_recompute_the_candidate_pool() -> None:
    """The first version asserted `compute()["holdout"] == frozen`, and running the hold-out
    destroyed it: rule 2 (never run) then excludes the very pairs that were frozen, so the
    recomputed set is necessarily different and the check is permanently red -- with the same
    message a real burn would produce. `--verify` must therefore pass on a tree where the
    hold-out has been run, and `compute()` must be allowed to differ from the frozen set.
    """
    assert holdout.main(["--verify"]) == 0
    recomputed = holdout.compute()["holdout"]
    # Not an equality assertion in either direction -- only that a difference is tolerated.
    assert isinstance(recomputed, list)


@pytest.mark.skipif(
    _HOLDOUT_DATA_SIDE_RETIRED,
    reason="hold-out 数据侧纪律已退役：带划分被用户裁定废止，留出集不再存在",
)
def test_no_naming_of_a_held_out_pair_goes_unaccounted() -> None:
    """The absolute form of this ran out of room, and weakening it needed saying out loud.

    It used to assert that no held-out pair is named anywhere. That is the right invariant while
    a hold-out is untouched, and it is unreachable once record-level burning exists: recording
    that `EIS-0032-02` is reportable names `0032`, so the absolute form goes red on correct
    bookkeeping. What replaces it is not weaker in the direction that matters -- every naming
    site must be claimed by a burn or a ruling -- but it is weaker in one direction, and that
    is exactly why `--verify` is the gate and this test only checks it agrees.
    """
    assert holdout.main(["--verify"]) == 0


def test_a_ruling_for_a_pair_nobody_names_is_a_matcher_regression() -> None:
    """Dead bookkeeping is how a broken detector looks from the inside.

    Six recurrences of the enumeration mistake all presented the same way: the rules stayed on
    the page, the matcher stopped finding what they were written for, and everything went green.
    A burn or ruling whose pair the detector no longer reports as named means either the entry
    is stale or the matcher has narrowed again -- and the second reading is the one this
    repository keeps landing on.
    """
    # The same two texts `--verify` reads. `tainted_pairs` covers source and tests only, so
    # using it here would make this test disagree with the gate about what "named" means -- a
    # second definition of the fact, which is the shape of the bug it is looking for.
    source, commits = holdout._source_and_test_text(), holdout._commit_text()
    named = {
        pair
        for pair in holdout.compute()["candidates"] + _frozen()["holdout"]
        if holdout._naming_in_prose(pair).search(source)
        or holdout._naming_in_prose(pair).search(commits)
    }
    d = _frozen()
    claimed = set(d.get("motive_adjudicated") or {})
    detail = {x["pair"]: x["record_ids"] for x in d["holdout_detail"]}
    for record in d.get("burned_records") or {}:
        for pair, records in detail.items():
            if record in records:
                claimed.add(pair)
    orphans = sorted(claimed - named)
    assert not orphans, (
        f"burns or rulings exist for {orphans}, which the detector no longer reports as named. "
        "Either the entries are stale or the matcher has narrowed -- check `_naming_in_prose` "
        "against the measurement in its docstring before touching the frozen set."
    )


def test_the_four_historical_cells_are_all_excluded() -> None:
    """0000/0006/0029/0050 are what eighteen generations were tuned against."""
    assert set(FROZEN["holdout"]).isdisjoint({"0000", "0006", "0029", "0050"})


def test_no_held_out_pair_shares_an_nl_group_with_a_tuned_cell() -> None:
    """Same group means the same requirement text and reference model.

    A rule written against one member acts on every member, which a pair-id spelling check
    cannot see. The first freeze held two pairs sharing NL08 and NL05 with the tuned cells.
    """
    assert set(FROZEN["holdout_groups"].values()).isdisjoint(set(FROZEN["excluded_tuned_groups"]))


def test_no_nl_group_dominates_the_holdout() -> None:
    counts = collections.Counter(FROZEN["holdout_groups"].values())
    assert max(counts.values()) <= FROZEN["max_per_group"]
    assert len(counts) >= 5, f"only {len(counts)} distinct NL groups: {dict(counts)}"


def test_no_held_out_pair_was_already_run_and_published() -> None:
    """`runs/` is not the only run ledger; two pairs' results were published in a PR comment."""
    assert set(FROZEN["holdout"]).isdisjoint(set(FROZEN["previously_run_and_published"]))
    assert set(FROZEN["holdout"]).isdisjoint(set(FROZEN["run_seen_in_runs_dir"]))


def test_layers_too_thin_to_report_are_marked_as_such() -> None:
    """Reporting `@k` per layer off 2 records is reporting a Bernoulli draw as a percentage."""
    reportable = FROZEN["layers_reportable_at_k"]
    for layer, ok in reportable.items():
        n = FROZEN["holdout_layer_coverage"].get(layer, 0)
        assert ok == (n >= 4), f"{layer}: {n} records but reportable={ok}"
    assert any(reportable.values()), "no layer has enough records to report at all"


def test_an_undersized_freeze_is_refused() -> None:
    """An empty hold-out written to disk looks exactly like a valid one, and divides by zero."""
    assert FROZEN["holdout_judgeable_total"] >= 20
    assert len(FROZEN["holdout"]) >= 5


def test_every_layer_is_represented() -> None:
    """A hold-out covering one defect layer would measure one thing and be reported as four."""
    assert set(FROZEN["holdout_layer_coverage"]) == set(holdout.LAYERS)


def test_the_denominator_is_stated_and_non_trivial() -> None:
    total = FROZEN["holdout_judgeable_total"]
    assert total == sum(row["judgeable_records"] for row in FROZEN["holdout_detail"])
    assert total >= 2 * len(FROZEN["holdout"])


def test_out_of_scope_records_are_excluded_not_counted_as_misses() -> None:
    """paper1 is `M = (S, E, V, Tr, A)`; clocks, invariants and orthogonal regions are outside it.

    A record the closed vocabulary cannot state is unfindable by construction. Counting it as a
    miss reports a declared boundary as a capability gap -- which is the error CLAUDE.md's
    project_1 boundary section exists to prevent.
    """
    excluded = FROZEN["excluded_records_inside_holdout_pairs"]
    assert excluded, "expected at least one excluded record; the filter may have stopped working"
    counted = {rid for row in FROZEN["holdout_detail"] for rid in row["record_ids"]}
    assert counted.isdisjoint(set(excluded))


def test_the_freeze_refuses_to_be_overwritten() -> None:
    """`--freeze` twice must not silently redefine the set after results are in."""
    assert holdout.main(["--freeze"]) == 2


# --- v21：烧毁记账 ---


def _frozen() -> dict:
    return json.loads((HERE / "holdout.json").read_text(encoding="utf-8"))


def test_burned_and_reportable_partition_the_frozen_set() -> None:
    """Every frozen pair is either still usable for a capability claim or recorded as burned.

    A pair that is in neither would drop out of the report silently; one in both would put a
    co-evolved cell back into the capability band, which is the whole thing this accounting
    exists to prevent.
    """
    d = _frozen()
    assert set(d["burned"]) | set(d["reportable_holdout"]) == set(d["holdout"])
    assert not (set(d["burned"]) & set(d["reportable_holdout"]))


def test_the_reportable_denominator_adds_up() -> None:
    """The shrunken denominator has to be derivable, not asserted.

    23 records became 9 by removing three pairs; if that arithmetic is wrong the capability
    claim is computed over a denominator nobody can reproduce.
    """
    d = _frozen()
    detail = {x["pair"]: x for x in d["holdout_detail"]}
    burned_records = d.get("burned_records") or {}
    # Record level, not cell level. A pair can be partially burned: a rule designed against one
    # of its ledger records leaves the others usable, and throwing the whole cell away would
    # shrink the denominator further than the contamination warrants.
    expected = [
        record
        for pair in d["reportable_holdout"]
        for record in detail[pair]["record_ids"]
        if record not in burned_records
    ]
    assert d["reportable_judgeable_total"] == len(expected)
    assert d["reportable_records"] == sorted(expected)


def test_a_naming_hit_needs_either_a_burn_or_a_ruling() -> None:
    """Every named reportable pair is accounted for, one way or the other.

    Naming demands an adjudication, not an automatic verdict: recording that a pair is
    reportable names it too, so auto-excluding on a spelling match would empty the set. What
    must not exist is a naming nobody ruled on.
    """
    d = _frozen()
    burned_records = d.get("burned_records") or {}
    adjudicated = d.get("motive_adjudicated") or {}
    detail = {x["pair"]: x for x in d["holdout_detail"]}
    for pair in d["reportable_holdout"]:
        has_burn = any(r in burned_records for r in detail[pair]["record_ids"])
        ruling = adjudicated.get(pair)
        assert has_burn or (
            isinstance(ruling, dict) and ruling.get("verdict") and ruling.get("reasoning")
        ), f"{pair} is reportable but neither partially burned nor adjudicated"


def test_a_burn_only_accounts_for_the_sites_it_names() -> None:
    """The negative control for the rubber stamp, because the stamp passed every positive one.

    Reconciliation used to ask whether *any* record of the pair was burned. `0047` had
    `EIS-0047-02` burned for a commit-body naming, so a second, unrelated naming of `0047` in
    the coactivity gate -- targeting `EIS-0047-01`, for a different rule, in a different
    round -- was waved through. Two real contaminations entered that way.

    So every burn declares `named_at`, every ruling declares `covers`, and a site nobody
    claimed is a failure. Asserted here by removing coverage and requiring the failure, since
    the defect was invisible to every assertion that only checked the happy path.
    """
    d = _frozen()
    detail = {x["pair"]: x["record_ids"] for x in d["holdout_detail"]}
    for pair in d["reportable_holdout"]:
        sites = set()
        for record in detail[pair]:
            entry = (d.get("burned_records") or {}).get(record)
            if isinstance(entry, dict):
                sites.update(entry.get("named_at") or ())
        ruling = (d.get("motive_adjudicated") or {}).get(pair)
        if isinstance(ruling, dict):
            sites.update(ruling.get("covers") or ())
        assert sites, f"{pair} is named somewhere but no burn or ruling says where"
        # A burn may legitimately claim no location -- `EIS-0032-01`'s mechanism is motive, from
        # an analysis document, and the rule's own commit body names the pair zero times. What
        # must not happen is a *pair* with namings and nothing claiming any of them, and the
        # empty `named_at` there is annotated rather than left to look like an omission.
        for location in sites:
            assert location.startswith(("commit:", "src:")), location


def test_every_burn_says_where_it_was_named() -> None:
    """`named_at` is what reconciliation reads, so a burn without it silently covers nothing."""
    for record, entry in (_frozen().get("burned_records") or {}).items():
        assert entry.get("evidence"), f"{record} has no evidence"
        assert entry.get("since_commit"), f"{record} has no commit"
        # An empty `named_at` is legitimate and must be annotated, not merely empty. `EIS-0032-01`
        # burns on motive from an analysis document while the rule's own commit body names the
        # pair zero times -- and the previous version papered over that by recording the category
        # `commit_body`, which then silently covered a different commit's directional claim.
        assert entry.get("named_at") or entry.get("named_at_note"), (
            f"{record} claims no location and does not say why; an unexplained empty "
            "`named_at` is indistinguishable from forgetting to fill it in"
        )


def test_every_claimed_location_carries_a_reason() -> None:
    """A `covers` entry without a reason is a location waved past, which is the whole failure.

    Three rounds of rubber stamps: per-pair (`any` record burned), then per-site-name (one
    `commit_body` entry absorbing every commit body), now per-location. The remaining way to
    stamp is to list a location and say nothing about it, so the reason is required and the
    detector's own spelling of the location has to match.
    """
    d = _frozen()
    for pair, ruling in (d.get("motive_adjudicated") or {}).items():
        reasons = ruling.get("covers_reasons") or {}
        for location in ruling.get("covers") or ():
            assert reasons.get(location), f"{pair} claims {location} with no reason"
            assert len(reasons[location]) > 40, f"{pair}/{location} reason is too thin to audit"


def test_the_detector_reports_locations_not_categories() -> None:
    """Categories are claimable once and cover everything after; locations are not.

    Measured on the version this replaced: `EIS-0032-01`'s burn recorded
    `named_at: ["commit_body"]` against `23315498`, whose body names `0032` zero times -- and
    that mislabelled category then absorbed `0eb36a06`, which names it with a directional
    expectation about other scopes entirely. Nothing had ruled on it.
    """
    d = _frozen()
    claimed = set()
    for entry in (d.get("burned_records") or {}).values():
        claimed.update(entry.get("named_at") or ())
    for ruling in (d.get("motive_adjudicated") or {}).values():
        claimed.update(ruling.get("covers") or ())
    assert claimed, "nothing is claimed anywhere"
    for location in claimed:
        assert location.startswith(("commit:", "src:")), (
            f"{location!r} is a category, not a location. A category is claimed once and then "
            "covers every future naming inside it, which is the stamp this replaced."
        )


def test_a_prose_only_commit_is_auto_classified_but_a_real_change_is_not() -> None:
    """The negative control for the auto-classifier, which exists to keep the list bounded.

    Per-location accounting had one unwanted consequence: recording that a pair is reportable
    names it, so every bookkeeping commit became a location needing a ruling and `--verify` went
    red the moment the accounting was written. Going back to category names would be the stamp
    this replaced three times, so the classifier reads the *diff* instead: rules that reach the
    model live under the pipeline's `src/`, and a commit whose parsed trees there are unchanged
    cannot have authored one.

    The control that matters is the second half -- a commit that really did change behaviour must
    still demand a ruling. Checked on real commits: `a8123003` edited a `capability.py` docstring
    and nothing else, `02539b82` changed predicate and node behaviour.
    """
    prose_only, why = holdout._behaviour_changed_in_pipeline("a8123003")
    assert prose_only is False, why
    assert "docstring" in why or "no file" in why, why

    real_change, why = holdout._behaviour_changed_in_pipeline("02539b82")
    assert real_change is True, why
    assert "behaviour" in why, why


def test_the_classifier_fails_toward_demanding_a_ruling() -> None:
    """An unreadable commit must not be waved through.

    Getting a spurious ruling request costs a paragraph; missing one costs a capability claim,
    so every error path returns "behaviour changed" and lands the location in the unaccounted
    list rather than in the auto-classified one.
    """
    changed, why = holdout._behaviour_changed_in_pipeline("0000000")
    assert changed is True, why


def test_docstring_stripping_does_not_hide_a_code_change() -> None:
    """The tree comparison must be blind to prose and nothing else."""
    same = holdout._tree_without_docstrings('def f():\n    """one."""\n    return 1\n')
    other = holdout._tree_without_docstrings('def f():\n    """two, at length."""\n    return 1\n')
    assert same == other
    changed = holdout._tree_without_docstrings('def f():\n    """one."""\n    return 2\n')
    assert same != changed


def test_no_layer_reaches_the_reporting_threshold_after_record_level_burns() -> None:
    """Records the fact that v22 has no capability-claim band, so it cannot be discovered later.

    Two records remain, one each in `nl_named` / `nl_contradiction`; `wellformedness` and
    `over_specification` are both empty. The threshold is four. Writing this as
    a test rather than only as prose means a later change that quietly re-inflates the
    denominator has to argue with it.

    It was six until per-site reconciliation found two more, then four until per-location
    reconciliation found `EIS-0035-01`. Every one was free in scientific terms -- no layer reached
    the threshold at six either -- which is the reason to record them rather than argue about them.

    ⚠️ 又少一条：v23 写 `incumbent considered:` 约束时，实例表用了 `EIS-0032-02` primary 绑定末段
    的元素名，且给出了真值判定 —— prompt 侧自查时修了，测试 docstring 里的同一组名字漏了，由发布前
    的公平性 review 抓出。**一处泄漏的修复要覆盖它的全部副本。**

    Of the two that remain, `EIS-0047-03` was once thought structurally unreachable (see the
    pre-registration: both its encodings bind `source="[*]"` with a trigger the power-on word
    list does not admit, so `initialization_anchored_findings` refuses them). So the honest count
    of clean *and* reachable records is **two**.
    """
    d = _frozen()
    assert d["reportable_judgeable_total"] == 2
    assert d["reportable_layer_coverage"] == {
        "nl_named": 1,
        "nl_contradiction": 1,
    }
    # `over_specification` 在 v23 归零：`EIS-0032-02` 因 `incumbent considered:` 约束的实例表
    # 用了它 primary 末段的元素名（`IdleState` 在 60 份模型里只出现在那一个 pair）而烧毁。
    # 与 `wellformedness` 一样记为**缺键**而非零，好让后续任何重新充气都必须显式加回来。
    assert "over_specification" not in d["reportable_layer_coverage"]
    # `wellformedness` reached zero when `EIS-0035-01` burned on an element-name leak that no
    # id-based matcher can see: a gate test binds `<root>.DoorShut`, which is that record's own
    # primary shape, and the gate's commit says it was calibrated on twelve root-bound ledger
    # assertions. Recorded as an absent key rather than a zero so a later re-inflation has to
    # add it back deliberately.
    assert "wellformedness" not in d["reportable_layer_coverage"]
    assert not any(d["reportable_layers_at_k"].values()), d["reportable_layer_coverage"]


def test_every_burn_records_its_mechanism_and_evidence() -> None:
    """A burn with no stated reason cannot be checked, and would read as an excuse."""
    for pair, entry in _frozen()["burned"].items():
        assert entry["mechanism"] in {"motive", "nl_group"}, pair
        assert entry["evidence"].strip(), pair
        assert entry["since_commit"].strip(), pair
        assert entry["records"], pair


def test_verify_still_fails_on_a_burn_that_was_not_recorded() -> None:
    """Otherwise a green suite cannot be told from a detector that stopped working.

    Reconciling against `burned` makes the check pass on known burns by design, so the
    detector needs a positive control: name a reportable pair and `--verify` must refuse.
    """
    import subprocess

    frozen = HERE / "holdout.json"
    original = frozen.read_text(encoding="utf-8")
    d = json.loads(original)
    # `0018` is the one pair known to match the enumerating detector (`EIS-0018-` and
    # `pair 0018` both appear in commit bodies). Un-recording its burn is therefore a
    # faithful simulation of a burn nobody wrote down, and the check must catch it.
    victim = "0018"
    assert victim in d["burned"], "the positive control needs a pair that is actually named"
    d["burned"].pop(victim)
    d["reportable_holdout"] = sorted(set(d["reportable_holdout"]) | {victim})
    try:
        frozen.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
        done = subprocess.run(
            [sys.executable, str(HERE / "holdout.py"), "--verify"],
            capture_output=True, text=True, cwd=str(HERE),
        )
        assert done.returncode == 1, (done.returncode, done.stdout, done.stderr)
        assert victim in done.stderr
    finally:
        frozen.write_text(original)
