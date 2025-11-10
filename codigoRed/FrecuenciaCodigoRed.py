import streamlit as st
from Modelos import Tabla,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def FrecuenciaCodigoRed():
    with st.container():

        rutaTablaDescriptivasFrecuencia=Datos["Frecuencia"]["FrecuenciaTabla"]
        TablaDescriptivasFrecuencia=Tabla("Descripción Frecuencia",rutaTablaDescriptivasFrecuencia)
        TablaDescriptivasFrecuencia.construirContenedor()

        rutaImagenFrecuencia=Datos["Frecuencia"]["FrecuenciaSerieTiempo"]
        ImagenFrecuencia=Imagenes("Frecuencia Serie de Tiempo",rutaImagenFrecuencia)
        ImagenFrecuencia.ConstruirImagen()

        rutaImagenFrecuenciaDistr=Datos["Frecuencia"]["FrecuenciaDistr"]
        ImagenFrecuenciaDistr=Imagenes("Distribución de Frecuencia",rutaImagenFrecuenciaDistr)
        ImagenFrecuenciaDistr.ConstruirImagen()

            