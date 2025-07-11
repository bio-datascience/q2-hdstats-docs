# High-Dimensional Statistics with QIIME 2

We extend [QIIME 2](https://qiime2.org/) microbiome data analysis platform with advanced methods for high-dimensional statistical modeling and inference.  
This suite currently features two powerful plugins:

- [**q2-gglasso**](https://github.com/bio-datascience/q2-gglasso): Solves General Graphical Lasso (GGLasso) problems with microbiome data using sparse inverse covariance estimation. Use this plugin to infer association networks among microbial taxa, even in high-dimensional datasets.
- [**q2-classo**](https://github.com/bio-datascience/q2-classo): Implements sparse log-contrast regression and classification models. Use this plugin to get interpretable regression and classification results using microbiome data while automatically identifying the most relevant microbial features.

These plugins are fully integrated with the QIIME 2 framework, ensuring artifact-based, reproducible workflows and seamless interoperability with other QIIME 2 tools. Both plugins are designed to help researchers model, visualize, and interpret complex microbiome data using state-of-the-art high-dimensional statistical methods.

---

## What can you do with q2-gglasso and q2-classo?

- **Analyze high-dimensional data** using regularization to control overfitting and increase interpretability.
- **Infer microbial association networks** with graphical lasso and group graphical lasso.
- **Perform sparse, interpretable classification and regression** with sprase log-contrast models
- **Build reproducible workflows** leveraging QIIME 2’s artifact system.

---

This documentation will walk you through installation, setup, and example analyses using q2-gglasso and q2-classo, showing how high-dimensional statistics can advance your microbiome research.

**Let’s get started!**
