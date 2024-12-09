import boto3
import emoji
import pandas as pd
import concurrent.futures
from aws import get_bucket_data, upload_to_s3

# Configurando o cliente Comprehend
comprehend = boto3.client('comprehend', region_name='us-east-1')

df_video_comments = pd.read_csv(get_bucket_data('podpahdata', 'video_comments.csv','raw/video_comments'))

# Adiciona as colunas 'Sentiment' e 'SentimentScore'
df_resultado_final = df_video_comments.assign(Sentiment=None, SentimentScore=None)

# Função para processar cada comentário
def process_comment(index, texto):
    texto_sem_emoji = emoji.replace_emoji(str(texto), replace='')
    print(f'comentario {index}')
    # Verifica se o texto não está vazio
    if len(texto_sem_emoji.strip()) > 0:
        resposta = comprehend.detect_sentiment(Text=texto_sem_emoji, LanguageCode='pt')
        sentiment = resposta['Sentiment']
        sentiment_score = None
        if sentiment == 'POSITIVE':
            sentiment_score = resposta['SentimentScore']['Positive']
        elif sentiment == 'NEGATIVE':
            sentiment_score = resposta['SentimentScore']['Negative']
        elif sentiment == 'NEUTRAL':
            sentiment_score = resposta['SentimentScore']['Neutral']
        elif sentiment == 'MIXED':
            sentiment_score = resposta['SentimentScore']['Mixed']
        return index, sentiment, sentiment_score
    else:
        return index, 'SEM COMENTARIO', None

# Usando ThreadPoolExecutor para executar as requisições em paralelo
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Envia as requisições em paralelo com os índices
    resultados = list(executor.map(lambda args: process_comment(*args), enumerate(df_resultado_final['comment_text'])))

# Atualiza o DataFrame com os resultados
for index, sentiment, sentiment_score in resultados:
    df_resultado_final.at[index, 'Sentiment'] = sentiment
    df_resultado_final.at[index, 'SentimentScore'] = sentiment_score

df_resultado_final = df_resultado_final.query('Sentiment != "SEM COMENTARIO"')
df_resultado_final.to_csv('SentimentScoreFinal.csv', index=False)


