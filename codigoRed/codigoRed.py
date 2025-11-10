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

def Ventana(MostrarVista):
    match MostrarVista:
        case "Descripcion":
            return Descripcion()
        case "Cumplimiento":
            return Cumplimiento()
        case "Resumen Sistema":
            return ResumenCodigoRed()
        case "Potencia":
            return PotenciaCodigoRed()
        case "Voltajes":
            return VoltajesCodigoRed()
        case "Corrientes":
            return CorrientesCodigoRed()
        case "Desbalances":
            return DesbalancesCodigoRed()
        case "Frecuencia":
            return FrecuenciaCodigoRed()
        case "Flicker":
            return FlickerCodigoRed()
        case "Armonicos Voltaje":
            return ArmonicosVoltaje()
        case "Armonicos Corriente":
            return ArmonicosCorriente()
        


Servicio=Data()
Datos=Servicio.LeerDatos()



   
def CodigoRed(report_id):
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
                Ventana(MostrarVista=st.session_state.mostrar_vista)
        with col3:
            st.subheader("Comentarios")
            with st.container():
                Notas=Comentarios(titulo="Notas",comentario=Datos["Comentarios"]["Notas"],key="Notas")
                NotasReporte=Notas.BloqueComentario()
                NotasReporte
                Importante=Comentarios(titulo="Importante",comentario="Hola",key="Importante")
                ImportanteReporte=Importante.BloqueComentario()
                ImportanteReporte
                Precaucion=Comentarios(titulo="Precacución",comentario="Hola",key="Precaución")
                PrecaucionReporte=Precaucion.BloqueComentario()
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
            
        