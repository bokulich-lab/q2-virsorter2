# q2-virsorter2

A [QIIME 2](https://qiime2.org) Plugin for detection and analysis of viral genomes using VirSorter 2.

## Installation
_q2-virsorter2_ can be installed into an existing QIIME 2 conda environment. The plugin should be compatible with the 
[metagenome](https://docs.qiime2.org/2024.10/install/native/#qiime-2-metagenome-distribution), 
[pathogenome](https://docs.qiime2.org/2024.10/install/native/#qiime-2-pathogenome-distribution), 
and [amplicon](https://docs.qiime2.org/2024.10/install/native/#qiime-2-amplicon-distribution) QIIME 2 distributions.


```shell
conda activate <environment name>
```

```shell
mamba install -c conda-forge -c bioconda -c defaults prodigal pyhmmer screed virsorter=2
```

```shell
pip install git+https://github.com/bokulich-lab/q2-virsorter2.git
```

```shell
qiime dev refresh-cache
```

## Usage
Start by downloading sample input [datasets](https://polybox.ethz.ch/index.php/s/BpFdP8bC9lcs7YW).

Fetch the VirSorter database:
```bash
qiime virsorter2 fetch-db --o-database db.qza --verbose
```

Run the CheckV analysis:
```bash
qiime virsorter2 run --i-database db.qza --i-sequences input_sequences.qza --output-dir results/ --verbose
```
