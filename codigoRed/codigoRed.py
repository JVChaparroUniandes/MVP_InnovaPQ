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
def get_diccionario_rutas(_Servicio):
    print("Escaneando bucket...")
    return _Servicio.obtener_rutas_actualizadas()

Servicio_aws=get_servicio_aws("report1")
Datos=get_diccionario_rutas(_Servicio=Servicio_aws)



   
def CodigoRed(report_id,Servicio=Servicio_aws,Datos=Datos):
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
            st.subheader("Comentarios")
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


                if st.button("Generar PDF con comentarios actualizados"):
                    with st.spinner("Generando PDF..."):
                        Servicio.GuardarDatos(
                            NotasReporte,
                            ImportanteReporte,
                            PrecaucionReporte
                        )

                


            
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
            
        