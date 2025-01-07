# q2-virsorter2

A [QIIME 2](https://qiime2.org) Plugin for detection and analysis of viral genomes using VirSorter 2.

## Installation
_q2-virsorter2_ is available as part of the QIIME 2 pathogenome distribution. For installation and usage instructions please consult the official [QIIME 2 documentation](https://docs.qiime2.org). 


## Usage
Start by downloading sample input [datasets](https://polybox.ethz.ch/index.php/s/Doa1ePP5IB7QRhI).

Fetch the VirSorter database:
```bash
qiime virsorter2 fetch-db --o-database db.qza --verbose
```

Run the CheckV analysis:
```bash
qiime virsorter2 run --i-database db.qza --i-sequences input.qza --output-dir results/ --verbose
```
