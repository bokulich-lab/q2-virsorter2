# q2-viromics

A [QIIME 2](https://qiime2.org) Plugin for Viromics Identification and Analysis.

## Installation instructions

### Install Prerequisites

[Miniconda](https://conda.io/miniconda.html) provides the `conda` environment and package manager, and is currently the only supported way to install QIIME 2.
Follow the instructions for downloading and installing Miniconda.

After installing Miniconda and opening a new terminal, make sure you're running the latest version of `conda`:

```bash
conda update conda
```

###  Install development version of `q2-viromics`
Clone the repository:
```shell
git clone https://github.com/bokulich-lab/q2-viromics.git
cd q2-viromics
```

Then, run:

```shell
mamba create -n q2-viromics -c conda-forge -c bioconda -c https://packages.qiime2.org/qiime2/2024.2/shotgun/released/  -c defaults q2-types q2cli virsorter=2 "python=3.8" scikit-learn=0.22.1 pandas seaborn hmmer==3.3 prodigal=2.6 screed=1 ruamel.yaml click pip last ncbi-genome-download checkv pyhmmer
```

After this completes, activate the new environment you created by running:

```shell
conda activate q2-viromics
```

```shell
make install
```

```shell
make dev
qiime dev refresh-cache
```
