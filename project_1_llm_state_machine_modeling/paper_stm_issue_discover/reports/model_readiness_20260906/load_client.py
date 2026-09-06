"""Explicit, synthetic OpenAI-compatible serving probe; never loads model weights."""

import argparse
import concurrent.futures
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
import tiktoken


SCHEMA = {
    "type": "object",
    "properties": {
        "issue": {"type": "string"},
        "source_transition": {"type": "string"},
        "missing_guard": {"type": "string"},
        "counterexample": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["issue", "source_transition", "missing_guard", "counterexample"],
    "additionalProperties": False,
}
TASK = (
    "Requirements: a pump may start only when the safety interlock is closed. "
    "It must stop when an emergency event occurs. Source transitions: "
    "Idle --> Running : start; Running --> Idle : emergency. "
    "Identify the concrete issue and a counterexample. Do not invent extra requirements. "
    "Return only concise JSON with issue, source_transition, missing_guard, counterexample. "
    "The first three fields must be strings. counterexample must be an ARRAY of strings, "
    "for example [\"initial condition\", \"event\", \"resulting state\"], never one string. "
    "Keep each string below 80 characters and use at most four counterexample steps. "
    "Fill every field with concrete task-specific content. Never use ellipses or placeholders."
)


def schema_valid(text):
    try:
        row = json.loads(text)
        return (
            isinstance(row, dict) and set(row) == set(SCHEMA["properties"])
            and all(isinstance(row[k], str) for k in SCHEMA["required"][:-1])
            and isinstance(row["counterexample"], list)
            and all(isinstance(x, str) for x in row["counterexample"])
        )
    except (ValueError, TypeError):
        return False


def percentile(values, q):
    return sorted(values)[max(0, math.ceil(len(values) * q) - 1)] if values else None


def input_text(args):
    enc = tiktoken.get_encoding('cl100k_base')
    padding_tokens = enc.encode(' '.join(
        f'Background signal {i}: telemetry is informational; no control transition.'
        for i in range(args.input_tokens)))
    size = max(0, args.input_tokens - len(enc.encode(TASK)) - 20)
    for _ in range(8):
        padding = enc.decode(padding_tokens[:size])
        text = 'Background context:\n' + padding + '\nAuthoritative task:\n' + TASK
        if not args.tokenize_path:
            return text, None
        messages = [{'role': 'user', 'content': 'Independent request 999999.\n' + text}]
        if args.system_prompt:
            messages.insert(0, {'role': 'system', 'content': args.system_prompt})
        response = requests.post(args.endpoint.removesuffix('/v1') + args.tokenize_path,
                                 json={'model': args.model, 'messages': messages,
                                     'chat_template_kwargs': {'enable_thinking': args.thinking}},
                                 timeout=(15, 120))
        response.raise_for_status()
        data = response.json()
        count = data.get('count')
        if count is None:
            tokens = data['tokens']
            count = len(tokens[0] if tokens and isinstance(tokens[0], list) else tokens)
        if args.input_tokens <= count <= args.input_tokens + max(64, args.input_tokens // 200):
            return text, count
        size = max(0, round(size * args.input_tokens / max(1, count)) + 16)
    raise ValueError('remote tokenizer could not calibrate the requested input size')


def request_one(args, text, index, warmup=False):
    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": f"Independent request {index}.\n{text}"}],
        "max_tokens": args.output_tokens, "temperature": 1.0 if args.thinking else 0.7,
        "top_p": 0.95 if args.thinking else 0.8,
        "stream": True, "stream_options": {"include_usage": True},
        "chat_template_kwargs": {"enable_thinking": args.thinking},
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "PumpIssue", "strict": True, "schema": SCHEMA}},
    }
    if args.system_prompt:
        payload['messages'].insert(0, {'role': 'system', 'content': args.system_prompt})
    if args.extra_body:
        payload.update(json.loads(args.extra_body))
    if args.tool_call:
        payload.pop('response_format', None)
        payload['tools'] = [{'type': 'function', 'function': {
            'name': 'PumpIssue', 'description': 'Report the concrete requirement violation.',
            'parameters': SCHEMA}}]
        payload['tool_choice'] = {'type': 'function', 'function': {'name': 'PumpIssue'}}
    row = {"index": index, "warmup": warmup, "payload": payload,
           "at": datetime.now(timezone.utc).isoformat(), "events": []}
    started = time.perf_counter()
    content, reasoning, tool_arguments, timestamps = [], [], [], []
    tool_names = set()
    try:
        with requests.post(args.endpoint.rstrip('/') + '/chat/completions',
                           json=payload, stream=True, timeout=(15, args.timeout)) as response:
            row['http_status'] = response.status_code
            response.raise_for_status()
            for line in response.iter_lines(chunk_size=1):
                if time.perf_counter() - started > args.timeout * 2:
                    raise TimeoutError('total request deadline exceeded')
                if not line.startswith(b'data: '):
                    continue
                data = line[6:]
                if data == b'[DONE]':
                    row['done_received'] = True
                    break
                event = json.loads(data)
                elapsed = time.perf_counter() - started
                row['events'].append({'seconds': elapsed, 'data': event})
                if event.get('usage'):
                    row['usage'] = event['usage']
                for choice in event.get('choices', []):
                    delta = choice.get('delta', {})
                    answer = delta.get('content') or ''
                    thought = delta.get('reasoning_content') or delta.get('reasoning') or ''
                    tool_output = False
                    for call in delta.get('tool_calls', []) or []:
                        function = call.get('function') or {}
                        if function.get('name'):
                            tool_names.add(function['name'])
                        fragment = function.get('arguments') or ''
                        tool_arguments.append(fragment)
                        tool_output = tool_output or bool(fragment)
                    if answer or thought or tool_output:
                        timestamps.append(elapsed)
                    content.append(answer)
                    reasoning.append(thought)
                    if choice.get('finish_reason'):
                        row['finish_reason'] = choice['finish_reason']
        candidate = ''.join(tool_arguments) if args.tool_call else ''.join(content)
        row['tool_arguments'] = candidate if args.tool_call else None
        row['schema_valid'] = schema_valid(candidate) and (not args.tool_call or tool_names == {'PumpIssue'})
        row['status'] = 'completed'
    except Exception as exc:
        # Error strings can contain private endpoints. Preserve type and HTTP status only.
        row.update(status='failed', error_type=type(exc).__name__, schema_valid=False)
    row.update(seconds=time.perf_counter() - started, content=''.join(content),
               reasoning=''.join(reasoning), ttft_seconds=timestamps[0] if timestamps else None,
               content_chunk_count=len(timestamps),
               inter_chunk_seconds=[b-a for a,b in zip(timestamps, timestamps[1:])])
    row['eligible'] = (row['status'] == 'completed' and row.get('done_received', False)
                       and row['schema_valid'] and row.get('finish_reason') == ('tool_calls' if args.tool_call else 'stop')
                       and bool(row.get('usage')))
    # A literal placeholder is a definite content failure, not a full semantic grader.
    row['placeholder_present'] = '...' in (row.get('tool_arguments') or row['content'])
    return row


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--endpoint', required=True)
    p.add_argument('--model', required=True)
    p.add_argument('--configuration', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--input-tokens', type=int, default=2000)
    p.add_argument('--output-tokens', type=int, default=256)
    p.add_argument('--concurrency', type=int, nargs='+', default=[1, 2, 4, 8, 16, 32])
    p.add_argument('--rounds', type=int, default=2)
    p.add_argument('--thinking', action='store_true')
    p.add_argument('--tokenize-path', choices=['/v1/tokenize', '/tokenize'])
    p.add_argument('--timeout', type=int, default=300)
    p.add_argument('--extra-body', help='Publisher-specific sampling controls as JSON')
    p.add_argument('--system-prompt', help='Explicit publisher reasoning instructions')
    p.add_argument('--tool-call', action='store_true', help='Use the PumpIssue function tool instead of response_format')
    args = p.parse_args()
    if urlparse(args.endpoint).hostname not in {'127.0.0.1', 'localhost'}:
        p.error('probe accepts only a loopback SSH-forwarded endpoint')
    if min(args.concurrency) < 1 or args.rounds < 2 or args.input_tokens < 200:
        p.error('positive concurrency, >=2 rounds and >=200 input tokens required')
    args.output.mkdir(parents=True, exist_ok=False)
    text, calibrated_count = input_text(args)
    manifest = {k: v for k,v in vars(args).items() if k not in {'endpoint','output'}}
    manifest.update(at=datetime.now(timezone.utc).isoformat(), formal_result_eligible=False,
                    endpoint_ref='SSH_FORWARDED_LOOPBACK',
                    input_estimator='remote_tokenizer' if args.tokenize_path else 'cl100k_base',
                    calibrated_input_tokens=calibrated_count,
                    prompt_sha256=hashlib.sha256(text.encode()).hexdigest(), prompt=text)
    (args.output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    summaries=[]
    with (args.output/'requests.jsonl').open('w') as log:
        for warm in range(2):
            row=request_one(args,text,-warm-1,True)
            log.write(json.dumps(row)+'\n'); log.flush()
        for concurrency in args.concurrency:
            batch_start=time.perf_counter()
            rows=[]
            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
                jobs=[pool.submit(request_one,args,text,concurrency*10000+i)
                      for i in range(concurrency*args.rounds)]
                for job in concurrent.futures.as_completed(jobs):
                    row=job.result(); row['concurrency']=concurrency; rows.append(row)
                    log.write(json.dumps(row)+'\n'); log.flush()
            wall=time.perf_counter()-batch_start
            summary={'configuration': args.configuration, 'concurrency': concurrency,
                     'requests': len(rows), 'eligible': sum(r['eligible'] for r in rows),
                     'transport_failed': sum(r['status']=='failed' for r in rows),
                     'truncated': sum(r.get('finish_reason')=='length' for r in rows),
                     'placeholder_present': sum(r['placeholder_present'] for r in rows),
                     'placeholder_free_eligible': sum(r['eligible'] and not r['placeholder_present'] for r in rows),
                     'schema_valid': sum(r['schema_valid'] for r in rows), 'wall_seconds': wall,
                     'output_tokens_per_second':sum(r.get('usage',{}).get('completion_tokens',0) for r in rows)/wall,
                     'requests_per_second':sum(r['eligible'] for r in rows)/wall,
                     'latency_p50':percentile([r['seconds'] for r in rows],0.5),
                     'latency_p95':percentile([r['seconds'] for r in rows],0.95),
                     'ttft_p95':percentile([r['ttft_seconds'] for r in rows if r['ttft_seconds'] is not None],0.95),
                     'input_tokens_min':min(r.get('usage',{}).get('prompt_tokens',0) for r in rows),
                     'input_tokens_max':max(r.get('usage',{}).get('prompt_tokens',0) for r in rows)}
            summaries.append(summary)
            (args.output/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
            print(json.dumps(summary),flush=True)


if __name__ == '__main__':
    assert schema_valid(json.dumps(dict(issue='guard',source_transition='start',missing_guard='closed',counterexample=['start'])))
    assert not schema_valid('{}')
    assert not schema_valid('{"issue":')
    assert percentile([4,1,2,3],0.95)==4
    from types import SimpleNamespace
    from unittest.mock import MagicMock, patch
    answer = json.dumps(dict(issue='guard', source_transition='start', missing_guard='closed', counterexample=['start']))
    events = [
        {'choices': [{'delta': {'tool_calls': [{'index': 0, 'function': {'name': 'PumpIssue', 'arguments': answer[:20]}}]}}]},
        {'choices': [{'delta': {'tool_calls': [{'index': 0, 'function': {'arguments': answer[20:]}}]}, 'finish_reason': 'tool_calls'}],
         'usage': {'prompt_tokens': 10, 'completion_tokens': 20}},
    ]
    response = MagicMock()
    response.__enter__.return_value = response
    response.status_code = 200
    response.iter_lines.return_value = iter([('data: ' + json.dumps(e)).encode() for e in events] + [b'data: [DONE]'])
    args = SimpleNamespace(model='mock', output_tokens=256, thinking=True, system_prompt='Reasoning strength: high',
                           extra_body=None, tool_call=True, endpoint='http://localhost/v1', timeout=2)
    with patch.object(requests, 'post', return_value=response):
        row = request_one(args, 'synthetic', 0)
    assert row['eligible'] and row['tool_arguments'] == answer and not row['placeholder_present']
    assert row['ttft_seconds'] is not None
    main()
