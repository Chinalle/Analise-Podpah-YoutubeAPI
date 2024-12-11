import os
import boto3
import pandas as pd
import sagemaker
from sagemaker import get_execution_role
from sagemaker.image_uris import retrieve
from sklearn.model_selection import train_test_split
from sklearn.datasets import dump_svmlight_file
from dotenv import load_dotenv

# Configuração inicial
session = boto3.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_ACCES_KEY"),
    region_name=os.getenv("REGION")
)

s3_client = session.client('s3')

bucket_name = "podpahdata"
file_key = "processed/part-00000-0a3af50d-d167-4356-abf0-969684c9398f-c000.snappy.parquet"

s3_client.download_file(bucket_name, file_key, "processed_data.parquet")

# Carregar os dados
data = pd.read_parquet("processed_data.parquet")

# Exibir os primeiros registros
print(data.head())
data['published_at'] = pd.to_datetime(data['published_at'])
data['hour'] = data['published_at'].dt.hour
data['day_of_week'] = data['published_at'].dt.dayofweek

# Taxa de engajamento com tratamento para divisão por zero
data['engagement_rate'] = (data['likes'] + data['comments']) / data['views'].replace(0, pd.NA)

# Codificar playlist_title
data['playlist_title'] = data['playlist_title'].astype('category').cat.codes

# Selecionar variáveis preditoras e alvos
X = data[['playlist_title', 'day_of_week', 'hour', 'duration']]
y_views = data['views']
y_likes = data['likes']
y_engagement = data['engagement_rate']

# Dividir os dados
X_train, X_test, y_views_train, y_views_test = train_test_split(X, y_views, test_size=0.2, random_state=42)
_, _, y_likes_train, y_likes_test = train_test_split(X, y_likes, test_size=0.2, random_state=42)
_, _, y_engagement_train, y_engagement_test = train_test_split(X, y_engagement, test_size=0.2, random_state=42)

# Salvar em formato LIBSVM
dump_svmlight_file(X_train, y_views_train, "X_train_views_libsvm.txt")
dump_svmlight_file(X_test, y_views_test, "X_test_views_libsvm.txt")
dump_svmlight_file(X_train, y_likes_train, "X_train_likes_libsvm.txt")
dump_svmlight_file(X_test, y_likes_test, "X_test_likes_libsvm.txt")
dump_svmlight_file(X_train, y_engagement_train, "X_train_engagement_libsvm.txt")
dump_svmlight_file(X_test, y_engagement_test, "X_test_engagement_libsvm.txt")

# Upload dos arquivos para S3
s3_client.upload_file("X_train_views_libsvm.txt", bucket_name, "train/X_train_views_libsvm.txt")
s3_client.upload_file("X_test_views_libsvm.txt", bucket_name, "test/X_test_views_libsvm.txt")
s3_client.upload_file("X_train_likes_libsvm.txt", bucket_name, "train/X_train_likes_libsvm.txt")
s3_client.upload_file("X_test_likes_libsvm.txt", bucket_name, "test/X_test_likes_libsvm.txt")
s3_client.upload_file("X_train_engagement_libsvm.txt", bucket_name, "train/X_train_engagement_libsvm.txt")
s3_client.upload_file("X_test_engagement_libsvm.txt", bucket_name, "test/X_test_engagement_libsvm.txt")

# Configuração SageMaker
role = get_execution_role()
session = sagemaker.Session()
xgboost_container = retrieve("xgboost", session.boto_region_name, version="1.3-1")

# Treinamento do modelo para Views
train_input_views = f"s3://{bucket_name}/train/X_train_views_libsvm.txt"
test_input_views = f"s3://{bucket_name}/test/X_test_views_libsvm.txt"

xgb_views = sagemaker.estimator.Estimator(
    image_uri=xgboost_container,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket_name}/ML_Model/views/",
    sagemaker_session=sagemaker.Session(),
)

xgb_views.set_hyperparameters(
    objective="reg:squarederror",
    num_round=100,
    max_depth=5,
    eta=0.2,
    subsample=0.8,
)

xgb_views.fit({"train": train_input_views, "validation": test_input_views})

# Treinamento do modelo para Likes
train_input_likes = f"s3://{bucket_name}/train/X_train_likes_libsvm.txt"
test_input_likes = f"s3://{bucket_name}/test/X_test_likes_libsvm.txt"

xgb_likes = sagemaker.estimator.Estimator(
    image_uri=xgboost_container,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket_name}/ML_Model/likes/",
    sagemaker_session=sagemaker.Session(),
)

xgb_likes.set_hyperparameters(
    objective="reg:squarederror",
    num_round=100,
    max_depth=5,
    eta=0.2,
    subsample=0.8,
)

xgb_likes.fit({"train": train_input_likes, "validation": test_input_likes})

# Treinamento do modelo para Engagement Rate
train_input_engagement = f"s3://{bucket_name}/train/X_train_engagement_libsvm.txt"
test_input_engagement = f"s3://{bucket_name}/test/X_test_engagement_libsvm.txt"

xgb_engagement = sagemaker.estimator.Estimator(
    image_uri=xgboost_container,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket_name}/ML_Model/engagement/",
    sagemaker_session=sagemaker.Session(),
)

xgb_engagement.set_hyperparameters(
    objective="reg:squarederror",
    num_round=100,
    max_depth=5,
    eta=0.2,
    subsample=0.8,
)

xgb_engagement.fit({"train": train_input_engagement, "validation": test_input_engagement})

# Deploy dos modelos
predictor_views = xgb_views.deploy(initial_instance_count=1, instance_type="ml.m5.large")
predictor_likes = xgb_likes.deploy(initial_instance_count=1, instance_type="ml.m5.large")
predictor_engagement = xgb_engagement.deploy(initial_instance_count=1, instance_type="ml.m5.large")