"""Continue exhausted judge nodes from their recorded conversation, without resampling siblings."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import uuid

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain.agents.structured_output import StructuredOutputValidationError, _parse_with_schema

from paper_stm_judge.cli import _code_commit
from paper_stm_judge.models import AdapterAudit, UnifiedJudgeInput
from paper_stm_judge.runner import judge_pair
from paper_stm_method.orchestration.runner import _model_config_hash
from utils.agent.runtime import _structured_output_repair_message
from utils.artifact_io import write_json
from utils.structured_runtime import (
    PublicStructuredRuntime, StructuredCallOutcome, StructuredContextBudget, _usage_rows,
)


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def records(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def history(rows, schema, prompt, system):
    """Rebuild typed tool messages and verify every recorded correction verbatim."""
    context = rows[0]
    assert context['input_text'] == prompt and context['system_prompt'] == system
    assert context['output_schema'] == schema.model_json_schema()
    assert not context['pages'], 'Resume with external context is not supported'
    calls = sorted((r for r in rows if 'rendered_input_projection' in r), key=lambda r: r['turn'])
    actions = sorted((r for r in rows if r.get('kind') == 'structured'), key=lambda r: r['turn'])
    assert len(calls) == len(actions) == 6
    messages = [HumanMessage(content=prompt)]
    for index, (call, action) in enumerate(zip(calls, actions, strict=True)):
        assert call['turn'] == action['turn']
        recorded = call['rendered_input_projection']['messages']
        rebuilt = [m.content for m in messages]
        assert recorded == rebuilt, ('history mismatch', call['turn'], [len(x) for x in recorded], [len(x) for x in rebuilt])
        ai = AIMessage(content='', tool_calls=[{
            'name': action['name'], 'args': action['arguments'], 'id': action['tool_call_id'],
        }])
        try:
            _parse_with_schema(schema, 'pydantic', action['arguments'])
        except ValueError as exc:
            error = StructuredOutputValidationError(action['name'], exc, ai)
            feedback = _structured_output_repair_message(error)
        else:
            raise ValueError('Saved failed output unexpectedly validates')
        if index + 1 < len(calls):
            # Keep provider-visible original feedback, including repr key order.
            feedback = calls[index + 1]['rendered_input_projection']['messages'][-1]
        elif action['arguments'] == actions[index - 1]['arguments']:
            feedback = calls[index]['rendered_input_projection']['messages'][-1]
        messages.extend([ai, ToolMessage(content=feedback, tool_call_id=action['tool_call_id'], name=action['name'])])
    return messages


class ContinueRuntime(PublicStructuredRuntime):
    resume_rows = None

    async def _arun_app(self, app, prompt, **options):
        if self.resume_rows is not None:
            options['resume_messages'] = history(self.resume_rows, app.spec.output_schema, prompt, app.spec.system_prompt)
        return await super()._arun_app(app, prompt, **options)


class ResumeStages:
    def __init__(self, failure, source, destination, executor, allow_live):
        self.manifest = read(source / 'run_manifest.json')
        self.profile = self.manifest['model_profile']
        from utils.llm import load_llm_registry
        self.config = load_llm_registry().require(self.profile)
        assert _model_config_hash(self.profile) == 'sha256:05e7d948fd676e677f49a039ea75f0356f5aa005bbc2db89f5e72bf6ff4e446a'
        self.destination, self.executor = destination, executor
        self.allow_live = allow_live
        self.saved, self.reused, self.continued = {}, {}, {}
        self.parent_failures = set()
        self.old_receipts = {}
        for receipt in failure['call_receipts']:
            paths = [Path(p) for p in receipt['artifact_paths'] if p.endswith('/result.json')]
            assert len(paths) == 1
            artifact = '/'.join(paths[0].parts[-5:-2])
            self.old_receipts[artifact] = receipt
            if receipt['status'] != 'success' and len(receipt['report_ids']) > 1:
                self.parent_failures.add(artifact)
        # A sibling may have finished even when the runner raised before appending its receipt.
        for path in (source / 'llm').glob(f"**/{failure['pair_id']}/round-{failure['round']}/**/result.json"):
            artifact = '/'.join(path.parts[-5:-2])
            assert artifact not in self.saved, 'Multiple prior attempts need explicit reconciliation'
            self.saved[artifact] = path

    def call_many(self, calls):
        futures = [self.executor.submit(self.call, **call) for call in calls]
        return tuple(future.result() for future in futures)

    def call(self, **call):
        artifact = call['artifact_id']
        path = self.saved.get(artifact)
        rows = None
        if path is not None:
            result = read(path)
            rows = records(path.with_name('audit.jsonl'))
            context = rows[0]
            assert context['input_text'] == call['prompt']
            assert context['system_prompt'] == call['system_prompt']
            assert context['output_schema'] == call['schema'].model_json_schema()
            assert result['model'] == self.config.model and result['real_llm']
            assert result['max_output_tokens'] == call['max_output_tokens']
            if result['status'] == 'success' or artifact in self.parent_failures:
                self.reused[artifact] = {'path': str(path), 'sha256': digest(path), 'status': result['status']}
                receipt = self.old_receipts.get(artifact)
                attempts = ([json.loads(r['raw_attempt_json']) for r in receipt['retries']] if receipt else [{
                    'outer_attempt': 1, 'status': result['status'], 'provider_error': False,
                    'error': result['error'], 'audit_path': str(path.with_name('audit.jsonl')), 'result_path': str(path),
                }])
                return StructuredCallOutcome(
                    kind=call['kind'], status=result['status'], result=result,
                    response=call['schema'].model_validate(result['output']) if result['status'] == 'success' else None,
                    attempts=attempts, usage=_usage_rows(result, outer_attempt=1),
                    cost={'total_usd': receipt['cost_usd'] if receipt else None, 'eligible': receipt['cost_eligible'] if receipt else False},
                    real_llm=True,
                    context_budget=StructuredContextBudget(
                        mode='structured_llm', projection_version='judge-exact-resume.v1',
                        prompt_characters=len(call['prompt']), estimated_prompt_tokens=(len(call['prompt'])+3)//4,
                        provider_input_tokens=sum(r.get('input_tokens') or 0 for r in _usage_rows(result)),
                        context_window_tokens=result['context_window_tokens'], max_output_tokens=result['max_output_tokens'],
                        truncation_applied=False, projection_decision='Replay exact prior outcome, including failed parent split.',
                        reason='No repeated provider call.', basis='Original prompt, schema and result verified.'),
                    reason='Exact prior stage replay.', basis='Original result retained by hash.')
            history(rows, call['schema'], call['prompt'], call['system_prompt'])
            self.continued[artifact] = {'path': str(path), 'sha256': digest(path), 'prior_turns': 6, 'additional_turn_limit': 6}
        if not self.allow_live:
            raise RuntimeError('PREFLIGHT_READY: ' + artifact)
        live = ContinueRuntime(self.profile, self.destination / 'llm' / uuid.uuid4().hex,
                               transport_retries=self.manifest['transport_retries'], streaming=True)
        try:
            live.resume_rows = rows
            return live.call(**call)
        finally:
            live.close()


def recover(path, destination, executor, allow_live):
    failure = read(path)
    manifest = read(path.parent.parent / 'run_manifest.json')
    assert manifest['model_profile'] == 'gpt-5.6-luna'
    assert manifest['validity_readings'] == 2 and manifest['validity_aggregation'] == 'arbitration'
    assert manifest['k_closure'] == 'relation_first' and manifest['validity_arbitration_trigger'] == 'any'
    run_id = uuid.uuid4().hex
    output = destination / run_id
    runtime = ResumeStages(failure, path.parent.parent, output, executor, allow_live)
    judge_input = UnifiedJudgeInput.model_validate(read(failure['input_path']))
    adapter = AdapterAudit.model_validate(read(failure['adapter_audit_path']))
    assert 'sha256:' + digest(adapter.source_path) == adapter.source_hash
    code_commit = _code_commit() if allow_live else 'offline-preflight'
    audit = {'schema': 'a4.judge-schema-continuation.v1', 'run_id': run_id,
             'source_failure': str(path), 'source_failure_sha256': digest(path),
             'workers_global_max': 8, 'additional_turn_limit': 6, 'code_commit': code_commit,
             'authorization': 'User requested continuation after disclosure of six-turn schema exhaustion.',
             'prior_call_receipts': failure['call_receipts']}
    write_json(output / 'run_manifest.json', audit)
    try:
        result = judge_pair(run_id=run_id, round_no=failure['round'], judge_input=judge_input,
                            adapter_audit=adapter, runtime=runtime, judge_code_commit=code_commit)
    except Exception as exc:
        if not allow_live and str(exc).startswith('PREFLIGHT_READY:'):
            print(json.dumps({'pair': failure['pair_id'], 'preflight': 'passed', 'continued': runtime.continued}), flush=True)
            return
        write_json(output / 'continuation_failure.json', {'type': type(exc).__name__, 'message': str(exc),
                   'call_receipts': [r.model_dump(mode='json') for r in getattr(exc, 'call_receipts', ())]})
        raise
    else:
        payload = result.model_dump(mode='json')
        write_json(output / 'pairs' / f"{failure['pair_id']}.json", payload)
        print(json.dumps({'pair': failure['pair_id'], 'round': failure['round'], 'status': payload['status'], 'output': str(output)}), flush=True)
    finally:
        audit.update(reused=runtime.reused, continued=runtime.continued)
        write_json(output / 'run_manifest.json', audit)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--failure', type=Path, action='append', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--allow-live', action='store_true')
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=8) as calls, ThreadPoolExecutor(max_workers=3) as cells:
        futures = [cells.submit(recover, p, args.output_dir, calls, args.allow_live) for p in args.failure]
        for future in futures:
            future.result()


if __name__ == '__main__':
    main()
