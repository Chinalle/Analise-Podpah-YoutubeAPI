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

# Escolher fonte dos dados
data_source = st.selectbox("Escolha a fonte dos dados:", ["local", "s3"])

# Configurações de carregamento de dados
if data_source == "s3":
    bucket = st.text_input("Informe o nome do bucket S3:", value="podpahdata")
    directory = st.text_input("Informe o diretório no bucket:", value="raw")
    file_name = st.text_input("Informe o nome do arquivo:", value="video_data.csv")
    data = load_data(source="s3", file_name=file_name, bucket_name=bucket, directory=directory)
else:
    file_name = st.text_input("Informe o caminho do arquivo local:", value="video_data.csv")
    data = load_data(source="local", file_name=file_name)

# Verificar se os dados foram carregados
if data is not None:
    st.write("### Dados Carregados:")
    st.dataframe(data.head())

    # Garantir que a coluna `published_at` está no formato correto
    if 'published_at' in data.columns:
        data['published_at'] = pd.to_datetime(data['published_at'], errors='coerce')
        data = data.dropna(subset=['published_at'])  # Remove valores inválidos

    # Filtros interativos
    if 'playlist_title' in data.columns:
        playlist_filter = st.multiselect("Filtrar por Playlist:", data['playlist_title'].unique(), default=data['playlist_title'].unique())
        data = data[data['playlist_title'].isin(playlist_filter)]

    date_range = st.date_input("Filtrar por Data de Publicação:", [])
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        data = data[(data['published_at'] >= pd.Timestamp(start_date)) & (data['published_at'] <= pd.Timestamp(end_date))]

    # Verificar se há dados após os filtros
    if not data.empty:
        # Gráficos
        st.write("### Estatísticas por Vídeo")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=data.sort_values('views', ascending=False).head(10), x="views", y="title", ax=ax)
        ax.set_title("Visualizações por Vídeo")
        st.pyplot(fig)

        st.write("### Duração dos Vídeos")
        if 'duration' in data.columns:
            data['duraçao_minutos'] = data['duration'].apply(
                lambda x: int(x.split(":")[1]) + int(x.split(":")[0]) * 60 if ":" in x else 0)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data['duraçao_minutos'], bins=20, kde=True, ax=ax)    
            ax.set_title("Distribuição de Duração dos Vídeos")
            st.pyplot(fig)

        # Exportar dados filtrados
        if st.button("Exportar Dados Filtrados"):
            data.to_csv("filtered_data.csv", index=False)
            st.success("Dados exportados para 'filtered_data.csv'!")
    else:
        st.warning("Nenhum dado disponível após aplicar os filtros.")
else:
    st.warning("Nenhum dado foi carregado. Verifique os inputs.")
