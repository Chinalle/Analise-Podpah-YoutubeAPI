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
            
            videos.append({
                'playlist_title': playlist_title, 
                'video_id': video_id,
                'title': title,
                'published_at': published_at
            })
    
    return videos


def get_playlist_videos(playlists):
  videos = []  # Lista para armazenar os dados dos vídeos

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






def get_playlist_videos(playlists):
  videos = {}
  for playlist in playlists:
    #videos.append(playlist['Playlist ID'])

    request = youtube.playlistItems().list(
    part='snippet, contentDetails',
    playlistId=playlist['Playlist ID'],
    maxResults=20
    ).execute() 
    
    playlist_title = playlist['Titulo']

    if playlist_title not in videos:
      videos[playlist_title] = []

    for item in request['items']:
      video_id = item['contentDetails']['videoId']
      title = item['snippet']['title']
      published_at = item['snippet']['publishedAt']

      videos[playlist_title].append({
        'video_id': video_id,
        'title': title,
        'published_at': published_at
      })



  return videos


""" exemplo de retorno da função 
{
    "Nome da Playlist 1": [
        {
            "video_id": "abc123",
            "title": "Título do Vídeo 1",
            "published_at": "2024-01-01T12:00:00Z"
        },
        {
            "video_id": "def456",
            "title": "Título do Vídeo 2",
            "published_at": "2024-01-02T12:00:00Z"
        }
    ],
    "Nome da Playlist 2": [
        {
            "video_id": "ghi789",
            "title": "Título do Vídeo 3",
            "published_at": "2024-01-03T12:00:00Z"
        }
    ]
}
"""

videos = get_playlist_videos(playlists_data)
#print(videos)
print(json.dumps(videos, indent=4, ensure_ascii=False))

# path = 'videos_by_playlist_data.json'
# with open(path, 'w', encoding='utf-8') as f:
#   json.dump(videos, f, ensure_ascii=False, indent=4) 

