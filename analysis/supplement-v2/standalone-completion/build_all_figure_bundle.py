"""Preserve all audited figure inputs and scripts in a portable, hashed mirror."""
from pathlib import Path
import hashlib
import json
import shutil

WORK = Path(__file__).resolve().parents[1]
CANON = Path('/Users/cmueller/Documents/ChatGPT/Atacama-q2-gglasso-q2-classo-tutorial')
REPO = Path('/Users/cmueller/Documents/GitHub/q2-hdstats-docs-biodatascience')
LEGACY = Path('/Users/cmueller/Documents/GitHub/q2-hdstats-docs')
OUT = WORK / 'outputs/standalone-completion/all-figures'
ROOTS = {str(CANON): 'canonical', str(WORK): 'audit-project', str(LEGACY): 'source-repo'}


def mapped(path):
    path = Path(path)
    for source, name in ROOTS.items():
        if path.is_relative_to(source):
            return Path('snapshot') / name / path.relative_to(source)
    raise ValueError('Unmapped source: ' + str(path))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    registry = json.loads((WORK / 'outputs/reproducibility-audit-2026-11-12/figure-registry.json').read_text())
    sources = set()
    figures = []
    for i, row in enumerate(registry['figures'], 1):
        sources.add(Path(row['generator']))
        for field in ('inputs', 'scripts', 'script_dependencies'):
            sources.update(Path(x['path']) for x in row.get(field, []) if x.get('exists', True))
        figure = {'id': f'S{i}', 'generator': str(mapped(row['generator'])),
                  'original_output': str(mapped(row['source'])),
                  'reference': 'reference/' + Path(row['include']).name}
        target = OUT / figure['reference']
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(row['include'], target)
        figures.append(figure)
    # Retain existing extraction/helper dependencies, not just drawing scripts.
    for row in json.loads((REPO / 'analysis/supplement-v2/script-path-map.json').read_text()):
        sources.add(Path(row['original_path']))
    # Some original plotters share extracted tables not repeated in every sidecar.
    for folder in ('metadata', 'q2-classo-top15', 'q2-classo-top300', 'q2-gglasso-top15', 'q2-gglasso-top300'):
        sources.update((CANON / 'outputs/fresh-atacama-workflow' / folder).glob('*.tsv'))
    sources.update((WORK / 'outputs/motus-merged/exports').rglob('*.tsv'))
    records = []
    for source in sorted(sources):
        assert source.is_file(), str(source)
        target = OUT / mapped(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        records.append({'file': str(mapped(source)), 'source': str(source), 'sha256': digest(source), 'bytes': source.stat().st_size})
    # Inputs reached through helper globals rather than figure sidecars.
    extras = [CANON / 'work/atacama-full/taxonomy-silva138-export/taxonomy.tsv']
    for source in extras:
        target = OUT / mapped(source)
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            records.append({'file': str(mapped(source)), 'source': str(source), 'sha256': digest(source), 'bytes': source.stat().st_size})
    manifest = {'description': 'Audited QIIME-derived plotting snapshot; no models are fitted by the figure runner.',
                'cocoa_redistribution_permission': 'Confirmed by the user on 2026-11-24.',
                'roots': ROOTS, 'figures': figures, 'files': records}
    (OUT / 'figure-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Preserved {len(records)} source/input files and {len(figures)} reference PDFs for portable plotting.')


if __name__ == '__main__':
    main()
