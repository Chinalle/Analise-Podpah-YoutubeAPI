import boto3
from datetime import datetime
import pandas as pd
from io import StringIO
from botocore.exceptions import NoCredentialsError
from sagemaker.predictor import Predictor
import json

s3 = boto3.client('s3') # instanciando armazenamento do aws s3 para dados não estruturados

def upload_to_s3(file_name, bucket, directory): # o file_name salva o arquivo exatamente como foi descrito no parametro 1 da função

    object_name = f"{directory}/{file_name.split('/')[-1]}" 

    try:
        s3.upload_file(file_name, bucket, object_name)
        print(f'Upload de {file_name} para s3://{bucket}/{object_name} realizado com sucesso!')
        
    except FileNotFoundError:
        print(f'O arquivo {file_name} não foi encontrado.')
    except NoCredentialsError:
        print('Credenciais não disponíveis.')
    except PartialCredentialsError: # type: ignore
        print('Credenciais incompletas.')

def get_bucket_data(bucket_name, file_name,directory):
    global s3
    object_name = f"{directory}/{file_name.split('/')[-1]}"
    
    object_name = f"{directory}/{file_name.split('/')[-1]}" 
    # Listar objetos no bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        #for obj in response['Contents']:
            #print(f'Nome: {obj["Key"]}, Última Modificação: {obj["LastModified"]}, Tamanho: {obj["Size"]} bytes')

        # Acessar o objeto específico
        try:
            object_s3 = s3.get_object(Bucket=bucket_name, Key=object_name)
            object_s3 = s3.get_object(Bucket=bucket_name, Key=object_name)
            csv_content = object_s3['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            
            print('Dados do Bucket S3: \n')
            #print(df)
            #print(df.head())
            return df
        except s3.exceptions.NoSuchKey:
            print(f'O arquivo {file_name} não foi encontrado no bucket {bucket_name}.')
    else:
        print('O bucket está vazio.')

# teste fora do uso da api do youtube -> utiliza dados diretos do csv salvo no bucket
#bucket_data = get_bucket_data('podpahdata', 'video_data.csv', 'raw')


endpoints = {
    "views": "sagemaker-xgboost-2024-12-11-00-55-20-339",
    "likes": "sagemaker-xgboost-2024-12-11-00-59-52-578",
    "engagement": "sagemaker-xgboost-2024-12-11-01-04-55-149",
}

data = {
    "playlist_title": 1,  # Código da categoria do título da playlist
    "day_of_week": 2,     # Dia da semana (0 = Segunda, ..., 6 = Domingo)
    "hour": 15,           # Hora do dia (formato 24 horas)
    "duration": 3600      # Duração do vídeo em segundos
}

def predict_all_endpoints(data, endpoints, region="us-east-1"):
    """
    Faz chamadas aos endpoints do SageMaker para obter previsões de Views, Likes e Engagement.
    
    :param data: Dados no formato JSON para a predição
    :param endpoints: Dicionário com os nomes dos endpoints
                      {"views": "endpoint-views-name",
                       "likes": "endpoint-likes-name",
                       "engagement": "endpoint-engagement-name"}
    :param region: Região da AWS onde os endpoints estão configurados
    :return: Dicionário com as previsões
    """
    # Cliente do SageMaker Runtime
    runtime = boto3.client("sagemaker-runtime", region_name=region)
    
    # Converter o dicionário 'data' para um DataFrame do Pandas
    endpoint_df = pd.DataFrame([data])
    
    # Converter o DataFrame para CSV (sem índice)
    csv_payload = endpoint_df.to_csv(index=False, header=False)
    
    predictions = {}
    
    # Loop pelos endpoints
    for key, endpoint_name in endpoints.items():
        try:
            response = runtime.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType="text/csv",  # Ajustado para CSV
                Body=csv_payload,
            )
            predictions[key] = json.loads(response["Body"].read().decode())
        except Exception as e:
            predictions[key] = f"Erro: {str(e)}"
    
    return predictions

response = predict_all_endpoints(data, endpoints)

# Exibir a resposta formatada
print(json.dumps(response, indent=4, ensure_ascii=False))

# Salvar a resposta em um arquivo JSON
file = 'endpoint.json'
with open(file, 'w', encoding='utf-8') as f:
    json.dump(response, f, ensure_ascii=False, indent=4)