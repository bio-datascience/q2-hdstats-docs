# Classification: Predicting Vegetation

This tutorial demonstrates how to predict vegetation presence using log-contrast classification with QIIME 2's classo plugin.

## Overview

Log-contrast classification is useful for predicting categorical outcomes (like vegetation presence/absence) from compositional data. This approach uses regularized logistic regression with log-contrast penalties to handle the compositional nature of microbiome data.

## Step 1: Train the Classification Model

First, we train a log-contrast classifier using cross-validation to predict vegetation presence:

```bash
# Log-contrast classification with cross-validation
qiime classo classify \
    --i-features classify-xtraining.qza \
    --i-c ccovariates.qza \
    --i-weights wcovariates.qza \
    --m-y-file atacama-sample-metadata.tsv \
    --m-y-column vegetation \
    --p-huber \
    --p-stabsel \
    --p-cv \
    --p-path \
    --p-lamfixed \
    --p-stabsel-threshold 0.5 \
    --p-cv-seed 42 \
    --p-no-cv-one-se \
    --o-result classifytaxa.qza
```

**Parameters explained:**
- `--i-features`: Training feature table
- `--i-c`: C matrix for log-contrast constraints
- `--i-weights`: Feature weights
- `--m-y-column vegetation`: Target variable (vegetation presence/absence)
- `--p-huber`: Use Huber loss for robustness
- `--p-stabsel`: Enable stability selection for feature selection
- `--p-cv`: Perform cross-validation
- `--p-stabsel-threshold 0.5`: Stability selection threshold

## Step 2: Make Predictions

Apply the trained model to test data:

```bash
qiime classo predict \
    --i-features classify-xtest.qza \
    --i-problem classifytaxa.qza \
    --o-predictions classify-predictions.qza
```

## Step 3: Generate Summary Visualization

Create a comprehensive summary of the classification results:

```bash
qiime classo summarize \
    --i-problem classifytaxa.qza \
    --i-taxa classification.qza \
    --i-predictions classify-predictions.qza \
    --o-visualization classifytaxa_C2.qzv
```

The resulting visualization will show model performance metrics, selected features, and prediction accuracy.