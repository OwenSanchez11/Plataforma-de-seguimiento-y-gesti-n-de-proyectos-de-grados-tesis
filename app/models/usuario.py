from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_user: Optional[int] = None
    username: str 
    nombre: str
    apellido: str
    email: str
    documento: str

    
class UsuarioCrear(BaseModel):
    username: str 
    nombre: str
    apellido: str
    email: str
    documento: str
    contraseña: str
    
class UsuarioRespuesta(BaseModel):
    id_user: int


class ActualizarUsuario(BaseModel):
    username: str
    email: str
    contraseña: str