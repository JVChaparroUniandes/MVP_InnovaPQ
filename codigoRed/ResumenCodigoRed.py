import streamlit as st
from Modelos import Tabla
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def ResumenCodigoRed():
    with st.container():
        st.subheader("Resumen de mediciones")
        
        with st.expander(label="Potencia activa"):
            rutaTablaResumenActiva=Datos["Resumen"]["ResumenActiva"]
            TablaResumenActiva=Tabla("Potencia activa",rutaTablaResumenActiva)
            TablaResumenActiva.construirContenedor()

        with st.expander(label="Potencia reactiva"):
            rutaTablaReactiva=Datos["Resumen"]["ResumenReactiva"]
            TablaResumenReactiva=Tabla("Potencia reactiva",rutaTablaReactiva)
            TablaResumenReactiva.construirContenedor()

        with st.expander(label="Potencia aparente"):
            rutaTablaAparente=Datos["Resumen"]["ResumenAparente"]
            TablaResumenAparente=Tabla("Potencia aparente",rutaTablaAparente)
            TablaResumenAparente.construirContenedor()

        with st.expander(label="Factor de potencia"):
            rutaTablaFP=Datos["Resumen"]["ResumenFP"]
            TablaResumenFP=Tabla("Factor de potencia",rutaTablaFP)
            TablaResumenFP.construirContenedor()

        with st.expander(label="THD"):
            rutaTablaTHD=Datos["Resumen"]["ResumenTHD"]
            TablaResumenTHD=Tabla("THD",rutaTablaTHD)
            TablaResumenTHD.construirContenedor()

        with st.expander(label="TDD"):
            rutaTablaTDD=Datos["Resumen"]["ResumenTDD"]
            TablaResumenTDD=Tabla("TDD",rutaTablaTDD)
            TablaResumenTDD.construirContenedor()

        with st.expander(label="Desbalance de voltaje"):
            rutaTablaDesVoltaje=Datos["Resumen"]["ResumenDesVoltaje"]
            TablaResumenDesVoltaje=Tabla("Desbalance de voltaje",rutaTablaDesVoltaje)
            TablaResumenDesVoltaje.construirContenedor()

        with st.expander(label="Desbalance de corriente"):
            rutaTablaDesCorriente=Datos["Resumen"]["ResumenDesCorriente"]
            TablaResumenDesCorriente=Tabla("Desbalance de corriente",rutaTablaDesCorriente)
            TablaResumenDesCorriente.construirContenedor()

        with st.expander(label="Voltajes RMS"):
            rutaTablaVProm=Datos["Resumen"]["ResumenVProm"]
            TablaResumenVProm=Tabla("Voltajes RMS",rutaTablaVProm)
            TablaResumenVProm.construirContenedor()

        with st.expander(label="Corrientes RMS"):
            rutaTablaCProm=Datos["Resumen"]["ResumenCProm"]
            TablaResumenCProm=Tabla("Corrientes RMS",rutaTablaCProm)
            TablaResumenCProm.construirContenedor()

        with st.expander(label="Flicker Pst"):
            rutaTablaFlickPst=Datos["Resumen"]["ResumenFlickPst"]
            TablaResumenFlickPst=Tabla("Flicker Pst",rutaTablaFlickPst)
            TablaResumenFlickPst.construirContenedor()

        with st.expander(label="Flicker Plt"):
            rutaTablaFlickPlt=Datos["Resumen"]["ResumenFlickPlt"]
            TablaResumenFlickPlt=Tabla("Flicker Plt",rutaTablaFlickPlt)
            TablaResumenFlickPlt.construirContenedor()

        with st.expander(label="Frecuencia"):
            rutaTablaFrecuencia=Datos["Resumen"]["ResumenFrecuencia"]
            TablaResumenFrecuencia=Tabla("Frecuencia",rutaTablaFrecuencia)
            TablaResumenFrecuencia.construirContenedor()
