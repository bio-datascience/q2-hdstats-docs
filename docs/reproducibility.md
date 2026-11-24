# Reproducibility and Source Versions

The supplement-derived pages retain the audited calculations. No models were
refitted during the website conversion. Figure PDFs are copied without changing
their contents; PNGs are rendered from those PDFs for browser display.

## Audited Environment

| Component | Source |
| --- | --- |
| QIIME 2 | 2026.7.0 |
| c-lasso | `d22da8d5ea54eb499de2fce82fa6c0e1f0c2dcc0` (GitHub, PR60) |
| q2-classo | `ae574af47b7d79761c01bb8ffcea161716387d11` |
| q2-gglasso | `3f586aa1e074727f497e59481ec1565228042cd3` |
| GGLasso | 0.3.1 |

The c-lasso PyPI release is not a substitute for this audited GitHub revision.
The scientific audit replayed the established environment. A subsequent test
installed a new isolated Intel macOS environment and ran the published top-15
and cocoa QIIME commands. This is not cross-platform or clean-hardware validation.

## Install the Tutorial Environment

Download the [tested Intel macOS installation bundle](downloads/tutorial-environment-osx64.zip)
and extract it. With micromamba installed, run from the extracted directory:

```bash
micromamba create -n q2-hdstats-tutorial --file conda-osx-64-explicit.txt
micromamba activate q2-hdstats-tutorial
python -m pip install --no-deps --no-build-isolation -r requirements-plugins.txt
python -m pip check
qiime info
```

The explicit conda file is for **Intel macOS (`osx-64`)**. It is not a Linux or
ARM-native environment file. The GitHub backend and plugin commits are pinned;
the recipe does not substitute the PyPI c-lasso release. Keep this environment
active for both QIIME commands and Python plotting. Conda package caching does
not change the version pins. No existing working environment is modified.

## Reading the Commands

The tutorial and supplement show non-default parameter settings only.
For example, the basic regression call uses the default R3 formulation;
the R1 comparison explicitly switches concomitant estimation off.
The scientific choices are explained beside the commands rather than
repeating default flags. Version pinning is essential: a different
plugin release may have different defaults.

The [registered action defaults](/downloads/qiime-interface-defaults.json)
record the exact interface used for this edition. The command-harmonization
report retains the previous explicit commands and verifies that omitting
default-valued options leaves the resolved parameter settings unchanged.

## Source Correspondence

The repository retains the authoritative supplement in
`analysis/supplement-v2/source/`, its conversion manifest in
`analysis/supplement-v2/conversion-manifest.json`, and the converter in
`analysis/scripts/migrate_supplement_book.py`.

The initial conversion uses Pandoc and Poppler. Once a page has been adapted for
step-by-step use, keep its supplement-derived baseline alongside the edited
version. `editorial-manifest.json` records both hashes and any explicit command
filename corrections. The checks require the source analysis commands, figures,
citations, and labels to remain available. Added preparation, prediction, and
visualization commands are recorded in the reviewed tutorial revision.

To check the current tutorial, run from the repository root:

```bash
python analysis/scripts/check_supplement_migration.py .
jupyter-book build docs --warningiserror
```

The checks retain the 30 source command blocks in the conversion baseline, all 26
original figure PDFs, and all 10 tables. Each figure has a PDF download
and a provenance JSON. The manifest maps supplement sections to web pages.
Historical tutorial files remain in Git and are excluded from the new navigation;
their URLs redirect to the corresponding new subject areas.

Do not run the initial converter over the edited book. To update it from a new
supplement, convert into a clean staging copy, compare with the retained
baselines, then review the tutorial adaptations.

## Optional Python Figures

The [complete plotting bundle](downloads/tutorial-figures.zip) provides a single
portable entry point for all 26 published figures. Extract the archive, activate
the tutorial environment, and run:

```bash
python plotting/reproduce_all_figures.py --case all --output-dir figures/all
```

Use `--case atacama`, `--case motus`, or `--case cocoa` for one case study.
This reads the archived QIIME-derived artifacts and extracted tables, checks
their hashes, and reuses the original plotting functions. It does not refit
models. Original scripts are preserved; only path strings in temporary execution
copies are relocated. Each output has a provenance JSON. The archive includes
reference PDFs; the original website/Supplement figures remain unchanged.

All 26 figures were regenerated in the isolated environment and compared with
the Supplement. Their text and layout agree; minor font/raster rounding is
recorded rather than claimed to be byte identity. The existing top-15 prediction
plotting adapter remains available for models you generate from the walkthrough.

## Input Distribution

Prepared input bundles are available for [Atacama top-15](tutorial/s2-01.md),
[Atacama top-300](tutorial/s2-02.md), and [MAP mOTUs](tutorial/s3.md).
Each contains a source/hash manifest, with no fitted models. The top-300
preparation helpers were tested in a clean working directory and retain the
original scientific calculations. mOTU inputs were checked for consistent
feature order, training support, and subject-disjoint splitting.

The [cocoa/Bracken inputs](tutorial/s4.md) are also available with confirmed
redistribution permission. The newly tested installation recipe above replaces
the historical environment locks in `analysis/envs` for this tutorial edition.
Those historical files are retained as provenance, not current instructions.
Historical absolute paths identify audited sources; the download bundles and
portable plotting entry point do not require access to those original paths.

The statistical-background command examples are schematic, as in the supplement.
Case-study commands require the matching prepared inputs and helper scripts;
do not replace them with historical 13-ASV, top-100 mOTU, or old solver outputs.
