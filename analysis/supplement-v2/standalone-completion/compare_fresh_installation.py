"""Compare fresh-environment QIIME outputs to the preserved audited artifacts."""
from pathlib import Path
import json
import zipfile
import audit_tutorial_release as audit

ROOT = Path(__file__).resolve().parents[1] / 'outputs/standalone-completion'
audit.AUDIT = ROOT / 'fresh-install-comparisons'
audit.AUDIT.mkdir(exist_ok=True)
fresh = ROOT / 'fresh-install-replay'
canon = Path('/Users/cmueller/Documents/ChatGPT/Atacama-q2-gglasso-q2-classo-tutorial/outputs/fresh-atacama-workflow')
references = (canon / 'q2-classo-top15', canon / 'q2-gglasso-top15', Path(__file__).resolve().parents[1] / 'outputs/bracken-beans/artifacts')
for folder in (fresh / 'atacama-top15', fresh / 'cocoa'):
    for output in sorted(folder.glob('*.qza')):
        reference = next((root / output.name for root in references if (root / output.name).is_file()), None)
        if reference is None:
            continue
        with zipfile.ZipFile(output) as archive:
            members = archive.namelist()
        if any(n.endswith('/data/problem.zip') for n in members):
            audit.compare_problem(output, reference, output.stem)
        elif any(n.endswith('/data/feature-table.biom') for n in members):
            audit.compare_table(output, reference, output.stem)
assert audit.RESULTS and all(row['passed'] for row in audit.RESULTS)
(ROOT / 'fresh-install-numerical-checks.json').write_text(json.dumps(audit.RESULTS, indent=2) + '\n')
print(f'PASS: {len(audit.RESULTS)} fresh-environment artifact comparisons match the audited results.')

audit.RESULTS.clear()
audit.AUDIT = ROOT / 'added-command-comparisons'
audit.AUDIT.mkdir(exist_ok=True)
top300 = canon / 'q2-classo-top300'
motus = Path(__file__).resolve().parents[1] / 'outputs/motus-merged/artifacts'
cocoa = references[-1]
aliases = {'cocoa-filtered.qza': cocoa / 'bracken-species-prev14-total50k.qza',
           'cocoa-train.qza': cocoa / 'bracken-species-prev14-total50k-train.qza',
           'cocoa-test.qza': cocoa / 'bracken-species-prev14-total50k-test.qza'}
for folder in (ROOT / 'added-command-replay').iterdir():
    if not folder.is_dir():
        continue
    for output in sorted(folder.glob('*.qza')):
        reference = aliases.get(output.name) or next((root / output.name for root in (top300, motus, cocoa) if (root / output.name).is_file()), None)
        if reference is None:
            continue
        with zipfile.ZipFile(output) as archive:
            members = archive.namelist()
        if any(n.endswith('/data/problem.zip') for n in members):
            audit.compare_problem(output, reference, output.stem)
        elif any(n.endswith('/data/feature-table.biom') for n in members):
            audit.compare_table(output, reference, output.stem)
assert audit.RESULTS and all(row['passed'] for row in audit.RESULTS)
(ROOT / 'added-command-numerical-checks.json').write_text(json.dumps(audit.RESULTS, indent=2) + '\n')
print(f'PASS: {len(audit.RESULTS)} additional-command inputs/outputs match the audited artifacts.')
