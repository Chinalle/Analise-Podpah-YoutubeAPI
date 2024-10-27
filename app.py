# Importando o modulo cliente que permite fazer a consulta
from googleapiclient.discovery import build

# Salvando a KEY API em uma váriavel
youtubeApiKey = 'AIzaSyAOtagOeO_TyVcBJLIjs5sQogyobUKPr2o'

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

def get_latest_videos(channelId): 
    res = youtube.search().list( 
        part='snippet', 
        channelId=channelId, 
        maxResults=20, 
        order='date', 
        type='video'
    ).execute() 

    videos = [] 
    for item in res['items']: 
        video_id = item['id']['videoId'] 
        title = item['snippet']['title'] 
        videos.append({'video_id': video_id, 'title': title}) 
    return videos 

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
    videos = get_latest_videos(channel_id) 
    filtered_videos = filter_non_shorts(videos)  # Filtra vídeos para evitar shorts

    for video in filtered_videos: 
        stats = video['stats'] 
        print(f"Título: {video['title']}") 
        print(f"URL: https://www.youtube.com/watch?v={video['video_id']}") 
        print(f"Visualizações: {stats['views']}") 
        print(f"Likes: {stats['likes']}") 
        print(f"Comentários: {stats['comments']}") 
        print(f"Duração: {stats['duration']}")  # Mostra a duração no formato ISO 8601
        print("="*50) 

main()