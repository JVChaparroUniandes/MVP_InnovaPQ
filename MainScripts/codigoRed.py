import streamlit as st
from Modelos.ModelosCodigoRed import Tabla,Descripciones,Imagenes
from Servicios.ServicioCodigoRed import Data


Servicio=Data()
Data=Servicio.LeerDatos()


# --- Configuración de la Página ---
st.set_page_config(
    page_title="Reporte código de red",
    layout="wide"
)
   

# --- Lógica Principal de la Aplicación ---

# Lee el query param "report_id" de la URL
# Ejemplo: https://mi-app-review.com/?report_id=123-456-789
report_id = st.query_params.get("report_id")

# Si hay report_id y AWS está OK, muestra la página de revisión
st.title(f"Código de red (ID: {report_id})")

# --- Información General ---

with st.container():
    with st.container(border=True):
        rutaCentroCarga=Data["Contexto"]["Descripcion"]
        DescripcionCentroCarga=Descripciones(rutaCentroCarga)
        DescripcionCentroCarga.ConstruirContenedor()

    
    with st.container(horizontal=True):
        with st.container(border=True):
                rutaDatosMedicion=Data["Contexto"]["Medicion"]
                DescripcionDatos=Descripciones(rutaDatosMedicion)
                DescripcionDatos.ConstruirContenedor()
        with st.container():

            with st.container(border=True):
                rutaInfoCarga=Data["Contexto"]["Informacion"]
                DescripcionInfoCarga=Descripciones(rutaInfoCarga)
                DescripcionInfoCarga.ConstruirContenedor()
            with st.container(border=True):
                rutaMedidor=Data["Contexto"]["Medidor"]
                DescripcionMedidor=Descripciones(rutaMedidor)
                DescripcionMedidor.ConstruirContenedor()
            
# --- Diagrama Unifilar---
with st.container():
    st.subheader("Diagrama Unifilar")
    rutaUnifilar=Data["Unifilar"]
    ImagenUnifilar=Imagenes("",rutaUnifilar)
    ImagenUnifilar.ConstruirImagen()
# --- Tabla cumplimiento ---
with st.container(border=True):
    with st.container():
        rutaTablaCumplimiento=Data["CumplimientoRed"]["Principal"]
        TablaCumplimiento=Tabla("Cumplimiento de red",rutaTablaCumplimiento)
        TablaCumplimiento.construirContenedor()

    with st.container():
        rutaTablaArmonicosP95=Data["ArmonicosCorriente"]["ArmonicosITablaP95"]
        TablaArmonicosP95=Tabla("Niveles de armónicos de corriente (P95)",rutaTablaArmonicosP95)
        TablaArmonicosP95.construirContenedor()

  
    with st.container():
        rutaTablaAplicables=Data["CumplimientoRed"]["limaplicables"]
        TablaAplicables=Tabla(" Límites aplicables código de red al centro de carga",rutaTablaAplicables)
        TablaAplicables.construirContenedor()

    with st.container():
        rutaTablaLimdatad=Data["CumplimientoRed"]["limdatd"]
        TablaAplicables=Tabla("Límites aplicables para DATD y DAI",rutaTablaLimdatad)
        TablaAplicables.construirContenedor()
# --- Resumen de mediciones ---
with st.container():
    st.subheader("Resumen de mediciones")
    with st.expander(label=""):
        with st.container(horizontal=True):
            with st.container():
                rutaTablaResumenActiva=Data["Resumen"]["ResumenActiva"]
                TablaResumenActiva=Tabla("Potencia activa",rutaTablaResumenActiva)
                TablaResumenActiva.construirContenedor()
            with st.container():
                rutaTablaReactiva=Data["Resumen"]["ResumenReactiva"]
                TablaResumenReactiva=Tabla("Potencia reactiva",rutaTablaReactiva)
                TablaResumenReactiva.construirContenedor()
        with st.container(horizontal=True):
            with st.container():
                rutaTablaAparente=Data["Resumen"]["ResumenAparente"]
                TablaResumenAparente=Tabla("Potencia aparente",rutaTablaAparente)
                TablaResumenAparente.construirContenedor()
            with st.container():
                rutaTablaFP=Data["Resumen"]["ResumenFP"]
                TablaResumenFP=Tabla("Factor de potencia",rutaTablaFP)
                TablaResumenFP.construirContenedor()
        with st.container(horizontal=True):
            with st.container():
                rutaTablaTHD=Data["Resumen"]["ResumenTHD"]
                TablaResumenTHD=Tabla("THD",rutaTablaTHD)
                TablaResumenTHD.construirContenedor()
            with st.container():
                rutaTablaTDD=Data["Resumen"]["ResumenTDD"]
                TablaResumenTDD=Tabla("TDD",rutaTablaTDD)
                TablaResumenTDD.construirContenedor()
        with st.container(horizontal=True):
            with st.container():
                rutaTablaDesVoltaje=Data["Resumen"]["ResumenDesVoltaje"]
                TablaResumenDesVoltaje=Tabla("Desbalance de voltaje",rutaTablaDesVoltaje)
                TablaResumenDesVoltaje.construirContenedor()
            with st.container():
                rutaTablaDesCorriente=Data["Resumen"]["ResumenDesCorriente"]
                TablaResumenDesCorriente=Tabla("Desbalance de corriente",rutaTablaDesCorriente)
                TablaResumenDesCorriente.construirContenedor()
        with st.container(horizontal=True):
            with st.container():
                rutaTablaVProm=Data["Resumen"]["ResumenVProm"]
                TablaResumenVProm=Tabla("Voltajes RMS",rutaTablaVProm)
                TablaResumenVProm.construirContenedor()
            with st.container():
                rutaTablaCProm=Data["Resumen"]["ResumenCProm"]
                TablaResumenCProm=Tabla("Corrientes RMS",rutaTablaCProm)
                TablaResumenCProm.construirContenedor()
        with st.container(horizontal=True):
            with st.container():
                rutaTablaFlickPst=Data["Resumen"]["ResumenFlickPst"]
                TablaResumenFlickPst=Tabla("Flicker Pst",rutaTablaFlickPst)
                TablaResumenFlickPst.construirContenedor()
            with st.container():
                rutaTablaFlickPlt=Data["Resumen"]["ResumenFlickPlt"]
                TablaResumenFlickPlt=Tabla("Flicker Plt",rutaTablaFlickPlt)
                TablaResumenFlickPlt.construirContenedor()
        with st.container(horizontal=True):
            with st.container():
                rutaTablaFrecuencia=Data["Resumen"]["ResumenFrecuencia"]
                TablaResumenFrecuencia=Tabla("Frecuencia",rutaTablaFrecuencia)
                TablaResumenFrecuencia.construirContenedor()
            with st.container():
                st.write("")  # Espacio vacío para mantener el diseño
# --- Potenccia ---
with st.container():
    st.subheader("Potencia")
    with st.expander(label=""):
        with st.container(horizontal=True):
            with st.container():
                rutaImagenPotenciaActiva=Data["Potencia"]["PotenciaActiva"]
                ImagenPotenciaActiva=Imagenes("Potencia Activa",rutaImagenPotenciaActiva)
                ImagenPotenciaActiva.ConstruirImagen()
            with st.container():
                rutaImagenPotenciaReactiva=Data["Potencia"]["PotenciaReactiva"]
                ImagenPotenciaReactiva=Imagenes("Potencia Reactiva",rutaImagenPotenciaReactiva)
                ImagenPotenciaReactiva.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaImagenPotenciaAparente=Data["Potencia"]["PotenciaAparente"]
                ImagenPotenciaAparente=Imagenes("Potencia Aparente",rutaImagenPotenciaAparente)
                ImagenPotenciaAparente.ConstruirImagen()
            with st.container():
                rutaImagenFactorPotencia=Data["Potencia"]["PotenciaFp"]
                ImagenFactorPotencia=Imagenes("Factor de Potencia",rutaImagenFactorPotencia)
                ImagenFactorPotencia.ConstruirImagen()
        st.subheader("Distribuciones de Potencia")
        with st.container(horizontal=True):
            with st.container():
                rutaImagenDistribucionActiva=Data["Potencia"]["PotenciaDistribucionActiva"]
                ImagenDistribucionActiva=Imagenes("Distribución Potencia Activa",rutaImagenDistribucionActiva)
                ImagenDistribucionActiva.ConstruirImagen()
            with st.container():
                rutaImagenDistribucionReactiva=Data["Potencia"]["PotenciaDistribucionReactiva"]
                ImagenDistribucionReactiva=Imagenes("Distribución Potencia Reactiva",rutaImagenDistribucionReactiva)
                ImagenDistribucionReactiva.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaImagenDistribucionAparente=Data["Potencia"]["PotenciaDistribucionAparente"]
                ImagenDistribucionAparente=Imagenes("Distribución Potencia Aparente",rutaImagenDistribucionAparente)
                ImagenDistribucionAparente.ConstruirImagen()
            with st.container():
                rutaImagenDistribucionFp=Data["Potencia"]["PotenciaDistribucionFp"]
                ImagenDistribucionFp=Imagenes("Distribución Factor de Potencia",rutaImagenDistribucionFp)
                ImagenDistribucionFp.ConstruirImagen()
        with st.container():
            rutaTablaDescriptivasPotencia=Data["Potencia"]["PotenciaDescriptivas"]
            TablaDescriptivasPotencia=Tabla("Estadísticos Descriptivos de Potencia",rutaTablaDescriptivasPotencia)
            TablaDescriptivasPotencia.construirContenedor()
        
with st.container():
    st.subheader("Voltajes")
    with st.expander(label=""):
        
        st.subheader(" Voltajes RMS")
        with st.container(horizontal=True):
            with st.container():
                rutaImagenVoltajeRMSMaximo=Data["Voltaje"]["VoltajeRMSMaximo"]
                ImagenVoltajeRMSMaximo=Imagenes("Voltajes RMS Máximo",rutaImagenVoltajeRMSMaximo)
                ImagenVoltajeRMSMaximo.ConstruirImagen()
            with st.container():
                rutaImagenVoltajeRMSMinimo=Data["Voltaje"]["VoltajeRMSMinimo"]
                ImagenVoltajeRMSMinimo=Imagenes("Voltajes RMS Mínimo",rutaImagenVoltajeRMSMinimo)
                ImagenVoltajeRMSMinimo.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaImagenVoltajeRMSPromedio=Data["Voltaje"]["VoltajeRMSPromedio"]
                ImagenVoltajeRMSPromedio=Imagenes("Voltajes RMS Promedio",rutaImagenVoltajeRMSPromedio)
                ImagenVoltajeRMSPromedio.ConstruirImagen()
            with st.container():
                st.write("") 
        with st.container(horizontal=True):
            with st.container():
                st.subheader(" Distribución de Voltajes")
                rutaImagenDistribucionLL=Data["Voltaje"]["VoltajeDistrLL"]
                ImagenDistribucionLL=Imagenes("Distribución Voltaje L-L",rutaImagenDistribucionLL)
                ImagenDistribucionLL.ConstruirImagen()
        with st.container():
            rutaTablaDescriptivasVoltaje=Data["Voltaje"]["VoltajeTablaDescriptiva"]
            TablaDescriptivasVoltaje=Tabla("Estadísticos Descriptivos de Voltajes RMS L-L",rutaTablaDescriptivasVoltaje)
            TablaDescriptivasVoltaje.construirContenedor()
with st.container():
    st.subheader("Corrientes")
    with st.expander(label=""):
        
        st.subheader(" Corrientes RMS")
        with st.container(horizontal=True):
            with st.container():
                rutaImagenCorrienteRMSMaximo=Data["Corriente"]["CorrienteRMSMaximo"]
                ImagenCorrienteRMSMaximo=Imagenes("Corrientes RMS Máximo",rutaImagenCorrienteRMSMaximo)
                ImagenCorrienteRMSMaximo.ConstruirImagen()
            with st.container():
                rutaImagenCorrienteRMSMinimo=Data["Corriente"]["CorrienteRMSMinimo"]
                ImagenCorrienteRMSMinimo=Imagenes("Corrientes RMS Mínimo",rutaImagenCorrienteRMSMinimo)
                ImagenCorrienteRMSMinimo.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaImagenCorrienteRMSPromedio=Data["Corriente"]["CorrienteRMSPromedio"]
                ImagenCorrienteRMSPromedio=Imagenes("Corrientes RMS Promedio",rutaImagenCorrienteRMSPromedio)
                ImagenCorrienteRMSPromedio.ConstruirImagen()
            with st.container():
                st.write("") 
        with st.container():
            with st.container():
                st.subheader(" Distribución de Corrientes")
                rutaImagenDistribucionCorriente=Data["Corriente"]["CorrienteDistr"]
                ImagenDistribucionCorriente=Imagenes("Distribución Corriente",rutaImagenDistribucionCorriente)
                ImagenDistribucionCorriente.ConstruirImagen()
        with st.container():
            rutaTablaDescriptivasCorriente=Data["Corriente"]["CorrienteTablaDescriptiva"]
            TablaDescriptivasCorriente=Tabla("Estadísticos Descriptivos de Corrientes RMS",rutaTablaDescriptivasCorriente)
            TablaDescriptivasCorriente.construirContenedor()

with st.container():
    st.subheader("Desbalances")
    with st.expander(label=""):
        
        with st.container(horizontal=True):
            with st.container():
                rutaImagenDesbalanceVoltaje=Data["Desbalance"]["DesbalanceVoltajeSerieTiempo"]
                ImagenDesbalanceVoltaje=Imagenes("Desbalance de Voltaje",rutaImagenDesbalanceVoltaje)
                ImagenDesbalanceVoltaje.ConstruirImagen()
            with st.container():
                rutaImagenDesbalanceCorriente=Data["Desbalance"]["DesbalanceCorrienteSerieTiempo"]
                ImagenDesbalanceCorriente=Imagenes("Desbalance de Corriente",rutaImagenDesbalanceCorriente)
                ImagenDesbalanceCorriente.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaDesbalanceDistrVoltaje=Data["Desbalance"]["DesbalanceDistrVoltaje"]
                ImagenDesbalanceDistrVoltaje=Imagenes("Distribución Desbalance de Voltaje",rutaDesbalanceDistrVoltaje)
                ImagenDesbalanceDistrVoltaje.ConstruirImagen()
            with st.container():
                rutaDesbalanceDistrCorriente=Data["Desbalance"]["DesbalanceDistrCorriente"]
                ImagenDesbalanceDistrCorriente=Imagenes("Distribución Desbalance de Corriente",rutaDesbalanceDistrCorriente)
                ImagenDesbalanceDistrCorriente.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaTablaDescriptivasDesbalanceV=Data["Desbalance"]["DesbalanceTablaDescriptivaVoltaje"]
                TablaDescriptivasDesbalanceV=Tabla("Estadísticos Descriptivos de Desbalances Voltaje",rutaTablaDescriptivasDesbalanceV)
                TablaDescriptivasDesbalanceV.construirContenedor()
            with st.container():
                rutaTablaDescriptivasDesbalanceC=Data["Desbalance"]["DesbalanceTablaDescriptivaCorriente"]
                TablaDescriptivasDesbalanceC=Tabla("Estadísticos Descriptivos de Desbalances Corriente",rutaTablaDescriptivasDesbalanceC)
                TablaDescriptivasDesbalanceC.construirContenedor()

with st.container():
    st.subheader("Frecuencia")
    with st.expander(label=""):
        
        with st.container():
            rutaImagenFrecuencia=Data["Frecuencia"]["FrecuenciaSerieTiempo"]
            ImagenFrecuencia=Imagenes("Frecuencia Serie de Tiempo",rutaImagenFrecuencia)
            ImagenFrecuencia.ConstruirImagen()
        with st.container():
            rutaImagenFrecuenciaDistr=Data["Frecuencia"]["FrecuenciaDistr"]
            ImagenFrecuenciaDistr=Imagenes("Distribución de Frecuencia",rutaImagenFrecuenciaDistr)
            ImagenFrecuenciaDistr.ConstruirImagen()
        with st.container():
            rutaTablaDescriptivasFrecuencia=Data["Frecuencia"]["FrecuenciaTabla"]
            TablaDescriptivasFrecuencia=Tabla("Estadísticos Descriptivos de Frecuencia",rutaTablaDescriptivasFrecuencia)
            TablaDescriptivasFrecuencia.construirContenedor()         

with st.container():
    st.subheader("Flicker")
    with st.expander(label=""):
        with st.container(horizontal=True):
            with st.container():
                rutaImagenFlickerPst=Data["Flicker"]["FlickerPstSerieTiempo"]
                ImagenFlickerPst=Imagenes("Flicker Pst Serie de Tiempo",rutaImagenFlickerPst)
                ImagenFlickerPst.ConstruirImagen()
            with st.container():
                rutaImagenFlickerPlt=Data["Flicker"]["FlickerPltSerieTiempo"]
                ImagenFlickerPlt=Imagenes("Flicker Plt Serie de Tiempo",rutaImagenFlickerPlt)
                ImagenFlickerPlt.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaImagenFlickerPstDistr=Data["Flicker"]["FlickerDistrPst"]
                ImagenFlickerPstDistr=Imagenes("Distribución Flicker Pst",rutaImagenFlickerPstDistr)
                ImagenFlickerPstDistr.ConstruirImagen()
            with st.container():
                rutaImagenFlickerPltDistr=Data["Flicker"]["FlickerDistrPlt"]
                ImagenFlickerPltDistr=Imagenes("Distribución Flicker Plt",rutaImagenFlickerPltDistr)
                ImagenFlickerPltDistr.ConstruirImagen()   
        with st.container(horizontal=True):
            with st.container():
                rutaTablaDescriptivasFlicker=Data["Flicker"]["FlickerTablaPst"]
                TablaDescriptivasFlicker=Tabla("Estadísticos Descriptivos Pst",rutaTablaDescriptivasFlicker)
                TablaDescriptivasFlicker.construirContenedor()
            with st.container():
                rutaTablaCumplimientoFlicker=Data["Flicker"]["FlickerTablaPlt"]
                TablaCumplimientoFlicker=Tabla("Estadísticos Descriptivos Plt",rutaTablaCumplimientoFlicker)
                TablaCumplimientoFlicker.construirContenedor()
with st.container():
    st.subheader("Armonicos Voltaje")
    with st.expander(label=""):
        
        with st.container():
            rutaImagenTHDVoltaje=Data["ArmonicosVoltaje"]["ArmonicosTiempo"]
            ImagenTHDVoltaje=Imagenes("THD Voltaje Serie de Tiempo",rutaImagenTHDVoltaje)
            ImagenTHDVoltaje.ConstruirImagen()
        with st.container():
            rutaImagenTHDVoltajeDistr=Data["ArmonicosVoltaje"]["ArmonicosDistr"]
            ImagenTHDVoltajeDistr=Imagenes("THD Voltaje Distribución",rutaImagenTHDVoltajeDistr)
            ImagenTHDVoltajeDistr.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaImagenTHDVoltajeDistrL1=Data["ArmonicosVoltaje"]["ArmonicosL1"]
                ImagenTHDVoltajeDistrL1=Imagenes("THD Voltaje L1",rutaImagenTHDVoltajeDistrL1)
                ImagenTHDVoltajeDistrL1.ConstruirImagen()
            with st.container():
                rutaImagenTHDVoltajeDistrL2=Data["ArmonicosVoltaje"]["ArmonicosL2"]
                ImagenTHDVoltajeDistrL2=Imagenes("THD Voltaje L2",rutaImagenTHDVoltajeDistrL2)
                ImagenTHDVoltajeDistrL2.ConstruirImagen()
            with st.container():
                rutaImagenTHDVoltajeDistrL3=Data["ArmonicosVoltaje"]["ArmonicosL3"]
                ImagenTHDVoltajeDistrL3=Imagenes("THD Voltaje L3",rutaImagenTHDVoltajeDistrL3)
                ImagenTHDVoltajeDistrL3.ConstruirImagen()
        with st.container():
            rutaTablaDescriptivasTHDVoltaje=Data["ArmonicosVoltaje"]["ArmonicosTabla"]
            TablaDescriptivasTHDVoltaje=Tabla("Estadísticos Descriptivos THD Voltaje",rutaTablaDescriptivasTHDVoltaje)
            TablaDescriptivasTHDVoltaje.construirContenedor()
with st.container():
    st.subheader("Armonicos Corriente")
    with st.expander(label=""):
        
        with st.container():
            rutaImagenTHDCorriente=Data["ArmonicosCorriente"]["ArmonicosITiempo"]
            ImagenTHDCorriente=Imagenes("THD Corriente Serie de Tiempo",rutaImagenTHDCorriente)
            ImagenTHDCorriente.ConstruirImagen()
        with st.container():
            rutaImagenTHDCorrienteDistr=Data["ArmonicosCorriente"]["ArmonicosIDistr"]
            ImagenTHDCorrienteDistr=Imagenes("THD Corriente Distribución",rutaImagenTHDCorrienteDistr)
            ImagenTHDCorrienteDistr.ConstruirImagen()
        with st.container(horizontal=True):
            with st.container():
                rutaImagenTHDCorrienteDistrL1=Data["ArmonicosCorriente"]["ArmonicosIL1"]
                ImagenTHDCorrienteDistrL1=Imagenes("THD Corriente L1",rutaImagenTHDCorrienteDistrL1)
                ImagenTHDCorrienteDistrL1.ConstruirImagen()
            with st.container():
                rutaImagenTHDCorrienteDistrL2=Data["ArmonicosCorriente"]["ArmonicosIL2"]
                ImagenTHDCorrienteDistrL2=Imagenes("THD Corriente L2",rutaImagenTHDCorrienteDistrL2)
                ImagenTHDCorrienteDistrL2.ConstruirImagen()
            with st.container():
                rutaImagenTHDCorrienteDistrL3=Data["ArmonicosCorriente"]["ArmonicosIL3"]
                ImagenTHDCorrienteDistrL3=Imagenes("THD Corriente L3",rutaImagenTHDCorrienteDistrL3)
                ImagenTHDCorrienteDistrL3.ConstruirImagen()
        with st.container():
            rutaTablaDescriptivasTHDCorriente=Data["ArmonicosCorriente"]["ArmonicosITabla"]
            TablaDescriptivasTHDCorriente=Tabla("Estadísticos Descriptivos THD Corriente",rutaTablaDescriptivasTHDCorriente)
            TablaDescriptivasTHDCorriente.construirContenedor()

# --- 2. Editar Comentarios ---

    
# En una v2, estos valores por defecto vendrían de un .txt o .json en S3
st.subheader("Notas")
comentario_Notas = st.text_area(label="",value="El voltaje se mantiene...")
st.subheader("Tips")
comentario_Tips = st.text_area(label="",value="Se detectaron picos de armónicos...")
st.subheader("Importante")
comentario_Importante = st.text_area(label="",value= "Se recomienda la instalación de...")
st.subheader("Precacución")
comentario_Precaucion = st.text_area(label="",value= "Cuidado con...")
st.subheader("Advertencia")
comentario_Advertencia = st.text_area(label="",value= "Accion inmediata")

# --- 3. Generar PDF ---
st.header("Generar PDF")
    
if st.button("Generar PDF con comentarios actualizados"):
    with st.spinner("Generando PDF..."):
        Servicio.GuardarDatos(
            comentario_Notas,
            comentario_Tips,
            comentario_Importante,
            comentario_Precaucion,
            comentario_Advertencia
        )