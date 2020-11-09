#

import os 
import subprocess
import sys

from subprocess import Popen, PIPE

# Diretorio da trimagem de dados
trimagem = "./trimagem"
os.mkdir(trimagem)

# Chamada para o FastQC
#fastqc = subprocess.call(["fastqc"])

# Testes - Deletar as pastas
os.rmdir(trimagem)

# Chamada qiime2
ativador = '. $CONDA_PREFIX/etc/profile.d/conda.sh && conda activate qiime2-2020.6 &&'
# De fastq para qza
singleend = "qiime tools import --type 'SampleData[SequencesWithQuality]' --input-path metadados/fqs --input-format CasavaOneEightSingleLanePerSampleDirFmt --output-path single-end.qza "
# Execucao do comando
cmd1 = ativador + " " + singleend
subprocess.run(cmd1, shell=True, executable="/bin/bash")
# Vizualizacao 
qzvANTESsingleend = "qiime demux summarize --i-data single-end.qza --o-visualization single-end-ANTES.qzv"
cmd2 = ativador + " " + qzvANTESsingleend
subprocess.run(cmd2, shell=True, executable="/bin/bash")

# Denoise-single
denoise = "qiime dada2 denoise-single --i-demultiplexed-seqs single-end.qza --p-trunc-len 224 --p-trim-left 9 --p-chimera-method consensus --o-table table-dada2.qza --o-representative-sequences rep-seq-dada2.qza --o-denoising-stats stats-dada2.qza"
cmd3 = ativador + " " + denoise
subprocess.run(cmd3, shell=True, executable="/bin/bash")
# Visualizacoes 
qzvTABLE = "qiime feature-table summarize --i-table table-dada2.qza --m-sample-metadata-file metadados/mapa.csv --o-visualization table-dada2.qzv"
cmd4 = ativador + " " + qzvTABLE
subprocess.run(cmd4, shell=True, executable="/bin/bash")
qzvREPSEQ = "qiime feature-table tabulate-seqs --i-data rep-seq-dada2.qza --o-visualization rep-seq-dada2.qzv"
cmd5 = ativador + " " + qzvREPSEQ
subprocess.run(cmd5, shell=True, executable="/bin/bash")
qzvSTATS = "qiime metadata tabulate --m-input-file stats-dada2.qza --o-visualization stats-dada2.qzv"
cmd6 = ativador + " " + qzvSTATS
subprocess.run(cmd6, shell=True, executable="/bin/bash")

# Classificacao Taxonomica via sklearn e SILVA 138
taxonomy = "qiime feature-classifier classify-sklearn --i-reads rep-seq-dada2.qza --i-classifier metadados/silva-138-99-515-806-nb-classifier.qza --o-classification taxonomia.qza"
cmd7 = ativador + " " + taxonomy
subprocess.run(cmd7, shell=True, executable="/bin/bash")
qzvTAXONOMY = "qiime metadata tabulate --m-input-file taxonomia.qza --o-visualization taxonomia.qzv"
cmd8 = ativador + " " + qzvTAXONOMY
subprocess.run(cmd8, shell=True, executable="/bin/bash")

# Tabela OTU
otutable = "qiime taxa collapse --i-table table-dada2.qza --i-taxonomy taxonomia.qza --p-level 7 --o-collapsed-table colapsed-table.qza"
cmd9 = ativador + " " + otutable
subprocess.run(cmd9, shell=True, executable="/bin/bash")
barplot = "qiime taxa barplot --i-table colapsed-table.qza --i-taxonomy taxonomia.qza --m-metadata-file metadados/mapa.csv --o-visualization barplot.qzv"
cmd10 = ativador + " " + barplot
subprocess.run(cmd10, shell=True, executable="/bin/bash")
