import openpyxl
import pandas as pd
import streamlit as st
import json
# --- Clases ---

class Tabla:
    def __init__(self,titulo,rutaDatos,servicio):
        self.titulo=titulo
        self.rutaDatos=rutaDatos
        self.servicio=servicio

    def construirContenedor(self):
        #df=pd.read_excel(io=self.rutaDatos,index_col=0)
        df=self.servicio.descargar_archivo_s3(self.rutaDatos)
        #df=df.round(decimals=1)
        st.subheader(self.titulo)
        st.table(data=df)

class Descripciones:
    def __init__(self,rutaDatos,servicio):
        self.rutaDatos=rutaDatos
        self.servicio=servicio
    
    def ConstruirContenedor(self):
        df=self.servicio.descargar_archivo_s3(self.rutaDatos)
        df_datos = df.iloc[1:]
        st.subheader(df.iloc[0,0])
        for index,row in df_datos.iterrows():
            with st.container(horizontal=True):
                col1,col2=st.columns([0.3,0.7])
                with col1:
                    st.markdown(
                        f'<p style="font-size: 18px; font-weight: bold;color:black;">{str(row[0])} </p>',
                        unsafe_allow_html=True
                        )
                with col2:
                    st.write(str(row[1]))
                
class Imagenes:
    def __init__(self,titulo,rutaDatos,servicio):
        self.rutaDatos=rutaDatos
        self.titulo=titulo
        self.servicio=servicio
    def ConstruirImagen(self):
        captionImg=st.markdown(
                f'<p style="font-size: 18px; font-weight: bold;color:black;">{self.titulo} </p>',
                unsafe_allow_html=True
                )
        col1, col2, col3 = st.columns([0.1,0.8,0.1])
        with col2:
            st.image(image=self.servicio.descargar_archivo_s3(self.rutaDatos)) 
    

class Comentarios:
    def __init__(self, titulo, seccion_json, rutaDatos, servicio):
        """
        Args:
            titulo_ui (str): El título que aparecerá arriba del text_area (ej: "Notas Técnicas").
            seccion_json (str): La llave del JSON a leer (ej: 'nota', 'importante', 'executive_summary').
            ruta_archivo_s3 (str): La ruta completa en S3 donde está este JSON de reporte.
            servicio_datos (Data): La instancia de tu servicio de conexión.
        """
        self.titulo_ui = titulo
        self.seccion_json = seccion_json
        self.ruta_archivo_s3 = rutaDatos
        self.servicio = servicio

    def render(self):
        # 1. Mostrar el título en la UI
        st.subheader(self.titulo_ui)

        # 2. Descargar el JSON crudo desde S3
        # Como tu clase Data devuelve 'bytes' para archivos desconocidos, aquí los procesamos.
        bytes_data = self.servicio.descargar_archivo_s3(self.ruta_archivo_s3)
        
        if not bytes_data:
            st.error("No se pudo cargar el archivo de comentarios.")
            return

        try:
            # 3. Parsear los bytes a Diccionario Python
            data_dict = json.loads(bytes_data.decode('utf-8'))
            
            # 4. Extraer la sección solicitada
            contenido_raw = data_dict.get(self.seccion_json, None)

            if contenido_raw is None:
                st.warning(f"No se encontró la sección '{self.seccion_json}' en el reporte.")
                return

            # 5. Lógica de Formateo Inteligente
            texto_final = ""

            if isinstance(contenido_raw, list):
                # CASO A: Es una lista (nota, importante, precaucion)
                for item in contenido_raw:
                    titulo_nota = item.get('title', 'Sin Título')
                    cuerpo_nota = item.get('content', '')
                    
                    # Construimos un string formateado
                    texto_final += f"- {titulo_nota.upper()}:\n{cuerpo_nota}\n\n"
                    
                    # (Opcional) Si quieres incluir referencias:
                    # refs = ", ".join(item.get('references', []))
                    # texto_final += f"   (Refs: {refs})\n\n"
            
            elif isinstance(contenido_raw, str):
                # CASO B: Es texto plano (executive_summary, technical_summary)
                texto_final = contenido_raw
            
            else:
                texto_final = str(contenido_raw)

            # 6. Renderizar en el Text Area
            # height=300 le da buen espacio, disabled=True evita que el usuario lo borre por error
            texto_usuario=st.text_area(
                label=f"Contenido de {self.seccion_json}", 
                value=texto_final, 
                height=500,
                label_visibility="collapsed" # Ocultamos el label pequeño porque ya pusimos subheader
            )

            return texto_usuario

        except json.JSONDecodeError:
            st.error("El archivo descargado no tiene un formato JSON válido.")
        except Exception as e:
            st.error(f"Error procesando comentarios: {e}")