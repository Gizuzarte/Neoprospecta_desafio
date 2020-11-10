FROM ubuntu:18.04

USER root

# Instalacao de softwares
RUN apt-get update && apt-get -y --fix-missing install git build-essential ncbi-blast+ gcc \ 
			software-properties-common tar zip unzip make nano \
			python3 python3-pip fastqc cutadapt pigz 

RUN apt-get -y install wget curl 

RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

RUN wget https://data.qiime2.org/distro/core/qiime2-2020.8-py36-linux-conda.yml && \
 	conda env create -n qiime2-2020.8 --file qiime2-2020.8-py36-linux-conda.yml 

RUN apt install fastqc -y

RUN rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash giovanna

USER giovanna

RUN mkdir -p /home/giovanna/desafio
WORKDIR /home/giovanna/desafio

COPY ./testes /home/giovanna/desafio/testes

USER root
WORKDIR /home/giovanna/desafio/testes
#RUN mkdir -p competencia_01
#RUN cd competencia_01
#WORKDIR /home/giovanna/desafio/testes/competencia_01

# Baixar o banco de dados disponibilizado
USER root
WORKDIR /home/giovanna/desafio/testes
RUN wget https://www.dropbox.com/s/uqadzqzhm8mq6ai/metadados.zip && \
	unzip metadados.zip
WORKDIR /home/giovanna/desafio/testes/metadados/fqs && \
	gzip *.fasta .

# Download script em python
USER root
WORKDIR /home/giovanna/desafio/testes
RUN wget https://www.dropbox.com/s/bztfjnfz33h8dgp/competencia01.py
	
VOLUME [ "/home/giovanna/desafio/testes" ]

RUN . ~/.bashrc

USER giovanna
WORKDIR /home/giovanna/desafio/testes

SHELL ["conda", "activate", "qiime2-2020.8", "fastqc", "/bin/bash", "-c"]
