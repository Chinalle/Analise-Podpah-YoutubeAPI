import boto3
import pandas as pd
from io import StringIO
from botocore.exceptions import NoCredentialsError

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
    except PartialCredentialsError:
        print('Credenciais incompletas.')

def get_bucket_data(bucket_name, file_name):
    global s3

    # Listar objetos no bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        for obj in response['Contents']:
            print(f'Nome: {obj["Key"]}, Última Modificação: {obj["LastModified"]}, Tamanho: {obj["Size"]} bytes')

        # Acessar o objeto específico
        try:
            object_s3 = s3.get_object(Bucket=bucket_name, Key=file_name)
            csv_content = object_s3['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            print('Dados do Bucket S3: \n')
            print(df)
            print()
            print(df.head())
        except s3.exceptions.NoSuchKey:
            print(f'O arquivo {file_name} não foi encontrado no bucket {bucket_name}.')
    else:
        print('O bucket está vazio.')

# teste fora do uso da api do youtube -> utiliza dados diretos do csv salvo no bucket
#get_bucket_data('podpahdata', './df.csv') 
