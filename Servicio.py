import json
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError
import streamlit as st

# --- PLACEHOLDERS DE AWS ---
AWS_S3_BUCKET_NAME = "tu-bucket-aqui"
AWS_SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789/tu-cola-sqs"

# --- Inicialización de Clientes ---
s3_client = None
sqs_client = None
aws_configured = False

class Data:
    def LeerDatos(self):
        data=json.load(open('Servicios/DB_OrigenCodigoRed.json', 'r', encoding='utf-8'))
        return data
    
    def GuardarDatos(self,com1,com3,com4):
        datos={
            "ComentarioNotas":com1,
            "ComentarioImportante":com3,
            "ComentarioPrecaucion":com4
            }
        nombreArchivo='Servicios/DB_ComentariosCodigoRed.json'
        with open(nombreArchivo,'w', encoding='utf-8') as archivo:
            json.dump(datos,archivo,indent=4,ensure_ascii=False)

    # Esta función se llamará al inicio de CADA app
    def init_aws_clients(self,s3_client,sqs_client,aws_configured):
        
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
        
