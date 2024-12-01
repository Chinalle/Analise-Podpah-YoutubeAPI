from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv
from utils import format_youtube_duration
from aws import s3, upload_to_s3
from youtube_api import get_playlists, playlists_data, youtubeApiKey, youtube


# tratando retorno: recebe um array com as informações das playlists do canal Podpah, para automatizar o processo de recuperar o id e nome das playlists



playlistId = "PLaE_mZALZ0V1R6Ztc8W7SeCi_hHtEQ1f2"
playlistName = 'QUERIDO DIÁRIO'

nextPage_token = None
playlist_videos = []

def get_videos_playlist(playlistId):
    res = youtube.playlistItems().list(
        part='snippet, contentDetails',  # Adiciona 'contentDetails' para incluir o videoId
        playlistId=playlistId,
        maxResults=17
    ).execute() 

    videos = []
    for item in res['items']:
        video_id = item['contentDetails']['videoId']
        title = item['snippet']['title']
        published_at = item['snippet']['publishedAt']
        videos.append({'video_id': video_id, 'title': title, 'published_at': published_at})

    #print(videos)
    #return videos


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
            'published_at': stats['published_at'],
            "duration": format_youtube_duration(stats["duration"])
        }

        playlist.append(video_info)

    df = pd.DataFrame(playlist)

    #print(df)


    df.to_csv('./df.csv', index=False)
    #upload_to_s3('df_querido_diario', 'podpahdata')


if __name__ == __main__:
    main()