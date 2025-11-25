from Servicio import Data
import json


Servicio=Data(folder="report1")
diccionario=Servicio.obtener_rutas_actualizadas()
print(json.dumps(diccionario, indent=2, ensure_ascii=False))
print(diccionario["ArmonicosCorriente"]["ArmonicosITabla"])
print(Servicio.descargar_archivo_s3(diccionario["ArmonicosCorriente"]["ArmonicosITabla"]))