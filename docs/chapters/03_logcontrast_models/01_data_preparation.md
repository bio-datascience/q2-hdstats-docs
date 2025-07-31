# Data Preparation

This guide demonstrates how to prepare microbiome data for log-contrast analysis using q2-classo. We'll walk through transforming features, adding taxonomic information and covariates, and splitting data for machine learning tasks.

## 1. Transform Features with CLR

The Centered Log-Ratio (CLR) transformation is essential for compositional data analysis:

```bash
qiime classo transform-features \
     --p-transformation clr \
     --p-coef 0.5 \
     --i-features genus_table.qza \
     --o-x genus_table_clr
```

## 2. Summarize Feature Table

Check your data quality and statistics:

```bash
qiime feature-table summarize \
    --i-table filtered-table.qza \
    --o-visualization table-summary.qzv
```

## 3. Apply CLR to Main Dataset

Transform your main feature table using the same parameters:

```bash
qiime classo transform-features \
     --p-transformation clr \
     --p-coef 0.5 \
     --i-features atacama-table.qza \
     --o-x xclr
```

## 4. Add Taxonomic Information

Incorporate taxonomic classifications and compute adaptive weights:

```bash
qiime classo add-taxa \
    --i-features xclr.qza  \
    --i-taxa classification.qza \
    --o-x xtaxa \
    --o-aweights wtaxa
```

## 5. Add Covariates

Include environmental metadata with custom weights for each covariate:

```bash
qiime classo add-covariates \
    --i-features xtaxa.qza \
    --i-weights wtaxa.qza \
    --m-covariates-file atacama-sample-metadata.tsv \
    --p-to-add elevation ph toc ec average-soil-relative-humidity average-soil-temperature \
    --p-w-to-add 1. 0.1 0.1 0.1 1. 1. \
    --o-new-features xcovariates \
    --o-new-c ccovariates \
    --o-new-w wcovariates
```

## 6. Split Data for Regression Analysis

Create training and test sets for continuous target prediction:

```bash
qiime sample-classifier split-table \
    --i-table xcovariates.qza \
    --m-metadata-file atacama-sample-metadata.tsv \
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

## 7. Split Data for Classification Analysis

Create training and test sets for categorical target prediction:

```bash
qiime sample-classifier split-table \
    --i-table xcovariates.qza \
    --m-metadata-file atacama-sample-metadata.tsv \
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