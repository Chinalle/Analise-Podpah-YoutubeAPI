from googleapiclient.discovery import build


youtubeApiKey = 'AIzaSyAOtagOeO_TyVcBJLIjs5sQogyobUKPr2o'

youtube = build('youtube', 'v3', developerKey=youtubeApiKey)

channel_name = "Podpah"

def get_channel_id(channel_name): 
    res = youtube.search().list( 
        part='snippet', 
        q=channel_name, 
        type='channel', 
        maxResults=1 
    ).execute() 

    if res['items']: 
        return res['items'][0]['snippet']['channelId'] 
    else: 
        return None 

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