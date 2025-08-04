# Installing q2-gglasso

### Conda Environment

Create a dedicated conda environment for q2-gglasso:

```bash
# Create and activate QIIME 2 environment
# Example for macOS (Intel) - see other options at:
# https://library.qiime2.org/quickstart/amplicon#id-3-install-the-base-distributions-conda-environment
conda env create \
  --name qiime2-amplicon-2025.4 \
  --file https://raw.githubusercontent.com/qiime2/distributions/refs/heads/dev/2025.4/amplicon/released/qiime2-amplicon-macos-latest-conda.yml

# Activate the environment
conda activate qiime2-amplicon-2025.4

# Clone and install q2-gglasso
git clone https://github.com/bio-datascience/q2-gglasso.git
cd q2-gglasso
pip install -e .

# Refresh QIIME 2 cache
qiime dev refresh-cache
```

### Docker Installation

Docker image of q2-gglasso is available through Docker Hub:

```bash
# Pull the Docker image
docker pull ovlasovets/q2-gglasso:latest

# Run q2-gglasso container with volume mapping for data
docker run -it -v $(pwd):/data ovlasovets/q2-gglasso:latest

# Alternative: Run specific analysis with data directory
docker run -it -v /path/to/your/data:/data ovlasovets/q2-gglasso:latest qiime gglasso --help
```

## Source Installation

The q2-gglasso plugin can be installed directly from the source:

```bash
# Clone the repository
git clone https://github.com/bio-datascience/q2-gglasso.git
cd q2-gglasso

# Install in development mode
pip install -e .

# Refresh QIIME 2 cache
qiime dev refresh-cache
```

### Verification

To verify that q2-gglasso is correctly installed:

```bash
# Check that gglasso is available
qiime gglasso --help

# List all gglasso commands
qiime gglasso info
```

The installation is now complete! You can proceed to explore the plugin's functionality.