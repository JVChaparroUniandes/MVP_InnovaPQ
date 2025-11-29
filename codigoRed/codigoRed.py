import streamlit as st
from Modelos import Comentarios
from Servicio import Data
from codigoRed.DescripcionCodigoRed import Descripcion
from codigoRed.CumplimientoCodigoRed import Cumplimiento
from codigoRed.ResumenCodigoRed import ResumenCodigoRed
from codigoRed.PotenciaCodigoRed import PotenciaCodigoRed
from codigoRed.VoltajesCodigoRed import VoltajesCodigoRed
from codigoRed.CorrientesCodigoRed import CorrientesCodigoRed
from codigoRed.DesbalancesCodigoRed import DesbalancesCodigoRed
from codigoRed.FrecuenciaCodigoRed import FrecuenciaCodigoRed
from codigoRed.FlickerCodigoRed import FlickerCodigoRed
from codigoRed.ArmonicosVoltajeCodigoRed import ArmonicosVoltaje
from codigoRed.ArmonicosCorrienteCodigoRed import ArmonicosCorriente

def Ventana(MostrarVista,Servicio,Datos):
    match MostrarVista:
        case "Descripcion":
            return Descripcion(Servicio,Datos)
        case "Cumplimiento":
            return Cumplimiento(Servicio,Datos)
        case "Resumen Sistema":
            return ResumenCodigoRed(Servicio,Datos)
        case "Potencia":
            return PotenciaCodigoRed(Servicio,Datos)
        case "Voltajes":
            return VoltajesCodigoRed(Servicio,Datos)
        case "Corrientes":
            return CorrientesCodigoRed(Servicio,Datos)
        case "Desbalances":
            return DesbalancesCodigoRed(Servicio,Datos)
        case "Frecuencia":
            return FrecuenciaCodigoRed(Servicio,Datos)
        case "Flicker":
            return FlickerCodigoRed(Servicio,Datos)
        case "Armonicos Voltaje":
            return ArmonicosVoltaje(Servicio,Datos)
        case "Armonicos Corriente":
            return ArmonicosCorriente(Servicio,Datos)
        

@st.cache_resource
def get_servicio_aws(report_id):
    print("Conectando a AWS...")
    return Data(report_id)

@st.cache_data
def get_diccionario_rutas(_Servicio,nombre_carpeta):
    print("Escaneando bucket...")
    return _Servicio.obtener_rutas_actualizadas()





   
def CodigoRed(report_id):

    Servicio=get_servicio_aws(report_id)
    Datos=get_diccionario_rutas(_Servicio=Servicio,nombre_carpeta=report_id)
# --- Lógica Principal de la Aplicación ---
    if 'mostrar_vista' not in st.session_state:
        st.session_state.mostrar_vista = "Descripcion"

    def MostrarVistaFunc(Pagina):
        st.session_state.mostrar_vista=Pagina
        return st.session_state.mostrar_vista

    with st.sidebar:
        st.title("Código de red")
        st.subheader(f'ID: {report_id}')
        st.divider()
        st.button("Descripción",on_click=MostrarVistaFunc,args=("Descripcion",),key="Descripcion",use_container_width=True)
        st.button("Cumplimiento",on_click=MostrarVistaFunc,args=("Cumplimiento",),key="Cumplimiento",use_container_width=True)
        st.button("Resumen Sistema",on_click=MostrarVistaFunc,args=("Resumen Sistema",),key="Resumen Sistema",use_container_width=True)
        st.button("Potencia",on_click=MostrarVistaFunc,args=("Potencia",),key="Potencia",use_container_width=True)
        st.button("Voltajes",on_click=MostrarVistaFunc,args=("Voltajes",),key="Voltajes",use_container_width=True)
        st.button("Corrientes",on_click=MostrarVistaFunc,args=("Corrientes",),key="Corrientes",use_container_width=True)
        st.button("Desbalances",on_click=MostrarVistaFunc,args=("Desbalances",),key="Desbalances",use_container_width=True)
        st.button("Frecuencia",on_click=MostrarVistaFunc,args=("Frecuencia",),key="Frecuencia",use_container_width=True)
        st.button("Flicker",on_click=MostrarVistaFunc,args=("Flicker",),key="Flicker",use_container_width=True)
        st.button("Armonicos Voltaje",on_click=MostrarVistaFunc,args=("Armonicos Voltaje",),key="Armonicos Voltaje",use_container_width=True)
        st.button("Armonicos Corriente",on_click=MostrarVistaFunc,args=("Armonicos Corriente",),key="Armonicos Corriente",use_container_width=True)

        

    with st.container():
        col2, col3 = st.columns([0.75,0.25])
            
        with col2:
            with st.container():
                Ventana(MostrarVista=st.session_state.mostrar_vista,Servicio=Servicio,Datos=Datos)
        with col3:
            
            with st.container():
                rutaComentarios=Datos["Comentarios"]["CodigoRed"]

                SeccionNotas=Comentarios(titulo="Notas",seccion_json="nota",rutaDatos=rutaComentarios,servicio=Servicio)
                NotasReporte=SeccionNotas.render()
                NotasReporte

                SeccionImportante=Comentarios(titulo="Importante",seccion_json="importante",rutaDatos=rutaComentarios,servicio=Servicio)
                ImportanteReporte=SeccionImportante.render()
                ImportanteReporte

                SeccionPrecaucion=Comentarios(titulo="Precaución",seccion_json="precaucion",rutaDatos=rutaComentarios,servicio=Servicio)
                PrecaucionReporte=SeccionPrecaucion.render()
                PrecaucionReporte


                # Inicializar estado del modal
                if 'mostrar_modal_pdf' not in st.session_state:
                    st.session_state.mostrar_modal_pdf = False
                if 'pdf_enviado' not in st.session_state:
                    st.session_state.pdf_enviado = False
                if 'email_pdf_enviado' not in st.session_state:
                    st.session_state.email_pdf_enviado = ""
                
                # Mostrar mensaje de éxito si ya se envió
                if st.session_state.pdf_enviado:
                    st.success(f"✅ **Solicitud de generación de PDF enviada exitosamente**\n\n"
                              f"El reporte PDF con los comentarios actualizados será generado y enviado a:\n"
                              f"**{st.session_state.email_pdf_enviado}**\n\n"
                              f"📬 Recibirá el correo con el PDF en los próximos minutos.")
                    if st.button("Cerrar", key="cerrar_mensaje_pdf"):
                        st.session_state.pdf_enviado = False
                        st.session_state.email_pdf_enviado = ""
                        st.rerun()
                
                # Botón para abrir modal
                if not st.session_state.pdf_enviado:
                    if st.button("Generar PDF con comentarios actualizados"):
                        st.session_state.mostrar_modal_pdf = True
                        st.rerun()
                
                # Modal para solicitar email
                if st.session_state.mostrar_modal_pdf and not st.session_state.pdf_enviado:
                    with st.container():
                        st.info("📧 Por favor, ingrese el correo electrónico al cual desea enviar el reporte PDF.")
                        
                        with st.form(key="form_modal_pdf", clear_on_submit=False):
                            email_pdf = st.text_input(
                                "Correo Electrónico",
                                placeholder="ejemplo@correo.com",
                                type="default"
                            )
                            
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                enviar_btn = st.form_submit_button("✅ Enviar", use_container_width=True, type="primary")
                            with col_btn2:
                                cancelar_btn = st.form_submit_button("❌ Cancelar", use_container_width=True)
                            
                            if cancelar_btn:
                                st.session_state.mostrar_modal_pdf = False
                                st.rerun()
                            
                            if enviar_btn:
                                # Validar email
                                if not email_pdf or email_pdf.strip() == "":
                                    st.error("Por favor, ingrese un correo electrónico válido.")
                                elif "@" not in email_pdf:
                                    st.error("Por favor, ingrese un correo electrónico válido.")
                                else:
                                    try:
                                        # Guardar comentarios actualizados
                                        Servicio.GuardarDatos(
                                            NotasReporte,
                                            ImportanteReporte,
                                            PrecaucionReporte
                                        )
                                        
                                        # Construir mensaje para SQS PDF
                                        mensaje_pdf_sqs = {
                                            "report_id": report_id,
                                            "bucket": Servicio.bucket,
                                            "region": Servicio.Region,
                                            "report_type": "codigo_red",
                                            "email": email_pdf.strip()
                                        }
                                        
                                        # Obtener URL de la cola PDF desde secrets
                                        queue_url_pdf = st.secrets["aws"]["sqs_pdf_queue_url"]
                                        
                                        # Enviar mensaje a SQS
                                        Servicio.enviar_mensaje_sqs(queue_url_pdf, mensaje_pdf_sqs)
                                        
                                        # Cerrar modal y marcar como enviado
                                        st.session_state.mostrar_modal_pdf = False
                                        st.session_state.pdf_enviado = True
                                        st.session_state.email_pdf_enviado = email_pdf.strip()
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error al enviar la solicitud: {str(e)}\n\nPor favor, intente nuevamente.")

                


            
        # En una v2, estos valores por defecto vendrían de un .txt o .json en S3
        #st.subheader("Notas")
        #comentario_Notas = st.text_area(label="",value="El voltaje se mantiene...")
        #st.subheader("Tips")
        #comentario_Tips = st.text_area(label="",value="Se detectaron picos de armónicos...")
        #st.subheader("Importante")
        #comentario_Importante = st.text_area(label="",value= "Se recomienda la instalación de...")
        #st.subheader("Precacución")
        #comentario_Precaucion = st.text_area(label="",value= "Cuidado con...")
        #st.subheader("Advertencia")
        #comentario_Advertencia = st.text_area(label="",value= "Accion inmediata")

        # --- 3. Generar PDF ---
        #st.header("Generar PDF")
            
        