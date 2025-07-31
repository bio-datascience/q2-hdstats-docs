# Atacama Soil Microbiome

In our example, we showcase the application of our QIIME2 plugins for high-dimensional statistics using the Atacama soil microbiome dataset (Neilson et al., 2017). With q2-gglasso we solve various graphical lasso problems to identify microbial associations which we later assess by fitting sparse log-contrast models implemented in q2-classo. Microbiome bioinformatics analyses was conducted using QIIME 2 version 2022.4 (Bolyen et al., 2019). The processing of raw sequence data involved demultiplexing and quality filtering, facilitated by the q2-demux plugin. Subsequent denoising was performed using DADA2 (Callahan et al., 2016) through the q2-dada2 plugin. Taxonomic assignments for Amplicon Sequence Variants (ASVs) were accomplished using the q2-feature-classifier (Bokulich et al., 2018b) with the naive Bayes taxonomy classifier, trained on the Silva Database (Quast et al., 2012).

## Data Preprocessing Pipeline

Here is the original code for Atacama example data preprocessing:

### 1. Import Raw Sequences

First, we import the raw paired-end sequences into QIIME2 format:

```bash
qiime tools import \
    --type EMPPairedEndSequences \
    --input-path data/atacama-emp-paired-end-sequences \
    --output-path data/atacama-emp-paired-end-sequences.qza
```

### 2. Demultiplex Sequences

Next, we demultiplex the sequences using the sample metadata and barcode information:

```bash
qiime demux emp-paired \
  --m-barcodes-file data/atacama-sample-metadata.tsv \
  --m-barcodes-column barcode-sequence \
  --p-rev-comp-mapping-barcodes \
  --i-seqs data/atacama-emp-paired-end-sequences.qza \
  --o-per-sample-sequences data/atacama-demux-full.qza \
  --o-error-correction-details data/atacama-demux-details.qza
```

### 3. Subsample Data

To reduce computational time, we subsample 30% of the sequences:

```bash
qiime demux subsample-paired \
  --i-sequences data/atacama-demux-full.qza \
  --p-fraction 0.3 \
  --o-subsampled-sequences data/atacama-demux-subsample.qza
```

### 4. Filter Low-Quality Samples

We filter out samples with fewer than 100 forward sequences:

```bash
qiime demux filter-samples \
  --i-demux data/atacama-demux-subsample.qza \
  --m-metadata-file data/atacama-demux-subsample/per-sample-fastq-counts.tsv \
  --p-where 'CAST([forward sequence count] AS INT) > 100' \
  --o-filtered-demux data/atacama-demux_subsample.qza
```

### 5. Denoise with DADA2

We perform denoising and chimera removal using DADA2:

```bash
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs data/atacama-demux_subsample.qza \
  --p-trim-left-f 13 \
  --p-trim-left-r 13 \
  --p-trunc-len-f 150 \
  --p-trunc-len-r 150 \
  --o-table data/atacama-table.qza \
  --o-representative-sequences data/atacama-subsample-rep-seqs.qza \
  --o-denoising-stats data/atacama-subsample-denoising-stats.qza
```

### 6. Filter Low-Frequency Features

Finally, we remove features that appear fewer than 100 times across all samples:

```bash
qiime feature-table filter-features \
     --i-table data/atacama-table.qza \
     --o-filtered-table data/atacama-table.qza \
     --p-min-frequency 100
```

## ASV Renaming

One can simply follow the original Atacama tutorial, but we wanted to give these ASVs meaningful names for the sake of this example. That's why we rename the ASV keys as follows:

| ASV label | Real ASV ID                      |
| --------- | -------------------------------- |
| ASV-1     | 89cb1ddf89dcf11d86f725dbcaa9a5ce |
| ASV-2     | cdb9c0ee3bba4c3d8b9292eb575bd9e3 |
| ASV-3     | 4c8ff0ea98d2c0ebb486e33bd96c61f9 |
| ASV-4     | a56b903521b8ab33a7878b35582803a8 |
| ASV-5     | 5c78314ff92e6fec9aa07acc1fa0dc24 |
| ASV-6     | dc8a2f47b3d1dc2e1f5f805891976b29 |
| ASV-7     | 6b780e361cfc5f06def718518324bdcb |
| ASV-8     | f6c10a04d57159c0d64d6bc30c677471 |
| ASV-9     | ffd60d684f32e6fd5b47fe90095f9d34 |
| ASV-10    | ef3fdbe1dcde754d91130cde6a4b4d61 |
| ASV-11    | a36b38f754f6abd278aeb9dbc7696343 |
| ASV-12    | a7b877ae6d2f079a15b6b192a4425620 |
| ASV-13    | 409faa5f5353e543bf6d99125c7c0e83 |

