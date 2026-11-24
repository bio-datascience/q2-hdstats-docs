"""Validate the installation and full-figure downloads with standard Python."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile


def main():
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    records = repo / 'analysis/supplement-v2/standalone-completion'
    manifest = json.loads((records / 'completion-manifest.json').read_text())
    for name, expected in manifest['downloads'].items():
        archive = repo / 'docs/downloads' / name
        assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected['sha256'], name
    with zipfile.ZipFile(repo / 'docs/downloads/tutorial-figures.zip') as archive:
        figures = json.loads(archive.read('plotting/figure-manifest.json'))
        assert len(figures['figures']) == 26
        for row in figures['files']:
            path = Path(row['file'])
            assert not path.is_absolute() and '..' not in path.parts
            content = archive.read('plotting/' + row['file'])
            assert hashlib.sha256(content).hexdigest() == row['sha256'], row['file']
        for row in figures['figures']:
            name = Path(row['reference']).name
            assert archive.read('plotting/' + row['reference']) == (repo / 'docs/images/tutorial-v2' / name).read_bytes(), name
        compile(archive.read('plotting/reproduce_all_figures.py'), 'reproduce_all_figures.py', 'exec')
    with zipfile.ZipFile(repo / 'docs/downloads/tutorial-environment-osx64.zip') as archive:
        explicit = archive.read('conda-osx-64-explicit.txt').decode()
        pins = archive.read('requirements-plugins.txt').decode()
        assert '@EXPLICIT' in explicit and 'file://' not in explicit
        assert 'd22da8d5ea54eb499de2fce82fa6c0e1f0c2dcc0' in pins
        assert 'ae574af47b7d79761c01bb8ffcea161716387d11' in pins
        assert '3f586aa1e074727f497e59481ec1565228042cd3' in pins
        assert 'gglasso==0.3.1' in pins
    for name in ('fresh-install-checks.json', 'added-command-checks.json'):
        checks = json.loads((records / name).read_text())
        assert checks and all(item['returncode'] == 0 for item in checks), name
    for name in ('fresh-install-numerical-checks.json', 'figure-render-checks.json'):
        checks = json.loads((records / name).read_text())
        assert checks and all(item['passed'] for item in checks), name
    print('PASS: installation pins, full-figure archive, 26 unchanged reference PDFs, and fresh-environment validation records.')


if __name__ == '__main__':
    main()
