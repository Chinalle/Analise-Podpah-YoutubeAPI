# Ciência de Dados em Nuvem

## Tecnologias usadas

[![YouTube API V3](https://img.shields.io/badge/YouTube%20API%20V3-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://developers.google.com/youtube/v3/docs/search/list?hl=pt-br)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/?hl=en)
[![Google Vertex AI](https://img.shields.io/badge/Google%20Vertex%20AI-0E86F0?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/vertex-ai?_gl=1*7ffbow*_up*MQ..&gclid=CjwKCAjwyfe4BhAWEiwAkIL8sKk1e1l8H_4woEnV9ipcHXA7Zd6XDQTE-e6ZM0PmSnC5GSgekvAudBoCjo4QAvD_BwE&gclsrc=aw.ds&hl=en)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/docs/index.html)
[![Postgres](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/doc/)

## 1. Coletar Dados de Todos os Vídeos de Cada Quadro

  Selecionar todos os vídeos de cada quadro: Coletar os dados de todos os vídeos disponíveis para cada quadro (Rango Brabo, Podpah Visita, Querido Diário, Quebrada FC, Batalha da Aldeia, etc.).

### - Extrair dados básicos

- Visualizações: Quantidade total de visualizações.
- Curtidas: Número de curtidas em cada vídeo.
- Comentários: Texto dos comentários para análise de sentimentos.
- Data e horário de postagem: Registrar a data e hora em que cada vídeo foi publicado.
- Duração do vídeo: Extrair a duração total do vídeo.

## 2. Armazenamento dos Dados em um Banco de Dados Local

Utilizar um banco de dados local (PostgreSQL) para armazenar todos os dados e permitir consultas rápidas e processamento eficiente.
Organizar os dados de forma estruturada e com possibilidade de exportação para a nuvem caso haja necessidade de escalabilidade futura.

## 3. Processamento dos Dados

### - Análise de Sentimentos (Processamento de Linguagem Natural)

- Uso da biblioteca de NLP (como NLTK, TextBlob ou APIs de NLP) para classificar os comentários como positivos, negativos ou neutros.
- Medir o nível de aceitação e negação com base na frequência e intensidade das opiniões positivas e negativas em cada vídeo.
- Análise de Engajamento:
- Curtidas por Visualização: Calcular a relação de curtidas em relação às visualizações para cada vídeo.
- Duração x Curtidas x Visualizações: Comparar a duração do vídeo com a quantidade de curtidas e visualizações para ver se vídeos mais curtos ou mais longos têm mais engajamento.
- Horário de Postagem x Curtidas e Visualizações: Analisar como o horário de publicação influencia o engajamento para encontrar horários ideais para postar.

## 4. Clusterização dos Vídeos (KMeans)

Definir os clusters: Usar o algoritmo de clusterização KMeans para agrupar vídeos com características similares (como visualizações, curtidas, duração, e sentimentos).

### - Parâmetros para clusterização

Quantidade de visualizações, curtidas, sentimento dos comentários e duração.

- Identificar padrões de engajamento em cada cluster para determinar quais grupos de vídeos (e quadros) têm menor engajamento em comparação aos demais.

## 5. Conclusão

Identificar Quadros de Menor Engajamento: Com base na clusterização, observar quais quadros estão em clusters de menor engajamento.
Recomendações: Sugerir estratégias como mudanças no horário de postagem, ajustes na duração dos vídeos ou melhorias no conteúdo para aumentar o engajamento dos quadros menos populares.