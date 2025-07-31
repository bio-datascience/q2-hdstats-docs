# Regression: Predicting Temperature

This tutorial demonstrates how to use log-contrast regression to predict average soil temperature from microbial community data. The regression model identifies which taxa are most predictive of temperature variations.

## Step 1: Train the Regression Model

Use log-contrast regression with stability selection to identify the most stable predictive features:

```bash
# Log-contrast regression with stability selection
qiime classo regress \
    --i-features regress-xtraining.qza \
    --i-c ccovariates.qza \
    --i-weights wcovariates.qza \
    --m-y-file atacama-sample-metadata.tsv \
    --m-y-column average-soil-temperature \
    --p-concomitant \
    --p-stabsel \
    --p-cv \
    --p-path \
    --p-lamfixed \
    --p-stabsel-threshold 0.5 \
    --p-cv-seed 1 \
    --p-no-cv-one-se \
    --o-result regresstaxa.qza
```

Key parameters:
- `--p-stabsel`: Enable stability selection for robust feature selection
- `--p-stabsel-threshold 0.5`: Features selected in >50% of subsamples
- `--p-cv`: Use cross-validation for model selection
- `--p-concomitant`: Include concomitant variables in the model

## Step 2: Make Predictions

Apply the trained model to test data:

```bash
qiime classo predict \
    --i-features regress-xtest.qza \
    --i-problem regresstaxa.qza \
    --o-predictions regress-predictions.qza
```

## Step 3: Visualize Results

Generate a comprehensive summary of the regression results:

```bash
qiime classo summarize \
    --i-problem regresstaxa.qza \
    --i-taxa classification.qza \
    --i-predictions regress-predictions.qza \
    --o-visualization regresstaxa_R3.qzv
```

The visualization will show selected taxa, model performance metrics, and prediction accuracy.