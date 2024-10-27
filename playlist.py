from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Obtendo a API key do .env
youtubeApiKey = os.getenv('YOUTUBE_API_KEY')

# Build é um recurso para interagir com a API
# Argumentos: NomeServiço, versão, API KEY
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
