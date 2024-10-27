from googleapiclient.discovery import build

youtubeApiKey = "AIzaSyAOtagOeO_TyVcBJLIjs5sQogyobUKPr2o"

youtube = build('youtube', 'v3', developerKey=youtubeApiKey)

# Extraindo vídeos de uma playlist
playlistId = "PLaE_mZALZ0V1R6Ztc8W7SeCi_hHtEQ1f2"


playlistName = 'QUERIDO DIÁRIO'
nextPage_token = None

playlist_videos = []

# Chamada correta da API com o execute()
res = youtube.playlistItems().list(
    part='snippet',
    playlistId=playlistId,
    maxResults=15
).execute()  # Chamando o método execute()

# Processamento dos itens da resposta
for item in res['items']:
    title = item['snippet']['title']
    video_id = item['snippet']['resourceId']['videoId']
    print(f'Título: {title}, URL: https://www.youtube.com/watch?v={video_id}')
