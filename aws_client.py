import streamlit as st
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError

# --- PLACEHOLDERS DE AWS ---
AWS_S3_BUCKET_NAME = "tu-bucket-aqui"
AWS_SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789/tu-cola-sqs"

# --- Inicialización de Clientes ---
s3_client = None
sqs_client = None
aws_configured = False

# Esta función se llamará al inicio de CADA app
def init_aws_clients():
    global s3_client, sqs_client, aws_configured
    
    if aws_configured: # No re-inicializar
        return s3_client, sqs_client, aws_configured

    try:
        s3_client = boto3.client('s3')
        sqs_client = boto3.client('sqs')
        
        # Validación (opcional pero recomendada)
        # s3_client.head_bucket(Bucket=AWS_S3_BUCKET_NAME) 
        
        aws_configured = True
        
    except (NoCredentialsError, BotoCoreError, ClientError) as e:
        st.error(f"Error crítico de AWS: No se pudo conectar. {e}")
        aws_configured = False
    except Exception as e:
        st.error(f"Error inesperado de AWS: {e}")
        aws_configured = False
        
    return s3_client, sqs_client, aws_configured