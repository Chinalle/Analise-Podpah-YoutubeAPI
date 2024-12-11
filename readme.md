# Ciência de Dados em Nuvem com serviços AWS

## Tecnologias usadas

[![YouTube API V3](https://img.shields.io/badge/YouTube%20API%20V3-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://developers.google.com/youtube/v3/docs/search/list?hl=pt-br)
[![AWS](https://img.shields.io/badge/Amazon%20Web%20Services-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/)
[![AWS Glue](https://img.shields.io/badge/Amazon%20Glue-FF9900?style=for-the-badge&logo=amazonglue&logoColor=white)](https://aws.amazon.com/glue/)
[![Amazon Comprehend](https://img.shields.io/badge/Amazon%20Comprehend-FF9900?style=for-the-badge&logo=amazoncomprehend&logoColor=white)](https://aws.amazon.com/comprehend/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/docs/index.html)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/doc/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/doc/)

# YouTube Data Analysis Pipeline

## Overview
Este projeto automatiza a coleta, armazenamento, processamento e análise de dados de vídeos do YouTube para diversas playlists. O pipeline extrai insights como taxas de engajamento e prevê métricas chave utilizando modelos de machine learning.

## Features
- **Coleta automatizada de dados** usando a API do YouTube.
- **Armazenamento local e na nuvem** (Amazon S3).
- **Processamento de dados** com AWS Glue para transformações e limpeza.
- **Análise e consulta** com Amazon Athena.
- **Modelos de machine learning** (XGBoost) treinados e implantados usando Amazon SageMaker.

## Table of Contents
- [Arquitetura](#arquitetura)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Setup](#setup)
- [Detalhes do Pipeline](#detalhes-do-pipeline)
  - [Coleta de Dados](#coleta-de-dados)
  - [Armazenamento de Dados](#armazenamento-de-dados)
  - [Processamento de Dados](#processamento-de-dados)
  - [Machine Learning](#machine-learning)
- [Uso](#uso)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## Arquitetura
![Arquitetura do Pipeline](path/to/architecture-diagram.png)

## Tecnologias Utilizadas
- **Linguagens de Programação**: Python
- **Armazenamento de Dados**: CSV, JSON, Amazon S3 (Parquet)
- **Processamento de Dados**: AWS Glue, Apache Spark
- **Machine Learning**: Amazon SageMaker, XGBoost
- **Consulta de Dados**: Amazon Athena
- **Variáveis de Ambiente**: Gerenciadas com dotenv

## Setup

### Pré-requisitos
- Python 3.8+
- Conta AWS
- AWS CLI instalada e configurada
- Bibliotecas Python necessárias: `boto3`, `pandas`, `sagemaker`, `dotenv`

### Instalação
1. **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repo.git
    cd seu-repo
    ```
2. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure as variáveis de ambiente no arquivo `.env`:**
    ```env
    ACCESS_KEY=seu-access-key
    SECRET_ACCESS_KEY=seu-secret-key
    REGION=sua-regiao
    ```

## Detalhes do Pipeline

### Coleta de Dados
- Extrai metadados de vídeos da API do YouTube para playlists especificadas.
- Campos capturados: visualizações, curtidas, comentários, duração, data de publicação e URL do thumbnail.

### Armazenamento de Dados
- **Local**: Salva dados brutos em formatos CSV e JSON usando Pandas.
- **Nuvem**: Envia dados brutos para o Amazon S3 no diretório `/raw`.

### Processamento de Dados
- Utiliza AWS Glue para:
  - Converter dados brutos para um formato estruturado.
  - Transformar a duração ISO 8601 para segundos.
  - Preencher valores ausentes e calcular taxas de engajamento.
  - Salvar dados processados de volta no Amazon S3 no diretório `/processed` em formato Parquet.

### Machine Learning
- Prepara conjuntos de dados de treinamento e teste usando Pandas e scikit-learn.
- Converte os dados para o formato LIBSVM para uso no XGBoost.
- Envia os conjuntos de dados para o Amazon S3.
- Treina modelos XGBoost usando Amazon SageMaker para:
  - Previsão de visualizações.
  - Previsão de curtidas.
  - Previsão da taxa de engajamento.
- Implanta os modelos com endpoints do SageMaker para previsões em tempo real.
