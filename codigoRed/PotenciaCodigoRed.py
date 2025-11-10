import streamlit as st
from Modelos import Tabla,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def PotenciaCodigoRed():
    with st.container():
        

        with st.container():
            rutaTablaDescriptivasPotencia=Datos["Potencia"]["PotenciaDescriptivas"]
            TablaDescriptivasPotencia=Tabla("Descripción Potencia",rutaTablaDescriptivasPotencia)
            TablaDescriptivasPotencia.construirContenedor()

        with st.expander(label="Potencia Activa"):
            rutaImagenPotenciaActiva=Datos["Potencia"]["PotenciaActiva"]
            ImagenPotenciaActiva=Imagenes("Potencia Activa",rutaImagenPotenciaActiva)
            ImagenPotenciaActiva.ConstruirImagen()

            rutaImagenDistribucionActiva=Datos["Potencia"]["PotenciaDistribucionActiva"]
            ImagenDistribucionActiva=Imagenes("Distribución Potencia Activa",rutaImagenDistribucionActiva)
            ImagenDistribucionActiva.ConstruirImagen()
        
            

        with st.expander(label="Potencia Reactiva"):
            rutaImagenPotenciaReactiva=Datos["Potencia"]["PotenciaReactiva"]
            ImagenPotenciaReactiva=Imagenes("Potencia Reactiva",rutaImagenPotenciaReactiva)
            ImagenPotenciaReactiva.ConstruirImagen()

            rutaImagenDistribucionReactiva=Datos["Potencia"]["PotenciaDistribucionReactiva"]
            ImagenDistribucionReactiva=Imagenes("Distribución Potencia Reactiva",rutaImagenDistribucionReactiva)
            ImagenDistribucionReactiva.ConstruirImagen()
            

        with st.expander(label="Potencia Aparente"):
            rutaImagenPotenciaAparente=Datos["Potencia"]["PotenciaAparente"]
            ImagenPotenciaAparente=Imagenes("Potencia Aparente",rutaImagenPotenciaAparente)
            ImagenPotenciaAparente.ConstruirImagen()

            rutaImagenDistribucionAparente=Datos["Potencia"]["PotenciaDistribucionAparente"]
            ImagenDistribucionAparente=Imagenes("Distribución Potencia Aparente",rutaImagenDistribucionAparente)
            ImagenDistribucionAparente.ConstruirImagen()


        with st.expander(label="Factor de Potencia"):
            rutaImagenFactorPotencia=Datos["Potencia"]["PotenciaFp"]
            ImagenFactorPotencia=Imagenes("Factor de Potencia",rutaImagenFactorPotencia)
            ImagenFactorPotencia.ConstruirImagen()

            rutaImagenDistribucionFp=Datos["Potencia"]["PotenciaDistribucionFp"]
            ImagenDistribucionFp=Imagenes("Distribución Factor de Potencia",rutaImagenDistribucionFp)
            ImagenDistribucionFp.ConstruirImagen()
            