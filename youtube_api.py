import os
import json
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from utils import format_youtube_duration
from aws import upload_to_s3

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
    snippet = stats['snippet']
    duration = stats['contentDetails']['duration']
    publishedAt = stats['snippet']['publishedAt']
    thumbnail = snippet['thumbnails']['high']['url']
    
    return { 
        'views': video_stats.get('viewCount', 0), 
        'likes': video_stats.get('likeCount', 0), 
        'comments': video_stats.get('commentCount', 0),
        'published_at': publishedAt,
        'duration': duration,
        'thumbnail': thumbnail
    } 


def get_video_comments(video_id, max_results=100):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )

    while request:
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'video_id': video_id,
                'comment_text': comment['textDisplay'],
                'like_count': comment['likeCount'],
            })

        request = youtube.commentThreads().list_next(request, response)

    return comments


def save_comments_to_csv(videos, file_name="video_comments.csv"):
    all_comments = []
    
    for video in videos:
        video_id = video['video_id']
        print(f"Buscando comentários do vídeo {video_id}...")
        comments = get_video_comments(video_id)
        all_comments.extend(comments)

    df = pd.DataFrame(all_comments)
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"Comentários salvos em: {file_name}!")



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
              'duration': stats['duration'],
              'thumbnail': stats['thumbnail']
          })

  return videos



videos = get_playlist_videos(playlists_data)
#save_comments_to_csv(videos)

df = pd.DataFrame(videos)
df.to_csv('./videos_data.csv', index=False)

upload_to_s3('videos_data.csv', 'podpahdata', 'raw')

#print(videos)
print(json.dumps(videos, indent=4, ensure_ascii=False))

path = 'videos_data.json'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(videos, f, ensure_ascii=False, indent=4) 
