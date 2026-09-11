"""Render the paper's bar charts from frozen archives (no API calls).

Outputs (svg/png/pdf each): corpus, main_hit, main_precision, rq3_inspection,
rq4_guidance, rq5_execution. Every rate is re-derived from numerator/denominator
and cross-checked against the frozen values quoted in the manuscript; a drift
in any archive fails loudly instead of silently redrawing the figure.
Also prints the Markdown rows used by the manuscript tables (--tables).
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
E2 = ROOT / 'final_results' / 'e2_20260907'
A1 = ROOT / 'final_results' / 'a1_no_inspect_vs_v61_20260906' / 'results.json'
A3 = ROOT / 'final_results' / 'a3_open_judge_20260910' / 'four_model_summary.json'
A4 = ROOT / 'reports' / 'a4_20260910'
LEDGER = ROOT / 'discover_matrix' / 'ledger_v2'
MODELS = {'luna': 'gpt-5.6-luna', 'sonnet': 'claude-sonnet-5',
          'qwen': 'qwen3.8-27b', 'muse': 'muse-glimmer-30b'}
C_BASE, C_FULL, C_ABL = '#62758a', '#007f73', '#c8772a'


def load(path):
    return json.loads(Path(path).read_text())


def rate(obj):
    """Return percentage from a {numerator, denominator, rate} object, checking consistency."""
    assert abs(obj['rate'] - obj['numerator'] / obj['denominator']) < 1e-12, obj
    return 100 * obj['numerator'] / obj['denominator']


def precision(m):
    k, n, i = m['K'], m['N'], m['I']
    assert m['reports'] == k + n + i
    p = m['precision']
    assert (p['numerator'], p['denominator']) == (k + n, k + n + i)
    return 100 * (k + n) / (k + n + i)


def strict(m):
    return rate(m['strict']['precision'])


def e2_metrics(key):
    data = load(E2 / ('luna_history.json' if key == 'luna' else f'{key}/statistics.json'))
    return (data['statistics'] if key == 'luna' else data)['metrics']


def style():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'svg.fonttype': 'none', 'pdf.fonttype': 42,
                         'axes.spines.top': False, 'axes.spines.right': False})


def grouped(ax, labels, series, colors, ylabel, ylim=(0, 100), fmt='{:.1f}', width=0.36, rotate_ticks=True):
    """Two- or three-series grouped bars with vertical value labels (no label collisions)."""
    n = len(series)
    offsets = [(i - (n - 1) / 2) * width for i in range(n)]
    span = ylim[1] - ylim[0]
    for (name, values), off, color in zip(series, offsets, colors):
        xs = [x + off for x in range(len(labels))]
        bars = ax.bar(xs, values, width=width, color=color, label=name, zorder=2)
        for b, v in zip(bars, values):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + span * 0.015,
                    fmt.format(v), ha='center', va='bottom', fontsize=7, rotation=90)
    ax.set_xticks(range(len(labels)), labels)
    if rotate_ticks:
        plt.setp(ax.get_xticklabels(), rotation=20, ha='right', rotation_mode='anchor', fontsize=7.8)
    ax.set_ylim(ylim[0], ylim[1] + span * 0.16)  # headroom for the rotated labels
    ax.set_yticks([t for t in ax.get_yticks() if ylim[0] <= t <= ylim[1]])
    ax.spines['left'].set_bounds(ylim[0], ylim[1])
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', color='#e3e5e8', linewidth=0.6, zorder=0)


def fig_legend(fig, ax, bottom):
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=len(labels), frameon=False, fontsize=8.5,
               bbox_to_anchor=(0.5, 0.0))
    fig.subplots_adjust(bottom=bottom)


def save(fig, name):
    for suffix in ('svg', 'png', 'pdf'):
        fig.savefig(HERE / f'{name}.{suffix}', dpi=220, facecolor='white', metadata={'Creator': 'Matplotlib'})
    svg = HERE / f'{name}.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
    plt.close(fig)


# ---------------------------------------------------------------- Figure: corpus
def fig_corpus():
    rows = [r for r in load(LEDGER / 'provenance' / 'corpus_structure.json') if not r['case'].endswith('8')]
    assert len(rows) == 54
    items = load(LEDGER / 'l_tier.json')['items']
    assert len(items) == 145
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 2.8), gridspec_kw={'width_ratios': [1.2, 0.72, 1.45]})

    ax = axes[0]
    bins = [(5, 7), (8, 10), (11, 13), (14, 16), (17, 20)]
    tbins = [(5, 9), (10, 14), (15, 19), (20, 29), (30, 49), (50, 70)]
    s_counts = [sum(lo <= r['states'] <= hi for r in rows) for lo, hi in bins]
    t_counts = [sum(lo <= r['transitions'] <= hi for r in rows) for lo, hi in tbins]
    assert sum(s_counts) == sum(t_counts) == 54
    xs = list(range(len(bins))) + list(range(len(bins) + 1, len(bins) + 1 + len(tbins)))
    ax.bar(xs[:len(bins)], s_counts, color=C_BASE, width=0.8, zorder=2)
    ax.bar(xs[len(bins):], t_counts, color=C_FULL, width=0.8, zorder=2)
    for x, c in zip(xs, s_counts + t_counts):
        ax.text(x, c + 0.4, str(c), ha='center', va='bottom', fontsize=7.2)
    ax.set_xticks(xs, [f'{lo}-{hi}' for lo, hi in bins] + [f'{lo}-{hi}' for lo, hi in tbins], rotation=45, ha='right')
    ax.text(len(bins) / 2 - 0.5, 27, 'States', ha='center', fontsize=8.5, color=C_BASE)
    ax.text(len(bins) + 1 + len(tbins) / 2 - 0.5, 27, 'Transitions', ha='center', fontsize=8.5, color=C_FULL)
    ax.set_ylim(0, 30)
    ax.set_ylabel('Artifacts (of 54)')
    ax.set_title('(a) Source artifact size', fontsize=9.5)
    ax.grid(axis='y', color='#e3e5e8', linewidth=0.6, zorder=0)

    ax = axes[1]
    levels = ('L0', 'L1', 'L2')
    d2 = [sum(1 for v in items.values() if v['L'] == L and v['D'] == 'D2') for L in levels]
    d1 = [sum(1 for v in items.values() if v['L'] == L and v['D'] == 'D1') for L in levels]
    assert [a + b for a, b in zip(d2, d1)] == [71, 35, 39] and sum(d2) == 98 and sum(d1) == 47
    ax.bar(levels, d2, color=C_FULL, label='D2', zorder=2)
    ax.bar(levels, d1, bottom=d2, color='#9fd3cc', label='D1', zorder=2)
    for x, (a, b) in enumerate(zip(d2, d1)):
        ax.text(x, a + b + 1, str(a + b), ha='center', va='bottom', fontsize=7.5)
    ax.set_ylim(0, 85)
    ax.set_ylabel('Reference issues (of 145)')
    ax.set_title('(b) Problem level and defect status', fontsize=9.5)
    ax.legend(frameon=False, fontsize=7.5, loc='upper right')
    ax.grid(axis='y', color='#e3e5e8', linewidth=0.6, zorder=0)

    ax = axes[2]
    element = [('transition', 'Transition'), ('trigger', 'Trigger'), ('effect', 'Effect'),
               ('state', 'State'), ('guard', 'Guard'), ('region', 'Region')]
    logic = [('unintended_terminal', 'Unintended terminal'), ('unreachable', 'Unreachable'),
             ('nondeterminism', 'Nondeterminism'), ('nontermination', 'Nontermination'),
             ('hierarchy_entry', 'Hierarchy entry'), ('priority_conflict', 'Priority conflict'), ('other', 'Other')]
    e_counts = [sum(1 for v in items.values() if v['defect_element'] == k) for k, _ in element]
    l_counts = [sum(1 for v in items.values() if v['defect_element'] is None and v['defect_logic_kind'] == k) for k, _ in logic]
    assert sum(e_counts) == 104 and sum(l_counts) == 41
    names = [n for _, n in element] + [n for _, n in logic]
    ys = list(range(len(names)))
    ax.barh(ys[:len(element)], e_counts, color=C_BASE, zorder=2, label='Element-anchored (104)')
    ax.barh(ys[len(element):], l_counts, color=C_ABL, zorder=2, label='Behavioral kind (41)')
    for y, c in zip(ys, e_counts + l_counts):
        ax.text(c + 0.6, y, str(c), va='center', fontsize=7.2)
    ax.set_yticks(ys, names, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 46)
    ax.set_xlabel('Reference issues')
    ax.set_title('(c) Defect element or behavioral kind', fontsize=9.5)
    ax.legend(frameon=False, fontsize=7.2, loc='lower right')
    ax.grid(axis='x', color='#e3e5e8', linewidth=0.6, zorder=0)
    fig.subplots_adjust(left=0.055, right=0.99, top=0.88, bottom=0.27, wspace=0.95)
    save(fig, 'corpus')


# ---------------------------------------------------------------- Figures: main comparison
def fig_main():
    labels = list(MODELS.values())
    hit = {k: [] for k in ('hit1', 'hit3', 'hitall')}
    prec = {'P': [], 'Ps': []}
    for key in MODELS:
        m = e2_metrics(key)
        for k in hit:
            hit[k].append((rate(m['baseline'][k]), rate(m['ours'][k])))
        prec['P'].append((precision(m['baseline']), precision(m['ours'])))
        prec['Ps'].append((strict(m['baseline']), strict(m['ours'])))
    # frozen anchors quoted in the manuscript (Table 3)
    assert [round(b, 2) for b, _ in hit['hit1']] == [51.72, 55.40, 51.72, 56.78]
    assert [round(f, 2) for _, f in hit['hit1']] == [74.25, 66.90, 71.49, 74.02]
    assert [round(f, 2) for _, f in prec['P']] == [84.05, 87.36, 89.25, 84.95]
    assert [round(b, 2) for b, _ in prec['Ps']] == [78.71, 53.43, 74.51, 70.04]

    fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.6), sharey=True)
    for ax, (k, title) in zip(axes, (('hit1', 'hit@1 (mean coverage, /435)'),
                                     ('hit3', 'hit@3 (union coverage, /145)'),
                                     ('hitall', 'hit@all (stable coverage, /145)'))):
        grouped(ax, labels, [('Baseline', [b for b, _ in hit[k]]), ('Full', [f for _, f in hit[k]])],
                (C_BASE, C_FULL), 'Coverage (%)' if k == 'hit1' else '')
        ax.set_title(title, fontsize=9.5)
    fig.subplots_adjust(left=0.065, right=0.995, top=0.88, wspace=0.08)
    fig_legend(fig, axes[0], bottom=0.33)
    save(fig, 'main_hit')

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 2.6), sharey=True)
    for ax, (k, title) in zip(axes, (('P', 'Precision P (all reports)'),
                                     ('Ps', 'Strict precision P_strict (D1/D2 only)'))):
        grouped(ax, labels, [('Baseline', [b for b, _ in prec[k]]), ('Full', [f for _, f in prec[k]])],
                (C_BASE, C_FULL), 'Precision (%)' if k == 'P' else '', ylim=(0, 100), width=0.34)
        ax.set_title(title, fontsize=9.5)
    fig.subplots_adjust(left=0.065, right=0.995, top=0.88, wspace=0.06)
    fig_legend(fig, axes[0], bottom=0.33)
    save(fig, 'main_precision')


# ---------------------------------------------------------------- Figure: RQ3 (A1)
def fig_rq3():
    d = load(A1)
    full, abl = d['v61']['metrics'], d['a1']['metrics']
    assert (full['hit1']['numerator'], abl['hit1']['numerator']) == (323, 233)
    assert (abl['reports'], abl['I']) == (814, 160)
    cov_labels = ['hit@1', 'L0 hit@1', 'L1 hit@1', 'L2 hit@1', 'L2 hit@all']
    cov = lambda m: [rate(m['hit1']), rate(m['tiers']['L0']['hit1']), rate(m['tiers']['L1']['hit1']),
                     rate(m['tiers']['L2']['hit1']), rate(m['tiers']['L2']['hitall'])]
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 2.6), gridspec_kw={'width_ratios': [2.2, 1]})
    grouped(axes[0], cov_labels, [('Full', cov(full)), ('No inspection facts', cov(abl))], (C_FULL, C_ABL), 'Coverage (%)', rotate_ticks=False)
    axes[0].set_title('(a) Coverage on gpt-5.6-luna', fontsize=9.5)
    grouped(axes[1], ['P', 'P_strict'], [('Full', [precision(full), strict(full)]),
                                          ('No inspection facts', [precision(abl), strict(abl)])],
            (C_FULL, C_ABL), 'Precision (%)', width=0.34, rotate_ticks=False)
    axes[1].set_title('(b) Report precision', fontsize=9.5)
    fig.subplots_adjust(left=0.065, right=0.995, top=0.88, wspace=0.28)
    fig_legend(fig, axes[0], bottom=0.24)
    save(fig, 'rq3_inspection')


# ---------------------------------------------------------------- Figure: RQ4 (A3)
def fig_rq4():
    d = load(A3)['models']
    labels = list(MODELS.values())
    full = [d[k]['full']['metrics'] for k in MODELS]
    abl = [d[k]['a3']['metrics'] for k in MODELS]
    assert [m['hit1']['numerator'] for m in abl] == [245, 230, 193, 175]
    assert [m['reports'] for m in abl] == [670, 684, 358, 495]
    for k, m in zip(MODELS, full):  # A3 archive's Full must equal the E2/v61 Full
        assert m['hit1']['numerator'] == e2_metrics(k)['ours']['hit1']['numerator']
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.6))
    series = lambda f: [('Full', [f(m) for m in full]), ('No intermediate guidance', [f(m) for m in abl])]
    grouped(axes[0], labels, series(lambda m: rate(m['hit1'])), (C_FULL, C_ABL), 'Coverage (%)')
    axes[0].set_title('(a) hit@1 (/435)', fontsize=9.5)
    grouped(axes[1], labels, series(precision), (C_FULL, C_ABL), 'Precision (%)')
    axes[1].set_title('(b) Precision P', fontsize=9.5)
    grouped(axes[2], labels, series(strict), (C_FULL, C_ABL), 'Strict precision (%)')
    axes[2].set_title('(c) Strict precision P_strict', fontsize=9.5)
    fig.subplots_adjust(left=0.065, right=0.995, top=0.88, wspace=0.34)
    fig_legend(fig, axes[0], bottom=0.34)
    save(fig, 'rq4_guidance')


# ---------------------------------------------------------------- Figure: RQ5 (A4)
def fig_rq5():
    labels = list(MODELS.values())
    full, abl = [], []
    for k in MODELS:
        m = load(A4 / f'{k}-accounting.json')['metrics']
        full.append(m['full'])
        abl.append(m['a4'])
    deltas = [precision(f) - precision(a) for f, a in zip(full, abl)]
    assert [round(x, 2) for x in deltas] == [4.03, 4.01, 2.75, 0.72], deltas
    assert [a['I'] - f['I'] for f, a in zip(full, abl)] == [43, 36, 30, 7]
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.6))
    series = lambda f: [('Full', [f(m) for m in full]), ('No execution feedback', [f(m) for m in abl])]
    grouped(axes[0], labels, series(precision), (C_FULL, C_ABL), 'Precision (%)', ylim=(60, 95))
    axes[0].set_title('(a) Precision P', fontsize=9.5)
    grouped(axes[1], labels, series(strict), (C_FULL, C_ABL), 'Strict precision (%)', ylim=(60, 95))
    axes[1].set_title('(b) Strict precision P_strict', fontsize=9.5)
    grouped(axes[2], labels, series(lambda m: m['I']), (C_FULL, C_ABL), 'Invalid reports I', ylim=(0, 220), fmt='{:.0f}')
    axes[2].set_title('(c) Invalid reports (three rounds)', fontsize=9.5)
    fig.subplots_adjust(left=0.065, right=0.995, top=0.88, wspace=0.34)
    fig_legend(fig, axes[0], bottom=0.34)
    save(fig, 'rq5_execution')


# ---------------------------------------------------------------- Markdown table rows
def frac(obj):
    return f"{obj['numerator']}/{obj['denominator']}（{rate(obj):.2f}%）"


def tables():
    out = []
    m = e2_metrics('luna')
    b, o = m['baseline'], m['ours']
    out.append('## RQ1 table (gpt-5.6-luna)')
    rows = [('hit@1', 'hit1'), ('hit@3', 'hit3'), ('hit@all', 'hitall')]
    for name, k in rows:
        out.append(f"| {name} | {frac(b[k])} | {frac(o[k])} | {rate(o[k]) - rate(b[k]):+.2f} |")
    for L in ('L0', 'L1', 'L2'):
        for name, k in rows:
            out.append(f"| {L} {name} | {frac(b['tiers'][L][k])} | {frac(o['tiers'][L][k])} | {rate(o['tiers'][L][k]) - rate(b['tiers'][L][k]):+.2f} |")
    out.append(f"| R；K/N/I | {b['reports']}；{b['K']}/{b['N']}/{b['I']} | {o['reports']}；{o['K']}/{o['N']}/{o['I']} | — |")
    out.append(f"| P | {frac(b['precision'])} | {frac(o['precision'])} | {precision(o) - precision(b):+.2f} |")
    out.append(f"| P_strict | {frac(b['strict']['precision'])} | {frac(o['strict']['precision'])} | {strict(o) - strict(b):+.2f} |")

    d = load(A1)
    f, a = d['v61']['metrics'], d['a1']['metrics']
    out.append('\n## RQ3 table')
    for name, get in (('hit@1', lambda m: m['hit1']), ('hit@3', lambda m: m['hit3']), ('hit@all', lambda m: m['hitall']),
                      ('L0 hit@1', lambda m: m['tiers']['L0']['hit1']), ('L1 hit@1', lambda m: m['tiers']['L1']['hit1']),
                      ('L2 hit@1', lambda m: m['tiers']['L2']['hit1']), ('L2 hit@all', lambda m: m['tiers']['L2']['hitall'])):
        out.append(f"| {name} | {frac(get(f))} | {frac(get(a))} | {rate(get(a)) - rate(get(f)):+.2f} |")
    out.append(f"| R；K/N/I | {f['reports']}；{f['K']}/{f['N']}/{f['I']} | {a['reports']}；{a['K']}/{a['N']}/{a['I']} | — |")
    out.append(f"| P | {frac(f['precision'])} | {frac(a['precision'])} | {precision(a) - precision(f):+.2f} |")
    out.append(f"| P_strict | {frac(f['strict']['precision'])} | {frac(a['strict']['precision'])} | {strict(a) - strict(f):+.2f} |")

    d = load(A3)['models']
    out.append('\n## RQ4 table')
    for k, name in MODELS.items():
        for cond, label in (('full', 'Full'), ('a3', '无中间引导')):
            m = d[k][cond]['metrics']
            out.append(f"| {name} | {label} | {m['reports']} | {m['K']}/{m['N']}/{m['I']} | {frac(m['hit1'])} | {m['hit3']['numerator']}/145 | {m['hitall']['numerator']}/145 | {precision(m):.2f}% | {strict(m):.2f}% |")

    out.append('\n## RQ5 table')
    for k, name in MODELS.items():
        mm = load(A4 / f'{k}-accounting.json')['metrics']
        for cond, label in (('full', 'Full'), ('a4', '无执行反馈')):
            m = mm[cond]
            out.append(f"| {name} | {label} | {m['reports']} | {m['K']}/{m['N']}/{m['I']} | {frac(m['hit1'])} | {precision(m):.2f}% | {strict(m):.2f}% |")
    print('\n'.join(out))


def main():
    style()
    fig_corpus()
    fig_main()
    fig_rq3()
    fig_rq4()
    fig_rq5()
    print('Verified frozen anchors; wrote corpus, main_hit, main_precision, rq3_inspection, rq4_guidance, rq5_execution (svg/png/pdf)')
    if '--tables' in sys.argv:
        tables()


if __name__ == '__main__':
    main()
