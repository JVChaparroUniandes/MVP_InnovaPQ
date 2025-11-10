import streamlit as st
from Modelos import Tabla,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def CorrientesCodigoRed():
    with st.container():
            rutaTablaDescriptivasCorriente=Datos["Corriente"]["CorrienteTablaDescriptiva"]
            TablaDescriptivasCorriente=Tabla("Descripción Corrientes RMS",rutaTablaDescriptivasCorriente)
            TablaDescriptivasCorriente.construirContenedor()
    with st.expander(label="Corrientes RMS"):
        with st.container():
            rutaImagenCorrienteRMSMaximo=Datos["Corriente"]["CorrienteRMSMaximo"]
            ImagenCorrienteRMSMaximo=Imagenes("Corrientes RMS Máximo",rutaImagenCorrienteRMSMaximo)
            ImagenCorrienteRMSMaximo.ConstruirImagen()
        with st.container():
            rutaImagenCorrienteRMSMinimo=Datos["Corriente"]["CorrienteRMSMinimo"]
            ImagenCorrienteRMSMinimo=Imagenes("Corrientes RMS Mínimo",rutaImagenCorrienteRMSMinimo)
            ImagenCorrienteRMSMinimo.ConstruirImagen()
            
        with st.container():
            rutaImagenCorrienteRMSPromedio=Datos["Corriente"]["CorrienteRMSPromedio"]
            ImagenCorrienteRMSPromedio=Imagenes("Corrientes RMS Promedio",rutaImagenCorrienteRMSPromedio)
            ImagenCorrienteRMSPromedio.ConstruirImagen()

    with st.expander(label="Distribución de corrientes"):

        rutaImagenDistribucionCorriente=Datos["Corriente"]["CorrienteDistr"]
        ImagenDistribucionCorriente=Imagenes("Distribución Corrientes",rutaImagenDistribucionCorriente)
        ImagenDistribucionCorriente.ConstruirImagen()
        