"""Run the newly displayed held-out steps through QIIME, using audited models."""
from pathlib import Path
import json
import os
import re
import shlex
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / 'outputs/standalone-completion'
REPO = Path('/Users/cmueller/Documents/GitHub/q2-hdstats-docs-biodatascience')
CANON = Path('/Users/cmueller/Documents/ChatGPT/Atacama-q2-gglasso-q2-classo-tutorial/outputs/fresh-atacama-workflow/q2-classo-top300')
MOTUS = ROOT / 'outputs/motus-merged'
COCOA = ROOT / 'outputs/bracken-beans'
ENV = STAGE / 'qiime-env'
OUT = STAGE / 'added-command-replay'


def commands(text):
    return [shlex.split(line, comments=True) for block in re.findall(r'^```bash\n(.*?)\n```', text, re.M | re.S)
            for line in block.replace('\\\n', ' ').splitlines() if line.strip().startswith('qiime ')]


def main():
    results = []
    env = os.environ.copy()
    env.update(PATH=str(ENV / 'bin') + os.pathsep + env['PATH'], CONDA_PREFIX=str(ENV),
               MPLCONFIGDIR=str(STAGE / 'cache/matplotlib'), XDG_CACHE_HOME=str(STAGE / 'cache'), NUMBA_CACHE_DIR=str(STAGE / 'cache/numba'))
    env.pop('PYTHONPATH', None)
    for page, case in (('s2-02', 'top300'), ('s3-01', 'motus'), ('s4', 'cocoa'), ('s4-01', 'cocoa-prediction')):
        relative = f'docs/tutorial/{page}.md'
        before = commands((REPO / relative).read_text())
        added = [command for command in commands((STAGE / 'web-overlay' / relative).read_text()) if command not in before]
        folder = OUT / case
        folder.mkdir(parents=True, exist_ok=True)
        aliases = {'motus-clr-train.qza': MOTUS / 'artifacts/motus-clr-pseudocount0.5-train.qza',
                   'motus-clr-test.qza': MOTUS / 'artifacts/motus-clr-pseudocount0.5-test.qza',
                   'motus-taxonomy.qza': MOTUS / 'artifacts/motus-complete-taxonomy.qza'}
        for i, command in enumerate(added, 1):
            for pos, flag in enumerate(command[:-1]):
                if flag.startswith('--i-') or (flag.startswith('--m-') and flag.endswith('-file')):
                    name = command[pos+1]
                    dest = folder / name
                    if dest.exists():
                        continue
                    source = aliases.get(name) or next((p / name for p in (CANON, MOTUS / 'artifacts', COCOA / 'artifacts', COCOA) if (p / name).is_file()), None)
                    assert source is not None, name
                    shutil.copy2(source, dest)
            command[0] = str(ENV / 'bin/qiime')
            print(f'{case}-{i:02d}: ' + ' '.join(command[1:3]), flush=True)
            log = folder / f'{i:02d}.log'
            with log.open('w') as handle:
                done = subprocess.run(command, cwd=folder, env=env, stdout=handle, stderr=subprocess.STDOUT)
            results.append({'page': page, 'command': command, 'returncode': done.returncode})
            (STAGE / 'added-command-checks.json').write_text(json.dumps(results, indent=2) + '\n')
            if done.returncode:
                raise SystemExit('Failed: ' + str(log))
    print(f'PASS: {len(results)} added web commands ran through QIIME without replacing any fitted model.')


if __name__ == '__main__':
    main()
