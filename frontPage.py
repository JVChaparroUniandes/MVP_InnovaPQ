import streamlit as st
import uuid
import json
from botocore.exceptions import ClientError
# Importamos la función de inicialización y variables
from aws_client import (
    init_aws_clients,
    AWS_S3_BUCKET_NAME, 
    AWS_SQS_QUEUE_URL
)

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Carga de Reportes PQ",
    layout="centered"
)

# --- Inicializar Clientes de AWS ---
s3_client, sqs_client, aws_configured = init_aws_clients()

st.title("Generador de Reportes de Calidad de Energía (MVP)")
st.write("Sube los archivos de entrada para iniciar el procesamiento.")

# --- 1. Definir los archivos que necesitamos ---
# Usamos un diccionario para organizar los campos del formulario
# (key: descripción)
file_definitions = {
    "info_carga": "Información centro de carga",
    "desc_carga": "Descripción centro de carga",
    "info_medidor": "Información del medidor",
    "datos_medicion": "Datos de medición en el punto",
    "diagrama": "Diagrama Unifilar",
    "stamp": "Sello (Stamp)",
    "main_data": "Archivo Principal de Datos (CSV, PQDIF, etc.)"
}

# Diccionario para guardar los archivos subidos
file_uploads = {}

with st.form(key="report_form",clear_on_submit=True,enter_to_submit=False):
    st.header("1. Información del Usuario")
    user_email = st.text_input(
        "Tu Correo Electrónico", 
        help="Recibirás un enlace al reporte en este correo."
    )
    
    st.header("2. Metadata del reporte")
    
    # --- 2. Crear los uploaders dinámicamente ---
    # Esto es más limpio si tienes muchos archivos
    ##col1= st.columns(1)
    ##with col1:
    with st.container():
        st.subheader(file_definitions["info_carga"])
        info_carga_empresa=st.text_input("Empresa")
        info_carga_direccion=st.text_input("Direccion")
        info_carga_responsable=st.text_input("Responsable de equipo")
    with st.container():
        st.subheader(file_definitions["desc_carga"])
        desc_carga_actividades=st.text_input("Descripción de actividades del centro de carga")
        desc_carga_punto=st.text_input("Nombre del punto de medición")
        desc_carga_carga=st.text_input("Descripción general de la carga")

    with st.container():
        st.subheader(file_definitions["info_medidor"])
        opciones_medidor=("Schneider ION-9000")
        info_medidor_marca=st.selectbox(label="Medidor",options=opciones_medidor)
        opciones_clase=("A")
        info_medidor_clase=st.selectbox(label="Clase",options=opciones_clase)
        opciones_tasa=("1 minuto","5 minutos","10 minutos","15 minutos")
        info_medidor_tasa=st.selectbox(label="Tasa de muestreo",options=opciones_tasa)
    
    with st.container():
        st.subheader(file_definitions["datos_medicion"])
        opciones_frecuencia=("60 Hz","50 Hz")
        datos_medicion_frecuencia=st.selectbox(label="frecuencia del sistema",options=opciones_frecuencia)

        opciones_unidades_voltaje=("V","kV")
        with st.container(horizontal=True):
            tension_suministro=st.text_input("Tensión de suministro")
            unidades_suministro=st.selectbox("Unidad",options=opciones_unidades_voltaje,key="unidades_suministro")
            datos_medicion_tension_suministro=f'{tension_suministro} {unidades_suministro}'

        with st.container(horizontal=True):
            tension_punto=st.text_input("Tensión de punto de medición")
            unidades_punto=st.selectbox("Unidad",options=opciones_unidades_voltaje,key="unidades_punto")
            datos_medicion_tension_punto=f'{tension_punto} {unidades_punto}'
        
        opciones_unidades_demanda=("W","kW","MW")
        with st.container(horizontal=True):
            demanda=st.text_input("Demanda contratada")
            unidades_demanda=st.selectbox("Unidad",options=opciones_unidades_demanda)
            datos_medicion_demanda=f'{demanda} {unidades_demanda}'

        opciones_unidades_corriente_d=("A")
        with st.container(horizontal=True):
            corriente_demanda=st.text_input("Corriente demanda máxima contratada")
            unidades_corriente_d=st.selectbox("Unidad",options=opciones_unidades_corriente_d)
            datos_medicion_corriente_demanda=f'{corriente_demanda} {unidades_corriente_d}'

        opciones_unidades_corriente_cc=("kA")
        with st.container(horizontal=True):
            corriente_cc=st.text_input("Corriente de corto circuito")
            unidades_corriente_cc=st.selectbox("Unidad",options=opciones_unidades_corriente_cc)
            datos_medicion_corriente_demanda=f'{corriente_cc} {unidades_corriente_cc}'

        datos_medicion_transformador=st.text_input("Transformador del tablero")

        opciones_temporalidad=("Diaria","Semanal","Mensual","Anual")
        datos_medicion_temporalidad=st.selectbox(label="Temporalidad de medición",options=opciones_temporalidad)

        datos_medicion_fecha_inicio=st.date_input(label="Fecha de medición inicial")
        datos_medicion_fecha_final=st.date_input(label="Fecha de medición final")

    with st.container():
        st.subheader("Diagrama unifilar")
        file_uploads["diagrama"] = st.file_uploader(file_definitions["diagrama"],type=["png", "jpg", "jpeg", "pdf"])

    with st.container():
        st.subheader("Sello")
        file_uploads["stamp"] = st.file_uploader(file_definitions["stamp"], type=["png", "jpg", "jpeg"])

    
    st.header("3. Archivo Principal de Datos")
    file_uploads["main_data"] = st.file_uploader(
        file_definitions["main_data"], 
        type=["csv", "pqd", "pqdif"]
    )

    submit_button = st.form_submit_button(label="Iniciar Procesamiento")

# --- 3. Lógica de Procesamiento (Más limpia) ---
if submit_button:
    
    # --- Validación ---
    if not user_email:
        st.error("Por favor, ingresa tu correo electrónico.")
    elif not all(file_uploads.values()):
        # Revisa si algún valor en el diccionario es None
        st.error("Por favor, sube todos los 7 archivos requeridos.")
    elif not aws_configured:
        st.error("Error: La configuración de AWS no es válida. Revisa las credenciales.")
    else:
        # ¡Todo listo para procesar!
        report_id = str(uuid.uuid4())
        s3_prefix = f"reports/{report_id}/inputs/"

        with st.spinner(f"Procesando reporte... ID: {report_id}"):
            try:
                # --- Subida a S3 (Ahora en un loop) ---
                st.write(f"Creando carpeta en S3: {s3_prefix}")
                
                for key, file_obj in file_uploads.items():
                    # Usamos el nombre original del archivo para guardarlo
                    file_name = file_obj.name
                    s3_key = f"{s3_prefix}{file_name}"
                    
                    st.write(f"Subiendo {file_name} a S3...")
                    s3_client.upload_fileobj(file_obj, AWS_S3_BUCKET_NAME, s3_key)
                
                st.write("Archivos subidos a S3 exitosamente.")

                # --- Envío de Mensaje SQS ---
                message_body = {
                    "report_id": report_id,
                    "user_email": user_email,
                    "s3_input_prefix": s3_prefix,
                    "s3_output_prefix": f"reports/{report_id}/outputs/" 
                }
                
                sqs_client.send_message(
                    QueueUrl=AWS_SQS_QUEUE_URL,
                    MessageBody=json.dumps(message_body)
                )
                
                st.write("Mensaje enviado a SQS para activar la Lambda.")
                st.success(f"¡Procesamiento iniciado con éxito! (ID: {report_id})")
                st.info(f"Recibirás un correo en {user_email} con el enlace a tus resultados.")
                st.balloons()

            except ClientError as e:
                st.error(f"Error de AWS durante la operación: {e}")
            except Exception as e:
                st.error(f"Ocurrió un error inesperado: {e}")