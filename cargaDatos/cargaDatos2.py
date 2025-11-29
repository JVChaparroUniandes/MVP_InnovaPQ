import streamlit as st
import uuid
import pandas as pd
import io
from Servicio import Data 

# --- 1. INSTANCIA DE SERVICIO (Recurso Compartido) ---
@st.cache_resource
def get_servicio_base():
    # Instanciamos sin carpeta específica
    return Data(folder="reports/")

def CargarDatos2():
    # Inicializamos el servicio
    Servicio = get_servicio_base()
    
    st.title("⚡ Nuevo Reporte de Calidad de Energía")
    st.info("Todos los campos marcados son obligatorios. Se generará la estructura requerida en S3.")

    # ==========================================
    # 1. FORMULARIO (UI)
    # ==========================================
    with st.form(key="formulario_carga", clear_on_submit=False):
        
        datos_formulario = {}
        archivos_formulario = {}

        tab1, tab2, tab3 = st.tabs(["📋 Información General", "⚙️ Datos Técnicos", "📂 Archivos"])

        # ---------------------------------------------------------
        # TAB 1: DATOS ADMINISTRATIVOS (Tablas 1 y 2)
        # ---------------------------------------------------------
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                # No guardamos correo en Excel según tus tablas, pero sirve para notificación
                datos_formulario["Correo Electrónico"] = st.text_input("Correo Electrónico")
                datos_formulario["Empresa"] = st.text_input("Empresa / Cliente")
            
            with col2:
                datos_formulario["Responsable de equipo"] = st.text_input("Responsable del sitio")
                datos_formulario["Dirección"] = st.text_input("Dirección del sitio")
            
            st.divider()
            datos_formulario["Descripción de actividades"] = st.text_area("Descripción de actividades", height=80)
            datos_formulario["Nombre del punto"] = st.text_input("Nombre del punto de medición")
            datos_formulario["Descripción carga"] = st.text_input("Descripción general de la carga")

        # ---------------------------------------------------------
        # TAB 2: DATOS TÉCNICOS (Tablas 3 y 4)
        # ---------------------------------------------------------
        with tab2:
            st.subheader("Medidor")
            c1, c2, c3 = st.columns(3)
            datos_formulario["Marca"] = c1.selectbox("Marca", ["Schneider ION-9000", "Otros"])
            datos_formulario["Clase"] = c2.selectbox("Clase", ["A", "S"])
            datos_formulario["Tasa muestreo"] = c3.selectbox("Tasa", ["1 min", "5 min", "10 min", "15 min"])

            st.divider()
            st.subheader("Parámetros Eléctricos")
            
            col_a, col_b = st.columns(2)
            with col_a:
                datos_formulario["Frecuencia del sistema"] = st.radio("Frecuencia", ["60 Hz", "50 Hz"], horizontal=True)
                
                # Tensión Suministro
                cc1, cc2 = st.columns([0.7, 0.3])
                t_sum = cc1.text_input("Tensión Suministro (Valor)")
                u_sum = cc2.selectbox("U.", ["V", "kV"], key="usum")
                datos_formulario["Tensión de suministro"] = f"{t_sum} {u_sum}" if t_sum else ""

                # Demanda
                cc1, cc2 = st.columns([0.7, 0.3])
                dem = cc1.text_input("Demanda Contratada (Valor)")
                u_dem = cc2.selectbox("U.", ["kW", "MW", "W"], key="udem")
                datos_formulario["Demanda contratada"] = f"{dem} {u_dem}" if dem else ""

                # Corriente Demanda
                cc1, cc2 = st.columns([0.7, 0.3])
                i_dem = cc1.text_input("Corriente demanda máx (Valor)")
                u_idem = cc2.selectbox("U.", ["A", "kA"], key="uidem")
                datos_formulario["Corriente demanda máxima contratada"] = f"{i_dem} {u_idem}" if i_dem else ""

            with col_b:
                datos_formulario["Transformador del tablero"] = st.text_input("Transformador (Capacidad/Tipo)")
                
                # Tensión Punto
                cc1, cc2 = st.columns([0.7, 0.3])
                t_pto = cc1.text_input("Tensión Punto (Valor)")
                u_pto = cc2.selectbox("U.", ["V", "kV"], key="upto")
                datos_formulario["Tensión de punto de medición"] = f"{t_pto} {u_pto}" if t_pto else ""

                # Corriente CC
                cc1, cc2 = st.columns([0.7, 0.3])
                icc = cc1.text_input("Corriente CC (Valor)")
                u_icc = cc2.selectbox("U.", ["kA", "A"], key="uicc")
                datos_formulario["Corriente de corto circuito"] = f"{icc} {u_icc}" if icc else ""

            st.divider()
            cd1, cd2 = st.columns(2)
            datos_formulario["Temporalidad de medición"] = st.selectbox("Temporalidad", ["Diaria", "Semanal", "Mensual"])
            # Convertimos a str para que sea serializable
            datos_formulario["Fecha de medición inicial"] = str(cd1.date_input("Inicio Medición"))
            datos_formulario["Fecha de medición final"] = str(cd2.date_input("Fin Medición"))

        # ---------------------------------------------------------
        # TAB 3: ARCHIVOS (Validación Crítica)
        # ---------------------------------------------------------
        with tab3:
            st.warning("⚠️ Todos los archivos son obligatorios.")
            
            st.subheader("Carpeta: raw_data")
            archivos_formulario["main_file"] = st.file_uploader("Archivo Principal (CSV/PQDIF)", type=["csv", "pqd", "pqdif"])
            
            st.divider()
            st.subheader("Carpeta: input")
            col_files_1, col_files_2 = st.columns(2)
            with col_files_1:
                archivos_formulario["Diagrama Unifilar"] = st.file_uploader("Diagrama Unifilar", type=["png", "jpg", "pdf"])
            with col_files_2:
                archivos_formulario["Sello"] = st.file_uploader("Sello (Stamp)", type=["png", "jpg"])

        st.divider()
        submit_button = st.form_submit_button("🚀 Iniciar Procesamiento", use_container_width=True, type="primary")

    # ==========================================
    # 2. LÓGICA DE PROCESAMIENTO Y CARGA
    # ==========================================
    if submit_button:
        
        # A. VALIDACIÓN ESTRICTA
        errores = []
        for campo, valor in datos_formulario.items():
            if not valor or str(valor).strip() == "": errores.append(campo)
        
        for nombre_archivo, objeto_archivo in archivos_formulario.items():
            if objeto_archivo is None: errores.append(nombre_archivo)

        if errores:
            st.error(f"❌ Faltan los siguientes campos obligatorios: {', '.join(errores)}")
            return 

        # B. PREPARACIÓN DE CARPETAS S3
        report_uuid = str(uuid.uuid4())
        prefix_root = f"report{report_uuid}/"
        prefix_raw = f"{prefix_root}raw_data/"
        prefix_input = f"{prefix_root}input/"

        client = Servicio.client_s3
        bucket = Servicio.bucket

        with st.status(f"Generando reporte ID: {report_uuid}...", expanded=True) as status:
            try:
                # ---------------------------------------------------------
                # PASO 1: Subir Archivo Principal a "raw_data"
                # ---------------------------------------------------------
                file_main = archivos_formulario["main_file"]
                file_main.seek(0)
                status.write(f"⬆️ Subiendo Raw Data: {file_main.name}")
                client.upload_fileobj(file_main, bucket, f"{prefix_raw}{file_main.name}")

                # ---------------------------------------------------------
                # PASO 2: Subir Archivos Físicos a "input"
                # ---------------------------------------------------------
                # Diagrama
                file_diag = archivos_formulario["Diagrama Unifilar"]
                file_diag.seek(0)
                ext_diag = file_diag.name.split('.')[-1]
                client.upload_fileobj(file_diag, bucket, f"{prefix_input}diagrama_unifilar.{ext_diag}")
                
                # Sello
                file_stamp = archivos_formulario["Sello"]
                file_stamp.seek(0)
                ext_stamp = file_stamp.name.split('.')[-1]
                client.upload_fileobj(file_stamp, bucket, f"{prefix_input}sello.{ext_stamp}")

                # ---------------------------------------------------------
                # PASO 3: GENERACIÓN DE EXCELS (Tablas 1, 2, 3, 4)
                # ---------------------------------------------------------
                status.write("⚙️ Generando Tablas de Información...")

                # Función interna para crear Excel en RAM y subir
                def subir_excel(nombre_s3, data_dict):
                    df = pd.DataFrame(list(data_dict.items()), columns=["Concepto", "Valor"])
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    output.seek(0)
                    client.upload_fileobj(output, bucket, f"{prefix_input}{nombre_s3}")

                # Generar Tabla 1
                subir_excel("Tabla 1 - Información Centro Carga.xlsx", {
                    "Empresa": datos_formulario["Empresa"],
                    "Dirección": datos_formulario["Dirección"],
                    "Responsable de equipo": datos_formulario["Responsable de equipo"]
                })

                # Generar Tabla 2
                subir_excel("Tabla 2 - Descripción Centro Carga.xlsx", {
                    "Descripción de actividades": datos_formulario["Descripción de actividades"],
                    "Nombre del punto de medición": datos_formulario["Nombre del punto"],
                    "Descripción general de la carga": datos_formulario["Descripción carga"]
                })

                # Generar Tabla 3
                subir_excel("Tabla 3 - Información Medidor.xlsx", {
                    "Marca": datos_formulario["Marca"],
                    "Clase": datos_formulario["Clase"],
                    "Tasa de muestreo": datos_formulario["Tasa muestreo"]
                })

                # Generar Tabla 4
                subir_excel("Tabla 4 - Datos Medición.xlsx", {
                    "Frecuencia del sistema": datos_formulario["Frecuencia del sistema"],
                    "Tensión de suministro": datos_formulario["Tensión de suministro"],
                    "Tensión de punto de medición": datos_formulario["Tensión de punto de medición"],
                    "Demanda contratada": datos_formulario["Demanda contratada"],
                    "Corriente demanda máxima contratada": datos_formulario["Corriente demanda máxima contratada"],
                    "Corriente de corto circuito": datos_formulario["Corriente de corto circuito"],
                    "Transformador del tablero": datos_formulario["Transformador del tablero"],
                    "Temporalidad de medición": datos_formulario["Temporalidad de medición"],
                    "Fecha de medición inicial": datos_formulario["Fecha de medición inicial"],
                    "Fecha de medición final": datos_formulario["Fecha de medición final"]
                })

                status.update(label="¡Carga Completa!", state="complete", expanded=False)
                
                st.balloons()
                st.success(f"Archivos recibidos. ID del reporte: {report_uuid}")
                st.info(f"Se ha enviado la confirmación a {datos_formulario['Correo Electrónico']}")

            except Exception as e:
                status.update(label="Error crítico", state="error")
                st.error(f"Hubo un error al conectar con AWS: {str(e)}")