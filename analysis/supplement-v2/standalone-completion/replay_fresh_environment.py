"""Exercise the published QIIME CLI commands in the newly installed environment."""
from pathlib import Path
import importlib.metadata as metadata
import json
import os
import re
import shlex
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1] / 'outputs/standalone-completion'
REPO = Path('/Users/cmueller/Documents/GitHub/q2-hdstats-docs-biodatascience')
ENV = ROOT / 'qiime-env'
OUT = ROOT / 'fresh-install-replay'


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / 'logs').mkdir(exist_ok=True)
    env = os.environ.copy()
    env.update(PATH=str(ENV / 'bin') + os.pathsep + env['PATH'], CONDA_PREFIX=str(ENV),
               MPLBACKEND='Agg', MPLCONFIGDIR=str(ROOT / 'cache/matplotlib'),
               XDG_CACHE_HOME=str(ROOT / 'cache'), NUMBA_CACHE_DIR=str(ROOT / 'cache/numba'))
    env.pop('PYTHONPATH', None)
    (ENV / 'var/q2cli').mkdir(parents=True, exist_ok=True)
    results = []
    def run(command, label, cwd=OUT):
        print(label, flush=True)
        with (OUT / 'logs' / (label + '.log')).open('w') as log:
            done = subprocess.run(command, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
        results.append({'stage': label, 'command': command, 'returncode': done.returncode})
        (OUT / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
        if done.returncode:
            raise SystemExit(f'Failed: {OUT / "logs" / (label + ".log")}')
    run([sys.executable, '-m', 'pip', 'check'], 'pip-check')
    run([str(ENV / 'bin/qiime'), 'info'], 'qiime-info')
    for page, bundle, case in (
        ('s2-01', REPO / 'docs/downloads/atacama-top15-inputs.zip', 'atacama-top15'),
        ('s4-01', ROOT / 'cocoa-inputs.zip', 'cocoa')):
        folder = OUT / case
        folder.mkdir(exist_ok=True)
        with zipfile.ZipFile(bundle) as archive:
            archive.extractall(folder)
        commands = []
        for block in re.findall(r'^```bash\n(.*?)\n```', (REPO / f'docs/tutorial/{page}.md').read_text(), re.M | re.S):
            for line in block.replace('\\\n', ' ').splitlines():
                if line.strip().startswith('qiime '):
                    commands.append(shlex.split(line, comments=True))
        for i, command in enumerate(commands, 1):
            command[0] = str(ENV / 'bin/qiime')
            run(command, case + f'-{i:02d}', folder)
    versions = {name: metadata.version(name) for name in ('qiime2', 'c-lasso', 'q2-classo', 'q2-gglasso', 'gglasso', 'numpy', 'scipy', 'matplotlib', 'setuptools', 'tomlkit')}
    (OUT / 'environment.json').write_text(json.dumps({'python': sys.version, 'packages': versions,
        'scope': 'New isolated Intel macOS environment; source-pinned plugin installation, pip check, complete published top15 QIIME commands, and cocoa classification commands.'}, indent=2) + '\n')
    print(f'PASS: {len(results)} fresh-install CLI checks.', flush=True)


if __name__ == '__main__':
    main()
