from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv
from utils import format_youtube_duration
import json

load_dotenv()
youtubeApiKey = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=youtubeApiKey)

channel_name = "Podpah"
def get_channel_id(channel_name): 
    # Variavel res é um dicinário que vai armazenar todas as propriedades do canal buscada
    # A função search.list vai retornar as propriedades
    # O argumento part recebendo o valor snippet, traz todos os parâmetros
    # O q é o termo de busca, nesse caso o nome do canal
    # Type especifica o tipo da busca, pode ser para videos ou playlist também
    # maxResults limita a busca 
    request = youtube.search().list( 
        part='snippet', 
        q=channel_name, 
        type='channel', 
        maxResults=1
    ).execute() 
    # Verifica se a algum item dentro da lista items que se encontra no dicionario request
    if request['items']: 
        # Retorna o channelId
        # [Items][0] é o primeiro valor dentro da lista items
        # O primeiro valor da list items ([Items][0]) é o dicionario snippet
        return request['items'][0]['snippet']['channelId'] 
    else: 
        return None 
channel_id = get_channel_id(channel_name)


def get_playlists(id):
  data_playlist = []

  request = youtube.playlists().list(
    part="snippet, contentDetails",
    channelId=id,
    maxResults=10
  )

  response = request.execute()

  playlists = response['items']

  for playlist in playlists:
    snippet = playlist['snippet']

    if snippet['title'] not in ['ESPECIAIS PODPAH', 'PODPAH PODCAST']:
          data_playlist.append({
        "Playlist ID": playlist['id'],
        "Titulo": snippet['title'],
        "Descrição": snippet.get('description'),
        "Data de publicação": snippet['publishedAt'],
        "Canal": snippet['channelTitle'],
        "Thumbnail": snippet['thumbnails']['high']['url']
      })

  #print(data_playlist)
  #df = pd.DataFrame(data_playlist)
  #print(df)
  return data_playlist

playlists_data = get_playlists(channel_id)

def get_video_stats(video_id): 
    res = youtube.videos().list( 
        part='statistics, contentDetails, snippet', 
        id=video_id 
    ).execute() 

    stats = res['items'][0]
    video_stats = stats['statistics']
    duration = stats['contentDetails']['duration']
    publishedAt = stats['snippet']['publishedAt']
    return { 
        'views': video_stats.get('viewCount', 0), 
        'likes': video_stats.get('likeCount', 0), 
        'comments': video_stats.get('commentCount', 0),
        'published_at': publishedAt,
        'duration': duration
    } 

def get_playlist_videos(playlists):
  videos = []

  for playlist in playlists:
      request = youtube.playlistItems().list(
          part='snippet, contentDetails',
          playlistId=playlist['Playlist ID'],
          maxResults=20
      ).execute()
      
      playlist_title = playlist['Titulo']

      for item in request['items']:
          video_id = item['contentDetails']['videoId']
          title = item['snippet']['title']
          published_at = item['snippet']['publishedAt']

          stats = get_video_stats(video_id)

          videos.append({
              'playlist_title': playlist_title, 
              'video_id': video_id,
              'title': title,
              'views': stats['views'],
              'likes': stats['likes'],
              'comments': stats['comments'],
              'published_at': stats['published_at'],
              'duration': stats['duration']
          })

  return videos

#exemplo do retorno da função
# [
#     {
#         "playlist_title": "PODPAQUERA",
#         "video_id": "-rYdWF9Ky2U",
#         "title": "10 MULHERES vs MANOEL GOMES ft. BRINO, MAUMAU & THAIZOCA",
#         "views": "981248",
#         "likes": "58339",
#         "comments": "1014",
#         "published_at": "2024-11-17T23:30:50Z",
#         "duration": "PT1H15M46S"
#     },
#     {
#         "playlist_title": "PODPAQUERA",
#         "video_id": "Ek4hPjbv0zY",
#         "title": "5 MULHERES + 5 HOMENS vs SOFIA SANTINO ft. DOARDA E CICLOPIN",
#         "views": "1914177",
#         "likes": "137858",
#         "comments": "794",
#         "published_at": "2024-11-03T22:56:48Z",
#         "duration": "PT52M55S"
#     },
#     {
#         "playlist_title": "PODPAQUERA",
#         "video_id": "lE2JZYBnQUA",
#         "title": "10 MULHERES vs MC TUTO ft. MC JOÃOZINHO VT, MAUMAU, THAIZOCA & MITICO",
#         "views": "1741456",
#         "likes": "85680",
#         "comments": "495",
#         "published_at": "2024-10-20T23:26:19Z",
#         "duration": "PT54M35S"
#     },
#     {
#         "playlist_title": "PODPAQUERA",
#         "video_id": "w_eWmUgqHLU",
#         "title": "10 MULHERES vs MITICO ft. BRINO, MAUMAU & THAIZOCA",
#         "views": "3107523",
#         "likes": "201981",
#         "comments": "1889",
#         "published_at": "2024-09-28T02:40:44Z",
#         "duration": "PT1H34M25S"
#     },
#     {
#         "playlist_title": "PODPAH EM PARIS",
#         "video_id": "ptFxlxNo51M",
#         "title": "ENTREVISTA COM ISAQUIAS QUEIROZ & DEFANTE NA MASSAGEM - PODPAH EM PARIS #18",
#         "views": "461197",
#         "likes": "14821",
#         "comments": "18",
#         "published_at": "2024-08-11T23:27:54Z",
#         "duration": "PT1H22M31S"
#     },
# ]

videos = get_playlist_videos(playlists_data)
#print(videos)
print(json.dumps(videos, indent=4, ensure_ascii=False))

# path = 'videos_full_data.json'
# with open(path, 'w', encoding='utf-8') as f:
#   json.dump(videos, f, ensure_ascii=False, indent=4) 

