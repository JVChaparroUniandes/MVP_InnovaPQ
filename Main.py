import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import pandas as pd
import uuid
import json
from fpdf import FPDF
import io

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Generador de Reportes PQ",
    layout="wide"
)

# --- PLACEHOLDERS DE AWS ---
# ¡IMPORTANTE! Reemplaza esto con tus valores reales.
# Se recomienda usar variables de entorno o secretos de Streamlit en lugar de hardcodear.
AWS_S3_BUCKET_NAME = "tu-bucket-aqui"
AWS_SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789/tu-cola-sqs"
# Boto3 usará las credenciales de entorno (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
# o un rol de IAM si se despliega en AWS (ej. EC2, Fargate).
try:
    s3_client = boto3.client('s3')
    sqs_client = boto3.client('sqs')
except Exception as e:
    st.error(f"Error inicializando AWS. Asegúrate de tener las credenciales configuradas. {e}")
    s3_client = None
    sqs_client = None


# --- FUNCIÓN DE LA PÁGINA DE REVISIÓN (Paso 5) ---

def create_pdf(report_id, comentario_1, comentario_2, comentario_3, images_urls):
    """
    Genera un PDF simple con los comentarios y (en un futuro) las imágenes.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    
    pdf.cell(200, 10, txt=f"Reporte ID: {report_id}", ln=True, align='C')
    pdf.ln(10)

    # Simulación de imágenes (en la v2, descargaríamos las URLs de S3)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="[Simulación de Gráfica 1 - Voltaje]", ln=True, border=1, align='C')
    pdf.ln(5)
    pdf.cell(200, 10, txt="[Simulación de Gráfica 2 - Armónicos]", ln=True, border=1, align='C')
    pdf.ln(10)

    # Comentarios editados
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Comentarios del Ingeniero", ln=True)
    pdf.set_font("Arial", size=12)
    
    pdf.multi_cell(0, 5, txt=f"Comentario 1: {comentario_1}")
    pdf.ln(5)
    pdf.multi_cell(0, 5, txt=f"Comentario 2: {comentario_2}")
    pdf.ln(5)
    pdf.multi_cell(0, 5, txt=f"Comentario 3: {comentario_3}")
    
    # Devuelve el PDF como bytes
    return pdf.output(dest='S').encode('latin-1')

def show_review_page(report_id):
    """
    Muestra la página de revisión de resultados (Paso 5).
    """
    st.title(f"Revisión del Reporte: {report_id}")
    st.info("Aquí es donde el usuario verá los resultados generados por la Lambda.")
    
    # --- 1. Mostrar Gráficas (Simulación) ---
    st.header("Visualización de Resultados")
    st.warning("MODO DE SIMULACIÓN: En producción, estas gráficas se cargarían desde S3.")
    
    # Estas serían las URLs a las imágenes que la Lambda guardó en S3
    mock_image_url_1 = "https://via.placeholder.com/800x400.png?text=Gráfica+de+Voltaje+(Resultado)"
    mock_image_url_2 = "https://via.placeholder.com/800x400.png?text=Gráfica+de+Armónicos+(Resultado)"
    
    st.image(mock_image_url_1, caption="Análisis de Voltaje (Generado por Lambda)")
    st.image(mock_image_url_2, caption="Análisis de Armónicos (Generado por Lambda)")

    # --- 2. Editar Comentarios ---
    st.header("Comentarios Editables")
    
    # En una v2, estos valores por defecto vendrían de un .txt o .json en S3
    comentario_1 = st.text_area("Comentario 1 (Voltaje)", "El voltaje se mantiene dentro de los límites de la norma XYZ.")
    comentario_2 = st.text_area("Comentario 2 (Armónicos)", "Se detectaron picos de armónicos en el 5to y 7mo orden, superando los límites.")
    comentario_3 = st.text_area("Comentario 3 (Conclusión)", "Se recomienda la instalación de un filtro activo de 100A para mitigar los armónicos.")

    # --- 3. Generar PDF ---
    st.header("Generar PDF")
    
    if st.button("Generar PDF con comentarios actualizados"):
        with st.spinner("Generando PDF..."):
            pdf_bytes = create_pdf(
                report_id, 
                comentario_1, 
                comentario_2, 
                comentario_3, 
                [mock_image_url_1, mock_image_url_2]
            )
            
            st.download_button(
                label="Descargar Reporte en PDF",
                data=pdf_bytes,
                file_name=f"reporte_{report_id}.pdf",
                mime="application/pdf"
            )

# --- FUNCIÓN DE LA PÁGINA DE SUBIDA (Paso 1) ---

def show_input_page():
    """
    Muestra el formulario principal para subir los datos (Paso 1).
    """
    st.title("Generador de Reportes de Calidad de Energía (MVP)")
    st.write("Sube los archivos de entrada para iniciar el procesamiento.")

    with st.form(key="report_form"):
        st.header("1. Información del Usuario")
        user_email = st.text_input(
            "Tu Correo Electrónico", 
            help="Recibirás un enlace al reporte en este correo cuando esté listo (Paso 3)."
        )
        
        st.header("2. Archivos de Configuración (Metadata)")
        
        col1, col2 = st.columns(2)
        with col1:
            info_carga_file = st.file_uploader("Tabla 1 - Información Centro Carga", type=["csv", "xlsx"])
            info_medidor_file = st.file_uploader("Tabla 3 - Información Medidor", type=["csv", "xlsx"])
            diagrama_file = st.file_uploader("Diagrama Unifilar", type=["png", "jpg", "jpeg", "pdf"])
        
        with col2:
            desc_carga_file = st.file_uploader("Tabla 2 - Descripción Centro Carga", type=["csv", "xlsx"])
            datos_medicion_file = st.file_uploader("Tabla 4 - Datos Medición", type=["csv", "xlsx"])
            stamp_file = st.file_uploader("Sello (Stamp)", type=["png", "jpg", "jpeg"])

        st.header("3. Archivo Principal de Datos")
        main_data_file = st.file_uploader(
            "Archivo de Datos (CSV, PQDIF, etc.)", 
            type=["csv", "pqd", "pqdif"],
            help="El archivo principal con las mediciones de calidad de energía."
        )

        submit_button = st.form_submit_button(label="Iniciar Procesamiento")

    # --- Lógica de Procesamiento (Paso 2) ---
    if submit_button:
        # Validación simple
        all_files = [info_carga_file, desc_carga_file, info_medidor_file, datos_medicion_file, diagrama_file, stamp_file, main_data_file]
        if not user_email or not all(all_files):
            st.error("Por favor, completa todos los campos y sube todos los archivos requeridos.")
            return

        if not s3_client or not sqs_client:
            st.error("La conexión con AWS no está configurada. No se puede continuar.")
            return

        report_id = str(uuid.uuid4())
        s3_prefix = f"reports/{report_id}/inputs/"

        with st.spinner(f"Procesando reporte... ID: {report_id}"):
            try:
                # --- Subida a S3 ---
                st.write(f"Creando carpeta en S3: {s3_prefix}")
                
                # Función auxiliar para subir
                def upload_to_s3(file_obj, s3_key):
                    s3_client.upload_fileobj(file_obj, AWS_S3_BUCKET_NAME, s3_key)
                
                # Subir todos los archivos
                upload_to_s3(main_data_file, f"{s3_prefix}{main_data_file.name}")
                upload_to_s3(info_carga_file, f"{s3_prefix}{info_carga_file.name}")
                upload_to_s3(desc_carga_file, f"{s3_prefix}{desc_carga_file.name}")
                upload_to_s3(info_medidor_file, f"{s3_prefix}{info_medidor_file.name}")
                upload_to_s3(datos_medicion_file, f"{s3_prefix}{datos_medicion_file.name}")
                upload_to_s3(diagrama_file, f"{s3_prefix}{diagrama_file.name}")
                upload_to_s3(stamp_file, f"{s3_prefix}{stamp_file.name}")
                
                st.write("Archivos subidos a S3 exitosamente.")

                # --- Envío de Mensaje SQS ---
                message_body = {
                    "report_id": report_id,
                    "user_email": user_email,
                    "s3_input_prefix": s3_prefix,
                    "s3_output_prefix": f"reports/{report_id}/outputs/" # Ruta donde la Lambda debe escribir
                }
                
                sqs_client.send_message(
                    QueueUrl=AWS_SQS_QUEUE_URL,
                    MessageBody=json.dumps(message_body)
                )
                
                st.write("Mensaje enviado a SQS para activar la Lambda.")
                
                # --- Fin ---
                st.success(f"¡Procesamiento iniciado con éxito! (ID: {report_id})")
                st.info(f"Recibirás un correo en {user_email} con el enlace a tus resultados cuando la Lambda termine (Paso 3 y 4).")
                st.balloons()

            except (NoCredentialsError, ClientError) as e:
                st.error(f"Error de AWS: {e}")
            except Exception as e:
                st.error(f"Ocurrió un error inesperado: {e}")


# --- LÓGICA DE ENRUTAMIENTO PRINCIPAL ---

def main():
    # Lee el query param "report_id" de la URL
    # Ejemplo: https://mi-app.streamlit.app/?report_id=123-456-789
    report_id = st.query_params.get("report_id")

    if not report_id:
        # Si no hay report_id, muestra la página de subida
        show_input_page()
    else:
        # Si hay report_id, muestra la página de revisión
        show_review_page(report_id)

if __name__ == "__main__":
    main()