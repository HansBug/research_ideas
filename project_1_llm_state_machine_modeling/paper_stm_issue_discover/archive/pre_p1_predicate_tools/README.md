# Pre-P1 Predicate Replay Tools

These files retain the historical replay tools, their command wrappers, and
dedicated tests from commit `4f74a2b60`. They use the
`four-family-19-core.v1` compiler and are outside the current method package.
They were moved with `git mv`; their source bytes and relative imports were
preserved. The nested paths show their original locations within the paper
workspace. Mixed test files still have their full historical versions at that
commit; their current copies test only the current method.

`tests/reproducibility/` also preserves the original predicate-gold execution
and release-refactor tests. Current tests retain the read-only contracts and
check that historical execution/refactor gates reject a mismatched registry.

## Reproduce the Historical Tools

Use a separate checkout of the recorded commit so its compiler, registry,
relative path anchors, fixture data, and imports agree. The archived files are
records, not entry points against the current twelve-predicate package.

```bash
git worktree add --detach /tmp/paper1-pre-p1-replay 4f74a2b60
cd /tmp/paper1-pre-p1-replay
git submodule update --init --recursive
python -m venv venv
venv/bin/pip install -e ./pyfcstm
venv/bin/pip install -e project_1_llm_state_machine_modeling/paper_stm_issue_discover/method
venv/bin/python -m paper_stm_method.tools.replay --help
```

Supply the original saved method run and input closure using that command's
arguments. Replay is provider-free. No `.env` or provider credential is needed.
Original raw runs may be git-ignored and must be available separately; their
manifest identifies the required input and registry hashes. Validate in that
checkout with the original `pipeline/evidence_discovery/tests/test_provider_free_replay.py`
and `test_primary_route_replay.py`, using the paper workspace on `PYTHONPATH`.
Do not run these tools over v61 to replace its frozen results.

For label-only statistics on existing data, use
`scripts/evaluation/predicate_id_view.py` in the current paper workspace.
It imports evaluation code only, preserves original IDs and counts, and does
not invoke any historical or current method backend.
