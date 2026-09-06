"""Offline verification of the sanitized E1 archive; never calls a provider."""
import hashlib
import json
import math
import zipfile
from pathlib import Path


def check(root):
    manifest = json.loads((root / 'manifest.json').read_text())
    assert manifest['formal_result_eligible'] is False
    checked = 0
    for name, members in manifest['archive_members_sha256'].items():
        with zipfile.ZipFile(root / name) as archive:
            assert set(archive.namelist()) == set(members)
            for member, digest in members.items():
                assert hashlib.sha256(archive.read(member)).hexdigest() == digest, member
                checked += 1
    summaries = json.loads((root / 'load_summary.json').read_text())
    with zipfile.ZipFile(root / 'sources.zip') as archive:
        for member in archive.namelist():
            if member.endswith('.json'):
                receipt = json.loads(archive.read(member))
                if isinstance(receipt, dict) and 'sha256' in receipt and 'retrieved_at' in receipt:
                    raw = archive.read(member.removesuffix('.json') + '.raw')
                    assert hashlib.sha256(raw).hexdigest() == receipt['sha256'], member
                    assert len(raw) == receipt['bytes'], member
    with zipfile.ZipFile(root / 'probes.zip') as archive:
        for sweep, batches in summaries.items():
            rows = [json.loads(line) for line in archive.read(
                f'results/{sweep}/requests.jsonl').splitlines() if line]
            for batch in batches:
                observations = [r for r in rows if not r['warmup']
                                and r['concurrency'] == batch['concurrency']]
                for field, expected in {
                    'requests': len(observations),
                    'eligible': sum(r['eligible'] for r in observations),
                    'transport_failed': sum(r['status'] == 'failed' for r in observations),
                    'truncated': sum(r.get('finish_reason') == 'length' for r in observations),
                    'schema_valid': sum(r['schema_valid'] for r in observations),
                    'input_tokens_min': min(r.get('usage', {}).get('prompt_tokens', 0) for r in observations),
                    'input_tokens_max': max(r.get('usage', {}).get('prompt_tokens', 0) for r in observations),
                }.items():
                    assert batch[field] == expected, (sweep, field)
                if 'placeholder_present' in batch:
                    assert batch['placeholder_present'] == sum('...' in (r.get('tool_arguments') or r['content']) for r in observations)
                    assert batch['placeholder_free_eligible'] == sum(
                        r['eligible'] and '...' not in (r.get('tool_arguments') or r['content']) for r in observations)
                latency = sorted(r['seconds'] for r in observations)
                assert batch['latency_p95'] == latency[math.ceil(len(latency) * .95) - 1]
                assert math.isclose(batch['requests_per_second'], batch['eligible'] / batch['wall_seconds'])
                output = sum(r.get('usage', {}).get('completion_tokens', 0) for r in observations)
                assert math.isclose(batch['output_tokens_per_second'], output / batch['wall_seconds'])
    return {'checked_archive_members': checked, 'recomputed_load_sweeps': len(summaries)}


if __name__ == '__main__':
    print(json.dumps(check(Path(__file__).parent / 'evidence')))
