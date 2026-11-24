"""Compare all reproduced figure PDFs to the Supplement by raster content."""
from pathlib import Path
import json
import re
import subprocess
import sys
import tempfile
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / 'outputs/standalone-completion'
REPLAY = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'figure-replay-03'
BUNDLE = ROOT / 'all-figures'
provenance = json.loads((REPLAY / 'reproduction.provenance.json').read_text())
checks = []
with tempfile.TemporaryDirectory() as temp:
    for row in provenance['outputs']:
        arrays = []
        for name, pdf in (('reference', BUNDLE / row['reference']), ('reproduced', REPLAY / row['pdf'])):
            stem = Path(temp) / name
            subprocess.run(['pdftoppm', '-singlefile', '-r', '100', '-png', str(pdf), str(stem)], check=True, capture_output=True)
            arrays.append(np.asarray(Image.open(stem.with_suffix('.png')).convert('RGB')))
        a, b = arrays
        same_shape = a.shape == b.shape
        dimension_delta = max(abs(x-y) for x,y in zip(a.shape[:2], b.shape[:2]))
        aligned = b if same_shape else np.asarray(Image.fromarray(b).resize((a.shape[1], a.shape[0]), Image.Resampling.BICUBIC))
        difference = float(np.mean(np.abs(a.astype(float) - aligned.astype(float))))
        exact = same_shape and np.array_equal(a, b)
        # Compare drawing-order text: layout extraction reorders tilted labels.
        texts = [subprocess.check_output(['pdftotext', '-raw', str(pdf), '-'], text=True) for pdf in (BUNDLE / row['reference'], REPLAY / row['pdf'])]
        same_text = re.sub(r'\s+', '', texts[0]) == re.sub(r'\s+', '', texts[1])
        passed = exact or (same_text and dimension_delta <= 2 and difference < 7)
        checks.append({'figure': row['id'], 'passed': passed, 'identical_pixels': exact, 'same_text': same_text,
                       'same_dimensions': same_shape, 'dimension_delta_pixels_100dpi': dimension_delta, 'mean_absolute_pixel_difference': difference})
        print(row['id'] + ': ' + ('identical' if exact else str(checks[-1])), flush=True)
(ROOT / 'figure-render-checks.json').write_text(json.dumps(checks, indent=2) + '\n')
assert len(checks) == 26 and all(r['passed'] for r in checks), 'Inspect figure-render-checks.json before publishing.'
print('PASS: all 26 figures preserve content and layout; exact-pixel matches: ' + str(sum(r['identical_pixels'] for r in checks)) + '. Minor font/raster rounding is recorded, not treated as byte identity.')
