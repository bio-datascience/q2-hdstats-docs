# Data Preparation

This guide demonstrates how to prepare microbiome data for log-contrast analysis using q2-classo. We'll walk through transforming features, adding taxonomic information and covariates, and splitting data for machine learning tasks.

## Load the Data

```bash
# Create data directory if it doesn't exist
mkdir -p data

# Download the example data files
wget -O data/atacama-counts.qza
wget -O data/classification.qza
wget -O data/atacama-selected-covariates.tsv 
```

## Data Transformation

Transform count data using CLR transformation:

```bash
qiime classo transform-features \
     --p-transformation clr \
     --p-coef 0.5 \
     --i-features atacama-table.qza \
     --o-x xclr
```

## Add Taxonomic Information

Incorporate taxonomic classifications and compute adaptive weights:

```bash
qiime classo add-taxa \
    --i-features xclr.qza  \
    --i-taxa classification.qza \
    --o-x xtaxa \
    --o-aweights wtaxa
```

## Add Covariates

Include environmental metadata with custom weights for each covariate:

```bash
qiime classo add-covariates \
    --i-features xtaxa.qza \
    --i-weights wtaxa.qza \
    --m-covariates-file atacama-selected-covariates.tsv \
    --p-to-add elevation ph toc ec average-soil-relative-humidity average-soil-temperature \
    --p-w-to-add 1. 0.1 0.1 0.1 1. 1. \
    --o-new-features xcovariates \
    --o-new-c ccovariates \
    --o-new-w wcovariates
```

## Split Data for Regression Analysis

Create training and test sets for continuous target prediction:

```bash
qiime sample-classifier split-table \
    --i-table xcovariates.qza \
    --m-metadata-file atacama-selected-covariates.tsv \
    --m-metadata-column average-soil-temperature \
    --p-test-size 0.2 \
    --p-random-state 42 \
    --p-stratify False \
    --o-training-table regress-xtraining \
    --o-test-table regress-xtest
```

**Note**: In newer QIIME versions, add these parameters:
```bash
# --o-training-targets training-targets.qza \
# --o-test-targets test-targets.qza
```

## Split Data for Classification Analysis

Create training and test sets for categorical target prediction:

```bash
qiime sample-classifier split-table \
    --i-table xcovariates.qza \
    --m-metadata-file atacama-selected-covariates.tsv \
    --m-metadata-column vegetation \
    --p-test-size 0.2 \
    --p-random-state 42 \
    --p-stratify False \
    --o-training-table classify-xtraining \
    --o-test-table classify-xtest
```

**Note**: In newer QIIME versions, add these parameters:
```bash
# --o-training-targets training-targets.qza \
# --o-test-targets test-targets.qza
```

Your data is now prepared for log-contrast modeling with both regression and classification targets.