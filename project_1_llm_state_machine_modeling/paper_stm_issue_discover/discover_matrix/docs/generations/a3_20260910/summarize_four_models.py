"""Print report tables from frozen labels; no provider or credentials required."""
from collections import Counter
import json
from pathlib import Path

PAPER = Path(__file__).resolve().parents[4]
MODELS = ('sonnet', 'luna', 'qwen', 'muse')


def load_models():
    models = {}
    for name in ('a3_20260910', 'a3_open_judge_20260910'):
        data = json.loads((PAPER / 'final_results' / name / 'results.json').read_text())
        assert data['complete']
        models.update(data['models'])
    assert set(models) == set(MODELS)
    return models


def table(headers, rows):
    return '\n'.join('| ' + ' | '.join(map(str, row)) + ' |' for row in
                     [headers, ['---'] * len(headers), *rows])


def ratio(x):
    return f"{x['numerator']}/{x['denominator']}（{100*x['rate']:.2f}%）"


def tables(models):
    out = {}
    rows, rounds, coverage, funnel, change, intervals, partitions = [], [], [], [], [], [], []
    for name in MODELS:
        model = models[name]
        for arm in ('full', 'a3'):
            data = model[arm]
            m = data['metrics']
            counts = Counter(r['validity'] for r in data['reports'])
            assert len(data['cells']) == 162 and len(data['reports']) == m['reports']
            assert [counts[k] for k in ('VALID_KNOWN', 'VALID_NOVEL', 'INVALID')] == [m[k] for k in ('K', 'N', 'I')]
            rows.append([name.title(), arm.upper(), m['reports'], f"{m['K']}/{m['N']}/{m['I']}", ratio(m['precision']), ratio(m['strict']['precision']), ratio(m['hit1'])])
            coverage.append([name.title(), arm.upper(), ratio(m['hit3']), ratio(m['hitall']), *[ratio(m['tiers'][l]['hit1']) for l in ('L0', 'L1', 'L2')]])
            for rd in ('1', '2', '3'):
                r = data['per_round'][rd]
                rounds.append([name.title(), arm.upper(), rd, r['judged_cells'], r['reports'], f"{r['K']}/{r['N']}/{r['I']}", ratio(r['precision']), ratio(r['hit'])])
        f, a = (model[arm]['metrics'] for arm in ('full', 'a3'))
        change.append([name.title(), f"{f['valid_reports']} → {a['valid_reports']}", f"{100*(a['valid_reports']/f['valid_reports']-1):.2f}%", f"{a['I']-f['I']:+d}", f"{f['I']/162:.3f} → {a['I']/162:.3f}", f"{100*(a['precision']['rate']-f['precision']['rate']):+.2f}", f"{100*(a['strict']['precision']['rate']-f['strict']['precision']['rate']):+.2f}"])
        assert all(model['a3']['per_round'][r]['hit']['numerator'] < model['full']['per_round'][r]['hit']['numerator'] for r in ('1','2','3'))
        g = model['a3']['funnel']
        maps = [x for c in model['a3']['cells'] for x in c['generation_mapping']]
        assert len(maps) == g['generated']
        funnel.append([name.title(), g['generated'], sum(x['binding_precise'] for x in maps), sum(x['execution_status']=='executed' for x in maps), '/'.join(str(g['raw_verdict_'+v]) for v in ('true','false','unknown')), g['publication_filtered_true'], g['publication_coverage_gap'], g['published'], '/'.join(str(g['witness_'+w]) for w in ('W0','W1','W2'))])
        ci=model['comparison']['cluster_bootstrap_95pct']
        intervals.append([name.title(), *[f"[{ci[k]['percentile_2_5']:.2f}, {ci[k]['percentile_97_5']:.2f}]" for k in ('precision','hit1')]])
        parts=model['comparison']['content']['partitions']
        partitions.append([name.title(), *[len(parts[k]) for k in ('shared','full_only','a3_only')]])
    out['main']=table(['模型','条件','报告 R','K/N/I','普通 precision','strict precision','hit@1'],rows)
    out['change']=table(['模型','有效报告 Full → A3','相对变化','ΔI','I/格 Full → A3','Δ普通 pp','Δstrict pp'],change)
    out['rounds']=table(['模型','条件','轮次','格数','报告','K/N/I','precision','hit'],rounds)
    out['coverage']=table(['模型','条件','hit@3','hit@all','L0 hit@1','L1 hit@1','L2 hit@1'],coverage)
    out['funnel']=table(['模型','生成','精确绑定标记','executed','true/false/unknown','true拦截','coverage gap','发布','W0/W1/W2'],funnel)
    out['intervals']=table(['模型','Δprecision 95%区间 pp','Δhit@1 95%区间 pp'],intervals)
    out['partitions']=table(['模型','共有命中单元','Full独有','A3独有'],partitions)
    rows=[]
    for axis, value in [('defect_element','trigger'),('defect_element','guard'),('defect_logic_kind','nondeterminism'),('defect_logic_kind','nontermination'),('defect_logic_kind','unreachable'),('defect_element','effect')]:
        groups=[models[n]['comparison']['content']['axes'][axis][value] for n in MODELS]
        rows.append([value, sum(x['expected_round_units'] for x in groups), sum(x['full_hit_units'] for x in groups),sum(x['a3_hit_units'] for x in groups), *[f"{x['full_hit_units']} → {x['a3_hit_units']}" for x in groups]])
    out['content']=table(['台账分类','分母','Full hit','A3 hit','Sonnet','Luna','Qwen','Muse'],rows)
    rows=[]
    for arm in ('full','a3'):
        ms=[models[n][arm]['metrics'] for n in MODELS]
        totals={k:sum(m[k] for m in ms) for k in ('reports','K','N','I','valid_reports')}
        rows.append([arm.upper(), *[totals[k] for k in ('reports','K','N','I','valid_reports')],sum(m['hit1']['numerator'] for m in ms), *[f"{100*sum(m[k]['rate'] for m in ms)/4:.2f}%" for k in ('precision','hit1')], f"{100*sum(m['strict']['precision']['rate'] for m in ms)/4:.2f}%", f"{100*totals['valid_reports']/totals['reports']:.2f}%",f"{100*sum(m['strict']['precision']['numerator'] for m in ms)/totals['reports']:.2f}%"])
    out['aggregate']=table(['条件','报告','K','N','I','有效','hit/1740分子','模型等权P','模型等权hit','模型等权strict','pooled P','pooled strict'],rows)
    assert len(rounds)==24
    return out


if __name__ == '__main__':
    for key, value in tables(load_models()).items():
        print(f'\n### {key}\n\n{value}')
