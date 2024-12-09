import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame 
from pyspark.sql.functions import to_timestamp, udf, year, month, col
import re
from datetime import timedelta
import logging

# Configuração inicial do Glue Job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Função para converter a duração ISO 8601 para segundos 
def duration_to_seconds(duration):
    # Expressão regular para capturar partes da duração (horas, minutos, segundos)
    regex = r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
    match = re.match(regex, duration)
    
    if not match:
        return None 
    
    # Extraindo as partes da duração
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    
    # Convertendo para segundos
    total_seconds = timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds()
    return int(total_seconds)

# Leitura dos dados brutos do bucket S3
S3bucket_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="podpahdata_db", 
    table_name="raw", 
    transformation_ctx="S3bucket_node1"
)

# Conversão de DynamicFrame para DataFrame
df = S3bucket_node1.toDF()

# Registro de função UDF para conversão de duração
udf_duration_to_seconds = udf(duration_to_seconds, "int")

# Transformações no DataFrame
df = (
    df.withColumn("published_at", to_timestamp("published_at", "yyyy-MM-dd'T'HH:mm:ss'Z'"))  # Conversão para timestamp
      .withColumn("duration", udf_duration_to_seconds("duration"))  # Conversão de duration para segundos
      .fillna({"views": 0, "likes": 0, "comments": 0})  # Preenchimento de valores nulos em métricas numéricas
      .withColumn("year", year("published_at"))  # Extração do ano
      .withColumn("month", month("published_at"))  # Extração do mês
      .withColumn("engagement_rate", (col("likes") + col("comments")) / col("views"))  # Possivel cálculo de taxa de engajamento
)

# Conversão de volta para DynamicFrame
processed_frame = DynamicFrame.fromDF(df, glueContext, "processed_frame")

# Escrita dos dados transformados no bucket S3 (diretório processed)
glueContext.write_dynamic_frame.from_options(
    frame=processed_frame,
    connection_type="s3",
    format="parquet",
    connection_options={
        "path": "s3://podpahdata/processed/",
        "partitionKeys": []
    },
    transformation_ctx="S3bucketprocessed"
)

# Finalização do job
job.commit()
