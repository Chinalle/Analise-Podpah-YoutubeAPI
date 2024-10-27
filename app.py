# Importando o modulo cliente que permite fazer a consulta
from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Obtendo a API key do .env
youtubeApiKey = os.getenv('YOUTUBE_API_KEY')

# Build é um recurso para interagir com a API
# Argumentos: NomeServiço, versão, API KEY
youtube = build('youtube', 'v3', developerKey=youtubeApiKey)

# Nome do canal do Youtube
channel_name = "Podpah"
# Função que retorna o id do canal através do nome
def get_channel_id(channel_name): 
    # Variavel res é um dicinário que vai armazenar todas as propriedades do canal buscada
    # A função search.list vai retornar as propriedades
    # O argumento part recebendo o valor snippet, traz todos os parâmetros
    # O q é o termo de busca, nesse caso o nome do canal
    # Type especifica o tipo da busca, pode ser para videos ou playlist também
    # maxResults limita a busca 
    res = youtube.search().list( 
        part='snippet', 
        q=channel_name, 
        type='channel', 
        maxResults=1 
    ).execute() 
    # Verifica se a algum item dentro da lista items que se encontra no dicionario res
    if res['items']: 
        # Retorna o channelId
        # [Items][0] é o primeiro valor dentro da lista items
        # O primeiro valor da list items ([Items][0]) é o dicionario snippet
        return res['items'][0]['snippet']['channelId'] 
    else: 
        return None 

# Executando a função e armazenando o valor dentro dele
channel_id = get_channel_id(channel_name) 


playlistId = "PLaE_mZALZ0V1R6Ztc8W7SeCi_hHtEQ1f2"
playlistName = 'QUERIDO DIÁRIO'
nextPage_token = None

playlist_videos = []

def get_videos_playlist(playlistId):
    # Chamada correta da API com o execute()
    res = youtube.playlistItems().list(
        part='snippet,contentDetails',  # Adiciona 'contentDetails' para incluir o videoId
        playlistId=playlistId,
        maxResults=17
    ).execute()  # Chamando o método execute()

    videos = []
    for item in res['items']:
        video_id = item['contentDetails']['videoId']
        title = item['snippet']['title']
        videos.append({'video_id': video_id, 'title': title})

    print(videos)
    return videos

    # Processamento dos itens da resposta
    # for item in res['items']:
    #     title = item['snippet']['title']
    #     video_id = item['snippet']['resourceId']['videoId']
    #     print(f'Título: {title}, URL: https://www.youtube.com/watch?v={video_id}')


# def get_latest_videos(channelId): 
#     res = youtube.search().list( 
#         part='snippet', 
#         channelId=channelId, 
#         #maxResults=999, 
#         order='date', 
#         type='video'
#     ).execute() 

#     videos = [] 
#     for item in res['items']: 
#         video_id = item['id']['videoId'] 
#         title = item['snippet']['title'] 
#         videos.append({'video_id': video_id, 'title': title}) 
#     return videos 

def get_video_stats(video_id): 
    res = youtube.videos().list( 
        part='statistics,contentDetails', 
        id=video_id 
    ).execute() 

    stats = res['items'][0]
    video_stats = stats['statistics']
    duration = stats['contentDetails']['duration'] 
    return { 
        'views': video_stats.get('viewCount', 0), 
        'likes': video_stats.get('likeCount', 0), 
        'comments': video_stats.get('commentCount', 0),
        'duration': duration
    } 

def filter_non_shorts(videos): 
    filtered_videos = []
    for video in videos: 
        stats = get_video_stats(video['video_id']) 
        video_duration = stats['duration']

        if 'PT' in video_duration:
            if 'H' in video_duration or 'M' in video_duration:
                filtered_videos.append({
                    'title': video['title'],
                    'video_id': video['video_id'],
                    'stats': stats
                })
    return filtered_videos 

def main(): 
    videos = get_videos_playlist(playlistId)
    #videos = get_latest_videos(channel_id)
    filtered_videos = filter_non_shorts(videos)  # Filtra vídeos para evitar shorts

    playlist = []

    for video in filtered_videos: 
        stats = video["stats"]
        video_info = {
            'title': video['title'],
            "url": f'https://www.youtube.com/watch?v={video['video_id']}',
            "views": stats["views"],
            "likes": stats["likes"],
            "comments": stats['comments'],
            "duration": stats["duration"]
        }

        playlist.append(video_info)
    
    df = pd.DataFrame(playlist)
    print(df)

    df.to_csv('./df.csv')


main()