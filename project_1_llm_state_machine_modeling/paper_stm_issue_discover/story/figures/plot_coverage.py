"""Render the paper's coverage figure from the frozen E2 statistics (no API calls)."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'final_results' / 'e2_20260907'
MODELS = {'luna': 'gpt-5.6-luna', 'sonnet': 'claude-sonnet-5',
          'qwen': 'qwen3.8-27b', 'muse': 'muse-glimmer-30b'}


def main():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'svg.fonttype': 'none', 'pdf.fonttype': 42})
    fig, axes = plt.subplots(2, 2, figsize=(8.4, 5.0), sharex=True, sharey=True)
    for ax, (key, name) in zip(axes.flat, MODELS.items()):
        path = DATA / ('luna_history.json' if key == 'luna' else f'{key}/statistics.json')
        data = json.loads(path.read_text())
        metrics = (data['statistics'] if key == 'luna' else data)['metrics']
        for y, (tier, denominator) in enumerate(zip(('L0', 'L1', 'L2'), (213, 105, 117))):
            values = []
            for condition in ('baseline', 'ours'):
                hit = metrics[condition]['tiers'][tier]['hit1']
                assert hit['denominator'] == denominator
                assert abs(hit['rate'] - hit['numerator'] / denominator) < 1e-12
                values.append(hit['rate'] * 100)
            ax.plot(values, [y, y], color='#8c939c', linewidth=1.3, zorder=1)
            for value, marker, color, label in zip(values, ('o', 's'), ('#62758a', '#007f73'), ('Baseline', 'Full')):
                ax.scatter(value, y, marker=marker, color=color, s=40, label=label if y == 0 else None, zorder=2)
            ax.text(101.5, y, f'{values[1] - values[0]:+.2f} pp', va='center', fontsize=9)
        # A stale historical tier split should fail even though its total still sums to 225.
        if key == 'luna':
            assert [metrics['baseline']['tiers'][t]['hit1']['numerator'] for t in ('L0', 'L1', 'L2')] == [108, 72, 45]
        ax.set_title(name, fontsize=11, pad=10)
        ax.set_xlim(0, 125)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_yticks([0, 1, 2], ['L0', 'L1', 'L2'])
        ax.set_ylim(2.55, -0.6)
        ax.grid(axis='x', color='#e3e5e8', linewidth=0.6)
        ax.tick_params(left=False, labelleft=True)
        for side in ('top', 'right', 'left'):
            ax.spines[side].set_visible(False)
        ax.spines['bottom'].set_bounds(0, 100)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.0))
    for ax in axes[1]:
        ax.set_xlabel('Mean coverage (%)')
    fig.subplots_adjust(left=0.06, right=0.99, top=0.92, bottom=0.17, hspace=0.47, wspace=0.15)
    for suffix in ('svg', 'png', 'pdf'):
        fig.savefig(HERE / f'coverage.{suffix}', dpi=220, facecolor='white', metadata={'Creator': 'Matplotlib'})
    svg = HERE / 'coverage.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
    plt.close(fig)
    print('Verified 24 tier rates; wrote coverage.svg, coverage.png, coverage.pdf')


if __name__ == '__main__':
    main()
