"""Rebuild the E1 AA matrices from the retained HTML/RSC snapshot, offline."""
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).parent
REPORT = ROOT / '2026-09-07-04-30-00-candidate-benchmarks.md'
ARCHIVE = ROOT / 'evidence/benchmarks_20260906.zip'
MANIFEST = ROOT / 'evidence/benchmarks_20260906.json'
SLUGS = (
    'gpt-5-6-luna', 'claude-sonnet-5', 'claude-4-5-haiku-reasoning',
    'claude-4-5-haiku', 'gemini-3-5-flash', 'gemini-3-6-flash',
    'gemini-3-7-flash', 'gemini-3-8-flash', 'qwen3-8-27b', 'qwen3-8-27b-low',
    'qwen3-6-35b-a3b', 'qwen3-6-35b-a3b-non-reasoning', 'qwen3-6-27b',
    'muse-glimmer', 'gemma-4-31b', 'nemotron-3-5-lightning', 'glm-4-7-flash',
    'gpt-oss-20b', 'llama-3-3-instruct-70b', 'glm-5-3-flash',
)
SOURCES = {
    'aa-qwen38.html': 'https://artificialanalysis.ai/models/qwen3-8-27b',
    'aa-methodology.html': 'https://artificialanalysis.ai/methodology/intelligence-benchmarking',
    'aa-lcr.html': 'https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning',
    'aa-omniscience.html': 'https://artificialanalysis.ai/evaluations/omniscience',
    'aa-models.json': 'derived from aa-qwen38.html by the retained HTML/RSC parser',
}


class Page(HTMLParser):
    """Reuse of the 09-06 investigation's extract.py RSC parser."""
    def __init__(self):
        super().__init__()
        self.script = None
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script = []

    def handle_data(self, data):
        if self.script is not None:
            self.script.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.scripts.append(''.join(self.script))
            self.script = None

    def records(self):
        chunks = []
        for script in self.scripts:
            if script.startswith('self.__next_f.push('):
                value = json.loads(script.removeprefix('self.__next_f.push(').removesuffix(')'))
                if len(value) > 1 and isinstance(value[1], str):
                    chunks.append(value[1])
        for line in ''.join(chunks).splitlines():
            _, separator, value = line.partition(':')
            if separator:
                try:
                    yield json.loads(value)
                except ValueError:
                    continue

    def models(self):
        result = {}

        def walk(value):
            if isinstance(value, dict):
                if 'gpqa' in value and 'ifbench' in value and 'slug' in value:
                    previous = result.setdefault(value['slug'], value)
                    for key in ('gpqa', 'ifbench', 'lcr', 'omniscience'):
                        assert previous.get(key) == value.get(key), (value['slug'], key)
                for item in value.values():
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        for record in self.records():
            walk(record)
        return result


def tables(rows):
    missing = '未取得可核验结果'
    def model(row):
        qualifier = {'nemotron-3-5-lightning': ' (Reasoning, effort 未披露)',
                     'glm-5-3-flash': ' (max)',
                     'llama-3-3-instruct-70b': ' (Non-reasoning)'}.get(row['slug'], '')
        return f"[{row['name']}{qualifier}](https://artificialanalysis.ai/models/{row['slug']})"

    def score(row, key):
        value = row.get(key)
        if value is None:
            return missing
        formatted = f'{value:+.4f}' if key == 'omniscience' else f'{value * 100:.1f}'
        if key == 'intelligenceIndex':
            formatted = f'{value:.1f}'
        return f"[{formatted}](https://artificialanalysis.ai/models/{row['slug']})"

    task = ['| 精确公开变体 / AA 档位 | LCR v1.1 | IFBench | Omni 净分 | GPQA Diamond | HLE text | SciCode |',
            '|---|---:|---:|---:|---:|---:|---:|']
    general = ['| 精确公开变体 / AA 档位 | Intelligence Index v4.2 | Terminal-Bench v2.1 |',
               '|---|---:|---:|']
    structure = ['| 精确公开变体 / AA 档位 | 严格 JSON Schema | SOB | LEDGER | 同口径 BFCL |',
                 '|---|---|---|---|---|']
    for row in rows:
        task.append('| ' + model(row) + ' | ' + ' | '.join(score(row,k) for k in ('lcr','ifbench','omniscience','gpqa','hle','scicode')) + ' |')
        general.append('| ' + model(row) + ' | ' + ' | '.join(score(row,k) for k in ('intelligenceIndex','terminalbenchV21')) + ' |')
        structure.append('| ' + model(row) + ' | ' + ' | '.join([missing]*4) + ' |')
    return {'aa-task': '\n'.join(task), 'aa-general': '\n'.join(general), 'aa-structure': '\n'.join(structure)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-from', type=Path, help='One-time import of the retained public snapshot')
    args = parser.parse_args()
    if args.build_from:
        assert not ARCHIVE.exists() and not MANIFEST.exists(), 'Do not overwrite frozen evidence'
        with ZipFile(ARCHIVE, 'w', ZIP_DEFLATED, compresslevel=9) as archive:
            for name in SOURCES:
                archive.write(args.build_from / name, name)
    with ZipFile(ARCHIVE) as archive:
        hashes = {name: hashlib.sha256(archive.read(name)).hexdigest() for name in SOURCES}
        page = Page()
        page.feed(archive.read('aa-qwen38.html').decode())
        extracted = page.models()
        saved = json.loads(archive.read('aa-models.json'))
        rows = []
        fields = ('name','slug','effort','isReasoning','reasoningTokens','lcr','ifbench',
                  'gpqa','hle','scicode','omniscience','intelligenceIndex','terminalbenchV21')
        for slug in SLUGS:
            row = {key: extracted[slug].get(key) for key in fields}
            assert row == {key: saved[slug].get(key) for key in fields}, slug
            rows.append(row)
        assert b'v4.2' in archive.read('aa-methodology.html')
        assert b'v1.1' in archive.read('aa-lcr.html')
    manifest = {'snapshot_time': '2026-09-06 approximately 23:30 Asia/Shanghai',
                'verified_date': '2026-09-07', 'evaluator': 'Artificial Analysis',
                'index_version': '4.2', 'lcr_version': '1.1', 'sources': SOURCES,
                'sha256': hashes, 'models': rows,
                'identity_limit': 'AA public variants, no independent provider revision attestation'}
    text = REPORT.read_text()
    for label, table in tables(rows).items():
        start, end = '<!-- ' + label + ' -->', '<!-- /' + label + ' -->'
        assert text.count(start) == text.count(end) == 1
        before, middle = text.split(start)
        body, after = middle.split(end)
        if args.build_from:
            text = before + start + '\n' + table + '\n' + end + after
        else:
            assert body.strip() == table, label
    if args.build_from:
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        REPORT.write_text(text)
    else:
        assert json.loads(MANIFEST.read_text()) == manifest
    print(f'{len(rows)} AA model/effort rows, {len(hashes)} source hashes, three Markdown matrices verified')


if __name__ == '__main__':
    main()
