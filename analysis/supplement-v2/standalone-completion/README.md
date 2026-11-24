# Standalone tutorial validation, 2026-11-24

This completes the previously listed installation, optional plotting, and cocoa
distribution tasks for the tested Intel macOS environment. It does not claim
cross-platform or fresh-hardware testing. The new environment uses exact conda
builds and GitHub source pins; pip compatibility pins fix setuptools/tomlkit
requirements without changing statistical backends.

30 fresh-install CLI checks and 29 numerical artifact comparisons passed.
13 added held-out/preparation commands passed, with 24 matching audited
input/output comparisons. All fitting used QIIME CLI actions. Existing models,
filtering, splits, hyperparameters, published PDFs, and drawing functions remain
unchanged. All 26 figures were reproduced from archived QIIME-derived data;
14 render pixel-identically and the remainder preserve text/layout with small
recorded font/raster rounding. Each generated figure has its own provenance.

The plots archive reproduces the published figures from their archived inputs;
it is not an automatic adapter for arbitrary newly fitted models. The existing
top-15 adapter remains available for fresh walkthrough outputs.

Cocoa artifact public redistribution was confirmed by the user. The permission
statement and input hashes are in the cocoa input manifest. Zenodo is untouched.
