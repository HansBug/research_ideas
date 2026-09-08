"""Frozen-rule paired arithmetic; requires all 324 decisions for a backbone."""
import hashlib,importlib.util,json,random
from collections import Counter
from pathlib import Path
paper=Path(__file__).resolve().parents[4]
spec=importlib.util.spec_from_file_location('a1_arithmetic',paper/'discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py')
a1=importlib.util.module_from_spec(spec);spec.loader.exec_module(a1)

def vector(reports,items):
    m=a1.calculate(reports,items)
    return {**{k:m[k] for k in ('hit1','hit3','hitall','precision')},
        **{f'{tier}_{k}':m['tiers'][tier][k] for tier in ('L0','L1','L2') for k in ('hit1','hit3','hitall')},
        **{f'strict_{k}':m['strict'][k] for k in ('hit1','hit3','hitall','precision')}}

def differences(rows,indices):
    output={}
    for key in rows[0]['ours']:
        rates={}
        for arm in ('ours','baseline'):
            n=sum(rows[i][arm][key]['numerator'] for i in indices)
            d=sum(rows[i][arm][key]['denominator'] for i in indices)
            rates[arm]=n/d if d else None
        output[key]=100*(rates['ours']-rates['baseline']) if None not in rates.values() else None
    return output

def analyze(data, items):
    model=data['model']
    cells=data['cells'];pairs=set(data['pair_clusters'])
    assert data['complete'] and len(cells)==324
    assert {(c['arm'],c['pair'],c['round']) for c in cells}=={(a,p,n) for a in ('ours','baseline') for p in pairs for n in (1,2,3)}
    reports={};metrics={}
    for arm in ('ours','baseline'):
        selected=[c for c in cells if c['arm']==arm]
        expected=[(e['ledger_id'],c['round']) for c in selected for e in c['expected']]
        assert len(expected)==435 and set(expected)=={(e,n) for e in items for n in (1,2,3)}
        reports[arm]=[dict(r,pair_id=c['pair'],round=c['round'],nl_cluster=c['nl_cluster']) for c in selected for r in c['reports']]
        assert len({(r['pair_id'],r['round'],r['original_report_id']) for r in reports[arm]})==len(reports[arm])
        for c in selected:
            for e in c['expected']:
                known=[r for r in c['reports'] if r['validity']=='VALID_KNOWN']
                full={r['original_report_id'] for r in known if e['ledger_id'] in r['full_ledger_ids']}
                partial={r['original_report_id'] for r in known if e['ledger_id'] in r['partial_ledger_ids']}
                assert full==set(e['full_report_ids']) and partial==set(e['partial_report_ids'])
                assert e['hit']==bool(full) and e['supported']==bool(full|partial)
        metrics[arm]=a1.calculate(reports[arm],items)
    clusters=sorted(set(data['pair_clusters'].values()));assert len(clusters)==9
    rows=[]
    for cluster in clusters:
        subitems={e:i for e,i in items.items() if i['pair_context']['nl_sha8']==cluster}
        rows.append({arm:vector([r for r in reports[arm] if r['nl_cluster']==cluster],subitems) for arm in reports})
    rng=random.Random(20260907)
    samples=[differences(rows,rng.choices(range(9),k=9)) for _ in range(10000)]
    intervals={}
    for key in rows[0]['ours']:
        values=sorted(s[key] for s in samples if s[key] is not None)
        intervals[key]=dict(low=values[int(.025*(len(values)-1))] if values else None,high=values[int(.975*(len(values)-1))] if values else None,defined_replicates=len(values))
    hit_units={arm:{(e,c['round']) for c in cells if c['arm']==arm for r in c['reports'] if r['validity']=='VALID_KNOWN' for e in r['full_ledger_ids']} for arm in reports}
    def changes(units,arm):
        return [dict(ledger_id=e,round=n,pair=items[e]['pair'],tier=items[e]['L'],nl_cluster=items[e]['pair_context']['nl_sha8'],
                     report_ids=[r['original_report_id'] for r in reports[arm] if r['round']==n and r['validity']=='VALID_KNOWN' and e in r['full_ledger_ids']]) for e,n in sorted(units)]
    gained=changes(hit_units['ours']-hit_units['baseline'],'ours')
    lost=changes(hit_units['baseline']-hit_units['ours'],'baseline')
    assert len(gained)-len(lost)==metrics['ours']['hit1']['numerator']-metrics['baseline']['hit1']['numerator']
    result=dict(model=model,metrics=metrics,delta_pp=differences(rows,list(range(9))),cluster_bootstrap_95pct=intervals,
        gained=gained,lost=lost,per_cluster_delta_pp={c:differences(rows,[i]) for i,c in enumerate(clusters)},
        seed=20260907,replicates=10000,leave_one_cluster_out={c:differences(rows,[j for j in range(9) if j!=i]) for i,c in enumerate(clusters)},
        note='Nine NL clusters resampled jointly across both arms and all three rounds; no semantic re-adjudication. Zero-report precision is undefined.')
    return result


def validate(data, items, snapshot, verification):
    from collections import Counter
    assert data['model'] in {'sonnet','qwen','muse'}
    assert data['complete'] and len(data['cells'])==324
    assert data['human_confirmations']==0
    pairs=set(snapshot['pair_ids'])
    assert len(pairs)==54 and set(data['pair_clusters'])==pairs
    assert len(set(data['pair_clusters'].values()))==9
    assert set(Counter(data['pair_clusters'].values()).values())=={6}
    assert len(items)==145
    assert Counter(i['L'] for i in items.values())=={'L0':71,'L1':35,'L2':39}
    keys=[(c['arm'],c['pair'],c['round']) for c in data['cells']]
    assert len(set(keys))==324
    assert set(keys)=={(a,p,n) for a in ('ours','baseline') for p in pairs for n in (1,2,3)}
    checked={(v['arm'],v['pair'],v['round']):v for v in verification}
    assert len(checked)==len(verification)==324 and set(checked)==set(keys)
    for c in data['cells']:
        receipt=checked[c['arm'],c['pair'],c['round']]
        assert receipt['model']==data['model']
        assert receipt['reports']==len(c['reports']) and receipt['expected']==len(c['expected'])
        assert receipt['source_hash'].removeprefix('sha256:')==c['sha256']
        assert receipt['result_hash']==c['judge_sha256']
        assert receipt['result_path']==c['judge_source']
        assert receipt['source_commit']==c['judge_commit']
        for field in ('validity_arbitrations','relation_arbitrations','recovered_failed_calls'):
            assert receipt[field]==c[field]
        audit=c['judge_audit']
        assert audit['logical_calls']==receipt['calls']==sum(audit['logical_statuses'].values())
        assert audit['logical_calls']-audit['logical_statuses'].get('success',0)==c['recovered_failed_calls']
        import re
        assert re.fullmatch(r'[0-9a-f]{64}',c['sha256'])
        assert re.fullmatch(r'sha256:[0-9a-f]{64}',c['judge_sha256'])
        for field in ('source','judge_source'):
            path=Path(c[field])
            assert not path.is_absolute() and '..' not in path.parts
            assert path.parts[0]==data['model']
        if c['arm']=='ours':
            assert set(c['stages'])=={'prepare','contract_extraction','contract_completion','discovery_grounding','execute_batch','d_adjudication','validate_d','publish'}
            assert set(c['stages'].values())<={'completed','completed_with_diagnostics'}
            assert c['audit_errors']==0
            validation=c['d_validation']
            expected_obligations=validation['expected_obligation_ids']
            unresolved=validation['final_unresolved_ids']
            assert len(set(expected_obligations))==len(expected_obligations)
            assert len(set(unresolved))==len(unresolved)
            assert set(unresolved)<=set(expected_obligations)
            if unresolved:
                assert c['stages']['d_adjudication']=='completed_with_diagnostics'
                assert c['stages']['validate_d']=='completed_with_diagnostics'
        assert c['judge_status']=='completed'
        assert c['judge_protocol']==snapshot['judge_protocol_hash']
        assert c['judge_prompt']==snapshot['judge_prompt_hash']
        assert c['nl_cluster']==data['pair_clusters'][c['pair']]
        assert c['status'] in ({'completed','completed_with_diagnostics'} if c['arm']=='ours' else {'ok'})
        expected={e['ledger_id']:e for e in c['expected']}
        assert len(expected)==len(c['expected'])
        assert set(expected)=={e for e,i in items.items() if i['pair']==c['pair']}
        for eid,e in expected.items():
            assert e['L']==items[eid]['L']
            assert c['nl_cluster']==items[eid]['pair_context']['nl_sha8']
        reports={r['original_report_id']:r for r in c['reports']}
        assert len(reports)==len(c['reports'])
        for r in reports.values():
            assert set(r['full_ledger_ids']+r['partial_ledger_ids'])<=set(expected)
            assert r['validity'] in {'VALID_KNOWN','VALID_NOVEL','INVALID'}
    return analyze(data,items)


def counts(rows, field):
    return dict(sorted(Counter(str(row.get(field)) for row in rows).items()))


def summarize_evidence(data):
    assert data['complete'] and len(data['cells']) == 324
    cells = [c for c in data['cells'] if c['arm'] == 'ours']
    assert len(cells) == 162
    candidates = [r for c in cells for r in c['candidate_evidence']]
    receipts = [r for c in cells for r in c['predicate_receipts']]
    reports = [r for c in cells for r in c['reports']]
    by_witness = {}
    for w in sorted({r['method_evidence']['witness_level'] for r in reports}):
        subset = [r for r in reports if r['method_evidence']['witness_level'] == w]
        validity = counts(subset, 'validity')
        valid = sum(r['validity'] != 'INVALID' for r in subset)
        by_witness[w] = dict(reports=len(subset), validity=validity,
            precision=dict(numerator=valid, denominator=len(subset), rate=valid/len(subset)))
    assert sum(v['reports'] for v in by_witness.values()) == len(reports)
    return dict(model=data['model'], cells=len(cells),
        candidates=dict(total=len(candidates), witness=counts(candidates,'witness_level'),
            predicate=counts(candidates,'predicate_id'), coverage=counts(candidates,'coverage_class')),
        execution_receipts=dict(total=len(receipts), backend=counts(receipts,'backend'),
            state=counts(receipts,'execution_state'), failure=counts(receipts,'failure_kind'),
            verdict=counts(receipts,'verdict'), witness=counts(receipts,'witness_level')),
        published=dict(total=len(reports), by_witness=by_witness,
            facets=sum(r['method_evidence']['facet_count'] for r in reports),
            folded_subclaims=sum(len(r['method_evidence']['folded_sub_claims'] or []) for r in reports),
            with_source_attribution=sum(bool(r['method_evidence']['source_attribution']) for r in reports)),
        caveat='Receipt counts include revisions and passes; they are not distinct bugs or successful published findings. W levels and source-attribution presence do not establish judge validity or causal hallucination reduction.')




def analyze_history(receipt, snapshot, items):
    """Recompute historical Luna arithmetic; do not generate or re-adjudicate."""
    prefix=Path('final_results/v61_source_divergence_vs_x1v2_baseline')
    assert receipt['source']==str(prefix)
    inputs=paper/'pipeline/representation/reports/llms_emp_r45_java_60/pairs'
    clusters={p:hashlib.sha256((inputs/p/'nl.txt').read_bytes()).hexdigest()[:8] for p in snapshot['pair_ids']}
    assert all(clusters[i['pair']]==i['pair_context']['nl_sha8'] for i in items.values())
    data=dict(model='luna-historical',complete=True,pair_clusters=clusters,cells=[])
    for arm in ('ours','baseline'):
        for cell in receipt['arms'][arm]['cells']:
            source=Path(cell['source'])
            assert not source.is_absolute() and '..' not in source.parts
            assert source.is_relative_to(prefix/'raw/judge_v3.11_iter6cfg')
            payload=(paper/source).read_bytes()
            assert hashlib.sha256(payload).hexdigest()==cell['sha256']
            raw=json.loads(payload)
            assert raw['status']=='completed'
            assert (raw['pair_id'],raw['round'])==(cell['pair_id'],cell['round'])
            assert raw['judge_code_commit']==cell['judge_commit']
            assert len(raw['report_outcomes'])==cell['reports']
            data['cells'].append(dict(arm=arm,pair=raw['pair_id'],round=raw['round'],
                nl_cluster=clusters[raw['pair_id']],reports=raw['report_outcomes'],expected=raw['expected_outcomes']))
    result=analyze(data,items)
    for arm in ('ours','baseline'):
        assert json.loads(json.dumps(result['metrics'][arm]))==receipt['arms'][arm]['metrics']
    return result

def check_counterexamples(data, items, snapshot, verification):
    """Reject damaged copies of a real complete group; never calls a provider."""
    import copy
    def reject(label,change):
        bad=copy.deepcopy(data)
        change(bad)
        try:validate(bad,items,snapshot,verification)
        except AssertionError:pass
        else:raise AssertionError(label+' accepted')

    reject('missing cell',lambda d:d['cells'].pop())
    reject('duplicate cell',lambda d:d['cells'].__setitem__(0,copy.deepcopy(d['cells'][1])))
    reject('partial flag',lambda d:d.__setitem__('complete',False))
    reject('wrong judge prompt',lambda d:d['cells'][0].__setitem__('judge_prompt','wrong'))
    reject('wrong NL cluster',lambda d:d['cells'][0].__setitem__('nl_cluster','wrong'))
    def wrong_ledger(d):
        c=next(c for c in d['cells'] if c['reports'])
        eid=next(e for e,i in items.items() if i['pair']!=c['pair'])
        c['reports'][0]['full_ledger_ids']=[eid]
    reject('cross-pair ledger reference',wrong_ledger)
    def wrong_expected(d):
        c=next(c for c in d['cells'] if c['expected'])
        c['expected'][0]['hit']=not c['expected'][0]['hit']
    reject('incorrect expected hit',wrong_expected)
    reject('missing stage receipt',lambda d:next(c for c in d['cells'] if c['arm']=='ours')['stages'].pop('publish'))
    reject('forged source hash',lambda d:d['cells'][0].__setitem__('sha256','0'*64))
    reject('unsafe source path',lambda d:d['cells'][0].__setitem__('source','../private/config'))
    def remove_unmatched_report(d):
        c=next(c for c in d['cells'] if any(r['validity']=='INVALID' for r in c['reports']))
        c['reports'].remove(next(r for r in c['reports'] if r['validity']=='INVALID'))
    reject('missing invalid report',remove_unmatched_report)
    reject('foreign unresolved obligation',lambda d:next(c for c in d['cells'] if c['arm']=='ours')['d_validation']['final_unresolved_ids'].append('foreign-obligation'))
    reject('unrecorded human confirmation',lambda d:d.__setitem__('human_confirmations',1))
    reject('inconsistent judge call count',lambda d:d['cells'][0]['judge_audit'].__setitem__('logical_calls',-1))


if __name__=='__main__':
    import argparse,hashlib
    parser=argparse.ArgumentParser(description='Verify frozen E2 decisions and arithmetic without API calls.')
    parser.add_argument('--archive',type=Path,default=paper/'final_results/e2_20260907')
    parser.add_argument('--model',choices=('sonnet','qwen','muse'),help='Explicit single complete backbone; default requires all three.')
    parser.add_argument('--check-counterexamples',action='store_true')
    args=parser.parse_args()
    archive=args.archive
    manifest=json.loads((archive/'archive_manifest.json').read_text())['files']
    actual_files={str(p.relative_to(archive)) for p in archive.rglob('*.json') if p!=archive/'archive_manifest.json'}
    assert set(manifest)==actual_files
    for name,receipt in manifest.items():
        relative=Path(name)
        assert not relative.is_absolute() and '..' not in relative.parts
        payload=(archive/relative).read_bytes()
        assert len(payload)==receipt['bytes']
        assert hashlib.sha256(payload).hexdigest()==receipt['sha256']
    snapshot=json.loads((archive/'input_snapshot.json').read_text())
    sources=json.loads((archive/'sources.json').read_text())
    ledger=paper/'discover_matrix/ledger_v2/ledger.json'
    actual_hash='sha256:'+hashlib.sha256(ledger.read_bytes()).hexdigest()
    assert snapshot['ledger_hash'] in (actual_hash,actual_hash.removeprefix('sha256:'))
    items=json.loads(ledger.read_text())['items']
    models=(args.model,) if args.model else ('sonnet','qwen','muse')
    for model in models:
        root=archive/model
        data=json.loads((root/'cells.json').read_text())
        assert data['model']==model and data['schema']=='paper1.e2.frozen-decisions.v1'
        generation=sources['models'][model]['generation_statistics']
        assert generation['model']==model
        for arm in ('ours','baseline'):
            cells=[c for c in data['cells'] if c['arm']==arm]
            saved=generation['arms'][arm]
            assert saved['cells']==len(cells)==162
            assert saved['reports']==sum(len(c['reports']) for c in cells)
            assert saved['statuses']==dict(Counter(c['status'] for c in cells))
            if arm=='ours':
                assert saved['schema_failure_events']==sum(c['schema_failures'] for c in cells)
        verification=json.loads((root/'verification.json').read_text())
        actual=validate(data,items,snapshot,verification)
        assert json.loads(json.dumps(actual))==json.loads((root/'statistics.json').read_text())
        assert summarize_evidence(data)==json.loads((root/'evidence.json').read_text())
        if args.check_counterexamples:
            check_counterexamples(data,items,snapshot,verification)
            print(model,'14 archive corruption counterexamples rejected')
        print(model,'324 cells, complete coverage and all paired/evidence statistics verified; no API calls')
    history=json.loads((archive/'luna_history.json').read_text())
    assert json.loads(json.dumps(analyze_history(history['verification'],snapshot,items)))==history['statistics']
    print('historical Luna: 324 source hashes and paired arithmetic verified; no re-adjudication')
