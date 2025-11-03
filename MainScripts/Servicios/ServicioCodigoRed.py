import json

class Data:
    def LeerDatos(self):
        data=json.load(open('MainScripts/Servicios/DB_OrigenCodigoRed.json', 'r', encoding='utf-8'))
        return data
    
    def GuardarDatos(self,com1,com2,com3,com4,com5):
        datos={
            "ComentarioNotas":com1,
            "ComentarioTips":com2,
            "ComentarioImportante":com3,
            "ComentarioPrecaucion":com4,
            "ComentarioAdvertencia":com5
            }
        nombreArchivo='MainScripts/Servicios/DB_ComentariosCodigoRed.json'
        with open(nombreArchivo,'w', encoding='utf-8') as archivo:
            json.dump(datos,archivo,indent=4,ensure_ascii=False)
        
