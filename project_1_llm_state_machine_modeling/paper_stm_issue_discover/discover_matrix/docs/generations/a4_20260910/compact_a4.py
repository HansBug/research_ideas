"""Export/check compact A4 accounting; no prompts, raw responses, or provider calls."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def compact(data, source_hash):
    keys = ('model', 'identity', 'namespace', 'source_hashes', 'metrics', 'rounds', 'routes',
            'transitions', 'candidate_flows', 'true_origins', 'd_transitions',
            'matched_wording_changed', 'matched_semantic_assessment_changed', 'stage_statuses',
            'calls', 'hit_changes', 'precision_decomposition', 'paired_by_pair', 'cells')
    result = {k: data[k] for k in keys}
    result.update(schema='paper1.a4.compact-accounting.v1', local_analysis_sha256=source_hash,
                  raw_calls_included=False)
    result['candidates'] = [{k: v for k, v in row.items() if k not in {'source', 'tail'}}
                            for row in data['candidates']]
    result['publications'] = [{**{k: v for k, v in row.items() if k != 'outcome'},
                              'outcome': {k: row['outcome'].get(k) for k in (
                                  'validity', 'd_tier', 'full_ledger_ids', 'partial_ledger_ids')}}
                             for row in data['publications']]
    check(result)
    return result


def check(data):
    if data['schema'] == 'paper1.a4.pending-bounds.v1':
        rows = data['reports']
        known = [r for r in rows if r['label'] is not None]
        n, missing = len(rows), len(rows) - len(known)
        valid = sum(r['label'] != 'INVALID' for r in known)
        strict = sum(r['label'] != 'INVALID' and r['d_tier'] in ('D1', 'D2') for r in known)
        assert len({(r['pair'], r['round'], r['report_id']) for r in rows}) == n
        assert data['pending'] == missing == 4
        assert data['precision_numerator_bounds'] == [valid, valid + missing]
        assert data['strict_numerator_bounds'] == [strict, strict + missing]
        assert data['denominator'] == n == 985
        return
    pubs = data['publications']
    assert len(data['cells']) == 162
    assert len({(r['pair'], r['round'], r['report_id']) for r in pubs}) == len(pubs)
    assert dict(Counter(r['route'] for r in pubs)) == data['routes']
    metrics = data['metrics']['a4']
    labels = Counter(r['label'] for r in pubs)
    assert all(labels[k] == metrics[k] for k in 'KNI')
    assert len(pubs) == metrics['reports']
    assert metrics['precision']['numerator'] == labels['K'] + labels['N']
    assert metrics['precision']['denominator'] == len(pubs)
    for rnd in (1, 2, 3):
        rows = [r for r in pubs if r['round'] == rnd]
        tally = data['rounds'][str(rnd)]['a4']
        assert len(rows) == tally['reports']
        assert all(sum(r['label'] == k for r in rows) == tally[k] for k in 'KNI')
        assert sum(r['label'] != 'I' and r['outcome']['d_tier'] in ('D1', 'D2') for r in rows) == tally['strict_precision']['numerator']
        hit = {e for r in rows if r['label'] == 'K' for e in r['outcome']['full_ledger_ids']}
        assert len(hit) == tally['hit']['numerator']
    flows = Counter('/'.join(r[k] for k in ('verdict', 'origin', 'new_d', 'publication')) for r in data['candidates'])
    assert dict(flows) == data['candidate_flows']


def pending_bounds(data, source_hash):
    labels = []
    for cell in data['cells']:
        for report in cell['reports']:
            outcome = report.get('outcome') or {}
            labels.append({'pair': cell['pair_id'], 'round': cell['round'], 'report_id': report['report_id'],
                           'route': report['route'], 'label': outcome.get('validity'), 'd_tier': outcome.get('d_tier')})
    known = [r for r in labels if r['label'] is not None]
    valid = sum(r['label'] != 'INVALID' for r in known)
    strict = sum(r['label'] != 'INVALID' and r['d_tier'] in ('D1', 'D2') for r in known)
    missing = len(labels) - len(known)
    result = {'schema': 'paper1.a4.pending-bounds.v1', 'model': 'qwen', 'reports': labels,
              'local_accounting_sha256': source_hash, 'pending': missing, 'denominator': len(labels),
              'precision_numerator_bounds': [valid, valid + missing],
              'strict_numerator_bounds': [strict, strict + missing],
              'scope': 'Unknown-label bounds with fixed full denominator; not a completed score or confidence interval.'}
    check(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--pending-bounds', action='store_true')
    args = parser.parse_args()
    raw = args.input.read_bytes()
    data = json.loads(raw)
    if args.output:
        data = (pending_bounds if args.pending_bounds else compact)(data, hashlib.sha256(raw).hexdigest())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    else:
        check(data)
    print(json.dumps({'model': data['model'], 'check': 'passed'}))


if __name__ == '__main__':
    main()
