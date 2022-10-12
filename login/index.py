from pydantic import BaseModel
class Credenciales(BaseModel):
    name : str
    password : str
    
    class Config:
        schema_extra={
            "example":{
                "name":"cnoc",
                "password":"ClaroGT",
            }
        }

def Inicio(name,password):
    if name == "cnoc" and password == "ClaroGT":
        r='si'
        msj="SE INICIO SESION, AUTOMATICAMENTE"
        url="panel.html"
    else: 
        r='no'
        msj="VERIFICAR DATOS, VERIFICAR DATOS"
        url=""
    respuesta={"code":200,"inicio_sesion":r,"msj":msj,"url":url}
    return respuesta