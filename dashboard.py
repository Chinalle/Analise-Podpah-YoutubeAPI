import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import boto3
import os

# Função para carregar dados do S3
def get_bucket_data(bucket_name, file_name, directory):
    try:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket_name, Key=f"{directory}/{file_name}")
        return pd.read_csv(obj['Body'])
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar arquivo do S3: {e}")

# Função para carregar os dados
def load_data(source='local', file_name=None, bucket_name=None, directory=None):
    try:
        if source == 'local':
            if file_name and os.path.exists(file_name):
                return pd.read_csv(file_name)
            else:
                st.error(f"Arquivo não encontrado: {file_name}")
                return None
        elif source == 's3':
            if bucket_name and directory and file_name:
                return get_bucket_data(bucket_name, file_name, directory)
            else:
                st.error("Configurações para o bucket S3 estão incompletas.")
                return None
        else:
            st.error("Fonte de dados inválida. Escolha entre 'local' ou 's3'.")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

# Configurar título da dashboard
st.title("Dashboard de Dados do Podpah")

# Sidebar para carregar os dados
st.sidebar.title("Carregar Dados")
data_source = st.sidebar.selectbox("Escolha a fonte dos dados:", ["local", "s3"])

if data_source == "s3":
    bucket = st.sidebar.text_input("Informe o nome do bucket S3:", value="podpahdata")
    directory = st.sidebar.text_input("Informe o diretório no bucket:", value="raw")
    file_name = st.sidebar.text_input("Informe o nome do arquivo:", value="video_data.csv")
    data = load_data(source="s3", file_name=file_name, bucket_name=bucket, directory=directory)
else:
    file_name = st.sidebar.text_input("Informe o caminho do arquivo local:", value="video_data.csv")
    data = load_data(source="local", file_name=file_name)

# Criar abas para separação de funcionalidades
tabs = st.tabs(["Visão Geral", "Gráficos", "K-Means (em breve)"])

# Aba: Visão Geral
with tabs[0]:
    st.header("Visão Geral dos Dados")

    if data is not None:
        # Filtro por playlist
        if 'playlist_title' in data.columns:
            playlist_filter = st.multiselect("Filtrar por Playlist:", data['playlist_title'].unique(), default=data['playlist_title'].unique())
            data = data[data['playlist_title'].isin(playlist_filter)]

        # Garantir que temos uma métrica de engajamento
        if 'views' in data.columns and 'likes' in data.columns and 'comments' in data.columns:
            data['engagement'] = data['likes'] + data['comments']  # Exemplo de métrica de engajamento

            # Dividir os dois carrosséis em blocos lado a lado
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Vídeos com Mais Engajamento")
                top_videos = data.sort_values('engagement', ascending=False).head(10).reset_index()
                top_index = st.slider("Selecione o Vídeo (Mais Engajados):", 0, len(top_videos) - 1, 0, key="top_carousel")
                video = top_videos.iloc[top_index]
                st.image(video.get('thumbnail', 'https://via.placeholder.com/150'), width=300)
                st.write(f"**Título:** {video['title']}")
                st.write(f"**Engajamento:** {video['engagement']} (Likes: {video['likes']}, Comentários: {video['comments']})")
                st.write(f"**Visualizações:** {video['views']}")

            with col2:
                st.subheader("Vídeos com Menos Engajamento")
                low_videos = data.sort_values('engagement', ascending=True).head(10).reset_index()
                low_index = st.slider("Selecione o Vídeo (Menos Engajados):", 0, len(low_videos) - 1, 0, key="low_carousel")
                video = low_videos.iloc[low_index]
                st.image(video.get('thumbnail', 'https://via.placeholder.com/150'), width=300)
                st.write(f"**Título:** {video['title']}")
                st.write(f"**Engajamento:** {video['engagement']} (Likes: {video['likes']}, Comentários: {video['comments']})")
                st.write(f"**Visualizações:** {video['views']}")

        # Exibir os dados abaixo dos carrosséis
        st.subheader("Dados Carregados")
        st.dataframe(data)

    else:
        st.warning("Nenhum dado carregado. Verifique as configurações na barra lateral.")
