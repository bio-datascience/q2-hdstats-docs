"""Select an exact dependency closure from the audited conda package records."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1] / 'outputs/standalone-completion'
SOURCE = Path('/Users/cmueller/Documents/ChatGPT/Atacama-q2-gglasso-q2-classo-tutorial/work/micromamba-root/envs/q2-hdstats-qiime2-2026.7')
ROOT.mkdir(parents=True, exist_ok=True)
records = {record['name']: record for file in (SOURCE / 'conda-meta').glob('*.json') for record in [json.loads(file.read_text())]}
roots = ['qiime2', 'rachis', 'q2cli', 'q2-types', 'q2-feature-table', 'q2templates',
         'gglasso', 'bokeh', 'zarr', 'numcodecs', 'plotly', 'matplotlib', 'pandas',
         'numpy', 'scipy', 'scikit-learn', 'versioneer', 'versioningit', 'pip',
         'setuptools', 'wheel', 'biom-format', 'h5py', 'networkx', 'seaborn',
         'lxml']
selected = set()
pending = roots[:]
while pending:
    name = pending.pop()
    if name in selected or name.startswith('__'):
        continue
    assert name in records, 'Unresolved dependency: ' + name
    selected.add(name)
    for dep in records[name].get('depends', []):
        pending.append(re.split(r'[ <>=!~]', dep, maxsplit=1)[0])
urls, manifest = [], []
for name in sorted(selected):
    r = records[name]
    assert r.get('url', '').startswith('https://'), name
    checksum = r.get('md5')
    urls.append(r['url'] + ('#' + checksum if checksum else ''))
    manifest.append({k: r.get(k) for k in ('name', 'version', 'build', 'url', 'sha256', 'md5', 'depends')})
(ROOT / 'conda-osx-64-explicit.txt').write_text('# Exact audited package closure for Intel macOS\n@EXPLICIT\n' + '\n'.join(urls) + '\n')
(ROOT / 'conda-package-manifest.json').write_text(json.dumps({'platform': 'osx-64', 'roots': roots, 'packages': manifest}, indent=2) + '\n')
print(f'Pinned {len(manifest)} conda packages from the audited environment; pip-installed plugins/backend will be installed separately from exact Git commits.')
